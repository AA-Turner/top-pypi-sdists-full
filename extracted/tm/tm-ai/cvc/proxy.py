"""
cvc.proxy — The Cognitive Proxy (FastAPI Interceptor).

A local middleware service that sits between the agent (e.g., Cursor, VS Code,
or any OpenAI-compatible client) and the upstream LLM provider.  It:

1. Intercepts every request on an OpenAI-compatible API surface.
2. Routes it through the LangGraph state machine to detect CVC commands.
3. For CVC commands: executes the operation and returns the result.
4. For generation: enriches the prompt with committed context, injects
   cache-control headers, and proxies to the upstream provider.
5. Records the assistant response in the context window.
6. Auto-commits at configurable intervals.

Runs on ``http://127.0.0.1:19333`` by default.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from cvc.adapters import BaseAdapter, create_adapter
from cvc.core.database import ContextDatabase
from cvc.core.models import (
    ChatCompletionChoice,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatMessage,
    CVCBranchRequest,
    CVCCommitRequest,
    CVCConfig,
    CVCMergeRequest,
    CVCOperationResponse,
    CVCRestoreRequest,
    UsageInfo,
)
from cvc.operations.engine import CVCEngine
from cvc.operations.state_machine import CVC_TOOLS, CVCGraphState, build_cvc_graph
from cvc.vcs.bridge import VCSBridge

logger = logging.getLogger("cvc.proxy")


# ---------------------------------------------------------------------------
# Time Machine configuration
# ---------------------------------------------------------------------------

# When CVC_TIME_MACHINE=1 (set by ``cvc launch``), auto-commit fires much
# more aggressively — every assistant turn instead of every 3.
# This ensures EVERYTHING is saved to .cvc/ database with zero data loss.
_TIME_MACHINE_ENABLED: bool = os.environ.get("CVC_TIME_MACHINE", "0") == "1"
_TIME_MACHINE_INTERVAL: int = int(os.environ.get("CVC_TIME_MACHINE_INTERVAL", "1"))  # Every turn!
_NORMAL_INTERVAL: int = int(os.environ.get("CVC_AUTO_COMMIT_INTERVAL", "3"))  # Every 3 turns

# Session detection — if no traffic for this many seconds, new session
_SESSION_TIMEOUT: int = int(os.environ.get("CVC_SESSION_TIMEOUT", "1800"))  # 30 min


# ---------------------------------------------------------------------------
# Application state (module-level singletons, initialised in lifespan)
# ---------------------------------------------------------------------------

_config: CVCConfig | None = None
_db: ContextDatabase | None = None
_engine: CVCEngine | None = None
_adapter: BaseAdapter | None = None
_bridge: VCSBridge | None = None
_graph: Any = None  # Compiled LangGraph
_hive: Any = None  # HiveMind SDK instance (Phase 8)


# ---------------------------------------------------------------------------
# Session tracking
# ---------------------------------------------------------------------------

class _SessionTracker:
    """Lightweight tracker for agent sessions going through the proxy."""

    def __init__(self) -> None:
        self.sessions: list[dict[str, Any]] = []
        self._current: dict[str, Any] | None = None
        self._last_request_ts: float = 0.0

    def touch(self, *, tool_hint: str = "") -> dict[str, Any]:
        """
        Called on every inbound request.  Starts a new session if enough
        idle time has elapsed (Time Machine session splitting).
        """
        now = time.time()
        gap = now - self._last_request_ts if self._last_request_ts else 0
        self._last_request_ts = now

        if self._current is None or gap > _SESSION_TIMEOUT:
            # Archive previous session
            if self._current is not None:
                self._current["ended_at"] = now - gap
                self.sessions.append(self._current)

            self._current = {
                "id": len(self.sessions) + 1,
                "started_at": now,
                "ended_at": None,
                "tool": tool_hint or "unknown",
                "messages": 0,
                "commits": 0,
                "branch_at_start": "",
            }

        self._current["messages"] += 1
        if tool_hint and self._current["tool"] == "unknown":
            self._current["tool"] = tool_hint
        return self._current

    @property
    def current(self) -> dict[str, Any] | None:
        return self._current

    def record_commit(self) -> None:
        if self._current:
            self._current["commits"] += 1

    def all_sessions(self) -> list[dict[str, Any]]:
        result = list(self.sessions)
        if self._current:
            result.append({**self._current, "active": True})
        return result


_session_tracker = _SessionTracker()


def _load_config() -> CVCConfig:
    """Build configuration using the unified project discovery + global config system."""
    return CVCConfig.for_project(mode="proxy")


def _auto_restore_context() -> None:
    """
    Auto-restore context on proxy startup.

    As of the engine rewrite, ``CVCEngine.__init__`` now auto-hydrates
    the context window from the HEAD commit blob or persistent cache.
    This function just logs the result for the proxy startup banner.
    """
    global _engine

    if not _engine:
        return

    ctx = _engine.context_window
    if ctx:
        logger.info(
            "Proxy started with %d messages in context (branch: %s)",
            len(ctx),
            _engine.active_branch,
        )
    else:
        logger.info("Proxy started with empty context (branch: %s)", _engine.active_branch)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise all CVC subsystems on startup, tear down on shutdown."""
    global _config, _db, _engine, _adapter, _bridge, _graph

    _config = _load_config()
    _config.ensure_dirs()

    _db = ContextDatabase(_config)
    _engine = CVCEngine(_config, _db)
    
    # Auto-restore last commit or persistent cache on startup
    _auto_restore_context()
    
    _adapter = create_adapter(
        provider=_config.provider,
        api_key=_config.api_key,
        model=_config.model,
        base_url=_config.upstream_base_url,
    )

    # Auth mode — determines whether CVC uses its own key or passes through
    # the client's auth header to the upstream provider.
    app.state.auth_mode = _config.auth_mode if hasattr(_config, 'auth_mode') else 'stored'
    _bridge = VCSBridge(_config, _db)

    # Build and compile the LangGraph state machine
    graph_builder = build_cvc_graph(_engine)
    _graph = graph_builder.compile()

    logger.info(
        "CVC Proxy started — agent=%s branch=%s provider=%s model=%s",
        _config.agent_id,
        _config.default_branch,
        _config.provider,
        _config.model,
    )

    yield

    # Teardown
    if _adapter:
        await _adapter.close()
    if _db:
        _db.close()
    logger.info("CVC Proxy shut down.")


