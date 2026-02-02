import base64
from typing import TYPE_CHECKING, Any

import msgspec
from pydantic_ai.format_prompt import format_as_xml

from exponent.core.remote_execution.file_reference import FilePath

if TYPE_CHECKING:
    from exponent_server.core.tools.edit_tool import (
        EditToolInput as ServerSideEditToolInput,
    )


class PartialToolResult(msgspec.Struct, tag_field="tool_name", omit_defaults=True):
    pass


class ToolInput(msgspec.Struct, tag_field="tool_name", omit_defaults=True):
    """Concrete subclasses describe the full input schema for a tool."""

    def to_llm(self) -> dict[str, Any]:
        """Convert ToolInput to LLM-friendly typed dict format.

        Returns a dictionary with the tool parameters, excluding the tool_name
        which is handled separately by the LLM integration layer.

        Returns:
            self by default, which msgspec will serialize appropriately.
        """
        return msgspec.to_builtins(self)

    def parallelism_key(self) -> str | None:
        """Return a key for parallelism control.

        Tools with the same non-None parallelism key will be executed serially,
        while tools with different keys (or None) can run in parallel.

        By default, returns None which means no parallelism restrictions.
        Subclasses can override this to implement custom parallelism behavior.

        Returns:
            A string key for grouping serial execution, or None for unrestricted parallelism.
        """
        return None


class ToolResult(msgspec.Struct, tag_field="tool_name", omit_defaults=True):
    """Concrete subclasses return data from a tool execution."""

    def to_text(self) -> str:
        """
        This provides a default textual representation of the tool result. Override it as needed for your tool."""
        d = msgspec.to_builtins(self)
        del d["tool_name"]
        return format_as_xml(d, include_root_tag=False, item_tag="item")


class ErrorToolResult(ToolResult, tag="error"):
    error_message: str
    is_assistant_error: bool = False


READ_TOOL_NAME = "read"
READ_TOOL_ARTIFACT_NAME = "read_tool_artifact"


class ReadToolInput(ToolInput, tag=READ_TOOL_NAME):
    file_path: FilePath
    offset: int | None = None
    limit: int | None = None


class FileMetadata(msgspec.Struct):
    modified_timestamp: float
    file_mode: str


class ReadToolArtifactResult(ToolResult, tag=READ_TOOL_ARTIFACT_NAME):
    s3_uri: str
    file_path: FilePath
    media_type: str

    def to_text(self) -> str:
        return f"[Image artifact uploaded to {self.s3_uri}]"

    async def get_base64_content(self, chat_uuid: str) -> str:
        """Download the artifact from S3 and return as base64-encoded string.

        Args:
            chat_uuid: The chat UUID for S3 client scoping

        Returns:
            Base64-encoded string of the file content
        """
        from exponent_server.core.services.s3_services.s3 import S3Client

        s3_client = S3Client(chat_uuid=chat_uuid)
        await s3_client.authenticate()

        s3_uri = self.s3_uri
        bucket_prefix = f"s3://{s3_client.bucket_name}/"
        if s3_uri.startswith(bucket_prefix):
            s3_key = s3_uri[len(bucket_prefix) :]
            chat_prefix = f"{chat_uuid}/"
            if s3_key.startswith(chat_prefix):
                s3_key = s3_key[len(chat_prefix) :]
        else:
            raise ValueError(
                f"S3 URI {s3_uri} does not match expected bucket prefix {bucket_prefix}"
            )

        file_bytes = await s3_client.get_object(s3_key)
        return base64.standard_b64encode(file_bytes).decode("utf-8")


class ReadToolResult(ToolResult, tag=READ_TOOL_NAME):
    content: str | None = None
    num_lines: int | None = None
    start_line: int | None = None
    total_lines: int | None = None
    metadata: FileMetadata | None = None
    artifact: ReadToolArtifactResult | None = None

    def to_text(self) -> str:
        if self.artifact:
            return self.artifact.to_text()
        assert self.content is not None
        assert self.start_line is not None

        metadata_attrs = []
        if self.total_lines is not None:
            metadata_attrs.append(f'total_lines="{self.total_lines}"')
        if self.metadata is not None:
            metadata_attrs.append(f'mtime="{self.metadata.modified_timestamp}"')
            metadata_attrs.append(f'mode="{self.metadata.file_mode}"')

        lines = self.content.splitlines()
        lines = [
            f"{str(i).rjust(6)}→{line}"
            for i, line in enumerate(lines, start=self.start_line + 1)
        ]

        if metadata_attrs:
            metadata_header = "<metadata " + " ".join(metadata_attrs) + " />"
            return metadata_header + "\n" + "\n".join(lines)
        return "\n".join(lines)


