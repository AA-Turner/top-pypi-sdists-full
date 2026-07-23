"""Dreadnode Agent Server.

FastAPI server with REST endpoints and websocket-first interactive transport.
"""

from __future__ import annotations

import asyncio
import json
import os
import time
import typing as t
from contextlib import asynccontextmanager, suppress
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID, uuid4

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from starlette.responses import JSONResponse

from dreadnode.app.api.models import (
    HealthResponse,
    HumanInputResponse,
    HumanPrompt,
    RuntimeInfoResponse,
    SessionCreateRequest,
    SessionEventPublishRequest,
    SessionGroupCreateRequest,
    SessionGroupInfo,
    SessionGroupUpdateRequest,
    SessionInfo,
    SessionMessage,
    SessionRestoreRequest,
    SessionRestoreResponse,
    SkillContentResponse,
    SkillsResponse,
    ToolInfo,
    ToolsResponse,
    WsTicketResponse,
)
from dreadnode.app.api.models import (
    SkillInfo as SkillInfoModel,
)
from dreadnode.app.env import read_env_with_deprecation
from dreadnode.app.server import capability_manager, model_resolution, runtime_events, ws_auth
from dreadnode.app.server.auth import SandboxAuthMiddleware, bearer_token
from dreadnode.app.server.prompt import (
    get_core_system_prompt,
    get_platform_context,
    get_project_memory_background_context,
    get_runtime_shell_prompt,
    render_project_memory_preload_xml,
)
from dreadnode.app.server.prompt_registry import SessionPromptRegistry
from dreadnode.app.server.runtime_events import (
    RuntimeSessionSnapshot,
    RuntimeSessionSyncStatus,
)
from dreadnode.app.server.runtime_token import get_token_source, materialize_runtime_token_file
from dreadnode.app.server.session_hydrator import SessionHydrator
from dreadnode.app.server.session_persistence import SessionPersistenceCoordinator
from dreadnode.app.server.turn_coordinator import QueuedTurnRequest, SessionTurnCoordinator
from dreadnode.app.server.websocket import (
    WebSocketConnectionRegistry,
    serve_runtime_event_stream,
    serve_runtime_websocket,
)
from dreadnode.tracing.span import bind_session_id

if t.TYPE_CHECKING:
    from dreadnode.agents import Agent
    from dreadnode.agents.events import AgentEvent
    from dreadnode.capabilities.capability import Capability
    from dreadnode.capabilities.types import AgentDef
    from dreadnode.generators.generator import Generator
    from dreadnode.generators.message import Message
    from dreadnode.policies import SessionPolicy
    from dreadnode.storage import SessionRecord, SessionStore

EventPayload = dict[str, t.Any]
DEFAULT_MODEL = "anthropic/claude-sonnet-4-20250514"
_BUNDLED_DEFAULT_CAPABILITY = "dreadnode"
_PROJECT_MEMORY_SCOPE_PROJECT = "project"


def _short_turn(turn_id: str | None) -> str:
    """Render a turn_id for logs: 8 hex chars, or ``-`` when no turn is active.

    The canonical format is ``turn_<32hex>`` (see
    :class:`QueuedTurnRequest`) so we strip the prefix and take the first
    eight hex chars — enough for correlation across a single session's
    log stream without dragging the full 36-char id across every line.
    """
    if turn_id is None:
        return "-"
    return turn_id.removeprefix("turn_")[:8]


def _log_chat_timing(session_id: str, turn_id: str | None, stage: str, started_at: float) -> None:
    """Emit a coarse timing marker for chat turn diagnostics."""
    elapsed_ms = round((time.perf_counter() - started_at) * 1000)
    logger.debug(
        "Chat timing | session={} turn={} stage={} elapsed_ms={}",
        session_id[:8],
        _short_turn(turn_id),
        stage,
        elapsed_ms,
    )


class SessionRestoreError(ValueError):
    """Raised when a restore payload is invalid for the session restore route."""


def _apply_session_restore_request(
    session: SessionRuntime,
    request: SessionRestoreRequest,
) -> None:
    """Apply a restore payload and narrow user-input failures."""
    try:
        if request.trajectory is not None:
            session.restore_trajectory(request.trajectory, model=request.model)
        elif request.messages:
            session.restore_messages(request.messages, model=request.model)
    except (KeyError, TypeError, ValueError) as exc:
        raise SessionRestoreError(str(exc)) from exc


def _format_session_binding(
    capability_name: str | None,
    agent_name: str | None,
) -> str:
    """Render a human-readable capability/agent binding."""
    parts: list[str] = []
    if capability_name:
        parts.append(f"capability '{capability_name}'")
    if agent_name:
        parts.append(f"agent '{agent_name}'")
    return " / ".join(parts) if parts else "the default runtime"


def _resolve_turn_model(
    requested_model: str | None,
    remembered_model: str | None,
    agent_def: AgentDef | None,
) -> str:
    """Resolve the canonical model id to use for a turn."""
    return model_resolution.resolve_turn_model_config(
        requested_model,
        remembered_model,
        agent_def,
    ).canonical_model


def _tool_name(tool: t.Any) -> str:
    """Get the name of a tool object."""
    return getattr(tool, "name", "")


_ITEM_TOOL_NAMES = {"report_item", "update_item", "link_items"}


def _selected_builtin_item_types(capability: Capability) -> set[str]:
    """Built-in item types a capability explicitly opted into."""
    from dreadnode.items.config import selected_builtin_item_types

    return selected_builtin_item_types(getattr(capability, "manifest", None))


def _capability_items_enabled(capability: Capability) -> bool:
    """True when the capability opted into built-ins or declares custom types."""
    from dreadnode.items.config import item_tools_enabled

    return item_tools_enabled(getattr(capability, "manifest", None))


def _make_agent_link_tool(
    *,
    model: str | Generator | None,
    capability: Capability,
    target_agent: AgentDef,
    extra_tools: list[t.Any] | None,
    extra_hooks: list[t.Any] | None,
    kind: str,
) -> t.Any:
    """Create a synthetic tool that delegates work to another capability agent."""
    from dreadnode.agents.tools import Tool

    async def _link_tool(task: str) -> str:
        delegated_agent = create_agent(
            model,
            capability=capability,
            agent_def=target_agent,
            extra_tools=extra_tools,
            extra_hooks=extra_hooks,
            system_prompt_append=get_state().system_prompt_append,
        )
        return await delegated_agent.chat(task)

    _link_tool.__name__ = f"{kind}_to_{target_agent.name}"
    description = (
        f"{kind.title()} work to the '{target_agent.name}' agent in capability "
        f"'{getattr(capability, 'name', 'unknown')}'."
    )
    return Tool.from_callable(_link_tool, description=description)


def _message_text(message: t.Any) -> str:
    """Flatten a message's content to a plain string."""
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block.get("text", "") if isinstance(block, dict) else str(block) for block in content
        )
    return ""


def _final_assistant_message(trajectory: t.Any) -> str:
    """Extract the last assistant message text from a trajectory."""
    for message in reversed(trajectory.messages):
        if getattr(message, "role", None) == "assistant":
            return _message_text(message)
    return ""


def _final_assistant_in_events(events: t.Iterable[t.Any]) -> str | None:
    """Last assistant-role message text within *events*, or ``None``.

    Used to build ``partial_response`` on failed/cancelled terminal envelopes
    (CAP-WEVT-008/009). Returns ``None`` when the turn produced no assistant
    text yet.
    """
    from dreadnode.agents.events import AgentStep

    for event in reversed(list(events)):
        if not isinstance(event, AgentStep) or not event.messages:
            continue
        for message in reversed(event.messages):
            if getattr(message, "role", None) == "assistant":
                text = _message_text(message)
                return text or None
    return None


def _parse_tool_arguments(raw: str) -> t.Any:
    """Decode tool-call arguments, keeping the raw string on parse failure."""
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return raw


def _turn_tool_calls_completed(events: t.Iterable[t.Any]) -> list[dict[str, t.Any]]:
    """Completed tool invocations in a turn slice: ``{name, arguments, result}``.

    Walks ``ToolStep`` entries — one per completed tool round-trip. Builds the
    ``tool_calls`` field of ``turn.completed`` per CAP-WEVT-007.
    """
    from dreadnode.agents.events import ToolStep

    calls: list[dict[str, t.Any]] = []
    for event in events:
        if not isinstance(event, ToolStep):
            continue
        result_text = _message_text(event.messages[0]) if event.messages else ""
        calls.append(
            {
                "name": event.tool_call.name,
                "arguments": _parse_tool_arguments(event.tool_call.arguments),
                "result": result_text,
            }
        )
    return calls


def _turn_tool_calls_attempted(events: t.Iterable[t.Any]) -> list[dict[str, t.Any]]:
    """Tool calls the assistant issued in a turn slice: ``{name, arguments}``.

    Walks ``GenerationStep`` assistant messages — each ``tool_calls`` entry is
    a call the model made, regardless of whether it executed. Builds
    ``tool_calls_attempted`` on ``turn.failed`` per CAP-WEVT-008.
    """
    from dreadnode.agents.events import GenerationStep

    attempts: list[dict[str, t.Any]] = []
    for event in events:
        if not isinstance(event, GenerationStep) or not event.messages:
            continue
        last_msg = event.messages[-1]
        if getattr(last_msg, "role", None) != "assistant":
            continue
        for tool_call in last_msg.tool_calls or []:
            attempts.append(
                {
                    "name": tool_call.name,
                    "arguments": _parse_tool_arguments(tool_call.arguments),
                }
            )
    return attempts


def _turn_usage(events: t.Iterable[t.Any]) -> dict[str, int]:
    """Aggregate input/output tokens across generation steps in a turn slice."""
    from dreadnode.agents.events import GenerationStep

    input_tokens = 0
    output_tokens = 0
    for event in events:
        if not isinstance(event, GenerationStep):
            continue
        input_tokens += event.usage.input_tokens
        output_tokens += event.usage.output_tokens
    return {"input_tokens": input_tokens, "output_tokens": output_tokens}


#: Stop reasons a client needs told about; everything else is a clean finish.
_NOTABLE_STOP_REASONS = frozenset({"content_filter", "length"})


def _turn_generation_stop_reason(events: t.Iterable[t.Any], *, produced_output: bool) -> str | None:
    """Return a turn slice's generation outcome, preferring one worth surfacing.

    A turn with tool calls holds one ``GenerationStep`` per react cycle and the
    last one is normally benign, so reporting only the final reason would hide
    a blocked or truncated earlier generation from clients recovering the turn
    from this payload rather than the live event stream (ENG-7585).

    That preference only applies while the turn still has nothing to show. When
    the agent looped past the blocked generation and produced a final answer,
    ``produced_output`` is true and the benign final reason wins — the notice
    these reasons drive exists to explain missing output, and a recovered turn
    is not missing any. Per-message ``generation_stop_reason`` metadata keeps
    the full step-by-step record either way.
    """
    from dreadnode.agents.events import GenerationStep

    last: str | None = None
    for event in events:
        if not isinstance(event, GenerationStep) or not event.stop_reason:
            continue
        if not produced_output and event.stop_reason.strip().casefold() in _NOTABLE_STOP_REASONS:
            return event.stop_reason
        last = event.stop_reason
    return last


def _resolve_session_binding(
    registry: capability_manager.CapabilityRegistry | None,
    *,
    capability_name: str | None,
    agent_name: str | None,
) -> tuple[str | None, Capability | None, AgentDef | None]:
    """Resolve a session's bound capability/agent against the current registry."""
    if registry is None:
        return capability_name, None, None

    try:
        return registry.resolve(
            capability_name=capability_name,
            agent_name=agent_name,
        )
    except ValueError:
        logger.warning(
            "Persisted session binding could not be fully resolved: capability={} agent={}",
            capability_name,
            agent_name,
        )

    capability = registry.get(capability_name) if capability_name else None
    agent_def = None

    if capability is not None and agent_name is not None:
        agent_def = next((agent for agent in capability.agents if agent.name == agent_name), None)
    elif capability is None and agent_name is not None:
        found = registry.find_agent(agent_name)
        if found is not None:
            return found

    return capability_name, capability, agent_def


def create_agent(
    model: str | Generator,
    *,
    capability: Capability | None = None,
    agent_def: AgentDef | None = None,
    extra_tools: list[t.Any] | None = None,
    extra_hooks: list[t.Any] | None = None,
    inherent_toolsets: list[t.Any] | None = None,
    system_prompt_append: str | None = None,
    engine: str | None = None,
    background_context: str | None = None,
) -> Agent:
    """Create an agent from a loaded capability.

    Tool assembly order:
    1. Inherent tools (from default_tools()) — always present, except item tools
       which are capability opt-in
    2. Extra tools (from global capability pool) — additive, skip duplicates
    3. Agent tool rules filter the combined pool (empty rules = all tools)

    Hooks from all loaded capabilities (passed via ``extra_hooks``) run
    as middleware on every turn; they're not filtered by agent tool
    rules since hooks aren't agent-scoped.
    """
    from dreadnode.agents import Agent
    from dreadnode.capabilities.tool_rules import filter_tools
    from dreadnode.tools import default_tools

    if not model or model == "inherit":
        raise ValueError(
            f"Agent '{agent_def.name if agent_def else 'dreadnode-agent'}' does not define a model"
        )

    cwd = Path.cwd()
    home_dir = Path.home()
    context = f"\nYour working directory is {cwd}.\nYour home directory is {home_dir}.\n"

    # System prompt: agent_def overrides core prompt; capability prompt layers on top
    core_prompt = get_core_system_prompt()
    runtime_shell_prompt = get_runtime_shell_prompt()
    agent_prompt = agent_def.system_prompt if agent_def and agent_def.system_prompt else ""
    base_prompt = agent_prompt or core_prompt
    instructions = base_prompt + context

    if agent_prompt and runtime_shell_prompt:
        instructions = instructions + "\n\n" + runtime_shell_prompt

    # Inject dynamic platform context (org/workspace/project) if available
    platform_context = get_platform_context()
    if platform_context:
        instructions = instructions + platform_context

    capability_system_prompt = (
        _read_capability_system_prompt(capability.path) if capability is not None else ""
    )
    if capability_system_prompt:
        instructions = instructions + "\n" + capability_system_prompt

    # Append CLI --system-prompt content as the final layer
    if system_prompt_append:
        instructions = instructions + "\n\n" + system_prompt_append

    if background_context:
        instructions = instructions + "\n\n" + background_context

    # 1. Inherent tools — always present. Item tools are capability opt-in and
    # added below only when the manifest asks for built-ins or custom types.
    base = default_tools(additional_toolsets=inherent_toolsets, include_items=False)

    pool: list[t.Any] = list(base.values())
    pool_names = set(base.keys())

    # Bundled @dreadnode gets the CLI helper, but it is not a global inherent tool.
    if (
        capability is not None
        and agent_def is not None
        and capability.name == _BUNDLED_DEFAULT_CAPABILITY
        and agent_def.name == _BUNDLED_DEFAULT_CAPABILITY
    ):
        from dreadnode.tools.dreadnode_cli import dreadnode_cli

        pool.append(dreadnode_cli)
        pool_names.add(dreadnode_cli.name)

    # 2. Extra tools from global capability pool — skip duplicates
    for tool in extra_tools or []:
        name = _tool_name(tool)
        if name and name not in pool_names:
            pool.append(tool)
            pool_names.add(name)

    if capability is not None and agent_def is not None:
        links = getattr(capability, "links", []) or []
        target_agents = {
            candidate.name: candidate for candidate in getattr(capability, "agents", [])
        }
        for link in links:
            if getattr(link, "source", None) != agent_def.name:
                continue
            if getattr(link, "kind", None) not in {"delegate", "subagent"}:
                continue
            target_name = getattr(link, "target", None)
            if not target_name:
                continue
            target_agent = target_agents.get(target_name)
            if target_agent is None:
                logger.warning(
                    f"Capability link target '{target_name}' not found for agent '{agent_def.name}'"
                )
                continue

            tool = _make_agent_link_tool(
                model=model,
                capability=capability,
                target_agent=target_agent,
                extra_tools=extra_tools,
                extra_hooks=extra_hooks,
                kind=link.kind,
            )
            name = _tool_name(tool)
            if name and name not in pool_names:
                pool.append(tool)
                pool_names.add(name)

    # Attribute emitted items to this capability so report_item can pass its
    # name+version for produces-schema validation. Bound to ``current_capability``
    # only for the duration of the agent's run (see ``Agent.stream``), NOT set
    # here — an unscoped set() would leak attribution into later capability-less
    # agents that share this async context.
    capability_context: tuple[str, str] | None = (
        (capability.name, getattr(capability, "version", "") or "")
        if capability is not None
        else None
    )

    # Structured items are capability opt-in. A capability gets report/update/link
    # only when `produces` selects built-ins or custom item types. The legacy
    # `items` key is still honored for compatibility.
    if capability is not None:
        pool = [item for item in pool if _tool_name(item) not in _ITEM_TOOL_NAMES]
        pool_names -= _ITEM_TOOL_NAMES

        if _capability_items_enabled(capability):
            try:
                from dreadnode.tools.report_items import (
                    build_capability_report_item,
                    link_items,
                    update_item,
                )

                report_item_tool = build_capability_report_item(
                    capability,
                    builtin_types=_selected_builtin_item_types(capability),
                )
            except Exception as exc:
                logger.warning(
                    "Failed to build typed report_item for capability {}: {}",
                    capability.name,
                    exc,
                )
                report_item_tool = None
            if report_item_tool is not None:
                pool.extend([report_item_tool, update_item, link_items])
                pool_names |= _ITEM_TOOL_NAMES

    # 3. Apply agent's tool rules (empty dict = all tools pass)
    rules = agent_def.tools if agent_def else {}
    tools = filter_tools(pool, rules, name_fn=_tool_name)

    # Engine (loop owner): explicit override > agent_def declaration > native.
    # ``inherit``/empty falls through to the native engine (``None``).
    def _resolve_engine_selector(value: str | None) -> str | None:
        return value if value and value != "inherit" else None

    resolved_engine = _resolve_engine_selector(engine) or (
        _resolve_engine_selector(agent_def.engine) if agent_def else None
    )

    agent = Agent(
        name=agent_def.name if agent_def else "dreadnode-agent",
        model=model,
        instructions=instructions,
        tools=tools,
        hooks=list(extra_hooks or []),
        max_steps=1000,
        engine=resolved_engine,
    )
    # Scope capability attribution to this agent's run (reset on exit) so it
    # never leaks to a later agent in the same async context.
    agent._capability = capability_context
    return agent


# =============================================================================
# FastAPI Application
# =============================================================================


def _warm_litellm() -> None:
    """Import litellm so the first chat turn doesn't pay the cold-import cost.

    litellm eagerly loads ~2200 modules and makes a network call to fetch
    model pricing on first import.  We skip the network call (the runtime
    doesn't need fresh pricing — cost tracking lives on the platform API)
    and run this at startup in a thread to shift the cost out of the
    user-visible request path.
    """
    _t0 = time.perf_counter()
    try:
        # Skip the httpx.get() to GitHub for model pricing on import.
        os.environ.setdefault("LITELLM_LOCAL_MODEL_COST_MAP", "True")
        import litellm
        import litellm.exceptions

        litellm.drop_params = True
        litellm.suppress_debug_info = True  # ty: ignore[invalid-assignment]

        elapsed = round((time.perf_counter() - _t0) * 1000)
        logger.info("litellm warmed in {}ms", elapsed)
    except Exception:
        elapsed = round((time.perf_counter() - _t0) * 1000)
        logger.debug("litellm warm failed after {}ms", elapsed)


def _is_synchronous_startup() -> bool:
    """Resolve the ``DREADNODE_SYNCHRONOUS_STARTUP`` env-var flag.

    When set, ``server_lifecycle()`` blocks on every backgrounded
    initialization (MCP connects, litellm warmup) before yielding —
    trading TUI-style fast startup for the deterministic toolset that
    eval orchestrators and other non-interactive callers need.
    """
    return os.environ.get("DREADNODE_SYNCHRONOUS_STARTUP", "").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )


