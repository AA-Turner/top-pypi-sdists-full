"""
Grounded search and file validation for SAGE - Fixes P0-3, P1 issues 21-40.

P0-3: File path hallucination
P0-14: Assumption-based responses
P1-21: SEARCH: command is cosmetic
P1-22: No file discovery before planning
P1-23: Doesn't read existing code
P1-24: Ignores search results
P1-27: Doesn't check if files exist
P1-30: Doesn't use indexed files

This module ensures all file references are verified before use.
"""

from __future__ import annotations

import fnmatch
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

if TYPE_CHECKING:
    from collections.abc import Iterator


@dataclass
class SearchResult:
    """A single search result with context."""

    file_path: str
    line_number: int
    line_content: str
    context_before: list[str] = field(default_factory=list)
    context_after: list[str] = field(default_factory=list)
    match_type: str = "content"  # content, filename, function, class

    @property
    def location(self) -> str:
        return f"{self.file_path}:{self.line_number}"


@dataclass
class SearchQuery:
    """A search query with parameters."""

    pattern: str
    file_glob: str | None = None  # e.g., "*.py"
    max_results: int = 50
    include_context: bool = True
    context_lines: int = 2
    case_sensitive: bool = False
    search_type: str = "content"  # content, filename, function, class


@dataclass
class SearchResponse:
    """Complete search response."""

    query: SearchQuery
    results: list[SearchResult]
    total_matches: int
    files_searched: int
    truncated: bool = False  # True if results were limited

    @property
    def has_results(self) -> bool:
        return len(self.results) > 0

    def get_unique_files(self) -> set[str]:
        return {r.file_path for r in self.results}

    def get_summary(self) -> str:
        if not self.has_results:
            return f"No results found for '{self.query.pattern}'"
        return (
            f"Found {self.total_matches} matches in {len(self.get_unique_files())} files "
            f"(showing {len(self.results)})"
        )


