from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Annotated, Literal
from uuid import UUID

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, JsonValue, model_validator


class BridgeAction(StrEnum):
    """The ONE advertised action vocabulary of the coding-session bridge.

    This enum is not an internal dispatch key: it IS the ``action`` parameter
    of the remote MCP tool and of ``POST /api/coding-sessions/bridge``, and MCP
    hosts fetch that schema live. **A member added here is callable by Claude
    Code, Codex, Cursor and VS Code the moment the server deploys** — so a
    member arrives only WITH its implementation, or it is refused out loud
    (:class:`BridgeRefusal`). Never add a placeholder member.

    The dispatch family (``capabilities``, ``handoff`` and ``send`` today;
    ``start``/``cancel`` in their own lanes) answers with
    :class:`BridgeDispatchResult` on ``BridgeResponse.dispatch`` — never by
    overloading the entry-ledger counters.
    """

    OBSERVE_HOOK = "observe_hook"
    APPEND_NATIVE = "append_native"
    LOAD_NATIVE = "load_native"
    LIST_NATIVE = "list_native"
    DELETE = "delete"
    HEALTH = "health"
    CAPABILITIES = "capabilities"
    HANDOFF = "handoff"
    SEND = "send"
    DIAGNOSE = "diagnose"
    REPROJECT = "reproject"


IMPLEMENTED_ACTIONS: frozenset[BridgeAction] = frozenset(
    {
        BridgeAction.OBSERVE_HOOK,
        BridgeAction.APPEND_NATIVE,
        BridgeAction.LOAD_NATIVE,
        BridgeAction.LIST_NATIVE,
        BridgeAction.DELETE,
        BridgeAction.HEALTH,
        BridgeAction.CAPABILITIES,
        BridgeAction.HANDOFF,
        BridgeAction.SEND,
        BridgeAction.DIAGNOSE,
        BridgeAction.REPROJECT,
    }
)
"""The actions this contract actually serves.

A :class:`BridgeAction` member missing from this set is refused with a typed
:class:`BridgeRefusal` naming the remedy — never a pydantic validation dump and
never a half-wired execution. Adding a member to the enum without adding it
here is legal on purpose: that is the only honest way an unimplemented verb can
exist in a vocabulary four hosts read live. The pairing is asserted by
``aidream/services/coding_session_bridge/tests/test_dispatch.py``.
"""


class BridgeProvider(StrEnum):
    CLAUDE_CODE = "claude_code"
    CODEX = "codex"
    CURSOR = "cursor"
    VSCODE = "vscode"


class BridgeOrigin(StrEnum):
    INDEPENDENT_HOOK = "independent_hook"
    MATRX_LOCAL = "matrx_local"
    MATRX_SANDBOX = "matrx_sandbox"


class BridgeRuntimeKind(StrEnum):
    """Which runtime can actually execute turns for a provider session.

    ``matrx_local`` and ``matrx_sandbox`` mirror the same-named
    :class:`BridgeOrigin` values (the user's own machine via Matrx Local, and
    the hosted Matrx Sandbox). ``seeded`` is the no-runtime case: a handoff
    that carries a seed packet instead of an executor, so a second tool can
    continue a conversation it never ran. It is implemented (lane XT-05) and is
    the only runtime that serves every provider, precisely because it executes
    nothing. ``independent_hook`` has no runtime
    by definition — nothing on our side executes those turns.
    """

    MATRX_LOCAL = "matrx_local"
    MATRX_SANDBOX = "matrx_sandbox"
    SEEDED = "seeded"


class BridgeOperation(StrEnum):
    """The ONE capability vocabulary every adapter and runtime reports against.

    Reconciles the two lists that disagreed before 2026-09-14: the ten adapter
    flags published in the contract doc (``start|send|stream|cancel|
    resume_native|fork_native|list|mirror|export|open``) and the six
    fidelity fields of :class:`BridgeCapabilities`. The ten OPERATIONS live
    here and are answered per provider × origin with a reason; the six
    fidelity FACTS stay in :class:`BridgeCapabilities`, which is also what
    ``chat.coding_session.capabilities`` stores. ``handoff`` is the eleventh
    member because the contract's collaboration section promises it as an
    operation; it is reported unsupported until its lane lands.

    Never mint a twelfth vocabulary: a new capability question becomes a member
    here, reported by every runtime descriptor in the same change.
    """

    START = "start"
    SEND = "send"
    STREAM = "stream"
    CANCEL = "cancel"
    RESUME_NATIVE = "resume_native"
    FORK_NATIVE = "fork_native"
    LIST = "list"
    MIRROR = "mirror"
    EXPORT = "export"
    OPEN = "open"
    HANDOFF = "handoff"


