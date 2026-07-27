"""Comprehensive tests for sage/core/grounded_search.py."""

from __future__ import annotations

import re
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest


# =============================================================================
# Tests for SearchResult Dataclass
# =============================================================================


class TestSearchResult:
    """Tests for SearchResult dataclass."""

    def test_import(self):
        """SearchResult can be imported."""
        from sage.core.grounded_search import SearchResult
        assert SearchResult is not None

    def test_create_minimal(self):
        """Create with minimal args."""
        from sage.core.grounded_search import SearchResult

        result = SearchResult(
            file_path="src/main.py",
            line_number=42,
            line_content="def hello():"
        )
        assert result.file_path == "src/main.py"
        assert result.line_number == 42
        assert result.line_content == "def hello():"

    def test_defaults(self):
        """Default values are set."""
        from sage.core.grounded_search import SearchResult

        result = SearchResult(
            file_path="file.py",
            line_number=1,
            line_content="test"
        )
        assert result.context_before == []
        assert result.context_after == []
        assert result.match_type == "content"

    def test_location_property(self):
        """location property formats correctly."""
        from sage.core.grounded_search import SearchResult

        result = SearchResult(
            file_path="src/app.py",
            line_number=100,
            line_content="code"
        )
        assert result.location == "src/app.py:100"


# =============================================================================
# Tests for SearchQuery Dataclass
# =============================================================================


class TestSearchQuery:
    """Tests for SearchQuery dataclass."""

    def test_import(self):
        """SearchQuery can be imported."""
        from sage.core.grounded_search import SearchQuery
        assert SearchQuery is not None

    def test_create_minimal(self):
        """Create with minimal args."""
        from sage.core.grounded_search import SearchQuery

        query = SearchQuery(pattern="def main")
        assert query.pattern == "def main"

    def test_defaults(self):
        """Default values are set."""
        from sage.core.grounded_search import SearchQuery

        query = SearchQuery(pattern="test")
        assert query.file_glob is None
        assert query.max_results == 50
        assert query.include_context is True
        assert query.context_lines == 2
        assert query.case_sensitive is False
        assert query.search_type == "content"

    def test_custom_options(self):
        """Create with custom options."""
        from sage.core.grounded_search import SearchQuery

        query = SearchQuery(
            pattern="pattern",
            file_glob="*.py",
            max_results=100,
            case_sensitive=True,
            search_type="function"
        )
        assert query.file_glob == "*.py"
        assert query.max_results == 100
        assert query.case_sensitive is True
        assert query.search_type == "function"


# =============================================================================
# Tests for SearchResponse Dataclass
# =============================================================================


class TestSearchResponse:
    """Tests for SearchResponse dataclass."""

    def test_import(self):
        """SearchResponse can be imported."""
        from sage.core.grounded_search import SearchResponse
        assert SearchResponse is not None

    def test_create(self):
        """Create SearchResponse."""
        from sage.core.grounded_search import SearchResponse, SearchQuery, SearchResult

        query = SearchQuery(pattern="test")
        results = [
            SearchResult("file1.py", 10, "test line"),
            SearchResult("file2.py", 20, "test line 2"),
        ]

        response = SearchResponse(
            query=query,
            results=results,
            total_matches=2,
            files_searched=10
        )

        assert response.query == query
        assert len(response.results) == 2
        assert response.total_matches == 2
        assert response.files_searched == 10
        assert response.truncated is False

    def test_has_results_true(self):
        """has_results returns True when results exist."""
        from sage.core.grounded_search import SearchResponse, SearchQuery, SearchResult

        response = SearchResponse(
            query=SearchQuery(pattern="test"),
            results=[SearchResult("file.py", 1, "test")],
            total_matches=1,
            files_searched=1
        )
        assert response.has_results is True

    def test_has_results_false(self):
        """has_results returns False when no results."""
        from sage.core.grounded_search import SearchResponse, SearchQuery

        response = SearchResponse(
            query=SearchQuery(pattern="test"),
            results=[],
            total_matches=0,
            files_searched=5
        )
        assert response.has_results is False

    def test_get_unique_files(self):
        """get_unique_files returns set of file paths."""
        from sage.core.grounded_search import SearchResponse, SearchQuery, SearchResult

        response = SearchResponse(
            query=SearchQuery(pattern="test"),
            results=[
                SearchResult("file1.py", 10, "test"),
                SearchResult("file1.py", 20, "test"),
                SearchResult("file2.py", 30, "test"),
            ],
            total_matches=3,
            files_searched=2
        )

        unique = response.get_unique_files()
        assert unique == {"file1.py", "file2.py"}

    def test_get_summary_no_results(self):
        """get_summary for no results."""
        from sage.core.grounded_search import SearchResponse, SearchQuery

        response = SearchResponse(
            query=SearchQuery(pattern="missing"),
            results=[],
            total_matches=0,
            files_searched=10
        )

        summary = response.get_summary()
        assert "No results found" in summary
        assert "missing" in summary

    def test_get_summary_with_results(self):
        """get_summary with results."""
        from sage.core.grounded_search import SearchResponse, SearchQuery, SearchResult

        response = SearchResponse(
            query=SearchQuery(pattern="test"),
            results=[SearchResult("file.py", 1, "test")],
            total_matches=10,
            files_searched=5
        )

        summary = response.get_summary()
        assert "10 matches" in summary
        assert "1 files" in summary