@asynccontextmanager
async def server_lifecycle() -> t.AsyncIterator[None]:
    """Shared startup/shutdown for the SDK server runtime.

    Manages MCP server connections, litellm warmup, and any other async
    lifecycle concerns. Used by both the FastAPI lifespan (uvicorn) and the
    TUI's in-process server mode so behaviour is identical regardless of
    how the server is hosted.

    Backgrounded initializations (MCP connects, litellm warmup) normally
    proceed without blocking the lifespan so the runtime becomes ready
    immediately. Set ``DREADNODE_SYNCHRONOUS_STARTUP=1`` to wait for
    every backgrounded init to settle before yielding — eval runs and
    other non-interactive contexts want this so their first agent turn
    sees the full toolset rather than racing it.
    """
    state = get_state()
    registry = state.capability_registry
    synchronous = _is_synchronous_startup()

    # Revoke a runtime token's live websockets and outstanding tickets the
    # moment it is rotated out. Wired here rather than at the uvicorn entrypoint
    # so every host of this app gets it (and so it is exercised by tests).
    get_token_source().set_on_retire(_on_runtime_token_retired)

    # MCP server connections — start() is non-blocking by design
    # (CAP-MCP-009); the wait happens below if requested.
    if registry and registry.mcp_manager is None:
        registry.mcp_manager = capability_manager.MCPLifecycleManager(event_bus=state.event_bus)
    if registry and registry.mcp_manager:
        await registry.mcp_manager.start(registry)

    # Workers start AFTER MCP servers (CAP-WLIF-002)
    if registry and registry.worker_manager is None:
        from dreadnode.app.server.worker_manager import WorkerLifecycleManager

        registry.worker_manager = WorkerLifecycleManager(state.event_bus, app)
    if registry and registry.worker_manager:
        await registry.worker_manager.start(registry)

    # Set critical litellm flags eagerly (before background import) so they
    # are active even if a chat request arrives before warmup completes.
    try:
        import litellm

        litellm.drop_params = True
        litellm.suppress_debug_info = True  # ty: ignore[invalid-assignment]
    except Exception:  # noqa: S110 - _warm_litellm will retry the full import
        pass

    # Warm litellm in a background thread so the health endpoint goes live
    # immediately while the ~2s import finishes in the background.
    warm_future = asyncio.get_running_loop().run_in_executor(None, _warm_litellm)

    if synchronous:
        wait_started_at = time.perf_counter()
        if registry and registry.mcp_manager:
            # Bounded by the per-server ``init_timeout`` (default 30s) —
            # never blocks indefinitely. Servers that need interactive
            # auth still settle into ``needs_auth`` once the bridge
            # times out, so the eval runs with an honest toolset.
            await registry.mcp_manager.wait_for_connects()
        # warmup logs its own failure; we just want it settled.
        with suppress(Exception):
            await asyncio.wrap_future(warm_future)
        logger.info(
            "Synchronous startup complete | total_ms={}",
            round((time.perf_counter() - wait_started_at) * 1000),
        )

    try:
        yield
    finally:
        if not synchronous:
            with suppress(Exception):
                await asyncio.wait_for(asyncio.shield(warm_future), timeout=2)
        # Workers stop BEFORE MCP teardown
        if registry and registry.worker_manager:
            await registry.worker_manager.stop()
        if registry and registry.mcp_manager:
            await registry.mcp_manager.stop()


@asynccontextmanager
async def _lifespan(_app_instance: t.Any) -> t.AsyncIterator[None]:
    """FastAPI lifespan: populate registry then delegate to server_lifecycle.

    Registry population is done here (rather than only in ``run_server()``)
    so that uvicorn ``--reload`` and externalized uvicorn invocations work:
    on reload the module is reimported and ``app.state`` is fresh, so the
    lifespan re-discovers capabilities automatically.
    """
    from dreadnode import _get_default_instance

    state = get_state()

    # Populate registry if not already done (supports both direct and reload paths).
    # When run_server() is used, it populates before uvicorn starts and we skip.
    # When uvicorn is invoked directly (e.g. from Docker provider), we populate here.
    if state.capability_registry is None:
        instance = _get_default_instance()
        if not instance._initialized:
            instance.configure()
        await asyncio.to_thread(_populate_registry, instance)

    async with server_lifecycle():
        yield


app = FastAPI(
    title="Dreadnode Agent Server",
    description="REST + WebSocket server for Dreadnode agents",
    version="1.0.0",
    lifespan=_lifespan,
)

# CORS must be at module level so it survives uvicorn --reload (module reimport).
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SandboxAuthMiddleware)


def _platform_usage_totals(
    usage: dict[str, t.Any] | None,
) -> tuple[int, int, float | None, int | None]:
    """Roll a platform ``SessionUsageResponse`` dict up into the runtime's
    flat ``(total_tokens, total_tool_call_count, total_cost_usd,
    last_generation_input_tokens)`` shape.

    The platform's :class:`SessionUsageResponse` doesn't expose
    ``total_tokens`` directly — it splits input across raw / cache-read /
    cache-creation buckets. Match the frontend's ``normalizeSession``
    rollup (``agents.svelte.ts``) so TUI rows surface the same total a
    user sees on the web monitoring grid:

        total = input + cache_read + cache_creation + output

    ``last_generation_input_tokens`` passes through verbatim — it's the
    "context the model last saw" value the TUI gauge displays.
    """
    if not isinstance(usage, dict):
        return 0, 0, None, None
    total_input = (
        int(usage.get("total_input_tokens", 0) or 0)
        + int(usage.get("total_cache_read_input_tokens", 0) or 0)
        + int(usage.get("total_cache_creation_input_tokens", 0) or 0)
    )
    total_output = int(usage.get("total_output_tokens", 0) or 0)
    tool_calls = int(usage.get("total_tool_call_count", 0) or 0)
    raw_cost = usage.get("total_cost_usd")
    cost = float(raw_cost) if raw_cost is not None else None
    raw_last_input = usage.get("last_generation_input_tokens")
    last_input = int(raw_last_input) if isinstance(raw_last_input, int) else None
    return total_input + total_output, tool_calls, cost, last_input


def _normalize_platform_session(s: dict[str, t.Any]) -> dict[str, t.Any]:
    """Translate a platform ``SessionResponse`` dict into the runtime's
    ``SessionInfo`` wire shape so the SDK's ``SessionInfo.from_dict`` /
    ``SessionListResult.from_dict`` can decode it without special-casing
    the browse path.

    Platform field names differ from the runtime's historical shape:

    - ``id`` → ``session_id``
    - ``project_name`` → ``project``
    - ``usage`` (split-bucket dict) → flat ``total_tokens`` /
      ``total_tool_call_count`` / ``total_cost_usd`` rollups
    - everything else passes through verbatim (including new lifecycle
      and label fields).
    """
    total_tokens, tool_calls, cost, last_input_tokens = _platform_usage_totals(s.get("usage"))
    return {
        "session_id": str(s.get("id", "")),
        "group_id": str(s["group_id"]) if s.get("group_id") else None,
        "project": s.get("project_name"),
        "created_at": s.get("created_at"),
        "updated_at": s.get("updated_at"),
        "message_count": s.get("message_count", 0),
        "session_dir": None,
        "capability": None,
        "agent": s.get("agent"),
        "model": s.get("model"),
        "title": s.get("title"),
        # Platform exposes the denormalized first-user-message snippet as
        # ``preview_text`` (SES-LST-011); the runtime's historical wire
        # field is ``preview``.
        "preview": s.get("preview_text") or s.get("preview"),
        # Platform-sourced lifecycle + identity fields.
        "visibility": s.get("visibility", "private"),
        "origin": s.get("origin", "user"),
        "archived_at": s.get("archived_at"),
        "frozen_at": s.get("frozen_at"),
        "frozen_by": s.get("frozen_by"),
        "labels": s.get("labels") or {},
        "created_by": s.get("created_by"),
        "user_id": str(s["user_id"]) if s.get("user_id") else None,
        "total_tokens": total_tokens,
        "total_tool_call_count": tool_calls,
        "total_cost_usd": cost,
        "last_generation_input_tokens": last_input_tokens,
    }


class ServerState:
    """Server state container stored on app.state."""

    def __init__(self) -> None:
        self.capability_registry: capability_manager.CapabilityRegistry | None = None
        self.event_bus = runtime_events.EventBus()
        self._sessions: dict[str, SessionRuntime] = {}
        self._session_hydrator = SessionHydrator(
            sessions=self._sessions,
            resolve_persisted_binding=self._resolve_persisted_binding,
            get_api_context=self._get_api_context,
            session_factory=self._create_hydrated_session,
        )
        # CLI overrides — sticky across /reload
        self.capability_dirs: list[str] | None = None
        self.enabled_capabilities: list[str] | None = None
        self.capability_flag_overrides: list[str] | None = None
        self.system_prompt_append: str | None = None
        # Authoritative connection identity for subprocess workers (and any
        # other capability subprocess that uses RuntimeClient). Populated by
        # whoever owns the bound socket — ManagedRuntimeClient for the TUI's
        # in-process runtime, run_server() for `dn serve`. Workers read these
        # via WorkerLifecycleManager._runtime_contract_env instead of
        # re-deriving from env, so the URL always matches the real bind.
        self.runtime_url: str | None = None
        self.runtime_token: str | None = None
        self.runtime_id: str | None = None
        # Single-use websocket auth tickets for browser clients, which cannot
        # set an Authorization header on the ws handshake. See ws_auth.py.
        self.ws_ticket_store = ws_auth.WsTicketStore()
        # Live websocket connections, tracked so they can be force-closed when
        # the runtime token rotates (lossless reconnect).
        self.ws_connections = WebSocketConnectionRegistry()

    def _get_session_store(self) -> SessionStore | None:
        """Get the local SQLite session store for legacy read-only fallback.

        Only returns a store if the SQLite database already exists on disk.
        Never creates a new database — new sessions go to the platform API.
        """
        try:
            from dreadnode import _get_default_instance
            from dreadnode.storage import SessionStore

            storage = _get_default_instance().storage
            # Check if the SQLite file exists without triggering creation
            db_file = storage.sessions_path / "sessions.sqlite3"
            if not db_file.exists():
                return None
            session_store = getattr(storage, "session_store", None)
            return session_store if isinstance(session_store, SessionStore) else None
        except Exception:
            logger.debug("Session store unavailable", exc_info=True)
            return None

    def _resolve_persisted_binding(
        self,
        capability_name: str | None,
        agent_name: str | None,
    ) -> tuple[str | None, Capability | None, AgentDef | None]:
        return _resolve_session_binding(
            self.capability_registry,
            capability_name=capability_name,
            agent_name=agent_name,
        )

    def _session_info_from_record(
        self, record: SessionRecord, preview: str | None = None
    ) -> SessionInfo:
        session_dir: str | None = None
        try:
            from dreadnode import _get_default_instance

            session_dir = str(_get_default_instance().storage.session_path(record.session_id))
        except Exception:
            logger.debug("Session directory unavailable", exc_info=True)

        return SessionInfo(
            session_id=record.session_id,
            project=record.project,
            created_at=record.created_at,
            updated_at=record.updated_at,
            message_count=record.message_count,
            session_dir=session_dir,
            capability=record.capability,
            agent=record.agent,
            model=record.model or None,
            title=record.title,
            preview=preview,
        )

    def _create_hydrated_session(
        self,
        session_id: str,
        *,
        model: str | None,
        project: str | None,
        capability_name: str | None,
        capability: Capability | None,
        agent_def: AgentDef | None,
    ) -> SessionRuntime:
        """Create a SessionRuntime for hydrated restore flows."""
        return SessionRuntime(
            session_id,
            event_bus=self.event_bus,
            model=model,
            project=project,
            registry=self.capability_registry,
            capability_name=capability_name,
            capability=capability,
            agent_def=agent_def,
            group_id=None,
        )

    def _get_api_context(self) -> tuple[t.Any, str, str, str] | None:
        """Return (api_client, org, workspace, user_id) if platform sync is available.

        Returns ``None`` if any of org/workspace/user are missing — callers
        skip platform integration in that case. The validated user id is
        required because the platform's session list defaults to
        workspace-wide; without a ``user_id`` filter the TUI session view
        would surface other workspace members' sessions. Reaching the
        TUI session view in the first place implies a validated user, so
        the missing-user branch is a safety net, not a routine path.
        """
        try:
            from dreadnode import _get_default_instance

            instance = _get_default_instance()
            if not instance.can_sync:
                return None
            api = instance.api
            org = instance.organization
            ws = instance.workspace
            user = instance.profile.user
            if not isinstance(org, str) or not isinstance(ws, str):
                return None
            if user is None:
                return None
        except Exception:
            return None
        else:
            return api, org, ws, user.id

    def get_session(self, session_id: str) -> SessionRuntime | None:
        """Get a session by ID — from memory, then API, then local store."""
        session = self._sessions.get(session_id)
        if session is not None:
            session.refresh_registry(self.capability_registry)
            return session

        # Try API first
        session = self._session_hydrator.hydrate_from_api(session_id)
        if session is not None:
            return session

        # Fall back to local session store (legacy)
        session_store = self._get_session_store()
        if session_store is None:
            return None

        record = session_store.get_session(session_id)
        if record is None:
            return None

        return self._session_hydrator.hydrate_record(record)

    def has_session(self, session_id: str) -> bool:
        """Check if a session exists."""
        return session_id in self._sessions

    def list_sessions(self) -> list[SessionRuntime]:
        """List all sessions."""
        return list(self._sessions.values())

    async def browse_platform_sessions(
        self,
        *,
        page: int,
        limit: int,
        sort_by: str,
        sort_dir: str,
        archived: str,
        label: list[str] | None,
        user_id: str | None,
        project_id: list[str] | None,
        origin: list[str] | None = None,
        search: str | None,
        include_workload_sessions: bool = False,
    ) -> dict[str, t.Any]:
        """Forward a paginated list query to the platform and normalize the
        envelope so the runtime's SDK clients can decode it via
        :class:`SessionListResult`.

        In-process sessions are NOT merged on this path — the table-view
        consumer trusts ``_register_session_with_platform`` to sync within
        a turn (per the §2 plan). Boot/swap callers should use
        :meth:`list_session_infos` for the live in-process set.
        """
        ctx = self._get_api_context()
        if ctx is None:
            return {
                "sessions": [],
                "total": 0,
                "page": page,
                "limit": limit,
                "total_pages": 0,
                "has_next": False,
                "has_previous": False,
            }
        api, org, ws, ctx_user_id = ctx
        # If the caller didn't pin user_id, default to the current user so
        # the workspace-wide list doesn't accidentally surface other users'
        # workspace-visible sessions in the boot/swap UX. The new table view
        # passes ``user_id=None`` explicitly (with the visibility predicate
        # doing the right thing) when it wants the cross-user view.
        effective_user_id = user_id if user_id is not None else ctx_user_id
        kwargs: dict[str, t.Any] = {
            "page": page,
            "limit": limit,
            "sort_by": sort_by,
            "sort_dir": sort_dir,
            "archived": archived,
            "include_workload_sessions": include_workload_sessions,
        }
        if effective_user_id is not None:
            kwargs["user_id"] = effective_user_id
        if label:
            kwargs["label"] = label
        if project_id:
            kwargs["project_id"] = project_id
        if origin:
            kwargs["origin"] = origin
        if search:
            kwargs["search"] = search
        try:
            data = await asyncio.to_thread(api.list_sessions, org, ws, **kwargs)
        except Exception:
            logger.opt(exception=True).warning("Failed to browse platform sessions")
            return {
                "sessions": [],
                "total": 0,
                "page": page,
                "limit": limit,
                "total_pages": 0,
                "has_next": False,
                "has_previous": False,
            }
        normalized = [
            _normalize_platform_session(s) for s in data.get("sessions", []) if isinstance(s, dict)
        ]
        return {
            "sessions": normalized,
            "total": int(data.get("total", len(normalized))),
            "page": int(data.get("page", page)),
            "limit": int(data.get("limit", limit)),
            "total_pages": int(data.get("total_pages", 1)),
            "has_next": bool(data.get("has_next", False)),
            "has_previous": bool(data.get("has_previous", False)),
        }

    async def browse_platform_facets(
        self,
        *,
        archived: str,
        label: list[str] | None,
        user_id: str | None,
        project_id: list[str] | None,
        origin: list[str] | None = None,
        search: str | None,
        include_workload_sessions: bool = False,
    ) -> dict[str, t.Any]:
        """Forward a facets query to the platform and return the raw
        ``{labels: {key: [{value, count}]}}`` envelope.

        Parallels :meth:`browse_platform_sessions`. The platform's facets
        endpoint omits keys with zero matches (SES-LBL-061); this wrapper
        returns an empty envelope instead of raising when the caller is
        unauthenticated so the sidebar can render without flashing an
        error during boot.
        """
        empty: dict[str, t.Any] = {"labels": {}}
        ctx = self._get_api_context()
        if ctx is None:
            return empty
        api, org, ws, ctx_user_id = ctx
        effective_user_id = user_id if user_id is not None else ctx_user_id
        kwargs: dict[str, t.Any] = {
            "archived": archived,
            "include_workload_sessions": include_workload_sessions,
        }
        if effective_user_id is not None:
            kwargs["user_id"] = effective_user_id
        if label:
            kwargs["label"] = label
        if project_id:
            kwargs["project_id"] = project_id
        if origin:
            kwargs["origin"] = origin
        if search:
            kwargs["search"] = search
        try:
            data = await asyncio.to_thread(api.get_session_facets, org, ws, **kwargs)
        except Exception:
            logger.opt(exception=True).warning("Failed to fetch session facets")
            return empty
        labels_raw = data.get("labels") or {}
        if not isinstance(labels_raw, dict):
            return empty
        return {"labels": labels_raw}

    def list_session_infos(self, *, include_platform: bool = False) -> list[SessionInfo]:
        """List active sessions, optionally merged with platform-persisted sessions.

        The platform fetch is a ~500ms round-trip that callers only need
        when rendering the full history (session picker, ``/sessions``
        slash command). Boot, runtime swap, and other fast paths skip it
        and get only the in-process set (plus legacy local store).
        """
        sessions = {session.session_id: session.to_info() for session in self._sessions.values()}

        # Platform-scoped list — scoped to the current user via ``user_id``
        # and to this SDK runtime via ``DREADNODE_RUNTIME_ID`` (None on
        # local, the sandbox id on remote). ``save_session`` tags new rows
        # with the same env so the filter stays consistent. Without the
        # runtime scope a local SDK server surfaces sessions from every
        # runtime the user has connected to, and the TUI swap-back lands
        # on a stray remote session. Stop-gap until the platform endpoint
        # gains a first-class runtime_id filter.
        own_runtime_id = os.environ.get("DREADNODE_RUNTIME_ID", "").strip() or None
        ctx = self._get_api_context()
        if include_platform and ctx is not None:
            api, org, ws, user_id = ctx
            try:
                data = api.list_sessions(org, ws, limit=100, user_id=user_id)
                for s in data.get("sessions", []):
                    sid = s.get("id", "")
                    session_runtime_id = s.get("runtime_id")
                    if session_runtime_id is not None:
                        session_runtime_id = str(session_runtime_id)
                    if session_runtime_id != own_runtime_id:
                        continue
                    if sid and sid not in sessions:
                        (
                            total_tokens,
                            tool_calls,
                            cost,
                            last_input_tokens,
                        ) = _platform_usage_totals(s.get("usage"))
                        sessions[sid] = SessionInfo(
                            session_id=sid,
                            project=s.get("project_name"),
                            group_id=str(s["group_id"]) if s.get("group_id") else None,
                            created_at=datetime.fromisoformat(s["created_at"])
                            if s.get("created_at")
                            else datetime.now(UTC),
                            message_count=s.get("message_count", 0),
                            session_dir=None,
                            capability=None,
                            agent=s.get("agent"),
                            model=s.get("model"),
                            title=s.get("title"),
                            preview=s.get("preview_text") or s.get("preview"),
                            total_tokens=total_tokens,
                            total_tool_call_count=tool_calls,
                            total_cost_usd=cost,
                            last_generation_input_tokens=last_input_tokens,
                        )
            except Exception:
                logger.debug("Failed to list sessions from API", exc_info=True)

        # Fall back to local session store for any additional sessions (legacy)
        session_store = self._get_session_store()
        if session_store is not None:
            stored_records = session_store.list_sessions()
            store_only_ids = [r.session_id for r in stored_records if r.session_id not in sessions]
            previews = session_store.first_user_messages(store_only_ids) if store_only_ids else {}
            for record in stored_records:
                sessions.setdefault(
                    record.session_id,
                    self._session_info_from_record(record, preview=previews.get(record.session_id)),
                )
        return sorted(
            sessions.values(),
            key=lambda session: session.updated_at or session.created_at,
            reverse=True,
        )

    def create_session(
        self,
        *,
        session_id: str | None = None,
        model: str | None = None,
        project: str | None = None,
        capability: str | None = None,
        agent: str | None = None,
        messages: list[SessionMessage] | None = None,
        policy: str | dict[str, t.Any] | None = None,
        labels: dict[str, list[str]] | None = None,
        origin: str | None = None,
        group_id: str | None = None,
        engine: str | None = None,
        project_memory_scope_kind: str = _PROJECT_MEMORY_SCOPE_PROJECT,
        enable_project_memory_preload: bool = True,
        project_memory_preload_limit: int = 20,
    ) -> SessionRuntime:
        """Create a new session or return an existing compatible one."""
        if session_id is not None and not session_id:
            raise ValueError("session_id must be a non-empty string")
        resolved_id = session_id or str(uuid4())

        if resolved_id in self._sessions:
            session = self._sessions[resolved_id]
            if agent is not None and session.agent_name is not None and agent != session.agent_name:
                raise ValueError(
                    f"Session '{resolved_id}' already started with agent '{session.agent_name}'. "
                    f"Create a new session to start with agent '{agent}'."
                )
            # Engine is sticky for the session (CAP-ERES-007) — reject a change.
            if engine is not None and session._engine is not None and engine != session._engine:
                raise ValueError(
                    f"Session '{resolved_id}' is already bound to engine "
                    f"'{session._engine}'. Create a new session to use engine '{engine}'."
                )
            if model is not None and model != session.model:
                session.model = model
                session._persist_state(update_messages=False)
            return session

        session_store = self._get_session_store()
        if session_store is not None:
            record = session_store.get_session(resolved_id)
            if record is not None:
                if agent is not None and record.agent is not None and agent != record.agent:
                    raise ValueError(
                        f"Session '{resolved_id}' already started with agent '{record.agent}'. "
                        f"Create a new session to start with agent '{agent}'."
                    )
                session = self._session_hydrator.hydrate_record(record)
                if model is not None and model != session.model:
                    session.model = model
                    session._persist_state(update_messages=False)
                return session

        if self.capability_registry is not None:
            capability_name, capability_obj, agent_def = self.capability_registry.resolve(
                capability_name=capability,
                agent_name=agent,
            )
        else:
            capability_name, capability_obj, agent_def = (None, None, None)

        from dreadnode.policies import resolve_policy

        resolved_policy = resolve_policy(policy)
        session = SessionRuntime(
            resolved_id,
            event_bus=self.event_bus,
            model=model,
            project=project,
            registry=self.capability_registry,
            capability_name=capability_name,
            capability=capability_obj,
            agent_def=agent_def,
            policy=resolved_policy,
            reserved_labels=labels,
            origin=origin,
            group_id=group_id,
            engine=engine,
            project_memory_scope_kind=project_memory_scope_kind,
            enable_project_memory_preload=enable_project_memory_preload,
            project_memory_preload_limit=project_memory_preload_limit,
        )
        self._sessions[resolved_id] = session
        try:
            loop = asyncio.get_running_loop()
            task = loop.create_task(
                self.event_bus.publish(
                    kind=runtime_events.EVENT_SESSION_CREATED,
                    payload={"session_id": resolved_id},
                )
            )
            task.add_done_callback(lambda t: t.exception() if not t.cancelled() else None)
        except RuntimeError:
            pass
        if messages:
            session.restore_messages(messages, model=model)
        else:
            session._persist_state(update_messages=False)

        # Best-effort registration with platform
        _register_session_with_platform(session, bootstrap_model=model)

        # Eagerly create the agent so first chat doesn't pay tool-assembly cost
        try:
            session.get_agent(model=model)
        except Exception:
            logger.debug("Eager agent creation deferred", exc_info=True)

        return session

    def delete_session(self, session_id: str) -> bool:
        """Delete a session. Returns True if deleted, False if not found.

        Propagates the delete to the platform first when an API context is
        available so the row doesn't reappear on the next ``browse_sessions``
        refresh. Local in-memory + SQLite cleanup runs regardless — a failed
        platform delete raises before we touch local state so the user sees
        the error in the picker rather than a silent half-delete.
        """
        platform_deleted = _delete_session_on_platform(session_id)

        deleted = False
        session = self._sessions.pop(session_id, None)
        if session is not None:
            try:
                loop = asyncio.get_running_loop()
                task = loop.create_task(
                    self.event_bus.publish(
                        kind=runtime_events.EVENT_SESSION_DELETED,
                        payload={"session_id": session_id},
                    )
                )
                task.add_done_callback(lambda t: t.exception() if not t.cancelled() else None)
            except RuntimeError:
                pass
            session.close()
            deleted = True

        session_store = self._get_session_store()
        if session_store is not None:
            deleted = session_store.delete_session(session_id) or deleted

        return deleted or platform_deleted

    def archive_session(self, session_id: str, *, archived: bool) -> bool:
        """Toggle a session's archive state on the platform.

        Returns ``True`` when the platform applied the flip, ``False`` when
        no platform context is available (purely-local sessions can't be
        archived — the concept lives on the platform). Local in-process state
        is left untouched: archive is a metadata flip, not a deletion.
        """
        return _archive_session_on_platform(session_id, archived=archived)

    def freeze_session(self, session_id: str) -> bool:
        """Mark a session frozen on the platform (terminal, idempotent).

        Returns ``True`` when the platform applied the freeze, ``False`` when
        no platform context is available. Frozen sessions can still be loaded
        for read; the platform rejects any new turns.
        """
        return _freeze_session_on_platform(session_id)


