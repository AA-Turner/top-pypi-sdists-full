"""The console, served by core itself: one address for the UI and its API.

    /api/<path>   core's own routes at /<path> (what nginx's `location /api/` did)
    /v1/<path>    core's OpenAI-compatible relay, unchanged (nginx's `location /v1/`)
    /live-api/<section>/<path>
                  the same routes as /api/<section>/<path> for a key holder: only the
                  sections named in LIVE_SECTIONS, and only for a caller the key gate
                  admits (a valid key, or a local caller when the mode is "outside")
    /health       {"ok": true, ...}: this process is answering
    /<page>       the built console (env HUGPY_CORE_UI_DIST = its dist/ dir): its files, and
                  the console page for the console's own pages (CONSOLE_PAGES: client-side
                  routing); an arm page (/fleet/..., /media/...) gets its own index.html
    anything else 404, as JSON, naming the prefixes above. A control route called without
                  /api is a mistake in the caller, and must not look like a page that loaded.

A page below its entry point (/console/workers, /video/jobs/7, /media/chat) is client-side
routing: the same HTML for any path. It is given to a browser navigation (Accept: text/html)
and to nobody else (PagesForBrowsers), because /video, /media and /fleet are API sections too
and /video/jobs/7 without /api is far more often a program's mistake than a page.

Without HUGPY_CORE_UI_DIST the console packaged in the wheel (web/console/) is served;
a dir with no index.html means core serves its routes only.
"""
from __future__ import annotations

import logging
import importlib.util
import mimetypes
import os
import re
from typing import Optional

from hugpy_core.imports import constants as _C

logger = logging.getLogger("hugpy_core")

API_PREFIX = "/api"
# The console's own pages (ui/src/App/App.jsx <Routes>), by first path segment. Only these get the
# console page for a path that is not a file.
CONSOLE_PAGES = frozenset({"", "welcome", "login", "docs", "guest", "console", "station", "video", "media"})

# The key holder's door onto control routes. /api itself carries no key check (a front gates it
# with the operator's session; direct callers are whoever can reach Core's bind address), so a
# client that holds a key and may be anywhere uses this prefix for every control call. The section
# list is the boundary of what a "use" key reaches: key minting, settings and the other operator
# surfaces are deliberately not on it.
LIVE_PREFIX = "/live-api"
LIVE_SECTIONS = frozenset({"media", "video", "uploads", "llm", "movie", "prompt", "version",
                           "models", "session", "chat", "oracle", "fleet", "agent"})
# Sections a "use" key reaches only in part: the routes matching the pattern (the path after the
# section). The rest of such a section needs admin scope (an admin key, or a caller on this box).
#   fleet: the worker tree, which /live-api/llm/workers/... already reaches through its alias, and
#          the model and catalog reads. Not the hub token, the central drives or storage owners.
#   agent: the one call a node makes with its own key.
LIVE_USE_ROUTES = {
    "fleet": re.compile(r"(workers|models|catalog)(/.*)?"),
    "agent": re.compile(r"register"),
}


class _Caller:
    """The request as the key gate reads one: peer address and headers."""

    class _Headers:
        def __init__(self, environ):
            self.environ = environ

        def get(self, name, default=None):
            return self.environ.get("HTTP_" + name.upper().replace("-", "_"), default)

    def __init__(self, environ):
        self.client_address = (environ.get("REMOTE_ADDR") or "", 0)
        self.headers = self._Headers(environ)


def _refuse(start_response, status: int, body: dict):
    return _json(start_response, status, body)


def _json(start_response, status: int, body: dict, *, head: bool = False):
    import json
    phrase = {200: "OK", 401: "Unauthorized", 403: "Forbidden", 404: "Not Found"}.get(status, "Error")
    data = json.dumps(body).encode()
    start_response(f"{status} {phrase}", [("Content-Type", "application/json"), ("Content-Length", str(len(data))),
                                           ("Cache-Control", "no-store")])
    return [b"" if head else data]


def _no_such_path(path: str, start_response, *, head: bool = False):
    hint = f" Did you mean {API_PREFIX}{path}?" if path.count("/") >= 1 and len(path) > 1 else ""
    return _json(start_response, 404, {"error": {
        "message": f"Core serves nothing at {path}. Control routes are under {API_PREFIX}/, the model API "
                   f"under /v1/, a key holder's control calls under {LIVE_PREFIX}/.{hint}",
        "code": "not_found"}}, head=head)


