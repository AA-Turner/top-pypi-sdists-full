import time
import typing as t
from dataclasses import dataclass, field, replace

from loguru import logger

from dreadnode.app.tui import wire_events as we
from dreadnode.app.tui.turn_state_phase import TurnStatePhase, phase_for_human_prompt

if t.TYPE_CHECKING:
    from dreadnode.app.api.models import HumanPrompt

ToolStatus = t.Literal["running", "completed", "errored"]


@dataclass(slots=True)
class ToolRun:
    """Tool lifecycle state for one tool call.

    Only raw data — no pre-computed display strings. Label formatting
    and result summarization happen at the view layer when building
    ``ToolCall`` widgets or transcript :class:`Message` records.
    """

    tool_call_id: str
    tool_name: str
    tool_args: dict[str, t.Any]
    status: ToolStatus
    started_at: float
    ended_at: float | None = None
    summary: str | None = None
    error: str | None = None
    partial: bool = False


@dataclass(slots=True)
class TurnState:
    """Reducer state for one session turn."""

    session_id: str
    phase: TurnStatePhase
    draft_text: str
    tool_runs: dict[str, ToolRun] = field(default_factory=dict)
    tool_order: list[str] = field(default_factory=list)
    pending_human_prompt: "HumanPrompt | None" = None
    # ``input_tokens`` from the most recent ``GenerationStep`` — i.e., the
    # size of the prompt the model just saw. This is what the context-window
    # gauge displays (``last_input_tokens / model_max_tokens``). Cumulative
    # session-total tokens are *not* what users want here — that sum grows
    # with each turn and would exceed the model's max context for any
    # multi-turn session.
    usage_last_input_tokens: int = 0
    # Session-cumulative tool call count (increments on ``ToolStart``) and
    # estimated USD cost (accumulates per-generation on ``GenerationStep``).
    # ``cost_unknown`` flips true the first time a generation reports
    # ``output_tokens`` but no rate — the TUI then suppresses the dollar
    # display rather than showing a partial sum, matching the backend's
    # null-propagation semantics for ``total_cost_usd``.
    usage_tool_call_count: int = 0
    usage_cost_usd: float = 0.0
    usage_subagent_cost_usd: float = 0.0
    cost_unknown: bool = False
    final_error: str | None = None
    last_heartbeat_at: str | None = None

    @classmethod
    def empty(cls, session_id: str) -> "TurnState":
        """Create a fresh empty turn state."""
        logger.debug("Turn start | session_id={}", session_id)
        return cls(session_id=session_id, phase=TurnStatePhase.IDLE, draft_text="")


