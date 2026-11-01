"""SpansMixin, Run's methods: spans and step records: SpanHandle, span ids, span upserts and the
flush a span citation needs."""

from __future__ import annotations

import contextvars
import os
from typing import TYPE_CHECKING, Any
from uuid import NAMESPACE_URL, UUID, uuid4, uuid5

from ....foundation.safe_warn import safe_warn as _diagnostics
from ..context import context as unit_context
from ....models import (
    SpanBatch,
    SpanCreate)
from probe.sdk.run.handle import _UNSET

if TYPE_CHECKING:  # Run only in annotations: importing it here would loop back into run.py
    from ..run import Run

#: The span currently entered via ``with run.span(...)``, or None. A contextvar
#: rather than an attribute on Run: concurrent rollouts in threads or asyncio
#: tasks each get their own view, so they never adopt each other as parents. This
#: is span NESTING, distinct from unit_context's coords/labels contextvar.
_current_span: contextvars.ContextVar["SpanHandle | None"] = contextvars.ContextVar(
    "probe_current_span", default=None
)


#: Namespace for :func:`_span_id_for`. Frozen: changing it re-points every
#: external-keyed span at a new id, which is a data migration, not a refactor.
_SPAN_NS = uuid5(NAMESPACE_URL, "https://probe.research/span")


def _span_id_for(run_id: str, span_type: str, external_key: str | None) -> str:
    """This span's id: derived from its identity when it has one, else random.

    A span is upserted ``ON CONFLICT (id)``, but the server ALSO holds a partial
    unique index on ``(run_id, span_type, external_key)`` -- so identity is stated
    twice, and a client that minted a fresh uuid per call made the two disagree.
    `probe span add --external-key k` twice was the observable form: the second
    call sent a NEW id carrying an external_key the first had already taken, and
    the write that reads as an upsert failed the uniqueness constraint instead
    (dead-lettered on the async path, where nobody was watching).

    Deriving the id from the natural key makes repeat calls address the SAME row,
    which is what "upsert one span" has always claimed. Costs no request and
    holds offline -- it has to, because the async path has no server to ask.

    An `external_key` is what a caller passes when the span has an identity in
    somebody else's system; without one there is no natural key to derive from
    and a random id is right. `span_type` is lowercased to match the server,
    which stores ``span_type.strip().lower()`` -- deriving from the raw casing
    would give ``LLM`` and ``llm`` two ids for one row.

    Spans written before this (random id + external_key) are NOT addressed by the
    derived id, so a re-push against one still conflicts. It now fails naming the
    incumbent: the backend resolves `existing_id` on this constraint too.
    """
    if not external_key:
        return str(uuid4())
    return str(uuid5(_SPAN_NS, f"{run_id}\0{span_type.strip().lower()}\0{external_key}"))


