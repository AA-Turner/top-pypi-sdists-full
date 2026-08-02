"""Builtin grep tool for the Vibe SDK."""

import asyncio
import shutil
from enum import StrEnum, auto
from pathlib import Path

from pydantic import BaseModel, Field, field_validator

from mistralai.vibe.sdk.capabilities import tool
from mistralai.vibe.sdk.capabilities.utils import candidate_encodings, resolve_path


class GrepBackend(StrEnum):
    RIPGREP = auto()
    GNU_GREP = auto()


class GrepArgs(BaseModel):
    pattern: str = Field(description="Regular expression pattern to search for.")
    path: str = Field(
        default=".",
        description="File or directory path to search recursively.",
    )
    max_matches: int = Field(
        default=100,
        gt=0,
        description="Maximum number of matches to return.",
    )
    max_output_bytes: int = Field(
        default=64_000,
        gt=0,
        description="Maximum UTF-8 output size to return across all matches.",
    )
    timeout_seconds: int = Field(
        default=60,
        gt=0,
        description="Timeout for the underlying search command.",
    )
    exclude_patterns: list[str] = Field(
        default_factory=lambda: [
            ".venv/",
            "venv/",
            ".env/",
            "env/",
            "node_modules/",
            ".git/",
            "__pycache__/",
            ".pytest_cache/",
            ".mypy_cache/",
            ".tox/",
            ".nox/",
            ".coverage/",
            "htmlcov/",
            "dist/",
            "build/",
            ".idea/",
            ".vscode/",
            "*.egg-info",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".DS_Store",
            "Thumbs.db",
        ],
        description="Glob patterns to exclude from the search.",
    )
    ignore_files: list[str] = Field(
        default_factory=lambda: [".vibeignore"],
        description="Ignore-rule files to apply in addition to backend defaults.",
    )
    use_native_ignore_files: bool = Field(
        default=True,
        description=(
            "When ripgrep is available, respect automatically discovered ignore "
            "files such as .gitignore, .ignore, and .rgignore. GNU grep fallback "
            "only applies explicit exclude_patterns and ignore_files."
        ),
    )

    @field_validator("pattern")
    @classmethod
    def _validate_pattern(cls, value: str) -> str:
        pattern = value.strip()
        if not pattern:
            raise ValueError("Empty search pattern provided.")
        return pattern

    @field_validator("path")
    @classmethod
    def _validate_path_str(cls, value: str) -> str:
        path = value.strip()
        if not path:
            raise ValueError("Path cannot be empty.")
        return path

    @field_validator("exclude_patterns", "ignore_files")
    @classmethod
    def _normalize_string_lists(cls, values: list[str]) -> list[str]:
        normalized: list[str] = []
        for value in values:
            stripped = value.strip()
            if stripped:
                normalized.append(stripped)
        return normalized


class GrepResult(BaseModel):
    matches: str
    match_count: int
    was_truncated: bool = Field(description="True if output was cut short by match or byte limits.")


@tool(
    name="grep",
    description=(
        "Recursively search files for a regex pattern using ripgrep (rg) or grep. "
        "Ripgrep respects native ignore files such as .gitignore, .ignore, and "
        ".rgignore when enabled; GNU grep fallback applies explicit "
        "exclude_patterns and ignore_files only."
    ),
    input_schema=GrepArgs,
    result_schema=GrepResult,
)
async def grep(args: GrepArgs) -> GrepResult:
    search_path = resolve_path(args.path)
    if not search_path.exists():
        raise ValueError(f"Path does not exist: {args.path}")
    backend = _detect_backend()
    search_root = search_path if search_path.is_dir() else search_path.parent
    ignore_file_paths = _resolve_existing_ignore_files(
        args.ignore_files,
        search_root=search_root,
    )
    exclude_patterns = _collect_exclude_patterns(
        args.exclude_patterns,
        ignore_file_paths=ignore_file_paths,
        backend=backend,
    )
    command = _build_command(
        args,
        backend=backend,
        exclude_patterns=exclude_patterns,
        ignore_file_paths=ignore_file_paths,
    )
    return await _execute_search(
        command,
        max_matches=args.max_matches,
        max_output_bytes=args.max_output_bytes,
        timeout_seconds=args.timeout_seconds,
    )


def _detect_backend() -> GrepBackend:
    if shutil.which("rg"):
        return GrepBackend.RIPGREP
    if shutil.which("grep"):
        return GrepBackend.GNU_GREP
    raise ValueError(
        "Neither ripgrep (rg) nor grep is installed. "
        "Please install ripgrep: https://github.com/BurntSushi/ripgrep#installation"
    )


