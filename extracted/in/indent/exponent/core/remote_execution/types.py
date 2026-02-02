import datetime
import json
from enum import Enum
from functools import cached_property
from os import PathLike
from pathlib import Path, PurePath
from typing import (
    Annotated,
    Any,
    Literal,
)

from anyio import Path as AsyncPath
from pydantic import BaseModel, Field

type FilePath = str | PathLike[str]


class CreateChatResponse(BaseModel):
    chat_uuid: str


class RunWorkflowRequest(BaseModel):
    chat_uuid: str
    workflow_id: str


# note: before adding fields here, probably update
# get_workflow_run_by_trigger db query
class PrReviewWorkflowInput(BaseModel):
    repo_owner: str
    repo_name: str
    pr_number: int
    branch: str | None = None
    banner_comment_id: int | None = None
    # PR metadata fields - populated from webhook payload
    pr_title: str | None = None
    pr_url: str | None = None
    pr_author: str | None = None
    pr_author_avatar_url: str | None = None
    pr_additions: int | None = None
    pr_deletions: int | None = None
    pr_changed_files: int | None = None
    head_sha: str | None = None


class SlackWorkflowInput(BaseModel):
    discriminator: Literal["slack_workflow"] = "slack_workflow"
    channel_id: str
    thread_ts: str
    slack_url: str | None = None
    channel_name: str | None = None
    message_ts: str | None = None
    message_text: str | None = None


class SlackPlanApprovalWorkflowInput(BaseModel):
    discriminator: Literal["slack_plan_approval"] = "slack_plan_approval"
    channel_id: str
    thread_ts: str
    slack_url: str
    channel_name: str
    message_ts: str


class LearnFromPrWorkflowInput(BaseModel):
    repo_owner: str
    repo_name: str
    pr_number: int


class SentryWorkflowInput(BaseModel):
    """Deprecated but kept for backcompat with existing DB rows."""

    title: str
    issue_id: str
    permalink: str


WorkflowInput = (
    PrReviewWorkflowInput
    | SlackWorkflowInput
    | SentryWorkflowInput
    | SlackPlanApprovalWorkflowInput
    | LearnFromPrWorkflowInput
)


class WorkflowTriggerRequest(BaseModel):
    workflow_name: str
    workflow_input: WorkflowInput


class WorkflowTriggerResponse(BaseModel):
    chat_uuid: str


class ExecutionEndResponse(BaseModel):
    execution_ended: bool


class SignalType(str, Enum):
    disconnect = "disconnect"

    def __str__(self) -> str:
        return self.value


class GitInfo(BaseModel):
    branch: str
    remote: str | None


class PythonEnvInfo(BaseModel):
    interpreter_path: str | None
    interpreter_version: str | None
    name: str | None = "exponent"
    provider: Literal["venv", "pyenv", "pipenv", "conda"] | None = "pyenv"


class PortInfo(BaseModel):
    process_name: str
    port: int
    protocol: str
    pid: int | None
    uptime_seconds: float | None


class SystemInfo(BaseModel):
    name: str
    cwd: str
    os: str
    shell: str
    git: GitInfo | None
    python_env: PythonEnvInfo | None
    port_usage: list[PortInfo] | None = None


class HeartbeatInfo(BaseModel):
    exponent_version: str | None = None
    editable_installation: bool = False
    system_info: SystemInfo | None
    timestamp: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )
    timestamp_received: datetime.datetime | None = None
    cli_uuid: str | None = None


class RemoteFile(BaseModel):
    file_path: str
    working_directory: str = "."

    @cached_property
    def pure_path(self) -> PurePath:
        return PurePath(self.working_directory, self.file_path)

    @cached_property
    def path(self) -> Path:
        return Path(self.working_directory, self.file_path)

    @cached_property
    def name(self) -> str:
        return self.pure_path.name

    @cached_property
    def absolute_path(self) -> str:
        return self.path.absolute().as_posix()

    async def resolve(self, client_working_directory: str) -> str:
        working_directory = AsyncPath(self.working_directory, self.file_path)

        if not working_directory.is_absolute():
            working_directory = AsyncPath(client_working_directory, working_directory)

        return str(await working_directory.resolve())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RemoteFile):
            return False

        return self.path.name == other.path.name

    def __lt__(self, other: "RemoteFile") -> bool:
        # Prefer shorter paths
        if (cmp := self._cmp_path_len(other)) is not None:
            return cmp

        # Prefer paths sorted by parent directory
        if (cmp := self._cmp_path_str(other)) is not None:
            return cmp

        # Prefer paths with alphabetical first character
        return self._cmp_first_char(other)

    def __hash__(self) -> int:
        return hash(self.absolute_path)

    def _cmp_first_char(self, other: "RemoteFile") -> bool:
        return self._cmp_str(self.path.name, other.path.name)

    def _cmp_path_len(self, other: "RemoteFile") -> bool | None:
        self_parts = self.path.absolute().parent.parts
        other_parts = other.path.absolute().parent.parts

        if len(self_parts) == len(other_parts):
            return None

        return len(self_parts) < len(other_parts)

    def _cmp_path_str(self, other: "RemoteFile") -> bool | None:
        self_parts = self.path.absolute().parent.parts
        other_parts = other.path.absolute().parent.parts

        if self_parts == other_parts:
            return None

        for a, b in zip(self_parts, other_parts):
            if a != b:
                return self._cmp_str(a, b)

        return False

    @staticmethod
    def _cmp_str(s1: str, s2: str) -> bool:
        if s1[:1].isalpha() == s2[:1].isalpha():
            return s1 < s2

        return s1[:1].isalpha()


