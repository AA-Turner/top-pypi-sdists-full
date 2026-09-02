"""Tests for run_langchain_workflow runner."""

import hashlib
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest


class TestRunLangchainWorkflowFreshInvocation:
    """Tests for fresh (non-resume) LangGraph workflow invocation."""

    def test_thread_id_includes_worktree_key(self, tmp_path):
        """Fresh invocations scope their checkpoint thread to the active worktree.

        The explicit invocation worktree key takes precedence over
        get_bootstrap_state() (FR-004), so the thread identity uses the validated
        active worktree key even when an env override or pinned path resolves to a
        non-canonical directory.
        The thread identity uses the length-prefixed injective encoding
        ``work-on-issue-{N}:{issue_key}--worktree-{M}:{worktree_key}`` per FR-004.
        """
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        scoped_state_dir = tmp_path / "feature-42"
        scoped_state_dir.mkdir()

        with (
            patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer,
            patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build,
            patch("agentic_devtools.state.get_state_dir", return_value=scoped_state_dir),
            patch(
                "agentic_devtools.state.get_bootstrap_state",
                return_value={"worktree_key": "feature-42"},
            ),
        ):
            mock_checkpointer.return_value = MagicMock()
            mock_build.return_value = mock_compiled
            from agentic_devtools.orchestration.runner import run_langchain_workflow

            run_langchain_workflow("TEST-123")

        config = mock_compiled.invoke.call_args.kwargs["config"]
        # FR-004: length-prefixed injective encoding
        # len("TEST-123") == 8, len("feature-42") == 10
        assert config["configurable"]["thread_id"] == "work-on-issue-8:TEST-123--worktree-10:feature-42"

        # The checkpointer must receive the resolved db path so the lock, thread,
        # and checkpoint all share the same state_dir scope.
        mock_checkpointer.assert_called_once_with(
            state_dir=scoped_state_dir,
            worktree_key="feature-42",
        )

    def test_thread_id_uses_bootstrap_worktree_key_not_state_dir_name(self, tmp_path):
        """Thread ID uses bootstrap worktree key even when state_dir has a different basename.

        When AGENTIC_DEVTOOLS_STATE_DIR or a validated pin resolves to a directory
        whose basename differs from the active worktree key, the thread identity must
        still carry the bootstrap worktree key (FR-004), not the directory name.
        """
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        # Simulate an env-override path: basename is "checkpoints", unrelated to
        # the bootstrap worktree_key "feature-99".
        override_state_dir = tmp_path / "checkpoints"
        override_state_dir.mkdir()

        with (
            patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer,
            patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build,
            patch("agentic_devtools.state.get_state_dir", return_value=override_state_dir),
            patch(
                "agentic_devtools.state.get_bootstrap_state",
                return_value={"worktree_key": "feature-99"},
            ),
        ):
            mock_checkpointer.return_value = MagicMock()
            mock_build.return_value = mock_compiled
            from agentic_devtools.orchestration.runner import run_langchain_workflow

            run_langchain_workflow("TEST-123")

        config = mock_compiled.invoke.call_args.kwargs["config"]
        thread_id = config["configurable"]["thread_id"]
        # Must use the bootstrap worktree_key ("feature-99"), not the dir name ("checkpoints").
        # len("TEST-123") == 8, len("feature-99") == 10
        assert thread_id == "work-on-issue-8:TEST-123--worktree-10:feature-99"
        assert "checkpoints" not in thread_id

        # Database is still resolved from the overridden state_dir.
        mock_checkpointer.assert_called_once_with(
            state_dir=override_state_dir,
            worktree_key="feature-99",
        )

    def test_missing_bootstrap_worktree_key_fails_closed(self, capsys):
        """Runner exits when bootstrap state has no valid worktree key.

        FR-004 requires failing closed rather than constructing an identity
        that could collide with a keyed worktree.
        """
        mock_compiled = MagicMock()

        with (
            patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer,
            patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build,
            patch("agentic_devtools.state.get_bootstrap_state", return_value={}),
        ):
            mock_checkpointer.return_value = MagicMock()
            mock_build.return_value = mock_compiled
            from agentic_devtools.orchestration.runner import run_langchain_workflow

            with pytest.raises(SystemExit) as exc_info:
                run_langchain_workflow("TEST-NOKEY")

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "No valid worktree key" in captured.err
        mock_compiled.invoke.assert_not_called()

    def test_explicit_worktree_key_bypasses_bootstrap(self, tmp_path):
        """Explicit worktree_key parameter takes precedence over bootstrap state.

        When AGENTIC_DEVTOOLS_STATE_DIR is set, _ensure_bootstrap_identity_and_scope
        skips set_bootstrap_state(), leaving bootstrap state empty.  The caller
        propagates the invocation worktree key via the worktree_key parameter so
        the runner does not need to consult bootstrap state.
        """
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        override_state_dir = tmp_path / "explicit-scope"
        override_state_dir.mkdir()

        with (
            patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer,
            patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build,
            patch("agentic_devtools.state.get_state_dir", return_value=override_state_dir),
            # Bootstrap returns empty — simulates AGENTIC_DEVTOOLS_STATE_DIR override path.
            patch("agentic_devtools.state.get_bootstrap_state", return_value={}),
        ):
            mock_checkpointer.return_value = MagicMock()
            mock_build.return_value = mock_compiled
            from agentic_devtools.orchestration.runner import run_langchain_workflow

            run_langchain_workflow("TEST-456", worktree_key="PROJECT-456")

        config = mock_compiled.invoke.call_args.kwargs["config"]
        thread_id = config["configurable"]["thread_id"]
        # len("TEST-456") == 8, len("PROJECT-456") == 11
        assert thread_id == "work-on-issue-8:TEST-456--worktree-11:PROJECT-456"

    def test_unscoped_state_dir_fails_closed(self, tmp_path, capsys):
        """Runner exits when get_state_dir() returns the _unscoped fallback.

        An _unscoped directory means bootstrap has not been fully initialised.
        Writing checkpoints there would interleave state from multiple worktrees
        and break the isolation contract, so the runner must fail closed even
        when an explicit worktree_key passes validation.
        """
        unscoped_dir = tmp_path / ".agdt" / "workflows" / "_unscoped"
        unscoped_dir.mkdir(parents=True)

        with (
            patch("agentic_devtools.state.get_state_dir", return_value=unscoped_dir),
            patch("agentic_devtools.state.get_repo_root", return_value=tmp_path),
        ):
            from agentic_devtools.orchestration.runner import run_langchain_workflow

            with pytest.raises(SystemExit) as exc_info:
                run_langchain_workflow("TEST-123", worktree_key="valid-key")

        assert exc_info.value.code == 1
        assert "unscoped fallback" in capsys.readouterr().err

    def test_agdt_temp_state_dir_fails_closed(self, tmp_path, capsys, monkeypatch):
        """Runner exits when get_state_dir() returns the .agdt-temp fallback.

        The .agdt-temp path is the last-resort fallback used when not in a git
        repo.  Checkpoints must never be written there because isolation cannot
        be guaranteed outside a repository context.
        """
        agdt_temp_dir = tmp_path / ".agdt-temp"
        agdt_temp_dir.mkdir()
        monkeypatch.chdir(tmp_path)

        with (
            patch("agentic_devtools.state.get_state_dir", return_value=agdt_temp_dir),
            patch("agentic_devtools.state.get_repo_root", return_value=None),
        ):
            from agentic_devtools.orchestration.runner import run_langchain_workflow

            with pytest.raises(SystemExit) as exc_info:
                run_langchain_workflow("TEST-123", worktree_key="valid-key")

        assert exc_info.value.code == 1
        assert "unscoped fallback" in capsys.readouterr().err

    def test_explicit_invalid_worktree_key_fails_closed(self, capsys):
        """Explicit non-None worktree_key that fails validation exits rather than falling back.

        Only None is treated as "not provided".  An explicit invalid key (e.g.
        containing path separators) must produce an error rather than silently
        falling back to bootstrap state, which could select the wrong checkpoint
        thread from a prior workflow.
        """
        with (
            patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer,
            patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build,
        ):
            mock_checkpointer.return_value = MagicMock()
            mock_build.return_value = MagicMock()
            from agentic_devtools.orchestration.runner import run_langchain_workflow

            with pytest.raises(SystemExit) as exc_info:
                run_langchain_workflow("TEST-123", worktree_key="invalid/key")

        assert exc_info.value.code == 1
        err = capsys.readouterr().err
        assert "not a valid scope identifier" in err
        # Must not fall back to bootstrap — the bootstrap mock provides a valid key
        # but the explicit invalid key should be rejected before bootstrap is consulted.

    def test_explicit_whitespace_only_worktree_key_fails_closed(self, capsys):
        """An explicit worktree_key of only whitespace is invalid and must fail closed.

        Before this fix the truthy check ``if worktree_key and ...`` treated a
        whitespace-only string as falsy (after stripping inside is_safe_dir_segment)
        and fell back to bootstrap state.  Now only None is "absent"; a non-None
        value that strips to empty is rejected explicitly.
        """
        with (
            patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer,
            patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build,
        ):
            mock_checkpointer.return_value = MagicMock()
            mock_build.return_value = MagicMock()
            from agentic_devtools.orchestration.runner import run_langchain_workflow

            with pytest.raises(SystemExit) as exc_info:
                run_langchain_workflow("TEST-123", worktree_key="   ")

        assert exc_info.value.code == 1
        assert "not a valid scope identifier" in capsys.readouterr().err

    def test_explicit_padded_worktree_key_is_normalized(self, tmp_path):
        """Explicit worktree_key with surrounding whitespace is stripped before use.

        is_safe_dir_segment() strips internally before validating, but the runner
        must also strip so that the thread ID contains the normalized form rather
        than the raw padded string.
        """
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }
        scoped_dir = tmp_path / "padded-key"
        scoped_dir.mkdir()

        with (
            patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer,
            patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build,
            patch("agentic_devtools.state.get_state_dir", return_value=scoped_dir),
            patch("agentic_devtools.state.get_bootstrap_state", return_value={}),
        ):
            mock_checkpointer.return_value = MagicMock()
            mock_build.return_value = mock_compiled
            from agentic_devtools.orchestration.runner import run_langchain_workflow

            run_langchain_workflow("TEST-789", worktree_key="  valid-key  ")

        config = mock_compiled.invoke.call_args.kwargs["config"]
        thread_id = config["configurable"]["thread_id"]
        # len("TEST-789") == 8, stripped "valid-key" == 9 bytes — NOT " valid-key " (11 bytes)
        assert thread_id == "work-on-issue-8:TEST-789--worktree-9:valid-key"

    def test_canonical_state_dir_mismatch_fails_closed(self, tmp_path, capsys):
        """Canonical scoped paths must agree with the validated active worktree key."""
        repo_root = tmp_path
        mismatched_state_dir = repo_root / ".agdt" / "workflows" / "tester" / "WORKTREE-A"
        mismatched_state_dir.mkdir(parents=True)

        with (
            patch("agentic_devtools.state.get_repo_root", return_value=repo_root),
            patch("agentic_devtools.state.get_state_dir", return_value=mismatched_state_dir),
            patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer,
            patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build,
        ):
            mock_checkpointer.return_value = MagicMock()
            mock_build.return_value = MagicMock()
            from agentic_devtools.orchestration.runner import run_langchain_workflow

            with pytest.raises(SystemExit) as exc_info:
                run_langchain_workflow("TEST-123", worktree_key="WORKTREE-B")

        assert exc_info.value.code == 1
        err = capsys.readouterr().err
        assert "pinned to worktree scope 'WORKTREE-A'" in err
        assert "active worktree key is 'WORKTREE-B'" in err
        mock_checkpointer.assert_not_called()
        mock_build.assert_not_called()

    def test_effective_state_dir_redirect_failure_exits(self, capsys):
        """Redirect to canonical directory raising ValueError causes a clean exit."""
        with patch(
            "agentic_devtools.orchestration.checkpointing.resolve_effective_workflow_state_dir",
            side_effect=ValueError("redirect identity unavailable"),
        ) as mock_resolve:
            with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer:
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                with pytest.raises(SystemExit) as exc_info:
                    run_langchain_workflow("TEST-123", worktree_key="test-worktree")

        assert exc_info.value.code == 1
        assert "redirect identity unavailable" in capsys.readouterr().err
        mock_resolve.assert_called_once()
        mock_checkpointer.assert_not_called()

    def test_integer_issue_key_encodes_as_string(self, tmp_path):
        """Integer issue_key (from JSON-parsed state) must not raise AttributeError.

        agdt-set JSON-parses numeric values, so jira.issue_key may be an int.
        The runner must coerce it to str before measuring its UTF-8 byte length.
        """
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with (
            patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer,
            patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build,
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
        ):
            mock_checkpointer.return_value = MagicMock()
            mock_build.return_value = mock_compiled
            from agentic_devtools.orchestration.runner import run_langchain_workflow

            # Pass an integer issue_key — mirrors state-backed callers.
            # The conftest autouse fixture provides worktree_key="test-worktree".
            run_langchain_workflow(42, worktree_key="test-worktree")  # type: ignore[arg-type]

        config = mock_compiled.invoke.call_args.kwargs["config"]
        initial_state = mock_compiled.invoke.call_args[0][0]
        thread_id = config["configurable"]["thread_id"]
        # str(42) == "42" (2 bytes), "test-worktree" == 13 bytes
        assert thread_id == "work-on-issue-2:42--worktree-13:test-worktree"
        assert initial_state["issue_key"] == "42"

    def test_non_string_non_integer_issue_key_exits_with_error(self, tmp_path, capsys):
        """issue_key of an unsupported type (e.g. float, bool) must be rejected.

        Only str and plain int are accepted; any other type is malformed state
        that must fail closed rather than being silently coerced.
        """
        from agentic_devtools.orchestration.runner import run_langchain_workflow

        with pytest.raises(SystemExit) as exc_info:
            run_langchain_workflow(1.5, worktree_key="test-worktree")  # type: ignore[arg-type]

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "issue_key must be a string or integer" in captured.err
        assert "float" in captured.err

    def test_fresh_invocation_calls_graph_invoke(self, tmp_path, capsys):
        """Fresh invocation builds graph and invokes with initial state."""
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer:
            mock_checkpointer.return_value = MagicMock()
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                run_langchain_workflow("TEST-123", interactive=True, model="gpt-4")

        # Verify graph was invoked with correct initial state
        call_args = mock_compiled.invoke.call_args
        initial_state = call_args[0][0]
        assert initial_state["issue_key"] == "TEST-123"
        assert initial_state["agent_context"]["interactive"] is True
        assert initial_state["agent_context"]["model"] == "gpt-4"

        captured = capsys.readouterr()
        assert "[langchain] Starting workflow for TEST-123" in captured.out
        assert "[langchain] Workflow completed" in captured.out

    def test_fresh_invocation_seeds_retry_budget_from_policy(self):
        """Fresh invocation carries the loaded retry budget into workflow state."""
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer:
            mock_checkpointer.return_value = MagicMock()
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                with patch(
                    "agentic_devtools.orchestration.runner._initialize_infrastructure",
                    return_value={"retry_budget": 5},
                ):
                    from agentic_devtools.orchestration.runner import run_langchain_workflow

                    run_langchain_workflow("TEST-123")

        call_args = mock_compiled.invoke.call_args
        initial_state = call_args[0][0]
        assert initial_state["retry_budget"] == 5

    def test_fresh_invocation_seeds_dry_run_from_execution_mode(self):
        """Fresh invocation seeds effective dry-run mode into workflow state."""
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer:
            mock_checkpointer.return_value = MagicMock()
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                with patch("agentic_devtools.orchestration.safety.mode.resolve_execution_mode_from_state") as mock_mode:
                    from agentic_devtools.orchestration.runner import run_langchain_workflow
                    from agentic_devtools.orchestration.safety.mode import ExecutionMode

                    mock_mode.return_value = ExecutionMode.dry_run
                    run_langchain_workflow("TEST-123")

        call_args = mock_compiled.invoke.call_args
        initial_state = call_args[0][0]
        assert initial_state["dry_run"] is True

    def test_restricted_mode_fails_closed_before_graph_invoke(self, capsys):
        """Restricted mode must abort because workflow contains local mutations."""
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer:
            mock_checkpointer.return_value = MagicMock()
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                with patch("agentic_devtools.orchestration.safety.mode.resolve_execution_mode_from_state") as mock_mode:
                    from agentic_devtools.orchestration.runner import run_langchain_workflow
                    from agentic_devtools.orchestration.safety.mode import ExecutionMode

                    mock_mode.return_value = ExecutionMode.restricted
                    with pytest.raises(SystemExit) as exc_info:
                        run_langchain_workflow("TEST-123")

                    assert exc_info.value.code == 1

        mock_compiled.invoke.assert_not_called()
        captured = capsys.readouterr()
        assert "execution_mode=restricted is read-only" in captured.err

    def test_fresh_invocation_handles_graph_interrupt(self, capsys):
        """Fresh invocation handles GraphInterrupt for human-in-the-loop pause."""
        mock_compiled = MagicMock()

        # Simulate GraphInterrupt
        class GraphInterrupt(Exception):
            pass

        mock_compiled.invoke.side_effect = GraphInterrupt("Waiting for approval")

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer:
            mock_checkpointer.return_value = MagicMock()
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                # Should not raise, should print resume instructions
                run_langchain_workflow("TEST-456")

        captured = capsys.readouterr()
        assert "paused" in captured.err
        assert "--resume" in captured.err

    def test_fresh_invocation_non_interrupt_error_exits(self, capsys):
        """Fresh invocation with non-GraphInterrupt error exits with code 1."""
        mock_compiled = MagicMock()
        mock_compiled.invoke.side_effect = RuntimeError("Something went wrong")

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer:
            mock_checkpointer.return_value = MagicMock()
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                with pytest.raises(SystemExit) as exc_info:
                    run_langchain_workflow("TEST-456")

                assert exc_info.value.code == 1
                captured = capsys.readouterr()
                assert "Workflow execution failed" in captured.err

    def test_fresh_invocation_pauses_when_status_not_completed(self, capsys):
        """Fresh invocation prints pause message when invoke returns non-completed status."""
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "planning",
            "status": "active",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer:
            mock_checkpointer.return_value = MagicMock()
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                run_langchain_workflow("TEST-456")

        captured = capsys.readouterr()
        assert "paused" in captured.err
        assert "--resume" in captured.err
        assert "Workflow completed" not in captured.out

    def test_fresh_invocation_pauses_when_status_empty(self, capsys):
        """Fresh invocation prints pause message when invoke returns empty status."""
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "initialization",
            "status": "",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer:
            mock_checkpointer.return_value = MagicMock()
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                run_langchain_workflow("TEST-456")

        captured = capsys.readouterr()
        assert "paused" in captured.err
        assert "Workflow completed" not in captured.out

    @pytest.mark.parametrize("status", ["failed", "blocked"])
    def test_fresh_invocation_exits_for_terminal_failure_statuses(self, capsys, status):
        """Fresh invocation exits non-zero for terminal failure statuses."""
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "error_handler",
            "status": status,
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_checkpointer:
            mock_checkpointer.return_value = MagicMock()
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                with pytest.raises(SystemExit) as exc_info:
                    run_langchain_workflow("TEST-456")

                assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "paused" not in captured.err
        assert "Workflow completed" not in captured.out
        assert f"ERROR: Workflow terminated unsuccessfully: step=error_handler, status={status}" in captured.err


