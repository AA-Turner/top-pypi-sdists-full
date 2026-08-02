"""Builtin write_file tool for the Vibe SDK."""

from pydantic import BaseModel, Field

from mistralai.vibe.sdk.capabilities import tool
from mistralai.vibe.sdk.capabilities.utils import resolve_path

MAX_WRITE_BYTES = 64_000


class WriteFileArgs(BaseModel):
    path: str
    content: str
    overwrite: bool = Field(
        default=False,
        description="Set to true to overwrite an existing file.",
    )


class WriteFileResult(BaseModel):
    path: str
    bytes_written: int
    file_existed: bool


@tool(
    name="write_file",
    description="Create or overwrite a UTF-8 file. Fails if file exists unless 'overwrite=True'.",
    input_schema=WriteFileArgs,
    result_schema=WriteFileResult,
)
def write_file(args: WriteFileArgs) -> WriteFileResult:
    path = args.path.strip()
    if not path:
        raise ValueError("Path cannot be empty")

    content_bytes = args.content.encode("utf-8")
    if len(content_bytes) > MAX_WRITE_BYTES:
        raise ValueError(f"Content exceeds {MAX_WRITE_BYTES} bytes limit")

    file_path = resolve_path(path)
    if file_path.exists() and file_path.is_dir():
        raise ValueError(f"Path is a directory, not a file: {file_path}")

    file_existed = file_path.exists()
    if file_existed and not args.overwrite:
        raise ValueError(f"File '{file_path}' exists. Set overwrite=True to replace.")

    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with file_path.open("wb") as handle:
            handle.write(content_bytes)
    except OSError as exc:
        raise ValueError(f"Error writing {file_path}: {exc}") from exc

    return WriteFileResult(
        path=str(file_path),
        bytes_written=len(content_bytes),
        file_existed=file_existed,
    )
