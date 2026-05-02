"""Tool Orchestrator module for SAGE.

Implements Items 161-200 from the product roadmap:
- Items 161-175: Search & Discovery
- Items 176-190: File Reading
- Items 191-200: Tool Orchestration
"""

from __future__ import annotations

import fnmatch
import re
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import ClassVar

# ============================================================================
# Items 161-175: Search & Discovery
# ============================================================================


class SearchStrategy(Enum):
    """Item 161: Search strategy selection."""

    EXACT_MATCH = auto()  # Item 162: Exact string search
    FUZZY_MATCH = auto()  # Item 163: Fuzzy/approximate search
    REGEX_MATCH = auto()  # Item 164: Regular expression search
    SEMANTIC = auto()  # Item 165: Semantic/meaning-based search
    STRUCTURAL = auto()  # Item 166: Code structure search (AST)
    COMBINED = auto()  # Item 167: Multi-strategy combination


@dataclass
class SearchQuery:
    """Item 168: Structured search query."""

    raw_query: str
    strategy: SearchStrategy = SearchStrategy.EXACT_MATCH
    file_patterns: list[str] = field(default_factory=list)  # Item 169
    exclude_patterns: list[str] = field(default_factory=list)  # Item 170
    case_sensitive: bool = False  # Item 171
    whole_word: bool = False  # Item 172
    max_results: int = 100  # Item 173
    include_context: bool = True  # Item 174
    context_lines: int = 3  # Item 175


@dataclass
class SearchResult:
    """Search result with context."""

    file_path: str
    line_number: int
    line_content: str
    match_start: int
    match_end: int
    context_before: list[str] = field(default_factory=list)
    context_after: list[str] = field(default_factory=list)
    relevance_score: float = 1.0


