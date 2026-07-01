"""
cvc.hermes_unified — Bridge between CVC's dashboard and the vendored full Hermes gateway.

This module replaces the hand-rolled `stream_unified_chat()` in gateway_chat.py
with a thin proxy that forwards dashboard requests to the vendored full Hermes
gateway (`cvc.agent._vendor.hermes.gateway.platforms.api_server`), which
exposes the full OpenAI-compatible HTTP API and a structured SSE event stream
with the complete agent loop:

  - POST /v1/chat/completions          (OpenAI Chat Completions, streaming)
  - POST /v1/responses                 (OpenAI Responses API, stateful)
  - POST /api/sessions/{id}/chat/stream (Hermes-native SSE event stream)
  - GET  /v1/models                    (model catalog)
  - GET  /v1/toolsets                  (available toolsets)
  - ... plus 89 tools, full skill system, memory, sessions, runs, cron, etc.

The vendored api_server is a self-contained aiohttp web app. We boot it
once (in the CVC gateway's FastAPI lifespan) on a sibling port
(`API_SERVER_PORT`, default 8642) and route dashboard traffic to it.

v3.2.0 — replaces the v3.1.x hand-rolled adapter that had no tools/sessions.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import secrets
import time
from pathlib import Path
from typing import Any, AsyncIterator

logger = logging.getLogger(__name__)

# Default port for the vendored full Hermes api_server. Lives on a sibling
# port because it runs an aiohttp web app while CVC's gateway is FastAPI/uvicorn.
DEFAULT_API_SERVER_PORT = 8642


def _resolve_api_server_endpoint() -> tuple[str, int, str]:
    """Return (host, port, api_key) for the vendored api_server.

    Reads env vars (set by the CVC gateway lifespan before booting the
    api_server, or overridden by the user). Generates a random API key
    on first boot if none was provided — the dashboard lives on
    localhost and shares the key via the CVC gateway's proxy.
    """
    host = os.environ.get("API_SERVER_HOST", "127.0.0.1")
    port = int(os.environ.get("API_SERVER_PORT", str(DEFAULT_API_SERVER_PORT)))
    api_key = os.environ.get("API_SERVER_KEY", "")
    if not api_key:
        # v3.2.0 — Generate a stable per-user API key on first boot and
        # persist it in ~/.cvc/api_server_key so the dashboard can reuse
        # the same key after restart without prompting. Without this,
        # every gateway restart would invalidate the dashboard's stored
        # key and the chat would 401. Matches the user's rule: zero
        # friction, no "set this env var" steps for the end user.
        key_path = Path.home() / ".cvc" / "api_server_key"
        try:
            if key_path.is_file():
                api_key = key_path.read_text(encoding="utf-8").strip()
            if not api_key or len(api_key) < 16:
                api_key = secrets.token_urlsafe(32)
                key_path.parent.mkdir(parents=True, exist_ok=True)
                key_path.write_text(api_key, encoding="utf-8")
                try:
                    key_path.chmod(0o600)
                except Exception:
                    pass
                logger.info("Generated new api_server key at %s", key_path)
            # Make the key visible to the api_server boot below.
            os.environ["API_SERVER_KEY"] = api_key
        except Exception as exc:
            logger.warning("Failed to persist api_server key: %s", exc)
            api_key = api_key or secrets.token_urlsafe(32)
            os.environ["API_SERVER_KEY"] = api_key
    return host, port, api_key


async def start_api_server_background() -> dict[str, Any]:
    """Boot the vendored full Hermes api_server as a background aiohttp server.

    Returns a handle dict with the endpoint info:
        {
            "host": "127.0.0.1",
            "port": 8642,
            "api_key": "<shared-secret>",
            "adapter": <APIServerAdapter>,
        }

    The returned adapter is connected and listening; the CVC gateway's
    lifespan holds a reference so the aiohttp app stays alive for the
    lifetime of the FastAPI process. The api_server's full agent loop
    is what handles the dashboard's chat, including all 89 tools, skills,
    memory, sessions, runs, etc.
    """
    host, port, api_key = _resolve_api_server_endpoint()

    # Make sure the env vars the vendored config layer reads are set
    # BEFORE we import the api_server (some modules cache the config at
    # import time).
    os.environ.setdefault("API_SERVER_ENABLED", "1")
    os.environ["API_SERVER_HOST"] = host
    os.environ["API_SERVER_PORT"] = str(port)
    os.environ["API_SERVER_KEY"] = api_key
    # The dashboard hits the api_server through the CVC gateway's proxy
    # on the same origin, so CORS isn't strictly required. Be permissive
    # for dev tools and CLI clients.
    os.environ.setdefault("API_SERVER_CORS_ORIGINS", "*")

    # v3.2.0 — Bridge CVC's `~/.cvc/config.yaml` provider/model/key
    # into the env vars the vendored Hermes runtime reads. Without this,
    # the api_server falls back to its own ~/.hermes/config.yaml (or no
    # config at all if HERMES_HOME is unset), which is empty on a fresh
    # CVC install — so the agent would have no provider and chat would
    # fail with "No API key for provider `passthrough`".
    try:
        from cvc.gateway_chat import _resolve_provider_config
        cfg = _resolve_provider_config()
        if cfg.get("provider"):
            os.environ["HERMES_INFERENCE_PROVIDER"] = str(cfg["provider"])
        if cfg.get("model"):
            os.environ["HERMES_INFERENCE_MODEL"] = str(cfg["model"])
        if cfg.get("api_key"):
            # The api_server's _run_agent() reads the provider-specific
            # env var (e.g. MINIMAX_API_KEY) directly. We map CVC's
            # resolved key back to the right env var name.
            _env_map = {
                "minimax": "MINIMAX_API_KEY",
                "anthropic": "ANTHROPIC_API_KEY",
                "openai": "OPENAI_API_KEY",
                "google": "GOOGLE_API_KEY",
                "github": "COPILOT_GITHUB_TOKEN",
                "copilot": "COPILOT_GITHUB_TOKEN",
                "groq": "GROQ_API_KEY",
                "xai": "XAI_API_KEY",
                "mistral": "MISTRAL_API_KEY",
                "deepseek": "DEEPSEEK_API_KEY",
                "nvidia": "NVIDIA_API_KEY",
            }
            env_key = _env_map.get(str(cfg["provider"]).lower())
            if env_key and not os.environ.get(env_key):
                os.environ[env_key] = str(cfg["api_key"])
        if cfg.get("base_url"):
            os.environ["HERMES_INFERENCE_BASE_URL"] = str(cfg["base_url"])
    except Exception as exc:
        logger.warning("Could not bridge CVC config to Hermes env: %s", exc)

    from cvc.agent._vendor.hermes.gateway.config import Platform, PlatformConfig
    from cvc.agent._vendor.hermes.gateway.platforms.api_server import (
        APIServerAdapter,
        check_api_server_requirements,
    )

    if not check_api_server_requirements():
        raise RuntimeError(
            "Vendored Hermes api_server requirements not satisfied. "
            "Ensure aiohttp is installed in the CVC venv."
        )

    config = PlatformConfig(
        enabled=True,
        extra={
            "host": host,
            "port": port,
            "key": api_key,
            "cors_origins": "*",
        },
    )
    adapter = APIServerAdapter(config)
    ok = await adapter.connect()
    if not ok:
        raise RuntimeError(
            f"Failed to start vendored api_server on {host}:{port}. "
            "Check the gateway logs for the specific reason "
            "(port conflict, missing API key, etc.)."
        )
    logger.info(
        "Vendored Hermes api_server listening on http://%s:%d (key len=%d)",
        host, port, len(api_key),
    )
    return {
        "host": host,
        "port": port,
        "api_key": api_key,
        "adapter": adapter,
    }


async def stop_api_server_background(handle: dict[str, Any] | None) -> None:
    """Stop the vendored api_server aiohttp server (called from FastAPI lifespan)."""
    if not handle:
        return
    adapter = handle.get("adapter")
    if adapter is None:
        return
    try:
        await adapter.disconnect()
    except Exception as exc:
        logger.warning("Error stopping vendored api_server: %s", exc)


# ───────────────────────────────────────────────────────────────────────────
#  HTTP / WebSocket proxy layer
# ───────────────────────────────────────────────────────────────────────────
#
# The dashboard already speaks the CVC gateway's own protocol
# (WebSocket events like `turn_start`, `assistant.delta`, `tool.started`, `done`).
# We translate between the dashboard's protocol and the vendored api_server's
# protocol on the way in and on the way out, so the dashboard keeps working
# without any changes.

def _dashboard_messages_to_openai(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Translate the dashboard's `messages` array (with `role`/`content`)
    into the OpenAI Chat Completions format that /v1/chat/completions expects.

    The dashboard sends a flat list of {role, content}. OpenAI wants the
    same. We just pass through.
    """
    out = []
    for m in messages or []:
        role = m.get("role")
        content = m.get("content")
        if not role or content is None:
            continue
        if isinstance(content, list):
            # Anthropic-style content blocks → flatten to text
            content = "\n".join(
                b.get("text", "") for b in content
                if isinstance(b, dict) and b.get("type") == "text"
            )
        out.append({"role": role, "content": str(content)})
    return out