# ---------------------------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------------------------

try:
    from cvc import __version__ as _cvc_version
except ImportError:
    _cvc_version = "1.1.5"

app = FastAPI(
    title="CVC — Cognitive Version Control Proxy",
    description="Git for the AI Mind. Intercepts LLM API calls and manages cognitive state.",
    version=_cvc_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# OpenAI-Compatible Chat Completions Endpoint (The Interceptor)
# ---------------------------------------------------------------------------

@app.post("/v1/chat/completions", response_model=None)
async def chat_completions(raw_request: Request) -> JSONResponse:
    """
    The primary interception point.

    Every request from the agent (Cursor / VS Code / CLI) flows through here.
    The LangGraph state machine decides whether it's a CVC command or a
    standard generation.

    Supports auth pass-through: if the client sends an Authorization header,
    CVC can forward it to the upstream provider.
    """
    assert _engine is not None and _graph is not None and _adapter is not None

    body = await raw_request.json()
    request = ChatCompletionRequest(**body)

    # 1. Run the request through the LangGraph state machine
    initial_state: CVCGraphState = {
        "request": request,
        "is_cvc_command": False,
        "cvc_tool_name": "",
        "cvc_tool_args": {},
        "response": None,
        "cvc_result": None,
        "active_branch": _engine.active_branch,
        "head_hash": _engine.head_hash or "",
        "committed_prefix_len": 0,
    }

    result_state = _graph.invoke(initial_state)

    # 2. If it was a CVC command, return the operation result directly
    if result_state.get("is_cvc_command") and result_state.get("cvc_result"):
        cvc_result: CVCOperationResponse = result_state["cvc_result"]
        # Wrap in a chat-completion envelope so the client can parse it
        wrapped = ChatCompletionResponse(
            model=request.model,
            choices=[
                ChatCompletionChoice(
                    message=ChatMessage(
                        role="assistant",
                        content=json.dumps(cvc_result.model_dump(), indent=2),
                    ),
                    finish_reason="stop",
                )
            ],
        )
        return JSONResponse(
            content=wrapped.model_dump(),
            headers={"X-CVC-Operation": cvc_result.operation},
        )

    # 3. Standard generation — proxy to upstream provider
    committed_prefix_len = result_state.get("committed_prefix_len", 0)

    # 3a. Record NEW inbound messages in the CVC context window.
    #     The OpenAI API sends the full message history on each call,
    #     so we only store messages beyond what we already have.
    existing_count = len(_engine.context_window)
    inbound_count = len(request.messages)
    if inbound_count > existing_count:
        # Only push messages that are new (beyond what CVC already has)
        for msg in request.messages[existing_count:]:
            if msg.role in ("user", "system", "tool"):
                _engine.push_chat_message(msg)

    # 3b. COGNOME injection — compile an Engram and prepend it as a system
    #     message so the upstream LLM has curated workspace context.
    _cognome_engram = None
    try:
        from cvc.operations.cognome_runtime import CognomeRuntime
        runtime = CognomeRuntime.for_engine(_engine)
        if runtime.is_active():
            raw_msgs = [{"role": m.role, "content": m.content or ""} for m in request.messages]
            updated_msgs, _cognome_engram = await runtime.resolve_messages(
                raw_msgs,
                provider=_config.provider,
                model=_config.model,
                branch=request.cvc_branch,
            )
            if _cognome_engram and _cognome_engram.preamble:
                from cvc.core.models import ChatMessage as CM
                request.messages = [CM(**m) for m in updated_msgs]
                committed_prefix_len += 1  # Engram counts as committed prefix
    except Exception as exc:
        logger.warning("COGNOME injection failed (non-fatal): %s", exc)

    try:
        response = await _adapter.complete(
            request, committed_prefix_len=committed_prefix_len
        )
    except Exception as exc:
        logger.error("Upstream provider error: %s", exc)
        raise HTTPException(status_code=502, detail=f"Upstream error: {exc}") from exc

    # 4. Record the assistant response in the context window
    if response.choices:
        assistant_msg = response.choices[0].message
        _engine.push_chat_message(assistant_msg)

        # Log cache performance
        if response.usage.cache_read_tokens > 0:
            logger.info(
                "Cache HIT: %d tokens read from cache (%.1f%% of prompt)",
                response.usage.cache_read_tokens,
                (response.usage.cache_read_tokens / max(response.usage.prompt_tokens, 1)) * 100,
            )

    # 5. Auto-commit if enabled
    if request.cvc_auto_commit and _should_auto_commit():
        auto_msg = _build_auto_commit_message()
        auto_result = _engine.commit(
            CVCCommitRequest(
                message=auto_msg,
                commit_type="checkpoint",
            )
        )
        if auto_result.success:
            _session_tracker.record_commit()
            logger.info("Auto-commit: %s", auto_result.commit_hash and auto_result.commit_hash[:12])

    return JSONResponse(content=response.model_dump())


def _should_auto_commit() -> bool:
    """
    Auto-commit heuristic.

    - **Time Machine mode** (``CVC_TIME_MACHINE=1``): commits every
      ``_TIME_MACHINE_INTERVAL`` assistant turns (default 3).
    - **Normal mode**: commits every ``_NORMAL_INTERVAL`` turns (default 10).
    """
    assert _engine is not None
    assistant_msgs = [m for m in _engine.context_window if m.role == "assistant"]
    count = len(assistant_msgs)
    if count == 0:
        return False
    interval = _TIME_MACHINE_INTERVAL if _TIME_MACHINE_ENABLED else _NORMAL_INTERVAL
    return count % interval == 0


def _build_auto_commit_message() -> str:
    """Generate a concise auto-commit message from recent context."""
    assert _engine is not None
    recent = [m for m in _engine.context_window if m.role in ("user", "assistant")]
    if not recent:
        return "Auto-checkpoint"
    # Use the last user message as summary hint
    last_user = next((m for m in reversed(recent) if m.role == "user"), None)
    if last_user:
        summary = last_user.content[:120].replace("\n", " ").strip()
        return f"Auto: {summary}"
    return f"Auto-checkpoint ({len(recent)} messages)"


# ---------------------------------------------------------------------------
# CVC Control Endpoints (Direct REST — alternative to function-calling)
# ---------------------------------------------------------------------------

@app.post("/cvc/commit", response_model=CVCOperationResponse)
async def cvc_commit_endpoint(request: CVCCommitRequest) -> CVCOperationResponse:
    assert _engine is not None
    result = _engine.commit(request)
    if result.success and result.commit_hash:
        _proxy_emit("commit.created", {
            "commit_hash": result.commit_hash,
            "branch": _engine.active_branch,
            "message": request.message or "",
        })
    return result


@app.post("/cvc/branch", response_model=CVCOperationResponse)
async def cvc_branch_endpoint(request: CVCBranchRequest) -> CVCOperationResponse:
    assert _engine is not None
    result = _engine.branch(request)
    if result.success:
        _proxy_emit("branch.updated", {
            "branch": request.name,
            "commit_hash": result.commit_hash or "",
        })
    return result


@app.post("/cvc/merge", response_model=CVCOperationResponse)
async def cvc_merge_endpoint(request: CVCMergeRequest) -> CVCOperationResponse:
    assert _engine is not None
    result = _engine.merge(request)
    if result.success:
        _proxy_emit("branch.updated", {
            "branch": request.target_branch,
            "commit_hash": result.commit_hash or "",
            "source_branch": request.source_branch,
        })
    return result


@app.post("/cvc/restore", response_model=CVCOperationResponse)
async def cvc_restore_endpoint(request: CVCRestoreRequest) -> CVCOperationResponse:
    assert _engine is not None
    return _engine.restore(request)


@app.get("/cvc/status")
async def cvc_status() -> dict[str, Any]:
    """Current CVC state: active branch, HEAD, branch list."""
    assert _engine is not None and _db is not None
    branches = _db.index.list_branches()
    return {
        "agent_id": _engine.config.agent_id,
        "active_branch": _engine.active_branch,
        "head_hash": _engine.head_hash,
        "context_size": len(_engine.context_window),
        "branches": [
            {
                "name": b.name,
                "head": b.head_hash[:12],
                "status": b.status.value,
            }
            for b in branches
        ],
    }


@app.get("/cvc/log")
async def cvc_log(limit: int = 20) -> dict[str, Any]:
    """Commit log for the active branch."""
    assert _engine is not None
    return {
        "branch": _engine.active_branch,
        "commits": _engine.log(limit=limit),
    }


@app.get("/cvc/search")
async def cvc_search(query: str, n: int = 5, deep: bool = True) -> dict[str, Any]:
    """Deep hybrid search over commits: semantic + message text + content."""
    assert _engine is not None
    results = _engine.recall(query, limit=n, deep=deep)
    return {
        "query": query,
        "vector_search_available": _engine.db.vectors.available,
        "result_count": len(results),
        "results": results,
    }


@app.get("/cvc/recall")
async def cvc_recall(query: str, limit: int = 10, deep: bool = True) -> dict[str, Any]:
    """Natural-language recall — find past conversations by meaning."""
    assert _engine is not None
    results = _engine.recall(query, limit=limit, deep=deep)
    return {
        "query": query,
        "vector_search_available": _engine.db.vectors.available,
        "result_count": len(results),
        "results": results,
    }


@app.get("/cvc/tools")
async def cvc_tools() -> list[dict[str, Any]]:
    """Return CVC tool definitions for function-calling / MCP integration."""
    return CVC_TOOLS


@app.get("/cvc/sessions")
async def cvc_sessions() -> dict[str, Any]:
    """
    Return the session history — every contiguous period of tool-proxy
    interaction.  This powers ``cvc sessions`` and the Time Machine UI.
    """
    sessions = _session_tracker.all_sessions()
    return {
        "time_machine": _TIME_MACHINE_ENABLED,
        "auto_commit_interval": _TIME_MACHINE_INTERVAL if _TIME_MACHINE_ENABLED else _NORMAL_INTERVAL,
        "session_timeout_seconds": _SESSION_TIMEOUT,
        "total": len(sessions),
        "sessions": sessions,
    }


@app.get("/cvc/config")
async def cvc_runtime_config() -> dict[str, Any]:
    """Return the current proxy runtime configuration."""
    return {
        "time_machine": _TIME_MACHINE_ENABLED,
        "auto_commit_interval": _TIME_MACHINE_INTERVAL if _TIME_MACHINE_ENABLED else _NORMAL_INTERVAL,
        "session_timeout_seconds": _SESSION_TIMEOUT,
        "provider": _config.provider if _config else "unknown",
        "model": _config.model if _config else "unknown",
        "agent_id": _config.agent_id if _config else "unknown",
    }


# ---------------------------------------------------------------------------
# VCS Bridge endpoints
# ---------------------------------------------------------------------------

@app.post("/cvc/vcs/capture")
async def vcs_capture(git_sha: str | None = None) -> dict[str, Any]:
    """Capture a CVC snapshot linked to the current Git commit."""
    assert _bridge is not None
    return _bridge.capture_snapshot(git_sha)


@app.post("/cvc/vcs/install-hooks")
async def vcs_install_hooks() -> dict[str, str]:
    """Install Git hooks for CVC synchronisation."""
    assert _bridge is not None
    return _bridge.install_hooks()


# ---------------------------------------------------------------------------
# Hive Mind REST API — Multi-Agent Endpoints (Phase 8)
# ---------------------------------------------------------------------------

def _get_hive():
    """Return the proxy-level HiveMind instance, creating lazily if needed."""
    global _hive
    if _hive is None:
        from cvc.sdk import HiveMind
        if _config is not None:
            cvc_root = _config.cvc_root
            vec = getattr(_config, "vector_enabled", None)
        else:
            # Standalone mode (e.g. TestClient without lifespan)
            cvc_root = Path.cwd() / ".cvc"
            vec = False
        _hive = HiveMind(cvc_root, vector_enabled=vec)
    return _hive


@app.post("/api/v1/agents")
async def api_register_agent(request: Request) -> JSONResponse:
    """Register a new agent in the hive mind.

    Body: ``{"agent_id": "...", "role": "...", "rank": "...", "squad": "...", ...}``
    """
    body = await request.json()
    agent_id = body.get("agent_id")
    if not agent_id:
        raise HTTPException(status_code=400, detail="agent_id is required")

    hive = _get_hive()
    agent = hive.register_agent(
        agent_id,
        name=body.get("name"),
        role=body.get("role"),
        rank=body.get("rank"),
        squad=body.get("squad"),
        capabilities=body.get("capabilities"),
        metadata=body.get("metadata"),
        readable_branches=body.get("readable_branches"),
        writable_branches=body.get("writable_branches"),
        agent_branch=body.get("agent_branch", False),
    )
    return JSONResponse(content={
        "success": True,
        "agent_id": agent.agent_id,
        "profile": agent.profile,
    })


@app.get("/api/v1/agents")
async def api_list_agents(squad: str | None = None, rank: str | None = None) -> JSONResponse:
    """List registered agents, optionally filtered by squad/rank."""
    hive = _get_hive()
    agents = hive.list_agents(squad=squad, rank=rank)
    return JSONResponse(content={"agents": agents, "count": len(agents)})


@app.post("/api/v1/commits")
async def api_create_commit(request: Request) -> JSONResponse:
    """Create a commit as a specific agent.

    Body: ``{"agent_id": "...", "message": "...", "content": {...}, "tags": [...]}``
    """
    body = await request.json()
    agent_id = body.get("agent_id")
    message = body.get("message")
    if not agent_id or not message:
        raise HTTPException(status_code=400, detail="agent_id and message are required")

    hive = _get_hive()
    agent = hive.get_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail=f"Agent not found: {agent_id}")

    commit_hash = agent.commit(
        message,
        content=body.get("content"),
        tags=body.get("tags"),
        target_agent_id=body.get("target_agent_id"),
        action_type=body.get("action_type"),
        branch=body.get("branch"),
        messages=body.get("messages"),
    )
    _proxy_emit("commit.created", {
        "commit_hash": commit_hash,
        "agent_id": agent_id,
        "message": message,
    })
    return JSONResponse(content={
        "success": True,
        "commit_hash": commit_hash,
        "agent_id": agent_id,
    })


