"""Pytest wrapper for `scripts/e2e_smoke.py`.

The smoke harness itself is a standalone script — runnable interactively
via `uv run python scripts/e2e_smoke.py`. This wrapper exposes it under
pytest so CI can invoke it with `pytest -k e2e`.

Skip semantics: without `ANTHROPIC_API_KEY` the harness exits 2 (not 0,
not 1) to distinguish "not configured for live test" from "live test
failed." This wrapper mirrors that: it skips when the key is absent so
developer-laptop `pytest -q` runs don't burn API credit by default.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "e2e_smoke.py"


@pytest.mark.e2e
def test_e2e_smoke_harness() -> None:
    """Run the E2E smoke harness against the real Anthropic API.

    Skipped when `ANTHROPIC_API_KEY` is unset. Otherwise invokes the
    script as a subprocess and asserts exit 0 — the script writes its
    own diagnostics (`.e2e-results/<ts>/summary.md`) that the developer
    consults on failure.

    Model selection (v0.1.10): defaults to Sonnet 4.6 (cheap,
    indistinguishable quality from Opus on this fixture per the
    v0.1.6-0.1.9 shakedown reports). `EFTERLEV_E2E_MODEL` overrides —
    useful for tracking regressions on a specific model or for local
    devs who want Opus-quality runs. Per-CI-run cost on Sonnet against
    the harness fixture is ~$0.30-0.50; Opus runs ~$2-3.
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        pytest.skip("ANTHROPIC_API_KEY unset -- E2E smoke harness requires a real API key")

    # 2026-05-09: default switched from claude-sonnet-4-6 to claude-haiku-4-5
    # after Sonnet's CI PR flake rate hit ~50% (output-validate-fail in
    # gap / document agents under load, not a real efterlev regression).
    # Haiku 4.5 is faster and the v0.2 eval-harness baseline showed
    # reliable M1 / M5 = 1.0 on it. Override via EFTERLEV_E2E_MODEL.
    model = os.environ.get("EFTERLEV_E2E_MODEL", "claude-haiku-4-5")
    proc = subprocess.run(
        ["uv", "run", "python", str(SCRIPT), "--llm-model", model],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, (
        f"e2e_smoke.py exited {proc.returncode} (model={model}).\n"
        f"--- stderr ---\n{proc.stderr}\n"
        "See .e2e-results/<timestamp>/summary.md for the full report."
    )
