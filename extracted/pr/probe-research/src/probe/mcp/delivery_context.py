"""Request-local document consistency hints, never public tool arguments/data.

The transport carries the small snapshot in its bound continuation. A native
view pins the document BEFORE selecting rows, so advancing that native cursor
cannot silently start reading a newer document. No context means no hashing or
extra source reads: ordinary SDK/service callers keep their existing behavior.
"""

from __future__ import annotations

import hashlib
import re
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Iterator

from ..sdk import errors


@dataclass
class DeliveryContext:
    snapshot: dict | None = None


_current: ContextVar[DeliveryContext | None] = ContextVar("mcp_delivery", default=None)


def current_delivery() -> DeliveryContext | None:
    return _current.get()


def source_changed(reason: str = "requested content changed") -> errors.ValidationError:
    return errors.ValidationError(f"source_changed: {reason}; restart the read.", status=409)


@contextmanager
def delivery_context(snapshot: dict | None = None) -> Iterator[DeliveryContext]:
    """Pass a decoded hint in; carry the yielded ``snapshot`` into every cursor.

    The caller owns cursor binding/authentication. Validate the decoded shape
    here as well, before any source uses a version as a URL path component.
    Enter separately for each batch item and drop the hint when moving items.
    """
    if snapshot is not None:
        if (
            not isinstance(snapshot, dict)
            or set(snapshot) - {"source", "end", "sha256", "version"}
            or not isinstance(snapshot.get("source"), str)
            or not 1 <= len(snapshot["source"]) <= 512
            or type(snapshot.get("end")) is not int
            or snapshot["end"] < 0
            or not isinstance(snapshot.get("sha256"), str)
            or re.fullmatch(r"[a-f0-9]{64}", snapshot["sha256"]) is None
            or (
                "version" in snapshot
                and (type(snapshot["version"]) is not int or snapshot["version"] < 1)
            )
        ):
            raise errors.ValidationError(
                "Invalid document continuation; restart the read.", status=422
            )
        snapshot = dict(snapshot)
    state = DeliveryContext(snapshot)
    token = _current.set(state)
    try:
        yield state
    finally:
        _current.reset(token)


def document_hint(source: str) -> dict | None:
    context = current_delivery()
    if context is None or context.snapshot is None:
        return None
    if context.snapshot["source"] != source:
        raise source_changed("document identity changed")
    return context.snapshot


def pin_document(text: str, source: str, *, version: int | None = None) -> str:
    """Freeze the original UTF-8 text prefix, permitting only later appends.

    A source with saved versions should read the hinted version first. Its
    bytes are verified too: a pruned/corrupt version never becomes a new head.
    ``end`` is a Python/JSON character offset, not a byte or line offset.
    """
    context = current_delivery()
    if context is None:
        return text
    hint = document_hint(source)
    end = hint["end"] if hint else len(text)
    if len(text) < end:
        raise source_changed("content was deleted")
    original = text[:end]
    fingerprint = hashlib.sha256(original.encode("utf-8")).hexdigest()
    if hint:
        if hint["sha256"] != fingerprint:
            raise source_changed()
        if "version" in hint and hint["version"] != version:
            raise source_changed("saved document version is unavailable")
    else:
        context.snapshot = {"source": source, "end": end, "sha256": fingerprint}
        if type(version) is int and version > 0:
            context.snapshot["version"] = version
    return original
