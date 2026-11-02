"""Core relays model bytes between wrappers (operator 2026-10-23: central sees
every wrapper and delegates the transfer between them).

A destination wrapper receives `receive-model` with source_url = Core + the relay
path below and a one-transfer credential. It pulls exactly as it would from a
wrapper — /v1/transfer/<model>/manifest | file | chunksums — and Core streams each
request from the source wrapper (its registered address + key), passing Range
through. No wrapper changes: the relay path ends in the usual /v1/transfer/...

    GET /fleet/workers/<source>/v1/transfer/<model_key>/manifest|file|chunksums

Credentials: an HMAC token Core mints per delegated transfer, bound to (source,
model_key, destination) and an expiry. The same token gates Core's own
/llm/models/<key>/* file server (source "core").
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import os
import secrets
import time
import urllib.error
import urllib.parse
import urllib.request

from flask import Blueprint, Response, jsonify, request, stream_with_context

log = logging.getLogger(__name__)
SECRET_PATH = os.environ.get("HUGPY_TRANSFER_SECRET_PATH", "/var/lib/hugpy-core/transfer-relay.secret")
TOKEN_TTL_S = 12 * 3600
CHUNK = 1 << 20
_PASS_HEADERS = ("Content-Type", "Content-Length", "Content-Range", "Accept-Ranges", "Content-Disposition", "ETag")
_secret_cache: bytes | None = None


def _secret() -> bytes:
    global _secret_cache
    if _secret_cache is None:
        try:
            with open(SECRET_PATH, "rb") as fh:
                _secret_cache = fh.read().strip()
        except FileNotFoundError:
            value = secrets.token_hex(32).encode()
            fd = os.open(SECRET_PATH, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "wb") as fh:
                fh.write(value)
            _secret_cache = value
        except FileExistsError:
            return _secret()
    return _secret_cache


def mint(source: str, model_key: str, destination: str, ttl_s: int = TOKEN_TTL_S) -> str:
    """A credential for one transfer: this model, from this source, to this destination."""
    body = json.dumps({"s": source, "m": model_key, "d": destination, "e": int(time.time() + ttl_s)},
                      separators=(",", ":"), sort_keys=True).encode()
    b64 = base64.urlsafe_b64encode(body).decode().rstrip("=")
    sig = hmac.new(_secret(), b64.encode(), hashlib.sha256).hexdigest()
    return f"htr1.{b64}.{sig}"


def verify(token: str, source: str, model_key: str) -> bool:
    try:
        tag, b64, sig = (token or "").split(".", 2)
        if tag != "htr1" or not hmac.compare_digest(sig, hmac.new(_secret(), b64.encode(), hashlib.sha256).hexdigest()):
            return False
        claims = json.loads(base64.urlsafe_b64decode(b64 + "=" * (-len(b64) % 4)))
        return claims.get("s") == source and claims.get("m") == model_key and int(claims.get("e", 0)) > time.time()
    except Exception:  # noqa: BLE001 — anything malformed is a refusal
        return False


def _bearer() -> str:
    h = request.headers.get("Authorization", "")
    return h[7:].strip() if h.lower().startswith("bearer ") else ""


def core_files_authorized() -> bool:
    """Gate for Core's own /llm/models/<key>/* file server: a transfer token for
    source "core", or a registered wrapper's key / the router key (existing pullers)."""
    token = _bearer()
    key = (request.view_args or {}).get("model_key")
    if token and key and verify(token, "core", key):
        return True
    if not token:
        return False
    router = os.environ.get("HUGPY_CORE_ROUTER_KEY", "").strip()
    if router and hmac.compare_digest(token, router):
        return True
    try:
        from hugpy_core.registry import registrations
        return any(c.get("key") and hmac.compare_digest(token, c["key"]) for c in registrations.all())
    except Exception:  # noqa: BLE001
        return False


transfer_relay_bp = Blueprint("transfer_relay", __name__)


@transfer_relay_bp.route("/fleet/workers/<name>/v1/transfer/<path:rest>", methods=["GET"])
def relay(name, rest):
    model_key, _, op = rest.rpartition("/")
    model_key = urllib.parse.unquote(model_key)
    if op not in ("manifest", "file", "chunksums") or not model_key:
        return jsonify(error={"message": "/fleet/workers/<source>/v1/transfer/<model>/manifest|file|chunksums",
                              "code": 404}), 404
    if not verify(_bearer(), name, model_key):
        return jsonify(error={"message": "transfer credential missing, expired or not for this model/source",
                              "code": 403}), 403
    from hugpy_core.registry import registrations
    src = registrations.get(name)
    if not src or not registrations.is_connected(src):
        return jsonify(error={"message": f"source worker {name!r} is not connected", "code": 409}), 409
    url = src["url"].rstrip("/") + "/v1/transfer/" + urllib.parse.quote(model_key, safe="") + "/" + op
    if request.query_string:
        url += "?" + request.query_string.decode()
    headers = {"Accept": request.headers.get("Accept", "*/*")}
    if src.get("key"):
        headers["Authorization"] = "Bearer " + src["key"]
    if request.headers.get("Range"):
        headers["Range"] = request.headers["Range"]
    try:
        upstream = urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=300)
    except urllib.error.HTTPError as exc:
        return Response(exc.read(), status=exc.code, content_type=exc.headers.get("Content-Type", "application/json"))
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return jsonify(error={"message": f"source worker unreachable: {exc}", "code": 502}), 502

    def body():
        try:
            while True:
                chunk = upstream.read(CHUNK)
                if not chunk:
                    break
                yield chunk
        finally:
            upstream.close()

    out = Response(stream_with_context(body()), status=upstream.status, direct_passthrough=True)
    for h in _PASS_HEADERS:
        if upstream.headers.get(h):
            out.headers[h] = upstream.headers[h]
    out.headers["X-Hugpy-Transfer-Source"] = name
    return out
