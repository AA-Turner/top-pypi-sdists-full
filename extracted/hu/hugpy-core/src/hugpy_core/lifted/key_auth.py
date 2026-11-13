"""Lifted from fitevict/serve/auth.py (sha256 abba8ee563f9fb2f): KeyAuth, parse and what they reach in that file.
Written by tools/refactors/core-off-fitevict-20261110/lift.py. One change since (2026-11-12), in
KeyAuth.client: a request forwarded by a trusted proxy is known only by an untrusted hop of its
X-Forwarded-For; the original fell back to the proxy's own address."""
from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import threading
import time
from typing import List, Optional, Tuple

from hugpy_resources.imports.functions.http_auth import _addr, _in, _nets, bearer

FORWARD_HEADERS = ('X-Forwarded-For', 'Forwarded', 'X-Real-IP')      # imports.constants.serving.AUTH_FORWARD_HEADERS
LAST_USED_EVERY_S = 60                                                 # imports.constants.serving.AUTH_LAST_USED_EVERY_S
_owned_C_BOX_KEY_ID = 'box'                                            # imports.constants.authentication
_owned_C_DEFAULT_TRUSTED_NETS = ('127.0.0.0/8', '::1/128', '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', 'fd00::/8', 'fe80::/10')
_owned_C_KEY_PREFIX = 'hpk_'
_owned_C_KEY_SCOPES = ('use', 'admin')


def _hash(secret: str) -> str:
    return hashlib.sha256(secret.encode()).hexdigest()


def parse(key: str) -> Optional[Tuple[str, str]]:
    """(id, secret) of a well-formed key, else None."""
    if not key or not key.startswith(_owned_C_KEY_PREFIX):
        return None
    kid, sep, secret = key[len(_owned_C_KEY_PREFIX):].partition("_")
    return (kid, secret) if sep and kid and secret else None


def _error(message: str, code: str = "invalid_api_key") -> dict:
    return {"error": {"message": message, "type": "invalid_request_error", "code": code}}


