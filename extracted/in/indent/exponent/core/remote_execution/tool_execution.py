import asyncio
import logging
import os
import shutil
import tempfile
import urllib.request
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from time import time
from typing import TYPE_CHECKING

import aiohttp
from anyio import Path as AsyncPath

from exponent.core.config import get_chat_artifacts_dir
from exponent.core.remote_execution import files
from exponent.core.remote_execution.cli_rpc_types import (
    BashToolInput,
    BashToolResult,
    DownloadArtifactToolInput,
    DownloadArtifactToolResult,
    EditToolInput,
    EditToolResult,
    ErrorToolResult,
    GlobToolInput,
    GlobToolResult,
    GrepToolInput,
    GrepToolResult,
    ReadToolArtifactResult,
    ReadToolInput,
    ReadToolResult,
    StreamingCodeExecutionRequest,
    StreamingCodeExecutionResponse,
    ToolInputType,
    ToolResultType,
    UploadArtifactToolInput,
    UploadArtifactToolResult,
    WriteToolInput,
    WriteToolResult,
)
from exponent.core.remote_execution.code_execution import (
    execute_code_streaming,
)
from exponent.core.remote_execution.default_env import get_process_env
from exponent.core.remote_execution.file_write import execute_full_file_rewrite
from exponent.core.remote_execution.languages.shell_streaming import (
    get_rc_file_source_command,
)
from exponent.core.remote_execution.truncation import truncate_tool_result
from exponent.core.remote_execution.utils import (
    assert_unreachable,
    safe_get_file_metadata,
    safe_read_file,
)

if TYPE_CHECKING:
    from exponent.core.remote_execution.client import RemoteExecutionClient

logger = logging.getLogger(__name__)


@dataclass
class BackgroundBashResult:
    """Result from spawning a background bash process.

    Contains both the tool result to return to the caller and the process
    object for tracking completion.
    """

    result: BashToolResult
    process: asyncio.subprocess.Process


async def execute_tool(
    tool_input: ToolInputType,
    working_directory: str,
    upload_client: "RemoteExecutionClient | None" = None,
) -> ToolResultType:
    if isinstance(tool_input, ReadToolInput):
        return await execute_read_file(tool_input, working_directory, upload_client)
    elif isinstance(tool_input, WriteToolInput):
        return await execute_write_file(tool_input, working_directory)
    elif isinstance(tool_input, GlobToolInput):
        return await execute_glob_files(tool_input, working_directory)
    elif isinstance(tool_input, GrepToolInput):
        return await execute_grep_files(tool_input, working_directory)
    elif isinstance(tool_input, EditToolInput):
        return await execute_edit_file(tool_input, working_directory)
    elif isinstance(tool_input, DownloadArtifactToolInput):
        return await execute_download_artifact(tool_input, working_directory)
    elif isinstance(tool_input, UploadArtifactToolInput):
        return await execute_upload_artifact(tool_input, working_directory)
    elif isinstance(tool_input, BashToolInput):
        raise ValueError("Bash tool input should be handled by execute_bash_tool")
    else:
        assert_unreachable(tool_input)


def truncate_result[T: ToolResultType](tool_result: T, chat_uuid: str) -> T:
    return truncate_tool_result(tool_result, chat_uuid)


def is_image_file(file_path: str) -> tuple[bool, str | None]:
    ext = Path(file_path).suffix.lower()
    if ext == ".png":
        return (True, "image/png")
    elif ext in [".jpg", ".jpeg"]:
        return (True, "image/jpeg")
    return (False, None)


