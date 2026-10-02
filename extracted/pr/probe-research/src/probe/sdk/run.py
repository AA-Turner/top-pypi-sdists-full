"""The SDK Run handle: the agent's per-run write surface.

Wraps a run row and exposes the write verbs from the SDK/CLI sketch, each mapped
to a v3 endpoint:

  log()/log_hw() -> POST /v1/runs/{id}/metrics       (first-class dimensions, fold #9)
  span()/step()  -> POST /v1/runs/{id}/spans | /steps      (trajectory)
  log_artifact() -> POST /v1/runs/{id}/artifacts, or the presign upload flow
                    (fold #16: fingerprint -> presign -> PUT to R2 -> confirm)
  link()         -> PATCH /v1/runs/{id} (per-key new-wins merge into the real
                    runs.foreign_keys column, fold #8)
  snapshot()     -> content-addressed execution record (fold #7); pins run.env_ref
                    and records git provenance on a code_snapshot artifact
  finish()       -> PATCH /v1/runs/{id} {status, ended_at}

The presign upload flow carries ``kind``/``meta`` (Harbor-ownership Phase 0), so
byte uploads and reference artifacts label identically — no gaps flagged.
"""

from __future__ import annotations

import contextvars
import errno
import functools
import json
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor, as_completed
import math
import os
import random
import re
import socket
import stat
import subprocess
import threading
import time
import tempfile
import warnings
import weakref
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any
from uuid import NAMESPACE_URL, UUID, uuid4, uuid5

from . import safe_warn as _diagnostics
from . import coerce as _coerce
from . import errors
from .redaction import default_scrub, is_sensitive_key
from .session_marker import WIZARD_HINT
from .secret_gate import (
    CredentialBlocked,
    CredentialInPath,
    _check_path as _check_upload_path,
    check_upload,
    freeze_upload,
    original_upload_path,
    prepare_upload,
)
from . import ignore as _ignore
from . import launch as _launch
from . import logstream as _logstream
from . import multipart as _multipart
from . import outputs as _outputs
from . import preempt as _preempt
from . import snapshot as _snapshot
from . import unit_context
from .filetype import artifact_kind_for, file_extension, name_with_extension
from .hashing import fingerprint, local_file_uri, reference_fields
from .unit_context import FailureContext, UnitContext
# What a metric point's step and key must fit (review of #2053): see
# `unstorable.drop_unstorable_points`, the choke point every metrics POST
# passes; `Run.log` checks first only to warn with the step and key it saw.
from .unstorable import MAX_METRIC_KEY_BYTES
from .unstorable import STEP_MAX as _STEP_MAX
from .unstorable import STEP_MIN as _STEP_MIN
from .unstorable import key_too_long as _key_too_long
from ..models import (
    ArtifactCreate,
    DerivedProvenance,
    ExecutionRecordCreate,
    MetricBatch,
    MetricPointIn,
    SpanBatch,
    SpanCreate,
    UploadRequest,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from .client import Client


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

#: How many distinct flattening warnings one run remembers (#2009 review).
_FLATTEN_WARNINGS_REMEMBERED = 256

#: Why a mapping was kept whole, as a warning names it.
_KEPT_WHOLE_REASONS = {
    "depth": f"nested past {_FLATTEN_MAX_DEPTH} levels",
    "cycle": "a dict that contains itself",
    "unreadable": "a mapping that could not be read",
    "length": f"a flattened key would pass {_NESTED_KEY_MAX_CHARS} characters",
    "budget": (
        f"this run already has {_NESTED_KEY_BUDGET} distinct keys from nested dicts; "
        "a dict keyed by data (example ids, file names) would mint a series per key -- "
        "log it as a list or an artifact instead"
    ),
}


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
    """``{"a": {"b": 1}}`` -> ``{"a/b": 1}``: the key shape the dashboard
    sections panels by (``dashboard/src/lib/chart.ts`` ``keyPrefix``).

    Returns ``(flat, collided, kept_whole)``. Only ``collections.abc.Mapping``
    values expand -- a dict, an OmegaConf ``DictConfig`` -- and a nested key
    becomes ``str(k)``; a TOP-LEVEL key passes through exactly as given, as it
    does when nothing is nested. Lists and every other value are leaves, left
    for the caller's numeric / step-attribute split. An empty mapping
    contributes nothing.

    Redaction is by a field's OWN key name, and flattening must not change that
    (#2009 review): ``db/pwd`` would normalise to ``db_pwd``, which no rule
    matches. So a nested leaf whose own key is sensitive goes through
    ``default_scrub(value, key=<its own key>)`` here, and a mapping under a
    sensitive key -- at the top level too, ``bytes`` keys included -- is never
    expanded: it is scrubbed whole, as the scrubber drops a credential bundle.
    An OmegaConf node is read through :mod:`probe.sdk.omegaconf_read`, so an
    interpolation that would reveal a secret (``${oc.env:...}``,
    ``${wandb.api_key}``, a chain to either) stays its unresolved text.

    ``collided``: ``(key, top-level key)`` for keys two spellings produced
    (``"a/b"`` beside ``{"a": {"b": ...}}``). The SHALLOWER spelling wins
    whatever the dict order, so an explicit key always beats a nested one.

    ``kept_whole``: ``(key, reason, top-level key)`` for each mapping that
    stays one value -- nested past ``_FLATTEN_MAX_DEPTH`` segments, a mapping
    that contains itself, one that raised when read, or one whose keys would
    pass ``_NESTED_KEY_MAX_CHARS``. The budget is per TOP-LEVEL key: when a
    top-level key's nested dicts would take the run's distinct nested keys
    (``known``, updated here) past ``_NESTED_KEY_BUDGET``, that whole
    top-level value stays one step attribute, so a dict of dicts keyed by data
    costs one attribute and one warning, not one per id. Never raises for such
    input: this runs inside the training loop."""
    from . import omegaconf_read

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
            sensitive = _sensitive_key_name(name)
            if not isinstance(value, Mapping) or sensitive:
                # A sensitive leaf is redacted by its own name, numbers
                # included where the scrubber redacts them; a mapping under a
                # sensitive name is a credential bundle, scrubbed whole.
                staged.append((key, default_scrub(value, key=name) if sensitive else value, depth, None))
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
        if not isinstance(value, Mapping) or _sensitive_key_name(name):
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


#: Plan (f): how many recent steps ``Run.log`` remembers the sent step-record
#: attributes of, so a repeat write to one of them sends the union.
_STEP_ATTRIBUTES_REMEMBERED = 64

#: How long ``finish()`` waits for a lock ``log()`` holds before giving up on the
#: held rows (#2025 review). A signal handler that calls ``finish()`` -- SLURM
#: ``--signal=USR1``, submitit preemption -- runs on the thread it interrupted,
#: so if that thread was inside ``log()`` the lock is never released and a
#: plain wait would hang the handler forever.
_CLOSE_LOCK_WAIT_SECONDS = 0.5


class _PendingRow:
    """One step's values held by ``Run.log(commit=False)`` (plan (f)).

    Last value per key wins. A numeric point's identity includes its
    dimensions and labels, as a series' does, so two ranks' ``loss`` stay two
    points; a key logged as a number and then as a string (or back) keeps only
    the latest. ``wall_clock`` is the latest contributing call's time."""

    __slots__ = ("step", "points", "other", "wall_clock")

    def __init__(self, step: int | None) -> None:
        self.step = step
        self.points: dict[tuple[str, str, str], tuple] = {}
        self.other: dict[str, Any] = {}
        self.wall_clock: str | None = None

    def merge(
        self,
        numeric: dict[str, float],
        other: dict[str, Any],
        dims: dict[str, Any],
        labs: dict[str, Any],
        span_id: str | None,
        agg: str | None,
        wall_clock: str,
    ) -> None:
        if other:
            for ident in [i for i in self.points if i[0] in other]:
                del self.points[ident]
            self.other.update(other)
        if numeric:
            coords = json.dumps(dims, sort_keys=True, default=repr)
            labels = json.dumps(labs, sort_keys=True, default=repr)
            for key, value in numeric.items():
                self.other.pop(key, None)
                ident = (key, coords, labels)
                self.points.pop(ident, None)
                self.points[ident] = (key, value, dims, labs, span_id, agg)
        self.wall_clock = wall_clock

    def point_list(self) -> list[tuple]:
        return list(self.points.values())


#: "The caller did not pass this at all", as distinct from an explicit ``None``.
#: Load-bearing for spans: the ATIF expander and the Harbor trial importer replay
#: STORED trajectories and pass ``started_at=<maybe None>`` deliberately, because a
#: stored step may have no usable timestamp. Defaulting those to ``now()`` would
#: write a fabricated time into a historical record. Omitting the argument — which
#: only live code does — is what opts into a default.
_UNSET: Any = object()

#: The span currently entered via ``with run.span(...)``, or None. A contextvar
#: rather than an attribute on Run: concurrent rollouts in threads or asyncio
#: tasks each get their own view, so they never adopt each other as parents. This
#: is span NESTING, distinct from unit_context's coords/labels contextvar.
_current_span: contextvars.ContextVar["SpanHandle | None"] = contextvars.ContextVar(
    "probe_current_span", default=None
)


def _metric_batch_body(
    points: list[MetricPointIn], *, provenance: DerivedProvenance | None = None
) -> dict:
    """Serialize a metric batch. Origin is BATCH-level by design (0087): a derived
    computation writes one logical stream, so a mixed-origin batch is
    unrepresentable rather than merely discouraged.

    A logged batch stays byte-identical to what it has always been — `origin` and
    `provenance` are None-excluded, so nothing new rides on the hot path."""
    batch = MetricBatch(
        points=points,
        origin="derived" if provenance is not None else None,
        provenance=provenance,
    )
    body = batch.model_dump(mode="json", exclude_none=True)
    if provenance is not None:
        # `inputs` are SeriesSelectors, whose READ-side fields (smoothing_factor,
        # smoothing_window, x_axis...) carry defaults. Dumped normally they land
        # in stored provenance as smoothing settings on a lineage record that has
        # nothing to do with smoothing — noise a human then has to discount.
        # exclude_defaults keeps only what the caller actually declared.
        body["provenance"] = provenance.model_dump(
            mode="json", exclude_none=True, exclude_defaults=True
        )
    return body


def _derived_provenance(
    *,
    producer: str,
    note: str | None,
    inputs: list[Any] | None,
    code_ref: str | None,
    kind: str,
) -> DerivedProvenance:
    """Build the provenance record for a derived write.

    `inputs` is self-declared lineage: which stored series the computation read.
    Bare strings are the common case and resolve to `{key, kind}` against the
    batch's own kind, so a caller writing `inputs=["eval/mean_reward"]` gets a
    real selector rather than a rejected body.
    """
    selectors = None
    if inputs:
        selectors = [
            {"key": item, "kind": kind} if isinstance(item, str) else item for item in inputs
        ]
    return DerivedProvenance(producer=producer, note=note, inputs=selectors, code_ref=code_ref)


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


class RunConfig(dict):
    """``run.config`` (plan (c)): the run's config as a dict whose writes merge
    into the stored config through :meth:`Run.update_config`.

    Reads come from this handle's copy. Writes -- ``cfg["lr"] = ...``,
    ``cfg.update(...)``, ``cfg.setdefault(...)``, ``cfg.lr = ...`` -- are sent
    first and then reflected here. Removing a key raises ``TypeError``: the
    server merges, it never deletes, so a local delete would be a lie."""

    __slots__ = ("_run",)

    def __init__(self, run: "Run") -> None:
        super().__init__(run._data.get("config") or {})
        object.__setattr__(self, "_run", run)

    def _merge(self, values: dict) -> None:
        # stacklevel 4: _update_config <- _merge <- the dict method <- the caller.
        self._run._update_config(values, allow_val_change=None, strict=None, stacklevel=4)
        super().clear()
        super().update(self._run._data.get("config") or {})

    def __setitem__(self, key: Any, value: Any) -> None:
        self._merge({key: value})

    def update(self, *args: Any, **kwargs: Any) -> None:  # type: ignore[override]
        # `run.config.update(args)` with an argparse Namespace is THE W&B
        # pattern (#2032 review): coerce anything config-shaped first; only a
        # plain iterable of pairs takes dict()'s path.
        values: dict = {}
        for arg in args:
            try:
                values.update(_coerce.to_config(arg))
            except errors.ValidationError:
                values.update(dict(arg))
        values.update(kwargs)
        self._merge(values)

    def __ior__(self, other: Any) -> "RunConfig":
        # `cfg |= {...}` would otherwise update only this local copy.
        self.update(other)
        return self

    def __reduce__(self) -> tuple:
        # copy.copy / deepcopy / pickle give a plain dict snapshot: a copy must
        # not send writes, and reconstructing this class would (#2032 review).
        return (dict, (dict(self),))

    def setdefault(self, key: Any, default: Any = None) -> Any:
        if key not in self:
            self._merge({key: default})
        return self.get(key, default)

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name) from None

    def __setattr__(self, name: str, value: Any) -> None:
        self._merge({name: value})

    def _no_removal(self, *_args: Any, **_kwargs: Any) -> Any:
        raise TypeError(
            "probe: a run's config only merges; keys cannot be removed "
            "(set the key to None instead)"
        )

    __delitem__ = pop = popitem = clear = __delattr__ = _no_removal  # type: ignore[assignment]


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
                from .failure_context import identifiers, remember

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


def _env_async_uploads(*, default: bool) -> bool:
    """`PROBE_ASYNC_UPLOADS` as a tri-state, mirroring `PROBE_ASYNC`.

    A separate knob from write mode on purpose: queueing a metric batch costs
    a few hundred bytes, queueing a checkpoint costs a copy of the checkpoint.
    Someone may reasonably want one and not the other.
    """
    raw = (os.environ.get("PROBE_ASYNC_UPLOADS") or "").strip().lower()
    if not raw:
        return default
    if raw in {"1", "true", "yes", "on"}:
        return True
    if raw in {"0", "false", "no", "off"}:
        return False
    _diagnostics.warn(f"ignoring unrecognised PROBE_ASYNC_UPLOADS={raw!r}; expected on or off")
    return default


#: How a snapshot stores the files git cannot supply. ``archive`` is one
#: deterministic tar.gz per run (the original design); ``artifacts`` is one
#: ``kind='code'`` artifact row per file, content-addressed so an unchanged
#: file across runs is stored once and every captured file is visible in the
#: run's artifact explorer. ``artifacts`` is the default since the CLI release
#: after 0.140.0 (the server's batch doors landed in 0.352.0.0);
#: ``PROBE_CODE_STORAGE=archive`` keeps the one-tarball-per-run behaviour.
CODE_STORAGE_ENV = "PROBE_CODE_STORAGE"
CODE_STORAGE_ARCHIVE = "archive"
CODE_STORAGE_ARTIFACTS = "artifacts"
DEFAULT_CODE_STORAGE = CODE_STORAGE_ARTIFACTS
#: The whole per-file capture gets this long, presign to last confirm. A tree of
#: thousands of files on a flaky network must not park `run.snapshot()` (which
#: runs before the training loop) for hours: past the deadline the remaining
#: files are named as unstored and the run goes on (under ``strict=True`` the
#: deadline raises, like any other storage failure). `PROBE_CODE_CAPTURE_DEADLINE`
#: (seconds) overrides it.
CAPTURE_DEADLINE_SECONDS = 600.0
#: The half-failed outage rule needs a window at least this big; below it only
#: a window that failed entirely is an outage.
OUTAGE_MIN_WINDOW = 8
#: Presign -> PUT -> confirm happens in windows of this many files, so a client
#: that dies mid-upload strands at most one window of pending rows for the
#: server's reaper, not a whole 7,942-file tree. Must stay <= the server's
#: confirm cap (500): one window is one confirm call.
CAPTURE_WINDOW = 256
#: Concurrent presigned PUTs per window.
CAPTURE_PUT_WORKERS = 16
#: The snapshot row's newline-joined path list is what /v1/search matches a
#: captured tree on; it also rides every list response that carries the row,
#: so it is bounded. 512 KB covers the largest tree seen so far (7,942 paths).
PATHS_TEXT_MAX_BYTES = 512 * 1024
_SIGNED_QUERY = re.compile(r"\?[^\s'\"]*")


def _code_storage() -> str:
    raw = (os.environ.get(CODE_STORAGE_ENV) or "").strip().lower()
    if raw in (CODE_STORAGE_ARCHIVE, CODE_STORAGE_ARTIFACTS):
        return raw
    if raw:
        _diagnostics.warn(
            f"{CODE_STORAGE_ENV}={raw!r} is not one of "
            f"{CODE_STORAGE_ARCHIVE!r}/{CODE_STORAGE_ARTIFACTS!r}; using {DEFAULT_CODE_STORAGE!r} "
            "(to store no code at all, pass upload=False / --no-upload)",
            stacklevel=2,
        )
    return DEFAULT_CODE_STORAGE


def _capture_deadline() -> float:
    raw = (os.environ.get("PROBE_CODE_CAPTURE_DEADLINE") or "").strip()
    try:
        return float(raw) if raw else float(CAPTURE_DEADLINE_SECONDS)
    except ValueError:
        return float(CAPTURE_DEADLINE_SECONDS)


def _redact_signed(message: str) -> str:
    """A presigned URL's query string IS its credential (an hour of access to
    that object); an error message that quotes one must not reach a warning, a
    transcript or the run's metadata."""
    return _SIGNED_QUERY.sub("?<signed>", message)


def _warn_credential_skips(manifest: dict) -> None:
    """Say, once, what code capture left out that the person would not expect:
    a file WITHHELD because its content looks like a credential, and any TRACKED
    file stopped by name or content (a committed file missing from a capture
    breaks its restore). An untracked `.env` skipped by name is expected and
    stays in the record only. Rule names only, never a value."""
    skipped = [s for s in manifest.get("skipped") or [] if isinstance(s, dict)]
    hits = [s for s in skipped if s.get("found_in") == "content"]
    slow = [s for s in skipped if s.get("found_in") == "scan_time"]
    tracked = [s for s in skipped if s.get("tracked") and s.get("found_in") not in ("content", "scan_time")]
    if not hits and not tracked and not slow:
        return

    def _names(items: list) -> str:
        shown = ", ".join(str(s.get("path")) for s in items[:10])
        return shown + (f" (+{len(items) - 10} more)" if len(items) > 10 else "")

    parts = []
    if hits:
        rules = sorted({str(r) for s in hits for r in s.get("rules") or ()})
        marked = [dict(s, path=f"{s.get('path')} (tracked)") if s.get("tracked") else s for s in hits]
        parts.append(
            f"withheld {len(hits)} file(s) whose contents look like a credential "
            f"({', '.join(rules)}): {_names(marked)}. A snapshot stores exact bytes and "
            "never redacts, so these were not uploaded; move the key to an environment "
            "variable or a gitignored file to capture the rest of the file"
        )
    if tracked:
        parts.append(
            f"left out {len(tracked)} tracked file(s) whose NAME marks a credential: "
            f"{_names(tracked)}; restoring this run will not rebuild them"
        )
    if slow:
        parts.append(
            f"withheld {len(slow)} file(s) whose credential scan could not finish in "
            f"time: {_names(slow)}. Unscanned bytes are never uploaded; raise "
            f"{_snapshot.FILE_SCAN_BUDGET_ENV} / {_snapshot.SNAPSHOT_SCAN_BUDGET_ENV} "
            "(seconds, 0 = no limit) to scan them"
        )
    _diagnostics.warn(
        "probe: code capture " + "; and ".join(parts) + ". All are listed as skipped "
        "(reason 'secret' or 'scan_budget') on the run's code snapshot.",
        stacklevel=3,
    )


#: How long `finish()` waits for another process (the worker) to finish scanning
#: this run's queued uploads. Scanning is local and takes seconds; this only
#: bounds a promoter that hung while holding an item.
WAITING_PROMOTE_TIMEOUT = 300.0

#: Returned by `_maybe_queue_upload` when the upload was NOT queued and the
#: caller must fall through to the synchronous path. Distinct from None, which
#: is a legitimate "queued, no row yet" answer.
_NOT_QUEUED = object()

#: Set by a caller that reports a failed upload in its OWN words (the
#: code-bytes archive), so `Run._warn_not_uploaded` stays quiet for that call
#: instead of telling the user to pass `strict=True` to a `log_artifact` they
#: never made. A ContextVar, not an attribute: a sampler thread logging its own
#: artifacts at the same moment must still hear about its failures.
_OWN_UPLOAD_WARNING: contextvars.ContextVar[bool] = contextvars.ContextVar(
    "probe_own_upload_warning", default=False
)


def _gate_reason(refusal: object) -> str:
    """A gate refusal's reason without its generic "Artifact upload refused: "
    prefix, for a sentence that already says it was refused."""
    return str(refusal).removeprefix("Artifact upload refused: ")


def _require_upload_source(path: str, *, allow_missing: bool) -> bool:
    """Raise for a mistake in the CALL, before the gate sees the file.

    Only what the credential gate refuses about a real file -- over the size
    limit, a credential in its path, its content, bytes that moved while they
    were read -- becomes a pointer row instead of an exception (plan 0.7). A
    typo'd path, a directory, a FIFO or an unreadable file is the caller's to
    fix and raises exactly as before, so it cannot hide behind a warning the
    warn-once rule would silence the second time.

    Returns True when there is a file to upload, False only for a missing one
    the caller passed ``allow_missing`` for (the ``reference=True`` rule).

    Run after the path's own credential check: every message here quotes it.
    """
    local = os.path.abspath(path)
    try:
        info = os.stat(local)
    except FileNotFoundError:
        if allow_missing:
            return False
        raise FileNotFoundError(
            errno.ENOENT,
            "cannot upload: no such file (pass allow_missing=True to record a pointer "
            "to it anyway)",
            local,
        ) from None
    if stat.S_ISDIR(info.st_mode):
        raise IsADirectoryError(
            errno.EISDIR, "cannot upload a directory: log each file in it", local
        )
    if not stat.S_ISREG(info.st_mode):
        # The gate's own refusal, raised as it always was: a FIFO or a device
        # is not a file the caller can have meant to upload.
        raise CredentialBlocked("Artifact upload refused: upload source must be a regular file")
    if not os.access(local, os.R_OK):
        raise PermissionError(errno.EACCES, "cannot upload: permission denied", local)
    return True


#: Statuses after which a run can never beat again. Mirrors the server's CHECK
#: constraint minus 'created'/'running' (db/experiment/schema.sql in research-os).
_TERMINAL_STATUSES = frozenset({"completed", "failed", "crashed", "canceled", "untracked"})



#: The server reaps a beating run after `run_heartbeat_stale_seconds` of silence
#: (default 900, floor 300 — app/core/config.py in research-os). 60s keeps many
#: beats inside even the floor, so one dropped request never looks like death.
_HEARTBEAT_INTERVAL_SECONDS = 60.0

#: The DEFAULT deadline for `finish()` (plan 0.2, decision D1), in seconds;
#: ``flush_timeout=`` or ``PROBE_FINISH_TIMEOUT_SEC`` overrides it.
#:
#: The default close used to be a hard barrier that made ONE delivery attempt
#: and raised (PR #1679 gave it a 15 s retry, and it still raised after). A
#: close that raises over telemetry breaks the maintainer rule written in
#: `_warn_if_capture_incomplete` -- "nothing, opt-in or otherwise, may block a
#: run" (2026-08-06, argued in design PR #1680) -- and live it raised on 4 of 6
#: ten-step runs whenever the hardware rail's write collided with the drain
#: (a 503 "concurrent telemetry write"). Now every close retries to this
#: deadline, then queues its terminal status BEHIND whatever is still
#: undelivered (`_queue_deferred_finish`) and returns. 600 s outlasts a deploy
#: or an ingress restart and stays under the server's 900 s silence reaper,
#: which the heartbeat keeps at bay while the close waits.
FINISH_TIMEOUT_DEFAULT_SECONDS = 600.0

#: `Run._finish_result` while a close is running (see `Run.finish`).
_FINISHING: Any = object()

#: The close loop's waits (first, ceiling), fed to `durable.backoff_delays`
#: like every other durable retry loop (plan 0.6). Short on purpose: someone is
#: waiting on this one, and the first retry of a blip should land in half a
#: second, while the 4 s ceiling keeps a long deadline from hammering a sick
#: server (PR #1679's numbers).
_FINISH_BACKOFF = (0.5, 4.0)

#: The part of the deadline kept back from the drain for the close ITSELF --
#: the final status write, or the deferred-close beacon -- so a drain that runs
#: to the deadline does not leave the terminal write no time at all. At most a
#: quarter of a short deadline.
_CLOSE_RESERVE_SECONDS = 5.0


def _close_reserve(timeout: float) -> float:
    """The slice of the close's budget that must reach the drain and the
    terminal write untouched: every LOCAL-only step before the drain
    (lineage hashing, the hardware collector, capture, upload promotion) is
    bounded to ``deadline - this``, never the raw deadline, so a close whose
    local finalizers spend their whole individual allowance under contention
    still leaves this reserve for delivery. Without it, a SIGTERM close with
    read/write capture on could spend the ENTIRE budget hashing and stopping
    the hardware collector -- both individually bounded to "half of what's
    left" -- and die with nothing sent at all: the run stayed `running`
    (review of the read/write capture flake, #2124 on #2119's budget)."""
    return min(_CLOSE_RESERVE_SECONDS, 0.25 * timeout)


#: Longest single wait for the drain lock before looking again at what of this
#: run is still queued: the lock's holder (the detached worker, mid-pass) may be
#: delivering exactly those ops.
_FINISH_LOCK_POLL_SECONDS = 1.0


def _heartbeat_interval() -> float:
    """Read PROBE_HEARTBEAT_SECONDS at call time, never at import time.

    ``0`` (or any non-positive value) is the kill switch: no thread is started.
    """
    raw = os.environ.get("PROBE_HEARTBEAT_SECONDS")
    if raw is None:
        return _HEARTBEAT_INTERVAL_SECONDS
    try:
        return float(raw)
    except ValueError:
        return _HEARTBEAT_INTERVAL_SECONDS


def _global_rank() -> int | None:
    """This process's global rank when above 0, else None (fluent's reading)."""
    from .fluent import _nonzero_global_rank

    return _nonzero_global_rank()


def _beat_forever(
    client: "Client",
    run_id: str,
    stop: threading.Event,
    interval: float,
    role: str = "owner",
    write_epoch: int | None = None,
    attached: bool = False,
    handle_ref: "weakref.ref[Run] | None" = None,
    lease: dict | None = None,
) -> None:
    """The heartbeat loop. A module function, not a bound method, so the thread
    pins only the client and the run id — an abandoned Run handle stays collectable.

    ``lease`` (SDK reliability 2.8): beat this writer's LEASE instead of the
    run-level heartbeat, carrying its progress counter, and JITTER every wait
    (the first one included) by +-20% of the interval, so 608 ranks started
    together never beat together. The lease already exists (the create, attach
    or reopen registered it), so a late first beat costs nothing.

    Failures are swallowed: a missed beat self-heals (the stale window is many
    intervals wide) and liveness reporting must never take down the work it is
    reporting on. Beats deliberately bypass the spool — replaying a stale "I was
    alive" later would be a lie.

    OBSERVER BEATS FAIL CLOSED against pre-0106 servers. A server that predates
    ``role`` silently drops the query param and records the beat in
    last_heartbeat_at — the OWNERSHIP column — which would permanently poison
    the crashed-vs-untracked verdict for a run that was only ever watched. The
    capability probe below reads the run first: a 0106+ server always serializes
    an ``observer_heartbeat_at`` key (null or set); an old server's response
    model has no such field. Absent key ⇒ old server ⇒ no beat is ever sent.
    """
    if role == "observer" and lease is None:
        try:
            if "observer_heartbeat_at" not in client.get_run(run_id):
                return
        except Exception:
            return  # can't prove support; not beating is the safe direction
    if lease is not None and stop.wait(random.uniform(0.0, interval)):
        return
    # 0205. Swallowing beat failures self-heals a blip, but an outage longer
    # than the server's stale window is not a blip: the reaper ends the run as
    # 'crashed' while this process is alive and still beating, and every beat
    # after that is a silent no-op against a terminal row. Nothing reconciled
    # it, so a healthy job stayed attached to a dead row for the rest of its
    # life. Count the failures; on the first beat that lands again, check
    # whether we were declared dead while we were away, and if the row is still
    # OURS (same write_epoch -- no newer attempt took it over) put it back.
    failures = 0
    # A recovery that failed TRANSIENTLY (a 503 while every rank's backlog
    # drains, a timeout) is retried on the following beats, up to a cap: one
    # try left a job that outlived an outage `crashed` for the rest of its life
    # although every later beat landed.
    recovery_tries = 0
    # Set when the capped retries ran out on a row that stays `crashed`, so a
    # beat landing on it does not restart the whole cycle every few beats.
    gave_up = False
    while True:
        try:
            row = _beat_once(
                client,
                run_id,
                role=role,
                attached=attached,
                write_epoch=write_epoch,
                lease=lease,
                handle_ref=handle_ref,
            )
            # 2.2: a beat that LANDS on a `crashed` row means something ended
            # this run while its owner is alive and heard -- a writer-gone
            # report that was wrong, or a reaper verdict from before a blip we
            # never saw fail. Same repair as after a failed beat.
            reaped = isinstance(row, dict) and row.get("status") == "crashed"
            if not reaped:
                gave_up = False
            if failures or (reaped and not gave_up):
                recovered = _recover_after_outage(
                    client,
                    run_id,
                    role=role,
                    write_epoch=write_epoch,
                    handle_ref=handle_ref,
                    # Beats kept landing, so no outage explains the verdict:
                    # repair only what the SYSTEM decided (the reaper, a
                    # writer-gone report), never a person's `crashed`.
                    system_verdict_only=not failures,
                )
                if recovered is _RECOVERY_RETRY:
                    recovery_tries += 1
                    if recovery_tries < _MAX_RECOVERY_TRIES:
                        if stop.wait(interval):
                            return
                        continue  # keep `failures`: the repair is still owed
                if recovered is None or recovered is _RECOVERY_RETRY:
                    # Nothing this process can do about THIS crashed row;
                    # a later change of the row (or a new outage) re-arms it.
                    gave_up = reaped
                else:
                    # The receipt's generation. With keep_epoch (1.1) it is the
                    # one we already hold; adopting it anyway (here AND on the
                    # handle, inside _recover_after_outage) keeps this process
                    # writable if a server ever answers with another.
                    write_epoch = recovered
            failures = 0
            recovery_tries = 0
        except errors.ConflictError:
            # 0185's fence answers a SUPERSEDED writer's beat with 409: a
            # relaunch took this run over (2.3) and owns it on a newer epoch.
            # Every later write from this process is refused too, so say so
            # once and stop beating instead of failing quietly forever.
            _diagnostics.warn(
                f"probe: run {run_id} was taken over by a newer attempt; this "
                "process no longer writes to it (its writes are refused). If "
                "this job is still meant to run, relaunch it as its own run."
            )
            return
        except Exception:
            failures += 1
        if stop.wait(interval * random.uniform(0.8, 1.2) if lease is not None else interval):
            return