class KeyAuth:
    """Keys + the inside/outside rule for one component: its store (which holds
    the api_keys table — migration 0002 of the wrapper's schema, or the same
    table in the component's own) and the names of its settings."""

    def __init__(self, store, env_box_key: str, env_require: str, env_trusted_nets: str,
                 env_trusted_proxies: str):
        self.store = store
        self.env_box_key = env_box_key
        self.env_require = env_require
        self.env_trusted_nets = env_trusted_nets
        self.env_trusted_proxies = env_trusted_proxies
        self._last_used: dict = {}
        self._lock = threading.Lock()

    # keys
    def create(self, name: str, scope: str = "use", expires_days: Optional[float] = None,
               created_by: Optional[str] = None) -> dict:
        """Make a key; the full key is in the result ONCE (only its hash is kept)."""
        if scope not in _owned_C_KEY_SCOPES:
            raise ValueError(f"scope must be one of {', '.join(_owned_C_KEY_SCOPES)}")
        name = (name or "").strip()
        if not name:
            raise ValueError("a key needs a name (who or what uses it)")
        kid, secret = secrets.token_hex(5), secrets.token_urlsafe(32)
        expires = time.time() + float(expires_days) * 86400 if expires_days else None
        self.store.write("INSERT INTO api_keys (id, name, scope, secret_hash, created_by, expires_at) "
                         "VALUES (?, ?, ?, ?, ?, ?)", (kid, name, scope, _hash(secret), created_by, expires))
        return {"id": kid, "name": name, "scope": scope, "expires_at": expires,
                "key": f"{_owned_C_KEY_PREFIX}{kid}_{secret}"}

    def list_keys(self, include_revoked: bool = False) -> List[dict]:
        rows = self.store.read("SELECT id, name, scope, created_at, created_by, expires_at, last_used_at, "
                               "revoked_at FROM api_keys"
                               + ("" if include_revoked else " WHERE revoked_at IS NULL") + " ORDER BY created_at")
        return [dict(r) for r in rows]

    def revoke(self, kid: str) -> bool:
        with self.store.transaction() as c:
            n = c.execute("UPDATE api_keys SET revoked_at = ? WHERE id = ? AND revoked_at IS NULL",
                          (time.time(), kid)).rowcount
        return n > 0

    def scope_of(self, key: str) -> Optional[str]:
        """'admin' / 'use' for a valid key, else None."""
        box = os.environ.get(self.env_box_key, "").strip()
        if box and hmac.compare_digest(key.encode(), box.encode()):
            return "admin"
        parsed = parse(key)
        if not parsed or parsed[0] == _owned_C_BOX_KEY_ID:
            return None
        kid, secret = parsed
        try:
            r = self.store.read_one("SELECT scope, secret_hash, expires_at, revoked_at FROM api_keys WHERE id = ?",
                                    (kid,))
        except Exception:  # noqa: BLE001 — a store problem never lets a key through
            return None
        now = time.time()
        if r is None or r["revoked_at"] is not None or (r["expires_at"] is not None and r["expires_at"] < now):
            return None
        if not hmac.compare_digest(_hash(secret), r["secret_hash"]):
            return None
        self._touch(kid, now)
        return r["scope"]

    def _touch(self, kid: str, now: float) -> None:
        with self._lock:
            if now - self._last_used.get(kid, 0) < LAST_USED_EVERY_S:
                return
            self._last_used[kid] = now
        try:
            self.store.write("UPDATE api_keys SET last_used_at = ? WHERE id = ?", (now, kid))
        except Exception:  # noqa: BLE001
            pass

    # where a request comes from
    def client(self, handler) -> Tuple[Optional[object], bool]:
        """(the caller's address, whether it is known) — see the module doc on
        proxies. Unknown = forwarded through a proxy we do not trust."""
        peer = _addr(handler.client_address[0])
        headers = handler.headers
        if not any(headers.get(h) for h in FORWARD_HEADERS):
            return peer, True
        proxies = _nets(os.environ.get(self.env_trusted_proxies), ())
        if not _in(peer, proxies):
            return None, False
        chain = [a.strip() for a in (headers.get("X-Forwarded-For") or "").split(",") if a.strip()]
        for hop in reversed(chain):
            a = _addr(hop)
            if a is None:
                return None, False
            if not _in(a, proxies):
                return a, True
        # Forwarded, yet no hop that is not one of our proxies: a front location that wrote no
        # X-Forwarded-For (only X-Real-IP or Forwarded, which a client can send itself), or a
        # chain of proxies alone. The caller is not the proxy; it is nobody we can name.
        return None, False

    def is_inside(self, handler) -> bool:
        addr, known = self.client(handler)
        return known and _in(addr, _nets(os.environ.get(self.env_trusted_nets), _owned_C_DEFAULT_TRUSTED_NETS))

    def is_loopback(self, handler) -> bool:
        """The caller is this box: loopback, or a peer whose address is the very
        address this connection was accepted on. The service listens on its LAN
        address (the installer's --host), so a same-box caller — the harness, core
        on this host — arrives from that address, never from 127.0.0.1; only a
        program on this host can open a connection from the host's own address
        (a spoofed source could never complete the handshake). The LAN at large
        stays outside: any other peer address is not local."""
        addr, known = self.client(handler)
        if not known or addr is None:
            return False
        if addr.is_loopback:
            return True
        sock = getattr(handler, "request", None)
        try:
            own = _addr(sock.getsockname()[0]) if sock is not None else None
        except (OSError, AttributeError, IndexError, TypeError):
            own = None
        return own is not None and not own.is_unspecified and addr == own

    # the checks
    def require_mode(self) -> str:
        mode = os.environ.get(self.env_require, "outside").strip().lower() or "outside"
        return mode if mode in ("never", "outside", "always") else "always"   # a typo fails closed

    def check(self, handler, need: str) -> Optional[Tuple[int, dict]]:
        """None when the request may proceed, else (status, OpenAI-style error)."""
        if need == "admin":
            # management is machine-to-machine (core / router hold the box key):
            # this box (loopback, or the box's own address — see is_loopback) or an
            # admin key, from anywhere else (the designed rule; a LAN relax shipped
            # as 0.1.82 was reverted the same night — an operator acts through the
            # console's login, not through this door)
            if self.is_loopback(handler):
                return None
        else:
            mode = self.require_mode()
            if mode == "never" or (mode == "outside" and self.is_inside(handler)):
                return None
        key = bearer(handler)
        if not key:
            return 401, _error("an API key is required from here: send Authorization: Bearer hpk_…")
        scope = self.scope_of(key)
        if scope is None:
            return 401, _error("invalid, expired or revoked API key")
        if need == "admin" and scope != "admin":
            return 403, _error("this key cannot manage the box (scope use); an admin key is needed",
                               code="insufficient_scope")
        return None