def _is_sandbox_mode() -> bool:
    """True when running inside a platform sandbox (not local TUI)."""
    return bool(os.environ.get("DREADNODE_RUNTIME_ID", "").strip())


def _resolve_platform_api() -> tuple[t.Any, str, str] | None:
    """Resolve the platform API client + org/workspace context for proxying.

    Returns ``None`` when the SDK isn't authenticated or hasn't been
    configured for sync — callers should treat that as a no-op rather than
    raising, so unauthenticated TUI use keeps working.
    """
    try:
        from dreadnode import _get_default_instance

        instance = _get_default_instance()
        if not instance.can_sync:
            return None
        org = instance.organization
        ws = instance.workspace
    except Exception:
        logger.opt(exception=True).debug("Platform proxy skipped: api context unavailable")
        return None
    if not isinstance(org, str) or not isinstance(ws, str):
        return None
    return instance.api, org, ws


def _resolve_platform_project_id(
    api: t.Any,
    org: str,
    ws: str,
    *,
    project_key: str | None = None,
) -> str | None:
    """Resolve the active platform project UUID for session/group writes."""
    from dreadnode import _get_default_instance

    instance = _get_default_instance()
    if project_key is None:
        default_project_key = getattr(instance, "project", None)
        if isinstance(default_project_key, str):
            project_key = default_project_key

    active_profile = getattr(instance, "_profile", None)
    active_project_key = getattr(active_profile, "project", None)
    active_project_id = getattr(active_profile, "project_id", None)
    if (
        project_key
        and active_project_id is not None
        and (active_project_key is None or active_project_key == project_key)
    ):
        return str(active_project_id)
    if project_key:
        project = api.get_project(org, ws, project_key)
        return str(project.id)
    return None


def _delete_session_on_platform(session_id: str) -> bool:
    """Forward a session delete to the platform when sync is available.

    Returns ``True`` when the platform row was removed, ``False`` when no
    platform context is available or the session was already absent (404).
    Other failures raise so the caller surfaces the error to the user
    instead of silently leaving a half-deleted state. A session that was
    only ever local (never registered with the platform) 404s here and is
    therefore treated as a successful no-op.
    """
    resolved = _resolve_platform_api()
    if resolved is None:
        return False
    api, org, ws = resolved
    from dreadnode.app.api.client import NotFoundError

    try:
        api.delete_session(org, ws, session_id)
    except NotFoundError:
        return False
    return True


def _archive_session_on_platform(session_id: str, *, archived: bool) -> bool:
    """Forward a session archive/unarchive to the platform.

    Returns ``False`` when no platform context is available (no auth /
    no workspace) so the caller can degrade silently. Other failures
    raise so the user sees the error instead of a silent no-op.
    """
    resolved = _resolve_platform_api()
    if resolved is None:
        return False
    api, org, ws = resolved
    if archived:
        api.archive_session(org, ws, session_id)
    else:
        api.unarchive_session(org, ws, session_id)
    return True


def _freeze_session_on_platform(session_id: str) -> bool:
    """Forward a session freeze to the platform when sync is available."""
    resolved = _resolve_platform_api()
    if resolved is None:
        return False
    api, org, ws = resolved
    api.freeze_session(org, ws, session_id)
    return True


def _create_session_group_on_platform(
    request: SessionGroupCreateRequest,
) -> dict[str, t.Any] | None:
    """Forward session group creation to the platform when sync is available."""
    resolved = _resolve_platform_api()
    if resolved is None:
        return None
    api, org, ws = resolved
    project_id = _resolve_platform_project_id(
        api,
        org,
        ws,
        project_key=request.project,
    )
    if project_id is None:
        raise ValueError("Session group creation requires a platform project")
    runtime_id = request.runtime_id or os.environ.get("DREADNODE_RUNTIME_ID", "").strip() or None
    return api.create_session_group(
        org,
        ws,
        project_id=project_id,
        kind=request.kind,
        title=request.title,
        status=request.status,
        runtime_id=runtime_id,
        capability=request.capability,
        capability_version=request.capability_version,
        worker=request.worker,
        evaluation_id=request.evaluation_id,
        evaluation_item_id=request.evaluation_item_id,
        evaluation_item_attempt_id=request.evaluation_item_attempt_id,
        metadata=request.metadata,
    )


def _update_session_group_on_platform(
    group_id: str,
    request: SessionGroupUpdateRequest,
) -> dict[str, t.Any] | None:
    """Forward session group lifecycle updates to the platform."""
    resolved = _resolve_platform_api()
    if resolved is None:
        return None
    api, org, ws = resolved
    return api.update_session_group(
        org,
        ws,
        group_id,
        title=request.title,
        status=request.status,
    )


def _register_session_with_platform(
    session: SessionRuntime, *, bootstrap_model: str | None = None
) -> None:
    """Best-effort registration of a new session with the platform API.

    Fire-and-forget: logs warnings on failure but never raises.
    Runs whenever the SDK can sync (authenticated profile), not just in sandbox mode.
    """
    try:
        from dreadnode import _get_default_instance

        instance = _get_default_instance()
        if not instance.can_sync:
            logger.debug("Session registration skipped: can_sync=False")
            return

        api = instance.api
        org = instance.organization
        ws = instance.workspace

        if not isinstance(org, str) or not isinstance(ws, str):
            logger.debug("Session registration skipped: org={!r}, ws={!r}", org, ws)
            return

        project_key = session.project_key
        if project_key is None:
            default_project_key = getattr(instance, "project", None)
            if isinstance(default_project_key, str):
                project_key = default_project_key

        project_id = _resolve_platform_project_id(
            api,
            org,
            ws,
            project_key=project_key,
        )

        runtime_id = os.environ.get("DREADNODE_RUNTIME_ID", "").strip() or None

        # SES-LBL-022: stamp capability-owned reserved labels when the session
        # runs inside a capability. Worker-bound RuntimeClients
        # (CAP-WCLI-022) additionally pre-stamp ``worker:<name>`` via
        # ``_reserved_labels`` and set ``origin=worker`` via ``_origin``.
        labels: dict[str, list[str]] = {}
        capability = session._capability
        if capability is not None:
            capability_name = getattr(capability, "name", None)
            capability_version = getattr(capability, "version", None)
            if isinstance(capability_name, str) and isinstance(capability_version, str):
                # SES-LBL-013 requires capability label values to be
                # ``{org}/{name}``. The local manifest's ``name`` may be bare
                # (e.g. ``airt``) or already qualified (e.g. ``dreadnode/airt``)
                # depending on how it was authored. Compose against the active
                # org so platform validation accepts either shape.
                qualified_name = (
                    capability_name if "/" in capability_name else f"{org}/{capability_name}"
                )
                labels["capability"] = [qualified_name]
                labels["capability_version"] = [capability_version]
        # Caller-supplied reserved overrides (e.g. ``worker:<name>`` from a
        # worker-bound RuntimeClient) merge into the label dict.
        for key, values in session._reserved_labels.items():
            labels[key] = list(values)

        # SES-ORG-003: default origin is ``user``. Worker-bound clients set
        # this to ``worker`` via the runtime client's default_session_origin.
        origin = session._origin or "user"

        api.save_session(
            org,
            ws,
            session.session_id,
            model_resolution.resolve_turn_model_config(
                bootstrap_model,
                session.model,
                session._agent_def,
            ).canonical_model,
            agent=session.agent_name,
            title=session.title,
            message_count=session.message_count,
            project_id=project_id,
            runtime_id=runtime_id,
            group_id=session._group_id,
            labels=labels,
            origin=origin,
        )
        session._platform_registered = True
        session.mark_sync_ok()
    except Exception as exc:
        session.mark_sync_degraded(exc)
        logger.opt(exception=True).warning("Failed to register session with platform")


def _sync_accepted_turn_with_platform(
    session: SessionRuntime,
    *,
    model: str | None = None,
    agent: str | None = None,
) -> None:
    """Best-effort sync of the accepted turn snapshot to platform storage."""
    if model is None and agent is None:
        return

    try:
        # Lazy registration: if the session wasn't registered during creation
        # (e.g. because the Dreadnode instance wasn't fully configured yet),
        # register it now before attempting the update.
        if not session._platform_registered:
            _register_session_with_platform(session, bootstrap_model=model or session.model)
            if not session._platform_registered:
                return  # Still can't register — give up silently

        from dreadnode import _get_default_instance

        instance = _get_default_instance()

        if not instance.can_sync:
            return

        org = instance.organization
        ws = instance.workspace
        if not isinstance(org, str) or not isinstance(ws, str):
            return

        instance.api.update_session(
            org,
            ws,
            session.session_id,
            model=model,
            agent=agent,
        )
        session.mark_sync_ok()
    except Exception as exc:
        session.mark_sync_degraded(exc)
        logger.opt(exception=True).warning("Failed to sync accepted turn with platform")


def get_state() -> ServerState:
    """Get the server state from app.state."""
    if not hasattr(app.state, "server"):
        app.state.server = ServerState()
    return app.state.server


# =============================================================================
# Session Runtime
# =============================================================================