class BridgeSendTarget(StrEnum):
    """WHO is meant to receive a turn sent with ``action=send``.

    There is no default and there never will be one. The three things a person
    could mean by "reply to this coding conversation" have completely different
    consequences — an AI Matrx agent answers and the coding tool never learns of
    it; the tool's own runtime continues the session and the provider's
    transcript grows — and a verb that guessed between them would silently do
    the other one. The caller names the target, and the answer says which target
    served it (:class:`BridgeSendResult.target`).

    ``seeded_handoff`` is deliberately NOT a target: handing a conversation to a
    second tool is its own verb (``action=handoff``) because it writes a binding
    rather than a turn, and folding it in here would put two different write
    shapes behind one word.
    """

    MATRX_AGENT = "matrx_agent"
    """AI Matrx answers, in AI Matrx, with the agent the
    ``coding_session.conversation_responder`` mandate resolves for this account.
    The coding tool does NOT see the question or the answer, and both rows say so
    (``metadata.origin = "ai_matrx_reply"``). This is the SAME producer as the web
    reply composer — one door's answer is the other door's answer."""

    PROVIDER_NATIVE = "provider_native"
    """The binding's own runtime continues the provider session, so the turn lands
    in the coding tool's own transcript. Served only where a registered
    ``SessionRuntime`` can actually be reached from this door; anywhere else the
    call is refused with the runtime's own name and a remedy, never queued and
    never silently rerouted to an AI Matrx agent."""


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


ACCOUNT_LABEL_MASK_CHARACTER = "*"


def refuse_masked_account_label(value: str) -> str:
    """THE BRIDGE DOOR'S REFUSAL OF A MASKED PROVIDER ACCOUNT LABEL.

    ``provider_account_label`` is the provider account's own identity as the
    person knows it — the signed-in email, else ``org:<id>``. Arman ruled on
    2026-09-07 that an account name is not a secret, and the masking code was
    deleted the same day. But the rows written before that deletion still
    carried ``a***n@t***.com``, every reader shows what the row holds, and on
    2026-09-17 Arman saw his own email masked in AI Matrx. The code fix alone
    could not prevent the class from re-entering, because nothing refused a
    masked label at the door.

    ``*`` is never a character in an email address (RFC 5322 dot-atom) nor in
    an organization UUID, so its presence is unambiguous evidence that a
    producer masked the value. Both wire carriers of the label —
    :class:`BridgeAccountIdentity` and :class:`BridgeSourceMetadata` — apply
    this validator, so the whole bridge has exactly one door and a masked
    envelope is refused as a typed validation error, never stored.

    Guard: ``packages/matrx-ai/tests/coding_sessions/test_account_label_is_never_masked.py``
    (it plants a masked envelope and proves the refusal, and proves the same
    validator accepts the real label).
    """

    if ACCOUNT_LABEL_MASK_CHARACTER in value:
        raise ValueError(
            "provider_account_label must be the account's own identity, never a mask: "
            f"{ACCOUNT_LABEL_MASK_CHARACTER!r} is not a character in an email address "
            "or an organization id (an account name is not a secret — Arman, 2026-09-07)"
        )
    return value


AccountLabel = Annotated[
    str,
    Field(min_length=1, max_length=320),
    AfterValidator(refuse_masked_account_label),
]
"""The only accepted shape of a provider account label on the bridge wire."""


