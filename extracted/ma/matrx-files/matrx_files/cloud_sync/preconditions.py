"""Write preconditions — the difference between two devices and one survivor.

SPEC-SERVER §3. Before this, NEITHER write path had a precondition of any kind:
two devices editing one file both won, in arrival order, and the loser's bytes
were simply gone with nothing anywhere to say a conflict had happened.

Three preconditions, one refusal code:

    POST /files/upload            expected_checksum   (form field)
    POST /files/upload/tus        expectedchecksum    (Upload-Metadata), evaluated
                                                      at creation AND re-evaluated
                                                      at finalize
    PATCH /files/{id}             If-Match            "<sha256hex>" | W/"v<version>"

The value is the SHA-256 the client believes the server currently holds at that
path, or the literal ``"absent"`` meaning "I believe no alive row exists here".
Omitted means today's last-write-wins, unchanged, so no existing client breaks
(S8: optional on the wire, mandatory in the engine).

A failure is **412, always, on all three routes** -- never 409 (TUS already owns
409 for upload-session state) and never 200-with-errors. The body is the engine's
conflict input: it carries everything needed to decide "fetch and merge", "make a
conflict copy", or "this was my own earlier write" (``origin_device_id``).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any

#: The value meaning "I believe no alive row exists at this path".
ABSENT = "absent"

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_WEAK_VERSION_RE = re.compile(r'^W/"v(\d+)"$')
_STRONG_RE = re.compile(r'^"([0-9a-f]{64})"$')


class PreconditionError(ValueError):
    """Base for a refused precondition. The REST layer maps this to 400."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class PreconditionFailed(Exception):
    """The client's belief about the server's state was wrong. HTTP 412.

    ``payload`` is the exact §3.2 body; it is the ENGINE'S CONFLICT INPUT, not a
    log line, so every field is populated from the row that actually exists.
    """

    def __init__(self, payload: dict[str, Any]) -> None:
        super().__init__(payload.get("message", "precondition failed"))
        self.payload = payload


@dataclass(frozen=True)
class IfMatch:
    """A parsed ``If-Match``: exactly one of the two forms."""

    checksum: str | None = None
    version: int | None = None

    @property
    def is_weak(self) -> bool:
        return self.version is not None


def _iso(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def conflict_payload(row: dict[str, Any] | None, expected: str | None) -> dict[str, Any]:
    """Build the exact §3.2 412 body from the row that actually exists."""
    row = row or {}
    return {
        "error": "precondition_failed",
        "message": "the file changed on the server since you last read it",
        "file_id": str(row["id"]) if row.get("id") else None,
        "current_checksum": row.get("checksum"),
        # files.files.current_version -- the feed's `version` field. NOT the
        # platform row `version` column; they are different columns and are
        # never conflated.
        "current_version": row.get("current_version"),
        "current_size_bytes": row.get("size_bytes"),
        "current_updated_at": _iso(row.get("updated_at")),
        "origin_device_id": (
            str(row["origin_device_id"]) if row.get("origin_device_id") else None
        ),
        "expected_checksum": expected,
    }


def normalize_expected_checksum(raw: str | None) -> str | None:
    """Validate the wire value: 64 lowercase hex, or the literal ``absent``."""
    if raw is None:
        return None
    value = raw.strip()
    if not value:
        return None
    if value.lower() == ABSENT:
        return ABSENT
    lowered = value.lower()
    if not _SHA256_RE.match(lowered):
        raise PreconditionError(
            "invalid_expected_checksum",
            f"expected_checksum must be 64 lowercase hex characters or the literal "
            f"{ABSENT!r}; got {raw!r}.",
        )
    return lowered


def parse_if_match(raw: str | None) -> IfMatch | None:
    """Parse ``If-Match: "<sha256hex>"`` or ``If-Match: W/"v<n>"``.

    The weak form exists for metadata-only mutations, where the bytes are
    untouched and a checksum would say nothing about what the client read.
    """
    if raw is None or not raw.strip():
        return None
    value = raw.strip()
    weak = _WEAK_VERSION_RE.match(value)
    if weak:
        return IfMatch(version=int(weak.group(1)))
    strong = _STRONG_RE.match(value.lower())
    if strong:
        return IfMatch(checksum=strong.group(1))
    if value.lower() == f'"{ABSENT}"' or value.lower() == ABSENT:
        return IfMatch(checksum=ABSENT)
    raise PreconditionError(
        "invalid_if_match",
        f'If-Match must be "<64 hex sha256>" or W/"v<version>"; got {raw!r}. '
        "A wildcard or an opaque ETag is not accepted: the point of the header is "
        "to name the exact state the client read.",
    )


def check_expected_checksum(row: dict[str, Any] | None, expected: str | None) -> None:
    """Raise :class:`PreconditionFailed` unless the server's state matches.

    ``expected is None`` is today's last-write-wins behavior, untouched.
    """
    if expected is None:
        return
    alive = row if row and not row.get("deleted_at") else None
    if expected == ABSENT:
        if alive is None:
            return
        raise PreconditionFailed(conflict_payload(alive, expected))
    if alive is None:
        # The client believed a specific version was there; nothing is.
        raise PreconditionFailed(conflict_payload(row, expected))
    current = (alive.get("checksum") or "").lower()
    if current != expected:
        raise PreconditionFailed(conflict_payload(alive, expected))


def check_if_match(row: dict[str, Any] | None, condition: IfMatch | None) -> None:
    """Raise :class:`PreconditionFailed` unless the row is in the named state."""
    if condition is None:
        return
    alive = row if row and not row.get("deleted_at") else None
    if condition.is_weak:
        if alive is None or int(alive.get("current_version") or 0) != condition.version:
            raise PreconditionFailed(
                conflict_payload(alive or row, f'W/"v{condition.version}"')
            )
        return
    check_expected_checksum(row, condition.checksum)