class SessionRuntime:
    """Encapsulates the runtime state for a single persisted session."""

    def __init__(
        self,
        session_id: str,
        *,
        event_bus: runtime_events.EventBus | None = None,
        model: str | None = None,
        project: str | None = None,
        registry: capability_manager.CapabilityRegistry | None = None,
        capability_name: str | None = None,
        capability: Capability | None = None,
        agent_def: AgentDef | None = None,
        policy: SessionPolicy | None = None,
        reserved_labels: dict[str, list[str]] | None = None,
        origin: str | None = None,
        group_id: str | None = None,
        engine: str | None = None,
        project_memory_scope_kind: str = _PROJECT_MEMORY_SCOPE_PROJECT,
        enable_project_memory_preload: bool = True,
        project_memory_preload_limit: int = 20,
    ) -> None:
        from dreadnode.policies import InteractiveSessionPolicy

        self.session_id = session_id
        self.model = model or ""
        # Loop owner, bound once at session creation and sticky for the session's
        # life (CAP-ERES-007). ``None`` falls through to the agent's declared
        # engine and ultimately the native engine. Unlike ``model`` it does not
        # vary per turn — the harness owns the session loop.
        self._engine: str | None = engine
        self.project_key = project
        self.created_at = datetime.now(UTC)
        self.title: str | None = None

        self._agent: Agent | None = None
        self._session_dir: Path | None = None
        self._turns = SessionTurnCoordinator(session_id)
        self._event_bus = event_bus or runtime_events.EventBus()
        self._registry = registry
        self._capability_name = capability_name
        self._capability = capability
        self._agent_def = agent_def
        self._policy: SessionPolicy = policy or InteractiveSessionPolicy()
        # Reserved-label overrides supplied by the caller (e.g. a worker-bound
        # RuntimeClient per CAP-WCLI-022). Consumed once at platform
        # registration to co-stamp ``worker:<name>`` (SES-LBL-024).
        self._reserved_labels: dict[str, list[str]] = dict(reserved_labels or {})
        # SES-ORG-003: session origin supplied by the caller. Worker-bound
        # RuntimeClients set this to ``worker``; standalone clients leave it
        # ``None`` and the platform's ``user`` default applies.
        self._origin: str | None = origin
        self._group_id: str | None = group_id
        normalized_scope_kind = (
            project_memory_scope_kind.strip() if project_memory_scope_kind else ""
        )
        self._project_memory_scope_kind = normalized_scope_kind or _PROJECT_MEMORY_SCOPE_PROJECT
        self._enable_project_memory_preload = enable_project_memory_preload
        self._project_memory_preload_limit = project_memory_preload_limit
        self._project_memory_background_context = ""
        if (
            self._enable_project_memory_preload
            and self._project_memory_scope_kind == _PROJECT_MEMORY_SCOPE_PROJECT
        ):
            self._project_memory_background_context = self._load_project_memory_background_context()
        self._generate_params_extra: dict[str, t.Any] = {}
        self._message_count: int = 0
        self._agent_name_override: str | None = None
        self._last_turn_agent: str | None = None
        # Session owns the trajectory — agents are ephemeral
        from dreadnode.agents.trajectory import Trajectory as TrajectoryModel

        self._trajectory = TrajectoryModel()

        self._prompt_registry = SessionPromptRegistry()
        self._persistence = SessionPersistenceCoordinator(
            session_id=session_id,
            resolve_api_context=self._get_api_context,
            register_session=lambda: _register_session_with_platform(self),
            get_platform_registered=lambda: self._platform_registered,
            get_model=lambda: self.model,
            get_title=lambda: self.title,
            get_agent_name=lambda: self.agent_name,
            get_trajectory=lambda: self._trajectory,
            resolve_agent_system_prompt=lambda agent_name: (
                agent_def.system_prompt
                if (agent_def := self._agent_def_for_turn(agent_name)) is not None
                else None
            ),
        )

        # Compaction state
        self._compaction_task: asyncio.Task[dict[str, t.Any]] | None = None

        # Platform sync
        self._platform_registered: bool = False
        self._sync_last_error: str | None = None
        self._sync_last_attempt_at: datetime | None = None
        try:
            self._event_loop: asyncio.AbstractEventLoop | None = asyncio.get_running_loop()
        except RuntimeError:
            self._event_loop = None

    @property
    def _storage(self) -> t.Any:
        from dreadnode import _get_default_instance

        return _get_default_instance().storage

    @property
    def capability_name(self) -> str | None:
        """Name of the capability bound to this session."""
        return self._capability_name

    @property
    def event_bus(self) -> runtime_events.EventBus:
        """Runtime event bus shared across all sessions."""
        return self._event_bus

    @property
    def active_turn_id(self) -> str | None:
        """Currently executing turn identifier, if any."""
        return self._turns.active_turn_id

    @property
    def turn_coordinator(self) -> SessionTurnCoordinator:
        """Serial turn coordinator for this session."""
        return self._turns

    @property
    def prompt_registry(self) -> SessionPromptRegistry:
        """Prompt and permission registry for this session."""
        return self._prompt_registry

    @property
    def persistence(self) -> SessionPersistenceCoordinator:
        """Transcript persistence coordinator for this session."""
        return self._persistence

    @property
    def agent_name(self) -> str | None:
        """Name of the agent last used in this session."""
        if self._last_turn_agent is not None:
            return self._last_turn_agent
        return self._agent_def.name if self._agent_def else self._agent_name_override

    async def build_snapshot(self) -> RuntimeSessionSnapshot:
        """Build the current transport snapshot for replay and reconnect."""
        return await self._event_bus.snapshot(
            self.session_id,
            active_turn_id=self.active_turn_id,
            turn_phase=self._prompt_registry.turn_phase(self.active_turn_id),
            pending_prompt=self._prompt_registry.pending_prompt,
            sync_status=self._sync_status_snapshot(),
        )

    def _sync_status_snapshot(self) -> RuntimeSessionSyncStatus:
        """Return the current platform-sync health for the session."""
        if self._get_api_context() is None:
            return RuntimeSessionSyncStatus(
                state="disabled",
                last_error=self._sync_last_error,
                last_attempt_at=self._sync_last_attempt_at,
            )
        if self._sync_last_error is not None:
            return RuntimeSessionSyncStatus(
                state="degraded",
                last_error=self._sync_last_error,
                last_attempt_at=self._sync_last_attempt_at,
            )
        return RuntimeSessionSyncStatus(
            state="ok",
            last_attempt_at=self._sync_last_attempt_at,
        )

    def mark_sync_ok(self) -> None:
        """Record a successful platform sync attempt."""
        self._sync_last_error = None
        self._sync_last_attempt_at = datetime.now(UTC)

    def mark_sync_degraded(self, exc: Exception) -> None:
        """Record a degraded platform sync state and publish a warning when possible."""
        detail = str(exc).strip() or type(exc).__name__
        previous_error = self._sync_last_error
        self._sync_last_error = detail
        self._sync_last_attempt_at = datetime.now(UTC)
        if detail != previous_error:
            self._publish_sync_warning(detail)

    def _publish_sync_warning(self, detail: str) -> None:
        """Best-effort publish of a sync warning onto the broker."""
        if self._event_loop is None or not self._event_loop.is_running():
            return

        coro = self._publish_broker_event(
            kind=runtime_events.EVENT_SESSION_WARNING,
            payload={
                "code": "platform_sync_degraded",
                "message": detail,
                "sync_status": self._sync_status_snapshot().model_dump(mode="json"),
            },
        )
        try:
            running_loop = asyncio.get_running_loop()
        except RuntimeError:
            running_loop = None

        if running_loop is self._event_loop:
            self._event_loop.create_task(coro)
            return

        future = asyncio.run_coroutine_threadsafe(coro, self._event_loop)

        def _report_warning_publish_failure(done: t.Any) -> None:
            try:
                done.result()
            except Exception:
                logger.opt(exception=True).debug(
                    "Failed to publish sync warning | session={}",
                    self.session_id,
                )

        future.add_done_callback(_report_warning_publish_failure)

    async def _publish_broker_event(
        self,
        *,
        kind: str,
        turn_id: str | None = None,
        payload: dict[str, t.Any] | None = None,
        terminal: bool = False,
    ) -> None:
        await self._event_bus.publish(
            kind=kind,
            session_id=self.session_id,
            turn_id=turn_id,
            payload=payload,
            terminal=terminal,
        )

    async def _publish_broker_raw_event(
        self,
        *,
        turn_id: str,
        raw_event: EventPayload,
    ) -> None:
        event_type = str(raw_event.get("type", "")).lower() or "unknown"
        kind = runtime_events.EVENT_TURN_EVENT
        if event_type in {"permissionrequired", "userinputrequired"}:
            kind = runtime_events.EVENT_PROMPT_REQUIRED
        elif event_type == "heartbeat":
            kind = runtime_events.EVENT_TRANSPORT_HEARTBEAT

        await self._publish_broker_event(
            kind=kind,
            turn_id=turn_id,
            payload={
                "event_type": event_type,
                "raw_event": raw_event,
            },
        )

    def _agent_def_for_turn(self, agent_name: str | None = None) -> AgentDef | None:
        """Resolve the agent definition that will handle a turn."""
        agent_def = self._agent_def
        if agent_name and self._registry is not None:
            _, _, agent_def = self._registry.resolve(agent_name=agent_name)
        return agent_def

    def refresh_registry(self, registry: capability_manager.CapabilityRegistry | None) -> None:
        """Rebind this session to the latest capability registry."""
        resolved_capability_name, resolved_capability, resolved_agent_def = (
            _resolve_session_binding(
                registry,
                capability_name=self._capability_name,
                agent_name=self.agent_name,
            )
        )

        self._registry = registry
        self._capability_name = resolved_capability_name
        self._capability = resolved_capability
        self._agent_def = resolved_agent_def
        self._agent = None

    def is_compatible(self) -> bool:
        """Check whether the session can be reused.

        Sessions are no longer scoped to a single capability — all
        capability tools are globally visible via the registry.
        """
        return True

    def _ensure_session_dir(self) -> Path:
        """Create and return the session directory."""
        if self._session_dir is None:
            self._session_dir = self._storage.session_path(self.session_id)
            self._session_dir.mkdir(parents=True, exist_ok=True)
        return self._session_dir

    def _resolve_capability_id(self) -> str | None:
        """Resolve a capability identifier for tool-write provenance."""
        capability = self._capability
        if capability is None:
            return None

        for attr in ("id", "artifact_id", "capability_id"):
            value = getattr(capability, attr, None)
            if value is None:
                continue
            text = str(value).strip()
            if text:
                return text
        return None

    def _project_memory_toolset(self) -> t.Any | None:
        """Build a session-scoped ProjectMemory toolset when sync is available."""
        if self._project_memory_scope_kind != _PROJECT_MEMORY_SCOPE_PROJECT:
            return None
        if not self.project_key:
            return None
        if self._get_api_context() is None:
            return None

        from dreadnode.tools.project_memory import ProjectMemory

        return ProjectMemory(
            session_id=self.session_id,
            project_key=self.project_key,
            scope_kind=self._project_memory_scope_kind,
            capability_id=self._resolve_capability_id(),
        )

    def _create_agent(
        self,
        *,
        model: str | None = None,
        agent_name: str | None = None,
        generate_params_extra: dict[str, t.Any] | None = None,
    ) -> Agent:
        """Create a fresh agent for this turn.

        Agents are ephemeral — created per-turn with current params.
        Trajectory lives on the session, not the agent.
        """
        self._ensure_session_dir()
        capability = self._capability
        agent_def = self._agent_def_for_turn(agent_name)
        if agent_name and self._registry is not None:
            _, capability, _ = self._registry.resolve(agent_name=agent_name)
        extra_tools = self._registry.all_tools() if self._registry else []
        capability_hooks = self._registry.all_hooks() if self._registry else []
        policy_hooks = self._policy.hooks
        extra_hooks = [*capability_hooks, *policy_hooks]

        model_config = model_resolution.resolve_turn_model_config(model, self.model, agent_def)
        effective_model = model_resolution.build_turn_generator(model_config)

        inherent_toolsets: list[t.Any] = []
        project_memory_toolset = self._project_memory_toolset()
        if project_memory_toolset is not None:
            inherent_toolsets.append(project_memory_toolset)

        agent = create_agent(
            effective_model,
            capability=capability,
            agent_def=agent_def,
            extra_tools=extra_tools,
            extra_hooks=extra_hooks,
            inherent_toolsets=inherent_toolsets,
            system_prompt_append=get_state().system_prompt_append,
            # Session-level engine (sticky) overrides the agent's declaration;
            # ``None`` falls through to agent_def.engine then native.
            engine=self._engine,
            background_context=self._project_memory_background_context,
        )

        self._wire_server_tools(agent)

        # Governance reconciliation (CAP-EGOV-*): refuse turns whose policy the
        # engine can't enforce, and warn on degraded/ignored facets. Native
        # enforces everything, so this is a no-op for the default engine.
        from dreadnode.agents.engines import AgentEngine
        from dreadnode.policies.reconciliation import (
            describe_component_gaps,
            describe_config_gaps,
            reconcile,
        )

        resolved_engine = agent._resolve_engine()
        if isinstance(resolved_engine, AgentEngine):
            reconciliation = reconcile(self._policy, resolved_engine)
            reconciliation.raise_if_refused()
            skill_count = len(self._registry.all_skills()) if self._registry else 0
            for warning in (
                *reconciliation.warnings,
                *describe_config_gaps(agent, resolved_engine),
                *describe_component_gaps(
                    resolved_engine,
                    tool_count=len(extra_tools or []),
                    skill_count=skill_count,
                ),
            ):
                logger.warning("engine '{}' reconciliation: {}", resolved_engine.name, warning)

        # Apply generate_params_extra (per-message overrides session default)
        effective_extra = generate_params_extra or self._generate_params_extra
        if effective_extra:
            agent.generate_params_extra = dict(effective_extra)

        return agent

    def get_agent(self, *, model: str | None = None) -> Agent:
        """Get or create agent (backward compat for restore paths).

        For chat turns, use _create_agent() which creates fresh agents.
        """
        if self._agent is None:
            self._agent = self._create_agent(model=model)
        return self._agent

    def set_policy(self, policy: SessionPolicy) -> None:
        """Swap the active policy. Hot-swap semantics apply.

        The ``_human_prompt_handler`` closure reads
        ``self._policy.is_autonomous`` at call time, so *new*
        ``ask_user()`` invocations after this call honor the new
        policy immediately. An *in-flight* ``ask_user()`` already
        awaiting a future is unaffected — by design, the user should
        finish answering the current prompt before autonomous
        behavior kicks in.

        Hooks from ``policy.hooks`` are attached at
        ``_create_agent`` time (turn start), so a mid-turn swap does
        not retroactively add continuation hooks to the running
        turn. They apply on the *next* turn. This is correct —
        urgent-prompt semantics need to swap immediately;
        continuation rules are between-turns concerns.
        """
        previous = getattr(self._policy, "name", "interactive")
        new_name = getattr(policy, "name", "interactive")
        self._policy = policy
        logger.info(
            "Session {} policy swap | {} -> {}",
            self.session_id[:8],
            previous,
            new_name,
        )

    def _wire_server_tools(self, agent: Agent) -> None:
        """Add tools that need server context to an already-created agent."""
        from dreadnode.agents.subagent import create_subagent_tool
        from dreadnode.tools.interaction import RuntimePermissionBridge

        agent.tools.append(create_subagent_tool(agent))

        # Foreign engines (e.g. claude-code) wire their tool-approval callback
        # into the runtime's per-turn human-prompt handler via this bridge, so
        # the existing prompt.required/respond HITL UX is preserved. The native
        # engine ignores it (it uses the ask_user tool directly).
        #
        # Policy-aware: only attach the bridge for non-autonomous (HITL) policies.
        # An autonomous policy auto-denies human prompts, so gating *every* tool
        # through it would deny all tool use — wrong for headless/eval. Leaving
        # the bridge off lets a foreign engine run tools freely, matching native
        # autonomous behavior where per-tool prompts don't fire.
        agent._permission_bridge = None if self._policy.is_autonomous else RuntimePermissionBridge()

        # Skills — pooled from all capabilities, or standalone capability
        all_skills: list = []
        if self._registry:
            all_skills = self._registry.all_skills()
        elif self._capability:
            from dreadnode.agents.skills import discover_skills

            for skills_path in getattr(self._capability, "skills_paths", None) or []:
                all_skills.extend(discover_skills(skills_path))

        if all_skills:
            from dreadnode.agents.skills import create_skill_tool

            agent.tools.append(create_skill_tool(all_skills))

            skills_reminder = (
                "\n\n## Skills\n\n"
                "Skills provide specialized instructions for specific tasks. "
                "Use the `skill` tool to load a skill when a task matches its description. "
                "If a skill is even plausibly relevant, load it before proceeding."
            )
            if agent.instructions:
                agent.instructions = agent.instructions + skills_reminder
            else:
                agent.instructions = skills_reminder.lstrip()

        # Trajectory search (requires storage)
        try:
            from dreadnode.tools.trajectory_search import TrajectorySearch

            storage = self._storage
            if storage is not None:
                agent.tools.append(TrajectorySearch(storage=storage, session_id=self.session_id))
        except Exception:
            logger.debug("TrajectorySearch not available", exc_info=True)

    @property
    def trajectory(self) -> t.Any:
        """Get session trajectory (owned by session, not agent)."""
        return self._trajectory

    @property
    def message_count(self) -> int:
        """Number of completed chat turns."""
        return self._message_count

    @property
    def is_busy(self) -> bool:
        """Whether the session has an active turn or compaction in progress."""
        task_running = self._turns.is_busy
        compacting = self._compaction_task is not None and not self._compaction_task.done()
        return task_running or compacting

    @staticmethod
    def _is_compaction_react(event: AgentEvent) -> bool:
        """Check if an event is a ReactStep whose Retry carries a compaction marker."""
        from dreadnode.agents.events import ReactStep
        from dreadnode.agents.reactions import Retry

        if not isinstance(event, ReactStep) or not isinstance(event.reaction, Retry):
            return False
        if not event.reaction.messages:
            return False
        return any(m.metadata.get("compaction") for m in event.reaction.messages)

    @staticmethod
    def _extract_compaction_trigger(event: AgentEvent) -> str:
        """Extract the compaction trigger from a ReactStep's Retry messages."""
        from dreadnode.agents.events import ReactStep
        from dreadnode.agents.reactions import Retry

        if (
            isinstance(event, ReactStep)
            and isinstance(event.reaction, Retry)
            and event.reaction.messages
        ):
            for m in event.reaction.messages:
                trigger = m.metadata.get("trigger")
                if m.metadata.get("compaction") and isinstance(trigger, str):
                    return trigger
        return "threshold"

    async def compact_session(
        self,
        *,
        trigger: str = "manual",
        guidance: str = "",
    ) -> dict[str, t.Any]:
        """Compact the session conversation history.

        Summarizes older messages while preserving a recent protected window.
        Uses the same model resolution as normal turns.

        Returns:
            Structured result with ``status`` (completed/skipped/failed),
            ``messages_before``, ``messages_after``, and optional ``reason``.
        """
        if self.is_busy:
            compacting = self._compaction_task is not None and not self._compaction_task.done()
            reason = "already_in_progress" if compacting else "turn_in_progress"
            return {"status": "skipped", "reason": reason}

        self._compaction_task = asyncio.create_task(
            self._do_compact(trigger=trigger, guidance=guidance)
        )
        try:
            return await self._compaction_task
        except asyncio.CancelledError:
            logger.info("Compaction cancelled for session {}", self.session_id)
            return {"status": "cancelled", "reason": "cancelled_by_user"}
        except Exception as exc:
            logger.exception("Compaction failed for session {}", self.session_id)
            return {"status": "failed", "reason": str(exc)}

    async def _do_compact(
        self,
        *,
        trigger: str,
        guidance: str,
    ) -> dict[str, t.Any]:
        """Internal compaction implementation."""
        from dreadnode.agents.hooks import find_summarization_boundary, summarize_conversation

        # Resolve model the same way turns do, including proxy setup (CMP-SUM-004)
        agent_def = self._agent_def_for_turn()
        model_config = model_resolution.resolve_turn_model_config(None, self.model, agent_def)
        if not model_config.canonical_model:
            return {"status": "failed", "reason": "no_model_configured"}

        # Build a configured generator for proxy models, same as _create_agent
        summarizer_model = model_resolution.build_turn_generator(model_config)

        messages = self._trajectory.messages
        messages_before = len(messages)

        # Pop system message if present
        work_messages = list(messages)
        if work_messages and work_messages[0].role == "system":
            work_messages.pop(0)

        if len(work_messages) <= 6:
            return {"status": "skipped", "reason": "insufficient_messages"}

        boundary = find_summarization_boundary(work_messages, min_messages_to_keep=6)
        if boundary == 0:
            return {"status": "skipped", "reason": "no_valid_boundary"}

        to_summarize = work_messages[:boundary]
        to_keep = work_messages[boundary:]

        # Check for prior compaction marker to incorporate (CMP-SUM-006)
        summarize_input = "\n".join(str(msg) for msg in to_summarize)
        prior_markers = [m for m in to_summarize if m.metadata and m.metadata.get("compaction")]
        if prior_markers:
            summarize_input = (
                "IMPORTANT: The conversation below contains a prior compaction summary. "
                "Incorporate, update, and extend it rather than regenerating context from scratch.\n\n"
                + summarize_input
            )

        summary = await summarize_conversation(
            summarizer_model,
            summarize_input,
            guidance=guidance,
        )

        # Build compaction marker message (CMP-PERS-001)
        from dreadnode.generators.message import make_compaction_message

        summary_message = make_compaction_message(
            summary.summary,
            messages_compacted=len(to_summarize),
            trigger=trigger,
        )

        # Non-destructive compaction: tell the API to mark old messages
        # and insert the summary, then rebuild in-memory for the live session.
        await asyncio.to_thread(self._compact_transcript_on_api, boundary, summary_message)

        # Rebuild trajectory preserving event types (avoid trajectory_from_openai_format)
        self._rebuild_compacted_trajectory(summary_message, to_keep)

        # After compaction, the in-memory trajectory has fewer messages.
        # The API already has the compacted state, so mark all current messages as persisted.
        self.persistence.persisted_message_count = len(self._trajectory.messages)

        messages_after = len(self._trajectory.messages)
        return {
            "status": "completed",
            "messages_before": messages_before,
            "messages_after": messages_after,
        }

    async def rewind_to(self, *, from_seq: int) -> dict[str, t.Any]:
        """Hard-truncate the session at a target user-message ``seq``.

        Calls the platform rewind endpoint, then re-fetches the truncated
        transcript and replaces the in-memory trajectory so the next chat
        turn won't replay the deleted messages as model context.

        Returns a dict with ``status`` (``completed`` | ``skipped`` |
        ``failed``), and on success ``deleted_count`` / ``target_seq`` /
        ``restored_content`` echoed straight from the platform response.

        Refuses when the session is busy (an in-flight turn would race
        with the truncate); the caller is expected to send ``/cancel``
        first and wait for the abort to settle. Refuses when the session
        isn't synced to a platform — there's no in-memory-only rewind
        primitive to fall back to (no marker, no shadow tree).
        """
        if self.is_busy:
            return {"status": "skipped", "reason": "turn_in_progress"}

        ctx = self._get_api_context()
        if ctx is None:
            return {"status": "failed", "reason": "no_platform_sync"}
        api, org, ws = ctx

        try:
            result = await asyncio.to_thread(
                api.rewind_transcript,
                org,
                ws,
                self.session_id,
                from_seq=from_seq,
            )
        except Exception as exc:
            logger.warning(
                "Rewind failed at platform | session={} from_seq={} error={}",
                self.session_id[:8],
                from_seq,
                exc,
            )
            return {"status": "failed", "reason": str(exc)}

        # Re-source the in-memory trajectory from the platform's truncated
        # transcript. ``restore_messages`` rebuilds via OpenAI-format
        # conversion, which loses event-type granularity (GenerationStep
        # vs ToolStep) — that's fine here: rewind is destructive, the
        # next turn re-derives event detail from the model's response.
        try:
            transcript = await asyncio.to_thread(
                api.get_transcript,
                org,
                ws,
                self.session_id,
            )
        except Exception:
            logger.opt(exception=True).warning(
                "Rewind succeeded on platform but transcript refetch failed | session={}",
                self.session_id[:8],
            )
            transcript = {"messages": []}

        rebuilt: list[SessionMessage] = []
        for raw in transcript.get("messages") or []:
            role = raw.get("role")
            content = raw.get("content") or ""
            if role in {"user", "assistant"} and isinstance(content, str):
                rebuilt.append(SessionMessage(role=role, content=content))

        self.restore_messages(rebuilt, persist=False)
        self.persistence.persisted_message_count = len(self._trajectory.messages)

        return {
            "status": "completed",
            "deleted_count": int(result.get("deleted_count") or 0),
            "target_seq": int(result.get("target_seq") or from_seq),
            "restored_content": str(result.get("restored_content") or ""),
        }

    def list_rewind_candidates(self) -> dict[str, t.Any]:
        """Return user-message rewind targets for the picker.

        Pulls non-compacted ``role='user'`` rows straight from the
        platform's transcript so the picker shows the same seqs the
        rewind endpoint accepts. Sessions without platform sync (offline
        runtime) return an empty list — there's no rewindable history
        to surface.
        """
        ctx = self._get_api_context()
        if ctx is None:
            return {"status": "unavailable", "reason": "no_platform_sync", "candidates": []}
        api, org, ws = ctx

        try:
            transcript = api.get_transcript(org, ws, self.session_id)
        except Exception as exc:
            logger.opt(exception=True).debug("Failed to load rewind candidates")
            return {"status": "failed", "reason": str(exc), "candidates": []}

        candidates: list[dict[str, t.Any]] = []
        for raw in transcript.get("messages") or []:
            if raw.get("role") != "user":
                continue
            if raw.get("compacted_at") is not None:
                continue
            content = raw.get("content")
            if not isinstance(content, str):
                continue
            candidates.append(
                {
                    "seq": int(raw.get("seq") or 0),
                    "content": content,
                    "created_at": raw.get("created_at"),
                }
            )
        return {"status": "ok", "candidates": candidates}

    def _compact_transcript_on_api(
        self,
        boundary: int,
        summary_message: t.Any,
    ) -> None:
        """Best-effort API compaction call. Marks old messages as compacted."""
        ctx = self._get_api_context()
        if ctx is None:
            return

        api, org, ws = ctx

        # The boundary index maps to the seq of the last message to compact.
        # Messages were assigned seqs 0..N by the API — the boundary-th message
        # (0-indexed) has seq = boundary - 1.
        up_to_seq = boundary - 1
        if up_to_seq < 0:
            return

        try:
            result = api.compact_transcript(
                org,
                ws,
                self.session_id,
                up_to_seq=up_to_seq,
                summary_message=summary_message,
            )
            # Update our tracked seq to include the new summary message
            summary_seq = result.get("summary_seq")
            if summary_seq is not None:
                self.persistence.last_persisted_seq = max(
                    self.persistence.last_persisted_seq,
                    summary_seq,
                )
        except Exception:
            logger.opt(exception=True).debug("Failed to compact transcript on API")

    def _rebuild_compacted_trajectory(
        self,
        summary_message: Message,
        kept_messages: list[Message],
    ) -> None:
        """Replace trajectory with compaction summary + events for kept messages.

        Uses UUID-based event mapping to preserve original event types
        (GenerationStep, ToolStep, etc.) rather than flattening to generic AgentSteps.
        """
        from dreadnode.agents.events import AgentStep, GenerationStep
        from dreadnode.agents.trajectory import Trajectory
        from dreadnode.generators.generator import Usage

        kept_msg_uuids = {m.uuid for m in kept_messages}

        # Find events that produced any kept message
        kept_events: list[AgentEvent] = [
            event
            for event in self._trajectory.events
            if isinstance(event, AgentStep)
            and hasattr(event, "messages")
            and any(m.uuid in kept_msg_uuids for m in event.messages)
        ]

        # Synthetic step for the compaction summary
        step_kwargs: dict[str, t.Any] = {
            "step": 0,
            "messages": [summary_message],
            "usage": Usage(input_tokens=0, output_tokens=0, total_tokens=0),
        }
        if self._trajectory.agent_id is not None:
            step_kwargs["agent_id"] = self._trajectory.agent_id
        compaction_step = GenerationStep(**step_kwargs)

        self._trajectory = Trajectory(
            session_id=self._trajectory.session_id,
            agent_id=self._trajectory.agent_id,
            system_prompt=self._trajectory.system_prompt,
            events=[compaction_step, *kept_events],
        )

    def _get_api_context(self) -> tuple[t.Any, str, str] | None:
        """Return (api_client, org, workspace) if platform sync is available."""
        try:
            from dreadnode import _get_default_instance

            instance = _get_default_instance()
            if not instance.can_sync:
                return None
            api = instance.api
            org = instance.organization
            ws = instance.workspace
            if not isinstance(org, str) or not isinstance(ws, str):
                return None
        except Exception:
            return None
        else:
            return api, org, ws

    def _load_project_memory_background_context(self) -> str:
        """Fetch and render project memory preload context for this session."""
        if self._project_memory_scope_kind != _PROJECT_MEMORY_SCOPE_PROJECT:
            return ""
        if not self.project_key:
            return ""

        ctx = self._get_api_context()
        if ctx is None:
            return ""
        api, org, workspace = ctx

        try:
            payload = api.list_project_memory_preload(
                org,
                workspace,
                self.project_key,
                scope_kind=self._project_memory_scope_kind,
                limit=self._project_memory_preload_limit,
            )
        except Exception:
            logger.debug(
                "Project memory preload fetch failed | session={}",
                self.session_id[:8],
                exc_info=True,
            )
            return ""

        raw_memories = payload.get("memories") if isinstance(payload, dict) else None
        memories = raw_memories if isinstance(raw_memories, list) else []
        preload_xml = render_project_memory_preload_xml(memories)
        if not preload_xml:
            return ""
        return get_project_memory_background_context(preload_xml)

    def _persist_state(self, *, update_messages: bool = True) -> None:
        """Persist session state to the platform API."""
        self.persistence.persist_state(update_messages=update_messages)

    async def _persist_state_locked(self, *, update_messages: bool = True) -> None:
        """Async wrapper around ``_persist_state`` with per-session locking."""
        await self.persistence.persist_state_locked(update_messages=update_messages)

    def restore_messages(
        self,
        messages: list[SessionMessage],
        *,
        model: str | None = None,
        persist: bool = True,
    ) -> None:
        """Seed the session agent trajectory from a simple message list.

        An empty ``messages`` list resets the trajectory to a fresh empty
        state — the rewind-to-seq-0 path relies on this to clear the
        in-memory transcript after the platform truncates everything
        (`ENG-6776`). Other callers guard against empty input upstream.
        """
        from dreadnode.agents.trajectory import trajectory_from_openai_format

        if model is not None:
            self.model = model
        trajectory = trajectory_from_openai_format(
            [
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in messages
            ]
        )
        with suppress(ValueError):
            trajectory.session_id = UUID(self.session_id)
        self._trajectory = trajectory
        self._agent = None  # Clear so next turn creates fresh
        if persist:
            self._persist_state()

    def restore_trajectory(
        self,
        trajectory_data: dict[str, t.Any],
        *,
        model: str | None = None,
        persist: bool = True,
    ) -> None:
        """Restore the session agent from a serialized trajectory."""
        from dreadnode.agents.trajectory import Trajectory as TrajectoryModel

        if model is not None:
            self.model = model
        trajectory = TrajectoryModel.from_dict(trajectory_data)
        with suppress(ValueError):
            trajectory.session_id = UUID(self.session_id)
        self._trajectory = trajectory
        self._agent = None
        if persist:
            self._persist_state()

    def resolve_permission(self, request_id: str, decision: str) -> None:
        """Resolve a pending permission request with a user decision."""
        self._prompt_registry.resolve_permission(request_id, decision)

    def register_human_prompt(self, prompt: HumanPrompt) -> asyncio.Future[HumanInputResponse]:
        """Register a pending human prompt and return its response future."""
        return self._prompt_registry.register_human_prompt(prompt)

    def resolve_human_input_response(self, response: HumanInputResponse) -> bool:
        """Resolve a pending human prompt response. Returns True if applied."""
        return self._prompt_registry.resolve_human_input_response(response)

    def resolve_human_response(self, response: HumanInputResponse) -> bool:
        """Resolve a human response against prompts or permissions."""
        return self._prompt_registry.resolve_human_response(response)

    def close(self) -> None:
        """Stop any background processing associated with this session."""
        self._turns.close()
        self.persistence.close()
        self._event_bus.drop_session(self.session_id)

    async def cancel(self) -> bool:
        """Cancel the active turn or compaction.

        If messages were queued while the turn was running, a new
        processing task is started so they are handled normally rather
        than being silently discarded.

        Returns True if a running turn/compaction was cancelled, False if already idle.
        """
        cancel_started_at = time.perf_counter()
        # Capture the active turn_id before cancel_active() clears it so
        # both the requested and complete markers share the same turn.
        cancelled_turn_id = self._turns.active_turn_id
        _log_chat_timing(self.session_id, cancelled_turn_id, "cancel_requested", cancel_started_at)
        was_busy = await self._turns.cancel_active()

        if self._compaction_task is not None and not self._compaction_task.done():
            self._compaction_task.cancel()
            was_busy = True
            with suppress(asyncio.CancelledError):
                await self._compaction_task

        # If new messages arrived while we were cancelling, start a fresh
        # processor so they are handled.  Previously we drained the queue
        # here, which silently dropped messages the user sent after Esc.
        await self._turns.ensure_processing(processor_factory=self._process_queue)
        _log_chat_timing(self.session_id, cancelled_turn_id, "cancel_complete", cancel_started_at)

        return was_busy

    async def enqueue_chat(
        self,
        message: str,
        *,
        model: str | None = None,
        agent: str | None = None,
        reset: bool = False,
        generate_params_extra: dict[str, t.Any] | None = None,
    ) -> tuple[str, asyncio.Queue[EventPayload | None]]:
        """Queue a chat turn and ensure the session processor is running.

        Returns ``(turn_id, queue)`` so callers (e.g. the websocket
        ``turn.start`` handler) can echo the assigned turn_id back to the
        client, which uses it to scope subsequent event-stream reads and
        reject stragglers from a prior cancelled turn.
        """
        request = QueuedTurnRequest(
            message=message,
            model=model,
            agent=agent,
            reset=reset,
            generate_params_extra=generate_params_extra,
        )
        _, queue_depth = await self._turns.enqueue(
            request,
            processor_factory=self._process_queue,
        )
        if self._turns.is_busy and queue_depth > 1:
            logger.debug(
                "Session {} turn={}: queued message (task still running, queue={})",
                self.session_id[:8],
                _short_turn(request.turn_id),
                queue_depth,
            )

        await self._publish_broker_event(
            kind=runtime_events.EVENT_TURN_ACCEPTED,
            turn_id=request.turn_id,
            payload={
                "agent": agent,
                "model": model,
                "reset": reset,
                "message_length": len(message),
                "queue_depth": queue_depth,
            },
        )

        return request.turn_id, request.stream.queue

    async def _process_queue(self) -> None:
        """Process queued chat turns sequentially for this session."""
        while True:
            context = await self._turns.dequeue_next()
            if context is None:
                return
            request = context.request

            logger.debug(
                "Session {} turn={}: processing chat (message={}...)",
                self.session_id[:8],
                _short_turn(request.turn_id),
                request.message[:40],
            )
            _log_chat_timing(
                self.session_id, request.turn_id, "processor_start", request.queued_at_monotonic
            )

            turn_status = "failed"
            emitted_event_count = 0
            # Anchor for terminal-envelope synthesis (CAP-WEVT-007..009): the
            # slice of trajectory events and the wall-clock duration belong to
            # this turn alone.
            turn_started_monotonic = time.perf_counter()
            trajectory_start_idx = len(self._trajectory.events)

            def _turn_slice() -> list[t.Any]:
                # B023: closures over the per-turn anchors are intentional —
                # same lifetime as ``_emit_turn_event`` below.
                return self._trajectory.events[trajectory_start_idx:]  # noqa: B023

            def _turn_duration_ms() -> int:
                return round((time.perf_counter() - turn_started_monotonic) * 1000)  # noqa: B023

            async def _emit_turn_event(event: EventPayload) -> None:
                nonlocal emitted_event_count
                emitted_event_count += 1
                # B023: closure over the per-turn `request` is intentional —
                # this helper is constructed and consumed within a single turn.
                await request.stream.publish(event)  # noqa: B023

            try:
                if request.model and request.model != self.model:
                    self.model = request.model

                # Fresh agent per turn — reads current params
                model_config = model_resolution.resolve_turn_model_config(
                    request.model,
                    self.model,
                    self._agent_def_for_turn(request.agent),
                )
                # Remember the canonical model actually used this turn so
                # subsequent transcript-flush snapshots (which read
                # ``self.model``) carry it in ``context.model`` instead of
                # empty string. Without this, non-interactive callers that
                # never pass ``model`` — capability workers relying on the
                # agent frontmatter default — persist an empty model and
                # the UI shows "Unknown model".
                if self.model != model_config.canonical_model:
                    self.model = model_config.canonical_model
                _log_chat_timing(
                    self.session_id,
                    request.turn_id,
                    "model_config_resolved",
                    request.queued_at_monotonic,
                )

                # Mark the turn started BEFORE running validation so the
                # broker lifecycle ``accepted → started → (completed|
                # failed|cancelled)`` stays consistent. Previously a
                # validation_error went straight from ``accepted`` to
                # ``failed`` with no ``started`` in between, breaking
                # the invariant clients rely on.
                self._turns.mark_started(
                    context,
                    agent_name=request.agent or self.agent_name,
                    model=model_config.canonical_model,
                )
                await self._publish_broker_event(
                    kind=runtime_events.EVENT_TURN_STARTED,
                    turn_id=request.turn_id,
                    payload={
                        "agent": request.agent or self.agent_name,
                        "model": model_config.canonical_model,
                    },
                )

                validation_error = model_resolution.validate_model_environment(model_config)
                if validation_error:
                    error_event: EventPayload = {
                        "type": "generationerror",
                        "data": {
                            "error": validation_error,
                            "error_type": "AuthenticationError",
                        },
                    }
                    await _emit_turn_event(error_event)
                    await self._publish_broker_raw_event(
                        turn_id=request.turn_id,
                        raw_event=error_event,
                    )
                    await self._publish_broker_event(
                        kind=runtime_events.EVENT_TURN_FAILED,
                        turn_id=request.turn_id,
                        payload={
                            "turn_id": request.turn_id,
                            "error": {
                                "type": "AuthenticationError",
                                "message": validation_error,
                            },
                            "partial_response": None,
                            "tool_calls_attempted": [],
                            "duration_ms": _turn_duration_ms(),
                        },
                        terminal=True,
                    )
                    turn_status = "failed"
                    continue

                agent = self._create_agent(
                    model=request.model,
                    agent_name=request.agent,
                    generate_params_extra=request.generate_params_extra,
                )
                _log_chat_timing(
                    self.session_id, request.turn_id, "agent_created", request.queued_at_monotonic
                )

                from dreadnode.app.api.models import HumanInputResponse
                from dreadnode.tools.interaction import (
                    reset_human_prompt_handler,
                    set_human_prompt_handler,
                )

                _log_chat_timing(
                    self.session_id,
                    request.turn_id,
                    "interaction_handlers_ready",
                    request.queued_at_monotonic,
                )

                async def _human_prompt_handler(
                    prompt: HumanPrompt,
                ) -> HumanInputResponse:
                    # The handler is registered per-turn (token / reset
                    # below). Closure references are deliberate — they
                    # carry the turn-id and emit callbacks to the
                    # ``ask_user()`` tool site without it needing a
                    # reference to the session.
                    if self._policy.is_autonomous:
                        # No human is in the loop. Resolve instantly with
                        # ``cancel`` so the agent's ``ask_user()`` raises
                        # ``UserCancelled`` without touching any transport.
                        # The mode-aware reason is a follow-up — see the
                        # ``HumanInputResponder`` plan in
                        # docs/later/SESSION_POLICY_REFACTOR.md.
                        return HumanInputResponse(
                            request_id=prompt.request_id,
                            action="cancel",
                        )
                    future = self.register_human_prompt(prompt)
                    event: EventPayload = {
                        "type": "userinputrequired",
                        "data": prompt.model_dump(),
                    }
                    await _emit_turn_event(event)
                    await self._publish_broker_raw_event(
                        turn_id=request.turn_id,  # noqa: B023
                        raw_event=event,
                    )
                    return await future

                token = set_human_prompt_handler(_human_prompt_handler)
                turn_was_compacted = False
                self.persistence.begin_turn()
                # Local import to match the existing lazy-import style in
                # this module and avoid eager event-module import at startup.
                from dreadnode.agents.events import GenerationStep

                try:
                    with bind_session_id(self.session_id):
                        # Session owns the trajectory — agent operates on it directly
                        async with agent.stream(
                            request.message,
                            reset=request.reset,
                            trajectory=self._trajectory,
                        ) as stream:
                            _log_chat_timing(
                                self.session_id,
                                request.turn_id,
                                "agent_stream_opened",
                                request.queued_at_monotonic,
                            )
                            async for event in stream:
                                event_dict = event.as_dict()
                                # Detect auto-compaction: a ReactStep whose Retry
                                # carries a message with compaction metadata.
                                if not turn_was_compacted and self._is_compaction_react(event):
                                    turn_was_compacted = True
                                    from dreadnode.agents.events import CompactionEvent

                                    trigger = self._extract_compaction_trigger(event)
                                    # Extract message counts from the compaction marker
                                    messages_compacted = 0
                                    messages_after = 0
                                    if hasattr(event, "reaction") and hasattr(
                                        event.reaction, "messages"
                                    ):
                                        messages_after = len(event.reaction.messages)
                                        for m in event.reaction.messages:
                                            mc = (m.metadata or {}).get("messages_compacted", 0)
                                            if mc:
                                                messages_compacted = mc
                                                break
                                    ce = CompactionEvent(
                                        trigger=trigger,
                                        compaction_status="completed",
                                        messages_before=messages_compacted + messages_after,
                                        messages_after=messages_after,
                                    )
                                    await _emit_turn_event(ce.as_dict())
                                    await self._publish_broker_raw_event(
                                        turn_id=request.turn_id,
                                        raw_event=ce.as_dict(),
                                    )
                                await _emit_turn_event(t.cast("EventPayload", event_dict))
                                await self._publish_broker_raw_event(
                                    turn_id=request.turn_id,
                                    raw_event=t.cast("EventPayload", event_dict),
                                )

                                # Mid-turn flush: GenerationStep is the
                                # react-cycle boundary. trajectory.messages
                                # is only consistent at this point (tool
                                # results buffer into the following
                                # GenerationStep — see
                                # Trajectory.messages). Fire-and-forget
                                # under _persist_lock so event delivery is
                                # not blocked on persistence I/O. The
                                # end-of-turn flush remains as the safety
                                # net for paths that don't terminate on a
                                # GenerationStep (errors, AgentEnd-only
                                # flows).
                                if isinstance(event, GenerationStep):
                                    flush_task = asyncio.create_task(self._persist_state_locked())
                                    self.persistence.track_flush_task(flush_task)
                finally:
                    reset_human_prompt_handler(token)

                self._last_turn_agent = request.agent
                self._message_count += 1

                # Clear cached agent so restore paths create fresh
                self._agent = None
                # Drain any in-flight mid-turn flushes before the final
                # safety flush, so the lock contention path is predictable
                # and the final call sees a quiescent _persisted_message_count.
                await self.persistence.drain_pending_flushes()
                await self._persist_state_locked()
                turn_events = _turn_slice()
                response_text = _final_assistant_message(self._trajectory)
                await self._publish_broker_event(
                    kind=runtime_events.EVENT_TURN_COMPLETED,
                    turn_id=request.turn_id,
                    payload={
                        "turn_id": request.turn_id,
                        "response_text": response_text,
                        "generation_stop_reason": _turn_generation_stop_reason(
                            turn_events, produced_output=bool(response_text.strip())
                        ),
                        "tool_calls": _turn_tool_calls_completed(turn_events),
                        "usage": _turn_usage(turn_events),
                        "duration_ms": _turn_duration_ms(),
                        "agent": self.agent_name,
                        "message_count": self._message_count,
                    },
                    terminal=True,
                )
                turn_status = "completed"
            except asyncio.CancelledError:
                logger.info(
                    "Session {} turn={}: cancelled by user",
                    self.session_id[:8],
                    _short_turn(request.turn_id),
                )
                self._agent = None

                # Clear any pending human prompts / permissions that were
                # active at cancel time. Without this, ``pending_prompt``
                # survives into the next ``build_snapshot`` and reconnect
                # shows an idle session as ``awaiting_input``, wedging the
                # loop-state recovery path on the TUI side.
                cleared = self._prompt_registry.cancel_all_pending()
                if cleared:
                    logger.info(
                        "Session {} turn={}: cancel cleared {} pending prompt(s)",
                        self.session_id[:8],
                        _short_turn(request.turn_id),
                        cleared,
                    )

                # Cancel-path persist now prefers correctness over the
                # previous detach-on-timeout behavior. We still log when
                # the platform is slow, but we wait for the final flush
                # so cancelled turns do not silently disappear from the
                # persisted transcript.
                try:
                    detached_count = await self.persistence.cancel_path_flush(
                        slow_warning_after_s=2.0
                    )
                except Exception:
                    logger.opt(exception=True).debug("cancel-path persist raised")
                    detached_count = 0

                if detached_count:
                    logger.warning(
                        "Session {} turn={}: cancel-path persist detached {} in-flight task(s)",
                        self.session_id[:8],
                        _short_turn(request.turn_id),
                        detached_count,
                    )

                cancelled_event: EventPayload = {
                    "type": "cancelled",
                    "data": {"reason": "user_interrupt"},
                }
                await _emit_turn_event(cancelled_event)
                await self._publish_broker_event(
                    kind=runtime_events.EVENT_TURN_CANCELLED,
                    turn_id=request.turn_id,
                    payload={
                        "turn_id": request.turn_id,
                        "reason": "user_interrupt",
                        "partial_response": _final_assistant_in_events(_turn_slice()),
                        "duration_ms": _turn_duration_ms(),
                        "raw_event": cancelled_event,
                    },
                    terminal=True,
                )
                turn_status = "cancelled"
                # Exit so cancel() can drain remaining queued requests.
                # The finally block still runs, sending the None sentinel.
                return
            except Exception as exc:
                logger.exception(
                    "Error during chat | session={} turn={}",
                    self.session_id[:8],
                    _short_turn(request.turn_id),
                )

                # Failed turns must still flush the transcript. Mirror the
                # success and cancel paths: drain the in-flight mid-turn
                # flushes, then run a final persist so the user message and
                # any partial assistant/tool steps reach the platform.
                # Without this the fire-and-forget flush tasks are left
                # in-flight and get cancelled when the session tears down
                # (close() -> persistence.close()), so a failed run shows an
                # empty transcript even though its tool calls were recorded.
                # Guarded so a persistence failure never masks the agent error.
                try:
                    await self.persistence.drain_pending_flushes()
                    await self._persist_state_locked()
                except Exception:
                    logger.opt(exception=True).debug("error-path persist raised")

                error_event: EventPayload = {"type": "error", "error": str(exc)}
                await _emit_turn_event(error_event)
                await self._publish_broker_raw_event(
                    turn_id=request.turn_id,
                    raw_event=error_event,
                )
                turn_events = _turn_slice()
                await self._publish_broker_event(
                    kind=runtime_events.EVENT_TURN_FAILED,
                    turn_id=request.turn_id,
                    payload={
                        "turn_id": request.turn_id,
                        "error": {
                            "type": type(exc).__name__,
                            "message": str(exc),
                        },
                        "partial_response": _final_assistant_in_events(turn_events),
                        "tool_calls_attempted": _turn_tool_calls_attempted(turn_events),
                        "duration_ms": _turn_duration_ms(),
                    },
                    terminal=True,
                )
            finally:
                self._turns.finish_turn(context, status=turn_status)
                logger.debug(
                    "Session {} turn={}: chat turn complete status={} emitted_events={}",
                    self.session_id[:8],
                    _short_turn(request.turn_id),
                    turn_status,
                    emitted_event_count,
                )
                _log_chat_timing(
                    self.session_id,
                    request.turn_id,
                    "processor_complete",
                    request.queued_at_monotonic,
                )
                # Always send None sentinel so queue consumers can close.
                # Previously this was skipped on cancel, leaving the
                # interactive turn consumer hanging forever.
                await request.stream.close()

    def _first_user_preview(self, max_len: int = 200) -> str | None:
        """Extract preview text from the first user message in the trajectory."""
        for msg in self._trajectory.messages:
            if getattr(msg, "role", None) == "user":
                content = getattr(msg, "content", "")
                if isinstance(content, str):
                    text = content.strip().replace("\n", " ")
                    if len(text) > max_len:
                        return text[: max_len - 1] + "\u2026"
                    return text or None
        return None

    def _trajectory_usage_rollup(self) -> tuple[int, int, float | None, int | None]:
        """Aggregate cumulative usage across the in-memory trajectory.

        Mirrors the platform's ``SessionUsageResponse`` shape so the TUI can
        seed footer state on session open without a separate fetch. Returns
        ``(total_tokens, total_tool_call_count, total_cost_usd,
        last_generation_input_tokens)``; cost is ``None`` when any
        ``GenerationStep`` reported output tokens but no rate — partial sums
        are misleading, so we honestly report unknown. The last-generation
        input token count is the size of the prompt the model most recently
        saw — the correct denominator for a context-window gauge — and is
        ``None`` when no generation has run yet.
        """
        from dreadnode.agents.events import GenerationStep

        total_tokens = 0
        tool_calls = 0
        cost = 0.0
        cost_unknown = False
        last_input_tokens: int | None = None
        for step in self._trajectory.steps:
            if not isinstance(step, GenerationStep):
                continue
            usage = step.usage
            total_tokens += usage.total_tokens or 0
            if usage.input_tokens:
                last_input_tokens = usage.input_tokens
            for assistant in (m for m in step.messages if str(m.role) == "assistant"):
                tool_calls += len(getattr(assistant, "tool_calls", None) or [])
            step_cost = step.estimated_cost
            if step_cost is not None:
                cost += step_cost
            elif (usage.output_tokens or 0) > 0:
                cost_unknown = True
        return total_tokens, tool_calls, None if cost_unknown else cost, last_input_tokens

    def to_info(self) -> SessionInfo:
        """Convert to SessionInfo for API responses."""
        policy_name = getattr(self._policy, "name", "interactive")
        policy_is_autonomous = bool(getattr(self._policy, "is_autonomous", False))
        policy_display_label = str(getattr(self._policy, "display_label", "") or "")
        total_tokens, tool_calls, cost, last_input_tokens = self._trajectory_usage_rollup()
        return SessionInfo(
            session_id=self.session_id,
            project=self.project_key,
            group_id=self._group_id,
            created_at=self.created_at,
            updated_at=datetime.now(UTC),
            message_count=self.message_count,
            session_dir=str(self._session_dir) if self._session_dir else None,
            capability=self.capability_name,
            agent=self.agent_name,
            model=self.model or None,
            title=self.title,
            preview=self._first_user_preview(),
            policy_name=policy_name,
            policy_is_autonomous=policy_is_autonomous,
            policy_display_label=policy_display_label,
            total_tokens=total_tokens,
            total_tool_call_count=tool_calls,
            total_cost_usd=cost,
            last_generation_input_tokens=last_input_tokens,
        )


