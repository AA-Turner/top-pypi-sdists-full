"""File and directory reading tool with binary detection, pagination, and fuzzy path suggestions."""

import base64
import mimetypes
import tempfile
import typing as t
from pathlib import Path
from urllib.parse import urlparse

import aiofiles

from dreadnode.agents.tools import tool

# --- Constants ----------------------------------------------------------------

DEFAULT_READ_LIMIT = 2000
"""Default maximum number of lines to return."""

MAX_LINE_LENGTH = 2000
"""Truncate individual lines longer than this."""

MAX_LINE_SUFFIX = f"... (line truncated to {MAX_LINE_LENGTH} chars)"

MAX_BYTES = 50 * 1024
"""Hard cap on total output size in bytes (50 KB)."""

_MAX_DOWNLOAD_BYTES = 10 * 1024 * 1024
"""Hard cap on remote file downloads in bytes (10 MB)."""

_BINARY_SAMPLE_SIZE = 4096
"""Number of bytes to sample for binary content detection."""

_NON_PRINTABLE_THRESHOLD = 0.30
"""If more than 30% of sampled bytes are non-printable, treat as binary."""

# Extensions that are always binary — no need to sample content.
_BINARY_EXTENSIONS: frozenset[str] = frozenset(
    {
        # Archives
        ".zip",
        ".tar",
        ".gz",
        ".bz2",
        ".xz",
        ".7z",
        ".rar",
        # Executables / shared objects
        ".exe",
        ".dll",
        ".so",
        ".dylib",
        ".class",
        ".jar",
        ".war",
        ".wasm",
        # Compiled Python
        ".pyc",
        ".pyo",
        # Object files / libraries
        ".o",
        ".a",
        ".obj",
        ".lib",
        # Data / binary blobs
        ".bin",
        ".dat",
        # Office documents (binary formats)
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".odt",
        ".ods",
        ".odp",
        # Media (non-image — images handled separately)
        ".mp3",
        ".mp4",
        ".avi",
        ".mov",
        ".flac",
        ".wav",
        # Databases
        ".sqlite",
        ".db",
    }
)


# --- Helpers ------------------------------------------------------------------


def _human_size(num_bytes: int) -> str:
    """Format a byte count as a compact human-readable string (e.g. ``12.3 KB``)."""
    size = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"  # unreachable, satisfies type checker


def _cleanup_temp_file(path: Path | None) -> None:
    if path is not None:
        path.unlink(missing_ok=True)


async def _download_url_to_temp(url: str, filename: str) -> Path:
    """Download a remote URL to a temporary file and return the path."""
    import httpx

    suffix = Path(filename).suffix or ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp_path = Path(tmp.name)
        completed = False
        try:
            async with (
                httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client,
                client.stream("GET", url) as response,
            ):
                response.raise_for_status()
                total = 0
                async for chunk in response.aiter_bytes():
                    total += len(chunk)
                    if total > _MAX_DOWNLOAD_BYTES:
                        raise ValueError("remote file exceeds max download size")
                    tmp.write(chunk)
            completed = True
        finally:
            if not completed:
                tmp_path.unlink(missing_ok=True)
        return tmp_path


async def _is_binary_file(filepath: Path, file_size: int) -> bool:
    """Detect whether a file is binary.

    Uses a two-tier strategy matching opencode's ``isBinaryFile``:
    1. Extension-based check for known binary types (instant).
    2. Content sampling — read first 4096 bytes, reject on null byte
       or >30% non-printable characters.
    """
    if filepath.suffix.lower() in _BINARY_EXTENSIONS:
        return True

    if file_size == 0:
        return False

    sample_size = min(_BINARY_SAMPLE_SIZE, file_size)
    async with aiofiles.open(filepath, "rb") as f:
        sample = await f.read(sample_size)

    if not sample:
        return False

    non_printable = 0
    for byte in sample:
        # Null byte is an immediate binary indicator.
        if byte == 0:
            return True
        # Non-printable: outside tab(9), LF(10), CR(13), and printable range (32-126).
        if byte < 9 or (13 < byte < 32):
            non_printable += 1

    return non_printable / len(sample) > _NON_PRINTABLE_THRESHOLD


