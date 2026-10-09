"""The virtual clipboard's store. Identical in every mode, so shared:
``testmu.ClipboardStore`` is this class, and each mode's ``_helpers.clipboard``
re-exports it (the interception script and query executor stay per mode).
"""
from __future__ import annotations

import base64
import hashlib
import logging

logger = logging.getLogger("testmu.clipboard")

_PREVIEW_LEN = 100


class ClipboardStore:
    """One current entry (real clipboard semantics, replace-on-copy).

    Representations: list of {"mime": str, "text": str} for text/* types or
    {"mime": str, "data_b64": str} for binary types. Content is runtime-only —
    never serialized to recordings or exports.
    """

    def __init__(self) -> None:
        self._reps: list[dict] = []

    # -- mutations ----------------------------------------------------------

    def write(self, text: str, html: str | None = None) -> None:
        reps = [{"mime": "text/plain", "text": str(text)}]
        if html:
            reps.append({"mime": "text/html", "text": str(html)})
        self.replace_from_reps(reps, source="write")

    def clear(self) -> None:
        self._reps = []
        logger.info("[clipboard] cleared")

    def replace_from_reps(self, reps: list[dict], source: str = "capture") -> None:
        cleaned = []
        for r in reps or []:
            mime = str(r.get("mime") or "")
            if not mime:
                continue
            if "text" in r and r["text"] is not None:
                cleaned.append({"mime": mime, "text": str(r["text"])})
            elif r.get("data_b64"):
                cleaned.append({"mime": mime, "data_b64": str(r["data_b64"])})
        self._reps = cleaned
        logger.info("[clipboard] %s: %s", source, self.summary())

    # -- bridge/paste payload ------------------------------------------------

    def to_reps(self) -> list[dict]:
        return list(self._reps)

    def summary(self) -> str:
        if not self._reps:
            return "(empty)"
        parts = []
        for r in self._reps:
            size = self.size(r["mime"])
            preview = ""
            if "text" in r:
                t = r["text"][:_PREVIEW_LEN]
                preview = f' "{t}{"…" if len(r["text"]) > _PREVIEW_LEN else ""}"'
            parts.append(f"{r['mime']} ({size} B){preview}")
        return "; ".join(parts)

    # -- query API (scalar-only, analyzer-facing) ----------------------------

    def _rep(self, mime: str) -> dict | None:
        for r in self._reps:
            if r["mime"] == mime:
                return r
        return None

    def text(self) -> str:
        r = self._rep("text/plain")
        return r["text"] if r else ""

    def html(self) -> str:
        r = self._rep("text/html")
        return r["text"] if r else ""

    def types(self) -> list[str]:
        return [r["mime"] for r in self._reps]

    def has(self, mime: str) -> bool:
        return self._rep(mime) is not None

    def _bytes(self, mime: str) -> bytes:
        r = self._rep(mime)
        if r is None:
            return b""
        if "text" in r:
            return r["text"].encode("utf-8")
        return base64.b64decode(r["data_b64"])

    def size(self, mime: str) -> int:
        return len(self._bytes(mime))

    def sha256(self, mime: str) -> str:
        data = self._bytes(mime)
        return hashlib.sha256(data).hexdigest() if data else ""
