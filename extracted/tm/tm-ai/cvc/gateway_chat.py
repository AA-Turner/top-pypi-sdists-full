"""
CVC v3.0 — Unified chat stream generator (called from `cvc.gateway`).

This module does NOT define a FastAPI route. It exposes a single
`stream_unified_chat()` async generator that yields SSE-formatted byte
strings. `cvc.gateway` adds the route (`/api/chat` when
`CVC_USE_UNIFIED_CORE=1`, or `/api/chat_unified` as an always-on
side-by-side route) that calls into this function.

Why a stream generator and not a route:
  - Keeps the unified-core wiring in ONE place.
  - `cvc.gateway` owns the FastAPI app and route table — we don't fight it.
  - Easy to test the generator directly (`async for chunk in
    stream_unified_chat(body): ...`).
  - The unified core's `AIAgent.run_conversation()` can also be called
    from CLI/headless contexts (e.g. `cvc chat --unified`) without
    going through HTTP.

Event schema (matches the dashboard's existing renderer):
  - {"type": "text",         "content": "..."}                  streaming text delta
  - {"type": "tool_use",     "id": "...", "name": "...", ...}   model emits a tool call
  - {"type": "tool_result",  "tool_call_id": "...", "content": "..."}  tool exec result
  - {"type": "status",       "message": "..."}                  progress / info
  - {"type": "error",        "message": "..."}                  unrecoverable error
  - {"type": "setup_required", "provider": "..."}               agent LLM not bound
  - data: [DONE]\\n\\n                                          end of stream
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any, AsyncIterator

logger = logging.getLogger("cvc.gateway_chat")

_VALID_REASONING_EFFORTS = {"low", "medium", "high", "xhigh", "minimal", "none"}

# Provider → (env-var-name, default-model, base-url-env-var).
# We support the same set the dashboard's setup flow supports.
_PROVIDER_DEFAULTS: dict[str, tuple[str, str, str | None]] = {
    "anthropic": ("ANTHROPIC_API_KEY", "claude-3-5-sonnet-latest", "ANTHROPIC_BASE_URL"),
    "openai":    ("OPENAI_API_KEY",    "gpt-4o-mini",             "OPENAI_BASE_URL"),
    "google":    ("GOOGLE_API_KEY",    "gemini-2.0-flash",        None),
    "github":    ("COPILOT_GITHUB_TOKEN", "gpt-4o",              None),
    "copilot":   ("COPILOT_GITHUB_TOKEN", "gpt-4o",              None),
    "vertex":    ("GOOGLE_API_KEY",    "gemini-2.0-flash",        None),
    "ollama":    ("",                  "llama3.2",                "OLLAMA_BASE_URL"),
    "lmstudio":  ("",                  "qwen2.5-7b-instruct",     "LMSTUDIO_BASE_URL"),
    "minimax":   ("MINIMAX_API_KEY",   "MiniMax-M3",              "MINIMAX_BASE_URL"),
}


def _sse(payload: dict[str, Any]) -> bytes:
    """Format a payload as one SSE `data:` chunk (UTF-8 bytes)."""
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n".encode("utf-8")


def _sse_done() -> bytes:
    """End-of-stream marker."""
    return b"data: [DONE]\n\n"


def _resolve_provider_config(workspace_path: str | None = None) -> dict[str, Any]:
    """Build a provider config dict from env vars + workspace settings.

    Order of precedence (highest first):
      1. Environment variables (ANTHROPIC_API_KEY, OPENAI_API_KEY, ...)
      2. Workspace settings file (`<workspace>/.cvc/settings.json`)
      3. Empty / unset (caller decides what to do with that)
    """
    # Read workspace settings if present.
    ws_settings: dict[str, Any] = {}
    if workspace_path:
        settings_path = Path(workspace_path) / ".cvc" / "settings.json"
        try:
            if settings_path.is_file():
                ws_settings = json.loads(settings_path.read_text(encoding="utf-8"))
        except Exception:
            logger.debug("Failed to read workspace settings at %s", settings_path,
                         exc_info=True)

    # Read the user-global CVC config (~/.cvc/config.yaml) as a middle
    # precedence layer: env > user-global > workspace > built-in default.
    user_settings: dict[str, Any] = {}
    try:
        import yaml  # already a CVC dep
        user_cfg_path = Path.home() / ".cvc" / "config.yaml"
        if user_cfg_path.is_file():
            user_settings = yaml.safe_load(user_cfg_path.read_text(encoding="utf-8")) or {}
    except Exception:
        logger.debug("Failed to read user config at ~/.cvc/config.yaml", exc_info=True)

    provider = (
        os.environ.get("CVC_PROVIDER")
        or user_settings.get("primary_provider")
        or ws_settings.get("provider")
        or "openai"
    )
    provider = str(provider).lower().strip()

    env_key, default_model, base_url_env = _PROVIDER_DEFAULTS.get(
        provider, ("OPENAI_API_KEY", "gpt-4o-mini", None)
    )
    # v3.1.3 — API key resolution chain (highest priority first):
    #   1. Environment variable (e.g. MINIMAX_API_KEY)
    #   2. user_settings["api_keys"][<provider>] from ~/.cvc/config.yaml
    #      (written by `cvc setup` via _sync_global_to_gateway_yaml)
    #   3. ws_settings["api_keys"][<provider>] from workspace settings
    #   4. Empty (the dashboard's setup_required path will surface this)
    # The previous v3.1.0–v3.1.2 chain only checked the env var, which
    # meant `cvc setup` saved the key to config.json but the gateway
    # never saw it — the dashboard always said "Setup Required" until
    # the user manually exported the key in their shell.
    api_key = ""
    if env_key:
        api_key = os.environ.get(env_key, "") or ""
    if not api_key:
        yaml_keys = user_settings.get("api_keys") or {}
        if isinstance(yaml_keys, dict) and yaml_keys.get(provider):
            api_key = yaml_keys[provider]
    if not api_key:
        ws_keys = ws_settings.get("api_keys") or {}
        if isinstance(ws_keys, dict) and ws_keys.get(provider):
            api_key = ws_keys[provider]
    if not api_key and provider in ("ollama", "lmstudio"):
        api_key = "ollama"  # Ollama accepts any non-empty key

    model = (
        os.environ.get("CVC_MODEL")
        or user_settings.get("default_model")
        or ws_settings.get("model")
        or default_model
    )
    base_url = os.environ.get(base_url_env) if base_url_env else None
    if not base_url and provider in ("ollama", "lmstudio"):
        base_url = "http://localhost:11434/v1" if provider == "ollama" else "http://localhost:1234/v1"
    # MiniMax: Anthropic-Messages-API-compatible (NOT OpenAI-compat).
    # CVC's provider router expects base_url = host only; the runtime
    # appends /anthropic/v1/messages. The dashboard setup / unified
    # handler doesn't always do that, so be explicit.
    if provider == "minimax" and not base_url:
        base_url = "https://api.minimax.io/anthropic"

    return {
        "provider": provider,
        "model": model,
        "api_key": api_key,
        "base_url": base_url,
    }


def _extract_user_message(messages: list[dict[str, Any]]) -> str:
    """Pull the most recent user turn out of the dashboard's messages list.

    The dashboard sends the full conversation history. The unified core
    wants a single user message per turn — we re-thread history separately
    as `conversation_history` so the model sees prior turns.
    """
    for msg in reversed(messages):
        if msg.get("role") == "user":
            content = msg.get("content", "")
            if isinstance(content, list):
                # Anthropic-style content blocks
                return "\n".join(
                    b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"
                )
            return str(content)
    return ""


def _extract_conversation_history(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return the conversation history (excluding the most recent user turn).

    The unified core's `run_conversation()` takes a `user_message` (the new
    turn) and a `conversation_history` (prior turns). We split them here.
    """
    history: list[dict[str, Any]] = []
    for msg in messages[:-1] if messages else []:
        role = msg.get("role")
        if role not in ("user", "assistant", "system"):
            continue
        content = msg.get("content", "")
        if isinstance(content, list):
            content = "\n".join(
                b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"
            )
        history.append({"role": role, "content": str(content)})
    return history


