from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator


class BridgeAction(StrEnum):
    OBSERVE_HOOK = "observe_hook"
    APPEND_NATIVE = "append_native"
    LOAD_NATIVE = "load_native"
    LIST_NATIVE = "list_native"
    DELETE = "delete"
    HEALTH = "health"


class BridgeProvider(StrEnum):
    CLAUDE_CODE = "claude_code"
    CODEX = "codex"
    CURSOR = "cursor"
    VSCODE = "vscode"


class BridgeOrigin(StrEnum):
    INDEPENDENT_HOOK = "independent_hook"
    MATRX_LOCAL = "matrx_local"
    MATRX_SANDBOX = "matrx_sandbox"


class EntryFidelity(StrEnum):
    EVENT_MIRROR = "event_mirror"
    NATIVE = "native"


class EntryFormat(StrEnum):
    HOOK_EVENT = "hook_event"
    NATIVE_ENTRY = "native_entry"


class ProjectionStatus(StrEnum):
    PENDING = "pending"
    PROJECTED = "projected"
    SKIPPED = "skipped"
    ERROR = "error"


class BridgeConversation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    conversation_id: UUID
    is_new: bool
    store: Literal[True] = True


class BridgeHookEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Annotated[str, Field(min_length=1, max_length=128)]
    stable_event_id: Annotated[str, Field(min_length=1, max_length=512)] | None = None
    payload: dict[str, JsonValue]
    occurred_at: datetime | None = None


class BridgeEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entry_id: Annotated[str, Field(min_length=1, max_length=512)]
    source_sequence: Annotated[int, Field(ge=0)] | None = None
    kind: Annotated[str, Field(min_length=1, max_length=256)]
    occurred_at: datetime | None = None
    payload_sha256: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")] | None = None
    payload: dict[str, JsonValue]
    source_cursor: dict[str, JsonValue] | None = None


class BridgeAccountIdentity(BaseModel):
    """Opaque, display-safe provider-account provenance. Never authorization.

    ``provider_account_key`` version 2 is the canonical contract: a deterministic
    SHA-256 of a fixed public platform namespace plus the provider's stable
    account fields, so the same provider account produces the same key on every
    machine. Version 1 (absent field) is the retired per-installation HMAC;
    v1 keys are never comparable across machines or against v2 keys.
    ``provider_account_fingerprint`` is the first 12 hex chars of the key.
    ``provider_account_label`` is a short display-safe label (masked email or an
    org-id prefix) — never a raw email, credential, or token.
    """

    model_config = ConfigDict(extra="forbid")

    provider_account_key: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
    provider_account_key_version: Literal[1, 2] = 2
    provider_account_fingerprint: Annotated[str, Field(pattern=r"^[0-9a-f]{12}$")] | None = None
    provider_account_label: Annotated[str, Field(min_length=1, max_length=64)] | None = None

    @model_validator(mode="after")
    def enforce_fingerprint_consistency(self) -> BridgeAccountIdentity:
        if (
            self.provider_account_fingerprint is not None
            and self.provider_account_fingerprint != self.provider_account_key[:12]
        ):
            raise ValueError("provider_account_fingerprint must be the key's first 12 hex chars")
        return self


class BridgeSourceMetadata(BaseModel):
    """Bounded, non-authoritative provenance for an explicit local import."""

    model_config = ConfigDict(extra="forbid")

    source_kind: Literal["claude_local_jsonl"]
    provider_native_session_id: UUID
    provider_account_key: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")] | None = None
    provider_account_key_version: Literal[1, 2] = 1
    provider_account_fingerprint: Annotated[str, Field(pattern=r"^[0-9a-f]{12}$")] | None = None
    provider_account_label: Annotated[str, Field(min_length=1, max_length=64)] | None = None
    importer_version: Annotated[str, Field(min_length=1, max_length=64)]
    client_version: Annotated[str, Field(min_length=1, max_length=64)] | None = None
    transcript_sha256: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
    transcript_bytes: Annotated[int, Field(ge=0, le=268_435_456)]
    transcript_entry_count: Annotated[int, Field(ge=0, le=1_000_000)]
    transcript_mtime_ns: Annotated[int, Field(ge=0)]
    source_complete: bool
    corrupt_line_count: Annotated[int, Field(ge=0, le=1_000_000)] = 0

    @model_validator(mode="after")
    def enforce_wire_size(self) -> BridgeSourceMetadata:
        if (
            self.provider_account_fingerprint is not None
            and self.provider_account_key is not None
            and self.provider_account_fingerprint != self.provider_account_key[:12]
        ):
            raise ValueError("provider_account_fingerprint must be the key's first 12 hex chars")
        if self.provider_account_key is None and self.provider_account_fingerprint is not None:
            raise ValueError("provider_account_fingerprint requires provider_account_key")
        encoded = self.model_dump_json(exclude_none=True).encode("utf-8")
        if len(encoded) > 2_048:
            raise ValueError("source_metadata exceeds the 2048-byte UTF-8 limit")
        return self


class BridgeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1] = 1
    action: BridgeAction
    provider: BridgeProvider
    provider_session_id: Annotated[str, Field(min_length=1, max_length=1024)] | None = None
    provider_project_key: Annotated[str, Field(min_length=1, max_length=1024)] | None = None
    conversation: BridgeConversation | None = None
    origin: BridgeOrigin | None = None
    stream_key: Annotated[str, Field(min_length=1, max_length=512)] = "main"
    hook_event: BridgeHookEvent | None = None
    entries: Annotated[list[BridgeEntry], Field(max_length=1000)] = Field(default_factory=list)
    source_metadata: BridgeSourceMetadata | None = None
    account_identity: BridgeAccountIdentity | None = None
    writer_runtime_id: Annotated[str, Field(min_length=1, max_length=512)] | None = None
    writer_lease_seconds: Annotated[int, Field(ge=30, le=3600)] = 300
    after_source_sequence: Annotated[int, Field(ge=0)] | None = None
    limit: Annotated[int, Field(ge=1, le=1000)] = 250

    @model_validator(mode="after")
    def validate_action_shape(self) -> BridgeRequest:
        session_actions = {
            BridgeAction.OBSERVE_HOOK,
            BridgeAction.APPEND_NATIVE,
            BridgeAction.LOAD_NATIVE,
            BridgeAction.DELETE,
        }
        if self.action in session_actions and self.provider_session_id is None:
            raise ValueError(f"provider_session_id is required for {self.action.value}")
        if self.action is BridgeAction.OBSERVE_HOOK:
            if self.hook_event is None:
                raise ValueError("hook_event is required for observe_hook")
            if self.origin not in {None, BridgeOrigin.INDEPENDENT_HOOK}:
                raise ValueError("observe_hook origin must be independent_hook")
            if self.entries:
                raise ValueError("observe_hook accepts hook_event, not entries")
        elif self.hook_event is not None:
            raise ValueError("hook_event is only valid for observe_hook")
        if self.action is BridgeAction.APPEND_NATIVE:
            if not self.entries:
                raise ValueError("entries are required for append_native")
            if self.conversation is None:
                raise ValueError("conversation is required for append_native")
            if self.origin not in {BridgeOrigin.MATRX_LOCAL, BridgeOrigin.MATRX_SANDBOX}:
                raise ValueError("append_native origin must be matrx_local or matrx_sandbox")
            if self.writer_runtime_id is None:
                raise ValueError("writer_runtime_id is required for append_native")
            if self.source_metadata is not None and (
                self.provider is not BridgeProvider.CLAUDE_CODE
                or self.origin is not BridgeOrigin.MATRX_LOCAL
            ):
                raise ValueError("source_metadata is supported only for Matrx Local Claude imports")
            if self.source_metadata is not None and self.provider_project_key is None:
                raise ValueError("provider_project_key is required for local Claude imports")
        elif self.entries:
            raise ValueError("entries are only valid for append_native")
        elif self.source_metadata is not None:
            raise ValueError("source_metadata is only valid for append_native")
        if self.account_identity is not None:
            if self.action is not BridgeAction.OBSERVE_HOOK:
                raise ValueError(
                    "account_identity is only valid for observe_hook; "
                    "append_native carries account provenance inside source_metadata"
                )
        if self.action is BridgeAction.LOAD_NATIVE and self.conversation is not None:
            raise ValueError("load_native resolves its persisted binding; omit conversation")
        if self.after_source_sequence is not None and self.action is not BridgeAction.LOAD_NATIVE:
            raise ValueError("after_source_sequence is only valid for load_native")
        return self


class BridgeProjectionReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider_entry_id: str
    status: ProjectionStatus
    normalized_message_id: UUID | None = None
    normalized_tool_call_id: UUID | None = None
    error_code: str | None = None
    detail: str | None = None


class BridgeCheckpoint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stream_key: str
    highest_contiguous: int | None
    highest_seen: int | None
    missing_ranges: list[tuple[int, int]] = Field(default_factory=list)
    next_ingest_order: int
    complete: bool


class BridgeCapabilities(BaseModel):
    model_config = ConfigDict(extra="forbid")

    native_resume: bool
    native_fork: bool
    exact_entries: bool
    hook_event_mirror: bool
    stable_hook_ids: Literal["full", "partial", "none"]
    tool_payload_fidelity: Literal["full", "partial", "none"]


class BridgeHealth(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1] = 1
    status: Literal["ok"] = "ok"
    provider: BridgeProvider
    capabilities: BridgeCapabilities
    checkpoint: BridgeCheckpoint | None = None


class BridgeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1] = 1
    action: BridgeAction
    provider: BridgeProvider
    session_id: UUID | None = None
    conversation_id: UUID | None = None
    fidelity: EntryFidelity | None = None
    accepted: int = 0
    duplicates: int = 0
    conflicts: int = 0
    receipts: list[BridgeProjectionReceipt] = Field(default_factory=list)
    entries: list[BridgeEntry] = Field(default_factory=list)
    sessions: list[dict[str, JsonValue]] = Field(default_factory=list)
    has_more: bool = False
    checkpoint: BridgeCheckpoint | None = None
    health: BridgeHealth | None = None
    deleted: bool = False
    hook_specific_output: dict[str, JsonValue] | None = Field(
        default=None,
        serialization_alias="hookSpecificOutput",
    )