@app.get("/api/v1/commits")
async def api_query_commits(
    agent_id: str | None = None,
    squad: str | None = None,
    branch: str | None = None,
    limit: int = 50,
) -> JSONResponse:
    """Query commits filtered by agent, squad, or branch."""
    hive = _get_hive()
    commits = hive.log(branch=branch, agent_id=agent_id, squad=squad, limit=limit)
    return JSONResponse(content={
        "commits": [
            {
                "commit_hash": c.commit_hash,
                "short_hash": c.short_hash,
                "message": c.message,
                "commit_type": c.commit_type.value,
                "timestamp": c.metadata.timestamp,
                "agent_id": c.metadata.agent_id,
                "squad": c.metadata.squad,
                "branch": getattr(c, "branch", None),
            }
            for c in commits
        ],
        "count": len(commits),
    })


@app.post("/api/v1/recall")
async def api_recall(request: Request) -> JSONResponse:
    """Semantic search, optionally scoped to a specific agent.

    Body: ``{"query": "...", "agent_id": "..." (optional), "limit": 5}``
    """
    body = await request.json()
    query = body.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="query is required")

    hive = _get_hive()
    agent_id = body.get("agent_id")
    limit = body.get("limit", 5)

    if agent_id:
        agent = hive.get_agent(agent_id)
        if agent is None:
            raise HTTPException(status_code=404, detail=f"Agent not found: {agent_id}")
        results = agent.recall(query, limit=limit)
    else:
        results = hive.recall(query, limit=limit)

    return JSONResponse(content={
        "query": query,
        "results": [
            {
                "commit_hash": c.commit_hash,
                "short_hash": c.short_hash,
                "message": c.message,
                "commit_type": c.commit_type.value,
                "timestamp": c.metadata.timestamp,
                "agent_id": c.metadata.agent_id,
            }
            for c in results
        ],
        "count": len(results),
    })