class SpanHandle(str):
    """A span id that is also a context manager.

    Subclasses ``str`` because a span's handle IS its id: existing callers do
    ``span_id = run.span(...)`` and pass that string onward, so scope behaviour
    has to arrive without changing what :meth:`Run.span` returns.

        with run.span("rollout", name="rollout-0") as span:
            span.attributes["reward"] = reward

    Leaving the block upserts the same span id with ``ended_at``, a terminal
    status, and whatever accumulated in ``attributes``. An exception sets status
    ``failed`` and records its type and message.

    That last part is the reason this exists. A span opened with the two-call
    form and abandoned by a raise stays ``running`` forever: runs have a
    heartbeat and a server-side reaper, spans have neither, so nothing ever
    corrects it. The block closes the span on both paths.
    """

    def __new__(
        cls,
        span_id: str,
        *,
        run: "Run",
        span_type: str,
        fields: dict[str, Any],
        attributes: dict[str, Any],
        failure_values: dict[str, Any] | None = None,
    ) -> "SpanHandle":
        # str is variable-length, so no __slots__ here — these live in __dict__.
        self = super().__new__(cls, span_id)
        self._run = run
        self._span_type = span_type
        self._fields = fields
        self.attributes = attributes
        self._failure_values = dict(
            failure_values if failure_values is not None else fields.get("coords") or {}
        )
        self._token: contextvars.Token | None = None
        return self

    # A span id used to be a plain ``str``, and plain strings survive being
    # copied, pickled, and shipped across a process boundary — which distributed
    # training does routinely (Ray, multiprocessing, a checkpoint state dict).
    # Reconstructing goes through ``__new__``, which needs a live Run and a
    # thread lock, so without these a copy raises. Degrade to the plain id: the
    # scope behaviour is meaningless in another process anyway.
    def __reduce__(self):
        return (str, (str(self),))

    def __copy__(self) -> str:
        return str(self)

    def __deepcopy__(self, memo: dict) -> str:
        return str(self)

    def __enter__(self) -> "SpanHandle":
        # No write here: `span()` already upserted the row as `running`, so the
        # span is visible for the whole time the body runs rather than appearing
        # only once it closes.
        self._token = _current_span.set(self)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            if exc is not None:
                from ..context.failure import identifiers, remember

                remember(
                    exc,
                    self._run.id,
                    {
                        **self._failure_values,
                        **identifiers(self.attributes),
                        "phase": self._fields.get("name") or self._span_type,
                        "step": self._fields.get("step_index"),
                    },
                )
        except BaseException:  # noqa: BLE001 -- capture cannot replace the body error
            pass
        if self._token is not None:
            _current_span.reset(self._token)
            self._token = None
        if exc_type is not None:
            # setdefault: an explicit attribute the body already set about the
            # failure is better information than the exception repr.
            self.attributes.setdefault("error.type", exc_type.__name__)
            # str() on the caller's LIVE exception, during unwinding. Framework
            # exceptions in ML code format lazily -- a released CUDA context, a
            # closed file, a tensor repr -- so this can raise and destroy the
            # very exception it is trying to record.
            message = _diagnostics.describe(exc) if exc is not None else ""
            try:
                message = str(exc) if exc is not None else ""
            except BaseException:  # noqa: BLE001 -- keep the describe() fallback
                pass
            if message:
                self.attributes.setdefault("error.message", message)
        # `_fields` carries the RESOLVED parent, start time and coords, so this
        # upsert re-sends them verbatim instead of re-deriving them from a
        # contextvar that has already been reset (which would re-parent to the
        # grandparent). Re-sending an identical coords map is accepted — the
        # server's set-once rule 409s only on a DIFFERENT one.
        #
        # `attributes` is re-sent, not the copy span() sanitised — the body has
        # been assigning into it, so anything it added is unvetted. span() runs
        # it through _json_safe again on the way.
        # BaseException, and swallowed when the body already failed. This close
        # runs DURING unwinding, so anything it raises displaces the body's
        # exception -- the failure mode that killed a live campaign's workers,
        # and `with run.span(...)` is the SDK's advertised rollout API, so this
        # is its most-travelled unguarded path. `_run.span` can raise from at
        # least four places: attribute sanitising, coordinate merging, a strict
        # write, and the journal's own OSError. A stale span row is strictly
        # better than a lost traceback.
        #
        # With no body exception the raise still propagates: there is nothing to
        # protect, and a caller closing a span deserves to hear it failed.
        try:
            self._run.span(
                self._span_type,
                id=str(self),
                status="failed" if exc_type is not None else "completed",
                ended_at=_now(),
                attributes=self.attributes,
                **self._fields,
            )
        except BaseException as close_error:  # noqa: BLE001
            if exc_type is None:
                raise
            _diagnostics.warn(
                f"span {self!s} did not close cleanly "
                f"({_diagnostics.describe(close_error)}); re-raising the "
                "original error from the with-block instead."
            )
        # Returns None, so the exception keeps propagating. The span records that
        # it failed; it does not swallow the failure.


class SpansMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    # -- trajectory (spans) -------------------------------------------------
    def span(
        self,
        span_type: str,
        *,
        id: str | None = None,
        parent_span_id: str | None = _UNSET,
        name: str | None = None,
        step_index: int | None = None,
        external_key: str | None = None,
        provider: str | None = None,
        status: str = "running",
        started_at: str | None = _UNSET,
        ended_at: str | None = None,
        attributes: dict | None = None,
        summary: dict | None = None,
        coords: dict[str, Any] | None = None,
        strict: bool | None = None,
        blocking: bool = True,
    ) -> "SpanHandle":
        """Upsert one span (client-generated UUID). Returns the span id.

        ``coords`` is the span's below-run coordinate — the same bounded map
        metric points carry in ``dimensions`` — merged over the ambient
        :meth:`unit` context (call site wins per key). Sent as the dedicated
        ``coords`` field, never folded into ``attributes``: the server
        canonicalizes + hashes it (and mirrors it for display) itself. A span's
        coordinate is set-once server-side — a re-push may add one, an empty map
        keeps the existing coordinate, and a different one is a 409."""
        self._progress.bump()  # 2.8: a span (a step, a rollout, a trial) is work done
        span_id = id or _span_id_for(self.id, span_type, external_key)
        UUID(span_id)  # validate shape early
        if parent_span_id is _UNSET:
            enclosing = _current_span.get()
            # Only adopt a parent from the SAME run. `with runA.span(...):` around
            # a `runB.span(...)` would otherwise write runB a parent_span_id that
            # does not exist in runB — spans are per-run, and a dangling FK is a
            # worse record than no parent.
            parent_span_id = (
                str(enclosing) if enclosing is not None and enclosing._run.id == self.id else None
            )
        if started_at is _UNSET:
            # Only when CREATING. An explicit `id=` means this is an upsert of an
            # existing span — the documented two-call close does exactly that —
            # and stamping now() there would rewrite the start time to the close
            # time and collapse the span's duration to zero.
            started_at = _now() if id is None else None
        # Through _json_safe for the same reason log() is: `attributes` is JSONB,
        # so an unserialisable value blows up in model_dump() BEFORE the strict/
        # spool boundary — inside the training loop. Worse in the `with` form,
        # where the raise happens during unwinding and displaces the body's own
        # exception as the visible failure.
        attrs = {key: _json_safe(key, value) for key, value in (attributes or {}).items()}
        resolved_coords = unit_context.merged_coords(coords)
        span = SpanCreate(
            id=span_id,
            span_type=span_type,
            parent_span_id=parent_span_id,
            name=name,
            step_index=step_index,
            external_key=external_key,
            provider=provider,
            status=status,
            started_at=started_at,
            ended_at=ended_at,
            attributes=attrs,
            # `summary_metrics` IS THE GENERATED FIELD'S NAME, and passing the
            # old `summary=` here stopped landing the moment the models were
            # regenerated after the rename: the kwarg went nowhere, the field
            # stayed None, and -- because this body serializes WITHOUT
            # exclude_none -- every span shipped `summary_metrics: null` into a
            # server field that is a plain `dict`. 56 spans rejected, and the
            # run then refused to close on its own outbox.
            summary_metrics=summary or {},
            # Always a dict, never None: the span body serializes without
            # exclude_none, and the server's coords field is non-nullable with
            # {} meaning "no coordinate stated" (keeps any existing one).
            coords=resolved_coords,
        )
        body = SpanBatch(spans=[span]).model_dump(mode="json")
        # BOTH NAMES ON THE WIRE, for the reason `_summary_wire` gives for a
        # run: the generated model can only carry one, and a server older than
        # the rename reads only `summary`.
        for wire_span in body["spans"]:
            wire_span.update(_summary_wire(wire_span.get("summary_metrics") or {}))
        self._client.write(
            "POST",
            f"/v1/runs/{self.id}/spans",
            self._stamp_writer(body),
            strict=strict,
            blocking=blocking,
        )
        return SpanHandle(
            span_id,
            run=self,
            span_type=span_type,
            fields={
                "parent_span_id": parent_span_id,
                "name": name,
                "step_index": step_index,
                "external_key": external_key,
                "provider": provider,
                "started_at": started_at,
                # A Python kwarg replayed into `Run.span()`, NOT a wire body --
                # the wire names belong only where a body is posted.
                "summary": summary,
                # The RESOLVED coordinate, so the close re-sends the same map the
                # open did. Identical coords are accepted; the server's set-once
                # rule 409s only on a different one.
                "coords": resolved_coords,
                "strict": strict,
            },
            attributes=attrs,
            failure_values=unit_context.failure_values(self.id, coords),
        )

    def step(self, step_index: int, *, name: str | None = None, strict: bool | None = None, **kw):
        """Upsert the step record. The per-step home for anything that is not a
        number, which is what :meth:`log` routes non-numeric values into.

        ``strict`` is forwarded so this obeys fail-open like every other write —
        it used to swallow the argument and always take the client default.

        Below a resumed run's resume point it is dropped like :meth:`log`
        (plan 2.4): `/steps` is last-write-wins, so a re-logged record would
        silently replace the first execution's."""
        if (
            self._resume_from_step is not None
            and step_index is not None
            and step_index <= self._resume_from_step
        ):
            return self._drop_below_resume(step_index, strict=strict)
        if os.getpid() != self._opened_pid:
            self._note_forked_writer()
        self._progress.bump()  # 2.8: a step record is progress too
        body = {"step_index": step_index, "name": name, **kw}
        # Plan (f): the server replaces the record whole, so remember what was
        # sent; a later log() at this step keeps this name and these keys.
        self._remember_step_record(step_index, name, kw.get("attributes"))
        return self._client.write(
            "POST", f"/v1/runs/{self.id}/steps", self._stamp_writer(body), strict=strict
        )

    def _flush_for_span(self, span_id: str | None) -> None:
        """Deliver THIS RUN's queued ops before a direct post citing ``span_id``.

        Scoped with ``run_ref``, not ``client.flush()``. flush() is a
        machine-wide drain -- every run's ops, unbounded, behind the exclusive
        drain flock -- and this sits on a hot path: harbor calls
        ``log_artifact(path=..., span_id=...)`` once per file per trial, so a
        neighbour's queued backlog would be dragged through an artifact upload.
        That is the hazard `probe run end` already refuses for the same reason
        ("finish() would foreground-drain the whole machine-wide journal").

        Gated on a queued SPAN specifically: a pending metric point says nothing
        about whether the span this artifact cites has landed, and draining on
        its account would make every artifact upload wait for telemetry it does
        not depend on.

        Best-effort. If the drain fails the upload still proceeds and its own
        fail-open path records a reference, which beats refusing to log an
        artifact because telemetry is unreachable.
        """
        if not span_id or not self._client.async_writes:
            return
        if not any(
            op.get("path", "").endswith("/spans")
            for op in self._queued_ops(self._client.journal.pending())
        ):
            return
        from ...delivery.outbox.drain.drain import drain

        try:
            drain(
                self._client.journal,
                run_ref=self.id,
                client_factory=self._client._outbox_client_factory(),
            )
        except Exception:  # noqa: BLE001 -- drain records last_error itself
            pass
from probe.sdk.run.metrics.values import _json_safe, _now  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.run.summary import _summary_wire  # noqa: E402 -- pieces need each other; the front door loads this one first
