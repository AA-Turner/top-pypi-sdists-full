"""Tests for review_files helpers and node."""

from __future__ import annotations

import builtins
import json
import traceback
from contextlib import contextmanager
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.orchestration.review.llm_error_normalizer import TransientLLMError
from agentic_devtools.orchestration.review.nodes.review_files import (
    _build_pre_enriched_context,
    _build_review_prompt,
    _format_numbered_file_content,
    _invoke_llm,
    _resolve_model,
    _review_single_file,
    _update_review_state_for_file,
    review_files_node,
)
from agentic_devtools.orchestration.review.state import (
    FileReviewOutput,
    FileReviewResult,
    SuggestionOutput,
)


class TestReviewFilesNode:
    """Tests for the review_files node wrapper."""

    def test_empty_files_returns_empty_results(self) -> None:
        """Returns empty results when no files to review."""
        result = review_files_node({"files": [], "review_state_path": ""})
        assert result["file_results"] == []
        assert result["errors"] == []

    def test_skips_files_without_path(self) -> None:
        """Skips file entries with no path — provider must NOT be called."""
        # Provider resolution must be skipped entirely; no patch needed or expected.
        result = review_files_node(
            {
                "files": [{"changeType": "edit"}],
                "review_state_path": "",
            }
        )
        assert result["file_results"] == []
        assert result["errors"] == []

    @patch("agentic_devtools.orchestration.llm.factory.get_provider")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._review_single_file")
    def test_skips_pathless_files_in_mixed_list(self, mock_review, mock_get_provider) -> None:
        """Pathless entries are skipped when the list also contains files with paths."""
        mock_review.return_value = FileReviewResult(
            file_path="/src/a.py",
            outcome="approve",
            summary="LGTM",
            model_id="gpt-4o",
        )

        result = review_files_node(
            {
                "files": [
                    {"path": "/src/a.py", "changeType": "edit"},
                    {"changeType": "edit"},  # no path — must be skipped
                ],
                "review_state_path": "",
                "config": {},
            }
        )

        assert len(result["file_results"]) == 1
        assert mock_review.call_count == 1

    @patch("agentic_devtools.orchestration.llm.factory.get_provider")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._review_single_file")
    def test_reviews_each_file(self, mock_review, mock_get_provider) -> None:
        """Calls _review_single_file for each file with a path."""
        mock_review.return_value = FileReviewResult(
            file_path="/src/a.py",
            outcome="approve",
            summary="LGTM",
            model_id="gpt-4o",
        )

        result = review_files_node(
            {
                "files": [
                    {"path": "/src/a.py", "changeType": "edit"},
                    {"path": "/src/b.py", "changeType": "edit"},
                ],
                "review_state_path": "",
                "config": {},
            }
        )

        assert len(result["file_results"]) == 2
        assert mock_review.call_count == 2

    @patch("agentic_devtools.orchestration.review.nodes.review_files._review_single_file")
    def test_uses_injected_provider_factory(self, mock_review) -> None:
        """Uses the injected provider factory when one is passed via closure."""
        mock_provider = MagicMock()
        mock_provider_factory = MagicMock()
        mock_provider_factory.get_provider.return_value = mock_provider
        mock_review.return_value = FileReviewResult(
            file_path="/src/a.py",
            outcome="approve",
            summary="LGTM",
            model_id="gpt-4o",
        )

        result = review_files_node(
            {
                "files": [{"path": "/src/a.py", "changeType": "edit"}],
                "review_state_path": "",
                "config": {},
            },
            provider_factory=mock_provider_factory,
        )

        assert len(result["file_results"]) == 1
        mock_provider_factory.get_provider.assert_called_once_with("review_files", "pr_review")

    @patch("agentic_devtools.orchestration.llm.factory.get_provider")
    def test_fails_node_if_provider_unconfigured(self, mock_get_provider) -> None:
        """Fails fast when no provider is configured, avoiding false 'request-changes'."""
        from agentic_devtools.orchestration.llm.errors import ProviderNotConfiguredError

        mock_get_provider.side_effect = ProviderNotConfiguredError("No provider")

        with pytest.raises(ProviderNotConfiguredError):
            review_files_node(
                {
                    "files": [{"path": "/src/a.py", "changeType": "edit"}],
                    "review_state_path": "",
                }
            )

    @patch("agentic_devtools.orchestration.llm.factory.get_provider")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._update_review_state_for_file")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._review_single_file")
    def test_updates_review_state_when_pr_id_present(
        self,
        mock_review,
        mock_update_state,
        mock_get_provider,
    ) -> None:
        """Successful file reviews are persisted when a pr_id is present."""
        mock_review.return_value = FileReviewResult(
            file_path="/src/a.py",
            outcome="approve",
            summary="LGTM",
            model_id="gpt-4o",
        )

        result = review_files_node(
            {
                "files": [{"path": "/src/a.py", "changeType": "edit"}],
                "pr_id": 123,
                "config": {},
            }
        )

        assert result["errors"] == []
        mock_update_state.assert_called_once()

    @patch("agentic_devtools.orchestration.llm.factory.get_provider")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._update_review_state_for_file")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._review_single_file")
    def test_handles_review_error_gracefully(self, mock_review, mock_update_state, mock_get_provider) -> None:
        """Records error result when single-file review fails.

        Sensitive exception text must NOT appear in persisted summary or errors —
        only a sanitized message is stored to prevent provider details from
        flowing into review-state.json or PR comments.
        """
        mock_review.side_effect = RuntimeError("LLM unavailable")

        result = review_files_node(
            {
                "files": [{"path": "/src/a.py", "changeType": "edit"}],
                "pr_id": 123,
                "review_state_path": "",
            }
        )

        assert len(result["file_results"]) == 1
        assert result["file_results"][0]["outcome"] == "request-changes"
        # Summary must be generic — exception text must not be persisted
        assert result["file_results"][0]["summary"] == "Review failed: see error log for details"
        assert "LLM unavailable" not in result["file_results"][0]["summary"]
        assert len(result["errors"]) == 1
        # errors entry must identify the file but must not include exception text
        assert "/src/a.py" in result["errors"][0]
        assert "LLM unavailable" not in result["errors"][0]
        mock_update_state.assert_called_once()

    @patch("agentic_devtools.orchestration.llm.factory.get_provider")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._update_review_state_for_file")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._review_single_file")
    def test_does_not_persist_error_result_without_pr_id(
        self, mock_review, mock_update_state, mock_get_provider
    ) -> None:
        """Error results are not persisted when no pr_id is available."""
        mock_review.side_effect = RuntimeError("LLM unavailable")

        review_files_node(
            {
                "files": [{"path": "/src/a.py", "changeType": "edit"}],
                "review_state_path": "",
            }
        )

        mock_update_state.assert_not_called()

    @patch("agentic_devtools.orchestration.llm.factory.get_provider")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._update_review_state_for_file")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._review_single_file")
    def test_re_raises_provider_authentication_failure(
        self,
        mock_review,
        mock_update_state,
        mock_get_provider,
    ) -> None:
        """Provider-wide auth failures abort the node instead of per-file verdicts."""

        class UnauthorizedError(RuntimeError):
            def __init__(self) -> None:
                super().__init__("unauthorized")
                self.status_code = 401

        mock_review.side_effect = UnauthorizedError()

        with pytest.raises(UnauthorizedError):
            review_files_node(
                {
                    "files": [{"path": "/src/a.py", "changeType": "edit"}],
                    "pr_id": 123,
                    "review_state_path": "",
                }
            )

        mock_update_state.assert_not_called()

    @patch("agentic_devtools.orchestration.llm.factory.get_provider")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._update_review_state_for_file")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._review_single_file")
    def test_transient_failure_is_recorded_as_file_error(
        self,
        mock_review,
        mock_update_state,
        mock_get_provider,
    ) -> None:
        """Exhausted transient failures are handled per-file, not as node-fatal errors."""
        mock_review.side_effect = TransientLLMError("HTTP 503", status_code=503)

        result = review_files_node(
            {
                "files": [{"path": "/src/a.py", "changeType": "edit"}],
                "pr_id": 123,
                "review_state_path": "",
            }
        )

        assert len(result["file_results"]) == 1
        assert result["file_results"][0]["outcome"] == "request-changes"
        assert result["errors"] == ["review_files: failed to review /src/a.py"]
        mock_update_state.assert_called_once()

    @patch("agentic_devtools.orchestration.llm.factory.get_provider")
    @patch("agentic_devtools.orchestration.llm.config.load_config")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._review_single_file")
    def test_forwards_llm_config_path_from_state(self, mock_review, mock_load_config, mock_get_provider) -> None:
        """llm_config_path in state is forwarded to load_config and the snapshot to get_provider."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        mock_snapshot = LLMConfigSnapshot()
        mock_load_config.return_value = mock_snapshot
        mock_review.return_value = FileReviewResult(
            file_path="/src/a.py",
            outcome="approve",
            summary="LGTM",
            model_id="gemini-3.7-flash",
        )

        review_files_node(
            {
                "files": [{"path": "/src/a.py", "changeType": "edit"}],
                "llm_config_path": "/repo/.agdt/config/llm-providers.yml",
                "config": {},
            }
        )

        mock_load_config.assert_called_once_with("/repo/.agdt/config/llm-providers.yml")
        mock_get_provider.assert_called_once_with("review_files", "pr_review", config=mock_snapshot)

    @patch("agentic_devtools.orchestration.llm.factory.get_provider")
    @patch("agentic_devtools.orchestration.llm.config.load_config")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._review_single_file")
    def test_uses_default_config_when_llm_config_path_absent(
        self, mock_review, mock_load_config, mock_get_provider
    ) -> None:
        """When llm_config_path is absent from state, load_config is called with None."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        mock_snapshot = LLMConfigSnapshot()
        mock_load_config.return_value = mock_snapshot
        mock_review.return_value = FileReviewResult(
            file_path="/src/a.py",
            outcome="approve",
            summary="LGTM",
            model_id="gemini-3.7-flash",
        )

        review_files_node(
            {
                "files": [{"path": "/src/a.py", "changeType": "edit"}],
                "config": {},
            }
        )

        mock_load_config.assert_called_once_with(None)
        mock_get_provider.assert_called_once_with("review_files", "pr_review", config=mock_snapshot)