@app.get("/api/v1/branches")
async def api_list_branches() -> JSONResponse:
    """List all branches in the hive mind."""
    hive = _get_hive()
    branches = hive.db.index.list_branches()
    return JSONResponse(content={
        "branches": [
            {
                "name": b.name,
                "head_hash": b.head_hash,
                "short_head": b.head_hash[:12],
                "status": b.status.value,
                "created_at": b.created_at,
            }
            for b in branches
        ],
        "count": len(branches),
    })


@app.post("/api/v1/sync")
async def api_sync(request: Request) -> JSONResponse:
    """Push/pull with a remote CVC repository.

    Body: ``{"remote_path": "...", "direction": "push"|"pull", "branch": "..."}``
    """
    body = await request.json()
    remote_path = body.get("remote_path")
    if not remote_path:
        raise HTTPException(status_code=400, detail="remote_path is required")

    direction = body.get("direction", "push")
    branch = body.get("branch")

    assert _engine is not None
    if direction == "push":
        result = _engine.sync_push(remote_path=remote_path, branch=branch)
    elif direction == "pull":
        result = _engine.sync_pull(remote_path=remote_path, branch=branch)
    else:
        raise HTTPException(status_code=400, detail="direction must be 'push' or 'pull'")

    return JSONResponse(content=result.model_dump())


