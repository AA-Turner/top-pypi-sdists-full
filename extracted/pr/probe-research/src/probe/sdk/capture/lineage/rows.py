"""build read and write rows in the server's typed shape and key order."""

from __future__ import annotations
import hashlib
import re
from datetime import datetime
from probe.foundation.compat.compat import UTC
from typing import Any
#: With an observation id the server keys on the host too, and bounds it.
MAX_OBSERVATION_HOST_BYTES = 255


_HEX64 = re.compile(r"[0-9a-f]{64}")
_HEX32 = re.compile(r"[0-9a-f]{32}")
#: `hash_file`'s fingerprint: size, mtime_ns, sha256 of the edges.
_FINGERPRINT = re.compile(r"[0-9]+:-?[0-9]+:[0-9a-f]{64}")
#: What `_now_iso()` writes into a spool's "t".
_ISO_INSTANT = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,9})?(?:Z|[+-][0-9]{2}:[0-9]{2})")


def _valid_instant(seen_at: Any) -> bool:
    """Whether a spool's "t" is the ISO instant this module (or the child hook)
    wrote. Anything else is a corrupt or edited spool line."""
    return isinstance(seen_at, str) and bool(_ISO_INSTANT.fullmatch(seen_at))


def _read_observation(run_id: str, host: str, path: str, ident: tuple) -> str:
    """A read's observation id (0290, F7), in the shape write rows carry (32
    hex): DERIVED from what identifies the read -- the run, this host, the path
    and the file's identity when read -- so every report of it (the close's, a
    replay, a recovery, a late hash) carries the same one, and the server
    replaces the read's unhashed row instead of adding a second."""
    raw = "\0".join((run_id, host, path, ":".join(str(v) for v in ident)))
    return hashlib.sha256(raw.encode("utf-8", "surrogatepass")).hexdigest()[:32]


def _typed_row(
    path: str,
    sha: Any,
    fp: Any,
    size: Any,
    host: str,
    stable: bool,
    seen_at: Any,
    observation_id: str | None = None,
    *,
    rows: Any = None,
) -> dict | None:
    """One read row, sanitized BY TYPE instead of by a generic walk (plan (k)),
    or None when its timestamp is not one this module wrote.

    A read list used to reach the wire through the journal's `default_scrub`,
    which walks every key and value of every row, several times -- ~200k
    `scrub_string` calls for 10k rows. Most of a row cannot hold a credential
    by construction: a hash is 64 hex digits or it is dropped, a size is an int,
    a timestamp is the ISO instant this module wrote. Only the PATH is free
    text a person chose, and it is scrubbed exactly once, here.

    `scrub_string`, not `scrub_text`: `scrub_text` also rewrites every home path
    to `<path>` (a traceback's username), which would erase the input -- the
    server keys reads on the path and matches a fingerprint to a reference at
    the same host and path. `scrub_string` is what the journal's scrub did to
    this field before, so the stored path is unchanged.

    A malformed timestamp DROPS the row (the caller counts it in coverage as
    ``malformed_rows``): the server requires ``first_seen_at``, and stamping the
    collect time in its place would record a read at a moment it did not happen.
    """
    if not _valid_instant(seen_at):
        return None
    # scanning disabled: from . import redaction

    row = {
        # scanning disabled: "path": redaction.scrub_string(path),
        "path": path,
        "content_hash": sha if isinstance(sha, str) and _HEX64.fullmatch(sha) else None,
        "fingerprint": fp if isinstance(fp, str) and _FINGERPRINT.fullmatch(fp) else None,
        "size_bytes": size if isinstance(size, int) and not isinstance(size, bool) and size >= 0 else None,
        "host": host,
        "stable": bool(stable),
        "first_seen_at": seen_at,
    }
    if _row_count(rows) is not None:
        # C9: nullable `rows` on run_inputs; a server before it ignores it.
        row["rows"] = rows
    # With an id the server keys on the host as well, and bounds it in bytes:
    # a host past that sends the row as before, keyed on (path, hash).
    if (
        isinstance(observation_id, str)
        and _HEX32.fullmatch(observation_id)
        and len(host.encode("utf-8", "surrogatepass")) <= MAX_OBSERVATION_HOST_BYTES
    ):
        row["observation_id"] = observation_id
    return row


def _iso_from_ns(ns: Any) -> str | None:
    """An mtime in ns as the ISO instant the server stores (UTC, microseconds)."""
    if not isinstance(ns, int) or isinstance(ns, bool):
        return None
    try:
        whole, rest = divmod(ns, 1_000_000_000)
        return datetime.fromtimestamp(whole, UTC).replace(microsecond=rest // 1000).isoformat()
    except (OverflowError, OSError, ValueError):
        return None


def _typed_output_row(
    path: str,
    sha: Any,
    fp: Any,
    size: Any,
    host: str,
    written_at: Any,
    modified_at: Any,
    observation_id: Any,
    *,
    rows: Any = None,
) -> dict | None:
    """One write row in the contract's shape and key order (``POST
    /v1/runs/{id}/outputs``), sanitized by type like :func:`_typed_row`: only
    the path is free text and scrubbed here; an unhashed file's
    ``content_hash`` is ``""``. None when a time or the observation id is not
    one this module (or the child hook) wrote."""
    if not (_valid_instant(written_at) and _valid_instant(modified_at)):
        return None
    if not (isinstance(observation_id, str) and _HEX32.fullmatch(observation_id)):
        return None
    # scanning disabled: from . import redaction

    row = {
        # scanning disabled: "path": redaction.scrub_string(path),
        "path": path,
        "host": host,
        "content_hash": sha if isinstance(sha, str) and _HEX64.fullmatch(sha) else "",
        "fingerprint": fp if isinstance(fp, str) and _FINGERPRINT.fullmatch(fp) else None,
        "size_bytes": size if isinstance(size, int) and not isinstance(size, bool) and size >= 0 else None,
        "first_written_at": written_at,
        "last_modified_at": modified_at,
        "observation_id": observation_id,
    }
    if _row_count(rows) is not None:
        row["rows"] = rows  # C9: nullable `rows` on run_outputs
    return row


def _row_count(rows: Any) -> int | None:
    """A row count fit to send: a non-negative int, else None (the key is left out)."""
    return rows if isinstance(rows, int) and not isinstance(rows, bool) and rows >= 0 else None


def _without_observation(row: dict) -> dict:
    return {k: v for k, v in row.items() if k != "observation_id"}
