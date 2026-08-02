"""Builtin read_file tool for the Vibe SDK."""

from pathlib import Path

from pydantic import BaseModel, Field

from mistralai.vibe.sdk.capabilities import tool
from mistralai.vibe.sdk.capabilities.utils import candidate_encodings, resolve_path

MAX_READ_BYTES = 64_000
SNIFF_BYTES = 4_096


class ReadFileArgs(BaseModel):
    path: str
    offset: int = Field(
        default=0,
        description="Line number to start reading from (0-indexed, inclusive).",
    )
    limit: int | None = Field(
        default=None,
        description="Maximum number of lines to read.",
    )


class ReadFileResult(BaseModel):
    path: str
    content: str
    file_size_bytes: int
    returned_bytes: int
    offset: int = 0
    lines_read: int
    was_truncated: bool = False


@tool(
    name="read_file",
    description=(
        "Read a text file (encoding detected safely), returning content from a "
        "specific line range. Reading is capped by a byte limit for safety."
    ),
    input_schema=ReadFileArgs,
    result_schema=ReadFileResult,
)
def read_file(args: ReadFileArgs) -> ReadFileResult:
    path = args.path.strip()
    if not path:
        raise ValueError("Path cannot be empty")
    if args.offset < 0:
        raise ValueError("Offset cannot be negative")
    if args.limit is not None and args.limit <= 0:
        raise ValueError("Limit, if provided, must be a positive number")

    file_path = resolve_path(path)
    if not file_path.exists():
        raise ValueError(f"File not found at: {file_path}")
    if file_path.is_dir():
        raise ValueError(f"Path is a directory, not a file: {file_path}")
    try:
        file_size_bytes = file_path.stat().st_size
    except OSError as exc:
        raise ValueError(f"Error reading {file_path}: {exc}") from exc

    try:
        with file_path.open("rb") as handle:
            raw_prefix = handle.read(SNIFF_BYTES)
    except OSError as exc:
        raise ValueError(f"Error reading {file_path}: {exc}") from exc

    for encoding in candidate_encodings(raw_prefix):
        try:
            content, was_truncated = _read_content(
                file_path=file_path,
                encoding=encoding,
                offset=args.offset,
                limit=args.limit,
            )
            return ReadFileResult(
                path=str(file_path),
                content=content,
                file_size_bytes=file_size_bytes,
                returned_bytes=len(content.encode("utf-8")),
                offset=args.offset,
                lines_read=len(content.splitlines()),
                was_truncated=was_truncated,
            )
        except UnicodeDecodeError:
            continue
        except OSError as exc:
            raise ValueError(f"Error reading {file_path}: {exc}") from exc

    raise ValueError(f"Could not decode text file with supported encodings: {file_path}")


def _read_content(
    *,
    file_path: Path,
    encoding: str,
    offset: int,
    limit: int | None,
) -> tuple[str, bool]:
    parts: list[str] = []
    bytes_written = 0
    seen = 0
    yielded = 0

    with file_path.open("r", encoding=encoding, errors="strict", newline="") as handle:
        for line in handle:
            if seen < offset:
                seen += 1
                continue
            if limit is not None and yielded >= limit:
                break

            line_bytes = len(line.encode("utf-8"))
            if bytes_written + line_bytes <= MAX_READ_BYTES:
                parts.append(line)
                bytes_written += line_bytes
                yielded += 1
                continue

            truncated = line.encode("utf-8")[: MAX_READ_BYTES - bytes_written].decode(
                "utf-8", errors="ignore"
            )
            if truncated:
                parts.append(truncated)
            return "".join(parts), True

    return "".join(parts), False