@app.get("/api/v1/status")
async def api_hive_status() -> JSONResponse:
    """Return a summary of the hive mind state."""
    hive = _get_hive()
    return JSONResponse(content=hive.status())


@app.post("/api/v1/compact")
async def api_compact(request: Request) -> JSONResponse:
    """Trigger hive mind compaction.

    Body: ``{"strategy": "summarize", "max_age_hours": 24, "branch": "...", "min_commits": 3}``
    """
    body = await request.json()
    hive = _get_hive()
    result = hive.compact(
        strategy=body.get("strategy", "summarize"),
        max_age_hours=body.get("max_age_hours", 24.0),
        branch=body.get("branch"),
        min_commits=body.get("min_commits", 3),
    )
    return JSONResponse(content={
        "success": True,
        "distilled_commits": result.distilled_commits,
        "anchors_created": result.anchors_created,
        "branches_compacted": result.branches_compacted,
    })


@app.post("/api/v1/merge")
async def api_merge(request: Request) -> JSONResponse:
    """Merge branches, optionally merging all squads.

    Body: ``{"source": "...", "target": "main"}``
    or ``{"squads": true, "target": "main", "strategy": "all"}``
    """
    body = await request.json()
    hive = _get_hive()

    if body.get("squads"):
        merged = hive.merge_squads(
            target=body.get("target", "main"),
            strategy=body.get("strategy", "all"),
        )
        return JSONResponse(content={
            "success": True,
            "merged_hashes": merged,
            "count": len(merged),
        })
    else:
        source = body.get("source")
        if not source:
            raise HTTPException(status_code=400, detail="source is required")
        commit_hash = hive.merge(source, body.get("target", "main"))
        return JSONResponse(content={
            "success": True,
            "commit_hash": commit_hash,
        })