class TestReviewSingleFile:
    """Tests for _review_single_file()."""

    @patch("agentic_devtools.orchestration.review.nodes.review_files._invoke_llm")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._build_review_prompt")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._resolve_model")
    def test_returns_structured_result(
        self,
        mock_resolve_model,
        mock_build_prompt,
        mock_invoke,
    ) -> None:
        """A successful LLM invocation becomes a FileReviewResult."""
        mock_resolve_model.return_value = "claude-sonnet"
        mock_build_prompt.return_value = "prompt"
        mock_invoke.return_value = (
            FileReviewOutput(
                outcome="approve",
                summary="Looks good.",
                suggestions=[SuggestionOutput(severity="low", content="Nice cleanup.", line=12)],
            ),
            17,
            "claude-sonnet",
            "copilot",
            123,
            "stop",
        )

        result = _review_single_file(
            file_path="/src/main.py",
            file_info={"path": "/src/main.py", "changeType": "edit"},
            config={},
            source_context_enabled=True,
            model_config_raw={},
            state={},
        )

        assert result.file_path == "/src/main.py"
        assert result.outcome == "approve"
        assert result.model_id == "claude-sonnet"
        assert result.provider_type == "copilot"
        assert result.latency_ms == 123
        assert result.finish_reason == "stop"
        assert result.tokens_used == 17
        assert result.suggestions == [
            {
                "severity": "low",
                "content": "Nice cleanup.",
                "replacement_code": None,
                "line": 12,
                "endLine": None,
                "out_of_scope": False,
            }
        ]

    @patch("time.sleep")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._invoke_llm")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._build_review_prompt")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._resolve_model")
    def test_retries_transient_errors_then_succeeds(
        self,
        mock_resolve_model,
        mock_build_prompt,
        mock_invoke,
        mock_sleep,
    ) -> None:
        """Transient LLM failures are retried with exponential backoff."""
        mock_resolve_model.return_value = "gpt-4o"
        mock_build_prompt.return_value = "prompt"
        mock_invoke.side_effect = [
            TransientLLMError("HTTP 429", status_code=429),
            (
                FileReviewOutput(
                    outcome="approve",
                    summary="Recovered.",
                    suggestions=[],
                ),
                3,
                "gpt-4o",
                "copilot",
                41,
                "stop",
            ),
        ]

        result = _review_single_file(
            file_path="/src/main.py",
            file_info={"path": "/src/main.py"},
            config={},
            source_context_enabled=True,
            model_config_raw={},
            state={},
        )

        assert result.summary == "Recovered."
        mock_sleep.assert_called_once_with(1)

    @patch("time.sleep")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._invoke_llm")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._build_review_prompt")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._resolve_model")
    def test_raises_last_transient_error_after_retries(
        self,
        mock_resolve_model,
        mock_build_prompt,
        mock_invoke,
        mock_sleep,
    ) -> None:
        """Exhausted transient retries re-raise the last transient error."""
        mock_resolve_model.return_value = "gpt-4o"
        mock_build_prompt.return_value = "prompt"

        def _raise_transient(*_args: object, **_kwargs: object) -> None:
            raise TransientLLMError("HTTP 503", status_code=503)

        mock_invoke.side_effect = _raise_transient

        with pytest.raises(TransientLLMError) as exc_info:
            _review_single_file(
                file_path="/src/main.py",
                file_info={"path": "/src/main.py"},
                config={},
                source_context_enabled=True,
                model_config_raw={},
                state={},
            )

        frame_names = [frame.name for frame in traceback.extract_tb(exc_info.value.__traceback__)]
        assert frame_names.count("_review_single_file") == 1
        assert "_raise_transient" in frame_names
        assert mock_sleep.call_args_list == [((1,), {}), ((2,), {})]

    @patch("time.sleep")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._invoke_llm")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._build_review_prompt")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._resolve_model")
    def test_non_transient_errors_fail_immediately(
        self,
        mock_resolve_model,
        mock_build_prompt,
        mock_invoke,
        mock_sleep,
    ) -> None:
        """Non-transient errors bypass the retry loop."""
        mock_resolve_model.return_value = "gpt-4o"
        mock_build_prompt.return_value = "prompt"
        mock_invoke.side_effect = ValueError("bad output")

        with pytest.raises(ValueError, match="bad output"):
            _review_single_file(
                file_path="/src/main.py",
                file_info={"path": "/src/main.py"},
                config={},
                source_context_enabled=True,
                model_config_raw={},
                state={},
            )

        mock_sleep.assert_not_called()

    @patch("time.sleep")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._invoke_llm")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._build_review_prompt")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._resolve_model")
    def test_retry_exhausted_errors_bypass_outer_transient_retry(
        self,
        mock_resolve_model,
        mock_build_prompt,
        mock_invoke,
        mock_sleep,
    ) -> None:
        """RetryExhaustedError propagates immediately instead of re-entering file retries."""
        from agentic_devtools.orchestration.llm.errors import RetryExhaustedError

        mock_resolve_model.return_value = "gpt-4o"
        mock_build_prompt.return_value = "prompt"
        mock_invoke.side_effect = RetryExhaustedError(
            "All 5 retry attempts exhausted",
            attempts=5,
            total_wait_seconds=1.0,
            last_status_code=503,
        )

        with pytest.raises(RetryExhaustedError, match="All 5 retry attempts exhausted"):
            _review_single_file(
                file_path="/src/main.py",
                file_info={"path": "/src/main.py"},
                config={},
                source_context_enabled=True,
                model_config_raw={},
                state={},
            )

        assert mock_invoke.call_count == 1
        mock_sleep.assert_not_called()

    @patch("agentic_devtools.orchestration.review.nodes.review_files._invoke_llm")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._build_review_prompt")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._resolve_model")
    def test_uses_supplied_provider_for_invoke(
        self,
        mock_resolve_model,
        mock_build_prompt,
        mock_invoke,
    ) -> None:
        """A supplied provider is forwarded to _invoke_llm."""
        provider = object()
        mock_resolve_model.return_value = "gpt-4o"
        mock_build_prompt.return_value = "prompt"
        mock_invoke.return_value = (
            FileReviewOutput(outcome="approve", summary="ok", suggestions=[]),
            5,
            "gpt-4o",
            "copilot",
            9,
            "stop",
        )

        result = _review_single_file(
            file_path="/src/main.py",
            file_info={"path": "/src/main.py"},
            config={},
            source_context_enabled=True,
            model_config_raw={},
            state={},
            provider=provider,
        )

        assert result.outcome == "approve"
        mock_invoke.assert_called_once_with("prompt", "gpt-4o", provider=provider)


