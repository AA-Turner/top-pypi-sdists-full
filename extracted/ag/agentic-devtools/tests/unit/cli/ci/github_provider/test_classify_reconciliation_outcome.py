"""Tests for GitHub reconciliation-outcome classification."""

from __future__ import annotations

from agentic_devtools.cli.ci.github_provider import (
    classify_reconciliation_outcome,
    is_trusted_inaccessible_evidence,
)
from agentic_devtools.cli.ci.reconciliation.models import ObservationOutcome


def test_inaccessible_evidence_requires_reason_and_source() -> None:
    assert is_trusted_inaccessible_evidence({"reason": "deleted", "source": "github"})
    assert not is_trusted_inaccessible_evidence({"reason": "deleted"})
    assert not is_trusted_inaccessible_evidence({"source": "github"})


def test_terminal_and_inaccessible_classification_have_precedence() -> None:
    assert (
        classify_reconciliation_outcome(record_found=True, terminal_state=True) == ObservationOutcome.TRUSTED_TERMINAL
    )
    assert (
        classify_reconciliation_outcome(
            record_found=False,
            inaccessible_evidence={"reason": "deleted", "source": "graphql"},
            provider_status_code=503,
        )
        == ObservationOutcome.TRUSTED_INACCESSIBLE
    )


def test_status_codes_map_to_rate_limit_transient_and_provider_failure() -> None:
    assert (
        classify_reconciliation_outcome(record_found=False, provider_status_code=429) == ObservationOutcome.RATE_LIMIT
    )
    assert (
        classify_reconciliation_outcome(record_found=False, provider_status_code=503)
        == ObservationOutcome.TRANSIENT_FAILURE
    )
    assert (
        classify_reconciliation_outcome(record_found=False, provider_status_code=500)
        == ObservationOutcome.PROVIDER_FAILURE
    )


def test_generic_failure_cannot_become_inaccessible_without_record_specific_evidence() -> None:
    assert (
        classify_reconciliation_outcome(
            record_found=False,
            inaccessible_evidence={"reason": " ", "source": ""},
            provider_status_code=500,
        )
        == ObservationOutcome.PROVIDER_FAILURE
    )


def test_partial_and_success_outcomes() -> None:
    assert classify_reconciliation_outcome(record_found=False) == ObservationOutcome.PARTIAL_EVIDENCE
    assert (
        classify_reconciliation_outcome(record_found=True, partial_evidence=True) == ObservationOutcome.PARTIAL_EVIDENCE
    )
    assert classify_reconciliation_outcome(record_found=True) == ObservationOutcome.TRUSTED_OBSERVATION


def test_authorization_outage_precedes_generic_failures() -> None:
    assert (
        classify_reconciliation_outcome(
            record_found=False,
            provider_status_code=503,
            authorization_outage=True,
        )
        == ObservationOutcome.AUTHORIZATION_OUTAGE
    )
