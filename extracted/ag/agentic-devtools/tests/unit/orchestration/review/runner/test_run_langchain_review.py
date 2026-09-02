"""Tests for run_langchain_review()."""

from __future__ import annotations

import builtins
import json
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.orchestration.review.runner import (
    run_langchain_review,
    run_langchain_review_background,
)


class TestRunLangchainReview:
    """Tests for the review runner."""

    @pytest.fixture(autouse=True)
    def skip_provider_preflight(self, monkeypatch) -> None:
        """Keep graph-runner unit tests independent from repository LLM config."""
        monkeypatch.setattr(
            "agentic_devtools.orchestration.review.runner._validate_provider_configuration",
            lambda _model_config=None, requested_model=None, config_path=None: None,
        )

    @patch("agentic_devtools.orchestration.review.runner.build_review_graph")
    def test_invokes_graph_with_initial_state(self, mock_build) -> None:
        """run_langchain_review invokes the compiled graph."""
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {
            "overall_decision": "approve",
            "summary": "All good",
            "errors": [],
        }
        mock_build.return_value = mock_compiled

        result = run_langchain_review(123)

        mock_build.assert_called_once()
        mock_compiled.invoke.assert_called_once()
        call_args = mock_compiled.invoke.call_args.args[0]
        assert call_args["pr_id"] == 123
        assert call_args["files"] == []
        assert result["overall_decision"] == "approve"

    @patch("agentic_devtools.orchestration.review.runner.build_review_graph")
    def test_status_messages_go_to_stderr(self, mock_build, capsys) -> None:
        """Human-readable status messages are written to stderr by the runner itself.

        The runner's own code does not write to stdout; structured JSON output
        on success is emitted by the post_results graph node (NFR-003), which
        is mocked here and therefore produces no stdout output in this test.
        """
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {}
        mock_build.return_value = mock_compiled

        run_langchain_review(123)

        captured = capsys.readouterr()
        assert "[langchain-review] Starting review for PR #123..." in captured.err
        assert "[langchain-review] Review completed for PR #123" in captured.err
        assert captured.out == ""

    @patch("agentic_devtools.orchestration.review.runner.build_review_graph")
    def test_handles_graph_error(self, mock_build, capsys) -> None:
        """Returns error output when graph execution fails."""
        mock_compiled = MagicMock()
        mock_compiled.invoke.side_effect = RuntimeError("graph exploded")
        mock_build.return_value = mock_compiled

        result = run_langchain_review(456)

        assert result["status"] == "failed"
        assert "graph exploded" in result["error"]
        assert json.loads(capsys.readouterr().out) == result

    @patch("agentic_devtools.orchestration.review.runner.build_review_graph")
    @patch("agentic_devtools.orchestration.review.runner._validate_provider_configuration")
    def test_provider_configuration_failure_precedes_graph_execution(self, mock_validate, mock_build, capsys) -> None:
        """Provider configuration failure is returned before the graph is built."""
        mock_validate.side_effect = RuntimeError(
            "LangChain provider configuration is unavailable: no credentials. "
            "Configure .agdt/config/llm-providers.yml and its required credentials."
        )

        result = run_langchain_review(456, model_config={"default-model": "gemini-3.7-flash"})

        assert result["status"] == "failed"
        assert "provider configuration" in result["error"]
        assert "llm-providers.yml" in result["error"]
        mock_build.assert_not_called()
        assert json.loads(capsys.readouterr().out) == result

    @patch("agentic_devtools.orchestration.review.runner.build_review_graph")
    def test_passes_source_context_flag(self, mock_build) -> None:
        """Source context enabled flag is passed to initial state."""
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {}
        mock_build.return_value = mock_compiled

        run_langchain_review(789, source_context_enabled=False)

        call_args = mock_compiled.invoke.call_args.args[0]
        assert call_args["source_context_enabled"] is False

    @patch("agentic_devtools.orchestration.review.runner.build_review_graph")
    def test_passes_model_config(self, mock_build) -> None:
        """Model config is passed to initial state."""
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {}
        mock_build.return_value = mock_compiled

        model_cfg = {"default-model": "claude-opus-4"}
        run_langchain_review(789, model_config=model_cfg)

        call_args = mock_compiled.invoke.call_args.args[0]
        assert call_args["model_config_raw"] == model_cfg

    @patch("agentic_devtools.orchestration.review.runner.build_review_graph")
    def test_passes_requested_model(self, mock_build) -> None:
        """Explicit requested_model is passed into the initial state."""
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {}
        mock_build.return_value = mock_compiled

        run_langchain_review(789, requested_model="gemini-3.7-flash")

        call_args = mock_compiled.invoke.call_args.args[0]
        assert call_args["requested_model"] == "gemini-3.7-flash"

    @patch("agentic_devtools.orchestration.review.runner.build_review_graph")
    @patch("agentic_devtools.orchestration.review.runner._resolve_llm_config_path")
    def test_passes_llm_config_path_to_initial_state(self, mock_resolve, mock_build) -> None:
        """Resolved LLM config path is forwarded to the graph initial state."""
        from pathlib import Path

        fake_path = Path("/repo/.agdt/config/llm-providers.yml")
        mock_resolve.return_value = fake_path
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {}
        mock_build.return_value = mock_compiled

        run_langchain_review(789)

        call_args = mock_compiled.invoke.call_args.args[0]
        assert call_args["llm_config_path"] == str(fake_path)

    @patch("agentic_devtools.orchestration.review.runner.build_review_graph")
    @patch("agentic_devtools.orchestration.review.runner._resolve_llm_config_path")
    def test_omits_llm_config_path_when_not_resolved(self, mock_resolve, mock_build) -> None:
        """The graph state omits the config path when no repository root is found."""
        mock_resolve.return_value = None
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {}
        mock_build.return_value = mock_compiled

        run_langchain_review(789)

        call_args = mock_compiled.invoke.call_args.args[0]
        assert "llm_config_path" not in call_args

    @patch("agentic_devtools.orchestration.review.runner.build_review_graph")
    @patch("agentic_devtools.orchestration.review.runner._validate_provider_configuration")
    def test_passes_preflighted_provider_factory_to_graph_builder(self, mock_validate, mock_build) -> None:
        """The preflighted provider factory is passed to build_review_graph, not graph state."""
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = {}
        mock_build.return_value = mock_compiled
        sentinel_factory = object()
        mock_validate.return_value = sentinel_factory

        run_langchain_review(789)

        mock_build.assert_called_once_with(provider_factory=sentinel_factory)
        call_args = mock_compiled.invoke.call_args.args[0]
        assert "_provider_factory" not in call_args

    @patch("agentic_devtools.orchestration.review.runner.build_review_graph")
    def test_non_dict_graph_result_returns_empty_dict(self, mock_build) -> None:
        """Non-dict graph results are normalized to an empty dict."""
        mock_compiled = MagicMock()
        mock_compiled.invoke.return_value = "done"
        mock_build.return_value = mock_compiled

        assert run_langchain_review(321) == {}

    def test_exits_when_langgraph_dependency_is_missing(self, capsys) -> None:
        """A helpful error is printed when LangGraph cannot be imported."""
        original_import = builtins.__import__

        def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "langgraph.graph.state":
                raise ImportError("missing")
            return original_import(name, globals, locals, fromlist, level)

        with patch.object(builtins, "__import__", side_effect=fake_import):
            with pytest.raises(SystemExit) as exc_info:
                run_langchain_review(999)

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "LangGraph dependencies are not available" in captured.err
        assert "Install them with:\n  pip install agentic-devtools\n" in captured.err

    @patch("agentic_devtools.task_state.print_task_tracking_info")
    @patch("agentic_devtools.background_tasks.run_function_in_background")
    def test_background_runner_starts_task(self, mock_run, mock_print_tracking) -> None:
        """Background mode delegates to shared background task tracking."""
        mock_task = SimpleNamespace(id="task-123")
        mock_run.return_value = mock_task

        task_id = run_langchain_review_background(
            123,
            source_context_enabled=False,
            model_config={"default-model": "gpt-4o-mini"},
            requested_model="gemini-3.7-flash",
        )

        assert task_id == "task-123"
        mock_run.assert_called_once_with(
            module_path="agentic_devtools.orchestration.review.runner",
            function_name="_run_langchain_review_task",
            command_display_name="langchain-review",
            func_kwargs={
                "pr_id": 123,
                "source_context_enabled": False,
                "model_config": {"default-model": "gpt-4o-mini"},
                "requested_model": "gemini-3.7-flash",
            },
        )
        mock_print_tracking.assert_called_once_with(
            mock_task,
            "Running LangChain review for PR #123",
        )
