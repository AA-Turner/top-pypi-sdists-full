"""HTTP + WebSocket routes for the Bingo web IDE.

All routes here sit behind the token/origin middleware in server.py. The WS
endpoint uses a raw Starlette WebSocketRoute (not @app.websocket) to skip
FastAPI's dependency-injection layer, which otherwise rejects the handshake
with code=1008 → 403 when no dependencies are declared.
"""
from __future__ import annotations

import asyncio
import json

from fastapi import Request, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse

from .security import safe_resolve


def register(app, session, port: int) -> None:
    from .server import _serve_index

    @app.get("/")
    async def index():
        return HTMLResponse(_serve_index(port, session.config.lang))

    _register_config(app, session)
    _register_files(app, session)
    _register_chat(app, session)
    _register_commands(app, session)
    _register_automation(app, session)
    _register_ws(app, session)


def _register_commands(app, session) -> None:

    @app.get("/api/commands")
    async def list_commands():
        from ..lang.strings import get_slash_commands
        cmds = get_slash_commands(session.config.lang)
        return JSONResponse({"commands": [
            {"cmd": c, "desc": d} for c, d in cmds]})

    @app.post("/api/command")
    async def run_command(request: Request):
        body = await request.json()
        name = str(body.get("name", ""))
        arg = str(body.get("arg", ""))
        if not name.startswith("/"):
            return JSONResponse({"ok": False, "error": "not a command"},
                                status_code=400)
        return JSONResponse(session.run_command(name, arg))


def _register_config(app, session) -> None:

    @app.get("/api/config")
    async def get_config():
        from ..models.registry import BUILTIN_PROVIDERS, get_provider_label
        cfg = session.config
        active = cfg.get_active_model_config()
        return JSONResponse({
            "lang": cfg.lang,
            "root": str(session.root),
            "active_model": active.display_name() if active else "",
            "models": [
                {"name": m.display_name(), "provider": m.provider,
                 "model": m.model, "alias": m.alias}
                for m in cfg.models
            ],
            "providers": [
                {"id": pid, "label": get_provider_label(info, cfg.lang),
                 "base_url": info.get("base_url", ""),
                 "default_model": info.get("default_model", ""),
                 "models": info.get("models", [])}
                for pid, info in BUILTIN_PROVIDERS.items()
            ],
        })

    @app.post("/api/lang")
    async def set_lang(request: Request):
        body = await request.json()
        lang = str(body.get("lang", "en"))
        if lang in ("en", "ko", "zh"):
            session.config.lang = lang
            session.config.save()
        return JSONResponse({"lang": session.config.lang})

    @app.post("/api/model")
    async def set_model(request: Request):
        body = await request.json()
        name = str(body.get("name", ""))
        for m in session.config.models:
            if m.display_name() == name:
                session.config.active_model = name
                session.config.save()
                return JSONResponse({"active_model": name})
        return JSONResponse({"error": "unknown model"}, status_code=400)

    @app.post("/api/model/add")
    async def add_model(request: Request):
        from ..models.registry import BUILTIN_PROVIDERS
        from ..models.base import ModelConfig
        body = await request.json()
        provider = str(body.get("provider", "")).strip()
        api_key = str(body.get("api_key", "")).strip()
        info = BUILTIN_PROVIDERS.get(provider)
        if info is None:
            return JSONResponse({"error": "unknown provider"}, status_code=400)
        base_url = str(body.get("base_url", "")).strip() or info.get("base_url", "")
        model_name = str(body.get("model", "")).strip() or info.get("default_model", "")
        alias = str(body.get("alias", "")).strip()
        if not model_name or not base_url:
            return JSONResponse({"error": "model and base_url required"},
                                status_code=400)
        if not api_key:
            return JSONResponse({"error": "api_key required"}, status_code=400)
        cfg = ModelConfig(provider=provider, model=model_name,
                          api_key=api_key, base_url=base_url, alias=alias)
        session.config.add_model(cfg)
        session.config.active_model = cfg.display_name()
        session.config.save()
        return JSONResponse({"ok": True, "active_model": cfg.display_name()})

    @app.post("/api/model/delete")
    async def delete_model(request: Request):
        body = await request.json()
        name = str(body.get("name", "")).strip()
        if not session.config.remove_model(name):
            return JSONResponse({"error": "unknown model"}, status_code=400)
        session.config.save()
        active = session.config.get_active_model_config()
        return JSONResponse({"ok": True,
                             "active_model": active.display_name() if active else ""})


