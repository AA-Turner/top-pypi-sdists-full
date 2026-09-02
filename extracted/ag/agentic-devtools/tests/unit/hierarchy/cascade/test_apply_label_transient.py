"""Tests for _apply_label transient error retry exhaustion."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.hierarchy.cascade import CascadeApiRetryExhaustedError, CascadeProcessor


class TestApplyLabelTransient:
    """Tests that _apply_label handles transient errors via retry."""

    def test_transient_error_exhausts_retries_raises(self) -> None:
        """When all retry attempts hit transient HTTP errors, raises."""
        processor = CascadeProcessor(owner="org", repo="repo")

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "HTTP 502 Bad Gateway"
        mock_result.stdout = ""  # no Retry-After header in response

        with (
            patch("agentic_devtools.hierarchy.cascade.run_safe", return_value=mock_result),
            patch("agentic_devtools.hierarchy.cascade.time.sleep"),
            pytest.raises(CascadeApiRetryExhaustedError, match="Retry exhausted applying"),
        ):
            processor._apply_label(42)

    def test_transient_429_exhausts_retries_raises(self) -> None:
        """Transient 429 error triggers retry; if all fail, raises."""
        processor = CascadeProcessor(owner="org", repo="repo")

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "HTTP 429 Too Many Requests"
        mock_result.stdout = ""  # no Retry-After header in response

        with (
            patch("agentic_devtools.hierarchy.cascade.run_safe", return_value=mock_result),
            patch("agentic_devtools.hierarchy.cascade.time.sleep"),
            pytest.raises(CascadeApiRetryExhaustedError, match="Retry exhausted applying"),
        ):
            processor._apply_label(42)

    def test_retry_after_header_is_honoured(self) -> None:
        """When Retry-After header is in --include output, that delay is used (NFR-005)."""
        processor = CascadeProcessor(owner="org", repo="repo")

        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            mock = MagicMock()
            if call_count == 1:
                mock.returncode = 1
                mock.stderr = "HTTP 429 Too Many Requests"
                mock.stdout = "HTTP/2 429\nRetry-After: 45\nContent-Type: application/json\n\n{}"
            else:
                mock.returncode = 0
                mock.stdout = "[]"
                mock.stderr = ""
            return mock

        with patch("agentic_devtools.hierarchy.cascade.run_safe", side_effect=side_effect) as _:
            with patch("agentic_devtools.hierarchy.cascade.time.sleep") as mock_sleep:
                result = processor._apply_label(42)

        assert result is True
        # Asserts that time.sleep was called exactly once with the Retry-After value (45s),
        # not the exponential backoff default (1s for first retry).
        mock_sleep.assert_called_once_with(45.0)