class TestResolveModel:
    """Tests for _resolve_model()."""

    @patch(
        "agentic_devtools.orchestration.review.model_routing.resolve_model_for_file",
        return_value="claude-opus-4",
    )
    def test_delegates_to_model_routing(self, mock_resolve) -> None:
        """When available, model routing decides the file model."""
        assert _resolve_model("/src/main.py", {}) == "claude-opus-4"
        mock_resolve.assert_called_once_with("/src/main.py", {}, default_model=None)

    @patch(
        "agentic_devtools.orchestration.review.model_routing.resolve_model_for_file",
        return_value="gemini-3.7-flash",
    )
    def test_requested_model_takes_precedence_over_provider_default(self, mock_resolve) -> None:
        """A non-empty requested model bypasses routing and is returned directly."""
        assert (
            _resolve_model(
                "/src/main.py",
                {},
                requested_model="gemini-3.7-flash",
                provider_default_model="gpt-4o",
            )
            == "gemini-3.7-flash"
        )
        mock_resolve.assert_not_called()

    def test_import_error_uses_default_model_from_config(self) -> None:
        """If model routing cannot be imported, config fallback is used."""
        original_import = builtins.__import__

        def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "model_routing" and level == 2:
                raise ImportError("missing")
            return original_import(name, globals, locals, fromlist, level)

        with patch.object(builtins, "__import__", side_effect=fake_import):
            assert _resolve_model("/src/main.py", {"default-model": "fallback-model"}) == "fallback-model"

    def test_import_error_uses_state_default_when_config_default_missing(self) -> None:
        """State-derived defaults are used when routing import and config default both fail."""
        original_import = builtins.__import__

        def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "model_routing" and level == 2:
                raise ImportError("missing")
            return original_import(name, globals, locals, fromlist, level)

        with (
            patch.object(builtins, "__import__", side_effect=fake_import),
            patch("agentic_devtools.state.get_value", return_value="state-model"),
        ):
            assert _resolve_model("/src/main.py", {}) == "state-model"

    def test_import_error_uses_provider_default_when_present(self) -> None:
        """Provider default model takes precedence over state fallback."""
        original_import = builtins.__import__

        def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "model_routing" and level == 2:
                raise ImportError("missing")
            return original_import(name, globals, locals, fromlist, level)

        with (
            patch.object(builtins, "__import__", side_effect=fake_import),
            patch("agentic_devtools.state.get_value", return_value="state-model") as mock_get_value,
        ):
            assert (
                _resolve_model(
                    "/src/main.py",
                    {},
                    provider_default_model="provider-model",
                )
                == "provider-model"
            )

        mock_get_value.assert_not_called()

    def test_import_error_uses_requested_model_before_provider_default(self) -> None:
        """Requested model takes precedence over provider and state fallbacks."""
        original_import = builtins.__import__

        def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "model_routing" and level == 2:
                raise ImportError("missing")
            return original_import(name, globals, locals, fromlist, level)

        with (
            patch.object(builtins, "__import__", side_effect=fake_import),
            patch("agentic_devtools.state.get_value", return_value="state-model") as mock_get_value,
        ):
            assert (
                _resolve_model(
                    "/src/main.py",
                    {},
                    requested_model="gemini-3.7-flash",
                    provider_default_model="provider-model",
                )
                == "gemini-3.7-flash"
            )

        mock_get_value.assert_not_called()

    def test_import_error_uses_requested_model_before_config_default(self) -> None:
        """Requested model also overrides config default in the import-error fallback."""
        original_import = builtins.__import__

        def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "model_routing" and level == 2:
                raise ImportError("missing")
            return original_import(name, globals, locals, fromlist, level)

        with patch.object(builtins, "__import__", side_effect=fake_import):
            assert (
                _resolve_model(
                    "/src/main.py",
                    {"default-model": "config-model"},
                    requested_model="gemini-3.7-flash",
                )
                == "gemini-3.7-flash"
            )

    @patch("time.sleep")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._invoke_llm")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._build_review_prompt")
    @patch("agentic_devtools.orchestration.review.nodes.review_files._resolve_model")
    def test_retry_loop_stops_after_max_attempts(
        self,
        mock_resolve_model,
        mock_build_prompt,
        mock_invoke,
        mock_sleep,
    ) -> None:
        """Transient failures are attempted exactly max_retries times."""
        mock_resolve_model.return_value = "gpt-4o"
        mock_build_prompt.return_value = "prompt"

        def _raise_transient(*_args: object, **_kwargs: object) -> None:
            raise TransientLLMError("HTTP 503", status_code=503)

        mock_invoke.side_effect = _raise_transient

        with pytest.raises(TransientLLMError, match="HTTP 503"):
            _review_single_file(
                file_path="/src/main.py",
                file_info={"path": "/src/main.py"},
                config={},
                source_context_enabled=True,
                model_config_raw={},
                state={},
            )

        assert mock_invoke.call_count == 3
        assert mock_sleep.call_args_list == [((1,), {}), ((2,), {})]


