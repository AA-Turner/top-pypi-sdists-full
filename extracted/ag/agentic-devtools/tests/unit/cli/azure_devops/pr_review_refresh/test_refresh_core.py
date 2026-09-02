"""Tests for refresh_core."""

from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.pr_review_refresh import refresh_core

_M = "agentic_devtools.cli.azure_devops.pr_review_refresh"


def _stub_state():
    return SimpleNamespace(
        repoId="repo-guid",
        overallSummary=SimpleNamespace(threadId=1, commentId=1),
        commitComments={},
        files={},
    )


def _patch_core(stack, *, should=True, missing=False):
    resolve_answers_dir = stack.enter_context(patch(f"{_M}.resolve_answers_dir", return_value=Path("answers")))
    stack.enter_context(patch(f"{_M}.read_ledger_entries", return_value=[]))
    stack.enter_context(patch(f"{_M}.latest_accepted_by_file_key", return_value={}))
    stack.enter_context(patch(f"{_M}.summarize_accepted", return_value={"approved": 1, "needsWork": 2, "reviewed": 3}))
    stack.enter_context(patch(f"{_M}.get_value", return_value=None))
    stack.enter_context(patch(f"{_M}.should_refresh", return_value=should))
    if missing:
        stack.enter_context(patch(f"{_M}.load_review_state", side_effect=FileNotFoundError))
    else:
        stack.enter_context(patch(f"{_M}.load_review_state", return_value=_stub_state()))
    config_cls = stack.enter_context(patch(f"{_M}.AzureDevOpsConfig"))
    config_cls.from_state.return_value = "config"
    stack.enter_context(patch(f"{_M}.get_auth_headers", return_value={"h": "v"}))
    stack.enter_context(patch(f"{_M}.get_pat", return_value="pat"))
    return SimpleNamespace(
        resolve_answers_dir=resolve_answers_dir,
        overlay=stack.enter_context(patch(f"{_M}.overlay_ledger_onto_state")),
        upsert=stack.enter_context(patch(f"{_M}.upsert_consolidated_comment")),
        save=stack.enter_context(patch(f"{_M}.save_review_state")),
        setv=stack.enter_context(patch(f"{_M}.set_value")),
    )


class TestRefreshCore:
    def test_throttled_skips_render(self):
        with ExitStack() as stack:
            mocks = _patch_core(stack, should=False)
            result = refresh_core(5, now_fn=lambda: 100.0)
        assert result["refreshed"] is False
        assert result["reason"] == "throttled"
        assert result["reviewed"] == 3
        mocks.upsert.assert_not_called()

    def test_no_review_state(self):
        with ExitStack() as stack:
            mocks = _patch_core(stack, missing=True)
            result = refresh_core(5)
        assert result["refreshed"] is False
        assert result["reason"] == "no-review-state"
        mocks.upsert.assert_not_called()

    def test_non_final_real_overlays_and_persists(self):
        with ExitStack() as stack:
            mocks = _patch_core(stack)
            result = refresh_core(5, dry_run=False, now_fn=lambda: 123.0)
        assert result["refreshed"] is True
        assert result["reason"] == "updated"
        mocks.resolve_answers_dir.assert_called_once_with(5, backfill=True)
        mocks.overlay.assert_called_once()
        assert mocks.upsert.call_args.kwargs["force_in_progress"] is True
        assert mocks.upsert.call_args.kwargs["dry_run"] is False
        mocks.save.assert_called_once()
        assert mocks.setv.call_count == 2

    def test_non_final_dry_run_does_not_persist(self):
        with ExitStack() as stack:
            mocks = _patch_core(stack)
            result = refresh_core(5, dry_run=True)
        assert result["refreshed"] is True
        mocks.resolve_answers_dir.assert_called_once_with(5, backfill=False)
        assert mocks.upsert.call_args.kwargs["force_in_progress"] is True
        assert mocks.upsert.call_args.kwargs["dry_run"] is True
        mocks.save.assert_not_called()
        mocks.setv.assert_not_called()

    def test_final_real_renders_terminal_full(self):
        with ExitStack() as stack:
            mocks = _patch_core(stack)
            result = refresh_core(5, dry_run=False, final=True)
        assert result["refreshed"] is True
        assert result["reason"] == "final"
        mocks.overlay.assert_not_called()
        assert mocks.upsert.call_args.kwargs["force_in_progress"] is False
        mocks.save.assert_called_once()

    def test_final_dry_run_does_not_persist(self):
        with ExitStack() as stack:
            mocks = _patch_core(stack)
            result = refresh_core(5, dry_run=True, final=True)
        assert result["refreshed"] is True
        assert result["reason"] == "final"
        assert mocks.upsert.call_args.kwargs["dry_run"] is True
        mocks.save.assert_not_called()

    def test_defaults_requests_module_when_not_provided(self):
        with ExitStack() as stack:
            mocks = _patch_core(stack)
            result = refresh_core(5, dry_run=False)
        assert result["refreshed"] is True
        assert mocks.upsert.call_args.args[3] is not None
