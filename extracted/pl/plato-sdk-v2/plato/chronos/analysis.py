"""Client-side session analysis for Chronos OTel spans."""

from __future__ import annotations

import asyncio
import json
import time
from collections import defaultdict
from collections.abc import Callable
from typing import Any

import httpx
from pydantic import BaseModel, ConfigDict, Field, computed_field

from plato.chronos.api.sessions import stream_session_logs
from plato.chronos.models import OTelSpanSchema as OTelSpan

# ---------------------------------------------------------------------------
# Span tree
# ---------------------------------------------------------------------------


class SpanNode(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    span: OTelSpan
    children: list[SpanNode] = []
    parent_span_id: str | None = None

    @computed_field
    @property
    def duration_ms(self) -> float | None:
        if self.span.end_time_unix_nano is None:
            return None
        return (self.span.end_time_unix_nano - self.span.start_time_unix_nano) / 1e6

    @computed_field
    @property
    def name(self) -> str:
        return self.span.name

    def get_attr(self, key: str, default: Any = None) -> Any:
        attrs = self.span.attributes or {}
        return attrs.get(key, default)


class SpanTree(BaseModel):
    roots: list[SpanNode] = []
    orphan_roots: list[SpanNode] = []
    by_id: dict[str, SpanNode] = Field(default_factory=dict, exclude=True)


def build_span_tree(spans: list[OTelSpan]) -> SpanTree:
    by_id: dict[str, SpanNode] = {}
    for s in spans:
        by_id[s.span_id] = SpanNode(span=s, parent_span_id=s.parent_span_id)

    roots: list[SpanNode] = []
    orphan_roots: list[SpanNode] = []

    for node in by_id.values():
        if node.parent_span_id is None:
            roots.append(node)
        elif node.parent_span_id in by_id:
            by_id[node.parent_span_id].children.append(node)
        else:
            orphan_roots.append(node)

    return SpanTree(roots=roots, orphan_roots=orphan_roots, by_id=by_id)


# ---------------------------------------------------------------------------
# Auto-paginated fetch (via the logs-stream endpoint)
# ---------------------------------------------------------------------------
#
# Spans are fetched by draining the `/api/sessions/{id}/logs-stream` NDJSON
# endpoint — the same source the session-viewer uses. The backend walks its
# own log pages server-side and emits a `chunk` event per page (each carrying
# a batch of spans) then a final `complete`. This streams the *entire* session
# in one request, unlike the legacy `/api/otel/.../traces` cursor pagination
# which capped out and silently dropped spans on large sessions.

_STREAM_PAGE_LIMIT = 10000
_STREAM_MAX_RETRIES = 3
_STREAM_RETRY_BASE_DELAY_S = 1.0

# (fetched_span_count, page_count) -> None
ProgressCallback = Callable[[int, int], None]


def stream_all_spans(
    client: httpx.Client,
    session_id: str,
    *,
    search: str | None = None,
    errors_only: bool = False,
    atif_only: bool = False,
    on_progress: ProgressCallback | None = None,
) -> list[OTelSpan]:
    """Fetch ALL spans for a session by draining the logs-stream endpoint.

    Dedupes by ``span_id`` and resumes from the last cursor on a mid-stream
    drop (network blip or backend ``error`` event), so retries never duplicate
    or re-fetch already-streamed spans. ``on_progress`` is called after each
    chunk with the running span count and page count.
    """
    spans: list[OTelSpan] = []
    seen: set[str] = set()
    cursor: str | None = None
    page_count = 0
    attempt = 0

    while True:
        completed = False
        try:
            for event in stream_session_logs.sync_stream(
                client,
                public_id=session_id,
                limit=_STREAM_PAGE_LIMIT,
                cursor=cursor,
                search=search,
                errors_only=errors_only,
                atif_only=atif_only,
            ):
                if event.get("cursor"):
                    cursor = event["cursor"]
                kind = event.get("kind")
                if kind == "error":
                    raise RuntimeError(event.get("error") or "Log stream failed")
                if kind == "complete":
                    completed = True
                    break
                for raw in event.get("logs") or []:
                    span = OTelSpan.model_validate(raw)
                    if span.span_id not in seen:
                        seen.add(span.span_id)
                        spans.append(span)
                page_count += 1
                if on_progress is not None:
                    on_progress(len(spans), page_count)

            # `complete` is the only signal the session fully streamed. A loop
            # that ends without it means a truncated body or quiet disconnect —
            # resume from the cursor rather than returning a partial span set.
            if not completed:
                raise RuntimeError("Log stream ended before completion")
            return spans
        except (httpx.HTTPError, RuntimeError):
            attempt += 1
            if attempt > _STREAM_MAX_RETRIES:
                raise
            time.sleep(_STREAM_RETRY_BASE_DELAY_S * attempt)


async def stream_all_spans_async(
    client: httpx.AsyncClient,
    session_id: str,
    *,
    search: str | None = None,
    errors_only: bool = False,
    atif_only: bool = False,
    on_progress: ProgressCallback | None = None,
) -> list[OTelSpan]:
    """Async counterpart of :func:`stream_all_spans`."""
    spans: list[OTelSpan] = []
    seen: set[str] = set()
    cursor: str | None = None
    page_count = 0
    attempt = 0

    while True:
        completed = False
        try:
            async for event in stream_session_logs.asyncio_stream(
                client,
                public_id=session_id,
                limit=_STREAM_PAGE_LIMIT,
                cursor=cursor,
                search=search,
                errors_only=errors_only,
                atif_only=atif_only,
            ):
                if event.get("cursor"):
                    cursor = event["cursor"]
                kind = event.get("kind")
                if kind == "error":
                    raise RuntimeError(event.get("error") or "Log stream failed")
                if kind == "complete":
                    completed = True
                    break
                for raw in event.get("logs") or []:
                    span = OTelSpan.model_validate(raw)
                    if span.span_id not in seen:
                        seen.add(span.span_id)
                        spans.append(span)
                page_count += 1
                if on_progress is not None:
                    on_progress(len(spans), page_count)

            if not completed:
                raise RuntimeError("Log stream ended before completion")
            return spans
        except (httpx.HTTPError, RuntimeError):
            attempt += 1
            if attempt > _STREAM_MAX_RETRIES:
                raise
            await asyncio.sleep(_STREAM_RETRY_BASE_DELAY_S * attempt)


def fetch_all_spans(client: httpx.Client, session_id: str) -> list[OTelSpan]:
    """Auto-paginated: fetches ALL spans for a session via logs-stream."""
    return stream_all_spans(client, session_id)


async def fetch_all_spans_async(client: httpx.AsyncClient, session_id: str) -> list[OTelSpan]:
    """Auto-paginated: fetches ALL spans for a session via logs-stream."""
    return await stream_all_spans_async(client, session_id)


# ---------------------------------------------------------------------------
# Summary models
# ---------------------------------------------------------------------------


class TokenSummary(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    cost_usd: float = 0.0


class AgentStepInfo(BaseModel):
    step_id: int = 0
    source: str = ""
    model_name: str | None = None
    message_preview: str = ""
    tool_names: list[str] = []
    mcp_tool_names: list[str] = []
    mcp_servers: list[str] = []
    prompt_tokens: int = 0
    completion_tokens: int = 0


class AgentExecution(BaseModel):
    execution_index: int = 0
    agent_name: str | None = None
    root_span_id: str | None = None
    steps: list[AgentStepInfo] = []
    models_used: list[str] = []
    token_summary: TokenSummary = TokenSummary()
    tool_usage: dict[str, int] = {}
    mcp_tool_usage: dict[str, int] = {}
    mcp_server_usage: dict[str, int] = {}
    duration_ms: float | None = None
    step_count: int = 0
    is_orphaned: bool = False


class PhaseInfo(BaseModel):
    name: str
    offset_ms: float = 0.0
    duration_ms: float = 0.0


class SessionAnalysis(BaseModel):
    session_id: str
    total_spans: int = 0
    total_duration_ms: float | None = None
    orphan_span_count: int = 0
    phases: list[PhaseInfo] = []
    agent_executions: list[AgentExecution] = []
    token_summary: TokenSummary = TokenSummary()
    tool_usage: dict[str, int] = {}
    mcp_tool_usage: dict[str, int] = {}
    mcp_server_usage: dict[str, int] = {}


# ---------------------------------------------------------------------------
# Step parsing helpers
# ---------------------------------------------------------------------------

_STRUCTURAL_PREFIXES = ("reset", "ad_loop", "transition_analysis", "ingest", "annotate", "improve", "analyze")


def _parse_step_info(node: SpanNode) -> AgentStepInfo:
    attrs = node.span.attributes or {}
    tool_names: list[str] = []
    mcp_tool_names: list[str] = []
    mcp_servers: list[str] = []
    raw_tools = attrs.get("atif.step.tool_calls")
    if raw_tools:
        try:
            calls = json.loads(raw_tools) if isinstance(raw_tools, str) else raw_tools
            if isinstance(calls, list):
                for tc in calls:
                    if not isinstance(tc, dict):
                        continue
                    name = (
                        tc.get("function_name")
                        or tc.get("name")
                        or (tc["function"].get("name") if isinstance(tc.get("function"), dict) else None)
                    )
                    if name:
                        tool_names.append(name)
                        if tc.get("origin") == "mcp":
                            mcp_tool_names.append(name)
                            server = tc.get("mcp_server")
                            if isinstance(server, str) and server:
                                mcp_servers.append(server)
        except (json.JSONDecodeError, TypeError):
            pass

    message = str(attrs.get("atif.step.message", ""))[:200]
    return AgentStepInfo(
        step_id=int(attrs.get("atif.step.id", 0)),
        source=str(attrs.get("atif.step.source", "")),
        model_name=attrs.get("atif.step.model_name"),
        message_preview=message,
        tool_names=tool_names,
        mcp_tool_names=mcp_tool_names,
        mcp_servers=mcp_servers,
        prompt_tokens=int(attrs.get("atif.step.prompt_tokens", 0)),
        completion_tokens=int(attrs.get("atif.step.completion_tokens", 0)),
    )


def _collect_descendant_steps(node: SpanNode) -> list[SpanNode]:
    """BFS to collect all descendant atif.step.* spans."""
    result: list[SpanNode] = []
    queue = list(node.children)
    while queue:
        child = queue.pop(0)
        if child.span.name.startswith("atif.step."):
            result.append(child)
        queue.extend(child.children)
    return result


# ---------------------------------------------------------------------------
# Core analysis
# ---------------------------------------------------------------------------


def analyze_session(spans: list[OTelSpan], session_id: str) -> SessionAnalysis:
    if not spans:
        return SessionAnalysis(session_id=session_id)

    tree = build_span_tree(spans)

    # Session timing
    min_start = min(s.start_time_unix_nano for s in spans)
    max_end_candidates = [s.end_time_unix_nano for s in spans if s.end_time_unix_nano is not None]
    max_end = max(max_end_candidates) if max_end_candidates else None
    total_duration_ms = (max_end - min_start) / 1e6 if max_end is not None else None

    # Phase detection: structural root/near-root spans
    phases: list[PhaseInfo] = []
    for node in tree.roots + tree.orphan_roots:
        name = node.span.name
        if name.startswith("atif.step.") or name.startswith("log."):
            continue
        if any(name.startswith(p) or name == p for p in _STRUCTURAL_PREFIXES) or (
            not name.startswith("atif.") and not name.startswith("agent.")
        ):
            dur = node.duration_ms or 0.0
            offset = (node.span.start_time_unix_nano - min_start) / 1e6
            phases.append(PhaseInfo(name=name, offset_ms=offset, duration_ms=dur))
    phases.sort(key=lambda p: p.offset_ms)

    # Agent execution grouping
    claimed_span_ids: set[str] = set()
    executions: list[AgentExecution] = []

    # Strategy 1: agent.execution.output spans
    for sid, node in tree.by_id.items():
        if node.span.name == "agent.execution.output":
            step_nodes = _collect_descendant_steps(node)
            claimed_span_ids.add(sid)
            for sn in step_nodes:
                claimed_span_ids.add(sn.span.span_id)
            agent_name = node.get_attr("atif.agent.name")
            exec_info = _build_execution(node, step_nodes, agent_name, is_orphaned=False)
            executions.append(exec_info)

    # Strategy 2: spans with atif.agent.name not yet claimed
    # Skip spans whose parent is already claimed (e.g. "session" spans nested
    # under "agent.execution.output" — their steps were already collected).
    for sid, node in tree.by_id.items():
        if sid in claimed_span_ids:
            continue
        if node.parent_span_id and node.parent_span_id in claimed_span_ids:
            continue
        if node.get_attr("atif.agent.name") and node.span.name != "agent.execution.output":
            step_nodes = [sn for sn in _collect_descendant_steps(node) if sn.span.span_id not in claimed_span_ids]
            claimed_span_ids.add(sid)
            for sn in step_nodes:
                claimed_span_ids.add(sn.span.span_id)
            exec_info = _build_execution(node, step_nodes, node.get_attr("atif.agent.name"), is_orphaned=False)
            executions.append(exec_info)

    # Strategy 3: unclaimed atif.step.* spans grouped by shared parent_span_id
    orphan_groups: dict[str | None, list[SpanNode]] = defaultdict(list)
    for sid, node in tree.by_id.items():
        if sid in claimed_span_ids:
            continue
        if node.span.name.startswith("atif.step."):
            orphan_groups[node.parent_span_id].append(node)
            claimed_span_ids.add(sid)

    for parent_id, step_nodes in orphan_groups.items():
        step_nodes.sort(key=lambda n: n.span.start_time_unix_nano)
        exec_info = _build_execution(None, step_nodes, None, is_orphaned=True)
        exec_info.root_span_id = parent_id
        executions.append(exec_info)

    # Sort by start time and assign indices
    executions.sort(key=lambda e: _execution_start(e, tree))
    for i, ex in enumerate(executions):
        ex.execution_index = i

    # Aggregate tokens/tools across all executions
    global_tokens = TokenSummary()
    global_tools: dict[str, int] = defaultdict(int)
    global_mcp_tools: dict[str, int] = defaultdict(int)
    global_mcp_servers: dict[str, int] = defaultdict(int)
    for ex in executions:
        global_tokens.prompt_tokens += ex.token_summary.prompt_tokens
        global_tokens.completion_tokens += ex.token_summary.completion_tokens
        global_tokens.cache_read_tokens += ex.token_summary.cache_read_tokens
        global_tokens.cache_write_tokens += ex.token_summary.cache_write_tokens
        global_tokens.cost_usd += ex.token_summary.cost_usd
        for tool, count in ex.tool_usage.items():
            global_tools[tool] += count
        for tool, count in ex.mcp_tool_usage.items():
            global_mcp_tools[tool] += count
        for server, count in ex.mcp_server_usage.items():
            global_mcp_servers[server] += count

    return SessionAnalysis(
        session_id=session_id,
        total_spans=len(spans),
        total_duration_ms=total_duration_ms,
        orphan_span_count=len(tree.orphan_roots),
        phases=phases,
        agent_executions=executions,
        token_summary=global_tokens,
        tool_usage=dict(global_tools),
        mcp_tool_usage=dict(global_mcp_tools),
        mcp_server_usage=dict(global_mcp_servers),
    )


def _execution_start(ex: AgentExecution, tree: SpanTree) -> int:
    if ex.root_span_id and ex.root_span_id in tree.by_id:
        return tree.by_id[ex.root_span_id].span.start_time_unix_nano
    if ex.steps:
        return 0  # fallback
    return 0


def _build_execution(
    root_node: SpanNode | None,
    step_nodes: list[SpanNode],
    agent_name: str | None,
    is_orphaned: bool,
) -> AgentExecution:
    steps: list[AgentStepInfo] = []
    models: set[str] = set()
    tool_usage: dict[str, int] = defaultdict(int)
    mcp_tool_usage: dict[str, int] = defaultdict(int)
    mcp_server_usage: dict[str, int] = defaultdict(int)
    total_prompt = 0
    total_completion = 0
    total_cost = 0.0

    for sn in step_nodes:
        info = _parse_step_info(sn)
        steps.append(info)
        if info.model_name:
            models.add(info.model_name)
        for tool in info.tool_names:
            tool_usage[tool] += 1
        for tool in info.mcp_tool_names:
            mcp_tool_usage[tool] += 1
        for server in info.mcp_servers:
            mcp_server_usage[server] += 1
        total_prompt += info.prompt_tokens
        total_completion += info.completion_tokens
        total_cost += float(sn.get_attr("atif.step.cost_usd", 0) or 0)

    # Try to get cost/tokens from the root node or its immediate children
    # (e.g. "session" spans carry cost data but live under "agent.execution.output")
    cache_read = 0
    cache_write = 0
    cost_node = None
    if root_node:
        if root_node.get_attr("atif.agent.cost_usd"):
            cost_node = root_node
        else:
            for child in root_node.children:
                if child.get_attr("atif.agent.cost_usd"):
                    cost_node = child
                    break
    if cost_node:
        total_cost = float(cost_node.get_attr("atif.agent.cost_usd", 0))
        root_prompt = cost_node.get_attr("atif.agent.prompt_tokens")
        root_completion = cost_node.get_attr("atif.agent.completion_tokens")
        if root_prompt is not None:
            total_prompt = int(root_prompt)
        if root_completion is not None:
            total_completion = int(root_completion)
        cache_read = int(cost_node.get_attr("atif.agent.cache_read_tokens", 0))
        cache_write = int(cost_node.get_attr("atif.agent.cache_write_tokens", 0))
        if not agent_name:
            agent_name = cost_node.get_attr("atif.agent.name")

    duration = root_node.duration_ms if root_node else None
    if duration is None and step_nodes:
        first_start = min(sn.span.start_time_unix_nano for sn in step_nodes)
        last_ends = [sn.span.end_time_unix_nano for sn in step_nodes if sn.span.end_time_unix_nano]
        if last_ends:
            duration = (max(last_ends) - first_start) / 1e6

    steps.sort(key=lambda s: s.step_id)

    return AgentExecution(
        agent_name=agent_name,
        root_span_id=root_node.span.span_id if root_node else None,
        steps=steps,
        models_used=sorted(models),
        token_summary=TokenSummary(
            prompt_tokens=total_prompt,
            completion_tokens=total_completion,
            cache_read_tokens=cache_read,
            cache_write_tokens=cache_write,
            cost_usd=total_cost,
        ),
        tool_usage=dict(tool_usage),
        mcp_tool_usage=dict(mcp_tool_usage),
        mcp_server_usage=dict(mcp_server_usage),
        duration_ms=duration,
        step_count=len(steps),
        is_orphaned=is_orphaned,
    )
