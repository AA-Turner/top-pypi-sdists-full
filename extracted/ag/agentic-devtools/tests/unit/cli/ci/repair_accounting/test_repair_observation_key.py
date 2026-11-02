"""Exhaustion fingerprints ignore ordering but detect changed actionable work."""

from dataclasses import replace
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.models import CheckRunStatus, ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot
from agentic_devtools.cli.ci.repair_accounting import repair_observation_key
from agentic_devtools.cli.ci.review_thread_state import ReviewThreadStates


def test_repair_observation_key_tracks_actionable_inventory() -> None:
    snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="head",
        ci_status="failing",
        ci_failed_checks=["lint"],
        review_state="CHANGES_REQUESTED",
        copilot_review_id=10,
        reviews=[ReviewInfo(10, "Copilot", "CHANGES_REQUESTED")],
        check_runs=[CheckRunStatus(1, "lint", "completed", "failure")],
    )
    provider = MagicMock()
    provider.list_review_comments.return_value = [ReviewCommentInfo(-1, "x", "body", "", source_review_id=10)]
    with patch(
        "agentic_devtools.cli.ci.repair_accounting.fetch_review_thread_states",
        return_value=ReviewThreadStates(states={}),
    ):
        original = repair_observation_key(provider, snapshot)
        assert original == repair_observation_key(provider, snapshot)
        assert original != repair_observation_key(provider, replace(snapshot, head_sha="new"))
        assert original != repair_observation_key(provider, replace(snapshot, copilot_review_id=11))
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair._declared_suppressed_counts_by_review",
            return_value={10: 2},
        ):
            assert original != repair_observation_key(provider, snapshot)
        provider.list_review_comments.return_value = []
        assert original != repair_observation_key(provider, snapshot)


def test_repair_observation_key_requires_known_thread_inventory() -> None:
    with (
        patch(
            "agentic_devtools.cli.ci.repair_accounting.fetch_review_thread_states",
            return_value=ReviewThreadStates(degraded=True),
        ),
        pytest.raises(RuntimeError, match="thread inventory"),
    ):
        repair_observation_key(MagicMock(), PRStateSnapshot(pr_number=42))
