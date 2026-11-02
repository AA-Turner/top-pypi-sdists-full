"""Tests for provider-outcome compatibility wrappers."""

from __future__ import annotations

from typing import Any

from agentic_devtools.cli.ci.github_provider import (
    classify_reconciliation_outcome as classify_via_github_provider,
)
from agentic_devtools.cli.ci.github_provider import is_trusted_inaccessible_evidence as inaccessible_via_github_provider
from agentic_devtools.cli.ci.reconciliation.provider_outcomes import (
    classify_reconciliation_outcome,
    is_trusted_inaccessible_evidence,
)


def test_reconciliation_wrapper_uses_github_provider_classification() -> None:
    kwargs: dict[str, Any] = {
        "record_found": False,
        "partial_evidence": False,
        "terminal_state": False,
        "inaccessible_evidence": {"reason": "deleted", "source": "graphql"},
        "provider_status_code": 503,
        "authorization_outage": False,
    }
    assert classify_reconciliation_outcome(**kwargs) == classify_via_github_provider(**kwargs)


def test_inaccessible_evidence_wrapper_uses_github_provider_function() -> None:
    evidence = {"reason": "removed", "source": "api"}
    assert is_trusted_inaccessible_evidence(evidence) == inaccessible_via_github_provider(evidence)
