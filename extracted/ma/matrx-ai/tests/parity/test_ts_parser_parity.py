"""CI face of the Python <-> TypeScript block-splitter parity gate.

The Stage-1 gate for the kinds program: Python is about to become the canonical
resolver of agent output into kinds for the workflow system, so a detection
difference between the two runtimes is silently different results per surface.

The frontend is the richer, currently-live implementation — a difference is a
Python defect until a finding says otherwise (see EXPECTED_DIVERGENT_FIXTURES).

Skips LOUDLY when the sibling matrx-frontend checkout or node is unavailable:
an unverifiable gate must never read as a passing one.

**In CI the skip itself is the failure.** A skipped parity run is indistinguishable
from a green one in a summary table, so the ``kinds-parity`` job in
``.github/workflows/test.yml`` sets ``MATRX_PARITY_REQUIRED=1`` and every path that
would skip fails instead. Locally the variable is unset and the loud skip stands.
"""

from __future__ import annotations

import os

import pytest

from .harness import (
    EXPECTED_DIVERGENT_FIXTURES,
    BridgeUnavailable,
    compare_all,
    fixtures,
    frontend_root,
)


def _unverified(reason: str):
    """Skip locally, FAIL where the run was declared enforcing.

    ``MATRX_PARITY_REQUIRED=1`` is set by the CI job that provisions the sibling
    checkout and node. There, "could not run" is a broken gate, not an excuse.
    """
    message = f"PARITY UNVERIFIED: {reason}"
    if os.environ.get("MATRX_PARITY_REQUIRED") == "1":
        pytest.fail(
            f"{message}\n\nMATRX_PARITY_REQUIRED=1 — this run was declared enforcing, "
            "so an unverifiable parity gate is a FAILING one. Fix the sibling "
            "matrx-frontend checkout / node setup in the job; never relax this flag."
        )
    pytest.skip(message)


@pytest.fixture(scope="module")
def parity_results():
    fe = frontend_root()
    if fe is None:
        _unverified(
            "matrx-frontend not found — set MATRX_FRONTEND_ROOT or check out the "
            "sibling repo. This is NOT a passing parity gate."
        )
    try:
        return compare_all(fixtures(), fe)
    except BridgeUnavailable as exc:
        _unverified(f"TS bridge could not run — {exc}")


def test_fixture_corpus_is_not_empty() -> None:
    assert fixtures(), "the parity corpus is empty — the gate would pass vacuously"


@pytest.mark.parametrize("fixture_path", fixtures(), ids=lambda p: p.name)
def test_python_matches_typescript(fixture_path, parity_results) -> None:
    diffs = parity_results[fixture_path.name]
    reason = EXPECTED_DIVERGENT_FIXTURES.get(fixture_path.name)

    if reason is None:
        assert not diffs, "Python/TypeScript splitter drift:\n" + "\n".join(
            d.render() for d in diffs
        )
        return

    assert diffs, (
        f"{fixture_path.name} is recorded as a KNOWN divergence but the two "
        f"runtimes now agree. Re-decide the finding and remove the entry "
        f"deliberately — do not delete it to make this pass.\nRecorded: {reason}"
    )
