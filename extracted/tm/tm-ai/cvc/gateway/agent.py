"""
AIAgent factory — the single source of truth for agent construction in CVC.

Replaces:
- cvc/gateway_chat.py:284-292 (broken bare AIAgent() with no toolsets)
- cvc/hermes_unified.py:start_api_server_background (aiohttp sidecar on :8642)

Pattern lifted from cvc/agent/_vendor/hermes/gateway/platforms/api_server.py
(APIServerAdapter._create_agent, lines 955-1024) — proven production path.
"""

from __future__ import annotations

import logging
import os
import threading
from typing import Any, Callable, Optional

logger = logging.getLogger("cvc.gateway.agent")

# Module-level state — one runtime per worker process.
_agent_state: dict[str, Any] = {
    "session_db": None,
    "config": None,
    "model": None,
    "provider": None,
    "api_key": None,
    "base_url": None,
    "toolsets": [],
    "lock": threading.Lock(),
    # Cached AIAgent — built once per worker, reused across WS requests.
    # Saves ~1.8s of constructor time per request (tool schema generation,
    # registry load, session DB hydration). The session_id is mutable on
    # the AIAgent, so we patch it per request.
    "agent": None,
    "agent_session_id": None,
    "agent_signature": None,  # hash of (model, provider, base_url, api_key, toolsets)
}


async def init_runtime() -> None:
    """Load config, set up session DB, resolve model + provider.

    v3.3.16 — Mirror the vendored upstream pattern from
    ``cvc/agent/_vendor/hermes/hermes_cli/oneshot.py:169-171``,
    which sets ``HERMES_YOLO_MODE=1`` for non-interactive runs
    so the agent doesn't block on per-call approval prompts.

    v3.3.21 — Inject dashboard-appropriate defaults for
    ``tool_loop_guardrails``. The vendored runtime defaults to
    ``hard_stop_enabled: false`` because the upstream CLI is
    interactive (a human can break a loop with Ctrl-C). The CVC
    dashboard is non-interactive: the user has walked away and
    waits for a complete answer. A runaway loop (the same tool
    called 12+ times with identical args, same result) MUST be
    auto-stopped, not just warned about — otherwise the user sees
    the activity dropdown fill with identical cards for ~1 minute
    while the model ignores the warning guidance.

    User overrides in ``~/.cvc/config.yaml`` still win — we only
    fill in defaults when the section is missing.

    v3.3.22 — REMOVED the ``HERMES_YOLO_MODE=1`` setdefault that
    used to live here. That env var forced the vendored runtime to
    skip its approval gate entirely, which is what caused the
    dashboard to never show the "Allow / Deny" approval card even
    when the user had flipped the ApprovalModeSwitcher pill to
    "Default". The gate now lives in ``cvc/gateway/chat.py``
    (``_ApprovalGate``) and is consulted inline before each tool
    runs. The legacy mode tracker (``cvc.gateway_legacy._approval_mode``)
    is the single source of truth, shared with the dashboard's
    ApprovalModeSwitcher pill.
    """
    # v3.3.22 — DO NOT set HERMES_YOLO_MODE here. The dashboard's
    # approval gate lives in cvc/gateway/chat.py and consults
    # cvc.gateway_legacy._approval_mode. Forcing yolo bypassed the
    # gate even when the user had explicitly selected "Default" in
    # the ApprovalModeSwitcher pill. Respect any explicit env var
    # the user set (e.g. HERMES_YOLO_MODE=0 for paranoid mode).

    from cvc.gateway.config_bridge import load_runtime_config

    cfg = load_runtime_config()

    # v3.3.21 — Inject dashboard-appropriate tool_loop_guardrails defaults.
    # The dashboard is non-interactive, so hard stops MUST be on by default
    # (otherwise the agent can burn its entire budget calling read_file
    # with the same args on the same path). Tightened thresholds vs the
    # upstream CLI defaults because there's no human to break the loop.
    #
    # Schema (post-vendor-sync): flat field names on ToolCallGuardrailConfig.
    #   warnings_enabled / hard_stop_enabled  (booleans)
    #   exact_failure_warn_after / exact_failure_block_after
    #   same_tool_failure_warn_after / same_tool_failure_halt_after
    #   no_progress_warn_after / no_progress_block_after
    #
    # A user who wants CLI-like permissive defaults can override in
    # ~/.cvc/config.yaml — we only fill in missing keys.
    cfg.setdefault("tool_loop_guardrails", {})
    tlg = cfg["tool_loop_guardrails"]
    tlg.setdefault("warnings_enabled", True)
    tlg.setdefault("hard_stop_enabled", True)              # <-- the fix
    tlg.setdefault("exact_failure_warn_after", 2)
    tlg.setdefault("exact_failure_block_after", 4)         # was 5
    tlg.setdefault("same_tool_failure_warn_after", 3)
    tlg.setdefault("same_tool_failure_halt_after", 6)      # was 8
    tlg.setdefault("no_progress_warn_after", 2)
    tlg.setdefault("no_progress_block_after", 3)          # was 5 — the dashboard fix

    _agent_state["config"] = cfg
    _agent_state["model"] = cfg.get("model")
    _agent_state["provider"] = cfg.get("provider")
    _agent_state["api_key"] = cfg.get("api_key")
    _agent_state["base_url"] = cfg.get("base_url")
    _agent_state["toolsets"] = cfg.get("toolsets", [])

    # Lazy session DB
    try:
        from cvc.agent._vendor.hermes.hermes_state import SessionDB
        _agent_state["session_db"] = SessionDB()
    except Exception as e:
        logger.debug("SessionDB unavailable: %s", e)

    logger.info(
        "AIAgent runtime ready: provider=%s model=%s toolsets=%d",
        _agent_state["provider"],
        _agent_state["model"],
        len(_agent_state["toolsets"]),
    )


