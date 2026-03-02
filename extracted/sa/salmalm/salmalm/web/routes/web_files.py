"""SalmAlm Web — WebFilesMixin routes."""

import json
import re
import time
from pathlib import Path

from salmalm.constants import WORKSPACE_DIR
from salmalm.core import audit_log
from salmalm.security.crypto import vault, log

_RE_SESSION_EXPORT = re.compile(r"^/api/sessions/([^/]+)/export")


def _populate_export_zip(zf, inc_sessions, inc_data, inc_vault, export_user, _json, datetime) -> None:
    """Populate export zip file with soul, memory, config, sessions, data, vault."""
    from salmalm.constants import DATA_DIR, MEMORY_DIR, VERSION

    # Soul + memory
    for name in ("soul.md", "memory.md"):
        p = DATA_DIR / name
        if p.exists():
            zf.writestr(name, p.read_text(encoding="utf-8"))
    if MEMORY_DIR.exists():
        for f in MEMORY_DIR.glob("*"):
            if f.is_file():
                zf.writestr(f"memory/{f.name}", f.read_text(encoding="utf-8"))
    # Config
    for name in ("config.json", "routing.json"):
        p = DATA_DIR / name
        if p.exists():
            zf.writestr(name, p.read_text(encoding="utf-8"))
    # Sessions
    if inc_sessions:
        from salmalm.core import _get_db

        conn = _get_db()
        uid = export_user.get("id", 0)
        if uid and uid > 0:
            rows = conn.execute(
                "SELECT session_id, messages, title FROM session_store WHERE user_id=? OR user_id IS NULL", (uid,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT session_id, messages, title FROM session_store").fetchall()
        zf.writestr(
            "sessions.json",
            _json.dumps(
                [{"id": r[0], "data": r[1], "title": r[2] if len(r) > 2 else ""} for r in rows],
                ensure_ascii=False,
                indent=2,
            ),
        )
    # Data files
    if inc_data:
        for name in ("notes.json", "expenses.json", "habits.json", "journal.json", "dashboard.json"):
            p = DATA_DIR / name
            if p.exists():
                zf.writestr(f"data/{name}", p.read_text(encoding="utf-8"))
    # Vault keys
    if inc_vault:
        from salmalm.security.crypto import vault as _v

        if _v.is_unlocked:
            keys = {k: _v.get(k) for k in _v.keys() if _v.get(k)}
            if keys:
                zf.writestr("vault_keys.json", _json.dumps(keys, indent=2))
    # Manifest
    zf.writestr(
        "manifest.json",
        _json.dumps(
            {
                "version": VERSION,
                "exported_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "includes": {"sessions": inc_sessions, "data": inc_data, "vault": inc_vault},
            },
            indent=2,
        ),
    )


class WebFilesMixin:
    POST_ROUTES = {
        "/api/agent/import/preview": "_post_api_agent_import_preview",
        "/api/upload": "_post_api_upload",
    }
    GET_PREFIX_ROUTES = [
        ("/api/sessions/", "_get_api_sessions_export", "/export"),
        ("/api/google/callback", "_get_api_google_callback", None),
        ("/api/agent/export", "_get_api_agent_export", None),
        ("/uploads/", "_get_uploads", None),
    ]

    """Mixin for web_files routes."""

    def _get_uploads(self) -> None:
        """Handle GET /uploads/ routes."""
        # Serve uploaded files (images, audio) — basename-only to prevent traversal
        fname = Path(self.path.split("/uploads/", 1)[-1]).name
        if not fname:
            self.send_error(400)
            return
        upload_dir = (WORKSPACE_DIR / "uploads").resolve()  # noqa: F405
        fpath = (upload_dir / fname).resolve()
        if not fpath.is_relative_to(upload_dir) or not fpath.exists():
            self.send_error(404)
            return
        mime_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
            ".mp3": "audio/mpeg",
            ".wav": "audio/wav",
            ".ogg": "audio/ogg",
        }
        ext = fpath.suffix.lower()
        mime = mime_map.get(ext, "application/octet-stream")
        # ETag caching for static uploads
        stat = fpath.stat()
        etag = f'"{int(stat.st_mtime)}-{stat.st_size}"'
        if self.headers.get("If-None-Match") == etag:
            self.send_response(304)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(stat.st_size))
        self.send_header("ETag", etag)
        self.send_header("Cache-Control", "public, max-age=86400")
        self.end_headers()
        self.wfile.write(fpath.read_bytes())