# =============================================================================
# Routes
# =============================================================================


@app.get("/api/sessions", response_model=list[SessionInfo])
async def list_sessions(include_platform: bool = False) -> list[SessionInfo]:
    """List active agent sessions.

    Defaults to the in-process set; pass ``include_platform=true`` to
    merge platform-persisted sessions for this runtime (slower). The
    table view should call ``GET /api/sessions/browse`` instead — it
    returns a paginated envelope and skips the runtime-id self-filter.
    """
    return get_state().list_session_infos(include_platform=include_platform)


@app.get("/api/sessions/browse")
async def browse_sessions(
    page: int = 1,
    limit: int = 20,
    sort_by: str = "updated_at",
    sort_dir: str = "desc",
    archived: str = "active",
    label: t.Annotated[list[str] | None, Query()] = None,
    user_id: str | None = None,
    project_id: t.Annotated[list[str] | None, Query()] = None,
    origin: t.Annotated[list[str] | None, Query()] = None,
    search: str | None = None,
    include_workload_sessions: bool = False,
) -> JSONResponse:
    """Paginated platform-sourced session list (the table-view path).

    Forwards every query param to the platform's ``GET /sessions`` and
    returns the paginated envelope with sessions normalized to the
    runtime's ``SessionInfo`` wire shape. In-process sessions are not
    merged here — the table view trusts ``_register_session_with_platform``
    to sync within a turn. Boot/swap callers should keep using
    ``GET /api/sessions`` for the live in-process set.

    ``include_workload_sessions`` defaults to ``False`` per SES-LST-009;
    pass ``true`` to include eval (and future optimization / training /
    world) runs in the table view.
    """
    envelope = await get_state().browse_platform_sessions(
        page=page,
        limit=limit,
        sort_by=sort_by,
        sort_dir=sort_dir,
        archived=archived,
        label=label,
        user_id=user_id,
        project_id=project_id,
        origin=origin,
        search=search,
        include_workload_sessions=include_workload_sessions,
    )
    return JSONResponse(content=envelope)


