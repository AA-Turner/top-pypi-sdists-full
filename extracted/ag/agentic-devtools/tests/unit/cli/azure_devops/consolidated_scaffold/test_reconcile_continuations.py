"""Tests for _reconcile_continuations."""

from unittest.mock import MagicMock

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.consolidated_scaffold import _reconcile_continuations
from agentic_devtools.cli.azure_devops.review_state import (
    CommitComment,
    ModelCommentRef,
    ReviewState,
)

_COMMIT = "4a8685bda246f3bf826efabaf990fe9c3d1da125"
_MODEL = "claude-opus-4.6"


def _config() -> AzureDevOpsConfig:
    return AzureDevOpsConfig(organization="https://dev.azure.com/org", project="proj", repository="repo")


def _state(continuation_ids: list[int], thread_id: int = 555) -> ReviewState:
    state = MagicMock(spec=ReviewState)
    state.prId = 42
    state.commitHash = _COMMIT
    state.modelId = _MODEL
    entry = CommitComment(
        commitHash=_COMMIT,
        threadId=thread_id,
        models=[ModelCommentRef(modelId=_MODEL, commentId=7, continuationCommentIds=list(continuation_ids))],
    )
    state.commitComments = {_COMMIT: entry}
    return state


def _reconcile(state, continuations, req):
    _reconcile_continuations(
        state=state,
        config=_config(),
        repo_id="repo",
        requests_module=req,
        headers={},
        continuations=continuations,
    )


class TestReconcileContinuations:
    """Create/update/retire continuation reply comments."""

    def test_no_continuations_no_calls(self):
        state = _state(continuation_ids=[])
        req = MagicMock()
        _reconcile(state, [], req)
        req.post.assert_not_called()

    def test_posts_new_continuation(self):
        state = _state(continuation_ids=[])
        req = MagicMock()
        req.post.return_value.json.return_value = {"id": 88}
        req.post.return_value.raise_for_status.return_value = None
        _reconcile(state, ["payload one"], req)
        req.post.assert_called_once()
        ref = state.commitComments[_COMMIT].get_model(_MODEL)
        assert ref.continuationCommentIds == [88]

    def test_patches_existing_continuation(self):
        state = _state(continuation_ids=[88])
        req = MagicMock()
        req.patch.return_value.status_code = 200
        req.patch.return_value.json.return_value = {"id": 88}
        req.patch.return_value.raise_for_status.return_value = None
        _reconcile(state, ["updated payload"], req)
        req.patch.assert_called_once()
        req.post.assert_not_called()
        ref = state.commitComments[_COMMIT].get_model(_MODEL)
        assert ref.continuationCommentIds == [88]

    def test_retires_stale_continuation(self):
        state = _state(continuation_ids=[88, 99])
        req = MagicMock()
        req.patch.return_value.status_code = 200
        req.patch.return_value.json.return_value = {"id": 88}
        req.patch.return_value.raise_for_status.return_value = None
        # Now only one continuation is needed; 99 must be retired (tombstoned).
        _reconcile(state, ["only payload"], req)
        # Two patches: one update of 88, one tombstone of 99.
        assert req.patch.call_count == 2
        ref = state.commitComments[_COMMIT].get_model(_MODEL)
        assert ref.continuationCommentIds == [88, 99]

    def test_retire_forbidden_does_not_post_fallback_reply(self):
        # When retiring a stale continuation hits a 403 (comment owned by
        # another identity), the retirement should be silently skipped rather
        # than posting an unbounded cross-identity fallback reply on every run.
        state = _state(continuation_ids=[88, 99])
        req = MagicMock()
        # First PATCH (update 88) succeeds; second PATCH (retire 99) gets 403.
        ok_resp = MagicMock()
        ok_resp.status_code = 200
        ok_resp.json.return_value = {"id": 88}
        ok_resp.raise_for_status.return_value = None
        forbidden_resp = MagicMock()
        forbidden_resp.status_code = 403
        forbidden_resp.raise_for_status.side_effect = Exception("403 Forbidden")
        req.patch.side_effect = [ok_resp, forbidden_resp]
        _reconcile(state, ["only payload"], req)
        # No fallback POST should have been made for the failed retirement.
        req.post.assert_not_called()

    def test_noop_when_no_thread(self):
        state = _state(continuation_ids=[88], thread_id=0)
        req = MagicMock()
        _reconcile(state, ["x"], req)
        req.patch.assert_not_called()
        req.post.assert_not_called()

    def test_noop_when_no_registry_entry(self):
        state = MagicMock(spec=ReviewState)
        state.prId = 42
        state.commitHash = _COMMIT
        state.modelId = _MODEL
        state.commitComments = {}
        req = MagicMock()
        _reconcile(state, ["x"], req)
        req.post.assert_not_called()

    def test_noop_when_no_commit_hash(self):
        state = _state(continuation_ids=[88])
        state.commitHash = ""
        req = MagicMock()
        _reconcile(state, ["x"], req)
        req.post.assert_not_called()
        req.patch.assert_not_called()

    def test_noop_when_model_ref_absent(self):
        # Registry entry exists for the commit but has no ref for the current
        # model, so there is no continuation chain to reconcile.
        state = _state(continuation_ids=[88])
        state.commitComments[_COMMIT].models = [ModelCommentRef(modelId="other-model", commentId=1)]
        req = MagicMock()
        _reconcile(state, ["x"], req)
        req.post.assert_not_called()
        req.patch.assert_not_called()

    def test_post_without_id_not_tracked(self):
        # When a newly posted continuation reply yields no usable id, it is not
        # appended to the tracked continuation ids.
        state = _state(continuation_ids=[])
        req = MagicMock()
        req.post.return_value.json.return_value = {"id": 0}
        req.post.return_value.raise_for_status.return_value = None
        _reconcile(state, ["payload one"], req)
        req.post.assert_called_once()
        ref = state.commitComments[_COMMIT].get_model(_MODEL)
        assert ref.continuationCommentIds == []