class GroundedSearch:
    """
    Search implementation that actually executes and returns real results.

    Fixes:
    - P1-21: SEARCH: command actually executes
    - P1-22: Discovers files before planning
    - P1-24: Results are captured and used
    """

    # Directories to skip
    SKIP_DIRS: ClassVar[set[str]] = {
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        ".tox",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "dist",
        "build",
        ".eggs",
        "*.egg-info",
        ".next",
        ".nuxt",
        "coverage",
        "htmlcov",
        ".coverage",
        ".sage",
    }

    # File extensions to search
    CODE_EXTENSIONS: ClassVar[set[str]] = {
        ".py",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".go",
        ".rs",
        ".java",
        ".c",
        ".cpp",
        ".h",
        ".hpp",
        ".cs",
        ".rb",
        ".php",
        ".swift",
        ".kt",
        ".scala",
        ".sh",
        ".bash",
        ".zsh",
        ".yaml",
        ".yml",
        ".json",
        ".toml",
        ".md",
        ".rst",
        ".txt",
        ".sql",
        ".html",
        ".css",
        ".scss",
        ".sass",
        ".less",
    }

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self._file_cache: dict[str, list[str]] = {}
        self._file_index: set[str] = set()
        self._indexed = False

    def index_files(self, force: bool = False) -> int:
        """Index all files in the project. Returns count of indexed files."""
        if self._indexed and not force:
            return len(self._file_index)

        self._file_index.clear()

        for file_path in self._walk_files():
            rel_path = str(file_path.relative_to(self.base_dir))
            self._file_index.add(rel_path)

        self._indexed = True
        return len(self._file_index)

    def _walk_files(self) -> Iterator[Path]:
        """Walk directory tree yielding code files."""
        for root, dirs, files in os.walk(self.base_dir):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if not self._should_skip_dir(d)]

            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in self.CODE_EXTENSIONS:
                    yield file_path

    def _should_skip_dir(self, dirname: str) -> bool:
        """Check if directory should be skipped."""
        return any(fnmatch.fnmatch(dirname, pattern) for pattern in self.SKIP_DIRS)

    def file_exists(self, path: str) -> bool:
        """Check if a file exists (relative to base_dir or absolute)."""
        if Path(path).is_absolute():
            return Path(path).exists()
        return (self.base_dir / path).exists()

    def verify_file(self, path: str) -> tuple[bool, Path | None]:
        """Verify file exists and return its full path."""
        full_path = Path(path) if Path(path).is_absolute() else self.base_dir / path

        if full_path.exists():
            return True, full_path
        return False, None

    def verify_files(self, paths: list[str]) -> dict[str, bool]:
        """Verify multiple files exist."""
        return {path: self.file_exists(path) for path in paths}

    def search(self, query: SearchQuery) -> SearchResponse:
        """
        Execute a search query and return real results.

        This is the core function that makes SEARCH: commands actually work.
        """
        results: list[SearchResult] = []
        total_matches = 0
        files_searched = 0

        # Try ripgrep first (faster)
        if self._has_ripgrep():
            return self._search_with_ripgrep(query)

        # Fallback to Python implementation
        pattern = re.compile(query.pattern, re.IGNORECASE if not query.case_sensitive else 0)

        for file_path in self._walk_files():
            # Apply file glob filter
            if query.file_glob and not fnmatch.fnmatch(file_path.name, query.file_glob):
                continue

            files_searched += 1
            file_results = self._search_file(file_path, pattern, query)
            total_matches += len(file_results)
            results.extend(file_results)

            # Limit results
            if len(results) >= query.max_results:
                return SearchResponse(
                    query=query,
                    results=results[: query.max_results],
                    total_matches=total_matches,
                    files_searched=files_searched,
                    truncated=True,
                )

        return SearchResponse(
            query=query,
            results=results,
            total_matches=total_matches,
            files_searched=files_searched,
            truncated=False,
        )

    def _search_file(
        self, file_path: Path, pattern: re.Pattern, query: SearchQuery
    ) -> list[SearchResult]:
        """Search a single file for pattern matches."""
        results = []
        rel_path = str(file_path.relative_to(self.base_dir))

        try:
            # Get file content from cache or read
            if rel_path not in self._file_cache:
                content = file_path.read_text(encoding="utf-8", errors="replace")
                self._file_cache[rel_path] = content.splitlines()

            lines = self._file_cache[rel_path]

            for i, line in enumerate(lines, start=1):
                if pattern.search(line):
                    result = SearchResult(
                        file_path=rel_path,
                        line_number=i,
                        line_content=line.strip(),
                        match_type=query.search_type,
                    )

                    # Add context if requested
                    if query.include_context:
                        start = max(0, i - 1 - query.context_lines)
                        end = min(len(lines), i + query.context_lines)
                        result.context_before = [lines[j].strip() for j in range(start, i - 1)]
                        result.context_after = [lines[j].strip() for j in range(i, end)]

                    results.append(result)

        except Exception:  # noqa: S110
            pass  # Skip unreadable files silently

        return results

    def _has_ripgrep(self) -> bool:
        """Check if ripgrep is available."""
        try:
            subprocess.run(["rg", "--version"], capture_output=True, timeout=5, check=False)
            return True
        except Exception:
            return False

    def _search_with_ripgrep(self, query: SearchQuery) -> SearchResponse:
        """Use ripgrep for faster searching."""
        cmd = ["rg", "--line-number", "--no-heading", "--color=never"]

        if not query.case_sensitive:
            cmd.append("--ignore-case")

        if query.file_glob:
            cmd.extend(["--glob", query.file_glob])

        cmd.extend(["--max-count", str(query.max_results)])
        cmd.append(query.pattern)
        cmd.append(str(self.base_dir))

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.base_dir,
                check=False,
            )

            results = []
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue

                # Parse ripgrep output: file:line:content
                match = re.match(r"^([^:]+):(\d+):(.*)$", line)
                if match:
                    file_path, line_num, content = match.groups()
                    # Make path relative
                    try:
                        rel_path = str(Path(file_path).relative_to(self.base_dir))
                    except ValueError:
                        rel_path = file_path

                    results.append(
                        SearchResult(
                            file_path=rel_path,
                            line_number=int(line_num),
                            line_content=content.strip(),
                            match_type=query.search_type,
                        )
                    )

            return SearchResponse(
                query=query,
                results=results,
                total_matches=len(results),
                files_searched=-1,  # ripgrep doesn't report this
                truncated=len(results) >= query.max_results,
            )

        except Exception:
            # Fall back to Python search
            return self.search(
                SearchQuery(
                    pattern=query.pattern,
                    file_glob=query.file_glob,
                    max_results=query.max_results,
                )
            )

    def search_content(self, pattern: str, file_glob: str | None = None) -> SearchResponse:
        """Convenience method to search file contents."""
        return self.search(
            SearchQuery(
                pattern=pattern,
                file_glob=file_glob,
                search_type="content",
            )
        )

    def search_functions(self, name: str, language: str = "python") -> SearchResponse:
        """Search for function definitions."""
        if language == "python":
            pattern = rf"def\s+{re.escape(name)}\s*\("
        elif language in ("javascript", "typescript"):
            pattern = rf"(?:function\s+{re.escape(name)}|{re.escape(name)}\s*[=:]\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))"
        else:
            pattern = rf"\b{re.escape(name)}\s*\("

        return self.search(
            SearchQuery(
                pattern=pattern,
                search_type="function",
            )
        )

    def search_classes(self, name: str, language: str = "python") -> SearchResponse:
        """Search for class definitions."""
        if language == "python":
            pattern = rf"class\s+{re.escape(name)}\s*[:\(]"
        elif language in ("javascript", "typescript"):
            pattern = rf"class\s+{re.escape(name)}\s*(?:extends|implements|\{{)"
        else:
            pattern = rf"class\s+{re.escape(name)}"

        return self.search(
            SearchQuery(
                pattern=pattern,
                search_type="class",
            )
        )

    def find_files(self, pattern: str) -> list[str]:
        """Find files matching a glob pattern."""
        if not self._indexed:
            self.index_files()

        matching = []
        for file_path in self._file_index:
            if fnmatch.fnmatch(file_path, pattern) or fnmatch.fnmatch(
                Path(file_path).name, pattern
            ):
                matching.append(file_path)

        return sorted(matching)

    def read_file(self, path: str, max_lines: int = 500) -> str | None:
        """Read file content with line limit."""
        exists, full_path = self.verify_file(path)
        if not exists or full_path is None:
            return None

        try:
            content = full_path.read_text(encoding="utf-8", errors="replace")
            lines = content.splitlines()
            if len(lines) > max_lines:
                return (
                    "\n".join(lines[:max_lines])
                    + f"\n\n... (truncated, {len(lines) - max_lines} more lines)"
                )
            return content
        except Exception:
            return None