# ── FastAPI router ────────────────────────────────────────────────────────────
import asyncio as _asyncio
from fastapi import APIRouter as _APIRouter, Request as _Request, Depends as _Depends, Query as _Query
from fastapi.responses import JSONResponse as _JSON, Response as _Response, HTMLResponse as _HTML, StreamingResponse as _SR, RedirectResponse as _RR
from salmalm.web.fastapi_deps import require_auth as _auth, optional_auth as _optauth

router = _APIRouter()

@router.get("/api/sessions/{session_id}/export")
async def get_session_export(request: _Request, session_id: str, format: str = _Query("json"), _u=_Depends(_auth)):
    import json as _json
    from salmalm.core import _get_db
    conn = _get_db()
    _uid_e = _u.get("id") if _u.get("role") != "admin" else None
    if _uid_e is not None:
        row = conn.execute(
            "SELECT messages, updated_at FROM session_store WHERE session_id=? AND (user_id=? OR user_id IS NULL)",
            (session_id, _uid_e),
        ).fetchone()
    else:
        row = conn.execute("SELECT messages, updated_at FROM session_store WHERE session_id=?", (session_id,)).fetchone()
    if not row:
        return _JSON(content={"error": "Session not found"}, status_code=404)
    msgs = _json.loads(row[0])
    updated_at = row[1]
    if format == "md":
        lines = ["# SalmAlm Chat Export", f"Session: {session_id}", f"Date: {updated_at}", ""]
        for msg in msgs:
            role = msg.get("role", "")
            if role == "system":
                continue
            content = msg.get("content", "")
            if isinstance(content, list):
                content = " ".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
            icon = "## 👤 User" if role == "user" else "## 😈 Assistant"
            lines.extend([icon, str(content), "", "---", ""])
        body = "\n".join(lines).encode("utf-8")
        fname = f"salmalm_{session_id}_{updated_at[:10]}.md"
        return _Response(content=body, media_type="text/markdown; charset=utf-8",
                        headers={"Content-Disposition": f'attachment; filename="{fname}"', "Content-Length": str(len(body))})
    else:
        export_data = {"session_id": session_id, "updated_at": updated_at, "messages": msgs}
        body = _json.dumps(export_data, ensure_ascii=False, indent=2).encode("utf-8")
        fname = f"salmalm_{session_id}_{updated_at[:10]}.json"
        return _Response(content=body, media_type="application/json; charset=utf-8",
                        headers={"Content-Disposition": f'attachment; filename="{fname}"', "Content-Length": str(len(body))})

@router.get("/api/google/callback")
async def get_google_callback(request: _Request):
    import json as _json, time, urllib.request, urllib.error, urllib.parse as _urlparse, os as _os
    from salmalm.security.crypto import vault, log
    from salmalm.web.web import _google_oauth_pending_states
    params = dict(request.query_params)
    code = params.get("code", "")
    state = params.get("state", "")
    error = params.get("error", "")
    if not state or state not in _google_oauth_pending_states:
        return _HTML(content="<html><body><h2>Invalid OAuth State</h2><p><a href=\"/\">Back</a></p></body></html>")
    issued_at = _google_oauth_pending_states.pop(state)
    if time.time() - issued_at > 600:
        return _HTML(content="<html><body><h2>OAuth State Expired</h2><p><a href=\"/\">Back</a></p></body></html>")
    if error:
        import html as _html_escape_mod
        return _HTML(content=f"<html><body><h2>Google OAuth Error</h2><p>{_html_escape_mod.escape(error)}</p><p><a href=\"/\">Back</a></p></body></html>")
    if not code:
        return _HTML(content="<html><body><h2>No code received</h2><p><a href=\"/\">Back</a></p></body></html>")
    client_id = vault.get("google_client_id") or ""
    client_secret = vault.get("google_client_secret") or ""
    port = int(_os.environ.get("SALMALM_PORT", 18800))
    redirect_uri = f"http://localhost:{port}/api/google/callback"
    try:
        data = _urlparse.urlencode({"code": code, "client_id": client_id, "client_secret": client_secret,
                                    "redirect_uri": redirect_uri, "grant_type": "authorization_code"}).encode()
        req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data,
                                    headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST")
        import asyncio as _aio_oauth
        def _do_token_req():
            with urllib.request.urlopen(req, timeout=15) as resp:
                return _json.loads(resp.read(4 * 1024 * 1024))
        result = await _aio_oauth.to_thread(_do_token_req)
        access_token = result.get("access_token", "")
        refresh_token = result.get("refresh_token", "")
        if refresh_token:
            vault.set("google_refresh_token", refresh_token)
        if access_token:
            vault.set("google_access_token", access_token)
        scopes = result.get("scope", "")
        return _HTML(content=f"""<html><body style="font-family:sans-serif;max-width:600px;margin:40px auto;text-align:center">
            <h2 style="color:#22c55e">✅ Google 연동 완료!</h2>
            <p>Refresh token이 vault에 저장되었습니다.</p>
            <p style="font-size:0.85em;color:#666">Scopes: {scopes}</p>
            <p><a href="/" style="color:#6366f1">← SalmAlm으로 돌아가기</a></p>
            </body></html>""")
    except Exception as e:
        return _HTML(content=f"""<html><body style="font-family:sans-serif;max-width:600px;margin:40px auto;text-align:center">
            <h2 style="color:#ef4444">❌ 토큰 교환 실패</h2><p>{str(e)[:200]}</p>
            <p><a href="/" style="color:#6366f1">← SalmAlm으로 돌아가기</a></p></body></html>""")

