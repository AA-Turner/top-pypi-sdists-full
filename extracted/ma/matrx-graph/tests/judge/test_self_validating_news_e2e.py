"""Runtime AI-judged test for the self-validating news workflow.

This is the **reference implementation** of the ``judge`` test tier, and it is a
thin shell on purpose: the work, the money decision, and the verification all
live in the platform's Proof Run system (``aidream/services/proof_runs/``), so
the identical check can be run from the terminal, from an API call, and from a
UI button — not only from pytest.

    uv run python -m aidream.services.proof_runs.cli run news_self_validating

What this test asserts is the system's own verdict: the ``news_self_validating``
check ran and every REQUIRED proof passed. Those proofs include provider
receipts read back out of the cost ledger, so a green run here is evidence that
real models were really called and really billed — not that a mock returned a
plausible string. See ``aidream/services/proof_runs/FEATURE.md``.

Cost: the gate decides. Most invocations REPLAY recorded payloads for free; the
cadence (``ops.proof_check.live_every_seconds``, six hours by default) and the
monthly ceiling (``proof_runs.monthly_spend_ceiling_usd``) decide when one costs
money. Nothing here schedules anything.

THE GATE DETERMINISM RULE
-------------------------
Every precondition below is evaluated at a fixed point — after this module loads
the repo ``.env`` itself — so this module's skip decision is IDENTICAL whether it
is collected alone or after a suite that happens to import ``aidream`` (which
loads ``.env`` as an import side effect). That ordering bug made this file skip
when run alone and run-and-fail when collected after an aidream suite; see
``scripts/check_test_gate_determinism.py``, which now fails the build on any test
whose gate reads process state it does not establish itself.
"""

from __future__ import annotations

import importlib.util
import os
from collections.abc import Iterator
from pathlib import Path

import pytest

# --- Deterministic environment -------------------------------------------
# Load the repo .env HERE, before any precondition is evaluated. Without this,
# whether these variables exist depends on whether some other test module
# imported aidream first — which made this file's skip decision depend on
# COLLECTION ORDER.
_REPO_ROOT = Path(__file__).resolve().parents[4]

if (_REPO_ROOT / ".env").is_file():
    from dotenv import load_dotenv

    load_dotenv(_REPO_ROOT / ".env")

#: Provider keys the workflow itself needs.
REQUIRED_ENV_VARS = ("ANTHROPIC_API_KEY", "NEWS_API_KEY", "BRAVE_SEARCH_API_KEY_PRO_AI")
#: The database this check reads its own receipts from — and the kind catalog
#: the workflow's output-kind checks resolve against. Without it the run would
#: still "work" while every kind check silently degraded to unverified, which is
#: how this test used to fail for a reason that had nothing to do with the news.
REQUIRED_DB_VARS = (
    "SUPABASE_MATRIX_HOST",
    "SUPABASE_MATRIX_PORT",
    "SUPABASE_MATRIX_USER",
    "SUPABASE_MATRIX_PASSWORD",
    "SUPABASE_MATRIX_DATABASE_NAME",
)
REQUIRED_PACKAGES = ("matrx_ai", "matrx_scraper", "aidream")


def _missing_env() -> list[str]:
    return [v for v in REQUIRED_ENV_VARS if not os.environ.get(v)]


def _missing_db_env() -> list[str]:
    return [v for v in REQUIRED_DB_VARS if not os.environ.get(v)]


def _missing_packages() -> list[str]:
    return [p for p in REQUIRED_PACKAGES if importlib.util.find_spec(p) is None]


_MISSING_ENV = _missing_env()
_MISSING_DB = _missing_db_env()
_MISSING_PACKAGES = _missing_packages()

pytestmark = [
    pytest.mark.skipif(
        bool(_MISSING_ENV),
        reason=f"Missing provider env vars: {_MISSING_ENV}",
    ),
    pytest.mark.skipif(
        bool(_MISSING_DB),
        reason=(
            f"Missing database env vars: {_MISSING_DB} — the proof run reads its own "
            f"provider receipts out of the cost ledger and resolves the kind catalog, "
            f"so it cannot run without a database."
        ),
    ),
    pytest.mark.skipif(
        bool(_MISSING_PACKAGES),
        reason=f"Missing packages: {_MISSING_PACKAGES}",
    ),
]


@pytest.fixture(scope="module", autouse=True)
def _wired_platform() -> Iterator[None]:
    """Register the database and wire the packages, exactly as startup does.

    The kind catalog (``kind_definition_manager``) is part of this: without it
    every ``output_kind`` check in the workflow degrades to "catalog unreachable"
    — a neutral verdict that is NOT a pass — and the run proves less than it
    claims. Wiring it is a precondition of the test, not an optional extra.
    """
    from matrx_graph.db import _registry
    from matrx_graph.kinds import invalidate_kind_catalog_cache

    previous_instances = dict(_registry._instances)
    invalidate_kind_catalog_cache()
    try:
        from matrx_orm import register_platform_db

        register_platform_db(
            "supabase_automation_matrix",
            package="matrx-graph judge tests",
            additional_schemas=["auth", "content_ir", "workflow", "ops", "chat"],
        )

        from aidream._generated.package_db_wiring import wire_package_db

        wire_package_db()

        # Production startup installs the canonical ORM-backed mandate resolver
        # before any workflow can execute.  This test owns its startup wiring,
        # so it must establish that same seam rather than depending on another
        # test module having imported it first.
        import aidream.services.mandates.package_mandates  # noqa: F401

        from matrx_graph.db import is_configured

        assert is_configured(), (
            "matrx-graph DB wiring did not take effect after wire_package_db(); the "
            "workflow's kind checks would all degrade to 'catalog unreachable'."
        )
        yield
    finally:
        # This live suite owns its injected manager instances. In particular,
        # leaving kind_definition_manager behind makes later unit suites resolve
        # their fabricated kind slugs against production, where workflow_io
        # enforcement correctly rejects them as unregistered.
        _registry._instances.clear()
        _registry._instances.update(previous_instances)
        invalidate_kind_catalog_cache()


async def test_self_validating_news_workflow_passes_judge() -> None:
    """The news check runs and every required proof passes.

    Live or replay is the GATE's call, not this test's — but either way a
    failure here means something real broke: in replay, the workflow's wiring;
    live, the wiring, the providers, the persistence, or the answer's truth.
    """
    from aidream.services.proof_runs import ProofRunRequest, run_proof_check

    result = await run_proof_check(
        None,
        ProofRunRequest(
            slug="news_self_validating",
            mode="auto",
            trigger_source="pytest",
            reason="pytest: packages/matrx-graph/tests/judge",
        ),
    )

    if not result.ran:
        pytest.skip(f"Proof gate declined to run: {result.gate_reason}")

    attestation = result.attestation
    assert attestation is not None, "A run that happened must carry an attestation."

    failed_proofs = [p for p in attestation.proofs if p.status == "failed"]
    detail = "\n".join(f"  - {p.id}: {p.detail}" for p in attestation.proofs)
    assert result.verdict == "pass", (
        f"news_self_validating {result.verdict.upper()} in {result.mode} mode "
        f"({attestation.strength}).\n"
        f"{attestation.summary}\n"
        f"Failed: {[p.id for p in failed_proofs]}\n"
        f"All proofs:\n{detail}\n"
        f"Run row: ops.proof_run id={result.run_id} "
        f"(inspect: uv run python -m aidream.services.proof_runs.cli show {result.run_id})"
    )