class BridgeAccountIdentity(BaseModel):
    """Opaque, display-safe provider-account provenance. Never authorization.

    ``provider_account_key`` version 2 is the canonical contract: a deterministic
    SHA-256 of a fixed public platform namespace plus the provider's stable
    account fields, so the same provider account produces the same key on every
    machine. Version 1 (absent field) is the retired per-installation HMAC;
    v1 keys are never comparable across machines or against v2 keys.
    ``provider_account_fingerprint`` is the first 12 hex chars of the key.
    ``provider_account_label`` is the provider account's own identity as the
    person knows it — the signed-in email, else the organization id. It is
    provenance the owner already has, so it is shown in full (Arman's ruling,
    2026-09-07: an account name is not a secret). Never a credential or token.
    """

    model_config = ConfigDict(extra="forbid")

    provider_account_key: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
    provider_account_key_version: Literal[1, 2] = 2
    provider_account_fingerprint: Annotated[str, Field(pattern=r"^[0-9a-f]{12}$")] | None = None
    provider_account_label: AccountLabel | None = None

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
    provider_account_label: AccountLabel | None = None
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
    # --- the `send` verb (lane XT-03b) -----------------------------------
    text: Annotated[str, Field(min_length=1, max_length=200_000)] | None = None
    """The turn being sent. Required by ``send`` and valid for nothing else:
    every other action carries provider ENTRIES, and a free-text field that
    silently did nothing on them would be the quietest possible lie."""
    target: BridgeSendTarget | None = None
    """Who receives the turn. Required by ``send``; never defaulted."""
    client_request_id: Annotated[str, Field(min_length=1, max_length=200)] | None = None
    """The caller's own replay identity for ONE paid dispatch (plan-attack F10).

    MCP hosts retry tool calls and Matrx Local's outbox replays envelopes after a
    restart by design, so a dispatch verb without a client key bills twice for
    one intention. Pass the host's tool-call id (the only value stable across a
    retry that re-sends the same arguments). Omitted, the server derives the key
    from the content of the dispatch, which is still replay-safe for an identical
    retry — and two deliberately different sends of the SAME text then need two
    different keys, which is the honest way to ask for two turns."""

    @model_validator(mode="after")
    def validate_action_shape(self) -> BridgeRequest:
        session_actions = {
            BridgeAction.OBSERVE_HOOK,
            BridgeAction.APPEND_NATIVE,
            BridgeAction.LOAD_NATIVE,
            BridgeAction.DELETE,
            # Both sync-truth verbs answer ABOUT one provider session, so the
            # id is the whole input. Without it there is nothing to diagnose
            # and nothing to re-project.
            BridgeAction.DIAGNOSE,
            BridgeAction.REPROJECT,
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
        if self.action is BridgeAction.HANDOFF:
            # `provider` IS the destination for a handoff: the call is about the
            # binding it creates. Deliberately no `to_provider` field — a new
            # enum-typed input would have to be widened on both doors and listed
            # in BRIDGE_ENUM_FIELDS, and the contract already has the field that
            # means "the provider this call is about".
            if self.conversation is None:
                raise ValueError(
                    "conversation is required for handoff: a handoff moves an EXISTING "
                    "conversation to a second provider"
                )
            if self.conversation.is_new:
                raise ValueError(
                    "handoff never creates a conversation; send conversation.is_new=false "
                    "with the id of the conversation being handed off"
                )
            if self.origin is not None:
                raise ValueError(
                    "handoff does not take an origin: the seeded binding's origin is the "
                    "receiving tool's own (independent_hook), decided server-side"
                )
            if self.writer_runtime_id is not None:
                raise ValueError(
                    "handoff claims no writer lease; a seeded binding has no runtime writing "
                    "native entries"
                )
        if (
            self.action in {BridgeAction.DIAGNOSE, BridgeAction.REPROJECT}
            and self.conversation is not None
        ):
            raise ValueError(
                f"{self.action.value} resolves its persisted binding; omit conversation"
            )
        if self.action is BridgeAction.SEND:
            if self.conversation is None:
                raise ValueError(
                    "conversation is required for send: a turn is sent INTO an existing "
                    "conversation"
                )
            if self.conversation.is_new:
                raise ValueError(
                    "send never creates a conversation; send conversation.is_new=false with "
                    "the id of the conversation you are replying in"
                )
            if self.text is None:
                raise ValueError("text is required for send: it is the turn being sent")
            if self.target is None:
                raise ValueError(
                    "target is required for send: name matrx_agent (AI Matrx answers and the "
                    "coding tool never sees it) or provider_native (the tool's own runtime "
                    "continues the session). There is no default — the two do different things"
                )
            if self.origin is not None:
                raise ValueError(
                    "send does not take an origin: the origin is the binding's own, read "
                    "server-side from the conversation"
                )
            if self.writer_runtime_id is not None:
                raise ValueError(
                    "send claims no writer lease; it writes canonical turns, never native "
                    "ledger entries"
                )
        else:
            if self.text is not None:
                raise ValueError("text is only valid for send")
            if self.target is not None:
                raise ValueError("target is only valid for send")
            if self.client_request_id is not None:
                raise ValueError(
                    "client_request_id is only valid for send — it is the replay identity of a "
                    "PAID dispatch, and no other action here spends a model call. handoff's "
                    "replay identity is structural (the deterministic offer id), and the entry "
                    "ledger's is provider_entry_id"
                )
        if self.action is BridgeAction.LOAD_NATIVE and self.conversation is not None:
            raise ValueError("load_native resolves its persisted binding; omit conversation")
        if self.action is BridgeAction.CAPABILITIES and self.conversation is not None:
            raise ValueError(
                "capabilities answers for a provider and origin; "
                "name provider_session_id to scope it to an existing binding, not conversation"
            )
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


class CapabilityVerdict(BaseModel):
    """One operation's truthful answer for one provider × origin.

    ``reason`` is MANDATORY whenever ``supported`` is false: a UI renders this
    sentence instead of guessing parity, and "unavailable" with no reason is
    the silent failure the contract forbids. When ``supported`` is true the
    reason may still carry the live-probe caveat (a hosted runtime needs a
    Matrx Sandbox; a local runtime needs Matrx Local running).
    """

    model_config = ConfigDict(extra="forbid")

    operation: BridgeOperation
    supported: bool
    reason: Annotated[str, Field(min_length=1, max_length=1024)] | None = None
    live_probe: Annotated[str, Field(min_length=1, max_length=512)] | None = None

    @model_validator(mode="after")
    def enforce_reason_on_refusal(self) -> CapabilityVerdict:
        if not self.supported and not self.reason:
            raise ValueError(
                f"{self.operation.value} is reported unsupported with no reason; "
                "an unsupported capability always names why"
            )
        return self


class BridgeCapabilityReport(BaseModel):
    """The `capabilities` action's answer: provider × origin, with reasons.

    Generalizes the Claude-only ``GET /api/coding-sessions/claude/capabilities``
    probe to every provider and every origin, and is the ONLY place a client
    may learn what it can do — see ``supported_actions``. A client that
    hardcodes an action list breaks on the first server that predates or
    postdates it, which is why there is no version number to negotiate.
    """

    model_config = ConfigDict(extra="forbid")

    provider: BridgeProvider
    origin: BridgeOrigin | None = None
    runtime: BridgeRuntimeKind | None = None
    available: bool
    reason: Annotated[str, Field(min_length=1, max_length=2048)] | None = None
    operations: Annotated[list[CapabilityVerdict], Field(min_length=1, max_length=64)]
    fidelity: BridgeCapabilities
    supported_actions: list[BridgeAction]

    @model_validator(mode="after")
    def enforce_report_truth(self) -> BridgeCapabilityReport:
        seen = [verdict.operation for verdict in self.operations]
        if len(seen) != len(set(seen)):
            raise ValueError("each operation is reported exactly once")
        missing = [member for member in BridgeOperation if member not in set(seen)]
        if missing:
            raise ValueError(
                "every BridgeOperation needs a verdict; missing: "
                + ", ".join(member.value for member in missing)
            )
        if not self.available and not self.reason:
            raise ValueError("an unavailable provider/origin always names why")
        verdicts = {verdict.operation: verdict.supported for verdict in self.operations}
        if verdicts[BridgeOperation.RESUME_NATIVE] != self.fidelity.native_resume:
            raise ValueError(
                "resume_native verdict and fidelity.native_resume must agree — "
                "they are the same fact in the two vocabularies"
            )
        if verdicts[BridgeOperation.FORK_NATIVE] != self.fidelity.native_fork:
            raise ValueError(
                "fork_native verdict and fidelity.native_fork must agree — "
                "they are the same fact in the two vocabularies"
            )
        return self


class BridgeRefusalCode(StrEnum):
    UNKNOWN_ACTION = "unknown_action"
    """The caller named an action this server has never heard of."""

    UNIMPLEMENTED_ACTION = "unimplemented_action"
    """The action is in this server's vocabulary but has no implementation."""

    UNKNOWN_FIELD_VALUE = "unknown_field_value"
    """A typed field other than ``action`` carried a value outside its vocabulary.

    ``action`` keeps its own two codes because clients already branch on them;
    every OTHER enum-typed input (``provider``, ``origin``) refuses under this
    one code, naming the field, the value and that field's supported values.
    The class this closes (2026-09-15, V-XT-2): only ``action`` was widened, so
    ``provider=claude`` — the name a coding agent guesses for ``claude_code`` —
    came back as a pydantic enum dump with no reason and no remedy from both
    doors, which is exactly the defect the action refusal was built to end.
    """

    MALFORMED_FIELD = "malformed_field"
    """An OBJECT-typed field carried a value that is not the shape it accepts.

    The sibling of ``UNKNOWN_FIELD_VALUE``, for the fields whose value is a
    structure rather than a token: ``conversation``, ``hook_event``, ``entries``,
    ``source_metadata``, ``account_identity``. It names which part is wrong, in
    plain words, and lists the field's accepted keys in ``supported_values`` —
    the object equivalent of a vocabulary.

    The class this closes (2026-09-17, V-CLOSE P3): the typed refusal was built
    for every enum and stopped there, so the object fields on the SAME signature
    were the untouched siblings — a malformed ``hook_event`` came back as "5
    validation errors for coding_session_bridgeArguments … visit
    https://errors.pydantic.dev/2.12/v/missing", and ``conversation`` sent as a
    string as "Input should be a valid dictionary or instance of
    BridgeConversation". A refusal that names our internal class names and links
    a validator's documentation is the same dead end the action refusal was
    built to end.
    """

    UNSUPPORTED_RUNTIME = "unsupported_runtime"
    """The action is implemented, but no runtime can serve this provider/origin."""

    HANDOFF_NOT_POSSIBLE = "handoff_not_possible"
    """There is nothing to hand off, or the hand-off would not be truthful.

    The two real cases (lane XT-05): the conversation carries no coding-session
    binding at all, so there is no source tool to hand FROM; and the caller
    named a receiving provider session that is already bound to a different
    owner's conversation. Both name the conversation and the remedy.
    """

    CONVERSATION_NOT_OWNED = "conversation_not_owned"
    """The conversation named by the call is not the authenticated account's.

    One code for the two readings a caller cannot distinguish and must not be
    told apart: the conversation belongs to someone else, or no conversation
    with that id exists. Every bridge read is owner-scoped, so answering
    "not found" for a row that exists would leak its existence and answering
    "not yours" for a typo would be a lie; the refusal names both readings and
    the remedy. The class this closes (2026-09-15, V-XT-5): `handoff` on
    another account's conversation raised a bare `PermissionError`, which no
    door had a handler for, so the ordinary first mistake of a coding agent —
    pasting someone else's conversation id — came back as HTTP 500
    "Something went wrong. Please try again later." and filed TWO
    `ops.system_error` rows per call. A refusal is client-fixable and is never
    a server fault.
    """

    SEND_NOT_POSSIBLE = "send_not_possible"
    """``send`` cannot be served for this conversation, and nothing was charged.

    The two real cases (lane XT-03b): the conversation carries no coding-session
    binding this account owns, so the bridge is not the door for it (an ordinary
    AI Matrx conversation is continued in AI Matrx); and no agent is bound to
    answer coding-conversation replies at all — neither
    ``coding_session.conversation_responder`` nor the platform's own default chat
    mandate resolves to an agent Holder, so answering would mean running an agent
    nobody configured. Both name the conversation and the remedy.
    """

    RUN_IN_FLIGHT = "run_in_flight"
    """Something is already running, so this turn was NOT started or charged.

    Three readings, each with its own remedy in the refusal's own words: another
    turn is live on this conversation (one live run per conversation is the
    platform's rule, so wait or cancel it); an IDENTICAL send — same
    ``client_request_id`` — is in flight and did not finish inside this call's
    wait bound, so call again with the SAME key to collect its answer rather than
    buying a second one; or that identical send gave its claim back without an
    answer, in which case retrying now wins the claim outright.
    """

    DISPATCH_CEILING = "dispatch_ceiling"
    """The account's daily coding-tool dispatch ceiling refused this call.

    Carries the ceiling, the rung that set it and the screen where it is raised,
    quoted from the one ceiling resolver — never a generic "try later".
    """


class BridgeRefusal(BaseModel):
    """A typed refusal — never a validation dump, never silence.

    Every refusal carries the action that was asked for, why it cannot be
    served, what to do instead, and the live list of actions this server does
    implement. That list is the version negotiation: there is no version number
    to compare, so a client asks and believes the answer.
    """

    model_config = ConfigDict(extra="forbid")

    code: BridgeRefusalCode
    #: The input that was refused. ``action`` for the two action codes; the
    #: field name (``provider``, ``origin``) for ``unknown_field_value``.
    requested_field: Annotated[str, Field(min_length=1, max_length=64)] = "action"
    #: The offending value of ``requested_field``, echoed back truncated.
    requested_value: Annotated[str, Field(min_length=1, max_length=128)]
    #: The action of the refused call. Equal to ``requested_value`` when the
    #: action itself was the problem; kept as its own field because every
    #: client that reads a refusal today reads this one.
    requested_action: Annotated[str, Field(min_length=1, max_length=128)]
    reason: Annotated[str, Field(min_length=1, max_length=2048)]
    remedy: Annotated[str, Field(min_length=1, max_length=2048)]
    #: This server's live vocabulary for ``requested_field``.
    supported_values: list[str]
    supported_actions: list[BridgeAction]


class BridgeHandoffState(StrEnum):
    """Where one handoff stands. Never inferred by a reader from other fields."""

    OFFERED = "offered"
    """The second binding exists and carries the seed packet, but no real
    provider session has claimed it yet. Its ``provider_session_id`` is the
    self-describing ``matrx-handoff:<digest>`` placeholder."""

    CLAIMED = "claimed"
    """A real session of the receiving provider is bound to the conversation:
    every turn its hooks mirror from here on lands on THIS conversation."""

    ALREADY_BOUND = "already_bound"
    """The receiving provider already had a live binding on this conversation,
    so nothing was minted. Answered, not refused — a handoff asked for twice is
    the same handoff (the replay rule), and saying "already bound" is the only
    honest reading of a second call."""


class BridgeSeedRead(BaseModel):
    """One call the receiving tool makes to read the conversation it inherits.

    The seed packet does NOT carry the transcript: it carries the reads. The
    adapter skills (``matrx-claude-plugin/skills/conversations``,
    ``matrx-codex-plugin/skills/use-ai-matrx``) already consume exactly these
    two ``conversations`` actions, so a handoff needs no client release — which
    is the whole point of putting the verb on the bridge contract.
    """

    model_config = ConfigDict(extra="forbid")

    tool: Literal["conversations"] = "conversations"
    action: Literal["get_summary", "get_messages"]
    arguments: dict[str, JsonValue]
    returns: Annotated[str, Field(min_length=1, max_length=512)]


class BridgeSeedPacket(BaseModel):
    """The seed a second tool continues a conversation from.

    ``native_resume`` is a ``Literal[False]``, not a bool: a seeded handoff can
    never become a native resume by any code path, and the contract forbids
    calling prompt seeding "resume" (FEATURE.md §collaboration). A reader that
    has this object in hand cannot be misled about which one it got.
    """

    model_config = ConfigDict(extra="forbid")

    kind: Literal["seeded_handoff"] = "seeded_handoff"
    native_resume: Literal[False] = False
    conversation_id: UUID
    title: Annotated[str, Field(max_length=512)] | None = None
    visible_message_count: Annotated[int, Field(ge=0)]
    read_with: Annotated[list[BridgeSeedRead], Field(min_length=1, max_length=8)]
    instructions: Annotated[str, Field(min_length=1, max_length=2048)]
    claim_with: dict[str, JsonValue] | None = None
    """The exact bridge call that turns this offer into a claimed binding, with
    the receiving session's own id as the one blank. ``None`` once claimed."""


class BridgeHandoffResult(BaseModel):
    """What a handoff did — both bindings named, with an explicit verdict.

    The FIRST contract object that describes two provider bindings on one
    conversation. Until 2026-09-15 every one of 4,633 bound conversations in
    production had exactly one binding and one provider, so "take a
    conversation from one tool and continue it in another" had zero instances;
    this result is that operation's receipt.
    """

    model_config = ConfigDict(extra="forbid")

    state: BridgeHandoffState
    conversation_id: UUID
    fidelity: Literal["seeded"] = "seeded"
    """The bridge-level fidelity verdict of the receiving binding. It is NOT the
    stored ``chat.coding_session.fidelity`` column, which is ``event_mirror``
    for this row and means what it has always meant (the receiving tool's own
    hooks mirror its turns). The seeded verdict is stored beside it in
    ``metadata.handoff`` so no schema change was needed to tell the truth.
    """
    verdict: Annotated[str, Field(min_length=1, max_length=1024)]
    from_provider: BridgeProvider
    from_provider_session_id: Annotated[str, Field(min_length=1, max_length=1024)]
    from_coding_session_id: UUID
    to_provider: BridgeProvider
    to_provider_session_id: Annotated[str, Field(min_length=1, max_length=1024)] | None = None
    to_coding_session_id: UUID
    rebound_from_conversation_id: UUID | None = None
    """Set when the receiving session already had a binding of its own: that row
    was MOVED onto this conversation rather than a second row inserted, because
    an active provider identity is unique per owner (FEATURE.md §identity)."""
    carried_message_count: Annotated[int, Field(ge=0)] = 0
    """How many turns moved WITH the binding on a rebind.

    A rebind moves a claiming session's row off its own conversation; any turns
    that session had already produced there travel with it, appended in order
    with provenance. Zero means the old conversation held nothing — never that
    content was left behind silently: `rebound_from_conversation_id` plus this
    count is the whole truth about what moved (V-XT-5 found the content-bearing
    case stranded, and the residue remedy only covered empty ones).
    """

    prior_context_conversation_id: UUID | None = None
    """Set when a rebind's turns STAYED on the old conversation because there
    were more of them than one transaction moves (`CARRY_LIMIT`). They are not
    stranded: that conversation is named here and readable with
    `conversations get_messages`. Never set together with a non-zero
    `carried_message_count` — exactly one of the two answers "where are the
    turns that session already produced".
    """

    prior_context_message_count: Annotated[int, Field(ge=0)] = 0
    """How many turns are on `prior_context_conversation_id`. Zero when none
    stayed behind."""

    absorbed_offer_session_id: UUID | None = None
    """The placeholder offer row this claim replaced, when the claim landed on a
    different row. It is deleted, so the conversation never shows a stale
    "handoff offered" binding beside the real one."""

    archived_source_conversation_id: UUID | None = None
    """The conversation this move left with nothing, and therefore ARCHIVED.

    Set only when the rebind emptied the source completely — no live message, no
    live binding — and the row was archived in the same unit of work as the
    move. Null when the source still holds something, which is every other case.
    Reported rather than done quietly: a move that changes the state of a second
    conversation must say which one (the XT-05 residue, still live on production
    2026-09-17 as an empty `status: active` row per handoff rebind)."""

    bindings_on_conversation: Annotated[int, Field(ge=1)]
    seed: BridgeSeedPacket


class BridgeSendState(StrEnum):
    """Where one ``send`` stands. Never inferred by a reader from other fields."""

    ANSWERED = "answered"
    """The turn was delivered and this call carries its answer."""

    REPLAYED = "replayed"
    """An earlier send with the same replay identity already produced this answer;
    nothing was run and nothing was charged a second time."""


class BridgeSendResult(BaseModel):
    """What a ``send`` did — with the one fact a coding agent must not get wrong.

    ``provider_sees_this`` is that fact. A turn answered by an AI Matrx agent is
    invisible to Claude Code, Codex, Cursor and VS Code: their transcripts never
    learn it happened. An agent that read an answer here and told the person "I
    have updated the session" would be inventing. So the flag is on the wire, and
    the ``detail`` sentence says it in words as well.
    """

    model_config = ConfigDict(extra="forbid")

    state: BridgeSendState
    target: BridgeSendTarget
    conversation_id: UUID
    client_request_id: Annotated[str, Field(min_length=1, max_length=256)]
    """The replay identity this send was filed under — host-supplied or derived.
    Passing it back on a retry collects THIS answer instead of buying another."""
    provider_sees_this: bool
    """False for ``matrx_agent``: the coding tool never receives the turn or the
    answer. True only when a provider runtime actually delivered it."""
    answered_by_agent_id: UUID | None = None
    answered_by_agent_name: Annotated[str, Field(min_length=1, max_length=255)] | None = None
    responder_setting_key: Annotated[str, Field(min_length=1, max_length=128)] | None = None
    used_platform_default: bool = False
    """True when no agent is chosen for coding-conversation replies and the
    platform's default chat agent stood in — announced, never silent."""
    user_message_id: UUID | None = None
    answer_message_id: UUID | None = None
    answer: Annotated[str, Field(max_length=32_000)] = ""
    """The answer's text, so the calling agent can show it in the coding session
    without a second round trip. Truncated to the bound above; when it is,
    ``answer_truncated`` says so and the full turn is at the conversation."""
    answer_truncated: bool = False
    messages_written: Annotated[int, Field(ge=0)] = 0
    """How many canonical rows this turn persisted — the person's own turn and the
    answer. A reader never has to infer it from the two id fields."""


class BridgeDispatchResult(BaseModel):
    """Result of a dispatch-family action.

    ``BridgeResponse``'s ``accepted/duplicates/conflicts/receipts`` counters are
    the RAW-LEDGER receipt and mean nothing for a dispatch verb; reusing them
    (``accepted: 1`` for "the agent answered") is contract-lying. Dispatch
    results land here instead, and each future verb adds its own fields in its
    own lane rather than overloading an existing one.
    """

    model_config = ConfigDict(extra="forbid")

    action: BridgeAction
    status: Literal["completed", "accepted", "in_flight", "refused"]
    runtime: BridgeRuntimeKind | None = None
    capabilities: BridgeCapabilityReport | None = None
    handoff: BridgeHandoffResult | None = None
    send: BridgeSendResult | None = None
    detail: Annotated[str, Field(min_length=1, max_length=2048)] | None = None


class BridgeHealth(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1] = 1
    status: Literal["ok"] = "ok"
    provider: BridgeProvider
    capabilities: BridgeCapabilities
    checkpoint: BridgeCheckpoint | None = None


SYNC_VERDICT_CODES: frozenset[str] = frozenset(
    {
        "in_sync",
        "partial_by_design",
        "behind_local",
        "behind_cloud",
        "mirror_stale",
        "diverged",
        "quarantined",
        "not_in_cloud",
        "unknown",
    }
)
"""The CLOSED verdict vocabulary of per-conversation sync truth (CS-25 §1).

Three surfaces in two repos render these words. A code outside this set is not
a verdict, and ``unknown`` is mandatory whenever a layer could not be read: a
layer that could not be read is NEVER rendered as agreement.
"""


FORBIDDEN_CLOUD_VERDICTS: frozenset[str] = frozenset({"in_sync"})
"""What the SERVER may never conclude, however good the cloud half looks.

The server sees the entry ledger and the projected messages. It cannot see this
Mac's transcript, the delivery queue, or the local mirror — so ``in_sync`` is
not a verdict it is entitled to reach. Only the engine, which reads all four
layers, may. This is the dead fish (Arman, 2026-09-17: *"A normal DB system
would show me that it can't sync… this thing is a dead fish."*) stated as data
instead of as a comment, so :data:`CLOUD_VERDICT_SENTENCES` cannot grow the
branch by accident.
"""


CLOUD_VERDICT_SENTENCES: dict[tuple[str, str | None], tuple[str, str | None]] = {
    ("partial_by_design", "hook_lane"): (
        "AI Matrx has the shape of this conversation — the {cloud_entries} prompts and "
        "tool calls its hooks recorded, projected into {messages} messages — not the "
        "{transcript_entries}-entry transcript. Hook capture is a summary by design.",
        "Reconcile to import the full transcript file into AI Matrx.",
    ),
    ("behind_local", "no_delivery_ledger_in_cloud"): (
        "AI Matrx has a conversation for this session but no record of a single "
        "delivered entry, so none of the {transcript_entries} entries in your local "
        "transcript are in it. The {messages} messages you see there came from the run "
        "itself, not from this transcript.",
        "Reconcile to deliver the transcript.",
    ),
    ("behind_cloud", "projection_error"): (
        "AI Matrx received all {cloud_entries} entries but {error_entries} never became "
        "messages: {error_reason}.",
        "Reconcile to ask the server to project them again.",
    ),
    ("behind_cloud", "awaiting_projection"): (
        "AI Matrx received all {cloud_entries} entries but {pending_projection} are still "
        "waiting to become messages.",
        "Reconcile to ask the server to project them now.",
    ),
    ("not_in_cloud", None): (
        "This conversation is not in AI Matrx at all — no session, no messages. Its "
        "{transcript_entries} local entries have never been delivered.",
        "Reconcile to send it.",
    ),
    ("unknown", None): (
        "Cannot tell whether this conversation is in sync: {unreadable_layer} could not "
        "be read ({reason}).",
        "Try again in a moment; if it keeps failing, check that AI Matrx is reachable "
        "and you are signed in.",
    ),
}
"""VERBATIM CS-25 §2 wording for the verdicts the CLOUD HALF can reach.

Keyed by ``(code, reason)``; the value is ``(sentence template, remedy)``, and a
``None`` remedy means the row has none. The rows this table omits
(``mirror_stale``, ``diverged``, ``quarantined``, ``in_sync``) need the
transcript, the delivery queue or the mirror to decide, so they belong to the
engine door that reads those layers (§5) — not to this server.

A ``{substitution}`` this server cannot see is left in the rendered sentence as
its own placeholder rather than filled with a guessed number: the engine, which
holds the transcript, substitutes it before anything is shown to a person. A
fabricated count would be the same lie in a politer voice.
"""


class BridgeProjectionErrorGroup(BaseModel):
    """One ``projection_error`` shape, and how many entries carry it."""

    model_config = ConfigDict(extra="forbid")

    code: str | None = None
    detail: str | None = None
    count: int


class BridgeDiagnosis(BaseModel):
    """What AI Matrx actually holds for ONE provider session (CS-25 §4).

    Every count here is read from the cloud's own rows. The verdict is computed
    from those rows ALONE: see :data:`FORBIDDEN_CLOUD_VERDICTS` for the one
    conclusion this half is never entitled to reach.
    """

    model_config = ConfigDict(extra="forbid")

    schema_version: int = 1
    provider_session_id: str
    session_present: bool
    conversation_id: UUID | None = None
    fidelity: str | None = None
    status: str | None = None
    last_seen_at: datetime | None = None
    entries: int
    projected_entries: int
    skipped_entries: int
    pending_entries: int
    error_entries: int
    projection_errors: list[BridgeProjectionErrorGroup] = Field(default_factory=list)
    last_entry_at: datetime | None = None
    last_entry_id: str | None = None
    messages: int
    last_position: int | None = None
    last_message_at: datetime | None = None
    cloud_verdict: str
    cloud_sentence: str
    cloud_remedy: str | None = None


class BridgeReprojection(BaseModel):
    """The result of re-entering the ONE projector over a session's stuck rows.

    Idempotent by construction: it only ever examines entries whose
    ``projection_status`` is ``error`` or ``pending``, so a second pass over an
    already-healed session examines nothing and returns the same diagnosis.
    """

    model_config = ConfigDict(extra="forbid")

    schema_version: int = 1
    examined: int
    projected: int
    skipped: int
    still_error: int
    diagnosis: BridgeDiagnosis


class BridgeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1] = 1
    action: BridgeAction
    provider: BridgeProvider
    # Every response carries what this server implements, so no client ever
    # hardcodes an action list (there is no version number to negotiate).
    supported_actions: list[BridgeAction] = Field(
        default_factory=lambda: sorted(IMPLEMENTED_ACTIONS, key=lambda member: member.value)
    )
    refusal: BridgeRefusal | None = None
    dispatch: BridgeDispatchResult | None = None
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
    diagnosis: BridgeDiagnosis | None = None
    reprojection: BridgeReprojection | None = None
    deleted: bool = False
    hook_specific_output: dict[str, JsonValue] | None = Field(
        default=None,
        serialization_alias="hookSpecificOutput",
    )