@router.get("/api/agent/export")
async def get_agent_export(request: _Request, vault_export: int = _Query(0, alias="vault"),
                           sessions: int = _Query(1), data: int = _Query(1)):
    import zipfile, io, json as _json, datetime
    from salmalm.web.fastapi_deps import optional_auth as _oa
    _u = await _oa(request)
    if not _u:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Unauthorized")
    min_role = "admin" if vault_export else "user"
    if min_role == "admin" and _u.get("role") != "admin":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Admin required")
    from salmalm.web.routes.web_files import _populate_export_zip
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        _populate_export_zip(zf, bool(sessions), bool(data), bool(vault_export), _u, _json, datetime)
    data_bytes = buf.getvalue()
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
    return _Response(content=data_bytes, media_type="application/zip",
                    headers={"Content-Disposition": f'attachment; filename="salmalm-export-{ts}.zip"',
                             "Content-Length": str(len(data_bytes))})

@router.get("/uploads/{file_path:path}")
async def get_uploads(file_path: str):
    from pathlib import Path
    from salmalm.constants import WORKSPACE_DIR
    fname = Path(file_path).name
    if not fname:
        return _Response(status_code=400)
    upload_dir = (WORKSPACE_DIR / "uploads").resolve()
    fpath = (upload_dir / fname).resolve()
    if not fpath.is_relative_to(upload_dir) or not fpath.exists():
        return _Response(status_code=404)
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
                ".webp": "image/webp", ".mp3": "audio/mpeg", ".wav": "audio/wav", ".ogg": "audio/ogg"}
    ext = fpath.suffix.lower()
    mime = mime_map.get(ext, "application/octet-stream")
    stat = fpath.stat()
    etag = f'"{int(stat.st_mtime)}-{stat.st_size}"'
    return _Response(content=fpath.read_bytes(), media_type=mime,
                    headers={"ETag": etag, "Cache-Control": "public, max-age=86400", "Content-Length": str(stat.st_size)})