# ---------------------------------------------------------------------------
# Real-Time Event Bus — WebSocket & SSE Endpoints (Phase 5)
# ---------------------------------------------------------------------------

from starlette.websockets import WebSocket, WebSocketDisconnect

# Module-level event bus shared by all proxy endpoints.
# Initialised in lifespan if a HiveMind SDK is attached; otherwise a
# standalone bus is created so the WS/SSE endpoints always work.
_event_bus: Any = None


def _get_event_bus():
    """Return the proxy-level EventBus, creating one lazily if needed."""
    global _event_bus
    if _event_bus is None:
        from cvc.sdk.events import EventBus
        _event_bus = EventBus()
    return _event_bus


def _proxy_emit(event: str, data: dict[str, Any]) -> None:
    """Emit an event on the proxy event bus (called from commit endpoints)."""
    bus = _get_event_bus()
    bus.emit(event, data)


@app.websocket("/ws/events")
async def ws_events(websocket: WebSocket):
    """
    WebSocket endpoint for real-time hive mind event streaming.

    Query params:
        agent_id  — only receive events relevant to this agent
        events    — comma-separated event types to subscribe to
        replay    — if "true", replay recent history on connect

    Messages sent to the client are JSON objects with ``event``,
    ``data``, and ``timestamp`` fields.
    """
    await websocket.accept()

    agent_id = websocket.query_params.get("agent_id")
    events_csv = websocket.query_params.get("events", "")
    replay = websocket.query_params.get("replay", "").lower() == "true"

    event_filter = [e.strip() for e in events_csv.split(",") if e.strip()] or None

    bus = _get_event_bus()
    sub_id = f"ws-{agent_id or 'anon'}-{id(websocket)}"
    sub = bus.subscribe(
        sub_id,
        events=event_filter,
        agent_filter=agent_id,
        replay=replay,
    )

    try:
        # Drain replayed events first
        for env in sub.drain():
            await websocket.send_json({
                "event": env.event,
                "data": env.data,
                "timestamp": env.timestamp,
            })

        # Then stream live events
        while sub.active:
            try:
                envelope = await asyncio.wait_for(sub.get(), timeout=30.0)
                await websocket.send_json({
                    "event": envelope.event,
                    "data": envelope.data,
                    "timestamp": envelope.timestamp,
                })
            except asyncio.TimeoutError:
                # Send keepalive ping
                try:
                    await websocket.send_json({"event": "ping", "data": {}, "timestamp": time.time()})
                except Exception:
                    break
    except WebSocketDisconnect:
        pass
    except Exception:
        logger.exception("WebSocket error for %s", sub_id)
    finally:
        bus.unsubscribe(sub_id)


@app.get("/sse/events")
async def sse_events(request: Request):
    """
    Server-Sent Events endpoint for real-time hive mind event streaming.

    Query params are the same as ``/ws/events``.
    Clients that can't use WebSocket (e.g. curl, browser fetch) use this.
    """
    from starlette.responses import StreamingResponse as _SSEStreamingResponse

    agent_id = request.query_params.get("agent_id")
    events_csv = request.query_params.get("events", "")
    replay = request.query_params.get("replay", "").lower() == "true"

    event_filter = [e.strip() for e in events_csv.split(",") if e.strip()] or None

    bus = _get_event_bus()
    sub_id = f"sse-{agent_id or 'anon'}-{id(request)}"
    sub = bus.subscribe(
        sub_id,
        events=event_filter,
        agent_filter=agent_id,
        replay=replay,
    )

    async def _generate():
        try:
            # Drain replayed events
            for env in sub.drain():
                yield f"event: {env.event}\ndata: {json.dumps({'event': env.event, 'data': env.data, 'timestamp': env.timestamp})}\n\n"

            while sub.active:
                try:
                    envelope = await asyncio.wait_for(sub.get(), timeout=30.0)
                    yield f"event: {envelope.event}\ndata: {json.dumps({'event': envelope.event, 'data': envelope.data, 'timestamp': envelope.timestamp})}\n\n"
                except asyncio.TimeoutError:
                    yield f"event: ping\ndata: {json.dumps({'event': 'ping', 'data': {}, 'timestamp': time.time()})}\n\n"
                except asyncio.CancelledError:
                    break
        finally:
            bus.unsubscribe(sub_id)

    return _SSEStreamingResponse(
        _generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "cvc-proxy", "version": _cvc_version}


