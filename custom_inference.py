from pydeseq2.default_inference import DefaultInference
from joblib import parallel_backend, delayed, Parallel
import numpy as np
from pydeseq2 import utils
import pandas as pd
from scipy.optimize import minimize

from typing import Literal
from typing import Optional
from typing import Tuple


class CustomInference(DefaultInference):
    def lin_reg_mu(  # noqa: D102
        self,
        counts: np.ndarray,
        size_factors: np.ndarray,
        design_matrix: np.ndarray,
        min_mu: float,
    ) -> np.ndarray:
        with parallel_backend(self._backend):
            mu_hat_ = np.array(
                Parallel(
                    n_jobs=self.n_cpus,
                    verbose=self._joblib_verbosity,
                    batch_size=self._batch_size,
                )(
                    delayed(utils.fit_lin_mu)(
                        counts=counts[:, i],
                        size_factors=size_factors,
                        design_matrix=design_matrix,
                        min_mu=min_mu,
                    )
                    for i in range(counts.shape[1])
                )
            )
        return mu_hat_.T

    def irls(  # noqa: D102
        self,
        counts: np.ndarray,
        size_factors: np.ndarray,
        design_matrix: np.ndarray,
        disp: np.ndarray,
        min_mu: float,
        beta_tol: float,
        min_beta: float = -30,
        max_beta: float = 30,
        optimizer: Literal["BFGS", "L-BFGS-B"] = "L-BFGS-B",
        maxiter: int = 250,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        with parallel_backend(self._backend):

            res = Parallel(
                n_jobs=self.n_cpus,
                verbose=self._joblib_verbosity,
                batch_size=self._batch_size,
            )(
                delayed(utils.irls_solver)(
                    counts=counts[:, i],
                    size_factors=size_factors,
                    design_matrix=design_matrix,
                    disp=disp[i],
                    min_mu=min_mu,
                    beta_tol=beta_tol,
                    min_beta=min_beta,
                    max_beta=max_beta,
                    optimizer=optimizer,
                    maxiter=maxiter,
                )
                for i in range(counts.shape[1])
            )
        res = zip(*res)
        MLE_lfcs_, mu_hat_, hat_diagonals_, converged_ = (np.array(m) for m in res)

        return (
            MLE_lfcs_,
            mu_hat_.T,
            hat_diagonals_.T,
            converged_,
        )

    def alpha_mle(  # noqa: D102
        self,
        counts: np.ndarray,
        design_matrix: np.ndarray,
        mu: np.ndarray,
        alpha_hat: np.ndarray,
        min_disp: float,
        max_disp: float,
        prior_disp_var: Optional[float] = None,
        cr_reg: bool = True,
        prior_reg: bool = False,
        optimizer: Literal["BFGS", "L-BFGS-B"] = "L-BFGS-B",
    ) -> Tuple[np.ndarray, np.ndarray]:
        with parallel_backend(self._backend):
            res = Parallel(
                n_jobs=self.n_cpus,
                verbose=self._joblib_verbosity,
                batch_size=self._batch_size,
            )(
                delayed(utils.fit_alpha_mle)(
                    counts=counts[:, i],
                    design_matrix=design_matrix,
                    mu=mu[:, i],
                    alpha_hat=alpha_hat[i],
                    min_disp=min_disp,
                    max_disp=max_disp,
                    prior_disp_var=prior_disp_var,
                    cr_reg=cr_reg,
                    prior_reg=prior_reg,
                    optimizer=optimizer,
                )
                for i in range(counts.shape[1])
            )
        res = zip(*res)
        dispersions_, l_bfgs_b_converged_ = (np.array(m) for m in res)
        return dispersions_, l_bfgs_b_converged_

    def wald_test(  # noqa: D102
        self,
        design_matrix: np.ndarray,
        disp: np.ndarray,
        lfc: np.ndarray,
        mu: np.ndarray,
        ridge_factor: np.ndarray,
        contrast: np.ndarray,
        lfc_null: np.ndarray,
        alt_hypothesis: Optional[
            Literal["greaterAbs", "lessAbs", "greater", "less"]
        ] = None,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        num_genes = mu.shape[1]
        with parallel_backend(self._backend):

            res = Parallel(
                n_jobs=self.n_cpus,
                verbose=self._joblib_verbosity,
                batch_size=self._batch_size,
            )(
                delayed(utils.wald_test)(
                    design_matrix=design_matrix,
                    disp=disp[i],
                    lfc=lfc[i],
                    mu=mu[:, i],
                    ridge_factor=ridge_factor,
                    contrast=contrast,
                    lfc_null=lfc_null,  # Convert log2 to natural log
                    alt_hypothesis=alt_hypothesis,
                )
                for i in range(num_genes)
            )
        res = zip(*res)
        pvals, stats, se = (np.array(m) for m in res)

        return pvals, stats, se

    def dispersion_trend_gamma_glm(  # noqa: D102
        self, covariates: pd.Series, targets: pd.Series
    ) -> Tuple[np.ndarray, np.ndarray, bool]:
        covariates_w_intercept = covariates.to_frame()
        covariates_w_intercept.insert(0, "intercept", 1)
        covariates_fit = covariates_w_intercept.values
        targets_fit = targets.values

        def loss(coeffs):
            mu = covariates_fit @ coeffs
            return np.nanmean(targets_fit / mu + np.log(mu), axis=0)

        def grad(coeffs):
            mu = covariates_fit @ coeffs
            return -np.nanmean(
                ((targets_fit / mu - 1)[:, None] * covariates_fit) / mu[:, None], axis=0
            )

        try:
            res = minimize(
                loss,
                x0=np.array([1.0, 1.0]),
                jac=grad,
                method="L-BFGS-B",
                bounds=[(1e-12, np.inf)],
            )
        except RuntimeWarning:  # Could happen if the coefficients fall to zero
            return np.array([np.nan, np.nan]), np.array([np.nan, np.nan]), False

        coeffs = res.x
        return coeffs, covariates_fit @ coeffs, res.success

    def lfc_shrink_nbinom_glm(  # noqa: D102
        self,
        design_matrix: np.ndarray,
        counts: np.ndarray,
        size: np.ndarray,
        offset: np.ndarray,
        prior_no_shrink_scale: float,
        prior_scale: float,
        optimizer: str,
        shrink_index: int,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        with parallel_backend(self._backend):

            num_genes = counts.shape[1]
            res = Parallel(
                n_jobs=self.n_cpus,
                verbose=self._joblib_verbosity,
                batch_size=self._batch_size,
            )(
                delayed(utils.nbinomGLM)(
                    design_matrix=design_matrix,
                    counts=counts[:, i],
                    size=size[i],
                    offset=offset,
                    prior_no_shrink_scale=prior_no_shrink_scale,
                    prior_scale=prior_scale,
                    optimizer=optimizer,
                    shrink_index=shrink_index,
                )
                for i in range(num_genes)
            )
        res = zip(*res)
        lfcs, inv_hessians, l_bfgs_b_converged_ = (np.array(m) for m in res)
        return lfcs, inv_hessians, l_bfgs_b_converged_