async def shutdown_runtime() -> None:
    """Clean up runtime state."""
    _agent_state["session_db"] = None
    _agent_state["config"] = None
    logger.info("AIAgent runtime shut down.")


def get_session_db():
    return _agent_state.get("session_db")


def get_config() -> dict:
    return _agent_state.get("config") or {}


def create_agent(
    *,
    session_id: Optional[str] = None,
    workspace_path: Optional[str] = None,
    ephemeral_system_prompt: Optional[str] = None,
    stream_delta_callback: Optional[Callable] = None,
    tool_progress_callback: Optional[Callable] = None,
    tool_start_callback: Optional[Callable] = None,
    tool_complete_callback: Optional[Callable] = None,
) -> Any:
    """Build an AIAgent with the right provider/model/toolsets/callbacks.

    Mirrors `APIServerAdapter._create_agent` from the vendored runtime —
    that's the production-tested path.

    **Caching:** the AIAgent is heavy to build (~1.8s for the 12-tool schema
    generation + registry hydration). We cache one AIAgent per worker process
    and re-use it across requests. Cache is invalidated when model, provider,
    base_url, api_key, or toolsets change. The session_id is patched onto the
    cached agent before returning.
    """
    from cvc.agent._vendor.hermes.run_agent import AIAgent
    from cvc.agent._vendor.hermes.gateway.run import (
        _resolve_runtime_agent_kwargs,
        _resolve_gateway_model,
        GatewayRunner,
    )
    from cvc.agent._vendor.hermes.hermes_cli.tools_config import _get_platform_tools

    with _agent_state["lock"]:
        runtime_kwargs = _resolve_runtime_agent_kwargs()
        # Override with CVC's resolved values if the runtime provider failed
        if not runtime_kwargs.get("api_key") and _agent_state.get("api_key"):
            runtime_kwargs["api_key"] = _agent_state["api_key"]
        if not runtime_kwargs.get("base_url") and _agent_state.get("base_url"):
            runtime_kwargs["base_url"] = _agent_state["base_url"]
        if not runtime_kwargs.get("provider") and _agent_state.get("provider"):
            runtime_kwargs["provider"] = _agent_state["provider"]

        try:
            model = _resolve_gateway_model(_agent_state["config"])
        except Exception:
            model = _agent_state.get("model") or runtime_kwargs.get("model", "gpt-4")

        cfg = _agent_state.get("config") or {}
        # v3.3.16 — Register ``cvc-dashboard`` as a first-class
        # platform in platforms.py with default toolset ``hermes-cli``
        # (the same toolset upstream CLI users get — 50+ core tools:
        # web, terminal, file, vision, image_gen, skills, browser,
        # session_search, delegate_task, cronjob, send_message,
        # kanban, plus all opt-in toolsets).
        #
        # Previously the gateway called _get_platform_tools with
        # ``"api_server"`` which resolved to ``hermes-api-server`` —
        # a NARROWER subset (35 tools, no kanban, no image_generate,
        # no send_message, no homeassistant). This was the root
        # cause of "the cvc agent is missing tools" reports.
        #
        # ``hermes-api-server`` is now the FINAL fallback only — used
        # when the user has explicitly configured a narrower set
        # via ``platform_toolsets.api_server`` in ~/.cvc/config.yaml.
        # The user can ALSO override ``cvc-dashboard`` directly via
        # ``platform_toolsets.cvc-dashboard`` if they want a curated
        # set (e.g. ``[search]`` for read-only mode).
        #
        # CVC is now runtime-independent: the user does NOT need a
        # separate upstream install to get the full tool surface. The
        # vendored toolsets module ships with CVC and resolves
        # identically whether or not ``cvc`` is on $PATH.
        enabled_toolsets = sorted(_get_platform_tools(cfg, "cvc-dashboard"))
        if not enabled_toolsets:
            enabled_toolsets = sorted(_get_platform_tools(cfg, "api_server"))
        if not enabled_toolsets:
            enabled_toolsets = ["hermes-cli"]  # ultimate safety net

        try:
            reasoning_config = GatewayRunner._load_reasoning_config()
        except Exception:
            reasoning_config = None
        try:
            fallback_model = GatewayRunner._load_fallback_model()
        except Exception:
            fallback_model = None

        # Build the workspace-aware system prompt
        from cvc.gateway.context import build_system_prompt
        system_prompt = build_system_prompt(
            workspace_path=workspace_path,
            extra=ephemeral_system_prompt,
        )

        max_iterations = int(os.getenv("HERMES_MAX_ITERATIONS", "15"))

        # Cache key — changes when any model/provider/base_url/api_key/toolsets
        # OR the workspace path (which changes the system prompt) differs.
        # We keep a small LRU of 4 (workspace, session) -> AIAgent so a user
        # who switches between 2-3 workspaces doesn't pay the ~1.8s build
        # cost on every switch.
        sig = (
            model,
            runtime_kwargs.get("provider"),
            runtime_kwargs.get("base_url"),
            bool(runtime_kwargs.get("api_key")),
            tuple(enabled_toolsets),
            str(workspace_path) if workspace_path else "",
        )
        cache = _agent_state.setdefault("agent_cache", {})
        # LRU-ish: keep last 4 (workspace) -> AIAgent entries so a user
        # who switches between 2-3 workspaces doesn't pay the ~1.8s build
        # cost on every switch. session_id is mutable on the agent, so
        # we patch it in place and return the same AIAgent across
        # multiple sessions in the same workspace.
        if len(cache) > 4:
            # Drop the oldest by insertion order
            try:
                oldest_key = next(iter(cache))
                cache.pop(oldest_key, None)
            except Exception:
                pass
        cached = cache.get(sig)
        if cached is not None:
            # Patch the per-request callbacks onto the cached agent so the
            # new request's stream deltas / tool events go to the new
            # request's queue, not the first request's.
            #
            # CRITICAL (v3.3.12 hotfix): the cache must NOT blindly
            # overwrite a callback the agent already owns with a None
            # from a caller that didn't supply one. Doing so silently
            # kills streaming + tool event visibility for whatever
            # request the cached agent was originally bound to (which
            # may still be in flight). Only overwrite when the caller
            # actually passed a non-None callable.
            try:
                if stream_delta_callback is not None:
                    cached.stream_delta_callback = stream_delta_callback
                if tool_progress_callback is not None:
                    cached.tool_progress_callback = tool_progress_callback
                if tool_start_callback is not None:
                    cached.tool_start_callback = tool_start_callback
                if tool_complete_callback is not None:
                    cached.tool_complete_callback = tool_complete_callback
                if session_id is not None:
                    cached.session_id = session_id
            except Exception:
                pass
            # v3.4.13 — WORKSPACE-FRESH system prompt. On cache HIT the agent
            # keeps whatever `ephemeral_system_prompt` it was built with.
            # That can be a STALE workspace (e.g. user was in HydroPlus,
            # switched to cvc — cache key normally forces a rebuild because
            # `workspace_path` is in `sig`, BUT if any caching path skips
            # the rebuild the agent answers as if still in the OLD
            # workspace). Force-inject the freshly built prompt so every
            # request sees the workspace the user actually selected.
            if system_prompt is not None:
                try:
                    cached.ephemeral_system_prompt = system_prompt
                    # Also clear the cached built prompt — the next
                    # ``_restore_or_build_system_prompt`` call will rebuild
                    # from scratch (because the stored session-DB row
                    # doesn't match the new runtime workspace).
                    if hasattr(cached, "_cached_system_prompt"):
                        cached._cached_system_prompt = None
                except Exception:
                    pass
            # v3.3.26 — Clear any stale interrupt flag on the cached agent.
            #
            # Root cause: the vendored ``conversation_loop.run_conversation``
            # at agent/turn_context.py:400-407 INTENTIONALLY preserves
            # ``agent._interrupt_requested`` across turns (it only clears
            # the per-thread tool-level signal). If a prior request set the
            # flag — typically because a WebSocket / SSE client disconnected
            # mid-turn, which fires ``agent_ref[0].interrupt()`` in
            # ``cvc/gateway/chat.py``'s disconnect handlers — the next
            # request on this same cached agent sees ``_interrupt_requested
            # is True`` at the top of the loop and exits immediately with
            # ``reason="interrupted_by_user"``, ``api_calls=0``, and
            # ``response_len=0``. No model call. No tool calls. No text
            # deltas. The dashboard just sees a flash / no streaming.
            #
            # Clearing the flag at the cache-handoff point is the right
            # place because:
            #   1. It applies to every caller of ``create_agent`` — the
            #      dashboard today, but also any future external channel
            #      (Telegram, Slack, webhooks) that goes through this
            #      factory. One place to fix, all consumers protected.
            #   2. The cache returns a reused AIAgent across requests; the
            #      "new request started" boundary is exactly when a stale
            #      interrupt from a previous turn becomes harmful.
            #   3. A request that itself wants to interrupt the agent mid-
            #      turn can still set the flag — ``clear_interrupt()`` only
            #      resets the *baseline* before the new turn begins.
            #
            # The vendored agent's own ``clear_interrupt()`` is safe to
            # call here: it resets ``_interrupt_requested = False``, the
            # per-thread tool interrupt signal, and any pending steer
            # metadata. We guard it with hasattr so a non-vendored
            # ``AIAgent`` subclass in tests still works.
            try:
                if hasattr(cached, "clear_interrupt"):
                    cached.clear_interrupt()
            except Exception:
                # If clear_interrupt raises on a partially-initialized
                # agent, the worst case is the new turn exits with
                # ``interrupted_by_user`` (the pre-patch behavior). The
                # patch is a strict improvement; never let a cleanup
                # failure block the new request.
                pass
            return cached

        # No cached agent for this (config, workspace) — build one
        agent = AIAgent(
            model=model,
            **runtime_kwargs,
            max_iterations=max_iterations,
            quiet_mode=True,
            verbose_logging=False,
            ephemeral_system_prompt=system_prompt or None,
            enabled_toolsets=enabled_toolsets,
            session_id=session_id,
            platform="cvc-dashboard",
            stream_delta_callback=stream_delta_callback,
            tool_progress_callback=tool_progress_callback,
            tool_start_callback=tool_start_callback,
            tool_complete_callback=tool_complete_callback,
            session_db=_agent_state.get("session_db"),
            fallback_model=fallback_model,
            reasoning_config=reasoning_config,
        )
        cache[sig] = agent
        _agent_state["agent_signature"] = sig
        return agent
