from cx_Freeze import setup, Executable
import os
import sys

# Ensure the vcomp140.dll path is correct
vcomp140_dll_path = os.path.join(os.environ["WINDIR"], "System32", "vcomp140.dll")

# Build options
build_exe_options = {
    "packages": [
        "seaborn",
        "matplotlib",
        "numpy",
        "pandas",
        "scipy",
        "sklearn",
        "os",
        "multiprocessing",
        "pydeseq2",
    ],
    "include_files": [
        (vcomp140_dll_path, "dlls/vcomp140.dll"),
    ],
    "include_msvcr": True,  # Include Microsoft Visual C++ Redistributable DLLs
}

# Define the executable
executables = [Executable("rna_app.py")]

# Setup configuration
setup(
    name="RNASeqApp",
    version="0.0.1",
    description="RNA Sequencing Application",
    options={"build_exe": build_exe_options},
    executables=executables,
)
