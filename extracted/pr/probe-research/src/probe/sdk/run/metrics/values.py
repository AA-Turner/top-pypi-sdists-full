"""turn logged values into metric points: strictly increasing stamps, JSON-safe values, nested-dict flattening within a key budget."""

from __future__ import annotations
import functools
import json
from collections.abc import Mapping
import threading
from datetime import datetime, timedelta, timezone
from typing import Any

from ....foundation.safe_warn import safe_warn as _diagnostics
from ...values import values as _coerce
# scanning disabled: from .redaction import default_scrub, is_sensitive_key
from ...redaction import is_sensitive_key


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


#: The last stamp `_log_stamp` handed out in this process, and its lock.
_last_log_stamp: datetime | None = None
_log_stamp_lock = threading.Lock()


def _log_stamp() -> str:
    """``_now()`` for ``Run.log``'s points, strictly increasing per process.

    An unstepped point's server identity includes its ``wall_clock`` (the
    wall-clock unique index on ``metric_points``, ``ON CONFLICT DO NOTHING``),
    so two ``log(step=None)`` calls that read the same clock value -- a frozen
    clock under freezegun, a clock stepped backwards -- would collapse into
    the first one, silently. A stamp not later than the last one becomes the
    last one plus 1 us (PR #2002 review)."""
    global _last_log_stamp
    stamp = datetime.fromisoformat(_now())
    with _log_stamp_lock:
        last = _last_log_stamp
        if last is not None and stamp <= last:
            stamp = last + timedelta(microseconds=1)
        _last_log_stamp = stamp
    return stamp.isoformat()


def _as_metric_value(value: Any) -> float | None:
    """``value`` as a metric point, or None if it belongs in the step record.

    ``metric_points.value`` is ``DOUBLE PRECISION NOT NULL`` (db/experiment/
    schema.sql), so this is a hard contract boundary, not a preference.

    Strings are excluded deliberately even though ``float("0.4")`` parses: a
    caller who logged ``"0.4"`` meant the string, and quietly retyping it would
    make it indistinguishable from the number afterwards. Bools DO become 1/0 —
    they are plottable, and a chart is what people log them for. Anything with a
    ``__float__`` coerces for free.

    numpy values and torch tensors (plan (c)) go through ``.item()`` when they
    hold ONE element -- a scalar, a size-1 array, a 1-element tensor with or
    without grad -- which never warns the way ``float(np.array([x]))`` does.
    With several elements they are not a metric: they go to the step record,
    where ``float()`` used to raise a RuntimeError into the loop for a tensor."""
    kind = type(value)
    if kind is float:
        return value
    if kind is int:
        return float(value)
    if isinstance(value, (str, bytes, bytearray)):
        return None
    if isinstance(value, bool):
        return float(value)
    unwrapped = _coerce.array_scalar(value)
    if unwrapped is not _coerce.NOT_AN_ARRAY:
        return unwrapped
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _json_safe(key: str, value: Any) -> Any:
    """``value`` if it survives a JSON round trip, else its repr.

    ``spans.attributes`` is JSONB, so an unserialisable object would fail at
    encode time — INSIDE the training loop, past the fail-open boundary. Keeping
    the repr loses fidelity but never the loop, and says so."""
    try:
        json.dumps(value)
        return value
    except (TypeError, ValueError):
        # `_diagnostics.warn`: a plain warning RAISES under `-W error`, inside
        # the training loop -- the one place this function exists to protect.
        _diagnostics.warn(
            f"metric {key!r} is not JSON-serialisable ({type(value).__name__}); "
            "recording repr() instead.",
            stacklevel=3,
        )
        return repr(value)


#: Plan (d): the most segments a key flattened by ``Run.log`` can have. A mapping
#: nested deeper stays whole under its 16-segment key (one step attribute). A
#: guard against pathological input, not a depth real metrics reach.
_FLATTEN_MAX_DEPTH = 16

#: How many distinct keys nested dicts may mint over one run (#2009 review). A
#: dict keyed by DATA -- ``{"per_example_loss": {example_id: v}}`` -- mints a
#: series per id; past the server's per-run series cap it refuses the whole
#: batch, ``loss`` included. Past this budget the offending mapping stays one
#: step attribute instead.
_NESTED_KEY_BUDGET = 1_000

#: The longest key flattening may build. A mapping whose children would pass it
#: stays whole.
_NESTED_KEY_MAX_CHARS = 256

#: ``is_sensitive_key`` for the keys a loop logs every step: cached, since the
#: same few names repeat for the whole run.
_sensitive_key_name = functools.lru_cache(maxsize=4096)(is_sensitive_key)


def _is_omegaconf(value: Any) -> bool:
    module = getattr(type(value), "__module__", "") or ""
    return module == "omegaconf" or module.startswith("omegaconf.")


class _BudgetSpent(Exception):
    """A top-level key's nested dicts would take the run past `_NESTED_KEY_BUDGET`."""