async def execute_read_file(  # noqa: PLR0911
    tool_input: ReadToolInput,
    working_directory: str,
    upload_client: "RemoteExecutionClient | None" = None,
) -> ReadToolResult | ErrorToolResult:
    # Validate absolute path requirement
    if not tool_input.file_path.startswith("/"):
        return ErrorToolResult(
            error_message=f"File path must be absolute, got relative path: {tool_input.file_path}"
        )

    # Validate offset and limit
    offset = tool_input.offset if tool_input.offset is not None else 0
    limit = tool_input.limit if tool_input.limit is not None else 2000

    if limit <= 0:
        return ErrorToolResult(error_message=f"Limit must be positive, got: {limit}")

    file = AsyncPath(working_directory, tool_input.file_path)

    # Check if this is an image file and we have an upload client
    is_image, media_type = is_image_file(tool_input.file_path)
    if is_image and media_type and upload_client is not None:
        try:
            file_name = Path(tool_input.file_path).name
            s3_key = f"images/{uuid.uuid4()}/{file_name}"

            upload_response = await upload_client.request_upload_url(s3_key, media_type)

            f = await file.open("rb")
            async with f:
                file_data = await f.read()

                def _upload() -> int:
                    req = urllib.request.Request(
                        upload_response.upload_url,
                        data=file_data,
                        headers={"Content-Type": media_type},
                        method="PUT",
                    )
                    with urllib.request.urlopen(req) as resp:
                        status: int = resp.status
                        return status

                status = await asyncio.to_thread(_upload)
                if status != 200:
                    raise RuntimeError(f"Upload failed with status {status}")

            return ReadToolResult(
                artifact=ReadToolArtifactResult(
                    s3_uri=upload_response.s3_uri,
                    file_path=tool_input.file_path,
                    media_type=media_type,
                )
            )
        except Exception as e:
            return ErrorToolResult(error_message=f"Failed to upload image to S3: {e!s}")

    try:
        exists = await file.exists()
    except (OSError, PermissionError) as e:
        return ErrorToolResult(error_message=f"Cannot access file: {e!s}")

    if not exists:
        return ErrorToolResult(
            error_message="File not found",
        )

    try:
        if await file.is_dir():
            return ErrorToolResult(
                error_message=f"{await file.absolute()} is a directory",
            )
    except (OSError, PermissionError) as e:
        return ErrorToolResult(error_message=f"Cannot check file type: {e!s}")

    try:
        content = await safe_read_file(file)
    except PermissionError:
        return ErrorToolResult(
            error_message=f"Permission denied: cannot read {tool_input.file_path}"
        )
    except UnicodeDecodeError:
        return ErrorToolResult(
            error_message="File appears to be binary or has invalid text encoding"
        )
    except Exception as e:
        return ErrorToolResult(error_message=f"Error reading file: {e!s}")

    metadata = await safe_get_file_metadata(file)

    # Handle empty files
    if not content:
        return ReadToolResult(
            content="",
            num_lines=0,
            start_line=0,
            total_lines=0,
            metadata=metadata,
        )

    content_lines = content.splitlines(keepends=True)
    total_lines = len(content_lines)

    # Handle offset beyond file length for positive offsets
    if offset >= 0 and offset >= total_lines:
        return ReadToolResult(
            content="",
            num_lines=0,
            start_line=offset,
            total_lines=total_lines,
            metadata=metadata,
        )

    # Use Python's native slicing - it handles negative offsets naturally
    # Handle the case where offset + limit < 0 (can't mix negative and non-negative indices)
    if offset < 0 and offset + limit < 0:
        # Both start and end are negative, use negative end index
        end_index = offset + limit
    elif offset < 0 and offset + limit >= 0:
        # Start is negative but end would be positive/zero, slice to end
        end_index = None
    else:
        # Normal case: both indices are non-negative
        end_index = offset + limit

    content_lines = content_lines[offset:end_index]

    # Calculate the actual start line for the result
    if offset < 0:
        # For negative offsets, calculate where we actually started
        actual_start_line = max(0, total_lines + offset)
    else:
        actual_start_line = offset

    # Apply character-level truncation at line boundaries to ensure consistency
    # This ensures the content field and num_lines field remain in sync
    # This is the primary truncation point for ReadToolResult - truncation.py
    # also has a fallback but this handles line-count synchronization
    CHARACTER_LIMIT = 20_000  # Match DEFAULT_CHARACTER_LIMIT in truncation.py

    # Join lines and check total size
    final_content = "".join(content_lines)

    if len(final_content) > CHARACTER_LIMIT:
        # Truncate at line boundaries to stay under the limit
        truncated_lines: list[str] = []
        current_size = 0
        truncation_message = "\n[Content truncated due to size limit]"
        truncation_size = len(truncation_message)
        lines_included = 0

        for line in content_lines:
            # Check if adding this line would exceed the limit (accounting for truncation message)
            if current_size + len(line) + truncation_size > CHARACTER_LIMIT:
                final_content = "".join(truncated_lines) + truncation_message
                break
            truncated_lines.append(line)
            current_size += len(line)
            lines_included += 1
        else:
            # All lines fit (shouldn't happen if we got here, but be safe)
            final_content = "".join(truncated_lines)
            lines_included = len(content_lines)

        num_lines = lines_included
    else:
        num_lines = len(content_lines)

    return ReadToolResult(
        content=final_content,
        num_lines=num_lines,
        start_line=actual_start_line,
        total_lines=total_lines,
        metadata=metadata,
    )