def _resolve_existing_ignore_files(
    ignore_files: list[str],
    *,
    search_root: Path,
) -> list[Path]:
    resolved_paths: list[Path] = []
    seen_paths: set[Path] = set()
    for ignore_file in ignore_files:
        ignore_path = Path(ignore_file)
        candidate_paths = (
            [resolve_path(ignore_file)]
            if ignore_path.is_absolute()
            else [
                (search_root / ignore_file).resolve(),
                resolve_path(ignore_file),
            ]
        )
        for candidate_path in candidate_paths:
            if not candidate_path.is_file():
                continue
            if candidate_path in seen_paths:
                continue
            seen_paths.add(candidate_path)
            resolved_paths.append(candidate_path)
    return resolved_paths


def _collect_exclude_patterns(
    exclude_patterns: list[str],
    *,
    ignore_file_paths: list[Path],
    backend: GrepBackend,
) -> list[str]:
    patterns = list(exclude_patterns)
    if backend == GrepBackend.RIPGREP:
        return patterns

    for ignore_path in ignore_file_paths:
        patterns.extend(_load_ignore_patterns(ignore_path))
    return patterns


def _load_ignore_patterns(ignore_path: Path) -> list[str]:
    try:
        raw = ignore_path.read_bytes()
    except OSError:
        return []

    for encoding in candidate_encodings(raw):
        try:
            content = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        return []

    patterns: list[str] = []
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("!"):
            continue
        patterns.append(stripped)
    return patterns


def _build_command(
    args: GrepArgs,
    *,
    backend: GrepBackend,
    exclude_patterns: list[str],
    ignore_file_paths: list[Path],
) -> list[str]:
    if backend == GrepBackend.RIPGREP:
        return _build_ripgrep_command(args, exclude_patterns, ignore_file_paths)
    return _build_gnu_grep_command(args, exclude_patterns)


def _build_ripgrep_command(
    args: GrepArgs,
    exclude_patterns: list[str],
    ignore_file_paths: list[Path],
) -> list[str]:
    command = [
        "rg",
        "--line-number",
        "--no-heading",
        "--with-filename",
        "--smart-case",
        "--no-binary",
        "--max-count",
        str(args.max_matches + 1),
    ]

    if not args.use_native_ignore_files:
        command.append("--no-ignore")

    for ignore_file_path in ignore_file_paths:
        command.extend(["--ignore-file", str(ignore_file_path)])

    for pattern in exclude_patterns:
        command.extend(["--glob", f"!{pattern}"])

    command.extend(["-e", args.pattern, args.path])
    return command


def _build_gnu_grep_command(args: GrepArgs, exclude_patterns: list[str]) -> list[str]:
    command = ["grep", "-r", "-n", "-I", "-E", f"--max-count={args.max_matches + 1}"]

    if args.pattern.islower():
        command.append("-i")

    for pattern in exclude_patterns:
        if pattern.endswith("/"):
            command.append(f"--exclude-dir={pattern.rstrip('/')}")
            continue
        command.append(f"--exclude={pattern}")

    command.extend(["-e", args.pattern, args.path])
    return command


async def _execute_search(
    command: list[str],
    *,
    max_matches: int,
    max_output_bytes: int,
    timeout_seconds: int,
) -> GrepResult:
    try:
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    except OSError as exc:
        raise ValueError(f"Error running grep: {exc}") from exc

    try:
        stdout_bytes, stderr_bytes = await asyncio.wait_for(
            process.communicate(),
            timeout=timeout_seconds,
        )
    except TimeoutError as exc:
        process.kill()
        await process.communicate()
        raise ValueError(f"Search timed out after {timeout_seconds}s") from exc

    stderr = stderr_bytes.decode("utf-8", errors="ignore") if stderr_bytes else ""

    if process.returncode not in {0, 1}:
        error_message = stderr or f"Process exited with code {process.returncode}"
        raise ValueError(f"grep error: {error_message}")

    return _parse_output(
        stdout_bytes or b"",
        max_matches=max_matches,
        max_output_bytes=max_output_bytes,
    )


def _parse_output(
    stdout: bytes,
    *,
    max_matches: int,
    max_output_bytes: int,
) -> GrepResult:
    output_lines = stdout.splitlines()
    candidate_lines = output_lines[:max_matches]
    emitted_output = bytearray()
    emitted_count = 0

    for line in candidate_lines:
        chunk = line if emitted_count == 0 else b"\n" + line
        if len(emitted_output) + len(chunk) > max_output_bytes:
            break
        emitted_output.extend(chunk)
        emitted_count += 1

    was_truncated = len(output_lines) > max_matches or emitted_count < len(candidate_lines)

    return GrepResult(
        matches=emitted_output.decode("utf-8", errors="ignore"),
        match_count=emitted_count,
        was_truncated=was_truncated,
    )