# =============================================================================
# Tests for GroundedSearch Class
# =============================================================================


class TestGroundedSearch:
    """Tests for GroundedSearch class."""

    def test_import(self):
        """GroundedSearch can be imported."""
        from sage.core.grounded_search import GroundedSearch
        assert GroundedSearch is not None

    def test_create(self, tmp_path):
        """Create GroundedSearch."""
        from sage.core.grounded_search import GroundedSearch

        searcher = GroundedSearch(tmp_path)
        assert searcher.base_dir == tmp_path
        assert searcher._indexed is False

    def test_skip_dirs(self, tmp_path):
        """SKIP_DIRS contains expected directories."""
        from sage.core.grounded_search import GroundedSearch

        assert ".git" in GroundedSearch.SKIP_DIRS
        assert "node_modules" in GroundedSearch.SKIP_DIRS
        assert "__pycache__" in GroundedSearch.SKIP_DIRS

    def test_code_extensions(self, tmp_path):
        """CODE_EXTENSIONS contains expected extensions."""
        from sage.core.grounded_search import GroundedSearch

        assert ".py" in GroundedSearch.CODE_EXTENSIONS
        assert ".js" in GroundedSearch.CODE_EXTENSIONS
        assert ".ts" in GroundedSearch.CODE_EXTENSIONS

    def test_should_skip_dir_git(self, tmp_path):
        """Should skip .git directory."""
        from sage.core.grounded_search import GroundedSearch

        searcher = GroundedSearch(tmp_path)
        assert searcher._should_skip_dir(".git") is True

    def test_should_skip_dir_normal(self, tmp_path):
        """Should not skip normal directory."""
        from sage.core.grounded_search import GroundedSearch

        searcher = GroundedSearch(tmp_path)
        assert searcher._should_skip_dir("src") is False

    def test_file_exists_relative(self, tmp_path):
        """Check relative file exists."""
        from sage.core.grounded_search import GroundedSearch

        (tmp_path / "test.py").write_text("content")

        searcher = GroundedSearch(tmp_path)
        assert searcher.file_exists("test.py") is True
        assert searcher.file_exists("missing.py") is False

    def test_file_exists_absolute(self, tmp_path):
        """Check absolute file exists."""
        from sage.core.grounded_search import GroundedSearch

        test_file = tmp_path / "test.py"
        test_file.write_text("content")

        searcher = GroundedSearch(tmp_path)
        assert searcher.file_exists(str(test_file)) is True

    def test_verify_file_exists(self, tmp_path):
        """Verify file exists returns path."""
        from sage.core.grounded_search import GroundedSearch

        (tmp_path / "test.py").write_text("content")

        searcher = GroundedSearch(tmp_path)
        exists, path = searcher.verify_file("test.py")

        assert exists is True
        assert path == tmp_path / "test.py"

    def test_verify_file_not_exists(self, tmp_path):
        """Verify file not exists returns None."""
        from sage.core.grounded_search import GroundedSearch

        searcher = GroundedSearch(tmp_path)
        exists, path = searcher.verify_file("missing.py")

        assert exists is False
        assert path is None

    def test_verify_files(self, tmp_path):
        """Verify multiple files."""
        from sage.core.grounded_search import GroundedSearch

        (tmp_path / "exists.py").write_text("content")

        searcher = GroundedSearch(tmp_path)
        results = searcher.verify_files(["exists.py", "missing.py"])

        assert results["exists.py"] is True
        assert results["missing.py"] is False

    def test_index_files(self, tmp_path):
        """Index files in project."""
        from sage.core.grounded_search import GroundedSearch

        (tmp_path / "file1.py").write_text("content")
        (tmp_path / "file2.py").write_text("content")
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "file3.py").write_text("content")

        searcher = GroundedSearch(tmp_path)
        count = searcher.index_files()

        assert count == 3
        assert searcher._indexed is True

    def test_index_files_cached(self, tmp_path):
        """Index files uses cache."""
        from sage.core.grounded_search import GroundedSearch

        (tmp_path / "file.py").write_text("content")

        searcher = GroundedSearch(tmp_path)
        count1 = searcher.index_files()
        count2 = searcher.index_files()  # Should use cache

        assert count1 == count2 == 1

    def test_index_files_force(self, tmp_path):
        """Force re-index files."""
        from sage.core.grounded_search import GroundedSearch

        (tmp_path / "file.py").write_text("content")

        searcher = GroundedSearch(tmp_path)
        searcher.index_files()

        # Add another file
        (tmp_path / "file2.py").write_text("content")

        # Force re-index
        count = searcher.index_files(force=True)
        assert count == 2

    def test_search_content(self, tmp_path):
        """Search file contents."""
        from sage.core.grounded_search import GroundedSearch

        (tmp_path / "test.py").write_text("def hello():\n    print('world')\n")

        searcher = GroundedSearch(tmp_path)

        with patch.object(searcher, "_has_ripgrep", return_value=False):
            response = searcher.search_content("hello")

        assert response.has_results is True
        assert response.results[0].file_path == "test.py"

    def test_search_with_file_glob(self, tmp_path):
        """Search with file glob filter."""
        from sage.core.grounded_search import GroundedSearch, SearchQuery

        (tmp_path / "test.py").write_text("def hello():\n")
        (tmp_path / "test.js").write_text("function hello() {}\n")

        searcher = GroundedSearch(tmp_path)

        with patch.object(searcher, "_has_ripgrep", return_value=False):
            response = searcher.search(SearchQuery(
                pattern="hello",
                file_glob="*.py"
            ))

        assert response.has_results is True
        assert all(r.file_path.endswith(".py") for r in response.results)

    def test_search_max_results(self, tmp_path):
        """Search respects max_results."""
        from sage.core.grounded_search import GroundedSearch, SearchQuery

        # Create file with many matches
        content = "\n".join([f"match line {i}" for i in range(100)])
        (tmp_path / "test.py").write_text(content)

        searcher = GroundedSearch(tmp_path)

        with patch.object(searcher, "_has_ripgrep", return_value=False):
            response = searcher.search(SearchQuery(
                pattern="match",
                max_results=10
            ))

        assert len(response.results) <= 10
        assert response.truncated is True

    def test_search_with_context(self, tmp_path):
        """Search includes context lines."""
        from sage.core.grounded_search import GroundedSearch, SearchQuery

        (tmp_path / "test.py").write_text("line1\nline2\nmatch\nline4\nline5\n")

        searcher = GroundedSearch(tmp_path)

        with patch.object(searcher, "_has_ripgrep", return_value=False):
            response = searcher.search(SearchQuery(
                pattern="match",
                include_context=True,
                context_lines=2
            ))

        assert response.has_results is True
        result = response.results[0]
        assert len(result.context_before) > 0 or len(result.context_after) > 0

    def test_search_case_insensitive(self, tmp_path):
        """Search is case insensitive by default."""
        from sage.core.grounded_search import GroundedSearch, SearchQuery

        (tmp_path / "test.py").write_text("HELLO\nhello\nHeLLo\n")

        searcher = GroundedSearch(tmp_path)

        with patch.object(searcher, "_has_ripgrep", return_value=False):
            response = searcher.search(SearchQuery(
                pattern="hello",
                case_sensitive=False
            ))

        assert response.total_matches == 3

    def test_search_case_sensitive(self, tmp_path):
        """Search can be case sensitive."""
        from sage.core.grounded_search import GroundedSearch, SearchQuery

        (tmp_path / "test.py").write_text("HELLO\nhello\nHeLLo\n")

        searcher = GroundedSearch(tmp_path)

        with patch.object(searcher, "_has_ripgrep", return_value=False):
            response = searcher.search(SearchQuery(
                pattern="hello",
                case_sensitive=True
            ))

        assert response.total_matches == 1

    def test_search_functions_python(self, tmp_path):
        """Search for Python function definitions."""
        from sage.core.grounded_search import GroundedSearch

        (tmp_path / "test.py").write_text(
            "def foo():\n    pass\n\ndef bar():\n    pass\n"
        )

        searcher = GroundedSearch(tmp_path)

        with patch.object(searcher, "_has_ripgrep", return_value=False):
            response = searcher.search_functions("foo", language="python")

        assert response.has_results is True
        assert "foo" in response.results[0].line_content

    def test_search_functions_javascript(self, tmp_path):
        """Search for JavaScript function definitions."""
        from sage.core.grounded_search import GroundedSearch

        (tmp_path / "test.js").write_text(
            "function myFunc() {}\nconst arrow = () => {}\n"
        )

        searcher = GroundedSearch(tmp_path)

        with patch.object(searcher, "_has_ripgrep", return_value=False):
            response = searcher.search_functions("myFunc", language="javascript")

        assert response.has_results is True

    def test_search_classes_python(self, tmp_path):
        """Search for Python class definitions."""
        from sage.core.grounded_search import GroundedSearch

        (tmp_path / "test.py").write_text(
            "class MyClass:\n    pass\n\nclass Other(Base):\n    pass\n"
        )

        searcher = GroundedSearch(tmp_path)

        with patch.object(searcher, "_has_ripgrep", return_value=False):
            response = searcher.search_classes("MyClass", language="python")

        assert response.has_results is True
        assert "MyClass" in response.results[0].line_content

    def test_find_files(self, tmp_path):
        """Find files matching pattern."""
        from sage.core.grounded_search import GroundedSearch

        (tmp_path / "test.py").write_text("content")
        (tmp_path / "test_utils.py").write_text("content")
        (tmp_path / "main.py").write_text("content")

        searcher = GroundedSearch(tmp_path)
        matches = searcher.find_files("test*.py")

        assert len(matches) == 2
        assert any("test.py" in m for m in matches)
        assert any("test_utils.py" in m for m in matches)

    def test_read_file(self, tmp_path):
        """Read file content."""
        from sage.core.grounded_search import GroundedSearch

        (tmp_path / "test.py").write_text("line1\nline2\nline3\n")

        searcher = GroundedSearch(tmp_path)
        content = searcher.read_file("test.py")

        assert content == "line1\nline2\nline3\n"

    def test_read_file_not_exists(self, tmp_path):
        """Read non-existent file returns None."""
        from sage.core.grounded_search import GroundedSearch

        searcher = GroundedSearch(tmp_path)
        content = searcher.read_file("missing.py")

        assert content is None

    def test_read_file_truncated(self, tmp_path):
        """Read large file is truncated."""
        from sage.core.grounded_search import GroundedSearch

        content = "\n".join([f"line{i}" for i in range(1000)])
        (tmp_path / "big.py").write_text(content)

        searcher = GroundedSearch(tmp_path)
        result = searcher.read_file("big.py", max_lines=100)

        assert "truncated" in result
        assert "900 more lines" in result


