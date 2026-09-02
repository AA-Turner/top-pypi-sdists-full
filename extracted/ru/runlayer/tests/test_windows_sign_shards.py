"""Runtime smoke tests for Windows payload signing orchestration."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest


_ROOT = Path(__file__).parents[2]
_SIGN_SCRIPT = (
    _ROOT / ".github" / "actions" / "sign-windows-payload" / "sign-shards.ps1"
)
_SMOKE_SCRIPT = Path(__file__).with_name("sign_shards_smoke.ps1")
_PWSH = shutil.which("pwsh")

pytestmark = pytest.mark.skipif(_PWSH is None, reason="pwsh is not installed")


def test_sign_shards_process_orchestration() -> None:
    result = subprocess.run(
        [
            _PWSH or "pwsh",
            "-NoLogo",
            "-NoProfile",
            "-File",
            str(_SMOKE_SCRIPT),
            "-ProductionScript",
            str(_SIGN_SCRIPT),
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stdout + result.stderr