class TestRunLangchainWorkflowResume:
    """Tests for resume path in LangGraph workflow."""

    def test_resume_with_no_checkpoint_exits(self, capsys):
        """Resume with no existing checkpoint exits with error."""
        mock_checkpointer = MagicMock()
        mock_checkpointer.get.return_value = None

        mock_compiled = MagicMock()

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                with pytest.raises(SystemExit) as exc_info:
                    run_langchain_workflow("TEST-789", resume=True)

                assert exc_info.value.code == 1
                captured = capsys.readouterr()
                assert "No existing checkpoint" in captured.err

    def test_resume_with_existing_checkpoint_invokes_command(self, capsys):
        """Resume with existing checkpoint invokes graph with Command(resume=True)."""
        mock_checkpointer = MagicMock()
        mock_checkpointer.get.return_value = {"some": "checkpoint"}

        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                run_langchain_workflow("TEST-789", resume=True)

        captured = capsys.readouterr()
        assert "[langchain] Resuming workflow for TEST-789" in captured.out

    def test_resume_patches_dry_run_into_checkpoint_before_invoke(self, capsys):
        """Resume overwrites checkpoint dry_run with the current execution mode."""
        mock_checkpointer = MagicMock()
        mock_checkpointer.get.return_value = {"some": "checkpoint"}

        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                with patch("agentic_devtools.orchestration.safety.mode.resolve_execution_mode_from_state") as mock_mode:
                    from agentic_devtools.orchestration.runner import run_langchain_workflow
                    from agentic_devtools.orchestration.safety.mode import ExecutionMode

                    mock_mode.return_value = ExecutionMode.dry_run
                    run_langchain_workflow("TEST-789", resume=True)

        # update_state must have been called with dry_run=True and run_id before invoke
        mock_compiled.update_state.assert_called_once()
        update_call = mock_compiled.update_state.call_args
        update_dict = update_call[0][1]
        assert update_dict.get("dry_run") is True
        assert isinstance(update_dict.get("run_id"), str)

        # invoke must follow update_state
        assert mock_compiled.invoke.call_count == 1

    def test_resume_with_resume_data_passes_data_to_command(self, capsys):
        """Resume with resume_data passes structured data to Command(resume=...)."""
        mock_checkpointer = MagicMock()
        mock_checkpointer.get.return_value = {"some": "checkpoint"}

        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        resume_payload = {"completed": True, "summary": "Work done"}

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                run_langchain_workflow("TEST-789", resume=True, resume_data=resume_payload)

        # Verify Command was called with the resume data
        call_args = mock_compiled.invoke.call_args
        command_arg = call_args[0][0]
        # The Command object should have resume=resume_payload
        assert command_arg.resume == resume_payload

    def test_resume_failure_exits_with_error(self, capsys):
        """Resume failure exits with error code 1."""
        mock_checkpointer = MagicMock()
        mock_checkpointer.get.return_value = {"some": "checkpoint"}

        mock_compiled = MagicMock()
        mock_compiled.invoke.side_effect = RuntimeError("Resume failed")

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                with pytest.raises(SystemExit) as exc_info:
                    run_langchain_workflow("TEST-789", resume=True)

                assert exc_info.value.code == 1
                captured = capsys.readouterr()
                assert "Workflow resume failed" in captured.err

    def test_resume_handles_graph_interrupt(self, capsys):
        """Resume path handles GraphInterrupt for a later gate pause."""
        mock_checkpointer = MagicMock()
        mock_checkpointer.get.return_value = {"some": "checkpoint"}

        mock_compiled = MagicMock()

        # Simulate GraphInterrupt during resume
        class GraphInterrupt(Exception):
            pass

        mock_compiled.invoke.side_effect = GraphInterrupt("Waiting for next gate")

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                # Should not raise, should print pause/resume instructions
                run_langchain_workflow("TEST-789", resume=True)

        captured = capsys.readouterr()
        assert "paused" in captured.err
        assert "--resume" in captured.err

    def test_resume_pauses_when_status_not_completed(self, capsys):
        """Resume prints pause message when invoke returns non-completed status."""
        mock_checkpointer = MagicMock()
        mock_checkpointer.get.return_value = {"some": "checkpoint"}

        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "commit",
            "status": "active",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                run_langchain_workflow("TEST-789", resume=True)

        captured = capsys.readouterr()
        assert "paused" in captured.err
        assert "--resume" in captured.err
        assert "Workflow completed" not in captured.out

    @pytest.mark.parametrize("status", ["failed", "blocked"])
    def test_resume_exits_for_terminal_failure_statuses(self, capsys, status):
        """Resume exits non-zero for terminal failure statuses."""
        mock_checkpointer = MagicMock()
        mock_checkpointer.get.return_value = {"some": "checkpoint"}

        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": status,
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                with pytest.raises(SystemExit) as exc_info:
                    run_langchain_workflow("TEST-789", resume=True)

                assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "paused" not in captured.err
        assert "Workflow completed" not in captured.out
        assert f"ERROR: Workflow terminated unsuccessfully: step=completion, status={status}" in captured.err