GLOB_TOOL_NAME = "glob"


class GlobToolInput(ToolInput, tag=GLOB_TOOL_NAME):
    pattern: str
    path: str | None = None


class GlobToolResult(ToolResult, tag=GLOB_TOOL_NAME):
    filenames: list[str]
    duration_ms: int
    num_files: int
    truncated: bool


WRITE_TOOL_NAME = "write"


class WriteToolInput(ToolInput, tag=WRITE_TOOL_NAME):
    file_path: FilePath
    content: str


class WriteToolResult(ToolResult, tag=WRITE_TOOL_NAME):
    message: str
    metadata: FileMetadata | None = None


GREP_TOOL_NAME = "grep"


class GrepToolInput(ToolInput, tag=GREP_TOOL_NAME):
    pattern: str
    path: str | None = None
    include: str | None = None
    multiline: bool | None = None


class GrepToolResult(ToolResult, tag=GREP_TOOL_NAME):
    matches: list[str]
    truncated: bool = False


EDIT_TOOL_NAME = "edit"


# This is only used in the CLI. The server side type is edit_tool.py
class EditToolInput(ToolInput, tag=EDIT_TOOL_NAME):
    file_path: FilePath
    old_string: str
    new_string: str
    replace_all: bool = False
    # When set, matches everything from old_string up to and including old_string_end.
    # Cannot be used with replace_all=True.
    old_string_end: str | None = None
    # The last retrieved modified timestamp. This is used to check if the file has been modified since the last read/write that we are aware of (in which case we should re-read the file before editing).
    last_known_modified_timestamp: float | None = None

    @classmethod
    def from_server_side_input(
        cls,
        server_side_input: "ServerSideEditToolInput",
        last_known_modified_timestamp: float | None,
    ) -> "EditToolInput":
        return cls(
            file_path=server_side_input.file_path,
            old_string=server_side_input.old_string,
            new_string=server_side_input.new_string,
            replace_all=server_side_input.replace_all,
            old_string_end=server_side_input.old_string_end,
            last_known_modified_timestamp=last_known_modified_timestamp,
        )


class EditToolResult(ToolResult, tag=EDIT_TOOL_NAME):
    message: str
    metadata: FileMetadata | None = None


BASH_TOOL_NAME = "bash"


class BashToolInput(ToolInput, tag=BASH_TOOL_NAME):
    command: str
    timeout: int | None = None
    description: str | None = None
    background: bool = False


class PartialBashToolResult(PartialToolResult, tag=BASH_TOOL_NAME):
    shell_output: str | None = None


class BashToolResult(ToolResult, tag=BASH_TOOL_NAME):
    shell_output: str
    duration_ms: int
    exit_code: int | None
    timed_out: bool
    stopped_by_user: bool
    pid: int | None = None
    output_file: str | None = None


DOWNLOAD_ARTIFACT_TOOL_NAME = "download_artifact"


class DownloadArtifactToolInput(ToolInput, tag=DOWNLOAD_ARTIFACT_TOOL_NAME):
    presigned_url: str
    file_path: FilePath
    artifact_id: str
    overwrite: bool = True


class DownloadArtifactToolResult(ToolResult, tag=DOWNLOAD_ARTIFACT_TOOL_NAME):
    file_path: FilePath
    artifact_id: str
    file_size_bytes: int
    content_preview: str | None = None
    num_lines: int | None = None
    total_lines: int | None = None
    truncated: bool = False


UPLOAD_ARTIFACT_TOOL_NAME = "upload_artifact"


class UploadArtifactToolInput(ToolInput, tag=UPLOAD_ARTIFACT_TOOL_NAME):
    presigned_url: str
    file_path: FilePath
    artifact_id: str
    content_type: str


