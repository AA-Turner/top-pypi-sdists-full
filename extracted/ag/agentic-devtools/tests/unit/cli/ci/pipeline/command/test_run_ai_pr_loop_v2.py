"""Tests for run_ai_pr_loop_v2 command."""

import os
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.models import EventPayload
from agentic_devtools.cli.ci.pipeline.command import (
    EXIT_GUARD_BLOCKED,
    EXIT_METADATA_FAILED,
    EXIT_RATE_LIMIT_PAUSED,
    EXIT_SUCCESS,
    run_ai_pr_loop_v2,
)
from agentic_devtools.cli.ci.pipeline.summary import render_summary_comment
from agentic_devtools.cli.shared.retry import ProviderRateLimitError
from tests.unit.cli.ci.pipeline._preflight_fixtures import (
    _blocked_preflight_summary,
    _ignored_pr_provider,
    _preflight_rate_limit_case,
)


class TestRunAiPrLoopV2:
    """Tests for the pipeline v2 command entry point."""

    def test_returns_success_when_no_pr_number(self) -> None:
        provider = MagicMock()
        event = EventPayload(pr_number=0)
        result = run_ai_pr_loop_v2(provider, event)
        assert result == EXIT_SUCCESS

    def test_returns_metadata_failed_on_snapshot_error(self) -> None:
        """Snapshot build failure after lock acquisition returns EXIT_METADATA_FAILED."""
        provider = MagicMock()
        provider.get_pr_metadata.side_effect = RuntimeError("API error")
        event = EventPayload(pr_number=1)
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.command.acquire_lock",
                return_value="token-abc",
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.command.release_lock",
            ),
        ):
            result = run_ai_pr_loop_v2(provider, event)
            assert result == EXIT_METADATA_FAILED

    def test_lock_acquired_before_snapshot(self) -> None:
        """Lock must be acquired before building the snapshot to save API quota on races."""
        call_order: list[str] = []
        provider = MagicMock()

        def _acquire(p, pr):
            call_order.append("acquire_lock")
            return "tok"

        def _get_meta(pr):
            call_order.append("get_pr_metadata")
            raise RuntimeError("stop here")

        provider.get_pr_metadata.side_effect = _get_meta
        event = EventPayload(pr_number=1)

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.command.acquire_lock",
                side_effect=_acquire,
            ),
            patch("agentic_devtools.cli.ci.pipeline.command.release_lock"),
        ):
            run_ai_pr_loop_v2(provider, event)

        assert call_order == ["acquire_lock", "get_pr_metadata"], "Lock must be acquired before building the snapshot"

    def test_snapshot_not_built_when_lock_not_acquired(self) -> None:
        """When lock returns None (already held), snapshot API calls are never made."""
        provider = MagicMock()
        event = EventPayload(pr_number=1)

        with patch(
            "agentic_devtools.cli.ci.pipeline.command.acquire_lock",
            return_value=None,
        ):
            result = run_ai_pr_loop_v2(provider, event)
            assert result == EXIT_SUCCESS
            provider.get_pr_metadata.assert_not_called()

    def test_guard_blocked_returns_guard_exit_code(self) -> None:
        provider = _ignored_pr_provider()
        event = EventPayload(pr_number=1)

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.command.acquire_lock",
                return_value="token-123",
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.command.release_lock",
            ),
        ):
            result = run_ai_pr_loop_v2(provider, event)
            assert result == EXIT_GUARD_BLOCKED

    def test_preflight_block_returns_one_and_posts_safe_existing_summary(self) -> None:
        provider, summary = MagicMock(), _blocked_preflight_summary()
        with (
            patch("agentic_devtools.cli.ci.pipeline.command.acquire_lock", return_value="token"),
            patch("agentic_devtools.cli.ci.pipeline.command.release_lock"),
            patch("agentic_devtools.cli.ci.pipeline.command.build_pr_state_snapshot", return_value=summary.snapshot),
            patch("agentic_devtools.cli.ci.pipeline.command.run_pipeline", return_value=summary),
            patch("agentic_devtools.cli.ci.pipeline.command.post_summary_comment") as post,
        ):
            assert run_ai_pr_loop_v2(provider, EventPayload(pr_number=1)) == EXIT_GUARD_BLOCKED == 1
        rendered = render_summary_comment(post.call_args.args[2])
        assert "repository_visibility" in rendered and "HTTP 404" in rendered
        assert "blocked" in rendered and "token" not in rendered
        provider.approve_pr.assert_not_called()

    def test_pipeline_runs_resolve_threads_before_squash_and_review_request(self) -> None:
        """Thread resolution must run before squash and review request in the same pass."""
        provider = MagicMock()
        event = EventPayload(pr_number=1)

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.command.acquire_lock",
                return_value="token-123",
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.command.release_lock",
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.command.build_pr_state_snapshot",
                return_value=MagicMock(),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.command.run_pipeline",
            ) as mock_run_pipeline,
            patch(
                "agentic_devtools.cli.ci.pipeline.command.post_summary_comment",
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.command._determine_exit_code",
                return_value=EXIT_SUCCESS,
            ),
        ):
            run_ai_pr_loop_v2(provider, event)

        actions = mock_run_pipeline.call_args.args[2]
        action_names = [action.name for action in actions]
        assert action_names.index("safety_guards") < action_names.index("retry_failed_session")
        assert action_names.index("retry_failed_session") < action_names.index("guards")
        assert action_names.index("retry_failed_session") < action_names.index("publish")
        assert action_names.index("resolve_threads") < action_names.index("squash")
        assert action_names.index("resolve_threads") < action_names.index("request_review")
        assert action_names.index("rebase") < action_names.index("dispatch_conflict_resolution")
        assert action_names.index("dispatch_conflict_resolution") < action_names.index("request_review")

    def test_actionable_check_names_are_threaded_into_run_pipeline(self) -> None:
        """run_pipeline receives the same actionable_check_names as the initial snapshot build."""
        provider = MagicMock()
        event = EventPayload(pr_number=1)
        actionable_check_names = frozenset({"custom-check"})

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.command.acquire_lock",
                return_value="token-123",
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.command.release_lock",
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.command.build_pr_state_snapshot",
                return_value=MagicMock(),
            ) as mock_build,
            patch(
                "agentic_devtools.cli.ci.pipeline.command.run_pipeline",
            ) as mock_run_pipeline,
            patch(
                "agentic_devtools.cli.ci.pipeline.command.post_summary_comment",
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.command._determine_exit_code",
                return_value=EXIT_SUCCESS,
            ),
        ):
            run_ai_pr_loop_v2(provider, event, actionable_check_names=actionable_check_names)

        assert mock_build.call_args.kwargs["actionable_check_names"] == actionable_check_names
        assert mock_run_pipeline.call_args.kwargs["actionable_check_names"] == actionable_check_names

    def test_returns_metadata_failed_when_lock_acquisition_raises(self) -> None:
        provider = MagicMock()
        event = EventPayload(pr_number=1)

        with patch(
            "agentic_devtools.cli.ci.pipeline.command.acquire_lock",
            side_effect=RuntimeError("lock boom"),
        ):
            result = run_ai_pr_loop_v2(provider, event)

        assert result == EXIT_METADATA_FAILED

    def test_release_lock_exception_is_non_fatal(self) -> None:
        provider = MagicMock()
        event = EventPayload(pr_number=1)

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.command.acquire_lock",
                return_value="token-123",
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.command.build_pr_state_snapshot",
                return_value=MagicMock(ci_status="passing"),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.command.run_pipeline",
                return_value=MagicMock(results=[], snapshot=MagicMock(ci_status="passing")),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.command.post_summary_comment",
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.command._determine_exit_code",
                return_value=EXIT_SUCCESS,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.command.release_lock",
                side_effect=RuntimeError("release boom"),
            ),
        ):
            result = run_ai_pr_loop_v2(provider, event)

        assert result == EXIT_SUCCESS

    def test_rate_limit_during_lock_is_controlled_pause(self) -> None:
        provider = MagicMock()
        event = EventPayload(pr_number=1)
        error = ProviderRateLimitError(retry_after_seconds=30, provider="github", credential_identity="GH_TOKEN")
        with (
            patch("agentic_devtools.cli.ci.pipeline.command.acquire_lock", side_effect=error),
            patch("agentic_devtools.cli.ci.pipeline.command.persist_cooldown", return_value=None),
        ):
            assert run_ai_pr_loop_v2(provider, event) == EXIT_RATE_LIMIT_PAUSED

    def test_non_rate_limit_lock_error_remains_metadata_failure(self) -> None:
        provider = MagicMock()
        event = EventPayload(pr_number=1)
        error = ProviderRateLimitError(is_rate_limit=False)
        with patch("agentic_devtools.cli.ci.pipeline.command.acquire_lock", side_effect=error):
            assert run_ai_pr_loop_v2(provider, event) == EXIT_METADATA_FAILED

    @pytest.mark.parametrize("endpoint", ["/user", "/repos/base/target"])
    def test_rate_limit_during_snapshot_is_controlled_pause(self, endpoint, monkeypatch) -> None:
        monkeypatch.setenv("AGDT_PR_APPROVER_PAT", "offline-credential")
        provider, metadata, responses = _preflight_rate_limit_case(endpoint)
        with (
            patch("agentic_devtools.cli.ci.pipeline.command.acquire_lock", return_value="token"),
            patch.object(provider, "get_pr_metadata", return_value=metadata),
            patch("agentic_devtools.cli.ci.github_provider.run_safe", side_effect=responses) as runner,
            patch("agentic_devtools.cli.ci.pipeline.command.release_lock"),
            patch("agentic_devtools.cli.ci.pipeline.command.persist_cooldown", return_value=None) as cooldown,
        ):
            assert run_ai_pr_loop_v2(provider, EventPayload(pr_number=1)) == EXIT_RATE_LIMIT_PAUSED
        error = cooldown.call_args.args[1]
        assert (error.retry_after_seconds, error.reset_timestamp, error.remaining) == (42, 123, 0)
        assert (error.provider, error.credential_identity, error.source) == (
            "github",
            "AGDT_PR_APPROVER_PAT",
            "retry-after",
        )
        assert "offline-credential" not in str(error)
        assert runner.call_count == len(responses)
        assert runner.call_args.args[0][2] == endpoint

    def test_non_rate_limit_snapshot_error_remains_metadata_failure(self) -> None:
        provider = MagicMock()
        event = EventPayload(pr_number=1)
        error = ProviderRateLimitError(is_rate_limit=False)
        with (
            patch("agentic_devtools.cli.ci.pipeline.command.acquire_lock", return_value="token"),
            patch("agentic_devtools.cli.ci.pipeline.command.build_pr_state_snapshot", side_effect=error),
            patch("agentic_devtools.cli.ci.pipeline.command.release_lock"),
        ):
            assert run_ai_pr_loop_v2(provider, event) == EXIT_METADATA_FAILED

    @pytest.mark.parametrize("stage", ["run_pipeline", "post_summary_comment"])
    def test_rate_limit_during_pipeline_or_summary_is_controlled_pause(self, stage) -> None:
        provider = MagicMock()
        event = EventPayload(pr_number=1)
        error = ProviderRateLimitError(provider="github", credential_identity="GH_TOKEN")
        with (
            patch("agentic_devtools.cli.ci.pipeline.command.acquire_lock", return_value="token"),
            patch("agentic_devtools.cli.ci.pipeline.command.build_pr_state_snapshot", return_value=MagicMock()),
            patch("agentic_devtools.cli.ci.pipeline.command.run_pipeline", return_value=MagicMock()),
            patch(f"agentic_devtools.cli.ci.pipeline.command.{stage}", side_effect=error),
            patch("agentic_devtools.cli.ci.pipeline.command.release_lock"),
            patch("agentic_devtools.cli.ci.pipeline.command.persist_cooldown", return_value=None),
        ):
            assert run_ai_pr_loop_v2(provider, event) == EXIT_RATE_LIMIT_PAUSED

    def test_non_rate_limit_pipeline_error_is_reraised(self) -> None:
        provider = MagicMock()
        event = EventPayload(pr_number=1)
        error = ProviderRateLimitError(is_rate_limit=False)
        with (
            patch("agentic_devtools.cli.ci.pipeline.command.acquire_lock", return_value="token"),
            patch("agentic_devtools.cli.ci.pipeline.command.build_pr_state_snapshot", return_value=MagicMock()),
            patch("agentic_devtools.cli.ci.pipeline.command.run_pipeline", side_effect=error),
            patch("agentic_devtools.cli.ci.pipeline.command.release_lock"),
        ):
            with pytest.raises(ProviderRateLimitError):
                run_ai_pr_loop_v2(provider, event)

    def test_non_rate_limit_summary_error_is_reraised(self) -> None:
        provider = MagicMock()
        event = EventPayload(pr_number=1)
        error = ProviderRateLimitError(is_rate_limit=False)
        with (
            patch("agentic_devtools.cli.ci.pipeline.command.acquire_lock", return_value="token"),
            patch("agentic_devtools.cli.ci.pipeline.command.build_pr_state_snapshot", return_value=MagicMock()),
            patch("agentic_devtools.cli.ci.pipeline.command.run_pipeline", return_value=MagicMock()),
            patch("agentic_devtools.cli.ci.pipeline.command.post_summary_comment", side_effect=error),
            patch("agentic_devtools.cli.ci.pipeline.command.release_lock"),
        ):
            with pytest.raises(ProviderRateLimitError):
                run_ai_pr_loop_v2(provider, event)

    def test_rate_limit_during_release_lock_is_controlled_pause(self) -> None:
        """A rate-limit error from release_lock must be converted to the paused outcome."""
        provider = MagicMock()
        event = EventPayload(pr_number=1)
        error = ProviderRateLimitError(retry_after_seconds=60, provider="github", credential_identity="GH_TOKEN")
        with (
            patch("agentic_devtools.cli.ci.pipeline.command.acquire_lock", return_value="token"),
            patch("agentic_devtools.cli.ci.pipeline.command.build_pr_state_snapshot", return_value=MagicMock()),
            patch("agentic_devtools.cli.ci.pipeline.command.run_pipeline", return_value=MagicMock()),
            patch("agentic_devtools.cli.ci.pipeline.command.post_summary_comment"),
            patch("agentic_devtools.cli.ci.pipeline.command._determine_exit_code", return_value=EXIT_SUCCESS),
            patch("agentic_devtools.cli.ci.pipeline.command.release_lock", side_effect=error),
            patch("agentic_devtools.cli.ci.pipeline.command.persist_cooldown", return_value=None),
        ):
            assert run_ai_pr_loop_v2(provider, event) == EXIT_RATE_LIMIT_PAUSED

    def test_rate_limit_during_release_lock_overrides_snapshot_failure(self) -> None:
        """A lock-release rate limit must be handled after an early snapshot-failure return."""
        provider = MagicMock()
        event = EventPayload(pr_number=1)
        error = ProviderRateLimitError(retry_after_seconds=60, provider="github", credential_identity="GH_TOKEN")
        with (
            patch("agentic_devtools.cli.ci.pipeline.command.acquire_lock", return_value="token"),
            patch(
                "agentic_devtools.cli.ci.pipeline.command.build_pr_state_snapshot",
                side_effect=RuntimeError("snapshot failure"),
            ),
            patch("agentic_devtools.cli.ci.pipeline.command.release_lock", side_effect=error),
            patch("agentic_devtools.cli.ci.pipeline.command.persist_cooldown", return_value=None),
        ):
            assert run_ai_pr_loop_v2(provider, event) == EXIT_RATE_LIMIT_PAUSED

    def test_non_rate_limit_release_lock_error_is_non_fatal(self) -> None:
        """A non-rate-limit ProviderRateLimitError from release_lock is logged and ignored."""
        provider = MagicMock()
        event = EventPayload(pr_number=1)
        error = ProviderRateLimitError(is_rate_limit=False)
        with (
            patch("agentic_devtools.cli.ci.pipeline.command.acquire_lock", return_value="token"),
            patch("agentic_devtools.cli.ci.pipeline.command.build_pr_state_snapshot", return_value=MagicMock()),
            patch("agentic_devtools.cli.ci.pipeline.command.run_pipeline", return_value=MagicMock()),
            patch("agentic_devtools.cli.ci.pipeline.command.post_summary_comment"),
            patch("agentic_devtools.cli.ci.pipeline.command._determine_exit_code", return_value=EXIT_SUCCESS),
            patch("agentic_devtools.cli.ci.pipeline.command.release_lock", side_effect=error),
        ):
            assert run_ai_pr_loop_v2(provider, event) == EXIT_SUCCESS

    def test_primary_exception_not_suppressed_by_release_lock_rate_limit(self) -> None:
        """A rate-limit error in release_lock must not suppress a propagating primary exception."""
        provider = MagicMock()
        event = EventPayload(pr_number=1)
        primary_error = RuntimeError("pipeline failure")
        lock_error = ProviderRateLimitError(retry_after_seconds=60, provider="github", credential_identity="GH_TOKEN")
        with (
            patch("agentic_devtools.cli.ci.pipeline.command.acquire_lock", return_value="token"),
            patch("agentic_devtools.cli.ci.pipeline.command.build_pr_state_snapshot", return_value=MagicMock()),
            patch("agentic_devtools.cli.ci.pipeline.command.run_pipeline", side_effect=primary_error),
            patch("agentic_devtools.cli.ci.pipeline.command.release_lock", side_effect=lock_error),
            patch("agentic_devtools.cli.ci.pipeline.command.persist_cooldown", return_value=None),
        ):
            with pytest.raises(RuntimeError, match="pipeline failure"):
                run_ai_pr_loop_v2(provider, event)

    def test_writes_actions_executed_true_to_github_output(self, tmp_path) -> None:
        """When an action executed, actions_executed=true is appended to GITHUB_OUTPUT."""
        output_file = tmp_path / "github_output.txt"
        provider = MagicMock()
        event = EventPayload(pr_number=1)
        mock_summary = MagicMock(
            results=[MagicMock(name="rebase", decision=MagicMock(name="EXECUTE"))],
            snapshot=MagicMock(ci_status="passing"),
        )
        # Decision comparison must match ActionDecision.EXECUTE
        from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult

        mock_summary.results = [ActionResult(name="rebase", decision=ActionDecision.EXECUTE, details="rebased")]

        with (
            patch.dict("os.environ", {"GITHUB_OUTPUT": str(output_file)}),
            patch("agentic_devtools.cli.ci.pipeline.command.acquire_lock", return_value="token"),
            patch("agentic_devtools.cli.ci.pipeline.command.build_pr_state_snapshot", return_value=MagicMock()),
            patch("agentic_devtools.cli.ci.pipeline.command.run_pipeline", return_value=mock_summary),
            patch("agentic_devtools.cli.ci.pipeline.command.post_summary_comment"),
            patch("agentic_devtools.cli.ci.pipeline.command._determine_exit_code", return_value=EXIT_SUCCESS),
            patch("agentic_devtools.cli.ci.pipeline.command.release_lock"),
        ):
            assert run_ai_pr_loop_v2(provider, event) == EXIT_SUCCESS

        content = output_file.read_text(encoding="utf-8")
        assert "actions_executed=true\n" in content

    def test_writes_actions_executed_false_to_github_output(self, tmp_path) -> None:
        """When no action executed, actions_executed=false is appended to GITHUB_OUTPUT."""
        output_file = tmp_path / "github_output.txt"
        provider = MagicMock()
        event = EventPayload(pr_number=1)
        from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult

        mock_summary = MagicMock(
            results=[ActionResult(name="guards", decision=ActionDecision.SKIP, details="all skipped")],
            snapshot=MagicMock(ci_status="passing"),
        )

        with (
            patch.dict("os.environ", {"GITHUB_OUTPUT": str(output_file)}),
            patch("agentic_devtools.cli.ci.pipeline.command.acquire_lock", return_value="token"),
            patch("agentic_devtools.cli.ci.pipeline.command.build_pr_state_snapshot", return_value=MagicMock()),
            patch("agentic_devtools.cli.ci.pipeline.command.run_pipeline", return_value=mock_summary),
            patch("agentic_devtools.cli.ci.pipeline.command.post_summary_comment"),
            patch("agentic_devtools.cli.ci.pipeline.command._determine_exit_code", return_value=EXIT_SUCCESS),
            patch("agentic_devtools.cli.ci.pipeline.command.release_lock"),
        ):
            assert run_ai_pr_loop_v2(provider, event) == EXIT_SUCCESS

        content = output_file.read_text(encoding="utf-8")
        assert "actions_executed=false\n" in content

    def test_handles_github_output_oserror(self) -> None:
        """When writing to GITHUB_OUTPUT raises OSError, logs warning and continues."""
        provider = MagicMock()
        event = EventPayload(pr_number=1)
        from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult

        mock_summary = MagicMock(
            results=[ActionResult(name="guards", decision=ActionDecision.SKIP, details="all skipped")],
            snapshot=MagicMock(ci_status="passing"),
        )

        with (
            patch.dict("os.environ", {"GITHUB_OUTPUT": "/nonexistent/invalid/dir/output.txt"}),
            patch("agentic_devtools.cli.ci.pipeline.command.acquire_lock", return_value="token"),
            patch("agentic_devtools.cli.ci.pipeline.command.build_pr_state_snapshot", return_value=MagicMock()),
            patch("agentic_devtools.cli.ci.pipeline.command.run_pipeline", return_value=mock_summary),
            patch("agentic_devtools.cli.ci.pipeline.command.post_summary_comment"),
            patch("agentic_devtools.cli.ci.pipeline.command._determine_exit_code", return_value=EXIT_SUCCESS),
            patch("agentic_devtools.cli.ci.pipeline.command.release_lock"),
        ):
            assert run_ai_pr_loop_v2(provider, event) == EXIT_SUCCESS

    def test_runs_when_github_output_not_set(self) -> None:
        """When GITHUB_OUTPUT is not set in environment, completes normally."""
        provider = MagicMock()
        event = EventPayload(pr_number=1)
        from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult

        mock_summary = MagicMock(
            results=[ActionResult(name="guards", decision=ActionDecision.SKIP, details="all skipped")],
            snapshot=MagicMock(ci_status="passing"),
        )

        with (
            patch.dict("os.environ", {}, clear=False),
            patch("agentic_devtools.cli.ci.pipeline.command.acquire_lock", return_value="token"),
            patch("agentic_devtools.cli.ci.pipeline.command.build_pr_state_snapshot", return_value=MagicMock()),
            patch("agentic_devtools.cli.ci.pipeline.command.run_pipeline", return_value=mock_summary),
            patch("agentic_devtools.cli.ci.pipeline.command.post_summary_comment"),
            patch("agentic_devtools.cli.ci.pipeline.command._determine_exit_code", return_value=EXIT_SUCCESS),
            patch("agentic_devtools.cli.ci.pipeline.command.release_lock"),
        ):
            os.environ.pop("GITHUB_OUTPUT", None)
            assert run_ai_pr_loop_v2(provider, event) == EXIT_SUCCESS