async def stream_unified_chat(body: dict[str, Any]) -> AsyncIterator[bytes]:
    """The unified-core backed SSE generator.

    v3.2.0 — Now a thin proxy to the vendored full api_server
    (`cvc.agent._vendor.hermes.gateway.platforms.api_server`), which
    exposes the complete agent loop with 89 tools, sessions, runs,
    skills, and memory. Previous v3.1.x versions constructed a bare
    AIAgent() with no toolset, which is why the agent could chat but
    couldn't read files, run commands, or do anything useful.

    The api_server is booted as a sibling aiohttp process by the CVC
    gateway's FastAPI lifespan (see `cvc.hermes_unified`). This
    function translates the dashboard's chat protocol to the
    api_server's SSE event format and back.

    Args:
        body: The parsed JSON body of the dashboard's /api/chat POST.
              Keys: messages, stream, reasoning_effort, persona_id,
                    thread_id, workspace_path.

    Yields:
        UTF-8 bytes ready to write to a StreamingResponse. Always ends
        with `data: [DONE]\\n\\n`.
    """
    # 1. Get the api_server handle from the CVC gateway module.
    # The FastAPI lifespan stored it in cvc.gateway._hermes_api_server.
    try:
        from cvc.gateway import _hermes_api_server
        handle = _hermes_api_server
    except ImportError:
        handle = None

    if handle:
        # 2. v3.2.0 — Proxy to the vendored full api_server.
        # This is the path with the full tool set, sessions, runs,
        # memory, skills, etc. The api_server's _run_agent()
        # constructs an AIAgent with all the proper context.
        from cvc.hermes_unified import stream_chat_to_dashboard
        async for chunk in stream_chat_to_dashboard(handle, body):
            yield chunk
        return

    # 3. Fallback: api_server didn't boot. Use the legacy hand-rolled
    # AIAgent path (no tools, no sessions — degraded but functional).
    logger.warning(
        "Vendored api_server is not running; falling back to the "
        "legacy hand-rolled chat path. The agent will be able to chat "
        "but will not have access to file/bash/etc. tools. Check the "
        "gateway logs for the api_server boot error."
    )
    async for chunk in _stream_unified_chat_legacy(body):
        yield chunk