async def stream_chat_to_dashboard(
    handle: dict[str, Any],
    body: dict[str, Any],
) -> AsyncIterator[bytes]:
    """Yield dashboard-protocol SSE events by proxying to the vendored api_server.

    The dashboard's chat expects:
      - data: {"type": "turn_start", "turn_id": "..."}
      - data: {"type": "status",     "message": "..."}
      - data: {"type": "assistant.delta", ...}
      - data: {"type": "tool.started", ...}
      - data: {"type": "tool.completed", ...}
      - data: {"type": "error", ...}
      - data: {"type": "done", "turn_id": "..."}

    The vendored api_server's /api/sessions/{id}/chat/stream emits:
      - event: run.started
      - event: message.started
      - event: assistant.delta
      - event: tool.started
      - event: tool.completed
      - event: tool.failed
      - event: assistant.completed
      - event: run.completed
      - event: error
      - event: done

    We translate between the two protocols, including the session-id
    lifecycle (create a Hermes session on first call, reuse it for the
    same conversation thread).
    """
    import httpx

    if not handle or not handle.get("adapter"):
        yield _sse({"type": "error", "message": "Vendored api_server not running."})
        yield _sse_done()
        return

    host = handle["host"]
    port = handle["port"]
    api_key = handle["api_key"]
    base = f"http://{host}:{port}"

    # Pre-extract the user message so we can fire per-turn soul update
    # after the stream ends (regardless of which SSE event finishes).
    _pre_messages = body.get("messages", []) or []
    _pre_user_message = ""
    for _m in reversed(_pre_messages):
        if _m.get("role") == "user":
            _c = _m.get("content", "")
            if isinstance(_c, list):
                _c = "\n".join(
                    b.get("text", "") for b in _c
                    if isinstance(b, dict) and b.get("type") == "text"
                )
            _pre_user_message = str(_c or "")
            break

    # 1. Reuse or create a Hermes session.
    thread_id = body.get("thread_id") or ""
    session_id = body.get("hermes_session_id") or ""
    if not session_id:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.post(
                    f"{base}/api/sessions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    json={},
                )
                r.raise_for_status()
                _body = r.json()
                # The api_server returns either {"id": "..."} or
                # {"session": {"id": "..."}} depending on the version.
                session_id = (
                    _body.get("id")
                    or _body.get("session_id")
                    or _body.get("session", {}).get("id", "")
                )
        except Exception as exc:
            logger.warning("Failed to create Hermes session: %s", exc)
            session_id = ""

    if not session_id:
        # Fall back to a stateless /v1/chat/completions call.
        async for chunk in _stream_via_chat_completions(handle, body):
            yield chunk
        return

    # 2. Build the request to /api/sessions/{id}/chat/stream.
    messages = body.get("messages", []) or []
    user_message = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            content = m.get("content", "")
            if isinstance(content, list):
                content = "\n".join(
                    b.get("text", "") for b in content
                    if isinstance(b, dict) and b.get("type") == "text"
                )
            user_message = str(content)
            break
    if not user_message:
        yield _sse({"type": "error", "message": "No user message in request."})
        yield _sse_done()
        return

    # 3. Yield turn_start so the dashboard can show "thinking..." immediately.
    turn_id = f"turn_{int(time.time() * 1000)}_{secrets.token_hex(4)}"
    yield _sse({"type": "turn_start", "turn_id": turn_id, "hermes_session_id": session_id})
    yield _sse({"type": "status", "message": f"Sending to vendored Hermes api_server (session {session_id[:8]}…)."})

    # 4. Stream the SSE response from the api_server and translate events.
    # The api_server expects `message` at the top level of the body
    # (a plain string, not a {role, content} dict).
    payload = {
        "message": user_message,
        "stream": True,
    }
    if body.get("reasoning_effort"):
        payload["reasoning_effort"] = body["reasoning_effort"]

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                f"{base}/api/sessions/{session_id}/chat/stream",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "Accept": "text/event-stream",
                },
                json=payload,
            ) as r:
                if r.status_code != 200:
                    text = await r.aread()
                    yield _sse({
                        "type": "error",
                        "message": f"api_server returned {r.status_code}: {text.decode('utf-8', 'replace')[:500]}",
                    })
                    yield _sse({"type": "done", "turn_id": turn_id})
                    return
                # Parse SSE: lines starting with "event: NAME" + "data: JSON"
                current_event: str | None = None
                current_data_lines: list[str] = []
                async for line in r.aiter_lines():
                    if not line:
                        # Dispatch the buffered event.
                        if current_event and current_data_lines:
                            data_str = "\n".join(current_data_lines)
                            try:
                                data = json.loads(data_str)
                            except Exception:
                                data = {"raw": data_str}
                            translated = _translate_hermes_event(
                                current_event, data, turn_id,
                                user_message=user_message,
                                body=body,
                            )
                            if translated is not None:
                                yield _sse(translated)
                        current_event = None
                        current_data_lines = []
                        if translated_was_done(current_event):
                            break
                        continue
                    if line.startswith("event: "):
                        current_event = line[len("event: "):].strip()
                    elif line.startswith("data: "):
                        current_data_lines.append(line[len("data: "):])
                    elif line.startswith(":"):
                        # SSE comment / keepalive — ignore
                        pass
    except Exception as exc:
        logger.exception("Proxy to vendored api_server failed")
        yield _sse({"type": "error", "message": f"api_server proxy error: {exc}"})
        yield _sse({"type": "done", "turn_id": turn_id})
        return

    # Ensure we always emit done.
    yield _sse({"type": "done", "turn_id": turn_id})


