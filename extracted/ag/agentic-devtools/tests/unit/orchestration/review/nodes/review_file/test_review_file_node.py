"""Tests for review_file_node()."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.execution.types import ReasoningResponse
from agentic_devtools.orchestration.review.nodes.review_file import review_file_node
from agentic_devtools.orchestration.schemas._validation import SchemaValidationError


class TestReviewFileNode:
    """Tests for review_file_node() graph node."""

    def _make_context(self, reasoning_response: ReasoningResponse) -> MagicMock:
        """Create a mock ExecutionContext."""
        context = MagicMock()
        context.reasoning.invoke.return_value = reasoning_response
        context.tools.invoke.return_value = {"success": True}
        return context

    def test_missing_file_key_returns_error(self) -> None:
        """Returns error when neither file_path nor file_key is in state."""
        context = MagicMock()
        result = review_file_node({"current_file_key": ""}, context=context)
        assert result["status"] == "failed"
        assert result["error"]["type"] == "missing_input"
        assert "file_path" in result["error"]["message"]

    def test_approve_outcome(self) -> None:
        """Approve outcome invokes approve tool."""
        response: ReasoningResponse[Any] = ReasoningResponse(
            raw_text='{"outcome": "approve", "summary": "Looks good", "suggestions": []}'
        )
        context = self._make_context(response)

        with patch("agentic_devtools.orchestration.schemas._validation.validate_llm_output") as mock_validate:
            mock_verdict = MagicMock()
            mock_verdict.outcome = "approve"
            mock_verdict.summary = "Looks good"
            mock_validate.return_value = mock_verdict

            result = review_file_node(
                {
                    "current_file_key": "src/main.py",
                    "current_file_diff": "diff content",
                    "review_prompt": "",
                },
                context=context,
            )

        assert result["status"] == "completed"
        assert result["current_file_outcome"] == "approve"
        context.tools.invoke.assert_called_once_with(
            "azure_devops_approve_file",
            node_name="review_file_node",
            file_path="src/main.py",
            summary="Looks good",
        )

    def test_request_changes_outcome(self) -> None:
        """Request-changes outcome invokes request_changes tool."""
        response: ReasoningResponse[Any] = ReasoningResponse(
            raw_text='{"outcome": "request-changes", "summary": "Fix bug", "suggestions": []}'
        )
        context = self._make_context(response)

        with patch("agentic_devtools.orchestration.schemas._validation.validate_llm_output") as mock_validate:
            mock_verdict = MagicMock()
            mock_verdict.outcome = "request-changes"
            mock_verdict.summary = "Fix bug"
            mock_verdict.suggestions = []
            mock_validate.return_value = mock_verdict

            result = review_file_node(
                {
                    "current_file_key": "src/main.py",
                    "current_file_diff": "diff",
                    "review_prompt": "Review this",
                },
                context=context,
            )

        assert result["status"] == "completed"
        assert result["current_file_outcome"] == "request-changes"
        context.tools.invoke.assert_called_once_with(
            "azure_devops_request_changes",
            node_name="review_file_node",
            file_path="src/main.py",
            summary="Fix bug",
            suggestions=[],
        )

    def test_request_changes_with_suggestion_outcome(self) -> None:
        """Request-changes-with-suggestion invokes appropriate tool."""
        raw = (
            '{"outcome": "request-changes-with-suggestion",'
            ' "summary": "Add type hint",'
            ' "suggestions": [{"description": "add type"}]}'
        )
        response: ReasoningResponse[Any] = ReasoningResponse(raw_text=raw)
        context = self._make_context(response)

        with patch("agentic_devtools.orchestration.schemas._validation.validate_llm_output") as mock_validate:
            mock_verdict = MagicMock()
            mock_verdict.outcome = "request-changes-with-suggestion"
            mock_verdict.summary = "Add type hint"
            mock_verdict.suggestions = [{"description": "add type"}]
            mock_validate.return_value = mock_verdict

            result = review_file_node(
                {
                    "current_file_key": "src/main.py",
                    "current_file_diff": "diff",
                    "review_prompt": "",
                },
                context=context,
            )

        assert result["status"] == "completed"
        assert result["current_file_outcome"] == "request-changes-with-suggestion"
        context.tools.invoke.assert_called_once_with(
            "azure_devops_request_changes_with_suggestion",
            node_name="review_file_node",
            file_path="src/main.py",
            summary="Add type hint",
            suggestions=[{"description": "add type"}],
        )

    def test_uses_review_prompt_when_provided(self) -> None:
        """Uses review_prompt from state when available."""
        response: ReasoningResponse[Any] = ReasoningResponse(
            raw_text='{"outcome": "approve", "summary": "", "suggestions": []}'
        )
        context = self._make_context(response)

        with patch("agentic_devtools.orchestration.schemas._validation.validate_llm_output") as mock_validate:
            mock_verdict = MagicMock()
            mock_verdict.outcome = "approve"
            mock_verdict.summary = ""
            mock_validate.return_value = mock_verdict

            review_file_node(
                {
                    "current_file_key": "src/main.py",
                    "current_file_diff": "diff content",
                    "review_prompt": "Custom prompt here",
                },
                context=context,
            )

        # Verify the custom prompt was passed to reasoning
        context.reasoning.invoke.assert_called_once()
        call_args = context.reasoning.invoke.call_args
        assert call_args[0][0] == "Custom prompt here"

    def test_fallback_prompt_uses_diff(self) -> None:
        """Falls back to diff-based prompt when review_prompt is empty."""
        response: ReasoningResponse[Any] = ReasoningResponse(
            raw_text='{"outcome": "approve", "summary": "", "suggestions": []}'
        )
        context = self._make_context(response)

        with patch("agentic_devtools.orchestration.schemas._validation.validate_llm_output") as mock_validate:
            mock_verdict = MagicMock()
            mock_verdict.outcome = "approve"
            mock_verdict.summary = ""
            mock_validate.return_value = mock_verdict

            review_file_node(
                {
                    "current_file_key": "src/main.py",
                    "current_file_diff": "my diff content",
                    "review_prompt": "",
                },
                context=context,
            )

        call_args = context.reasoning.invoke.call_args
        assert "my diff content" in call_args[0][0]

    def test_unknown_outcome_returns_failed(self) -> None:
        """Unknown outcome returns status='failed' so the pipeline does not silently proceed."""
        response: ReasoningResponse[Any] = ReasoningResponse(
            raw_text='{"outcome": "unknown", "summary": "Unsure", "suggestions": []}'
        )
        context = self._make_context(response)

        with patch("agentic_devtools.orchestration.schemas._validation.validate_llm_output") as mock_validate:
            mock_verdict = MagicMock()
            mock_verdict.outcome = "unknown"
            mock_verdict.summary = "Unsure"
            mock_validate.return_value = mock_verdict

            result = review_file_node(
                {
                    "current_file_key": "src/main.py",
                    "current_file_diff": "diff",
                    "review_prompt": "",
                },
                context=context,
            )

        assert result["status"] == "failed"
        assert result["error"]["type"] == "unrecognized_outcome"
        assert "unknown" in result["error"]["message"]
        context.tools.invoke.assert_not_called()

    def test_tool_returns_unsuccessful_result_returns_failed(self) -> None:
        """Tool-level failure result is propagated as node failure."""
        response: ReasoningResponse[Any] = ReasoningResponse(
            raw_text='{"outcome": "approve", "summary": "Looks good", "suggestions": []}'
        )
        context = self._make_context(response)
        context.tools.invoke.return_value = {"success": False, "error": "api failed"}

        with patch("agentic_devtools.orchestration.schemas._validation.validate_llm_output") as mock_validate:
            mock_verdict = MagicMock()
            mock_verdict.outcome = "approve"
            mock_verdict.summary = "Looks good"
            mock_validate.return_value = mock_verdict

            result = review_file_node(
                {
                    "current_file_key": "src/main.py",
                    "current_file_diff": "diff content",
                    "review_prompt": "",
                },
                context=context,
            )

        assert result["status"] == "failed"
        assert result["error"]["type"] == "tool_invoke_failed"
        assert result["error"]["tool"] == "azure_devops_approve_file"

    def test_tool_failure_surfaces_error_message_from_executor_envelope(self) -> None:
        """ToolExecutor envelope error_message is propagated when success is false."""
        response: ReasoningResponse[Any] = ReasoningResponse(
            raw_text='{"outcome": "approve", "summary": "Looks good", "suggestions": []}'
        )
        context = self._make_context(response)
        context.tools.invoke.return_value = {
            "success": False,
            "error_message": "executor failed while posting",
        }

        with patch("agentic_devtools.orchestration.schemas._validation.validate_llm_output") as mock_validate:
            mock_verdict = MagicMock()
            mock_verdict.outcome = "approve"
            mock_verdict.summary = "Looks good"
            mock_validate.return_value = mock_verdict

            result = review_file_node(
                {
                    "current_file_key": "src/main.py",
                    "current_file_diff": "diff content",
                    "review_prompt": "",
                },
                context=context,
            )

        assert result["status"] == "failed"
        assert result["error"]["type"] == "tool_invoke_failed"
        assert result["error"]["message"] == "executor failed while posting"

    def test_tool_invoke_exception_returns_failed(self) -> None:
        """Tool invocation exceptions are converted into structured failure output."""
        response: ReasoningResponse[Any] = ReasoningResponse(
            raw_text='{"outcome": "approve", "summary": "Looks good", "suggestions": []}'
        )
        context = self._make_context(response)
        context.tools.invoke.side_effect = RuntimeError("network error")

        with patch("agentic_devtools.orchestration.schemas._validation.validate_llm_output") as mock_validate:
            mock_verdict = MagicMock()
            mock_verdict.outcome = "approve"
            mock_verdict.summary = "Looks good"
            mock_validate.return_value = mock_verdict

            result = review_file_node(
                {
                    "current_file_key": "src/main.py",
                    "current_file_diff": "diff content",
                    "review_prompt": "",
                },
                context=context,
            )

        assert result["status"] == "failed"
        assert result["error"]["type"] == "tool_invoke_exception"
        assert result["error"]["tool"] == "azure_devops_approve_file"
        assert "network error" in result["error"]["message"]

    def test_schema_validation_error_returns_failed(self) -> None:
        """Schema validation errors are converted into structured failure output."""
        response: ReasoningResponse[Any] = ReasoningResponse(raw_text='{"outcome":"approve"}')
        context = self._make_context(response)

        with patch("agentic_devtools.orchestration.schemas._validation.validate_llm_output") as mock_validate:
            mock_validate.side_effect = SchemaValidationError(
                model_name="ReviewVerdict",
                raw_input="not valid json",
                errors=[{"loc": ("outcome",), "msg": "invalid", "type": "value_error"}],
            )

            result = review_file_node(
                {
                    "current_file_key": "src/main.py",
                    "current_file_diff": "diff content",
                    "review_prompt": "",
                },
                context=context,
            )

        assert result["status"] == "failed"
        assert result["error"]["type"] == "schema_validation_failed"
        assert "ReviewVerdict" in result["error"]["message"]

    def test_submission_item_surfaced_in_completed_result(self) -> None:
        """submission_item from the tool result is included in the completed state."""
        response: ReasoningResponse[Any] = ReasoningResponse(
            raw_text='{"outcome": "approve", "summary": "Looks good", "suggestions": []}'
        )
        context = self._make_context(response)
        expected_item = {"file_path": "src/main.py", "outcome": "approve", "summary": "Looks good"}
        context.tools.invoke.return_value = {"success": True, "submission_item": expected_item}

        with patch("agentic_devtools.orchestration.schemas._validation.validate_llm_output") as mock_validate:
            mock_verdict = MagicMock()
            mock_verdict.outcome = "approve"
            mock_verdict.summary = "Looks good"
            mock_validate.return_value = mock_verdict

            result = review_file_node(
                {
                    "current_file_key": "src/main.py",
                    "current_file_diff": "diff content",
                    "review_prompt": "",
                },
                context=context,
            )

        assert result["status"] == "completed"
        assert result["current_file_submission_item"] == expected_item

    def test_no_submission_item_when_tool_returns_none(self) -> None:
        """current_file_submission_item is absent when tool result has no submission_item."""
        response: ReasoningResponse[Any] = ReasoningResponse(
            raw_text='{"outcome": "approve", "summary": "Looks good", "suggestions": []}'
        )
        context = self._make_context(response)
        context.tools.invoke.return_value = {"success": True}

        with patch("agentic_devtools.orchestration.schemas._validation.validate_llm_output") as mock_validate:
            mock_verdict = MagicMock()
            mock_verdict.outcome = "approve"
            mock_verdict.summary = "Looks good"
            mock_validate.return_value = mock_verdict

            result = review_file_node(
                {
                    "current_file_key": "src/main.py",
                    "current_file_diff": "diff content",
                    "review_prompt": "",
                },
                context=context,
            )

        assert result["status"] == "completed"
        assert "current_file_submission_item" not in result

    def test_submission_item_surfaced_from_tool_executor_output_envelope(self) -> None:
        """submission_item is read from tool_result["output"] when using ToolExecutor envelope."""
        response: ReasoningResponse[Any] = ReasoningResponse(
            raw_text='{"outcome": "approve", "summary": "Looks good", "suggestions": []}'
        )
        context = self._make_context(response)
        expected_item = {"file_path": "src/main.py", "outcome": "approve", "summary": "Looks good"}
        context.tools.invoke.return_value = {
            "success": True,
            "output": {"success": True, "submission_item": expected_item},
        }

        with patch("agentic_devtools.orchestration.schemas._validation.validate_llm_output") as mock_validate:
            mock_verdict = MagicMock()
            mock_verdict.outcome = "approve"
            mock_verdict.summary = "Looks good"
            mock_validate.return_value = mock_verdict

            result = review_file_node(
                {
                    "current_file_key": "src/main.py",
                    "current_file_diff": "diff content",
                    "review_prompt": "",
                },
                context=context,
            )

        assert result["status"] == "completed"
        assert result["current_file_submission_item"] == expected_item

    def test_no_submission_item_when_tool_result_is_non_dict(self) -> None:
        """Non-dict tool result still completes and omits submission_item."""
        response: ReasoningResponse[Any] = ReasoningResponse(
            raw_text='{"outcome": "approve", "summary": "Looks good", "suggestions": []}'
        )
        context = self._make_context(response)
        context.tools.invoke.return_value = "ok"

        with patch("agentic_devtools.orchestration.schemas._validation.validate_llm_output") as mock_validate:
            mock_verdict = MagicMock()
            mock_verdict.outcome = "approve"
            mock_verdict.summary = "Looks good"
            mock_validate.return_value = mock_verdict

            result = review_file_node(
                {
                    "current_file_key": "src/main.py",
                    "current_file_diff": "diff content",
                    "review_prompt": "",
                },
                context=context,
            )

        assert result["status"] == "completed"
        assert "current_file_submission_item" not in result

    def test_prefers_current_file_path_over_current_file_key(self) -> None:
        """current_file_path is preferred over current_file_key when both are set."""
        response: ReasoningResponse[Any] = ReasoningResponse(
            raw_text='{"outcome": "approve", "summary": "ok", "suggestions": []}'
        )
        context = self._make_context(response)

        with patch("agentic_devtools.orchestration.schemas._validation.validate_llm_output") as mock_validate:
            mock_verdict = MagicMock()
            mock_verdict.outcome = "approve"
            mock_verdict.summary = "ok"
            mock_validate.return_value = mock_verdict

            review_file_node(
                {
                    "current_file_path": "real/repo/path.py",
                    "current_file_key": "slug-abc123",
                    "current_file_diff": "",
                    "review_prompt": "",
                },
                context=context,
            )

        context.tools.invoke.assert_called_once()
        _, call_kwargs = context.tools.invoke.call_args
        assert call_kwargs["file_path"] == "real/repo/path.py"

    def test_falls_back_to_path_like_current_file_key_when_no_file_path(self) -> None:
        """Falls back only when current_file_key is already a repo-relative path."""
        response: ReasoningResponse[Any] = ReasoningResponse(
            raw_text='{"outcome": "approve", "summary": "ok", "suggestions": []}'
        )
        context = self._make_context(response)

        with patch("agentic_devtools.orchestration.schemas._validation.validate_llm_output") as mock_validate:
            mock_verdict = MagicMock()
            mock_verdict.outcome = "approve"
            mock_verdict.summary = "ok"
            mock_validate.return_value = mock_verdict

            result = review_file_node(
                {
                    "current_file_key": "src/legacy.py",
                    "current_file_diff": "",
                    "review_prompt": "",
                },
                context=context,
            )

        assert result["status"] == "completed"
        _, call_kwargs = context.tools.invoke.call_args
        assert call_kwargs["file_path"] == "src/legacy.py"

    def test_rejects_non_path_like_current_file_key_when_no_file_path(self) -> None:
        """Bare slug+hash file keys are rejected until current_file_path is populated."""
        context = MagicMock()

        result = review_file_node({"current_file_key": "slug-abc123"}, context=context)

        assert result["status"] == "failed"
        assert result["error"]["type"] == "missing_input"
        context.reasoning.invoke.assert_not_called()
        context.tools.invoke.assert_not_called()