# the published @hugpy/ui build shipped inside the wheel (console/PROVENANCE.md)
PACKAGED_DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "console")


def ui_dist() -> Optional[str]:
    d = os.environ.get(_C.ENV_UI_DIST, "").strip() or PACKAGED_DIST
    if d and os.path.isfile(os.path.join(d, "index.html")):
        return os.path.realpath(d)
    if d:
        logger.warning("%s=%s has no index.html: console not served", _C.ENV_UI_DIST, d)
    return None


class LiveApi:
    """WSGI, outermost: /live-api/<section>/... for a caller the key gate admits becomes
    /api/<section>/... for everything below (aliases, the guest gate, arms, the console)."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO") or "/"
        if not (path == LIVE_PREFIX or path.startswith(LIVE_PREFIX + "/")):
            return self.app(environ, start_response)
        rest = path[len(LIVE_PREFIX):]
        section, _, tail = rest.lstrip("/").partition("/")
        if section not in LIVE_SECTIONS:
            return _refuse(start_response, 404, {"error": {
                "message": "not a key holder's route; the sections are " + ", ".join(sorted(LIVE_SECTIONS)),
                "code": "not_found"}})
        limited = LIVE_USE_ROUTES.get(section)
        need = "use" if limited is None or limited.fullmatch(tail.rstrip("/")) else "admin"
        from hugpy_core.router.observability import store as routing
        denied = routing.KEYS.check(_Caller(environ), need)
        if denied is not None:
            return _refuse(start_response, *denied)
        return self.app(dict(environ, PATH_INFO=API_PREFIX + rest), start_response)


# First path segments that are never a page: the API's own prefixes and plain file trees.
_NOT_PAGES = frozenset({"api", "v1", "live-api", "guest-api", "public-api", "ts", "assets", "static"})


class PagesForBrowsers:
    """WSGI, around everything that serves pages (the console, hosted and proxied arms): a GET
    below a page's entry point that would be answered with HTML is a 404 unless the request
    asks for HTML. Entry points (/, /console, /video/), files and every API prefix pass through."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO") or "/"
        method = environ.get("REQUEST_METHOD", "GET")
        inner = path.strip("/")
        if (method not in ("GET", "HEAD") or "/" not in inner or inner.split("/", 1)[0] in _NOT_PAGES
                or path.endswith((".html", ".htm")) or "text/html" in environ.get("HTTP_ACCEPT", "")):
            return self.app(environ, start_response)
        held = {}

        def hold(status, headers, exc_info=None):
            held.update(status=status, headers=headers)
            return lambda data: None

        body = self.app(environ, hold)
        chunks = iter(body)
        first = b""
        if not held:                      # an app that answers only once iterated
            first = next(chunks, b"")
        kind = next((value for name, value in held.get("headers", []) if name.lower() == "content-type"), "")
        if held.get("status", "").startswith("200") and kind.split(";")[0].strip().lower() == "text/html":
            close = getattr(body, "close", None)
            if close:
                close()
            return _no_such_path(path, start_response, head=method == "HEAD")
        start_response(held["status"], held["headers"])

        def rest():
            try:
                if first:
                    yield first
                yield from chunks
            finally:
                close = getattr(body, "close", None)
                if close:
                    close()
        return rest()