class TestRunLangchainWorkflowLockFailure:
    """Tests for ExecutionLock acquisition failure path."""

    def test_lock_failure_exits_without_initializing_checkpointer(self, capsys):
        """Lock acquisition failure exits before checkpointer setup starts."""
        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            with patch("agentic_devtools.orchestration.execution_lock.ExecutionLock.acquire") as mock_acquire:
                mock_acquire.side_effect = RuntimeError("Lock held by PID 12345")
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                with pytest.raises(SystemExit) as exc_info:
                    run_langchain_workflow("TEST-LOCK")

                assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Lock held by PID 12345" in captured.err
        mock_get_cp.assert_not_called()

    def test_lock_failure_before_checkpointer_initialization_exits_cleanly(self, capsys):
        """Lock failure path exits cleanly before checkpointer initialization begins."""
        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            with patch("agentic_devtools.orchestration.execution_lock.ExecutionLock.acquire") as mock_acquire:
                mock_acquire.side_effect = RuntimeError("Lock held")
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                with pytest.raises(SystemExit) as exc_info:
                    run_langchain_workflow("TEST-LOCK2")

                assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Lock held" in captured.err
        mock_get_cp.assert_not_called()

    def test_lock_released_when_get_checkpointer_raises(self, tmp_path):
        """Lock is released when get_checkpointer() raises after lock acquisition."""
        from agentic_devtools.orchestration.runner import run_langchain_workflow

        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
        ):
            with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
                mock_get_cp.side_effect = RuntimeError("SQLite open failure")
                with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph"):
                    with pytest.raises(RuntimeError, match="SQLite open failure"):
                        run_langchain_workflow("TEST-LOCK3")

        # Lock directory exists because acquire() created it; the lock file itself
        # must have been removed by release() in the finally block.
        # FR-004: length-prefixed encoding; conftest default worktree_key is "test-worktree" (13 bytes)
        # len("TEST-LOCK3") == 10, len("test-worktree") == 13
        thread_id = "work-on-issue-10:TEST-LOCK3--worktree-13:test-worktree"
        lock_file = tmp_path / "locks" / f"{hashlib.sha256(thread_id.encode('utf-8')).hexdigest()}.lock"
        assert not lock_file.exists(), "Stale lock file left behind after get_checkpointer() failure"


