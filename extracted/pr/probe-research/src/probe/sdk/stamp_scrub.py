"""The credential scrubber, minus the metric timestamps ``Run.log`` stamps.

Plan 1.4 gives every point ``Run.log`` sends a ``wall_clock``. The shared
scrubber (:func:`probe.sdk.redaction.default_scrub`) costs ~22 us per string,
and a metrics body crosses it at up to five boundaries (``Client.write``, the
journal's ``append_http`` and ``_append``, the drain, the transport), so a fresh
timestamp per point made a 5-key ``log()`` 0.35-0.9 ms slower (PR #2002 review).

A value that is EXACTLY an ISO-8601 timestamp -- digits and fixed separators,
nothing else -- cannot hold a credential. These wrappers lift such a
``wall_clock`` out of each metric point, run the unchanged shared scrubber over
everything else, and put the timestamp back where it was. Anything they do not
recognise (a non-timestamp string under ``wall_clock``, a point whose keys are
not in the SDK's order, a scrubber that changed the body's shape) takes the
plain ``default_scrub`` path, so they can only ever skip work, never skip a
check a credential could hide from.

The same holds for a read-capture row (plan (k)): ``inputs._typed_row`` already
checked its hash (64 hex), fingerprint, size (an int), ``stable`` (a bool) and
timestamp (ISO) by SHAPE, so only its path and host -- free text -- go through the
scrubber again. And for a write row (``inputs._typed_output_row``, lineage plan 3):
its hash, fingerprint, size, two timestamps and observation id (32 hex). Without this, 10k reads put ~40k distinct strings through the
scrubber at each boundary: more than its cache holds, so nearly every one was a
full scan (the (k) review measured 23,743 of them).

Kept out of ``redaction.py`` on purpose: that file is copied verbatim to the
server and to prbe-knowledge (``scripts/sync_credential_scrubber.py``).
Stdlib-only, like everything on the enqueue path.
"""

from __future__ import annotations

import re
from typing import Any

from .redaction import _SENSITIVE_KEYS, _normalize_key, default_scrub, is_sensitive_key, scrub_string

#: What ``_now()`` and pydantic's ``AwareDatetime`` serialisation produce:
#: ``2026-09-27T12:00:00.123456+00:00`` / ``...Z``. Anchored by ``fullmatch``.
_ISO_STAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})")


def _lift_stamps(points: Any) -> tuple[list, list] | None:
    """``(points without a trusted wall_clock, the stamps)``, or None when there
    is nothing to lift. A stamp is lifted only when it is the point's LAST key
    (true of every SDK-built point: the model dumps fields alphabetically), so
    putting it back reproduces the exact bytes."""
    if not isinstance(points, list):
        return None
    stripped: list = []
    stamps: list = []
    lifted = False
    for point in points:
        if isinstance(point, dict) and point:
            stamp = point.get("wall_clock")
            if (
                isinstance(stamp, str)
                and next(reversed(point)) == "wall_clock"
                and _ISO_STAMP.fullmatch(stamp)
            ):
                stripped.append({k: v for k, v in point.items() if k != "wall_clock"})
                stamps.append(stamp)
                lifted = True
                continue
        stripped.append(point)
        stamps.append(None)
    return (stripped, stamps) if lifted else None


def _restore(points: Any, stamps: list) -> bool:
    if not isinstance(points, list) or len(points) != len(stamps):
        return False
    for point, stamp in zip(points, stamps):
        if stamp is not None:
            if not isinstance(point, dict):
                return False
            point["wall_clock"] = stamp
    return True


def _scrub_segments(key: str, value: Any) -> Any:
    """One ``a/b/c`` step attribute, judged by its SEGMENTS (#2009 review).

    ``Run.log`` flattens ``{"tok": {"pad_token": "<pad>"}}`` to
    ``tok/pad_token``; judged as one joined name (``tok_pad_token``, ends in
    ``_token``) it was redacted, while the same dict unflattened was not. So
    the value is redacted when a PARENT segment is credential-shaped (a
    credential bundle, as the scrubber drops one) or the joined name is an
    exact credential name (``api/key``); otherwise it is scrubbed under its
    leaf's own name, exactly as it would be nested."""
    *parents, leaf = key.split("/")
    if any(parent and is_sensitive_key(parent) for parent in parents) or (
        _normalize_key(key) in _SENSITIVE_KEYS
    ):
        return default_scrub(value, key="private_key")  # the scrubber's own redaction
    return default_scrub(value, key=leaf)