class _Progress:
    """This writer's PROGRESS counter (SDK reliability 2.8, Signal 1): bumped
    once per training or validation batch -- a non-hardware `log()` or
    `step()`, an integration's batch-end hook, or `Run.progress()` -- and sent
    on every lease beat for the server's stall detector.

    A span (a step, a rollout, a trial) and an artifact upload count too: a
    checkpoint save that uploads is work, not a stall.

    Idle is measured on the MONOTONIC clock, so an outage never fakes a stall
    and a slow network never hides one. The baseline is two numbers kept here
    so the server stores two, not a series: the p99 of the gap between bumps
    over the last 24 h (per-hour log-scale histograms, 1 ms to ~15 h, 25% bins,
    so the memory is fixed however fast the loop runs), and the longest gap
    that was followed by progress again over the WHOLE run (the nightly
    checkpoint or the long eval this run already survived)."""

    _WINDOW_HOURS = 24
    _FLOOR = 0.001
    _RATIO = 1.25
    _BINS = 80

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.count = 0
        self._last: float | None = None
        #: hour index -> (bin counts, longest gap that hour)
        self._hours: dict[int, tuple[list[int], float]] = {}
        #: The longest gap this writer ever recovered from, over the WHOLE run:
        #: a nightly checkpoint learned once stays learned (a 24 h window would
        #: forget it just before the next one).
        self._longest_ever = 0.0

    def bump(self) -> None:
        now = time.monotonic()
        with self._lock:
            if self._last is not None and now > self._last:
                self._record(now, now - self._last)
            self._last = now
            self.count += 1

    def _record(self, now: float, gap: float) -> None:
        hour = int(now // 3600)
        bins, longest = self._hours.get(hour) or ([0] * (self._BINS + 1), 0.0)
        index = 0 if gap <= self._FLOOR else int(math.log(gap / self._FLOOR, self._RATIO)) + 1
        bins[min(index, self._BINS)] += 1
        self._hours[hour] = (bins, max(longest, gap))
        self._longest_ever = max(self._longest_ever, gap)
        for old in [h for h in self._hours if h <= hour - self._WINDOW_HOURS]:
            del self._hours[old]

    def snapshot(self) -> dict:
        """The beat's progress fields (none before the first bump)."""
        now = time.monotonic()
        with self._lock:
            if self._last is None:
                return {}
            out: dict[str, Any] = {
                "progress": self.count,
                "progress_idle_seconds": round(now - self._last, 3),
            }
            live = {h: v for h, v in self._hours.items() if h > int(now // 3600) - self._WINDOW_HOURS}
            if live:
                merged = [0] * (self._BINS + 1)
                for bins, _ in live.values():
                    merged = [a + b for a, b in zip(merged, bins)]
                total = sum(merged)
                seen = 0
                for index, n in enumerate(merged):
                    seen += n
                    if seen >= 0.99 * total:
                        # The bin's UPPER edge: a conservative (longer) p99.
                        out["progress_gap_p99_seconds"] = round(self._FLOOR * self._RATIO**index, 3)
                        break
            if self._longest_ever > 0:
                out["progress_longest_gap_seconds"] = round(self._longest_ever, 3)
            return out


#: How long a finishing writer's draining beat keeps its lease live (2.8):
#: the server's cap. The queued release ends it sooner when it lands.
_LEASE_DRAIN_SECONDS = 3600.0
#: The most a close spends on one lease beat of its own (the draining beat, or
#: the beat that learns an unknown protocol): a liveness hint must never hold a
#: pre-empted job's exit (review of #2060).
_CLOSE_BEAT_SECONDS = 5.0
#: The least a deferred close's draining beat gets. That beat goes out AFTER
#: the close's own budget ran out -- the reason it deferred -- so under what was
#: left of it the beat was never sent: the lease then expired while the worker
#: was still delivering, and `writer_lost` fired falsely. It holds a close past
#: its deadline by at most this much.
_DRAINING_BEAT_MIN_SECONDS = 1.0


#: `_recover_after_outage` could not finish for a reason that may pass (see
#: `journal.classify`): the beat loop tries again on its next beats.
_RECOVERY_RETRY: Any = object()
#: Recovery attempts per outage before the loop gives up (about five minutes
#: at the default 60 s beat). The reaper's verdict then stands, as it did.
_MAX_RECOVERY_TRIES = 5


def _lease_beat(
    client: "Client",
    run_id: str,
    lease: dict,
    write_epoch: int | None,
    handle_ref: "weakref.ref[Run] | None",
    *,
    attached: bool = False,
) -> dict:
    """One lease beat (2.8), in the run-level beat's row shape (``status``,
    ``write_epoch``) so the loop's recovery reads it the same way. The
    handle, while it lives, supplies the progress counter and learns which
    protocol the server keeps this run on."""
    handle = handle_ref() if handle_ref is not None else None
    body = {**lease, "write_epoch": write_epoch or 1}
    body.pop("session_id", None)
    if attached:
        # From inside the work (0205): the beat stamps `attached_at`, as the
        # run-level `?attached=true` did -- an OWNER lease included.
        body["attached"] = True
    if handle is not None:
        body.update(handle._progress.snapshot())
    resp = client.beat_writer(run_id, lease["session_id"], body)
    if handle is not None:
        handle._note_lease_answer(resp)
    return {
        "status": resp.get("run_status") if isinstance(resp, dict) else None,
        "write_epoch": resp.get("write_epoch") if isinstance(resp, dict) else None,
    }


def _beat_once(
    client: "Client",
    run_id: str,
    *,
    role: str,
    attached: bool,
    write_epoch: int | None,
    lease: dict | None = None,
    handle_ref: "weakref.ref[Run] | None" = None,
) -> Any:
    """One beat. When the API refuses the CREDENTIAL (plan 2.7), re-read it and
    retry once: a re-login on the box revokes the token this process was built
    with, and a swallowed 401 on every beat after that is how a live run was
    reaped as `crashed` 15 minutes later. A refusal of one request's scope is
    not the credential and is not retried (`key_refusal.credential_refused`)."""
    refused = getattr(getattr(client, "settings", None), "token", None)

    def beat() -> Any:
        if lease is not None:
            return _lease_beat(client, run_id, lease, write_epoch, handle_ref, attached=attached)
        return client.heartbeat_run(run_id, role=role, attached=attached, write_epoch=write_epoch)

    try:
        return beat()
    except errors.RosError as exc:
        from .key_refusal import credential_refused

        refresh = getattr(client, "refresh_credentials", None)
        if (
            refresh is None
            or not credential_refused(exc.status, str(exc))
            or not refresh(refused=refused)
        ):
            raise
        return beat()


def _recover_after_outage(
    client: "Client",
    run_id: str,
    *,
    role: str,
    write_epoch: int | None,
    handle_ref: "weakref.ref[Run] | None" = None,
    system_verdict_only: bool = False,
) -> Any:
    """Reopen a run the reaper ended while this process could not be heard.

    Returns the epoch the run was reopened under, None when there was nothing
    to do (or nothing this process may do), or ``_RECOVERY_RETRY``.

    Deliberately narrow. Only an OWNER recovers -- an observer never staked its
    lifetime on the run and has no standing to resurrect it. Only 'crashed' is
    recovered: that is the verdict meaning "an owner was beating and stopped",
    which is exactly what an outage manufactures. And only when the row's epoch
    still matches ours, so a newer attempt that legitimately took the run over
    is never clobbered by the old process waking up. A handle that does not
    know its epoch cannot prove that, so it does not recover.

    The reopen KEEPS the epoch (SDK reliability 1.1). It used to bump it, and
    every op this process had already queued still carried the old one: the
    server fenced each with 409 and the drain dead-lettered it (live: a
    20-minute outage lost 2,478 of 2,659 steps), and every OTHER rank of the
    same job, still on the old epoch, was fenced for the rest of the run. The
    server honours `keep_epoch` only for a `crashed` row still on
    `expected_write_epoch`, so a writer a newer attempt superseded cannot use
    it to take the run back.

    An older server drops `keep_epoch` and would bump anyway, so there the
    reopen is SKIPPED (G1: `supports_feature` plus a fallback, not
    `_require_feature`, whose raise this thread would swallow). Nothing is lost
    by skipping: a crashed row still takes data (the fence refuses only an
    epoch OLDER than the row's), and `finish()` still writes the real verdict.

    Every failure here is swallowed: this is best-effort repair on a background
    thread, and it must never take down the work it is reporting on. A failure
    that may pass (a transport error, a 5xx) returns ``_RECOVERY_RETRY`` so the
    beat loop tries again; anything else (a 409: a sibling rank recovered it
    first, or a newer attempt owns it) ends the attempt.

    ``system_verdict_only`` (2.2) is for a beat that LANDED on a crashed row,
    with no failed beat to explain it: only a verdict the system made -- the
    reaper's (``reason: stale``) or a writer-gone report's -- is repaired. A
    person or an agent that set ``crashed`` on purpose (``probe run end
    --status crashed`` on a hung job whose beat thread still runs) meant it.
    """
    if role != "owner" or write_epoch is None:
        return None
    try:
        # Feature first: it is cached per client, so on an older server a beat
        # that keeps landing on the crashed row costs no request at all.
        if not client.supports_feature("run_reopen_keep_epoch"):
            return None
        row = client.get_run(run_id)
        if row.get("status") != "crashed":
            return None
        if row.get("write_epoch") != write_epoch:
            return None
        if system_verdict_only and not _crashed_by_the_system(client, run_id):
            return None
        # 2.8: a leased writer recovers under its OWN lease, so a GONE a wrong
        # writer-gone report left on it is undone (the server revives it), and
        # its later release does not close the run `crashed`.
        handle = handle_ref() if handle_ref is not None else None
        lease = getattr(handle, "_lease", None) if handle is not None else None
        receipt = client.reopen_run(
            run_id,
            session_id=lease["session_id"] if lease else str(uuid4()),
            keep_epoch=True,
            expected_write_epoch=write_epoch,
            writer=lease,
        )
    except Exception as exc:  # noqa: BLE001 -- see docstring
        from .journal import classify

        try:
            transient = classify(exc) == "transient"
        except Exception:  # noqa: BLE001
            transient = False
        return _RECOVERY_RETRY if transient else None
    new_epoch = receipt.get("write_epoch") if isinstance(receipt, dict) else None
    if new_epoch is None:
        return None
    new_epoch = int(new_epoch)
    # The handle is held WEAKLY so the beat thread still does not pin it: an
    # abandoned Run must stay collectable, and its collection is what ends the
    # beat. If it is already gone there is nothing left to write anyway.
    handle = handle_ref() if handle_ref is not None else None
    if handle is not None:
        handle.write_epoch = new_epoch
    return new_epoch


#: The `reason` a system-made `crashed` carries on its status event: the
#: reaper's stale sweep, and a writer-gone report (2.2). A status PATCH -- a
#: person, an agent, a launcher -- carries none.
_SYSTEM_CRASH_REASONS = frozenset({"stale", "writer_gone"})


def _crashed_by_the_system(client: "Client", run_id: str) -> bool:
    """Whether the run's latest status change is a system-made `crashed`.

    One read, and only when a beat lands on a crashed row (the loop then
    leaves that row alone until it changes). Raises on a failed read, which
    the caller classifies like any other recovery failure."""
    events = client.events.for_run(run_id)
    for event in events if isinstance(events, list) else []:
        if not isinstance(event, dict) or event.get("event_type") != "run.status_changed":
            continue
        payload = event.get("payload") or {}
        return payload.get("status") == "crashed" and payload.get("reason") in _SYSTEM_CRASH_REASONS
    return False


def _summary_wire(summary: dict | None) -> dict[str, dict]:
    """The headline-scalar map under BOTH wire names, for any body that carries it.

    `summary_metrics` is the real field; `summary` is the alias the server still
    accepts. Sending both is what makes this client safe in either direction, and
    neither hazard is hypothetical:

    * send only `summary` and the server can never drop the alias, because doing so
      would silently discard the map from every client still in the field;
    * send only `summary_metrics` and a server OLDER than the rename discards it
      just as silently -- and prod ran a pre-rename image for ~30 minutes on
      2026-09-21 while a failing post-upgrade hook rolled releases back.

    Both keys cost a few bytes and close both holes: every input schema resolves
    `AliasChoices("summary_metrics", "summary")`, taking the new name when present,
    and none sets `extra="forbid"`, so the spare key is ignored rather than refused
    -- including by a future server that has dropped the alias entirely.
    """
    return {"summary_metrics": summary, "summary": summary}


def _one_summary(summary_metrics: dict | None, summary: dict | None) -> dict | None:
    """Resolve the new kwarg against its deprecated spelling.

    `summary_metrics` is the field's real name: headline scalars the run ACHIEVED,
    which read as prose under the old name beside `summary_markdown` and the
    generated AI summary. `summary` is still accepted so a script written against an
    older SDK keeps working; passing both is a contradiction, not a merge.

    ON THE WIRE the map is sent under BOTH names -- see `_summary_wire`.
    """
    if summary_metrics is not None and summary is not None:
        raise errors.ValidationError(
            "pass summary_metrics or summary, not both: they are the same field, and "
            "silently preferring either is how a run ends up with the wrong numbers"
        )
    return summary_metrics if summary_metrics is not None else summary


def _with_finish_accounting(summary: dict | None, facts: dict[str, Any]) -> dict:
    """``summary`` with ``facts`` added to its ``probe_finish`` map, never in
    place of it: a caller's own close accounting (a reinit's ``closed_by``)
    survives the deferred and dead-letter branches, which write theirs into
    the same key."""
    accounting = (summary or {}).get("probe_finish")
    return {
        **(summary or {}),
        "probe_finish": {**(accounting if isinstance(accounting, dict) else {}), **facts},
    }


#: The id of the run whose launcher will close it, set in a child that
#: `execute(finalize=True)` runs: the launcher holds the child's real exit code
#: and closes the run from it. A `probe.init()` attached to THAT run sends no
#: terminal status at exit unless its own hooks saw how it ended --
#: `sys.exit(main())` looks `sys.exit` up before main() runs, so no wrapper sees
#: that exit, and the child's guess of `completed` used to land first and win
#: against the launcher's `only_if_running`. The id, not "1": a sweep driver
#: under `probe exec` that opens run B and hands PROBE_RUN_ID=B to a job passes
#: this variable on too, and B has no launcher to close it.
EXEC_FINALIZES_ENV = "PROBE_EXEC_FINALIZES"


def _status_for_system_exit(code: object, in_flight: BaseException | None) -> tuple[str, int]:
    """(run status, process exit status) for ``sys.exit(code)`` / ``SystemExit(code)``.

    The exit status is what the OS will report: None and False are 0, an int
    is taken modulo 256 (``sys.exit(-1)`` exits 255, ``sys.exit(256)`` exits
    0), anything else -- a message -- prints and exits 1. Never negative, so a
    stored code can never read as "killed by a signal". Ctrl-C in flight
    (Lightning's ``except KeyboardInterrupt: sys.exit(1)``) is ``canceled``."""
    exit_code = (int(code) & 0xFF) if isinstance(code, int) else (0 if code is None else 1)
    if isinstance(in_flight, KeyboardInterrupt):
        return "canceled", exit_code
    return ("completed" if exit_code == 0 else "failed"), exit_code


#: A child's exit reported as a RUN status.
#:
#: SIGINT IS A DECISION, NOT A DEFECT. `fluent.py` already says so for the
#: in-process path -- it maps KeyboardInterrupt to 'canceled' -- but `execute`
#: mapped purely on "is the code zero", so Ctrl-C under `probe exec` closed the
#: run 'failed' and mailed the researcher a crash notice about a run they had
#: just stopped themselves. That lands in the client-reported bucket, which is
#: otherwise the trustworthy 85% of crash alerts.
#:
#: BOTH SPELLINGS. `subprocess.run` reports a signalled child as -N; a shell in
#: between reports 128+N. Ctrl-C therefore arrives as -2 or 130 depending on
#: what was wrapped.
#:
#: SIGTERM IS DELIBERATELY NOT HERE. A scheduler preempting a job, an eviction,
#: a `kill` from another session -- those are exactly the deaths a researcher
#: does NOT already know about, and they are the case the crash email exists
#: for. Only the interrupt the person typed is a decision.
def _status_for_exit(returncode: int) -> str:
    import signal as _signal

    if returncode == 0:
        return "completed"
    if returncode in (-_signal.SIGINT, 128 + int(_signal.SIGINT)):
        return "canceled"
    return "failed"


class Run:
    def __init__(self, client: "Client", data: dict):
        self._client = client
        self._data = data
        self._hb_stop: threading.Event | None = None
        self._hb_thread: threading.Thread | None = None
        self._hb_finalizer: weakref.finalize | None = None
        # Auto-update run lock. Held for the life of a process-bound run so an
        # upgrade cannot replace the installed tree mid-experiment; see
        # probe._shared.run_lock. None for detached runs, which use a lease instead.
        self._run_lock = None
        self._run_lock_leased = False
        # Auto-step counters, per metric kind. Guarded because logging from
        # several threads is ordinary (a sampler beside a training loop), and two
        # threads reading the same counter would put two points on one step.
        self._steps: dict[str, int] = {}
        self._steps_lock = threading.Lock()
        # Plan (d): (reason, key) pairs `log` already warned about while
        # flattening a nested dict -- once per key per run, not once per step.
        self._flatten_warned: set[tuple[str, str]] = set()
        # ...and the distinct keys nested dicts have minted on this run, against
        # `_NESTED_KEY_BUDGET` (#2009 review).
        self._nested_keys: set[str] = set()
        # Plan (f): rows `log(commit=False)` is holding, one per metric kind, and
        # the attributes recently sent per step (the server replaces a step
        # record whole, so a repeat write sends the union). One lock for both.
        self._pending_rows: dict[str, _PendingRow] = {}
        self._step_records_sent: dict[int, tuple[str | None, dict[str, Any]]] = {}
        self._pending_lock = threading.Lock()
        self._commit_after_finish_warned = False
        # Plan (c): config keys `update_config` already warned about changing,
        # and whether it already said the server cannot merge config.
        self._config_warned: set[str] = set()
        self._config_merge_refused = False
        # Writer-session identity (research-os#364): one id per handle, so the
        # engine can tell which process produced a write once a run has been
        # reopened. A reattached handle gets the id its reopen registered.
        self.session_id: str = str(uuid4())
        # Writer epoch (0185): the generation this handle writes under — 1 for
        # the original execution, bumped by the server on every reopen. Rides
        # on every telemetry write so a superseded process is refused at the
        # door instead of splicing into the successor's curve. Taken from the
        # row a create/read/reopen returned (RunDetailOut always carries it);
        # attach_run overrides from its receipt or PROBE_RUN_EPOCH.
        #
        # None when nothing SUPPLIED it (SDK reliability 1.10): the CLI's
        # offline handle is `Run(client, {"id": ref})`, and defaulting that to
        # 1 fenced every `probe --async log` on a reopened run (409, dead
        # letter). An unknown epoch is sent as no epoch, the fence's fail-open.
        raw_epoch = (data or {}).get("write_epoch")
        self.write_epoch: int | None = int(raw_epoch) if raw_epoch is not None else None
        # 0205. Do this handle's beats come from INSIDE the work? `_wrap_run`
        # sets it; a launcher's handle leaves it False. Under a wrapped run the
        # launcher and the job both beat as owners, and this is the only thing
        # that distinguishes "the run is held open" from "the job is reporting".
        self.attached: bool = False
        # Armed by attach_run() after a reopen: the last step the previous
        # execution wrote. Explicit steps at or below it are refused, and
        # auto-steps start above it.
        self._resume_from_step: int | None = None
        self._auto_step_floor = 0
        # D17: what this run produces, captured when it ends. Set by
        # `_start_capture` (Client.run / probe.init) or `execute`.
        self._capture: _outputs.OutputCapture | None = None
        # Plan (n): `ignore=` patterns from Client.run / probe.init, added to the
        # `.probeignore` file and PROBE_IGNORE; rules loaded once per directory.
        self._ignore_patterns: tuple[str, ...] = ()
        self._ignore_cache: dict[str, Any] = {}
        # The rules for the directory `execute` ran its child in, for the
        # child's reads (collected after it exits).
        self._child_ignore: Any = None
        # Reasons already warned about for an upload that ended as a pointer
        # row (`_warn_not_uploaded`): a checkpoint saved every N steps must
        # not print the same line N times.
        self._uploads_warned: set[str] = set()
        # Cleared by `fluent.init` for a non-zero rank attached to a shared run
        # (interim until per-writer leases, plan 2.8), and by `fluent`'s exit
        # hook when a finalizing launcher holds the real exit code: such a
        # handle delivers its data but sends no terminal status.
        self._sends_terminal_status: bool = True
        # The terminal status this handle has sent (written, or journaled to
        # land), or None. The exit hook reads it so it never closes a run the
        # script already closed.
        self._closed_status: str | None = None
        # 2.2: the process that opened this handle. A write from any OTHER pid
        # is a forked child carrying the run on (a daemonizing script), which
        # the output helper must not report dead when the opener exits.
        self._opened_pid = os.getpid()
        self._forked_writer_marked: int | None = None
        # SDK reliability 2.8. The writer lease this handle beats and closes
        # under (`Client._wrap_run` sets it), None for the run-level heartbeat;
        # the protocol the server last said the run is on ('leases', or
        # 'legacy' once a writer that does not speak leases joined); and the
        # progress counter its lease beats carry.
        self._lease: dict | None = None
        self._lease_protocol: str | None = None
        #: Whether the server is known to hold this lease (a create or reopen
        #: that carried it, or a beat that landed). A release of a lease the
        #: server never saw would close nothing.
        self._lease_registered = False
        self._progress = _Progress()
        # (status, exception) an integration reported through
        # `fluent.note_exit` for an ending no process hook sees (Lightning's
        # SIGTERMException: a code-less SystemExit). `__exit__` prefers it to
        # that SystemExit's "code None means success".
        self._noted_exit: tuple[str, BaseException | None] | None = None
        # What `finish()` returned; `_UNSET` until it is called. See `finish`.
        self._finish_result: Any = _UNSET
        # Writes the client had already DROPPED (outbox full, unwritable) when
        # this handle was made; finish() reports the ones dropped since (plan
        # 0.1). Per client, not per run: a client hosting two runs at once
        # reports its drops on whichever closes -- an over-report, never a
        # silent one.
        self._dropped_baseline = int(getattr(client, "dropped_writes", 0) or 0)
        # Likewise the writes sent straight to the server below the outbox's
        # free-space floor (plan 1.5): not lost, but not durable either.
        self._direct_baseline = int(getattr(client, "direct_sends", 0) or 0)
        # Set by `fluent` for a run whose closer is not the caller's choice (a
        # reinit closing the previous run): the status queued when Ctrl-C or a
        # SystemExit cuts the close short, instead of the one asked for.
        self._status_on_interrupt: str | None = None
        # The status of a terminal write already on its way (see `_close`).
        self._terminal_in_flight: str | None = None
        # Called once a close has settled (`fluent` releases the client it
        # built for a `create_new` run, which only its handle can close).
        self._after_finish: Callable[[], None] | None = None

    def _finish_called(self) -> bool:
        """Whether `finish()` has run on this handle, or is running now."""
        return getattr(self, "_finish_result", _UNSET) is not _UNSET

    def _hold_run_lock(self, *, process_bound: bool) -> None:
        """Claim this box against an auto-update while the run is open.

        Two tiers, and which one applies is decided by whether a process of ours
        outlives this call. A process-bound run takes an flock the kernel
        releases on death -- including SIGKILL and OOM-kill -- so a crashed run
        can never wedge auto-update. A detached run has nothing alive to hold
        anything, so it gets a lease that its own subsequent writes renew.

        Never raises and never blocks. Failing to take the lock leaves the run
        unprotected, which is bad; failing to START the run because the lock
        could not be taken would be worse.
        """
        try:
            from probe._shared import run_lock
        except Exception:  # noqa: BLE001 -- SDK must not hard-depend on the CLI package
            return
        try:
            if process_bound:
                self._run_lock = run_lock.acquire(self.id)
            else:
                run_lock.touch_lease(self.id)
                self._run_lock_leased = True
        except Exception:  # noqa: BLE001 -- see docstring
            pass

    def _release_run_lock(self) -> None:
        """Drop the claim. Idempotent, never raises."""
        try:
            if self._run_lock is not None:
                self._run_lock.release()
                self._run_lock = None
            if self._run_lock_leased:
                from probe._shared import run_lock

                run_lock.clear_lease(self.id)
                self._run_lock_leased = False
        except Exception:  # noqa: BLE001
            pass

    def _stamp_writer(self, body: dict) -> dict:
        """Ride the writer fingerprint on a telemetry body (0185).

        A pre-0185 server ignores both fields (Pydantic drops undeclared body
        keys), so stamping is unconditionally safe; a 0185+ server uses them to
        refuse a superseded writer at the door. An epoch this handle does not
        know is omitted, never guessed (see ``write_epoch``)."""
        body["session_id"] = self.session_id
        if self.write_epoch is not None:
            body["write_epoch"] = self.write_epoch
        return body

    def _next_step(self, kind: str) -> int:
        with self._steps_lock:
            # The hardware rail never consults the resume floor: its steps
            # are epoch-derived, not counted, and stay invisible to the
            # training rails' resume machinery.
            floor = 0 if kind == "hardware" else self._auto_step_floor
            step = self._steps.get(kind, floor)
            self._steps[kind] = step + 1
            return step

    def arm_resume_guard(self, last_step: int) -> None:
        """Called on attach after a reopen: refuse explicit steps the first
        execution already wrote, and start auto-steps above them — a resumed
        process must continue the curve, never re-log it."""
        self._resume_from_step = last_step
        with self._steps_lock:
            self._auto_step_floor = last_step + 1

    #: Plan 2.4 (D6): calls dropped below the resume point, and what the
    #: warning, the resume line and the `resume_guard` span report. Class
    #: defaults, so a handle that never resumes carries nothing.
    _resume_drops = 0
    _resume_first_dropped: int | None = None
    _resume_last_dropped: int | None = None
    _resume_first_drop_at: str | None = None
    _resume_announced = False
    _resume_resumed_at: int | None = None
    #: True when the guard was armed by an attach that reopened the run
    #: (PROBE_RUN_ID): `probe.init()` there takes no `on_conflict`, so the drop
    #: message names the exits that work from an attach (`_resume_exits`).
    _resume_via_attach = False

    def _resume_exits(self, step: int) -> tuple[str, str, str]:
        """(overwrite, start over, keep both): what each intent does from HERE.

        A job that rejoined its run through ``PROBE_RUN_ID`` cannot use
        ``on_conflict`` (`probe.init()` joining a run takes none, and ignores
        ``"supersede"``), and `probe run start --rewind-to-step` is deprecated
        (#1551) and refuses a run with no external id. So its exits are the
        ones that work there (#2044 review)."""
        if not self._resume_via_attach:
            return (
                f"relaunch with on_conflict=probe.Rewind(step={step})",
                'on_conflict="supersede" (a fresh retry run)',
                "client.fork_run(...) from the checkpoint step",
            )
        ref = self._data.get("slug") or self.id
        # `probe exec` files a new run in the ACTIVE project unless told: the
        # retry belongs beside the run it retries (#2044 verify).
        project = f" --project id:{self.project_id}" if self.project_id else ""
        external = self._data.get("external_id")
        overwrite = (
            f"relaunch the job WITHOUT PROBE_RUN_ID, with probe.init(external_id={external!r}, "
            f"on_conflict=probe.Rewind(step={step}))"
            if external
            else "not possible for this run (it has no external id, and a rewind needs one)"
        )
        return (
            overwrite,
            f"a new run: `probe exec{project} --parent {ref} --relation retry -- <command>`",
            f"`probe run fork {ref} --step {step}` (or client.fork_run(...)), then run the job "
            "under the fork",
        )

    def _drop_below_resume(self, step, *, strict: bool | None) -> None:
        """A write at or below the resume point: dropped, with one warning (D6).

        The first execution already wrote these steps. A relaunch that restarted
        from an OLDER checkpoint re-logs them, and appending would splice two
        executions into one curve; raising (what this did) killed the relaunch
        at its first step instead. W&B drops the call and warns once; so does
        this. Nothing is sent or queued. ``strict`` still raises: a caller who
        asked for loud failure gets it.

        Counted in a keyed `diagnostic` span (`resume_guard`), not in run
        metadata, which a PATCH replaces whole. The span is written on the 1st,
        10th, 100th... drop and when logging climbs past the resume point, so
        its counts stay current in O(log n) writes."""
        resume_point = self._resume_from_step
        overwrite, start_over, keep_both = self._resume_exits(step)
        if strict or (strict is None and not self._client.fail_open):
            raise errors.ValidationError(
                f"step {step} <= resume point {resume_point} on a "
                "resumed run — the first execution already wrote this step. "
                "Three exits, by intent: restarted from an EARLIER checkpoint "
                f"and want the old range overwritten -> {overwrite}; "
                f"repeating from scratch -> {start_over}; "
                f"keeping both curves -> {keep_both}."
            )
        # NOT counted on client.dropped_writes: that counts writes the OUTBOX
        # lost, and finish() reports any rise as data loss (#2014). A resume
        # drop is the design working; the run's own `_resume_drops` counts it.
        with self._steps_lock:
            self._resume_drops += 1
            drops = self._resume_drops
            if drops == 1:
                self._resume_first_dropped = step
                self._resume_first_drop_at = _now()
            self._resume_last_dropped = step
        if drops == 1:
            _diagnostics.warn(
                f"probe: step {step} is at or below this resumed run's resume point "
                f"({resume_point}): the first execution already logged it, so this call "
                f"and every later one at or below step {resume_point} is DROPPED, not "
                f"sent. Logging continues above step {resume_point}. To overwrite that "
                f"range instead: {overwrite}; to keep both curves: {keep_both}."
            )
        if 10 ** (len(str(drops)) - 1) == drops:  # 1, 10, 100, ...
            self._write_resume_span()
        return None

    def _note_resumed(self, step: int) -> None:
        """The first write past the resume point after drops: one line, and the
        span's final counts."""
        with self._steps_lock:
            if self._resume_announced or step <= (self._resume_from_step or 0):
                return
            self._resume_announced = True
            self._resume_resumed_at = step
            drops = self._resume_drops
        _diagnostics.warn(
            f"probe: logging resumed at step {step} after dropping {drops} call(s) at "
            f"or below resume point {self._resume_from_step}."
        )
        self._write_resume_span()

    def _write_resume_span(self, *, closing: bool = False) -> None:
        """Upsert the keyed counter span. Never raises, never holds the close.

        One span per RANK (ranks resuming together would otherwise overwrite
        each other's counts), never under the caller's open span or unit: it
        belongs to the run, and the server sets a span's coordinate once."""
        rank = _global_rank()
        with self._steps_lock:
            # One consistent snapshot: log() on another thread may be adding a
            # drop while this writes (#2044 review).
            resumed = self._resume_resumed_at
            drops = self._resume_drops
            first_dropped = self._resume_first_dropped
            last_dropped = self._resume_last_dropped
            first_drop_at = self._resume_first_drop_at
        done = closing or resumed is not None
        try:
            with unit_context.detached():
                self.span(
                    "diagnostic",
                    external_key="resume_guard" if rank is None else f"resume_guard/rank-{rank}",
                    name="resume_guard",
                    parent_span_id=None,
                    status="completed" if done else "running",
                    started_at=first_drop_at,
                    ended_at=_now() if done else None,
                    attributes={
                        "resume_point": self._resume_from_step,
                        "dropped_calls": drops,
                        "first_dropped_step": first_dropped,
                        "last_dropped_step": last_dropped,
                        "resumed_at_step": resumed,
                        **({"rank": rank} if rank is not None else {}),
                    },
                    strict=False,
                    blocking=False,
                )
        except Exception:  # noqa: BLE001 -- a counter must never break a log() call
            pass

    def _close_resume_span(self) -> None:
        """At finish, whenever there were drops: the final counts and a closed
        status. The span is written only on the 1st, 10th, 100th... drop and
        on the resume, so a run that finishes inside its dropped range left it
        `running`, often with a stale count. Always written (one keyed,
        non-blocking upsert) rather than only when "something is missing": that
        bookkeeping raced with log() on other threads (#2044 review)."""
        with self._steps_lock:
            drops = self._resume_drops
        if drops:
            self._write_resume_span(closing=True)

    def _note_step(self, kind: str, step: int) -> None:
        """Move the auto counter past an explicitly-given step.

        Without this, mixing ``log(step=i)`` with a bare ``log()`` would restart
        the auto sequence at 0 and stack a second set of points on steps the loop
        already used."""
        with self._steps_lock:
            self._steps[kind] = max(self._steps.get(kind, 0), step + 1)

    # -- identity -----------------------------------------------------------
    @property
    def id(self) -> str:
        return str(self._data["id"])

    @property
    def experiment_id(self) -> str | None:
        """This run's experiment, or None for a PROJECT-DIRECT run (0054).

        Returns None rather than the string ``"None"``. It used to stringify
        unconditionally, and the only caller is :meth:`child` -- which therefore
        POSTed to ``/v1/experiments/None/runs`` on every project-direct run, the
        W&B-shaped half of the platform.
        """
        value = self._data.get("experiment_id")
        return None if value is None else str(value)

    @property
    def project_id(self) -> str | None:
        """This run's project. Present on every run since 0054; None on a row
        from a backend that predates it."""
        value = self._data.get("project_id")
        return None if value is None else str(value)

    @property
    def name(self) -> str:
        return str(self._data["name"])

    @property
    def description(self) -> str | None:
        return self._data.get("description")

    @property
    def repo(self) -> str | None:
        """Repository derived from the standalone README embed, if present."""
        return self._data.get("repo")

    @property
    def status(self) -> str:
        return str(self._data.get("status", "running"))

    @property
    def slug(self) -> str | None:
        """Human-readable petname (fold #21); present on /v1 reads (RunDetailOut)."""
        return self._data.get("slug")

    @property
    def foreign_keys(self) -> dict:
        """Incumbent-id map (fold #8); present on /v1 reads (RunDetailOut)."""
        return self._data.get("foreign_keys") or {}

    #: The execution record this handle's own `snapshot()` pinned. Kept apart
    #: from `_data` because under async writes the env_ref PATCH is still
    #: queued, so the row this handle holds does not show it yet.
    _pinned_env_ref: str | None = None

    @property
    def env_ref(self) -> str | None:
        """The execution record this handle believes the run is pinned to
        (fold #7): the hash its own `snapshot()` pinned LOCALLY, else the
        server row this handle last read. Not proof the server stored it --
        under async writes that PATCH may still be queued, or may yet fail;
        `probe run check` reads the server's answer. None when nothing is
        pinned.

        The hardware rail reads it to never mint an inventory record over a
        real snapshot's: its env_ref PATCH would queue FIFO behind the
        snapshot's, so without this it would always land last and win."""
        return self._pinned_env_ref or self._data.get("env_ref")

    @property
    def url(self) -> str | None:
        """This run's dashboard page, or None when the origin cannot be known.

        A property and not a print: a library that writes to stdout corrupts
        whatever the training script's own output is being parsed by. Scripts
        that want it visible say so themselves -- `print(run.url)` at the end of
        a job puts a clickable link in the cluster log, which is the one place a
        researcher is already looking when they want to know how it went.
        """
        from .links import entity_url

        return entity_url("run", self.id, api_base_url=self._client.settings.base_url)

    @property
    def data(self) -> dict:
        return self._data

    def refresh(self) -> "Run":
        self._data = self._client.get_run(self.id)
        return self

    def edges(self) -> list[dict]:
        """Lineage edges touching this run (fold #2): GET /v1/runs/{id}/edges."""
        return self._client.transport.get(f"/v1/runs/{self.id}/edges")

    # -- spine --------------------------------------------------------------
    def child(self, name: str | None = None, *, relation: str, **kw) -> "Run":
        """Open a run descended from this one. ``relation`` is REQUIRED.

        ``name`` is not: omitted, the server mints a petname and titles the run
        from its own content once it finishes, exactly like any other run. A
        name passed here is a person's and is never renamed.

        ``fork`` (branched off mid-flight), ``resume`` (continued after a stop),
        ``retry`` (another attempt at the same thing) or ``branch``. There is no
        default: the four mean different things, and a guessed one is stored as a
        claim someone reads later as a measurement. The server refuses the pair
        without it anyway (`RunCreate` 422, and `runs_parent_pair_chk`).

        For a run that CONSUMED this one's output rather than re-attempting it --
        an eval of its checkpoint, an SFT run over its rollouts -- none of the four
        is honest. That is a lineage edge, not parentage: ``probe edge add
        --relation consumes`` (or ``evaluates_on`` / ``derived_from``).

        The child inherits this run's attachment, which is why it branches: a
        project-direct parent begets a project-direct child, and a FLOATING
        parent (no project yet, daemon v2) a floating child. Passing
        ``self.experiment_id`` unconditionally is what used to POST to
        ``/v1/experiments/None/runs`` for every project-direct run.
        """
        if self.experiment_id is not None:
            return self._client.create_run(
                self.experiment_id,
                name,
                parent_run_id=self.id,
                parent_relation=relation,
                **kw,
            )
        if self.project_id is not None:
            return self._client.create_project_run(
                self.project_id,
                name,
                parent_run_id=self.id,
                parent_relation=relation,
                **kw,
            )
        if "project_id" in self._data:
            # FLOATING parent (daemon v2): the key is there and null, which a
            # pre-0054 row never is (it has no key at all). The child floats
            # too, carrying its parentage, and is filed with the family later.
            return self._client.create_floating_run(
                name,
                parent_run_id=self.id,
                parent_relation=relation,
                **kw,
            )
        raise errors.ValidationError(
            f"run {self.id} reports neither an experiment nor a project — this "
            "research-os backend predates project-direct runs (0054). Upgrade the "
            "backend, or open the child under an experiment."
        )

    # -- below-run coordinates ----------------------------------------------
    def unit(
        self,
        *,
        coords: dict[str, Any] | None = None,
        labels: dict[str, Any] | None = None,
    ) -> UnitContext:
        """Ambient coordinate context for everything logged inside the block::

            with run.unit(coords={"rank": 0}, labels={"sample": 3}):
                run.log({"loss": 0.42}, step=12)   # dimensions/labels merged in
                with run.unit(labels={"uid": "p1"}):
                    ...                            # nested: child = parent ∪ child

        ``coords`` are the bounded grouping axes (SERIES identity: rank/split/...,
        never a per-sample id and never the step axis — an ambient coord is applied
        to EVERY point in the block, so a per-sample one shreds the block into
        one-point series, see :meth:`log`); ``labels`` are unbounded per-sample
        drill-down ids (POINT identity only). Nested units merge with
        the child winning per key; a key may not end up in both maps
        (``ValueError``, mirroring the server's 422). The context is contextvar-
        scoped: thread- and asyncio-task-local, restored on exit, and folded into
        payloads at call time so spooled writes replay with the coordinate that
        was ambient when the value was produced."""
        return UnitContext(coords=coords, labels=labels, run_id=self.id)

    def context(self, **ids: Any) -> FailureContext:
        """Name what the block is processing, for crash reports ONLY::

            for epoch in range(epochs):
                for i, batch in enumerate(loader):
                    with run.context(batch_id=i, epoch=epoch):
                        train_step(batch)   # its run.log() calls are unchanged

        If the block raises, the run's crash report -- and the crash email --
        names the batch, sample or epoch it died on. Unlike :meth:`unit`,
        nothing is stamped onto what is logged inside: no dimensions, no
        labels, so every curve plots exactly as it would without the block.

        Keys: ``batch_id``, ``sample_id`` (also ``sample``/``example_id``/
        ``row_id``), ``task_id``, ``prompt_id``, ``epoch``, ``step``,
        ``split``, ``phase``, ``dataset``, ``model``. Values are ints or
        strings; any other value, and any other key, is dropped. Nested blocks
        merge with the inner one winning per key, and exit restores the outer
        state (thread- and asyncio-task-local). No I/O, never raises: cheap
        enough to enter once per batch."""
        return FailureContext(self.id, ids)

    # -- metrics ------------------------------------------------------------
    def log(
        self,
        metrics: dict[str, Any],
        *,
        step: int | None = _UNSET,
        kind: str = "model",
        wall_clock: str | None = None,
        dimensions: dict[str, Any] | None = None,
        labels: dict[str, Any] | None = None,
        span_id: str | None = None,
        agg: str | None = None,
        strict: bool | None = None,
        commit: bool | None = None,
    ):
        """Append metric points. Fail-open by default (spools on failure).

        DECIDE THE SHAPE BEFORE YOU CALL THIS. Series identity is
        ``(run,kind,key,dims_hash)``, so every distinct ``dimensions`` combination
        is a SEPARATE series — and a series holding one point has nothing to plot,
        so it renders as a scalar tile rather than a graph. Each metric is one of
        three shapes:

        * **curve** (loss, lr, reward over time) — one series, many points,
          distinguished by ``step``. ONLY ``step`` makes a curve; spreading values
          across a dimension does not.
        * **headline scalar** (final accuracy) — one series, one point, 0-2
          low-cardinality dims.
        * **breakdown** (accuracy by category) — one series per category value.

        Budget it at the write: series ≈ the PRODUCT of your dimension
        cardinalities. Past ~50 you have designed a wall of tiles. That failure is
        silent — every call succeeds, the values are correct, the data stays fully
        queryable, and the only symptom is an unreadable run page — so assert the
        count after the first run instead of eyeballing the dashboard::

            series = client.run_series(run.id)     # one row per series
            assert len(series) < 50, f"{len(series)} series — a wall of tiles"

        ``dimensions`` is a bounded flat label map (<=8 keys) of the LOW-CARDINALITY
        axes you actually intend to group by — split, seed, rank, difficulty,
        category. Never an identifier: ``example_id``, a row id, a uuid, a
        filename, a per-field name each mint their own one-point series (500
        examples logged with ``example_id`` as a dimension = 500 series = 500
        tiles and zero graphs). Per-sample identity goes in ``labels`` instead
        (<=32 keys, POINT identity only — it does NOT widen the series), and
        per-item detail belongs in an artifact, which is where analysis code reads
        it from anyway. Metrics are for what a human should see; artifacts are for
        what code reads. ``span_id`` is an optional exemplar pointer to the span
        the value was produced under. Both maps merge over the ambient
        :meth:`unit` context (the explicit call site wins per key); a key in both
        maps raises ``ValueError``. Dimension-less points stay byte-identical.
        Built through the generated ``MetricBatch``/``MetricPointIn``, so schema
        drift fails here, not as a server 422.

        The headline number must be exactly ONE series: a computed view resolves a
        key and REFUSES one carrying several dimension variants ("series X has N
        dimension variants"). So never log a headline scalar and a per-item cloud
        under the same key — use two (``accuracy`` and ``accuracy_per_example``),
        and put the high-cardinality one under its own ``kind`` so the run page
        shows the handful of numbers that matter while the detail stays queryable.

        ``agg`` DECLARES the key's reduce fn (mean|sum|min|max|count) so a later
        grouped read can omit its own (server 0062: an omitted read-side ``agg``
        resolves to the declared one, else mean; conflicting declarations 422).
        The producer knows whether a count sums or a loss averages; declaring it
        at the write is what saves every reader from guessing.

        ``wall_clock`` defaults to the time of THIS call (strictly increasing
        within the process), so a point the outbox holds through an outage
        keeps the time it was logged; pass it only for an event that happened
        earlier. ``log_derived*`` sends none, and the server then stamps arrival.

        Nested dicts flatten to ``/`` keys, the separator the run page sections
        panels by: ``log({"eval": {"acc": 0.9, "note": "ok"}})`` writes the point
        ``eval/acc`` and puts ``eval/note`` in the step record, all at ONE step.
        Any ``Mapping`` flattens (an OmegaConf ``DictConfig`` too); lists do not,
        and an empty mapping writes nothing. An explicit ``"a/b"`` beside a nested
        ``{"a": {"b": ...}}`` wins, with a warning once per key per run. A mapping
        nested past 16 levels, or one that contains itself, stays one step
        attribute. ``dimensions`` and ``labels`` are never flattened (they must
        stay flat maps). W&B's own history uses ``.`` for nesting, so a run
        brought in with ``probe import wandb`` keeps ``a.b`` keys: a different
        series from ``a/b``.

        ``commit`` (W&B's spelling): ``commit=False`` holds this call's values in
        a pending row for its step instead of writing them. The next call
        without ``commit=False`` at the same step, or with ``step`` omitted,
        merges into that row and writes it once (last value per key wins); a
        call at a different step writes the pending row first. ``finish()`` --
        and so the ``with`` block and the exit hook -- writes a row still
        pending; a crash before that loses it, as in W&B. Pending rows are per
        ``kind``. One difference from W&B: a bare ``log()`` after
        ``log(step=5)`` lands at 6 here (W&B: 5), because an explicit step
        always moves the counter past itself.

        Non-numeric values logged twice at one step keep the first call's keys
        too (new wins per key): the server replaces a step record whole, so the
        SDK sends the union for the steps it wrote recently."""
        # A SIGTERM handler installed since `probe.init` that runs ours only
        # after its own (Lightning's) gets ours put first (`preempt.run_first`).
        _preempt.run_first()
        # Resume guard (research-os#364): a resumed run continues its curve. A
        # step at or below the resume point means the process restarted from
        # scratch — that is a RETRY, and appending it here would splice two
        # executions into one series. The HARDWARE rail is exempt in both
        # directions: its steps are epoch-derived (a different clock), so
        # they neither clear nor trip a training-step floor.
        if (
            kind != "hardware"
            and self._resume_from_step is not None
            and step is not _UNSET
            and step is not None
            and step <= self._resume_from_step
        ):
            return self._drop_below_resume(step, strict=strict)
        # Plan (d): nested dicts flatten to `/` keys. Only when a value IS a
        # Mapping, so a flat call never pays for it and its body stays
        # byte-identical to what it has always been.
        # A DictConfig always takes the flattening path: even `.values()`
        # resolves its interpolations (and raises on a `???`), and the
        # flattening path reads it without resolving secrets.
        if _is_omegaconf(metrics) or any(isinstance(value, Mapping) for value in metrics.values()):
            metrics = self._flatten_metrics(metrics)
        numeric: dict[str, float] = {}
        other: dict[str, Any] = {}
        for key, value in metrics.items():
            as_number = _as_metric_value(value)
            if as_number is None:
                other[key] = _json_safe(key, value)
            else:
                numeric[key] = as_number

        # Plan (f): `commit=False`, or a row already pending for this kind, takes
        # the buffered path. An ordinary call never does, so its bodies are
        # byte-identical to what they have always been.
        if commit is False or kind in self._pending_rows:
            return self._log_pending(
                kind, step, numeric, other, dimensions, labels, span_id, agg,
                wall_clock, strict, commit,
            )

        # Split BEFORE drawing a step, so a call with nothing to write does not
        # consume one. `if metrics: run.log(metrics)` guards get written the
        # other way round, and burning an index there would drift the auto axis
        # away from the loop index — the exact failure auto-increment prevents.
        if not numeric and not other:
            return None

        if step is _UNSET:
            step = self._next_step(kind)
        elif step is not None:
            step = int(step)
            self._note_step(kind, step)
        if self._resume_drops and kind != "hardware" and step is not None:
            self._note_resumed(step)

        dims, labs = unit_context.merged(dimensions, labels)
        if numeric and wall_clock is None:
            # Plan 1.4: date the points when the loop LOGGED them. Omitted, the
            # server stores COALESCE(wall_clock, now()) -- its receive time -- so
            # a point the journal held through an outage landed up to minutes
            # late and findings (which bin by point wall_clock) saw a gap, then a
            # burst. Stamped here, the time is frozen into the journaled body and
            # survives any delayed drain. Not in `log_derived*`: a backfill's
            # call time is not when anything was measured.
            wall_clock = _log_stamp()
        points = [(key, value, dims, labs, span_id, agg) for key, value in numeric.items()]
        return self._write_row(kind, step, points, other, wall_clock, strict, stacklevel=3)

    def _write_row(
        self,
        kind: str,
        step: int | None,
        points: list[tuple],
        other: dict[str, Any],
        wall_clock: str | None,
        strict: bool | None,
        *,
        stacklevel: int,
    ):
        """Write one step's row: every numeric point in ONE metrics POST, the
        rest as the step record. ``points`` are ``(key, value, dimensions,
        labels, span_id, agg)``; ``stacklevel`` makes a warning name the
        caller's ``log()`` line, however deep this was reached from. Warnings
        go through ``_diagnostics.warn``: this also runs inside ``finish()``,
        where a warning raised by ``-W error`` would read as a lost row."""
        if os.getpid() != self._opened_pid:
            self._note_forked_writer()
        if kind != "hardware":
            self._progress.bump()  # 2.8: one user row is one unit of progress
        result = None
        # What the server cannot store, dropped here with a warning rather than
        # queued: it answered a step past int64 or a key past its index row
        # size with a 500, which the outbox retries for 24 h and which held
        # the run's later writes behind it (review of #2053).
        if step is not None and not (_STEP_MIN <= step <= _STEP_MAX):
            if not getattr(self, "_step_range_warned", False):
                self._step_range_warned = True
                _diagnostics.warn(
                    f"probe: dropped the metrics of step {step}: a step must fit in a "
                    "64-bit signed integer. Later steps out of range are dropped "
                    "silently.",
                    stacklevel=stacklevel,
                )
            return None
        kept = [point for point in points if not _key_too_long(point[0])]
        if len(kept) != len(points):
            warned = self.__dict__.setdefault("_long_keys_warned", set())
            for point in points:
                key = point[0]
                if _key_too_long(key) and key not in warned:
                    warned.add(key)
                    _diagnostics.warn(
                        f"probe: dropped metric {key[:60]!r}...: a key may be at most "
                        f"{MAX_METRIC_KEY_BYTES} bytes ({len(key.encode('utf-8', 'surrogatepass'))} given).",
                        stacklevel=stacklevel,
                    )
            points = kept
            if not points and not other:
                return None
        if points:
            body = _metric_batch_body(
                [
                    MetricPointIn(
                        key=key,
                        kind=kind,
                        value=value,
                        step_index=step,
                        wall_clock=wall_clock,
                        dimensions=dims,
                        labels=labs or None,
                        span_id=span_id,
                        agg=agg,
                    )
                    for key, value, dims, labs, span_id, agg in points
                ]
            )
            # Returned even when a step record is also written: callers key off
            # this to tell "confirmed" from "spooled" (connectors/harbor.py).
            result = self._client.write(
                "POST", f"/v1/runs/{self.id}/metrics", self._stamp_writer(body), strict=strict
            )

        if other:
            if step is None:
                _diagnostics.warn(
                    f"dropped non-numeric {sorted(other)} — a step record needs a step "
                    "index, and step=None was passed explicitly to mean no step axis. "
                    "Omit step= to auto-increment, or pass one.",
                    stacklevel=stacklevel,
                )
            elif kind != "model":
                # StepCreate has no `kind` — a step record is keyed on
                # (run, step_index) alone. So a hardware value at hardware-step 3
                # would merge into the model loop's record at step 3. Numeric
                # hardware metrics are unaffected: those are metric points, where
                # kind IS part of the series identity.
                _diagnostics.warn(
                    f"dropped non-numeric {sorted(other)} from a {kind!r} log — step "
                    "records are keyed by step index alone, with no kind, so these "
                    "would overwrite the model loop's record at the same step.",
                    stacklevel=stacklevel,
                )
            else:
                name, attributes = self._union_step_record(step, other)
                step_result = self.step(step, name=name, attributes=attributes, strict=strict)
                # Only stand in when there was NOTHING numeric to write. A
                # successful step record must never mask a metrics write that
                # spooled: harbor.py reads None as "spooled".
                if not points:
                    result = step_result
        return result

    def _union_step_record(
        self, step: int, other: dict[str, Any]
    ) -> tuple[str | None, dict[str, Any]]:
        """``(name, other plus the attributes)`` this handle already sent to
        ``step``'s record, by :meth:`log` or :meth:`step`.

        The server REPLACES a step record's name and attributes on upsert
        (``app/telemetry/spans_router.py``), so ``log({"phase": "eval"},
        step=3)`` then ``log({"note": "x"}, step=3)`` used to leave only
        ``note``, and a ``step(3, name="warmup")`` lost its name to the next
        ``log(..., step=3)``. :meth:`step` remembers what it sent for the last
        ``_STEP_ATTRIBUTES_REMEMBERED`` steps, so memory stays flat over a long
        run. A first write to a step sends ``other`` unchanged. Never waits
        long on the lock (a signal handler may hold it): without it, no union."""
        if not self._pending_lock.acquire(timeout=_CLOSE_LOCK_WAIT_SECONDS):
            return None, other
        try:
            name, sent = self._step_records_sent.get(step, (None, {}))
        finally:
            self._pending_lock.release()
        return name, {**sent, **other}

    def _remember_step_record(self, step: int, name: str | None, attributes: Any) -> None:
        if not isinstance(attributes, dict):
            attributes = {}
        if not self._pending_lock.acquire(timeout=_CLOSE_LOCK_WAIT_SECONDS):
            return
        try:
            sent = self._step_records_sent
            sent.pop(step, None)
            sent[step] = (name, dict(attributes))
            if len(sent) > _STEP_ATTRIBUTES_REMEMBERED:
                del sent[next(iter(sent))]
        finally:
            self._pending_lock.release()

    def _log_pending(
        self,
        kind: str,
        step: Any,
        numeric: dict[str, float],
        other: dict[str, Any],
        dimensions: dict[str, Any] | None,
        labels: dict[str, Any] | None,
        span_id: str | None,
        agg: str | None,
        wall_clock: str | None,
        strict: bool | None,
        commit: bool | None,
    ):
        """Plan (f)'s buffered path; the rules are in :meth:`log`'s docstring.

        A pending row with an omitted step PEEKS the auto counter rather than
        drawing from it, so ``commit=False`` never advances the axis; the row
        claims its step when it is written. The network I/O runs outside the
        lock.

        A signal handler's ``log()`` runs on the thread it interrupted, so if
        that thread was inside the locked block below, the lock is never
        released. Past a short wait this call is then written at once, as an
        ordinary write, instead of hanging. This call holds and flushes
        nothing; the row the interrupted call was building stays pending."""
        dims, labs = unit_context.merged(dimensions, labels)
        stamp = wall_clock if wall_clock is not None else _log_stamp()
        if commit is False:
            # Validate NOW (#2025 review): a bad point surfacing at the next,
            # innocent call would lose both that call and this row.
            for key, value in numeric.items():
                MetricPointIn(
                    key=key, kind=kind, value=value, wall_clock=stamp, dimensions=dims,
                    labels=labs or None, span_id=span_id, agg=agg,
                )
            if self._closed_status is not None and not self._commit_after_finish_warned:
                self._commit_after_finish_warned = True
                _diagnostics.warn(
                    "probe.log(commit=False) after finish(): this row is held until the "
                    "next log() call on this run, and finish() will not send it.",
                    stacklevel=3,
                )
        flush: _PendingRow | None = None
        row: _PendingRow | None = None
        if self._pending_lock.acquire(timeout=_CLOSE_LOCK_WAIT_SECONDS):
            try:
                row = self._pending_rows.get(kind)
                if step is _UNSET:
                    target = row.step if row is not None else self._peek_step(kind)
                else:
                    target = None if step is None else int(step)
                if row is not None and row.step != target:
                    flush, row = self._pending_rows.pop(kind), None
                if commit is False:
                    if numeric or other:
                        if row is None:
                            row = self._pending_rows[kind] = _PendingRow(target)
                        row.merge(numeric, other, dims, labs, span_id, agg, stamp)
                    row = None
                elif row is not None:
                    del self._pending_rows[kind]
                    row.merge(numeric, other, dims, labs, span_id, agg, stamp)
            finally:
                self._pending_lock.release()
            if flush is not None:
                self._flush_row(kind, flush)
            if commit is False:
                return None
        else:
            # Held by the log() this call interrupted (see docstring).
            target = self._peek_step(kind) if step is _UNSET else (None if step is None else int(step))
        if row is None:
            # Nothing was pending at this call's step (a row at another step was
            # just flushed): this call is an ordinary write.
            if not numeric and not other:
                return None
            row = _PendingRow(target)
            row.merge(numeric, other, dims, labs, span_id, agg, stamp)
        self._claim_step(kind, row.step)
        return self._write_row(
            kind, row.step, row.point_list(), row.other, row.wall_clock, strict, stacklevel=4
        )

    def _peek_step(self, kind: str) -> int:
        """The step the next omitted-step call would draw, without drawing it."""
        with self._steps_lock:
            floor = 0 if kind == "hardware" else self._auto_step_floor
            return self._steps.get(kind, floor)

    def _claim_step(self, kind: str, step: int | None) -> None:
        """Move the counter past a pending row's step as it is written, and
        tell plan 2.4's resume guard, exactly as the ordinary path in
        :meth:`log` does."""
        if step is not None:
            self._note_step(kind, step)
            if self._resume_drops and kind != "hardware":
                self._note_resumed(step)

    def _flush_row(self, kind: str, row: "_PendingRow") -> None:
        """Write a pending row fail-open, and never raise: this runs inside a
        later ``log()`` or inside ``finish()``, and a row the caller already let
        go of must not fail either. ``strict=False`` journals it on a transport
        failure (even on a ``fail_open=False`` client) so the close barrier
        delivers it."""
        try:
            self._claim_step(kind, row.step)
            # 5 frames: _write_row <- here <- _log_pending/_flush_pending_rows
            # <- log/finish <- the caller's line.
            self._write_row(
                kind, row.step, row.point_list(), row.other, row.wall_clock, False, stacklevel=5
            )
        except Exception as exc:  # noqa: BLE001 -- see docstring
            _diagnostics.warn(
                f"probe.log: could not write the commit=False row for step {row.step} "
                f"({type(exc).__name__}: {_diagnostics.describe(exc)}); it was dropped.",
                stacklevel=4,
            )

    def _flush_pending_rows(self) -> None:
        """Write every row ``log(commit=False)`` still holds. Called first thing
        in ``finish()``, which every close funnels through (``__exit__``, the
        exit hook). Never raises."""
        if not self._pending_rows:
            return
        # A signal handler calling finish() runs on the thread it interrupted.
        # If that thread was inside log(), it holds one of these locks and never
        # will release it: give up on the held rows rather than hang (#2025
        # review). `_steps_lock` first, so rows are only taken once both are free.
        if not self._steps_lock.acquire(timeout=_CLOSE_LOCK_WAIT_SECONDS):
            self._warn_rows_not_flushed()
            return
        self._steps_lock.release()
        if not self._pending_lock.acquire(timeout=_CLOSE_LOCK_WAIT_SECONDS):
            self._warn_rows_not_flushed()
            return
        try:
            rows = list(self._pending_rows.items())
            self._pending_rows.clear()
        finally:
            self._pending_lock.release()
        for kind, row in rows:
            self._flush_row(kind, row)

    def _warn_rows_not_flushed(self) -> None:
        _diagnostics.warn(
            "probe: finish() could not flush the log(commit=False) row(s): a log() call "
            "was interrupted mid-write (finish() called from a signal handler?), so they "
            "were not sent. Everything logged without commit=False is unaffected.",
            stacklevel=4,
        )

    def _flatten_metrics(self, metrics: Mapping[Any, Any]) -> dict[str, Any]:
        """``_flatten`` plus its warnings, each once per key per run: a loop logs
        the same structure every step, and a warning per step is noise.
        ``_diagnostics.warn`` because a plain warning raises under ``-W error``."""
        flat, collided, kept_whole = _flatten(metrics, known=self._nested_keys)
        for key, _top in collided:
            self._warn_flatten_once(
                ("collided", str(key)),
                f"probe.log: {key!r} was given twice, as an explicit key and through "
                "a nested dict; kept the explicit (least nested) one. Warned once per "
                "key per run.",
            )
        for key, reason, top in kept_whole:
            # Once per reason per TOP-LEVEL key: a dict keyed by data would
            # otherwise warn once per id.
            self._warn_flatten_once(
                (reason, top),
                f"probe.log: {key!r} was not flattened ({_KEPT_WHOLE_REASONS[reason]}); "
                f"recorded whole in the step record. Warned once per reason under {top!r} "
                "per run.",
            )
        return flat

    def _warn_flatten_once(self, token: tuple[str, str], message: str) -> None:
        """One warning per ``token`` per run, from a set bounded at
        ``_FLATTEN_WARNINGS_REMEMBERED``: past it, flattening goes quiet rather
        than growing without bound on a pathological structure."""
        warned = self._flatten_warned
        if token in warned or len(warned) >= _FLATTEN_WARNINGS_REMEMBERED:
            return
        warned.add(token)
        # 4 frames: warn <- here <- _flatten_metrics <- log <- the caller's line.
        _diagnostics.warn(message, stacklevel=4)

    # -- derived metrics (computed after the fact, research-os 0087) --------
    def log_derived(
        self,
        metrics: dict[str, float],
        *,
        step: int,
        producer: str,
        note: str | None = None,
        inputs: list[Any] | None = None,
        code_ref: str | None = None,
        kind: str = "model",
        wall_clock: str | None = None,
        dimensions: dict[str, Any] | None = None,
        agg: str | None = None,
        strict: bool | None = None,
    ):
        """Write metrics that were COMPUTED after the fact, not measured live.

        The door for an agent backfilling a metric nobody logged at training
        time — AUROC from stored predictions, a cumulative integral of reward, a
        rescored eval. It works on a **completed** run: the series catalog is a
        row store, so a finished run is not a sealed archive.

        ``producer`` is required and is the point — a derived series carries
        ``origin="derived"`` plus provenance saying what produced it, so nobody
        ever has to wonder whether a curve came from the training loop or from a
        notebook two weeks later. The server stamps ``computed_at`` and
        ``created_by`` on top; a client cannot forge either.

        ``step`` is required, unlike :meth:`log`. Auto-increment is a footgun
        here: a backfill lands on steps that already exist, and a counter
        starting at 0 on a fresh handle would silently write the wrong axis.

        ``inputs`` is best-effort lineage — which stored series the computation
        read. Pass metric keys as strings (resolved against ``kind``) or full
        selector dicts. Use :meth:`log_derived_series` to push a whole curve in
        one request rather than one call per step.

        A derived key that collides with an existing LOGGED series is refused
        for that series alone: the ingest door skips it, reports it loudly, and
        writes the rest of the batch. Origin is fixed at a series' first write.

        ``metrics`` must be flat: unlike :meth:`log`, nested dicts are NOT
        flattened here (every value must be a number).
        """
        numeric = {k: float(v) for k, v in metrics.items()}
        if not numeric:
            return None
        points = [
            MetricPointIn(
                key=key,
                kind=kind,
                value=value,
                step_index=int(step),
                wall_clock=wall_clock,
                dimensions=dimensions,
                agg=agg,
            )
            for key, value in numeric.items()
        ]
        body = _metric_batch_body(
            points,
            provenance=_derived_provenance(
                producer=producer, note=note, inputs=inputs, code_ref=code_ref, kind=kind
            ),
        )
        return self._client.write(
            "POST", f"/v1/runs/{self.id}/metrics", self._stamp_writer(body), strict=strict
        )

    def log_derived_series(
        self,
        key: str,
        points: Any,
        *,
        producer: str,
        note: str | None = None,
        inputs: list[Any] | None = None,
        code_ref: str | None = None,
        kind: str = "model",
        dimensions: dict[str, Any] | None = None,
        agg: str | None = None,
        strict: bool | None = None,
    ):
        """Push a whole derived CURVE in one request — the usual backfill shape.

        ``points`` is either a ``{step: value}`` mapping or an iterable of
        ``(step, value)`` pairs. One batch, one request: a 3000-step backfill
        through :meth:`log_derived` would be 3000 round trips, which is the
        difference between tooling and a demo.

        Provenance arguments mean exactly what they do on :meth:`log_derived`.
        """
        pairs = points.items() if hasattr(points, "items") else points
        rows = [
            MetricPointIn(
                key=key,
                kind=kind,
                value=float(value),
                step_index=int(step),
                dimensions=dimensions,
                agg=agg,
            )
            for step, value in pairs
        ]
        if not rows:
            return None
        body = _metric_batch_body(
            rows,
            provenance=_derived_provenance(
                producer=producer, note=note, inputs=inputs, code_ref=code_ref, kind=kind
            ),
        )
        return self._client.write(
            "POST", f"/v1/runs/{self.id}/metrics", self._stamp_writer(body), strict=strict
        )

    # -- expression views (read-time computed panels, research-os 0088) -----
    def views(self) -> list[dict]:
        """Every live expression view on this run."""
        return self._client.list_views(self.id)

    def create_view(self, name: str, spec: Any) -> dict:
        """Save an expression view — a formula over series this run already has,
        evaluated at read time. ``spec`` is a :class:`probe.expr.Expr`, a node
        dict, or a full ``{"expression": ...}`` mapping. See
        :meth:`Client.create_view`."""
        return self._client.create_view(self.id, name, spec)

    def view_data(self, view_id: str, **kw: Any) -> dict:
        """Evaluate a saved view; see :meth:`Client.view_data` for the envelope
        (``missing_inputs`` / ``dropped_nonfinite`` / ``truncated``)."""
        return self._client.view_data(self.id, view_id, **kw)

    def preview_view(self, spec: Any, **kw: Any) -> dict:
        """Evaluate a spec without saving it — the check to run before
        :meth:`create_view`."""
        return self._client.preview_view(self.id, spec, **kw)

    def log_hw(
        self,
        metrics: dict[str, Any],
        *,
        step: int | None = _UNSET,
        wall_clock: str | None = None,
        strict: bool | None = None,
        **dims: Any,
    ):
        """Log hardware metrics with real dimensions (host/rank/device, fold #9).

        ``run.log_hw({"gpu_temp": 88}, device=3, host="n1")`` sends
        ``dimensions={"device": 3, "host": "n1"}``, kind=hardware."""
        return self.log(
            metrics,
            step=step,
            kind="hardware",
            wall_clock=wall_clock,
            dimensions=dims or None,
            strict=strict,
        )

    # -- metrics / coordinates (read) ---------------------------------------
    def grouped_metrics(self, key: str, **kw: Any) -> dict:
        """Server-side reduce/group over this run's points; see
        :meth:`Client.get_metrics_grouped` for the parameters and paging."""
        return self._client.get_metrics_grouped(self.id, key, **kw)

    def wide_metrics(self, **kw: Any) -> dict:
        """Step x metric table for this run; see :meth:`Client.get_metrics_wide`."""
        return self._client.get_metrics_wide(self.id, **kw)

    def export_points(self, **kw: Any):
        """Lossless raw-point generator for this run; see
        :meth:`Client.export_metric_points`."""
        return self._client.export_metric_points(self.id, **kw)

    def coordinates(self) -> list[dict]:
        """This run's coordinate catalog (0060); see
        :meth:`Client.list_run_coordinates`."""
        return self._client.list_run_coordinates(self.id)

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

    def progress(self) -> None:
        """Say this process made progress (SDK reliability 2.8).

        Every non-hardware ``log()`` and ``step()`` already counts, and so do
        the Lightning and Hugging Face integrations' batch ends. Call this in
        a custom loop that logs rarely -- or inside a long phase that logs
        nothing, such as a checkpoint upload -- so the stall detector, which
        pages when a live process stops advancing, knows it is still moving.
        Cheap (a counter under a lock) and it never raises."""
        try:
            self._progress.bump()
        except Exception:  # noqa: BLE001 -- bookkeeping never touches the work
            pass

    # -- artifacts ----------------------------------------------------------
    def log_artifact(
        self,
        name: str,
        *,
        sync: bool | None = None,
        path: str | None = None,
        uri: str | None = None,
        kind: str | None = None,
        content_hash: str | None = None,
        content_type: str | None = None,
        size_bytes: int | None = None,
        is_reference: bool | None = None,
        reference: bool = False,
        hash_content: bool = False,
        allow_missing: bool = False,
        span_id: str | None = None,
        step_index: int | None = None,
        meta: dict | None = None,
        notes: str | None = None,
        coords: dict[str, Any] | None = None,
        labels: dict[str, Any] | None = None,
        strict: bool | None = None,
    ):
        """Record an artifact.

        ``coords``/``labels`` are the below-run coordinate maps (same split as
        :meth:`log`), merged over the ambient :meth:`unit` context and sent as
        top-level ``ArtifactCreate`` fields — the server hashes coords into the
        cross-table join key and mirrors both maps into ``meta`` for display, so
        the client never folds them into ``meta`` itself. The presign *uploads*
        door does not accept them (its request model has no such fields), so a
        byte upload records them only if it falls back to a reference artifact.

        With ``path`` and no ``uri`` and no ``reference``: the real presign upload flow
        (fold #16) runs, fingerprint -> presign -> PUT bytes to R2 -> confirm.

        With ``reference=True`` and a ``path``: a PATH reference is recorded -- the file's
        location is stored as a ``file://`` uri (raw path in ``meta.local_path``, recording
        host in ``meta.host``) and its bytes are NOT uploaded. Only ``os.stat`` runs unless
        ``hash_content`` asks for a fingerprint. This is the shared-volume case: a 16 GB
        checkpoint or a TB of files an agent on the same volume resolves locally. Raises
        ``FileNotFoundError`` if the path is missing unless ``allow_missing``.

        With ``uri`` (object already in a bucket) or no bytes: a metadata-only reference
        artifact is recorded, as before.

        ``kind`` left out is read from the file's extension (``artifact_kind_for``):
        an image is a ``plot``, anything else (a PDF included) a ``file``. A
        ``kind`` the caller passes always wins, ``"file"`` included."""
        self._progress.bump()  # 2.8: a checkpoint or output upload is work done
        # Before anything branches on it: every branch below stores `name`, and the
        # preview route reads its extension. `log_artifact("ckpt", path="ckpt-4000.pt")`
        # -- the shape the skill documents -- would otherwise store an extensionless
        # name for a file that has one. Restored from the path; additive only.
        from .redaction import default_scrub, scrub_text

        name = scrub_text(name_with_extension(name, path))
        if kind is None:
            kind = artifact_kind_for(name, path)
        notes = scrub_text(notes) if notes is not None else None
        meta = default_scrub(dict(meta or {}))
        # Lineage (server 0255): did THIS run write the file, or only log one it
        # read? Stamped from the file's mtime against the run's start, and
        # carried onto the version the upload becomes -- which is how a file the
        # run overwrote stays recognisable as its output. A caller's own value
        # wins.
        if path is not None:
            for key, value in self._write_marks(path).items():
                meta.setdefault(key, value)
        # Resolve the coordinate at CALL time (the fail-open spool replays this
        # payload later; the ambient unit must not be re-read at flush time).
        coords, labels = unit_context.merged(coords, labels)
        # Explicit path reference: record WHERE the bytes live (file://) instead of
        # uploading them. Takes precedence over the upload branch so path + reference
        # never force-uploads (the old code ignored is_reference for path+no-uri).
        if reference and path is not None:
            fields = reference_fields(
                path, hash_content=hash_content, allow_missing=allow_missing, size_bytes=size_bytes
            )
            self._note_logged(path, fields.get("content_hash"))
            uri = uri or fields["uri"]
            if content_hash is None:
                content_hash = fields.get("content_hash")
            if size_bytes is None:
                size_bytes = fields.get("size_bytes")
            for key, value in fields["meta"].items():
                meta.setdefault(key, value)
            is_reference = True
        elif path is not None and uri is None:
            # A REFUSAL by the credential gate -- over the 64 MiB inspection
            # limit, a credential in the path, the content, bytes that moved
            # while they were read -- is not the training loop's problem:
            # outside `strict` it becomes a warning and a reference row, like
            # any other upload that did not land (plan 0.7). A mistake in the
            # CALL (a missing path, a directory, a hash that does not match the
            # file) still raises: see `_require_upload_source`.
            strict_resolved = (not self._client.fail_open) if strict is None else strict

            def refused(reason: str, *, withhold_path: bool = False, missing: bool = False):
                return self._record_refused_upload(
                    name,
                    path,
                    reason,
                    withhold_path=withhold_path,
                    kind=kind,
                    content_type=content_type,
                    span_id=span_id,
                    step_index=step_index,
                    meta=meta,
                    notes=notes,
                    coords=coords,
                    labels=labels,
                    allow_missing=missing,
                    sync=sync,
                )

            try:
                # First, and before anything quotes the path.
                _check_upload_path(path)
            except CredentialInPath as exc:
                if strict_resolved:
                    raise
                return refused(str(exc), withhold_path=True)
            if not _require_upload_source(path, allow_missing=allow_missing):
                # Missing, and the caller said that is expected: the pointer is
                # what they asked for, so no `strict` raise either.
                return refused("no such file on this host", missing=True)
            if _multipart.over_threshold(path):
                # Plan item (g): over the 64 MiB inspection limit, a server
                # that takes multipart uploads gets the file in parts -- staged
                # now, sent by the outbox in the background. Otherwise (an old
                # server, an offline run) `check_upload` below refuses it and
                # 0.7's warning + reference row stands.
                handled = self._maybe_multipart(
                    name,
                    path,
                    kind=kind,
                    content_type=content_type,
                    span_id=span_id,
                    step_index=step_index,
                    meta=meta,
                    notes=notes,
                    strict=strict_resolved,
                    sync=sync,
                    refused=refused,
                )
                if handled is not _NOT_QUEUED:
                    self._note_logged(path)
                    return handled
            try:
                check_upload(path)
                queued = self._maybe_queue_upload(
                    name,
                    path,
                    kind=kind,
                    content_type=content_type,
                    span_id=span_id,
                    step_index=step_index,
                    meta=meta,
                    notes=notes,
                    strict=strict,
                    sync=sync,
                )
                if queued is not _NOT_QUEUED:
                    # After the queue took it, never before: a log_artifact that
                    # failed must not stop output capture from storing the file.
                    self._note_logged(path)
                    return queued
                # The queued branch above redacts when it stages its snapshot. This
                # is the synchronous branch, so redaction happens here instead --
                # before the fingerprint, which the server signs.
                with prepare_upload(path) as prepared:
                    digest, size = _fingerprint(prepared.path)
                    if not prepared.was_redacted and (
                        (content_hash is not None and content_hash.lower() != digest)
                        or (size_bytes is not None and size_bytes != size)
                    ):
                        # The caller's fingerprint is wrong. Left to the
                        # `@freeze_upload` check it reads as "source changed"
                        # -- a refusal, so a pointer row and a warning -- for
                        # what is a bug in the call.
                        raise ValueError(
                            f"log_artifact({name!r}): the content_hash/size_bytes passed do "
                            f"not match the file (sha256 {digest}, {size} bytes). Leave them "
                            "out and the SDK fingerprints the file itself."
                        )
                    if prepared.was_redacted:
                        # The stored hash will name the REDACTED bytes, which no
                        # reader ever opened; the original's hash is what a run
                        # reading this file can be matched on.
                        meta = {**meta, "source_sha256": _fingerprint(path)[0]}
                    # A caller-supplied hash describes the file on disk. Once a span
                    # is replaced that is no longer what leaves, and honouring it
                    # would refuse the upload on a digest mismatch, so the prepared
                    # bytes win. Only redaction overrides the caller.
                    uploaded = self._upload_file(
                        name,
                        prepared.path,
                        kind=kind,
                        # Checked equal above, so this is the caller's own
                        # value whenever they passed one (lower-cased).
                        content_hash=digest,
                        size_bytes=size,
                        content_type=content_type,
                        span_id=span_id,
                        step_index=step_index,
                        meta=meta,
                        notes=notes,
                        coords=coords,
                        labels=labels,
                        strict=strict,
                    )
                    self._note_logged(path, digest)
                    return uploaded
            except CredentialBlocked as exc:
                if strict_resolved:
                    raise
                return refused(str(exc), withhold_path=isinstance(exc, CredentialInPath))
        elif path is not None:
            # A uri AND a local copy: fingerprint for metadata, keep uri as the pointer.
            digest, size = _fingerprint(path)
            self._note_logged(path, digest)
            content_hash = content_hash or digest
            size_bytes = size_bytes if size_bytes is not None else size
            meta.setdefault("local_path", os.path.abspath(path))
        artifact = ArtifactCreate(
            kind=kind,
            name=name,
            uri=uri,
            content_hash=content_hash,
            content_type=content_type,
            size_bytes=size_bytes,
            is_reference=bool(is_reference) if is_reference is not None else (uri is not None),
            span_id=span_id,
            step_index=step_index,
            meta=meta,
            notes=notes,
            coords=coords or None,
            labels=labels or None,
        )
        body = artifact.model_dump(mode="json", exclude_none=True)
        return self._client.write("POST", f"/v1/runs/{self.id}/artifacts", body, strict=strict)

    def list_artifacts(self, *, scope: str = "all", **filters: Any) -> list[dict]:
        """Artifacts visible to this run. Defaults to ``scope="all"`` -- the run's own
        artifacts PLUS the ones promoted to its experiment and project, each tagged
        ``source_level`` -- because during a run that inherited context is usually what
        you want. Pass ``scope="own"`` to see only this run's, ``scope="inherited"`` for
        just the parent levels. Extra kwargs (``kind``, ``step_from``, ``step_to``) filter
        server-side."""
        return self._client.list_run_artifacts(self.id, scope=scope, **filters)

    def reconcile_artifact(self, name: str, content_hash: str) -> dict | None:
        """This run's already-recorded artifact with ``name`` AND ``content_hash``.

        OPT-IN helper: the SDK's own ``log_artifact`` does NOT call this yet, so a
        caller that retries artifact creation must invoke it explicitly.

        A proxy in front of the API can return 502 AFTER the write has landed, so
        the response is lost while the artifact exists. A blind retry then records
        the same bytes twice, and later selection
        (``next(a for a in arts if a["kind"] == "checkpoint")``) silently chooses
        between duplicates.

        Matching on the content hash makes this exact rather than a guess:
        artifacts are content-addressed, so identical hash under the same name on
        the same run IS the same artifact.
        """
        if not content_hash:
            return None
        for row in self._client.list_run_artifacts(self.id, name=name, scope="own") or []:
            if row.get("content_hash") == content_hash:
                return row
        # The server is not the only place a record can be. Under async the
        # original `log_artifact` may have journaled, so the artifact exists as
        # a queued op and the listing above sees nothing -- the caller then
        # re-logs, and BOTH land when the queue drains, producing exactly the
        # duplicate this method exists to prevent. A queued match is reported
        # with `state: "queued"` rather than a server row, because it has no id
        # yet and pretending otherwise would be a different lie.
        try:
            queued = self._queued_ops(self._client.journal.pending())
        except Exception:  # noqa: BLE001 -- no journal, or unreadable; the
            queued = []  # server listing above is still a valid answer
        for op in queued:
            if op.get("method") != "POST" or not str(op.get("path", "")).endswith("/artifacts"):
                continue
            body = op.get("body") or {}
            if body.get("name") == name and body.get("content_hash") == content_hash:
                return {**body, "state": "queued"}
        return None

    def resolve_artifact(self, name: str, *, scope: str = "all") -> dict | None:
        """The nearest artifact named ``name`` visible to this run, or ``None``. The
        backend returns nearest-wins order (run before experiment before project), so a
        run-level artifact shadows a same-named one promoted higher.

        An exact miss falls back to ``name`` plus ONE extension, because uploads keep
        the file's extension now (:mod:`probe.sdk.filetype`): a script that logged
        ``log_artifact("ckpt", path="ckpt-4000.pt")`` stored ``ckpt.pt`` and would
        otherwise stop finding its own artifact. The fallback costs one extra listing
        and only on a miss, so the hit path is unchanged.

        Nearest-wins still decides, and among equals at the same level the FIRST match
        wins -- with both ``ckpt.pt`` and ``ckpt.tar`` present, ``"ckpt"`` is genuinely
        ambiguous and this picks one. Pass the full name to say which.
        """
        rows = self._client.list_run_artifacts(self.id, name=name, scope=scope)
        if rows:
            return rows[0]
        stem = f"{name}."
        for row in self._client.list_run_artifacts(self.id, scope=scope):
            candidate = row.get("name") or ""
            if candidate.startswith(stem) and file_extension(candidate) == candidate[len(stem) :]:
                return row
        return None

    def claim_sandbox_base_state(
        self,
        ref: str,
        owner_key: str,
        *,
        strict: bool | None = None,
    ) -> dict[str, Any]:
        """Elect one worker to archive a shared sandbox begin state.

        Under fail-open operation an unavailable/older server returns
        ``capture_here=True`` and ``coordinated=False``: duplicate work is
        preferable to losing the only recoverable begin state.
        """
        if not ref.strip():
            raise ValueError("base-state ref must not be blank")
        if not owner_key.strip():
            raise ValueError("base-state owner_key must not be blank")
        strict_resolved = (not self._client.fail_open) if strict is None else strict
        try:
            return self._client.claim_sandbox_base_state(self.id, ref, owner_key)
        except Exception:  # noqa: BLE001 -- fail-open capture survives API drift/outage
            if strict_resolved:
                raise
            return {
                "ref": ref,
                "owner_key": owner_key,
                "capture_here": True,
                "coordinated": False,
            }

    def promote_artifact(self, artifact_id: str, *, to: str) -> dict:
        """Promote one of this run's artifacts up to its experiment or project so every
        run under that scope can see it (``to="experiment"`` or ``"project"``). Sugar over
        ``Client.move_artifact``; the target scope is derived from this run's chain."""
        return self._client.move_artifact(artifact_id, level=to)

    def _maybe_multipart(
        self,
        name: str,
        path: str,
        *,
        kind: str,
        content_type: str | None,
        span_id: str | None,
        step_index: int | None,
        meta: dict,
        notes: str | None,
        strict: bool,
        sync: bool | None,
        refused: Any,
    ):
        """An artifact over 64 MiB, in parts (plan item (g), `sdk/multipart.py`).

        Returns ``_NOT_QUEUED`` when this server or this run cannot take one
        (the caller then refuses it as before: a warning and a reference row);
        None once it is staged and queued -- the call returns at once and the
        outbox sends it in the background, in a lane of its own; or the
        server's answer after a synchronous upload (``sync=True``, ``strict`` --
        which a fail-closed client (``fail_open=False``) is by default -- or a
        client with no queue), which blocks for the whole transfer.

        An offline run (plan 2.12) keeps the pointer: its queue never touches
        the network until `probe sync`, and D12's over-64-MiB rule holds. So
        does a client under ``PROBE_ARTIFACT_OPAQUE_POLICY=block``.
        """
        client = self._client
        if getattr(client, "_drains_by_hand", False):
            return _NOT_QUEUED
        from . import secret_gate as _gate

        if not _gate.policy().allow_opaque:
            # `PROBE_ARTIFACT_OPAQUE_POLICY=block`: this user asked for nothing
            # that cannot be inspected to leave the machine, and a multipart
            # upload's bytes are stored before anything reads them.
            return _NOT_QUEUED
        try:
            supported = client.supports_feature(_multipart.FEATURE) is True
        except Exception:  # noqa: BLE001 -- unknown is not advertised
            supported = False
        if not supported:
            # Only a server that ADVERTISES `artifact_multipart` gets one --
            # prod ships the doors off (501, not declared) until its verifier
            # runs. Anything else, a features probe that failed included,
            # keeps today's path: the gate refuses the size, and 0.7's
            # warning and reference row stand.
            return _NOT_QUEUED
        fields = {
            "run_id": self.id,
            "name": name,
            "src": path,
            "kind": kind if kind != "file" else None,
            "content_type": content_type,
            "meta": meta or None,
            "notes": notes,
            "span_id": span_id,
            "step_index": step_index,
        }
        queue = (
            sync is not True
            and not strict
            and getattr(client, "async_writes", False)
            and (sync is not None or _env_async_uploads(default=True))
            and os.path.isfile(path)
        )
        if queue:
            journal = client.journal
            try:
                op = _multipart.build_op(journal, **fields)
            except _multipart.StageRefused as refusal:
                return refused(f"Artifact upload refused: {refusal}")
            except OSError as exc:
                return refused(f"Artifact upload refused: it could not be staged ({exc.strerror})")
            try:
                _multipart.enqueue(journal, op)
            except Exception as exc:  # noqa: BLE001 -- a full outbox is not the loop's problem
                _multipart.release_staged(op["multipart"])
                return refused(f"Artifact upload refused: the outbox could not take it ({exc})")
            self._multipart_ops = [*getattr(self, "_multipart_ops", []), op["op_id"]]
            client._after_enqueue()
            return None
        try:
            return _multipart.upload_now(client, **fields)
        except errors.RosError as exc:
            if strict:
                raise
            return refused(f"Artifact upload refused: the multipart upload failed ({exc})")
        except (OSError, _multipart.StageRefused) as exc:
            if strict:
                raise
            return refused(f"Artifact upload refused: {exc}")

    def _multipart_still_uploading(self) -> list[str]:
        """This run's multipart uploads still queued (plan (g)), by op id."""
        ops = getattr(self, "_multipart_ops", None)
        journal = getattr(self._client, "journal", None) if ops else None
        if not ops or journal is None:
            return []
        try:
            return _multipart.still_uploading(journal, ops)
        except Exception:  # noqa: BLE001 -- a count for a message
            return []

    def _maybe_queue_upload(
        self,
        name: str,
        path: str,
        *,
        kind: str,
        content_type: str | None,
        span_id: str | None,
        step_index: int | None,
        meta: dict,
        notes: str | None,
        strict: bool | None,
        sync: bool | None,
    ):
        """Queue an artifact upload, or return ``_NOT_QUEUED`` to upload now.

        STAGED-OR-SYNCHRONOUS. The queue is taken only when the outbox actually
        snapshots the bytes. `append_upload` would otherwise degrade to an
        UNSTAGED op that references the live file, which is right at a command
        line and wrong beside a training loop: checkpoint rotation -- write
        ckpt-1000, delete ckpt-900 -- is the normal shape of this workload, and
        an unstaged op whose source rotated either dead-letters or, above the
        inline-hash threshold, uploads different bytes under the caller's name.
        Falling back to the synchronous upload costs latency; the alternative
        costs correctness.

        Synchronous, always, when: the caller said so, `strict` demands a loud
        failure and a real row, the client is not async at all, or the file is
        not a regular file (a FIFO would block the snapshot forever, the guard
        `probe artifact log --async` already carries).
        """
        client = self._client
        if sync is True or not getattr(client, "async_writes", False):
            return _NOT_QUEUED
        if sync is None and not _env_async_uploads(default=True):
            return _NOT_QUEUED
        strict_resolved = (not client.fail_open) if strict is None else strict
        if strict_resolved:
            # strict means "raise, and hand back the row" -- neither of which a
            # queued write can do. Same resolution order as Client.write.
            return _NOT_QUEUED
        try:
            if not os.path.isfile(path):
                return _NOT_QUEUED
            from .journal import INLINE_HASH_MAX_BYTES

            # `require_staged` asks and appends in ONE step. This used to be a
            # separate "is there headroom?" pre-check followed by an append,
            # which is check-then-act: the same free-space measurement is redone
            # inside `append_upload`, and between the two another writer on this
            # journal -- a neighbouring agent session, or this very training loop
            # writing the next checkpoint -- can take the headroom. The pre-check
            # then says yes, the append degrades to an UNSTAGED op referencing
            # the live file, and nothing reads the receipt that says so. That op
            # is precisely what the staged-or-synchronous rule exists to prevent.
            #
            # Atomic collapses the window: either the bytes are snapshotted, or
            # no op was written and we upload below.
            queued = client.journal.append_upload(
                anchor="run",
                anchor_id=self.id,
                name=name,
                src_path=path,
                inline_hash=os.path.getsize(path) <= INLINE_HASH_MAX_BYTES,
                content_type=content_type,
                kind=kind if kind != "file" else None,
                meta=meta or None,
                notes=notes,
                span_id=span_id,
                step_index=step_index,
                run_ref=self.id,
                require_staged=True,
                # The credential scan runs later, off this thread: the file is
                # copied into the waiting room and a promoter (the detached
                # worker, a barrier, this process at exit) scans, redacts and
                # fingerprints the copy before it can become an op.
                defer_scan=True,
            )
        except Exception:  # noqa: BLE001 -- a queue that cannot take it is not
            return _NOT_QUEUED  # a reason to lose the artifact; upload it now
        if not queued.get("staged"):
            # Refused for want of headroom, and nothing was appended. Upload it
            # now, while the source is still the only copy we are sure of.
            return _NOT_QUEUED
        if queued.get("waiting"):
            client._promote_waiting_at_exit(self.id)
        client._after_enqueue()
        # None, deliberately: the SDK-wide "this was journaled" answer. A
        # receipt-shaped dict would be worse than nothing here -- harbor reads
        # `is_reference` off the returned row to decide whether bytes landed,
        # so a dict missing that key would mark the capture confirmed with no
        # artifact id. None degrades pessimistically, which is correct.
        return None

    def _write_marks(self, path: str | os.PathLike) -> dict[str, Any]:
        """`written_during_run` / `written_at` for a file being logged.

        The run's start is the server's `started_at` (or `created_at`), which
        for an attached run is the launcher's start -- the right boundary. A
        second of slack absorbs filesystem timestamp granularity."""
        try:
            mtime = os.stat(path).st_mtime
        except OSError:
            return {}
        started = self._data.get("started_at") or self._data.get("created_at")
        start_ts: float | None = None
        if isinstance(started, str):
            try:
                start_ts = datetime.fromisoformat(started.replace("Z", "+00:00")).timestamp()
            except ValueError:
                start_ts = None
        if start_ts is None:
            return {}
        return {
            "written_during_run": mtime >= start_ts - 1.0,
            "written_at": datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat(),
        }

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
        from .journal import drain

        try:
            drain(
                self._client.journal,
                run_ref=self.id,
                client_factory=self._client._outbox_client_factory(),
            )
        except Exception:  # noqa: BLE001 -- drain records last_error itself
            pass

    def _record_refused_upload(
        self,
        name: str,
        path: str,
        reason: str,
        *,
        withhold_path: bool,
        kind: str,
        content_type: str | None,
        span_id: str | None,
        step_index: int | None,
        meta: dict,
        notes: str | None,
        coords: dict[str, Any] | None,
        labels: dict[str, Any] | None,
        allow_missing: bool,
        sync: bool | None,
    ):
        """The row for an upload the gate REFUSED, instead of an exception in
        the caller's training loop (plan 0.7).

        The same shape `_upload_file` writes when an upload fails: a pointer to
        the file (``file://`` uri, ``meta.local_path``, ``meta.host``), its size,
        ``meta.upload = "failed"`` so `check_run` counts the gap, and the
        refusal in ``meta.upload_error`` -- value-free by construction, the gate
        never interpolates a path or a byte into it. No hash: a 70 GB
        checkpoint must not be read to record that it was not uploaded.

        One exception to the pointer: a credential in the PATH
        (``withhold_path``). The path is the thing that must not be stored, so
        the row carries a placeholder instead of it (``CredentialInPath``'s
        whole contract).

        ``sync`` is the caller's: a caller that asked for the row in hand
        (harbor's capture ledger, `sync=True`) gets it back, with its reason,
        instead of a journaled write that returns None.
        """
        if withhold_path:
            fields: dict[str, Any] = {
                "uri": None,
                # NEVER EMPTY: the server refuses a reference with neither a
                # uri nor a meta.local_path (`_validate_reference_coherence`,
                # app/artifacts/schemas.py), and this row is the only record
                # that the file existed.
                "meta": {"local_path": "<withheld: the path looks like it holds a credential>"},
            }
            try:
                fields["size_bytes"] = os.path.getsize(path)
            except OSError:
                pass
        else:
            # `allow_missing` is the caller's own: a source that vanished
            # between the gate and here is as missing as one that never was.
            fields = reference_fields(path, allow_missing=allow_missing)
        row = ArtifactCreate(
            kind=kind,
            name=name,
            uri=fields.get("uri"),
            size_bytes=fields.get("size_bytes"),
            content_type=content_type,
            is_reference=True,
            span_id=span_id,
            step_index=step_index,
            meta={**meta, **fields["meta"], "upload": "failed", "upload_error": reason},
            notes=notes,
            coords=coords or None,
            labels=labels or None,
        )
        # Recorded BEFORE the warning, as in `_upload_file`: under `-W error` a
        # warning that raised first would lose the only record of the file.
        recorded = self._client.write(
            "POST",
            f"/v1/runs/{self.id}/artifacts",
            row.model_dump(mode="json", exclude_none=True),
            strict=False,
            sync=bool(sync),
        )
        # This method, log_artifact's `refused` closure, log_artifact, the caller.
        self._warn_not_uploaded(name, reason, stacklevel=4)
        return recorded

    def _warn_not_uploaded(self, name: str, reason: str, *, stacklevel: int) -> None:
        """THE warning for an upload that ended as a pointer row -- a gate
        refusal (`_record_refused_upload`) or a failed upload
        (`_upload_file`'s fallback). Once per run per reason: a checkpoint
        saved every N steps must not print the same line N times, and every
        row still carries its own ``meta.upload``/``meta.upload_error``.

        Silent while `_OWN_UPLOAD_WARNING` is set: that caller says what
        happened in its own words, once."""
        if _OWN_UPLOAD_WARNING.get() or reason in self._uploads_warned:
            return
        self._uploads_warned.add(reason)
        _diagnostics.warn(
            f"probe: artifact {name!r} was not uploaded ({reason}); recorded as a reference "
            "to the file instead, and the run continues. Later uploads that fail for the "
            "same reason on this run are recorded the same way without another warning. "
            "Pass strict=True to raise instead.",
            stacklevel=stacklevel + 1,
        )

    @freeze_upload
    def _upload_file(
        self,
        name: str,
        path: str,
        *,
        kind: str,
        content_hash: str,
        size_bytes: int,
        content_type: str | None,
        span_id: str | None,
        step_index: int | None,
        meta: dict,
        notes: str | None = None,
        coords: dict[str, Any] | None = None,
        labels: dict[str, Any] | None = None,
        strict: bool | None = None,
    ):
        """presign -> PUT -> confirm. Fail-open: on failure (and not strict) falls
        back to recording a hash+metadata reference so the training loop is unblocked.

        ``coords``/``labels`` (already merged with the ambient unit by the caller)
        ride only the fallback ``ArtifactCreate``: the presign ``UploadRequest``
        model has no coordinate fields server-side, so sending them there would be
        silently dropped at best and a 422 on a stricter model at worst."""
        strict_resolved = (not self._client.fail_open) if strict is None else strict
        # The upload presign goes straight to the network, but `Run.span` is
        # journaled -- so under async the artifact can reach the server before
        # the span it points at, and the server enforces the foreign key
        # (`span_id not found for this run`, 422). Deliver the queue first so
        # the reference cannot outrun its referent. Only when a span is actually
        # cited, and only on the direct-post path: the metadata-only branch goes
        # through the journal, where FIFO already orders it behind the span.
        self._flush_for_span(span_id)
        req = UploadRequest(
            name=name,
            content_hash=content_hash,
            size_bytes=size_bytes,
            content_type=content_type,
            span_id=span_id,
            step_index=step_index,
            kind=kind if kind != "file" else None,  # None preserves labels on restage
            meta=meta or None,
            notes=notes,
        )
        try:
            presign = self._client.transport.post(
                f"/v1/runs/{self.id}/artifacts/uploads",
                req.model_dump(mode="json", exclude_none=True),
            )
            if not presign.get("have"):
                # Stream the file (model weights fit here); never read it whole into
                # memory. size_bytes is the fingerprinted length the presign signed.
                self._client.transport.put_file(
                    presign["upload_url"],
                    path,
                    content_type=content_type or "application/octet-stream",
                    headers=presign.get("upload_headers") or presign.get("headers"),
                )
            return self._client.transport.post(
                f"/v1/artifacts/{presign['artifact_id']}/confirm", None
            )
        except (errors.RosError, AttributeError, KeyError, TypeError, ValueError, OSError) as exc:
            # Broader than RosError on purpose. `presign` is None for an empty
            # 2xx (a proxy or CDN interstitial), so `.get`/`['artifact_id']`
            # raise AttributeError/KeyError; `put_file` re-opens the file per
            # attempt, so a checkpoint reaped mid-upload raises OSError; a
            # non-JSON 2xx body raises ValueError. Every one of those used to
            # sail past this handler into the training loop, which is precisely
            # what "fail-open" promised it would not do.
            if strict_resolved:
                raise
            # The recovery runs BEFORE the diagnostic. It used to be the other
            # way round, and under `-W error` the warn raised out of the handler
            # so the fallback row was never written -- the run lost the only
            # record of the file, and the message meant to explain the
            # degradation caused a worse one.
            local = os.path.abspath(original_upload_path(path))
            # THE URI NAMES THE ORIGINAL FILE, so the hash beside it must
            # describe that file. `content_hash`/`size_bytes` arrive from
            # `prepare_upload`, so after a redaction they describe bytes that
            # exist nowhere on disk: anyone resolving this pointer on a shared
            # volume and verifying the digest would get a mismatch and conclude
            # the file had been tampered with. Re-fingerprint what the uri
            # actually points at, and say in `meta` why the two differ.
            local_hash, local_size = content_hash, size_bytes
            redacted_hash = None
            try:
                if os.path.abspath(path) != local:
                    redacted_hash = content_hash
                    local_hash, local_size = _fingerprint(local)
            except OSError:
                # The source is gone; keep what we have rather than lose the row.
                local_hash, local_size = content_hash, size_bytes
            fallback = ArtifactCreate(
                kind=kind,
                name=name,
                uri=local_file_uri(local),
                content_hash=local_hash,
                size_bytes=local_size,
                content_type=content_type,
                is_reference=True,
                span_id=span_id,
                step_index=step_index,
                meta={
                    **meta,
                    "local_path": local,
                    "host": socket.gethostname(),
                    "upload": "failed",
                    # The transport's own gate refusing (a source that changed
                    # size mid-upload) says why; value-free by construction.
                    # Other failures keep their old shape: their text can quote
                    # a presigned URL.
                    **({"upload_error": str(exc)} if isinstance(exc, CredentialBlocked) else {}),
                    # Present only when the refused upload had been redacted:
                    # it names the digest of the bytes that WOULD have been
                    # stored, so the two hashes can be told apart later.
                    **({"redacted_content_hash": redacted_hash} if redacted_hash else {}),
                },
                # The description survives the fail-open downgrade: the row that
                # lands is the only record of this file, so dropping it here would
                # lose exactly what the caller took the trouble to write.
                notes=notes,
                coords=coords or None,
                labels=labels or None,
            )
            recorded = self._client.write(
                "POST",
                f"/v1/runs/{self.id}/artifacts",
                fallback.model_dump(mode="json", exclude_none=True),
                strict=False,
            )
            # The gate's reason is value-free; any other failure's text can
            # quote a presigned URL, so it is named, not quoted.
            self._warn_not_uploaded(
                name,
                str(exc) if isinstance(exc, CredentialBlocked) else "the upload did not complete",
                # _upload_file, its @freeze_upload wrapper, log_artifact, the caller.
                stacklevel=4,
            )
            return recorded

    # -- tags ----------------------------------------------------------------
    @property
    def tags(self) -> list[str]:
        return list(self._data.get("tags") or [])

    def set_tags(self, tags: list[str], *, strict: bool | None = None):
        """REPLACE the run's whole tag list ([] clears). The server normalizes
        to lowercase-kebab and 422s past the caps (CONTRACT.md "tags").
        Granular add/remove is the CLI ``probe run tag`` verb's
        read-modify-write job, not a server op.

        A pre-0066 backend would silently drop the field and 200 the old row;
        the response is verified so that no-op cannot masquerade as success.
        A spooled fail-open write returns None (unverifiable until flush).

        sync=True: that verification is the whole point of the method, and it
        only runs on a returned row -- under async this write journals, `data`
        is None, and the guard silently never fires for the SDK callers it was
        written for. `run.tags` would also keep reporting the pre-write list.
        One tag write per run is not loop traffic, so the round trip is free
        in the only sense that matters here."""
        data = self._client.write(
            "PATCH", f"/v1/runs/{self.id}", {"tags": list(tags)}, strict=strict, sync=True
        )
        if data:
            self._client._verify_tags_written(list(tags), data, "PATCH /v1/runs/{id}")
            self._data = data
        return data

    # -- config (plan (c)) ---------------------------------------------------
    @property
    def config(self) -> "RunConfig":
        """This run's config as a dict: reads are local, writes are not.
        ``run.config["lr"] = 3e-4``, ``run.config.update({...})`` and
        ``run.config.lr = 3e-4`` all merge into the stored config through
        :meth:`update_config`. Keys can be added and changed, never removed:
        the server merges, it never deletes."""
        return RunConfig(self)

    def update_config(
        self,
        values: Any,
        *,
        allow_val_change: bool | None = None,
        strict: bool | None = None,
    ):
        """Merge ``values`` into this run's config after it started (plan (c)).

        Shallow and new-wins, like W&B's ``run.config.update``: each top-level
        key replaces the stored one whole, and keys not named are untouched.
        ``values`` is anything ``config=`` takes -- a dict, a Hydra
        ``DictConfig``, an ``argparse.Namespace``, a dataclass, a pydantic
        model -- coerced to plain JSON first (:mod:`probe.sdk.coerce`).

        A key whose value CHANGES warns once per key per run and the new value
        wins; ``allow_val_change=True`` changes it quietly, and
        ``allow_val_change=False`` refuses the whole update with
        ``ValidationError`` before anything is sent (W&B's default). Fail-open
        and journaled like every write; ``strict=True`` raises instead.

        Needs a server that serves ``run_config_merge``. An older one accepts
        the request and silently drops the field, so the SDK does not send it:
        it warns once per run and returns None (``strict=True``:
        ``CapabilityUnavailable``). When the server cannot be asked at all, the
        update is sent anyway -- an older server drops it harmlessly, a newer
        one stores it."""
        return self._update_config(
            values, allow_val_change=allow_val_change, strict=strict, stacklevel=3
        )

    def _update_config(
        self,
        values: Any,
        *,
        allow_val_change: bool | None,
        strict: bool | None,
        stacklevel: int,
    ):
        plain = _coerce.to_config(values)
        if not plain:
            return None
        # Compare and print only what goes over the wire (#2032 review): the
        # stored config is scrubbed, so a raw value under a credential key
        # always looked "changed", and the warning printed the raw secret into
        # stderr -- which the run log uploads.
        wire = default_scrub(plain)
        if not isinstance(wire, dict):
            return None
        current = self._data.get("config") or {}
        changed = sorted(k for k, v in wire.items() if k in current and current[k] != v)
        if changed and allow_val_change is False:
            raise errors.ValidationError(
                f"config key(s) {changed} already have different values on this run; "
                "pass allow_val_change=True to change them"
            )
        if changed and allow_val_change is None:
            for key in changed:
                if key in self._config_warned:
                    continue
                self._config_warned.add(key)
                _diagnostics.warn(
                    f"probe: config {key!r} changed from {_diagnostics.describe(current[key])} "
                    f"to {_diagnostics.describe(wire[key])}; the new value wins. Pass "
                    "allow_val_change=True to change it without this warning.",
                    stacklevel=stacklevel,
                )
        try:
            supported = self._client.supports_feature("run_config_merge")
        except Exception:  # noqa: BLE001 -- cannot ask: send anyway (see update_config)
            supported = True
        if not supported:
            if strict:
                raise errors.CapabilityUnavailable(
                    "run_config_merge",
                    "this Probe server cannot merge a run's config after it started "
                    "(feature run_config_merge); pass config= when the run is created",
                )
            if not self._config_merge_refused:
                self._config_merge_refused = True
                _diagnostics.warn(
                    "probe: this Probe server cannot merge a run's config after it "
                    f"started (feature run_config_merge), so {sorted(plain)} were not "
                    "recorded. Pass config= when the run is created, or upgrade the server.",
                    stacklevel=stacklevel,
                )
            return None
        self._data["config"] = {**current, **wire}
        data = self._client.write(
            "PATCH", f"/v1/runs/{self.id}", {"config_merge": plain}, strict=strict
        )
        if isinstance(data, dict) and isinstance(data.get("config"), dict):
            self._data["config"] = data["config"]
        return data

    # -- foreign keys (shadow-SoT handles) ----------------------------------
    def link(self, *, strict: bool | None = None, **foreign_keys: Any):
        """Attach foreign keys (wandb_run_id, mlflow_run_id, s3_prefix, ...) to the
        real ``runs.foreign_keys`` column (fold #8). The server merges per-key
        new-wins via RunPatch, so a late-discovered id attaches without clobbering
        earlier keys and no read-modify-write round-trip is needed."""
        data = self._client.write(
            "PATCH", f"/v1/runs/{self.id}", {"foreign_keys": foreign_keys}, strict=strict
        )
        if data:
            self._data = data
        return data

    # -- declared metric ranges (0263) ----------------------------------------
    def expect(self, ranges: dict[str, Any], *, strict: bool | None = None):
        """Declare where metrics should stay; Probe emails you when one leaves.

        ::

            run.expect({
                "val/acc": (0.5, 1.0),      # email if it goes below 0.5 or above 1
                "train/loss": (None, 20),   # None = no limit on that side
            })

        OPTIONAL AND ADDITIVE. Call it once after the run opens -- before the
        training loop is the natural place -- or at any time later: every value
        already logged for the key is judged too. Calling it again adds or
        changes ranges (an unchanged range keeps its alert state, so a relaunch
        does not re-send an email); ``{"key": None}`` removes one. A range covers
        every series of that key (all ranks and coordinates).

        IT NEVER BREAKS THE SCRIPT: a malformed entry is dropped with a warning,
        and delivery is fail-open like :meth:`log` unless ``strict=True``.
        Returns the server's run row, or None when nothing was sent."""
        from . import expectations as _expectations

        wire, problems = _expectations.normalize(ranges)
        if strict and problems:
            # The CLI asked: a range it cannot record is an error, not a warning.
            raise ValueError("; ".join(problems))
        try:
            # `_diagnostics.warn`, never `warnings.warn`: under `-W error` a plain
            # warning RAISES, and an optional add-on must not end a training run.
            for problem in problems:
                _diagnostics.warn(f"probe.expect: dropped {problem}", stacklevel=2)
            if not wire:
                return None
            data = self._client.write(
                "PATCH",
                f"/v1/runs/{self.id}",
                {"metric_expectations": wire},
                strict=strict,
            )
        except Exception as exc:  # noqa: BLE001 -- an optional add-on cannot break the run
            if strict:
                raise
            _diagnostics.warn(f"probe.expect: not recorded ({exc})", stacklevel=2)
            return None
        if data:
            self._data = data
        return data

    # -- snapshot (execution record) ----------------------------------------
    def _upload_pending_code(
        self,
        manifest: dict,
        cwd: str | None,
        *,
        upload: bool,
        max_upload_bytes: int,
        strict: bool | None,
    ) -> dict:
        """Store the files git cannot supply. Returns what to record in meta.

        The returned ``pending_upload`` is the count that SURVIVES this call, so
        a reader can trust it: it is 0 only when the bytes are actually stored.
        `Client.check_run` gates `pending_code_bytes` on it.
        """
        pending = _snapshot.pending_entries(manifest)
        # Stamped before the branch: a run with nothing to store, or one that
        # opted out of uploads, is still recorded under the storage it would
        # have used, not under the archive by default.
        if not pending:
            return {
                "uploaded": False,
                "pending_upload": 0,
                "reason": "nothing pending",
                "storage": _code_storage(),
            }
        if not upload:
            return {
                "uploaded": False,
                "pending_upload": len(pending),
                "reason": "upload disabled",
                "storage": _code_storage(),
            }

        root = os.path.abspath(cwd or os.getcwd())
        if _code_storage() == CODE_STORAGE_ARTIFACTS:
            result = self._upload_pending_files(
                root, pending, strict=strict, max_upload_bytes=max_upload_bytes
            )
            if result.get("fallback") != CODE_STORAGE_ARCHIVE:
                return result
            # A server that predates the batch doors (404/405 on the first
            # presign) still takes the archive; a lagging deploy must not turn
            # every run into an unreproducible one.
            _diagnostics.warn(
                "this server has no per-file capture doors yet; storing the "
                "code-bytes archive instead",
                stacklevel=3,
            )
        tmp = tempfile.NamedTemporaryFile(prefix="probe-code-", suffix=".tar.gz", delete=False)
        tmp.close()
        try:
            summary = _snapshot.build_pending_archive(
                root, manifest, tmp.name, max_bytes=max_upload_bytes
            )
            drifted = list(summary["missing"]) + list(summary["changed"])
            drift_meta = {"drifted": drifted[: _snapshot.DRIFTED_META_LIMIT]} if drifted else {}
            drift_warning = (
                f"code capture stored {summary['n_files']} of {len(pending)} files; "
                f"{summary['drift_message']}"
            )
            if summary["n_files"] == 0:
                # Every pending file moved between manifest and archive; an
                # empty archive would claim a capture that did not happen.
                _diagnostics.warn(drift_warning, stacklevel=3)
                return {
                    "uploaded": False,
                    "pending_upload": len(pending),
                    "reason": "tree drifted during capture",
                    **drift_meta,
                }
            drifted_set = set(drifted)
            # This method says what happened to the archive, once, below: the
            # generic "pass strict=True" line would name a call the user never
            # made, on top of that.
            own_warning = _OWN_UPLOAD_WARNING.set(True)
            try:
                rec = self.log_artifact(
                    _snapshot.CODE_BYTES_ARTIFACT,
                    # sync=True: the `finally` below unlinks this tmp archive, so a
                    # queued op would reference a file guaranteed to be gone by the
                    # time the drainer read it -- a dead letter with 100% hit rate.
                    sync=True,
                    path=tmp.name,
                    kind="code_bytes",
                    content_type="application/gzip",
                    meta={
                        "n_files": summary["n_files"],
                        "uncompressed_bytes": summary["uncompressed_bytes"],
                        "tree_sha256": manifest.get("tree_sha256"),
                        # Only the members whose bytes VERIFIED against the manifest.
                        # A path listed here that the archive does not hold is the
                        # lie this whole path removes.
                        "paths": [e["path"] for e in pending if e["path"] not in drifted_set],
                        **drift_meta,
                    },
                    strict=strict,
                )
            finally:
                _OWN_UPLOAD_WARNING.reset(own_warning)
        except _snapshot.SnapshotTooLarge:
            raise
        except errors.RosError as exc:
            # Fail-open like every other write: the training run continues, but
            # the count stays non-zero so nothing reads this as captured. Drift
            # never raises (it is recorded, below); what does is a malformed
            # manifest entry, a file that shrank or changed under the stream,
            # or an upload error -- and the cause rides in the warning.
            if strict is True or (strict is None and not self._client.fail_open):
                raise
            _diagnostics.warn(
                f"code-bytes upload failed ({exc}); {len(pending)} files remain unstored "
                "and this run is not reproducible from the record alone.",
                stacklevel=3,
            )
            return {"uploaded": False, "pending_upload": len(pending), "reason": "upload failed"}
        finally:
            try:
                os.unlink(tmp.name)
            except OSError:
                pass

        if drifted:
            _diagnostics.warn(drift_warning, stacklevel=3)
        # A fail-open spooled write returns None -- unverifiable until flush, so
        # it cannot be claimed as stored.
        if not rec:
            return {
                "uploaded": False,
                "pending_upload": len(pending),
                "reason": "spooled",
                **drift_meta,
            }
        # A storage failure under fail-open makes `log_artifact` record a
        # REFERENCE to the tmp archive (a pointer the `finally` above deletes).
        # That is not stored bytes: it used to read as a complete capture with
        # `n_pending_upload` 0, the same lie as the short archive.
        if rec.get("is_reference") or (rec.get("meta") or {}).get("upload") == "failed":
            # The gate's own reason when it was the gate (an archive over the
            # inspection limit never reached storage at all).
            refusal = (rec.get("meta") or {}).get("upload_error")
            cause = (
                f"refused by the credential gate: {_gate_reason(refusal)}"
                if refusal
                else "storage refused the archive"
            )
            _diagnostics.warn(
                f"code-bytes upload failed ({cause}); {len(pending)} "
                "files remain unstored and this run is not reproducible from the record alone.",
                stacklevel=3,
            )
            return {
                "uploaded": False,
                "pending_upload": len(pending),
                "reason": "upload failed",
                **drift_meta,
            }
        return {
            "uploaded": True,
            # The files whose bytes did NOT land: drifted ones are unstored
            # exactly like a failed upload, and named so a reader knows which.
            "pending_upload": len(drifted),
            "artifact_id": rec.get("id"),
            "archive_sha256": summary["sha256"],
            "size_bytes": summary["size_bytes"],
            "n_files": summary["n_files"],
            **drift_meta,
        }

    def _upload_pending_files(
        self,
        root: str,
        pending: list[dict],
        *,
        strict: bool | None,
        max_upload_bytes: int,
    ) -> dict:
        """Store the files git cannot supply as one artifact row PER FILE.

        Windows of ``CAPTURE_WINDOW``: presign the window (the server dedupes on
        content and answers ``have`` for bytes it already holds), PUT the misses
        ``CAPTURE_PUT_WORKERS`` wide against checksum-pinned URLs, confirm, retry
        the unconfirmed ONCE with fresh URLs, then the next window. Symlinks are
        never uploaded: the manifest carries their target and restore writes
        them from it.

        Every byte that leaves the machine was verified first: the file is opened
        the way the archive path opens it (``snapshot.open_verified_file`` --
        ``O_NOFOLLOW``, size and sha re-checked on the descriptor) and that same
        descriptor is streamed. A file that drifted since the manifest is
        reported ``changed``, never sent. The whole tree is bounded by
        ``max_upload_bytes`` exactly like the archive (``SnapshotTooLarge``).

        Fail-open exactly like the archive path: a server error stops the
        upload, warns, and the returned ``pending_upload`` is every file whose
        bytes did not land -- so ``check_run`` still reads the run as not
        reproducible. Three things stop the walk early, each with one warning
        and the rest named as unstored: a window whose PUTs all fail against
        storage (or half of a window of ``OUTAGE_MIN_WINDOW`` or more), a
        window storage rejects outright, and ``CAPTURE_DEADLINE_SECONDS``
        elapsing. Under ``strict=True`` any file that storage failed to take
        (not one that drifted on disk) raises at the end. Every file that is
        not stored is listed in
        ``unstored`` with a reason so a reader can see WHICH files, not just how
        many; the list is capped, the count is not.

        Returns ``{"fallback": "archive"}`` when the first presign answers
        404/405: the server predates the batch doors and the caller stores the
        archive instead.
        """
        files = [e for e in pending if e.get("mode") != "120000"]
        n_symlinks = len(pending) - len(files)
        total = sum(int(e.get("size") or 0) for e in files)
        if total > max_upload_bytes:
            raise _snapshot.SnapshotTooLarge(
                f"pending files total {total} bytes, above the {max_upload_bytes}-byte "
                "cap; raise --max-upload-mb or add the large paths to .gitignore/a "
                "reference rule rather than shipping a partial capture"
            )
        captured_at = datetime.now(timezone.utc).isoformat()
        stored: set[str] = set()
        unstored: dict[str, str] = {}  # path -> reason; sorted and capped on the way out
        n_uploaded = n_deduped = 0
        client = self._client

        def _wire_name(path: str) -> str:
            # NFC (the server canonicalises to it and echoes that form) with
            # POSIX separators; the manifest keeps the path as the filesystem
            # spelled it.
            return _snapshot.wire_name(path)

        def _mark_stored(path: str) -> None:
            stored.add(path)
            unstored.pop(path, None)

        def _result(reason: str | None = None) -> dict:
            missing = [e["path"] for e in files if e["path"] not in stored]
            for p in missing:
                # A file no verdict ever named was never reached: the upload
                # stopped (a server error, an outage) before its window. Files
                # whose window WAS in flight carry their own reason already.
                unstored.setdefault(p, "upload stopped before this file")
            listed = sorted(unstored.items())
            return {
                "uploaded": bool(stored),
                "pending_upload": len(missing),
                "storage": CODE_STORAGE_ARTIFACTS,
                **({"reason": reason} if reason else {}),
                "n_files": len(stored),
                "n_uploaded": n_uploaded,
                "n_deduped": n_deduped,
                "n_symlinks": n_symlinks,
                "unstored": [
                    {"path": p, "reason": r} for p, r in listed[: _snapshot.DRIFTED_META_LIMIT]
                ],
                "captured_at": captured_at,
            }

        if not files:
            return _result("nothing to upload")

        drifted_paths: set[str] = set()  # the tree moved: named, never a strict failure

        def _put(entry: dict, out: dict) -> tuple[str, str | None, str]:
            """Verify, then stream. Returns (path, error, kind) where kind is
            ``ok`` | ``drift`` (never sent) | ``rejected`` (storage said no:
            not retried) | ``refused`` (the local credential gate said no: not
            retried, never an outage) | ``transport`` (network / 5xx: retried
            once)."""
            path = entry["path"]
            try:
                verdict, fh = _snapshot.open_verified_file(root, entry)
            except _snapshot.SnapshotError as exc:
                return path, str(exc), "drift"
            if verdict != "ok" or fh is None:
                return path, f"{verdict} since the manifest was taken", "drift"
            with fh:
                try:
                    client.transport.put_fileobj(
                        out["upload_url"],
                        fh,
                        size=int(entry["size"]),
                        content_type="application/octet-stream",
                        headers=out.get("upload_headers") or None,
                    )
                except CredentialBlocked as exc:
                    # THIS machine's gate said no (the file grew past the
                    # inspection limit, or moved under the stream): storage
                    # never saw it. Checked before RosError, which it is.
                    return path, f"refused by the credential gate: {_gate_reason(exc)}", "refused"
                except errors.TransportError as exc:
                    return path, _redact_signed(str(exc)), "transport"
                except errors.RosError as exc:
                    status = exc.status or 0
                    throttled = status in (408, 429)
                    return (
                        path,
                        _redact_signed(str(exc)),
                        "transport" if status >= 500 or throttled else "rejected",
                    )
                except Exception as exc:  # noqa: BLE001 -- reported per file below
                    return path, _redact_signed(str(exc)), "transport"
            return path, None, "ok"

        def _presign(entries: list[dict]) -> dict:
            # Path and size only: this path never calls `prepare_upload`, and a
            # snapshot must not be redacted anyway. The CONTENT was scanned when
            # the manifest was built (snapshot._ContentGate), and `_put` streams
            # only bytes whose sha256 still matches that record.
            for entry in entries:
                check_upload(os.path.join(root, entry["path"]))
            items = [
                {
                    "name": _wire_name(e["path"]),
                    "content_hash": e["sha256"],
                    "size_bytes": int(e.get("size") or 0),
                    "mode": "100755" if e.get("mode") == "100755" else "100644",
                }
                for e in entries
            ]
            return client.presign_capture_batch(self.id, items, captured_at=captured_at)

        twins: dict[str, list[str]] = {}  # artifact id -> extra paths it also serves

        def _paths_for(aid: str) -> list[str]:
            return [need[aid][0]["path"], *twins.get(aid, ())]

        def _take_slots(entries: list[dict], presigned: dict, need: dict) -> None:
            """Join the server's answer to the window BY POSITION (the server
            guarantees one slot per item, in order); a missing or empty slot is
            a verdict of its own, never a silent success."""
            slots = presigned.get("items") or []
            for idx, entry in enumerate(entries):
                nonlocal n_deduped
                path = entry["path"]
                out = slots[idx] if idx < len(slots) else None
                if not isinstance(out, dict):
                    unstored[path] = "no verdict from storage"
                    continue
                if out.get("error"):
                    unstored[path] = str(out["error"])
                    continue
                if out.get("have"):
                    n_deduped += 1
                    _mark_stored(path)
                    continue
                aid, url = out.get("artifact_id"), out.get("upload_url")
                if not aid or not url:
                    unstored[path] = "no verdict from storage"
                    continue
                if aid in need:
                    # Two manifest paths that normalise to ONE name with the same
                    # bytes (an NFC and an NFD spelling of the same file) share one
                    # row: upload it once, and give every spelling the verdict.
                    twins.setdefault(aid, []).append(path)
                    continue
                need[aid] = (entry, out)

        deadline = _capture_deadline()
        started_at = time.monotonic()

        def _check_deadline() -> None:
            if time.monotonic() - started_at >= deadline:
                raise errors.TransportError(f"capture deadline of {deadline:.0f}s reached")

        try:
            for start in range(0, len(files), CAPTURE_WINDOW):
                _check_deadline()
                window = files[start : start + CAPTURE_WINDOW]
                try:
                    presigned = _presign(window)
                except errors.RosError as exc:
                    if start == 0 and exc.status in (404, 405):
                        return {"fallback": CODE_STORAGE_ARCHIVE, "reason": "no batch doors"}
                    raise
                need: dict[str, tuple[dict, dict]] = {}  # artifact_id -> (entry, item_out)
                _take_slots(window, presigned, need)

                pending_ids = list(need)
                for attempt in (1, 2):
                    if not pending_ids:
                        break
                    if attempt == 2:
                        _check_deadline()
                        # Fresh URLs for the stragglers: a presigned PUT expires,
                        # and the server hands the same rows back for the same
                        # identities. A `have` on the retry means another run
                        # stored those bytes meanwhile.
                        retry_entries = [need[aid][0] for aid in pending_ids]
                        fresh: dict[str, tuple[dict, dict]] = {}
                        _take_slots(retry_entries, _presign(retry_entries), fresh)
                        for aid in list(pending_ids):
                            if aid in fresh:
                                need[aid] = fresh[aid]
                            else:
                                # Stored (`have`), or a verdict already recorded
                                # for the primary spelling: its twins follow it.
                                primary = need[aid][0]["path"]
                                for p in twins.get(aid, ()):
                                    if primary in stored:
                                        _mark_stored(p)
                                    else:
                                        unstored[p] = unstored.get(
                                            primary, "no verdict from storage"
                                        )
                                pending_ids.remove(aid)
                        if not pending_ids:
                            break
                    failed_put: dict[str, tuple[str, str]] = {}  # aid -> (kind, error)
                    pool = ThreadPoolExecutor(max_workers=CAPTURE_PUT_WORKERS)
                    try:
                        futures = {pool.submit(_put, *need[aid]): aid for aid in pending_ids}
                        for fut in as_completed(futures):
                            _path, error, kind = fut.result()
                            if error is None:
                                # The bytes are in the store; only a confirm
                                # makes them a file of this run. Recorded now
                                # so a confirm that never returns is named as
                                # what it is, not as "never attempted".
                                for p in _paths_for(futures[fut]):
                                    unstored[p] = "uploaded, not confirmed by storage"
                            else:
                                failed_put[futures[fut]] = (kind, error)
                    except BaseException:
                        # Ctrl-C mid-window: the queued PUTs must not run to
                        # completion behind the user's back.
                        pool.shutdown(wait=False, cancel_futures=True)
                        raise
                    else:
                        pool.shutdown(wait=True)
                    for aid, (kind, error) in failed_put.items():
                        for path in _paths_for(aid):
                            if kind == "drift":
                                drifted_paths.add(path)
                                unstored[path] = error
                            elif kind == "rejected":
                                unstored[path] = f"upload rejected: {error}"
                            elif kind == "refused":
                                unstored[path] = error
                            else:
                                unstored[path] = f"upload failed: {error}"
                    to_confirm = [aid for aid in pending_ids if aid not in failed_put]
                    unconfirmed: list[str] = []
                    if to_confirm:
                        result = client.confirm_capture_batch(to_confirm)
                        seen: set[str] = set()
                        for aid in result.get("confirmed") or []:
                            if aid in need:
                                seen.add(aid)
                                n_uploaded += 1
                                for p in _paths_for(aid):
                                    _mark_stored(p)
                        for aid in result.get("unconfirmed") or []:
                            if aid in need:
                                seen.add(aid)
                                unconfirmed.append(aid)
                                for p in _paths_for(aid):
                                    unstored[p] = "not confirmed by storage"
                        # Only `unconfirmed` (HEAD did not see the object yet)
                        # is worth a second PUT + confirm. The other buckets
                        # are verdicts: `refused` is a live row that is not a
                        # capture row (the researcher registered that name
                        # and bytes on purpose), `failed` is a row the upload
                        # reaper gave up on, `unknown` has no live row.
                        for bucket, reason in (
                            ("refused", "already an artifact of this run, not captured"),
                            ("failed", "reaped by storage before the upload landed"),
                            ("unknown", "no live artifact row for this file"),
                        ):
                            for aid in result.get(bucket) or []:
                                if aid in need:
                                    seen.add(aid)
                                    for p in _paths_for(aid):
                                        unstored[p] = reason
                        for aid in to_confirm:
                            if aid not in seen:
                                if attempt == 1:
                                    unconfirmed.append(aid)
                                else:
                                    for p in _paths_for(aid):
                                        unstored[p] = "no verdict from storage"
                    transport_failed = [a for a, (k, _) in failed_put.items() if k == "transport"]
                    rejected = [a for a, (k, _) in failed_put.items() if k == "rejected"]
                    if attempt == 1 and len(pending_ids) >= 2:
                        # Evaluated AFTER the confirm so the PUTs that landed are
                        # banked before the walk stops. Every PUT in a window
                        # failed against storage on the first pass -- or, in a window of OUTAGE_MIN_WINDOW or
                        # more, at least half of them: that is an outage, not
                        # 128 individual mishaps, and a flaky link must not be
                        # walked for hours. A window storage REJECTED outright
                        # (a proxy that strips the checksum header, a bucket
                        # policy) is the same verdict. (The retry pass is only
                        # the stragglers; two flaky files in a small window
                        # are retried, not declared an outage.)
                        all_failed = len(transport_failed) == len(pending_ids)
                        half_failed = len(pending_ids) >= OUTAGE_MIN_WINDOW and len(
                            transport_failed
                        ) * 2 >= len(pending_ids)
                        if all_failed or half_failed:
                            first = failed_put[transport_failed[0]][1]
                            raise errors.TransportError(f"storage unreachable: {first}")
                        if len(rejected) == len(pending_ids):
                            first = failed_put[rejected[0]][1]
                            raise errors.TransportError(
                                f"storage rejected every upload in this window: {first}"
                            )
                    # Every verdict above was recorded as it happened and a
                    # later success pops it, so the second pass needs no
                    # bookkeeping of its own: whatever is still named after it
                    # is the final word.
                    pending_ids = transport_failed + unconfirmed
        except errors.RosError as exc:
            if strict is True or (strict is None and not client.fail_open):
                raise
            out = _result("upload failed")
            _diagnostics.warn(
                f"code capture stopped after {len(stored)} of {len(files)} files "
                f"({_redact_signed(str(exc))}); {out['pending_upload']} remain unstored and "
                "this run is not reproducible from the record alone.",
                stacklevel=3,
            )
            return out

        out = _result()
        if out["unstored"]:
            first = out["unstored"][0]
            message = (
                f"{out['pending_upload']} of {len(files)} captured files could not be stored "
                f"(first: {first['path']}: {first['reason']}); this run is not fully "
                "reproducible from the record alone."
            )
            # `strict` means "raise if my code was not saved": a file STORAGE
            # failed to take (a rejected or failed PUT, a refused name, a
            # confirm that never came back) raises; a file that changed on
            # disk while it was read is the tree moving, and stays a warning.
            storage_failed = [u for u in out["unstored"] if u["path"] not in drifted_paths]
            if storage_failed and (strict is True or (strict is None and not client.fail_open)):
                raise errors.RosError(message)
            _diagnostics.warn(message, stacklevel=3)
        return out

    def snapshot(
        self,
        *,
        cwd: str | None = None,
        include_env: bool = True,
        include_gpu: bool = True,
        venv: str | None = None,
        detect_venv: bool = False,
        upload: bool = True,
        max_upload_bytes: int = _snapshot.DEFAULT_MAX_UPLOAD_BYTES,
        include: list[str] | None = None,
        reference_over_bytes: int = _snapshot.DEFAULT_REFERENCE_OVER_BYTES,
        strict: bool | None = None,
        argv: list[str] | None = None,
    ) -> dict:
        """Capture code + deps + GPUs as a content-addressed execution record
        (fold #7), with git provenance (HEAD, branch, dirty -- read, never
        written) on the code-snapshot artifact. Non-disruptive.

        ``argv`` — the command this run executes, when a caller launches a
        child process; defaults to this process's argv.

        ``venv`` / ``detect_venv`` choose WHICH environment is recorded. The
        default records this interpreter's, which is correct here and only here:
        an in-process caller is running in the environment being snapshotted.
        A caller that launches the code as a subprocess -- the CLI, or any
        launcher script outside the training venv -- must pass ``detect_venv=True``
        (or an explicit ``venv``), otherwise it records its OWN packages with
        full confidence. See :func:`probe.sdk.snapshot.capture_env`.

        The execution record pins ``run.env_ref`` to its content hash via RunPatch
        (fold #7 + the RunPatch env_ref parity), the same column the ingest path sets.

        Git is provenance, NOT the code record -- neither the retired shadow ref
        (it lived in the object database of whatever machine ran the job, so on an
        ephemeral box it stopped resolving the moment that box was destroyed) nor the pushed
        remote (a force-push, a deleted fork or a private repo an auditor cannot
        read all break it silently). So ``capture_manifest`` no longer classifies
        anything as retrievable-from-git: THE BYTES ARE THE RECORD.

        ``upload`` (default ON) STORES them. Every file classified
        ``source="blob"`` -- which is now every file that fits under
        ``reference_over_bytes`` -- is stored as its own ``kind='code'`` artifact
        row, content-addressed (presign in windows of ``CAPTURE_WINDOW``, the
        server's ``have`` answer dedupes unchanged files across runs and users);
        ``PROBE_CODE_STORAGE=archive`` tars them into a single deterministic
        ``code-bytes`` artifact instead. Without either the record holds a
        sha256, and a sha256 verifies a file you already have rather than
        producing one you do not: the run is identified and unreproducible.

        The one thing still recorded rather than copied is a file ABOVE
        ``reference_over_bytes`` -- a base checkpoint or a dataset shard, whose
        path, host and sha256 are recorded as a file-path reference. That is a
        deliberate size decision, not a bet on a remote still existing.

        Manifests of 200+ entries are ordinary; the per-file path batches them
        (one presign and one confirm per window, 16 PUTs in flight) so the cost
        is a few round-trips, not hundreds, and a sweep of N runs over unchanged
        code uploads each changed file once. The archive path keeps the older
        single-object shape for servers without the batch doors."""
        # Git is PROVENANCE, read-only, and never a gate (plan 2.6): no author
        # identity, an unborn HEAD, a read-only `.git` or no git binary used to
        # abort the whole capture (no code, deps or argv). Now the tree is
        # captured regardless -- as a plain directory when git cannot read it --
        # and why git failed rides in `meta.git_error`.
        git, git_error = _snapshot.git_provenance(cwd or os.getcwd())
        manifest = _snapshot.capture_manifest(
            cwd,
            include=include,
            reference_over_bytes=reference_over_bytes,
            # Every file that could be uploaded is content-scanned and withheld
            # when it holds a credential (snapshot._ContentGate) -- whether or not
            # this capture uploads, so the tree's identity never depends on the
            # flag. Bounded by the upload cap only when uploading.
            scan=True,
            scan_budget_bytes=max_upload_bytes if upload else None,
            # `.probeignore` (plan (n)): excluded after the safety stops, and
            # never over an explicit `include=`.
            ignore=self._ignore_rules(cwd),
        )
        _warn_credential_skips(manifest)
        # Identity is hashed into the execution record; provenance is NOT --
        # a venv path in `deps` would make two identical environments at
        # different paths produce different env_refs. See split_env_provenance.
        deps, env_provenance = _snapshot.split_env_provenance(
            _snapshot.capture_env(
                cwd,
                venv=venv,
                detect_venv=detect_venv,
                strict=strict if strict is not None else not self._client.fail_open,
            )
            if include_env
            else {}
        )
        # Warn HERE rather than in the CLI's display code, because `probe exec`
        # reaches this same `detect_venv=True` path (see `execute`) and has no
        # display layer to carry the notice. Without this the exec path records
        # no environment and says nothing -- and absence that prints nothing is
        # how a run reaches the record looking captured. The `probe snapshot`
        # command prints its own fuller message, so that one path says it twice;
        # a duplicated warning is the cheap side of never losing it.
        if env_provenance.get("resolved_via") == _snapshot.UNRESOLVED_FALLBACK:
            warnings.warn(
                "environment NOT captured: no virtualenv could be attributed to "
                f"{os.path.abspath(cwd or os.getcwd())}, and the interpreter "
                f"({env_provenance.get('python_executable')}) is outside it. "
                "Recording its packages would describe the launcher, not the "
                "run. Pass venv=... (CLI: --venv PATH), or activate the "
                "environment the code runs in.",
                stacklevel=2,
            )
        lockfiles = sorted(
            (
                {"path": e["path"], "sha256": e["sha256"]}
                for e in manifest["entries"]
                if e.get("lockfile") and e.get("source") != "withheld"
            ),
            key=lambda item: item["path"],
        )
        if lockfiles:
            deps = {**deps, "lockfiles": lockfiles}
        record = ExecutionRecordCreate(
            # `git` is deliberately NOT hashed into the execution record (design
            # doc D1): the identity table names the code MANIFEST as identity.
            # Git is provenance, not identity -- HEAD, branch and dirty ride the
            # code-snapshot artifact's meta below.
            code={"manifest": manifest},
            deps=deps,
            hardware=(
                {"gpu": _snapshot.capture_gpu(), **_snapshot.capture_system()}
                if include_gpu
                else {}
            ),
        )
        exec_rec = self._client.transport.post(
            "/v1/execution-records", record.model_dump(mode="json", exclude_none=True)
        )
        content_hash = exec_rec.get("content_hash") if exec_rec else None

        # Store the bytes git cannot supply. Runs BEFORE the code-snapshot
        # artifact is written, so its meta records the real outcome rather than
        # a promise: `pending_upload` in that meta means those bytes are gone,
        # and it must never say 0 because an upload was merely attempted.
        code_bytes = self._upload_pending_code(
            manifest, cwd, upload=upload, max_upload_bytes=max_upload_bytes, strict=strict
        )

        # Pin the real runs.env_ref column (FK to the execution record just
        # created). Launch ephemera ride the SAME patch as env_ref: one write, and
        # the metadata merge is client-side (read-modify-write) because RunPatch
        # REPLACES metadata. Single-writer per run is the operating assumption
        # (probe exec holds the run lock; SDK runs are process-bound).
        launch_block = _launch.build_launch_block(
            argv=argv,
            cwd=cwd,
            config=(self._data or {}).get("config"),
        )
        current_meta = dict((self._data or {}).get("metadata") or {})
        patch_body: dict = {"metadata": {**current_meta, "launch": launch_block}}
        if content_hash is not None:
            patch_body["env_ref"] = content_hash
            # Before the write, so no reader sees the PATCH queued and the pin
            # missing (the hardware rail's never-clobber check).
            self._pinned_env_ref = content_hash
        # Deliberately NOT sync. `finish()` orders its completeness check after
        # the drain precisely so this PATCH and the code-snapshot artifact are
        # observed together; forcing this one to land early would break that
        # ordering (tests/test_run_check_launch.py pins it) and put a round trip
        # on run open.
        #
        # The cost is that the env_ref persistence probe below -- which catches a
        # backend that accepts the field, ignores it and answers 200 -- only runs
        # when a row comes back. That is now SAID rather than silently skipped:
        # a guard nobody knows was skipped is worse than no guard.
        data = self._client.write("PATCH", f"/v1/runs/{self.id}", patch_body, strict=strict)
        if data is None and content_hash is not None:
            _diagnostics.warn(
                "probe: env_ref was queued, not confirmed — the backend-capability "
                "check is unavailable for this write. `probe run check` after the "
                "outbox drains verifies it."
            )
        if data:
            self._data = data
            if content_hash is not None and data.get("env_ref") != content_hash:
                message = (
                    "Probe Research API did not persist run.env_ref after snapshot "
                    f"(expected {content_hash}, got {data.get('env_ref')!r})"
                )
                if strict is True or (strict is None and not self._client.fail_open):
                    raise errors.CapabilityUnavailable("run.env_ref", message)
                warnings.warn(message, stacklevel=2)
        # The code-snapshot row points at what was STORED, git repo or not: the
        # `git:refs/probe/snapshots/...` uri named a shadow commit that is no
        # longer written (plan 2.6). The manifest travels with it so a reader can
        # tell, without fetching anything, which files the capture holds.
        # `check_run` requires a code_snapshot row to exist at all.
        if code_bytes.get("storage") == CODE_STORAGE_ARTIFACTS and content_hash:
            # Per-file storage has no single archive to point at; the execution
            # record (keyed by env_ref) IS the record of what was captured, and
            # its rows sit on this run.
            code_uri = f"probe-manifest:{content_hash}"
        elif code_bytes.get("artifact_id"):
            code_uri = f"probe-artifact:{code_bytes.get('artifact_id')}"
        elif content_hash:
            # Nothing stored (upload off or failed; `n_pending_upload` says so),
            # but the manifest still identifies the tree -- and a reference row
            # must name something (the server 422s one that names nothing).
            code_uri = f"probe-manifest:{content_hash}"
        else:
            code_uri = None
        paths_text = "\n".join(
            sorted(e["path"] for e in (manifest.get("entries") or []) if e.get("path"))
        )
        paths_truncated = False
        if len(paths_text.encode("utf-8")) > PATHS_TEXT_MAX_BYTES:
            cut = paths_text.encode("utf-8")[:PATHS_TEXT_MAX_BYTES].decode("utf-8", "ignore")
            paths_text = cut.rsplit("\n", 1)[0]
            paths_truncated = True
        self.log_artifact(
            "code-snapshot",
            uri=code_uri,
            kind="code_snapshot",
            is_reference=True,
            allow_missing=True,
            meta={
                "vcs": "git" if git else None,
                "branch": git.get("branch") if git else None,
                "dirty": git.get("dirty") if git else None,
                # The commit the tree sat on (None on an unborn branch). The uri
                # used to carry a shadow commit; this is the real one.
                "head": git.get("head") if git else None,
                **({"git_error": git_error} if git_error else {}),
                "skipped": manifest.get("skipped") or None,
                # `skipped` lists at most PROBEIGNORE_REPORT_LIMIT of these.
                **({"n_probeignore": manifest["n_probeignore"]} if manifest.get("n_probeignore") else {}),
                "env_ref": content_hash,
                "tree_sha256": manifest["tree_sha256"],
                "base_commit": manifest["base_commit"],
                "remote": manifest["remote"],
                "n_git_referenced": manifest["n_git_referenced"],
                # What SURVIVES, not what was classified. `check_run` gates
                # `pending_code_bytes` on this, so it must mean "these bytes are
                # gone" -- never "an upload was attempted". `n_classified_pending`
                # keeps the pre-upload count for diagnostics.
                "n_pending_upload": code_bytes["pending_upload"],
                "n_classified_pending": manifest["n_pending_upload"],
                "n_referenced_offsite": manifest.get("n_referenced_offsite", 0),
                # Files left out whole because their content holds a credential
                # (`source: "withheld"` in the manifest; the paths are in `skipped`).
                "n_withheld": manifest.get("n_withheld", 0),
                # Which storage the captured bytes live in (0193): "artifacts"
                # means one code row per file on this run; "archive" means the
                # code-bytes tarball. A label for readers and search; restore
                # does NOT branch on it -- it looks for complete capture rows
                # on the run and falls back to the archive.
                "storage": code_bytes.get("storage", CODE_STORAGE_ARCHIVE),
                # Every path this run ran with, newline-joined, so /v1/search
                # can answer "which run captured results.jsonl" from THIS row
                # instead of from thousands of per-file rows. Bounded (see
                # PATHS_TEXT_MAX_BYTES); a cut list says so.
                "paths_text": paths_text,
                **({"paths_text_truncated": True} if paths_truncated else {}),
                "code_bytes": code_bytes,
                # WHICH environment the deps came from. Deliberately here and
                # not in the hashed execution record (split_env_provenance).
                **({"env": env_provenance} if env_provenance else {}),
                "n_lockfiles": len(lockfiles),
                **({"launch_errors": launch_block["errors"]} if launch_block.get("errors") else {}),
            },
            strict=strict,
        )
        return {
            "git": git,
            "git_error": git_error,
            "manifest": manifest,
            "code_bytes": code_bytes,
            "deps": deps,
            "env_provenance": env_provenance,
            "execution_record": exec_rec,
            "content_hash": content_hash,
            "launch": launch_block,
        }

    # -- output capture (D17) -------------------------------------------------
    def _ignore_rules(self, cwd: str | os.PathLike | None = None) -> Any:
        """This run's ``.probeignore`` rules for ``cwd`` (plan (n)), or None when
        nothing is configured. Loaded once per directory; never raises."""
        cache = self.__dict__.setdefault("_ignore_cache", {})
        try:
            key = os.path.abspath(os.fspath(cwd) if cwd is not None else os.getcwd())
        except OSError:  # the working directory was deleted under the run
            return None
        if key not in cache:
            try:
                cache[key] = _ignore.load(key, extra=getattr(self, "_ignore_patterns", ()))
            except Exception:  # noqa: BLE001 -- an ignore file may never cost a capture
                cache[key] = None
        return cache[key]

    def _set_ignore(self, patterns: Any) -> None:
        """Record ``ignore=`` patterns (a string is one pattern)."""
        if patterns is None:
            return
        try:
            self._ignore_patterns = _ignore.normalize(patterns)
        except ValueError as exc:
            raise errors.ValidationError(str(exc)) from None
        self.__dict__.pop("_ignore_cache", None)

    def _hand_ignore_to_launcher(self) -> None:
        """A JOINED run's own ``ignore=`` patterns (plan (n), #2045 review).

        Under ``probe exec`` the launcher on this host collects this
        process's reads and sweeps its folder after it exits, with the rules
        the LAUNCHER loaded, which never saw these. They travel through the
        channels those captures already read: the read spool
        (:func:`inputs.hand_to_launcher`) and the output window's registry
        record (:func:`outputs.share_ignore`); with no launcher on this host
        both are no-ops. The code snapshot is the one capture they cannot
        reach -- a launcher takes it before this process starts -- so a
        pattern the launcher never loaded is named in a warning. Never raises.
        """
        patterns = getattr(self, "_ignore_patterns", ())
        if not patterns:
            return
        try:
            rules = self._ignore_rules()
            if rules is None:
                return
            from . import inputs as _inputs

            _inputs.hand_to_launcher(self.id, rules)
            _outputs.share_ignore(self.id, rules)
            unseen = _ignore.unseen_by_launcher(patterns, rules)
            if unseen and os.environ.get("PROBE_AUTO_SNAPSHOT", "1") != "0":
                from . import safe_warn

                safe_warn.warn(
                    f"probe: ignore={unseen!r} cannot keep files out of this run's code snapshot: "
                    "the launcher that opened the run (`probe exec`) took it before this script "
                    "started. They still keep matching files out of what this script reads and "
                    "writes. To keep them out of code capture too, put them in .probeignore (at "
                    "the git toplevel) or PROBE_IGNORE where you launch.",
                    stacklevel=3,
                )
        except Exception:  # noqa: BLE001 -- filtering is never a reason to fail init
            pass

    def _start_capture(
        self,
        *,
        outputs: str | os.PathLike | None = None,
        capture_outputs: bool | None = None,
    ) -> None:
        """Open this run's capture window IN THIS PROCESS: the folder's
        baseline now, fds 1/2 teed to ``probe/run.log``, the sweep at close. A
        no-op when opted out, or when a launcher on this host (``probe
        exec``) already captures for this process."""
        if self._capture is not None or not _outputs.enabled(capture_outputs):
            return
        try:
            root = _outputs.target_root(outputs=outputs)
            if _outputs.outputs_owned_here(root) and _outputs.log_owned_here():
                # `probe exec` on this host already sweeps this folder and tees
                # this process (PROBE_CAPTURE_OWNER/_ROOT/_LOG_OWNER).
                return
            # When exec sweeps the folder but does not tee (it could not), this
            # window keeps the log only.
            self._capture = _outputs.OutputCapture.start(
                self._client,
                self.id,
                outputs=outputs,
                sweep=not _outputs.outputs_owned_here(root),
                ignore=self._ignore_rules(),
                epoch=_logstream.handle_epoch(self),
                writer=self._writer_record(),
            )
        except Exception as exc:  # noqa: BLE001 -- capture never stops a run from opening
            warnings.warn(f"probe: output capture could not start ({type(exc).__name__}): {exc}", stacklevel=2)

    def _note_forked_writer(self) -> None:
        """This handle is writing from a forked child (2.2): leave a marker
        beside the capture record, once per child, so the output helper's
        reporter does not call the run's writer dead when the process that
        opened it exits (`fork()` then `os._exit()` in the parent is how a
        script daemonizes). A child that never writes (a DataLoader worker)
        leaves none, and the opener's death is still reported."""
        pid = os.getpid()
        if self._forked_writer_marked == pid:
            return
        self._forked_writer_marked = pid
        try:
            capture = self._capture
            entry = getattr(capture, "_entry", None) if capture is not None else None
            if entry is not None:
                _outputs.mark_forked_writer(entry, pid)
        except Exception:  # noqa: BLE001 -- bookkeeping never touches a write
            pass

    def _writer_record(self) -> dict:
        """What the output helper needs to report this process's death (2.2).

        ``sole_writer`` is this process's own belief: a handle attached through
        PROBE_RUN_ID (a rank, a job under a launcher) is one of several writers
        by construction, and the server additionally refuses when anything
        attached (`attached_at`) or the run is not in-process."""
        attached = bool(getattr(self, "attached", False))
        return {
            "session_id": self.session_id,
            "write_epoch": self.write_epoch,
            "role": "attached" if attached else "owner",
            "sole_writer": not attached,
        }

    def _note_logged(self, path: str, digest: str | None = None) -> None:
        capture = self._capture
        if capture is not None:
            try:
                capture.note_logged(path, digest)
            except Exception:  # noqa: BLE001 -- bookkeeping never touches a write
                pass

    def _finalize_capture(self, budget: float | None = None) -> dict | None:
        """Queue this run's log, then sweep and queue its outputs, within
        ``budget`` seconds. Before the barrier drain, so the close makes one
        attempt at delivering them -- but they are non-blocking ops, and an
        undeliverable one never holds the close: it stays queued for the
        detached drainer."""
        capture = self._capture
        if capture is None:
            return None
        try:
            return capture.finalize(budget=budget)
        except Exception:  # noqa: BLE001 -- finalize warns itself; never block a close
            return None

    # -- liveness -----------------------------------------------------------
    def start_heartbeat(
        self,
        interval_seconds: float | None = None,
        role: str = "owner",
        *,
        attached: bool | None = None,
    ) -> None:
        """Beat ``POST /v1/runs/{id}/heartbeat`` from a daemon thread until a
        terminal :meth:`set_status` (or the process exits). Idempotent.

        ``Client.create_run`` calls this for every handle it mints, so the rule
        from :meth:`Client.heartbeat_run` — beat for the run's whole life or not
        at all — holds by construction: the beats stop exactly when this process
        stops, and a process that dies without finishing is precisely what the
        server's reaper should flip to 'crashed'. Only start an OWNER beat on a
        handle whose run lives and dies with the current process; a run managed
        from outside (CLI ``run start``) must never owner-beat.

        ``role="observer"`` (0106) is the sanctioned beat for processes that
        watch a run they do not own — the miles exporter sidecar. It asserts
        "something is attached", keeping the run alive while present, and its
        silence resolves to 'untracked' rather than 'crashed'.

        ``attached`` (0205) marks these beats as coming from INSIDE the work, so
        the server stamps ``attached_at``. Defaults to the handle's own flag,
        which ``_wrap_run`` set: a launcher's handle beats without it, a handle
        opened by ``probe.init()`` from PROBE_RUN_ID beats with it. Under a
        wrapped run both processes beat as owners, and this is the only thing
        that tells them apart.

        Interval precedence: explicit argument, then PROBE_HEARTBEAT_SECONDS,
        then the 60s default. Non-positive disables.

        The thread also stops when this handle is garbage-collected (an
        abandoned run's process may still be alive, but nobody can ever finish
        it — letting the reaper end it is the honest outcome) and when the
        owning ``Client`` closes (beats ride its transport).
        """
        if role not in ("owner", "observer"):
            # Fail loudly HERE: the beat loop swallows every exception, so a
            # typo'd role would otherwise 422 silently forever and the run
            # would be reaped despite a "running" heartbeat thread.
            raise ValueError(f"heartbeat role must be 'owner' or 'observer', got {role!r}")
        if self._hb_thread is not None and self._hb_thread.is_alive():
            if getattr(self, "_hb_role", "owner") != role:
                # Role change is explicit, never silent: an owner beat that
                # quietly stayed 'observer' would make a real death read
                # 'untracked', and the reverse keeps asserting ownership after
                # the owner detached. Restart the loop under the new role.
                self.stop_heartbeat()
                if self._hb_thread is not None:
                    self._hb_thread.join(timeout=1.0)
            else:
                return
        interval = _heartbeat_interval() if interval_seconds is None else float(interval_seconds)
        if interval <= 0:
            return
        self._hb_role = role
        # The beat may have to re-read a refused credential (plan 2.7), which
        # needs to know whose it was while it still works.
        learn = getattr(self._client, "_learn_identity", None)
        if learn is not None:
            learn()
        stop = threading.Event()
        thread = threading.Thread(
            target=_beat_forever,
            args=(
                self._client,
                self.id,
                stop,
                interval,
                role,
                self.write_epoch,
                getattr(self, "attached", False) if attached is None else attached,
                # WEAK on purpose: the thread must not pin the handle (its
                # collection is what stops the beat), but a reopen after an
                # outage has to reach the handle's epoch or the process is
                # locked out of the run it just recovered.
                weakref.ref(self),
                # 2.8: beat the writer's lease instead of the run-level beat.
                None
                if self._lease is None
                else {**self._lease, "role": "observer"}
                if role == "observer"
                else self._lease,
            ),
            name=f"probe-run-heartbeat-{self.id[:8]}",
            daemon=True,
        )
        self._hb_stop = stop
        self._hb_thread = thread
        # OWNER beats are the moment this process declares that its lifetime
        # IS the run's lifetime, which is exactly the claim the node agent
        # needs in order to blame a vanished pid on a run. Observers are not
        # registered: an observer never staked its lifetime on anything, and
        # its exit says nothing about the work.
        if role == "owner":
            self._register_with_node_agent()
        # finalize holds the Event (its callback arg), never the Run, so the
        # handle stays collectable and its collection is what ends the beat.
        self._hb_finalizer = weakref.finalize(self, stop.set)
        self._client._register_run_heartbeat(stop)
        thread.start()

    def stop_heartbeat(self) -> None:
        if self._hb_stop is not None:
            self._hb_stop.set()
        if self._hb_finalizer is not None:
            self._hb_finalizer.detach()
        self._hb_stop = None
        self._hb_thread = None
        self._hb_finalizer = None

    # -- lifecycle ----------------------------------------------------------
    def set_status(
        self,
        status: str,
        *,
        ended_at: str | None = None,
        summary_metrics: dict | None = None,
        summary: dict | None = None,
        sync: bool = False,
        strict: bool | None = None,
        only_if_running: bool = False,
    ):
        summary = _one_summary(summary_metrics, summary)
        if status in _TERMINAL_STATUSES and self._lease is not None:
            if self._lease_protocol is None and sync:
                # No beat of this lease has answered yet: one bounded beat
                # learns which rules the run follows (and registers the lease).
                self._draining_beat(draining=False)
            if self._leased():
                # 2.8: a writer on a lease RELEASES it with its verdict and the
                # server closes the run once its leases say the work ended --
                # the worst of every writer's verdict, never whichever landed
                # last.
                return self._release_lease(
                    status, ended_at=ended_at, summary=summary, sync=sync, strict=strict
                )
            # A lease on a run that is NOT on leases (NULL: opened before 0271 or
            # by an older client; flipped; the kill switch off; or not known):
            # close it exactly as before 2.8, then release the lease so it reads
            # released rather than expired (review of #2060, HIGH-1).
            lease, self._lease = self._lease, None
            try:
                data = self.set_status(
                    status,
                    ended_at=ended_at,
                    summary=summary,
                    sync=sync,
                    strict=strict,
                    only_if_running=only_if_running,
                )
            finally:
                self._lease = lease
            # Only after a close that did not raise: a strict close that failed
            # must not be completed later by a queued release.
            self._send_release(status, sync=sync, strict=False)
            return data
        if status in _TERMINAL_STATUSES and not getattr(self, "_sends_terminal_status", True):
            # A non-zero rank attached to a SHARED run (`fluent.init` sets the
            # flag; interim until per-writer leases, plan 2.8). Its ending is
            # one rank's, not the run's: rank 0 and the launcher own the close.
            # It stops beating and leaves the row as it is.
            self.stop_heartbeat()
            self._closed_status = status
            return self._data
        # 0205. `only_if_running` makes this write CONDITIONAL: it is skipped
        # when the row this handle last saw is already terminal. The designated
        # finalizer of a wrapped run (the launcher, holding the exit code) uses
        # it so it can close a run nobody else ended WITHOUT overwriting a
        # verdict the job itself already wrote from inside the work. Terminal
        # authority belongs to whoever spoke with knowledge, not to whoever's
        # request happened to land second.
        #
        # The local view can be stale, which is fine in the safe direction: if
        # the child finished after our last read we may still PATCH, and the
        # server's own guard (WHERE status = 'running') refuses it there. This
        # check exists to avoid the pointless write and the confusing audit
        # event, not as the only lock.
        if only_if_running:
            # RE-READ. The launcher's cached row is whatever it saw at attach
            # time -- always 'running' on the execute() path -- and the server
            # has NO terminal guard of its own (patch_run appends `status = $n`
            # unconditionally). Trusting the cache let a launcher exiting 0
            # overwrite a child's own `finish("failed")` with 'completed',
            # which is the verdict-authority bug this flag exists to prevent.
            # One GET, on the finalize path only.
            try:
                current = self._client.get_run(self.id).get("status")
            except Exception:
                # Cannot prove the run is still open -> do not write. A missed
                # terminal flip is recoverable (the reaper ends it); stomping a
                # real verdict is not.
                return None
            # `crashed` is the one terminal status nobody wrote with
            # knowledge: it is the reaper's GUESS (or a writer-gone report)
            # about a process that went quiet. A launcher holding the real
            # exit code replaces it -- a wrapped job that exited 0 through an
            # outage whose recovery could not run must not end `crashed`.
            # Every verdict a writer chose (completed, failed, canceled) and
            # `untracked` still stand.
            if current in _TERMINAL_STATUSES and current != "crashed":
                return None
        if status in _TERMINAL_STATUSES:
            # Stop before the PATCH: once the intent is to end the run, a beat
            # racing the flip is noise (the server no-ops late beats anyway), and
            # if the PATCH itself fails the reaper finishing the job is correct.
            self.stop_heartbeat()
            # Every close -- finish(), `probe run end` (either mode), a caller's
            # own set_status -- must land BEHIND this run's uploads, and an
            # upload still waiting for its credential scan is not in the queue
            # yet. Scanning is local CPU: finish it here, before the PATCH is
            # written or journaled.
            self._promote_uploads_before_close(
                strict=(not self._client.fail_open) if strict is None else bool(strict)
            )
        body: dict[str, Any] = {"status": status}
        # 1.10: a status write names the generation that sent it, so a
        # superseded attempt's close (sync, or replayed from the outbox after
        # a relaunch took the run over) is refused instead of closing the live
        # attempt. Only a KNOWN epoch; a server predating 1.10 ignores it.
        if self.write_epoch is not None:
            body["write_epoch"] = self.write_epoch
        if ended_at is not None:
            body["ended_at"] = ended_at
        if summary is not None:
            body.update(_summary_wire(summary))
        # `sync` belongs to the CALLER, not to this method: `finish()` drains
        # and then closes, so it needs the row in hand and passes sync=True,
        # while `probe run end --async` deliberately queues the close behind
        # the run's own data and must stay journaled.
        #
        # Fail-open, though it used to be strict=True (ProSeCo, 2026-08-19).
        # This was the one write in the SDK that propagated a TransportError,
        # and `Run.__exit__` calls it from inside an exception handler -- so a
        # network blip while a run was already failing replaced the body's real
        # traceback with a transport one and took the process down. Journaling
        # is strictly better: the status still lands on the next drain, and the
        # reaper already closes a run whose terminal flip never arrives.
        # `strict` is the CLI's door back to the old loud behaviour: `probe run
        # end` is documented as the delivery barrier, so it must still raise
        # rather than journal-and-exit-0. The SDK's finish() leaves it None and
        # fail-opens, which is what keeps a blip from killing a training
        # process; the two callers want opposite things from the same PATCH.
        # A terminal status that fails open into the journal is `admitted`: the
        # queue-length cap must not refuse the one op that closes the run, as
        # the deferred close already is not (review of #2014, H5b).
        data = self._client.write(
            "PATCH",
            f"/v1/runs/{self.id}",
            body,
            sync=sync,
            strict=strict,
            admitted=status in _TERMINAL_STATUSES,
        )
        if data:
            self._data = data
        if status in _TERMINAL_STATUSES:
            self._closed_status = status
            # This process ended the run (written, or journaled to land): tell
            # the session's daemon. Fire-and-forget, never raises.
            from . import daemon_channel

            daemon_channel.run_ended(self.id, status)
        return data

    def _owns_run_fields(self) -> bool:
        """A leased writer whose close carries the run's own fields (end
        time, headline scalars): an owner or a launcher, never a rank."""
        return getattr(self, "_sends_terminal_status", True) and (
            (self._lease or {}).get("role") != "rank"
        )

    def _leased(self) -> bool:
        """Whether this handle closes through its lease (2.8): it has one, and
        the server said the run follows the lease rules. Anything else -- the
        server's `legacy` (NULL, flipped, the kill switch off) or no answer
        yet -- closes the pre-2.8 way (review of #2060, HIGH-1)."""
        return self._lease is not None and self._lease_protocol == "leases"

    def _note_lease_answer(self, resp: Any) -> None:
        """What a lease beat's answer says: the lease is registered, which rules
        the run follows, and -- once -- that something reported this writer
        dead while it still runs (its lease is GONE: its verdict reads
        `crashed` unless its own recovery reopens the run)."""
        self._lease_registered = True
        if not isinstance(resp, dict):
            return
        if resp.get("liveness_protocol"):
            self._lease_protocol = resp["liveness_protocol"]
        if resp.get("lease") == "gone" and not getattr(self, "_lease_gone_warned", False):
            self._lease_gone_warned = True
            _diagnostics.warn(
                f"probe: run {self.id}: this process was reported dead (writer-gone) while "
                "it is still running; the server counts its lease as crashed."
            )

    def _release_body(self, status: str) -> dict:
        """A release names its writer, so a lease no beat registered still counts."""
        writer = {k: v for k, v in (self._lease or {}).items() if k != "session_id"}
        return {"write_epoch": self.write_epoch or 1, "exit_status": status, "writer": writer}

    def _send_release(self, status: str, *, sync: bool, strict: bool | None):
        """POST this writer's release through `Client.write` (journaled on a
        transport failure, behind whatever this close already wrote)."""
        session = self._lease["session_id"]
        # Literal call site: the tests/test_parity.py AST scan must see the route.
        return self._client.write(
            "POST",
            f"/v1/runs/{self.id}/writers/{session}/release",
            self._release_body(status),
            sync=sync,
            strict=strict,
        )

    def _release_lease(
        self,
        status: str,
        *,
        ended_at: str | None,
        summary: dict | None,
        sync: bool,
        strict: bool | None,
    ):
        """The terminal write of a leased handle on a `leases` run (2.8).

        The run's own fields (the end time, the headline scalars) still go as
        a PATCH -- WITHOUT `status`, which is now the server's to decide -- from
        a writer whose verdict the run carries (not a non-zero rank's, as
        before). Then the release, naming the writer. Both go through
        `Client.write`, so a transport failure journals them in this order,
        behind the run's data, and `finish()` settles a journaled close as it
        always has. A run flipped to legacy between the last beat and this
        release needs nothing more: on a run that is not `leases` the server
        closes it on an owner's or launcher's release, with its verdict."""
        self.stop_heartbeat()
        self._promote_uploads_before_close(
            strict=(not self._client.fail_open) if strict is None else bool(strict)
        )
        data = None
        # The run's own fields (end time, headline scalars) come from a writer
        # whose verdict the run carries: an owner or a launcher. A job that
        # joined from inside the work and owns its verdict (a forwarded
        # PROBE_RUN_ID, a hand-off) holds an OWNER lease for exactly that; a
        # rank, or a job under a finalizing launcher, sends none. Nobody sends
        # `status`: the leases decide it, and a status written after their
        # close overwrote the worst verdict (review of #2060).
        owns_verdict = self._owns_run_fields()
        if owns_verdict and (ended_at is not None or summary is not None):
            body: dict[str, Any] = {}
            if ended_at is not None:
                body["ended_at"] = ended_at
            if summary is not None:
                body.update(_summary_wire(summary))
            data = self._client.write("PATCH", f"/v1/runs/{self.id}", body, sync=sync, strict=strict)
        resp = self._send_release(status, sync=sync, strict=strict)
        self._closed_status = status
        from . import daemon_channel

        daemon_channel.run_ended(self.id, status)
        if not isinstance(resp, dict):
            # Journaled (fail-open) or queued: the release lands on the next
            # drain. `finish()` reads it as the pending terminal op.
            return None if owns_verdict or data is None else data
        if resp.get("liveness_protocol"):
            self._lease_protocol = resp["liveness_protocol"]
        row = dict(data if isinstance(data, dict) else self._data)
        if resp.get("run_status"):
            row["status"] = resp["run_status"]
        self._data = row
        return row

    def _queued_ops(self, rows) -> list[dict]:
        """This run's ops that are allowed to hold its close.

        ``blocking=False`` ops are excluded: they are best-effort by contract
        (diagnostics), and letting one dead-letter into this set would keep a
        run `running` for the reaper instead of closing it `failed`.
        """
        return [op for _, op in rows if op.get("run_ref") == self.id and op.get("blocking", True)]

    def _register_with_node_agent(self) -> None:
        """Tell a watcher on this box which process owns this run.

        Fail-open and silent: the agent is opt-in, and a researcher who has
        not asked for it pays one environment read. Nothing here may raise --
        this runs while a training job is starting.
        """
        try:
            from probe.box import registry, watch

            if not watch.enabled():
                return
            settings = getattr(self._client, "settings", None)
            registry.register(
                self.id,
                context=getattr(settings, "context", None),
                base_url=getattr(settings, "base_url", None),
                writer=self._writer_record(),
            )
            # Every owner tries; the lease makes all but one a no-op. No run
            # can know whether it is the first on this machine, and asking the
            # server would be a round trip in the run's start path.
            from probe.box import spawn

            spawn.maybe_spawn()
        except Exception:  # noqa: BLE001 -- bookkeeping never touches the run
            pass

    def _deregister_with_node_agent(self) -> None:
        """The run closed itself, so its absence needs no explaining."""
        try:
            from probe.box import registry

            registry.deregister(self.id)
        except Exception:  # noqa: BLE001
            pass

    @staticmethod
    def _resolve_finish_timeout(flush_timeout: float | None, *, default: Any = _UNSET) -> float | None:
        """The close's deadline in seconds: ``flush_timeout``, else
        ``PROBE_FINISH_TIMEOUT_SEC``, else ``default`` -- by default
        `FINISH_TIMEOUT_DEFAULT_SECONDS` (600), read at call time; `execute()`
        passes None to keep its one-pass delivery of captured outputs. Read
        ONCE per close, so a mid-close env change cannot extend it. Negative
        means zero: queue everything, wait for nothing."""
        if default is _UNSET:
            default = FINISH_TIMEOUT_DEFAULT_SECONDS
        if flush_timeout is not None:
            return max(float(flush_timeout), 0.0)
        raw = os.environ.get("PROBE_FINISH_TIMEOUT_SEC")
        if raw:
            try:
                return max(float(raw), 0.0)
            except ValueError:
                # Read inside a close: a plain warnings.warn raises under -W error.
                _diagnostics.warn(
                    f"ignoring malformed PROBE_FINISH_TIMEOUT_SEC={raw!r}; "
                    "expected seconds as a float",
                    stacklevel=3,
                )
        return default

    def _drain_until(
        self, drain_deadline: float, *, strict: bool
    ) -> tuple[list, list, int, bool]:
        """Deliver THIS run's ops until none is left or ``drain_deadline``.

        Returns ``(pending, dead, delivered, auth_blocked)``: this run's
        blocking ops still queued, its dead letters, how many ops the loop
        delivered, and whether it stopped on a refused credential.

        Grown from PR #1679's ``_barrier_drain_with_retry`` (Mahit), which gave
        the old one-attempt hard barrier a bounded retry: a two-second blip --
        a pod rolling, a DNS hiccup, a 502 that recovers at once -- must not
        decide a run whose data is durable on disk. What holds it to its
        deadline now (plan 0.6):

          * the caller wraps it in `transport.deadline_scope`, so every request
            -- each attempt's timeout and every transport-level retry -- ends by
            ``drain_deadline``, not merely each PASS;
          * the drain lock is polled, at most `_FINISH_LOCK_POLL_SECONDS` at a
            time, never blocked on: a detached worker mid-pass cannot hold the
            close past its deadline, and between polls the loop looks at what
            of this run is still queued, since that worker may be delivering it;
          * the waits come from `durable.backoff_delays` (`_FINISH_BACKOFF`),
            at least the server's ``Retry-After`` when it named one, and never
            past the deadline.

        Counts only THIS run's ops (`Journal.run_ops`): each op file is parsed
        once, not the whole machine-wide queue after every pass.

        ``strict`` returns at the first dead letter: a strict close refuses on
        it, and waiting cannot heal a permanent rejection (#1679's rule). A
        default close keeps delivering the rest and reports the dead letters on
        the run instead.

        A refused credential (401/403) on THIS run's pass returns at once: only
        a login fixes it, so waiting out the deadline was dead time (review of
        #2011: a 401 held the close 300 s where main raised in 0.01 s). The
        signal is the run-scoped pass's own `auth_blocked`, never the
        machine-wide `auth_blocked_since` in status.json, which a NEIGHBOUR
        run's expired token could have written (#1679).
        """
        from . import durable

        mine = self._client.journal.run_ops(self.id)
        # Writes of this run queued under ANOTHER credential (#2035) sit in
        # their own queue, where this process cannot deliver them and this
        # queue's order cannot see them. Counted, never waited on: a close is
        # then deferred, and the drain keeps a queued close behind them
        # (#2041 round 3: the close landed first, 5 of 5).
        elsewhere = self._client.journal.run_ops_elsewhere(self.id, min_epoch=self.write_epoch)
        delays = durable.backoff_delays(None, _FINISH_BACKOFF)
        delivered = 0
        while True:
            report = None
            left = drain_deadline - time.monotonic()
            try:
                report = self._client._drain_for_close(
                    self.id, lock_timeout=max(0.0, min(left, _FINISH_LOCK_POLL_SECONDS))
                )
                delivered += report.delivered
            except Exception:  # noqa: BLE001 -- drain records last_error itself
                pass
            pending = mine.pending()
            dead = mine.failed()
            auth_blocked = report is not None and report.auth_blocked
            if not pending:
                return elsewhere.pending(), dead, delivered, auth_blocked
            if (strict and dead) or auth_blocked:
                return pending, dead, delivered, auth_blocked
            left = drain_deadline - time.monotonic()
            if left <= 0:
                return pending, dead, delivered, False
            if report is not None and report.lock_busy:
                # Already waited on the lock; its holder may be delivering ours.
                continue
            if report is not None and report.delivered:
                delays = durable.backoff_delays(None, _FINISH_BACKOFF)  # progress: stay prompt
            time.sleep(
                durable.honor_retry_after(
                    next(delays),
                    None if report is None else report.retry_after,
                    ceiling=left,
                )
            )

    def _queue_deferred_finish(
        self,
        status: str,
        summary: dict | None,
        pending_count: int,
        *,
        accounting: dict | None = None,
        beacon: bool = True,
    ) -> dict:
        """Journal the terminal status BEHIND this run's queued ops (F3/F3a).

        FIFO is the correctness guarantee: the run can never read terminal
        ahead of the data queued before it. The op carries the accounting a
        late drain needs -- the REAL local end time, the pending count at
        exit, and the writing session -- so "final data arrived late via the
        outbox" stays visible on the run after it lands, not just while
        queued. A best-effort beacon tags the run "draining" so the dashboard
        shows intent instead of a phantom "running"; the queued finish
        restores the tags, so the tag lives exactly as long as the drain gap.
        When the network is down (the very reason the flush timed out) the
        beacon fails silently -- nothing informs a server without a network.

        A leased handle (2.8) queues its release as the close, and only THEN
        sends one bounded DRAINING beat (`_queue_terminal_op`): its lease stays
        live (not beating) for up to an hour, so a close still delivering its
        backlog is neither closed early nor alerted on, while a requeue can
        still take the run over. Verdict first: a pre-empted job killed
        during that beat has already saved it (review of #2060).
        """
        self.stop_heartbeat()
        if not getattr(self, "_sends_terminal_status", True) and not self._leased():
            # Same rule as `set_status`: this rank's data stays queued for the
            # detached worker, but no terminal op rides behind it.
            self._client.hand_off_delivery()
            self._closed_status = status
            return {"finish_queued": False, "delivered": 0, "remaining": pending_count}
        ended_at = _now()
        # The close is queued behind the run's data, but this process is done
        # with the run: the daemon hears it now (fire-and-forget).
        from . import daemon_channel

        daemon_channel.run_ended(self.id, status)
        beacon_tags: list | None = None
        # A queued tag write makes the beacon unsafe. `set_tags` REPLACES the
        # whole list, so under async the caller's tags may be sitting in the
        # queue while the server still holds the old ones. Reading the server
        # here would capture that stale list, and FIFO replay then lands the
        # queued write FIRST and this restore SECOND -- silently reverting a
        # tag change the caller made before closing. Skip the beacon entirely
        # in that case: a missing "draining" hint costs a dashboard some
        # nuance for the length of the drain, while the clobber loses data.
        if not beacon or self._has_queued_tag_write():
            return self._queue_terminal_op(
                status, summary, pending_count, ended_at, None, accounting=accounting
            )
        try:
            row = self._client.get_run(self.id)
            current = [t for t in (row.get("tags") or []) if t != "draining"]
            self._client.transport.request(
                "PATCH",
                f"/v1/runs/{self.id}",
                json_body={"tags": [*current, "draining"]},
            )
            beacon_tags = current
        except Exception:  # noqa: BLE001 -- the beacon is best-effort by definition
            beacon_tags = None
        return self._queue_terminal_op(
            status, summary, pending_count, ended_at, beacon_tags, accounting=accounting
        )

    def _draining_beat(self, *, draining: bool = True) -> None:
        """One synchronous lease beat saying this writer is finishing (2.8),
        or (``draining=False``) registering it and learning the run's rules.
        Best-effort and bounded (`_CLOSE_BEAT_SECONDS`; the registering beat
        also inside any close's own deadline, the draining one given at least
        `_DRAINING_BEAT_MIN_SECONDS` of its own): nothing informs a server
        without a network, and the lease then simply expires."""
        from .transport import deadline_remaining, deadline_scope, fresh_deadline_scope

        lease = self._lease or {}
        body = {k: v for k, v in lease.items() if k != "session_id"}
        body.update({"write_epoch": self.write_epoch or 1, **self._progress.snapshot()})
        if getattr(self, "attached", False):
            body["attached"] = True
        if draining:
            body["draining_for_seconds"] = _LEASE_DRAIN_SECONDS
            # What is left of the close's budget, but never under
            # `_DRAINING_BEAT_MIN_SECONDS`: a nested `deadline_scope` would keep
            # the close's spent deadline and raise before sending.
            left = deadline_remaining(_CLOSE_BEAT_SECONDS)
            scope = fresh_deadline_scope(
                time.monotonic() + max(left, _DRAINING_BEAT_MIN_SECONDS)
            )
        else:
            scope = deadline_scope(time.monotonic() + _CLOSE_BEAT_SECONDS)
        try:
            with scope:
                resp = self._client.beat_writer(self.id, lease["session_id"], body)
            self._note_lease_answer(resp)
        except Exception:  # noqa: BLE001 -- a liveness hint, never a reason a close fails
            pass

    def _has_queued_tag_write(self) -> bool:
        """Whether this run has a PATCH carrying `tags` still in the queue.

        `set_tags` replaces the WHOLE list, so a queued one and a server read
        disagree by construction, and FIFO makes the queued write land first.
        Anything derived from the server's current tags is therefore stale the
        moment one is pending.
        """
        try:
            for op in self._queued_ops(self._client.journal.pending()):
                if op.get("method") == "PATCH" and "tags" in (op.get("body") or {}):
                    return True
        except Exception:  # noqa: BLE001 -- a probe may never break a close
            return True  # unknown means assume conflict; skipping the beacon is cheap
        return False

    def _promote_uploads_before_close(self, *, strict: bool, timeout: float | None = None) -> list[str]:
        """Turn this run's waiting uploads into queued ops (see
        `Journal.promote_waiting`) within ``timeout``; returns the ones still
        waiting that hold the close. ``strict`` raises when one cannot be
        prepared; otherwise the close stays fail-open, as `set_status` promises
        -- a close must never replace the traceback of a run that is failing --
        and the caller counts them as undelivered: a close queued behind them
        waits for them (the drain holds a run's later ops behind its waiting
        uploads)."""
        if timeout is None:
            # Inside a close's `deadline_scope` (the terminal `set_status` that
            # finish() makes), what is left of that deadline bounds this too.
            from .transport import deadline_remaining

            timeout = deadline_remaining(WAITING_PROMOTE_TIMEOUT)
        stuck = self._client.journal.promote_for_close(
            self.id, timeout=max(0.0, min(WAITING_PROMOTE_TIMEOUT, timeout))
        )
        if stuck and strict:
            raise errors.RosError(
                f"run {self.id} not closed: {len(stuck)} queued upload(s) could not be "
                "prepared for delivery (credential scan) — see `probe outbox status`, "
                "then close again"
            )
        return stuck

    def _queue_terminal_op(
        self,
        status: str,
        summary: dict | None,
        pending_count: int,
        ended_at: str,
        beacon_tags: list | None,
        *,
        accounting: dict | None = None,
    ) -> dict:
        """Journal the terminal PATCH behind this run's queued ops."""
        block: dict[str, Any] = {
            **(accounting or {}),
            "deferred": True,
            "ended_at": ended_at,
            "pending_at_exit": pending_count,
            "session_id": self.session_id,
        }
        body: dict[str, Any] = {
            "status": status,
            "ended_at": ended_at,
            **_summary_wire(_with_finish_accounting(summary, block)),
        }
        leased = self._leased()
        if leased:
            # 2.8: the verdict is the lease release queued right behind this
            # PATCH; the server sets `status` when the leases say the run ended.
            del body["status"]
        if beacon_tags is not None:
            body["tags"] = beacon_tags  # clears "draining" atomically with the flip
        if self.write_epoch is not None:
            # 1.10: this op can land long after a relaunch took the run over;
            # the epoch is what lets the server refuse it then.
            body["write_epoch"] = self.write_epoch
        try:
            # `admitted`: the close skips the queue-length cap. A run whose
            # writes were dropped at the cap still has a near-full queue here,
            # and the cap refusing its close lost both the verdict and the
            # `dropped_writes` marker (review of #2014). One small op.
            if not leased or self._owns_run_fields():
                self._client.journal.append_http(
                    "PATCH", f"/v1/runs/{self.id}", body, run_ref=self.id, admitted=True
                )
            if self._lease is not None:
                # Leased: the verdict. On a run that is not `leases` the PATCH
                # above keeps its `status` (HIGH-1) and this marks the lease
                # released behind it.
                session = self._lease["session_id"]
                self._client.journal.append_http(
                    "POST",
                    f"/v1/runs/{self.id}/writers/{session}/release",
                    self._release_body(status),
                    run_ref=self.id,
                    admitted=True,
                )
            self._closed_status = status
        except Exception as exc:  # noqa: BLE001 -- a close never raises over its bookkeeping
            # Nowhere left to record the verdict: the server did not take the
            # data in time and the outbox cannot take the close (read-only,
            # full). Raising here would turn a finished run into a crashed
            # script at its last line. Say so; the run stays open until the
            # server's reaper closes it, and whatever data IS queued is still
            # handed to the worker below.
            _diagnostics.warn(
                f"probe: run {self.id} could not be closed: the server did not take "
                f"its last {pending_count} write(s) in time and the outbox cannot "
                f"record the close ({_diagnostics.describe(exc)}). The server will "
                "close the run when it goes quiet. See `probe outbox status`.",
                stacklevel=3,
            )
            try:
                self._client.hand_off_delivery()
            except Exception:  # noqa: BLE001
                pass
            return {
                "finish_queued": False,
                "delivered": 0,
                "remaining": pending_count,
                "close_unrecorded": True,
            }
        # The in-process exporter dies with this (exiting) process; hand the
        # journal to the crash-surviving detached worker instead. One shared
        # helper, because this site and `_settle_journaled_finish` used to be
        # near-duplicates and only one of them got fixed.
        self._client.hand_off_delivery()
        if leased:
            # AFTER the verdict is on disk: bounded, best-effort.
            self._draining_beat()
        return {"finish_queued": True, "delivered": 0, "remaining": pending_count + 1}

    def _close_on_interrupt(self, status: str, summary: dict | None, *, strict: bool) -> None:
        """Ctrl-C landed inside the close. Whatever of this run is on disk
        stays there; make sure the run still gets its verdict and something
        delivers it, then let the interrupt propagate.

        Only local work: journal the terminal status behind the queued data (no
        beacon -- that is a network round trip the person just asked to skip)
        and hand the journal to the detached worker. A strict close queues no
        verdict (it promises not to close over undelivered data), but still
        hands off the data. Never raises: the caller re-raises the interrupt.
        """
        try:
            if getattr(self, "_closed_status", None) is None and not strict:
                pending = len(self._client.journal.run_ops(self.id).pending())
                report = self._queue_deferred_finish(status, summary, pending, beacon=False)
                self._finish_result = report
                self._release_run_lock()
            else:
                self._client.hand_off_delivery()
        except BaseException:  # noqa: BLE001 -- the interrupt is what must propagate
            pass

    def _latest_terminal_patch(self) -> tuple[str, Any] | None:
        """``("pending" | "failed", path)`` for this run's NEWEST queued
        terminal-status PATCH, or None. Op filenames sort by enqueue time."""
        journal = self._client.journal
        best: tuple[str, Any] | None = None
        for where, rows in (("pending", journal.pending()), ("failed", journal.failed())):
            for path, op in rows:
                terminal = (
                    op.get("method") == "PATCH"
                    and (op.get("body") or {}).get("status") in _TERMINAL_STATUSES
                ) or (
                    # 2.8: a leased handle's terminal op is its lease release.
                    op.get("method") == "POST"
                    and str(op.get("path") or "").endswith("/release")
                )
                if (
                    op.get("run_ref") == self.id
                    and terminal
                    and (best is None or path.name > best[1].name)
                ):
                    best = (where, path)
        return best

    def _settle_journaled_finish(
        self, *, strict: bool, deadline: float | None = None, dropped: bool = False
    ) -> dict:
        """The terminal PATCH fail-opened into the journal instead of landing.

        `set_status` no longer raises on a transport failure, which is what
        keeps a blip from killing a training process -- but the run is then not
        closed server-side yet, and returning the caller a bare None would be
        the very "closed 'completed' over silently missing data" that the
        barrier exists to prevent. So: drain once more (within what is left of
        the close's ``deadline``), then say plainly which of the two happened,
        in the same shape a deferred finish reports.

        Judged by the TERMINAL PATCH itself, never by the run's dead letters in
        general: a default close now proceeds past DATA dead letters (it marks
        them on the run), and counting those read a close that had landed as
        "the terminal status was rejected" (review of #2011). A rejected close
        raises only under ``strict``; otherwise it warns and the server's reaper
        closes the run. Whatever of the run is still queued is handed to the
        detached worker either way.

        The run lock is NOT released while anything is queued: the close has
        not been confirmed, and holding the lock slightly too long is the cheap
        failure.

        ``dropped``: the terminal PATCH did not even reach the journal (an
        unwritable outbox). The close is then reported ``close_unrecorded``,
        never as delivered, and the server's reaper closes the run (review of
        #2014, H5b).
        """
        journal = self._client.journal
        if dropped and self._latest_terminal_patch() is None:
            _diagnostics.warn(
                f"probe: run {self.id} could not be closed: the server did not take its "
                "status in time and the outbox cannot record it. The server will mark the "
                "run crashed once it goes quiet (about 15 minutes; a run over 3 hours also "
                "sends a crash email). See `probe outbox status`."
            )
            self._client.hand_off_delivery()
            return {
                "finish_queued": False,
                "delivered": 0,
                "remaining": len(self._queued_ops(journal.pending())),
                "close_unrecorded": True,
            }
        left = None if deadline is None else max(0.0, deadline - time.monotonic())
        try:
            # Scoped, like the loop in finish(): this drain exists to land THIS
            # run's fail-opened terminal PATCH. The lock wait and the promotion
            # are bounded by the close's deadline, like every other wait in it.
            self._client._drain_for_close(self.id, lock_timeout=left)
        except Exception:  # noqa: BLE001 -- drain records last_error itself
            pass
        terminal = self._latest_terminal_patch()
        remaining = len(self._queued_ops(journal.pending()))
        if remaining:
            # Wake delivery. The op arrived through the sync fail-open branch,
            # which -- unlike the async branch -- does NOT call `_after_enqueue`,
            # so nothing has kicked a drainer. `Run.__exit__` usually exits the
            # process immediately after this, so without the handoff the close
            # sits on disk until some unrelated future `probe` command. See
            # `Client.hand_off_delivery` for why this is gated on the transport
            # and why a dead exporter is not cleared.
            self._client.hand_off_delivery()
        if terminal is not None and terminal[0] == "failed":
            message = (
                f"run {self.id} not closed: the terminal status was rejected and "
                "dead-lettered — see `probe outbox status`, then `probe outbox retry`"
            )
            if strict:
                raise errors.RosError(message)
            _diagnostics.warn(f"probe: {message}. The server will close the run when it goes quiet.")
            return {
                "finish_queued": False,
                "delivered": 0,
                "remaining": remaining,
                "close_rejected": True,
            }
        if not remaining:
            self._release_run_lock()
        return {
            "finish_queued": bool(remaining),
            "delivered": 0 if remaining else 1,
            "remaining": remaining,
        }

    def _warn_if_capture_incomplete(self) -> None:
        """Completion warning, never a gate (maintainer decision 2026-08-06):
        an incomplete capture makes the record honest about itself at the one
        moment someone claims success -- but nothing, opt-in or otherwise, may
        block a run. PROBE_AUTO_SNAPSHOT=0 means capture was declined; a
        warning would be nagging about a choice, so it is silent too.
        Placed after the journal drain so it never fires on writes this very
        finish() is about to deliver (the async_writes false-positive)."""
        try:
            result = self._client.check_run(self.id)
        except BaseException:  # noqa: BLE001
            return  # a completeness probe must never break a close-out
        # Everything below is diagnostics, and all of it used to be able to kill
        # the run it was describing. The warn raised under `-W error`, and the
        # `", ".join(...)` sat OUTSIDE the guard above, so a backend answering
        # `missing` with objects or nulls raised TypeError -- either one turning
        # a SUCCESSFUL twelve-hour run into a failure at its closing brace, on
        # the clean path, against the explicit rule two lines up that nothing
        # may block a run.
        try:
            state = result.get("state")
        except BaseException:  # noqa: BLE001
            return
        if state == "incomplete":
            missing = _diagnostics.join(result.get("missing"))
            _diagnostics.warn(
                "run may not be reproducible -- capture incomplete: "
                f"{missing}. See `probe run check {self.id}` for the full audit.",
                stacklevel=3,
            )

    def finish(
        self,
        status: str = "completed",
        *,
        summary_metrics: dict | None = None,
        summary: dict | None = None,
        flush_timeout: float | None = None,
        strict: bool | None = None,
    ):
        """Close the run. Outside ``strict`` it NEVER raises over delivery.

        This run's journaled writes are drained, retried with backoff, to ONE
        deadline -- ``flush_timeout``, else ``PROBE_FINISH_TIMEOUT_SEC``, else
        600 s (`FINISH_TIMEOUT_DEFAULT_SECONDS`) -- that bounds everything the
        close does: upload promotion, the drain-lock wait, each request, the
        final status write (plan 0.2/0.6). Then:

        * everything delivered: the terminal status is written and the run
          row returned -- as before;
        * writes still undelivered at the deadline: they stay durable on disk,
          the terminal status is journaled BEHIND them
          (``_queue_deferred_finish``, stamped ``probe_finish.deferred``), a
          warning names the count, and a report ``{finish_queued, delivered,
          remaining}`` is returned instead of the row. FIFO is the correctness
          guarantee: the run can never read terminal ahead of its own data;
        * writes the server permanently rejected (dead letters): a warning, and
          the run closes with ``probe_finish.dead_lettered = N`` on it, so a
          ``completed`` run with missing data says so on the RECORD, not only
          on a terminal that has scrolled away;
        * writes this client DROPPED before they reached the outbox (full, or
          unwritable -- `Client.dropped_writes`): a warning, and
          ``probe_finish.dropped_writes = N`` on the run the same way (plan 0.1).

        So a run with undelivered or dead-lettered data never reads
        ``completed`` without ``probe_finish.deferred`` or
        ``probe_finish.dead_lettered``. Red team's original finding -- finish()
        "used to discard the drain outcome and close 'completed' over silently
        missing data" -- is answered by the marker, not by refusing to close:
        refusing broke the standing rule that nothing may block a run
        (maintainer decision 2026-08-06, `_warn_if_capture_incomplete`; argued
        in design PR #1680), and live it failed 4 of 6 ten-step runs on one
        503 from a colliding write.

        ``strict`` (default: the client's ``not fail_open``) keeps the old
        barrier for a caller who wants delivery or an exception: dead letters
        raise at once, anything still undelivered at the deadline raises, and
        the run is NOT closed. `probe run end` is the CLI's barrier.

        A completion WARNING (never a gate) fires when ``status == "completed"``
        and capture was not opted out (``PROBE_AUTO_SNAPSHOT`` != ``"0"``). A
        run finishing "failed" (the body already raised, or the caller is
        being honest about a bad outcome) never warns -- there is no claim of
        completeness to caveat, and ``Run.__exit__`` depends on this so a
        body's real exception is never masked by a capture warning on the way
        out.

        The warning's ``check_run`` reads the run BUNDLE -- a plain GET,
        never the journal -- so under ``async_writes`` the env_ref PATCH and
        code-snapshot artifact ``snapshot()`` just journaled are not yet
        server-visible. The check must observe the very capture this finish()
        is about to claim, so it runs AFTER the drain (below), never before:
        checking first would make a spurious warning fire on data that is
        durable on disk and about to be delivered, not actually missing.
        """
        # IDEMPOTENT (review of #2011). `with probe.init() as run:` closes the
        # run in `Run.__exit__` and the atexit hook used to close it AGAIN --
        # two full deadlines at exit during an outage, and two terminal PATCHes
        # queued. A repeat returns what the first close returned. A close that
        # raised before sending any verdict (strict) stays retryable.
        #
        # A close ALREADY RUNNING in another thread (a watchdog, a second
        # `probe.finish()`) is waited for, up to what is left of its deadline,
        # and its answer returned. Returning at once let `fluent.finish` close
        # the client the first close was still sending through, and its
        # terminal write then raised "the client has been closed" (re-review
        # of #2011). The SAME thread re-entering (a signal handler that calls
        # `probe.finish()` mid-close) cannot wait on itself: it gets
        # ``{"finish_in_progress": True}`` and `fluent.finish` then leaves the
        # client alone.
        lock = self.__dict__.setdefault("_finish_lock", threading.Lock())
        # A SIGTERM is ending this process (`preempt`): whoever closes -- the
        # handler's worker, a `with` block's exit, a `finally`, atexit -- the
        # run ends `failed`, marked preempted, within the SIGTERM's budget.
        preempted = _preempt.ending()
        with lock:
            previous = getattr(self, "_finish_result", _UNSET)
            if previous is _UNSET:
                if preempted is not None:
                    status = "failed"
                    flush_timeout = preempted.close_timeout(
                        self._resolve_finish_timeout(flush_timeout)
                    )
                timeout = self._resolve_finish_timeout(flush_timeout)
                self._finish_result = _FINISHING
                self._finish_done = threading.Event()
                self._finish_thread = threading.get_ident()
                self._finish_deadline = time.monotonic() + timeout
        if previous is _FINISHING:
            done = getattr(self, "_finish_done", None)
            if done is not None and getattr(self, "_finish_thread", None) != threading.get_ident():
                left = max(0.0, (self._finish_deadline or 0.0) - time.monotonic())
                done.wait(left + _CLOSE_RESERVE_SECONDS)
            result = self._finish_result
            return {"finish_in_progress": True} if result is _FINISHING else result
        if previous is not _UNSET:
            return previous
        close_summary = _one_summary(summary_metrics, summary)
        if preempted is not None:
            close_summary = _with_finish_accounting(close_summary, preempted.facts())
            if preempted.exit_code is not None:
                # How the process is about to die, where the crash email and
                # the killed-by-signal detector read it: a NEGATIVE code is
                # "died on that signal" there (`-15` -> "stopped after
                # receiving SIGTERM"), as for a launcher's child. The 143 a
                # shell reports rides in `probe_finish`. Before the close, like
                # every exit span.
                from . import fluent

                fluent._write_exit_span(
                    self, -preempted.signum, "signal", status, extra=preempted.facts()
                )
        try:
            result = self._close(
                status,
                summary=close_summary,
                flush_timeout=timeout,
                strict=strict,
            )
        except BaseException:
            if self._finish_result is _FINISHING:
                # Nothing was closed or queued: a later finish() may try again.
                # Otherwise the verdict went out; a repeat returns None.
                self._finish_result = (
                    _UNSET if getattr(self, "_closed_status", None) is None else None
                )
            self._finish_done.set()
            if self._finish_result is not _UNSET:
                self._settled()
            raise
        self._finish_result = result
        self._finish_done.set()
        # Delivery trouble held back by the notices' 5-minute limit, said once
        # at the close (plan 1.7). Never raises.
        notices = getattr(self._client, "_notices", None)
        if notices is not None:
            notices.summary()
        # And the process's delivery counts, to our telemetry (plan 1.12).
        report = getattr(self._client, "_report_delivery", None)
        if report is not None:
            report(final=True)
        # Last: it may close this run's client (a `create_new` run's).
        self._settled()
        return result

    def _settled(self) -> None:
        """This handle's close is over: run the one `_after_finish` callback."""
        from . import _open_runs

        # One run fewer open here: workers may be bound to the one left (F5).
        _open_runs.closed(self)
        callback, self._after_finish = getattr(self, "_after_finish", None), None
        if callback is not None:
            try:
                callback()
            except Exception:  # noqa: BLE001 -- bookkeeping after a close never raises
                pass

    def _close(
        self,
        status: str,
        *,
        summary: dict | None,
        flush_timeout: float | None,
        strict: bool | None,
    ):
        """`finish()`'s body, run at most once per handle (see `finish`)."""
        # ONE deadline, taken FIRST, for everything the close does (plan 0.6):
        # the lineage and hardware finalizers below, capture, promotion, the
        # drain, and the terminal write.
        timeout = self._resolve_finish_timeout(flush_timeout)
        strict = (not self._client.fail_open) if strict is None else bool(strict)
        close_started = time.monotonic()
        deadline = close_started + timeout
        # `set_status` already sent this run's verdict (`execute()`'s finalize,
        # `probe run end`, a caller's own call): the close below still runs --
        # crumb, lineage, hardware, capture, drain -- and only the terminal
        # write is skipped (`_close_within`).
        verdict_sent = getattr(self, "_closed_status", None) is not None
        # `_close_within` keeps `_close_reserve(timeout)` back for the drain
        # and the terminal write: `_close_finalize`'s own local-only work must
        # never spend it (see `_close_reserve`).
        finalize_ceiling = deadline - _close_reserve(timeout)
        try:
            self._close_finalize(deadline, finalize_ceiling)
        except (KeyboardInterrupt, SystemExit) as interrupt:
            # A Ctrl-C (or a SystemExit) BEFORE the drain started: the
            # finalizers can take seconds (hashing the files the run read,
            # joining the hardware collector), and an interrupt there
            # left no status queued at all, so the run sat `running` until the
            # reaper called it crashed (lane E, building on #2011). Nothing was
            # delivered and the lineage/hardware tail was cut short, so the
            # verdict is the interrupt's own -- `canceled` for Ctrl-C, a
            # SystemExit's code otherwise -- queued behind the data and handed
            # to the worker like the later window below.
            self._close_on_interrupt(
                self._interrupted_status(interrupt, status), summary, strict=strict
            )
            # Cut short before it stopped the hardware collector (read capture
            # hashing comes first): it must not go on sampling a closed run.
            monitor = getattr(self, "_hw_monitor", None)
            if monitor is not None:
                try:
                    monitor.request_stop()
                except BaseException:  # noqa: BLE001 -- the interrupt must propagate
                    pass
            raise
        # A Ctrl-C during the close (it may wait up to the deadline) must not
        # leave the run with no terminal status queued and nothing handed to
        # the worker: the reaper would call it `crashed` (review of #2011).
        # SystemExit too: Lightning turns SIGTERM into a code-less SystemExit,
        # and a preempted job must still queue its verdict (re-review of #2011).
        try:
            return self._close_within(
                status,
                summary,
                strict=strict,
                timeout=timeout,
                deadline=deadline,
                verdict_sent=verdict_sent,
            )
        except (KeyboardInterrupt, SystemExit):
            # Once the terminal write is on its way the server may already have
            # applied it, and the response is what the interrupt cut off. The
            # status queued then is THAT one again -- an idempotent replay (the
            # server acts on a status only when it changes) -- never a
            # different one: a reinit's `canceled` queued there landed later
            # and overwrote the `completed` already applied (review of #2016).
            sent = getattr(self, "_terminal_in_flight", None)
            self._close_on_interrupt(
                sent or getattr(self, "_status_on_interrupt", None) or status,
                summary,
                strict=strict,
            )
            raise

    def _interrupted_status(self, interrupt: BaseException, requested: str) -> str:
        """The verdict for a close interrupted before it delivered anything:
        read the way `Run.__exit__` reads an ending. Ctrl-C is ``canceled``;
        a SystemExit is its code, and a clean one (Lightning's code-less
        SIGTERM) takes what `note_exit` recorded, else the status asked for.
        A close its caller did not choose (a reinit closing the previous run)
        sets `_status_on_interrupt`, which wins in both windows."""
        override = getattr(self, "_status_on_interrupt", None)
        if override:
            return override
        if isinstance(interrupt, KeyboardInterrupt):
            return "canceled"
        verdict, _ = _status_for_system_exit(
            getattr(interrupt, "code", None), interrupt.__context__
        )
        if verdict != "completed":
            return verdict
        noted = getattr(self, "_noted_exit", None)
        return noted[0] if noted else requested

    def _close_finalize(self, deadline: float, finalize_ceiling: float | None = None) -> None:
        """The close's local finalizers, before any delivery (see `_close`).

        ``finalize_ceiling`` (defaults to ``deadline``) bounds the LOCAL-only
        waits below (lineage hashing, the hardware collector): never the raw
        ``deadline``, so they cannot spend the reserve `_close_within` keeps
        for the drain and the terminal write (`_close_reserve`)."""
        from .transport import deadline_scope

        if finalize_ceiling is None:
            finalize_ceiling = deadline

        with deadline_scope(deadline):
            # Plan (f): rows held by `log(commit=False)` go out first, so the
            # drain below delivers them before the close. Never raises. Inside
            # the deadline: under sync writes this is a request, and outside it
            # a hung API held the close for the transport's own timeout (30 s)
            # before the deadline started (review of #2016). One that runs out
            # of time is journaled like any failed sync write, so it stays
            # queued ahead of the close.
            self._flush_pending_rows()
            # Disarm the hard-exit breadcrumb HERE, not in fluent.finish: every
            # close funnels through this method, including Run.__exit__ from the
            # `with probe.init(...) as run:` form the docs advertise. Reaching
            # finish() at all is this process saying it is closing its own run,
            # which is the exact negation of the crumb's claim.
            try:
                from . import diagnostics

                diagnostics.disarm(self._client, self.id)
            except Exception:  # noqa: BLE001 -- a breadcrumb must never gate a close
                pass
            # Same statement as the disarm above, one layer out: reaching finish()
            # is this process closing its own run, so a watcher on this box has
            # nothing left to explain about it. Left registered, the entry would
            # become a vanished pid the moment the interpreter exits -- and a
            # "process disappeared" note on a run that closed itself cleanly is
            # exactly the false alarm this whole design exists to avoid.
            self._deregister_with_node_agent()
            # The resume guard's final counts (plan 2.4), queued before the drain.
            self._close_resume_span()
            # The files this run read (lineage): collected, hashed and journaled as
            # NON-blocking ops before the drain, so they ride the same flush but can
            # never hold the close.
            try:
                from . import inputs as _inputs

                if _inputs.is_recording(self.id):
                    # Its wait for hashing is local, so no request deadline
                    # bounds it: at most half of what is left of
                    # `finalize_ceiling` -- never the raw deadline, or a short
                    # close (a reinit's 10 s) spent it all on hashing and
                    # queued every write (review of #2016), or under
                    # contention spent it all WAITING and left the drain no
                    # reserve at all (review of the read/write capture flake).
                    _inputs.finalize(
                        self._client,
                        self.id,
                        wait_s=min(
                            _inputs.FINISH_WAIT_S,
                            0.5 * max(0.0, finalize_ceiling - time.monotonic()),
                        ),
                    )
            except Exception:  # noqa: BLE001 -- lineage evidence never gates a close
                pass
            # Stop the hardware collector first: its final windows emit (or drop —
            # best-effort) before the close; it must never block or fail the close.
            # Within at most half of what is left of `finalize_ceiling`, like the
            # hashing wait above: a collector stuck in a hung driver call is
            # abandoned, never waited on past it, and the drain and the
            # terminal write keep time of their own (review of #2016 and of
            # the read/write capture flake).
            monitor = getattr(self, "_hw_monitor", None)
            if monitor is not None:
                try:
                    monitor.finish(timeout=0.5 * max(0.0, finalize_ceiling - time.monotonic()))
                except Exception:  # noqa: BLE001
                    pass
                self._hw_monitor = None

    def _close_within(
        self,
        status: str,
        summary: dict | None,
        *,
        strict: bool,
        timeout: float,
        deadline: float,
        verdict_sent: bool = False,
    ):
        from .transport import deadline_scope

        # The drain may run to the deadline minus a slice kept for the close
        # itself (the status write, or the deferred-close beacon). Computed
        # FIRST: capture and upload promotion below are local-only work like
        # `_close_finalize`'s, so they are bounded to this same reserve-aware
        # ceiling, never the raw deadline -- else they can spend the drain's
        # own reserve before the drain ever runs (`_close_reserve`).
        drain_deadline = deadline - _close_reserve(timeout)
        # D17's capture queues the run's log and sweeps its folder BEFORE the
        # drain, so the drain tries to deliver them before the terminal status;
        # they are non-blocking, so an outage leaves them queued and the run
        # still closes.
        self._finalize_capture(
            budget=min(_outputs.close_budget(), max(0.0, drain_deadline - time.monotonic()))
        )
        should_warn = status == "completed" and os.environ.get("PROBE_AUTO_SNAPSHOT", "1") != "0"
        # Uploads still waiting for their credential scan become ops FIRST, on
        # this thread if nobody else is at it -- the terminal status must queue
        # BEHIND this run's uploads, never ahead of them. Local CPU, but inside
        # the deadline like the rest.
        stuck = self._promote_uploads_before_close(
            strict=strict, timeout=max(0.0, drain_deadline - time.monotonic())
        )
        with deadline_scope(drain_deadline):
            pending, dead, delivered, auth_blocked = self._drain_until(
                drain_deadline, strict=strict
            )
        uploading = self._multipart_still_uploading()
        if uploading:
            # Plan (g). Never waited on while a detached worker on durable
            # storage will carry them after this process exits: said, and the
            # worker kicked. When nothing would -- a client that sends its own
            # writes (a token passed in code, drain_interval), an outbox on a
            # disposable disk -- sent now, within the close's budget, and what
            # does not make it is recorded as a reference row before this
            # returns: the run never ends with no record of the file.
            why = _multipart.settle_reason(self._client)
            if why is None:
                _diagnostics.warn(
                    f"probe: run {self.id} closing with {len(uploading)} artifact(s) still "
                    "uploading in the background; the outbox worker finishes them and each "
                    "is live once the server has verified it. See `probe outbox status`.",
                    stacklevel=4,
                )
                try:
                    self._client._after_enqueue()
                except Exception:  # noqa: BLE001 -- a kick never fails a close
                    pass
            else:
                try:
                    with deadline_scope(drain_deadline):
                        recorded = _multipart.settle_for_close(
                            self._client, uploading, drain_deadline, why=why
                        )
                except Exception:  # noqa: BLE001 -- the close goes on
                    recorded = 0
                if recorded:
                    _diagnostics.warn(
                        f"probe: run {self.id}: {recorded} artifact(s) did not finish uploading "
                        f"before the run closed ({why}); each is recorded as a reference to "
                        "its local file.",
                        stacklevel=4,
                    )
        undelivered = len(pending) + len(stuck)
        if dead and strict:
            # Deliberately BEFORE the raise is not where the lock is released:
            # a run that refuses to close is still open, and still has to keep
            # the box claimed against an upgrade.
            raise errors.RosError(
                f"run {self.id} not closed: {len(dead)} outbox op(s) are "
                "dead-lettered — waiting cannot heal a permanent rejection; see "
                "`probe outbox status`, then `probe outbox retry`"
            )
        if undelivered and strict:
            raise errors.RosError(
                f"run {self.id} not closed: {undelivered} outbox op(s) are "
                + (
                    f"undelivered: the server refused the credential ({WIZARD_HINT})"
                    if auth_blocked
                    else f"undelivered after {timeout:g}s"
                )
                + " — see `probe outbox status`, fix or `probe outbox retry`, then finish again"
            )
        # What the record must say about data that will never arrive (plan
        # 0.1/0.2): dead letters (the server refused them) and dropped writes
        # (they never reached the outbox at all).
        # The warnings that say so are printed AFTER the close, and say "marked"
        # only when the close carrying the marker was actually recorded.
        accounting: dict[str, Any] = {}
        if dead:
            accounting["dead_lettered"] = len(dead)
        dropped = max(
            0, int(getattr(self._client, "dropped_writes", 0) or 0) - self._dropped_baseline
        )
        if dropped:
            accounting["dropped_writes"] = dropped
        direct = max(
            0,
            int(getattr(self._client, "direct_sends", 0) or 0)
            - int(getattr(self, "_direct_baseline", 0) or 0),
        )
        if direct:
            accounting["direct_sends"] = direct
        if verdict_sent:
            return self._close_after_verdict(
                accounting, undelivered, delivered, auth_blocked, timeout, dead=dead
            )
        with deadline_scope(deadline):
            lost_with = self._preempted_outbox_goes_with_machine() if undelivered else None
            if lost_with is not None:
                return self._close_preempted_directly(
                    status, summary, undelivered, delivered, accounting, lost_with
                )
            if undelivered:
                # Writes are still pending past the deadline: the terminal
                # status is itself DEFERRED behind them (queued, not written
                # now), so there is no "completed" claim yet for the capture
                # warning to check against -- it applies on whatever later
                # drain actually finishes this run.
                why = (
                    "the server refused this machine's credential (401/403) -- "
                    f"{WIZARD_HINT}; the queued writes deliver once it is fixed"
                    if auth_blocked
                    else f"not delivered within {timeout:g}s; the background worker "
                    "will deliver them"
                )
                _diagnostics.warn(
                    f"probe: run {self.id} closing with {undelivered} write(s) still "
                    f"queued on disk: {why}, then mark the run {status} "
                    "(probe_finish.deferred). See `probe outbox status`.",
                    stacklevel=4,
                )
                report = self._queue_deferred_finish(
                    status, summary, undelivered, accounting=accounting
                )
                report["delivered"] = delivered
                report.update(accounting)
                self._warn_unrecoverable(accounting, recorded=self._close_recorded(report))
                # The writer is exiting by definition of a deferred finish; the
                # run's claim on the box goes with it.
                self._release_run_lock()
                return report
            # AFTER the drain, BEFORE the terminal write: the drain is what
            # makes the just-journaled env_ref PATCH + code-snapshot artifact
            # server-visible, so the check observes the real state rather than
            # a stale one that reads as incomplete.
            if should_warn:
                self._warn_if_capture_incomplete()
            close_summary = summary
            if accounting:
                close_summary = _with_finish_accounting(
                    summary, {**accounting, "session_id": self.session_id}
                )
            # From here an interrupt may land after the server applied this
            # status: `_close` queues this same status then, not another.
            self._terminal_in_flight = status
            dropped_before = int(getattr(self._client, "dropped_writes", 0) or 0)
            result = self.set_status(
                status, ended_at=_now(), summary=close_summary, sync=True, strict=strict
            )
            if result is None:
                settled = self._settle_journaled_finish(
                    strict=strict,
                    deadline=deadline,
                    dropped=int(getattr(self._client, "dropped_writes", 0) or 0) > dropped_before,
                )
                self._warn_unrecoverable(accounting, recorded=self._close_recorded(settled))
                return settled
        self._warn_unrecoverable(accounting, recorded=True)
        # ONLY on success, and deliberately not in a `finally`.
        #
        # If set_status raised, the run is not closed: the caller may catch the
        # error and keep training, and releasing here would hand auto-update a
        # green light over a live process. Holding costs nothing -- an flock is
        # bound to this process and the kernel frees it at exit regardless, so
        # the failure mode of keeping it is "protected slightly too long", while
        # the failure mode of dropping it is an upgrade landing mid-run.
        self._release_run_lock()
        return result

    def _preempted_outbox_goes_with_machine(self) -> str | None:
        """Why this close must not queue behind its undelivered writes: a
        SIGTERM is ending the process and the outbox is on a throwaway disk
        (`ephemeral`), so the queue -- and the worker that would drain it --
        goes with the machine. None otherwise, including when unknown."""
        if _preempt.ending() is None:
            return None
        try:
            from . import ephemeral

            where = ephemeral.describe(str(self._client.journal.dir))
        except Exception:  # noqa: BLE001 -- unknown: queue it, as any close
            return None
        if where.get("durable", True):
            return None
        return str(where.get("reason") or "a disposable disk")

    def _close_preempted_directly(
        self,
        status: str,
        summary: dict | None,
        undelivered: int,
        delivered: int,
        accounting: dict,
        lost_with: str,
    ) -> dict:
        """The close of a SIGTERMed run whose outbox dies with the machine:
        sent NOW, marking what will never arrive, instead of queued behind it
        (`_queue_deferred_finish`) for a worker that dies with the container
        -- or behind a draining lease beat that would keep a dead run live for
        an hour. What is still queued may yet go out before the machine does."""
        accounting = {**accounting, "undelivered": undelivered, "outbox": lost_with}
        close_summary = _with_finish_accounting(
            summary, {**accounting, "session_id": self.session_id}
        )
        preempted = _preempt.ending()
        if preempted is not None and preempted.exit_code is not None:
            # The exit span `finish()` queued sits behind that same data: sent
            # directly too (the same row, so a queued copy landing is harmless).
            from . import fluent

            fluent._write_exit_span(
                self, -preempted.signum, "signal", status, extra=preempted.facts(), direct=True
            )
        self._terminal_in_flight = status
        result = self.set_status(
            status, ended_at=_now(), summary=close_summary, sync=True, strict=False
        )
        _diagnostics.warn(
            f"probe: run {self.id} closed {status} on SIGTERM with {undelivered} write(s) "
            f"undelivered: the outbox is on {lost_with}, which goes with this machine "
            "(probe_finish.undelivered).",
            stacklevel=5,
        )
        self._warn_unrecoverable(accounting, recorded=getattr(self, "_closed_status", None) is not None)
        self._release_run_lock()
        return {
            "finish_queued": result is None,
            "delivered": delivered,
            "remaining": undelivered,
            **accounting,
        }

    def _close_recorded(self, report: dict) -> bool:
        """Whether the terminal status -- and the accounting it carries -- was
        written or queued, as opposed to refused or unrecordable."""
        return (
            getattr(self, "_closed_status", None) is not None
            and not report.get("close_unrecorded")
            and not report.get("close_rejected")
        )

    def _warn_unrecoverable(
        self,
        accounting: dict,
        *,
        recorded: bool,
        unmarked_because: str = "its close was not recorded either",
    ) -> None:
        """Say what of this run will never arrive, AFTER the close, and say it
        is marked on the run only when the close carrying the marker landed or
        was queued (review of #2014: a cap-refused close had already printed
        "marked")."""
        where = (
            "the run is marked {key}={n}"
            if recorded
            else f"the run could NOT be marked: {unmarked_because}"
        )
        dead = accounting.get("dead_lettered")
        if dead:
            _diagnostics.warn(
                f"probe: {dead} of run {self.id}'s writes were permanently rejected "
                "by the server (dead-lettered); "
                + where.format(key="probe_finish.dead_lettered", n=dead)
                + ". See `probe outbox status`, then `probe outbox retry`.",
                stacklevel=5,
            )
        dropped = accounting.get("dropped_writes")
        if dropped:
            _diagnostics.warn(
                f"probe: {dropped} write(s) for run {self.id} were dropped before they "
                "reached the outbox (full or unwritable, or logged while probe.init() was "
                "still opening this run -- see the earlier warning; "
                "counted in this process only); "
                + where.format(key="probe_finish.dropped_writes", n=dropped)
                + ". See `probe outbox status`.",
                stacklevel=5,
            )

    def _close_after_verdict(
        self,
        accounting: dict,
        undelivered: int,
        delivered: int,
        auth_blocked: bool,
        timeout: float,
        *,
        dead: list | None = None,
    ):
        """The end of a close whose verdict `set_status` had already sent.

        That verdict stands, so nothing terminal is written or queued here: a
        second terminal PATCH overwrote it with this call's guess (`execute()`
        closed a run `failed` from its child's exit code, and the `finish()`
        after it re-closed it `completed`). The rest of the close has run --
        crumb disarmed, lineage and hardware finalized, capture swept, this
        run's writes drained -- because returning early left the crumb armed,
        and the next `probe.init()` on the host then filed a `hard_exit` on a
        run that had closed cleanly (review of #2016). What could not be
        delivered stays queued for the detached worker, as after any close;
        dead letters and dropped writes are warned about, but cannot be
        marked on a run whose close already went out without them.

        "Sent" is checked, not assumed: a `set_status` that fail-opened into
        the journal only QUEUED its verdict, and the server may then refuse
        it for good. That close was rejected -- the run is still open, and the
        reaper will call it crashed -- and is reported as such, the way a
        `finish()` whose own terminal write was refused reports it
        (`_settle_journaled_finish`), never as a verdict already sent
        (review of #2016).
        """
        terminal = self._latest_terminal_patch()
        verdict = self._closed_status
        if terminal is not None and terminal[0] == "failed":
            # The dead letter IS the close; only the rest is data it lost.
            data_dead = [p for p in (dead or []) if p != terminal[1]]
            if data_dead:
                accounting["dead_lettered"] = len(data_dead)
            else:
                accounting.pop("dead_lettered", None)
            _diagnostics.warn(
                f"probe: run {self.id} not closed: the terminal status was rejected and "
                "dead-lettered — see `probe outbox status`, then `probe outbox retry`. "
                "The server will close the run when it goes quiet.",
                stacklevel=5,
            )
            if undelivered:
                self._client.hand_off_delivery()
            self._warn_unrecoverable(
                accounting, recorded=False, unmarked_because="its close was rejected too"
            )
            # Not released: the run is not closed (as in `_settle_journaled_finish`).
            return {
                "finish_queued": False,
                "delivered": delivered,
                "remaining": undelivered,
                "close_rejected": True,
                **accounting,
            }
        queued = terminal is not None  # still pending: queued, not yet sent
        if undelivered:
            why = (
                f"the server refused this machine's credential (401/403) -- {WIZARD_HINT}"
                if auth_blocked
                else f"not delivered within {timeout:g}s; the background worker will deliver them"
            )
            state = f"closing {verdict} (queued)" if queued else f"already {verdict}"
            _diagnostics.warn(
                f"probe: run {self.id} is {state}; {undelivered} of its write(s) are "
                f"still queued on disk: {why}. See `probe outbox status`.",
                stacklevel=5,
            )
            self._client.hand_off_delivery()
        self._warn_unrecoverable(
            accounting,
            recorded=False,
            unmarked_because=(
                f"its close ({verdict}) was already queued without the marker"
                if queued
                else f"its close ({verdict}) was already sent"
            ),
        )
        self._release_run_lock()
        if undelivered or accounting:
            return {
                "finish_queued": False,
                "delivered": delivered,
                "remaining": undelivered,
                **accounting,
            }
        return self._data

    def execute(
        self,
        argv: list[str],
        *,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
        finalize: bool = True,
        outputs: str | os.PathLike | None = None,
        capture_outputs: bool | None = None,
    ) -> subprocess.CompletedProcess:
        """Run a local command with deterministic run/process correlation.

        This is normal experiment execution capture, not the hook-only session
        API. Output streams pass through to the caller; a process span records
        argv, cwd, timestamps, and exit state.

        D17: the child's stdout/stderr are TEED -- to this process's own streams
        (a pty when those are a terminal, so the child still sees one) and to
        ``probe/run.log`` -- and the folder it works in (``cwd``, or ``outputs``) is
        swept when it exits. ``capture_outputs=False`` (or
        ``PROBE_CAPTURE_OUTPUTS=0``) turns both off. A handle whose own window
        is already open (``Client.run``) closes it here too, and tees nothing
        twice: the child inherits its streams. A submit-and-return launcher
        (``finalize=False``) captures nothing: the job's own ``probe.init()``
        does, wherever it runs. The child is told what this host captures
        (``PROBE_CAPTURE_OWNER``/``_ROOT`` for the folder,
        ``PROBE_CAPTURE_LOG_OWNER`` for its output) so a ``probe.init()`` inside
        it does not capture the same thing twice.
        """
        if not argv:
            raise ValueError("argv must not be empty")
        # Span attributes are persisted telemetry, not the launch mechanism --
        # they must carry the SAME scrubbed argv the launch block ships, never
        # the raw one. The raw argv is kept only for the actual subprocess
        # invocation and for `snapshot(argv=argv)` below, which scrubs
        # internally and needs the raw form for entrypoint detection.
        scrubbed_argv, _ = _launch.scrub_argv(list(argv))
        # Every executed run snapshots by default (design D3). detect_venv=True
        # because THIS interpreter is the launcher, not the environment being
        # recorded -- see Run.snapshot's docstring. Failure never blocks the
        # child: capture is never a gate, opt-in or otherwise (maintainer
        # decision 2026-08-06) -- it only ever warns.
        if os.environ.get("PROBE_AUTO_SNAPSHOT", "1") != "0":
            try:
                self.snapshot(cwd=cwd, detect_venv=True, argv=argv)
            except Exception as exc:
                warnings.warn(
                    f"auto-snapshot failed; run continues uncaptured: {exc}",
                    stacklevel=2,
                )
        started_at = _now()
        span_id = self.span(
            "process",
            name=os.path.basename(argv[0]),
            status="running",
            started_at=started_at,
            attributes={"argv": scrubbed_argv, "cwd": os.path.abspath(cwd or os.getcwd())},
        )
        # 0205. The EPOCH travels with the id. A run id names a row, not an
        # execution attempt: a stale process that still has the id would
        # otherwise attach to a row a newer attempt already reopened and inherit
        # its write authority. With the epoch in hand the server's 0185 fencing
        # (ensure_writer_epoch) refuses the old attempt at the door. Anything
        # forwarding these across a machine boundary -- Modal secrets, Ray
        # runtime_env, sbatch --export -- must carry BOTH.
        #
        # The agent session travels the same way (audit E2): a job that leaves
        # this machine has none of the agent's own variables, and without the
        # session its runs lose the tag the daemon finds them by. Locally it
        # changes nothing -- the agent's variables win wherever they exist.
        from . import agent_session

        # `existing`: a window this handle opened in-process (Client.run). It
        # closes with this command. `capture`: one for the command's own folder
        # when `existing` does not already sweep it. The log is teed here
        # unless `existing` already tees this process -- the child inherits it.
        existing = self._capture if finalize else None
        capture = None
        log_path = None
        if finalize and _outputs.enabled(capture_outputs):
            try:
                target = _outputs.target_root(outputs=outputs, cwd=cwd)
                if existing is None or not (existing.sweeps and _outputs._within(target, existing.root)):
                    capture = _outputs.OutputCapture.start(
                        self._client,
                        self.id,
                        outputs=outputs,
                        cwd=cwd,
                        tee=False,
                        launcher=True,
                        ignore=self._ignore_rules(cwd),
                        # The launcher's chunks name this handle's attempt.
                        epoch=_logstream.handle_epoch(self),
                    )
                    if self._capture is None:
                        self._capture = capture
                holder = capture or existing
                teed = existing is not None and existing._tee is not None
                if holder is not None and not teed and _outputs.log_enabled() and os.name == "posix":
                    log_path = _outputs.reserve_log_path(self.id)
                    holder.adopt_log(log_path)
            except Exception:  # noqa: BLE001 -- capture never stops the command
                pass
        process_env = {
            **os.environ,
            **agent_session.forwarding_env(),
            **(env or {}),
            "PROBE_RUN_ID": self.id,
            # Explicit either way: a submitted job (finalize=False) must not
            # inherit an outer `probe exec`'s value.
            EXEC_FINALIZES_ENV: self.id if finalize else "",
        }
        # Only an epoch this handle KNOWS travels. An inherited value names
        # some other run's generation, so it is removed rather than passed on.
        if self.write_epoch is not None:
            process_env["PROBE_RUN_EPOCH"] = str(self.write_epoch)
        else:
            process_env.pop("PROBE_RUN_EPOCH", None)
        # What the child reads (lineage). This process cannot see a child's
        # opens, so a Python child gets a small stdlib hook through an injected
        # `sitecustomize` and spools them; this launcher hashes and sends them
        # once the child exits. Only for a child it RUNS: a submitted job
        # (finalize=False) reads on another machine, where its own
        # `probe.init()` records. Never a gate.
        reads_child = False
        # `.probeignore` (plan (n)) for the directory the child runs in: its
        # reads are filtered with these after it exits (`_finalize_child_reads`),
        # or by a recovery if this launcher never collects them.
        self._child_ignore = self._ignore_rules(cwd)
        if finalize:
            try:
                from . import inputs as _inputs

                reads_child = _inputs.prepare_child(
                    self.id,
                    process_env,
                    client=self._client,
                    ignore=self._child_ignore,
                    capture_outputs=capture_outputs,
                )
            except Exception:  # noqa: BLE001
                reads_child = False
        # Tell the child what this host already captures, so its own
        # probe.init() does not capture it twice (R12).
        # Only a window that really sweeps may claim the folder: a log-only one
        # (`/`, a workspace too big to list) must leave a narrower
        # `probe.init(outputs=...)` in the child to sweep its own.
        sweeper = next((w for w in (capture, existing) if w is not None and w.sweeps), None)
        if sweeper is not None:
            process_env[_outputs.OWNER_ENV] = socket.gethostname()
            process_env[_outputs.ROOT_ENV] = sweeper.root
        if existing is not None and existing._tee is not None:
            process_env[_outputs.LOG_OWNER_ENV] = socket.gethostname()
        if capture_outputs is False:
            process_env[_outputs.CAPTURE_ENV] = "0"
        # `.probeignore` (plan (n)): the child uses THIS run's file even if it
        # changes directory, and sees the `ignore=` patterns too.
        if self._child_ignore is not None:
            if self._child_ignore.source_file:
                process_env[_ignore.ENV_FILE] = self._child_ignore.source_file
            if self._ignore_patterns:
                # In their own variable, one per line: through PROBE_IGNORE a
                # comma inside a pattern would split it in two. PROBE_IGNORE
                # itself is inherited as it is.
                process_env[_ignore.ENV_EXPORTED] = _ignore.join_lines(
                    [*_ignore.split_lines(process_env.get(_ignore.ENV_EXPORTED)), *self._ignore_patterns]
                )
        log_stats = None
        try:
            if log_path is not None:
                from .logcapture import run_teed

                result, log_stats = run_teed(
                    argv,
                    cwd=cwd,
                    env=process_env,
                    log_path=log_path,
                    # If this process dies first, the helper -- which outlives
                    # it -- recovers the log and the folder once the child ends.
                    recovery_entry=str(capture._entry) if capture is not None and capture._entry else None,
                    on_helper=capture.note_helper if capture is not None else None,
                    # Only once the tee is live: a child told its output is
                    # logged, when it is not, would keep no log at all.
                    teed_env={_outputs.LOG_OWNER_ENV: socket.gethostname()},
                )
            else:
                result = subprocess.run(argv, cwd=cwd, env=process_env, check=False)
        except BaseException as exc:
            if reads_child:
                self._finalize_child_reads(interrupted=True)
            if capture is not None:
                # Ctrl-C, or a launch failure: what the child wrote so far is
                # still this run's. Queued, then left to the detached drainer.
                try:
                    capture.finalize(log_path=log_path)
                    self._client._kick_drainer(force=True)
                except Exception:  # noqa: BLE001
                    pass
            self.span(
                "process",
                id=span_id,
                name=os.path.basename(argv[0]),
                status="failed",
                started_at=started_at,
                ended_at=_now(),
                attributes={"argv": scrubbed_argv, "cwd": os.path.abspath(cwd or os.getcwd())},
            )
            # Ctrl-C reaches the whole foreground process group, so the LAUNCHER
            # takes it too and lands here. The run was never closed: it sat
            # `running` until the reaper called it `crashed`, and a crash notice
            # went to the person who had just pressed Ctrl-C. KeyboardInterrupt
            # only -- a launcher that broke for its own reasons (a fork failure,
            # a bad argv) has no standing to call the run stopped on purpose.
            # `only_if_running`, like the finalize below: a job that closed
            # itself from inside already wrote the honest verdict.
            if finalize and isinstance(exc, KeyboardInterrupt):
                try:
                    self.set_status("canceled", only_if_running=True)
                except Exception:  # noqa: BLE001 -- the interrupt must still propagate
                    pass
            raise
        self.span(
            "process",
            id=span_id,
            name=os.path.basename(argv[0]),
            status="completed" if result.returncode == 0 else "failed",
            started_at=started_at,
            ended_at=_now(),
            attributes={
                "argv": scrubbed_argv,
                "cwd": os.path.abspath(cwd or os.getcwd()),
                "exit_code": result.returncode,
            },
        )
        # 0205. The launcher is the DESIGNATED FINALIZER for a wrapped run: it
        # is the only party holding the child's exit code. Before this, execute()
        # recorded the span and returned, so a wrapped run was never closed by
        # anyone -- it sat 'running' until the reaper, and with no beats the
        # reaper called it 'untracked'. A real exit code became a guess.
        #
        # GUARDED, because the child may have finished the run itself: a script
        # calling probe.init() ... finish() has already written the authoritative
        # verdict from inside the work, and the launcher must not overwrite it
        # with its own view. `only_if_running` makes this a no-op against any
        # row already terminal, so the child's verdict wins on arrival ORDER
        # being irrelevant -- whoever spoke first and meant it, stands.
        # finalize=False when this process SUBMITTED the work rather than running
        # it: a scheduler accepting a job says nothing about how the job ends,
        # and recording the submitter's exit code as the run's is exactly the
        # lie the hand-off path exists to avoid. The job's own probe.init()
        # owns the verdict there.
        if reads_child:
            self._finalize_child_reads()
        try:
            enqueued = False
            holder = capture or existing
            # ONE deadline for the whole close -- every window and the delivery.
            timeout = self._resolve_finish_timeout(None, default=None)
            deadline = None if timeout is None else time.monotonic() + max(timeout, 0.0)
            for window in (capture, existing):
                if window is None:
                    continue
                budget = None if deadline is None else min(
                    _outputs.close_budget(), max(0.0, deadline - time.monotonic())
                )
                try:
                    if window is holder:
                        window.finalize(log_path=log_path, log_stats=log_stats, budget=budget)
                    else:
                        window.finalize(budget=budget)
                except Exception:  # noqa: BLE001 -- the child's verdict is recorded regardless
                    pass
                enqueued = enqueued or bool(window.enqueued)
            if enqueued:
                self._deliver_captured(deadline)
        finally:
            # In a `finally`: a Ctrl-C during the sweep must not cost the run
            # the child's exit code.
            if finalize:
                self.set_status(
                    _status_for_exit(result.returncode),
                    only_if_running=True,
                )
        return result

    def _finalize_child_reads(self, *, interrupted: bool = False) -> None:
        """Send what the executed child read. Never raises. Interrupted, the
        launcher does not stop to hash: the child's spools stay, and the next
        run on this host sends them. A Ctrl-C during that hashing only skips
        it, as it always has here: the child has exited, and its exit code is
        what closes the run next."""
        try:
            from . import inputs as _inputs

            if interrupted:
                _inputs.abandon(self.id)
            else:
                _inputs.finalize(self._client, self.id, ignore=self._child_ignore)
        except (Exception, KeyboardInterrupt):  # noqa: BLE001
            pass

    def _deliver_captured(self, deadline: float | None) -> None:
        """Try to deliver captured outputs before the terminal status, like
        finish(), within what is left of the close's deadline. They are
        non-blocking: whatever does not land is left to the detached drainer."""
        while deadline is None or time.monotonic() < deadline:
            try:
                self._client.flush(run_ref=self.id)
            except Exception:  # noqa: BLE001 -- drain records last_error itself
                pass
            if deadline is None or not self._queued_ops_any(self._client.journal.pending()):
                break
            time.sleep(min(0.25, max(deadline - time.monotonic(), 0.0)))
        try:
            if self._queued_ops_any(self._client.journal.pending()):
                self._client.hand_off_delivery()
        except Exception:  # noqa: BLE001
            pass

    def _queued_ops_any(self, rows) -> bool:
        """Any op of this run still queued, blocking or not."""
        return any(op.get("run_ref") == self.id for _, op in rows)

    # -- context manager ----------------------------------------------------
    def __enter__(self) -> "Run":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        """Close the run, but never let closing it displace the body's failure.

        This block is the whole reason the campaign's workers died: `finish()`
        runs inside an exception handler, so anything it raises REPLACES the
        traceback the researcher actually needs. Making `set_status` fail-open
        fixed the transport case and then the dead-letter raise reopened it from
        a different direction -- a permanently rejected terminal PATCH (a 422,
        not a blip) turned `1/0` into "the terminal status was dead-lettered".

        So the rule lives here, once, where it cannot be reopened again: when
        the body already failed, a close failure is downgraded to a warning and
        the original exception propagates. An explicit `run.finish()` still
        raises -- there is no other error to protect, and a caller who asked to
        close deserves to hear that it did not happen.

        BaseException, not Exception. `finish()` sleeps and does blocking
        network I/O on an unbounded drain, so a Ctrl-C landing in it is not
        exotic -- it is the likely case: the body fails, finish() hangs on a
        dead API, the researcher interrupts, and the real error is gone. The
        warning itself goes through the non-raising channel, because the
        previous version of this handler used `warnings.warn` and reopened the
        bug a third time under `-W error`.
        """
        # The same reading of the ending as `fluent`'s process hooks, which
        # now stand down for a run this block closed: a SystemExit is its code
        # (`sys.exit(0)` is not a failure) and Ctrl-C is `canceled`, both when
        # it escapes the block and when it is in flight behind a SystemExit.
        cause: BaseException | None = None
        exit_code = 0
        if exc is None:
            status = "completed"
        elif (
            isinstance(exc, SystemExit)
            and exc.code is None
            and getattr(self, "_noted_exit", None) is not None
        ):
            # Lightning on SIGTERM: on_exception -> note_exit("failed", exc),
            # then a SystemExit with no code, which alone reads as success.
            status, noted = self._noted_exit
            if status == "failed":
                cause = noted
        elif isinstance(exc, SystemExit):
            status, exit_code = _status_for_system_exit(exc.code, exc.__context__)
            # Hydra's shape: the traceback it swallowed is the crash report,
            # never the SystemExit itself.
            if status == "failed" and isinstance(exc.__context__, Exception):
                cause = exc.__context__
        elif isinstance(exc, KeyboardInterrupt):
            status = "canceled"
        else:
            status, cause = "failed", exc
        if getattr(self, "_closed_status", None) is not None or self._finish_called():
            # The run was closed inside the block -- a second probe.init()
            # replaced it (reinit), or `run.finish()` / `set_status` ran. Its
            # verdict stands, and what ended the block after that is not its
            # ending: no exit code or crash report is filed on it (the
            # exception still propagates). finish() below returns the first
            # close's answer, or finishes the cleanup a bare set_status left.
            exit_code, cause = 0, None
        if exit_code:
            try:
                from . import fluent

                fluent._write_exit_span(self, exit_code, "SystemExit", status)
            except BaseException:  # noqa: BLE001 -- evidence is best effort
                pass
        if cause is not None:
            try:
                from . import diagnostics

                diagnostics.report_exception(self, cause)
            except BaseException:  # noqa: BLE001 -- even an interrupted report is best effort
                pass
        try:
            self.finish(status)
        except BaseException as close_error:  # noqa: BLE001
            if exc_type is None:
                raise
            _diagnostics.warn(
                f"run {self.id} did not close cleanly "
                f"({_diagnostics.describe(close_error)}); re-raising the "
                "original error from the with-block instead. See "
                "`probe outbox status`."
            )


#: One definition, shared with the anchored-upload path in sdk/client.py — the hash
#: is part of the wire contract, so two copies could silently diverge.
_fingerprint = fingerprint
