"""Build management for emake."""

import glob
import shutil
import sys
from pathlib import Path

from .venv import VirtualEnvironment


def build_sdist(venv: VirtualEnvironment) -> None:
    """Build a source distribution.

    Args:
        venv: VirtualEnvironment instance.
    """
    if not venv.exists:
        print(
            "Error: Virtual environment not found. Run 'emake requirements' first.",
            file=sys.stderr,
        )
        sys.exit(1)

    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)

    print("Building sdist...")
    if venv.run("-um", "build", "--sdist").returncode:
        raise RuntimeError("sdist build failed")

    print("sdist built successfully")


def clean() -> None:
    """Remove build artifacts."""
    print("Cleaning build artifacts...")

    # Directories to remove
    dirs_to_remove = ["build", "dist", ".venv", "wheelhouse"]
    for d in dirs_to_remove:
        path = Path(d)
        if path.exists():
            shutil.rmtree(path)

    # Files to remove
    files_to_remove = glob.glob("*.egg-info")
    for f in files_to_remove:
        path = Path(f)
        if path.exists():
            shutil.rmtree(path)

    # Additional patterns
    for pattern in ["*.build", "*.dist"]:
        for f in glob.glob(pattern):
            path = Path(f)
            if path.exists():
                shutil.rmtree(path)

    # Clean pycache
    for d in Path(".").rglob("__pycache__"):
        shutil.rmtree(d)

    for f in Path(".").rglob("*.pyc"):
        f.unlink()

    print("Clean complete")
