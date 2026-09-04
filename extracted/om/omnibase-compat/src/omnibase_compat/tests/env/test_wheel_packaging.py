# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# compat-skip-retention: test-only wheel packaging regression fixture

"""Wheel-build content-parity regression test (OMN-14636).

Workspace-mode wheel builds stage a git-stripped sibling copy of this repo
(``omnibase_infra/scripts/runtime_build/stage_workspace.sh`` rsyncs every
sibling without its ``.git`` directory). Hatchling's default wheel
file-selection always applies ``.gitignore`` as an exclude filter
(``BuilderConfig.exclude_spec`` loads it unconditionally unless
``ignore-vcs`` is set), independent of whether ``.git`` is present.

A bare, unanchored ``env/`` pattern in ``.gitignore`` (intended to ignore
virtualenv directories such as ``.venv/``/``venv/``/``env/``) matches ANY
directory literally named ``env`` at ANY depth -- including this package's
real, git-tracked ``src/omnibase_compat/env/`` submodule and its test
counterpart ``src/omnibase_compat/tests/env/``. That collision silently
dropped both from every workspace-mode wheel build even though the files
are genuinely git-tracked source, not build/venv artifacts.

This test builds a wheel from a git-stripped copy of the CURRENT working
tree (mirroring ``stage_workspace.sh``'s rsync-without-``.git`` staging)
and asserts the ``env`` submodule survives packaging.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest

# Repo root is four levels up from this test file:
# src/omnibase_compat/tests/env/test_wheel_packaging.py -> env/ -> tests/
# -> omnibase_compat/ -> src/ -> <repo_root>
REPO_ROOT = Path(__file__).resolve().parents[4]

_REQUIRED_WHEEL_MEMBERS = (
    "omnibase_compat/env/__init__.py",
    "omnibase_compat/env/util_is_strict_mode.py",
    "omnibase_compat/tests/env/__init__.py",
    "omnibase_compat/tests/env/test_is_strict_mode.py",
)

# `logs/` is a genuine .gitignore pattern (not one of hatchling's hardcoded
# EXCLUDED_DIRECTORIES like __pycache__/.venv/.git, which get pruned
# structurally regardless of .gitignore state). Using it as the canary
# proves exclude_spec (the .gitignore-driven filter) is genuinely active.
_GITIGNORE_CANARY = "omnibase_compat/logs/wheel_packaging_canary.log"


def _stage_git_stripped_copy(destination: Path) -> None:
    """Copy the working tree into ``destination`` with ``.git`` stripped.

    Deliberately placed as a SIBLING of ``REPO_ROOT`` -- NOT under a system
    temp directory (``tempfile.gettempdir()`` / pytest's ``tmp_path``).
    Hatchling's ``BuilderConfig.load_vcs_exclusion_patterns`` has a related
    quirk: it discards ALL ``.gitignore`` patterns outright if the absolute
    project root path happens to match one of them (it runs
    ``exclude_spec.match_file(self.root)`` against the raw absolute path).
    Staging under a platform temp dir (``/tmp/...`` on Linux CI runners)
    spuriously matches this repo's own unrelated ``tmp/`` ignore pattern and
    silently disables gitignore-based exclusion ENTIRELY -- which would make
    this test pass for the wrong reason (nothing excluded, including the
    dropped ``env/`` files) instead of proving the real fix.
    """
    ignore = shutil.ignore_patterns(".git", "dist", ".venv", "*.egg-info", "__pycache__")
    shutil.copytree(REPO_ROOT, destination, ignore=ignore)
    assert not (destination / ".git").exists(), "staged copy must not carry .git"


def _build_wheel(staged_root: Path) -> zipfile.ZipFile:
    uv_bin = shutil.which("uv")
    assert uv_bin is not None, "uv executable not found on PATH"
    dist_dir = staged_root / "dist"
    result = subprocess.run(
        [uv_bin, "build", "--wheel", "-o", str(dist_dir)],
        cwd=staged_root,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert result.returncode == 0, (
        f"uv build --wheel failed (rc={result.returncode}):\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    wheels = list(dist_dir.glob("*.whl"))
    assert len(wheels) == 1, f"expected exactly one built wheel, got {wheels}"
    return zipfile.ZipFile(wheels[0])


@pytest.mark.unit
@pytest.mark.timeout(180)
class TestWheelPackagingContent:
    def test_git_stripped_wheel_build_contains_env_module(self) -> None:
        """A git-stripped workspace-mode build must ship env/ + tests/env/."""
        staging_dir = REPO_ROOT.parent / f"omnibase_compat_wheel_stage_test_{os.getpid()}"
        if staging_dir.exists():
            shutil.rmtree(staging_dir)
        try:
            _stage_git_stripped_copy(staging_dir)

            # Canary: prove exclude_spec is genuinely active during this
            # build (not silently short-circuited to "include everything"
            # by the absolute-path quirk documented above), so a passing
            # env/-present assertion below is actually meaningful.
            canary_dir = staging_dir / "src" / "omnibase_compat" / "logs"
            canary_dir.mkdir(parents=True, exist_ok=True)
            (canary_dir / "wheel_packaging_canary.log").write_bytes(b"canary")

            with _build_wheel(staging_dir) as wheel:
                names = set(wheel.namelist())

            assert _GITIGNORE_CANARY not in names, (
                "logs/ canary survived packaging -- .gitignore-based "
                "exclusion is not active in this build; the env/-present "
                "assertion below would be meaningless. See "
                "BuilderConfig.load_vcs_exclusion_patterns absolute-path quirk."
            )

            missing = [m for m in _REQUIRED_WHEEL_MEMBERS if m not in names]
            assert not missing, (
                f"wheel is missing required env/ module files: {missing}\n"
                f"(OMN-14636 regression: bare .gitignore `env/` pattern "
                f"collides with the real src/omnibase_compat/env/ submodule)"
            )
        finally:
            shutil.rmtree(staging_dir, ignore_errors=True)