@app.get("/api/sessions/facets")
async def browse_session_facets(
    archived: str = "active",
    label: t.Annotated[list[str] | None, Query()] = None,
    user_id: str | None = None,
    project_id: t.Annotated[list[str] | None, Query()] = None,
    origin: t.Annotated[list[str] | None, Query()] = None,
    search: str | None = None,
    include_workload_sessions: bool = False,
) -> JSONResponse:
    """Per-key value counts for sessions the caller can see (SES-LBL-060).

    Parallels ``GET /api/sessions/browse`` — takes the same filter set
    (minus pagination / sort) and returns
    ``{"labels": {key: [{"value": ..., "count": ...}, ...]}}``. The table
    view calls this to populate its left facets sidebar. Honors the same
    ``include_workload_sessions`` default as the browse endpoint so the
    list and its facets agree on what's counted.
    """
    envelope = await get_state().browse_platform_facets(
        archived=archived,
        label=label,
        user_id=user_id,
        project_id=project_id,
        origin=origin,
        search=search,
        include_workload_sessions=include_workload_sessions,
    )
    return JSONResponse(content=envelope)


@app.post("/api/session-groups", response_model=SessionGroupInfo)
async def create_session_group(request: SessionGroupCreateRequest) -> SessionGroupInfo:
    """Create a platform-backed session group for workflow contexts."""
    try:
        group = _create_session_group_on_platform(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Session groups require a connected platform workspace",
        )
    return SessionGroupInfo(
        id=str(group["id"]),
        kind=str(group.get("kind", request.kind)),
        title=str(group["title"]) if group.get("title") is not None else None,
        status=str(group["status"]) if group.get("status") is not None else None,
    )


@app.patch("/api/session-groups/{group_id}", response_model=SessionGroupInfo)
async def update_session_group(
    group_id: str,
    request: SessionGroupUpdateRequest,
) -> SessionGroupInfo:
    """Update lifecycle fields for a platform-backed session group."""
    group = _update_session_group_on_platform(group_id, request)
    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Session groups require a connected platform workspace",
        )
    return SessionGroupInfo(
        id=str(group["id"]),
        kind=str(group.get("kind", "")),
        title=str(group["title"]) if group.get("title") is not None else None,
        status=str(group["status"]) if group.get("status") is not None else None,
    )


@app.post("/api/sessions", response_model=SessionInfo)
async def create_session(request: SessionCreateRequest) -> SessionInfo:
    """Create or resolve a capability-bound session runtime."""
    try:
        session = get_state().create_session(
            session_id=request.session_id,
            model=request.model,
            project=request.project,
            capability=request.capability,
            agent=request.agent,
            messages=request.messages,
            policy=request.policy,
            labels=request.labels,
            origin=request.origin,
            group_id=request.group_id,
            engine=request.engine,
            project_memory_scope_kind=request.project_memory_scope_kind,
            enable_project_memory_preload=request.enable_project_memory_preload,
            project_memory_preload_limit=request.project_memory_preload_limit,
        )
    except ValueError as exc:
        # Session-id collision with different agent, unknown capability,
        # missing model, unknown policy name, engine/policy mismatch —
        # all 409 conflicts.
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return session.to_info()


@app.get("/api/sessions/status")
async def list_session_statuses() -> JSONResponse:
    """Return runtime-owned live state for currently loaded sessions."""
    sessions: dict[str, dict[str, t.Any]] = {}
    for session in get_state().list_sessions():
        active_turn_id = session.active_turn_id
        sessions[session.session_id] = {
            "session_id": session.session_id,
            "active_turn_id": active_turn_id,
            "is_busy": session.is_busy,
            "queue_depth": session.turn_coordinator.queue_depth,
            "turn_phase": session.prompt_registry.turn_phase(active_turn_id),
            "pending_prompt": session.prompt_registry.pending_prompt is not None,
        }
    return JSONResponse(content={"sessions": sessions})


@app.post("/api/sessions/{session_id}/restore", response_model=SessionRestoreResponse)
async def restore_session(
    session_id: str,
    request: SessionRestoreRequest,
) -> SessionRestoreResponse:
    """Restore a bound session runtime from saved messages or trajectory data."""
    try:
        session = get_state().create_session(
            session_id=session_id,
            model=request.model,
            project=request.project,
            capability=request.capability,
            agent=request.agent,
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    try:
        _apply_session_restore_request(session, request)
    except SessionRestoreError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    step_count = len(session.trajectory.steps) if session.trajectory is not None else 0
    return SessionRestoreResponse(
        session_id=session.session_id,
        message_count=session.message_count,
        step_count=step_count,
        capability=session.capability_name,
        agent=session.agent_name,
        project=session.project_key,
    )


@app.get("/api/sessions/{session_id}", response_model=SessionInfo)
async def get_session(session_id: str) -> SessionInfo:
    """Get information about a specific session."""
    session = get_state().get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")
    return session.to_info()


@app.get("/api/sessions/{session_id}/messages")
async def get_session_messages(session_id: str) -> JSONResponse:
    """Return the conversation messages for a session."""
    session = get_state().get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")
    messages = session._trajectory.messages if session._trajectory is not None else []

    # Build tool_call_id → tool call metadata from assistant messages.
    # Tool result messages only carry the id; the TUI needs the original
    # arguments on transcript rebuild to render compact labels like
    # ``report(Findings)`` and to recover report content passed via args.
    tool_call_names: dict[str, str] = {}
    tool_call_args: dict[str, t.Any] = {}
    for msg in messages:
        if msg.role == "assistant" and msg.tool_calls:
            for tc in msg.tool_calls:
                tool_call_names[tc.id] = tc.function.name
                tool_call_args[tc.id] = _parse_tool_arguments(tc.function.arguments)

    return JSONResponse(
        content=[
            {
                "role": msg.role,
                "content": msg.content or "",
                "metadata": msg.metadata or None,
                "tool_call_id": msg.tool_call_id,
                "tool_name": tool_call_names.get(msg.tool_call_id or ""),
                "tool_args": tool_call_args.get(msg.tool_call_id or ""),
            }
            for msg in messages
        ]
    )


@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str) -> JSONResponse:
    """Delete an agent session."""
    if not get_state().delete_session(session_id):
        raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")
    return JSONResponse(content={"status": "deleted", "session_id": session_id})


@app.post("/api/sessions/{session_id}/archive")
async def archive_session(session_id: str) -> JSONResponse:
    """Archive an agent session on the platform (idempotent).

    404s when no platform context is available — purely-local sessions
    can't be archived because the lifecycle field lives on the platform.
    """
    if not get_state().archive_session(session_id, archived=True):
        raise HTTPException(
            status_code=404,
            detail="Session archive requires a connected platform workspace",
        )
    return JSONResponse(content={"status": "archived", "session_id": session_id})


@app.post("/api/sessions/{session_id}/unarchive")
async def unarchive_session(session_id: str) -> JSONResponse:
    """Unarchive a previously archived session (idempotent)."""
    if not get_state().archive_session(session_id, archived=False):
        raise HTTPException(
            status_code=404,
            detail="Session unarchive requires a connected platform workspace",
        )
    return JSONResponse(content={"status": "unarchived", "session_id": session_id})


@app.post("/api/sessions/{session_id}/freeze")
async def freeze_session(session_id: str) -> JSONResponse:
    """Freeze a session on the platform (terminal, idempotent).

    Frozen sessions can still be loaded for read but reject any new turns.
    """
    if not get_state().freeze_session(session_id):
        raise HTTPException(
            status_code=404,
            detail="Session freeze requires a connected platform workspace",
        )
    return JSONResponse(content={"status": "frozen", "session_id": session_id})


def _reject_reserved_kind(kind: str) -> None:
    if runtime_events.is_reserved_kind(kind):
        raise HTTPException(
            status_code=400,
            detail=(
                f"Event kind '{kind}' uses a runtime-reserved namespace "
                f"(one of: {', '.join(runtime_events.RESERVED_KIND_PREFIXES)})"
            ),
        )


@app.post("/api/sessions/{session_id}/events")
async def publish_session_event(
    session_id: str, request: SessionEventPublishRequest
) -> dict[str, t.Any]:
    """Inject a session-scoped event into the runtime event bus (CAP-WCLI-013).

    The event is visible to all bus subscribers (other workers, the TUI,
    external clients). Runtime-reserved namespaces (e.g. ``turn.*``,
    ``prompt.*``, ``session.*``, ``transport.*``, ``capabilities.*``) are
    rejected so external callers can't forge lifecycle events.
    """
    _reject_reserved_kind(request.kind)
    state = get_state()
    if not state.has_session(session_id):
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
    envelope = await state.event_bus.publish(
        kind=request.kind,
        session_id=session_id,
        payload=request.payload,
    )
    if envelope is None:
        raise HTTPException(status_code=410, detail="Session has been dropped")
    return {"event_id": envelope.event_id, "seq": envelope.seq}


@app.post("/api/events")
async def publish_runtime_event(request: SessionEventPublishRequest) -> dict[str, t.Any]:
    """Inject a runtime-scope event into the runtime event bus (CAP-WCLI-013).

    Peer of ``/api/sessions/{session_id}/events`` for events without a session
    scope. Subscribers receive the event regardless of scope per CAP-WEVT-002.
    Reserved-prefix kinds are rejected (CAP-WEVT-003).
    """
    _reject_reserved_kind(request.kind)
    envelope = await get_state().event_bus.publish(
        kind=request.kind,
        session_id=None,
        payload=request.payload,
    )
    # event_bus.publish only returns None for dropped sessions; runtime-scope
    # publishes carry no session_id, so None is not a reachable outcome here.
    assert envelope is not None
    return {"event_id": envelope.event_id, "seq": envelope.seq}


