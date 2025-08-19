"""Tests for paper search functionality."""

import pytest
import json
from unittest.mock import patch, MagicMock
from arxiv_mcp_server.tools import handle_search
from arxiv_mcp_server.tools.search import _validate_categories, _build_date_filter


@pytest.mark.asyncio
async def test_basic_search(mock_client):
    """Test basic paper search functionality."""
    with patch("arxiv.Client", return_value=mock_client):
        result = await handle_search({"query": "test query", "max_results": 1})

        assert len(result) == 1
        content = json.loads(result[0].text)
        assert content["total_results"] == 1
        paper = content["papers"][0]
        assert paper["id"] == "2103.12345"
        assert paper["title"] == "Test Paper"
        assert "resource_uri" in paper


@pytest.mark.asyncio
async def test_search_with_categories(mock_client):
    """Test paper search with category filtering."""
    with patch("arxiv.Client", return_value=mock_client):
        result = await handle_search(
            {"query": "test query", "categories": ["cs.AI", "cs.LG"], "max_results": 1}
        )

        content = json.loads(result[0].text)
        assert content["papers"][0]["categories"] == ["cs.AI", "cs.LG"]


@pytest.mark.asyncio
async def test_search_with_dates(mock_client):
    """Test paper search with date filtering."""
    with patch("arxiv.Client", return_value=mock_client):
        result = await handle_search(
            {
                "query": "test query",
                "date_from": "2022-01-01",
                "date_to": "2024-01-01",
                "max_results": 1,
            }
        )

        content = json.loads(result[0].text)
        assert content["total_results"] == 1
        assert len(content["papers"]) == 1


@pytest.mark.asyncio
async def test_search_with_invalid_dates(mock_client):
    """Test search with invalid date formats."""
    with patch("arxiv.Client", return_value=mock_client):
        result = await handle_search(
            {"query": "test query", "date_from": "invalid-date", "max_results": 1}
        )

        assert result[0].text.startswith("Error: Invalid date")


def test_validate_categories():
    """Test category validation function."""
    # Valid categories
    assert _validate_categories(["cs.AI", "cs.LG"])
    assert _validate_categories(["math.CO", "physics.gen-ph"])

    # Invalid categories
    assert not _validate_categories(["invalid.category"])
    assert not _validate_categories(["cs.AI", "invalid.test"])


def test_build_date_filter():
    """Test date filter construction."""
    # Test with both dates
    filter_str = _build_date_filter("2023-01-01", "2023-12-31")
    assert "submittedDate:[20230101" in filter_str
    assert "20231231" in filter_str

    # Test with only start date
    filter_str = _build_date_filter("2023-01-01", None)
    assert "submittedDate:[20230101" in filter_str

    # Test with no dates
    assert _build_date_filter(None, None) == ""

    # Test with invalid date
    with pytest.raises(ValueError):
        _build_date_filter("invalid-date", None)


@pytest.mark.asyncio
async def test_search_with_invalid_categories(mock_client):
    """Test search with invalid categories."""
    with patch("arxiv.Client", return_value=mock_client):
        result = await handle_search(
            {
                "query": "test query",
                "categories": ["invalid.category"],
                "max_results": 1,
            }
        )

        assert "Error: Invalid category" in result[0].text


@pytest.mark.asyncio
async def test_search_empty_query(mock_client):
    """Test search with empty query but categories."""
    with patch("arxiv.Client", return_value=mock_client):
        result = await handle_search(
            {"query": "", "categories": ["cs.AI"], "max_results": 1}
        )

        # Should still work with just categories
        content = json.loads(result[0].text)
        assert "papers" in content


@pytest.mark.asyncio
async def test_search_arxiv_error(mock_client):
    """Test handling of arXiv API errors."""
    import arxiv

    # Create proper ArxivError with required parameters
    error = arxiv.ArxivError("http://example.com", retry=3, message="API Error")
    mock_client.results.side_effect = error

    with patch("arxiv.Client", return_value=mock_client):
        result = await handle_search({"query": "test", "max_results": 1})

        assert "ArXiv API error" in result[0].text


@pytest.mark.asyncio
async def test_search_max_results_limiting(mock_client):
    """Test that max_results is properly limited."""
    with patch("arxiv.Client", return_value=mock_client):
        # Test that very large max_results gets capped
        result = await handle_search({"query": "test", "max_results": 1000})

        # Should not fail and should be limited by settings.MAX_RESULTS
        content = json.loads(result[0].text)
        assert "papers" in content


@pytest.mark.asyncio
async def test_search_sort_by_relevance(mock_client):
    """Test search with relevance sorting (default)."""
    with patch("arxiv.Client", return_value=mock_client):
        result = await handle_search({"query": "test", "sort_by": "relevance"})

        content = json.loads(result[0].text)
        assert "papers" in content


@pytest.mark.asyncio
async def test_search_sort_by_date(mock_client):
    """Test search with date sorting."""
    with patch("arxiv.Client", return_value=mock_client):
        result = await handle_search({"query": "test", "sort_by": "date"})

        content = json.loads(result[0].text)
        assert "papers" in content


@pytest.mark.asyncio
async def test_search_no_query_optimization(mock_client):
    """Test that queries are not automatically modified."""
    from arxiv_mcp_server.tools.search import _optimize_query

    # Test that complex queries are not mangled
    complex_query = "graph neural networks message passing attention mechanism"
    optimized = _optimize_query(complex_query)
    assert optimized == complex_query

    # Test that field-specific queries are preserved
    field_query = 'ti:"graph neural networks"'
    optimized = _optimize_query(field_query)
    assert optimized == field_query

    # Test that boolean queries are preserved
    bool_query = "machine learning AND deep learning"
    optimized = _optimize_query(bool_query)
    assert optimized == bool_query