@app.post("/cvc/reload-config")
async def reload_config():
    """Reload config from disk (called by gateway when model is switched)."""
    global _config, _adapter
    try:
        _config = _load_config()
        _adapter = create_adapter(
            provider=_config.provider,
            api_key=_config.api_key,
            model=_config.model,
            base_url=_config.upstream_base_url,
        )
        logger.info("Config reloaded — provider=%s model=%s", _config.provider, _config.model)
        return {"status": "ok", "provider": _config.provider, "model": _config.model}
    except Exception as exc:
        logger.error("Config reload error: %s", exc)
        return {"status": "error", "error": str(exc)}


# ---------------------------------------------------------------------------
# Auth Pass-Through Middleware
# ---------------------------------------------------------------------------

@app.middleware("http")
async def auth_passthrough_middleware(request: Request, call_next):
    """
    When auth_mode is 'pass_through', extract the client's Bearer token
    (or x-api-key header) and stash it on request.state so downstream
    handlers can forward it to the upstream provider.

    Also tracks sessions and identifies the connecting tool from
    the User-Agent header (e.g. 'claude-code/1.x', 'aider/0.x').
    """
    # Extract client auth from the incoming request
    auth_header = request.headers.get("authorization", "")
    x_api_key = request.headers.get("x-api-key", "")
    request.state.client_api_key = ""
    request.state.client_bearer = ""

    if x_api_key:
        request.state.client_api_key = x_api_key
    if auth_header.lower().startswith("bearer "):
        request.state.client_bearer = auth_header[7:].strip()

    # Session tracking — detect tool from User-Agent
    ua = request.headers.get("user-agent", "").lower()
    tool_hint = ""
    if "claude" in ua:
        tool_hint = "claude"
    elif "aider" in ua:
        tool_hint = "aider"
    elif "codex" in ua:
        tool_hint = "codex"
    elif "cursor" in ua:
        tool_hint = "cursor"
    elif "copilot" in ua:
        tool_hint = "copilot"
    elif "gemini" in ua:
        tool_hint = "gemini"

    session = _session_tracker.touch(tool_hint=tool_hint)
    if _engine and not session.get("branch_at_start"):
        session["branch_at_start"] = _engine.active_branch

    return await call_next(request)


# ---------------------------------------------------------------------------
# Anthropic Messages API — Native Claude Code CLI Support
# ---------------------------------------------------------------------------