class SearchEngine:
    """Item 161-175: Intelligent search engine."""

    # Item 169: Common file patterns
    LANGUAGE_PATTERNS: ClassVar[dict[str, list[str]]] = {
        "python": ["*.py", "*.pyi", "*.pyw"],
        "javascript": ["*.js", "*.jsx", "*.mjs", "*.cjs"],
        "typescript": ["*.ts", "*.tsx", "*.mts", "*.cts"],
        "java": ["*.java"],
        "go": ["*.go"],
        "rust": ["*.rs"],
        "c": ["*.c", "*.h"],
        "cpp": ["*.cpp", "*.cc", "*.cxx", "*.hpp", "*.hh"],
        "config": ["*.json", "*.yaml", "*.yml", "*.toml", "*.ini", "*.cfg"],
        "docs": ["*.md", "*.rst", "*.txt"],
    }

    # Item 170: Default exclude patterns
    DEFAULT_EXCLUDES: ClassVar[list[str]] = [
        "__pycache__",
        "*.pyc",
        ".git",
        ".svn",
        "node_modules",
        ".venv",
        "venv",
        "env",
        ".env",
        "dist",
        "build",
        "*.egg-info",
        ".tox",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "htmlcov",
        "*.min.js",
        "*.min.css",
        "*.map",
    ]

    def __init__(self, root_path: str | Path):
        self.root_path = Path(root_path)
        self._file_cache: dict[str, str] = {}

    def search(self, query: SearchQuery) -> list[SearchResult]:
        """Execute search with given query."""
        results: list[SearchResult] = []

        # Get files to search
        files = self._get_searchable_files(query.file_patterns, query.exclude_patterns)

        for file_path in files:
            if len(results) >= query.max_results:
                break

            file_results = self._search_file(file_path, query)
            results.extend(file_results)

        # Sort by relevance
        results.sort(key=lambda r: r.relevance_score, reverse=True)

        return results[: query.max_results]

    def _get_searchable_files(
        self, include_patterns: list[str], exclude_patterns: list[str]
    ) -> list[Path]:
        """Item 169-170: Get files matching patterns."""
        exclude = set(exclude_patterns) | set(self.DEFAULT_EXCLUDES)

        files: list[Path] = []
        for path in self.root_path.rglob("*"):
            if not path.is_file():
                continue

            # Check excludes
            path_str = str(path)
            if any(fnmatch.fnmatch(path_str, excl) or excl in path_str for excl in exclude):
                continue

            # Check includes (if specified)
            if include_patterns:
                if not any(fnmatch.fnmatch(path.name, pat) for pat in include_patterns):
                    continue

            files.append(path)

        return files

    def _search_file(self, file_path: Path, query: SearchQuery) -> list[SearchResult]:
        """Search within a single file."""
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return []

        lines = content.splitlines()
        results: list[SearchResult] = []

        pattern = self._build_pattern(query)
        flags = 0 if query.case_sensitive else re.IGNORECASE

        for i, line in enumerate(lines):
            matches = list(re.finditer(pattern, line, flags))
            for match in matches:
                # Item 174-175: Context extraction
                context_before = lines[max(0, i - query.context_lines) : i]
                context_after = lines[i + 1 : i + 1 + query.context_lines]

                results.append(
                    SearchResult(
                        file_path=str(file_path.relative_to(self.root_path)),
                        line_number=i + 1,
                        line_content=line,
                        match_start=match.start(),
                        match_end=match.end(),
                        context_before=context_before if query.include_context else [],
                        context_after=context_after if query.include_context else [],
                        relevance_score=self._calculate_relevance(match, line, file_path),
                    )
                )

        return results

    def _build_pattern(self, query: SearchQuery) -> str:
        """Item 162-164: Build search pattern based on strategy."""
        if query.strategy == SearchStrategy.REGEX_MATCH:
            return query.raw_query

        # Escape for exact/fuzzy match
        escaped = re.escape(query.raw_query)

        if query.whole_word:
            escaped = rf"\b{escaped}\b"

        return escaped

    def _calculate_relevance(self, match: re.Match, line: str, file_path: Path) -> float:
        """Item 165: Calculate result relevance."""
        score = 1.0

        # Boost for exact case match
        if match.group() == match.string[match.start() : match.end()]:
            score += 0.2

        # Boost for matches at word boundaries
        if match.start() == 0 or not line[match.start() - 1].isalnum():
            score += 0.1

        # Boost for source files over tests
        if "test" in str(file_path).lower():
            score -= 0.1

        # Boost for core modules
        if "core" in str(file_path).lower():
            score += 0.1

        return min(score, 2.0)


class QueryAnalyzer:
    """Item 167: Analyze queries to determine best search strategy."""

    # Item 162: Patterns indicating exact search
    EXACT_INDICATORS: ClassVar[list[str]] = [
        r"^[\"\'].*[\"\']$",  # Quoted strings
        r"^[A-Z][a-z]+[A-Z]",  # CamelCase
        r"^[a-z]+_[a-z]+",  # snake_case
    ]

    # Item 164: Patterns indicating regex search
    REGEX_INDICATORS: ClassVar[list[str]] = [
        r"[\.\*\+\?\[\]\(\)\{\}\|\\]",  # Regex metacharacters
    ]

    @classmethod
    def analyze(cls, query: str) -> SearchStrategy:
        """Determine best search strategy for query."""
        # Check for regex indicators
        for pattern in cls.REGEX_INDICATORS:
            if re.search(pattern, query):
                return SearchStrategy.REGEX_MATCH

        # Check for exact match indicators
        for pattern in cls.EXACT_INDICATORS:
            if re.search(pattern, query):
                return SearchStrategy.EXACT_MATCH

        # Default to fuzzy for natural language queries
        if " " in query and len(query.split()) > 2:
            return SearchStrategy.FUZZY_MATCH

        return SearchStrategy.EXACT_MATCH


# ============================================================================
# Items 176-190: File Reading
# ============================================================================


class FileReadStrategy(Enum):
    """Item 176: File reading strategies."""

    FULL = auto()  # Item 177: Read entire file
    RANGE = auto()  # Item 178: Read specific line range
    CHUNK = auto()  # Item 179: Read in chunks
    SMART = auto()  # Item 180: Smart context-aware reading
    SUMMARY = auto()  # Item 181: Read and summarize