@router.post("/api/agent/import/preview")
async def post_agent_import_preview(request: _Request, _u=_Depends(_auth)):
    import zipfile, io, json as _json
    body_bytes = await request.body()
    content_type = request.headers.get("content-type", "")
    if "multipart" not in content_type:
        return _JSON(content={"ok": False, "error": "Expected multipart upload"}, status_code=400)
    boundary = content_type.split("boundary=")[1].encode() if "boundary=" in content_type else b""
    parts = body_bytes.split(b"--" + boundary)
    zip_data = None
    for part in parts:
        if b"filename=" in part:
            body_start = part.find(b"\r\n\r\n")
            if body_start > 0:
                zip_data = part[body_start + 4:]
                if zip_data.endswith(b"\r\n"):
                    zip_data = zip_data[:-2]
                break
    if not zip_data:
        return _JSON(content={"ok": False, "error": "No ZIP file found"}, status_code=400)
    _MAX_ZIP_ENTRIES = 1000
    _MAX_MANIFEST_BYTES = 512 * 1024
    try:
        zf = zipfile.ZipFile(io.BytesIO(zip_data))
        names = zf.namelist()
        if len(names) > _MAX_ZIP_ENTRIES:
            return _JSON(content={"ok": False, "error": "ZIP contains too many entries"}, status_code=400)
        manifest = {}
        if "manifest.json" in names:
            info = zf.getinfo("manifest.json")
            if info.file_size > _MAX_MANIFEST_BYTES:
                return _JSON(content={"ok": False, "error": "manifest.json too large"}, status_code=400)
            manifest = _json.loads(zf.read("manifest.json"))
        preview = {"files": names, "manifest": manifest, "size": len(zip_data)}
        return _JSON(content={"ok": True, "preview": preview})
    except Exception:
        return _JSON(content={"ok": False, "error": "Invalid ZIP file"}, status_code=400)

@router.post("/api/upload")
async def post_upload(request: _Request, _u=_Depends(_auth)):
    import email.parser, email.policy
    from pathlib import Path
    from salmalm.constants import WORKSPACE_DIR
    from salmalm.core import audit_log
    from salmalm.security.crypto import vault, log
    if not vault.is_unlocked:
        return _JSON(content={"error": "Vault locked"}, status_code=403)
    content_type = request.headers.get("content-type", "")
    if "multipart/form-data" not in content_type:
        return _JSON(content={"error": "multipart required"}, status_code=400)
    try:
        raw = await request.body()
        header_bytes = f"Content-Type: {content_type}\r\n\r\n".encode()
        msg = email.parser.BytesParser(policy=email.policy.compat32).parsebytes(header_bytes + raw)
        for part in msg.walk():
            fname_raw = part.get_filename()
            if not fname_raw:
                continue
            fname = Path(fname_raw).name
            if not fname or ".." in fname or "/" in fname or "\\" in fname or "\x00" in fname:
                return _JSON(content={"error": "Invalid filename"}, status_code=400)
            from salmalm.features.edge_cases import validate_upload
            ok, err = validate_upload(fname, len(part.get_payload(decode=True) or b""))
            if not ok:
                return _JSON(content={"error": err}, status_code=400)
            file_data = part.get_payload(decode=True)
            if not file_data:
                continue
            if len(file_data) > 50 * 1024 * 1024:
                return _JSON(content={"error": "File too large (max 50MB)"}, status_code=413)
            save_dir = WORKSPACE_DIR / "uploads"
            save_dir.mkdir(exist_ok=True)
            (save_dir / fname).write_bytes(file_data)
            size_kb = len(file_data) / 1024
            is_image = any(fname.lower().endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"))
            is_text = any(fname.lower().endswith(ext) for ext in (".txt", ".md", ".py", ".js", ".json", ".csv", ".log", ".html", ".css", ".sh", ".bat", ".yaml", ".yml", ".xml", ".sql"))
            is_pdf = fname.lower().endswith(".pdf")
            info = f"[{'🖼️ Image' if is_image else '📎 File'} uploaded: uploads/{fname} ({size_kb:.1f}KB)]"
            if is_pdf or is_text:
                try:
                    from salmalm.features.edge_cases import process_uploaded_file
                    info = process_uploaded_file(fname, file_data)
                except Exception:
                    if is_text:
                        preview = file_data.decode("utf-8", errors="replace")[:3000]
                        info += f"\n[File content]\n{preview}"
            log.info(f"[SEND] Web upload: {fname} ({size_kb:.1f}KB)")
            audit_log("web_upload", fname)
            resp = {"ok": True, "filename": fname, "size": len(file_data), "info": info, "is_image": is_image}
            if is_image:
                import base64
                ext = fname.rsplit(".", 1)[-1].lower()
                mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp", ".bmp": "image/bmp"}.get(f".{ext}", "image/png")
                resp["image_base64"] = base64.b64encode(file_data).decode()
                resp["image_mime"] = mime
            return _JSON(content=resp)
        return _JSON(content={"error": "No file found"}, status_code=400)
    except Exception as e:
        return _JSON(content={"error": "Internal server error"}, status_code=500)
