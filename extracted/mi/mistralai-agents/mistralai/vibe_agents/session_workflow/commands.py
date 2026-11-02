"""Command types sent into a running session workflow via submit_command.

The public workflow input surface collapses to one generic command signal.
Provider-specific signals (GitHub PR events, Slack thread events, ...) stay
runtime-private, fed by routers and subscriber mixins. The control plane
only sees normalized SessionWorkflowCommand.
"""

import base64
import binascii
import re
from collections.abc import Sequence
from enum import StrEnum
from typing import TYPE_CHECKING, Annotated, Any, Final, Generic, Literal, Self
from urllib.parse import quote
from uuid import UUID

import structlog
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    JsonValue,
    StrictBool,
    StrictStr,
    ValidationError,
    field_validator,
)
from typing_extensions import TypeVar

from mistralai.vibe_agents.session_workflow.toolsets import ToolsetInput

if TYPE_CHECKING:
    # Type-only: plain installs of this package import it without the Harness.
    from mistralai.vibe.harness.session_v1_wire import ContentBlock

type TeleportContextEntrypoint = Literal["cli", "acp", "programmatic", "unknown"]

# The standard reasoning settings, plus OpenAI's names for off (none) and low (minimal).
ReasoningEffort = Literal["off", "none", "minimal", "low", "medium", "high", "xhigh", "max"]

logger = structlog.get_logger(__name__)

type JsonObject = dict[str, JsonValue]
IntegrationEventBodyT = TypeVar("IntegrationEventBodyT", default=JsonObject)


class MessagePartText(BaseModel):
    type: Literal["text"] = "text"
    text: str


_BASE64_MARKER = ";base64,"
_HTTP_URL_SAFE_CHARACTERS = ":/?#[]@!$&'()*+,;=%"
_INVALID_PERCENT_ESCAPE_PATTERN = re.compile(r"%(?![0-9A-Fa-f]{2})")
_MIME_ATOM_PATTERN = r"[!#$%&'*+\-.^_`|~0-9A-Za-z]+"
_IMAGE_MEDIA_TYPE_PATTERN = re.compile(
    rf"image/{_MIME_ATOM_PATTERN}(?:;{_MIME_ATOM_PATTERN}="
    rf'(?:{_MIME_ATOM_PATTERN}|"(?:[^"\\\r\n]|\\.)*"))*'
)


def _validate_image_data_uri(value: str) -> str:
    prefix, separator, body = value.partition(_BASE64_MARKER)
    media_type = prefix.removeprefix("data:")
    if not separator or _IMAGE_MEDIA_TYPE_PATTERN.fullmatch(media_type) is None:
        raise ValueError("image data URIs must have the form data:image/<type>;base64,<data>")
    if not body:
        raise ValueError("image data URI has an empty base64 body")
    try:
        base64.b64decode(body, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError("image data URI has a malformed base64 body") from exc
    return value


def validate_image_url(value: str) -> str:
    """Accept an http(s) URL or a base64 ``data:image/*`` URI; reject anything else.

    A ``data:`` value is validated as an image data URI (targeting a clear error
    for non-image or malformed payloads); any other value is validated as an
    http(s) URL via ``HttpUrl``.
    """
    if value.startswith("data:"):
        return _validate_image_data_uri(value)
    value = value.strip()
    if quote(value, safe=_HTTP_URL_SAFE_CHARACTERS) != value or _INVALID_PERCENT_ESCAPE_PATTERN.search(value):
        raise ValueError("HTTP image URLs must not require escaping")
    HttpUrl(value)
    return value


class MessagePartImage(BaseModel):
    type: Literal["image"] = "image"
    image_url: str

    @field_validator("image_url")
    @classmethod
    def _validate_image_url(cls, value: str) -> str:
        return validate_image_url(value)


class MessagePartResourceLink(BaseModel):
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    type: Literal["resource_link"] = "resource_link"
    uri: str
    name: str | None = None
    mime_type: str | None = Field(default=None, alias="mimeType")
    annotations: JsonObject | None = None


class MessagePartForm(BaseModel):
    type: Literal["form"] = "form"
    form_id: str
    values: dict[str, Any] = Field(default_factory=dict)


MessagePart = Annotated[
    MessagePartText | MessagePartImage | MessagePartResourceLink | MessagePartForm,
    Field(discriminator="type"),
]


MESSAGE_CONTEXT_MAX_LENGTH = 8_000


class _WireModel(BaseModel):
    """Accept both camelCase wire aliases and Python field names."""

    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)


class TeleportMessageContextSource(_WireModel):
    type: Literal["teleport"] = "teleport"
    entrypoint: TeleportContextEntrypoint = "unknown"
    client_name: str | None = Field(default=None, alias="clientName")