class URLAttachment(BaseModel):
    attachment_type: Literal["url"] = "url"
    url: str
    content: str


class FileAttachment(BaseModel):
    attachment_type: Literal["file"] = "file"
    file: RemoteFile
    content: str
    truncated: bool = False


class TableSchemaAttachment(BaseModel):
    attachment_type: Literal["table_schema"] = "table_schema"
    table_name: str
    table_schema: dict[str, Any]


class PromptAttachment(BaseModel):
    attachment_type: Literal["prompt"] = "prompt"
    prompt_name: str
    prompt_content: str


class SQLAttachment(BaseModel):
    attachment_type: Literal["sql"] = "sql"
    query_content: str
    query_id: str


MessageAttachment = Annotated[
    FileAttachment
    | URLAttachment
    | TableSchemaAttachment
    | PromptAttachment
    | SQLAttachment,
    Field(discriminator="attachment_type"),
]


SupportedLanguage = Literal[
    "python",
    "shell",
]

SUPPORTED_LANGUAGES: list[SupportedLanguage] = ["python", "shell"]


class GitFileChange(BaseModel):
    path: str
    lines_added: int
    lines_deleted: int


class GitDiff(BaseModel):
    files: list[GitFileChange]
    truncated: bool = False  # True if there were more files than the limit
    total_files: int  # Total number of files changed, even if truncated


class GitCommitMetadata(BaseModel):
    author_name: str
    author_email: str
    author_date: str
    commit_date: str
    commit_message: str
    branch: str


class ChatMode(str, Enum):
    DEFAULT = "DEFAULT"  # chat just with model
    CLI = "CLI"
    CLOUD = "CLOUD"  # chat with cloud devbox
    CLOUD_SETUP = "CLOUD_SETUP"  # cloud environment setup
    CLOUD_SETUP_AUTO = "CLOUD_SETUP_AUTO"  # autonomous cloud environment setup
    CODEBASE = "CODEBASE"  # chat with codebase
    DATABASE = "DATABASE"  # chat with database connection
    WORKFLOW = "WORKFLOW"
    PLAYGROUND = "PLAYGROUND"  # playground mode with MCP tools only
    ONCALL = (
        "ONCALL"  # incident response mode with auto-configured Datadog/Sentry/Sandbox
    )

    @classmethod
    def requires_cli(cls, mode: "ChatMode") -> bool:
        return mode not in [
            cls.DATABASE,
            cls.CLOUD_SETUP,
            cls.CLOUD_SETUP_AUTO,
            cls.PLAYGROUND,
        ]


class ChatSource(str, Enum):
    CLI_SHELL = "CLI_SHELL"
    CLI_RUN = "CLI_RUN"
    WEB = "WEB"
    DESKTOP_APP = "DESKTOP_APP"
    VSCODE_EXTENSION = "VSCODE_EXTENSION"
    SLACK_APP = "SLACK_APP"
    SENTRY_APP = "SENTRY_APP"
    GITHUB_APP = "GITHUB_APP"


class AgentSubtype(str, Enum):
    CODING_AGENT = "CODING_AGENT"
    SRE_AGENT = "SRE_AGENT"


class CLIConnectedState(BaseModel):
    chat_uuid: str
    connected: bool
    last_connected_at: datetime.datetime | None
    connection_latency_ms: int | None
    system_info: SystemInfo | None
    exponent_version: str | None = None
    editable_installation: bool = False


class DevboxConnectedState(str, Enum):
    # The chat has been initialized, but the devbox is still loading
    DEVBOX_LOADING = "DEVBOX_LOADING"
    # CLI is connected and running on devbox
    CONNECTED = "CONNECTED"
    # Devbox has an error
    DEVBOX_ERROR = "DEVBOX_ERROR"
    # Devbox is going to idle
    PAUSING = "PAUSING"
    # Devbox has been paused and is not running
    PAUSED = "PAUSED"
    # Dev box is starting up. Sandbox exists but devbox is not running
    RESUMING = "RESUMING"


class CloudConnectedState(BaseModel):
    chat_uuid: str
    connected_state: DevboxConnectedState
    last_connected_at: datetime.datetime | None
    system_info: SystemInfo | None


class CLIErrorLog(BaseModel):
    event_data: str
    timestamp: datetime.datetime = datetime.datetime.now()
    attachment_data: str | None = None
    version: str | None = None
    chat_uuid: str | None = None

    @property
    def loaded_event_data(self) -> Any | None:
        try:
            return json.loads(self.event_data)
        except json.JSONDecodeError:
            return None

    @property
    def attachment_bytes(self) -> bytes | None:
        if not self.attachment_data:
            return None
        return self.attachment_data.encode()