async def execute_write_file(
    tool_input: WriteToolInput, working_directory: str
) -> WriteToolResult:
    file_path = tool_input.file_path
    path = Path(working_directory, file_path)
    result = await execute_full_file_rewrite(
        path, tool_input.content, working_directory
    )
    return WriteToolResult(message=result)


async def execute_edit_file(  # noqa: PLR0911
    tool_input: EditToolInput, working_directory: str
) -> EditToolResult | ErrorToolResult:
    # Validate absolute path requirement
    if not tool_input.file_path.startswith("/"):
        return ErrorToolResult(
            error_message=f"File path must be absolute, got relative path: {tool_input.file_path}"
        )

    file = AsyncPath(working_directory, tool_input.file_path)

    try:
        exists = await file.exists()
    except (OSError, PermissionError) as e:
        return ErrorToolResult(error_message=f"Cannot access file: {e!s}")

    if not exists:
        return ErrorToolResult(error_message="File not found")

    if tool_input.last_known_modified_timestamp is not None:
        metadata = await safe_get_file_metadata(file)
        if (
            metadata is not None
            and metadata.modified_timestamp > tool_input.last_known_modified_timestamp
        ):
            return ErrorToolResult(
                error_message="File has been modified since last read/write"
            )

    try:
        if await file.is_dir():
            return ErrorToolResult(
                error_message=f"{await file.absolute()} is a directory"
            )
    except (OSError, PermissionError) as e:
        return ErrorToolResult(error_message=f"Cannot check file type: {e!s}")

    try:
        # Read the entire file without truncation limits
        content = await safe_read_file(file)
    except PermissionError:
        return ErrorToolResult(
            error_message=f"Permission denied: cannot read {tool_input.file_path}"
        )
    except UnicodeDecodeError:
        return ErrorToolResult(
            error_message="File appears to be binary or has invalid text encoding"
        )
    except Exception as e:
        return ErrorToolResult(error_message=f"Error reading file: {e!s}")

    # Check if search text exists
    if tool_input.old_string not in content:
        return ErrorToolResult(
            error_message=f"Search text not found in {tool_input.file_path}"
        )

    # Handle `old_string_end` parameter for range-based replacement (inclusive)
    if tool_input.old_string_end is not None:
        if tool_input.replace_all:
            return ErrorToolResult(
                error_message="Cannot use 'old_string_end' with 'replace_all=True'"
            )

        # Both old_string and old_string_end must be unique
        old_string_occurrences = content.count(tool_input.old_string)
        if old_string_occurrences > 1:
            return ErrorToolResult(
                error_message=f"String '{tool_input.old_string}' appears {old_string_occurrences} times in file. Use a more specific start marker."
            )

        end_occurrences = content.count(tool_input.old_string_end)
        if end_occurrences > 1:
            return ErrorToolResult(
                error_message="Multiple matches for 'old_string_end'. Use a more specific end marker."
            )

        start_idx = content.find(tool_input.old_string)
        if start_idx == -1:
            return ErrorToolResult(
                error_message=f"'old_string' text not found in {tool_input.file_path}"
            )

        search_after_start = start_idx + len(tool_input.old_string)
        until_idx = content.find(tool_input.old_string_end, search_after_start)
        if until_idx == -1:
            return ErrorToolResult(
                error_message=f"'old_string_end' text not found after 'old_string' in {tool_input.file_path}"
            )

        end_idx = until_idx + len(tool_input.old_string_end)

        old_text = content[start_idx:end_idx]
        if old_text == tool_input.new_string:
            return ErrorToolResult(
                error_message="Old string and new string are identical"
            )

        new_content = content[:start_idx] + tool_input.new_string + content[end_idx:]
        replaced_old_lines = old_text.count("\n") + 1
        replaced_new_lines = tool_input.new_string.count("\n") + 1
    else:
        # Standard replacement logic
        if tool_input.old_string == tool_input.new_string:
            return ErrorToolResult(
                error_message="Old string and new string are identical"
            )

        if not tool_input.replace_all:
            occurrences = content.count(tool_input.old_string)
            if occurrences > 1:
                return ErrorToolResult(
                    error_message=f"String '{tool_input.old_string}' appears {occurrences} times in file. Use a larger context or replace_all=True"
                )

        if tool_input.replace_all:
            new_content = content.replace(tool_input.old_string, tool_input.new_string)
        else:
            new_content = content.replace(
                tool_input.old_string, tool_input.new_string, 1
            )
        replaced_old_lines = tool_input.old_string.count("\n") + 1
        replaced_new_lines = tool_input.new_string.count("\n") + 1

    # Write back to file
    try:
        path = Path(working_directory, tool_input.file_path)
        await execute_full_file_rewrite(path, new_content, working_directory)
        return EditToolResult(
            message=f"Replaced {replaced_old_lines} lines with {replaced_new_lines} lines in {tool_input.file_path}",
            metadata=await safe_get_file_metadata(path),
        )
    except Exception as e:
        return ErrorToolResult(error_message=f"Error writing file: {e!s}")