class TestBuildReviewPrompt:
    """Tests for _build_review_prompt()."""

    @patch("agentic_devtools.orchestration.review.source_context.fetch_source_context")
    @patch("agentic_devtools.config.load_review_focus_areas", return_value="- Check error handling")
    def test_includes_source_context_and_focus_areas(
        self,
        mock_load_focus_areas,
        mock_fetch_context,
    ) -> None:
        """Prompt rendering includes optional source context and embedded focus areas."""
        mock_fetch_context.return_value = "def helper():\n    return 1"

        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={"changeType": "edit", "patch": "@@ -1 +1 @@\n-old\n+new"},
            config={"review": {"focus-areas-file": ".github/review-focus-areas.md"}},
            source_context_enabled=True,
            state={"repo_id": "repo-guid"},
        )

        assert "## Patch" in prompt
        assert "@@ -1 +1 @@" in prompt
        assert "## Source Context" in prompt
        assert "def helper():" in prompt
        assert "## Review Focus Areas" in prompt
        assert "- Check error handling" in prompt
        mock_load_focus_areas.assert_called_once()

    @patch(
        "agentic_devtools.orchestration.review.source_context.fetch_source_context",
        side_effect=RuntimeError("boom"),
    )
    def test_ignores_source_context_failures_and_invalid_review_config(
        self,
        mock_fetch_context,
        capsys,
    ) -> None:
        """Prompt generation continues when optional context enrichment fails, emitting a warning."""
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={"changeType": "add"},
            config={"review": "invalid"},
            source_context_enabled=True,
            state={},
        )

        assert "Change type: add" in prompt
        assert "## Source Context" not in prompt
        assert "Review Focus Areas" not in prompt
        assert "Warning: source context enrichment skipped for /src/main.py: boom" in capsys.readouterr().err

    def test_silently_skips_source_context_on_import_error(self, capsys) -> None:
        """ImportError during source_context import is swallowed without any warning."""
        original_import = builtins.__import__

        def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "source_context" and level == 2:
                raise ImportError("source_context not available")
            return original_import(name, globals, locals, fromlist, level)

        with patch.object(builtins, "__import__", side_effect=fake_import):
            prompt = _build_review_prompt(
                file_path="/src/main.py",
                file_info={"changeType": "edit"},
                config={"review": {}},
                source_context_enabled=True,
                state={},
            )

        assert "## Source Context" not in prompt
        assert capsys.readouterr().err == ""

    @patch("agentic_devtools.orchestration.review.source_context.fetch_source_context")
    def test_omits_source_context_when_fetch_returns_none(self, mock_fetch_context) -> None:
        """Empty context responses do not add a source-context section."""
        mock_fetch_context.return_value = None

        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={"changeType": "edit"},
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        assert "## Source Context" not in prompt
        assert "Review Focus Areas" not in prompt

    def test_skips_source_context_when_disabled(self) -> None:
        """Disabling source context avoids any enrichment call path."""
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={"changeType": "edit"},
            config={"review": {}},
            source_context_enabled=False,
            state={},
        )

        assert "## Source Context" not in prompt
        assert "Review Focus Areas" not in prompt

    @patch("agentic_devtools.orchestration.review.source_context.fetch_source_context")
    def test_prefers_pre_enriched_source_context_fields(self, mock_fetch_context) -> None:
        """When source_context node already enriched file_info, prompt uses that and skips re-fetch."""
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "edit",
                "full_content_source": "def enriched():\n    return 1",
                "full_content_target": "def previous():\n    return 0",
                "related_tests": ["tests/unit/src/main/test_main.py"],
                "related_test_contents": [
                    {"path": "tests/unit/src/main/test_main.py", "content": "def test_main():\n    assert True"}
                ],
                "resolved_imports": ["agentic_devtools/state.py"],
                "resolved_import_contents": [
                    {"path": "agentic_devtools/state.py", "content": "def get_value():\n    return 1"}
                ],
                "related_config_docs": ["pyproject.toml"],
                "related_config_doc_contents": [{"path": "pyproject.toml", "content": "[project]\nname='agdt'\n"}],
            },
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        assert "## Source Context" in prompt
        assert "def enriched():" in prompt
        assert "## Target/Base Context" in prompt
        assert "def previous():" in prompt
        assert "## Related Test Files" in prompt
        assert "tests/unit/src/main/test_main.py" in prompt
        assert "def test_main():" in prompt
        assert "## Resolved First-Party Imports" in prompt
        assert "agentic_devtools/state.py" in prompt
        assert "def get_value():" in prompt
        assert "## Related Config/Documentation Files" in prompt
        assert "pyproject.toml" in prompt
        assert "[project]" in prompt
        mock_fetch_context.assert_not_called()

    def test_uses_target_context_for_deleted_files(self) -> None:
        """Deleted files render pre-enriched target/base context."""
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "delete",
                "full_content_target": "def deleted():\n    return 0",
                "removedLines": [{"line": 1, "content": "def deleted():"}],
            },
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        assert "## Source Context" not in prompt
        assert "## Target/Base Context" in prompt
        assert "def deleted():" in prompt

    def test_related_file_sections_fall_back_to_paths_when_content_items_are_invalid(self) -> None:
        """Invalid related-file content entries fall back to the path-only rendering with omission note."""
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "edit",
                "related_tests": ["tests/test_main.py"],
                "related_test_contents": ["bad", {"path": 1, "content": "x"}],
                "related_tests_omitted_count": 1,
            },
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        assert "## Related Test Files" in prompt
        assert "- tests/test_main.py" in prompt
        assert "1 file(s) were omitted or truncated" in prompt

    def test_related_file_sections_render_paths_without_budget_note_when_none_omitted(self) -> None:
        """Path-only related files without an omission count omit the budget note."""
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "edit",
                "resolved_imports": ["agentic_devtools/state.py"],
            },
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        assert "## Resolved First-Party Imports" in prompt
        assert "- agentic_devtools/state.py" in prompt
        assert "were omitted or truncated" not in prompt

    def test_related_file_sections_emit_omission_note_when_items_retained(self) -> None:
        """Rendered content items still emit the omission note when later files were dropped."""
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "edit",
                "related_tests": ["tests/test_main.py", "tests/test_extra.py"],
                "related_test_contents": [{"path": "tests/test_main.py", "content": "def test(): pass"}],
                "related_tests_omitted_count": 2,
            },
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        assert "## Related Test Files" in prompt
        assert "def test(): pass" in prompt
        assert "2 file(s) were omitted or truncated" in prompt

    def test_prefers_budget_excerpt_over_full_patch(self) -> None:
        """A non-empty patch_budget_excerpt takes precedence over the full patch."""
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "edit",
                "patch": "@@ -1 +1 @@\n-old\n+new\n@@ -5 +5 @@\n-more\n+extra",
                "patch_budget_excerpt": "@@ -1 +1 @@\n-old\n+new",
            },
            config={"review": {}},
            source_context_enabled=False,
            state={},
        )

        assert "## Patch" in prompt
        assert "-old" in prompt
        assert "+extra" not in prompt

    def test_empty_budget_excerpt_renders_patch_unavailable(self) -> None:
        """An intentionally empty excerpt suppresses the full patch (budget honoured)."""
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "edit",
                "patch": "@@ -1 +1 @@\n-old\n+new",
                "patch_budget_excerpt": "",
            },
            config={"review": {}},
            source_context_enabled=False,
            state={},
        )

        assert "## Patch unavailable" in prompt
        assert "+new" not in prompt

    def test_per_side_truncated_source_renders_excerpt_directly(self) -> None:
        """Per-side truncated source content is rendered directly without re-anchoring."""
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "edit",
                "patch": "@@ -1 +1 @@\n-old\n+new",
                "full_content_source": "windowed line a\nwindowed line b",
                "addedLines": [{"line": 1, "content": "windowed line a"}],
                "full_content_source_truncated": True,
            },
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        assert "## Source Context" in prompt
        assert "windowed line a" in prompt

    @patch("agentic_devtools.orchestration.review.source_context.fetch_source_context")
    def test_pre_enriched_context_uses_added_lines_as_anchors(self, mock_fetch_context) -> None:
        """Pre-enriched full content uses addedLines for focused context extraction."""
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "edit",
                "full_content_source": "line1\nline2\nline3\nline4",
                "addedLines": [{"line": 3, "content": "line3"}],
            },
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        assert "## Source Context" in prompt
        assert "line3" in prompt
        mock_fetch_context.assert_not_called()

    @patch("agentic_devtools.orchestration.review.source_context.fetch_source_context")
    def test_pre_enriched_context_without_diff_anchors_uses_budgeted_content_verbatim(
        self,
        mock_fetch_context,
    ) -> None:
        """Pre-enriched full content without diff anchors is rendered without adding line-number prefixes."""
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "edit",
                "full_content_source": "alpha\nbeta",
            },
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        assert "## Source Context" in prompt
        assert "alpha\nbeta" in prompt
        assert "1 | alpha" not in prompt
        mock_fetch_context.assert_not_called()

    @patch("agentic_devtools.orchestration.review.source_context.extract_surrounding_context")
    @patch("agentic_devtools.orchestration.review.source_context.fetch_source_context")
    def test_pre_enriched_context_skips_zero_line_anchor_entries(
        self,
        mock_fetch_context,
        mock_extract_context,
    ) -> None:
        """Pre-enriched context ignores zero anchors and preserves full budgeted content."""
        mock_extract_context.return_value = "unused"
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "edit",
                "full_content_source": "line1\nline2\nline3\nline4",
                "addedLines": [
                    {"line": 0, "content": "ignored"},
                    {"line": 3, "content": "line3"},
                ],
            },
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        assert "## Source Context" in prompt
        assert "line1\nline2\nline3\nline4" in prompt
        mock_extract_context.assert_not_called()
        mock_fetch_context.assert_not_called()

    @patch("agentic_devtools.orchestration.review.source_context.extract_surrounding_context")
    @patch("agentic_devtools.orchestration.review.source_context.fetch_source_context")
    def test_pre_enriched_truncated_content_falls_back_when_anchor_exceeds_lines(
        self,
        mock_fetch_context,
        mock_extract_context,
    ) -> None:
        """When pre-enriched content is truncated and the highest diff anchor exceeds the
        available line count, extract_surrounding_context is skipped and fetch_source_context
        is called as fallback so the LLM receives relevant context instead of only file-top
        imports/signatures from the truncated content."""
        mock_fetch_context.return_value = "full content from server"
        mock_extract_context.return_value = "extracted"

        # 4-line truncated content, but diff anchor points at line 50 (beyond available lines)
        # truncation_applied is NOT set, so the live fallback is permitted.
        _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "edit",
                "full_content_source": "line1\nline2\nline3\nline4",
                "addedLines": [{"line": 50, "content": "something far down"}],
            },
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        # Should NOT use the truncated pre-enriched content — fetch from server first
        mock_fetch_context.assert_called_once()
        # extract_surrounding_context should be called on the FETCHED (untruncated) content,
        # not the truncated pre-enriched "line1\nline2\nline3\nline4" content.
        mock_extract_context.assert_called_once_with("full content from server", [(50, 50)])

    @patch("agentic_devtools.orchestration.review.source_context.extract_surrounding_context")
    @patch("agentic_devtools.orchestration.review.source_context.fetch_source_context")
    def test_skips_fallback_fetch_when_budget_was_enforced(
        self,
        mock_fetch_context,
        mock_extract_context,
    ) -> None:
        """When truncation_applied=True the source_context node already enforced the budget;
        the live fetch fallback must NOT run to avoid bypassing the per-prompt token limit."""
        mock_fetch_context.return_value = "full content from server"
        mock_extract_context.return_value = "extracted"

        # Budget was exhausted — node cleared full_content_source and set truncation_applied.
        _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "edit",
                "full_content_source": None,
                "addedLines": [{"line": 10, "content": "something"}],
                "truncation_applied": True,
            },
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        # The live fetch must be suppressed to honour the budget decision.
        mock_fetch_context.assert_not_called()

    @patch("agentic_devtools.orchestration.review.source_context.extract_surrounding_context")
    @patch("agentic_devtools.orchestration.review.source_context.fetch_source_context")
    def test_skips_fallback_fetch_when_budget_enforced_with_partial_content(
        self,
        mock_fetch_context,
        mock_extract_context,
    ) -> None:
        """When truncation_applied=True but full_content_source was partially preserved,
        the live fetch must still be skipped — the budget decision stands — and the
        preserved excerpt is presented directly instead of being dropped."""
        mock_fetch_context.return_value = "full content from server"
        mock_extract_context.return_value = "extracted"

        # Budget was partially exhausted — node kept a prefix and set truncation_applied.
        # Diff anchor is beyond the truncated prefix, but we must NOT re-fetch.
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "edit",
                "full_content_source": "line1\nline2",
                "addedLines": [{"line": 50, "content": "far down"}],
                "truncation_applied": True,
            },
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        mock_fetch_context.assert_not_called()
        # The preserved (smart-truncated) excerpt must appear in the prompt rather than
        # being silently omitted; extract_surrounding_context is skipped because the
        # anchor no longer maps onto the shifted line numbering.
        mock_extract_context.assert_not_called()
        assert "## Source Context" in prompt
        assert "line1\nline2" in prompt

    @patch("agentic_devtools.orchestration.review.source_context.extract_surrounding_context")
    @patch("agentic_devtools.orchestration.review.source_context.fetch_source_context")
    def test_skips_fallback_fetch_when_source_context_node_ran(
        self,
        mock_fetch_context,
        mock_extract_context,
    ) -> None:
        """When the source_context node already ran (``context_status`` present) but produced
        no source content — e.g. a deleted file or a known retrieval failure — the legacy live
        fetch must NOT run: it would inject content never charged to the PR-wide TokenBudget or
        redundantly repeat a request the node already made."""
        mock_fetch_context.return_value = "full content from server"
        mock_extract_context.return_value = "extracted"

        _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "delete",
                "full_content_source": None,
                "addedLines": [{"line": 10, "content": "something"}],
                "context_status": "partial",
                "context_status_reason": "not_found_on_source",
            },
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        mock_fetch_context.assert_not_called()

    @patch("agentic_devtools.cli.azure_devops.pr_review_manifest.resolve_repo_root", return_value="/repo")
    @patch("agentic_devtools.config.load_review_focus_areas", side_effect=RuntimeError("boom"))
    def test_ignores_focus_area_loading_failures(
        self,
        mock_load_focus_areas,
        mock_resolve_repo_root,
        capsys,
    ) -> None:
        """Prompt generation ignores focus-area loading failures."""
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={"changeType": "edit"},
            config={"review": {"focus-areas-file": ".github/review-focus-areas.md"}},
            source_context_enabled=False,
            state={},
        )

        assert "Review Focus Areas" not in prompt
        assert "failed to load review focus areas: boom" in capsys.readouterr().err
        mock_resolve_repo_root.assert_called_once_with()
        mock_load_focus_areas.assert_called_once_with("/repo")

    @patch("agentic_devtools.config.load_review_focus_areas")
    @patch(
        "agentic_devtools.cli.azure_devops.pr_review_manifest.resolve_repo_root",
        side_effect=RuntimeError("repo root missing"),
    )
    def test_ignores_repo_root_resolution_failures(
        self,
        mock_resolve_repo_root,
        mock_load_focus_areas,
        capsys,
    ) -> None:
        """Prompt generation ignores repo-root resolution failures for focus areas."""
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={"changeType": "edit"},
            config={"review": {"focus-areas-file": ".github/review-focus-areas.md"}},
            source_context_enabled=False,
            state={},
        )

        assert "Review Focus Areas" not in prompt
        assert "failed to load review focus areas: repo root missing" in capsys.readouterr().err
        mock_resolve_repo_root.assert_called_once_with()
        mock_load_focus_areas.assert_not_called()

    @patch("agentic_devtools.orchestration.review.source_context.fetch_source_context")
    def test_uses_extract_surrounding_context_when_added_lines_available(self, mock_fetch_context) -> None:
        """When addedLines are present, extract_surrounding_context is used with new-file anchors."""
        # 5-line file; the diff adds a line at position 3 in the new file
        mock_fetch_context.return_value = "line1\nline2\nline3\nline4\nline5"

        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "edit",
                "patch": "@@ -3 +3 @@\n-line3\n+changed",
                "addedLines": [{"line": 3, "content": "changed"}],
                "removedLines": [{"line": 3, "content": "line3"}],
            },
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        # extract_surrounding_context emits numbered lines; bare content should appear
        assert "## Source Context" in prompt
        assert "line1" in prompt
        assert "line3" in prompt

    @patch("agentic_devtools.orchestration.review.source_context.fetch_source_context")
    def test_removed_lines_are_not_used_as_context_anchors(self, mock_fetch_context) -> None:
        """removedLines carry base-file numbers and must not anchor new-file context extraction."""
        # File content has 3 lines; only removedLines (base-file) are present — no addedLines
        mock_fetch_context.return_value = "line1\nline2\nline3"

        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "edit",
                "removedLines": [{"line": 2, "content": "line2"}],
            },
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        # With no addedLines, diff_ranges is empty → falls back to full content
        assert "## Source Context" in prompt
        assert "line1" in prompt  # full content present, not just line 2

    @patch("agentic_devtools.orchestration.review.source_context.fetch_source_context")
    def test_falls_back_to_full_content_when_no_diff_ranges(self, mock_fetch_context) -> None:
        """When no addedLines/removedLines exist, the full file content is used."""
        mock_fetch_context.return_value = "def helper():\n    return 1"

        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={"changeType": "edit"},
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        assert "## Source Context" in prompt
        assert "   1 | def helper():" in prompt
        assert "   2 |     return 1" in prompt

    @patch("agentic_devtools.orchestration.review.source_context.fetch_source_context")
    def test_fallback_numbering_omits_spurious_trailing_empty_line(self, mock_fetch_context) -> None:
        """Fallback numbering uses splitlines() so a trailing newline is not counted as an extra line."""
        mock_fetch_context.return_value = "def helper():\n    return 1\n"

        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={"changeType": "edit"},
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        assert "   1 | def helper():" in prompt
        assert "   2 |     return 1" in prompt
        # trailing newline must NOT produce a spurious "   3 | " line
        assert "   3 | " not in prompt

    @patch("agentic_devtools.orchestration.review.source_context.fetch_source_context")
    def test_skips_zero_line_entries_when_building_diff_ranges(self, mock_fetch_context) -> None:
        """addedLines entries with line=0 are skipped; falls back to full content."""
        mock_fetch_context.return_value = "def helper():\n    return 1"

        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "edit",
                "addedLines": [{"line": 0, "content": "x"}],
                "removedLines": [{"line": 0, "content": "y"}],
            },
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        # Both entries have line=0 so diff_ranges stays empty; full content is the fallback
        assert "## Source Context" in prompt
        assert "def helper():" in prompt

    @patch("agentic_devtools.orchestration.review.source_context.extract_surrounding_context", return_value="")
    @patch("agentic_devtools.orchestration.review.source_context.fetch_source_context")
    def test_omits_context_section_when_extract_returns_empty(self, mock_fetch_context, mock_extract) -> None:
        """No source context section is added when extract_surrounding_context returns empty."""
        mock_fetch_context.return_value = "a\nb\nc"

        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={
                "changeType": "edit",
                "addedLines": [{"line": 2, "content": "b"}],
            },
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        assert "## Source Context" not in prompt

    @patch("agentic_devtools.orchestration.review.source_context.fetch_source_context")
    def test_skips_source_context_for_binary_files(self, mock_fetch_context) -> None:
        """Source-context enrichment is skipped when isBinary is True."""
        mock_fetch_context.return_value = "binary content"

        prompt = _build_review_prompt(
            file_path="/assets/logo.png",
            file_info={"changeType": "edit", "isBinary": True},
            config={"review": {}},
            source_context_enabled=True,
            state={},
        )

        assert "## Source Context" not in prompt
        mock_fetch_context.assert_not_called()

    def test_prompt_instructs_1_based_file_line_numbers(self) -> None:
        """Prompt instructs the LLM to use 1-based file line numbers for suggestions."""
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={"changeType": "edit"},
            config={},
            source_context_enabled=False,
            state={},
        )

        assert "1-based line numbers in the" in prompt
        assert "not diff/patch-relative" in prompt

    def test_includes_patch_unavailable_note_when_no_patch(self) -> None:
        """When no patch payload is present, the prompt contains a 'Patch unavailable' note."""
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={"changeType": "edit"},
            config={},
            source_context_enabled=False,
            state={},
        )

        assert "## Patch unavailable" in prompt
        assert "## Patch" not in prompt.replace("## Patch unavailable", "")
        assert "Prefer 'approve'" not in prompt
        assert "Do not approve the file" in prompt

    def test_includes_patch_unavailable_note_when_patch_is_whitespace_only(self) -> None:
        """Whitespace-only patch strings are treated as absent and trigger the unavailable note."""
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={"changeType": "edit", "patch": "   \n  "},
            config={},
            source_context_enabled=False,
            state={},
        )

        assert "## Patch unavailable" in prompt

    def test_omits_patch_unavailable_note_when_patch_is_present(self) -> None:
        """When a real diff patch is present, 'Patch unavailable' is not emitted."""
        prompt = _build_review_prompt(
            file_path="/src/main.py",
            file_info={"changeType": "edit", "patch": "@@ -1 +1 @@\n-old\n+new"},
            config={},
            source_context_enabled=False,
            state={},
        )

        assert "## Patch unavailable" not in prompt
        assert "## Patch" in prompt
        assert "@@ -1 +1 @@" in prompt