class FileReferenceValidator:
    """
    Validates that file references in generated content actually exist.

    Fixes:
    - P0-3: File path hallucination
    - P0-14: Assumption-based responses
    - P1-27: Doesn't check if files exist
    """

    def __init__(self, searcher: GroundedSearch):
        self.searcher = searcher
        self.verified_paths: set[str] = set()
        self.invalid_paths: set[str] = set()

    def extract_paths(self, content: str) -> set[str]:
        """Extract file paths from content."""
        paths = set()

        # Extract from FILE: block markers
        for match in re.finditer(r"FILE:\s*`([^`]+)`", content):
            paths.add(match.group(1))

        # Backtick paths with extensions
        for match in re.finditer(
            r"`([^`]+\.(?:py|js|ts|json|yaml|yml|md|toml|go|rs|java))`", content
        ):
            paths.add(match.group(1))

        # path:line references
        for match in re.finditer(
            r"([a-zA-Z0-9_/\-]+\.(?:py|js|ts|json|yaml|yml|md|toml|go|rs|java)):\d+", content
        ):
            paths.add(match.group(1))

        return paths

    def validate_content(self, content: str) -> tuple[set[str], set[str]]:
        """
        Validate all file references in content.

        Returns:
            Tuple of (valid_paths, invalid_paths)
        """
        paths = self.extract_paths(content)
        valid = set()
        invalid = set()

        for path in paths:
            if path in self.verified_paths:
                valid.add(path)
            elif path in self.invalid_paths:
                invalid.add(path)
            elif self.searcher.file_exists(path):
                valid.add(path)
                self.verified_paths.add(path)
            else:
                invalid.add(path)
                self.invalid_paths.add(path)

        return valid, invalid

    def must_verify_before_reference(self, path: str) -> bool:
        """Check if a path must be verified before being referenced."""
        # Already verified
        if path in self.verified_paths:
            return False

        # Known invalid
        if path in self.invalid_paths:
            return True

        # Unknown - needs verification
        return True

    def get_verification_status(self) -> dict[str, Any]:
        """Get current verification status."""
        return {
            "verified_count": len(self.verified_paths),
            "invalid_count": len(self.invalid_paths),
            "verified_paths": list(self.verified_paths),
            "invalid_paths": list(self.invalid_paths),
        }