@dataclass
class ReadRequest:
    """Item 182: Structured read request."""

    file_path: str
    strategy: FileReadStrategy = FileReadStrategy.FULL
    start_line: int | None = None  # Item 178
    end_line: int | None = None
    chunk_size: int = 500  # Item 179
    focus_pattern: str | None = None  # Item 180
    include_metadata: bool = True  # Item 183


@dataclass
class FileMetadata:
    """Item 183: File metadata."""

    file_path: str
    size_bytes: int
    line_count: int
    language: str
    encoding: str
    last_modified: float
    is_binary: bool


@dataclass
class ReadResult:
    """Item 184: Read result with metadata."""

    content: str
    metadata: FileMetadata | None
    start_line: int
    end_line: int
    truncated: bool = False
    truncation_message: str = ""


class SmartFileReader:
    """Items 176-190: Intelligent file reader."""

    # Item 185: Maximum file sizes
    MAX_FULL_READ_SIZE: ClassVar[int] = 100_000  # 100KB
    MAX_CONTEXT_LINES: ClassVar[int] = 500
    CHUNK_SIZE: ClassVar[int] = 1000

    # Item 186: Language detection by extension
    LANGUAGE_MAP: ClassVar[dict[str, str]] = {
        ".py": "python",
        ".pyi": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".java": "java",
        ".go": "go",
        ".rs": "rust",
        ".c": "c",
        ".h": "c",
        ".cpp": "cpp",
        ".hpp": "cpp",
        ".rb": "ruby",
        ".php": "php",
        ".swift": "swift",
        ".kt": "kotlin",
        ".scala": "scala",
        ".sh": "bash",
        ".bash": "bash",
        ".zsh": "zsh",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".toml": "toml",
        ".xml": "xml",
        ".html": "html",
        ".css": "css",
        ".scss": "scss",
        ".md": "markdown",
        ".rst": "restructuredtext",
        ".sql": "sql",
        ".dockerfile": "dockerfile",
    }

    # Item 187: Binary file extensions
    BINARY_EXTENSIONS: ClassVar[set[str]] = {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".ico",
        ".bmp",
        ".webp",
        ".svg",
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".zip",
        ".tar",
        ".gz",
        ".bz2",
        ".7z",
        ".rar",
        ".exe",
        ".dll",
        ".so",
        ".dylib",
        ".pyc",
        ".pyo",
        ".class",
        ".o",
        ".obj",
        ".woff",
        ".woff2",
        ".ttf",
        ".eot",
        ".mp3",
        ".mp4",
        ".wav",
        ".avi",
        ".mov",
    }

    def __init__(self, root_path: str | Path):
        self.root_path = Path(root_path)

    def read(self, request: ReadRequest) -> ReadResult:
        """Item 176: Read file according to strategy."""
        file_path = self.root_path / request.file_path

        if not file_path.exists():
            return ReadResult(
                content="",
                metadata=None,
                start_line=0,
                end_line=0,
                truncated=True,
                truncation_message=f"File not found: {request.file_path}",
            )

        metadata = self._get_metadata(file_path) if request.include_metadata else None

        if metadata and metadata.is_binary:
            return ReadResult(
                content="",
                metadata=metadata,
                start_line=0,
                end_line=0,
                truncated=True,
                truncation_message="Binary file cannot be read as text",
            )

        if request.strategy == FileReadStrategy.FULL:
            return self._read_full(file_path, metadata)
        elif request.strategy == FileReadStrategy.RANGE:
            return self._read_range(file_path, request.start_line, request.end_line, metadata)
        elif request.strategy == FileReadStrategy.CHUNK:
            return self._read_chunk(
                file_path, request.start_line or 1, request.chunk_size, metadata
            )
        elif request.strategy == FileReadStrategy.SMART:
            return self._read_smart(file_path, request.focus_pattern, metadata)
        else:  # SUMMARY
            return self._read_summary(file_path, metadata)

    def _get_metadata(self, file_path: Path) -> FileMetadata:
        """Item 183: Extract file metadata."""
        stat = file_path.stat()
        extension = file_path.suffix.lower()
        is_binary = extension in self.BINARY_EXTENSIONS

        line_count = 0
        encoding = "utf-8"
        if not is_binary:
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                line_count = content.count("\n") + 1
            except OSError:
                pass

        return FileMetadata(
            file_path=str(file_path),
            size_bytes=stat.st_size,
            line_count=line_count,
            language=self.LANGUAGE_MAP.get(extension, "unknown"),
            encoding=encoding,
            last_modified=stat.st_mtime,
            is_binary=is_binary,
        )

    def _read_full(self, file_path: Path, metadata: FileMetadata | None) -> ReadResult:
        """Item 177: Read entire file."""
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            lines = content.splitlines()

            # Check size limit
            if len(content) > self.MAX_FULL_READ_SIZE:
                # Truncate to fit
                truncated_lines = lines[: self.CHUNK_SIZE]
                return ReadResult(
                    content="\n".join(truncated_lines),
                    metadata=metadata,
                    start_line=1,
                    end_line=len(truncated_lines),
                    truncated=True,
                    truncation_message=f"File truncated from {len(lines)} to {len(truncated_lines)} lines",
                )

            return ReadResult(
                content=content,
                metadata=metadata,
                start_line=1,
                end_line=len(lines),
            )
        except OSError as e:
            return ReadResult(
                content="",
                metadata=metadata,
                start_line=0,
                end_line=0,
                truncated=True,
                truncation_message=f"Error reading file: {e}",
            )

    def _read_range(
        self,
        file_path: Path,
        start_line: int | None,
        end_line: int | None,
        metadata: FileMetadata | None,
    ) -> ReadResult:
        """Item 178: Read specific line range."""
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            lines = content.splitlines()

            start = (start_line or 1) - 1  # Convert to 0-indexed
            end = end_line or len(lines)

            # Clamp to valid range
            start = max(0, min(start, len(lines)))
            end = max(start, min(end, len(lines)))

            selected = lines[start:end]

            return ReadResult(
                content="\n".join(selected),
                metadata=metadata,
                start_line=start + 1,
                end_line=end,
            )
        except OSError as e:
            return ReadResult(
                content="",
                metadata=metadata,
                start_line=0,
                end_line=0,
                truncated=True,
                truncation_message=f"Error reading file: {e}",
            )

    def _read_chunk(
        self,
        file_path: Path,
        start_line: int,
        chunk_size: int,
        metadata: FileMetadata | None,
    ) -> ReadResult:
        """Item 179: Read in chunks."""
        return self._read_range(file_path, start_line, start_line + chunk_size - 1, metadata)

    def _read_smart(
        self,
        file_path: Path,
        focus_pattern: str | None,
        metadata: FileMetadata | None,
    ) -> ReadResult:
        """Item 180: Smart context-aware reading."""
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            lines = content.splitlines()

            if not focus_pattern:
                return self._read_full(file_path, metadata)

            # Find all matches
            match_lines: list[int] = []
            for i, line in enumerate(lines):
                if re.search(focus_pattern, line, re.IGNORECASE):
                    match_lines.append(i)

            if not match_lines:
                fallback = self._read_full(file_path, metadata)
                existing_message = fallback.truncation_message.strip()
                message = f"No matches for pattern '{focus_pattern}'. Showing full file."
                if existing_message:
                    message = f"{message} {existing_message}"
                return ReadResult(
                    content=fallback.content,
                    metadata=fallback.metadata,
                    start_line=fallback.start_line,
                    end_line=fallback.end_line,
                    truncated=True,
                    truncation_message=message,
                )

            # Build context around matches
            context_range = 20  # Lines before/after match
            included: set[int] = set()

            for match_line in match_lines:
                for i in range(
                    max(0, match_line - context_range),
                    min(len(lines), match_line + context_range + 1),
                ):
                    included.add(i)

            # Extract included lines
            sorted_included = sorted(included)
            selected_lines: list[str] = []
            prev_line = -2

            for line_num in sorted_included:
                if line_num > prev_line + 1:
                    selected_lines.append(f"... (skipped lines {prev_line + 2}-{line_num}) ...")
                selected_lines.append(f"{line_num + 1}: {lines[line_num]}")
                prev_line = line_num

            return ReadResult(
                content="\n".join(selected_lines),
                metadata=metadata,
                start_line=sorted_included[0] + 1 if sorted_included else 1,
                end_line=sorted_included[-1] + 1 if sorted_included else 1,
                truncated=len(included) < len(lines),
                truncation_message=f"Smart read: {len(included)} of {len(lines)} lines around pattern matches",
            )
        except OSError as e:
            return ReadResult(
                content="",
                metadata=metadata,
                start_line=0,
                end_line=0,
                truncated=True,
                truncation_message=f"Error reading file: {e}",
            )

    def _read_summary(self, file_path: Path, metadata: FileMetadata | None) -> ReadResult:
        """Item 181: Read and create summary."""
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            lines = content.splitlines()

            summary_parts: list[str] = []

            # Extract imports/includes (top of file)
            import_lines: list[str] = []
            for line in lines[:50]:
                if re.match(r"^\s*(import|from|#include|require|use|using)\s", line):
                    import_lines.append(line.strip())

            if import_lines:
                summary_parts.append("== IMPORTS ==")
                summary_parts.extend(import_lines[:20])
                summary_parts.append("")

            # Extract class/function definitions
            definitions: list[str] = []
            for i, line in enumerate(lines):
                if re.match(
                    r"^\s*(class|def|function|func|fn|pub fn|async fn|const|let|var)\s+\w+",
                    line,
                ):
                    definitions.append(f"{i + 1}: {line.strip()}")

            if definitions:
                summary_parts.append("== DEFINITIONS ==")
                summary_parts.extend(definitions[:50])
                summary_parts.append("")

            # Add file structure info
            summary_parts.append("== STRUCTURE ==")
            summary_parts.append(f"Total lines: {len(lines)}")
            summary_parts.append(
                f"Classes: {len([d for d in definitions if 'class' in d.lower()])}"
            )
            summary_parts.append(
                f"Functions: {len([d for d in definitions if 'def' in d.lower() or 'function' in d.lower() or 'func' in d.lower()])}"
            )

            return ReadResult(
                content="\n".join(summary_parts),
                metadata=metadata,
                start_line=1,
                end_line=len(lines),
                truncated=True,
                truncation_message="Summary view - use FULL strategy for complete content",
            )
        except OSError as e:
            return ReadResult(
                content="",
                metadata=metadata,
                start_line=0,
                end_line=0,
                truncated=True,
                truncation_message=f"Error reading file: {e}",
            )


