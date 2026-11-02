"""Integration checks that CCR requests require a verified non-empty PR diff."""

from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.pipeline.actions.request_review import RequestReviewAction
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot


@pytest.mark.parametrize("files", [[], None], ids=["empty", "incomplete"])
def test_empty_or_unknown_diff_suppresses_ccr_request(files: list[str] | None) -> None:
    provider = Mock()
    expected_count = 0 if files == [] else 1
    metadata = PRMetadata(
        number=1,
        title="change",
        head_branch="feature",
        head_sha="head",
        base_branch="main",
        changed_files=expected_count,
    )
    provider.get_pr_metadata.side_effect = [metadata, metadata]
    provider.get_ref_sha.return_value = "base"
    provider.list_pr_files_complete.return_value = files
    snapshot = PRStateSnapshot(pr_number=1)

    result = RequestReviewAction().execute(provider, snapshot, DerivedState(snapshot))

    assert result.decision is ActionDecision.SKIP
    provider.request_reviewer.assert_not_called()


def test_unconfigured_pr_metadata_suppresses_ccr_request() -> None:
    provider = Mock()
    snapshot = PRStateSnapshot(pr_number=1)

    result = RequestReviewAction().execute(provider, snapshot, DerivedState(snapshot))

    assert result.decision is ActionDecision.SKIP
    provider.request_reviewer.assert_not_called()