class UploadArtifactToolResult(ToolResult, tag=UPLOAD_ARTIFACT_TOOL_NAME):
    artifact_id: str
    file_size_bytes: int
    content_type: str


class HttpRequest(msgspec.Struct, tag="http_fetch_cli"):
    url: str
    method: str = "GET"
    headers: dict[str, str] | None = None
    timeout: int | None = None


class HttpResponse(msgspec.Struct, tag="http_fetch_cli"):
    status_code: int | None = None
    content: str | None = None
    error_message: str | None = None
    duration_ms: int | None = None
    headers: dict[str, str] | None = None


ToolInputType = (
    ReadToolInput
    | WriteToolInput
    | GlobToolInput
    | GrepToolInput
    | EditToolInput
    | BashToolInput
    | DownloadArtifactToolInput
    | UploadArtifactToolInput
)
PartialToolResultType = PartialBashToolResult

ToolResultType = (
    ReadToolResult
    | ReadToolArtifactResult
    | WriteToolResult
    | GlobToolResult
    | GrepToolResult
    | EditToolResult
    | BashToolResult
    | DownloadArtifactToolResult
    | UploadArtifactToolResult
    | ErrorToolResult
)


class ToolExecutionRequest(msgspec.Struct, tag="tool_execution"):
    tool_input: ToolInputType


class GetAllFilesRequest(msgspec.Struct, tag="get_all_files"):
    pass


class TerminateRequest(msgspec.Struct, tag="terminate"):
    pass


class SwitchCLIChatRequest(msgspec.Struct, tag="switch_cli_chat"):
    new_chat_uuid: str


# This message is sent periodically from the client to keep the connection alive while the chat is turning.
# This synergizes with CLI-side timeouts to avoid disconnecting during long operations.
class KeepAliveCliChatRequest(msgspec.Struct, tag="keep_alive_cli_chat"):
    pass


class BatchToolExecutionRequest(msgspec.Struct, tag="batch_tool_execution"):
    tool_inputs: list[ToolInputType]


class GetAllFilesResponse(msgspec.Struct, tag="get_all_files"):
    files: list[str]


class TerminateResponse(msgspec.Struct, tag="terminate"):
    pass


class TimeoutResponse(msgspec.Struct, tag="timeout"):
    pass


class BatchToolExecutionResponse(msgspec.Struct, tag="batch_tool_execution"):
    tool_results: list[ToolResultType]


class SwitchCLIChatResponse(msgspec.Struct, tag="switch_cli_chat"):
    pass


class KeepAliveCliChatResponse(msgspec.Struct, tag="keep_alive_cli_chat"):
    pass


class GenerateUploadUrlRequest(msgspec.Struct, tag="generate_upload_url"):
    s3_key: str
    content_type: str


class GenerateUploadUrlResponse(msgspec.Struct, tag="generate_upload_url"):
    upload_url: str
    s3_uri: str


class DownloadFromUrlRequest(msgspec.Struct, tag="download_from_url"):
    """Request to download a file from a URL to the local filesystem."""

    url: str
    file_path: str
    timeout: int = 300


class DownloadFromUrlResponse(msgspec.Struct, tag="download_from_url"):
    """Response after downloading a file from a URL."""

    file_path: str
    file_size_bytes: int
    success: bool
    error_message: str | None = None


# Terminal session management
class StartTerminalRequest(msgspec.Struct, tag="start_terminal"):
    """Start a new terminal session with PTY"""

    session_id: str
    command: list[str] | None = None  # None = default shell, or specific command
    cols: int = 80
    rows: int = 24
    env: dict[str, str] | None = None  # Additional environment variables
    name: str | None = None  # Display name for the terminal


class StartTerminalResponse(msgspec.Struct, tag="start_terminal"):
    """Response after starting terminal"""

    session_id: str
    success: bool
    error_message: str | None = None
    name: str | None = None  # Display name for the terminal


# Terminal input (user typing)
class TerminalInputRequest(msgspec.Struct, tag="terminal_input"):
    """Send user input to terminal"""

    session_id: str
    data: str  # Raw input data from user


class TerminalInputResponse(msgspec.Struct, tag="terminal_input"):
    """Acknowledge input received"""

    session_id: str
    success: bool
    error_message: str | None = None