class TestRunLangchainWorkflowRunIdRestore:
    """Tests for run_id restoration from checkpoint on resume."""

    @staticmethod
    def _make_state_snapshot(values: dict) -> MagicMock:
        """Return a MagicMock that behaves like a LangGraph StateSnapshot."""
        snap = MagicMock()
        snap.values = values
        return snap

    def test_resume_restores_run_id_from_plain_dict_checkpoint(self, capsys):
        """Resume restores run_id from compiled.get_state().values."""
        stored_run_id = "restored-uuid-from-checkpoint"
        mock_checkpointer = MagicMock()
        mock_checkpointer.get.return_value = {"some": "checkpoint"}

        mock_compiled = MagicMock()
        # StateSnapshot returned by compiled.get_state() carries run_id in .values
        mock_compiled.get_state.return_value = self._make_state_snapshot({"run_id": stored_run_id, "step": "planning"})
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                run_langchain_workflow("TEST-RUNID", resume=True)

        # Verify the config passed to invoke contains the restored run_id
        call_args = mock_compiled.invoke.call_args
        config_arg = call_args[1]["config"]
        assert config_arg["configurable"]["run_id"] == stored_run_id

    def test_resume_generates_fresh_run_id_when_checkpoint_is_non_dict_object(self, capsys):
        """Resume generates a fresh run_id when compiled.get_state() returns None.

        SqliteSaver.get() returns a CheckpointTuple, not a plain dict.  The
        runner now uses compiled.get_state() to read channel values.  When
        get_state() returns None (no checkpoint exists), a fresh UUID4 is used.
        """
        mock_checkpointer = MagicMock()
        # Second checkpointer.get() call (existence check) returns non-None so the
        # test does not exit early — it proceeds to verify fresh UUID generation.
        mock_checkpointer.get.return_value = SimpleNamespace(config={})

        mock_compiled = MagicMock()
        # No StateSnapshot available → run_id cannot be restored.
        mock_compiled.get_state.return_value = None
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                run_langchain_workflow("TEST-RUNID-TUPLE", resume=True)

        call_args = mock_compiled.invoke.call_args
        config_arg = call_args[1]["config"]
        # no snapshot → fresh UUID generated
        assert config_arg["configurable"]["run_id"]

    def test_resume_restores_run_id_from_graph_state_top_level_key(self, capsys):
        """Resume reads run_id from StateSnapshot.values, not from nested config."""
        stored_run_id = "restored-from-graph-state"

        mock_checkpointer = MagicMock()
        mock_checkpointer.get.return_value = {"some": "checkpoint"}

        mock_compiled = MagicMock()
        mock_compiled.get_state.return_value = self._make_state_snapshot({"run_id": stored_run_id, "step": "planning"})
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                run_langchain_workflow("TEST-RUNID-TUPLE-PREFERRED", resume=True)

        call_args = mock_compiled.invoke.call_args
        config_arg = call_args[1]["config"]
        assert config_arg["configurable"]["run_id"] == stored_run_id

    def test_resume_generates_fresh_run_id_when_state_dict_has_no_run_id(self, capsys):
        """Resume generates a fresh UUID when the StateSnapshot has no run_id key."""
        mock_checkpointer = MagicMock()
        mock_checkpointer.get.return_value = {"some": "checkpoint"}

        mock_compiled = MagicMock()
        # StateSnapshot exists but run_id was not persisted (pre-run_id checkpoint)
        mock_compiled.get_state.return_value = self._make_state_snapshot({"step": "planning", "issue_key": "TEST-123"})
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                run_langchain_workflow("TEST-RUNID-TUPLE-NO-RUNID", resume=True)

        call_args = mock_compiled.invoke.call_args
        config_arg = call_args[1]["config"]
        assert config_arg["configurable"]["run_id"]

    def test_resume_generates_fresh_run_id_when_not_in_checkpoint(self, capsys):
        """Resume generates a fresh run_id when the StateSnapshot holds no run_id."""
        mock_checkpointer = MagicMock()
        mock_checkpointer.get.return_value = {"some": "checkpoint"}

        mock_compiled = MagicMock()
        mock_compiled.get_state.return_value = self._make_state_snapshot({"step": "planning"})
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                run_langchain_workflow("TEST-RUNID-FRESH", resume=True)

        call_args = mock_compiled.invoke.call_args
        config_arg = call_args[1]["config"]
        # run_id is still populated (freshly generated)
        assert config_arg["configurable"]["run_id"]

    def test_resume_generates_fresh_run_id_when_checkpoint_has_unknown_shape(self, capsys):
        """Resume generates a fresh run_id when compiled.get_state() returns None.

        When there is no restorable channel-values snapshot, run_id is populated
        via UUID4 fallback.
        """
        mock_checkpointer = MagicMock()
        mock_checkpointer.get.return_value = {"some": "checkpoint"}

        mock_compiled = MagicMock()
        mock_compiled.get_state.return_value = None
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                run_langchain_workflow("TEST-RUNID-UNKNOWN", resume=True)

        call_args = mock_compiled.invoke.call_args
        config_arg = call_args[1]["config"]
        # run_id must be populated with a freshly generated UUID
        assert config_arg["configurable"]["run_id"]

    def test_resume_restores_run_id_from_graph_state(self, capsys):
        """Resume reads run_id from StateSnapshot.values via compiled.get_state()."""
        stored_run_id = "restored-from-graph-state"
        mock_checkpointer = MagicMock()
        mock_checkpointer.get.return_value = {"some": "checkpoint"}

        mock_compiled = MagicMock()
        mock_compiled.get_state.return_value = self._make_state_snapshot({"run_id": stored_run_id, "step": "planning"})
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                run_langchain_workflow("TEST-RUNID-NO-GET-TUPLE", resume=True)

        call_args = mock_compiled.invoke.call_args
        config_arg = call_args[1]["config"]
        assert config_arg["configurable"]["run_id"] == stored_run_id

    def test_resume_exits_when_checkpoint_not_found(self, capsys):
        """Resume exits when checkpointer.get() returns None (no prior checkpoint)."""
        mock_checkpointer = MagicMock()
        mock_checkpointer.get.return_value = None

        mock_compiled = MagicMock()
        mock_compiled.get_state.return_value = None

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                with pytest.raises(SystemExit) as exc_info:
                    run_langchain_workflow("TEST-RUNID-NO-CHECKPOINT", resume=True)

        assert exc_info.value.code == 1
        mock_compiled.invoke.assert_not_called()

    def test_resume_generates_fresh_run_id_for_non_dict_checkpoint_payload(self, capsys):
        """Resume generates a fresh run_id when compiled.get_state() returns None."""
        mock_checkpointer = MagicMock()
        mock_checkpointer.get.return_value = {"some": "checkpoint"}

        mock_compiled = MagicMock()
        mock_compiled.get_state.return_value = None
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                run_langchain_workflow("TEST-RUNID-NON-DICT", resume=True)

        call_args = mock_compiled.invoke.call_args
        config_arg = call_args[1]["config"]
        assert config_arg["configurable"]["run_id"]

    def test_resume_generates_fresh_run_id_for_non_string_stored_run_id(self, capsys):
        """Resume generates a fresh run_id when the stored run_id is not a non-empty string."""
        mock_checkpointer = MagicMock()
        mock_checkpointer.get.return_value = {"some": "checkpoint"}

        mock_compiled = MagicMock()
        # StateSnapshot with a non-string run_id (e.g. stored as int due to a bug)
        mock_compiled.get_state.return_value = self._make_state_snapshot({"run_id": 123, "step": "planning"})
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                run_langchain_workflow("TEST-RUNID-NON-STRING", resume=True)

        call_args = mock_compiled.invoke.call_args
        config_arg = call_args[1]["config"]
        assert isinstance(config_arg["configurable"]["run_id"], str)
        assert config_arg["configurable"]["run_id"]

    def test_resume_preserves_dry_run_when_checkpoint_had_dry_run_true_and_current_mode_is_live(self, capsys):
        """When a checkpoint was created in dry-run mode, resume preserves dry_run=True even if current mode is live."""
        mock_checkpointer = MagicMock()
        mock_checkpointer.get.return_value = {"some": "checkpoint"}

        mock_compiled = MagicMock()
        # Checkpoint was started in dry_run mode
        mock_compiled.get_state.return_value = self._make_state_snapshot({"dry_run": True})
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                with patch("agentic_devtools.orchestration.safety.mode.resolve_execution_mode_from_state") as mock_mode:
                    from agentic_devtools.orchestration.runner import run_langchain_workflow
                    from agentic_devtools.orchestration.safety.mode import ExecutionMode

                    # Current mode is live (dry_run_enabled=False)
                    mock_mode.return_value = ExecutionMode.live
                    run_langchain_workflow("TEST-DRY-PRESERVE", resume=True)

        # update_state must have been called with dry_run=True (preserved from checkpoint)
        mock_compiled.update_state.assert_called_once()
        update_call = mock_compiled.update_state.call_args
        update_dict = update_call[0][1]
        assert update_dict.get("dry_run") is True

        # Warning must be printed to stderr
        captured = capsys.readouterr()
        assert "dry_run=True preserved from checkpoint" in captured.err
        assert "Start a new session with execution_mode=live" in captured.err


