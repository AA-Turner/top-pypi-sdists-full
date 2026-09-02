"""Tests for _post_comment transient error retry exhaustion."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.hierarchy.cascade import CascadeApiRetryExhaustedError, CascadeProcessor


class TestPostCommentTransient:
    """Tests that _post_comment handles transient errors via retry."""

    def test_transient_error_exhausts_retries_raises(self) -> None:
        """When all retry attempts hit transient HTTP 503, raises."""
        processor = CascadeProcessor(owner="org", repo="repo")

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "HTTP 503 Service Unavailable"

        with (
            patch("agentic_devtools.hierarchy.cascade.run_safe", return_value=mock_result),
            patch("agentic_devtools.hierarchy.cascade.time.sleep"),
            pytest.raises(CascadeApiRetryExhaustedError, match="Retry exhausted posting"),
        ):
            processor._post_comment(42, "test comment")

    def test_transient_429_exhausts_retries_raises(self) -> None:
        """When all retry attempts hit HTTP 429, raises."""
        processor = CascadeProcessor(owner="org", repo="repo")

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "HTTP 429 rate limit exceeded"

        with (
            patch("agentic_devtools.hierarchy.cascade.run_safe", return_value=mock_result),
            patch("agentic_devtools.hierarchy.cascade.time.sleep"),
            pytest.raises(CascadeApiRetryExhaustedError, match="Retry exhausted posting"),
        ):
            processor._post_comment(42, "test")

    def test_retry_after_header_is_honoured(self) -> None:
        """Uses Retry-After header delay for 429 when available."""
        processor = CascadeProcessor(owner="org", repo="repo")
        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            mock = MagicMock()
            if call_count == 1:
                mock.returncode = 1
                mock.stderr = "HTTP 429 Too Many Requests"
                mock.stdout = "HTTP/2 429\nRetry-After: 45\n\n{}"
            else:
                mock.returncode = 0
                mock.stderr = ""
                mock.stdout = "{}"
            return mock

        with patch("agentic_devtools.hierarchy.cascade.run_safe", side_effect=side_effect):
            with patch("agentic_devtools.hierarchy.cascade.time.sleep") as mock_sleep:
                result = processor._post_comment(42, "test")

        assert result is True
        mock_sleep.assert_called_once_with(45.0)
