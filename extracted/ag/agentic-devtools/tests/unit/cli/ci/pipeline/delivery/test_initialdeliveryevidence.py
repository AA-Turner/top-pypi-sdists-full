"""Typed initial-delivery admission preserves the original recovery identity."""

from dataclasses import FrozenInstanceError

import pytest

from agentic_devtools.cli.ci.pipeline.delivery import InitialDeliveryEvidence, InitialDeliveryOutcome


def test_evidence_is_an_immutable_handoff_not_a_classifier():
    evidence = InitialDeliveryEvidence(InitialDeliveryOutcome.NO_DELIVERY, "task", "plan", "head")
    assert evidence.push_diagnostics == ""
    with pytest.raises(FrozenInstanceError):
        evidence.initial_task_id = "changed"
