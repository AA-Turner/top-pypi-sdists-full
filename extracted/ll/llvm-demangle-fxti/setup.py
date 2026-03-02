# setup.py

import re
import shutil
import platform
from pathlib import Path
from setuptools import setup, find_packages, Extension

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

PACKAGE_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Discover all vendored LLVM versions (vendor/llvm11, vendor/llvm12, …)
# ---------------------------------------------------------------------------
vendor_root = this_directory / "vendor"
vendor_versions = sorted(
    int(d.name[4:])  # strip "llvm" prefix
    for d in vendor_root.iterdir()
    if d.is_dir() and re.fullmatch(r"llvm\d+", d.name)
) if vendor_root.is_dir() else []

if not vendor_versions:
    import sys
    print(
        "Error: No vendored LLVM directories found under vendor/\n"
        "Run: python vendor_llvm.py --llvm-version <N>",
        file=sys.stderr,
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# Platform-specific compiler flags (shared across all backends)
# ---------------------------------------------------------------------------
if platform.system() == "Windows":
    base_compile_args = ["/std:c++17", "/EHsc"]
else:
    base_compile_args = ["-std=c++17", "-fPIC"]

extra_link_args = []
if platform.system() == "Darwin":
    base_compile_args.append("-stdlib=libc++")
    extra_link_args.append("-stdlib=libc++")

# ---------------------------------------------------------------------------
# Generate one Extension per vendored LLVM version
# ---------------------------------------------------------------------------
pyx_template = this_directory / "src" / "llvmdemangle" / "demangle.pyx"
extensions = []

for v in vendor_versions:
    vendor_dir = vendor_root / f"llvm{v}"
    vendor_include = vendor_dir / "include"
    vendor_lib = vendor_dir / "lib" / "Demangle"
    llvm_sources = sorted(str(p) for p in vendor_lib.glob("*.cpp"))

    # Copy demangle.pyx → _backend_<v>.pyx (Cython needs distinct filenames)
    backend_pyx = this_directory / "src" / "llvmdemangle" / f"_backend_{v}.pyx"
    shutil.copy2(pyx_template, backend_pyx)

    compile_args = list(base_compile_args)
    if platform.system() == "Windows":
        compile_args.append(f"/DLLVM_MAJOR={v}")
    else:
        compile_args.append(f"-DLLVM_MAJOR={v}")

    extensions.append(
        Extension(
            f"llvmdemangle._backend_{v}",
            sources=[str(backend_pyx)] + llvm_sources,
            language="c++",
            include_dirs=[str(vendor_include), "src/llvmdemangle"],
            extra_compile_args=compile_args,
            extra_link_args=extra_link_args,
            depends=["src/llvmdemangle/demangle_shim.h"],
            define_macros=[("Py_LIMITED_API", "0x03060000")],
            py_limited_api=True,
        ),
    )

setup(
    name="llvm-demangle-fxti",
    version=PACKAGE_VERSION,
    description="Python bindings for the LLVM Demangle library, with vendored LLVM source.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="0BSD AND Apache-2.0 WITH LLVM-exception",
    author="FXTi",
    author_email="fx.ti@outlook.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/FXTi/llvmdemangle/tree/master",
    keywords="demangling c++ cxx cpp llvm",
    ext_modules=extensions,
    python_requires=">=3.6",
    options={"bdist_wheel": {"py_limited_api": "cp36"}},
)
