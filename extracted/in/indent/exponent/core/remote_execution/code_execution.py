from collections.abc import AsyncGenerator, Callable
from typing import TYPE_CHECKING

from exponent.core.remote_execution.cli_rpc_types import (
    StreamingCodeExecutionRequest,
    StreamingCodeExecutionResponse,
    StreamingCodeExecutionResponseChunk,
)
from exponent.core.remote_execution.languages.shell_streaming import (
    execute_shell_streaming,
)
from exponent.core.remote_execution.languages.types import StreamedOutputPiece
from exponent.core.remote_execution.truncation import (
    BASH_CHARACTER_LIMIT,
    _write_full_output_to_file,
)

if TYPE_CHECKING:
    from exponent.core.remote_execution.session import RemoteExecutionClientSession

EMPTY_OUTPUT_STRING = "(No output)"


def _truncate_shell_output(
    content: str, chat_uuid: str
) -> tuple[str, bool, str | None]:
    """Write shell output to disk and truncate if needed.

    Returns:
        Tuple of (content, was_truncated, output_file_path)
    """
    file_path = _write_full_output_to_file(content, chat_uuid)

    if len(content) <= BASH_CHARACTER_LIMIT:
        return content, False, file_path

    truncated_value = content[-BASH_CHARACTER_LIMIT:]
    newline_pos = truncated_value.find("\n")
    if newline_pos != -1 and newline_pos < 1000:
        truncated_value = truncated_value[newline_pos + 1 :]

    if file_path:
        truncation_msg = f"[Truncated to last {BASH_CHARACTER_LIMIT} characters. Full output written to: {file_path}]\n"
    else:
        truncation_msg = f"[Truncated to last {BASH_CHARACTER_LIMIT} characters.]\n"

    return truncation_msg + truncated_value, True, file_path


async def execute_code_streaming(
    request: StreamingCodeExecutionRequest,
    session: "RemoteExecutionClientSession | None",
    working_directory: str,
    should_halt: Callable[[], bool] | None = None,
    chat_uuid: str | None = None,
) -> AsyncGenerator[
    StreamingCodeExecutionResponseChunk | StreamingCodeExecutionResponse, None
]:
    """Execute code and stream output.

    Shell output is truncated to BASH_CHARACTER_LIMIT (8k chars) with full output
    written to a temp file.

    Args:
        request: The streaming code execution request.
        session: The session (required for Python, optional for shell).
        working_directory: The working directory for code execution.
        should_halt: Optional callback to check if execution should halt.
        chat_uuid: Optional chat UUID for output file storage (used if session is None).
    """
    if request.language == "python":
        if session is None:
            raise ValueError("Session is required for Python execution")

        from exponent.core.remote_execution.languages.python_execution import (
            execute_python_streaming,
        )

        async for output in execute_python_streaming(
            request.content, session.kernel, user_interrupted=should_halt
        ):
            if isinstance(output, StreamedOutputPiece):
                yield StreamingCodeExecutionResponseChunk(
                    content=output.content, correlation_id=request.correlation_id
                )
            else:
                yield StreamingCodeExecutionResponse(
                    correlation_id=request.correlation_id,
                    content=output.output or EMPTY_OUTPUT_STRING,
                    halted=output.halted,
                )

    elif request.language == "shell":
        async for shell_output in execute_shell_streaming(
            request.content, working_directory, request.timeout, should_halt
        ):
            if isinstance(shell_output, StreamedOutputPiece):
                yield StreamingCodeExecutionResponseChunk(
                    content=shell_output.content, correlation_id=request.correlation_id
                )
            else:
                content = shell_output.output or EMPTY_OUTPUT_STRING
                output_file: str | None = None
                effective_chat_uuid = chat_uuid or (
                    session.chat_uuid if session else None
                )
                if effective_chat_uuid:
                    truncated_content, was_truncated, output_file = (
                        _truncate_shell_output(content, effective_chat_uuid)
                    )
                elif len(content) > BASH_CHARACTER_LIMIT:
                    truncated_content = content[-BASH_CHARACTER_LIMIT:]
                    was_truncated = True
                else:
                    truncated_content, was_truncated = content, False
                yield StreamingCodeExecutionResponse(
                    correlation_id=request.correlation_id,
                    content=truncated_content,
                    truncated=was_truncated,
                    halted=shell_output.halted,
                    exit_code=shell_output.exit_code,
                    cancelled_for_timeout=shell_output.cancelled_for_timeout,
                    output_file=output_file,
                )