class TestInvokeLlm:
    """Tests for _invoke_llm()."""

    @patch("agentic_devtools.orchestration.llm.factory.get_provider")
    @patch("agentic_devtools.orchestration.execution.context_factory.build_execution_context")
    def test_uses_parsed_output_directly_when_available(self, mock_build_context, mock_get_provider) -> None:
        """parsed_output is returned directly without re-parsing raw_text."""
        parsed = FileReviewOutput(outcome="approve", summary="Already parsed.", suggestions=[])
        response = SimpleNamespace(
            raw_text="this-is-not-json",
            parsed_output=parsed,
            usage=SimpleNamespace(total_tokens=7),
        )
        reasoning = SimpleNamespace(invoke=MagicMock(return_value=response))
        mock_build_context.return_value = SimpleNamespace(reasoning=reasoning)

        output, tokens, model, provider_type, latency_ms, finish_reason = _invoke_llm("prompt", "gpt-4o")

        assert output is parsed
        assert output.outcome == "approve"
        assert tokens == 7
        assert model is None
        assert provider_type is None
        assert latency_ms is None
        assert finish_reason is None
        mock_get_provider.assert_called_once_with("review_files", "pr_review")
        mock_build_context.assert_called_once_with(provider=mock_get_provider.return_value)

    @patch("agentic_devtools.orchestration.llm.factory.get_provider")
    @patch("agentic_devtools.orchestration.execution.context_factory.build_execution_context")
    def test_parses_structured_output_and_usage(self, mock_build_context, mock_get_provider) -> None:
        """Valid JSON in raw_text is parsed when parsed_output is absent."""
        response = SimpleNamespace(
            raw_text=json.dumps(
                {
                    "outcome": "approve",
                    "summary": "Looks good.",
                    "suggestions": [],
                }
            ),
            parsed_output=None,
            usage=SimpleNamespace(total_tokens=12),
            model="gemini-3.7-flash",
            provider_type="copilot",
            latency_ms=52,
            finish_reason="stop",
        )
        reasoning = SimpleNamespace(invoke=MagicMock(return_value=response))
        mock_build_context.return_value = SimpleNamespace(reasoning=reasoning)

        output, tokens, model, provider_type, latency_ms, finish_reason = _invoke_llm("prompt", "gpt-4o")

        assert output.outcome == "approve"
        assert output.summary == "Looks good."
        assert tokens == 12
        assert model == "gemini-3.7-flash"
        assert provider_type == "copilot"
        assert latency_ms == 52
        assert finish_reason == "stop"
        mock_get_provider.assert_called_once_with("review_files", "pr_review")
        mock_build_context.assert_called_once_with(provider=mock_get_provider.return_value)

    @patch("agentic_devtools.orchestration.llm.factory.get_provider")
    @patch("agentic_devtools.orchestration.execution.context_factory.build_execution_context")
    def test_falls_back_to_plain_json_dict(self, mock_build_context, mock_get_provider) -> None:
        """If model_validate_json fails, plain JSON parsing is attempted."""
        response = SimpleNamespace(
            raw_text=json.dumps(
                {
                    "outcome": "request-changes",
                    "summary": "Needs work.",
                    "suggestions": [],
                }
            ),
            parsed_output=None,
            usage=None,
        )
        reasoning = SimpleNamespace(invoke=MagicMock(return_value=response))
        mock_build_context.return_value = SimpleNamespace(reasoning=reasoning)

        with patch.object(
            FileReviewOutput,
            "model_validate_json",
            side_effect=ValueError("bad schema"),
        ):
            output, tokens, model, provider_type, latency_ms, finish_reason = _invoke_llm("prompt", "gpt-4o")

        assert output.outcome == "request-changes"
        assert tokens is None
        assert model is None
        assert provider_type is None
        assert latency_ms is None
        assert finish_reason is None
        mock_get_provider.assert_called_once_with("review_files", "pr_review")
        mock_build_context.assert_called_once_with(provider=mock_get_provider.return_value)

    @patch("agentic_devtools.orchestration.llm.factory.get_provider")
    @patch("agentic_devtools.orchestration.execution.context_factory.build_execution_context")
    def test_raises_value_error_when_output_cannot_be_parsed(self, mock_build_context, mock_get_provider) -> None:
        """Completely invalid raw output raises a descriptive parse error."""
        response = SimpleNamespace(raw_text="not json", parsed_output=None, usage=None)
        reasoning = SimpleNamespace(invoke=MagicMock(return_value=response))
        mock_build_context.return_value = SimpleNamespace(reasoning=reasoning)

        with patch.object(
            FileReviewOutput,
            "model_validate_json",
            side_effect=ValueError("bad schema"),
        ):
            with pytest.raises(ValueError, match="Failed to parse LLM output"):
                _invoke_llm("prompt", "gpt-4o")

        mock_get_provider.assert_called_once_with("review_files", "pr_review")
        mock_build_context.assert_called_once_with(provider=mock_get_provider.return_value)

    @patch("agentic_devtools.orchestration.llm.factory.get_provider")
    @patch("agentic_devtools.orchestration.execution.context_factory.build_execution_context")
    def test_uses_supplied_provider_without_resolving_again(self, mock_build_context, mock_get_provider) -> None:
        """A supplied provider is reused directly."""
        response = SimpleNamespace(
            raw_text=json.dumps({"outcome": "approve", "summary": "ok", "suggestions": []}),
            parsed_output=None,
            usage=None,
        )
        reasoning = SimpleNamespace(invoke=MagicMock(return_value=response))
        mock_build_context.return_value = SimpleNamespace(reasoning=reasoning)
        provided_provider = object()

        output, tokens, model, provider_type, latency_ms, finish_reason = _invoke_llm(
            "prompt", "gpt-4o", provider=provided_provider
        )

        assert output.outcome == "approve"
        assert tokens is None
        assert model is None
        assert provider_type is None
        assert latency_ms is None
        assert finish_reason is None
        mock_get_provider.assert_not_called()
        mock_build_context.assert_called_once_with(provider=provided_provider)


