"""TUI-side per-session state manager.

This module owns everything the TUI needs to know about its live sessions:

- :class:`SessionRecord` — the per-session view model (cache of server state
  plus TUI-only fields like unread event count, queued messages, draft
  text, and transcript entries).
- :class:`SessionsManager` — the single coordinator for incoming wire
  events, per-session transcript state, and the per-session reactive
  projection. It replaces ~15 scattered methods that used to live on
  ``DreadnodeTextualApp``.

The design matches the "session manager / chat controller" pattern that
``docs/later/TUI_RUNTIME_SESSIONS.MD`` Phases 1-3 called out as missing.
The server already has a rich per-session graph (``SessionRuntime`` /
``SessionTurnCoordinator`` / ``EventBus`` / etc.). The TUI now
has its own counterpart as a *single* manager — it doesn't need the
server's level of concurrency machinery because the runtime WebSocket
client already mediates transport.

Boundaries:

- The manager owns the ``sessions`` dict, the transient
  ``tool_call_widgets`` dict, and ``last_auth_error`` tracking.
- UI coupling goes through :class:`SessionsUiPort` — widget lookups,
  ``call_after_refresh`` scheduling, flash/activity writes, and
  composer enable/disable. Nothing else in this module knows about
  Textual.
- App-level reactives (``active_session_id``, ``authenticated``,
  ``show_thinking``, ``last_input_tokens``) and the shared app-global
  ``TurnLifecycle`` stay on the app and are accessed through
  :class:`SessionsContextPort`.
- The auto-approve path for allowlisted tools calls back into the app's
  outgoing chat layer via :class:`ChatResponder` — one narrow method.

``DreadnodeTextualApp`` continues to expose 1-line delegation methods
(``_handle_event``, ``_session_turn_state``, ``_append_transcript``, ...)
that forward to this manager. That keeps the ~40 existing test call
sites working without a test rewrite: tests that do
``app._handle_event(...)`` still hit a real method that routes into
the manager, and tests that do ``app._handle_event = MagicMock()``
still shadow the delegation at instance level.
"""

import json
import typing as t
from dataclasses import dataclass, field

from loguru import logger

from dreadnode.app.api.client import AuthenticationError
from dreadnode.app.api.models import HumanPrompt
from dreadnode.app.client.models import SessionInfo
from dreadnode.app.tui import wire_events as we
from dreadnode.app.tui.error_handler import (
    ErrorHandler,
    classify_error_message,
    enrich_error_body,
    split_missing_api_key_message,
)
from dreadnode.app.tui.tool_format import (
    _format_tool_label,
    _summarize_tool_result,
)
from dreadnode.app.tui.turn_lifecycle import TurnPhase as LifecyclePhase
from dreadnode.app.tui.turn_reducer import (
    ToolRun,
    TurnState,
    reduce_event,
    reduce_human_prompt_response,
)
from dreadnode.app.tui.turn_state_phase import (
    TurnStatePhase,
    is_blocked_phase,
    is_running_phase,
    lifecycle_projection_for_phase,
    phase_for_human_prompt,
    phase_from_wire,
    subscription_reason_for_phase,
)
from dreadnode.app.tui.widgets import (
    ConversationView,
    HumanPromptWidget,
    MessageQueue,
    StreamingDraft,
    ToolProgress,
)
from dreadnode.app.tui.widgets.composer import ComposerInput
from dreadnode.app.tui.widgets.tool import ToolCall
from dreadnode.app.tui.wire_events import parse_wire_event
from dreadnode.generators.message import Message

DN_MODEL_ACCESS_CHANGED_MESSAGE = "Model no longer available — your access may have changed"

# =============================================================================
# Wire event helpers — small utilities used by handle_event
# =============================================================================


def _last_input_tokens_from(event: we.WireEvent) -> int | None:
    """Extract the ``usage.input_tokens`` value from events that carry it.

    This is the size of the prompt the model just saw — the right value to
    feed the context-window gauge. Returns ``None`` for events without
    usage or with a zero/missing ``input_tokens`` so callers can no-op
    rather than blank the gauge mid-turn.
    """
    if isinstance(event, (we.GenerationStep, we.GenerationEnd)):
        return event.data.usage.input_tokens or None
    return None


def _reasoning_from_extra(extra: dict[str, t.Any] | None) -> str | None:
    """Extract reasoning/thinking content from a generation event's ``extra`` dict.

    OpenAI/DeepSeek put this as ``extra.reasoning_content`` (plain string).
    Anthropic puts it in ``extra.thinking_blocks`` as a list of
    ``{type, thinking}`` dicts.
    """
    if not isinstance(extra, dict):
        return None
    rc = extra.get("reasoning_content")
    if isinstance(rc, str) and rc:
        return rc
    blocks = extra.get("thinking_blocks")
    if isinstance(blocks, list):
        parts = [
            b["thinking"]
            for b in blocks
            if isinstance(b, dict) and isinstance(b.get("thinking"), str)
        ]
        return "\n".join(parts) if parts else None
    return None


def _coerce_tool_args(args: t.Any) -> dict[str, t.Any]:
    """Normalize ``tool_call.arguments`` (dict or str) to a dict for display."""
    if isinstance(args, dict):
        return args
    if isinstance(args, str) and args.strip():
        return {"raw": args.strip()}
    return {}


def _tool_name_args_from_run_or_wire(
    run: "ToolRun | None",
    tc: we.WireToolCall,
) -> tuple[str, dict[str, t.Any]]:
    """Resolve tool name + args for display, preferring the matched run.

    When an ``in-flight`` run exists (matched by tool_call_id back to
    the prior ``ToolStart`` event), its cached args are the canonical
    source — ``ToolEnd``/``ToolError`` events typically don't re-send
    ``arguments``. Fallback is whatever the wire tool_call carries.
    """
    if run is not None:
        return run.tool_name, run.tool_args
    return tc.name or "tool", _coerce_tool_args(tc.arguments)


def _make_tool_message(
    *,
    tool_name: str,
    tool_args: dict[str, t.Any],
    body: str,
    summary: str | None,
    tool_call_id: str | None = None,
    error: str | None = None,
    error_type: str | None = None,
    report_url: str | None = None,
) -> Message:
    """Build a ``role="tool"`` Message for the transcript.

    The label the conversation view renders (``"read(README.md)"``) is
    computed at render time from ``tool_name`` + ``tool_args`` in
    metadata, not baked into the content. The ``summary`` line is the
    ``_summarize_tool_result`` one-liner shown as the row's meta
    (``"Read 42 lines."``). When ``error`` is set the tool ran to
    completion but reported a failure — the conversation view picks
    this up to render the call with the same red treatment used for
    uncaught exceptions.

    ``report_url`` is UI-only context computed from the active platform
    session. Report title/body/format stay in ``tool_args``.
    """
    metadata: dict[str, t.Any] = {"tool_name": tool_name, "tool_args": tool_args}
    if summary is not None:
        metadata["summary"] = summary
    if error:
        metadata["error"] = error
    if error_type:
        metadata["error_type"] = error_type
    if report_url:
        metadata["report_url"] = report_url
    return Message(
        role="tool",
        content=body,
        tool_call_id=tool_call_id,
        metadata=metadata,
    )


def _make_error_message(*, title: str, body: str) -> Message:
    """Build a ``role="system"`` Message flagged as an inline error row.

    The conversation view looks for ``metadata["error"] is True`` and
    uses ``metadata["error_title"]`` as the label. Kept at module
    scope so ``handle_event`` branches can swap ``TranscriptEntry(kind="error", …)``
    out without each caller repeating the metadata boilerplate.
    """
    return Message(
        role="system",
        content=body,
        metadata={"error": True, "error_title": title},
    )


# =============================================================================
# Transcript materialization from persisted messages
# =============================================================================