def _translate_hermes_event(
    name: str,
    data: dict[str, Any],
    turn_id: str,
    *,
    user_message: str = "",
    body: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Translate a vendored api_server SSE event to a dashboard SSE event."""
    if name == "run.started":
        return None  # Already emitted as turn_start
    if name == "message.started":
        return None
    if name == "assistant.delta":
        return {
            "type": "assistant.delta",
            "delta": data.get("delta", ""),
            "message_id": data.get("message_id"),
        }
    if name == "tool.started":
        # The api_server's session chat-stream sometimes calls
        # _tool_progress with tool_name=None for internal/auxiliary
        # events. Surface these as a generic "_thinking" event so the
        # dashboard's tool panel can still show progress, mirroring
        # the api_server's own internal logic.
        return {
            "type": "tool.started",
            "tool_name": data.get("tool_name") or "_thinking",
            "args": data.get("args"),
            "message_id": data.get("message_id"),
        }
    if name == "tool.completed":
        return {
            "type": "tool.completed",
            "tool_name": data.get("tool_name", ""),
            "preview": data.get("preview"),
            "message_id": data.get("message_id"),
        }
    if name == "tool.failed":
        return {
            "type": "tool.failed",
            "tool_name": data.get("tool_name", ""),
            "preview": data.get("preview"),
            "message_id": data.get("message_id"),
        }
    if name == "tool.progress":
        return {
            "type": "tool.progress",
            "tool_name": data.get("tool_name", ""),
            "delta": data.get("delta", ""),
            "message_id": data.get("message_id"),
        }
    if name == "assistant.completed":
        assistant_text = data.get("content", "") or ""
        # ── Per-turn soul auto-encoding (H2) ────────────────────────
        # Dashboard sessions never end, so the legacy on_session_stop
        # hook never fires. Capture the assistant text + the user
        # message we already have, then run the heuristic H2
        # classifiers off the hot path (daemon thread) so the soul
        # learns from every turn — regardless of workspace, chat, or
        # provider.
        try:
            from cvc.operations.per_turn_soul import fire_and_forget_update
            fire_and_forget_update(
                user_message=user_message,
                assistant_text=assistant_text,
                workspace_path=(body or {}).get("workspace_path"),
            )
        except Exception as _soul_exc:
            logger.debug("per-turn soul dispatch failed (non-fatal): %s", _soul_exc)
        return {
            "type": "assistant.completed",
            "content": assistant_text,
            "message_id": data.get("message_id"),
        }
    if name == "run.completed":
        return None  # We emit our own `done` below
    if name == "error":
        return {"type": "error", "message": data.get("message", str(data))}
    if name == "done":
        return None
    # Unknown event — pass through for debugging.
    return {"type": name, **data}


def translated_was_done(_evt: str | None) -> bool:
    return False


async def _stream_via_chat_completions(
    handle: dict[str, Any],
    body: dict[str, Any],
) -> AsyncIterator[bytes]:
    """Stateless fallback: proxy to /v1/chat/completions (no session)."""
    import httpx

    turn_id = f"turn_{int(time.time() * 1000)}_{secrets.token_hex(4)}"
    yield _sse({"type": "turn_start", "turn_id": turn_id})
    yield _sse({"type": "status", "message": "Falling back to stateless /v1/chat/completions."})

    # Pre-extract user_message + accumulate assistant_text for the
    # per-turn soul auto-encoding hook.
    _pre_msgs = body.get("messages", []) or []
    _user_message = ""
    for _m in reversed(_pre_msgs):
        if _m.get("role") == "user":
            _c = _m.get("content", "")
            if isinstance(_c, list):
                _c = "\n".join(
                    b.get("text", "") for b in _c
                    if isinstance(b, dict) and b.get("type") == "text"
                )
            _user_message = str(_c or "")
            break
    _assistant_acc: list[str] = []

    base = f"http://{handle['host']}:{handle['port']}"
    payload = {
        "model": body.get("model") or "hermes-agent",
        "messages": _dashboard_messages_to_openai(body.get("messages", [])),
        "stream": True,
    }
    if body.get("reasoning_effort"):
        payload["reasoning_effort"] = body["reasoning_effort"]

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                f"{base}/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {handle['api_key']}",
                    "Content-Type": "application/json",
                },
                json=payload,
            ) as r:
                if r.status_code != 200:
                    text = await r.aread()
                    yield _sse({"type": "error", "message": f"chat/completions returned {r.status_code}: {text.decode('utf-8', 'replace')[:500]}"})
                    yield _sse({"type": "done", "turn_id": turn_id})
                    return
                async for line in r.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    data_str = line[len("data: "):]
                    if data_str.strip() == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                    except Exception:
                        continue
                    choices = chunk.get("choices") or []
                    for c in choices:
                        delta = (c.get("delta") or {}).get("content")
                        if delta:
                            _assistant_acc.append(delta)
                            yield _sse({"type": "assistant.delta", "delta": delta})
    except Exception as exc:
        logger.exception("chat/completions proxy failed")
        yield _sse({"type": "error", "message": f"chat/completions proxy error: {exc}"})

    # ── Per-turn soul auto-encoding (H2) — fire-and-forget thread ──
    try:
        from cvc.operations.per_turn_soul import fire_and_forget_update
        fire_and_forget_update(
            user_message=_user_message,
            assistant_text="".join(_assistant_acc),
            workspace_path=body.get("workspace_path"),
        )
    except Exception as _soul_exc:
        logger.debug("per-turn soul dispatch failed (non-fatal): %s", _soul_exc)

    yield _sse({"type": "done", "turn_id": turn_id})


def _sse(data: dict[str, Any]) -> bytes:
    """Format a dict as a single SSE `data:` line."""
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n".encode("utf-8")


def _sse_done() -> bytes:
    return b"data: [DONE]\n\n"
