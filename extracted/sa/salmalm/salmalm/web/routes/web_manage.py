"""Web Manage routes mixin."""

import logging
import os
import sys
import time

from salmalm.core import audit_log

from salmalm.constants import DATA_DIR, VERSION, WORKSPACE_DIR, BASE_DIR  # noqa: F401
from salmalm.security.crypto import vault, log  # noqa: F401
from salmalm.web.auth import extract_auth, auth_manager  # noqa: F401

log = logging.getLogger(__name__)


def _systemd_restart_after_upgrade() -> None:
    """Schedule a `systemctl --user restart salmalm` 2s after upgrade completes.

    Non-blocking: spawns a background thread so the HTTP response returns first.
    Silently no-ops if systemd is unavailable or service isn't installed.
    """
    import threading
    import subprocess
    import time

    def _restart():
        time.sleep(2)  # Let the HTTP response flush to client
        try:
            r = subprocess.run(
                ["systemctl", "--user", "is-active", "salmalm.service"],
                capture_output=True, text=True, timeout=5,
            )
            if r.stdout.strip() == "active":
                subprocess.run(
                    ["systemctl", "--user", "restart", "salmalm.service"],
                    capture_output=True, timeout=10,
                )
                log.info("[UPDATE] systemd service restarted with new binary")
        except Exception as e:
            log.debug(f"[UPDATE] systemd restart skipped: {e}")

    threading.Thread(target=_restart, daemon=True, name="systemd-restart").start()


class ManageMixin:
    GET_ROUTES = {
        "/api/backup": "_get_backup",
    }
    POST_ROUTES = {
        "/api/do-update": "_post_api_do_update",
        "/api/restart": "_post_api_restart",
        "/api/update": "_post_api_update",
        "/api/persona/switch": "_post_api_persona_switch",
        "/api/persona/create": "_post_api_persona_create",
        "/api/persona/delete": "_post_api_persona_delete",
        "/api/stt": "_post_api_stt",
        "/api/agent/sync": "_post_api_agent_sync",
        "/api/queue/mode": "_post_api_queue_mode",
        "/api/soul": "_post_api_soul",
        "/api/agents": "_post_api_agents",
        "/api/hooks": "_post_api_hooks",
        "/api/plugins/manage": "_post_api_plugins_manage",
        "/api/groups": "_post_api_groups",
        "/api/paste/detect": "_post_api_paste_detect",
        "/api/vault": "_post_api_vault",
        "/api/cooldowns/reset": "_post_api_cooldowns_reset",
        "/api/backup/restore": "_post_api_backup_restore",
        "/api/presence": "_post_api_presence",
        "/api/node/execute": "_post_api_node_execute",
    }

    def _get_backup(self):
        """GET /api/backup — download ~/SalmAlm as zip."""
        if not self._require_auth("admin"):
            return
        import zipfile
        import io
        import time as _time

        buf = io.BytesIO()
        skip_ext = {".pyc"}
        skip_dirs = {"__pycache__", ".git", "node_modules"}
        max_file_size = 50 * 1024 * 1024  # 50MB

        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(str(DATA_DIR)):
                dirs[:] = [d for d in dirs if d not in skip_dirs]
                for fname in files:
                    fpath = os.path.join(root, fname)
                    if any(fname.endswith(e) for e in skip_ext):
                        continue
                    try:
                        if os.path.getsize(fpath) > max_file_size:
                            continue
                    except OSError:
                        continue
                    arcname = os.path.relpath(fpath, str(DATA_DIR))
                    zf.write(fpath, arcname)

        body = buf.getvalue()
        ts = _time.strftime("%Y%m%d_%H%M%S")
        self.send_response(200)
        self.send_header("Content-Type", "application/zip")
        self.send_header("Content-Disposition", f'attachment; filename="salmalm_backup_{ts}.zip"')
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

