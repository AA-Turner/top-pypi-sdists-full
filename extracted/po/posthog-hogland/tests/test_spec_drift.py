"""Drift gate.

Re-runs ``scripts/gen_models.py`` against the current ``openapi.yaml``
and diffs the result against the checked-in
``src/hogland/_generated/models.py``. If they don't match,
``openapi.yaml`` moved without somebody running ``task py:gen-models``.

The drift is the same kind of pin the Go side enforces via
``cmd/openapi-gen/regen_test.go`` — except the Go side asserts the
*spec* matches the handlers, and this asserts the *SDK models* match
the spec. Together they make the chain Go handlers → openapi.yaml →
hogland Python SDK tight.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

# tests/test_spec_drift.py → parents[0]=tests, [1]=python, [2]=sdk, [3]=repo root.
REPO_ROOT = Path(__file__).resolve().parents[3]
GEN_SCRIPT = REPO_ROOT / "sdk" / "python" / "scripts" / "gen_models.py"
COMMITTED = REPO_ROOT / "sdk" / "python" / "src" / "hogland" / "_generated" / "models.py"


_UV = shutil.which("uv")


@pytest.mark.skipif(
    _UV is None,
    reason="uv not on PATH — drift gate runs in CI, not in every local venv",
)
def test_generated_models_match_spec() -> None:
    """Re-run the generator and assert the output matches the committed file."""
    assert _UV is not None  # for the type checker; skipif guards the run
    backup = COMMITTED.read_bytes()
    try:
        result = subprocess.run(  # noqa: S603 — argv is fully controlled
            [
                _UV,
                "run",
                "--with",
                "pyyaml",
                "--with",
                "datamodel-code-generator[http]==0.57.0",
                "python",
                str(GEN_SCRIPT),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            pytest.fail(
                f"gen_models.py exited {result.returncode}\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
        fresh = COMMITTED.read_bytes()
    finally:
        # Always restore — don't let a stale generator clobber the
        # committed file when the test fails locally.
        COMMITTED.write_bytes(backup)

    if fresh != backup:
        pytest.fail(
            "hogland: _generated/models.py is out of date.\n"
            "Run: task py:gen-models\n"
            f"(Or: uv run --with pyyaml --with 'datamodel-code-generator[http]' "
            f"python {GEN_SCRIPT.relative_to(REPO_ROOT)})",
        )