async def _read_directory(dirpath: Path, offset: int, limit: int) -> str:
    """List directory entries with pagination.

    Directories get a trailing ``/``. Symlinks to directories likewise.
    Entries are sorted alphabetically (case-insensitive).
    """
    entries: list[str] = []
    for child in dirpath.iterdir():
        try:
            if child.is_dir():
                entries.append(child.name + "/")
            elif child.is_symlink():
                # Resolve symlink — if target is a directory, add trailing /
                try:
                    if child.resolve().is_dir():
                        entries.append(child.name + "/")
                    else:
                        entries.append(child.name)
                except OSError:
                    entries.append(child.name)
            else:
                entries.append(child.name)
        except OSError:
            entries.append(child.name)

    entries.sort(key=str.lower)

    start = offset - 1
    sliced = entries[start : start + limit]
    truncated = start + len(sliced) < len(entries)

    lines = [str(dirpath)]
    lines.extend(sliced)

    if truncated:
        lines.append(
            f"\n(Showing {len(sliced)} of {len(entries)} entries. "
            f"Use offset={offset + len(sliced)} to see more.)"
        )
    else:
        lines.append(f"\n({len(entries)} entries)")

    return "\n".join(lines)


def _suggest_similar(filepath: Path) -> list[str]:
    """Find up to 3 similarly-named files in the parent directory."""
    parent = filepath.parent
    base = filepath.name.lower()

    if not parent.is_dir():
        return []

    suggestions: list[str] = []
    try:
        for entry in parent.iterdir():
            name = entry.name.lower()
            if base in name or name in base:
                suggestions.append(str(entry))
                if len(suggestions) >= 3:
                    break
    except OSError:
        pass

    return suggestions


# --- Tool ---------------------------------------------------------------------


