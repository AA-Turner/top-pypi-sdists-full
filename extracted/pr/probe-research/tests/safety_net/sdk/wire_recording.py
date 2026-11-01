"""Requests a fake Probe server received, as stable JSON for a baseline.

Ids, times, tmp paths, hosts, pids, ports and versions become placeholders; the rest is kept.
"""

from __future__ import annotations

import gzip
import json
import os
import re
import socket
from collections.abc import Iterable
from typing import Any

import httpx

#: Header names httpx adds on its own: a library detail, not the product's wire.
HTTPX_OWNED_HEADERS = frozenset({"accept", "accept-encoding", "connection", "content-length", "host", "user-agent"})

_UUID = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
# 12+ hex chars with a letter in them (uuid4().hex, sha256, short ids); pure digits stay.
_HEX = re.compile(r"(?<![0-9A-Za-z])(?=[0-9a-f]*[a-f])[0-9a-f]{12,}(?![0-9A-Za-z])")
_TIME = re.compile(
    r"\d{4}-\d{2}-\d{2}[T _]\d{2}[:\-]?\d{2}[:\-]?\d{2}(?:[.,]\d+)?(?:Z|[+-]\d{2}:?\d{2})?"
)
#: pytest's per-session temp root, wherever TMPDIR puts it.
_BASETEMP = re.compile(r"(?:/[\w.\-]+)*/pytest-of-[^/\s\"']+/pytest-\d+")
_COMPACT_TIME = re.compile(r"(?<!\d)20\d{6}[-_T]?\d{6}(?!\d)")
#: Keys whose number is a clock reading or a measured duration, never a constant.
_CLOCK_KEY = re.compile(
    r"(_at|_time|time_ns|_ts|timestamp|_seconds|_secs|_ms|_ns|duration|elapsed|latency|uptime|pid)$"
)


class Normaliser:
    """Replaces what differs between runs; numbers each distinct id by first sight."""

    def __init__(self, literals: dict[str, str] | None = None) -> None:
        self._literals = sorted(
            {**_ambient_paths(), **(literals or {})}.items(), key=lambda kv: -len(kv[0])
        )
        self._tokens = _ambient_tokens()
        self._ids: dict[str, str] = {}

    def _id(self, kind: str, value: str) -> str:
        key = value.lower()
        if key not in self._ids:
            count = sum(1 for v in self._ids.values() if v.startswith(f"<{kind}:"))
            self._ids[key] = f"<{kind}:{count + 1}>"
        return self._ids[key]

    def text(self, value: str) -> str:
        for literal, placeholder in self._literals:
            if literal:
                value = value.replace(literal, placeholder)
        for pattern, placeholder in self._tokens:
            value = pattern.sub(placeholder, value)
        value = _BASETEMP.sub("<basetemp>", value)
        value = _TIME.sub("<time>", value)
        value = _COMPACT_TIME.sub("<time>", value)
        value = _UUID.sub(lambda m: self._id("uuid", m.group(0)), value)
        return _HEX.sub(lambda m: self._id(f"hex{len(m.group(0))}", m.group(0)), value)

    def value(self, value: Any, key: str = "") -> Any:
        if isinstance(value, dict):
            return {self.text(str(k)): self.value(v, str(k)) for k, v in value.items()}
        if isinstance(value, list):
            return [self.value(v, key) for v in value]
        if isinstance(value, str):
            return self.text(value)
        if isinstance(value, (int, float)) and not isinstance(value, bool) and _CLOCK_KEY.search(key.lower()):
            return f"<{type(value).__name__}>"
        return value


def _ambient_tokens() -> list[tuple[re.Pattern, str]]:
    """This machine's name and this build's version, matched as whole tokens only."""
    import probe

    return [
        (re.compile(rf"(?<![\w.-]){re.escape(token)}(?![\w-]|\.\w)"), placeholder)
        for token, placeholder in ((socket.gethostname(), "<host>"), (probe.__version__, "<version>"))
        if token
    ]


def _ambient_paths() -> dict[str, str]:
    found = {}
    for name in ("HOME", "PROBE_OUTBOX_DIR", "XDG_STATE_HOME", "XDG_CONFIG_HOME"):
        if os.environ.get(name):
            found[os.environ[name]] = f"<{name.lower()}>"
    return found


def _body(request: httpx.Request) -> Any:
    raw = request.content
    if not raw:
        return None
    if (request.headers.get("content-encoding") or "").lower() == "gzip":
        raw = gzip.decompress(raw)
    try:
        return {"json": json.loads(raw)}
    except (ValueError, UnicodeDecodeError):
        return {"bytes": len(raw)}


def record(request: httpx.Request, normaliser: Normaliser) -> dict:
    """One request: method, path, sorted query KEYS, product header NAMES, body."""
    url = request.url
    entry: dict[str, Any] = {"method": request.method, "path": normaliser.text(url.path)}
    if url.params:
        entry["query"] = sorted(set(url.params.keys()))
    entry["headers"] = " ".join(sorted({k.lower() for k in request.headers.keys()} - HTTPX_OWNED_HEADERS))
    body = _body(request)
    if body is not None:
        entry.update(normaliser.value(body))
    return entry


def in_stable_order(requests: Iterable[httpx.Request]) -> list[httpx.Request]:
    """Sort each run of consecutive PUTs by path: multipart parts go out in parallel."""
    ordered: list[httpx.Request] = []
    block: list[httpx.Request] = []
    for request in [*requests, None]:
        if request is not None and request.method == "PUT":
            block.append(request)
            continue
        ordered.extend(sorted(block, key=lambda r: r.url.path))
        block = []
        if request is not None:
            ordered.append(request)
    return ordered


def recording(requests: Iterable[httpx.Request], literals: dict[str, str] | None = None) -> list[dict]:
    """Every request, normalised, in the order the server saw them (parallel PUTs sorted)."""
    normaliser = Normaliser(literals)
    return [record(r, normaliser) for r in in_stable_order(requests)]