# =============================================================================
# Tests for FileReferenceValidator Class
# =============================================================================


class TestFileReferenceValidator:
    """Tests for FileReferenceValidator class."""

    def test_import(self):
        """FileReferenceValidator can be imported."""
        from sage.core.grounded_search import FileReferenceValidator
        assert FileReferenceValidator is not None

    def test_create(self, tmp_path):
        """Create FileReferenceValidator."""
        from sage.core.grounded_search import FileReferenceValidator, GroundedSearch

        searcher = GroundedSearch(tmp_path)
        validator = FileReferenceValidator(searcher)

        assert validator.searcher == searcher
        assert len(validator.verified_paths) == 0

    def test_extract_paths_file_block(self, tmp_path):
        """Extract paths from FILE: blocks."""
        from sage.core.grounded_search import FileReferenceValidator, GroundedSearch

        searcher = GroundedSearch(tmp_path)
        validator = FileReferenceValidator(searcher)

        content = "Create FILE: `src/main.py` with the following..."
        paths = validator.extract_paths(content)

        assert "src/main.py" in paths

    def test_extract_paths_backticks(self, tmp_path):
        """Extract paths from backticks."""
        from sage.core.grounded_search import FileReferenceValidator, GroundedSearch

        searcher = GroundedSearch(tmp_path)
        validator = FileReferenceValidator(searcher)

        content = "Edit `utils/helper.py` and `config.json`"
        paths = validator.extract_paths(content)

        assert "utils/helper.py" in paths
        assert "config.json" in paths

    def test_extract_paths_line_references(self, tmp_path):
        """Extract paths from line references."""
        from sage.core.grounded_search import FileReferenceValidator, GroundedSearch

        searcher = GroundedSearch(tmp_path)
        validator = FileReferenceValidator(searcher)

        content = "Error at src/main.py:42 and tests/test.py:100"
        paths = validator.extract_paths(content)

        assert "src/main.py" in paths
        assert "tests/test.py" in paths

    def test_validate_content_valid(self, tmp_path):
        """Validate content with valid paths."""
        from sage.core.grounded_search import FileReferenceValidator, GroundedSearch

        (tmp_path / "exists.py").write_text("content")

        searcher = GroundedSearch(tmp_path)
        validator = FileReferenceValidator(searcher)

        content = "Edit `exists.py` and `missing.py`"
        valid, invalid = validator.validate_content(content)

        assert "exists.py" in valid
        assert "missing.py" in invalid

    def test_validate_content_caches(self, tmp_path):
        """Validate content uses cache."""
        from sage.core.grounded_search import FileReferenceValidator, GroundedSearch

        (tmp_path / "file.py").write_text("content")

        searcher = GroundedSearch(tmp_path)
        validator = FileReferenceValidator(searcher)

        # First validation
        validator.validate_content("Edit `file.py`")
        assert "file.py" in validator.verified_paths

        # Second validation should use cache
        valid, invalid = validator.validate_content("Also `file.py`")
        assert "file.py" in valid

    def test_must_verify_before_reference_verified(self, tmp_path):
        """Already verified paths don't need verification."""
        from sage.core.grounded_search import FileReferenceValidator, GroundedSearch

        searcher = GroundedSearch(tmp_path)
        validator = FileReferenceValidator(searcher)
        validator.verified_paths.add("verified.py")

        assert validator.must_verify_before_reference("verified.py") is False

    def test_must_verify_before_reference_invalid(self, tmp_path):
        """Invalid paths need verification."""
        from sage.core.grounded_search import FileReferenceValidator, GroundedSearch

        searcher = GroundedSearch(tmp_path)
        validator = FileReferenceValidator(searcher)
        validator.invalid_paths.add("bad.py")

        assert validator.must_verify_before_reference("bad.py") is True

    def test_must_verify_before_reference_unknown(self, tmp_path):
        """Unknown paths need verification."""
        from sage.core.grounded_search import FileReferenceValidator, GroundedSearch

        searcher = GroundedSearch(tmp_path)
        validator = FileReferenceValidator(searcher)

        assert validator.must_verify_before_reference("unknown.py") is True

    def test_get_verification_status(self, tmp_path):
        """Get verification status."""
        from sage.core.grounded_search import FileReferenceValidator, GroundedSearch

        searcher = GroundedSearch(tmp_path)
        validator = FileReferenceValidator(searcher)
        validator.verified_paths.add("good.py")
        validator.invalid_paths.add("bad.py")

        status = validator.get_verification_status()

        assert status["verified_count"] == 1
        assert status["invalid_count"] == 1
        assert "good.py" in status["verified_paths"]
        assert "bad.py" in status["invalid_paths"]