# Command execution for SEARCH: directives


class SearchCommandExecutor:
    """
    Executes SEARCH: commands from agent output.

    Fixes:
    - P1-21: SEARCH: command actually executes
    - P1-24: Results are captured and returned
    """

    def __init__(self, base_dir: Path):
        self.searcher = GroundedSearch(base_dir)
        self.validator = FileReferenceValidator(self.searcher)
        self.search_history: list[dict[str, Any]] = []

    def execute(self, command: str) -> SearchResponse:
        """
        Execute a SEARCH: command and return results.

        Supports formats:
        - SEARCH: pattern
        - SEARCH: pattern *.py
        - SEARCH: "multi word pattern"
        """
        # Parse command
        command = command.strip()
        if command.upper().startswith("SEARCH:"):
            command = command[7:].strip()

        # Extract file glob if present
        file_glob = None
        match = re.match(r"^(.+?)\s+(\*\.\w+)$", command)
        if match:
            command = match.group(1)
            file_glob = match.group(2)

        # Remove quotes if present
        if (command.startswith('"') and command.endswith('"')) or (
            command.startswith("'") and command.endswith("'")
        ):
            command = command[1:-1]

        # Execute search
        query = SearchQuery(
            pattern=command,
            file_glob=file_glob,
            max_results=50,
            include_context=True,
        )

        response = self.searcher.search(query)

        # Record in history
        self.search_history.append(
            {
                "query": command,
                "file_glob": file_glob,
                "results_count": len(response.results),
                "files_found": list(response.get_unique_files()),
            }
        )

        return response

    def format_results(self, response: SearchResponse) -> str:
        """Format search results for inclusion in prompts."""
        if not response.has_results:
            return f"No results found for: {response.query.pattern}"

        lines = [response.get_summary(), ""]

        for result in response.results[:20]:  # Limit displayed results
            lines.append(f"  {result.location}: {result.line_content[:80]}")

        if len(response.results) > 20:
            lines.append(f"  ... and {len(response.results) - 20} more matches")

        return "\n".join(lines)


# Convenience functions


def search_codebase(base_dir: Path, pattern: str, file_glob: str | None = None) -> SearchResponse:
    """Search codebase for pattern."""
    searcher = GroundedSearch(base_dir)
    return searcher.search(
        SearchQuery(
            pattern=pattern,
            file_glob=file_glob,
        )
    )


def verify_file_exists(base_dir: Path, path: str) -> bool:
    """Verify a file exists."""
    searcher = GroundedSearch(base_dir)
    return searcher.file_exists(path)


def find_files_matching(base_dir: Path, pattern: str) -> list[str]:
    """Find files matching a glob pattern."""
    searcher = GroundedSearch(base_dir)
    searcher.index_files()
    return searcher.find_files(pattern)