_MAX_READ = 2_000_000  # 2 MB — editors don't need more, and it caps blast radius


def _register_files(app, session) -> None:

    @app.get("/api/files")
    async def list_files(path: str = ""):
        return JSONResponse({"entries": session.list_tree(path)})

    @app.get("/api/file")
    async def read_file(path: str):
        target = safe_resolve(session.root, path)
        if target is None or not target.is_file():
            return JSONResponse({"error": "not found"}, status_code=404)
        try:
            if target.stat().st_size > _MAX_READ:
                return JSONResponse({"error": "file too large"}, status_code=413)
            text = target.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            return JSONResponse({"error": str(exc)}, status_code=500)
        return JSONResponse({"path": path, "text": text})

    @app.post("/api/file")
    async def write_file(request: Request):
        body = await request.json()
        target = safe_resolve(session.root, str(body.get("path", "")))
        if target is None:
            return JSONResponse({"error": "bad path"}, status_code=400)
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(str(body.get("text", "")), encoding="utf-8")
        except OSError as exc:
            return JSONResponse({"error": str(exc)}, status_code=500)
        return JSONResponse({"ok": True, "path": body.get("path", "")})


def _register_chat(app, session) -> None:

    @app.post("/api/dev/ask")
    async def dev_ask(request: Request):
        body = await request.json()
        session.dev_ask(
            str(body.get("message", "")),
            str(body.get("file_name", "")),
            str(body.get("file_text", "")),
        )
        return JSONResponse({"ok": True})

    @app.post("/api/pentest/start")
    async def pentest_start(request: Request):
        body = await request.json()
        target = session.pentest_start(str(body.get("message", "")))
        return JSONResponse({"ok": bool(target), "target": target})

    @app.post("/api/pentest/hint")
    async def pentest_hint(request: Request):
        body = await request.json()
        session.pentest_hint(str(body.get("text", "")))
        return JSONResponse({"ok": True})

    @app.post("/api/pentest/stop")
    async def pentest_stop():
        session.pentest_stop()
        return JSONResponse({"ok": True})

    @app.get("/api/history")
    async def get_history():
        return JSONResponse({"turns": session.history.context(limit=400)})

    @app.post("/api/history/clear")
    async def clear_history():
        session.history.clear()
        return JSONResponse({"ok": True})

    @app.get("/api/findings")
    async def get_findings():
        return JSONResponse({"findings": session.findings, "stats": session.stats})


def _register_automation(app, session) -> None:

    @app.post("/api/scan")
    async def scan(request: Request):
        body = await request.json()
        session.run_scan(str(body.get("target", "")))
        return JSONResponse({"ok": True})

    @app.post("/api/waf")
    async def waf(request: Request):
        body = await request.json()
        session.run_waf(str(body.get("target", "")))
        return JSONResponse({"ok": True})


def _register_ws(app, session) -> None:

    async def ws_endpoint(websocket: WebSocket):
        # Token check on the handshake (query param — WS can't set headers).
        from .security import verify_token

        if not verify_token(websocket.query_params.get("token")):
            await websocket.close(code=1008)
            return
        try:
            await websocket.accept()
        except Exception:
            return

        session.set_loop(asyncio.get_running_loop())
        q: asyncio.Queue = asyncio.Queue(maxsize=1000)
        session.attach(q)
        try:
            # Replay existing findings/stats to the freshly connected client.
            for f in session.findings:
                await websocket.send_text(json.dumps({"type": "finding", "data": f}))
            if session.stats:
                await websocket.send_text(
                    json.dumps({"type": "stats", "data": session.stats}))
            while True:
                try:
                    msg = await asyncio.wait_for(q.get(), timeout=15.0)
                    await websocket.send_text(json.dumps(msg))
                except asyncio.TimeoutError:
                    await websocket.send_text(json.dumps({"type": "ping"}))
        except Exception:
            pass
        finally:
            session.detach(q)

    app.router.add_websocket_route("/ws", ws_endpoint)
