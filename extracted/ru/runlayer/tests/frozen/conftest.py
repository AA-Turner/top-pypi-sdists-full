"""Fixtures for the frozen-binary (Tier 2) hook-install tests.

These build the real PyInstaller onedir bundle once per session and hand the
``aiwatch`` exe to the tests, which run it as a subprocess. This is the only
tier that exercises ``resolve_hook_binary()`` (``sys.frozen`` / ``sys.executable``)
and proves the install path survives the bundle's excludes at runtime.

Slow (a full PyInstaller build) and opt-in: gated behind ``-m frozen_binary``
(registered in pyproject.toml, excluded from the default ``addopts``).
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

CLI_ROOT = Path(__file__).resolve().parents[2]
_EXE_SUFFIX = ".exe" if os.name == "nt" else ""


def _build_bundle(tmp_path_factory, *, spec: str, name: str) -> Path:
    """Build a PyInstaller onedir bundle once; return the path to its exe."""
    if shutil.which("uv") is None:
        pytest.skip("uv not available to build the frozen bundle")

    out = tmp_path_factory.mktemp(f"frozen_{name}")
    dist = out / "dist"
    work = out / "build"

    result = subprocess.run(
        [
            "uv",
            "run",
            "--with",
            "pyinstaller",
            "pyinstaller",
            "--noconfirm",
            "--distpath",
            str(dist),
            "--workpath",
            str(work),
            spec,
        ],
        cwd=CLI_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.fail(
            "pyinstaller build failed:\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    exe = dist / name / f"{name}{_EXE_SUFFIX}"
    if not exe.exists():
        pytest.fail(f"frozen bundle missing expected exe at {exe}")
    return exe


@pytest.fixture(scope="session")
def frozen_aiwatch(tmp_path_factory) -> Path:
    """Build the aiwatch onedir bundle once; return the path to the exe."""
    return _build_bundle(
        tmp_path_factory, spec="packaging/aiwatch.spec", name="aiwatch"
    )


@pytest.fixture(scope="session")
def frozen_runlayer(tmp_path_factory) -> Path:
    """Build the full runlayer CLI onedir bundle once; return the path to the exe."""
    return _build_bundle(
        tmp_path_factory, spec="packaging/runlayer.spec", name="runlayer"
    )
