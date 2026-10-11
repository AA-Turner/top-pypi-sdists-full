"""Tests for dealcloud_sdk.data.pagination."""

import logging

import pytest
from unittest.mock import MagicMock

from intapp_rest_client.models import ErrorHandling

from dealcloud_sdk.data.pagination import (
    parallel_requests_get,
    parallel_requests_post,
    paginated_read_until_empty,
    parallel_get,
    parallel_post,
    paginated_read,
)
from dealcloud_sdk.data.models import BatchResult


class TestParallelRequestsGet:
    """Tests for parallel_requests_get."""

    def test_returns_parallel_get_result(self):
        """Returns whatever client.parallel_get returns."""
        client = MagicMock()
        client.parallel_get.return_value = [{"rows": [{"id": 1}]}, {"rows": [{"id": 2}]}]
        result = parallel_requests_get(client, ["/a", "/b"], max_workers=2)
        assert result == [{"rows": [{"id": 1}]}, {"rows": [{"id": 2}]}]
        client.parallel_get.assert_called_once_with(
            endpoints=["/a", "/b"],
            max_workers=2,
            error_handling=ErrorHandling.FAIL_FAST,
        )

    def test_passes_error_handling(self):
        """Passes error_handling to client.parallel_get."""
        client = MagicMock()
        client.parallel_get.return_value = ([], [])
        parallel_requests_get(
            client, ["/a"], max_workers=1, error_handling=ErrorHandling.COLLECT
        )
        client.parallel_get.assert_called_once_with(
            endpoints=["/a"],
            max_workers=1,
            error_handling=ErrorHandling.COLLECT,
        )


class TestParallelRequestsPost:
    """Tests for parallel_requests_post."""

    def test_returns_parallel_post_result(self):
        """Returns whatever client.parallel_post returns."""
        client = MagicMock()
        client.parallel_post.return_value = [{"rows": [{"id": 1}]}]
        result = parallel_requests_post(
            client, "/query", [{"limit": 10}], max_workers=1
        )
        assert result == [{"rows": [{"id": 1}]}]
        client.parallel_post.assert_called_once_with(
            endpoint="/query",
            payloads=[{"limit": 10}],
            max_workers=1,
            error_handling=ErrorHandling.FAIL_FAST,
        )

    def test_passes_error_handling(self):
        """Passes error_handling to client.parallel_post."""
        client = MagicMock()
        client.parallel_post.return_value = ([], [])
        parallel_requests_post(
            client, "/url", [{}], max_workers=1, error_handling=ErrorHandling.LOG_ONLY
        )
        client.parallel_get.assert_not_called()
        client.parallel_post.assert_called_once_with(
            endpoint="/url",
            payloads=[{}],
            max_workers=1,
            error_handling=ErrorHandling.LOG_ONLY,
        )