async def execute_glob_files(
    tool_input: GlobToolInput, working_directory: str
) -> GlobToolResult:
    # async timer
    start_time = time()
    results = await files.glob(
        path=working_directory if tool_input.path is None else tool_input.path,
        glob_pattern=tool_input.pattern,
    )
    duration_ms = int((time() - start_time) * 1000)
    return GlobToolResult(
        filenames=results,
        duration_ms=duration_ms,
        num_files=len(results),
        truncated=len(results) >= files.GLOB_MAX_COUNT,
    )


async def execute_grep_files(
    tool_input: GrepToolInput, working_directory: str
) -> GrepToolResult | ErrorToolResult:
    return await files.search_files(
        path_str=working_directory if tool_input.path is None else tool_input.path,
        file_pattern=tool_input.include,
        regex=tool_input.pattern,
        working_directory=working_directory,
        multiline=tool_input.multiline,
    )


async def execute_bash_tool(
    tool_input: BashToolInput,
    working_directory: str,
    should_halt: Callable[[], bool],
    chat_uuid: str,
) -> BashToolResult | BackgroundBashResult:
    """Execute a bash command.

    For background commands, returns BackgroundBashResult containing both the result
    and the process object for tracking. For foreground commands, returns BashToolResult.
    """
    if tool_input.background:
        return await execute_bash_tool_background(
            tool_input, working_directory, chat_uuid
        )

    start_time = time()
    result = None
    async for result in execute_code_streaming(
        StreamingCodeExecutionRequest(
            language="shell",
            content=tool_input.command,
            timeout=120 if tool_input.timeout is None else tool_input.timeout,
            correlation_id=str(uuid.uuid4()),
        ),
        session=None,
        working_directory=working_directory,
        should_halt=should_halt,
        chat_uuid=chat_uuid,
    ):
        pass

    assert isinstance(result, StreamingCodeExecutionResponse)

    return BashToolResult(
        shell_output=result.content,
        exit_code=result.exit_code,
        duration_ms=int((time() - start_time) * 1000),
        timed_out=result.cancelled_for_timeout,
        stopped_by_user=result.halted,
    )


async def execute_bash_tool_background(
    tool_input: BashToolInput, working_directory: str, chat_uuid: str
) -> BackgroundBashResult:
    """Execute a bash command in the background, returning immediately with PID and output file.

    The command is spawned as a detached process with stdout/stderr redirected to a temp file.
    Output is streamed to the file in real-time, so it can be read while the process runs.

    Log files are written to the per-chat artifacts directory (~/.indent/chats/{uuid}/).

    Returns a BackgroundBashResult containing both the tool result and the process object
    for tracking completion.
    """
    start_time = time()

    artifacts_dir = get_chat_artifacts_dir(chat_uuid)
    os.makedirs(artifacts_dir, exist_ok=True)

    fd, output_file = tempfile.mkstemp(prefix="bg_", suffix=".log", dir=artifacts_dir)
    os.close(fd)

    shell_path = os.environ.get("SHELL") or shutil.which("bash") or shutil.which("sh")
    if not shell_path:
        shell_path = "/bin/sh"

    rc_source_cmd = get_rc_file_source_command(shell_path)
    full_command = f"{rc_source_cmd}{tool_input.command}"

    output_fd = os.open(output_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)

    try:
        process = await asyncio.create_subprocess_exec(
            shell_path,
            "-l",
            "-c",
            full_command,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=output_fd,
            stderr=output_fd,
            cwd=working_directory,
            env=get_process_env(None),
            start_new_session=True,
        )
    finally:
        os.close(output_fd)

    result = BashToolResult(
        shell_output=f"Background process started. Output is being written to: {output_file}",
        duration_ms=int((time() - start_time) * 1000),
        exit_code=None,
        timed_out=False,
        stopped_by_user=False,
        pid=process.pid,
        output_file=output_file,
    )

    return BackgroundBashResult(result=result, process=process)


