"""Comprehensive tests for sage/core/awareness.py."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest


# =============================================================================
# Tests for ScanCoverage Dataclass
# =============================================================================


class TestScanCoverage:
    """Tests for ScanCoverage dataclass."""

    def test_import(self):
        """ScanCoverage can be imported."""
        from sage.core.awareness import ScanCoverage
        assert ScanCoverage is not None

    def test_create_defaults(self):
        """Create with default values."""
        from sage.core.awareness import ScanCoverage

        coverage = ScanCoverage()
        assert coverage.files_scanned == 0
        assert coverage.files_total == 0
        assert coverage.files_truncated is False
        assert coverage.directories_scanned == 0
        assert coverage.files_content_read == 0
        assert coverage.files_indexed == 0

    def test_is_complete_true(self):
        """is_complete returns True when no truncation."""
        from sage.core.awareness import ScanCoverage

        coverage = ScanCoverage()
        assert coverage.is_complete is True

    def test_is_complete_false_files_truncated(self):
        """is_complete returns False when files truncated."""
        from sage.core.awareness import ScanCoverage

        coverage = ScanCoverage(files_truncated=True)
        assert coverage.is_complete is False

    def test_is_complete_false_dirs_truncated(self):
        """is_complete returns False when directories truncated."""
        from sage.core.awareness import ScanCoverage

        coverage = ScanCoverage(directories_truncated=True)
        assert coverage.is_complete is False

    def test_is_complete_false_index_truncated(self):
        """is_complete returns False when index truncated."""
        from sage.core.awareness import ScanCoverage

        coverage = ScanCoverage(index_truncated=True)
        assert coverage.is_complete is False

    def test_is_complete_false_source_truncated(self):
        """is_complete returns False when source content truncated."""
        from sage.core.awareness import ScanCoverage

        coverage = ScanCoverage(source_content_truncated=True)
        assert coverage.is_complete is False

    def test_is_complete_false_tree_depth_reached(self):
        """is_complete returns False when max tree depth reached."""
        from sage.core.awareness import ScanCoverage

        coverage = ScanCoverage(max_tree_depth_reached=True)
        assert coverage.is_complete is False

    def test_coverage_percent_empty(self):
        """coverage_percent returns 100 when no files."""
        from sage.core.awareness import ScanCoverage

        coverage = ScanCoverage(files_total=0)
        assert coverage.coverage_percent == 100.0

    def test_coverage_percent_full(self):
        """coverage_percent returns 100 when all scanned."""
        from sage.core.awareness import ScanCoverage

        coverage = ScanCoverage(files_scanned=100, files_total=100)
        assert coverage.coverage_percent == 100.0

    def test_coverage_percent_partial(self):
        """coverage_percent calculates correctly."""
        from sage.core.awareness import ScanCoverage

        coverage = ScanCoverage(files_scanned=50, files_total=100)
        assert coverage.coverage_percent == 50.0

    def test_to_dict(self):
        """to_dict serializes correctly."""
        from sage.core.awareness import ScanCoverage

        coverage = ScanCoverage(
            files_scanned=10,
            files_total=20,
            files_truncated=True,
            files_by_language={"python": 8, "javascript": 2},
            languages_indexed={"python", "javascript"}
        )
        data = coverage.to_dict()

        assert data["files_scanned"] == 10
        assert data["files_total"] == 20
        assert data["files_truncated"] is True
        assert data["files_by_language"] == {"python": 8, "javascript": 2}
        assert set(data["languages_indexed"]) == {"python", "javascript"}

    def test_from_dict(self):
        """from_dict deserializes correctly."""
        from sage.core.awareness import ScanCoverage

        data = {
            "files_scanned": 15,
            "files_total": 30,
            "files_truncated": True,
            "files_by_language": {"python": 10},
            "languages_indexed": ["python", "go"]
        }
        coverage = ScanCoverage.from_dict(data)

        assert coverage.files_scanned == 15
        assert coverage.files_total == 30
        assert coverage.files_truncated is True
        assert coverage.files_by_language == {"python": 10}
        assert coverage.languages_indexed == {"python", "go"}

    def test_from_dict_empty(self):
        """from_dict handles empty dict."""
        from sage.core.awareness import ScanCoverage

        coverage = ScanCoverage.from_dict({})
        assert coverage.files_scanned == 0


# =============================================================================
# Tests for AwarenessContext Dataclass
# =============================================================================


class TestAwarenessContext:
    """Tests for AwarenessContext dataclass."""

    def test_import(self):
        """AwarenessContext can be imported."""
        from sage.core.awareness import AwarenessContext
        assert AwarenessContext is not None

    def test_create(self, tmp_path):
        """Create AwarenessContext."""
        from sage.core.awareness import AwarenessContext, ScanCoverage

        context = AwarenessContext(
            coverage=ScanCoverage(),
            project_root=tmp_path
        )
        assert context.project_root == tmp_path

    def test_get_honest_context_statement_complete(self, tmp_path):
        """Honest statement for complete scan."""
        from sage.core.awareness import AwarenessContext, ScanCoverage

        coverage = ScanCoverage(files_scanned=100, files_total=100)
        context = AwarenessContext(coverage=coverage, project_root=tmp_path)

        statement = context.get_honest_context_statement()
        assert "Full project scan" in statement
        assert "all files" in statement.lower()

    def test_get_honest_context_statement_partial_files(self, tmp_path):
        """Honest statement for partial file scan."""
        from sage.core.awareness import AwarenessContext, ScanCoverage

        coverage = ScanCoverage(
            files_scanned=50,
            files_total=100,
            files_truncated=True
        )
        context = AwarenessContext(coverage=coverage, project_root=tmp_path)

        statement = context.get_honest_context_statement()
        assert "PARTIAL SCAN" in statement
        assert "50" in statement
        assert "100" in statement

    def test_get_honest_context_statement_tree_depth(self, tmp_path):
        """Honest statement includes tree depth info."""
        from sage.core.awareness import AwarenessContext, ScanCoverage

        coverage = ScanCoverage(
            max_tree_depth_reached=True,
            tree_depth_limit=5
        )
        context = AwarenessContext(coverage=coverage, project_root=tmp_path)

        statement = context.get_honest_context_statement()
        assert "tree truncated" in statement.lower()
        assert "5" in statement

    def test_get_honest_context_statement_source_truncated(self, tmp_path):
        """Honest statement includes source truncation info."""
        from sage.core.awareness import AwarenessContext, ScanCoverage

        coverage = ScanCoverage(
            source_content_truncated=True,
            source_files_shown=10,
            source_files_total=50,
            max_source_lines=200
        )
        context = AwarenessContext(coverage=coverage, project_root=tmp_path)

        statement = context.get_honest_context_statement()
        assert "10" in statement
        assert "50" in statement

    def test_get_honest_context_statement_content_truncated(self, tmp_path):
        """Honest statement includes content truncation info."""
        from sage.core.awareness import AwarenessContext, ScanCoverage

        coverage = ScanCoverage(
            files_content_truncated=5,
            files_truncated=True  # To trigger partial scan
        )
        context = AwarenessContext(coverage=coverage, project_root=tmp_path)

        statement = context.get_honest_context_statement()
        assert "5 files had content truncated" in statement

    def test_get_honest_context_statement_index_truncated(self, tmp_path):
        """Honest statement includes index truncation info."""
        from sage.core.awareness import AwarenessContext, ScanCoverage

        coverage = ScanCoverage(
            index_truncated=True,
            files_indexed=100,
            index_limit=100
        )
        context = AwarenessContext(coverage=coverage, project_root=tmp_path)

        statement = context.get_honest_context_statement()
        assert "index" in statement.lower()
        assert "100" in statement

    def test_get_honest_context_statement_language_breakdown(self, tmp_path):
        """Honest statement includes language breakdown."""
        from sage.core.awareness import AwarenessContext, ScanCoverage

        coverage = ScanCoverage(
            files_by_language={"python": 50, "javascript": 30, "go": 10}
        )
        context = AwarenessContext(coverage=coverage, project_root=tmp_path)

        statement = context.get_honest_context_statement()
        assert "Language breakdown" in statement
        assert "python" in statement.lower()

    def test_get_honest_context_statement_exploration_tips(self, tmp_path):
        """Partial scan includes exploration tips."""
        from sage.core.awareness import AwarenessContext, ScanCoverage

        coverage = ScanCoverage(files_truncated=True)
        context = AwarenessContext(coverage=coverage, project_root=tmp_path)

        statement = context.get_honest_context_statement()
        assert "READ:" in statement
        assert "SEARCH:" in statement

    def test_get_coverage_summary_line_complete(self, tmp_path):
        """Summary line for complete scan."""
        from sage.core.awareness import AwarenessContext, ScanCoverage

        coverage = ScanCoverage(files_scanned=100, files_total=100)
        context = AwarenessContext(coverage=coverage, project_root=tmp_path)

        summary = context.get_coverage_summary_line()
        assert "Full scan" in summary
        assert "100 files" in summary

    def test_get_coverage_summary_line_partial(self, tmp_path):
        """Summary line for partial scan."""
        from sage.core.awareness import AwarenessContext, ScanCoverage

        coverage = ScanCoverage(
            files_scanned=50,
            files_total=100,
            files_truncated=True
        )
        context = AwarenessContext(coverage=coverage, project_root=tmp_path)

        summary = context.get_coverage_summary_line()
        assert "Partial scan" in summary
        assert "50/100" in summary
        assert "50%" in summary


# =============================================================================
# Tests for RepoAwareness Class
# =============================================================================


class TestRepoAwareness:
    """Tests for RepoAwareness class."""

    def test_create(self, tmp_path):
        """Create RepoAwareness."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        assert awareness.project_root == tmp_path.resolve()
        assert awareness.coverage is not None

    def test_skip_dirs(self, tmp_path):
        """SKIP_DIRS contains expected directories."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        assert ".git" in awareness.SKIP_DIRS
        assert "node_modules" in awareness.SKIP_DIRS
        assert "__pycache__" in awareness.SKIP_DIRS

    def test_should_skip_git(self, tmp_path):
        """Should skip .git directory."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        git_path = tmp_path / ".git" / "config"
        assert awareness._should_skip(git_path) is True

    def test_should_skip_node_modules(self, tmp_path):
        """Should skip node_modules."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        nm_path = tmp_path / "node_modules" / "some_package" / "index.js"
        assert awareness._should_skip(nm_path) is True

    def test_should_skip_hidden(self, tmp_path):
        """Should skip hidden directories."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        hidden_path = tmp_path / ".hidden" / "file.txt"
        assert awareness._should_skip(hidden_path) is True

    def test_should_not_skip_normal(self, tmp_path):
        """Should not skip normal files."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        normal_path = tmp_path / "src" / "main.py"
        assert awareness._should_skip(normal_path) is False

    def test_count_total_files(self, tmp_path):
        """Count files in project."""
        from sage.core.awareness import RepoAwareness

        # Create some files
        (tmp_path / "file1.py").write_text("content")
        (tmp_path / "file2.py").write_text("content")
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "file3.py").write_text("content")

        awareness = RepoAwareness(tmp_path)
        count = awareness.count_total_files()

        assert count == 3
        assert awareness.coverage.files_total == 3

    def test_count_total_files_skips_git(self, tmp_path):
        """Count files skips .git."""
        from sage.core.awareness import RepoAwareness

        # Create normal files
        (tmp_path / "file1.py").write_text("content")

        # Create .git
        (tmp_path / ".git").mkdir()
        (tmp_path / ".git" / "config").write_text("git config")

        awareness = RepoAwareness(tmp_path)
        count = awareness.count_total_files()

        assert count == 1  # Only file1.py

    def test_count_total_files_max_limit(self, tmp_path):
        """Count files respects max limit."""
        from sage.core.awareness import RepoAwareness

        # Create many files
        for i in range(20):
            (tmp_path / f"file{i}.py").write_text("content")

        awareness = RepoAwareness(tmp_path)
        count = awareness.count_total_files(max_count=10)

        assert count == 10
        assert awareness.coverage.files_truncated is True

    def test_record_file_scan(self, tmp_path):
        """Record file scan."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        awareness.record_file_scan("src/main.py")

        assert "src/main.py" in awareness._known_files
        assert awareness.coverage.files_scanned == 1

    def test_record_file_scan_with_content(self, tmp_path):
        """Record file scan with content."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        awareness.record_file_scan(
            "src/main.py",
            with_content=True,
            lines_read=100
        )

        assert awareness.coverage.files_content_read == 1
        assert awareness.coverage.total_lines_read == 100
        assert "src/main.py" in awareness._files_with_content

    def test_record_file_scan_truncated(self, tmp_path):
        """Record truncated file scan."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        awareness.record_file_scan(
            "src/main.py",
            with_content=True,
            was_truncated=True
        )

        assert awareness.coverage.files_content_truncated == 1

    def test_record_file_scan_tracks_language(self, tmp_path):
        """Record file scan tracks language."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        awareness.record_file_scan("src/main.py")
        awareness.record_file_scan("src/util.py")
        awareness.record_file_scan("src/app.js")

        assert awareness.coverage.files_by_language.get("python", 0) == 2
        assert awareness.coverage.files_by_language.get("javascript", 0) == 1

    def test_record_directory_scan(self, tmp_path):
        """Record directory scan."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        awareness.record_directory_scan("src")
        awareness.record_directory_scan("src/utils")

        assert "src" in awareness._known_dirs
        assert "src/utils" in awareness._known_dirs
        assert awareness.coverage.directories_scanned == 2

    def test_record_tree_depth_limit(self, tmp_path):
        """Record tree depth limit."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        awareness.record_tree_depth_limit(5)

        assert awareness.coverage.max_tree_depth_reached is True
        assert awareness.coverage.tree_depth_limit == 5

    def test_record_source_display(self, tmp_path):
        """Record source display limits."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        awareness.record_source_display(
            files_shown=10,
            files_total=50,
            max_files=20,
            max_lines=500
        )

        assert awareness.coverage.source_files_shown == 10
        assert awareness.coverage.source_files_total == 50
        assert awareness.coverage.max_source_files == 20
        assert awareness.coverage.max_source_lines == 500
        assert awareness.coverage.source_content_truncated is True

    def test_record_source_display_not_truncated(self, tmp_path):
        """Record source display when not truncated."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        awareness.record_source_display(
            files_shown=50,
            files_total=50,
            max_files=100,
            max_lines=500
        )

        assert awareness.coverage.source_content_truncated is False

    def test_record_dependency_index(self, tmp_path):
        """Record dependency index."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        awareness.record_dependency_index(
            files_indexed=100,
            limit=200,
            languages={"python", "javascript"}
        )

        assert awareness.coverage.files_indexed == 100
        assert awareness.coverage.index_limit == 200
        assert awareness.coverage.languages_indexed == {"python", "javascript"}
        assert awareness.coverage.index_truncated is False

    def test_record_dependency_index_truncated(self, tmp_path):
        """Record truncated dependency index."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        awareness.record_dependency_index(
            files_indexed=100,
            limit=100,  # Hit the limit
            languages={"python"}
        )

        assert awareness.coverage.index_truncated is True

    def test_record_file_dependency_indexed(self, tmp_path):
        """Record file dependency indexed."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        awareness.record_file_dependency_indexed("src/main.py")

        assert "src/main.py" in awareness._files_with_deps

    def test_get_context(self, tmp_path):
        """Get awareness context."""
        from sage.core.awareness import RepoAwareness, AwarenessContext

        awareness = RepoAwareness(tmp_path)
        awareness.record_file_scan("src/main.py", with_content=True)
        awareness.record_directory_scan("src")

        context = awareness.get_context()

        assert isinstance(context, AwarenessContext)
        assert context.project_root == tmp_path.resolve()
        assert "src/main.py" in context.known_files
        assert "src" in context.known_directories
        assert "src/main.py" in context.files_with_content
        assert context.scan_timestamp != ""

    def test_get_context_unread_files(self, tmp_path):
        """Context tracks unread files."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        awareness.record_file_scan("src/main.py", with_content=True)
        awareness.record_file_scan("src/utils.py", with_content=False)

        context = awareness.get_context()

        assert "src/utils.py" in context.unread_files
        assert "src/main.py" not in context.unread_files

    def test_get_honest_prompt_context(self, tmp_path):
        """Get honest prompt context."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        awareness.record_file_scan("src/main.py")

        prompt_context = awareness.get_honest_prompt_context()

        assert isinstance(prompt_context, str)
        assert len(prompt_context) > 0

    def test_save_and_load(self, tmp_path):
        """Save and load awareness state."""
        from sage.core.awareness import RepoAwareness

        # Create and save
        awareness1 = RepoAwareness(tmp_path)
        awareness1.record_file_scan("src/main.py", with_content=True)
        awareness1.record_directory_scan("src")
        awareness1.coverage.files_total = 100
        awareness1.save()

        # Load in new instance
        awareness2 = RepoAwareness(tmp_path)
        loaded = awareness2.load()

        assert loaded is True
        assert "src/main.py" in awareness2._known_files
        assert "src" in awareness2._known_dirs
        assert "src/main.py" in awareness2._files_with_content
        assert awareness2.coverage.files_total == 100

    def test_load_no_file(self, tmp_path):
        """Load returns False when no cache file."""
        from sage.core.awareness import RepoAwareness

        awareness = RepoAwareness(tmp_path)
        loaded = awareness.load()

        assert loaded is False

    def test_load_corrupt_file(self, tmp_path):
        """Load handles corrupt cache file."""
        from sage.core.awareness import RepoAwareness

        # Create corrupt cache file
        cache_dir = tmp_path / ".sage"
        cache_dir.mkdir()
        (cache_dir / "awareness.json").write_text("invalid json")

        awareness = RepoAwareness(tmp_path)
        loaded = awareness.load()

        assert loaded is False

    def test_needs_rescan_no_previous(self, tmp_path):
        """needs_rescan when no previous scan."""
        from sage.core.awareness import RepoAwareness

        # Create a file
        (tmp_path / "file.py").write_text("content")

        awareness = RepoAwareness(tmp_path)
        # First count
        awareness.count_total_files()

        # Should not need rescan (no previous data to compare)
        assert awareness.needs_rescan() is False

    def test_needs_rescan_no_previous_data(self, tmp_path):
        """needs_rescan returns False when no previous files_total."""
        from sage.core.awareness import RepoAwareness

        # Create some files
        for i in range(5):
            (tmp_path / f"file{i}.py").write_text("content")

        awareness = RepoAwareness(tmp_path)
        # With default files_total=0, ratio check is skipped
        assert awareness.needs_rescan() is False