# ============================================================================
# Items 191-200: Tool Orchestration
# ============================================================================


class ToolType(Enum):
    """Item 191: Available tool types."""

    SEARCH = auto()
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()
    ANALYZE = auto()
    VALIDATE = auto()


@dataclass
class ToolCall:
    """Item 192: Structured tool call."""

    tool_type: ToolType
    name: str
    parameters: dict
    priority: int = 0
    depends_on: list[str] = field(default_factory=list)  # Item 193


@dataclass
class ToolResult:
    """Item 194: Tool execution result."""

    call_id: str
    tool_type: ToolType
    success: bool
    output: str
    error: str | None = None
    execution_time_ms: float = 0.0
    metadata: dict = field(default_factory=dict)


class ToolOrchestrator:
    """Items 191-200: Coordinate tool usage."""

    # Item 195: Tool limits
    MAX_PARALLEL_CALLS: ClassVar[int] = 5
    MAX_SEQUENTIAL_CALLS: ClassVar[int] = 20
    MAX_SEARCH_RESULTS: ClassVar[int] = 100
    MAX_READ_BYTES: ClassVar[int] = 500_000

    # Item 196: Tool selection patterns
    TASK_TOOL_MAP: ClassVar[dict[str, list[ToolType]]] = {
        "find": [ToolType.SEARCH],
        "search": [ToolType.SEARCH],
        "locate": [ToolType.SEARCH],
        "read": [ToolType.READ],
        "show": [ToolType.READ],
        "display": [ToolType.READ],
        "write": [ToolType.WRITE],
        "create": [ToolType.WRITE],
        "modify": [ToolType.READ, ToolType.WRITE],
        "edit": [ToolType.READ, ToolType.WRITE],
        "run": [ToolType.EXECUTE],
        "execute": [ToolType.EXECUTE],
        "test": [ToolType.EXECUTE],
        "analyze": [ToolType.ANALYZE],
        "review": [ToolType.ANALYZE],
        "check": [ToolType.VALIDATE],
        "verify": [ToolType.VALIDATE],
        "validate": [ToolType.VALIDATE],
    }

    def __init__(self, root_path: str | Path):
        self.root_path = Path(root_path)
        self.search_engine = SearchEngine(root_path)
        self.file_reader = SmartFileReader(root_path)
        self._call_counter = 0
        self._results_cache: dict[str, ToolResult] = {}

    def plan_tool_sequence(self, task: str) -> list[ToolCall]:
        """Item 197: Plan optimal tool sequence for task."""
        calls: list[ToolCall] = []
        words = task.lower().split()

        # Identify required tools
        required_tools: set[ToolType] = set()
        for word in words:
            for pattern, tools in self.TASK_TOOL_MAP.items():
                if pattern in word:
                    required_tools.update(tools)

        # Create ordered tool calls
        priority = 0

        # Search first to locate files
        if ToolType.SEARCH in required_tools:
            calls.append(
                ToolCall(
                    tool_type=ToolType.SEARCH,
                    name="search",
                    parameters={"query": task},
                    priority=priority,
                )
            )
            priority += 1

        # Then read for context
        if ToolType.READ in required_tools or ToolType.ANALYZE in required_tools:
            search_id = calls[0].name if calls else None
            calls.append(
                ToolCall(
                    tool_type=ToolType.READ,
                    name="read",
                    parameters={},
                    priority=priority,
                    depends_on=[search_id] if search_id else [],
                )
            )
            priority += 1

        # Analyze if needed
        if ToolType.ANALYZE in required_tools:
            read_id = next((c.name for c in calls if c.tool_type == ToolType.READ), None)
            calls.append(
                ToolCall(
                    tool_type=ToolType.ANALYZE,
                    name="analyze",
                    parameters={},
                    priority=priority,
                    depends_on=[read_id] if read_id else [],
                )
            )
            priority += 1

        # Write/execute last
        if ToolType.WRITE in required_tools:
            analyze_id = next((c.name for c in calls if c.tool_type == ToolType.ANALYZE), None)
            calls.append(
                ToolCall(
                    tool_type=ToolType.WRITE,
                    name="write",
                    parameters={},
                    priority=priority,
                    depends_on=[analyze_id] if analyze_id else [],
                )
            )
            priority += 1

        if ToolType.EXECUTE in required_tools:
            write_id = next((c.name for c in calls if c.tool_type == ToolType.WRITE), None)
            calls.append(
                ToolCall(
                    tool_type=ToolType.EXECUTE,
                    name="execute",
                    parameters={},
                    priority=priority,
                    depends_on=[write_id] if write_id else [],
                )
            )
            priority += 1

        # Validate at end
        if ToolType.VALIDATE in required_tools:
            last_id = calls[-1].name if calls else None
            calls.append(
                ToolCall(
                    tool_type=ToolType.VALIDATE,
                    name="validate",
                    parameters={},
                    priority=priority,
                    depends_on=[last_id] if last_id else [],
                )
            )

        return calls

    def can_parallelize(self, calls: list[ToolCall]) -> list[list[ToolCall]]:
        """Item 198: Identify parallelizable tool calls."""
        if not calls:
            return []

        # Group by priority (same priority can run in parallel)
        by_priority: dict[int, list[ToolCall]] = {}
        for call in calls:
            if call.priority not in by_priority:
                by_priority[call.priority] = []
            by_priority[call.priority].append(call)

        # Check dependencies within each group
        parallel_groups: list[list[ToolCall]] = []
        for priority in sorted(by_priority.keys()):
            group = by_priority[priority]

            # Split group if there are internal dependencies
            independent: list[ToolCall] = []
            dependent: list[ToolCall] = []

            group_ids = {c.name for c in group}
            for call in group:
                if any(dep in group_ids for dep in call.depends_on):
                    dependent.append(call)
                else:
                    independent.append(call)

            if independent:
                parallel_groups.append(independent)
            for call in dependent:
                parallel_groups.append([call])

        return parallel_groups

    def select_tool_for_task(self, task: str) -> ToolType | None:
        """Item 199: Select most appropriate tool for simple task."""
        task_lower = task.lower()

        # Check each pattern
        best_match: ToolType | None = None
        for pattern, tools in self.TASK_TOOL_MAP.items():
            if pattern in task_lower:
                if not best_match or len(pattern) > 4:
                    best_match = tools[0]

        return best_match

    def estimate_tool_cost(self, call: ToolCall) -> dict[str, float]:
        """Item 200: Estimate resource cost of tool call."""
        costs = {
            "time_ms": 0.0,
            "memory_mb": 0.0,
            "io_ops": 0.0,
        }

        if call.tool_type == ToolType.SEARCH:
            costs["time_ms"] = 500.0
            costs["memory_mb"] = 50.0
            costs["io_ops"] = 100.0
        elif call.tool_type == ToolType.READ:
            costs["time_ms"] = 100.0
            costs["memory_mb"] = 10.0
            costs["io_ops"] = 1.0
        elif call.tool_type == ToolType.WRITE:
            costs["time_ms"] = 50.0
            costs["memory_mb"] = 5.0
            costs["io_ops"] = 1.0
        elif call.tool_type == ToolType.EXECUTE:
            costs["time_ms"] = 5000.0
            costs["memory_mb"] = 100.0
            costs["io_ops"] = 10.0
        elif call.tool_type == ToolType.ANALYZE:
            costs["time_ms"] = 1000.0
            costs["memory_mb"] = 200.0
            costs["io_ops"] = 50.0
        elif call.tool_type == ToolType.VALIDATE:
            costs["time_ms"] = 200.0
            costs["memory_mb"] = 20.0
            costs["io_ops"] = 5.0

        return costs


