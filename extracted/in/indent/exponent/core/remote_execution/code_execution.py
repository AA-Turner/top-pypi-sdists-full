from collections.abc import AsyncGenerator, Callable

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

EMPTY_OUTPUT_STRING = "(No output)"


def _truncate_shell_output(content: str, chat_uuid: str) -> tuple[str, bool, str | None]:
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

    truncation_msg = f"[Truncated to last {BASH_CHARACTER_LIMIT} characters.]\n"

    return truncation_msg + truncated_value, True, file_path


async def execute_code_streaming(
    request: StreamingCodeExecutionRequest,
    working_directory: str,
    should_halt: Callable[[], bool],
    chat_uuid: str,
) -> AsyncGenerator[StreamingCodeExecutionResponseChunk | StreamingCodeExecutionResponse, None]:
    if request.language == "shell":
        async for shell_output in execute_shell_streaming(
            request.content, working_directory, request.timeout, should_halt
        ):
            if isinstance(shell_output, StreamedOutputPiece):
                yield StreamingCodeExecutionResponseChunk(
                    content=shell_output.content, correlation_id=request.correlation_id
                )
            else:
                content = shell_output.output or EMPTY_OUTPUT_STRING
                truncated_content, was_truncated, output_file = _truncate_shell_output(content, chat_uuid)
                yield StreamingCodeExecutionResponse(
                    correlation_id=request.correlation_id,
                    content=truncated_content,
                    truncated=was_truncated,
                    halted=shell_output.halted,
                    exit_code=shell_output.exit_code,
                    cancelled_for_timeout=shell_output.cancelled_for_timeout,
                    output_file=output_file,
                )