# ── FastAPI router ────────────────────────────────────────────────────────────
import asyncio as _asyncio
from fastapi import APIRouter as _APIRouter, Request as _Request, Depends as _Depends, Query as _Query
from fastapi.responses import JSONResponse as _JSON, Response as _Response, HTMLResponse as _HTML, StreamingResponse as _SR, RedirectResponse as _RR
from salmalm.web.fastapi_deps import require_auth as _auth, optional_auth as _optauth

router = _APIRouter()

@router.get("/api/backup")
async def get_backup(request: _Request, _u=_Depends(_auth)):
    import zipfile, io, time as _time, os
    from salmalm.constants import DATA_DIR
    if _u.get("role") != "admin":
        return _JSON(content={"error": "Admin access required"}, status_code=403)
    buf = io.BytesIO()
    skip_ext = {".pyc"}
    skip_dirs = {"__pycache__", ".git", "node_modules"}
    max_file_size = 50 * 1024 * 1024
    def _make_zip():
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(str(DATA_DIR)):
                dirs[:] = [d for d in dirs if d not in skip_dirs]
                for fname in files:
                    fpath = os.path.join(root, fname)
                    if any(fname.endswith(e) for e in skip_ext):
                        continue
                    try:
                        if os.path.getsize(fpath) > max_file_size:
                            continue
                    except OSError:
                        continue
                    arcname = os.path.relpath(fpath, str(DATA_DIR))
                    zf.write(fpath, arcname)
        return buf.getvalue()
    body = await _asyncio.to_thread(_make_zip)
    ts = _time.strftime("%Y%m%d_%H%M%S")
    return _Response(content=body, media_type="application/zip",
                     headers={"Content-Disposition": f'attachment; filename="salmalm_backup_{ts}.zip"',
                              "Content-Length": str(len(body))})

@router.post("/api/do-update")
async def post_do_update(request: _Request, _u=_Depends(_auth)):
    import subprocess, sys, shutil
    from salmalm.core import audit_log
    if _u.get("role") != "admin":
        return _JSON(content={"error": "Admin access required"}, status_code=403)
    if request.client and request.client.host not in ("127.0.0.1", "::1", "localhost"):
        return _JSON(content={"error": "Update only allowed from localhost"}, status_code=403)
    try:
        _use_pipx = shutil.which("pipx") is not None
        _update_cmd = ["pipx", "install", "salmalm", "--force"] if _use_pipx else [sys.executable, "-m", "pip", "install", "--upgrade", "--no-cache-dir", "salmalm"]
        result = await _asyncio.to_thread(lambda: subprocess.run(_update_cmd, capture_output=True, text=True, timeout=120))
        if result.returncode == 0:
            ver_result = await _asyncio.to_thread(lambda: subprocess.run([sys.executable, "-c", "from salmalm.constants import VERSION; print(VERSION)"], capture_output=True, text=True, timeout=10))
            new_ver = ver_result.stdout.strip() or "?"
            audit_log("update", f"upgraded to v{new_ver}")
            from salmalm.web.routes.web_manage import _systemd_restart_after_upgrade
            _systemd_restart_after_upgrade()
            return _JSON(content={"ok": True, "version": new_ver, "output": result.stdout[-200:]})
        return _JSON(content={"ok": False, "error": result.stderr[-200:]})
    except Exception as e:
        return _JSON(content={"ok": False, "error": "Internal server error"})

@router.post("/api/restart")
async def post_restart(request: _Request, _u=_Depends(_auth)):
    import sys, threading, time, os
    from salmalm.core import audit_log
    if _u.get("role") != "admin":
        return _JSON(content={"error": "Admin access required"}, status_code=403)
    if request.client and request.client.host not in ("127.0.0.1", "::1", "localhost"):
        return _JSON(content={"error": "Restart only allowed from localhost"}, status_code=403)
    audit_log("restart", "user-initiated restart")
    def _do_restart():
        time.sleep(0.5)
        os.execv(sys.executable, [sys.executable] + sys.argv)
    threading.Thread(target=_do_restart, daemon=True).start()
    return _JSON(content={"ok": True, "message": "Restarting..."})

