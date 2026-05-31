"""
Mypyc-compiled build configuration for matrice.

This setup.py can build in two modes:
- With mypyc: Compiles Python to native extensions (faster, platform-specific wheels)
- Without mypyc: Pure Python package (cross-platform, slower)

Set ENABLE_MYPYC=true environment variable to enable mypyc compilation.
"""

import os
import subprocess
import sys
from pathlib import Path

from setuptools import find_packages, setup

# Package configuration
PACKAGE_NAME = "matrice"
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
    print(f"Building version: {version}")
    return version


def ensure_py_typed():
    """Create py.typed marker file for PEP 561 compliance."""
    py_typed = Path(SOURCE_DIR) / "py.typed"
    if not py_typed.exists():
        py_typed.write_text("")
        print("Created py.typed file")


def run_stub_generator():
    """Run stub generator script to create .pyi files."""
    script_path = Path(__file__).parent / "stub_generation.py"
    if not script_path.exists():
        print(f"Warning: Stub generator not found: {script_path}")
        return

    print(f"Running stub generator: {script_path}")
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

    print(f"Discovered {len(modules)} Python files for mypyc compilation")
    return modules


def get_ext_modules():
    """Get extension modules - mypyc compiled or empty for pure Python."""
    if not ENABLE_MYPYC:
        print("Building PURE PYTHON package (mypyc disabled)")
        return []

    print("Building MYPYC COMPILED package")
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
    packages=find_packages(where="src"),
    include_package_data=True,
    package_data={
        PACKAGE_NAME: ["py.typed", "*.pyi", "**/*.pyi"],
    },
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
    },
    ext_modules=get_ext_modules(),
    zip_safe=False,
    python_requires=">=3.8",
)
