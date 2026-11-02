"""WSGI proxy for addons running outside the Flask Core process.

The standalone arms publish descriptors in ``/usr/share/hugpy/arms.d``. The
new aiohttp core router consumes those directly; this adapter gives the live
Flask core the same API/UI paths while that process still serves the console.
Core routes keep precedence: API requests are proxied only when Flask has no
matching route. Embedded addon UIs take precedence over old descriptors;
remaining UI paths are served by the arm that owns the descriptor.
"""
from __future__ import annotations

import json
import logging
import os
import tempfile
from pathlib import Path
import requests
from werkzeug.exceptions import MethodNotAllowed, NotFound

log = logging.getLogger("hugpy_core.arms")
DEFAULT_ARMS_DIR = "/usr/share/hugpy/arms.d"
CONNECT_TIMEOUT_S = 5
DROP_REQUEST = {"connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
                "te", "trailer", "transfer-encoding", "upgrade", "host", "cookie",
                "authorization"}
DROP_RESPONSE = {"connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
                 "te", "trailer", "transfer-encoding", "upgrade"}


def _descriptors() -> list[dict]:
    root = Path(os.environ.get("HUGPY_ARMS_DIR") or DEFAULT_ARMS_DIR)
    rows = []
    try:
        files = sorted(root.glob("*.json"))
    except OSError as exc:
        log.warning("cannot list arm descriptors at %s: %s", root, exc)
        return rows
    for path in files:
        try:
            row = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(row, dict) or not row.get("arm") or not row.get("upstream"):
                continue
            row["upstream"] = str(row["upstream"]).rstrip("/")
            row["api_prefix"] = "/" + str(row.get("api_prefix") or "/api").strip("/")
            row["categories"] = [str(x) for x in row.get("categories", [])]
            rows.append(row)
        except (OSError, ValueError, TypeError) as exc:
            log.warning("invalid arm descriptor %s: %s", path, exc)
    return rows


def _core_owns(app, environ: dict) -> bool:
    """Whether the Flask URL map has a rule for this normalized API path."""
    env = dict(environ)
    path = env.get("PATH_INFO", "")
    if path == "/api":
        path = "/"
    elif path.startswith("/api/"):
        path = path[4:]
    else:
        return True
    env["PATH_INFO"] = path or "/"
    try:
        app.url_map.bind_to_environ(env).match(method=env.get("REQUEST_METHOD", "GET"))
        return True
    except MethodNotAllowed:
        return True
    except NotFound:
        return False


def _target(path: str, descriptors: list[dict]):
    """Return (descriptor, upstream path) for a claimed API or UI URL."""
    if path.startswith("/api/arms/"):
        tail = path[len("/api/arms/"):]
        arm_name, _, rest = tail.partition("/")
        cfg = next((x for x in descriptors if x.get("arm") == arm_name), None)
        if cfg and rest:
            return cfg, cfg["api_prefix"] + "/" + rest
    elif path.startswith("/api/"):
        tail = path[len("/api/"):]
        category, sep, rest = tail.partition("/")
        # Upload sessions belong to the Media arm even though its discovery
        # category is "media". Keep the session API on that same storage host.
        owner = "media" if category in ("session", "prompt") else category
        cfg = next((x for x in descriptors if owner in x["categories"]), None)
        if cfg:
            inner = category + ("/" + rest if sep else "")
            return cfg, cfg["api_prefix"] + "/" + inner
    elif path != "/api" and not path.startswith("/api/"):
        prefix = path.strip("/").partition("/")[0]
        # Backend-only arms publish an empty UI path. That is not a claim on
        # the console root (whose first path segment is also empty).
        cfg = next((x for x in descriptors
                    if prefix and str(x.get("ui") or "").strip("/").partition("/")[0] == prefix), None)
        if cfg:
            return cfg, path if path.startswith("/") else "/" + path
    return None, None