@router.post("/api/update")
async def post_update(request: _Request, _u=_Depends(_auth)):
    import subprocess, sys, shutil
    from salmalm.core import audit_log
    if _u.get("role") != "admin":
        return _JSON(content={"error": "Admin access required"}, status_code=403)
    if request.client and request.client.host not in ("127.0.0.1", "::1", "localhost"):
        return _JSON(content={"error": "Update only allowed from localhost"}, status_code=403)
    try:
        _use_pipx = shutil.which("pipx") is not None
        _update_cmd = ["pipx", "install", "salmalm", "--force"] if _use_pipx else [sys.executable, "-m", "pip", "install", "--upgrade", "--no-cache-dir", "salmalm"]
        result = await _asyncio.to_thread(lambda: subprocess.run(_update_cmd, capture_output=True, text=True, timeout=120))
        if result.returncode == 0:
            ver_result = await _asyncio.to_thread(lambda: subprocess.run([sys.executable, "-c", "from salmalm.constants import VERSION; print(VERSION)"], capture_output=True, text=True, timeout=10))
            new_ver = ver_result.stdout.strip() or "?"
            audit_log("update", f"upgraded to v{new_ver}")
            from salmalm.web.routes.web_manage import _systemd_restart_after_upgrade
            _systemd_restart_after_upgrade()
            return _JSON(content={"ok": True, "version": new_ver, "output": result.stdout[-200:]})
        return _JSON(content={"ok": False, "error": result.stderr[-200:]})
    except Exception as e:
        return _JSON(content={"ok": False, "error": "Internal server error"})

@router.post("/api/persona/switch")
async def post_persona_switch(request: _Request, _u=_Depends(_auth)):
    body = await request.json()
    session_id = body.get("session_id", request.headers.get("x-session-id", "web"))
    name = body.get("name", "")
    if not name:
        return _JSON(content={"error": "name required"}, status_code=400)
    from salmalm.core.prompt import switch_persona
    content = switch_persona(session_id, name)
    if content is None:
        return _JSON(content={"error": f'Persona "{name}" not found'}, status_code=404)
    return _JSON(content={"ok": True, "name": name, "content": content})

@router.post("/api/persona/create")
async def post_persona_create(request: _Request, _u=_Depends(_auth)):
    body = await request.json()
    name = body.get("name", "")
    content = body.get("content", "")
    if not name or not content:
        return _JSON(content={"error": "name and content required"}, status_code=400)
    from salmalm.core.prompt import create_persona
    ok = create_persona(name, content)
    return _JSON(content={"ok": True} if ok else {"error": "Invalid persona name"}, status_code=200 if ok else 400)

@router.post("/api/persona/delete")
async def post_persona_delete(request: _Request, _u=_Depends(_auth)):
    body = await request.json()
    name = body.get("name", "")
    if not name:
        return _JSON(content={"error": "name required"}, status_code=400)
    from salmalm.core.prompt import delete_persona
    ok = delete_persona(name)
    return _JSON(content={"ok": True} if ok else {"error": "Cannot delete built-in persona or not found"}, status_code=200 if ok else 400)

@router.post("/api/stt")
async def post_stt(request: _Request, _u=_Depends(_auth)):
    body = await request.json()
    audio_b64 = body.get("audio_base64", "")
    lang = body.get("language", "ko")
    if not audio_b64:
        return _JSON(content={"error": "No audio data"}, status_code=400)
    try:
        from salmalm.tools.tool_handlers import execute_tool
        result = await _asyncio.to_thread(execute_tool, "stt", {"audio_base64": audio_b64, "language": lang})
        text = result.replace("🎤 Transcription:\n", "") if isinstance(result, str) else ""
        return _JSON(content={"ok": True, "text": text})
    except Exception as e:
        return _JSON(content={"ok": False, "error": "Internal server error"}, status_code=500)