def _scrub_step_body(body: dict) -> dict | None:
    """``default_scrub`` for a ``/steps`` body whose attributes have ``/``
    keys, with those judged per segment; None to take the plain path."""
    attributes = body.get("attributes")
    if "step_index" not in body or not isinstance(attributes, dict):
        return None
    slash = {
        key for key in attributes
        if isinstance(key, str) and "/" in key and scrub_string(key) == key
    }
    if not slash:
        return None
    rest = {key: value for key, value in attributes.items() if key not in slash}
    out = default_scrub({**body, "attributes": rest})
    scrubbed = out.get("attributes") if isinstance(out, dict) else None
    if not isinstance(scrubbed, dict) or len(scrubbed) != len(rest):
        return None
    renamed = dict(zip(rest, scrubbed))  # same order in, same order out
    merged: dict = {}
    for key, value in attributes.items():
        name = key if key in slash else renamed[key]
        if name in merged:
            return None
        merged[name] = _scrub_segments(key, value) if key in slash else scrubbed[name]
    return {**out, "attributes": merged}


#: A read row as ``inputs._typed_row`` builds it, keys in its order -- with
#: the read's ``observation_id`` last when it carries one (F7).
_READ_ROW_KEYS = ("path", "content_hash", "fingerprint", "size_bytes", "host", "stable", "first_seen_at")
_READ_ROW_KEYS_OBSERVED = (*_READ_ROW_KEYS, "observation_id")
_HEX64 = re.compile(r"[0-9a-f]{64}")
_HEX32 = re.compile(r"[0-9a-f]{32}")
_FINGERPRINT = re.compile(r"[0-9]+:-?[0-9]+:[0-9a-f]{64}")


def _checked_fields(row: Any) -> tuple | None:
    """A read row's shape-checked fields, or None if the row is not exactly
    what ``_typed_row`` builds (then it is scrubbed whole)."""
    if not isinstance(row, dict):
        return None
    keys = tuple(row)
    if keys != _READ_ROW_KEYS and keys != _READ_ROW_KEYS_OBSERVED:
        return None
    sha, fp, size = row["content_hash"], row["fingerprint"], row["size_bytes"]
    stable, seen = row["stable"], row["first_seen_at"]
    observation = row.get("observation_id")
    if not (sha is None or (isinstance(sha, str) and _HEX64.fullmatch(sha))):
        return None
    if not (fp is None or (isinstance(fp, str) and _FINGERPRINT.fullmatch(fp))):
        return None
    if not (size is None or (type(size) is int and size >= 0)):
        return None
    if type(stable) is not bool or not (isinstance(seen, str) and _ISO_STAMP.fullmatch(seen)):
        return None
    if keys == _READ_ROW_KEYS_OBSERVED and not (
        isinstance(observation, str) and _HEX32.fullmatch(observation)
    ):
        return None
    return sha, fp, size, stable, seen, observation


def _lift_reads(rows: Any) -> tuple[list, list] | None:
    """``(rows reduced to path + host, the lifted fields)``, or None."""
    if not isinstance(rows, list):
        return None
    stripped: list = []
    kept: list = []
    for row in rows:
        fields = _checked_fields(row)
        stripped.append(row if fields is None else {"path": row["path"], "host": row["host"]})
        kept.append(fields)
    return (stripped, kept) if any(k is not None for k in kept) else None


def _restore_reads(rows: Any, kept: list) -> list | None:
    """The full rows again, in ``_typed_row``'s key order, or None when the
    scrubber changed their shape."""
    if not isinstance(rows, list) or len(rows) != len(kept):
        return None
    out: list = []
    for row, fields in zip(rows, kept):
        if fields is None:
            out.append(row)
            continue
        if not isinstance(row, dict) or tuple(row) != ("path", "host"):
            return None
        sha, fp, size, stable, seen, observation = fields
        restored = {
            "path": row["path"], "content_hash": sha, "fingerprint": fp, "size_bytes": size,
            "host": row["host"], "stable": stable, "first_seen_at": seen,
        }
        if observation is not None:
            restored["observation_id"] = observation
        out.append(restored)
    return out


#: A write row as ``inputs._typed_output_row`` builds it (the ``/outputs``
#: contract), keys in its order.
_WRITE_ROW_KEYS = (
    "path", "host", "content_hash", "fingerprint", "size_bytes",
    "first_written_at", "last_modified_at", "observation_id",
)


def _checked_write_fields(row: Any) -> tuple | None:
    """A write row's shape-checked fields, or None if the row is not exactly
    what ``_typed_output_row`` builds (then it is scrubbed whole)."""
    if not isinstance(row, dict) or tuple(row) != _WRITE_ROW_KEYS:
        return None
    sha, fp, size = row["content_hash"], row["fingerprint"], row["size_bytes"]
    written, modified, observation = row["first_written_at"], row["last_modified_at"], row["observation_id"]
    if not (sha == "" or (isinstance(sha, str) and _HEX64.fullmatch(sha))):
        return None
    if not (fp is None or (isinstance(fp, str) and _FINGERPRINT.fullmatch(fp))):
        return None
    if not (size is None or (type(size) is int and size >= 0)):
        return None
    for stamp in (written, modified):
        if not (isinstance(stamp, str) and _ISO_STAMP.fullmatch(stamp)):
            return None
    if not (isinstance(observation, str) and _HEX32.fullmatch(observation)):
        return None
    return sha, fp, size, written, modified, observation