class TestPaginatedReadUntilEmpty:
    """Tests for paginated_read_until_empty."""

    def test_get_stops_on_empty_page_fail_fast(self):
        """GET path stops when empty rows returned; FAIL_FAST returns list."""
        client = MagicMock()
        client.parallel_get.return_value = [
            {"rows": [{"EntryId": 1}], "totalRecords": 1},
            {"rows": []},
        ]
        result = paginated_read_until_empty(
            client, "https://api.gmail.co/rows", method="GET", page_size=100
        )
        assert result == [{"EntryId": 1}]
        client.parallel_get.assert_called_once()

    def test_get_multiple_pages(self):
        """GET path continues until empty page."""
        client = MagicMock()
        client.parallel_get.side_effect = [
            [
                {"rows": [{"EntryId": i} for i in range(1, 4)]},
                {"rows": [{"EntryId": i} for i in range(4, 7)]},
            ],
            [{"rows": [{"EntryId": 7}]}, {"rows": []}],
        ]
        result = paginated_read_until_empty(
            client, "https://api.gmail.co/rows", method="GET", page_size=3, max_workers=2
        )
        assert len(result) == 7
        assert result[0]["EntryId"] == 1
        assert result[6]["EntryId"] == 7
        assert client.parallel_get.call_count == 2

    def test_post_stops_on_empty_page(self):
        """POST path stops when empty rows returned."""
        client = MagicMock()
        client.parallel_post.return_value = [
            {"rows": [{"EntryId": 1}]},
            {"rows": []},
        ]
        result = paginated_read_until_empty(
            client,
            "https://api.gmail.co/query",
            method="POST",
            request_body={"filter": "x"},
            page_size=100,
        )
        assert result == [{"EntryId": 1}]
        client.parallel_post.assert_called_once()
        call_kw = client.parallel_post.call_args[1]
        assert call_kw["endpoint"] == "https://api.gmail.co/query"
        assert len(call_kw["payloads"]) >= 1
        assert call_kw["payloads"][0].get("limit") == 100
        assert call_kw["payloads"][0].get("filter") == "x"

    def test_collect_returns_batch_result(self):
        """COLLECT error_handling returns BatchResult."""
        client = MagicMock()
        client.parallel_get.return_value = (
            [{"rows": [{"EntryId": 1}]}, {"rows": []}],
            [],
        )
        result = paginated_read_until_empty(
            client,
            "https://api.gmail.co/rows",
            method="GET",
            page_size=100,
            max_workers=2,
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(result, BatchResult)
        assert result.results == [{"EntryId": 1}]
        assert result.total_succeeded == 1

    def test_progress_callback_called(self):
        """Progress callback is called when provided."""
        client = MagicMock()
        client.parallel_get.return_value = [{"rows": [{"EntryId": 1}]}, {"rows": []}]
        progress_calls = []
        result = paginated_read_until_empty(
            client,
            "https://api.gmail.co/rows",
            method="GET",
            page_size=100,
            progress_callback=lambda cur, tot: progress_calls.append((cur, tot)),
        )
        assert len(progress_calls) >= 1
        assert progress_calls[0][0] == 1

    def test_explicit_logger_skips_default_getLogger(self):
        """When logger is passed, paginated_read_until_empty does not replace it."""
        client = MagicMock()
        client.parallel_get.return_value = [{"rows": []}]
        log = logging.getLogger("pagination.test_explicit")
        paginated_read_until_empty(
            client,
            "https://api.example/rows",
            method="GET",
            page_size=10,
            max_workers=1,
            logger=log,
        )

    def test_get_base_url_with_query_string_appends_skip_with_ampersand(self):
        client = MagicMock()
        client.parallel_get.return_value = [{"rows": []}]
        paginated_read_until_empty(
            client,
            "https://api.example/rows?filter=1",
            method="GET",
            page_size=50,
            max_workers=1,
        )
        ep = client.parallel_get.call_args[1]["endpoints"][0]
        assert "filter=1" in ep
        assert "skip=0" in ep

    def test_get_base_url_with_existing_skip_parameter(self):
        client = MagicMock()
        client.parallel_get.return_value = [{"rows": []}]
        paginated_read_until_empty(
            client,
            "https://api.example/rows?skip=0",
            method="GET",
            page_size=50,
            max_workers=1,
        )
        assert client.parallel_get.call_args[1]["endpoints"][0] == (
            "https://api.example/rows?skip=0"
        )

    def test_post_collect_merges_parallel_errors(self):
        client = MagicMock()
        client.parallel_post.return_value = (
            [{"rows": [{"id": 1}]}, {"rows": []}],
            [{"error": "bad"}],
        )
        result = paginated_read_until_empty(
            client,
            "https://api.example/query",
            method="POST",
            request_body={"q": "x"},
            page_size=100,
            max_workers=2,
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(result, BatchResult)
        assert len(result.errors) == 1

    def test_progress_callback_logs_warning_on_exception(self, caplog):
        client = MagicMock()
        client.parallel_get.return_value = [{"rows": []}]

        def bad_cb(c, t):
            raise RuntimeError("cb")

        with caplog.at_level(logging.WARNING):
            paginated_read_until_empty(
                client,
                "https://api.example/rows",
                method="GET",
                page_size=10,
                max_workers=1,
                progress_callback=bad_cb,
            )
        assert any("Progress callback failed" in r.message for r in caplog.records)

    def test_progress_estimated_total_when_full_speculative_batch(self):
        client = MagicMock()
        client.parallel_get.side_effect = [
            [
                {"rows": [{"EntryId": i} for i in range(1, 4)]},
                {"rows": [{"EntryId": i} for i in range(4, 7)]},
            ],
            [{"rows": [{"EntryId": 7}]}, {"rows": []}],
        ]
        estimates = []
        paginated_read_until_empty(
            client,
            "https://api.example/rows",
            method="GET",
            page_size=3,
            max_workers=2,
            progress_callback=lambda cur, tot: estimates.append((cur, tot)),
        )
        assert len(estimates) >= 1
        assert estimates[0][1] > estimates[0][0]


class TestParallelGet:
    """Tests for parallel_get (wrapper)."""

    def test_calls_client_parallel_get(self):
        """Calls client.parallel_get with correct args."""
        client = MagicMock()
        client.parallel_get.return_value = [{"a": 1}]
        result = parallel_get(client, ["/u1", "/u2"], max_workers=4)
        assert result == [{"a": 1}]
        client.parallel_get.assert_called_once_with(
            endpoints=["/u1", "/u2"],
            max_workers=4,
            error_handling=ErrorHandling.FAIL_FAST,
        )


class TestParallelPost:
    """Tests for parallel_post (wrapper)."""

    def test_calls_client_parallel_post(self):
        """Calls client.parallel_post with correct args."""
        client = MagicMock()
        client.parallel_post.return_value = [{"a": 1}]
        result = parallel_post(client, "/url", [{"x": 1}], max_workers=2)
        assert result == [{"a": 1}]
        client.parallel_post.assert_called_once_with(
            endpoint="/url",
            payloads=[{"x": 1}],
            max_workers=2,
            error_handling=ErrorHandling.FAIL_FAST,
        )


class TestPaginatedRead:
    """Tests for paginated_read (delegates to paginated_read_until_empty)."""

    def test_delegates_to_paginated_read_until_empty(self):
        """paginated_read calls paginated_read_until_empty with same args."""
        client = MagicMock()
        client.parallel_get.return_value = [{"rows": []}]
        result = paginated_read(
            client, "https://api.gmail.co/rows", page_size=500, max_workers=4
        )
        assert result == []
        client.parallel_get.assert_called_once()
        call_kw = client.parallel_get.call_args[1]
        assert "skip=0" in call_kw["endpoints"][0] or "skip=0" in str(call_kw["endpoints"])