def _key_name(key: Any) -> str:
    """A key's text for the credential check: a ``str`` as itself, ``bytes``
    decoded (``{b"token": {...}}`` is a credential bundle too), else ``str()``."""
    if isinstance(key, str):
        return key
    if isinstance(key, (bytes, bytearray)):
        return bytes(key).decode("utf-8", "replace")
    return str(key)


def _flatten(
    metrics: Mapping[Any, Any], *, sep: str = "/", known: set[str] | None = None
) -> tuple[dict[Any, Any], list[tuple[Any, str]], list[tuple[str, str, str]]]:
    """``{"a": {"b": 1}}`` -> ``{"a/b": 1}``. Returns ``(flat, collided, kept_whole)``; only Mapping
    values expand, and it never raises (it runs inside the training loop). Sensitive-key scrubbing is
    off while scanning is disabled. Collisions, depth and the key budget: DESIGN.md."""
    from ...values import omegaconf_read

    known = set() if known is None else known
    reader: omegaconf_read.Reader | None = None
    flat: dict[Any, Any] = {}
    depth_of: dict[Any, int] = {}
    collided: list[tuple[Any, str]] = []
    kept_whole: list[tuple[str, str, str]] = []

    def children_of(mapping: Any) -> list:
        nonlocal reader
        if omegaconf_read.is_omegaconf(mapping):
            reader = omegaconf_read.Reader() if reader is None else reader
            return reader.items(mapping)
        return list(mapping.items())

    def put(key: Any, value: Any, depth: int, top: str) -> None:
        seen = depth_of.get(key)
        if seen is None:
            flat[key] = value
            depth_of[key] = depth
            return
        if all(key != k for k, _ in collided):
            collided.append((key, top))
        if depth < seen:
            flat[key] = value
            depth_of[key] = depth

    def stage(prefix: str, items: list, depth: int, path: set[int], staged: list, fresh: set) -> str | None:
        """Stage one mapping's children as ``(key, value, depth, reason)``;
        a reason instead when this mapping must stay whole (decided before
        any child is staged); `_BudgetSpent` when the run's budget runs out."""
        children = [(f"{prefix}{sep}{name}", name, value) for name, value in
                    ((str(raw_key), value) for raw_key, value in items)]
        if any(len(key) > _NESTED_KEY_MAX_CHARS for key, _, _ in children):
            return "length"
        new = {
            key
            for key, _, value in children
            if not isinstance(value, Mapping) and key not in known and key not in fresh
        }
        if len(known) + len(fresh) + len(new) > _NESTED_KEY_BUDGET:
            raise _BudgetSpent
        fresh.update(new)
        for key, name, value in children:
            # scanning disabled: sensitive = _sensitive_key_name(name)
            sensitive = False
            if not isinstance(value, Mapping) or sensitive:
                # With scanning on, a sensitive leaf is redacted by its own name and a mapping under a
                # sensitive name is scrubbed whole; scanning is disabled, so `sensitive` is False.
                # scanning disabled: staged.append((key, default_scrub(value, key=name) if sensitive else value, depth, None))
                staged.append((key, value, depth, None))
                continue
            try:
                grandchildren = children_of(value)
            except Exception:  # noqa: BLE001 -- see docstring: never into the loop
                staged.append((key, value, depth, "unreadable"))
                continue
            if not grandchildren:
                continue
            # A key at `depth` has depth+1 segments; its children would have depth+2.
            if depth + 2 > _FLATTEN_MAX_DEPTH:
                staged.append((key, value, depth, "depth"))
                continue
            if id(value) in path:
                staged.append((key, value, depth, "cycle"))
                continue
            path.add(id(value))
            try:
                refused = stage(key, grandchildren, depth + 1, path, staged, fresh)
            finally:
                path.discard(id(value))
            if refused is not None:
                staged.append((key, value, depth, refused))
        return None

    try:
        top_items = children_of(metrics)
    except Exception:  # noqa: BLE001 -- an unlistable top level: nothing to flatten
        return dict(metrics) if isinstance(metrics, dict) else {}, [], []
    for raw_key, value in top_items:
        name = _key_name(raw_key)
        # scanning disabled: if not isinstance(value, Mapping) or _sensitive_key_name(name):
        if not isinstance(value, Mapping):
            # Top level: left as it is, under its own key, for the body scrub
            # -- exactly what an unflattened call sends.
            put(raw_key, value, 0, name)
            continue
        try:
            grandchildren = children_of(value)
        except Exception:  # noqa: BLE001
            kept_whole.append((name, "unreadable", name))
            put(raw_key, value, 0, name)
            continue
        if not grandchildren:
            continue
        if value is metrics:
            kept_whole.append((name, "cycle", name))
            put(raw_key, value, 0, name)
            continue
        staged: list = []
        fresh: set = set()
        try:
            refused = stage(name, grandchildren, 1, {id(metrics), id(value)}, staged, fresh)
        except _BudgetSpent:
            refused = "budget"
        if refused is not None:
            kept_whole.append((name, refused, name))
            put(raw_key, value, 0, name)
            continue
        known.update(fresh)
        for key, staged_value, depth, reason in staged:
            if reason is not None:
                kept_whole.append((key, reason, name))
            put(key, staged_value, depth, name)
    return flat, collided, kept_whole
