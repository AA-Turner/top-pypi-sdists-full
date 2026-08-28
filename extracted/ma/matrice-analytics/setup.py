"""
Build configuration for matrice_analytics.

Version is injected via PACKAGE_VERSION environment variable (set by CI).
"""

# CICD retrigger: empty commits did not fire Dispatch B on this PR.

import logging
import os
import shutil
import subprocess
import sys
import sysconfig
from pathlib import Path

from setuptools import find_packages, setup
from setuptools.command.install import install as _install

_PTH_FILENAME = "matrice_analytics_ort_bootstrap.pth"


class install(_install):
    """Custom install command that drops the ORT bootstrap ``.pth`` at the
    site-packages root.

    ``setuptools.data_files`` is unreliable for ``.pth`` placement on
    Debian/Ubuntu (their pip patch prepends an extra ``/local`` to data
    install paths). Writing directly to ``sysconfig.get_path('purelib')``
    after the standard install runs avoids that quirk and works across
    distros.
    """

    def run(self):
        _install.run(self)
        src = Path(__file__).resolve().parent / _PTH_FILENAME
        if not src.is_file():
            return
        purelib = sysconfig.get_path("purelib")
        if not purelib:
            return
        dst = Path(purelib) / _PTH_FILENAME
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(src), str(dst))
            print(f"matrice_analytics: installed ORT bootstrap .pth at {dst}")
        except OSError as exc:
            print(f"matrice_analytics: failed to install .pth at {dst}: {exc}")


logger = logging.getLogger(__name__)

# Package configuration
PACKAGE_NAME = "matrice_analytics"
SOURCE_DIR = f"src/{PACKAGE_NAME}"


def get_version() -> str:
    """Get version from PACKAGE_VERSION environment variable."""
    version = os.environ.get("PACKAGE_VERSION", "0.0.0.dev0")
    logger.info("Building version: %s", version)
    return version


def ensure_py_typed():
    """Create py.typed marker file for PEP 561 compliance."""
    py_typed = Path(SOURCE_DIR) / "py.typed"
    if not py_typed.exists():
        py_typed.write_text("")
        logger.info("Created py.typed file")


def run_stub_generator():
    """Run stub generator script to create .pyi files."""
    script_path = Path(__file__).parent / "stub_generation.py"
    if not script_path.exists():
        logger.warning("Stub generator not found: %s", script_path)
        return

    logger.info("Running stub generator: %s", script_path)
    subprocess.run([sys.executable, str(script_path)], check=True)


# Build preparation
ensure_py_typed()
run_stub_generator()

# Setup
setup(
    name=PACKAGE_NAME,
    version=get_version(),
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    # Top-level bootstrap module loaded by site.py via the .pth file (see
    # data_files below). Lives OUTSIDE the matrice_analytics package so its
    # import does not trigger matrice_analytics/__init__.py (which would
    # eagerly import onnxruntime-using submodules and defeat the purpose).
    py_modules=["_matrice_ort_bootstrap"],
    include_package_data=True,
    package_data={
        # **/*.yaml ships the analytics app manifests (analytics/config/) —
        # without them AnalyticsEngine("<app>") finds no manifest in
        # pip-installed environments and the new flow silently never runs.
        PACKAGE_NAME: ["py.typed", "*.pyi", "**/*.pyi", "**/*.yaml"],
    },
    # .pth placement is handled by the custom `install` cmdclass below
    # because Debian's pip patches data_files into an unwanted /local prefix.
    cmdclass={"install": install},
    zip_safe=False,
    python_requires=">=3.8",
)