@tool
async def read(
    file_path: t.Annotated[
        str, "Absolute or relative path, or a http/https URL, to the file or directory to read"
    ],
    offset: t.Annotated[int | None, "Line number to start reading from (1-indexed)"] = None,
    limit: t.Annotated[int | None, "Maximum number of lines to read (default 2000)"] = None,
    *,
    cwd: t.Annotated[str | None, "Working directory for relative paths"] = None,
) -> t.Any:
    """
    Read a file or directory from the local filesystem, or download and read
    a remote file via http/https URL.

    Contents are returned with each line prefixed by its line number as
    ``<line>: <content>``. For directories, entries are listed one per line
    with a trailing ``/`` for subdirectories. Images and videos are returned
    as a short text caption plus a multimodal ``ContentImageUrl`` or
    ``ContentVideoUrl`` object so VLMs receive proper vision/video input.
    PDFs are returned as base64-encoded text.

    - Use ``offset`` and ``limit`` to page through large files. Avoid tiny
      repeated slices (e.g. 30 lines) — read a larger window instead.
    - Use the ``grep`` tool to find specific content in large files.
    - If you are unsure of the correct file path, use ``glob`` to look up
      filenames by pattern.
    - Call this tool in parallel when you know there are multiple files to
      read.
    - Any line longer than 2000 characters is truncated.

    Args:
        file_path: Path to the file or directory (absolute or relative to cwd),
            or an http/https URL to a remote file.
        offset: Line number to start reading from (1-indexed). Default: 1.
        limit: Maximum number of lines to return. Default: 2000.
        cwd: Working directory for resolving relative paths.

    Returns:
        File contents with line numbers, directory listing, or multimodal/base64 data.
    """
    effective_offset = offset if offset is not None else 1
    effective_limit = limit if limit is not None else DEFAULT_READ_LIMIT

    if effective_offset < 1:
        raise ValueError("offset must be >= 1")

    # --- Remote URL → download to temp file ---
    parsed = urlparse(file_path)
    source_name: str | None = None
    remote_temp_path: Path | None = None
    if parsed.scheme in ("http", "https"):
        source_name = Path(parsed.path).name or "download"
        filepath = await _download_url_to_temp(file_path, source_name)
        remote_temp_path = filepath
    else:
        base = Path(cwd) if cwd else Path.cwd()
        filepath = base / file_path if not Path(file_path).is_absolute() else Path(file_path)
        source_name = filepath.name

    # --- Not found → fuzzy suggestions ---
    if not filepath.exists():
        suggestions = _suggest_similar(filepath)
        msg = f"File not found: {filepath}"
        if suggestions:
            msg += "\n\nDid you mean one of these?\n" + "\n".join(suggestions)
        raise FileNotFoundError(msg)

    # --- Directory listing ---
    if filepath.is_dir():
        result = await _read_directory(filepath, effective_offset, effective_limit)
        _cleanup_temp_file(remote_temp_path)
        return result

    stat = filepath.stat()

    # ".ts"/".mts" TypeScript source maps to the "video/mp2t" MIME type in the
    # stdlib, since ".ts" is also the MPEG transport stream extension. Reading
    # such a file would otherwise ship TypeScript source to the model as a video,
    # which the provider rejects and which fails the whole generation. So the
    # video branch is additionally gated on the content actually being binary.
    # Image and PDF routing stays MIME-based — no plain-text extension collides
    # with those types (SVG, the one text-based image type, is excluded below).
    is_binary = await _is_binary_file(filepath, stat.st_size)

    # --- Image / Video / PDF → structured content or base64 ---
    mime_type, _ = mimetypes.guess_type(str(filepath))
    if mime_type:
        is_image = mime_type.startswith("image/") and mime_type not in (
            "image/svg+xml",  # SVG is XML-based text
        )
        is_video = mime_type.startswith("video/") and is_binary
        is_pdf = mime_type == "application/pdf"

        if is_image or is_video or is_pdf:
            async with aiofiles.open(filepath, "rb") as f:
                raw = await f.read()
            if is_image:
                from dreadnode.generators.message import ContentImageUrl, ContentText

                # Pair the image with a short text caption. The caption gives the
                # model a label for what it's looking at and is the single line the
                # TUI shows as the call's result summary — the path is already
                # visible in the call itself, so it is deliberately omitted here.
                fmt = mime_type.split("/", 1)[-1].upper()
                caption = f"Read image · {fmt} · {_human_size(len(raw))}"
                result = [
                    ContentText(text=caption),
                    ContentImageUrl.from_bytes(raw, mimetype=mime_type),
                ]
                _cleanup_temp_file(remote_temp_path)
                return result
            if is_video:
                from dreadnode.generators.message import ContentText, ContentVideoUrl

                # Pair the video with a short text caption, mirroring the image
                # path so vision-language models receive proper video input.
                fmt = mime_type.split("/", 1)[-1].upper()
                caption = f"Read video · {fmt} · {_human_size(len(raw))}"
                result = [
                    ContentText(text=caption),
                    ContentVideoUrl.from_bytes(raw, mimetype=mime_type, filename=source_name),
                ]
                _cleanup_temp_file(remote_temp_path)
                return result
            encoded = base64.b64encode(raw).decode("ascii")
            result = (
                f"PDF: {filepath}\n"
                f"Type: {mime_type}\n"
                f"Size: {stat.st_size:,} bytes\n"
                f"Base64: {encoded}"
            )
            _cleanup_temp_file(remote_temp_path)
            return result

    # --- Binary detection ---
    # Binary files that aren't recognized media (handled above) can't be read.
    if is_binary:
        _cleanup_temp_file(remote_temp_path)
        raise ValueError(f"Cannot read binary file: {filepath}")

    # --- Text file reading with dual truncation ---
    lines_out: list[str] = []
    total_bytes = 0
    total_lines = 0
    lines_read = 0
    truncated_by_bytes = False
    has_more_lines = False
    start = effective_offset - 1

    async with aiofiles.open(filepath, errors="replace") as f:
        line_num = 0
        async for raw_line in f:
            line_num += 1
            total_lines = line_num

            # Skip lines before offset.
            if line_num <= start:
                continue

            # Already collected enough lines — just count remaining.
            if lines_read >= effective_limit:
                has_more_lines = True
                continue

            line_content = raw_line.rstrip("\n\r")

            # Per-line truncation.
            if len(line_content) > MAX_LINE_LENGTH:
                line_content = line_content[:MAX_LINE_LENGTH] + MAX_LINE_SUFFIX

            formatted = f"{line_num:>6}\u2192{line_content}"

            # Byte-level cap check.
            line_bytes = len(formatted.encode("utf-8")) + (1 if lines_out else 0)
            if total_bytes + line_bytes > MAX_BYTES:
                truncated_by_bytes = True
                has_more_lines = True
                break

            lines_out.append(formatted)
            total_bytes += line_bytes
            lines_read += 1

    # Edge case: offset beyond file length.
    if total_lines < effective_offset and not (total_lines == 0 and effective_offset == 1):
        _cleanup_temp_file(remote_temp_path)
        raise ValueError(f"offset {effective_offset} is beyond end of file ({total_lines} lines)")

    # --- Build output ---
    content = "\n".join(lines_out)

    last_line = effective_offset + lines_read - 1
    next_offset = last_line + 1

    if truncated_by_bytes:
        content += (
            f"\n\n(Output capped at {MAX_BYTES // 1024} KB. "
            f"Showing lines {effective_offset}-{last_line}. "
            f"Use offset={next_offset} to continue.)"
        )
    elif has_more_lines:
        content += (
            f"\n\n(Showing lines {effective_offset}-{last_line} of {total_lines}. "
            f"Use offset={next_offset} to continue.)"
        )
    else:
        content += f"\n\n(End of file — {total_lines} lines total)"

    _cleanup_temp_file(remote_temp_path)
    return content
