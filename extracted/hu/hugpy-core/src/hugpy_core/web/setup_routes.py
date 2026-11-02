"""GET /api/setup/status — what `hugpy-core install` set up, so the console can show
the orbit's shape. STABLE JSON (documented below); carries NO secrets. Read from the
endpoint file the installer wrote (install/installer.py step 8) plus a short live
health probe; core never crashes if the file is absent — absences are reported as nulls.

Shape (stable):
  {
    "ok": true,
    "endpoint_present": bool,            # was core.endpoint.json found
    "db": {
      "server":       "own" | "existing" | null,   # the database server the installer chose
      "mode":         same as server (the install mode),
      "socket_dir":   str | null,        # own mode: the orbit cluster's unix socket dir
      "host":         str | null,        # existing/create-db: the db host
      "port":         int | null,        # 7305 for the orbit's own cluster
      "core_db":      str | null,        # core's database (or "<db> schema <schema>")
      "core_schema":  str | null,        # existing-DSN mode only
      "toolserver_db":str | null,        # the orbit toolserver's own database
      "ready":        bool | null        # the db CLI's readiness, as last recorded
    },
    "core":    {"url": str|null, "health": "ok"|"down"|null},
    "wrapper": {"url": str|null, "health": "ok"|"down"|null},
    "router":  {"url": str|null, "health": "ok"|"down"|null}
  }

Access: loopback-direct (the request came from 127.0.0.1/::1) OR a bearer token equal to
the operator toolserver token core holds (HUGPY_CORE_TOOLSERVER_TOKEN). Off-box without the
token is 403 with an honest reason. No secret is ever in the response.
"""
from __future__ import annotations

import json
import os
import urllib.request

from flask import jsonify, request

from hugpy_core.imports import constants as _C


def _json(payload, status=200):
    """Wrap JSON-able data in a Response so register_route passes the custom
    status through (a returned (body, status) tuple would be re-wrapped)."""
    r = jsonify(payload)
    r.status_code = status
    return r


_LOOPBACK = {"127.0.0.1", "::1", "::ffff:127.0.0.1"}
ENV_TS_TOKEN = "HUGPY_CORE_TOOLSERVER_TOKEN"


def _endpoint() -> dict:
    """The installer's endpoint file (no secrets in it), or {} when it is not there."""
    try:
        from hugpy_core.install.installer import layout
        with open(layout().endpoint_file, encoding="utf-8") as fh:
            return json.load(fh) or {}
    except Exception:  # noqa: BLE001 — never crash the route on a missing/odd file
        return {}


def _health(base: str, path: str) -> "str | None":
    if not base:
        return None
    try:
        with urllib.request.urlopen(base.rstrip("/") + path, timeout=2) as r:
            return "ok" if r.status == 200 else "down"
    except Exception:  # noqa: BLE001
        return "down"


def _allowed() -> bool:
    if (request.remote_addr or "") in _LOOPBACK:
        return True
    tok = os.environ.get(ENV_TS_TOKEN, "").strip()
    auth = request.headers.get("Authorization", "")
    given = auth[7:].strip() if auth[:7].lower() == "bearer " else (request.args.get("token") or "").strip()
    return bool(tok) and given == tok


def setup_status(**kwargs):
    # Access is decided from the request (loopback / operator token), not body input.
    if not _allowed():
        return _json({"ok": False, "error": "setup status is loopback-only; from off the box pass the "
                                             "operator toolserver token as a Bearer token"}, 403)
    ep = _endpoint()
    srv = ep.get("db_server") or {}
    db = {"server": srv.get("mode") or ep.get("db_mode"), "mode": ep.get("db_mode"),
          "socket_dir": srv.get("socket_dir"), "host": srv.get("host"), "port": srv.get("port"),
          "core_db": ep.get("db") or os.environ.get(_C.ENV_CORE_DB),
          "core_schema": ep.get("core_schema") or os.environ.get(_C.ENV_CORE_SCHEMA),
          "toolserver_db": srv.get("database"), "ready": srv.get("ready")}
    return jsonify({
        "ok": True, "endpoint_present": bool(ep), "db": db,
        "core": {"url": ep.get("core"), "health": _health(ep.get("core"), "/api/auth/config")},
        "wrapper": {"url": ep.get("wrapper"), "health": _health(ep.get("wrapper"), "/health")},
        "router": {"url": ep.get("router"), "health": _health(ep.get("router"), "/health")},
    })


# category -> {route_name: callable}
SETUP_CATEGORIES = {
    "setup": {"status": setup_status},
}

__all__ = ["setup_status", "SETUP_CATEGORIES"]
