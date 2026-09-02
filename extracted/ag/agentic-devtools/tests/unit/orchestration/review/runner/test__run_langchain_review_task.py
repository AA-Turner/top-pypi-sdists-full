"""Tests for _run_langchain_review_task()."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.orchestration.review.runner import _run_langchain_review_task


class TestRunLangchainReviewTask:
    """Tests for the background task entrypoint wrapper."""

    @patch("agentic_devtools.orchestration.review.runner.run_langchain_review")
    def test_returns_zero_on_success(self, mock_review) -> None:
        """Returns exit code 0 when the review completes successfully."""
        mock_review.return_value = {"overall_decision": "approve", "errors": []}

        result = _run_langchain_review_task(123)

        assert result == 0
        mock_review.assert_called_once_with(
            123,
            source_context_enabled=True,
            model_config=None,
            requested_model=None,
        )

    @patch("agentic_devtools.orchestration.review.runner.run_langchain_review")
    def test_returns_one_on_failed_status(self, mock_review) -> None:
        """Returns exit code 1 when the review result has status == 'failed'."""
        mock_review.return_value = {"status": "failed", "error": "provider auth error", "pr_id": 456}

        result = _run_langchain_review_task(456)

        assert result == 1

    @patch("agentic_devtools.orchestration.review.runner.run_langchain_review")
    def test_forwards_kwargs_to_run_langchain_review(self, mock_review) -> None:
        """Passes source_context_enabled and model_config through to the inner call."""
        mock_review.return_value = {}
        model_cfg = {"default-model": "gpt-4o-mini"}

        _run_langchain_review_task(
            789,
            source_context_enabled=False,
            model_config=model_cfg,
            requested_model="gemini-3.7-flash",
        )

        mock_review.assert_called_once_with(
            789,
            source_context_enabled=False,
            model_config=model_cfg,
            requested_model="gemini-3.7-flash",
        )

    @patch("agentic_devtools.orchestration.review.runner.run_langchain_review")
    def test_returns_zero_for_non_failed_status(self, mock_review) -> None:
        """Returns exit code 0 when the result dict has a status other than 'failed'."""
        mock_review.return_value = {"status": "completed"}

        result = _run_langchain_review_task(111)

        assert result == 0

    @patch("agentic_devtools.orchestration.review.runner.run_langchain_review")
    def test_returns_zero_for_empty_dict(self, mock_review) -> None:
        """Returns exit code 0 for an empty result dict (no status key)."""
        mock_review.return_value = {}

        result = _run_langchain_review_task(222)

        assert result == 0