@app.post("/api/ws/ticket", response_model=WsTicketResponse)
async def create_ws_ticket_endpoint(request: Request) -> WsTicketResponse | JSONResponse:
    """Mint a short-lived, single-use websocket auth ticket.

    Browsers cannot set an ``Authorization`` header on a websocket handshake,
    so they exchange the runtime bearer token (over HTTP, where the header
    *is* allowed) for a one-time ticket, then open
    ``wss://<runtime>/api/ws?ticket=<ticket>``.

    Protected by ``SandboxAuthMiddleware``: the caller must already present the
    runtime bearer token. Returns 400 when runtime auth is disabled, since
    tickets are meaningless there (local unsecured ws auth is headerless).

    The ticket is bound to the token that minted it, and only a *current* token
    may mint one — otherwise a client whose token was just rotated out could
    trade its retired credential for a ticket and reconnect anyway.
    """
    source = get_token_source()
    if not source.enabled():
        return JSONResponse(
            {"detail": "Runtime websocket tickets require runtime auth"},
            status_code=400,
        )

    presented = bearer_token(request.headers.get("authorization"))
    if presented is None or not source.is_current(presented):
        return JSONResponse(
            {"detail": "Websocket tickets require the current runtime token"},
            status_code=401,
        )

    ticket = get_state().ws_ticket_store.mint(token=presented, ttl_seconds=30)
    return WsTicketResponse(ticket=ticket.ticket, expires_at=ticket.expires_at)


@app.websocket("/api/ws")
async def runtime_websocket_endpoint(websocket: WebSocket) -> None:
    """Interactive websocket transport for runtime session control and streaming."""

    def _resolve_socket_session(session_id: str) -> SessionRuntime:
        session = get_state().get_session(session_id)
        if session is None:
            # Websocket-first session creation — no client ever called
            # POST /api/sessions. This means the session gets the default
            # interactive policy regardless of what the client intended.
            # Clients needing a non-default policy must POST first.
            logger.warning(
                "Auto-creating session {} from websocket command — "
                "non-default session policy is ignored on this path, "
                "POST /api/sessions first if you need one",
                session_id[:8],
            )
            session = get_state().create_session(session_id=session_id)
        return session

    await serve_runtime_websocket(
        websocket,
        event_bus=get_state().event_bus,
        resolve_session=_resolve_socket_session,
        get_session=lambda session_id: get_state().get_session(session_id),
        sync_accepted_turn=_sync_accepted_turn_with_platform,
        consume_ticket=get_state().ws_ticket_store.consume,
        connection_registry=get_state().ws_connections,
    )


@app.websocket("/api/ws/events")
async def runtime_event_stream_endpoint(websocket: WebSocket) -> None:
    """Runtime-bus event subscription stream (CAP-WCLI-018..020).

    Consumers subscribe with an optional repeated ``?kinds=<kind>`` query
    param to filter by kind; omit it to receive every event. Both
    session- and runtime-scope envelopes are delivered so subscribers can
    inspect ``session_id`` to distinguish. Peer of the interactive
    transport at :func:`runtime_websocket_endpoint`; kept separate so
    the session control plane and the worker-facing bus stream do not
    share a protocol.
    """
    await serve_runtime_event_stream(
        websocket,
        event_bus=get_state().event_bus,
        consume_ticket=get_state().ws_ticket_store.consume,
        connection_registry=get_state().ws_connections,
    )


@app.post("/api/sessions/{session_id}/title")
async def set_session_title(session_id: str, body: dict[str, t.Any]) -> JSONResponse:
    """Set the session title."""
    session = get_state().get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")
    title = body.get("title", "")
    session.title = title or None
    await asyncio.to_thread(session._persist_state, update_messages=False)
    return JSONResponse({"status": "ok", "session_id": session_id, "title": session.title})


@app.post("/api/sessions/{session_id}/policy")
async def set_session_policy(session_id: str, body: dict[str, t.Any]) -> JSONResponse:
    """Swap the session's active policy mid-run.

    Body shape: ``{"policy": "interactive"}`` or
    ``{"policy": {"name": "headless", "max_steps": 30}}`` — same spec
    format accepted by ``POST /api/sessions`` so both paths share one
    registry. Invalid policy names fail with 400.

    Hot-swap semantics: new ``ask_user()`` calls after this endpoint
    returns hit the new policy immediately; continuation hooks apply
    on the next turn (see ``SessionRuntime.set_policy``).
    """
    from dreadnode.policies import resolve_policy

    session = get_state().get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")
    spec = body.get("policy")
    try:
        resolved = resolve_policy(spec)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    session.set_policy(resolved)
    return JSONResponse(
        {
            "status": "ok",
            "session_id": session_id,
            "policy_name": getattr(resolved, "name", "interactive"),
            "policy_is_autonomous": bool(getattr(resolved, "is_autonomous", False)),
            "policy_display_label": str(getattr(resolved, "display_label", "") or ""),
        }
    )


@app.post("/api/sessions/{session_id}/cancel")
async def cancel_session(session_id: str) -> JSONResponse:
    """Cancel the active turn and drain queued requests for a session."""
    session = get_state().get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")
    was_busy = await session.cancel()
    return JSONResponse(
        content={
            "status": "cancelled" if was_busy else "idle",
            "session_id": session_id,
        }
    )


@app.post("/api/sessions/{session_id}/compact")
async def compact_session(session_id: str, body: dict[str, t.Any] | None = None) -> JSONResponse:
    """Compact a session's conversation history (CMP-API-001)."""
    session = get_state().get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")
    if session.is_busy:
        return JSONResponse(content={"status": "skipped", "reason": "turn_in_progress"})
    guidance = (body or {}).get("guidance", "")
    result = await session.compact_session(trigger="manual", guidance=guidance)
    return JSONResponse(content=result)


@app.get("/api/sessions/{session_id}/rewind/candidates")
async def list_rewind_candidates(session_id: str) -> JSONResponse:
    """Return user-message rewind targets pulled from platform-side transcript.

    The picker uses this rather than the runtime's in-memory trajectory
    because seqs only exist on the platform side; the in-memory copy
    does not track them.
    """
    session = get_state().get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")
    return JSONResponse(content=await asyncio.to_thread(session.list_rewind_candidates))


@app.post("/api/sessions/{session_id}/rewind")
async def rewind_session(session_id: str, body: dict[str, t.Any]) -> JSONResponse:
    """Hard-truncate a session's transcript at a target user-message seq."""
    session = get_state().get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")
    raw_seq = body.get("from_seq")
    if not isinstance(raw_seq, int) or raw_seq < 0:
        raise HTTPException(
            status_code=422,
            detail="from_seq must be a non-negative integer",
        )
    result = await session.rewind_to(from_seq=raw_seq)
    return JSONResponse(content=result)


# =============================================================================
# File & Shell Endpoints
# =============================================================================

IGNORED_NAMES = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
        ".tox",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "dist",
        "build",
        ".eggs",
    }
)


@app.get("/api/files")
async def list_files(
    path: str | None = None,
    depth: int = 10,
) -> JSONResponse:
    """List directory contents recursively."""

    # When DREADNODE_PROJECT_ROOT is set (E2B sandboxes), scope the file
    # browser to the workspace directory instead of showing the entire
    # home directory (which may contain pip-installed SDK source trees).
    project_root = os.environ.get("DREADNODE_PROJECT_ROOT")
    if project_root:
        base = Path(project_root)
    elif path:
        base = Path(path)
    else:
        base = Path.cwd()
    if not base.is_dir():
        return JSONResponse({"path": str(base), "entries": [], "error": "Not a directory"})

    entries: list[dict[str, t.Any]] = []

    async def _walk(dir_path: Path, current_depth: int) -> None:
        try:
            items = sorted(dir_path.iterdir())
        except PermissionError:
            return
        for item in items:
            if item.name.startswith(".") or item.name in IGNORED_NAMES:
                continue
            is_dir = item.is_dir()
            size = None
            if not is_dir:
                with suppress(OSError):
                    size = item.stat().st_size
            entries.append(
                {
                    "name": item.name,
                    "path": str(item.relative_to(base)),
                    "isDir": is_dir,
                    "size": size,
                }
            )
            if is_dir and current_depth < depth:
                await _walk(item, current_depth + 1)

    await _walk(base, 0)
    return JSONResponse({"path": str(base), "entries": entries})


@app.get("/api/files/read")
async def read_file(path: str) -> JSONResponse:
    """Read a file's content."""
    file_path = Path(path)
    if not file_path.is_file():
        return JSONResponse(
            {"path": path, "content": "", "error": "File not found"}, status_code=404
        )
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
        return JSONResponse({"path": path, "content": content})
    except Exception as exc:
        return JSONResponse({"path": path, "content": "", "error": str(exc)}, status_code=500)


@app.post("/api/shell")
async def execute_shell(
    command: str = "",
    cwd: str | None = None,
    timeout: int = 30,  # noqa: ASYNC109
) -> JSONResponse:
    """Execute a shell command directly (not through agent)."""
    import asyncio as _asyncio

    if not command.strip():
        return JSONResponse({"error": "Empty command"}, status_code=400)

    work_dir = cwd or str(Path.cwd())
    try:
        proc = await _asyncio.create_subprocess_shell(
            command,
            stdout=_asyncio.subprocess.PIPE,
            stderr=_asyncio.subprocess.PIPE,
            cwd=work_dir,
        )
        stdout_bytes, stderr_bytes = await _asyncio.wait_for(proc.communicate(), timeout=timeout)
        return JSONResponse(
            {
                "stdout": stdout_bytes.decode("utf-8", errors="replace"),
                "stderr": stderr_bytes.decode("utf-8", errors="replace"),
                "exitCode": proc.returncode,
                "command": command,
            }
        )
    except TimeoutError:
        proc.kill()
        return JSONResponse(
            {"error": f"Command timed out after {timeout}s", "command": command}, status_code=408
        )
    except Exception as exc:
        return JSONResponse({"error": str(exc), "command": command}, status_code=500)


@app.get("/api/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="ok")


@app.get("/api/runtime", response_model=RuntimeInfoResponse)
async def runtime_info() -> RuntimeInfoResponse:
    """Expose loaded capability metadata for CLI/runtime synchronization."""
    registry = get_state().capability_registry
    if registry is None:
        return RuntimeInfoResponse(working_dir=str(Path.cwd()))
    return registry.to_runtime_info(working_dir=Path.cwd())


def _tool_description(tool: t.Any) -> str:
    desc = getattr(tool, "description", None)
    if isinstance(desc, str) and desc:
        return desc
    doc = getattr(tool, "__doc__", None)
    return (doc or "").split("\n")[0] if isinstance(doc, str) else ""


def _tool_parameters_schema(tool: t.Any) -> dict[str, t.Any] | None:
    """Extract a JSON Schema for a tool's parameters, if it exposes one.

    First-class :class:`dreadnode.agents.tools.Tool` instances use
    ``parameters_schema``; MCP tools typically expose ``parameters`` (a
    raw JSON Schema) or ``input_schema``. Return ``None`` for anything
    else — the TUI falls back to its generic formatter.
    """
    schema = getattr(tool, "parameters_schema", None)
    if isinstance(schema, dict):
        return schema
    params = getattr(tool, "parameters", None)
    if isinstance(params, dict):
        return params
    input_schema = getattr(tool, "input_schema", None)
    if isinstance(input_schema, dict):
        return input_schema
    return None


@app.get("/api/tools", response_model=ToolsResponse)
async def list_tools() -> ToolsResponse:
    """List all available tools grouped by source capability."""
    from dreadnode.tools import default_tools

    registry = get_state().capability_registry
    items: list[ToolInfo] = []

    # Built-in tools
    for name, tool in default_tools().items():
        items.append(
            ToolInfo(
                name=name,
                wire_name=getattr(tool, "wire_name", name),
                source=getattr(tool, "source", "builtin"),
                description=_tool_description(tool),
                capability="built-in",
                parameters_schema=_tool_parameters_schema(tool),
            )
        )

    if registry is None:
        return ToolsResponse(tools=items)

    # Capability tools (Python + bundled). MCP tools are walked separately
    # via iter_qualified_tools so the server segment is populated correctly.
    for cap_name, capability in registry.capabilities.items():
        for tool in capability.tools:
            items.append(
                ToolInfo(
                    name=_tool_name(tool) or "?",
                    wire_name=getattr(tool, "wire_name", None),
                    source=getattr(tool, "source", None),
                    description=_tool_description(tool),
                    capability=cap_name,
                    parameters_schema=_tool_parameters_schema(tool),
                )
            )

    # MCP tools — use the snapshotting iterator so concurrent reconnect
    # doesn't raise (CAP-IDENT-007, Will's Gap #11).
    if registry.mcp_manager:
        for cap_name, server_name, tool in registry.mcp_manager.iter_qualified_tools():
            items.append(
                ToolInfo(
                    name=_tool_name(tool) or "?",
                    wire_name=getattr(tool, "wire_name", None),
                    source=getattr(tool, "source", "mcp"),
                    server=server_name,
                    description=getattr(tool, "description", "") or "",
                    capability=cap_name,
                    parameters_schema=_tool_parameters_schema(tool),
                )
            )

    # Session-scoped tools (always present when skills/subagents available)
    all_skills = registry.all_skills()
    if all_skills:
        skill_names = ", ".join(s.name for s in all_skills[:5])
        suffix = f" (+{len(all_skills) - 5} more)" if len(all_skills) > 5 else ""
        items.append(
            ToolInfo(
                name="load_skill",
                description=f"Load skill instructions ({skill_names}{suffix})",
                capability="session",
            )
        )
    items.append(
        ToolInfo(
            name="spawn_agent",
            description="Spawn a sub-agent for task delegation",
            capability="session",
        )
    )

    return ToolsResponse(tools=items)


@app.get("/api/skills", response_model=SkillsResponse)
async def list_skills() -> SkillsResponse:
    """List all available skills from loaded capabilities.

    Response includes the qualified identifier (`qualified_id`), source, and
    owning capability per skill (CAP-IDENT-019).
    """
    registry = get_state().capability_registry
    if registry is None:
        return SkillsResponse()

    def _capability_of(skill: t.Any) -> str | None:
        namespace = getattr(skill, "namespace", ()) or ()
        return namespace[0] if namespace else None

    return SkillsResponse(
        skills=[
            SkillInfoModel(
                name=s.name,
                description=s.description,
                qualified_id=s.qualified_id,
                source=getattr(s, "source", None),
                capability=_capability_of(s),
            )
            for s in sorted(registry.all_skills(), key=lambda s: s.qualified_id)
        ]
    )


@app.get("/api/skills/{name}", response_model=SkillContentResponse)
async def get_skill(name: str) -> SkillContentResponse:
    """Get full skill content by qualified identifier or bare name.

    Accepts either the qualified id (`{cap}:{name}`) or an unambiguous bare
    name (CAP-IDENT-017). Ambiguous bare names return 404 with qualified
    candidates in the detail. Returns both raw instructions and rendered
    content (matching load_skill tool output).
    """
    from dreadnode.agents.skills import resolve_skill

    registry = get_state().capability_registry
    if registry is None:
        raise HTTPException(status_code=404, detail="No capabilities loaded")

    skills = registry.all_skills()
    try:
        skill = resolve_skill(name, skills)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    namespace = getattr(skill, "namespace", ()) or ()
    return SkillContentResponse(
        name=skill.name,
        description=skill.description,
        instructions=skill.instructions,
        allowed_tools=skill.allowed_tools,
        rendered=skill.render_content(),
        qualified_id=skill.qualified_id,
        source=getattr(skill, "source", None),
        capability=namespace[0] if namespace else None,
    )


@app.post("/api/reload", response_model=RuntimeInfoResponse)
async def reload_capabilities() -> RuntimeInfoResponse:
    """Re-discover capabilities and rebuild the registry.

    Active sessions detect the change on their next turn and recreate
    agents with the updated tool/skill set.
    """
    from dreadnode import _get_default_instance

    reload_started_at = time.perf_counter()
    stop_ms = 0
    populate_ms = 0
    start_ms = 0

    # Stop old workers first (CAP-WLIF-005: cold restart on reload)
    old_registry = get_state().capability_registry
    if old_registry and old_registry.worker_manager:
        await old_registry.worker_manager.stop()

    # Stop old MCP servers before replacing the registry
    if old_registry and old_registry.mcp_manager:
        stop_started_at = time.perf_counter()
        await old_registry.mcp_manager.stop()
        stop_ms = round((time.perf_counter() - stop_started_at) * 1000)

    instance = _get_default_instance()
    populate_started_at = time.perf_counter()
    await asyncio.to_thread(_populate_registry, instance)
    populate_ms = round((time.perf_counter() - populate_started_at) * 1000)

    # Start MCP servers for the new registry. ``start()`` is non-blocking
    # (CAP-MCP-009); under DREADNODE_SYNCHRONOUS_STARTUP, the reload also
    # waits for connects to settle so the response reflects the post-reload
    # toolset, matching the eval-orchestrator contract.
    registry = get_state().capability_registry
    if registry:
        registry.mcp_manager = capability_manager.MCPLifecycleManager(
            event_bus=get_state().event_bus,
        )
        start_started_at = time.perf_counter()
        await registry.mcp_manager.start(registry)
        if _is_synchronous_startup():
            await registry.mcp_manager.wait_for_connects()
        start_ms = round((time.perf_counter() - start_started_at) * 1000)

    # Start new workers AFTER MCP (CAP-WLIF-002)
    if registry:
        from dreadnode.app.server.worker_manager import WorkerLifecycleManager

        registry.worker_manager = WorkerLifecycleManager(get_state().event_bus, app)
        await registry.worker_manager.start(registry)

    capability_count = len(registry.capabilities) if registry else 0
    logger.info(
        "Capability reload timing | stop_mcp_ms={} | populate_ms={} | start_mcp_ms={} | total_ms={} | capabilities={}",
        stop_ms,
        populate_ms,
        start_ms,
        round((time.perf_counter() - reload_started_at) * 1000),
        capability_count,
    )

    await get_state().event_bus.publish(
        kind=runtime_events.EVENT_CAPABILITIES_RELOADED,
        payload={"capability_count": capability_count},
    )

    if registry is None:
        return RuntimeInfoResponse(working_dir=str(Path.cwd()))
    return registry.to_runtime_info(working_dir=Path.cwd())


@app.get("/api/mcp/{capability}/{server_name}")
async def get_mcp_server_detail(capability: str, server_name: str) -> dict[str, t.Any]:
    """Return full detail for an MCP server."""
    state = get_state()
    if state.capability_registry is None or state.capability_registry.mcp_manager is None:
        raise HTTPException(status_code=404, detail="No MCP manager available")
    detail = state.capability_registry.mcp_manager.get_server_detail(capability, server_name)
    if detail is None:
        raise HTTPException(
            status_code=404, detail=f"MCP server '{capability}:{server_name}' not found"
        )
    return detail


@app.post("/api/mcp/{capability}/{server_name}/reconnect")
async def reconnect_mcp_server(capability: str, server_name: str) -> dict[str, t.Any]:
    """Reconnect an MCP server.

    Returns 409 when the server is gated off (CAP-FLAG-014 / CAP-WLIF-006
    parity), identifying the gating flag(s).
    """
    state = get_state()
    if state.capability_registry is None or state.capability_registry.mcp_manager is None:
        raise HTTPException(status_code=404, detail="No MCP manager available")
    result = await state.capability_registry.mcp_manager.reconnect_server(capability, server_name)
    if result is None:
        raise HTTPException(
            status_code=404, detail=f"MCP server '{capability}:{server_name}' not found"
        )
    if result.get("gated_off"):
        flags = result.get("when") or []
        flags_label = ", ".join(flags) if flags else "(none)"
        raise HTTPException(
            status_code=409,
            detail={
                "reason": "gated_off",
                "message": (
                    f"MCP server '{capability}:{server_name}' is gated off "
                    f"by flag(s): {flags_label}"
                ),
                "when": flags,
            },
        )
    return result


@app.post("/api/mcp/{capability}/{server_name}/reauthenticate")
async def reauthenticate_mcp_server(capability: str, server_name: str) -> dict[str, t.Any]:
    """Clear stored OAuth credentials and trigger a fresh OAuth flow.

    Targeted: only this server's tokens are removed; other authenticated
    capabilities keep their credentials. Use ``reconnect`` if you just
    want to drop the connection and re-establish with the current
    credentials (no browser open for cached-token cases).

    Returns 404 if the server is not OAuth-configured (stdio servers and
    HTTP servers without ``auth: oauth`` are not eligible — re-auth on
    those would be a no-op).
    """
    state = get_state()
    if state.capability_registry is None or state.capability_registry.mcp_manager is None:
        raise HTTPException(status_code=404, detail="No MCP manager available")
    manager = state.capability_registry.mcp_manager
    result = await manager.reauthenticate_server(capability, server_name)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"MCP server '{capability}:{server_name}' not found or not "
                f"OAuth-configured (re-authenticate only applies to servers "
                f"with auth: oauth)."
            ),
        )
    return result