class ConsoleApp:
    """WSGI: /api/* -> ``api`` with the prefix stripped; everything else -> files under ``root``."""

    def __init__(self, api, root: str):
        self.api, self.root = api, root

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO") or "/"
        if path == API_PREFIX or path.startswith(API_PREFIX + "/"):
            environ = dict(environ)
            environ["SCRIPT_NAME"] = environ.get("SCRIPT_NAME", "") + API_PREFIX
            environ["PATH_INFO"] = path[len(API_PREFIX):] or "/"
            return self.api(environ, start_response)
        if path == "/v1" or path.startswith("/v1/") or path.startswith("/ts/"):       # OpenAI clients: core's /v1 as is
            return self.api(environ, start_response)
        return self._static(path, environ, start_response)

    def _static(self, path, environ, start_response):
        method = environ.get("REQUEST_METHOD", "GET")
        page = path.lstrip("/").split("/", 1)[0] in CONSOLE_PAGES
        if method not in ("GET", "HEAD"):
            if not page:        # e.g. a POST to a control route without /api
                return _no_such_path(path, start_response)
            start_response("405 Method Not Allowed", [("Content-Type", "text/plain"), ("Allow", "GET, HEAD")])
            return [b"method not allowed\n"]
        if path == "/health":
            from importlib.metadata import version
            return _json(start_response, 200, {"ok": True, "service": "hugpy-core", "version": version("hugpy-core")},
                         head=method == "HEAD")
        if path in ("/dbviewer", "/static/dbviewer.js", "/static/dbviewer.css"):
            name = "dbviewer.html" if path == "/dbviewer" else path.rsplit("/", 1)[-1]
            viewer = os.path.join(os.path.dirname(__file__), "static", name)
            return self._file(viewer, method, start_response)
        if path == "/video" or path.startswith("/video/"):
            # Video owns its bundle. Core wheels deliberately exclude arm assets.
            spec = importlib.util.find_spec("hugpy_video")
            locations = spec.submodule_search_locations if spec else None
            video_root = os.path.realpath(os.path.join(next(iter(locations)), "ui_dist")) if locations else ""
            rel = path[len("/video/"):] if path.startswith("/video/") else ""
            target = os.path.realpath(os.path.join(video_root, rel)) if video_root else ""
            inside = bool(video_root) and (target == video_root or target.startswith(video_root + os.sep))
            if inside and os.path.isdir(target):
                target = os.path.join(target, "index.html")
            if inside and not os.path.isfile(target) and not os.path.splitext(rel)[1] and not rel.startswith("assets/"):
                target = os.path.join(video_root, "index.html")
            if not inside or not os.path.isfile(target):
                start_response("404 Not Found", [("Content-Type", "text/plain")])
                return [b"" if method == "HEAD" else b"video asset not found\n"]
            return self._file(target, method, start_response)
        if path == "/fit" or path.startswith("/fit/"):
            fit_root = os.environ.get("HUGPY_CORE_FIT_UI_DIST") or os.path.join(
                os.path.dirname(self.root), "dist-fit")
            fit_root = os.path.realpath(fit_root)
            rel = path[len("/fit/"):] if path.startswith("/fit/") else ""
            target = os.path.realpath(os.path.join(fit_root, rel)) if rel else ""
            inside = target.startswith(fit_root + os.sep)
            f = target if inside and os.path.isfile(target) else os.path.join(fit_root, "index.html")
            if not os.path.isfile(f):
                start_response("404 Not Found", [("Content-Type", "text/plain")])
                return [b"fit station is not built\n"]
            return self._file(f, method, start_response)
        rel = path.lstrip("/")
        f = os.path.realpath(os.path.join(self.root, rel)) if rel else ""
        inside = f.startswith(self.root + os.sep)
        if inside and os.path.isdir(f):
            f = os.path.join(f, "index.html")
        if not (inside and os.path.isfile(f)):
            arm = os.path.join(self.root, rel.split("/", 1)[0], "index.html") if "/" in rel else ""
            if arm and os.path.isfile(arm):
                f = arm
            elif page:
                f = os.path.join(self.root, "index.html")
            else:
                return _no_such_path(path, start_response, head=method == "HEAD")
        return self._file(f, method, start_response)

    @staticmethod
    def _file(f, method, start_response):
        headers = [("Content-Type", mimetypes.guess_type(f)[0] or "application/octet-stream"),
                   ("Content-Length", str(os.path.getsize(f)))]
        if f.endswith("index.html"):
            headers.append(("Cache-Control", "no-store"))
        start_response("200 OK", headers)
        if method == "HEAD":
            return [b""]
        with open(f, "rb") as fh:
            return [fh.read()]


def wrap(api):
    """``api`` behind the console when a UI build is configured, else ``api`` as is."""
    root = ui_dist()
    if not root:
        return api
    logger.info("console: %s at /, core's routes at %s/", root, API_PREFIX)
    return ConsoleApp(api, root)


__all__ = ["ConsoleApp", "LiveApi", "PagesForBrowsers", "wrap", "ui_dist", "API_PREFIX", "LIVE_PREFIX", "LIVE_SECTIONS", "LIVE_USE_ROUTES", "CONSOLE_PAGES"]
