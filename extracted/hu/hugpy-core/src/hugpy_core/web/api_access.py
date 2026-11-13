"""Same-origin console controls for the OpenAI-compatible API.

These endpoints stay on core's Flask surface so the packaged console can mint
and revoke use keys and apply the selected requirement mode without relying on
the retired aiohttp Basic app.
"""
from __future__ import annotations

import os
import hmac
import threading
import time
import math

from flask import jsonify, request
from abstract_flask import get_bp, register_categories, spec

from hugpy_core.router.observability import store as routing

api_access_bp, logger = get_bp("api_access_bp", __name__)
_lock = threading.Lock()
_SETTING = "require_key_mode"
_MODES = ("never", "outside", "always")
_TABLE = "hugpy_console_settings"
_INSTALL_BRIDGE_FILE = "/etc/hugpy/install-link-bridge.secret"


def valid_use_authorization(auth):
    """Shared bearer validation for HTTP and hosted arms."""
    token = auth[7:].strip() if auth.lower().startswith("bearer ") else ""
    return bool(token and routing.KEYS.scope_of(token) in ("use", "admin"))


def principal():
    """Who is calling, as the key gate judges the current request:
    ``{"scope", "inside", "console", "role"}``.

    scope "admin": an admin key, or this box itself (a direct loopback caller: the gate's own
    rule for managing the box). "use": a valid use key, or a caller the requirement mode admits
    to the model API without one. None: nobody the gate would admit. ``inside`` says whether
    the caller's address is on this box or its trusted networks.

    ``console`` is True when the request came through a front's session gate (its verified
    marker, from a configured console proxy address); ``role`` is then what that front said of
    the session (X-Hugpy-Role), which Core passes on and does not interpret. Such a request
    reaches Core from the front's own address, so its scope reads as this box: a caller that
    must tell the operator from any signed-in session looks at ``role`` as well.

    Hosted arms receive this function with Core's other services, so one rule decides who is
    calling everywhere."""
    class RequestView:
        client_address = (request.remote_addr or "", 0)
        headers = request.headers

    view = RequestView()
    proxies = {value.strip() for value in os.environ.get(
        'HUGPY_CONSOLE_PROXY_ADDRS', '127.0.0.1,::1').split(',') if value.strip()}
    console = (request.remote_addr in proxies
               and request.headers.get('X-Hugpy-Console-Authenticated') == '1')
    who = {"scope": None, "inside": routing.KEYS.is_inside(view), "console": console,
           "role": request.headers.get('X-Hugpy-Role') if console else None}
    for scope in ("admin", "use"):
        if routing.KEYS.check(view, scope) is None:
            who["scope"] = scope
            break
    return who


def verify_use_key():
    """Nginx auth_request gate for the public media/video API projection."""
    if valid_use_authorization(request.headers.get("Authorization", "")):
        return "", 204
    return jsonify({"error": "A valid Hugpy API key is required"}), 401


def _ensure_settings():
    routing.STORE.write(f"CREATE TABLE IF NOT EXISTS {_TABLE} (key TEXT PRIMARY KEY, value TEXT NOT NULL)")


def initialize_api_access():
    """Restore the console's persisted key gate before requests are served."""
    try:
        _ensure_settings()
        rows = routing.STORE.read(f"SELECT value FROM {_TABLE} WHERE key = ?", (_SETTING,))
        if rows and rows[0]["value"] in _MODES:
            os.environ[routing.KEYS.env_require] = rows[0]["value"]
    except Exception:  # noqa: BLE001 - the endpoint surfaces persistence errors to operators
        return


def _mode_view():
    mode = routing.KEYS.require_mode()
    return {"require_key": mode == "always", "mode": mode}


def _set_mode(mode):
    _ensure_settings()
    routing.STORE.write(f"INSERT INTO {_TABLE} (key, value) VALUES (?, ?) "
                        "ON CONFLICT(key) DO UPDATE SET value = excluded.value", (_SETTING, mode))
    os.environ[routing.KEYS.env_require] = mode


def _panel_key(key):
    exp = key.get("expires_at")
    guest = key.get("created_by") == "guest-pass"
    return {**key, "kind": "guest" if guest else "api", "scopes": ["guest" if guest else key.get("scope")], "prefix": f"hpk_{key['id']}",
            "last_used": key.get("last_used_at"), "expired": bool(exp and exp < time.time())}


def install_link_key():
    """Private, shared-secret bridge for the Agent install-link service.

    The same Core KeyAuth store that enforces /v1 issues and revokes these keys.
    The secret file is provisioned by the Core and Agent Debian postinst scripts.
    """
    try:
        with open(_INSTALL_BRIDGE_FILE, encoding="ascii") as fh:
            expected = fh.read().strip()
    except OSError:
        return jsonify({"error": "install-link key bridge unavailable"}), 503
    supplied = request.headers.get("X-Hugpy-Install-Bridge", "")
    if not expected or not hmac.compare_digest(supplied, expected):
        return jsonify({"error": "forbidden"}), 403
    body = request.get_json(silent=True) or {}
    action = body.get("action")
    if action == "create":
        label = str(body.get("label") or "").strip()
        link_id = str(body.get("link_id") or "")
        if not label or not link_id or len(link_id) > 128:
            return jsonify({"error": "label and link_id are required"}), 400
        expiry = body.get("expires_at")
        try:
            expires_days = max(0, (float(expiry) - time.time()) / 86400) if expiry is not None else None
            if expiry is not None and expires_days <= 0:
                raise ValueError("key expiry must be in the future")
            key = routing.KEYS.create(label, "use", expires_days,
                                      created_by=f"install-link:{link_id}")
        except (TypeError, ValueError) as exc:
            return jsonify({"error": str(exc)}), 400
        return jsonify({"id": key["id"], "key": key["key"], "scope": "use",
                        "expires_at": key["expires_at"]}), 201
    if action == "revoke":
        key_id = str(body.get("key_id") or "")
        return jsonify({"revoked": routing.KEYS.revoke(key_id)})
    return jsonify({"error": "unknown action"}), 400


