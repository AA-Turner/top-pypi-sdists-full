"""
Build configuration for matrice_analytics.

Version is injected via PACKAGE_VERSION environment variable (set by CI).
"""

import logging
import os
import subprocess
import sys
from pathlib import Path

from setuptools import find_packages, setup

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
    include_package_data=True,
    package_data={
        PACKAGE_NAME: ["py.typed", "*.pyi", "**/*.pyi"],
    },
    zip_safe=False,
    python_requires=">=3.8",
)
