"""Ambient below-run coordinate context: the ``run.unit(...)`` surface.

The coordinate layer (server PR prbe-ai/research-os#177) splits sub-run
identity into two flat maps:

- ``coords`` — bounded, low-cardinality grouping axes (``rank``, ``split``,
  ``phase``…). SERIES identity: the server canonicalizes + hashes them so
  metric points, spans, and artifacts stamped at one coordinate always join.
  Never a per-sample id, and never the step axis (that is ``step_index``).
- ``labels`` — unbounded per-sample drill-down ids (``sample``, ``uid``…).
  POINT identity only; they can never mint a metric series.

A key may not appear in both maps — the server 422s that, and this module
raises the same complaint client-side, where the stack trace still points at
the offending call site.

:class:`FailureContext` (``probe.context(...)``) is the failure-only sibling:
it names the batch/sample for a crash report and stamps nothing onto payloads.

``UnitContext`` rides a :class:`contextvars.ContextVar`, so a unit entered in
one thread or asyncio task never leaks into another, and exit restores the
previous state by token (safe under overlapping generators/awaits). Nested
units MERGE: child ∪ parent, child winning per key within the same map.

The ambient maps are folded into each producer's payload at CALL time —
before the fail-open spool ever sees the body — so a spooled write replayed
minutes later still carries the coordinate that was ambient when the value
was produced, not whatever is ambient at flush time.
"""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar, Token
from typing import Any, Mapping

from .failure_context import identifiers, remember

#: (coords, labels) of the innermost active unit. The default is a shared
#: empty pair; every mutation path builds fresh dicts, so it is never written.
_STATE: ContextVar[tuple[dict[str, Any], dict[str, Any]]] = ContextVar(
    "probe_unit_context", default=({}, {})
)


# Diagnostic context has explicit ownership. The legacy coordinate API is
# ambient; its maps cannot establish which run owns an inherited sample.
_FAILURE_STATE: ContextVar[tuple[str | None, dict[str, Any]]] = ContextVar(
    "probe_failure_unit", default=(None, {})
)


def failure_values(run_id: str | None, explicit: dict[str, Any] | None = None) -> dict[str, Any]:
    owner, values = _FAILURE_STATE.get()
    return {**(values if run_id and owner == run_id else {}), **identifiers(explicit or {})}


def _flat(mapping: Mapping[str, Any] | None, what: str) -> dict[str, Any]:
    """A defensive copy of ``mapping``, shape-checked as a flat scalar map.

    Mirrors the cheap half of the server's ``validate_flat_map`` (string keys,
    no nested containers) so the common mistakes fail here with a useful
    traceback; budgets (key counts, value lengths) stay server-enforced.
    """
    if mapping is None:
        return {}
    if not isinstance(mapping, Mapping):
        raise TypeError(f"{what} must be a flat mapping, got {type(mapping).__name__}")
    for key, value in mapping.items():
        if not isinstance(key, str) or not key:
            raise ValueError(f"{what} keys must be non-empty strings, got {key!r}")
        if isinstance(value, (Mapping, list, tuple, set)):
            raise ValueError(
                f"{what}[{key!r}] must be a scalar (flat map), got {type(value).__name__}"
            )
    return dict(mapping)


def _check_disjoint(coords: dict[str, Any], labels: dict[str, Any]) -> None:
    overlap = sorted(coords.keys() & labels.keys())
    if overlap:
        raise ValueError(
            f"key(s) {overlap} appear in both coords and labels after merging; "
            "a key is either a grouping axis (coords) or a per-sample id (labels), "
            "never both (the server rejects this with a 422)"
        )


def current() -> tuple[dict[str, Any], dict[str, Any]]:
    """The ambient ``(coords, labels)`` pair — copies, safe for the caller to own."""
    coords, labels = _STATE.get()
    return dict(coords), dict(labels)