def _transcript_from_messages(
    messages: list[dict[str, t.Any]],
    *,
    report_url: str | None = None,
) -> list[Message]:
    """Build :class:`Message` objects from a server ``/messages`` response.

    Used when the TUI needs to materialize a transcript it doesn't have
    cached yet: cold-start session switch, ``--resume`` flag, and after
    ``/compact`` rewrites server history. The local streaming pipeline
    (``SessionsManager.handle_event``) normally appends entries as they
    happen — this function covers the case where there's no live
    stream to watch.

    Compaction rows are modelled as ``role="system"`` messages with a
    ``compaction`` metadata flag so the conversation view can render
    them as dividers. Empty assistant messages (tool-only turns) and
    prompt-style system messages are dropped since they have no display
    shape.
    """
    out: list[Message] = []
    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "") or ""
        metadata = msg.get("metadata") or {}

        if metadata.get("compaction"):
            count = metadata.get("messages_compacted", "?")
            trigger = metadata.get("trigger", "manual")
            label = "Auto-compacted" if trigger == "threshold" else "Compacted"
            out.append(
                Message(
                    role="system",
                    content=f"{label} — {count} messages summarized",
                    metadata={"compaction": True, "expanded_detail": content},
                )
            )
            continue
        if role == "user":
            out.append(Message(role="user", content=content))
            continue
        if role == "assistant":
            if not content.strip():
                continue  # Skip empty assistant messages (tool-only turns)
            out.append(Message(role="assistant", content=content))
            continue
        if role == "tool":
            tool_name = msg.get("tool_name") or "tool"
            tool_args = _coerce_tool_args(msg.get("tool_args"))
            summary = _summarize_tool_result(tool_name, tool_args, content) if content else None
            tool_metadata: dict[str, t.Any] = {
                "tool_name": tool_name,
                "tool_args": tool_args,
            }
            if summary is not None:
                tool_metadata["summary"] = summary
            if tool_name == "report":
                if report_url:
                    tool_metadata["report_url"] = report_url
            # Surface persisted error metadata (set by Message.from_model
            # when the tool returned an ErrorModel) so transcript replay
            # renders failed calls with the same red treatment as the
            # live event stream.
            persisted_error = metadata.get("error")
            if persisted_error:
                tool_metadata["error"] = persisted_error
            persisted_error_type = metadata.get("error_type")
            if persisted_error_type:
                tool_metadata["error_type"] = persisted_error_type
            out.append(
                Message(
                    role="tool",
                    content=content,
                    tool_call_id=msg.get("tool_call_id"),
                    metadata=tool_metadata,
                )
            )
            continue
        # ``role == "system"`` — system prompts are not shown in transcript.

    return out


def _apply_session_info_to_turn_state(state: TurnState, info: SessionInfo) -> None:
    """Pull usage roll-ups from ``SessionInfo`` into ``TurnState``.

    Pure function (no I/O, no manager state) so the seed contract is
    testable in isolation: ``total_cost_usd is None`` flips ``cost_unknown``
    and zeros the cost accumulator (the live wire path can't recover what
    the source already declared unknown); a known cost replaces both.
    ``last_generation_input_tokens`` only seeds when the live wire hasn't
    received anything yet — once we have a live value it's the authoritative
    "current context" and shouldn't be clobbered by a potentially stale
    snapshot.
    """
    if info.last_generation_input_tokens is not None and state.usage_last_input_tokens == 0:
        state.usage_last_input_tokens = info.last_generation_input_tokens
    state.usage_tool_call_count = info.total_tool_call_count
    if info.total_cost_usd is None:
        state.cost_unknown = True
        state.usage_cost_usd = 0.0
    else:
        state.cost_unknown = False
        state.usage_cost_usd = info.total_cost_usd


# =============================================================================
# SessionRecord — the per-session view model
# =============================================================================


@dataclass(slots=True)
class SessionRecord:
    """UI-side cache for one runtime session.

    Holds the server's :class:`SessionInfo` snapshot, the current model,
    any loaded transcript entries, TUI-only fields (unread event count,
    queued messages, draft state, inline activity), and the per-session
    reduced :class:`TurnState`.

    Title and preview live on ``info`` — there is no local override field.
    ``/rename`` writes ``info.title`` optimistically and persists to the
    platform in a background worker; the narrow race where a refresh
    races in front of the persist is acceptable because the platform
    write is a single round-trip.
    """

    info: SessionInfo
    model: str
    transcript: list[Message] = field(default_factory=list)
    turn_count: int = 0
    queued_messages: list[str] = field(default_factory=list)
    allowlisted_tools: set[str] = field(default_factory=set)
    unread_events: int = 0
    turn_state: TurnState | None = None
    subscribed: bool = False
    subscription_reason: str | None = None
    inline_activity: str | None = None
    last_seq: int | None = None
    resync_required: bool = False
    resync_summary: str | None = None

    def __post_init__(self) -> None:
        if self.turn_state is None:
            self.turn_state = TurnState.empty(self.info.session_id)

    def display_title(self) -> str:
        """Label for this session — never empty.

        Mirrors the frontend monitoring grid (columns.ts:138): the
        platform-persisted ``info.title`` if set, otherwise a generic
        ``"<agent> session"`` fallback so the row always carries a
        usable identity even before the user names it via ``/rename``.
        Title is the *label* — content samples render through
        :meth:`display_preview` alongside the title, not as a fallback
        for it.
        """
        if self.info.title:
            return self.info.title
        agent = self.info.agent or "default"
        return f"{agent} session"

    def display_preview(self) -> str | None:
        """First user-message snippet, or None when no turn has been sent.

        Prefers the server-populated denormalized preview (rule
        SES-LST-011): set once on first user-message persist, frozen
        thereafter, survives reload. Falls back to walking the local
        transcript so a freshly sent in-memory turn shows its prompt
        before the platform has acknowledged the persist.
        """
        if self.info.preview:
            return self.info.preview
        for entry in self.transcript:
            if entry.role == "user" and entry.content:
                return entry.content
        return None


@dataclass(slots=True)
class SessionStateBundle:
    """Snapshot of per-runtime session state for swap on connect/disconnect.

    The ``RuntimeConnectionManager`` stashes one of these before swapping
    between the local and remote runtime clients and restores it when
    swapping back, so each runtime keeps its own independent session
    view.
    """

    sessions: dict[str, SessionRecord]
    active_session_id: str | None


# =============================================================================
# Ports
# =============================================================================


class SessionsUiPort(t.Protocol):
    """UI widget access needed by :class:`SessionsManager`.

    These are pure view-side operations: query for a named widget, schedule
    work after the next refresh, and emit flash / activity messages.
    Nothing in this port carries business state.
    """

    def query_draft(self) -> StreamingDraft: ...

    def query_composer(self) -> ComposerInput: ...

    def query_conversation(self) -> ConversationView: ...

    def query_prompt_widget(self) -> HumanPromptWidget: ...

    def query_tool_progress(self) -> ToolProgress: ...

    def query_message_queue(self) -> MessageQueue: ...

    def call_after_refresh(
        self,
        callback: t.Callable[..., t.Any],
        /,
        *args: t.Any,
        **kwargs: t.Any,
    ) -> None: ...

    def flash(self, message: str, *, severity: str = "info") -> None: ...

    def write_activity(self, message: str, *, style: str = "info") -> None: ...

    def set_composer_enabled(self, enabled: bool) -> None: ...

    def append_transcript(
        self,
        entry: Message,
        session_id: str,
        *,
        scroll: bool = True,
    ) -> None:
        """Append a message to the session's transcript and, if the session is
        active, schedule a conversation-widget append.

        The implementation lives in ``DreadnodeTextualApp._append_transcript``
        because tests rely on being able to patch that method with a
        ``MagicMock()`` to observe event-to-transcript routing. The UI
        adapter on the app calls through at invocation time (late binding)
        so the patches still take effect even when the manager dispatches.
        """
        ...


