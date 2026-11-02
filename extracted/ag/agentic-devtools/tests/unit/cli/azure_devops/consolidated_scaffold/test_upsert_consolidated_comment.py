"""Tests for upsert_consolidated_comment."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.consolidated_scaffold import upsert_consolidated_comment
from agentic_devtools.cli.azure_devops.review_state import (
    FileEntry,
    FolderGroup,
    OverallSummary,
    ReviewState,
    ReviewStatus,
)

_MOD = "agentic_devtools.cli.azure_devops.consolidated_scaffold"
REPO_ID = "repo-guid-123"


def _config() -> AzureDevOpsConfig:
    return AzureDevOpsConfig(
        organization="https://dev.azure.com/org",
        project="proj",
        repository="repo",
    )


def _state(thread_id: int = 0, comment_id: int = 0) -> ReviewState:
    fe = FileEntry(threadId=0, commentId=0, folder="src", fileName="a.py", status=ReviewStatus.APPROVED.value)
    return ReviewState(
        prId=42,
        repoId=REPO_ID,
        repoName="repo",
        project="proj",
        organization="https://dev.azure.com/org",
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00Z",
        overallSummary=OverallSummary(threadId=thread_id, commentId=comment_id, narrativeSummary="Looks good."),
        folders={"src": FolderGroup(files=["/src/a.py"])},
        files={"/src/a.py": fe},
        commitHash="4a8685bda246f3bf826efabaf990fe9c3d1da125",
        modelId="claude-opus-4.6",
    )


def _post_response():
    resp = MagicMock()
    resp.json.return_value = {"id": 555, "comments": [{"id": 7}]}
    resp.raise_for_status.return_value = None
    return resp


class TestUpsertConsolidatedCommentCreate:
    """First-call (create) behaviour."""

    @patch(f"{_MOD}.patch_thread_status")
    def test_create_posts_thread_and_records_ids(self, mock_status):
        state = _state(thread_id=0)
        req = MagicMock()
        req.post.return_value = _post_response()

        result = upsert_consolidated_comment(state, _config(), REPO_ID, req, {"Authorization": "x"})

        req.post.assert_called_once()
        # New thread/comment ids recorded on state.
        assert result.overallSummary.threadId == 555
        assert result.overallSummary.commentId == 7
        # Posted content carries the v2 consolidated marker.
        body = req.post.call_args.kwargs["json"]
        assert "agdt-review:v2 type:consolidated" in body["comments"][0]["content"]

    @patch(f"{_MOD}.patch_thread_status")
    def test_create_resolves_thread_to_closed(self, mock_status):
        state = _state(thread_id=0)
        req = MagicMock()
        req.post.return_value = _post_response()

        upsert_consolidated_comment(state, _config(), REPO_ID, req, {})

        mock_status.assert_called_once()
        assert mock_status.call_args.kwargs["status"] == "closed"
        assert mock_status.call_args.kwargs["thread_id"] == 555

    @patch(f"{_MOD}.patch_comment")
    @patch(f"{_MOD}.patch_thread_status")
    def test_create_does_not_patch_existing_comment(self, mock_status, mock_patch):
        state = _state(thread_id=0)
        req = MagicMock()
        req.post.return_value = _post_response()

        upsert_consolidated_comment(state, _config(), REPO_ID, req, {})

        mock_patch.assert_not_called()

    @patch(f"{_MOD}.patch_thread_status", side_effect=RuntimeError("boom"))
    def test_create_warns_when_closing_thread_fails(self, mock_status, capsys):
        state = _state(thread_id=0)
        req = MagicMock()
        req.post.return_value = _post_response()

        result = upsert_consolidated_comment(state, _config(), REPO_ID, req, {})

        assert result.overallSummary.threadId == 555
        assert result.overallSummary.commentId == 7
        assert "Warning: Could not resolve thread 555: boom" in capsys.readouterr().err


class TestUpsertConsolidatedCommentUpdate:
    """Subsequent-call (update) behaviour."""

    @patch(f"{_MOD}.patch_thread_status")
    @patch(f"{_MOD}.patch_comment", return_value={"id": 5})
    def test_update_patches_existing_comment(self, mock_patch, mock_status):
        state = _state(thread_id=100, comment_id=5)
        req = MagicMock()

        result = upsert_consolidated_comment(state, _config(), REPO_ID, req, {})

        req.post.assert_not_called()
        mock_status.assert_not_called()
        mock_patch.assert_called_once()
        kwargs = mock_patch.call_args.kwargs
        assert kwargs["thread_id"] == 100
        assert kwargs["comment_id"] == 5
        assert kwargs["reply_on_forbidden"] is True
        assert "agdt-review:v2 type:consolidated" in kwargs["new_content"]
        # Ids unchanged after normal PATCH (same id returned).
        assert result.overallSummary.threadId == 100
        assert result.overallSummary.commentId == 5

    @patch(f"{_MOD}.patch_comment", return_value={"id": 99})
    def test_update_records_new_comment_id_after_cross_identity_reply(self, mock_patch):
        """When patch_comment falls back to a cross-identity reply, the new comment id is stored."""
        state = _state(thread_id=100, comment_id=5)
        req = MagicMock()

        result = upsert_consolidated_comment(state, _config(), REPO_ID, req, {})

        mock_patch.assert_called_once_with(
            requests_module=req,
            headers={},
            config=_config(),
            repo_id=REPO_ID,
            pull_request_id=42,
            thread_id=100,
            comment_id=5,
            new_content=mock_patch.call_args.kwargs["new_content"],
            reply_on_forbidden=True,
        )
        # New reply id recorded so next update targets it instead of the original.
        assert result.overallSummary.commentId == 99

    @patch(f"{_MOD}.patch_comment", return_value={"id": "not-a-number"})
    def test_update_ignores_non_numeric_id_in_response(self, mock_patch):
        """A non-numeric id from the API is silently ignored; commentId is not changed."""
        state = _state(thread_id=100, comment_id=5)
        req = MagicMock()

        result = upsert_consolidated_comment(state, _config(), REPO_ID, req, {})

        # commentId unchanged; no exception raised.
        assert result.overallSummary.commentId == 5

    @patch(f"{_MOD}.patch_comment", return_value={})
    def test_update_handles_missing_id_in_response(self, mock_patch):
        """When patch_comment returns a dict without 'id', commentId is not changed."""
        state = _state(thread_id=100, comment_id=5)
        req = MagicMock()

        result = upsert_consolidated_comment(state, _config(), REPO_ID, req, {})

        assert result.overallSummary.commentId == 5

    @patch(f"{_MOD}.patch_comment")
    def test_update_rediscovers_comment_id_when_zero(self, mock_patch):
        """When commentId is 0 but threadId is valid, the thread is fetched to find the id."""
        state = _state(thread_id=100, comment_id=0)
        req = MagicMock()
        get_resp = MagicMock()
        get_resp.raise_for_status.return_value = None
        get_resp.json.return_value = {"comments": [{"id": 3, "isDeleted": False}]}
        req.get.return_value = get_resp
        # Successful PATCH returns the patched comment (same id).
        mock_patch.return_value = {"id": 3}

        result = upsert_consolidated_comment(state, _config(), REPO_ID, req, {})

        # GET was issued to fetch the thread.
        req.get.assert_called_once()
        # Rediscovered id used for patch call.
        kwargs = mock_patch.call_args.kwargs
        assert kwargs["comment_id"] == 3
        # State updated with rediscovered id (patch returned same id, no further update).
        assert result.overallSummary.commentId == 3

    @patch(f"{_MOD}.patch_comment")
    def test_update_skips_deleted_comments_during_rediscovery(self, mock_patch):
        """Re-discovery skips deleted comments and uses the first non-deleted one."""
        state = _state(thread_id=100, comment_id=0)
        req = MagicMock()
        get_resp = MagicMock()
        get_resp.raise_for_status.return_value = None
        get_resp.json.return_value = {
            "comments": [
                {"id": 1, "isDeleted": True},
                {"id": 2, "isDeleted": False},
            ]
        }
        req.get.return_value = get_resp
        mock_patch.return_value = {"id": 2}

        result = upsert_consolidated_comment(state, _config(), REPO_ID, req, {})

        kwargs = mock_patch.call_args.kwargs
        assert kwargs["comment_id"] == 2
        assert result.overallSummary.commentId == 2

    @patch(f"{_MOD}.patch_comment", return_value={"id": 1})
    def test_update_falls_back_to_1_when_get_fails(self, mock_patch, capsys):
        """When the thread GET fails, comment id falls back to 1."""
        state = _state(thread_id=100, comment_id=0)
        req = MagicMock()
        req.get.side_effect = RuntimeError("network error")

        result = upsert_consolidated_comment(state, _config(), REPO_ID, req, {})

        kwargs = mock_patch.call_args.kwargs
        assert kwargs["comment_id"] == 1
        assert "Warning: Could not re-discover comment id for thread 100" in capsys.readouterr().err
        assert result.overallSummary.commentId == 1

    @patch(f"{_MOD}.patch_comment", return_value={"id": 1})
    def test_update_falls_back_to_1_when_no_comments_returned(self, mock_patch):
        """When the thread GET returns no non-deleted comments, comment id falls back to 1."""
        state = _state(thread_id=100, comment_id=0)
        req = MagicMock()
        get_resp = MagicMock()
        get_resp.raise_for_status.return_value = None
        get_resp.json.return_value = {"comments": []}
        req.get.return_value = get_resp

        result = upsert_consolidated_comment(state, _config(), REPO_ID, req, {})

        kwargs = mock_patch.call_args.kwargs
        assert kwargs["comment_id"] == 1
        assert result.overallSummary.commentId == 1

    @patch(f"{_MOD}.patch_comment")
    def test_update_prefers_marker_comment_over_first_nondeleted_during_rediscovery(self, mock_patch):
        """Re-discovery prefers a marker comment over the first non-deleted comment."""
        from agentic_devtools.cli.azure_devops.consolidated_review import build_consolidated_marker

        state = _state(thread_id=100, comment_id=0)
        req = MagicMock()
        get_resp = MagicMock()
        get_resp.raise_for_status.return_value = None
        # id=2 is the first non-deleted; id=5 carries the v2 marker — id=5 should win.
        marker_content = build_consolidated_marker(42, "abc123")
        get_resp.json.return_value = {
            "comments": [
                {"id": 2, "isDeleted": False, "content": "some other comment"},
                {"id": 5, "isDeleted": False, "content": marker_content},
            ]
        }
        req.get.return_value = get_resp
        mock_patch.return_value = {"id": 5}

        result = upsert_consolidated_comment(state, _config(), REPO_ID, req, {})

        kwargs = mock_patch.call_args.kwargs
        assert kwargs["comment_id"] == 5
        assert result.overallSummary.commentId == 5

    @patch(f"{_MOD}.patch_comment")
    def test_update_prefers_newest_marker_comment_during_rediscovery(self, mock_patch):
        """Re-discovery should target the newest marker comment for cross-identity replies."""
        from agentic_devtools.cli.azure_devops.consolidated_review import build_consolidated_marker

        state = _state(thread_id=100, comment_id=0)
        req = MagicMock()
        get_resp = MagicMock()
        get_resp.raise_for_status.return_value = None
        marker_content = build_consolidated_marker(42, "abc123")
        get_resp.json.return_value = {
            "comments": [
                {"id": 5, "isDeleted": False, "content": marker_content},
                {"id": 9, "isDeleted": False, "content": marker_content},
            ]
        }
        req.get.return_value = get_resp
        mock_patch.return_value = {"id": 9}

        result = upsert_consolidated_comment(state, _config(), REPO_ID, req, {})

        kwargs = mock_patch.call_args.kwargs
        assert kwargs["comment_id"] == 9
        assert result.overallSummary.commentId == 9

    @patch(f"{_MOD}.patch_comment")
    def test_update_falls_back_to_first_nondeleted_when_no_marker_comment(self, mock_patch):
        """When no non-deleted comment carries the v2 marker, the first non-deleted is used."""
        state = _state(thread_id=100, comment_id=0)
        req = MagicMock()
        get_resp = MagicMock()
        get_resp.raise_for_status.return_value = None
        get_resp.json.return_value = {
            "comments": [
                {"id": 3, "isDeleted": False, "content": "no marker here"},
                {"id": 7, "isDeleted": False, "content": "still no marker"},
            ]
        }
        req.get.return_value = get_resp
        mock_patch.return_value = {"id": 3}

        result = upsert_consolidated_comment(state, _config(), REPO_ID, req, {})

        kwargs = mock_patch.call_args.kwargs
        assert kwargs["comment_id"] == 3
        assert result.overallSummary.commentId == 3


class TestUpsertConsolidatedCommentDryRun:
    """Dry-run makes no API calls."""

    @patch(f"{_MOD}.patch_comment")
    @patch(f"{_MOD}.patch_thread_status")
    def test_dry_run_create_makes_no_calls(self, mock_status, mock_patch, capsys):
        state = _state(thread_id=0)
        req = MagicMock()

        result = upsert_consolidated_comment(state, _config(), REPO_ID, req, {}, dry_run=True)

        req.post.assert_not_called()
        mock_status.assert_not_called()
        mock_patch.assert_not_called()
        assert result.overallSummary.threadId == 0
        assert "Would create" in capsys.readouterr().out

    @patch(f"{_MOD}.patch_comment")
    @patch(f"{_MOD}.patch_thread_status")
    def test_dry_run_update_makes_no_calls(self, mock_status, mock_patch, capsys):
        state = _state(thread_id=100, comment_id=5)
        req = MagicMock()

        upsert_consolidated_comment(state, _config(), REPO_ID, req, {}, dry_run=True)

        req.post.assert_not_called()
        mock_patch.assert_not_called()
        assert "Would update" in capsys.readouterr().out
