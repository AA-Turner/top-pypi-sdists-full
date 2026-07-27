"""Honest repo awareness tracking for SAGE.

This module tracks what SAGE actually knows about a codebase and provides
honest reporting to the model prompt. It prevents SAGE from claiming
"full context" when scan depth and indexing are limited.

This addresses P0 items 9-11:
- Item 9: Stop claiming full repo awareness when scan/index limits are active
- Item 10: Surface scan truncation directly in the model prompt
- Item 11: Surface dependency-index coverage directly in the model prompt

Key principles:
- Never claim more knowledge than we actually have
- Be explicit about what has been scanned vs. what exists
- Track scan coverage and report gaps
- Enable the model to request more context when needed
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .languages import Language, get_language_for_extension

__all__ = [
    "AwarenessContext",
    "RepoAwareness",
    "ScanCoverage",
    "build_awareness_context",
]


@dataclass
class ScanCoverage:
    """Tracks what has been scanned and what was truncated."""

    # File scanning
    files_scanned: int = 0
    files_total: int = 0
    files_truncated: bool = False  # True if we hit a limit
    files_by_language: dict[str, int] = field(default_factory=dict)

    # Directory scanning
    directories_scanned: int = 0
    directories_total: int = 0
    directories_truncated: bool = False
    max_tree_depth_reached: bool = False
    tree_depth_limit: int = 0

    # Content scanning
    files_content_read: int = 0
    files_content_truncated: int = 0  # Files where content was cut off
    total_lines_read: int = 0
    max_lines_per_file: int = 0

    # Dependency indexing
    files_indexed: int = 0
    index_limit: int = 0
    index_truncated: bool = False
    languages_indexed: set[str] = field(default_factory=set)

    # Source file display
    source_files_shown: int = 0
    source_files_total: int = 0
    source_content_truncated: bool = False
    max_source_files: int = 0
    max_source_lines: int = 0

    @property
    def is_complete(self) -> bool:
        """True if we have scanned everything without truncation."""
        return (
            not self.files_truncated
            and not self.directories_truncated
            and not self.index_truncated
            and not self.source_content_truncated
            and not self.max_tree_depth_reached
        )

    @property
    def coverage_percent(self) -> float:
        """Approximate coverage percentage based on file counts."""
        if self.files_total == 0:
            return 100.0
        return (self.files_scanned / self.files_total) * 100

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "files_scanned": self.files_scanned,
            "files_total": self.files_total,
            "files_truncated": self.files_truncated,
            "files_by_language": self.files_by_language,
            "directories_scanned": self.directories_scanned,
            "directories_total": self.directories_total,
            "directories_truncated": self.directories_truncated,
            "max_tree_depth_reached": self.max_tree_depth_reached,
            "tree_depth_limit": self.tree_depth_limit,
            "files_content_read": self.files_content_read,
            "files_content_truncated": self.files_content_truncated,
            "total_lines_read": self.total_lines_read,
            "max_lines_per_file": self.max_lines_per_file,
            "files_indexed": self.files_indexed,
            "index_limit": self.index_limit,
            "index_truncated": self.index_truncated,
            "languages_indexed": list(self.languages_indexed),
            "source_files_shown": self.source_files_shown,
            "source_files_total": self.source_files_total,
            "source_content_truncated": self.source_content_truncated,
            "max_source_files": self.max_source_files,
            "max_source_lines": self.max_source_lines,
        }

    @classmethod
    def from_dict(cls, data: dict) -> ScanCoverage:
        """Deserialize from dictionary."""
        coverage = cls()
        for key, value in data.items():
            if key == "languages_indexed":
                coverage.languages_indexed = set(value)
            elif hasattr(coverage, key):
                setattr(coverage, key, value)
        return coverage


@dataclass
class AwarenessContext:
    """Context about what SAGE knows, for injection into prompts."""

    coverage: ScanCoverage
    project_root: Path
    scan_timestamp: str = ""

    # What we definitely know
    known_files: set[str] = field(default_factory=set)
    known_directories: set[str] = field(default_factory=set)

    # What we've seen content of
    files_with_content: set[str] = field(default_factory=set)

    # What we've indexed for dependencies
    files_with_deps: set[str] = field(default_factory=set)

    # Files we know exist but haven't read
    unread_files: set[str] = field(default_factory=set)

    def get_honest_context_statement(self) -> str:
        """Generate an honest context statement for the model prompt.

        This tells the model exactly what it knows and doesn't know.
        """
        lines = []

        # Coverage summary
        if self.coverage.is_complete:
            lines.append("✓ Full project scan completed - you have visibility into all files.")
        else:
            lines.append("⚠️ PARTIAL SCAN - You do NOT have full context of this codebase:")

            if self.coverage.files_truncated:
                lines.append(
                    f"  • File listing truncated: scanned {self.coverage.files_scanned} "
                    f"of {self.coverage.files_total} files ({self.coverage.coverage_percent:.0f}% coverage)"
                )

            if self.coverage.max_tree_depth_reached:
                lines.append(
                    f"  • Directory tree truncated at depth {self.coverage.tree_depth_limit}"
                )

            if self.coverage.source_content_truncated:
                lines.append(
                    f"  • Source content limited: showed {self.coverage.source_files_shown} "
                    f"of {self.coverage.source_files_total} source files "
                    f"(max {self.coverage.max_source_lines} lines each)"
                )

            if self.coverage.files_content_truncated > 0:
                lines.append(
                    f"  • {self.coverage.files_content_truncated} files had content truncated"
                )

            if self.coverage.index_truncated:
                lines.append(
                    f"  • Dependency index limited to {self.coverage.files_indexed} "
                    f"of {self.coverage.index_limit} files"
                )

        # Language breakdown
        if self.coverage.files_by_language:
            lang_summary = ", ".join(
                f"{lang}: {count}"
                for lang, count in sorted(
                    self.coverage.files_by_language.items(), key=lambda x: x[1], reverse=True
                )[:5]
            )
            lines.append(f"\nLanguage breakdown: {lang_summary}")

        # What to do about gaps
        if not self.coverage.is_complete:
            lines.append("\nTo explore files not shown:")
            lines.append("  • Use READ: <filepath> to read specific files")
            lines.append("  • Use SEARCH: <pattern> to find files by content")
            lines.append("  • Ask about specific directories to explore them")

        return "\n".join(lines)

    def get_coverage_summary_line(self) -> str:
        """Get a single-line coverage summary."""
        if self.coverage.is_complete:
            return f"Full scan: {self.coverage.files_scanned} files"
        return (
            f"Partial scan: {self.coverage.files_scanned}/{self.coverage.files_total} files "
            f"({self.coverage.coverage_percent:.0f}%)"
        )


class RepoAwareness:
    """Tracks and manages SAGE's awareness of a repository.

    Use this class to:
    1. Track what has been scanned
    2. Generate honest context statements
    3. Identify gaps in knowledge
    """

    SKIP_DIRS: set[str] = {
        ".git",
        ".svn",
        ".hg",
        ".venv",
        "venv",
        "env",
        ".env",
        "__pycache__",
        "node_modules",
        "dist",
        "build",
        "target",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".tox",
        "vendor",
        "deps",
        "_build",
        ".next",
        ".nuxt",
        ".output",
        "coverage",
        ".coverage",
        "htmlcov",
        ".idea",
        ".vscode",
    }

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.resolve()
        self.coverage = ScanCoverage()
        self._known_files: set[str] = set()
        self._known_dirs: set[str] = set()
        self._files_with_content: set[str] = set()
        self._files_with_deps: set[str] = set()
        self._cache_file = project_root / ".sage" / "awareness.json"

    def _should_skip(self, path: Path) -> bool:
        """Check if a path should be skipped."""
        try:
            rel = path.relative_to(self.project_root)
            parts = rel.parts
            return any(p.startswith(".") or p in self.SKIP_DIRS for p in parts)
        except ValueError:
            return True

    def count_total_files(self, max_count: int = 10000) -> int:
        """Count total files in the project (for coverage calculation).

        Args:
            max_count: Maximum files to count before stopping

        Returns:
            Number of files found (may be capped at max_count)
        """
        count = 0
        dirs_count = 0

        from sage.core.project import safe_walk
        for path in safe_walk(self.project_root, max_files=max_count + 1000):
            if count >= max_count:
                self.coverage.files_truncated = True
                break

            if path.is_file():
                count += 1
            elif path.is_dir():
                dirs_count += 1

        self.coverage.files_total = count
        self.coverage.directories_total = dirs_count
        return count

    def record_file_scan(
        self,
        filepath: str,
        with_content: bool = False,
        lines_read: int = 0,
        was_truncated: bool = False,
    ) -> None:
        """Record that a file was scanned.

        Args:
            filepath: Relative path to the file
            with_content: Whether content was read
            lines_read: Number of lines read
            was_truncated: Whether content was truncated
        """
        self._known_files.add(filepath)
        self.coverage.files_scanned += 1

        # Track language
        ext = Path(filepath).suffix.lower()
        lang = get_language_for_extension(ext)
        if lang != Language.UNKNOWN:
            lang_str = lang.value
            self.coverage.files_by_language[lang_str] = (
                self.coverage.files_by_language.get(lang_str, 0) + 1
            )

        if with_content:
            self.coverage.files_content_read += 1
            self._files_with_content.add(filepath)
            self.coverage.total_lines_read += lines_read

            if was_truncated:
                self.coverage.files_content_truncated += 1

    def record_directory_scan(self, dirpath: str) -> None:
        """Record that a directory was scanned.

        Args:
            dirpath: Relative path to the directory
        """
        self._known_dirs.add(dirpath)
        self.coverage.directories_scanned += 1

    def record_tree_depth_limit(self, limit: int) -> None:
        """Record that tree depth was limited.

        Args:
            limit: The depth limit that was applied
        """
        self.coverage.max_tree_depth_reached = True
        self.coverage.tree_depth_limit = limit

    def record_source_display(
        self,
        files_shown: int,
        files_total: int,
        max_files: int,
        max_lines: int,
    ) -> None:
        """Record source file display limits.

        Args:
            files_shown: Number of source files shown
            files_total: Total source files available
            max_files: Maximum files setting
            max_lines: Maximum lines per file setting
        """
        self.coverage.source_files_shown = files_shown
        self.coverage.source_files_total = files_total
        self.coverage.max_source_files = max_files
        self.coverage.max_source_lines = max_lines

        if files_shown < files_total:
            self.coverage.source_content_truncated = True

    def record_dependency_index(
        self,
        files_indexed: int,
        limit: int,
        languages: set[str],
    ) -> None:
        """Record dependency indexing results.

        Args:
            files_indexed: Number of files indexed
            limit: The index limit that was applied
            languages: Languages that were indexed
        """
        self.coverage.files_indexed = files_indexed
        self.coverage.index_limit = limit
        self.coverage.languages_indexed = languages

        if files_indexed >= limit:
            self.coverage.index_truncated = True

    def record_file_dependency_indexed(self, filepath: str) -> None:
        """Record that a file was indexed for dependencies.

        Args:
            filepath: Relative path to the file
        """
        self._files_with_deps.add(filepath)

    def get_context(self) -> AwarenessContext:
        """Get the current awareness context.

        Returns:
            AwarenessContext with all tracking data
        """
        from datetime import datetime

        return AwarenessContext(
            coverage=self.coverage,
            project_root=self.project_root,
            scan_timestamp=datetime.now().isoformat(),
            known_files=self._known_files.copy(),
            known_directories=self._known_dirs.copy(),
            files_with_content=self._files_with_content.copy(),
            files_with_deps=self._files_with_deps.copy(),
            unread_files=self._known_files - self._files_with_content,
        )

    def get_honest_prompt_context(self) -> str:
        """Get an honest context statement for the model prompt.

        This should be included in the system prompt to ensure the model
        knows exactly what it has and hasn't seen.

        Returns:
            Formatted context string
        """
        context = self.get_context()
        return context.get_honest_context_statement()

    def save(self) -> None:
        """Save awareness state to disk."""
        self._cache_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "coverage": self.coverage.to_dict(),
            "known_files": list(self._known_files),
            "known_dirs": list(self._known_dirs),
            "files_with_content": list(self._files_with_content),
            "files_with_deps": list(self._files_with_deps),
        }
        self._cache_file.write_text(json.dumps(data, indent=2))

    def load(self) -> bool:
        """Load awareness state from disk.

        Returns:
            True if loaded successfully, False otherwise
        """
        if not self._cache_file.exists():
            return False

        try:
            data = json.loads(self._cache_file.read_text(encoding="utf-8", errors="replace"))
            self.coverage = ScanCoverage.from_dict(data.get("coverage", {}))
            self._known_files = set(data.get("known_files", []))
            self._known_dirs = set(data.get("known_dirs", []))
            self._files_with_content = set(data.get("files_with_content", []))
            self._files_with_deps = set(data.get("files_with_deps", []))
            return True
        except Exception:
            return False

    def needs_rescan(self) -> bool:
        """Check if a rescan is needed (e.g., files changed).

        Returns:
            True if rescan recommended
        """
        # Simple heuristic: check if total file count changed significantly
        current_count = self.count_total_files(max_count=1000)
        if self.coverage.files_total > 0:
            ratio = current_count / self.coverage.files_total
            if ratio < 0.9 or ratio > 1.1:
                return True
        return False


def build_awareness_context(
    project_root: Path,
    scan_results: dict[str, Any],
    dependency_stats: dict[str, Any] | None = None,
) -> AwarenessContext:
    """Build an awareness context from scan results.

    This is a convenience function for converting scan results into
    an awareness context.

    Args:
        project_root: Path to the project root
        scan_results: Dictionary with scan results (files, dirs, etc.)
        dependency_stats: Optional dependency graph statistics

    Returns:
        AwarenessContext
    """
    awareness = RepoAwareness(project_root)

    # Process file list
    files = scan_results.get("files", [])
    for f in files:
        awareness.record_file_scan(
            f.get("path", ""),
            with_content=f.get("has_content", False),
            lines_read=f.get("lines", 0),
            was_truncated=f.get("truncated", False),
        )

    # Process directory list
    dirs = scan_results.get("directories", [])
    for d in dirs:
        awareness.record_directory_scan(d)

    # Process limits
    if scan_results.get("tree_depth_limited"):
        awareness.record_tree_depth_limit(scan_results.get("tree_depth_limit", 0))

    if scan_results.get("source_display"):
        sd = scan_results["source_display"]
        awareness.record_source_display(
            files_shown=sd.get("shown", 0),
            files_total=sd.get("total", 0),
            max_files=sd.get("max_files", 0),
            max_lines=sd.get("max_lines", 0),
        )

    # Process dependency stats
    if dependency_stats:
        awareness.record_dependency_index(
            files_indexed=dependency_stats.get("total_files", 0),
            limit=dependency_stats.get("limit", 0),
            languages=set(dependency_stats.get("by_language", {}).keys()),
        )

    return awareness.get_context()