@router.post("/api/agent/sync")
async def post_agent_sync(request: _Request, _u=_Depends(_auth)):
    import json as _json
    from salmalm.constants import DATA_DIR, BASE_DIR
    body = await request.json()
    action = body.get("action", "export")
    if action == "export":
        export_data = {}
        soul_path = DATA_DIR / "soul.md"
        if soul_path.exists():
            export_data["soul"] = soul_path.read_text(encoding="utf-8")
        config_path = DATA_DIR / "config.json"
        if config_path.exists():
            export_data["config"] = _json.loads(config_path.read_text(encoding="utf-8"))
        routing_path = DATA_DIR / "routing.json"
        if routing_path.exists():
            export_data["routing"] = _json.loads(routing_path.read_text(encoding="utf-8"))
        memory_dir = BASE_DIR / "memory"
        if memory_dir.exists():
            export_data["memory"] = {}
            for f in memory_dir.glob("*"):
                if f.is_file():
                    export_data["memory"][f.name] = f.read_text(encoding="utf-8")
        return _JSON(content={"ok": True, "data": export_data})
    return _JSON(content={"ok": False, "error": "Unknown action"}, status_code=400)

@router.post("/api/queue/mode")
async def post_queue_mode(request: _Request, _u=_Depends(_auth)):
    from salmalm.features.queue import set_queue_mode
    body = await request.json()
    mode = body.get("mode", "collect")
    session_id = body.get("session_id", "web")
    try:
        result = set_queue_mode(session_id, mode)
        return _JSON(content={"ok": True, "message": result})
    except ValueError as e:
        return _JSON(content={"ok": False, "error": str(e)}, status_code=400)

@router.post("/api/soul")
async def post_soul(request: _Request, _u=_Depends(_auth)):
    body = await request.json()
    content = body.get("content", "")
    if len(content) > 100 * 1024:
        return _JSON(content={"error": "Content too large (max 100KB)"}, status_code=400)
    from salmalm.core.prompt import set_user_soul, reset_user_soul
    if content.strip():
        set_user_soul(content)
        return _JSON(content={"ok": True, "message": "SOUL.md saved"})
    else:
        reset_user_soul()
        return _JSON(content={"ok": True, "message": "SOUL.md reset to default"})

@router.post("/api/agents")
async def post_agents_manage(request: _Request, _u=_Depends(_auth)):
    # BUG-CJ fix: agent create/delete/bind are destructive filesystem ops — admin only
    if _u.get("role") != "admin":
        return _JSON(content={"error": "Admin access required"}, status_code=403)
    from salmalm.features.agents import agent_manager
    body = await request.json()
    action = body.get("action", "")
    if action == "create":
        result = agent_manager.create(body.get("id", ""), body.get("display_name", ""))
        return _JSON(content={"ok": "✅" in result, "message": result})
    elif action == "delete":
        result = agent_manager.delete(body.get("id", ""))
        return _JSON(content={"ok": True, "message": result})
    elif action == "bind":
        result = agent_manager.bind(body.get("chat_key", ""), body.get("agent_id", ""))
        return _JSON(content={"ok": True, "message": result})
    elif action == "switch":
        result = agent_manager.switch(body.get("chat_key", ""), body.get("agent_id", ""))
        return _JSON(content={"ok": True, "message": result})
    return _JSON(content={"error": "Unknown action. Use: create, delete, bind, switch"}, status_code=400)

@router.post("/api/hooks")
async def post_hooks(request: _Request, _u=_Depends(_auth)):
    if _u.get("role") != "admin":  # Hooks execute shell commands — admin only
        return _JSON(content={"error": "Admin access required"}, status_code=403)
    from salmalm.features.hooks import hook_manager
    body = await request.json()
    action = body.get("action", "")
    if action == "add":
        result = hook_manager.add_hook(body.get("event", ""), body.get("command", ""))
        return _JSON(content={"ok": True, "message": result})
    elif action == "remove":
        result = hook_manager.remove_hook(body.get("event", ""), body.get("index", 0))
        return _JSON(content={"ok": True, "message": result})
    elif action == "test":
        result = hook_manager.test_hook(body.get("event", ""))
        return _JSON(content={"ok": True, "message": result})
    elif action == "reload":
        hook_manager.reload()
        return _JSON(content={"ok": True, "message": "🔄 Hooks reloaded"})
    return _JSON(content={"error": "Unknown action"}, status_code=400)