class SessionsContextPort(t.Protocol):
    """App-level read/write state needed by :class:`SessionsManager`.

    Keeps the manager free of direct reactive access. The app implements
    this by wrapping its reactives (``active_session_id``,
    ``last_input_tokens``, ``authenticated``, ``_show_thinking``) plus the
    shared ``TurnLifecycle``.
    """

    def active_session_id(self) -> str | None: ...

    def set_active_session_id(self, session_id: str | None) -> None: ...

    def update_context(self) -> None: ...

    def last_input_tokens(self) -> int: ...

    def set_last_input_tokens(self, tokens: int) -> None: ...

    def tool_call_count(self) -> int: ...

    def set_tool_call_count(self, count: int) -> None: ...

    def cost_usd(self) -> float: ...

    def set_cost_usd(self, cost: float) -> None: ...

    def cost_unknown(self) -> bool: ...

    def set_cost_unknown(self, unknown: bool) -> None: ...

    def show_thinking(self) -> bool: ...

    def authenticated(self) -> bool: ...

    def current_model(self) -> str: ...

    def apply_model_change(self, model: str) -> None:
        """Switch the app's active model after restoring a session."""
        ...

    def turn_enter_awaiting(self, status: str) -> None: ...

    def turn_sync_projection(
        self,
        *,
        owner: str | None,
        phase: LifecyclePhase,
        status: str,
        authenticated: bool,
    ) -> None: ...

    def report_url(self, session_id: str) -> str | None:
        """Build a deep-link URL into the platform Reports tab for the
        given session, or None when the platform context isn't available
        (unauthenticated, local-only, or no API client wired). The manager
        uses this to render a clickable hyperlink under report tool results.
        """
        ...


class SessionsTransportPort(t.Protocol):
    """Runtime transport access for the session subscription controller.

    Narrow view of ``ManagedRuntimeClient`` that the manager needs to drive
    the per-session subscription policy — nothing else from the client
    leaks through. The app's adapter delegates each call to the active
    ``managed_client`` at invocation time so the policy tracks
    local/remote runtime switching without re-wiring.
    """

    def is_runtime_started(self) -> bool: ...

    def desired_session_subscriptions(self) -> set[str]: ...

    async def subscribe_session(self, session_id: str) -> None: ...

    async def unsubscribe_session(self, session_id: str) -> None: ...

    def latest_session_snapshot(self, session_id: str) -> dict[str, t.Any] | None: ...

    def latest_session_resync_required(self, session_id: str) -> dict[str, t.Any] | None: ...

    async def fetch_session_messages(self, session_id: str) -> list[dict[str, t.Any]]: ...

    async def list_sessions(self, *, include_platform: bool = False) -> list[SessionInfo]: ...

    async def get_session(self, session_id: str) -> SessionInfo | None: ...


class SessionsModelAccessPort(t.Protocol):
    """Optional app actions for dn/* model access refresh flows."""

    def refresh_platform_model_access(self) -> None: ...


# =============================================================================
# SessionsManager
# =============================================================================