def reduce_event(
    state: TurnState,
    event: we.WireEvent,
    *,
    now: t.Callable[[], float] = time.monotonic,
) -> TurnState:
    """Reduce one typed wire event into next turn state.

    Dispatches on :class:`WireEvent` subclass via isinstance — each
    branch sees a precise payload type, so no optional-field digging
    or string-type comparisons are needed. Caller is responsible for
    passing an event that belongs to ``state.session_id``: the
    subscription layer in :class:`SessionsManager` already enforces
    per-session event routing, so the old in-reducer
    ``session_id`` mismatch guard was redundant and has been removed.
    """
    old_phase = state.phase
    next_state = _clone_state(state)
    event_label = type(event).__name__

    if isinstance(event, we.GenerationStart):
        next_state.phase = TurnStatePhase.GENERATING

    elif isinstance(event, we.GenerationContent):
        # Text content from the LLM — fires before tools (ENG-5879)
        next_state.phase = TurnStatePhase.GENERATING
        if event.data.content:
            next_state.draft_text += event.data.content

    elif isinstance(event, we.GenerationStep):
        # Lifecycle marker only — don't touch ``draft_text`` here.
        # ``GenerationStep.data.content`` mirrors ``GenerationContent.data.content``
        # (both derive from ``messages[-1].content`` at ``agent.py:833/864/902/1008``),
        # so accumulating it again would double the assistant message whenever
        # the state.draft_text fallback path is taken (background session,
        # empty widget buffer, ToolStart with from_widget=False). Treat this
        # the same as ``ToolStep`` — a trajectory/usage marker.
        next_state.phase = TurnStatePhase.GENERATING
        # Latest generation's ``input_tokens`` is the size of the prompt the
        # model just saw — what the context-window gauge displays. Skip
        # zero/None payloads so we don't blank the gauge on partial events.
        if event.data.usage.input_tokens:
            next_state.usage_last_input_tokens = event.data.usage.input_tokens
        # Cost is per-generation; sum across steps. ``GenerationEnd`` does
        # not contribute (would double-count the terminal step). A step that
        # reports output tokens but no cost rate (model not in litellm's
        # catalog) flips ``cost_unknown`` so the footer suppresses the dollar
        # display — partial sums are misleading.
        cost_usd = event.data.usage.cost_usd
        output_tokens = event.data.usage.output_tokens or 0
        if cost_usd is not None:
            next_state.usage_cost_usd += cost_usd
        elif output_tokens > 0:
            next_state.cost_unknown = True
        logger.debug(
            "Generation step | step={} | stop_reason={} | input_tokens={} | last_input={}",
            event.data.step,
            event.data.stop_reason,
            event.data.usage.input_tokens,
            next_state.usage_last_input_tokens,
        )

    elif isinstance(event, we.GenerationEnd):
        if event.data.usage.input_tokens:
            next_state.usage_last_input_tokens = event.data.usage.input_tokens
        logger.debug(
            "Generation end | stop_reason={} | input_tokens={} | last_input={}",
            event.data.stop_reason,
            event.data.usage.input_tokens,
            next_state.usage_last_input_tokens,
        )
        if not _has_running_tools(next_state):
            next_state.phase = TurnStatePhase.IDLE

    elif isinstance(event, we.ToolStart):
        tc = event.data.tool_call
        key = _tool_key_for_call(next_state, tc.id, tc.name, is_end=False)
        tool_name = tc.name or "tool"
        tool_args = _coerce_tool_args(tc.arguments)
        # Count first observation of this tool call only; replays of the
        # same id (e.g., reconnect) shouldn't inflate the counter.
        if key not in next_state.tool_runs:
            next_state.usage_tool_call_count += 1
        next_state.tool_runs[key] = ToolRun(
            tool_call_id=key,
            tool_name=tool_name,
            tool_args=tool_args,
            status="running",
            started_at=now(),
        )
        if key not in next_state.tool_order:
            next_state.tool_order.append(key)
        next_state.phase = TurnStatePhase.RUNNING_TOOLS
        logger.debug("Tool start | tool={} | id={}", tool_name, key)

    elif isinstance(event, we.ToolEnd):
        tc = event.data.tool_call
        # ToolEnd may carry an error message when the tool caught its
        # own exception (bash non-zero exit, @tool(catch=True), MCP
        # isError). Promote those to status="errored" so the widget
        # picks up the same red treatment as uncaught exceptions.
        end_status: ToolStatus = "errored" if event.data.error else "completed"
        next_state = _finish_tool(
            next_state,
            tool_call_id=tc.id,
            tool_name=tc.name,
            tool_args=_coerce_tool_args(tc.arguments),
            status=end_status,
            now=now,
        )
        if event.data.error:
            key = _tool_key_for_call(next_state, tc.id, tc.name, is_end=True)
            run = next_state.tool_runs.get(key)
            if run is not None:
                run.error = event.data.error
        # Accumulate sub-agent LLM cost carried on the ToolEnd event
        # (set by ``spawn_agent`` via message metadata). Kept separate
        # from the main ``usage_cost_usd`` so the footer can show it
        # as "(subagents $X.XX)" alongside the parent session cost.
        if event.data.cost_usd is not None:
            next_state.usage_subagent_cost_usd += event.data.cost_usd

    elif isinstance(event, we.ToolError):
        tc = event.data.tool_call
        next_state = _finish_tool(
            next_state,
            tool_call_id=tc.id,
            tool_name=tc.name,
            tool_args=_coerce_tool_args(tc.arguments),
            status="errored",
            now=now,
        )
        if event.data.error:
            key = _tool_key_for_call(next_state, tc.id, tc.name, is_end=True)
            run = next_state.tool_runs.get(key)
            if run is not None:
                run.error = event.data.error

    elif isinstance(event, we.ToolStep):
        pass  # Intermediate tool progress — no phase change

    elif isinstance(event, we.UserInputRequired):
        prompt = event.data  # HumanPrompt
        next_state.pending_human_prompt = prompt
        next_state.phase = phase_for_human_prompt()

    elif isinstance(event, we.Compaction):
        pass  # Lifecycle signal — no phase change

    elif isinstance(event, we.AgentStart):
        # New turn — clear stale tool state from prior turn / cancellation
        next_state.tool_runs = {}
        next_state.tool_order = []
        next_state.draft_text = ""
        next_state.final_error = None

    elif isinstance(event, we.Heartbeat):
        next_state.last_heartbeat_at = event.timestamp

    elif isinstance(event, we.AgentEnd):
        next_state.pending_human_prompt = None
        if event.data.error:
            next_state.phase = TurnStatePhase.FAILED
            next_state.final_error = event.data.error
        else:
            next_state.phase = TurnStatePhase.COMPLETED

    elif isinstance(event, we.Cancelled):
        # Server confirmed cancellation — mark any still-running tools as errored
        for run in next_state.tool_runs.values():
            if run.status == "running":
                run.status = "errored"
                run.ended_at = now()
        next_state.phase = TurnStatePhase.IDLE

    elif isinstance(event, (we.GenerationError, we.AgentError)):
        next_state.phase = TurnStatePhase.FAILED
        next_state.final_error = event.data.error or "unknown error"

    elif isinstance(event, we.AgentStalled):
        next_state.phase = TurnStatePhase.FAILED
        next_state.final_error = event.data.reason or "unknown error"

    elif isinstance(event, we.RuntimeErrorEvent):
        next_state.phase = TurnStatePhase.FAILED
        next_state.final_error = event.error or "unknown error"

    elif isinstance(event, we.GenerationRetry):
        pass  # Surface-only signal, no phase change

    else:
        logger.warning("Unknown wire event | type={}", event_label)

    if next_state.phase != old_phase:
        logger.debug(
            "Phase transition | {} -> {} | event={}",
            old_phase,
            next_state.phase,
            event_label,
        )

    if next_state.phase in {TurnStatePhase.COMPLETED, TurnStatePhase.FAILED}:
        logger.debug(
            "Turn complete | phase={} | tools_ran={} | last_input_tokens={}",
            next_state.phase,
            len(next_state.tool_runs),
            next_state.usage_last_input_tokens,
        )

    return next_state