async def _stream_unified_chat_legacy(body: dict[str, Any]) -> AsyncIterator[bytes]:
    """Legacy v3.1.x hand-rolled chat path (no tools, no sessions).

    Kept as a fallback in case the vendored api_server fails to boot.
    This is the path the user has been hitting — it constructs a bare
    AIAgent with no tools, so the agent can only chat. The dashboard
    shows "JUST WAIT..." because the agent has no way to read the
    project the user is asking about.

    DO NOT DELETE — this is the rollback path. If the api_server
    integration breaks, the user can still chat (degraded) via this
    path. Saved in line with the "never delete CVC code" rule.
    """
    messages = body.get("messages", []) or []
    stream = body.get("stream", True)
    workspace_path = body.get("workspace_path")
    persona_id = body.get("persona_id") or ""
    thread_id = body.get("thread_id") or ""

    if not messages:
        yield _sse({"type": "error", "message": "No messages in request body."})
        yield _sse_done()
        return

    cfg = _resolve_provider_config(workspace_path)
    if not cfg["api_key"] and cfg["provider"] not in ("ollama", "lmstudio"):
        # v3.1.0 — Tell the dashboard which env var will actually fix
        # this. Send the primary env var for the user's selected
        # provider (e.g. MINIMAX_API_KEY) as the first item, then a
        # fallback list of common providers so users on the legacy
        # four (Anthropic/OpenAI/Google/Copilot) still get useful
        # hints. Without this, the dashboard falls back to its own
        # hardcoded 4-provider list and reports "set COPILOT_..." even
        # when the user is on MiniMax.
        primary_key, _default_model, _base_url = _PROVIDER_DEFAULTS.get(
            cfg["provider"], (None, "", None)
        )
        fallback_keys = [
            "ANTHROPIC_API_KEY",
            "OPENAI_API_KEY",
            "GOOGLE_API_KEY",
            "COPILOT_GITHUB_TOKEN",
        ]
        env_keys = [primary_key] if primary_key else []
        env_keys = env_keys + [k for k in fallback_keys if k not in env_keys]
        yield _sse({
            "type": "setup_required",
            "provider": cfg["provider"],
            "env_keys": env_keys,
            "message": (
                f"No API key for provider `{cfg['provider']}`. Set "
                f"{primary_key or 'your provider API key'} "
                "and restart, or run `cvc setup`."
            ),
        })
        yield _sse_done()
        return

    user_message = _extract_user_message(messages)
    history = _extract_conversation_history(messages)

    if not user_message:
        yield _sse({"type": "error", "message": "Last message in conversation must be a user turn."})
        yield _sse_done()
        return

    # Approval mode: opt-in bypass that mirrors the legacy CVC loop's
    # `CVC_APPROVAL_MODE` semantics. Default: leave the upstream approval flow
    # intact (safer). Set `CVC_APPROVAL_MODE=bypass` or `autopilot` to
    # auto-allow write/edit/patch/dangerous-bash calls.
    approval_mode = (
        os.environ.get("CVC_APPROVAL_MODE", "").strip().lower()
    )
    if approval_mode in ("bypass", "autopilot", "yolo", "off"):
        try:
            from cvc.agent._vendor.hermes.tools.approval import (
                enable_session_yolo,
            )
            sess_key = thread_id or "unified-default"
            enable_session_yolo(sess_key)
            yield _sse({"type": "status", "message": f"Approval mode: {approval_mode} (auto-allow enabled)"})
        except Exception as exc:
            logger.warning("Failed to enable session yolo: %s", exc)

    # Build the agent. Done in a thread because the constructor is sync
    # and may take a moment (loads skills, builds system prompt).
    yield _sse({"type": "status", "message": f"Initialising unified core ({cfg['provider']} / {cfg['model']})…"})

    def _build() -> Any:
        # Import here so the cost is only paid when the unified route is hit.
        from cvc.agent._vendor.hermes.run_agent import AIAgent
        return AIAgent(
            provider=cfg["provider"],
            model=cfg["model"],
            api_key=cfg["api_key"],
            base_url=cfg["base_url"],
            # We do our own SSE event emission; the unified core's
            # `stream_callback` will receive text deltas which we forward.
            stream_delta_callback=None,
        )

    try:
        agent = await asyncio.to_thread(_build)
    except Exception as exc:
        logger.exception("Failed to construct unified core AIAgent")
        yield _sse({"type": "error", "message": f"Unified core init failed: {exc}"})
        yield _sse_done()
        return

    # System prompt: persona override → workspace → default.
    system_prompt = ""
    if persona_id:
        try:
            from cvc.dashboard.personas_api import _get_persona  # type: ignore
            persona = _get_persona(persona_id)
            if persona and persona.get("system_prompt"):
                system_prompt = persona["system_prompt"]
        except Exception:
            logger.debug("Persona override lookup failed for %s", persona_id,
                         exc_info=True)
    if not system_prompt:
        try:
            from cvc.agent.system_prompt import build_system_prompt
            system_prompt = build_system_prompt(
                workspace_path or os.getcwd(), cfg["provider"]
            )
        except Exception:
            logger.debug("Default system prompt build failed", exc_info=True)
            system_prompt = "You are the CVC agent. Help the user."

    # Bridge the unified core's stream_callback into our SSE queue.
    sse_queue: asyncio.Queue[dict[str, Any] | None] = asyncio.Queue()
    # Accumulate assistant text for the per-turn soul auto-encoder.
    # The legacy unified-core path emits `text` deltas (not
    # `assistant.completed`), so we have to assemble the full response
    # ourselves before firing the hook at end-of-turn.
    _assistant_text_parts: list[str] = []

    def _stream_callback(event: dict[str, Any]) -> None:
        """Unified-core → SSE event bridge.

        The unified core invokes this synchronously with an event dict.
        We normalise it into the dashboard's event schema and push to
        the async queue.
        """
        ev_type = event.get("type", "")
        if ev_type in ("text_delta", "text", "delta"):
            text = event.get("content", "")
            if text:
                _assistant_text_parts.append(text)
            sse_queue.put_nowait({"type": "text", "content": text})
        elif ev_type in ("tool_use", "tool_call"):
            sse_queue.put_nowait({
                "type": "tool_use",
                "id": event.get("id", ""),
                "name": event.get("name", ""),
                "arguments": event.get("arguments", {}),
            })
        elif ev_type in ("tool_result", "tool_output"):
            sse_queue.put_nowait({
                "type": "tool_result",
                "tool_call_id": event.get("tool_call_id", event.get("id", "")),
                "content": event.get("content", ""),
            })
        elif ev_type in ("status", "info"):
            sse_queue.put_nowait({"type": "status", "message": event.get("message", "")})
        elif ev_type in ("error", "fatal"):
            sse_queue.put_nowait({"type": "error", "message": event.get("message", "")})
        # Other event types (intermediate, usage, debug) are dropped — the
        # dashboard doesn't render them.

    def _drain_into_queue() -> None:
        """Run the unified core to completion. Pushes events to sse_queue."""
        try:
            result = agent.run_conversation(
                user_message=user_message,
                system_message=system_prompt,
                conversation_history=history,
                task_id=thread_id or None,
                stream_callback=_stream_callback,
                persist_user_message=True,
            )
            # Final assistant message comes back as `final_response`.
            final = result.get("final_response", "")
            if final:
                _assistant_text_parts.append(final)
                sse_queue.put_nowait({"type": "text", "content": final})
            # Fire per-turn soul update now that we have the full
            # assistant response. Fire-and-forget thread so the SSE
            # stream doesn't wait on disk I/O.
            try:
                from cvc.operations.per_turn_soul import fire_and_forget_update
                fire_and_forget_update(
                    user_message=user_message,
                    assistant_text="".join(_assistant_text_parts),
                    workspace_path=workspace_path,
                )
            except Exception as _soul_exc:
                logger.debug("per-turn soul dispatch failed (non-fatal): %s", _soul_exc)
            if result.get("failed"):
                sse_queue.put_nowait({
                    "type": "error",
                    "message": result.get("error") or result.get("failure_reason") or "Agent failed",
                })
        except Exception as exc:
            logger.exception("Unified core run_conversation raised")
            sse_queue.put_nowait({"type": "error", "message": str(exc)})
        finally:
            sse_queue.put_nowait(None)  # sentinel = done

    runner = asyncio.get_event_loop().run_in_executor(None, _drain_into_queue)

    # Stream events out of the queue as SSE bytes.
    while True:
        ev = await sse_queue.get()
        if ev is None:
            break
        yield _sse(ev)
        if ev.get("type") == "error":
            # Don't keep the runner alive if the agent already errored.
            break

    # Wait for the runner to finish (it should already be done by the
    # time we get the sentinel, but be defensive).
    try:
        await asyncio.wait_for(runner, timeout=2.0)
    except asyncio.TimeoutError:
        logger.warning("Unified core runner did not finish within 2s of stream end")
    except Exception:
        pass

    if stream:
        yield _sse_done()