class McpAppMessageContextEntry(_WireModel):
    tool_call_id: str = Field(min_length=1, alias="toolCallId")
    tool_name: str = Field(min_length=1, alias="toolName")
    app_name: str = Field(min_length=1, alias="appName")
    resource_uri: str = Field(min_length=6, pattern=r"^ui://", alias="resourceUri")
    integration_id: str | None = Field(default=None, min_length=1, alias="integrationId")


class McpAppMessageContextSource(BaseModel):
    type: Literal["mcp_app"] = "mcp_app"
    apps: list[McpAppMessageContextEntry] = Field(min_length=1, max_length=32)


type MessageContextSource = Annotated[
    TeleportMessageContextSource | McpAppMessageContextSource,
    Field(discriminator="type"),
]


class MessageContext(BaseModel):
    summary: str = Field(min_length=1, max_length=MESSAGE_CONTEXT_MAX_LENGTH)
    source: MessageContextSource | None = None


class CommandObservability(BaseModel):
    dora_tracing_enabled: StrictBool
    conversation_id: str | None = Field(
        default=None,
        min_length=1,
        max_length=128,
        exclude_if=lambda value: value is None,
    )
    traceparent: StrictStr | None = None
    tracestate: StrictStr | None = None

    @field_validator("traceparent", mode="before")
    @classmethod
    def _discard_invalid_traceparent(cls, value: object) -> str | None:
        if not isinstance(value, str):
            return None
        match = re.fullmatch(r"00-([0-9a-f]{32})-([0-9a-f]{16})-[0-9a-f]{2}", value)
        if match is None or match.group(1) == "0" * 32 or match.group(2) == "0" * 16:
            return None
        return value

    @field_validator("tracestate", mode="before")
    @classmethod
    def _discard_invalid_tracestate(cls, value: object) -> str | None:
        if not isinstance(value, str) or not value or len(value) > 512:
            return None
        return value if value.isascii() and value.isprintable() else None


class CommandMetadata(BaseModel):
    idempotency_key: str | None = None
    correlation_id: str | None = None
    observability: CommandObservability | None = None

    @field_validator("observability", mode="before")
    @classmethod
    def _ignore_malformed_observability(cls, value: object) -> object:
        if value is None or isinstance(value, CommandObservability):
            return value
        try:
            return CommandObservability.model_validate(value)
        except ValidationError:
            return None


class MessageInput(BaseModel):
    role: Literal["user"] = "user"
    parts: list[MessagePart]

    @classmethod
    def from_content(cls, content: Sequence["ContentBlock"]) -> Self:
        """Translate Harness content blocks into Workflow message parts.

        A bridge for the remote transport, whose Turn start and steer still send ``type=message``
        in the Nuage message shape.

        Raises ``TypeError`` for a block kind this message contract cannot carry, and
        ``ValidationError`` for a value it refuses, such as a non-image data URI. Fields the
        Workflow message has no slot for (image alt text, resource link title, description and
        size) are dropped.
        """

        parts: list[MessagePart] = []
        for block in content:
            if block.type == "text":
                parts.append(MessagePartText(text=block.text))
            elif block.type == "image":
                parts.append(MessagePartImage(image_url=block.uri))
            elif block.type == "resource_link":
                parts.append(MessagePartResourceLink(uri=block.uri, name=block.name, mime_type=block.media_type))
            else:
                raise TypeError(f"the Session Workflow message contract cannot carry {type(block).__name__}")
        return cls(parts=parts)


# Identifies commands sent by the Agents SDK, independently of application routing
# and internal-service authentication. SDK commands must not inherit the VCW source.
AGENTS_SDK_COMMAND_SOURCE: Final = "agents_sdk"

# Canonical set of MessageCommand sources. The field is still typed `str` during
# the P1.1 observation phase: any value outside this set is logged via
# `_observe_message_source` so we can spot stragglers before tightening to a
# `Literal[...]` in a follow-up PR.
CANONICAL_MESSAGE_SOURCES = frozenset(
    {
        "vibe_code_web",
        "vibe_code_cli",
        "slack",
        "slack_connector",
        "github",
        "linear",
        "notion",
        "cloud_test",
        AGENTS_SDK_COMMAND_SOURCE,
    }
)
_seen_message_source_violations: set[str] = set()


def require_canonical_source(source: str) -> str:
    """Refuse a ``source`` outside ``CANONICAL_MESSAGE_SOURCES`` in an HTTP request body."""

    # A new contract starts strict: tightening the accepted products later would break callers.
    if source not in CANONICAL_MESSAGE_SOURCES:
        raise ValueError(f"source must be one of {sorted(CANONICAL_MESSAGE_SOURCES)}")
    return source


