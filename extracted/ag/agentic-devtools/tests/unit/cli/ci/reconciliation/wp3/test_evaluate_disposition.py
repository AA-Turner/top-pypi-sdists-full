import pytest

from agentic_devtools.cli.ci.reconciliation.wp3 import (
    Disposition,
    DispositionEvidence,
    evaluate_disposition,
)


def evidence(disposition: Disposition, *, code_changed: bool = False, text: str = "") -> DispositionEvidence:
    return DispositionEvidence(disposition, "f1", "head", "rev", True, code_changed, text)


@pytest.mark.parametrize(
    ("disposition", "candidate"),
    [
        (Disposition.IMPLEMENT_SUGGESTION, evidence(Disposition.IMPLEMENT_SUGGESTION, code_changed=True)),
        (Disposition.IMPLEMENT_BETTER_FIX, evidence(Disposition.IMPLEMENT_BETTER_FIX, code_changed=True)),
        (Disposition.REJECT_WITH_EVIDENCE, evidence(Disposition.REJECT_WITH_EVIDENCE, text="reproduced")),
        (
            Disposition.DEFER_WITH_FOLLOWUP,
            DispositionEvidence(Disposition.DEFER_WITH_FOLLOWUP, "f1", "head", "rev", True, followup_issue_id=1),
        ),
    ],
)
def test_accepts_four_verified_dispositions(disposition: Disposition, candidate: DispositionEvidence) -> None:
    result = evaluate_disposition(candidate, current_head_sha="head", current_source_revision="rev")
    assert result.accepted is True
    assert result.disposition is disposition


@pytest.mark.parametrize(
    "candidate",
    [
        DispositionEvidence(Disposition.DEFER_WITH_FOLLOWUP, "f1", "head", "rev", False),
        DispositionEvidence(Disposition.DEFER_WITH_FOLLOWUP, "f1", "old", "rev", True),
        DispositionEvidence(Disposition.DEFER_WITH_FOLLOWUP, "f1", "head", "rev", True, blocking=True),
        DispositionEvidence(Disposition.IMPLEMENT_SUGGESTION, "f1", "head", "rev", True),
        DispositionEvidence(Disposition.REJECT_WITH_EVIDENCE, "f1", "head", "rev", True),
    ],
)
def test_rejects_unsafe_disposition_evidence(candidate: DispositionEvidence) -> None:
    result = evaluate_disposition(candidate, current_head_sha="head", current_source_revision="rev")
    assert result.accepted is False


def test_rejects_malformed_and_invalid_inputs() -> None:
    with pytest.raises(TypeError):
        evaluate_disposition(object(), current_head_sha="head", current_source_revision="rev")  # type: ignore[arg-type]
    assert not evaluate_disposition(
        DispositionEvidence(Disposition.DEFER_WITH_FOLLOWUP, "", "head", "rev", True),
        current_head_sha="head",
        current_source_revision="rev",
    ).accepted
    assert not evaluate_disposition(
        DispositionEvidence(Disposition.DEFER_WITH_FOLLOWUP, "f1", "head", "rev", True, followup_issue_id=0),
        current_head_sha="head",
        current_source_revision="rev",
    ).accepted