class TestUpdateReviewStateForFile:
    """Tests for _update_review_state_for_file()."""

    def test_load_failure_is_ignored(self, capsys) -> None:
        """State load/lock failures are tolerated for best-effort persistence."""
        with patch(
            "agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state",
            side_effect=RuntimeError("lock failed"),
        ):
            _update_review_state_for_file(
                123,
                "/src/main.py",
                FileReviewResult(
                    file_path="/src/main.py",
                    outcome="approve",
                    summary="OK",
                ),
            )

        assert "failed to save review state" in capsys.readouterr().err

    def test_updates_existing_file_entry(self) -> None:
        """Known file entries receive the mapped status and summary."""
        entry = SimpleNamespace(
            status="unreviewed",
            summary="",
            modelId=None,
            providerType=None,
            latencyMs=None,
            finishReason=None,
            tokensUsed=None,
        )
        review_state = SimpleNamespace(files={"/src/main.py": entry})

        @contextmanager
        def _fake_rmw(_):
            yield review_state

        with patch(
            "agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state",
            side_effect=_fake_rmw,
        ):
            _update_review_state_for_file(
                123,
                "/src/main.py",
                FileReviewResult(
                    file_path="/src/main.py",
                    outcome="request-changes-with-suggestion",
                    summary="Needs a guard.",
                    model_id="gemini-3.7-flash",
                    provider_type="copilot",
                    latency_ms=78,
                    finish_reason="stop",
                    tokens_used=321,
                ),
            )

        assert entry.status == "needs-work"
        assert entry.summary == "Needs a guard."
        assert entry.modelId == "gemini-3.7-flash"
        assert entry.providerType == "copilot"
        assert entry.latencyMs == 78
        assert entry.finishReason == "stop"
        assert entry.tokensUsed == 321

    def test_unknown_file_path_leaves_state_unchanged(self) -> None:
        """Unknown file paths do not create or mutate entries."""
        existing_entry = SimpleNamespace(status="approved", summary="Existing")
        review_state = SimpleNamespace(files={"/src/known.py": existing_entry})

        @contextmanager
        def _fake_rmw(_):
            yield review_state

        with patch(
            "agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state",
            side_effect=_fake_rmw,
        ):
            _update_review_state_for_file(
                123,
                "/src/other.py",
                FileReviewResult(
                    file_path="/src/other.py",
                    outcome="approve",
                    summary="OK",
                ),
            )

        assert existing_entry.status == "approved"
        assert existing_entry.summary == "Existing"

    def test_normalizes_file_path_before_lookup(self) -> None:
        """Repo-relative and Windows-style paths are normalized for file lookup."""
        entry = SimpleNamespace(status="unreviewed", summary="")
        review_state = SimpleNamespace(files={"/src/main.py": entry})

        @contextmanager
        def _fake_rmw(_):
            yield review_state

        with patch(
            "agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state",
            side_effect=_fake_rmw,
        ):
            _update_review_state_for_file(
                123,
                r"src\main.py",
                FileReviewResult(
                    file_path=r"src\main.py",
                    outcome="approve",
                    summary="OK",
                ),
            )

        assert entry.status == "approved"
        assert entry.summary == "OK"

    def test_save_failure_is_reported(self, capsys) -> None:
        """Exceptions raised inside the context manager are downgraded to warnings."""
        entry = SimpleNamespace(status="unreviewed", summary="")

        @contextmanager
        def _fake_rmw_raises(_):
            yield SimpleNamespace(files={"/src/main.py": entry})
            raise RuntimeError("disk full")

        with patch(
            "agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state",
            side_effect=_fake_rmw_raises,
        ):
            _update_review_state_for_file(
                123,
                "/src/main.py",
                FileReviewResult(
                    file_path="/src/main.py",
                    outcome="approve",
                    summary="OK",
                ),
            )

        assert "failed to save review state" in capsys.readouterr().err

    def test_persists_draft_suggestions_with_placeholder_ids(self) -> None:
        """Draft suggestions are persisted with threadId=0 / commentId=0 sentinels."""
        from agentic_devtools.cli.azure_devops.review_state import SuggestionEntry

        entry = SimpleNamespace(status="unreviewed", summary="", suggestions=[])
        review_state = SimpleNamespace(files={"/src/main.py": entry})

        @contextmanager
        def _fake_rmw(_):
            yield review_state

        with patch(
            "agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state",
            side_effect=_fake_rmw,
        ):
            _update_review_state_for_file(
                123,
                "/src/main.py",
                FileReviewResult(
                    file_path="/src/main.py",
                    outcome="request-changes",
                    summary="Needs a fix.",
                    suggestions=[
                        {
                            "severity": "high",
                            "content": "Fix this!",
                            "line": 5,
                            "endLine": 7,
                            "out_of_scope": False,
                            "replacement_code": "return 0",
                        }
                    ],
                ),
            )

        assert len(entry.suggestions) == 1
        s = entry.suggestions[0]
        assert isinstance(s, SuggestionEntry)
        assert s.threadId == 0  # draft: not yet posted to ADO
        assert s.commentId == 0  # draft: not yet posted to ADO
        assert s.severity == "high"
        assert s.content == "Fix this!"
        assert s.line == 5
        assert s.endLine == 7
        assert s.linkText == ""  # populated after ADO post
        assert s.replacement_code == "return 0"
        assert s.outOfScope is False

    def test_draft_suggestion_end_line_falls_back_to_line_when_none(self) -> None:
        """When endLine is None the draft suggestion uses line as endLine."""
        entry = SimpleNamespace(status="unreviewed", summary="", suggestions=[])
        review_state = SimpleNamespace(files={"/src/main.py": entry})

        @contextmanager
        def _fake_rmw(_):
            yield review_state

        with patch(
            "agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state",
            side_effect=_fake_rmw,
        ):
            _update_review_state_for_file(
                123,
                "/src/main.py",
                FileReviewResult(
                    file_path="/src/main.py",
                    outcome="request-changes",
                    summary="Issue found.",
                    suggestions=[
                        {
                            "severity": "medium",
                            "content": "Check this.",
                            "line": 10,
                            "endLine": None,
                            "out_of_scope": False,
                            "replacement_code": None,
                        }
                    ],
                ),
            )

        assert len(entry.suggestions) == 1
        s = entry.suggestions[0]
        assert s.line == 10
        assert s.endLine == 10  # fallback to line when endLine is None

    def test_persists_empty_suggestions_when_no_findings(self) -> None:
        """When the result has no suggestions, the entry's suggestions list is cleared."""
        entry = SimpleNamespace(status="unreviewed", summary="", suggestions=["old"])
        review_state = SimpleNamespace(files={"/src/main.py": entry})

        @contextmanager
        def _fake_rmw(_):
            yield review_state

        with patch(
            "agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state",
            side_effect=_fake_rmw,
        ):
            _update_review_state_for_file(
                123,
                "/src/main.py",
                FileReviewResult(
                    file_path="/src/main.py",
                    outcome="approve",
                    summary="All good.",
                    suggestions=[],
                ),
            )

        assert entry.suggestions == []

    def test_persists_draft_suggestions_from_non_dict_suggestion_objects(self) -> None:
        """Non-dict suggestion objects (e.g. SuggestionOutput) are handled via getattr."""
        from agentic_devtools.cli.azure_devops.review_state import SuggestionEntry

        entry = SimpleNamespace(status="unreviewed", summary="", suggestions=[])
        review_state = SimpleNamespace(files={"/src/main.py": entry})

        # Build a non-dict suggestion (SuggestionOutput is a Pydantic model, not a dict)
        suggestion_obj = SuggestionOutput(severity="low", content="Note this.", line=3)

        @contextmanager
        def _fake_rmw(_):
            yield review_state

        with patch(
            "agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state",
            side_effect=_fake_rmw,
        ):
            _update_review_state_for_file(
                123,
                "/src/main.py",
                FileReviewResult(
                    file_path="/src/main.py",
                    outcome="approve",
                    summary="Minor note.",
                    suggestions=[suggestion_obj],  # type: ignore[list-item]  # non-dict: uses getattr path
                ),
            )

        assert len(entry.suggestions) == 1
        s = entry.suggestions[0]
        assert isinstance(s, SuggestionEntry)
        assert s.threadId == 0
        assert s.severity == "low"
        assert s.content == "Note this."
        assert s.line == 3
        assert s.endLine == 3  # endLine=None in SuggestionOutput → falls back to line


