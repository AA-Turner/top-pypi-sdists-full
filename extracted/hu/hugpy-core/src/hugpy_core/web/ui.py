"""The console, served by core itself: one address for the UI and its API.

    /api/<path>   core's own routes at /<path> (what nginx's `location /api/` did)
    /v1/<path>    core's OpenAI-compatible relay, unchanged (nginx's `location /v1/`)
    /<anything>   the built console (env HUGPY_CORE_UI_DIST = its dist/ dir); an
                  unknown path gets index.html (client-side routing), an arm page
                  (/fleet/..., /media/...) its own index.html

Without HUGPY_CORE_UI_DIST the console packaged in the wheel (web/console/) is served;
a dir with no index.html means core serves its routes only.
"""
from __future__ import annotations

import logging
import importlib.util
import mimetypes
import os
from typing import Optional

from hugpy_core.imports import constants as _C

logger = logging.getLogger("hugpy_core")

API_PREFIX = "/api"


# the published @hugpy/ui build shipped inside the wheel (console/PROVENANCE.md)
PACKAGED_DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "console")


def ui_dist() -> Optional[str]:
    d = os.environ.get(_C.ENV_UI_DIST, "").strip() or PACKAGED_DIST
    if d and os.path.isfile(os.path.join(d, "index.html")):
        return os.path.realpath(d)
    if d:
        logger.warning("%s=%s has no index.html: console not served", _C.ENV_UI_DIST, d)
    return None


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
        if method not in ("GET", "HEAD"):
            start_response("405 Method Not Allowed", [("Content-Type", "text/plain"), ("Allow", "GET, HEAD")])
            return [b"method not allowed\n"]
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
            f = arm if arm and os.path.isfile(arm) else os.path.join(self.root, "index.html")
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


__all__ = ["ConsoleApp", "wrap", "ui_dist", "API_PREFIX"]
