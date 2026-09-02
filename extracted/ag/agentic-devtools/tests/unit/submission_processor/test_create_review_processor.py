"""Tests for agentic_devtools.submission_processor.create_review_processor."""

from unittest.mock import MagicMock, patch

from agentic_devtools.submission_processor import create_review_processor

from .conftest import REPO_ID, make_item


class TestCreateReviewProcessor:
    """Tests for create_review_processor factory function."""

    @patch("agentic_devtools.submission_processor.fetch_reviewer_context")
    @patch("agentic_devtools.submission_processor.process_submission")
    def test_returns_callable_that_invokes_process_submission(self, mock_process, mock_fetch, config):
        """Verify create_review_processor returns a callable that invokes process_submission."""
        headers = {"Auth": "x"}
        mock_requests = MagicMock()
        mock_fetch.return_value = None

        processor = create_review_processor(config, headers, REPO_ID, requests_module=mock_requests)
        assert callable(processor)

        item = make_item()
        processor(item)

        mock_fetch.assert_called_once_with(config)
        mock_process.assert_called_once_with(
            item,
            config,
            headers,
            REPO_ID,
            requests_module=mock_requests,
            cached_context=None,
        )

    @patch("agentic_devtools.submission_processor.fetch_reviewer_context")
    @patch("agentic_devtools.submission_processor.process_submission")
    def test_prefetches_reviewer_context(self, mock_process, mock_fetch, config):
        """Verify the factory prefetches reviewer context when none is supplied."""
        cached_context = MagicMock()
        mock_fetch.return_value = cached_context

        processor = create_review_processor(config, {}, REPO_ID)
        processor(make_item())

        mock_fetch.assert_called_once_with(config)
        assert mock_process.call_args.kwargs["cached_context"] is cached_context

    @patch("agentic_devtools.submission_processor.fetch_reviewer_context", side_effect=RuntimeError("network error"))
    @patch("agentic_devtools.submission_processor.process_submission")
    def test_handles_prefetch_failure(self, mock_process, mock_fetch, config):
        """Verify prefetch failures leave a callable that submits without cached context."""
        processor = create_review_processor(config, {}, REPO_ID)
        processor(make_item())

        mock_fetch.assert_called_once_with(config)
        assert mock_process.call_args.kwargs["cached_context"] is None

    @patch("agentic_devtools.submission_processor.fetch_reviewer_context")
    @patch("agentic_devtools.submission_processor.process_submission")
    def test_uses_explicit_reviewer_context(self, mock_process, mock_fetch, config):
        """Verify an explicit reviewer context bypasses prefetch and is forwarded."""
        cached_context = MagicMock()

        processor = create_review_processor(config, {}, REPO_ID, cached_context=cached_context)
        processor(make_item())

        mock_fetch.assert_not_called()
        assert mock_process.call_args.kwargs["cached_context"] is cached_context

    @patch("agentic_devtools.submission_processor.fetch_reviewer_context")
    @patch("agentic_devtools.submission_processor.process_submission")
    def test_deferred_mode_skips_reviewer_prefetch_and_forwards_flag(self, mock_process, mock_fetch, config):
        """Deferred mode leaves shared reviewer context to the batch finalizer."""
        processor = create_review_processor(config, {}, REPO_ID, defer_shared_updates=True)
        processor(make_item())

        mock_fetch.assert_not_called()
        mock_process.assert_called_once()
        assert mock_process.call_args.kwargs["cached_context"] is None
        assert mock_process.call_args.kwargs["defer_shared_updates"] is True
