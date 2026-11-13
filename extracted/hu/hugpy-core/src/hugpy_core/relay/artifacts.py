"""Deliver a task reply's artifacts the way the old front door did.

The standalone wrapper returns its engines' JSON unchanged: each artifact is
``{"path": <worker-local file>, "artifact_id": <plain name>, ...}``, with the
bytes served separately by ``GET /v1/artifacts/{artifact_id}``. The retired
fitevict front door inlined those bytes itself (``b64_json``, OpenAI image
``data`` rows, raw audio), and core's task clients — hosted Video/TTS/imagegen
and external OpenAI-style callers — were written against that contract.

Core is the hop that knows both the caller's asked ``response_format`` and the
worker's artifact handle, so the delivery now happens here. Bytes are read from
the artifact's path when core can see the file (same box), else fetched from
the worker's artifact route. Nothing is deleted: the wrapper owns its
ARTIFACT_DIR housekeeping.
"""
from __future__ import annotations

import base64
import json
import os
import re
import time
import urllib.request

IMAGE_ROUTES = ("/v1/images/generations", "/v1/images/edits")
AUDIO_ROUTES = ("/v1/audio/speech",)
# Larger artifacts stay a path/id reference instead of exhausting core's memory.
MAX_INLINE_BYTES = int(os.environ.get("HUGPY_RELAY_INLINE_MAX_BYTES") or 2 << 30)


def response_format(raw: bytes, ctype: str) -> str:
    """The caller's asked response_format, from a JSON or multipart request body."""
    if (ctype or "").lower().startswith("multipart/"):
        m = re.search(rb'name="response_format"\r\n\r\n([^\r]+)\r\n', raw or b"")
        return m.group(1).decode("utf-8", "replace").strip().lower() if m else ""
    try:
        body = json.loads((raw or b"").decode("utf-8", "replace") or "{}")
    except ValueError:
        return ""
    return str(body.get("response_format") or "").lower() if isinstance(body, dict) else ""


def _fetch(worker: dict, art: dict) -> bytes:
    """An artifact's bytes: the local file when core can read it, else the worker's artifact route."""
    path = art.get("path")
    if isinstance(path, str) and os.path.isfile(path) and os.access(path, os.R_OK):
        if os.path.getsize(path) > MAX_INLINE_BYTES:
            raise ValueError(f"artifact exceeds the inline cap ({os.path.getsize(path)} bytes)")
        with open(path, "rb") as fh:
            return fh.read()
    artifact_id = art.get("artifact_id")
    if not artifact_id or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._\-]*", str(artifact_id)):
        raise ValueError("artifact has no readable path and no plain artifact_id")
    from hugpy_core.registry.transport import headers
    req = urllib.request.Request(worker["url"].rstrip("/") + "/v1/artifacts/" + str(artifact_id),
                                 headers=headers(worker))
    with urllib.request.urlopen(req, timeout=600) as response:
        size = response.headers.get("Content-Length")
        if size and int(size) > MAX_INLINE_BYTES:
            raise ValueError(f"artifact exceeds the inline cap ({size} bytes)")
        data = response.read(MAX_INLINE_BYTES + 1)
    if len(data) > MAX_INLINE_BYTES:
        raise ValueError("artifact exceeds the inline cap")
    return data


def _inline(worker: dict, art: dict) -> dict:
    """The artifact with its bytes inlined as b64_json, or with a stated b64_error."""
    if art.get("b64_json"):
        return art
    try:
        return {**art, "b64_json": base64.b64encode(_fetch(worker, art)).decode("ascii")}
    except Exception as exc:  # noqa: BLE001 — delivery failure is stated, never fabricated
        return {**art, "b64_error": f"{type(exc).__name__}: {exc}"}


def deliver(worker: dict, route: str, request_raw: bytes, request_ctype: str, payload):
    """The reply payload with its artifacts delivered per the asked response_format.

    Returns the (possibly unchanged) payload. Mirrors the retired front door's
    ``render_artifacts``: images grow OpenAI ``data`` rows; audio and an explicit
    ``response_format=b64_json`` inline the bytes; everything else keeps the
    worker's path/artifact_id reference.
    """
    if not isinstance(payload, dict):
        return payload
    arts = [a for a in (payload.get("artifacts") or []) if isinstance(a, dict)
            and (a.get("path") or a.get("artifact_id"))]
    if not arts:
        return payload
    fmt = response_format(request_raw, request_ctype)
    if route in IMAGE_ROUTES:
        out = dict(payload)
        out.setdefault("created", int(time.time()))
        if not out.get("data"):
            data = []
            for art in arts:
                row = {"revised_prompt": art["revised_prompt"]} if art.get("revised_prompt") else {}
                if fmt in ("url", "path"):
                    row.update({"url": "file://" + (art.get("path") or ""), "path": art.get("path")})
                else:
                    inlined = _inline(worker, art)
                    row["b64_json"] = inlined.get("b64_json")
                    if inlined.get("b64_error"):
                        row["b64_error"] = inlined["b64_error"]
                data.append(row)
            out["data"] = data
        return out
    if route in AUDIO_ROUTES and fmt in ("", "json", "b64_json") or fmt == "b64_json":
        return {**payload, "artifacts": [_inline(worker, a) for a in arts]}
    return payload