class TestRunLangchainWorkflowCheckpointerCleanup:
    """Tests for checkpointer connection cleanup."""

    def test_checkpointer_connection_closed_on_success(self, capsys):
        """Checkpointer connection is closed after successful invocation."""
        mock_conn = MagicMock()
        mock_checkpointer = MagicMock()
        mock_checkpointer.conn = mock_conn

        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                run_langchain_workflow("TEST-123")

        mock_conn.close.assert_called_once()

    def test_checkpointer_connection_closed_on_error(self, capsys):
        """Checkpointer connection is closed even when invocation fails."""
        mock_conn = MagicMock()
        mock_checkpointer = MagicMock()
        mock_checkpointer.conn = mock_conn

        mock_compiled = MagicMock()
        mock_compiled.invoke.side_effect = RuntimeError("fail")

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                with pytest.raises(SystemExit):
                    run_langchain_workflow("TEST-123")

        mock_conn.close.assert_called_once()

    def test_checkpointer_without_conn_attribute_does_not_crash(self, capsys):
        """Checkpointer without a conn attribute does not crash on cleanup."""
        mock_checkpointer = MagicMock(spec=[])  # no attributes

        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "step": "completion",
            "status": "completed",
            "events": [],
        }

        with patch("agentic_devtools.orchestration.checkpointing.get_checkpointer") as mock_get_cp:
            mock_get_cp.return_value = mock_checkpointer
            with patch("agentic_devtools.orchestration.graph_builder.build_work_on_issue_graph") as mock_build:
                mock_build.return_value = mock_compiled
                from agentic_devtools.orchestration.runner import run_langchain_workflow

                # Should not raise
                run_langchain_workflow("TEST-123")
