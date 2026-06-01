"""FastAPI/SSE backend server for the TypeScript TUI."""

from __future__ import annotations

import asyncio
import json
import os
import time
import threading
from collections import defaultdict
from typing import Any, AsyncIterator, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from .agent import Agent, AgentMode
from .config import Config
from .core import AICode

app = FastAPI(title="codrninja-server", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_ai: Optional[AICode] = None

# ── background-run registry ───────────────────────────────────────────────────
# Tracks sessions that have an agent run in flight so the server stays alive
# until they finish even if every TUI client has disconnected.
_active_runs: set[str] = set()
_run_subscribers: dict[str, List[asyncio.Queue]] = defaultdict(list)
_running_agents: dict[str, Any] = {}
_run_lock = threading.Lock()
_last_activity: float = time.time()
_active_oauth_cb: Optional[Any] = None  # active OAuthCallbackServer for manual injection


def get_ai() -> AICode:
    global _ai
    if _ai is None:
        _ai = AICode()
    return _ai


# ── request models ────────────────────────────────────────────────────────────

class SendRequest(BaseModel):
    message: str
    model: Optional[str] = None
    max_steps: int = 50
    auto_approve: bool = False
    mode: str = "build"
    temperature: Optional[float] = None


class PermissionRespondRequest(BaseModel):
    call_id: str
    decision: str  # 'yes' | 'always' | 'no' | 'never'


class CreateSessionRequest(BaseModel):
    name: str


class ExecRequest(BaseModel):
    command: str


class PermissionModeRequest(BaseModel):
    mode: str


class SearchRequest(BaseModel):
    query: str


class FetchRequest(BaseModel):
    url: str


class CommitRequest(BaseModel):
    message: str


class TestRequest(BaseModel):
    command: str = "pytest -q"


class SetModelRequest(BaseModel):
    model: str
    provider: Optional[str] = None


class SetProviderRequest(BaseModel):
    provider: str


class ApiKeyRequest(BaseModel):
    api_key: str


class OllamaConfigRequest(BaseModel):
    url: str


class SessionModelRequest(BaseModel):
    model: str
    provider: Optional[str] = None
    set_as_default: bool = False


class ReasoningLevelRequest(BaseModel):
    level: str


class ModelPrefsRequest(BaseModel):
    prefs: Dict[str, List[str]]


# ── routes ────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/config")
def get_config():
    cfg = get_ai().config
    return {
        "provider": cfg.default_provider,
        "model": cfg.default_model,
        "ollama_url": cfg.ollama_url,
        "reasoning_level": cfg.reasoning_level,
        "permissions_mode": cfg.permissions_mode,
        "model_prefs": cfg.model_prefs,
    }


@app.get("/config/model-prefs")
def get_model_prefs():
    return {"prefs": get_ai().config.model_prefs}


@app.post("/config/model-prefs")
def save_model_prefs(req: ModelPrefsRequest):
    ai = get_ai()
    ai.config.model_prefs = req.prefs
    _persist_config({"model_prefs": req.prefs})
    return {"prefs": ai.config.model_prefs}


@app.get("/sessions")
def list_sessions():
    sessions = get_ai().list_sessions()
    with _run_lock:
        running_now = set(_active_runs)
    for s in sessions:
        s['running'] = s.get('name') in running_now
    return {"sessions": sessions}


@app.post("/sessions")
def create_session(req: CreateSessionRequest):
    session = get_ai().create_session(req.name)
    return {"id": session.id, "name": session.name, "created_at": session.created_at}


@app.get("/sessions/{name}")
def get_session(name: str):
    ai = get_ai()
    history = ai.get_history(name)
    if not history:
        raise HTTPException(status_code=404, detail=f"Session '{name}' not found")
    return history


@app.delete("/sessions/{name}")
def delete_session(name: str):
    ai = get_ai()
    try:
        ai.session_manager.delete(name)
        return {"deleted": name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class RenameSessionRequest(BaseModel):
    new_name: str

@app.post("/sessions/{name}/rename")
def rename_session(name: str, req: RenameSessionRequest):
    ai = get_ai()
    new_name = req.new_name.strip()
    if not new_name:
        raise HTTPException(status_code=400, detail="new_name cannot be empty")
    ok = ai.session_manager.rename(name, new_name)
    if not ok:
        raise HTTPException(status_code=404, detail=f"Session not found: {name}")
    return {"renamed": True, "old_name": name, "new_name": new_name}


@app.get("/sessions/claude-import/list")
def list_claude_import_sessions():
    """List available Claude Code sessions that can be imported."""
    from .claude_import import list_claude_sessions
    return {"sessions": list_claude_sessions()}


class ImportClaudeRequest(BaseModel):
    path: str
    name: str


@app.post("/sessions/claude-import")
def import_claude_session(req: ImportClaudeRequest):
    """Import a Claude Code JSONL session into codrninja."""
    from .claude_import import import_session
    import uuid as _uuid
    from datetime import datetime, timezone

    messages = import_session(req.path)
    if not messages:
        raise HTTPException(status_code=400, detail="No messages found in session file")

    ai = get_ai()
    # Create session (deduplicate name if needed)
    base_name = req.name
    name = base_name
    counter = 1
    while ai.session_manager.get(name):
        name = f"{base_name}-{counter}"
        counter += 1

    ai.session_manager.create(name)

    # Write each message into the session's messages.jsonl
    for msg in messages:
        role = msg.get('role', 'user')
        content = msg.get('content', '')
        if not content:
            continue
        ai.session_manager.append_message(name, role, content)

    state = ai.session_manager.get(name)
    return {
        "name": name,
        "imported_messages": len(messages),
        "session": state,
    }


@app.post("/sessions/{name}/stream")
async def stream_agent(name: str, req: SendRequest) -> StreamingResponse:
    """Start a new agent run and stream events as Server-Sent Events.

    The run continues on the server even if this client disconnects.
    Other clients can reconnect via GET /sessions/{name}/stream.
    """
    global _last_activity
    with _run_lock:
        if name in _active_runs:
            raise HTTPException(status_code=409, detail="Session already has an active run. Use GET to reconnect.")

    ai = get_ai()
    ai.create_session(name)
    _MODE_MAP = {
        "plan":           (AgentMode.PLAN,          "ask"),
        "review":         (AgentMode.REVIEW,         "ask"),
        "vision":         (AgentMode.VISION,         "ask"),
        "build-auto":     (AgentMode.BUILD,          "auto"),
        "build-ask":      (AgentMode.BUILD,          "ask"),
        "build-readonly": (AgentMode.BUILD_READONLY, "ask"),
    }
    mode, perm_override = _MODE_MAP.get(req.mode, (AgentMode.BUILD, None))
    _TEMP_DEFAULTS = {
        "plan": 0.4, "review": 0.1, "vision": 0.85,
        "build-auto": 0.2, "build-ask": 0.2, "build-readonly": 0.2,
    }
    temperature = req.temperature if req.temperature is not None else _TEMP_DEFAULTS.get(req.mode)
    loop = asyncio.get_running_loop()

    sub_queue: asyncio.Queue[Optional[Dict[str, Any]]] = asyncio.Queue(maxsize=500)

    # Stop any running agent for this session before starting a new one
    with _run_lock:
        existing = _running_agents.get(name)
        if existing:
            existing._stop_requested = True

    with _run_lock:
        _active_runs.add(name)
        _run_subscribers[name].append(sub_queue)
    _last_activity = time.time()

    def _broadcast(event: Optional[Dict[str, Any]]) -> None:
        with _run_lock:
            for q in list(_run_subscribers.get(name, [])):
                try:
                    loop.call_soon_threadsafe(q.put_nowait, event)
                except Exception:
                    pass

    def run_agent() -> None:
        agent = Agent(ai, name, max_iterations=req.max_steps, mode=mode, temperature=temperature)
        if perm_override:
            agent.permissions.set_mode(perm_override)
        agent._event_callback = _broadcast
        with _run_lock:
            _running_agents[name] = agent
        try:
            for event in agent.stream_run(req.message):
                _broadcast(event)
        except Exception as exc:
            _broadcast({"type": "result", "result": {"success": False, "error": str(exc)}})
        finally:
            with _run_lock:
                _active_runs.discard(name)
                _running_agents.pop(name, None)
                subs = _run_subscribers.get(name, [])
                # Remove only our own subscriber, not all subscribers
                try:
                    subs.remove(sub_queue)
                except ValueError:
                    pass
                # If no subscribers left for this session, clean up the key
                if not subs:
                    _run_subscribers.pop(name, None)
            # Signal only our own queue with None (done)
            try:
                loop.call_soon_threadsafe(sub_queue.put_nowait, None)
            except Exception:
                pass

    thread = threading.Thread(target=run_agent, daemon=False)  # non-daemon: keeps process alive
    thread.start()

    async def event_generator() -> AsyncIterator[str]:
        global _last_activity
        try:
            while True:
                event = await sub_queue.get()
                if event is None:
                    yield "event: done\ndata: {}\n\n"
                    break
                yield f"data: {json.dumps(event)}\n\n"
        finally:
            with _run_lock:
                try:
                    _run_subscribers[name].remove(sub_queue)
                except ValueError:
                    pass
            _last_activity = time.time()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/sessions/{name}/stream")
async def reconnect_stream(name: str) -> StreamingResponse:
    """Reconnect to an in-progress agent run for this session.

    Returns 404 if no run is currently active. Events are broadcast from
    the point of reconnection — earlier events are already in session history.
    """
    global _last_activity
    sub_queue: asyncio.Queue[Optional[Dict[str, Any]]] = asyncio.Queue(maxsize=500)
    with _run_lock:
        if name not in _active_runs:
            raise HTTPException(status_code=404, detail="No active run for this session")
        _run_subscribers[name].append(sub_queue)
    _last_activity = time.time()

    async def reconnect_generator() -> AsyncIterator[str]:
        global _last_activity
        try:
            while True:
                event = await sub_queue.get()
                if event is None:
                    yield "event: done\ndata: {}\n\n"
                    break
                yield f"data: {json.dumps(event)}\n\n"
        finally:
            with _run_lock:
                try:
                    _run_subscribers[name].remove(sub_queue)
                except ValueError:
                    pass
            _last_activity = time.time()

    return StreamingResponse(
        reconnect_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/models")
def list_models():
    ai = get_ai()
    # Return models per provider so the TUI can always link model → provider.
    # Dynamic providers (ollama, openrouter) are fetched live; static ones
    # (anthropic, openai) keep their hardcoded lists in the TUI.
    by_provider: dict = {}
    _MAX_MODELS = 300  # cap per provider to prevent OOM in TUI
    for name in ("ollama", "openrouter"):
        # Only query if configured/authenticated
        has_key = bool(getattr(ai.config, f"{name}_api_key", ""))
        if name == "ollama":
            has_key = bool(getattr(ai.config, "ollama_configured", False))
        if not has_key:
            by_provider[name] = []
            continue
        try:
            prov = ai.provider_manager.get_provider(name)
            raw = prov.list_models()
            by_provider[name] = raw[:_MAX_MODELS]
        except Exception:
            by_provider[name] = []
    # Legacy flat list: current provider's models (for backward compat)
    try:
        legacy = ai.provider_manager.list_models()
    except Exception:
        legacy = []
    return {
        "by_provider": by_provider,
        "models": legacy[:_MAX_MODELS],
        "current_model": ai.config.default_model,
        "current_provider": ai.config.default_provider,
    }


@app.post("/config/model")
def set_model(req: SetModelRequest):
    ai = get_ai()
    ai.config.default_model = req.model
    if req.provider:
        ai.config.default_provider = req.provider
    ai.refresh_provider()
    try:
        ai.config.save()
    except Exception:
        pass
    return {"model": ai.config.default_model, "provider": ai.config.default_provider}


@app.get("/providers")
def list_providers():
    from .auth import TokenManager
    ai = get_ai()
    tm = TokenManager()
    providers = ai.provider_manager.list_providers()
    result = []
    for name in providers:
        status = tm.list_status().get(name, {})
        has_key = bool(getattr(ai.config, f"{name}_api_key", ""))
        if name == "ollama":
            has_key = bool(getattr(ai.config, "ollama_configured", False))

        # Determine which auth method is currently active for this provider.
        # Lets the TUI show clear ✓ badges next to the configured method.
        # Explicit API keys take priority over stored OAuth tokens.
        auth_method: str | None = None
        if has_key:
            if name == "ollama":
                auth_method = "ollama"
            else:
                key_val = getattr(ai.config, f"{name}_api_key", "") or ""
                if name == "anthropic" and key_val.startswith("sk-ant-oat"):
                    auth_method = "setuptoken"
                else:
                    auth_method = "apikey"
        elif status.get("authenticated"):
            auth_method = "oauth"

        result.append({
            "name": name,
            "active": ai.config.default_provider == name,
            "authenticated": bool(status.get("authenticated") or has_key),
            "oauth": bool(status.get("authenticated")),
            "expired": bool(status.get("expired")),
            "auth_method": auth_method,
        })
    return {"providers": result, "current": ai.config.default_provider}


@app.post("/config/provider")
def set_active_provider(req: SetProviderRequest):
    ai = get_ai()
    ai.config.default_provider = req.provider
    ai.refresh_provider()
    try:
        ai.config.save()
    except Exception:
        pass
    return {"provider": ai.config.default_provider}


@app.post("/config/reasoning")
def set_reasoning_level(req: ReasoningLevelRequest):
    valid = ("none", "low", "medium", "high")
    if req.level not in valid:
        raise HTTPException(status_code=400, detail=f"level must be one of: {', '.join(valid)}")
    ai = get_ai()
    ai.config.reasoning_level = req.level
    try:
        ai.config.save()
    except Exception:
        pass
    return {"reasoning_level": ai.config.reasoning_level}


@app.post("/providers/{name}/apikey")
def set_api_key(name: str, req: ApiKeyRequest):
    ai = get_ai()
    key = req.api_key.strip()
    if name == "openai":
        ai.config.openai_api_key = key
    elif name == "anthropic":
        ai.config.anthropic_api_key = key
    elif name == "openrouter":
        ai.config.openrouter_api_key = key
    elif name == "ollama":
        ai.config.ollama_api_key = key
        ai.config.ollama_configured = True
        _persist_config({"ollama_api_key": key, "ollama_configured": True})
        ai.refresh_provider()
        return {"success": True, "provider": name}
    else:
        raise HTTPException(status_code=400, detail=f"API key not applicable for {name}")
    # Revoke any stored OAuth tokens for this provider so they don't override the new key.
    try:
        from .auth import TokenManager
        TokenManager().revoke(name)
    except Exception:
        pass
    # persist
    import os, json as _json
    cfg_path = os.path.expanduser("~/.config/codrninja/config.json")
    try:
        cfg: dict = {}
        if os.path.exists(cfg_path):
            with open(cfg_path) as f:
                cfg = _json.load(f)
        cfg.setdefault("api_keys", {})[name] = key
        os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
        with open(cfg_path, "w") as f:
            _json.dump(cfg, f, indent=2)
    except Exception:
        pass
    ai.refresh_provider()
    return {"success": True, "provider": name}


@app.post("/sessions/{name}/model")
def set_session_model(name: str, req: SessionModelRequest):
    ai = get_ai()
    if req.provider:
        ai.config.default_provider = req.provider
        ai.refresh_provider()
    ai.config.default_model = req.model
    if req.set_as_default:
        try:
            ai.config.save()
        except Exception:
            pass
    else:
        ai.refresh_provider()
    # Keep the session's state.json in sync with the chosen model.
    try:
        ai.session_manager.update_model(name, ai.config.default_model, ai.config.default_provider)
    except Exception:
        pass
    return {"model": ai.config.default_model, "provider": ai.config.default_provider}


@app.post("/providers/openai/credentials")
def load_openai_credentials():
    """Check if OpenAI OAuth tokens already exist and load them."""
    from .auth import TokenManager
    tm = TokenManager()
    status = tm.list_status().get("openai", {})
    if status.get("authenticated") and not status.get("expired"):
        get_ai().refresh_provider()
        return {"success": True}
    return {"success": False, "error": "No valid OpenAI credentials found"}


@app.post("/providers/ollama/configure")
def configure_ollama(req: OllamaConfigRequest):
    import requests as _req
    url = req.url.rstrip("/")
    try:
        r = _req.get(f"{url}/api/tags", timeout=5)
        r.raise_for_status()
        models = [m["name"] for m in r.json().get("models", [])]
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Cannot reach Ollama at {url}: {e}")
    ai = get_ai()
    ai.config.ollama_url = url
    ai.config.ollama_configured = True
    _persist_config({"ollama_url": url, "ollama_configured": True})
    ai.refresh_provider()
    return {"success": True, "url": url, "models": models}


class OllamaApiKeyRequest(BaseModel):
    api_key: str
    url: str = "https://ollama.com"

@app.post("/providers/ollama/apikey")
def configure_ollama_apikey(req: OllamaApiKeyRequest):
    """Save Ollama Cloud API key and (optionally) custom host."""
    ai = get_ai()
    ai.config.ollama_url = req.url.rstrip("/")
    ai.config.ollama_api_key = req.api_key
    ai.config.ollama_configured = True
    _persist_config({
        "ollama_url": req.url.rstrip("/"),
        "ollama_api_key": req.api_key,
        "ollama_configured": True,
    })
    ai.refresh_provider()
    # Fetch models to verify key works
    try:
        models = ai.provider_manager.list_models()
    except Exception:
        models = []
    return {"success": True, "url": req.url, "models": models}


def _extract_account_id(access_token: str) -> Optional[str]:
    import base64 as _b64, json as _json
    try:
        parts = access_token.split(".")
        if len(parts) >= 2:
            padded = parts[1] + "=" * (4 - len(parts[1]) % 4)
            payload = _json.loads(_b64.urlsafe_b64decode(padded))
            return payload.get("sub") or payload.get("account_id") or payload.get("accountId")
    except Exception:
        pass
    return None


def _persist_config(updates: dict):
    import os, json as _json
    cfg_path = os.path.expanduser("~/.config/codrninja/config.json")
    try:
        cfg: dict = {}
        if os.path.exists(cfg_path):
            with open(cfg_path) as f:
                cfg = _json.load(f)
        cfg.update(updates)
        os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
        with open(cfg_path, "w") as f:
            _json.dump(cfg, f, indent=2)
    except Exception:
        pass


def _probe_ollama(url: str):
    """Return list of model names or raise HTTPException."""
    import requests as _req
    try:
        r = _req.get(f"{url}/api/tags", timeout=5)
        r.raise_for_status()
        return [m["name"] for m in r.json().get("models", [])]
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Cannot reach Ollama at {url}: {e}")


def _get_ollama_servers() -> list:
    import json as _json, os
    cfg_path = os.path.expanduser("~/.config/codrninja/config.json")
    try:
        if os.path.exists(cfg_path):
            cfg = _json.loads(open(cfg_path).read())
            servers = cfg.get("ollama_servers", [])
            if servers:
                return servers
    except Exception:
        pass
    # Fall back to ollama_url as a single-server entry
    url = get_ai().config.ollama_url
    if url:
        return [{"url": url, "active": True}]
    return []


def _save_ollama_servers(servers: list):
    _persist_config({"ollama_servers": servers})
    # also set ollama_url to first active server for backwards compat
    active = next((s["url"] for s in servers if s.get("active")), None)
    if active:
        ai = get_ai()
        ai.config.ollama_url = active
        _persist_config({"ollama_url": active})
        ai.refresh_provider()


@app.get("/providers/ollama/servers")
def list_ollama_servers():
    import requests as _req
    from concurrent.futures import ThreadPoolExecutor, as_completed

    servers = _get_ollama_servers()
    primary = ""
    for s in servers:
        if s.get("active") and not primary:
            primary = s.get("url", "")

    def probe(s):
        url = s.get("url", "")
        active = bool(s.get("active"))
        try:
            r = _req.get(f"{url}/api/tags", timeout=2)
            r.raise_for_status()
            models = [m["name"] for m in r.json().get("models", [])]
            return {"url": url, "active": active, "online": True, "models": models}
        except Exception:
            return {"url": url, "active": active, "online": False, "models": []}

    result = []
    if servers:
        with ThreadPoolExecutor(max_workers=min(len(servers), 8)) as pool:
            futures = {pool.submit(probe, s): s for s in servers}
            ordered = {id(s): None for s in servers}
            for fut in as_completed(futures):
                ordered[id(futures[fut])] = fut.result()
            result = [ordered[id(s)] for s in servers if ordered[id(s)] is not None]

    return {"servers": result, "primary": primary}


class OllamaServerRequest(BaseModel):
    url: str


@app.post("/providers/ollama/add-server")
def add_ollama_server(req: OllamaServerRequest):
    url = req.url.rstrip("/")
    models = _probe_ollama(url)
    servers = _get_ollama_servers()
    if not any(s["url"] == url for s in servers):
        servers.append({"url": url, "active": len(servers) == 0})
    _save_ollama_servers(servers)
    ai = get_ai()
    ai.config.ollama_configured = True
    _persist_config({"ollama_configured": True})
    return {"success": True, "url": url, "models": models}


@app.post("/providers/ollama/remove-server")
def remove_ollama_server(req: OllamaServerRequest):
    url = req.url.rstrip("/")
    servers = [s for s in _get_ollama_servers() if s["url"] != url]
    if servers and not any(s.get("active") for s in servers):
        servers[0]["active"] = True
    _save_ollama_servers(servers)
    return {"success": True}


@app.post("/providers/ollama/toggle-server")
def toggle_ollama_server(req: OllamaServerRequest):
    url = req.url.rstrip("/")
    servers = _get_ollama_servers()
    for s in servers:
        s["active"] = s["url"] == url
    _save_ollama_servers(servers)
    active = [s["url"] for s in servers if s.get("active")]
    return {"success": True, "active": active}


@app.post("/providers/openai/oauth")
async def run_openai_oauth() -> StreamingResponse:
    """Run OpenAI OAuth flow via SSE — streams url → waiting → success/error."""
    async def generator() -> AsyncIterator[str]:
        loop = asyncio.get_running_loop()
        queue: asyncio.Queue[Optional[Dict[str, Any]]] = asyncio.Queue()

        def run_flow():
            global _active_oauth_cb
            from .auth import OAuthCallbackServer, PKCEHandler, TokenManager
            from .oauth_providers import OpenAIOAuth
            import webbrowser
            provider = OpenAIOAuth()
            # On SSH servers there is no browser session — simplified flow causes unknown_error
            is_ssh = bool(os.environ.get("SSH_CLIENT") or os.environ.get("SSH_TTY") or os.environ.get("SSH_CONNECTION"))
            if is_ssh:
                provider.extra_auth_params = {k: v for k, v in provider.extra_auth_params.items() if k != "codex_cli_simplified_flow"}
            cb = OAuthCallbackServer(
                host=OpenAIOAuth.CALLBACK_HOST,
                port=OpenAIOAuth.CALLBACK_PORT,
                callback_path=OpenAIOAuth.CALLBACK_PATH,
            )
            callback_url = cb.start()
            _active_oauth_cb = cb
            verifier = PKCEHandler.generate_verifier()
            challenge = PKCEHandler.generate_challenge(verifier)
            state = PKCEHandler.generate_state()
            auth_url = provider.build_authorization_url(callback_url, challenge, state)
            url_file = "/tmp/codrninja_auth.url"
            try:
                with open(url_file, "w") as _f:
                    _f.write(auth_url + "\n")
            except Exception:
                url_file = None
            loop.call_soon_threadsafe(queue.put_nowait, {"type": "url", "url": auth_url, "url_file": url_file})
            try:
                webbrowser.open(auth_url)
            except Exception:
                pass
            loop.call_soon_threadsafe(queue.put_nowait, {"type": "waiting"})
            result = cb.wait_for_callback()
            cb.shutdown()
            if result.error:
                loop.call_soon_threadsafe(queue.put_nowait, {"type": "error", "error": result.error_description or result.error})
            elif not result.code or result.state != state:
                loop.call_soon_threadsafe(queue.put_nowait, {"type": "error", "error": "Invalid OAuth response"})
            else:
                try:
                    tokens = provider.exchange_code(result.code, verifier, callback_url)
                    if not tokens.get("account_id"):
                        tokens["account_id"] = _extract_account_id(tokens.get("access_token", "")) or ""
                    TokenManager().store_tokens("openai", tokens)
                    get_ai().refresh_provider()
                    loop.call_soon_threadsafe(queue.put_nowait, {"type": "success"})
                except Exception as exc:
                    loop.call_soon_threadsafe(queue.put_nowait, {"type": "error", "error": str(exc)})
            _active_oauth_cb = None
            loop.call_soon_threadsafe(queue.put_nowait, None)

        threading.Thread(target=run_flow, daemon=True).start()
        while True:
            event = await queue.get()
            if event is None:
                yield "event: done\ndata: {}\n\n"
                break
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(generator(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


class OAuthCallbackRequest(BaseModel):
    url: str


@app.post("/providers/openai/oauth/callback")
def submit_openai_oauth_callback(req: OAuthCallbackRequest):
    """Accept a manually pasted OAuth callback URL and inject it into the running flow."""
    from urllib.parse import urlparse, parse_qs
    if _active_oauth_cb is None:
        raise HTTPException(status_code=404, detail="No active OAuth session")
    parsed = urlparse(req.url)
    qs = parse_qs(parsed.query, keep_blank_values=True)
    error = (qs.get("error") or [None])[0]
    code = (qs.get("code") or [None])[0]
    state = (qs.get("state") or [None])[0]
    _active_oauth_cb.inject_callback(code=code, state=state, error=error)
    return {"success": True}


@app.post("/providers/anthropic/oauth")
async def run_anthropic_oauth() -> StreamingResponse:
    """Run Anthropic OAuth PKCE browser flow."""
    async def generator() -> AsyncIterator[str]:
        loop = asyncio.get_running_loop()
        queue: asyncio.Queue[Optional[Dict[str, Any]]] = asyncio.Queue()

        def run_flow():
            # Full PKCE browser flow
            from .auth import OAuthCallbackServer, PKCEHandler, TokenManager
            from .oauth_providers import AnthropicOAuth
            import webbrowser
            provider = AnthropicOAuth()
            cb = OAuthCallbackServer()
            callback_url = cb.start()
            verifier = PKCEHandler.generate_verifier()
            challenge = PKCEHandler.generate_challenge(verifier)
            state = PKCEHandler.generate_state()
            auth_url = provider.build_authorization_url(callback_url, challenge, state)
            loop.call_soon_threadsafe(queue.put_nowait, {"type": "url", "url": auth_url})
            try:
                webbrowser.open(auth_url)
            except Exception:
                pass
            loop.call_soon_threadsafe(queue.put_nowait, {"type": "waiting"})
            result = cb.wait_for_callback()
            cb.shutdown()
            if result.error:
                loop.call_soon_threadsafe(queue.put_nowait, {"type": "error", "error": result.error_description or result.error})
            elif not result.code or result.state != state:
                loop.call_soon_threadsafe(queue.put_nowait, {"type": "error", "error": "Invalid OAuth response"})
            else:
                try:
                    tokens = provider.exchange_code(result.code, verifier, callback_url)
                    TokenManager().store_tokens("anthropic", tokens)
                    get_ai().refresh_provider()
                    loop.call_soon_threadsafe(queue.put_nowait, {"type": "success"})
                except Exception as exc:
                    loop.call_soon_threadsafe(queue.put_nowait, {"type": "error", "error": str(exc)})
            loop.call_soon_threadsafe(queue.put_nowait, None)

        threading.Thread(target=run_flow, daemon=True).start()
        while True:
            event = await queue.get()
            if event is None:
                yield "event: done\ndata: {}\n\n"
                break
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(generator(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.post("/run/exec")
def run_exec(req: ExecRequest):
    result = get_ai().tools.execute_command(req.command)
    return {"success": result.success, "output": result.output, "error": result.error}


@app.post("/run/search")
def run_search(req: SearchRequest):
    result = get_ai().tools.web_search(req.query)
    return {"success": result.success, "output": result.output, "error": result.error}


@app.post("/run/fetch")
def run_fetch(req: FetchRequest):
    result = get_ai().tools.web_fetch(req.url)
    return {"success": result.success, "output": result.output, "error": result.error}


@app.post("/run/commit")
def run_commit(req: CommitRequest):
    import shlex
    get_ai().tools.execute_command("git add -A")
    result = get_ai().tools.execute_command(f"git commit -m {shlex.quote(req.message)}")
    return {"success": result.success, "output": result.output, "error": result.error}


@app.post("/run/test")
def run_test(req: TestRequest):
    result = get_ai().tools.execute_command(req.command)
    return {"success": result.success, "output": result.output, "error": result.error}


@app.get("/version")
def get_version():
    from codrninja import __version__
    return {"version": __version__}


@app.post("/shutdown")
@app.get("/shutdown")
async def shutdown_server():
    """Ask the server to exit cleanly. Used by the CLI to kill servers from any installation."""
    async def _do_exit():
        await asyncio.sleep(0.1)
        os._exit(0)
    asyncio.create_task(_do_exit())
    return {"ok": True}


@app.post("/providers/{provider}/oauth/browser")
def open_oauth_browser(provider: str):
    """Open the browser to the provider's OAuth/API key page."""
    import subprocess, sys
    urls = {
        "openai":      "https://platform.openai.com/api-keys",
        "anthropic":   "https://console.anthropic.com/settings/keys",
        "openrouter":  "https://openrouter.ai/keys",
    }
    url = urls.get(provider, "")
    if url:
        try:
            if sys.platform == "darwin":
                subprocess.Popen(["open", url])
            elif sys.platform.startswith("linux"):
                subprocess.Popen(["xdg-open", url])
            else:
                subprocess.Popen(["start", url], shell=True)
        except Exception:
            pass
    return {"success": bool(url), "url": url}


@app.post("/permissions/mode")
def set_permission_mode(req: PermissionModeRequest):
    from .permissions import PermissionManager
    pm = PermissionManager()
    try:
        pm.set_mode(req.mode)
        pm.save_config()
        # Propagate to any running agents so the change takes effect immediately
        with _run_lock:
            for agent in list(_running_agents.values()):
                try:
                    agent.permissions.set_mode(req.mode)
                except Exception:
                    pass
        return {"success": True, "mode": req.mode}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/sessions/{name}/permission_respond")
def permission_respond(name: str, req: PermissionRespondRequest):
    with _run_lock:
        agent = _running_agents.get(name)
    if agent is None:
        raise HTTPException(status_code=404, detail="No active run for this session")
    agent.resolve_permission(req.decision)
    return {"success": True}


@app.post("/sessions/{name}/stop")
def stop_session(name: str):
    """Signal the running agent for this session to stop at the next safe point."""
    with _run_lock:
        agent = _running_agents.get(name)
        if agent:
            agent._stop_requested = True
    return {"ok": True}




@app.on_event("startup")
async def _startup_ollama_autodetect():
    """If provider is ollama and the configured model doesn't exist there, pick the first available one."""
    try:
        ai = get_ai()
        if ai.config.default_provider != "ollama":
            return
        bad = ai.config.default_model in ("", "codellama", None)
        if not bad:
            return
        import requests as _req
        url = (ai.config.ollama_url or "http://localhost:11434").rstrip("/")
        r = _req.get(f"{url}/api/tags", timeout=3)
        r.raise_for_status()
        models = [m["name"] for m in r.json().get("models", [])]
        if models:
            ai.config.default_model = models[0]
            try:
                ai.config.save()
            except Exception:
                pass
    except Exception:
        pass


def _write_version_stamp(port: int):
    """Write current __version__ to a stamp file so the CLI can detect stale servers."""
    try:
        from codrninja import __version__
        stamp = os.path.expanduser(f"~/.codrninja/server-{port}.ver")
        os.makedirs(os.path.dirname(stamp), exist_ok=True)
        with open(stamp, "w") as f:
            f.write(__version__)
    except Exception:
        pass


def run_server(host: str = "127.0.0.1", port: int = 7384):
    import uvicorn
    _write_version_stamp(port)
    uvicorn.run(app, host=host, port=port, log_level="warning")