# Terminal resize
class TerminalResizeRequest(msgspec.Struct, tag="terminal_resize"):
    """Resize terminal dimensions"""

    session_id: str
    cols: int
    rows: int


class TerminalResizeResponse(msgspec.Struct, tag="terminal_resize"):
    """Acknowledge resize"""

    session_id: str
    success: bool
    error_message: str | None = None


# Terminal stop
class StopTerminalRequest(msgspec.Struct, tag="stop_terminal"):
    """Stop a terminal session"""

    session_id: str


class StopTerminalResponse(msgspec.Struct, tag="stop_terminal"):
    """Acknowledge terminal stopped"""

    session_id: str
    success: bool
    error_message: str | None = None


class StreamingCodeExecutionRequest(msgspec.Struct, tag="streaming_code_execution"):
    correlation_id: str
    language: str  # "python" or "shell"
    content: str
    timeout: int


class CliRpcRequest(msgspec.Struct):
    request_id: str
    request: (
        ToolExecutionRequest
        | GetAllFilesRequest
        | TerminateRequest
        | HttpRequest
        | BatchToolExecutionRequest
        | SwitchCLIChatRequest
        | KeepAliveCliChatRequest
        | GenerateUploadUrlRequest
        | DownloadFromUrlRequest
        | StartTerminalRequest
        | TerminalInputRequest
        | TerminalResizeRequest
        | StopTerminalRequest
        | StreamingCodeExecutionRequest
    )


class ToolExecutionResponse(msgspec.Struct, tag="tool_execution"):
    tool_result: ToolResultType


class ErrorResponse(msgspec.Struct, tag="error"):
    error_message: str


class StreamingCodeExecutionResponseChunk(
    msgspec.Struct, tag="streaming_code_execution_chunk"
):
    correlation_id: str
    content: str
    truncated: bool = False

    def add(
        self, new_chunk: "StreamingCodeExecutionResponseChunk"
    ) -> "StreamingCodeExecutionResponseChunk":
        """Aggregates content of this and a new chunk."""
        assert self.correlation_id == new_chunk.correlation_id
        return StreamingCodeExecutionResponseChunk(
            correlation_id=self.correlation_id,
            content=self.content + new_chunk.content,
            truncated=self.truncated or new_chunk.truncated,
        )


class StreamingCodeExecutionResponse(msgspec.Struct, tag="streaming_code_execution"):
    correlation_id: str
    content: str
    truncated: bool = False
    # Only present for shell code execution
    cancelled_for_timeout: bool = False
    exit_code: int | None = None
    halted: bool = False
    output_file: str | None = None


class StreamingErrorResponse(msgspec.Struct, tag="streaming_error"):
    correlation_id: str
    error_message: str


# WebSocket Authentication Messages
class AuthMessage(msgspec.Struct):
    """Authentication message sent over websocket."""

    api_key: str | None = None
    token: str | None = None


class AuthSuccessMessage(msgspec.Struct):
    """Authentication success response."""

    pass


class AuthFailedMessage(msgspec.Struct):
    """Authentication failure response."""

    reason: str


class BackgroundProcessCompletedNotification(
    msgspec.Struct, tag="background_process_completed"
):
    """Sent from CLI to server when a background bash process completes."""

    pid: int
    command: str
    exit_code: int
    output: str
    output_file: str
    correlation_id: str
    truncated: bool = False
    duration_ms: int | None = None


CliNotificationType = BackgroundProcessCompletedNotification


class CliRpcResponse(msgspec.Struct):
    request_id: str
    response: (
        ToolExecutionResponse
        | GetAllFilesResponse
        | ErrorResponse
        | TerminateResponse
        | TimeoutResponse
        | BatchToolExecutionResponse
        | HttpResponse
        | SwitchCLIChatResponse
        | KeepAliveCliChatResponse
        | GenerateUploadUrlResponse
        | DownloadFromUrlResponse
        | StartTerminalResponse
        | TerminalInputResponse
        | TerminalResizeResponse
        | StopTerminalResponse
        | StreamingCodeExecutionResponseChunk
        | StreamingCodeExecutionResponse
        | StreamingErrorResponse
    )
