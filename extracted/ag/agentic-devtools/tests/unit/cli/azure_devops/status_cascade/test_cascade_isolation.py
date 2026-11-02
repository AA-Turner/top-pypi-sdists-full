"""Tests for execute_cascade per-thread error isolation."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.helpers import CrossIdentityForbiddenError
from agentic_devtools.cli.azure_devops.review_state import (
    FileEntry,
    FolderGroup,
    OverallSummary,
    ReviewState,
    ReviewStatus,
)
from agentic_devtools.cli.azure_devops.status_cascade import CascadeResult, PatchOperation, execute_cascade


def _make_config() -> AzureDevOpsConfig:
    return AzureDevOpsConfig(
        organization="https://dev.azure.com/myorg",
        project="MyProject",
        repository="MyRepo",
    )


def _make_op(thread_id: int = 10, comment_id: int = 20) -> PatchOperation:
    return PatchOperation(
        thread_id=thread_id,
        comment_id=comment_id,
        new_content="content",
        thread_status="closed",
    )


def _state_with_overall(thread_id: int, comment_id: int) -> ReviewState:
    fe = FileEntry(threadId=0, commentId=0, folder="src", fileName="a.py", status=ReviewStatus.APPROVED.value)
    return ReviewState(
        prId=42,
        repoId="repo-123",
        repoName="repo",
        project="proj",
        organization="https://dev.azure.com/org",
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00Z",
        overallSummary=OverallSummary(threadId=thread_id, commentId=comment_id),
        folders={"src": FolderGroup(files=["/src/a.py"])},
        files={"/src/a.py": fe},
        commitHash="4a8685bda246f3bf826efabaf990fe9c3d1da125",
        modelId="claude-opus-4.6",
    )


class TestCascadeIsolation:
    """Tests for execute_cascade per-thread 403 error isolation."""

    def test_returns_cascade_result(self):
        """Should return a CascadeResult object."""
        with (
            patch("agentic_devtools.cli.azure_devops.status_cascade.patch_comment") as mock_pc,
            patch("agentic_devtools.cli.azure_devops.status_cascade.patch_thread_status") as mock_pts,
        ):
            mock_pc.return_value = {}
            mock_pts.return_value = {}

            result = execute_cascade(
                patch_operations=[_make_op()],
                requests_module=MagicMock(),
                headers={},
                config=_make_config(),
                repo_id="repo-123",
                pull_request_id=42,
            )

        assert isinstance(result, CascadeResult)
        assert result.succeeded == [10]
        assert result.blocked == []
        assert result.fallen_back == []

    def test_403_does_not_abort_batch(self):
        """One 403 should fall back to a reply without aborting the batch."""
        call_count = {"pc": 0}

        def mock_pc_side_effect(**kwargs):
            call_count["pc"] += 1
            if kwargs["thread_id"] == 10:
                raise CrossIdentityForbiddenError(10, 20)
            return {}

        with (
            patch("agentic_devtools.cli.azure_devops.status_cascade.patch_comment") as mock_pc,
            patch("agentic_devtools.cli.azure_devops.status_cascade.patch_thread_status") as mock_pts,
            patch("agentic_devtools.cli.azure_devops.status_cascade.post_cross_identity_reply") as mock_reply,
        ):
            mock_pc.side_effect = mock_pc_side_effect
            mock_pts.return_value = {}
            mock_reply.return_value = {}

            result = execute_cascade(
                patch_operations=[_make_op(10, 20), _make_op(30, 40)],
                requests_module=MagicMock(),
                headers={},
                config=_make_config(),
                repo_id="repo-123",
                pull_request_id=42,
            )

        assert 10 in result.fallen_back
        assert 30 in result.succeeded
        assert result.blocked == []
        # Both ops were attempted
        assert mock_pc.call_count == 2
        mock_reply.assert_called_once()

    def test_all_succeed(self):
        """All operations succeed → all in succeeded list."""
        with (
            patch("agentic_devtools.cli.azure_devops.status_cascade.patch_comment") as mock_pc,
            patch("agentic_devtools.cli.azure_devops.status_cascade.patch_thread_status") as mock_pts,
        ):
            mock_pc.return_value = {}
            mock_pts.return_value = {}

            result = execute_cascade(
                patch_operations=[_make_op(10, 20), _make_op(30, 40)],
                requests_module=MagicMock(),
                headers={},
                config=_make_config(),
                repo_id="repo-123",
                pull_request_id=42,
            )

        assert result.succeeded == [10, 30]
        assert result.blocked == []

    def test_all_blocked(self):
        """All operations are blocked when both PATCH and fallback fail."""
        with (
            patch("agentic_devtools.cli.azure_devops.status_cascade.patch_comment") as mock_pc,
            patch("agentic_devtools.cli.azure_devops.status_cascade.patch_thread_status") as mock_pts,
            patch("agentic_devtools.cli.azure_devops.status_cascade.post_cross_identity_reply") as mock_reply,
        ):
            mock_pc.side_effect = CrossIdentityForbiddenError(0, 0)
            mock_pts.return_value = {}
            mock_reply.side_effect = RuntimeError("reply failed")

            result = execute_cascade(
                patch_operations=[_make_op(10, 20), _make_op(30, 40)],
                requests_module=MagicMock(),
                headers={},
                config=_make_config(),
                repo_id="repo-123",
                pull_request_id=42,
            )

        assert result.blocked == [10, 30]
        assert result.succeeded == []
        assert result.fallen_back == []

    def test_fallback_updates_thread_status(self):
        """Fallback replies should still apply the desired thread status."""
        with (
            patch("agentic_devtools.cli.azure_devops.status_cascade.patch_comment") as mock_pc,
            patch("agentic_devtools.cli.azure_devops.status_cascade.patch_thread_status") as mock_pts,
            patch("agentic_devtools.cli.azure_devops.status_cascade.post_cross_identity_reply") as mock_reply,
        ):
            mock_pc.side_effect = CrossIdentityForbiddenError(10, 20)
            mock_pts.return_value = {}
            mock_reply.return_value = {}

            result = execute_cascade(
                patch_operations=[_make_op(10, 20)],
                requests_module=MagicMock(),
                headers={},
                config=_make_config(),
                repo_id="repo-123",
                pull_request_id=42,
            )

        assert result.fallen_back == [10]
        mock_reply.assert_called_once()
        mock_pts.assert_called_once()

    def test_empty_operations(self):
        """Empty list → empty result."""
        result = execute_cascade(
            patch_operations=[],
            requests_module=MagicMock(),
            headers={},
            config=_make_config(),
            repo_id="repo-123",
            pull_request_id=42,
        )

        assert isinstance(result, CascadeResult)
        assert result.succeeded == []
        assert result.blocked == []


class TestCascadeReplyIdFeedback:
    """execute_cascade feeds a cross-identity reply id back into state."""

    def test_fallback_with_state_retargets_overall_summary(self):
        """A 403 reply fallback records the reply id and re-targets state.overallSummary."""
        state = _state_with_overall(thread_id=10, comment_id=20)

        with (
            patch("agentic_devtools.cli.azure_devops.status_cascade.patch_comment") as mock_pc,
            patch("agentic_devtools.cli.azure_devops.status_cascade.patch_thread_status") as mock_pts,
            patch("agentic_devtools.cli.azure_devops.status_cascade.post_cross_identity_reply") as mock_reply,
        ):
            mock_pc.side_effect = CrossIdentityForbiddenError(10, 20)
            mock_pts.return_value = {}
            mock_reply.return_value = {"id": 4242}

            result = execute_cascade(
                patch_operations=[_make_op(10, 20)],
                requests_module=MagicMock(),
                headers={},
                config=_make_config(),
                repo_id="repo-123",
                pull_request_id=42,
                state=state,
            )

        assert result.fallen_back == [10]
        assert result.reply_comment_ids == {10: 4242}
        # The next cascade will PATCH our reply (4242) instead of re-replying.
        assert state.overallSummary.commentId == 4242

    def test_fallback_without_state_still_records_reply_id(self):
        """Without state the reply id is still recorded in the result (no crash)."""
        with (
            patch("agentic_devtools.cli.azure_devops.status_cascade.patch_comment") as mock_pc,
            patch("agentic_devtools.cli.azure_devops.status_cascade.patch_thread_status") as mock_pts,
            patch("agentic_devtools.cli.azure_devops.status_cascade.post_cross_identity_reply") as mock_reply,
        ):
            mock_pc.side_effect = CrossIdentityForbiddenError(10, 20)
            mock_pts.return_value = {}
            mock_reply.return_value = {"id": 4242}

            result = execute_cascade(
                patch_operations=[_make_op(10, 20)],
                requests_module=MagicMock(),
                headers={},
                config=_make_config(),
                repo_id="repo-123",
                pull_request_id=42,
            )

        assert result.fallen_back == [10]
        assert result.reply_comment_ids == {10: 4242}