# =============================================================================
# Tests for build_awareness_context Function
# =============================================================================


class TestBuildAwarenessContext:
    """Tests for build_awareness_context function."""

    def test_import(self):
        """Function can be imported."""
        from sage.core.awareness import build_awareness_context
        assert build_awareness_context is not None

    def test_build_from_empty(self, tmp_path):
        """Build from empty scan results."""
        from sage.core.awareness import build_awareness_context, AwarenessContext

        context = build_awareness_context(tmp_path, {})

        assert isinstance(context, AwarenessContext)
        assert context.coverage.files_scanned == 0

    def test_build_from_files(self, tmp_path):
        """Build from file scan results."""
        from sage.core.awareness import build_awareness_context

        scan_results = {
            "files": [
                {"path": "src/main.py", "has_content": True, "lines": 100},
                {"path": "src/utils.py", "has_content": False},
            ]
        }

        context = build_awareness_context(tmp_path, scan_results)

        assert context.coverage.files_scanned == 2
        assert context.coverage.files_content_read == 1
        assert context.coverage.total_lines_read == 100

    def test_build_from_directories(self, tmp_path):
        """Build from directory scan results."""
        from sage.core.awareness import build_awareness_context

        scan_results = {
            "directories": ["src", "tests", "docs"]
        }

        context = build_awareness_context(tmp_path, scan_results)

        assert context.coverage.directories_scanned == 3
        assert "src" in context.known_directories

    def test_build_with_tree_depth(self, tmp_path):
        """Build with tree depth limit."""
        from sage.core.awareness import build_awareness_context

        scan_results = {
            "tree_depth_limited": True,
            "tree_depth_limit": 5
        }

        context = build_awareness_context(tmp_path, scan_results)

        assert context.coverage.max_tree_depth_reached is True
        assert context.coverage.tree_depth_limit == 5

    def test_build_with_source_display(self, tmp_path):
        """Build with source display info."""
        from sage.core.awareness import build_awareness_context

        scan_results = {
            "source_display": {
                "shown": 10,
                "total": 50,
                "max_files": 20,
                "max_lines": 300
            }
        }

        context = build_awareness_context(tmp_path, scan_results)

        assert context.coverage.source_files_shown == 10
        assert context.coverage.source_files_total == 50
        assert context.coverage.source_content_truncated is True

    def test_build_with_dependency_stats(self, tmp_path):
        """Build with dependency stats."""
        from sage.core.awareness import build_awareness_context

        scan_results = {"files": []}
        dependency_stats = {
            "total_files": 100,
            "limit": 200,
            "by_language": {"python": 80, "javascript": 20}
        }

        context = build_awareness_context(
            tmp_path, scan_results, dependency_stats=dependency_stats
        )

        assert context.coverage.files_indexed == 100
        assert context.coverage.index_limit == 200
        assert "python" in context.coverage.languages_indexed

    def test_build_with_truncated_content(self, tmp_path):
        """Build with truncated file content."""
        from sage.core.awareness import build_awareness_context

        scan_results = {
            "files": [
                {"path": "big.py", "has_content": True, "truncated": True, "lines": 1000},
            ]
        }

        context = build_awareness_context(tmp_path, scan_results)

        assert context.coverage.files_content_truncated == 1