@router.post("/api/plugins/manage")
async def post_plugins_manage(request: _Request, _u=_Depends(_auth)):
    if _u.get("role") != "admin":  # plugin enable executes arbitrary code — admin only
        return _JSON(content={"error": "Admin access required"}, status_code=403)
    from salmalm.features.plugin_manager import plugin_manager
    body = await request.json()
    action = body.get("action", "")
    if action == "reload":
        result = plugin_manager.reload_all()
        return _JSON(content={"ok": True, "message": result})
    elif action == "enable":
        result = plugin_manager.enable(body.get("name", ""))
        return _JSON(content={"ok": True, "message": result})
    elif action == "disable":
        result = plugin_manager.disable(body.get("name", ""))
        return _JSON(content={"ok": True, "message": result})
    return _JSON(content={"error": "Unknown action"}, status_code=400)

@router.post("/api/groups")
async def post_groups(request: _Request, _u=_Depends(_auth)):
    from salmalm.features.edge_cases import session_groups
    body = await request.json()
    action = body.get("action", "create")
    if action == "create":
        name = body.get("name", "").strip()
        if not name:
            return _JSON(content={"error": "Missing name"}, status_code=400)
        result = session_groups.create_group(name, body.get("color", "#6366f1"))
        return _JSON(content=result)
    elif action == "update":
        gid = body.get("id")
        if not gid:
            return _JSON(content={"error": "Missing id"}, status_code=400)
        kwargs = {k: v for k, v in body.items() if k in ("name", "color", "sort_order", "collapsed")}
        ok = session_groups.update_group(int(gid), **kwargs)
        return _JSON(content={"ok": ok})
    elif action == "delete":
        gid = body.get("id")
        if not gid:
            return _JSON(content={"error": "Missing id"}, status_code=400)
        ok = session_groups.delete_group(int(gid))
        return _JSON(content={"ok": ok})
    elif action == "move":
        sid = body.get("session_id", "")
        gid = body.get("group_id")
        ok = session_groups.move_session(sid, int(gid) if gid else None)
        return _JSON(content={"ok": ok})
    return _JSON(content={"error": "Unknown action"}, status_code=400)

@router.post("/api/paste/detect")
async def post_paste_detect(request: _Request, _u=_Depends(_auth)):
    from salmalm.features.edge_cases import detect_paste_type
    body = await request.json()
    text = body.get("text", "")
    if not text:
        return _JSON(content={"error": "Missing text"}, status_code=400)
    return _JSON(content=detect_paste_type(text))

@router.post("/api/vault")
async def post_vault(request: _Request):
    from salmalm.security.crypto import vault
    from salmalm.web.auth import extract_auth, auth_manager
    from salmalm.core import audit_log
    if not vault.is_unlocked:
        return _JSON(content={"error": "Vault locked"}, status_code=403)
    user = extract_auth(dict(request.headers))
    ip = request.client.host if request.client else "unknown"
    _is_localhost = ip in ("127.0.0.1", "::1", "localhost")
    _is_admin = user and user.get("role") == "admin"
    if not _is_admin and not _is_localhost:
        return _JSON(content={"error": "Admin access required"}, status_code=403)
    body = await request.json()
    action = body.get("action")
    if action == "set":
        key = body.get("key")
        if not key:
            return _JSON(content={"error": "key required"}, status_code=400)
        try:
            vault.set(key, body.get("value"))
            return _JSON(content={"ok": True})
        except Exception as e:
            log.warning("[VAULT] FastAPI set failed for key=%s: %s", key, e)
            return _JSON(content={"error": "Vault write failed — check server logs"}, status_code=500)
    elif action == "get":
        key = body.get("key")
        if not key:
            return _JSON(content={"error": "key required"}, status_code=400)
        return _JSON(content={"value": vault.get(key)})
    elif action == "keys":
        return _JSON(content={"keys": vault.keys()})
    elif action == "delete":
        key = body.get("key")
        if not key:
            return _JSON(content={"error": "key required"}, status_code=400)
        vault.delete(key)
        return _JSON(content={"ok": True})
    elif action == "change_password":
        old_pw = body.get("old_password", "")
        new_pw = body.get("new_password", "")
        if new_pw and len(new_pw) < 4:
            return _JSON(content={"error": "Password must be at least 4 characters"}, status_code=400)
        elif new_pw and len(new_pw) > 1024:
            return _JSON(content={"error": "Password too long (max 1024 characters)"}, status_code=400)
        elif vault.change_password(old_pw, new_pw):
            audit_log("vault", "master password changed")
            return _JSON(content={"ok": True})
        else:
            return _JSON(content={"error": "Current password is incorrect"}, status_code=403)
    return _JSON(content={"error": "Unknown action"}, status_code=400)