class MessageCommand(BaseModel):
    type: Literal["message"] = "message"
    command_id: UUID | None = None
    source: str
    message: MessageInput
    metadata: CommandMetadata | None = None
    context: MessageContext | None = None
    expected_turn_id: str | None = Field(default=None, exclude_if=lambda value: value is None)

    @field_validator("source", mode="before")
    @classmethod
    def _observe_message_source(cls, v: object) -> object:
        """Observation step before tightening ``source`` to a ``Literal``.

        Logs a single warning per process per out-of-canonical value seen, so
        the soak signal stays usable even when Temporal replays the same
        signal payload many times. The warning is best-effort and may still
        double-fire across worker restarts — acceptable for observation
        purposes.
        """
        if isinstance(v, str) and v not in CANONICAL_MESSAGE_SOURCES and v not in _seen_message_source_violations:
            _seen_message_source_violations.add(v)
            logger.warning(
                "message_command.source.out_of_canonical_set",
                source=v,
                canonical=sorted(CANONICAL_MESSAGE_SOURCES),
            )
        return v


class CallbackResultAnswer(BaseModel):
    question: str
    answer: str | None = None
    selected: list[str] = Field(default_factory=list)


class CallbackResultTaskOutput(BaseModel):
    status: Literal["running", "failed", "completed", "canceled"] | str = "completed"
    value: JsonValue = Field(default_factory=dict)
    error: str | None = None
    # Client tool answers only. Blocks are Session content blocks in JSON form; the worker
    # validates them. A control plane without these fields drops them and the model sees value.
    # Unset fields stay off the wire so a deployed controller sees the payload it knows.
    content: list[JsonObject] | None = Field(default=None, exclude_if=lambda value: value is None)
    is_error: bool = Field(default=False, exclude_if=lambda value: not value)
    meta: JsonObject | None = Field(default=None, exclude_if=lambda value: value is None)


class CallbackResultTaskState(BaseModel):
    id: str = ""
    input: JsonValue = Field(default_factory=dict)
    output: CallbackResultTaskOutput = Field(default_factory=CallbackResultTaskOutput)
    history: list[JsonValue] = Field(default_factory=list)


class CallbackResultEventPayload(BaseModel):
    task_id: str = ""
    result: CallbackResultTaskState = Field(default_factory=CallbackResultTaskState)


class CallbackResultPayload(BaseModel):
    type: Literal["task_result"] = "task_result"
    payload: CallbackResultEventPayload = Field(default_factory=CallbackResultEventPayload)

    @classmethod
    def completed(
        cls,
        *,
        task_id: UUID | str = "",
        value: JsonValue = None,
        input: JsonValue = None,
    ) -> "CallbackResultPayload":
        task_id_text = str(task_id) if task_id else ""
        return cls(
            payload=CallbackResultEventPayload(
                task_id=task_id_text,
                result=CallbackResultTaskState(
                    id=task_id_text,
                    input={} if input is None else input,
                    output=CallbackResultTaskOutput(
                        status="completed",
                        value={} if value is None else value,
                    ),
                    history=[],
                ),
            )
        )


class CallbackResultCommand(BaseModel):
    type: Literal["callback_result"] = "callback_result"
    command_id: UUID | None = None
    callback_id: UUID
    result: CallbackResultPayload


class IntegrationEventPayload(BaseModel, Generic[IntegrationEventBodyT]):
    integration_id: str | None = None
    external_event_id: str
    routing_keys: list[str]
    body: IntegrationEventBodyT


class IntegrationEventCommand(BaseModel, Generic[IntegrationEventBodyT]):
    type: Literal["integration_event"] = "integration_event"
    command_id: UUID | None = None
    source: str
    event: IntegrationEventPayload[IntegrationEventBodyT]


class SystemCommand(BaseModel):
    type: Literal["system"] = "system"
    command_id: UUID | None = None
    action: Literal["resume", "retry", "stop", "interrupt"]
    reason: str | None = None
    expected_turn_id: str | None = Field(default=None, exclude_if=lambda value: value is None)
    # The Session limit behind a control-plane stop, such as a parent ending at its limit. A plain
    # string so an older reader still parses a cause it has no member for.
    cause: str | None = Field(default=None, exclude_if=lambda value: value is None)