def _clone_state(state: TurnState) -> TurnState:
    return TurnState(
        session_id=state.session_id,
        phase=state.phase,
        draft_text=state.draft_text,
        tool_runs={key: replace(run) for key, run in state.tool_runs.items()},
        tool_order=list(state.tool_order),
        pending_human_prompt=state.pending_human_prompt,
        usage_last_input_tokens=state.usage_last_input_tokens,
        usage_tool_call_count=state.usage_tool_call_count,
        usage_cost_usd=state.usage_cost_usd,
        usage_subagent_cost_usd=state.usage_subagent_cost_usd,
        cost_unknown=state.cost_unknown,
        final_error=state.final_error,
        last_heartbeat_at=state.last_heartbeat_at,
    )


def reduce_human_prompt_response(state: TurnState, *, action: str) -> TurnState:
    """Apply a local human prompt response to the turn state."""
    next_state = _clone_state(state)
    next_state.pending_human_prompt = None
    if action == "submit":
        next_state.phase = TurnStatePhase.RUNNING_TOOLS
    elif action == "cancel":
        next_state.phase = TurnStatePhase.IDLE
    return next_state


def _coerce_tool_args(args: t.Any) -> dict[str, t.Any]:
    """Normalize ``tool_call.arguments`` to a dict for the reducer state.

    The wire format sends ``dict`` when the server could parse the
    LLM's JSON and ``str`` when it couldn't. Downstream code (label
    formatters, widget renderers) always expects a dict.
    """
    if isinstance(args, dict):
        return args
    if isinstance(args, str) and args.strip():
        return {"raw": args.strip()}
    return {}


def _tool_key_for_call(
    state: TurnState,
    tool_call_id: str | None,
    tool_name: str | None,
    *,
    is_end: bool,
) -> str:
    """Resolve the state key for a tool call, including fallbacks.

    Prefers the server-provided ``tool_call_id``. When missing (older
    events, replay edge cases) we try to match an existing in-flight
    run by name on tool_end/tool_error, and otherwise invent a
    deterministic ``missing:<name>`` key so the run is still tracked.
    """
    if tool_call_id:
        return tool_call_id

    name = tool_name or "tool"
    if is_end:
        for key in reversed(state.tool_order):
            run = state.tool_runs.get(key)
            if run is None:
                continue
            if run.status == "running" and run.tool_name == name:
                return key

    base = f"missing:{name}"
    if base not in state.tool_runs:
        return base
    index = 2
    while f"{base}:{index}" in state.tool_runs:
        index += 1
    return f"{base}:{index}"


def _finish_tool(
    state: TurnState,
    *,
    tool_call_id: str | None,
    tool_name: str | None,
    tool_args: dict[str, t.Any],
    status: ToolStatus,
    now: t.Callable[[], float],
) -> TurnState:
    key = _tool_key_for_call(state, tool_call_id, tool_name, is_end=True)
    run = state.tool_runs.get(key)
    if run is None:
        name = tool_name or "tool"
        logger.warning("Unmatched tool {} | id={} | tool={}", status, key, name)
        run = ToolRun(
            tool_call_id=key,
            tool_name=name,
            tool_args=tool_args,
            status=status,
            started_at=now(),
            partial=True,
        )
        state.tool_runs[key] = run
        state.tool_order.append(key)
    else:
        logger.debug("Tool {} | tool={} | id={}", status, run.tool_name, key)
    run.status = status
    run.ended_at = now()
    if not _has_running_tools(state):
        state.phase = TurnStatePhase.IDLE
    return state


def _has_running_tools(state: TurnState) -> bool:
    return any(run.status == "running" for run in state.tool_runs.values())
