"""Expiring usage-only passes, enforced before static, Flask and arm proxies.

Passes use KeyAuth's hashed use keys and expiry/revocation machinery. The
created_by marker narrows those keys at *every* Core entrance, including /v1
and the legacy live-api projection. Unknown routes fail closed for guests.
"""
from __future__ import annotations

import time
import re
import hashlib
import json
import os
import tempfile
from urllib.parse import urlsplit

from werkzeug.wrappers import Request, Response
from hugpy_core.lifted.key_auth import parse
from hugpy_core.router.observability import store as routing

CREATOR = "guest-pass"
COOKIE = "hugpy_guest"
PUBLIC_CREATOR = "public-demo"
PUBLIC_COOKIE = "hugpy_public"

# Enumerate capabilities, never whole namespaces: many legacy GET endpoints
# mutate state. New routes therefore require an explicit guest-policy decision.
READ = {
    "/v1/models", "/v1/task-bindings", "/api/version", "/api/prompt/tasks", "/api/keys/verify-use",
    "/api/media/health", "/api/media/capabilities", "/api/media/manifest",
    "/api/video/health", "/api/video/manifest", "/api/video/jobs",
    "/api/video/job", "/api/video/jobs/stream", "/api/video/media",
    "/api/video/presets", "/api/video/render/presets", "/api/video/projects",
    "/api/video/prompt/assist/models", "/api/movie/presets",
}
RUN = {
    "/v1/chat/completions", "/api/prompt", "/api/media/upload", "/api/uploads", "/api/video/upload",
    "/api/media/analyze", "/api/media/transcribe", "/api/media/summarize",
    "/api/media/keywords", "/api/media/embed", "/api/media/similarity",
    "/api/media/vision", "/api/media/imagine", "/api/media/extract",
    "/api/media/depth", "/api/media/detect", "/api/media/classify",
    "/api/media/document_inspect", "/api/media/document_page", "/api/media/document_search",
    "/api/media/segment", "/api/session/ping", "/api/session/end", "/api/session/file",
    "/api/video/ingest", "/api/video/jobs/crop", "/api/video/jobs/frame_extract",
    "/api/video/jobs/audio_extract", "/api/video/jobs/generate_image",
    "/api/video/jobs/generate_scene", "/api/video/jobs/generate_movie",
    "/api/video/prompt/assist", "/api/video/prompt/intent",
}
# These reads contain operator configuration. Return only fields required by
# the model picker rather than forwarding raw worker/database records.
CAPACITY = {"/api/fleet/workers", "/api/llm/workers", "/api/models/database"}


def _record(token):
    parsed = parse(token)
    if not parsed:
        return None
    row = routing.STORE.read_one(
        "SELECT id, name, created_by, expires_at FROM api_keys WHERE id = ?", (parsed[0],))
    return dict(row) if row and row["created_by"] in (CREATOR, PUBLIC_CREATOR) else None