@api_access_bp.before_app_request
def enforce_api_key_mode():
    # Console session routes remain usable; this gate applies to the public
    # OpenAI-compatible API and task endpoints only.
    path = request.path.removeprefix("/api")
    if not (path == "/v1" or path.startswith("/v1/")):
        return None

    # The /api alias is session-gated at the configured reverse proxy. Its
    # verified marker is overwritten there, never trusted on the public /v1 API
    # or from an arbitrary client address.
    peer = (request.environ.get('werkzeug.proxy_fix.orig') or {}).get('REMOTE_ADDR', request.remote_addr)
    proxies = {value.strip() for value in os.environ.get(
        'HUGPY_CONSOLE_PROXY_ADDRS', '127.0.0.1,::1').split(',') if value.strip()}
    # ConsoleApp removes /api from PATH_INFO and records it in SCRIPT_NAME.
    # Reconstruct the mounted path so both WSGI and direct Flask aliases retain
    # the console's authenticated boundary.
    mounted_path = request.script_root.rstrip('/') + request.path
    if (mounted_path.startswith('/api/v1/') and peer in proxies
            and request.headers.get('X-Hugpy-Console-Authenticated') == '1'):
        return None

    class RequestView:
        client_address = (request.remote_addr or "", 0)
        headers = request.headers

    denied = routing.KEYS.check(RequestView(), "use")
    if denied is None:
        return None
    status, body = denied
    return jsonify(body), status


def keys_list():
    """GET /keys: the console's key panel rows plus the enforcement mode."""
    try:
        rows = routing.KEYS.list_keys()
        return {"keys": [_panel_key(row) for row in rows], **_mode_view()}
    except Exception as exc:  # noqa: BLE001
        return {"error": f"API key store unavailable: {exc}"}, 503


def keys_create(name=None, expires_days=None, kind=None, **_body):
    """POST /keys: mint a ``use`` key for the console (or a guest pass, which
    must expire). 201 with the panel row plus the one-time ``key``."""
    try:
        guest = kind == "guest"
        days = expires_days
        if days is not None:
            days = float(days)
            if not math.isfinite(days) or days <= 0 or days > 365:
                raise ValueError("duration must be greater than zero and at most 365 days")
        if guest and days is None:
            raise ValueError("guest passes require an expiry duration")
        key = routing.KEYS.create(name, "use", days,
                                  created_by="guest-pass" if guest else "console")
        key["created_by"] = "guest-pass" if guest else "console"
    except (ValueError, TypeError) as exc:
        return {"error": str(exc)}, 400
    return {**_panel_key(key), "key": key["key"]}, 201


def keys_require_get():
    """GET /keys/require: the current enforcement mode."""
    return _mode_view()


def keys_require_set(require=None, mode=None, **_body):
    """POST|PUT /keys/require: who needs an API key on /v1 and /live-api.

    ``{require: bool}``, the console's switch: on is "always" (everybody, local callers
    included), off is "never". ``{mode: "never" | "outside" | "always"}`` names a state outright;
    "outside" asks a key only of callers from outside this box and its trusted networks."""
    if mode is None:
        mode = "always" if require else "never"
    mode = str(mode).strip().lower()
    if mode not in _MODES:
        return {"error": f"mode must be one of {', '.join(_MODES)}"}, 400
    try:
        _set_mode(mode)
    except Exception as exc:  # noqa: BLE001
        return {"error": f"Could not save API key requirement: {exc}"}, 503
    return _mode_view()


def keys_prune(older_than_days=None, expired=None, unused_only=None, **_body):
    """POST /keys/prune: revoke expired keys and/or keys older than N days."""
    try:
        days = float(older_than_days) if older_than_days else None
    except (TypeError, ValueError):
        return {"error": "older_than_days must be a number"}, 400
    now = time.time()
    removed = 0
    for key in routing.KEYS.list_keys():
        is_expired = bool(expired and key.get("expires_at") and key["expires_at"] < now)
        aged = bool(days and key.get("created_at") and now - key["created_at"] > days * 86400
                    and (not unused_only or not key.get("last_used_at")))
        if (is_expired or aged) and routing.KEYS.revoke(key["id"]):
            removed += 1
    return {"count": removed}


def key_revoke(key_id=None, **_body):
    """DELETE|POST /keys/<key_id>: revoke one active key."""
    if not routing.KEYS.revoke(key_id):
        return {"error": "no such active key"}, 404
    return {"id": key_id, "revoked": True}


# The keys surface as a tree. ``verify_use_key`` and ``install_link_key`` read
# headers (nginx auth_request / the install-link shared secret), so they stay
# raw-request views (``inputs="path"``); everything else is kwargs in, data out.
ALL_CATEGORIES = {
    "keys": {
        "": [                                                       # /keys
            spec(keys_list, "GET", response="native"),
            spec(keys_create, "POST", response="native"),
        ],
        "verify-use": spec(verify_use_key, "GET,HEAD", response="native", inputs="path"),
        "install-link": spec(install_link_key, "POST", response="native", inputs="path"),
        "require": [                                                # /keys/require
            spec(keys_require_get, "GET", response="native"),
            spec(keys_require_set, "POST,PUT", response="native"),
        ],
        "prune": spec(keys_prune, "POST", response="native"),
        "<key_id>": spec(key_revoke, "DELETE,POST", response="native"),   # /keys/<key_id>
    },
}
register_categories(api_access_bp, ALL_CATEGORIES)
