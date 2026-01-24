#!/usr/bin/env python3
"""
Build standalone Anyscale CLI binary.

Creates a self-contained executable with PyInstaller that bundles the Python
interpreter and all dependencies. The binary is architecture-specific but
works across different Python runtime versions.

Usage:
    python3 build_standalone.py
"""

import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time


# Constants
CLI_DIR = Path(__file__).parent
PYINSTALLER_VERSION = "6.14.2"


def get_version():
    """
    Get version from version.py.

    This matches the PyPI package version (e.g., "0.0.0-dev" or "1.2.3").
    """
    version_file = CLI_DIR / "anyscale" / "version.py"
    content = version_file.read_text()
    match = re.search(r'__version__ = ["\']([^"\']+)["\']', content)
    if not match:
        sys.exit("Error: Could not find version in version.py")
    return match.group(1)


def build():
    """Build the standalone binary."""
    start_time = time.time()

    os.chdir(CLI_DIR)

    version = get_version()
    binary_name = f"anyscale-cli-{version}"

    print(f"Building {binary_name}")

    # Install PyInstaller and the anyscale package
    # Package version comes from version.py (no modification needed)
    print("Installing dependencies...")
    try:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--quiet",
                f"pyinstaller=={PYINSTALLER_VERSION}",
                ".",
            ]
        )
    except subprocess.CalledProcessError as e:
        sys.exit(f"Failed to install dependencies: {e}")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create symlinks for SDK modules that self-import
        # Generated OpenAPI client code imports itself as top-level modules
        # PyInstaller needs these to resolve imports like "from openapi_client import ..."
        try:
            os.symlink(
                CLI_DIR / "anyscale" / "client" / "openapi_client",
                Path(tmpdir) / "openapi_client",
            )
            os.symlink(
                CLI_DIR / "anyscale" / "sdk" / "anyscale_client",
                Path(tmpdir) / "anyscale_client",
            )
        except OSError as e:
            sys.exit(f"Failed to create symlinks: {e}")

        # Build with PyInstaller
        cmd = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",  # Create single executable file instead of directory
            "--name",
            binary_name,  # Output binary name
            "--clean",  # Clean cache before building
            "--collect-data",
            "anyscale",  # Include package data files (templates, configs, etc.)
            "--copy-metadata",
            "anyscale",  # Include package metadata for version detection
            "--paths",
            str(CLI_DIR.parent),  # Add search path for finding imports
            "--distpath",
            "dist",  # Output directory for built binary
            "--workpath",
            f"{tmpdir}/build",  # Temporary build directory
            "--specpath",
            tmpdir,  # Location for .spec file (build recipe)
            "anyscale/scripts.py",  # Entry point script
        ]

        # Prepend tmpdir to PYTHONPATH for symlink resolution
        # Keep existing PYTHONPATH so PyInstaller can find installed packages
        env = os.environ.copy()
        existing_pythonpath = env.get("PYTHONPATH", "")
        if existing_pythonpath:
            env["PYTHONPATH"] = f"{tmpdir}:{CLI_DIR.parent}:{existing_pythonpath}"
        else:
            env["PYTHONPATH"] = f"{tmpdir}:{CLI_DIR.parent}"

        try:
            subprocess.check_call(cmd, env=env)
        except subprocess.CalledProcessError as e:
            sys.exit(f"PyInstaller build failed: {e}")

    # Verify binary exists and works
    binary_path = Path("dist") / binary_name
    if not binary_path.exists():
        sys.exit(f"Binary was not created: {binary_path}")

    try:
        result = subprocess.run(
            [str(binary_path), "--version"], capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError as e:
        sys.exit(f"Binary verification failed: {e.stderr}")

    build_time = time.time() - start_time
    print(f"✓ Built: {binary_path} ({binary_path.stat().st_size / 1024 / 1024:.1f} MB)")
    print(f"✓ Version: {result.stdout.strip()}")
    print(f"✓ Build time: {build_time:.1f}s")

    # Return success for shell script
    return 0


if __name__ == "__main__":
    sys.exit(build())