def merged(
    coords: Mapping[str, Any] | None = None,
    labels: Mapping[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Ambient maps with explicit call-site maps merged over them.

    The call site wins per key. Raises ``ValueError`` when a key lands in both
    maps after merging — the client-side mirror of the server's 422.
    """
    ambient_coords, ambient_labels = _STATE.get()
    out_coords = {**ambient_coords, **_flat(coords, "coords")}
    out_labels = {**ambient_labels, **_flat(labels, "labels")}
    _check_disjoint(out_coords, out_labels)
    return out_coords, out_labels


@contextmanager
def detached():
    """No ambient unit inside the block: for a write that belongs to the RUN,
    not to whichever unit happened to be open when it fired (the resume guard's
    counter span -- the server sets a span's coordinate once, so inheriting one
    unit's would refuse every later write from another)."""
    token = _STATE.set(({}, {}))
    try:
        yield
    finally:
        _STATE.reset(token)


def merged_coords(coords: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Ambient coords with explicit coords merged over them (call site wins).

    For producers that carry only a coordinate (spans): ambient *labels* are
    deliberately not consulted, so a span write can never trip the
    coords/labels overlap check on a map it does not send.
    """
    ambient_coords, _ = _STATE.get()
    return {**ambient_coords, **_flat(coords, "coords")}


class UnitContext:
    """``with run.unit(coords=..., labels=...):`` — see :meth:`Run.unit`.

    Re-entrant per instance is NOT supported (one token per instance); create a
    fresh unit per ``with`` block, which is what the surface reads as anyway.
    """

    def __init__(
        self,
        *,
        coords: Mapping[str, Any] | None = None,
        labels: Mapping[str, Any] | None = None,
        run_id: str | None = None,
    ) -> None:
        # Validate shape eagerly, at the declaration site.
        self._coords = _flat(coords, "coords")
        self._labels = _flat(labels, "labels")
        self._token: Token | None = None
        self._run_id = run_id
        self._failure_token: Token | None = None

    def __enter__(self) -> "UnitContext":
        parent_coords, parent_labels = _STATE.get()
        coords = {**parent_coords, **self._coords}
        labels = {**parent_labels, **self._labels}
        _check_disjoint(coords, labels)
        self._token = _STATE.set((coords, labels))
        self._failure_token = _FAILURE_STATE.set((self._run_id, {
            **failure_values(self._run_id), **identifiers({**self._coords, **self._labels}),
        }))
        return self

    def __exit__(self, *exc: object) -> None:
        try:
            if len(exc) > 1 and isinstance(exc[1], BaseException):
                from .failure_context import remember

                remember(exc[1], self._run_id, failure_values(self._run_id))
        except BaseException:  # noqa: BLE001 -- keep the original failure
            pass
        finally:
            if self._failure_token is not None:
                _FAILURE_STATE.reset(self._failure_token)
                self._failure_token = None
        if self._token is not None:
            _STATE.reset(self._token)
            self._token = None


class FailureContext:
    """``with probe.context(batch_id=..., epoch=...):`` — see :meth:`Run.context`.

    The failure-only half of :class:`UnitContext`: it sets the diagnostic state
    a crash report reads (``_FAILURE_STATE``) and NEVER the coords/labels
    ``_STATE`` that producers fold into payloads, so everything logged inside
    the block is sent exactly as it would be outside it. That is the whole
    reason it exists: a per-batch unit label stops a curve plotting and a
    per-batch coord shreds it into one-point series.

    Entered once per batch, so it does no I/O and never raises into the caller:
    values :func:`~probe.sdk.failure_context.identifiers` cannot use are
    dropped, and with no owning run it is a no-op. One token per instance, like
    :class:`UnitContext`: create a fresh one per ``with`` block.
    """

    __slots__ = ("_run_id", "_values", "_token")

    def __init__(self, run_id: str | None, ids: dict[str, Any] | None = None) -> None:
        self._run_id = run_id if isinstance(run_id, str) and run_id else None
        # identifiers() swallows everything, so a hostile value costs the
        # context, never the caller.
        self._values = identifiers(ids) if isinstance(ids, dict) else {}
        self._token: Token | None = None

    def __enter__(self) -> "FailureContext":
        if self._run_id is not None:
            try:
                self._token = _FAILURE_STATE.set(
                    (self._run_id, {**failure_values(self._run_id), **self._values})
                )
            except Exception:  # noqa: BLE001 -- optional context cannot break the loop
                self._token = None
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        try:
            if isinstance(exc, BaseException) and self._run_id is not None:
                remember(exc, self._run_id, failure_values(self._run_id))
        except BaseException:  # noqa: BLE001 -- keep the original failure
            pass
        finally:
            token, self._token = self._token, None
            if token is not None:
                try:
                    _FAILURE_STATE.reset(token)
                except (ValueError, RuntimeError):
                    # Exited in another Context -- a generator that yielded
                    # inside the block and was resumed or closed elsewhere. The
                    # reset cannot happen here, so the value can outlive the
                    # block in the context that entered it: never `yield` inside
                    # `probe.context` (the skill says so).
                    pass