# =============================================================================
# Tests for SearchCommandExecutor Class
# =============================================================================


class TestSearchCommandExecutor:
    """Tests for SearchCommandExecutor class."""

    def test_import(self):
        """SearchCommandExecutor can be imported."""
        from sage.core.grounded_search import SearchCommandExecutor
        assert SearchCommandExecutor is not None

    def test_create(self, tmp_path):
        """Create SearchCommandExecutor."""
        from sage.core.grounded_search import SearchCommandExecutor

        executor = SearchCommandExecutor(tmp_path)

        assert executor.searcher is not None
        assert executor.validator is not None
        assert len(executor.search_history) == 0

    def test_execute_simple(self, tmp_path):
        """Execute simple search command."""
        from sage.core.grounded_search import SearchCommandExecutor

        (tmp_path / "test.py").write_text("def hello(): pass\n")

        executor = SearchCommandExecutor(tmp_path)

        with patch.object(executor.searcher, "_has_ripgrep", return_value=False):
            response = executor.execute("SEARCH: hello")

        assert response.has_results is True

    def test_execute_with_glob(self, tmp_path):
        """Execute search with file glob."""
        from sage.core.grounded_search import SearchCommandExecutor

        (tmp_path / "test.py").write_text("hello\n")
        (tmp_path / "test.js").write_text("hello\n")

        executor = SearchCommandExecutor(tmp_path)

        with patch.object(executor.searcher, "_has_ripgrep", return_value=False):
            response = executor.execute("SEARCH: hello *.py")

        # Should only find in .py files
        for result in response.results:
            assert result.file_path.endswith(".py")

    def test_execute_quoted_pattern(self, tmp_path):
        """Execute search with quoted pattern."""
        from sage.core.grounded_search import SearchCommandExecutor

        (tmp_path / "test.py").write_text("hello world\n")

        executor = SearchCommandExecutor(tmp_path)

        with patch.object(executor.searcher, "_has_ripgrep", return_value=False):
            response = executor.execute('SEARCH: "hello world"')

        assert response.has_results is True

    def test_execute_records_history(self, tmp_path):
        """Execute records search history."""
        from sage.core.grounded_search import SearchCommandExecutor

        (tmp_path / "test.py").write_text("content\n")

        executor = SearchCommandExecutor(tmp_path)

        with patch.object(executor.searcher, "_has_ripgrep", return_value=False):
            executor.execute("content")

        assert len(executor.search_history) == 1
        assert executor.search_history[0]["query"] == "content"

    def test_format_results_no_results(self, tmp_path):
        """Format results with no results."""
        from sage.core.grounded_search import SearchCommandExecutor, SearchResponse, SearchQuery

        executor = SearchCommandExecutor(tmp_path)

        response = SearchResponse(
            query=SearchQuery(pattern="missing"),
            results=[],
            total_matches=0,
            files_searched=10
        )

        formatted = executor.format_results(response)
        assert "No results found" in formatted

    def test_format_results_with_results(self, tmp_path):
        """Format results with results."""
        from sage.core.grounded_search import (
            SearchCommandExecutor, SearchResponse, SearchQuery, SearchResult
        )

        executor = SearchCommandExecutor(tmp_path)

        response = SearchResponse(
            query=SearchQuery(pattern="test"),
            results=[
                SearchResult("file.py", 10, "test line content"),
                SearchResult("file.py", 20, "another test"),
            ],
            total_matches=2,
            files_searched=5
        )

        formatted = executor.format_results(response)
        assert "2 matches" in formatted
        assert "file.py:10" in formatted


# =============================================================================
# Tests for Convenience Functions
# =============================================================================


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_search_codebase(self, tmp_path):
        """search_codebase function."""
        from sage.core.grounded_search import search_codebase

        (tmp_path / "test.py").write_text("hello world\n")

        with patch("sage.core.grounded_search.GroundedSearch._has_ripgrep", return_value=False):
            response = search_codebase(tmp_path, "hello")

        assert response.has_results is True

    def test_verify_file_exists(self, tmp_path):
        """verify_file_exists function."""
        from sage.core.grounded_search import verify_file_exists

        (tmp_path / "exists.py").write_text("content")

        assert verify_file_exists(tmp_path, "exists.py") is True
        assert verify_file_exists(tmp_path, "missing.py") is False

    def test_find_files_matching(self, tmp_path):
        """find_files_matching function."""
        from sage.core.grounded_search import find_files_matching

        (tmp_path / "test.py").write_text("content")
        (tmp_path / "test_utils.py").write_text("content")
        (tmp_path / "main.py").write_text("content")

        matches = find_files_matching(tmp_path, "test*.py")

        assert len(matches) == 2