def _lift_writes(rows: Any) -> tuple[list, list] | None:
    """``(rows reduced to path + host, the lifted fields)``, or None."""
    if not isinstance(rows, list):
        return None
    stripped: list = []
    kept: list = []
    for row in rows:
        fields = _checked_write_fields(row)
        stripped.append(row if fields is None else {"path": row["path"], "host": row["host"]})
        kept.append(fields)
    return (stripped, kept) if any(k is not None for k in kept) else None


def _restore_writes(rows: Any, kept: list) -> list | None:
    if not isinstance(rows, list) or len(rows) != len(kept):
        return None
    out: list = []
    for row, fields in zip(rows, kept):
        if fields is None:
            out.append(row)
            continue
        if not isinstance(row, dict) or tuple(row) != ("path", "host"):
            return None
        sha, fp, size, written, modified, observation = fields
        out.append({
            "path": row["path"], "host": row["host"], "content_hash": sha, "fingerprint": fp,
            "size_bytes": size, "first_written_at": written, "last_modified_at": modified,
            "observation_id": observation,
        })
    return out


def _lift(body: dict) -> tuple[dict, Any] | None:
    """``(body with its trusted fields lifted out, put_back)``, or None when there
    is nothing to lift. ``put_back(scrubbed_body)`` restores them in place and
    returns False when the scrubber changed the body's shape."""
    lifted = _lift_stamps(body.get("points"))
    if lifted is not None:
        stripped, stamps = lifted
        return {**body, "points": stripped}, lambda out: _restore(out.get("points"), stamps)
    reads = _lift_reads(body.get("inputs"))
    if reads is not None:
        rows, kept = reads

        def put_back(out: dict) -> bool:
            restored = _restore_reads(out.get("inputs"), kept)
            if restored is None:
                return False
            out["inputs"] = restored
            return True

        return {**body, "inputs": rows}, put_back
    writes = _lift_writes(body.get("outputs"))
    if writes is not None:
        wrows, wkept = writes

        def put_back_writes(out: dict) -> bool:
            restored = _restore_writes(out.get("outputs"), wkept)
            if restored is None:
                return False
            out["outputs"] = restored
            return True

        return {**body, "outputs": wrows}, put_back_writes
    return None


def scrub_body(body: Any) -> Any:
    """``default_scrub(body)`` for a request body, trusting metric timestamps
    and a read row's shape-checked fields, and judging a step record's ``/``
    attribute keys per segment."""
    if isinstance(body, dict):
        step = _scrub_step_body(body)
        if step is not None:
            return step
        lifted = _lift(body)
        if lifted is not None:
            stripped, put_back = lifted
            out = default_scrub(stripped)
            if isinstance(out, dict) and put_back(out):
                return out
    return default_scrub(body)


def scrub_op(op: dict) -> Any:
    """``default_scrub(op)`` for a journal op, whose ``body`` may be a metric
    batch, a read list or a step record."""
    body = op.get("body")
    if isinstance(body, dict):
        step = _scrub_step_body(body)
        if step is not None:
            rest = default_scrub({key: value for key, value in op.items() if key != "body"})
            if isinstance(rest, dict) and "body" not in rest:
                return {**rest, "body": step}
        lifted = _lift(body)
        if lifted is not None:
            stripped, put_back = lifted
            out = default_scrub({**op, "body": stripped})
            out_body = out.get("body") if isinstance(out, dict) else None
            if isinstance(out_body, dict) and put_back(out_body):
                return out
    return default_scrub(op)


def scrub_envelope(op: dict) -> dict:
    """``default_scrub`` over a journal op's fields EXCEPT ``body``, which is
    returned untouched (plan 1.3).

    Only for an op whose body was already scrubbed: `Journal._append` is the
    one caller, and every op reaching it with a ``body`` came through
    ``append_http``, which scrubs the body (or received one `Client.write` had
    just scrubbed). Upload ops carry no ``body`` and are scrubbed whole, as
    before.
    """
    if "body" not in op:
        return default_scrub(op)
    out = default_scrub({key: value for key, value in op.items() if key != "body"})
    if not isinstance(out, dict):
        return default_scrub(op)
    return {**out, "body": op["body"]}