class TestFormatNumberedFileContent:
    """Tests for _format_numbered_file_content()."""

    def test_basic_multiline(self) -> None:
        """Each line is prefixed with a 1-based line number."""
        result = _format_numbered_file_content("foo\nbar\nbaz")
        lines = result.splitlines()
        assert lines[0].startswith("   1 | foo")
        assert lines[1].startswith("   2 | bar")
        assert lines[2].startswith("   3 | baz")
        assert len(lines) == 3

    def test_trailing_newline_not_counted(self) -> None:
        """A trailing newline must not produce a spurious empty final line."""
        result = _format_numbered_file_content("foo\nbar\n")
        lines = result.splitlines()
        assert len(lines) == 2
        assert lines[0].startswith("   1 | foo")
        assert lines[1].startswith("   2 | bar")

    def test_single_line_no_trailing_newline(self) -> None:
        """Single line without trailing newline yields exactly one numbered line."""
        result = _format_numbered_file_content("only")
        lines = result.splitlines()
        assert len(lines) == 1
        assert lines[0].startswith("   1 | only")

    def test_empty_string(self) -> None:
        """Empty file content yields an empty string."""
        assert _format_numbered_file_content("") == ""


class TestBuildPreEnrichedContext:
    """Tests for _build_pre_enriched_context()."""

    def test_returns_full_content_when_not_truncated(self) -> None:
        """Pre-enriched full content is preserved when no truncation marker is present."""
        full_content = "line 1\nline 2\nline 3\nline 4"
        result = _build_pre_enriched_context(
            {"full_content_source": full_content, "addedLines": [{"line": 3}]},
            content_key="full_content_source",
            line_key="addedLines",
            bound_fallback_context=lambda content: f"bounded::{content}",
            extract_surrounding_context=lambda content, _ranges: f"surrounding::{content}",
        )
        assert result == full_content

    def test_ignores_malformed_line_metadata(self) -> None:
        """Malformed line metadata does not raise and still returns full content."""
        full_content = "line 1\nline 2\nline 3\nline 4"
        result = _build_pre_enriched_context(
            {"full_content_source": full_content, "addedLines": [None, {"line": "3"}, {"line": 2}, "x"]},
            content_key="full_content_source",
            line_key="addedLines",
            bound_fallback_context=lambda content: content,
            extract_surrounding_context=lambda content, _ranges: content,
        )
        assert result == full_content

    def test_ignores_non_list_line_metadata_container(self) -> None:
        """Non-list line metadata containers are ignored safely."""
        full_content = "line 1\nline 2\nline 3"
        result = _build_pre_enriched_context(
            {"full_content_source": full_content, "addedLines": {"line": 2}},
            content_key="full_content_source",
            line_key="addedLines",
            bound_fallback_context=lambda content: content,
            extract_surrounding_context=lambda content, _ranges: content,
        )
        assert result == full_content