@router.post("/api/cooldowns/reset")
async def post_cooldowns_reset(_u=_Depends(_auth)):
    from salmalm.core.llm_loop import reset_cooldowns
    reset_cooldowns()
    return _JSON(content={"ok": True, "message": "All cooldowns cleared"})

@router.post("/api/backup/restore")
async def post_backup_restore(request: _Request, _u=_Depends(_auth)):
    import zipfile, io
    from salmalm.constants import DATA_DIR
    if _u.get("role") != "admin":
        return _JSON(content={"error": "Admin access required"}, status_code=403)
    body_bytes = await request.body()
    if len(body_bytes) > 100 * 1024 * 1024:
        return _JSON(content={"ok": False, "error": "File too large (max 100MB)"}, status_code=400)
    try:
        zf = zipfile.ZipFile(io.BytesIO(body_bytes))
    except zipfile.BadZipFile:
        return _JSON(content={"ok": False, "error": "Invalid zip file"}, status_code=400)
    _MAX_RESTORE_ENTRIES = 10000
    _MAX_DECOMPRESSED = 500 * 1024 * 1024  # 500MB
    names = zf.namelist()
    if len(names) > _MAX_RESTORE_ENTRIES:
        return _JSON(content={"ok": False, "error": "Too many entries in ZIP"}, status_code=400)
    total_size = sum(zf.getinfo(n).file_size for n in names)
    if total_size > _MAX_DECOMPRESSED:
        return _JSON(content={"ok": False, "error": "ZIP decompressed size too large"}, status_code=400)
    for name in names:
        if name.startswith("/") or ".." in name:
            return _JSON(content={"ok": False, "error": f"Unsafe path in zip: {name}"}, status_code=400)
    # extractall is CPU/IO intensive — run in thread to avoid blocking event loop
    await _asyncio.to_thread(zf.extractall, str(DATA_DIR))
    n = len(names)
    zf.close()
    return _JSON(content={"ok": True, "message": f"Restored {n} files to {DATA_DIR}"})

@router.post("/api/presence")
async def post_presence(request: _Request, _u=_Depends(_auth)):
    from salmalm.features.presence import presence_manager
    body = await request.json()
    instance_id = body.get("instanceId", "")
    if not instance_id:
        return _JSON(content={"error": "instanceId required"}, status_code=400)
    ip = request.client.host if request.client else ""
    entry = presence_manager.register(instance_id, host=body.get("host", ""), ip=ip,
                                      mode=body.get("mode", "web"), user_agent=body.get("userAgent", ""))
    return _JSON(content={"ok": True, "state": entry.state})

@router.post("/api/node/execute")
async def post_node_execute(request: _Request, _u=_Depends(_auth)):
    from salmalm.tools.tool_handlers import execute_tool
    body = await request.json()
    tool = body.get("tool", "")
    args = body.get("args", {})
    if not tool:
        return _JSON(content={"error": "tool name required"}, status_code=400)
    try:
        result = await _asyncio.to_thread(execute_tool, tool, args)
        return _JSON(content={"ok": True, "result": result[:50000]})
    except Exception as e:
        return _JSON(content={"error": "Internal server error"}, status_code=500)