class SessionsManager:
    """Single coordinator for TUI per-session state.

    Owns the ``sessions`` dict and all behavior that reads or mutates per-
    session state: event handling, transcript updates, draft projection,
    unread counts, and the transient in-flight ``ToolCall`` widget cache.

    The manager never touches Textual widgets directly — it goes through
    :class:`SessionsUiPort`. The manager never reads app-global reactives
    directly — it goes through :class:`SessionsContextPort`. Auto-approve
    calls go through :class:`ChatResponder`. The existing stateless
    :class:`ErrorHandler` is passed in directly.
    """

    def __init__(
        self,
        *,
        ui: SessionsUiPort,
        context: SessionsContextPort,
        transport: SessionsTransportPort,
        error_handler: ErrorHandler,
        model_access: SessionsModelAccessPort | None = None,
    ) -> None:
        self._ui = ui
        self._context = context
        self._transport = transport
        self._error_handler = error_handler
        self._model_access = model_access
        self._sessions: dict[str, SessionRecord] = {}
        self._tool_call_widgets: dict[str, ToolCall] = {}
        self._last_auth_error: dict[str, str] = {}

    # ------------------------------------------------------------------
    # Sessions dict
    # ------------------------------------------------------------------

    @property
    def sessions(self) -> dict[str, SessionRecord]:
        """The live sessions dict. Mutated in place by the manager and app."""
        return self._sessions

    def replace_sessions(self, sessions: dict[str, SessionRecord]) -> None:
        """Replace the sessions dict wholesale (used by stash/restore and refresh).

        This atomically swaps the whole dict rather than mutating in place,
        so any external references must be refreshed via this method.
        """
        self._sessions = sessions

    # ------------------------------------------------------------------
    # Stash / restore for runtime client swap
    # ------------------------------------------------------------------

    def stash_state(self) -> SessionStateBundle:
        """Capture the current per-runtime session state as an opaque bundle.

        Called by :class:`RuntimeConnectionManager` before swapping the
        active runtime client — lets each runtime keep its own session
        view across connect/disconnect cycles.
        """
        return SessionStateBundle(
            sessions=dict(self._sessions),
            active_session_id=self._context.active_session_id(),
        )

    def restore_state(self, bundle: SessionStateBundle) -> None:
        """Restore a previously stashed bundle and re-sync the view."""
        self._sessions = bundle.sessions
        self._context.set_active_session_id(bundle.active_session_id)
        if bundle.active_session_id is not None:
            self.clear_session_unread(bundle.active_session_id)
        self.sync_conversation()
        self.sync_active_session_projection()
        self._context.update_context()

    # ------------------------------------------------------------------
    # Refresh from server (session list hydration)
    # ------------------------------------------------------------------

    async def refresh_from_server(self, *, include_platform: bool = False) -> None:
        """Pull the session list from the runtime server and reconcile.

        Preserves any locally-cached transcript and TUI-only per-session
        state (queued messages, allowlist, unread count, draft, turn
        state, subscription flag) that the server doesn't know about.
        Clears stale transcripts when ``message_count`` has diverged.
        Promotes the resulting first session to active if the previous
        ``active_session_id`` no longer exists. Lazy-loads the active
        session's transcript if the cache is empty.

        ``include_platform`` is forwarded to the runtime server; set it
        to True only when the caller needs the full persisted history
        (session picker, ``/sessions`` slash command). Fast paths — boot,
        runtime swap, auth refresh — leave it False to avoid a ~500ms
        platform round-trip.
        """
        session_infos = await self._transport.list_sessions(include_platform=include_platform)
        logger.debug("Sessions refresh | count={}", len(session_infos))
        current_model = self._context.current_model()
        refreshed: dict[str, SessionRecord] = {}
        for si in session_infos:
            record = self._sessions.get(si.session_id)
            if record is None:
                refreshed[si.session_id] = SessionRecord(info=si, model=current_model)
                continue
            transcript = record.transcript
            if si.message_count != len(transcript):
                transcript = []
            refreshed[si.session_id] = SessionRecord(
                info=si,
                model=record.model,
                transcript=transcript,
                turn_count=record.turn_count,
                queued_messages=list(record.queued_messages),
                allowlisted_tools=set(record.allowlisted_tools),
                unread_events=record.unread_events,
                turn_state=record.turn_state,
                subscribed=record.subscribed,
                subscription_reason=record.subscription_reason,
                inline_activity=record.inline_activity,
                last_seq=record.last_seq,
                resync_required=record.resync_required,
                resync_summary=record.resync_summary,
            )
        self._sessions = refreshed

        active_id = self._context.active_session_id()
        if active_id not in self._sessions:
            active_id = next(iter(self._sessions), None)
            self._context.set_active_session_id(active_id)

        if active_id is not None:
            self.clear_session_unread(active_id)
            active_model = self._sessions[active_id].model
            if active_model != current_model:
                self._context.apply_model_change(active_model)
            await self.load_transcript(active_id)

        await self.sync_runtime_session_subscriptions()
        self.sync_active_session_projection()
        self._context.update_context()

    async def ensure_session_loaded(self, session_id: str) -> SessionRecord | None:
        """Make sure ``session_id`` exists in ``self._sessions``, fetching by id if needed.

        Used by the resume flow to handle sessions that aren't in the
        in-memory list (platform-persisted, legacy local store, etc.)
        without paying for a bulk session refresh.
        """
        record = self._sessions.get(session_id)
        if record is not None:
            return record
        info = await self._transport.get_session(session_id)
        if info is None:
            return None
        record = SessionRecord(info=info, model=self._context.current_model())
        self._sessions[info.session_id] = record
        return record

    @property
    def tool_call_widgets(self) -> dict[str, ToolCall]:
        """The transient in-flight ToolCall widget cache keyed by tool_call_id."""
        return self._tool_call_widgets

    @property
    def last_auth_error(self) -> dict[str, str]:
        """Most recent authentication error text per session, used to dedupe duplicate surfacing."""
        return self._last_auth_error

    # ------------------------------------------------------------------
    # Per-session state helpers
    # ------------------------------------------------------------------

    def is_active_session(self, session_id: str) -> bool:
        return self._context.active_session_id() == session_id

    def session_turn_state(self, session_id: str) -> TurnState | None:
        session = self._sessions.get(session_id)
        if session is None:
            return None
        if session.turn_state is None:
            session.turn_state = TurnState.empty(session_id)
        return session.turn_state

    def set_session_turn_state(self, session_id: str, state: TurnState) -> None:
        session = self._sessions.get(session_id)
        if session is not None:
            session.turn_state = state
            self._context.update_context()

    def abort_running_tools(self, session_id: str) -> None:
        """Finalize in-flight tools for a session on interrupt.

        Marks every ``running`` ``ToolRun`` as ``errored`` and drops
        the corresponding entries from :attr:`_tool_call_widgets`. The
        widget cache is populated on ``tool_start`` and only popped on
        ``tool_end``/``tool_error``; cancelled tools never see either
        event, so without this cleanup their entries accumulate for
        the session's lifetime. Callers (currently only
        :class:`TurnCoordinator.interrupt`) should treat this as the
        single owner of the interrupt-time tool cleanup.
        """
        state = self.session_turn_state(session_id)
        if state is None:
            return
        for key, run in list(state.tool_runs.items()):
            if run.status == "running":
                run.status = "errored"
                self._tool_call_widgets.pop(key, None)
        state.phase = TurnStatePhase.IDLE

    def mark_session_unread(self, session_id: str) -> None:
        if self.is_active_session(session_id):
            return
        session = self._sessions.get(session_id)
        if session is not None:
            session.unread_events += 1
            self._context.update_context()

    def clear_session_unread(self, session_id: str) -> None:
        session = self._sessions.get(session_id)
        if session is not None:
            session.unread_events = 0
            self._context.update_context()

    # ------------------------------------------------------------------
    # Subscription policy (TUI_RUNTIME_SESSIONS.MD Phase 2)
    # ------------------------------------------------------------------

    def background_session_status(self) -> str:
        """Summarize activity across non-active sessions for the context bar."""
        blocked = 0
        running = 0
        unread = 0
        stale = 0
        for session_id, session in self._sessions.items():
            if self.is_active_session(session_id):
                continue
            state = self.session_turn_state(session_id)
            if state is not None:
                if is_blocked_phase(state.phase):
                    blocked += 1
                elif is_running_phase(state.phase):
                    running += 1
            if session.unread_events > 0:
                unread += 1
            if session.resync_required:
                stale += 1

        parts: list[str] = []
        if blocked:
            parts.append(f"{blocked} waiting")
        if running:
            parts.append(f"{running} running")
        if unread:
            parts.append(f"{unread} unread")
        if stale:
            parts.append(f"{stale} stale")
        return " · ".join(parts)

    def subscription_reason_for_session(
        self,
        session_id: str,
        session: SessionRecord,
    ) -> str | None:
        """Return the subscription reason for a session, or ``None`` if idle.

        Policy: always subscribe the active session, any session with a
        running or awaiting turn, and any session with unread events.
        Sessions that match none of these are left unsubscribed so the
        transport doesn't bulk-stream every historical session.
        """
        if self.is_active_session(session_id):
            return "active"
        state = self.session_turn_state(session_id)
        if state is not None:
            reason = subscription_reason_for_phase(state.phase)
            if reason is not None:
                return reason
        if session.unread_events > 0:
            return "unread"
        return None

    def apply_runtime_session_transport_state(self, session_id: str) -> None:
        """Project the transport's latest session snapshot onto stored session state.

        Called by :meth:`sync_runtime_session_subscriptions` after a
        subscribe settles. Copies the broker's latest sequence, pending
        prompt, turn phase, and draft usage tokens into the reducer
        :class:`TurnState` for the session. Also flashes a warning if a
        *new* pending prompt arrives on a background session.
        """
        session = self._sessions.get(session_id)
        if session is None:
            return

        session.resync_required = False
        session.resync_summary = None
        resync = self._transport.latest_session_resync_required(session_id)
        if resync is not None:
            session.resync_required = True
            after_seq = resync.get("after_seq")
            latest_seq = resync.get("latest_seq")
            session.resync_summary = f"replay gap after {after_seq} (latest {latest_seq})"

        snapshot = self._transport.latest_session_snapshot(session_id)
        if snapshot is None:
            return

        latest_seq = snapshot.get("latest_seq")
        if isinstance(latest_seq, int):
            session.last_seq = latest_seq

        state = self.session_turn_state(session_id) or TurnState.empty(session_id)
        prompt_payload = snapshot.get("pending_prompt")
        previous_prompt = state.pending_human_prompt
        pending_prompt: HumanPrompt | None = None
        if isinstance(prompt_payload, HumanPrompt):
            pending_prompt = prompt_payload
        elif isinstance(prompt_payload, dict):
            try:
                pending_prompt = HumanPrompt.model_validate(prompt_payload)
            except Exception:
                logger.opt(exception=True).warning(
                    "Invalid session snapshot prompt | session={}",
                    session_id[:8],
                )

        state.pending_human_prompt = pending_prompt
        turn_phase = snapshot.get("turn_phase")
        if pending_prompt is not None:
            state.phase = phase_for_human_prompt()
        elif isinstance(turn_phase, str):
            parsed_phase = phase_from_wire(turn_phase)
            if parsed_phase is not None:
                state.phase = parsed_phase

        draft_state = snapshot.get("draft_state")
        if isinstance(draft_state, dict):
            last_input_tokens = draft_state.get("last_generation_input_tokens")
            if isinstance(last_input_tokens, int) and state.usage_last_input_tokens == 0:
                state.usage_last_input_tokens = last_input_tokens

        self.set_session_turn_state(session_id, state)
        if (
            pending_prompt is not None
            and previous_prompt is None
            and not self.is_active_session(session_id)
        ):
            self.mark_session_unread(session_id)
            self._ui.flash(
                f"Session {session_id[:8]} awaiting input",
                severity="warning",
            )

    async def sync_runtime_session_subscriptions(self) -> None:
        """Reconcile the transport's subscription set with the desired policy.

        For each known session, compute its desired subscription reason
        from the current turn state and unread count. Unsubscribe sessions
        that no longer need a live stream, subscribe those that do, and
        then project the latest broker snapshot onto each subscribed
        session's reducer state.

        Idempotent — safe to call on every session-state change.
        """
        if not self._transport.is_runtime_started():
            for session in self._sessions.values():
                session.subscribed = False
                session.subscription_reason = None
                session.resync_required = False
                session.resync_summary = None
            self._context.update_context()
            return

        desired: dict[str, str] = {}
        for session_id, session in self._sessions.items():
            reason = self.subscription_reason_for_session(session_id, session)
            if reason is not None:
                desired[session_id] = reason

        current = self._transport.desired_session_subscriptions()

        for session_id in sorted(current - set(desired)):
            try:
                await self._transport.unsubscribe_session(session_id)
            except Exception:
                logger.opt(exception=True).warning(
                    "Session unsubscribe sync failed | session={}",
                    session_id[:8],
                )

        for session_id in sorted(set(desired) - current):
            try:
                await self._transport.subscribe_session(session_id)
            except Exception:
                logger.opt(exception=True).warning(
                    "Session subscribe sync failed | session={} reason={}",
                    session_id[:8],
                    desired[session_id],
                )

        effective = self._transport.desired_session_subscriptions()
        for session_id, session in self._sessions.items():
            session.subscribed = session_id in effective
            session.subscription_reason = desired.get(session_id) if session.subscribed else None
            if not session.subscribed:
                session.resync_required = False
                session.resync_summary = None
                continue
            self.apply_runtime_session_transport_state(session_id)

        self._context.update_context()

    def commit_session_draft_text(self, session_id: str, *, from_widget: bool) -> None:
        """Flush a live draft stream into the transcript and reset draft state."""
        state = self.session_turn_state(session_id)
        content = ""
        if from_widget:
            draft = self._ui.query_draft()
            content = draft.finish_stream()
            if not content and state is not None:
                content = state.draft_text
            draft.clear_stream()
        elif state is not None:
            content = state.draft_text

        if state is not None:
            state.draft_text = ""
            if state.phase is TurnStatePhase.GENERATING:
                state.phase = TurnStatePhase.IDLE

        if content.strip():
            self._ui.append_transcript(
                Message(role="assistant", content=content),
                session_id,
            )

    def apply_human_prompt_response(self, session_id: str, action: str) -> None:
        """Apply a local human-prompt response to the per-session turn state."""
        state = self.session_turn_state(session_id)
        if state is None:
            return
        self.set_session_turn_state(
            session_id,
            reduce_human_prompt_response(state, action=action),
        )

    def active_human_prompt(self, session_id: str | None = None) -> HumanPrompt | None:
        """Return the pending human prompt for the given (or active) session."""
        sid = session_id or self._context.active_session_id()
        if not sid:
            return None
        state = self.session_turn_state(sid)
        if state is None:
            return None
        return state.pending_human_prompt

    # ------------------------------------------------------------------
    # Per-session message queue
    # ------------------------------------------------------------------

    def enqueue_message(self, message: str) -> None:
        """Add a message to the active session's outbound queue."""
        sid = self._context.active_session_id()
        if not sid:
            return
        session = self._sessions.get(sid)
        if session is None:
            return
        session.queued_messages.append(message)
        self.sync_queue()

    def has_queued_messages(self) -> bool:
        """True if the active session has at least one queued message."""
        sid = self._context.active_session_id()
        if not sid:
            return False
        session = self._sessions.get(sid)
        if session is None:
            return False
        return bool(session.queued_messages)

    def retract_last_queued(self) -> str | None:
        """Pop and return the last queued message for the active session."""
        sid = self._context.active_session_id()
        if not sid:
            return None
        session = self._sessions.get(sid)
        if session is None:
            return None
        queue = session.queued_messages
        if not queue:
            return None
        message = queue.pop()
        self.sync_queue()
        return message

    def sync_queue(self) -> None:
        """Refresh the MessageQueue widget from the active session's queue."""
        sid = self._context.active_session_id()
        session = self._sessions.get(sid) if sid else None
        queue = session.queued_messages if session is not None else []
        self._ui.query_message_queue().set_messages(queue)

    # ------------------------------------------------------------------
    # Active-pane projection (TUI_RUNTIME_SESSIONS.MD Phase 3)
    # ------------------------------------------------------------------

    def active_session(self) -> SessionRecord | None:
        """Return the active session record, or ``None`` if no active session."""
        sid = self._context.active_session_id()
        if sid is None:
            return None
        return self._sessions.get(sid)

    def lifecycle_projection_for_state(
        self,
        session_id: str | None,
        state: TurnState | None,
    ) -> tuple[str | None, LifecyclePhase, str]:
        """Translate a session's reducer :class:`TurnState` into the global
        turn-lifecycle shape (owner, phase, status text)."""
        if session_id is None or state is None:
            return (None, LifecyclePhase.IDLE, "Ready")
        phase, status = lifecycle_projection_for_phase(state.phase)
        return (session_id, phase, status)

    def sync_active_session_lifecycle(self) -> None:
        """Push the active session's reduced turn state into the global turn lifecycle."""
        session = self.active_session()
        session_id = session.info.session_id if session is not None else None
        state = self.session_turn_state(session_id) if session_id is not None else None
        owner, phase, status = self.lifecycle_projection_for_state(session_id, state)
        self._context.turn_sync_projection(
            owner=owner,
            phase=phase,
            status=status,
            authenticated=self._context.authenticated(),
        )

    def sync_active_session_projection(self) -> None:
        """Rebuild every visible widget from the active session's stored state.

        This is the active-pane projection: draft text, pending prompt,
        tool progress, inline activity, and the token counter are all
        reloaded from the reducer :class:`TurnState`. Called after session
        switches, resumes, and any structural change that might leave the
        widgets out of sync with the model.
        """
        self.sync_active_session_lifecycle()
        try:
            draft = self._ui.query_draft()
            prompt_widget = self._ui.query_prompt_widget()
            composer = self._ui.query_composer()
            tool_progress = self._ui.query_tool_progress()
            conversation = self._ui.query_conversation()
        except Exception:
            return
        session = self.active_session()
        if session is None:
            draft.clear_stream()
            prompt_widget.hide_prompt()
            composer.placeholder = ""
            tool_progress.hide_tool()
            conversation.clear_activity()
            self._context.set_last_input_tokens(0)
            self._context.set_tool_call_count(0)
            self._context.set_cost_usd(0.0)
            self._context.set_cost_unknown(False)
            return

        state = self.session_turn_state(session.info.session_id)
        if state is None:
            draft.clear_stream()
            prompt_widget.hide_prompt()
            composer.placeholder = ""
            tool_progress.hide_tool()
            conversation.clear_activity()
            self._context.set_last_input_tokens(0)
            self._context.set_tool_call_count(0)
            self._context.set_cost_usd(0.0)
            self._context.set_cost_unknown(False)
            return

        self._context.set_last_input_tokens(state.usage_last_input_tokens)
        self._context.set_tool_call_count(state.usage_tool_call_count)
        self._context.set_cost_usd(state.usage_cost_usd)
        self._context.set_cost_unknown(state.cost_unknown)
        if state.draft_text:
            draft.set_buffer(state.draft_text)
        else:
            draft.clear_stream()

        prompt = state.pending_human_prompt
        if prompt is None:
            prompt_widget.hide_prompt()
            composer.placeholder = ""
            composer.disabled = False
        else:
            prompt_widget.show_prompt(prompt)
            composer.placeholder = "Answer the prompt above"
            composer.disabled = True

        if is_blocked_phase(state.phase):
            tool_progress.hide_tool()
        else:
            self.sync_progress_indicator(state)

        if session.inline_activity:
            conversation.write_activity(session.inline_activity)
        else:
            conversation.clear_activity()

    def commit_draft_to_transcript(self, session_id: str) -> None:
        """Flush live draft text into the transcript and reset draft widget state."""
        self.commit_session_draft_text(session_id, from_widget=True)

    def sync_conversation(self) -> None:
        """Rebuild the ConversationView from the active session's transcript."""
        try:
            conversation = self._ui.query_conversation()
        except Exception:
            return  # Widget already torn down during shutdown
        # Rebuilding removes every ``.entry`` widget — including any
        # in-flight ``ToolCall`` mounted by ``ToolStart``. The cache still
        # holding those references would let a later ``ToolEnd`` call
        # ``complete()`` on an orphan, silently dropping the tool result
        # from the UI. Drop the cache here so the cache-miss fallback
        # in the ``ToolEnd`` branch appends a fresh entry instead.
        self._tool_call_widgets.clear()
        session = self.active_session()
        if session is None:
            conversation.show_empty()
        else:
            conversation.load_session(session.transcript)

    async def load_transcript(
        self,
        session_id: str,
        *,
        force: bool = False,
    ) -> None:
        """Ensure a session's transcript is materialized, then sync the view.

        A transcript and a session are the same thing from the user's
        perspective — the TUI just caches them lazily, because fetching
        every session's full message history up front would be too
        expensive. This collapses the "do I need to rebuild?" check the
        callers used to repeat in four places into a single entry point:

        - ``force=False`` (default): only refetch if the local cache is
          empty and the server reports a non-zero message count. This
          is the "switched to / resumed a session" path.
        - ``force=True``: always refetch. Used after ``/compact`` has
          rewritten the canonical server history.

        Always re-syncs the conversation view afterwards so callers get
        a consistent post-condition regardless of whether a fetch
        happened.
        """
        session = self._sessions.get(session_id)
        if session is None:
            self.sync_conversation()
            return

        needs_fetch = force or (not session.transcript and session.info.message_count > 0)
        if needs_fetch:
            try:
                messages = await self._transport.fetch_session_messages(session_id)
            except Exception:
                logger.opt(exception=True).warning(
                    "Failed to fetch messages for transcript rebuild"
                )
                self._ui.flash("Could not load session history", severity="warning")
                self.sync_conversation()
                return
            session.transcript = _transcript_from_messages(
                messages,
                report_url=self._context.report_url(session_id),
            )
            self._seed_state_from_session_info(session_id, session.info)

        self.sync_conversation()

    def _seed_state_from_session_info(self, session_id: str, info: SessionInfo) -> None:
        """Hydrate ``TurnState`` cost / tool-call counters from ``SessionInfo``.

        The runtime server (for in-memory sessions) and the platform API
        (for synced sessions) both compute these roll-ups at the source —
        ``total_cost_usd`` is ``None`` when at least one generation in scope
        had no rate, mirroring ``SessionUsageResponse``'s null-propagation.
        Live wire events take over from the next ``GenerationStep`` onward.
        """
        state = self.session_turn_state(session_id)
        if state is None:
            return
        _apply_session_info_to_turn_state(state, info)
        self.set_session_turn_state(session_id, state)

    def show_inline_activity(self, session_id: str, label: str) -> None:
        """Render a removable activity indicator inline in the conversation."""
        session = self._sessions.get(session_id)
        if session is None:
            return
        message = f"{label}..."
        if session.inline_activity == message:
            return
        session.inline_activity = message
        if not self.is_active_session(session_id):
            return
        conv = self._ui.query_conversation()
        conv.write_activity(message)

    def clear_inline_activity(self, session_id: str) -> None:
        """Remove the inline activity indicator for a session."""
        session = self._sessions.get(session_id)
        if session is None or session.inline_activity is None:
            return
        session.inline_activity = None
        conv = self._ui.query_conversation()
        conv.clear_activity()

    # ------------------------------------------------------------------
    # Tool-run lookup helper
    # ------------------------------------------------------------------

    @staticmethod
    def _tool_run_for_wire_tool_call(
        state: TurnState,
        tool_call: we.WireToolCall,
    ) -> ToolRun | None:
        """Find the ``ToolRun`` in ``state`` that a wire tool_call refers to.

        Prefers an exact match by ``tool_call_id``; falls back to the
        most recently appended run with a matching ``tool_name`` so
        replay edge cases and events without ids still land on the
        right row.
        """
        if tool_call.id:
            run = state.tool_runs.get(tool_call.id)
            if run is not None:
                return run
        if tool_call.name:
            for key in reversed(state.tool_order):
                run = state.tool_runs.get(key)
                if run is None:
                    continue
                if run.tool_name == tool_call.name:
                    return run
        return None

    @staticmethod
    def tool_result_details(result: t.Any, max_len: int = 1600) -> str:
        """Render detailed tool result text for expanded transcript mode."""
        if result is None:
            return ""

        if isinstance(result, str):
            text = result.strip()
        elif isinstance(result, (dict, list)):
            try:
                text = json.dumps(result, indent=2, sort_keys=True)
            except TypeError:
                text = str(result)
        else:
            text = str(result)

        if not text:
            return ""
        if len(text) > max_len:
            return f"{text[:max_len]}..."
        return text

    # ------------------------------------------------------------------
    # Progress indicator
    # ------------------------------------------------------------------

    def sync_progress_indicator(self, state: TurnState) -> None:
        """Update the tool-progress indicator widget based on current turn state."""
        tp = self._ui.query_tool_progress()

        # A pending ``ask_user`` prompt is a hard "agent is paused" signal,
        # regardless of phase. ``ToolStart`` for ``ask_user`` can race
        # ``UserInputRequired`` and arrive second, flipping the reducer phase
        # back to ``RUNNING_TOOLS`` while the human is still being prompted —
        # gate the UI on the prompt itself, not the phase, so the spinner
        # stays down whether ``ToolStart`` arrives before or after.
        if state.pending_human_prompt is not None:
            tp.hide_tool()
            return

        running = [r for r in state.tool_runs.values() if r.status == "running"]

        if state.phase is TurnStatePhase.RUNNING_TOOLS and running:
            if len(running) == 1:
                tp.show_tool(running[0].tool_name)
            elif len(running) == 2:
                names = ", ".join(r.tool_name for r in running)
                tp.show_activity(names)
            else:
                names = ", ".join(r.tool_name for r in running[:2])
                tp.show_activity(f"{names}, +{len(running) - 2}")
        elif state.phase is TurnStatePhase.GENERATING:
            if state.draft_text:
                tp.show_activity("streaming")
            else:
                tp.show_activity("thinking")
        elif state.phase in {
            TurnStatePhase.COMPLETED,
            TurnStatePhase.FAILED,
            TurnStatePhase.IDLE,
        }:
            # Idle between tool_end and next generation — show thinking
            # unless the turn is actually done.
            if state.phase is TurnStatePhase.IDLE and state.tool_runs:
                tp.show_activity("thinking")
            else:
                tp.hide_tool()
        elif state.phase in {
            TurnStatePhase.AWAITING_INPUT,
            TurnStatePhase.AWAITING_PERMISSION,
        }:
            # Agent is paused waiting on the human — no work is happening,
            # so hide the spinner. The prompt widget is the active surface.
            tp.hide_tool()

    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------

    def handle_event(self, event: dict[str, t.Any], session_id: str) -> None:
        """Dispatch one raw runtime event into per-session state and UI.

        Parses the raw envelope into a typed :class:`WireEvent`, feeds
        it to the reducer for state transitions, then performs UI
        side-effects via one ``isinstance`` branch per event type. All
        widget access routes through :attr:`_ui`; all app-reactive
        access routes through :attr:`_context`.
        """
        wire_event = parse_wire_event(event)
        if wire_event is None:
            return  # Unknown/invalid event — already logged by the parser.

        prev_state = self.session_turn_state(session_id) or TurnState.empty(session_id)
        next_state = reduce_event(prev_state, wire_event)
        self.set_session_turn_state(session_id, next_state)

        is_active_session = self.is_active_session(session_id)
        session_record = self._sessions.get(session_id)

        # Latest-prompt-size tracker — update on any event whose usage carries
        # a non-zero ``input_tokens``. We replace (not max), because the gauge
        # shows "what context was just sent", not "the largest context ever".
        last_input_tokens = _last_input_tokens_from(wire_event)
        if last_input_tokens is not None and is_active_session:
            self._context.set_last_input_tokens(last_input_tokens)
        # Push live cost / tool-call-count from the freshly reduced state
        # so the footer tracks every wire event (ToolStart bumps tool
        # count, GenerationStep accumulates cost).
        if is_active_session:
            self._context.set_tool_call_count(next_state.usage_tool_call_count)
            self._context.set_cost_usd(next_state.usage_cost_usd)
            self._context.set_cost_unknown(next_state.cost_unknown)

        if isinstance(wire_event, we.Cancelled):
            logger.debug("Server confirmed turn cancellation for session {}", session_id[:8])
            return

        if isinstance(wire_event, we.GenerationContent):
            # Render text immediately — fires BEFORE tools (ENG-5879)
            reasoning = _reasoning_from_extra(wire_event.data.extra)
            if reasoning and self._context.show_thinking():
                self._ui.append_transcript(
                    Message(
                        role="assistant",
                        content=reasoning,
                        metadata={"thinking": True},
                    ),
                    session_id,
                )

            text = wire_event.data.content or ""
            if text:
                if not is_active_session and not prev_state.draft_text:
                    self.mark_session_unread(session_id)
                if is_active_session:
                    draft = self._ui.query_draft()
                    if not prev_state.draft_text:
                        draft.start_stream()
                    draft.append_token(text)
            if is_active_session:
                self.sync_progress_indicator(next_state)
            return

        if isinstance(wire_event, (we.GenerationEnd, we.GenerationStep, we.GenerationStart)):
            return

        if isinstance(wire_event, we.ToolStart):
            if prev_state.draft_text:
                self.commit_session_draft_text(
                    session_id,
                    from_widget=is_active_session,
                )
            if not is_active_session:
                self.mark_session_unread(session_id)
            # Mount a ToolCall widget showing the tool name immediately.
            # The mount is synchronous so the in-progress row is visible the
            # moment the tool fires — deferring via ``call_after_refresh``
            # used to race with the synchronous ``widget.complete()`` in
            # ``ToolEnd`` for fast tools, leaving the user with only the
            # finished state (the in-progress view never rendered).
            run = self._tool_run_for_wire_tool_call(next_state, wire_event.data.tool_call)
            if run is not None and is_active_session:
                widget = ToolCall(
                    name=_format_tool_label(run.tool_name, run.tool_args),
                    classes="entry tool-entry",
                )
                self._tool_call_widgets[run.tool_call_id] = widget
                conv = self._ui.query_conversation()
                conv.append_entry_widget(widget)
            if is_active_session:
                self.sync_progress_indicator(next_state)
            return

        if isinstance(wire_event, we.ToolEnd):
            run = self._tool_run_for_wire_tool_call(next_state, wire_event.data.tool_call)
            tool_name, tool_args = _tool_name_args_from_run_or_wire(run, wire_event.data.tool_call)
            result = wire_event.data.result
            summary = _summarize_tool_result(tool_name, tool_args, result)
            full_details = self.tool_result_details(result)
            tool_call_id = wire_event.data.tool_call.id or (run.tool_call_id if run else None)
            tool_error = wire_event.data.error
            tool_error_type = wire_event.data.error_type
            if tool_error:
                logger.warning("Tool reported error | tool={} | error={}", tool_name, tool_error)
            if not is_active_session:
                self.mark_session_unread(session_id)
            report_url: str | None = None
            expanded_body: str | None = None
            expanded_body_format: str | None = None
            if tool_name == "report" and not tool_error:
                report_url = self._context.report_url(session_id)
                content_arg = tool_args.get("content")
                expanded_body = content_arg if isinstance(content_arg, str) else None
                format_arg = tool_args.get("format")
                expanded_body_format = format_arg if isinstance(format_arg, str) else "markdown"
            tool_message = _make_tool_message(
                tool_name=tool_name,
                tool_args=tool_args,
                body=full_details,
                summary=summary,
                tool_call_id=tool_call_id,
                error=tool_error,
                error_type=tool_error_type,
                report_url=report_url,
            )
            # Update the in-progress widget in place, or append a new one
            was_following = False
            if is_active_session:
                conv = self._ui.query_conversation()
                # Snapshot follow state BEFORE any content change — reflow after
                # mount/complete extends max_scroll_y, which would falsely read
                # a following user as scrolled-up.
                was_following = conv.is_following
                widget = self._tool_call_widgets.pop(run.tool_call_id if run else "", None)
                if widget is not None:
                    widget.complete(
                        meta=summary,
                        details=full_details,
                        error=tool_error,
                        url=report_url,
                        expanded_body=expanded_body,
                        expanded_body_format=expanded_body_format,
                    )
                else:
                    # No in-progress widget (e.g. session replay, or ToolStart
                    # arrived while the session wasn't active) — append the
                    # final tool row synchronously so the result is guaranteed
                    # to land in the conversation view. A deferred refresh tick
                    # used to swallow the append intermittently when a
                    # transcript reload landed in between.
                    conv.append_entry(tool_message, scroll=False)
            # Always record in transcript with full details for session replay
            if session_record is not None:
                session_record.transcript.append(tool_message)
            if is_active_session:
                self.sync_progress_indicator(next_state)
                if was_following:
                    conv = self._ui.query_conversation()
                    self._ui.call_after_refresh(conv.scroll_end, animate=False)
            return

        if isinstance(wire_event, we.ToolStep):
            return

        if isinstance(wire_event, we.ToolError):
            error = wire_event.data.error or "Tool error"
            logger.error("Tool error: {}", error)
            run = self._tool_run_for_wire_tool_call(next_state, wire_event.data.tool_call)
            tool_name, tool_args = _tool_name_args_from_run_or_wire(run, wire_event.data.tool_call)
            label = _format_tool_label(tool_name, tool_args)
            if not is_active_session:
                self.mark_session_unread(session_id)
            # Update the in-progress widget, or append a new error entry
            if is_active_session:
                widget = self._tool_call_widgets.pop(run.tool_call_id if run else "", None)
                if widget is not None:
                    widget.complete(error=error)
            # Always record in transcript
            self._ui.append_transcript(
                _make_error_message(title=label, body=error),
                session_id,
            )
            return

        if isinstance(wire_event, we.GenerationError):
            error_text = wire_event.data.error or "Generation error"
            error_type = wire_event.data.error_type
            status_code = wire_event.data.status_code
            logger.error("Generation error: {} (type={})", error_text, error_type)
            if not is_active_session:
                self.mark_session_unread(session_id)
            classification = classify_error_message(error_text, error_type)
            title = "generation"
            body = classification.error_text or "Generation error"
            resolution = self._error_handler.resolve_proxy_error(
                classification.error_text or "",
                error_type,
            )
            if resolution.override:
                body = resolution.override
            self._error_handler.apply_resolution(resolution)
            split = None
            if classification.error_text:
                split = split_missing_api_key_message(classification.error_text)
                if split:
                    title, body = split
            if not resolution.override and not split:
                body = enrich_error_body(body, error_type, status_code)
            self._ui.append_transcript(
                _make_error_message(title=title, body=body),
                session_id,
            )
            if classification.is_authentication_error and classification.error_text:
                self._last_auth_error[session_id] = classification.error_text
            return

        if isinstance(wire_event, we.Compaction):
            if not is_active_session:
                self.mark_session_unread(session_id)
            if wire_event.data.compaction_status == "completed":
                before = wire_event.data.messages_before
                after = wire_event.data.messages_after
                compacted = before - after if before > after else 0
                if compacted > 0:
                    label = f"Auto-compacted — {compacted} messages summarized"
                else:
                    label = "Auto-compacted"
                self._ui.append_transcript(
                    Message(
                        role="system",
                        content=label,
                        metadata={"compaction": True},
                    ),
                    session_id,
                )
            return

        if isinstance(wire_event, we.GenerationRetry):
            if not is_active_session:
                self.mark_session_unread(session_id)
            err_type = wire_event.data.error_type or "error"
            err_msg = wire_event.data.error_message or ""
            detail = f": {err_msg}" if err_msg else ""
            label = (
                f"{err_type} — retrying in {wire_event.data.wait_seconds or 0.0:.1f}s "
                f"(attempt {wire_event.data.attempt or 0}/"
                f"{wire_event.data.max_attempts or 0}){detail}"
            )
            self._ui.append_transcript(
                Message(role="system", content=label, metadata={"retry": True}),
                session_id,
            )
            return

        if isinstance(wire_event, we.AgentStalled):
            reason = wire_event.data.reason or "Agent stalled"
            logger.warning("Agent stalled: {}", reason)
            if not is_active_session:
                self.mark_session_unread(session_id)
            self._ui.append_transcript(
                _make_error_message(title="agent", body=reason),
                session_id,
            )
            return

        if isinstance(wire_event, we.AgentError):
            error_text = wire_event.data.error
            error_type = wire_event.data.error_type
            status_code = wire_event.data.status_code
            logger.error("Agent error: {} (type={})", error_text, error_type)
            if not is_active_session:
                self.mark_session_unread(session_id)
            if error_text:
                classification = classify_error_message(error_text, error_type)
                resolution = self._error_handler.resolve_proxy_error(
                    classification.error_text or "",
                    error_type,
                )
                body = resolution.override or classification.error_text or error_text
                self._error_handler.apply_resolution(resolution)
                if not resolution.override:
                    body = enrich_error_body(body, error_type, status_code)
                self._ui.append_transcript(
                    _make_error_message(title="agent", body=body),
                    session_id,
                )
                if classification.is_authentication_error and classification.error_text:
                    self._last_auth_error[session_id] = classification.error_text
            return

        if isinstance(wire_event, we.AgentEnd):
            error_text = wire_event.data.error
            error_type = wire_event.data.error_type
            status_code = wire_event.data.status_code
            stop_reason = (wire_event.data.stop_reason or "").lower()
            envelope_status = wire_event.status
            if not is_active_session:
                self.mark_session_unread(session_id)
            logger.debug(
                "Agent end | session={} | stop_reason={} | status={} | error={}",
                session_id[:8],
                stop_reason or "finished",
                envelope_status or "ok",
                error_text or "none",
            )
            if is_active_session:
                # Perf telemetry — log one summary line per turn so we can
                # see how rendering cost correlates with session length.
                # See widgets/conversation.py:perf_snapshot_and_reset.
                try:
                    conv = self._ui.query_conversation()
                    draft = self._ui.query_draft()
                    entries, vsize_changes = conv.perf_snapshot_and_reset()
                    tok_n, tok_p50, tok_p95, tok_max = draft.perf_snapshot_and_reset()
                    logger.info(
                        "TUI perf | session={} | entries={} | vsize_events={} "
                        "| tokens={} | tok_us_p50={:.0f} | tok_us_p95={:.0f} | tok_us_max={:.0f}",
                        session_id[:8],
                        entries,
                        vsize_changes,
                        tok_n,
                        tok_p50,
                        tok_p95,
                        tok_max,
                    )
                except Exception:
                    logger.opt(exception=True).debug("TUI perf snapshot failed")
            if error_text:
                logger.error(
                    "Agent ended with error: {} (type={})",
                    error_text,
                    error_type,
                )
                classification = classify_error_message(error_text, error_type)
                resolution = self._error_handler.resolve_proxy_error(
                    classification.error_text or "",
                    error_type,
                )
                body = resolution.override or classification.error_text or error_text
                if classification.is_authentication_error and classification.error_text:
                    last_auth_error = self._last_auth_error.get(session_id)
                    if last_auth_error == classification.error_text:
                        return
                self._error_handler.apply_resolution(resolution)
                if not resolution.override:
                    body = enrich_error_body(body, error_type, status_code)
                self._ui.append_transcript(
                    _make_error_message(title="agent", body=body),
                    session_id,
                )
                if classification.is_authentication_error and classification.error_text:
                    self._last_auth_error[session_id] = classification.error_text
            elif envelope_status == "errored" or stop_reason == "error":
                logger.error("Agent ended with error status (no error text)")
                self._ui.append_transcript(
                    _make_error_message(title="agent", body="run ended with an error"),
                    session_id,
                )
            elif stop_reason == "max_steps_reached":
                logger.warning("Agent hit max steps | session={}", session_id[:8])
                self._ui.append_transcript(
                    _make_error_message(
                        title="agent",
                        body="stopped — reached the maximum number of steps. Send a follow-up message to continue.",
                    ),
                    session_id,
                )
            elif stop_reason == "stalled":
                logger.warning("Agent stalled | session={}", session_id[:8])
                self._ui.append_transcript(
                    _make_error_message(
                        title="agent",
                        body="stopped — agent appears stalled. Send a follow-up message to continue.",
                    ),
                    session_id,
                )
            return

        if isinstance(wire_event, we.UserInputRequired):
            prompt = wire_event.data  # HumanPrompt
            if not is_active_session:
                self.mark_session_unread(session_id)
                self._ui.flash(
                    f"Session {session_id[:8]} awaiting input",
                    severity="warning",
                )
            else:
                self._context.turn_enter_awaiting("Awaiting input")
                # Hide the running-tool spinner — the agent is paused on the
                # prompt; no work is being done.
                self._ui.query_tool_progress().hide_tool()
                widget = self._ui.query_prompt_widget()
                self._ui.call_after_refresh(widget.show_prompt, prompt)
                composer = self._ui.query_composer()
                composer.placeholder = "Answer the prompt above"
                composer.disabled = True
            return

        if isinstance(wire_event, we.RuntimeErrorEvent):
            error_text = wire_event.error or wire_event.data.error or "Runtime error"
            logger.error("Runtime error: {}", error_text)
            if not is_active_session:
                self.mark_session_unread(session_id)
            # ``status`` and ``status_code`` are the two shapes the
            # server's terminal-event shim may attach via ``data``. We
            # check both to stay defence-in-depth for any path that
            # surfaces an HTTP 401 as an error event instead of a
            # command.error response.
            status_code = wire_event.data.status_code
            if status_code is None:
                status_code = wire_event.data.status
            current_model = self._context.current_model()
            if (
                status_code in {401, 403}
                and isinstance(current_model, str)
                and current_model.startswith("dn/")
            ):
                logger.warning(
                    "Runtime returned {} for dn/* model — refreshing model access",
                    status_code,
                )
                self._ui.flash(DN_MODEL_ACCESS_CHANGED_MESSAGE, severity="warning")
                self._ui.append_transcript(
                    _make_error_message(title="runtime", body=DN_MODEL_ACCESS_CHANGED_MESSAGE),
                    session_id,
                )
                if self._model_access is not None:
                    self._model_access.refresh_platform_model_access()
                return
            if status_code == 401:
                logger.warning("Runtime returned 401 during chat — triggering re-auth")
                raise AuthenticationError("401: Unauthorized")
            if status_code == 403:
                logger.warning(
                    "Runtime returned 403 during chat — insufficient permissions: {}",
                    error_text,
                )
            resolution = self._error_handler.resolve_proxy_error(error_text, None)
            self._ui.write_activity(error_text, style="error")
            body = resolution.override or error_text
            if not resolution.override:
                body = enrich_error_body(body, None, status_code)
            self._ui.append_transcript(
                _make_error_message(title="runtime", body=body),
                session_id,
            )
            self._error_handler.apply_resolution(resolution)
            return

        # AgentStart and any unmatched event fall through with no UI effect.
        return