# =============================================================================
# Worker Endpoints
# =============================================================================


@app.get("/api/workers/{capability}/{worker_name}")
async def get_worker_detail(capability: str, worker_name: str) -> dict[str, t.Any]:
    """Return detail for a specific capability worker."""
    state = get_state()
    if state.capability_registry is None or state.capability_registry.worker_manager is None:
        raise HTTPException(status_code=404, detail="No worker manager available")
    detail = state.capability_registry.worker_manager.get_worker_detail(capability, worker_name)
    if detail is None:
        raise HTTPException(
            status_code=404, detail=f"Worker '{capability}:{worker_name}' not found"
        )
    return detail


@app.post("/api/workers/{capability}/{worker_name}/restart")
async def restart_worker(capability: str, worker_name: str) -> dict[str, t.Any]:
    """Restart a capability worker (CAP-WLIF-006).

    Returns 409 when the worker is gated off, identifying the gating
    flag(s) so the operator knows which flag to flip.
    """
    state = get_state()
    if state.capability_registry is None or state.capability_registry.worker_manager is None:
        raise HTTPException(status_code=404, detail="No worker manager available")
    result = await state.capability_registry.worker_manager.restart_worker(capability, worker_name)
    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Worker '{capability}:{worker_name}' not found"
        )
    if result.get("gated_off"):
        flags = result.get("when") or []
        flags_label = ", ".join(flags) if flags else "(none)"
        raise HTTPException(
            status_code=409,
            detail={
                "reason": "gated_off",
                "message": (
                    f"Worker '{capability}:{worker_name}' is gated off by flag(s): {flags_label}"
                ),
                "when": flags,
            },
        )
    return result


# =============================================================================
# Server Entry Point
# =============================================================================


def _read_capability_system_prompt(path: Path) -> str:
    """Read and normalize an optional capability-level system prompt."""
    import re

    prompt_file = path / "system-prompt.md"
    if not prompt_file.exists():
        return ""

    content = prompt_file.read_text().strip()
    frontmatter_match = re.match(r"^---\s*\n[\s\S]*?\n---\s*\n([\s\S]*)", content)
    if frontmatter_match:
        content = frontmatter_match.group(1).strip()
    return content


def _sync_runtime_capabilities_if_available(
    instance: t.Any,
) -> tuple[Path | None, list[dict[str, t.Any]]]:
    """Sync runtime-scoped capabilities if platform credentials are available.

    Returns (runtime_cache_dir, runtime_bindings).
    """
    runtime_id = os.environ.get("DREADNODE_RUNTIME_ID", "").strip()
    if not instance.can_sync or not runtime_id:
        logger.info(
            "Capability sync skipped (can_sync={}, runtime_id={})",
            instance.can_sync,
            runtime_id or "<empty>",
        )
        return None, []

    from dreadnode.capabilities.sync import CapabilitySyncClient

    try:
        cache_dir = instance.storage.workspace_capabilities_path
        # asyncio.run() is safe here because _populate_registry runs inside
        # asyncio.to_thread(), which means we're in a thread pool worker with
        # no running event loop. asyncio.run() creates a fresh loop.
        client = CapabilitySyncClient(
            api=instance.api,
            org=instance.profile.org_key,
            workspace=instance.profile.workspace_key,
            runtime_id=runtime_id,
            cache_dir=cache_dir,
        )
        result = asyncio.run(client.sync())
        if result.synced:
            logger.info("Synced workspace capabilities: {}", result.synced)
        if result.removed:
            logger.info("Removed stale workspace capabilities: {}", result.removed)
        if result.errors:
            for err in result.errors:
                logger.warning("Failed to sync '{}': {}", err.name, err.error)
    except Exception:
        logger.warning("Runtime capability sync failed — using local only", exc_info=True)
        return None, []
    else:
        return (
            cache_dir,
            result.bindings,
        )  # partial sync: returns bindings even when some errors occurred


def _check_capability_updates(
    api: t.Any,
    records: dict[str, dict[str, t.Any]],
    *,
    timeout: float = 2.0,
) -> dict[str, str]:
    """Check platform for newer versions of installed capabilities.

    Returns mapping of artifact_identity -> latest version for capabilities
    that have updates available. Returns empty dict on timeout or error.
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    from packaging.version import InvalidVersion, Version

    checkable: list[tuple[str, str, str, str, str]] = []
    for record in records.values():
        identity = record.get("artifact_identity")
        source = record.get("source", "org")
        version = record.get("version")
        if not identity or not version or "/" not in identity:
            continue
        owner, name = identity.split("/", 1)
        checkable.append((identity, owner, name, version, source))

    if not checkable:
        return {}

    def _fetch_latest(
        item: tuple[str, str, str, str, str],
    ) -> tuple[str, str | None, str]:
        identity, owner, name, installed_ver, _source = item
        try:
            resp = api.list_capability_versions(owner, name, timeout=timeout)
            latest = resp.get("latest")
            if isinstance(latest, dict):
                return identity, latest.get("version"), installed_ver
            versions = resp.get("versions", [])
            return identity, versions[0] if versions else None, installed_ver
        except Exception:
            return identity, None, installed_ver

    updates: dict[str, str] = {}
    executor = ThreadPoolExecutor(max_workers=min(len(checkable), 4))
    try:
        futures = {executor.submit(_fetch_latest, item): item for item in checkable}
        for future in as_completed(futures, timeout=timeout):
            try:
                identity, latest_ver, installed_ver = future.result()
                if latest_ver is None:
                    continue
                if Version(latest_ver) > Version(installed_ver):
                    updates[identity] = latest_ver
            except InvalidVersion:
                continue
            except Exception:
                logger.debug("Failed to check capability version", exc_info=True)
    except TimeoutError:
        logger.debug("Capability update check timed out after {}s", timeout)
    except Exception:
        logger.debug("Capability update check failed", exc_info=True)
    finally:
        executor.shutdown(wait=True, cancel_futures=True)

    return updates


def _populate_registry(instance: t.Any) -> None:
    """Discover capabilities and install them into app state."""
    from dreadnode.builtin_capabilities import load_builtin_capabilities
    from dreadnode.capabilities import Capability
    from dreadnode.capabilities.capability import (
        read_local_capability_records,
        read_local_capability_state,
    )

    state = get_state()
    registry = capability_manager.CapabilityRegistry()

    builtin_capabilities, builtin_failures = load_builtin_capabilities(
        cwd=Path.cwd(),
        storage=instance.storage,
        capability_dirs=state.capability_dirs,
    )
    registry.capabilities.update(builtin_capabilities)
    registry.load_failures.extend(builtin_failures)

    # 1. Sync runtime capabilities if platform credentials are available
    workspace_dir, runtime_bindings = _sync_runtime_capabilities_if_available(instance)
    registry.runtime_bindings = runtime_bindings
    # 2. Determine host type: sandbox if runtime binding env is set, local otherwise
    host = "sandbox" if os.environ.get("DREADNODE_RUNTIME_ID", "").strip() else "local"

    # 3. Install declared dependencies before discovery so preflight `checks:`
    # see installed binaries. Failures log loudly but never block load —
    # `checks:` is the user-visible signal for unmet prerequisites.
    install_failures: dict[str, str] = {}
    if host == "sandbox" and workspace_dir is not None:
        try:
            from dreadnode.capabilities.install import install_dependencies
            from dreadnode.capabilities.loader import preload_dependency_specs

            install_specs = preload_dependency_specs(workspace_dir)
            install_report = install_dependencies(install_specs)
            if install_report.installed:
                logger.info(
                    "Installed dependencies for {} capabilities: {}",
                    len(install_report.installed),
                    install_report.installed,
                )
            if install_report.cached:
                logger.debug("Skipped install (already cached) for: {}", install_report.cached)
            install_failures = dict(install_report.failed)
            for cap_name, error in install_report.failed.items():
                logger.error("Dependency install failed for capability '{}': {}", cap_name, error)
        except Exception:
            logger.opt(exception=True).warning(
                "Capability dependency install pass failed; continuing with discovery"
            )

    # 4. Discover with host-exclusive source (CAP-LOAD-014)
    shadowed_names: set[str] = set()
    try:
        result = Capability.discover(
            cwd=Path.cwd(),
            storage=instance.storage,
            capability_dirs=state.capability_dirs,
            workspace_dir=workspace_dir,
            host=host,
        )
        for cap in result.capabilities.values():
            if cap.name in registry.capabilities:
                logger.warning(
                    "Capability '{}' shadows bundled capability and will be ignored: {}",
                    cap.name,
                    cap.path,
                )
                shadowed_names.add(cap.name)
                continue
            registry.capabilities[cap.name] = cap
        registry.disabled_local = result.disabled
        registry.load_failures.extend(
            {
                "name": failure.get("name", "unknown"),
                "path": str(failure.get("path", "")),
                "error": failure.get("error", "unknown error"),
                "source": "local",
            }
            for failure in result.failures
        )
        registry.local_capability_records = read_local_capability_records(
            instance.storage.local_capability_state_path
        )
    except Exception:
        logger.exception("Failed to discover capabilities")

    # A dependency install failure leaves the capability loaded but missing the
    # packages its components import, so discovery alone reports it healthy.
    # Stamp the failure onto component_health — without it the runtime returns a
    # clean bill for a capability whose deps never landed (ENG-7599 / ENG-7607).
    for cap_name, error in install_failures.items():
        capability = registry.capabilities.get(cap_name)
        # A shadowed name resolves to the bundled capability, which is healthy —
        # stamping there would send operators after the wrong component.
        if capability is None or cap_name in shadowed_names:
            logger.warning(
                "Dependency install failed for capability '{}' but it is not registered; "
                "the failure will not appear in component health: {}",
                cap_name,
                error,
            )
            continue
        capability.component_health.append(
            {
                "kind": "capability",
                "name": cap_name,
                "status": "error",
                "error": f"Dependency install failed: {error}",
            }
        )

    # Bundled caps don't flow through Capability.discover(), so the
    # disabled-state filter that runs inside discover() never touches
    # them — they'd always load as active regardless of
    # local-capability-state.json. Apply the same filter here so the
    # toggle is honored. The default capability is pinned active.
    bundled_state = read_local_capability_state(instance.storage.local_capability_state_path)
    for name in list(registry.capabilities):
        if name == _BUNDLED_DEFAULT_CAPABILITY:
            continue
        if bundled_state.get(name, True) is False:
            registry.disabled_local[name] = registry.capabilities.pop(name)

    if instance.can_sync:
        try:
            registry.update_info = _check_capability_updates(
                instance.api,
                registry.local_capability_records,
            )
            if registry.update_info:
                logger.info(
                    "Capability updates available: {}",
                    dict(registry.update_info),
                )
        except Exception:
            logger.debug("Capability update check skipped", exc_info=True)

    # Apply exclusive capability filter from CLI --capability flags
    if state.enabled_capabilities:
        allowed = set(state.enabled_capabilities)
        to_disable = {n: c for n, c in registry.capabilities.items() if n not in allowed}
        for name, cap in to_disable.items():
            registry.disabled_local[name] = cap
            del registry.capabilities[name]

    if _BUNDLED_DEFAULT_CAPABILITY in registry.capabilities:
        registry.default_capability_name = _BUNDLED_DEFAULT_CAPABILITY
    elif registry.capabilities:
        registry.default_capability_name = next(iter(registry.capabilities))

    state.capability_registry = registry
    logger.info(
        "Loaded {} capabilities: {}",
        len(registry.capabilities),
        list(registry.capabilities.keys()) or "(none)",
    )
    # Register any policy classes shipped by the loaded capabilities
    # into the global ``POLICY_REGISTRY`` so they become resolvable by
    # name at session-create time. Built-in policies
    # (``interactive``, ``headless``) are already there; these layer
    # on top without overriding.
    try:
        registered_policies = registry.register_capability_policies()
        if registered_policies:
            logger.info(
                "Registered {} capability policies: {}",
                len(registered_policies),
                registered_policies,
            )
    except Exception:
        logger.opt(exception=True).warning("Policy registration failed during capability load")
    if registry.load_failures:
        for f in registry.load_failures:
            logger.warning(
                "Capability load failure: {} at {} — {}", f["name"], f["path"], f["error"]
            )

    # Resolve capability flags after all capabilities are loaded
    _resolve_all_flags(registry, instance)


def _resolve_all_flags(registry: capability_manager.CapabilityRegistry, _instance: t.Any) -> None:
    """Resolve capability flags for all loaded capabilities.

    After resolution, flag env vars are set in ``os.environ`` so that
    in-process Python tools can read them at both import and call time.
    Stale vars from a previous registry are cleaned up first.
    """
    from dreadnode.capabilities.flags import (
        parse_cli_flags,
        read_env_overrides,
        validate_flags_block,
    )

    state = get_state()
    cli_overrides = parse_cli_flags(state.capability_flag_overrides)
    is_sandbox = bool(os.environ.get("DREADNODE_RUNTIME_ID", "").strip())

    # In sandbox mode, binding flags come from the platform API
    binding_flags_by_name: dict[str, dict[str, bool]] = {}
    if is_sandbox:
        for binding in registry.runtime_bindings:
            from dreadnode.capabilities.sync import bare_capability_name

            bare = bare_capability_name(binding.get("capability_name", ""))
            binding_flags_by_name[bare] = binding.get("flags", {})

    for cap in registry.capabilities.values():
        flag_defs = validate_flags_block(cap.manifest.flags, Path(cap.path) / "capability.yaml")
        if not flag_defs:
            continue
        if is_sandbox:
            raw_flags = binding_flags_by_name.get(cap.name, {})
        else:
            raw_flags = registry.local_capability_records.get(cap.name, {}).get("flags", {})
        persisted = raw_flags if isinstance(raw_flags, dict) else {}
        env = read_env_overrides(cap.name, flag_defs)
        cli = cli_overrides.get(cap.name, {})
        cap.resolve_flags(persisted=persisted, env_overrides=env, cli_overrides=cli)

    # CAP-FLAG-020: set resolved flag env vars in the process environment.
    # Clean stale vars from a previous registry first, then set current values.
    stale = [k for k in os.environ if k.startswith("CAPABILITY_FLAG__")]
    for k in stale:
        del os.environ[k]
    for cap in registry.capabilities.values():
        os.environ.update(cap.flag_env_vars())


def initialize_app(
    *,
    server: str | None = None,
    api_key: str | None = None,
    organization: str | None = None,
    workspace: str | None = None,
    project: str | None = None,
    capability_dirs: list[str] | None = None,
    enabled_capabilities: list[str] | None = None,
    capability_flag_overrides: list[str] | None = None,
    system_prompt_append: str | None = None,
) -> None:
    """Initialize app state: configure a Dreadnode instance and discover capabilities.

    Creates a fresh ``Dreadnode`` instance (bypassing the singleton's idempotent
    guard) and replaces ``DEFAULT_INSTANCE`` so that server-side code using
    ``_get_default_instance()`` picks up the new credentials.

    Must be called via ``asyncio.to_thread()`` from async contexts because
    ``Capability.discover()`` internally calls ``asyncio.run()``.
    """
    import dreadnode.app.main as main_mod

    instance = main_mod.Dreadnode()
    instance.configure(
        server=server,
        api_key=api_key,
        organization=organization,
        workspace=workspace,
        project=project,
    )
    main_mod.DEFAULT_INSTANCE = instance

    # Store CLI overrides on state so they persist across /reload
    state = get_state()
    state.capability_dirs = capability_dirs
    state.enabled_capabilities = enabled_capabilities
    state.capability_flag_overrides = capability_flag_overrides
    state.system_prompt_append = system_prompt_append

    _populate_registry(instance)


def reset_app_state() -> None:
    """Clear all server state: close sessions and reset the capability registry.

    Called before re-running ``initialize_app()`` on restart.
    """
    if not hasattr(app.state, "server"):
        return

    state: ServerState = app.state.server

    # Stop MCP servers if running (best-effort, sync context)
    if state.capability_registry and state.capability_registry.mcp_manager:
        manager = state.capability_registry.mcp_manager
        try:
            asyncio.get_running_loop()
            # In async context — schedule and let it complete
            asyncio.create_task(manager.stop())  # noqa: RUF006
        except RuntimeError:
            # No running loop — safe to run synchronously
            asyncio.run(manager.stop())

    for session in state.list_sessions():
        session.close()

    app.state.server = ServerState()


def _on_runtime_token_retired(retired: str) -> None:
    """Revoke everything the retired runtime token still authorizes.

    Rotation is how the platform severs a stale client. Closing its live
    websockets is not enough on its own: an unredeemed ticket it minted before
    the rotation would let it right back in for the rest of that ticket's TTL.
    """
    state = get_state()
    closed = state.ws_connections.close_for_token(retired)
    purged = state.ws_ticket_store.purge_for_token(retired)
    logger.info(
        "Runtime token retired | websockets_closed={} tickets_revoked={}",
        closed,
        purged,
    )


def run_server(
    instance: t.Any | None = None,
    *,
    host: str | None = None,
    port: int | None = None,
    server: str | None = None,
    api_key: str | None = None,
    organization: str | None = None,
    workspace: str | None = None,
    project: str | None = None,
) -> None:
    """Run the FastAPI server with uvicorn."""
    from dreadnode import _get_default_instance

    if instance is None:
        instance = _get_default_instance()
    instance.configure(
        server=server,
        api_key=api_key,
        organization=organization,
        workspace=workspace,
        project=project,
    )

    _populate_registry(instance)

    resolved_host = host or read_env_with_deprecation(
        "DREADNODE_RUNTIME_HOST", "DREADNODE_SERVER_HOST", "127.0.0.1"
    )
    resolved_port = port or int(
        read_env_with_deprecation("DREADNODE_RUNTIME_PORT", "DREADNODE_SERVER_PORT", "8787")
    )

    # Workers connect via loopback even when we bind to all interfaces, since
    # the all-interfaces sentinel is a listen-only address — not a connect
    # target. ``resolved_host`` is what we pass to uvicorn; ``advertised_host``
    # is what subprocess workers (and other ``RuntimeClient`` consumers) use.
    advertised_host = (
        "127.0.0.1" if resolved_host in {"0.0.0.0", "::"} else resolved_host  # noqa: S104
    )
    state = get_state()
    state.runtime_url = f"http://{advertised_host}:{resolved_port}"
    state.runtime_token = read_env_with_deprecation("DREADNODE_RUNTIME_TOKEN", "SANDBOX_AUTH_TOKEN")
    state.runtime_id = os.environ.get("DREADNODE_RUNTIME_ID")

    # Materialize the token file so its existence signals to the platform that
    # this runtime can be reconnected (token rotated) rather than restarted.
    materialize_runtime_token_file()

    logger.info(f"Starting server at http://{resolved_host}:{resolved_port}")

    uvicorn.run(app, host=resolved_host, port=resolved_port, log_config=None)
