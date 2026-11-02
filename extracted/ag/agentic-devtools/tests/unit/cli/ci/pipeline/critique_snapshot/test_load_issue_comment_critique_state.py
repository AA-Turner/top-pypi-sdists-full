from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.models import IssueCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.critique_snapshot import (
    CritiqueSnapshotFields,
    load_issue_comment_critique_state,
)
from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_NEW_CCR_NOT_APPROVED, CopilotGateVerdict
from agentic_devtools.cli.ci.retry import ProviderRateLimitError


def _load(*, failure: Exception | None = None) -> tuple[int | None, int | None, int | None, CritiqueSnapshotFields]:
    provider = MagicMock()
    comments = [IssueCommentInfo(1, "github-actions[bot]", "marker")]
    reviews = [ReviewInfo(12, "copilot[bot]", "COMMENTED", "", "head")]
    verdict = CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 12, body_comment_count=0)
    fields = CritiqueSnapshotFields(critique_headline_classification="critique")
    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.critique_snapshot.find_repair_satisfied_review_id",
            return_value=12,
        ),
        patch(
            "agentic_devtools.cli.ci.pipeline.critique_snapshot.find_suppressed_deferral_state",
            return_value=(11, 99),
        ),
        patch(
            "agentic_devtools.cli.ci.pipeline.critique_snapshot.load_critique_snapshot_fields",
            side_effect=failure,
            return_value=fields,
        ) as load_fields,
    ):
        result = load_issue_comment_critique_state(
            provider,
            42,
            comments,
            reviews,
            "head",
            verdict,
            "A concrete defect remains.",
            "critique",
            frozenset({"github-actions[bot]"}),
        )

    load_fields.assert_called_once()
    return result


def test_loads_markers_and_critique_fields() -> None:
    result = _load()

    assert result == (
        12,
        11,
        99,
        CritiqueSnapshotFields(critique_headline_classification="critique"),
    )


def test_preserves_markers_and_logs_when_critique_state_fails(caplog: pytest.LogCaptureFixture) -> None:
    result = _load(failure=ValueError("invalid critique marker"))

    assert result[:3] == (12, 11, 99)
    assert result[3] == CritiqueSnapshotFields(
        critique_headline_classification="critique",
        critique_task_state_available=False,
    )
    assert "Failed to load critique task state" in caplog.text


def test_preserves_markers_when_non_rate_limit_provider_error_occurs() -> None:
    result = _load(failure=ProviderRateLimitError(is_rate_limit=False))

    assert result[:3] == (12, 11, 99)


def test_reraises_provider_rate_limit_error() -> None:
    error = ProviderRateLimitError(retry_after_seconds=30)
    with pytest.raises(ProviderRateLimitError):
        _load(failure=error)