async def execute_download_artifact(
    tool_input: DownloadArtifactToolInput, working_directory: str
) -> DownloadArtifactToolResult | ErrorToolResult:
    """Download an artifact from S3 using a pre-signed URL."""

    if not tool_input.file_path.startswith("/"):
        return ErrorToolResult(
            error_message=f"File path must be absolute, got relative path: {tool_input.file_path}"
        )

    file_path = Path(tool_input.file_path)
    if file_path.exists() and not tool_input.overwrite:
        return ErrorToolResult(
            error_message=f"File already exists: {tool_input.file_path}. Set overwrite=True to replace it."
        )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(tool_input.presigned_url) as response:
                if response.status != 200:
                    error_text = await response.text()
                    return ErrorToolResult(
                        error_message=f"Failed to download artifact: HTTP {response.status} - {error_text}"
                    )

                file_path.parent.mkdir(parents=True, exist_ok=True)

                content = await response.read()
                file_path.write_bytes(content)

        file_size = len(content)

        content_preview = None
        num_lines = None
        total_lines = None
        truncated = False

        try:
            text_content = content.decode("utf-8")
            lines = text_content.splitlines()
            total_lines = len(lines)

            preview_limit = 50
            if len(lines) > preview_limit:
                preview_lines = lines[:preview_limit]
                truncated = True
                num_lines = preview_limit
            else:
                preview_lines = lines
                num_lines = len(lines)

            content_preview = "\n".join(preview_lines)
        except UnicodeDecodeError:
            pass

        return DownloadArtifactToolResult(
            file_path=tool_input.file_path,
            artifact_id=tool_input.artifact_id,
            file_size_bytes=file_size,
            content_preview=content_preview,
            num_lines=num_lines,
            total_lines=total_lines,
            truncated=truncated,
        )

    except Exception as e:
        logger.exception("Failed to download artifact")
        return ErrorToolResult(error_message=f"Failed to download artifact: {e!s}")


async def execute_upload_artifact(
    tool_input: UploadArtifactToolInput, working_directory: str
) -> UploadArtifactToolResult | ErrorToolResult:
    """Upload an artifact to S3 using a pre-signed URL."""

    if not tool_input.file_path.startswith("/"):
        return ErrorToolResult(
            error_message=f"File path must be absolute, got relative path: {tool_input.file_path}"
        )

    file_path = Path(tool_input.file_path)
    if not file_path.exists():
        return ErrorToolResult(error_message=f"File not found: {tool_input.file_path}")

    if not file_path.is_file():
        return ErrorToolResult(
            error_message=f"Path is not a file: {tool_input.file_path}"
        )

    try:
        content = file_path.read_bytes()
        file_size = len(content)

        async with aiohttp.ClientSession() as session:
            headers = {"Content-Type": tool_input.content_type}
            async with session.put(
                tool_input.presigned_url, data=content, headers=headers
            ) as response:
                if response.status not in (200, 204):
                    error_text = await response.text()
                    return ErrorToolResult(
                        error_message=f"Failed to upload artifact: HTTP {response.status} - {error_text}"
                    )

        return UploadArtifactToolResult(
            artifact_id=tool_input.artifact_id,
            file_size_bytes=file_size,
            content_type=tool_input.content_type,
        )

    except Exception as e:
        logger.exception("Failed to upload artifact")
        return ErrorToolResult(error_message=f"Failed to upload artifact: {e!s}")
