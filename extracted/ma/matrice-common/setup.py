"""
Mypyc-compiled build configuration for matrice_common.

This setup.py can build in two modes:
- With mypyc: Compiles Python to native extensions (faster, platform-specific wheels)
- Without mypyc: Pure Python package (cross-platform, slower)

Set ENABLE_MYPYC=true environment variable to enable mypyc compilation.
"""

import logging
import os
import subprocess
import sys
from pathlib import Path

from setuptools import find_packages, setup

logger = logging.getLogger(__name__)

# Package configuration
PACKAGE_NAME = "matrice_common"
SOURCE_DIR = f"src/{PACKAGE_NAME}"


# Check if mypyc compilation is enabled.
# Falls back to build-config.json if env var is not set.
def _resolve_enable_mypyc() -> bool:
    env_val = os.environ.get("ENABLE_MYPYC")
    if env_val is not None:
        return env_val.lower() in ("true", "1", "yes")
    config_path = Path(__file__).parent / "build-config.json"
    if config_path.exists():
        import json

        try:
            with open(config_path) as f:
                config = json.load(f)
            return bool(config.get("build", {}).get("enable_mypyc", False))
        except Exception:
            pass
    return False


ENABLE_MYPYC = _resolve_enable_mypyc()


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


def discover_modules() -> "list[str]":
    """Discover Python modules for mypyc compilation."""
    src_root = Path(SOURCE_DIR)
    if not src_root.exists():
        return []

    exclude = {"__pycache__", "tests", "test", "docs"}
    modules = []

    for path in src_root.rglob("*.py"):
        if any(part in exclude for part in path.parts):
            continue
        modules.append(str(path).replace("\\", "/"))

    logger.info("Discovered %s Python files for mypyc compilation", len(modules))
    return modules


def get_ext_modules():
    """Get extension modules - mypyc compiled or empty for pure Python."""
    if not ENABLE_MYPYC:
        logger.info("Building PURE PYTHON package (mypyc disabled)")
        return []

    logger.info("Building MYPYC COMPILED package")
    from mypyc.build import mypycify

    mypyc_options = [
        "--follow-imports=skip",
        "--ignore-missing-imports",
    ]
    return mypycify(mypyc_options + discover_modules(), opt_level="3")


# Build preparation
ensure_py_typed()
run_stub_generator()

# Setup
setup(
    name=PACKAGE_NAME,
    version=get_version(),
    package_dir={"": "src"},
    # Only ship the matrice_common package; exclude any orphan top-level
    # packages or template scaffolding that may exist under src/.
    packages=find_packages(where="src", include=[PACKAGE_NAME, f"{PACKAGE_NAME}.*"]),
    include_package_data=True,
    package_data={
        PACKAGE_NAME: ["py.typed", "*.pyi", "**/*.pyi"],
    },
    ext_modules=get_ext_modules(),
    zip_safe=False,
    python_requires=">=3.8",
)