def _json(data, status=200):
    import json
    return Response(json.dumps(data), status=status, content_type="application/json",
                    headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"})


def _same_origin(req):
    origin = req.headers.get("Origin")
    # GET/HEAD cannot change guest state. Writes from another browser origin
    # are rejected; non-browser Bearer callers need no Origin header.
    return not origin or urlsplit(origin).netloc == req.host


def permitted(path, method):
    if "\\" in path or "//" in path or "%" in path or any(x in (".", "..") for x in path.split("/")):
        return False
    path = path.rstrip("/")
    return ((method in ("GET", "HEAD") and path in READ | CAPACITY)
            or (method == "POST" and path in RUN))


def upload_sid(token):
    return hashlib.sha256(("hugpy-guest-upload:" + token).encode()).hexdigest()[:32]


def validate_payload(value, sid, field="", *, principal=None):
    """Guest inputs cannot read host secrets or fetch local management URLs.

    Uploads live in a pass-specific session; video outputs remain under the
    arm's media jail. Output destinations and remote fetches are operator-only.
    """
    if isinstance(value, dict):
        return all(validate_payload(v, sid, str(k), principal=principal) for k, v in value.items())
    if isinstance(value, (list, tuple)):
        return all(validate_payload(v, sid, field, principal=principal) for v in value)
    if not isinstance(value, str) or not value:
        return True
    name = field.lower()
    if name == "sid":
        return value == sid
    if name in ("output_path", "save_path", "output_dir", "dest", "destination", "root", "cwd"):
        return False
    if name in ("source", "image_url") and value.startswith(("{", "[")):
        try:
            return validate_payload(json.loads(value), sid, name, principal=principal)
        except ValueError:
            return False
    if name in ("url", "image_url"):
        return value.startswith("data:image/")
    path_field = (name in ("file", "image", "audio", "video", "source", "id", "uri", "handle", "files", "images")
                  or name == "path" or name.endswith(("_path", "_file", "_dir")))
    if not path_field:
        return True
    if value.startswith("data:image/"):
        return True
    if not value.startswith("/"):
        return name == "id" and "://" not in value
    resolved = os.path.realpath(value)
    return (resolved == value and (f"/sessions/{sid}/" in resolved or "/video_intel/" in resolved
                                  or bool(principal and _public_handle(principal, resolved))))


def _capacity(path, req):
    """Project only model capacity facts, without credentials or worker controls."""
    if path in ("/api/fleet/workers", "/api/llm/workers"):
        from hugpy_core.web.routes import workers_list
        rows = workers_list().get_json()
        return _json([{"id": row.get("id"), "status": row.get("status"),
                       "allocations": [{k: a[k] for k in ("model_key", "ctx") if k in a}
                                       for a in row.get("allocations", [])],
                       "loaded_detail": {key: {"ctx": value.get("ctx")} for key, value in (row.get("loaded_detail") or {}).items()
                                         if isinstance(value, dict)}} for row in rows])
    if req.args.get("view") != "pair":
        return _json({"error": "Guest model reads require view=pair"}, 403)
    from hugpy_core.models.routes import models_database
    data = models_database(view="pair")
    rows = []
    for row in data.get("rows", []):
        item = {k: row[k] for k in ("model_key", "ctx_train") if k in row}
        item["workers"] = [{
            "worker_id": pair.get("worker_id"), "fits": pair.get("fits"),
            "user_settings": {k: (pair.get("user_settings") or {}).get(k) for k in ("blocked", "ctx_pct")},
            "live": {k: (pair.get("live") or {}).get(k) for k in ("gpu_fit", "ram_fit")},
        } for pair in row.get("workers", [])]
        rows.append(item)
    return _json({"rows": rows})


def _public_handle(principal, handle, *, remember=False):
    """Persist ownership alongside the existing Core key store, not in a worker DB."""
    routing.STORE.write("CREATE TABLE IF NOT EXISTS public_demo_handles (principal TEXT NOT NULL, handle TEXT NOT NULL, PRIMARY KEY(principal, handle))")
    if remember:
        routing.STORE.write("INSERT INTO public_demo_handles (principal, handle) VALUES (?, ?) ON CONFLICT DO NOTHING", (principal, handle))
        return True
    return bool(routing.STORE.read_one("SELECT handle FROM public_demo_handles WHERE principal = ? AND handle = ?", (principal, handle)))


def _public_result(principal, value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key in ("job_id", "path", "file_path", "image_path", "video_path", "audio_path", "uri", "handle") and isinstance(item, str):
                _public_handle(principal, item, remember=True)
            _public_result(principal, item)
    elif isinstance(value, list):
        for item in value: _public_result(principal, item)


def _public_inputs(principal, value, sid, field=""):
    if isinstance(value, dict):
        return all(_public_inputs(principal, item, sid, str(key)) for key, item in value.items())
    if isinstance(value, list):
        return all(_public_inputs(principal, item, sid, field) for item in value)
    if isinstance(value, str) and field in ("source", "image_url") and value.startswith(("{", "[")):
        try:
            return _public_inputs(principal, json.loads(value), sid, field)
        except ValueError:
            return False
    if isinstance(value, str) and value.startswith("/") and (field in ("path", "file", "image", "audio", "video", "source", "id", "uri", "handle", "files", "images") or field.endswith(("_path", "_file", "_dir"))):
        return f"/sessions/{sid}/" in os.path.realpath(value) or _public_handle(principal, value)
    return True


class GuestAccess:
    def __init__(self, app, core_app):
        self.app, self.core_app = app, core_app

    def __call__(self, environ, start_response):
        req = Request(environ)
        public_projection = req.path == "/public-api" or req.path.startswith("/public-api/")
        prefix = "/public-api" if public_projection else "/guest-api"
        projected = public_projection or req.path == "/guest-api" or req.path.startswith("/guest-api/")
        auth = req.headers.get("Authorization", "")
        bearer = auth[7:].strip() if auth.lower().startswith("bearer ") else ""
        cookie = PUBLIC_COOKIE if public_projection else COOKIE
        secure_cookie = req.host.split(":")[0] not in ("localhost", "127.0.0.1")
        embedded_public = public_projection and secure_cookie
        # The public projection cannot be upgraded with a visitor's Bearer key.
        token = req.cookies.get(cookie, "") if public_projection else bearer or req.cookies.get(cookie, "")
        try:
            record = _record(token) if token else None
        except Exception:
            # A failed key lookup cannot turn a supplied credential into local
            # trusted access or pass it to a privileged proxy.
            return _json({"error": "Guest key store unavailable"}, 503)(environ, start_response)
        if not projected and not record and not req.cookies.get(COOKIE):
            return self.app(environ, start_response)

        if projected and req.path.rstrip("/") == prefix + "/session":
            if req.method == "DELETE":
                if not _same_origin(req):
                    return _json({"error": "Cross-origin guest request refused"}, 403)(environ, start_response)
                response = _json({"ok": True})
                response.delete_cookie(cookie, path="/", secure=secure_cookie,
                                       samesite="None" if embedded_public else "Strict",
                                       partitioned=embedded_public)
                return response(environ, start_response)
            if req.method == "POST":
                if not _same_origin(req):
                    return _json({"error": "Cross-origin guest request refused"}, 403)(environ, start_response)
                body = req.get_json(silent=True) or {}
                if public_projection and record and routing.KEYS.scope_of(token) != "use":
                    record = None
                if public_projection and not record:
                    key = routing.KEYS.create("Public browser", "use", 1, created_by=PUBLIC_CREATOR)
                    token = key["key"]
                    record = _record(token)
                elif public_projection:
                    pass
                else:
                    token = body.get("key") if isinstance(body.get("key"), str) else ""
                    try:
                        record = _record(token)
                    except Exception:
                        record = None
            elif req.method not in ("GET", "HEAD"):
                return _json({"error": "Method not allowed"}, 405)(environ, start_response)
            if not record or routing.KEYS.scope_of(token) != "use" or not record.get("expires_at"):
                return _json({"error": "Guest pass is invalid, expired or revoked"}, 401)(environ, start_response)
            response = _json({"name": record["name"], "expires_at": record["expires_at"], "role": "public" if record["created_by"] == PUBLIC_CREATOR else "guest",
                              "upload_sid": upload_sid(token)})
            if req.method == "POST":
                response.set_cookie(cookie, token, max_age=max(1, int(record["expires_at"] - time.time())),
                                    secure=secure_cookie, httponly=True,
                                    samesite="None" if embedded_public else "Strict", path="/",
                                    partitioned=embedded_public)
            return response(environ, start_response)

        # Static files remain public; a stale cookie should not prevent the
        # guest from opening the page on which to enter a replacement pass.
        static = (req.path.rstrip("/") in ("", "/console", "/guest", "/docs", "/login", "/media", "/media/chat", "/media/console", "/video")
                  or re.fullmatch(r"/(?:assets|media/assets|video/assets)/[^/]+\.(?:js|css|png|svg|woff2?|ico)", req.path))
        if not projected and req.method in ("GET", "HEAD") and static:
            return self.app(environ, start_response)
        if not record or routing.KEYS.scope_of(token) != "use" or not record.get("expires_at"):
            return _json({"error": "Guest pass is invalid, expired or revoked"}, 401)(environ, start_response)
        path = req.path[len(prefix):] if projected else req.path
        if path.startswith("/live-api/"):
            path = "/api/" + path[len("/live-api/"):]
        public = record["created_by"] == PUBLIC_CREATOR
        from . import public_policy
        from hugpy_core.config import model_preferences
        surface = "video" if req.args.get("surface") == "video" or path.startswith("/api/video/") else "media"
        if not (public_policy.permitted(path, req.method) if public else permitted(path, req.method)):
            return _json({"error": "Guest passes allow usage only; this action requires an operator",
                          "code": "guest_forbidden"}, 403)(environ, start_response)
        if req.method not in ("GET", "HEAD") and not _same_origin(req):
            return _json({"error": "Cross-origin guest request refused"}, 403)(environ, start_response)
        env = dict(environ, PATH_INFO=path, HTTP_AUTHORIZATION="Bearer " + token)
        if public:
            service_key = os.environ.get("HUGPY_PUBLIC_API_KEY", "").strip()
            if not service_key or routing.KEYS.scope_of(service_key) != "use":
                return _json({"error": "Public inference is unavailable"}, 503)(environ, start_response)
            env["HTTP_AUTHORIZATION"] = "Bearer " + service_key
        if req.headers.get("Origin"):
            env["HTTP_ORIGIN"] = req.host_url.rstrip("/")
        for name in ("HTTP_COOKIE", "HTTP_X_HUGPY_ROLE", "HTTP_X_HUGPY_USER", "HTTP_X_CONSOLE_TOKEN"):
            env.pop(name, None)
        sid = upload_sid(token)
        if public and req.method == "POST" and public_policy.task_for(path, {}) is not None:
            if not req.is_json or not (req.content_length or environ.get("wsgi.input_terminated")) or req.args:
                return _json({"error": "Public processing requires a JSON body without query overrides"}, 400)(environ, start_response)
        query = req.args.to_dict(flat=False)
        if public and req.method in ("GET", "HEAD") and (path == "/api/video/job" or re.fullmatch(r"/api/video/jobs/[A-Za-z0-9_-]+", path)):
            job_id = req.args.get("id") or req.args.get("job_id") or path.rsplit("/", 1)[-1]
            if not _public_handle(record["id"], job_id):
                return _json({"error": "Job not found"}, 404)(environ, start_response)
        if not validate_payload(query, sid, principal=record["id"] if public else None) or (public and not _public_inputs(record["id"], query, sid)):
            return _json({"error": "Guest files must belong to this pass; remote URLs and output paths require an operator"}, 403)(environ, start_response)
        # Preserve the body for the downstream arm after inspecting it. Large
        # multipart uploads spool to disk instead of being copied into RAM.
        spool = None
        if req.method == "POST" and (req.content_length or environ.get("wsgi.input_terminated")):
            spool = tempfile.SpooledTemporaryFile(max_size=8 * 1024 * 1024)
            remaining = req.content_length if req.content_length else -1
            while remaining != 0:
                part = environ["wsgi.input"].read(min(65536, remaining) if remaining > 0 else 65536)
                if not part:
                    break
                spool.write(part)
                if remaining > 0:
                    remaining -= len(part)
            spool.seek(0)
            env["wsgi.input"] = spool
            body_req = Request(env)
            payload = body_req.get_json(silent=True) if body_req.is_json else body_req.form.to_dict(flat=False)
            valid = validate_payload(payload, sid, principal=record["id"] if public else None)
            if public and valid:
                valid = _public_inputs(record["id"], payload, sid)
            if public and body_req.is_json and valid:
                try:
                    payload = public_policy.pin_models(path, payload, public_policy.DEFAULTS)
                except (ValueError, TypeError) as exc:
                    spool.close()
                    return _json({"error": str(exc), "code": "public_demo_only", "downloads": "/downloads/"}, 403)(environ, start_response)
                encoded = json.dumps(payload).encode()
                spool.seek(0); spool.truncate(); spool.write(encoded); spool.seek(0)
                env["CONTENT_LENGTH"] = str(len(encoded))
            if path.rstrip("/") in ("/api/media/upload", "/api/uploads", "/api/video/upload"):
                valid = valid and body_req.form.get("sid") == sid
            body_req.close()
            spool.seek(0)
            if not valid:
                spool.close()
                return _json({"error": "Guest files must belong to this pass; remote URLs and output paths require an operator"}, 403)(environ, start_response)
        if path.rstrip("/") in CAPACITY:
            with self.core_app.test_request_context(path + ("?" + req.query_string.decode() if req.query_string else "")):
                response = _capacity(path.rstrip("/"), req)
                if public:
                    data = response.get_json()
                    allowed = model_preferences.public_catalog(surface)
                    if isinstance(data, dict):
                        data["rows"] = [r for r in data.get("rows", []) if r.get("model_key") in allowed]
                    else:
                        for row in data:
                            row["allocations"] = [a for a in row.get("allocations", []) if a.get("model_key") in allowed]
                            row["loaded_detail"] = {k:v for k,v in row.get("loaded_detail", {}).items() if k in allowed}
                    response = _json(data)
                return response(environ, start_response)
        if public and path in ("/v1/task-bindings", "/api/prompt/tasks"):
            data = {"defaults": model_preferences.public_defaults(surface)}
            if path == "/api/prompt/tasks":
                data = {"result": {**data, "tasks": list(data["defaults"])}}
            return _json(data)(environ, start_response)
        if public and path in ("/v1/models", "/api/models"):
            response = Response.from_app(self.app, env, buffered=True)
            if response.status_code != 200:
                return response(environ, start_response)
            data = response.get_json()
            rows = data if isinstance(data, list) else data.get("data", [])
            preferences = model_preferences.read()
            allowed = model_preferences.public_catalog(surface, preferences=preferences, rows=rows)
            fields = ("id", "model_key", "name", "tasks", "primary_task", "available", "model_max_length", "capabilities")
            rows = [{k:row[k] for k in fields if k in row} for row in rows if row.get("model_key", row.get("id")) in allowed]
            return _json(rows if isinstance(data, list) else {
                "object": "list", "data": rows,
                "model_preferences": model_preferences.projection(preferences, public=True, rows=rows),
            })(environ, start_response)
        response_info = {}
        def capture_start(status, headers, exc_info=None):
            response_info.update(status=status, headers=dict((k.lower(), v) for k, v in headers))
            return start_response(status, headers, exc_info)
        try:
            result = self.app(env, capture_start if public else start_response)
        except BaseException:
            if spool is not None:
                spool.close()
            raise
        def stream():
            collected = bytearray()
            bounded = True
            try:
                for chunk in result:
                    if public and bounded:
                        if len(collected) + len(chunk) <= 4 * 1024 * 1024:
                            collected.extend(chunk)
                        else:
                            collected.clear(); bounded = False
                    yield chunk
                if public and bounded and response_info.get("status", "").startswith("2") and "application/json" in response_info.get("headers", {}).get("content-type", ""):
                    try:
                        _public_result(record["id"], json.loads(collected))
                    except (ValueError, UnicodeDecodeError):
                        pass
            finally:
                if hasattr(result, "close"):
                    result.close()
                if spool is not None:
                    spool.close()
        return stream()


def wrap(app, core_app):
    return GuestAccess(app, core_app)