class ArmProxy:
    def __init__(self, app, core_app, embedded_arms=()):
        self.app = app
        self.core_app = core_app
        self.embedded_arms = frozenset(embedded_arms)

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO") or "/"
        # A mounted addon owns its UI even when an old service descriptor still
        # exists. Keep named API aliases local too; preserve method/body/query.
        if path.strip("/").partition("/")[0] in self.embedded_arms:
            return self.app(environ, start_response)
        if path.startswith("/api/arms/"):
            arm, _, rest = path[len("/api/arms/"):].partition("/")
            if arm in self.embedded_arms and rest:
                local = dict(environ)
                local["PATH_INFO"] = "/api/" + rest
                return self.app(local, start_response)
        descriptors = _descriptors()
        cfg = None
        inner_path = None
        if path.startswith("/api/") and _core_owns(self.core_app, environ):
            return self.app(environ, start_response)
        cfg, inner_path = _target(path, descriptors)
        if not cfg:
            return self.app(environ, start_response)

        target = cfg["upstream"] + inner_path
        query = environ.get("QUERY_STRING")
        if query:
            target += "?" + query
        headers = {}
        for name, value in environ.items():
            if name.startswith("HTTP_"):
                key = name[5:].replace("_", "-").title()
                if key.lower() not in DROP_REQUEST:
                    headers[key] = value
        # Scoped Media/Video live access is checked at nginx, then checked again
        # by the arm. Preserve that bearer across the Core-to-arm hop.
        if cfg.get("arm") in ("media", "video") and environ.get("HTTP_AUTHORIZATION"):
            headers["Authorization"] = environ["HTTP_AUTHORIZATION"]
        if environ.get("CONTENT_TYPE"):
            headers["Content-Type"] = environ["CONTENT_TYPE"]
        headers["Accept-Encoding"] = "identity"
        headers["X-Forwarded-For"] = environ.get("REMOTE_ADDR", "")
        headers["X-Forwarded-Proto"] = environ.get("wsgi.url_scheme", "http")
        headers["X-Forwarded-Host"] = environ.get("HTTP_HOST", "")
        # requests treats a raw WSGI input stream as an unknown-length body and
        # may send it chunked, even when the incoming request had a length.
        # The standalone Flask arms then try to parse those bytes as chunks and
        # fail with "Invalid chunk header". Spool exactly the advertised body
        # and rewind it so requests can set a correct Content-Length itself.
        spool = None
        length = int(environ.get("CONTENT_LENGTH") or 0)
        if length:
            spool = tempfile.SpooledTemporaryFile(max_size=8 * 1024 * 1024)
            remaining = length
            while remaining:
                chunk = environ["wsgi.input"].read(min(65536, remaining))
                if not chunk:
                    break
                spool.write(chunk)
                remaining -= len(chunk)
            spool.seek(0)
        try:
            response = requests.request(
                environ.get("REQUEST_METHOD", "GET"), target, headers=headers,
                data=spool, stream=True, allow_redirects=False,
                timeout=(CONNECT_TIMEOUT_S, None))
        except requests.RequestException as exc:
            arm = str(cfg.get("arm") or "arm")
            body = json.dumps({"error": {"message": f"arm {arm!r} is unreachable at {cfg['upstream']}: {type(exc).__name__}",
                                         "arm": arm, "upstream": cfg["upstream"]}}).encode()
            start_response("502 Bad Gateway", [("Content-Type", "application/json"),
                                                 ("Content-Length", str(len(body)))])
            return [body]
        finally:
            if spool is not None:
                spool.close()

        response_headers = [(k, v) for k, v in response.headers.items()
                            if k.lower() not in DROP_RESPONSE]
        start_response(f"{response.status_code} {response.reason}", response_headers)

        def stream():
            try:
                yield from response.iter_content(chunk_size=65536)
            finally:
                response.close()
        return stream()


def wrap(app, core_app, embedded_arms=()):
    return ArmProxy(app, core_app, embedded_arms=embedded_arms)
