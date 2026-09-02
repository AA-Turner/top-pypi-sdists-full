"""Tests for retrieve_files_concurrent function."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.orchestration.review.file_retriever import RetrievalResult, retrieve_files_concurrent


class TestRetrieveFilesConcurrent:
    """Tests for concurrent file retrieval."""

    def test_deduplicates_requests(self) -> None:
        """Duplicate (path, branch_side) requests are deduplicated."""
        requests = [
            ("/src/a.py", "abc", "source"),
            ("/src/a.py", "abc", "source"),  # duplicate
            ("/src/a.py", "def", "target"),
        ]

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_file_content") as mock_retrieve:
            mock_retrieve.return_value = RetrievalResult(content="ok", context_status="success")
            results = retrieve_files_concurrent(requests, {})

        # Should only have 2 unique keys
        assert len(results) == 2
        assert ("/src/a.py", "source") in results
        assert ("/src/a.py", "target") in results

    def test_respects_max_concurrency(self) -> None:
        """Max concurrency limits parallel workers."""
        requests = [(f"/src/f{i}.py", "abc", "source") for i in range(20)]

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_file_content") as mock_retrieve:
            mock_retrieve.return_value = RetrievalResult(content="ok", context_status="success")
            results = retrieve_files_concurrent(requests, {}, max_concurrency=5)

        assert len(results) == 20

    def test_invalid_max_concurrency_falls_back_to_one(self) -> None:
        """Non-numeric max_concurrency does not crash and falls back safely."""
        requests = [("/src/a.py", "abc", "source")]

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_file_content") as mock_retrieve:
            mock_retrieve.return_value = RetrievalResult(content="ok", context_status="success")
            results = retrieve_files_concurrent(requests, {}, max_concurrency="oops")  # type: ignore[arg-type]

        assert len(results) == 1

    def test_empty_requests_returns_empty(self) -> None:
        """Empty request list returns empty results without spawning threads."""
        results = retrieve_files_concurrent([], {})
        assert results == {}

    def test_future_exception_handled(self) -> None:
        """Exception from a future is caught and stored as unavailable."""
        requests = [("/src/app.py", "abc123", "source")]

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_file_content") as mock_retrieve:
            mock_retrieve.side_effect = RuntimeError("unexpected crash")
            results = retrieve_files_concurrent(requests, {})

        key = ("/src/app.py", "source")
        assert results[key].context_status == "unavailable"
        assert "concurrent_error" in results[key].context_status_reason
