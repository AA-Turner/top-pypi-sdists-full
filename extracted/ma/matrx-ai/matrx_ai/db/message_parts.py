"""MessagePart Pydantic models — the contract between Python and the database.

These models define exactly what is stored in cx_message.content (JSONB array).
They are the source of truth for TypeScript type generation and React rendering.

Architecture:
    - These models sit BETWEEN the existing dataclasses and the DB write.
    - The dataclasses (TextContent, ThinkingContent, etc.) are untouched.
    - validate_message_content() takes the raw dicts from to_storage_dict()
      and validates them through these models before writing to the DB.
    - model_dump(mode='json') produces the final DB-ready dict.

To regenerate TypeScript types:
    uv run python scripts/generate_types.py stream
"""

import base64
from typing import Annotated, Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    GetJsonSchemaHandler,
    GetPydanticSchema,
    model_validator,
)
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

from matrx_ai.config.citations import NormalizedCitation
from matrx_ai.db.content_types.data_ref import DataRef

# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------


class _MessagePartBase(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        core_schema_value: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        schema = handler(core_schema_value)
        properties = schema.get("properties", {})
        required = list(schema.get("required", []))
        # Pydantic defaults keep direct internal construction ergonomic, but a
        # persisted/request wire object without its discriminator is invalid.
        # Advertise that boundary truth to OpenAPI and every generated client.
        for discriminator in ("type", "kind"):
            if discriminator in properties and discriminator not in required:
                required.append(discriminator)
        if required:
            schema["required"] = required
        return schema


NonEmptyString = Annotated[str, Field(min_length=1)]


# ---------------------------------------------------------------------------
# TextPart
# Stored as: { "type": "text", "text": "...", "id": "...", "citations": [...], "metadata": {} }
# ---------------------------------------------------------------------------


class TextPart(_MessagePartBase):
    type: Literal["text"] = "text"
    text: str = ""
    id: str = ""
    # The canonical cross-provider citation shape (matrx_ai.config.citations).
    # Every ingestion path normalizes provider payloads BEFORE storage, so this
    # is strict on purpose — a raw provider citation reaching persistence is a
    # bug (the parse_content/reconstruct_content recovery coerces legacy items).
    citations: list[NormalizedCitation] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# ThinkingPart
# Stored as:
#   { "type": "thinking", "text": "...", "provider": "anthropic",
#     "signature": "...", "signature_encoding": "base64" | null,
#     "summary": [...], "id": "...", "metadata": {} }
#
# `signature_encoding` is the storage marker:
#   - "base64": signature is a base64-encoded binary blob (Google's
#     thought_signature is the only producer today).
#   - null: signature is an opaque provider string that round-trips verbatim
#     (OpenAI's encrypted_content, Anthropic's signature) — or there is no
#     signature at all.
# Always present (never elided), so consumers never have to disambiguate
# "missing key" from "explicitly raw".
# ---------------------------------------------------------------------------


class ThinkingPart(_MessagePartBase):
    type: Literal["thinking"] = "thinking"
    text: str = ""
    id: str = ""
    provider: Literal[
        "openai",
        "anthropic",
        "google",
        "cerebras",
        "moonshot",
        "together",
        "groq",
        "xai",
        "generic_openai",
    ] | None = None
    # Declared as str so the JSON schema (and TypeScript) always shows string.
    # bytes input is accepted and normalized to base64 by _normalize_signature.
    signature: str | None = None
    signature_encoding: Literal["base64"] | None = None
    summary: list[Any] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def _normalize_signature(cls, data: Any) -> Any:
        """Normalize a bytes signature to base64 string + encoding tag in lockstep.

        The dataclass layer (ThinkingContent.to_storage_dict) already does this,
        so the typical input here is already a string with a correct encoding
        tag. This validator is a defensive backstop for callers that construct
        ThinkingPart directly with raw bytes — it keeps signature and
        signature_encoding mutually consistent.
        """
        if not isinstance(data, dict):
            return data
        sig = data.get("signature")
        if isinstance(sig, bytes):
            return {
                **data,
                "signature": base64.b64encode(sig).decode("ascii"),
                "signature_encoding": "base64",
            }
        return data


# ---------------------------------------------------------------------------
# ToolCallPart
# Stored as: { "type": "tool_call", "call_id": "...", "name": "...", "arguments": {...}, "metadata": {} }
# ---------------------------------------------------------------------------


class ToolCallPart(_MessagePartBase):
    type: Literal["tool_call"] = "tool_call"
    call_id: str = ""
    name: str = ""
    arguments: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# ToolResultPart
# This is the POINTER block stored in cx_message.content for role="tool" messages.
# It is NOT the full output — the full output lives in cx_tool_call.output.
#
# Stored as:
#   {
#     "type": "tool_result",
#     "call_id": "...",          ← join key to cx_tool_call.call_id
#     "name": "...",             ← tool name (human-readable label)
#     "is_error": false,
#     "output_chars": 72,        ← true char count (pre-truncation) for size display
#     "output_preview": {...},   ← lightweight dict (≤ 500 chars) for UI rendering
#     "metadata": {}
#   }
#
# Notes:
#   - call_id is the primary join key; tool_use_id carries the same value (existing pattern).
#   - output_chars reflects the FULL output size even when cx_tool_call.output was truncated.
#   - output_preview is either tool-supplied or synthesized by ToolExecutionLogger.
#   - There is NO "content" field here — load cx_tool_call.output when the full result is needed.
# ---------------------------------------------------------------------------


class ToolResultPart(_MessagePartBase):
    type: Literal["tool_result"] = "tool_result"
    call_id: str = ""
    tool_use_id: str = ""
    name: str = ""
    is_error: bool = False
    output_chars: int = 0
    output_preview: dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# MediaPart  (type: "media")
# Covers image, audio, video, document, youtube — discriminated by "kind".
# Stored shape mirrors ``*Content.to_storage_dict()`` (Phase 3a/3b): origin,
# file_id, size_bytes, and kind-specific dims so cx_message reads do not need
# a follow-up GET /assets/{id}. Stream ``UnifiedMediaBlock`` is richer; this
# layer accepts the persistence subset only.
# NOTE: base64_data is stripped before validation — bytes must be uploaded to
# storage and replaced with url/file_id before reaching this layer.
# ---------------------------------------------------------------------------


class _StoredMediaPartBase(_MessagePartBase):
    origin: Literal["matrx", "external"] | None = None
    file_id: str | None = None
    url: str | None = None
    # NO file_uri: this shape is persisted in cx_message.content[] and streamed
    # to the client. The native storage location (s3://bucket/owner/key) is
    # server-only; a matrx file is identified by file_id, an external one by
    # url. The mode="before" validator drops a stale file_uri from historical
    # rows (extra="forbid" would otherwise reject it) and rescues a genuine
    # external URI into `url` when that's the only reference present.
    mime_type: str | None = None
    size_bytes: int | None = None

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        core_schema_value: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        schema = super().__get_pydantic_json_schema__(core_schema_value, handler)
        schema["allOf"] = [
            {
                "anyOf": [
                    {
                        "properties": {"url": {"type": "string", "minLength": 1}},
                        "required": ["url"],
                    },
                    {
                        "properties": {"file_id": {"type": "string", "minLength": 1}},
                        "required": ["file_id"],
                    },
                ]
            }
        ]
        return schema

    @model_validator(mode="before")
    @classmethod
    def _strip_inline_bytes(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        if any(k in data for k in ("base64_data", "base64", "file_uri")):
            data = {k: v for k, v in data.items() if k not in ("base64_data", "base64")}
            # A stale file_uri: drop the native storage location (identify by
            # file_id); rescue a genuine external URI into url if nothing else
            # references the media, so historical rows still validate.
            legacy = data.pop("file_uri", None)
            if (
                legacy
                and not data.get("url")
                and not data.get("file_id")
                and not str(legacy).startswith("s3://")
            ):
                data["url"] = legacy
        return data

    @model_validator(mode="after")
    def _require_resolvable_reference(self) -> "_StoredMediaPartBase":
        if not self.url and not self.file_id:
            raise ValueError(
                f"{self.__class__.__name__} requires 'url' or 'file_id'. "
                "Inline base64 must be uploaded to storage before persistence."
            )
        return self


class ImageMediaPart(_StoredMediaPartBase):
    type: Literal["media"] = "media"
    kind: Literal["image"] = "image"
    width: int | None = None
    height: int | None = None


class AudioMediaPart(_StoredMediaPartBase):
    type: Literal["media"] = "media"
    kind: Literal["audio"] = "audio"
    duration_ms: int | None = None
    transcription_result: str | None = None


class VideoMediaPart(_StoredMediaPartBase):
    type: Literal["media"] = "media"
    kind: Literal["video"] = "video"
    width: int | None = None
    height: int | None = None
    duration_ms: int | None = None


class DocumentMediaPart(_StoredMediaPartBase):
    type: Literal["media"] = "media"
    kind: Literal["document"] = "document"
    width: int | None = None
    height: int | None = None
    page_count: int | None = None


class YouTubeMediaPart(_MessagePartBase):
    type: Literal["media"] = "media"
    kind: Literal["youtube"] = "youtube"
    url: NonEmptyString
    external_url: str | None = None
    origin: Literal["external"] = "external"
    file_id: str | None = None
    mime_type: str | None = None
    size_bytes: int | None = None


# Discriminated union for all media kinds
MediaPart = Annotated[
    ImageMediaPart | AudioMediaPart | VideoMediaPart | DocumentMediaPart | YouTubeMediaPart,
    Field(discriminator="kind"),
]


# ---------------------------------------------------------------------------
# CodeExecPart
# Stored as: { "type": "code_exec", "language": "python", "code": "...", "metadata": {} }
# ---------------------------------------------------------------------------


class CodeExecPart(_MessagePartBase):
    type: Literal["code_exec"] = "code_exec"
    language: str = "python"
    code: str = ""


# ---------------------------------------------------------------------------
# CodeResultPart
# Stored as: { "type": "code_result", "output": "...", "outcome": "success", "metadata": {} }
# ---------------------------------------------------------------------------


class CodeResultPart(_MessagePartBase):
    type: Literal["code_result"] = "code_result"
    output: str = ""
    outcome: str = "success"


# ---------------------------------------------------------------------------
# WebSearchPart
# Stored as: { "type": "web_search", "id": "...", "status": "...", "metadata": {"action": {...}} }
# ---------------------------------------------------------------------------


class WebSearchPart(_MessagePartBase):
    type: Literal["web_search"] = "web_search"
    id: str = ""
    status: str = ""


# ---------------------------------------------------------------------------
# Structured input parts (client-sent context blocks)
# These are stored verbatim — the resolved_text goes in metadata.
# ---------------------------------------------------------------------------


class PreFetchedUrl(BaseModel):
    """A webpage entry that has already been scraped by the client.

    When the frontend has already fetched a page (e.g. via /scraper/quick-scrape)
    it can embed the content here instead of a plain URL string. The server will
    use this content directly and skip re-scraping.
    """

    model_config = ConfigDict(extra="allow")
    url: NonEmptyString
    textContent: str
    title: str | None = None
    scrapedAt: str | None = None
    charCount: int | None = Field(default=None, ge=0)


class WebpageInputPart(_MessagePartBase):
    type: Literal["input_webpage"] = "input_webpage"
    # Each entry is either a plain URL string or a pre-fetched object.
    urls: list[NonEmptyString | PreFetchedUrl] = Field(min_length=1)
    convert_to_text: bool = True
    optional_context: bool = False
    keep_fresh: bool = False
    # Tri-state editability (shared by every input_* part): true = inject the
    # resource's edit tools (wins over agent exclusions); false = explicit
    # read-only (no tools, a READ-ONLY notice, hard block on the id); omitted /
    # null = unspecified — inject nothing, leave the agent's own tools alone.
    editable: bool | None = None


class _EntityInputPartBase(_MessagePartBase):
    """Shared persisted wire controls for id-backed Matrx resources."""

    convert_to_text: bool = True
    optional_context: bool = False
    keep_fresh: bool = False
    editable: bool | None = None
    template: Literal["full", "compact", "minimal"] | None = None


NonEmptyResourceId = NonEmptyString


class LiveResourceRefInput(BaseModel):
    """A live id-backed reference; snapshots are not meaningful for opaque resources."""

    model_config = ConfigDict(extra="allow")
    id: NonEmptyResourceId
    mode: Literal["reference"] = "reference"


class SnapshotContentResourceRefInput(BaseModel):
    model_config = ConfigDict(extra="allow")
    mode: Literal["snapshot"]
    content: NonEmptyString


class SnapshotTextResourceRefInput(BaseModel):
    model_config = ConfigDict(extra="allow")
    mode: Literal["snapshot"]
    text: NonEmptyString


class SnapshotBodyResourceRefInput(BaseModel):
    model_config = ConfigDict(extra="allow")
    mode: Literal["snapshot"]
    body: NonEmptyString


class SnapshotDescriptionResourceRefInput(BaseModel):
    model_config = ConfigDict(extra="allow")
    mode: Literal["snapshot"]
    description: NonEmptyString


class SnapshotValueResourceRefInput(BaseModel):
    model_config = ConfigDict(extra="allow")
    mode: Literal["snapshot"]
    value: NonEmptyString


type ResourceRefInput = (
    LiveResourceRefInput
    | SnapshotContentResourceRefInput
    | SnapshotTextResourceRefInput
    | SnapshotBodyResourceRefInput
    | SnapshotDescriptionResourceRefInput
    | SnapshotValueResourceRefInput
)


class NotesInputPart(_MessagePartBase):
    type: Literal["input_notes"] = "input_notes"
    # A bare note-id string OR a ResourceRefInput object. Both are accepted so
    # the server can fetch live (reference) or render inline (snapshot).
    note_ids: list[NonEmptyResourceId | ResourceRefInput] = Field(min_length=1)
    template: str = "full"
    convert_to_text: bool = True
    optional_context: bool = False
    keep_fresh: bool = False
    editable: bool | None = None


class TaskInputPart(_MessagePartBase):
    type: Literal["input_task"] = "input_task"
    # A bare task-id string OR a ResourceRefInput object. Both are accepted so
    # the server can fetch live (reference) or render inline (snapshot).
    task_ids: list[NonEmptyResourceId | ResourceRefInput] = Field(min_length=1)
    template: str = "full"
    convert_to_text: bool = True
    optional_context: bool = False
    keep_fresh: bool = False
    editable: bool | None = None


class AgentInputPart(_EntityInputPartBase):
    type: Literal["input_agent"] = "input_agent"
    agent_ids: list[NonEmptyResourceId] = Field(min_length=1)


class ProjectInputPart(_EntityInputPartBase):
    type: Literal["input_project"] = "input_project"
    project_ids: list[NonEmptyResourceId] = Field(min_length=1)


class AgentAppInputPart(_EntityInputPartBase):
    type: Literal["input_agent_app"] = "input_agent_app"
    agent_app_ids: list[NonEmptyResourceId] = Field(min_length=1)


class TranscriptInputPart(_EntityInputPartBase):
    type: Literal["input_transcript"] = "input_transcript"
    transcript_ids: list[NonEmptyResourceId] = Field(min_length=1)


class TranscriptSessionInputPart(_EntityInputPartBase):
    type: Literal["input_transcript_session"] = "input_transcript_session"
    transcript_session_ids: list[NonEmptyResourceId] = Field(min_length=1)


class WorkbookInputPart(_EntityInputPartBase):
    type: Literal["input_workbook"] = "input_workbook"
    workbook_ids: list[NonEmptyResourceId | LiveResourceRefInput] = Field(min_length=1)


class DocumentInputPart(_EntityInputPartBase):
    type: Literal["input_document"] = "input_document"
    document_ids: list[NonEmptyResourceId | LiveResourceRefInput] = Field(min_length=1)


# ---------------------------------------------------------------------------
# Bookmark item models (the elements of input_table / input_list `bookmarks`)
#
# A bookmark is a typed pointer to a SCOPE of a user dataset/picklist. The wire
# `type` discriminates the scope; the ids are per-scope. These give the FE a
# precise contract (replacing the old opaque `dict[str, Any]` → `Record<string,
# unknown>[]`) and document exactly what a valid bookmark looks like.
#
# `extra="allow"` so UI-supplied fetch hints (limit/offset/sort_field/…) ride
# along without a validation failure — the resolver reads only the typed ids.
# These mirror the wire `type` literals consumed by the dataset / picklist
# fetch layer in matrx_ai.db.content_types.datasets / picklists. Bookmarks are
# resolved through the ownership-gated ReferenceOrchestrator
# (aidream/services/references/bookmarks.py::resolve_bookmarks); add a scope
# here → wire the matching fetch + resolver branch there.
# ---------------------------------------------------------------------------


class _BookmarkBase(BaseModel):
    model_config = ConfigDict(extra="allow")


class FullTableBookmark(_BookmarkBase):
    type: Literal["full_table"] = "full_table"
    table_id: NonEmptyString
    table_name: str | None = None


class TableColumnBookmark(_BookmarkBase):
    type: Literal["table_column"] = "table_column"
    table_id: NonEmptyString
    column_name: NonEmptyString
    table_name: str | None = None


class TableRowBookmark(_BookmarkBase):
    type: Literal["table_row"] = "table_row"
    table_id: NonEmptyString
    row_id: NonEmptyString
    table_name: str | None = None


class TableCellBookmark(_BookmarkBase):
    type: Literal["table_cell"] = "table_cell"
    table_id: NonEmptyString
    row_id: NonEmptyString
    column_name: NonEmptyString
    table_name: str | None = None


class TableSchemaBookmark(_BookmarkBase):
    # Schema-only pointer (columns/types, NEVER rows). Converges onto the `table_schema`
    # reference type (aidream references.bookmarks.BOOKMARK_TYPE_TO_REFERENCE).
    type: Literal["table_schema"] = "table_schema"
    table_id: NonEmptyString
    table_name: str | None = None


TableBookmark = Annotated[
    FullTableBookmark
    | TableColumnBookmark
    | TableRowBookmark
    | TableCellBookmark
    | TableSchemaBookmark,
    Field(discriminator="type"),
]


class FullListBookmark(_BookmarkBase):
    type: Literal["full_list"] = "full_list"
    list_id: NonEmptyString
    list_name: str | None = None


class ListGroupBookmark(_BookmarkBase):
    type: Literal["list_group"] = "list_group"
    list_id: NonEmptyString
    group_name: NonEmptyString
    list_name: str | None = None


class ListItemBookmark(_BookmarkBase):
    type: Literal["list_item"] = "list_item"
    list_id: NonEmptyString
    item_id: NonEmptyString
    list_name: str | None = None


ListBookmark = Annotated[
    FullListBookmark | ListGroupBookmark | ListItemBookmark,
    Field(discriminator="type"),
]


class TableInputPart(_MessagePartBase):
    type: Literal["input_table"] = "input_table"
    bookmarks: list[TableBookmark] = Field(min_length=1)
    convert_to_text: bool = True
    optional_context: bool = False
    keep_fresh: bool = False
    editable: bool | None = None


class ListInputPart(_MessagePartBase):
    type: Literal["input_list"] = "input_list"
    bookmarks: list[ListBookmark] = Field(min_length=1)
    convert_to_text: bool = True
    optional_context: bool = False
    keep_fresh: bool = False
    editable: bool | None = None


class DataInputPart(_MessagePartBase):
    type: Literal["input_data"] = "input_data"
    refs: list[DataRef] = Field(min_length=1)
    convert_to_text: bool = True
    optional_context: bool = False
    keep_fresh: bool = False
    editable: bool | None = None


class ContextInputPart(_MessagePartBase):
    type: Literal["input_context"] = "input_context"
    context_id: str = ""
    context_name: str = ""
    context_data: dict[str, Any] = Field(default_factory=dict)
    convert_to_text: bool = True
    optional_context: bool = False
    keep_fresh: bool = False
    editable: bool | None = None


# ---------------------------------------------------------------------------
# Persisted union + validated request-side union
# ---------------------------------------------------------------------------

MessagePart = (
    TextPart
    | ThinkingPart
    | ToolCallPart
    | ToolResultPart
    | MediaPart
    | CodeExecPart
    | CodeResultPart
    | WebSearchPart
    | WebpageInputPart
    | NotesInputPart
    | TaskInputPart
    | AgentInputPart
    | ProjectInputPart
    | AgentAppInputPart
    | TranscriptInputPart
    | TranscriptSessionInputPart
    | WorkbookInputPart
    | DocumentInputPart
    | TableInputPart
    | ListInputPart
    | DataInputPart
    | ContextInputPart
)


class _UserMediaInputPartBase(_MessagePartBase):
    """Request-side media accepts inline bytes before the upload/persist step."""

    origin: Literal["matrx", "external"] | None = None
    file_id: str | None = None
    url: str | None = None
    base64_data: str | None = None
    mime_type: str | None = None
    size_bytes: int | None = None

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        core_schema_value: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        schema = super().__get_pydantic_json_schema__(core_schema_value, handler)
        schema["allOf"] = [
            {
                "anyOf": [
                    {
                        "properties": {"url": {"type": "string", "minLength": 1}},
                        "required": ["url"],
                    },
                    {
                        "properties": {"file_id": {"type": "string", "minLength": 1}},
                        "required": ["file_id"],
                    },
                    {
                        "properties": {
                            "base64_data": {"type": "string", "minLength": 1}
                        },
                        "required": ["base64_data"],
                    },
                ]
            }
        ]
        return schema

    @model_validator(mode="after")
    def _require_resolvable_reference(self) -> "_UserMediaInputPartBase":
        if not self.url and not self.file_id and not self.base64_data:
            raise ValueError(
                f"{self.__class__.__name__} requires 'url', 'file_id', or 'base64_data'."
            )
        return self


class UserImageMediaPart(_UserMediaInputPartBase):
    type: Literal["media"] = "media"
    kind: Literal["image"] = "image"
    width: int | None = None
    height: int | None = None


class UserAudioMediaPart(_UserMediaInputPartBase):
    type: Literal["media"] = "media"
    kind: Literal["audio"] = "audio"
    duration_ms: int | None = None
    transcription_result: str | None = None


class UserVideoMediaPart(_UserMediaInputPartBase):
    type: Literal["media"] = "media"
    kind: Literal["video"] = "video"
    width: int | None = None
    height: int | None = None
    duration_ms: int | None = None


class UserDocumentMediaPart(_UserMediaInputPartBase):
    type: Literal["media"] = "media"
    kind: Literal["document"] = "document"
    width: int | None = None
    height: int | None = None
    page_count: int | None = None


class UserYouTubeMediaPart(_MessagePartBase):
    type: Literal["media"] = "media"
    kind: Literal["youtube"] = "youtube"
    url: NonEmptyString
    external_url: str | None = None
    origin: Literal["external"] = "external"
    mime_type: str | None = None


UserMediaPart = Annotated[
    UserImageMediaPart
    | UserAudioMediaPart
    | UserVideoMediaPart
    | UserDocumentMediaPart
    | UserYouTubeMediaPart,
    Field(discriminator="kind"),
]

_UserInputPartModel = (
    TextPart
    | ThinkingPart
    | ToolCallPart
    | ToolResultPart
    | UserMediaPart
    | CodeExecPart
    | CodeResultPart
    | WebSearchPart
    | WebpageInputPart
    | NotesInputPart
    | TaskInputPart
    | AgentInputPart
    | ProjectInputPart
    | AgentAppInputPart
    | TranscriptInputPart
    | TranscriptSessionInputPart
    | WorkbookInputPart
    | DocumentInputPart
    | TableInputPart
    | ListInputPart
    | DataInputPart
    | ContextInputPart
)

_MEDIA_TYPE_ALIASES: dict[str, str] = {
    "image": "image",
    "input_image": "image",
    "output_image": "image",
    "audio": "audio",
    "input_audio": "audio",
    "output_audio": "audio",
    "video": "video",
    "input_video": "video",
    "output_video": "video",
    "document": "document",
    "input_file": "document",
    "output_document": "document",
    "pdf": "document",
    "file": "document",
    "youtube_video": "youtube",
}


def _normalize_user_input_part(value: Any) -> Any:
    if not isinstance(value, dict):
        return value

    part = dict(value)
    part_type = part.get("type")
    if not isinstance(part_type, str) or not part_type:
        raise ValueError("Structured user-input parts require a non-empty 'type' discriminator.")
    if part_type == "input_document" and "document_ids" in part:
        return part

    media_kind = _MEDIA_TYPE_ALIASES.get(part_type)
    if media_kind is not None:
        part["type"] = "media"
        part["kind"] = media_kind
        for alias in ("image_url", "audio_url", "video_url", "file_url", "document_url"):
            if alias in part and "url" not in part:
                part["url"] = part.pop(alias)
        if "youtube_url" in part and "url" not in part:
            part["url"] = part.pop("youtube_url")
        return part

    type_aliases = {
        "input_text": "text",
        "output_text": "text",
        "function_call": "tool_call",
        "function_result": "tool_result",
        "tool_call_result": "tool_result",
        "code_execution": "code_exec",
        "code_execution_result": "code_result",
    }
    normalized_type = type_aliases.get(part_type)
    if normalized_type is not None:
        part["type"] = normalized_type
    return part


def _user_input_part_schema(
    _source_type: Any,
    handler: Any,
) -> core_schema.CoreSchema:
    model_schema = handler.generate_schema(_UserInputPartModel)

    def _dump_model(value: BaseModel) -> dict[str, Any]:
        return value.model_dump(mode="json", exclude_none=True, exclude_unset=True)

    normalized_schema = core_schema.no_info_before_validator_function(
        _normalize_user_input_part,
        model_schema,
    )
    return core_schema.no_info_after_validator_function(_dump_model, normalized_schema)


# Runtime value: a plain dict, preserving every existing downstream caller.
# JSON schema: the authoritative Pydantic union above, so OpenAPI gives clients
# a constructible contract instead of Record<string, unknown>.
UserInputPart = Annotated[
    dict[str, Any],
    GetPydanticSchema(_user_input_part_schema),
]


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

MESSAGE_PART_REGISTRY: dict[str, type[_MessagePartBase]] = {
    "text": TextPart,
    "thinking": ThinkingPart,
    "tool_call": ToolCallPart,
    "tool_result": ToolResultPart,
    "media": ImageMediaPart,  # media is further discriminated by 'kind'
    "code_exec": CodeExecPart,
    "code_result": CodeResultPart,
    "web_search": WebSearchPart,
    "input_webpage": WebpageInputPart,
    "input_notes": NotesInputPart,
    "input_task": TaskInputPart,
    "input_agent": AgentInputPart,
    "input_project": ProjectInputPart,
    "input_agent_app": AgentAppInputPart,
    "input_transcript": TranscriptInputPart,
    "input_transcript_session": TranscriptSessionInputPart,
    "input_workbook": WorkbookInputPart,
    "input_document": DocumentInputPart,
    "input_table": TableInputPart,
    "input_list": ListInputPart,
    "input_data": DataInputPart,
    "input_context": ContextInputPart,
}

# All concrete (non-media-union) types for codegen
MESSAGE_PART_MODELS: list[type[_MessagePartBase]] = [
    TextPart,
    ThinkingPart,
    ToolCallPart,
    ToolResultPart,
    ImageMediaPart,
    AudioMediaPart,
    VideoMediaPart,
    DocumentMediaPart,
    YouTubeMediaPart,
    CodeExecPart,
    CodeResultPart,
    WebSearchPart,
    WebpageInputPart,
    NotesInputPart,
    TaskInputPart,
    AgentInputPart,
    ProjectInputPart,
    AgentAppInputPart,
    TranscriptInputPart,
    TranscriptSessionInputPart,
    WorkbookInputPart,
    DocumentInputPart,
    TableInputPart,
    ListInputPart,
    DataInputPart,
    ContextInputPart,
]


# ---------------------------------------------------------------------------
# Validation entry point — called by persistence.py
# ---------------------------------------------------------------------------


def _sanitize_for_storage(value: Any) -> Any:
    """Recursively make a value safe for a PostgreSQL JSONB write.

    Two transforms, applied at the single persistence chokepoint so no provider
    can ever leak un-writable data into cx_message.content:

      - ``bytes`` -> base64 ``str``. PostgreSQL text/JSONB cannot store raw
        binary, and JSON has no bytes type. Providers occasionally hand us raw
        binary (e.g. Google's ``thought_signature`` on generated-image parts);
        base64 keeps the data round-trippable instead of crashing the write.
      - ``\\x00`` stripped from every string. PostgreSQL rejects NUL bytes in
        text with ``UntranslatableCharacterError`` (SQLSTATE 22P05); they carry
        no meaning in our content and only ever appear by accident.
    """
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("ascii")
    if isinstance(value, str):
        return value.replace("\x00", "") if "\x00" in value else value
    if isinstance(value, dict):
        return {k: _sanitize_for_storage(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [_sanitize_for_storage(v) for v in value]
    return value


def validate_message_content(raw: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Validate a raw content array from to_storage_dict() through Pydantic models.

    Raises ValueError with a clear message if any part fails validation.
    Returns a list of model_dump(mode='json') dicts ready to write to the DB.

    This is the single intercept point between the dataclass layer and the DB.
    """
    validated: list[dict[str, Any]] = []
    for i, raw_part in enumerate(raw):
        # Sanitize BEFORE validation so raw bytes / NUL bytes (e.g. Google's
        # thought_signature binary in media metadata) never reach the DB write
        # or the Pydantic JSON dump.
        raw_part = _sanitize_for_storage(raw_part)
        part_type = raw_part.get("type", "<missing>")
        part_kind = raw_part.get("kind")

        if part_type == "media":
            kind = raw_part.get("kind", "<missing>")
            kind_map: dict[str, type[_MessagePartBase]] = {
                "image": ImageMediaPart,
                "audio": AudioMediaPart,
                "video": VideoMediaPart,
                "document": DocumentMediaPart,
                "youtube": YouTubeMediaPart,
            }
            model_cls = kind_map.get(kind)
            if model_cls is None:
                raise ValueError(
                    f"Message content[{i}]: unknown media kind '{kind}'. "
                    f"Valid kinds: {list(kind_map)}"
                )
        else:
            model_cls = MESSAGE_PART_REGISTRY.get(part_type)
            if model_cls is None:
                raise ValueError(
                    f"Message content[{i}]: unknown part type '{part_type}'. "
                    f"Valid types: {list(MESSAGE_PART_REGISTRY)}"
                )

        try:
            part = model_cls.model_validate(raw_part)
        except Exception as exc:
            raise ValueError(
                f"Message content[{i}] (type='{part_type}', kind='{part_kind}'): "
                f"validation failed — {exc}"
            ) from exc

        validated.append(part.model_dump(mode="json", exclude_none=True))

    return validated