@app.post("/v1/messages")
async def anthropic_messages(request: Request) -> JSONResponse:
    """
    Anthropic-native Messages API endpoint.

    Claude Code CLI sends requests to ANTHROPIC_BASE_URL + '/v1/messages'
    using the Anthropic wire format (not OpenAI). This endpoint:

    1. Accepts the Anthropic Messages API format natively.
    2. Runs CVC interception (command detection, context enrichment).
    3. Forwards to the upstream Anthropic API (or configured provider).
    4. Returns the response in Anthropic Messages format.

    This means users can simply set:
        export ANTHROPIC_BASE_URL=http://127.0.0.1:19333
    and Claude Code CLI works with full CVC cognitive versioning.
    """
    assert _engine is not None and _config is not None

    body = await request.json()

    # --- Convert Anthropic format → internal OpenAI format ---
    messages_in = body.get("messages", [])
    system_text = body.get("system", "")

    # Build OpenAI-style messages list
    openai_messages: list[dict[str, Any]] = []
    if system_text:
        if isinstance(system_text, list):
            # Anthropic system can be a list of content blocks
            sys_parts = [b.get("text", "") for b in system_text if b.get("type") == "text"]
            system_text = "\n".join(sys_parts)
        openai_messages.append({"role": "system", "content": system_text})

    for msg in messages_in:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        # Anthropic content can be string or list of blocks
        if isinstance(content, list):
            text_parts = [b.get("text", "") for b in content if b.get("type") == "text"]
            content = "\n".join(text_parts)
        openai_messages.append({"role": role, "content": content})

    # Build ChatCompletionRequest for the CVC pipeline
    internal_request = ChatCompletionRequest(
        model=body.get("model", _config.model),
        messages=[ChatMessage(**m) for m in openai_messages],
        temperature=body.get("temperature", 0.7),
        max_tokens=body.get("max_tokens", 4096),
    )

    # Convert tools if present
    anthropic_tools = body.get("tools", [])
    if anthropic_tools:
        # Convert Anthropic tool format → OpenAI tool format for CVC pipeline
        openai_tools = []
        for t in anthropic_tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": t.get("name", ""),
                    "description": t.get("description", ""),
                    "parameters": t.get("input_schema", {}),
                },
            })
        internal_request.tools = openai_tools

    # --- Run through CVC state machine (same as /v1/chat/completions) ---
    assert _graph is not None

    # Record inbound user messages in CVC context (Anthropic native endpoint)
    existing_count = len(_engine.context_window)
    for msg in internal_request.messages[existing_count:]:
        if msg.role in ("user", "system", "tool"):
            _engine.push_chat_message(msg)

    initial_state: CVCGraphState = {
        "request": internal_request,
        "is_cvc_command": False,
        "cvc_tool_name": "",
        "cvc_tool_args": {},
        "response": None,
        "cvc_result": None,
        "active_branch": _engine.active_branch,
        "head_hash": _engine.head_hash or "",
        "committed_prefix_len": 0,
    }
    result_state = _graph.invoke(initial_state)

    # If CVC command, wrap result in Anthropic format
    if result_state.get("is_cvc_command") and result_state.get("cvc_result"):
        cvc_result: CVCOperationResponse = result_state["cvc_result"]
        return JSONResponse(content={
            "id": f"msg_cvc_{int(time.time())}",
            "type": "message",
            "role": "assistant",
            "model": internal_request.model,
            "content": [{
                "type": "text",
                "text": json.dumps(cvc_result.model_dump(), indent=2),
            }],
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 0, "output_tokens": 0},
        }, headers={"X-CVC-Operation": cvc_result.operation})

    # --- Forward to upstream Anthropic API ---
    # Use client's API key if available (pass-through), else use stored key
    client_api_key = getattr(request.state, 'client_api_key', '') or \
                     getattr(request.state, 'client_bearer', '')
    upstream_key = client_api_key or _config.api_key

    if not upstream_key:
        raise HTTPException(
            status_code=401,
            detail="No API key available. Either pass x-api-key / Authorization header, "
                   "or configure an API key via 'cvc setup'.",
        )

    import httpx
    headers = {
        "x-api-key": upstream_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    # Forward anthropic-beta if present
    beta = request.headers.get("anthropic-beta")
    if beta:
        headers["anthropic-beta"] = beta

    # Build the upstream body — pass through most fields as-is
    upstream_body = dict(body)
    
    # --- Inject Prompt Caching ---
    _breakpoints = 0
    if "system" in upstream_body and upstream_body["system"]:
        if isinstance(upstream_body["system"], str):
            upstream_body["system"] = [{"type": "text", "text": upstream_body["system"]}]
        if isinstance(upstream_body["system"], list) and len(upstream_body["system"]) > 0:
            upstream_body["system"][-1]["cache_control"] = {"type": "ephemeral"}
            _breakpoints += 1

    if "messages" in upstream_body and isinstance(upstream_body["messages"], list) and len(upstream_body["messages"]) > 0:
        if _breakpoints < 4:
            last_msg = upstream_body["messages"][-1]
            if "content" in last_msg:
                if isinstance(last_msg["content"], str):
                    last_msg["content"] = [{"type": "text", "text": last_msg["content"]}]
                if isinstance(last_msg["content"], list) and len(last_msg["content"]) > 0:
                    last_msg["content"][-1]["cache_control"] = {"type": "ephemeral"}
                    _breakpoints += 1
    # -----------------------------

    # Inject CVC context enrichment
    committed_prefix_len = result_state.get("committed_prefix_len", 0)

    try:
        upstream_url = _config.upstream_base_url.rstrip("/")
        if _config.provider == "anthropic":
            upstream_url = "https://api.anthropic.com"

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                f"{upstream_url}/v1/messages",
                json=upstream_body,
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        logger.error("Upstream Anthropic error: %s", exc)
        raise HTTPException(status_code=502, detail=f"Upstream error: {exc}") from exc

    # Record assistant response in CVC context
    content_blocks = data.get("content", [])
    text_parts = [b["text"] for b in content_blocks if b.get("type") == "text"]
    if text_parts:
        _engine.push_chat_message(ChatMessage(role="assistant", content="\n".join(text_parts)))

    # 5. Auto-commit if enabled
    if _should_auto_commit():
        auto_msg = _build_auto_commit_message()
        auto_result = _engine.commit(
            CVCCommitRequest(
                message=auto_msg,
                commit_type="checkpoint",
            )
        )
        if auto_result.success:
            _session_tracker.record_commit()

    return JSONResponse(content=data)


# ---------------------------------------------------------------------------
# OpenAI-Compatible Model Discovery
# ---------------------------------------------------------------------------

@app.get("/v1/models")
async def list_models() -> dict[str, Any]:
    """
    OpenAI-compatible model listing endpoint.

    Tools like Cursor, Cline, Continue.dev, and Open WebUI query this
    endpoint to auto-discover available models.  We return the model
    configured in the CVC proxy.
    """
    assert _config is not None
    model_id = _config.model
    return {
        "object": "list",
        "data": [
            {
                "id": model_id,
                "object": "model",
                "created": int(time.time()),
                "owned_by": f"cvc-proxy ({_config.provider})",
                "permission": [],
            }
        ],
    }