class SessionCommandVerdictReason(StrEnum):
    """Why the Session answered a compare-and-set, a Start or a ``send_message`` the way it did.

    Defined once, on the wire, because the Workflow sets these and the control plane routes
    on them from a separately versioned package. The field itself stays a plain string so an
    older reader still parses a reason it has no member for.
    """

    STALE_TURN = "stale_turn"
    # A Start the Session refused because a Turn is already running. Nothing was applied, and
    # ``active_turn_id`` names the Turn running when the verdict was read. A Start refused by
    # this Update is not kept for its id, so the same id may be retried once that Turn ends. A
    # legacy-protocol Session keeps the refusal of a Start it first got by signal, so that id is
    # refused again. An empty ``active_turn_id`` is not expected on Session v1, where the id is
    # read right after the refusal: on an empty one, retry with a new id, which is always safe.
    TURN_ACTIVE = "turn_active"
    ALREADY_OBSERVED = "already_observed"
    SESSION_CONTINUING = "session_continuing"
    # Only on ``send_message``: the run closed for Continue-As-New while the message waited, and
    # the next run admits it. A retry with the same key gets its Turn.
    MESSAGE_CARRIED_OVER = "message_carried_over"
    SESSION_NOT_ACCEPTING_COMMANDS = "session_not_accepting_commands"
    INTAKE_OVERLOADED = "intake_overloaded"
    # The command alone exceeds the intake's byte budget, so no retry of it can succeed.
    MESSAGE_TOO_LARGE = "message_too_large"
    WORKFLOW_RUNTIME_DISABLED = "workflow_runtime_disabled"
    UNREADABLE_VERDICT = "unreadable_verdict"
    IDEMPOTENCY_CONFLICT = "idempotency_conflict"
    SESSION_BUSY = "session_busy"
    MESSAGE_REJECTED = "message_rejected"


class SessionCommandVerdict(BaseModel):
    """Whether the Session accepted one compare-and-set command or one Start.

    Returned by the Workflow's command Update handler. A command carrying an
    ``expected_turn_id`` names the Turn the caller believes is running, and a Start (a message
    naming no Turn) claims that none is; the Session is the only authority on that, so it
    answers here rather than through an event. ``accepted`` is a real boolean: an unaccepted
    command was never applied.
    """

    accepted: bool
    reason: str | None = None
    active_turn_id: str | None = None


# Workflow Update that starts a Turn or steers the running one with a ``send_message.SendMessageInput``.
SEND_MESSAGE_UPDATE_NAME: Final = "send_message"
# How long the Update holds a message while the Session is busy before answering busy, under the
# Workflows API's 20 s Update RPC timeout. Startup and queueing behind earlier messages are not
# bounded: a caller that times out retries the same idempotency key, and its receipt answers.
# Remote clients size their busy cut-off on their own copy, so the Worker and the client should
# change it together.
SEND_MESSAGE_BUSY_WAIT_SECONDS: Final = 10.0


class SessionMessageVerdict(BaseModel):
    """Whether the Session accepted one message, and which Turn it joined.

    Returned by the ``send_message`` Update. An accepted message started or steered the Turn
    named by ``turn_id``, and ``message_entry_id`` names its history entry. A refused message
    was not applied, except that a stopping Session answers ``session_not_accepting_commands``
    even for a message it committed during the stop.
    Such a message may have started its Turn before the stop interrupted it.
    ``reason`` carries a ``SessionCommandVerdictReason`` value. ``session_busy`` means the
    same message can be retried later; ``message_rejected`` means the Session refused this
    message and will refuse it again.
    """

    accepted: bool
    message_entry_id: str | None = None
    turn_id: str | None = None
    reason: str | None = None


class AgentConfiguration(BaseModel):
    toolsets: list[ToolsetInput]
    additional_instructions: str = Field(default="", exclude_if=lambda value: value == "")
    model: str | None = Field(default=None, exclude_if=lambda value: value is None)
    reasoning_effort: ReasoningEffort | None = Field(default=None, exclude_if=lambda value: value is None)

    @classmethod
    def unspecified(cls) -> Self:
        return cls(toolsets=[])


SessionWorkflowCommand = Annotated[
    MessageCommand | CallbackResultCommand | IntegrationEventCommand | SystemCommand,
    Field(discriminator="type"),
]


__all__ = [
    "AGENTS_SDK_COMMAND_SOURCE",
    "AgentConfiguration",
    "CANONICAL_MESSAGE_SOURCES",
    "MESSAGE_CONTEXT_MAX_LENGTH",
    "SEND_MESSAGE_BUSY_WAIT_SECONDS",
    "SEND_MESSAGE_UPDATE_NAME",
    "CallbackResultAnswer",
    "CallbackResultCommand",
    "CallbackResultEventPayload",
    "CallbackResultPayload",
    "CallbackResultTaskOutput",
    "CallbackResultTaskState",
    "CommandMetadata",
    "CommandObservability",
    "IntegrationEventCommand",
    "IntegrationEventPayload",
    "JsonObject",
    "McpAppMessageContextEntry",
    "McpAppMessageContextSource",
    "MessageCommand",
    "MessageContext",
    "MessageContextSource",
    "MessageInput",
    "MessagePart",
    "MessagePartForm",
    "MessagePartImage",
    "MessagePartResourceLink",
    "MessagePartText",
    "TeleportContextEntrypoint",
    "TeleportMessageContextSource",
    "SessionCommandVerdict",
    "SessionCommandVerdictReason",
    "SessionMessageVerdict",
    "SessionWorkflowCommand",
    "SystemCommand",
    "require_canonical_source",
]