class ToolUsageTracker:
    """Track tool usage for optimization."""

    def __init__(self):
        self.calls: list[dict] = []
        self.errors: list[dict] = []

    def record_call(
        self,
        tool_type: ToolType,
        name: str,
        success: bool,
        execution_time_ms: float,
    ):
        """Record a tool call."""
        self.calls.append(
            {
                "tool_type": tool_type.name,
                "name": name,
                "success": success,
                "execution_time_ms": execution_time_ms,
            }
        )

    def record_error(self, tool_type: ToolType, error: str):
        """Record a tool error."""
        self.errors.append(
            {
                "tool_type": tool_type.name,
                "error": error,
            }
        )

    def get_stats(self) -> dict:
        """Get usage statistics."""
        total_calls = len(self.calls)
        successful = sum(1 for c in self.calls if c["success"])
        total_time = sum(c["execution_time_ms"] for c in self.calls)

        by_tool: dict[str, int] = {}
        for call in self.calls:
            tool = call["tool_type"]
            by_tool[tool] = by_tool.get(tool, 0) + 1

        return {
            "total_calls": total_calls,
            "successful_calls": successful,
            "failed_calls": total_calls - successful,
            "success_rate": successful / total_calls if total_calls > 0 else 0,
            "total_time_ms": total_time,
            "avg_time_ms": total_time / total_calls if total_calls > 0 else 0,
            "calls_by_tool": by_tool,
            "error_count": len(self.errors),
        }
