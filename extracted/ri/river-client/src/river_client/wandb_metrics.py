"""Experimental mirroring of W&B scalar logging into River Console.

``inject_metrics(model)`` is the only integration point. Call it once the River
model exists and immediately before ``wandb.init()``::

    model = session.create_model(...)
    river.inject_metrics(model)
    run = wandb.init(project="example")

Usage rules for the experiment:

* Inject before every ``wandb.init()`` whose metrics belong to that model; that
  call must create a new run object. Attaching to an already initialized run or
  injecting midway through training is unsupported.
* Do not overlap injections, initialize runs concurrently, or reuse one W&B run
  across River models.
* ``WANDB_MODE=disabled`` (or ``mode="disabled"``) also disables mirroring.
* ``RIVER_METRICS_DISABLED=1`` before injection turns injection into a no-op.

River mirroring never changes what W&B receives. Original W&B calls,
arguments, return values and errors are preserved; failures inside River's own
capture or delivery are contained and only reported as rate-limited warnings.
The one addition is a fallback for genuine operational W&B initialization
failures (unreachable service, authentication, timeout): ``wandb.init()`` then
returns W&B's own disabled run and River still records scalars.

Only finite Python/NumPy numeric scalars are mirrored. Tensors, arrays, nested
dictionaries and media are skipped.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import atexit
import functools
import importlib.util
import logging
import math
import numbers
import operator
import os
import tempfile
import threading
import time
from typing import Any
import uuid
import weakref

from river_client import metric_events
from river_client.metric_events import (
    MAX_BATCH_VALUES,
    MAX_DEFINITIONS_PER_REVISION,
    MAX_NAME_BYTES,
    warn_once,
)

_logger = logging.getLogger(__name__)

SUPPORTED_WANDB_VERSIONS = frozenset({"0.28.0"})
DISABLE_ENV = "RIVER_METRICS_DISABLED"
_WRAPPED = "__river_metrics_original__"

_state_lock = threading.Lock()
_pending: _Injection | None = None
_bindings: weakref.WeakKeyDictionary[Any, _Binding] = weakref.WeakKeyDictionary()
_hooks_installed = False


def inject_metrics(model: Any) -> None:
    """Mirror the next ``wandb.init()`` run's scalar logging to ``model``'s run.

    Never raises for instrumentation problems and performs no network request;
    without a supported W&B installation it does nothing.
    """
    try:
        _inject(model)
    except Exception:
        warn_once(
            "inject failed",
            "River metrics injection failed; W&B logging continues unchanged",
        )


@dataclass(frozen=True)
class _Injection:
    pid: int
    training_run_id: str
    api_key: str
    url: str


def _inject(model: Any) -> None:
    global _pending
    if os.environ.get(DISABLE_ENV, "").strip().lower() in {"1", "true", "yes", "on"}:
        _logger.info("River metrics mirroring disabled by %s", DISABLE_ENV)
        return
    if importlib.util.find_spec("wandb") is None:
        return
    import wandb

    version = getattr(wandb, "__version__", None)
    if version not in SUPPORTED_WANDB_VERSIONS:
        warn_once(
            "unsupported wandb",
            f"River metrics mirroring does not support wandb {version}; "
            f"supported: {', '.join(sorted(SUPPORTED_WANDB_VERSIONS))}",
        )
        return
    training_run_id = str(uuid.UUID(str(model.training_run_id)))
    api_key = model._session._client._api_key
    if not isinstance(api_key, str) or not api_key:
        warn_once("no api key", "River metrics mirroring needs a River API key")
        return
    url = metric_events.events_url(training_run_id)
    if url is None:
        warn_once(
            "unsafe url",
            "River metrics mirroring requires an HTTPS RIVER_CONSOLE_URL",
        )
        return
    with _state_lock:
        _install_hooks(wandb)
        if _pending is not None and _pending.pid == os.getpid():
            warn_once(
                "overlapping injection",
                "inject_metrics() was called again before wandb.init(); "
                "the latest model wins",
            )
        _pending = _Injection(os.getpid(), training_run_id, api_key, url)


def _take_pending() -> _Injection | None:
    global _pending
    # Check the owner before taking any lock: a forked child must never touch
    # state (or a lock) inherited from its parent.
    pending = _pending
    if pending is None or pending.pid != os.getpid():
        return None
    with _state_lock:
        pending, _pending = _pending, None
    return pending


def _reset_after_fork() -> None:
    global _state_lock, _pending
    _state_lock = threading.Lock()
    _pending = None


# Windows has no fork (and no os.register_at_fork).
if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_after_fork)


# ── Hooks ────────────────────────────────────────────────────────────────


def _install_hooks(wandb: Any) -> None:
    global _hooks_installed
    if _hooks_installed:
        return
    from wandb.sdk import wandb_run
    from wandb.sdk.lib import noop_run

    _wrap(wandb, "init", _init_hook)
    for cls in (wandb_run.Run, noop_run.NoopRun):
        _wrap(cls, "log", _log_hook)
        _wrap(cls, "define_metric", _define_metric_hook)
        # Run.finish, Run.__exit__ and W&B's exit teardown all go through
        # _finish; NoopRun.finish does not, so both are hooked there.
        _wrap(cls, "_finish", _finish_hook)
    _wrap(noop_run.NoopRun, "finish", _finish_hook)
    atexit.register(_close_all)
    _hooks_installed = True


def _wrap(owner: Any, name: str, make_hook: Any) -> None:
    original = owner.__dict__[name] if isinstance(owner, type) else getattr(owner, name)
    if getattr(original, _WRAPPED, None) is not None:
        return
    hook = functools.wraps(original)(make_hook(original))
    setattr(hook, _WRAPPED, original)
    setattr(owner, name, hook)


def _init_hook(original: Any) -> Any:
    def init(*args: Any, **kwargs: Any) -> Any:
        injection = _take_pending()
        if injection is None:
            return original(*args, **kwargs)
        try:
            run = original(*args, **kwargs)
        except Exception as error:
            fallback = _fallback_run(error, kwargs)
            if fallback is None:
                raise
            warn_once(
                "wandb init fallback",
                "wandb.init() failed; continuing with a disabled W&B run while "
                "River still records metrics",
            )
            _activate(injection, fallback, fallback=True)
            return fallback
        _activate(injection, run, fallback=False)
        return run

    return init


def _log_hook(original: Any) -> Any:
    def log(self: Any, *args: Any, **kwargs: Any) -> Any:
        result = original(self, *args, **kwargs)
        binding = _binding_for(self)
        if binding is not None:
            binding.capture_log(args, kwargs)
        return result

    return log


def _define_metric_hook(original: Any) -> Any:
    def define_metric(self: Any, *args: Any, **kwargs: Any) -> Any:
        result = original(self, *args, **kwargs)
        binding = _binding_for(self)
        if binding is not None:
            binding.capture_definition(args, kwargs)
        return result

    return define_metric


def _finish_hook(original: Any) -> Any:
    def finish(self: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            return original(self, *args, **kwargs)
        finally:
            binding = _binding_for(self)
            if binding is not None:
                binding.close()
                _forget(self)

    return finish


def _binding_for(run: Any) -> _Binding | None:
    """Return the live binding for ``run`` in this process, touching no locks."""
    try:
        binding = _bindings.get(run)
    except Exception:
        return None
    if binding is None or binding.pid != os.getpid():
        return None
    return binding


def _forget(run: Any) -> None:
    try:
        _bindings.pop(run, None)
    except Exception:
        pass


def _fallback_run(error: Exception, kwargs: Mapping[str, Any]) -> Any:
    """Build W&B's own disabled run after a genuine operational init failure."""
    try:
        from wandb import errors
        from wandb.sdk import wandb_settings
        from wandb.sdk.lib import noop_run, runid

        operational = (errors.CommError, errors.WandbCoreNotAvailableError, OSError)
        if not isinstance(error, operational):
            return None
        config = kwargs.get("config")
        run_id = runid.generate_id()
        # Mirrors W&B's own make_disabled_run(): no network, no run directory.
        return noop_run.init_noop_run(
            settings=wandb_settings.Settings(
                mode="disabled",
                root_dir=tempfile.gettempdir(),
                run_id=run_id,
                run_tags=(),
                run_notes=None,
                run_group=None,
                run_name=f"dummy-{run_id}",
                project="dummy",
                entity="dummy",
            ),
            config=dict(config) if isinstance(config, Mapping) else {},
        )
    except Exception:
        return None


def _activate(injection: _Injection, run: Any, *, fallback: bool) -> None:
    try:
        from wandb.sdk.lib import noop_run

        if not fallback and isinstance(run, noop_run.NoopRun):
            _logger.info("W&B is disabled; River metrics mirroring is inactive")
            return
        with _state_lock:
            if run in _bindings:
                warn_once(
                    "reused run",
                    "wandb.init() returned an already mirrored run; keeping its "
                    "original River binding",
                )
                return
            _bindings[run] = _Binding(injection, run, fallback=fallback)
    except Exception:
        warn_once(
            "activate failed",
            "River metrics could not attach to the W&B run; W&B continues unchanged",
        )


def _close_all() -> None:
    try:
        bindings = list(_bindings.values())
    except Exception:
        return
    for binding in bindings:
        if binding.pid == os.getpid():
            binding.close()


# ── Capture ──────────────────────────────────────────────────────────────


def _scalar(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, numbers.Real):
        return None
    number = float(value)
    return number if math.isfinite(number) else None


def _valid_name(name: Any) -> bool:
    return (
        isinstance(name, str)
        and bool(name)
        and not name.startswith("_")
        and len(name.encode("utf-8")) <= MAX_NAME_BYTES
    )


@dataclass(frozen=True)
class HistoryRow:
    history_step: int
    values: dict[str, float]
    logged_at: float
    elapsed_s: float
    # Names this row recorded with a value River does not mirror (NaN, text,
    # arrays, ...): known to be present in W&B, but with no River value.
    unmirrored: frozenset[str] = frozenset()
    # Too many scalars to mirror. Not uploaded, but it still updates the
    # coordinates carried into later rows.
    dropped: bool = False


class HistoryAssembler:
    """Reproduce W&B's history rows from ``log(data, step, commit)`` calls.

    Implicit steps advance on commit; ``commit=False`` merges into the current
    row; an explicit larger step finalizes the pending row; an explicit smaller
    step is dropped, as W&B drops it. Only valid scalar fields are kept, but
    every call advances steps exactly like W&B.
    """

    def __init__(self, starting_step: int, started_monotonic: float) -> None:
        self.step = starting_step
        self._started = started_monotonic
        self._values: dict[str, float] = {}
        self._unmirrored: set[str] = set()
        self._oversized = False
        self._logged_at = 0.0
        self._elapsed_s = 0.0

    def log(self, data: Mapping[str, Any], step: Any, commit: Any) -> list[HistoryRow]:
        rows: list[HistoryRow] = []
        if step is not None:
            if isinstance(step, bool):
                return rows
            step = operator.index(step)
            if step < self.step:
                return rows
            if step > self.step:
                rows.extend(self._finalize())
                self.step = step
        self._merge(data)
        if (step is None and commit is None) or commit:
            rows.extend(self._finalize())
            self.step += 1
        return rows

    def finish(self) -> list[HistoryRow]:
        return self._finalize()

    def _merge(self, data: Mapping[str, Any]) -> None:
        self._logged_at = time.time()
        self._elapsed_s = max(time.monotonic() - self._started, 0.0)
        for name, value in data.items():
            if not _valid_name(name):
                continue
            number = _scalar(value)
            if number is None:
                # W&B keeps the latest value for a key; a later non-scalar
                # value replaces an earlier scalar in the same row.
                self._values.pop(name, None)
                self._unmirrored.add(name)
                continue
            if name not in self._values and len(self._values) >= MAX_BATCH_VALUES:
                self._oversized = True
                self._unmirrored.add(name)
                continue
            self._values[name] = number
            self._unmirrored.discard(name)

    def _finalize(self) -> list[HistoryRow]:
        values, unmirrored, oversized = self._values, self._unmirrored, self._oversized
        self._values, self._unmirrored, self._oversized = {}, set(), False
        if oversized:
            warn_once(
                "oversized row",
                "River metrics skipped a W&B history row with too many scalars",
            )
        elif not values and not unmirrored:
            return []
        return [
            HistoryRow(
                self.step,
                values,
                self._logged_at,
                self._elapsed_s,
                frozenset(unmirrored),
                dropped=oversized,
            )
        ]


@dataclass(frozen=True)
class MetricDefinition:
    step_metric: str | None = None
    step_sync: bool | None = None
    hidden: bool | None = None

    @property
    def syncs_step(self) -> bool:
        """W&B defaults ``step_sync`` to true once a step metric is set."""
        return self.step_sync if self.step_sync is not None else bool(self.step_metric)

    def payload(self, name: str) -> dict[str, Any]:
        return {
            "name": name,
            "step_metric": self.step_metric,
            "step_sync": self.syncs_step,
            "hidden": bool(self.hidden),
        }


def resolve_definition(
    definitions: Mapping[str, MetricDefinition], metric: str
) -> MetricDefinition | None:
    """Exact definitions win; otherwise the longest matching ``prefix*`` rule."""
    exact = definitions.get(metric)
    if exact is not None:
        return exact
    best: tuple[int, MetricDefinition] | None = None
    for name, definition in definitions.items():
        if (
            name.endswith("*")
            and metric.startswith(name[:-1])
            and (best is None or len(name) > best[0])
        ):
            best = (len(name), definition)
    return best[1] if best else None


class _Binding:
    """One W&B run mirrored into one immutable River stream.

    It never references the run itself, so the run's lifetime still controls
    the weakly keyed registry entry.
    """

    def __init__(self, injection: _Injection, run: Any, *, fallback: bool) -> None:
        self.pid = injection.pid
        self._lock = threading.Lock()
        self._closed = False
        # Resumed runs start from W&B's locally known starting step; reading
        # run.step would be a blocking service request.
        starting_step = 0 if fallback else getattr(run, "_starting_step", 0)
        self._history = HistoryAssembler(
            starting_step if isinstance(starting_step, int) else 0, time.monotonic()
        )
        self._definitions: dict[str, MetricDefinition] = {}
        self._definitions_changed = False
        self._emitted_snapshot: tuple[tuple[str, MetricDefinition], ...] = ()
        self._definition_version: int | None = None
        self._last_values: dict[str, float] = {}
        self._next_seq = 0
        from river_client import __version__

        self._uploader = metric_events.EventUploader(
            url=injection.url,
            api_key=injection.api_key,
            user_agent=f"river-client-python/{__version__}",
            stream=_stream(run, fallback=fallback),
        )

    def capture_log(self, args: tuple[Any, ...], kwargs: Mapping[str, Any]) -> None:
        try:
            data = args[0] if args else kwargs.get("data")
            step = args[1] if len(args) > 1 else kwargs.get("step")
            commit = args[2] if len(args) > 2 else kwargs.get("commit")
            if not isinstance(data, Mapping):
                return
            with self._lock:
                if self._closed:
                    return
                self._emit(self._history.log(data, step, commit))
        except Exception:
            warn_once("capture failed", "River metrics skipped a W&B log call")

    def capture_definition(
        self, args: tuple[Any, ...], kwargs: Mapping[str, Any]
    ) -> None:
        try:
            names = ("name", "step_metric", "step_sync", "hidden")
            params = dict(zip(names, args, strict=False))
            params.update({key: kwargs[key] for key in names if key in kwargs})
            name = params.get("name")
            if not isinstance(name, str) or len(name.encode()) > MAX_NAME_BYTES:
                return
            # W&B treats an empty step metric as unspecified.
            step_metric = params.get("step_metric")
            step_metric = getattr(step_metric, "name", step_metric) or None
            if step_metric is not None and not isinstance(step_metric, str):
                return
            if step_metric is not None and len(step_metric.encode()) > MAX_NAME_BYTES:
                # River Console would reject the whole revision; keep the
                # rest of the run mirrored and leave this definition out.
                warn_once(
                    "long step metric",
                    "River metrics skipped a W&B metric definition whose step "
                    f"metric name exceeds {MAX_NAME_BYTES} bytes",
                )
                return
            # define_metric(name, step_metric, step_sync, hidden, summary, goal,
            # overwrite): without overwrite W&B merges unspecified parameters.
            overwrite = args[6] if len(args) > 6 else kwargs.get("overwrite")
            with self._lock:
                if (
                    name not in self._definitions
                    and len(self._definitions) >= MAX_DEFINITIONS_PER_REVISION
                ):
                    warn_once(
                        "too many definitions",
                        "River metrics records at most "
                        f"{MAX_DEFINITIONS_PER_REVISION} W&B metric definitions "
                        "per run; later ones are skipped",
                    )
                    return
                previous = MetricDefinition()
                if not overwrite:
                    previous = self._definitions.get(name, previous)
                self._definitions[name] = MetricDefinition(
                    step_metric=_first(step_metric, previous.step_metric),
                    step_sync=_first(params.get("step_sync"), previous.step_sync),
                    hidden=_first(params.get("hidden"), previous.hidden),
                )
                self._definitions_changed = True
        except Exception:
            warn_once(
                "definition failed", "River metrics skipped a W&B metric definition"
            )

    def close(self) -> None:
        try:
            with self._lock:
                if self._closed:
                    return
                self._closed = True
                self._emit(self._history.finish())
            self._uploader.close()
        except Exception:
            warn_once("close failed", "River metrics could not finish cleanly")

    def _emit(self, rows: list[HistoryRow]) -> None:
        for row in rows:
            if row.dropped:
                self._carry(row)
                continue
            version = self._current_definition_version()
            axes: dict[str, float] = {}
            for metric in row.values:
                definition = resolve_definition(self._definitions, metric)
                if definition is None or not definition.step_metric:
                    continue
                step_metric = definition.step_metric
                if step_metric in axes:
                    continue
                if step_metric in row.values:
                    axes[step_metric] = row.values[step_metric]
                elif (
                    definition.syncs_step
                    and step_metric not in row.unmirrored
                    and step_metric in self._last_values
                ):
                    axes[step_metric] = self._last_values[step_metric]
            self._carry(row)
            if not row.values:
                continue
            self._uploader.submit(
                {
                    "event_seq": self._next_seq,
                    "history_step": row.history_step,
                    "logged_at": metric_events.format_timestamp(row.logged_at),
                    "elapsed_s": row.elapsed_s,
                    "definition_version": version,
                    "values": row.values,
                    "axes": axes,
                }
            )
            self._next_seq += 1

    def _carry(self, row: HistoryRow) -> None:
        """Remember the latest values W&B carries into later rows.

        Only declared step metrics can be carried, so only they are kept; the
        state stays bounded by the definition limit however many names a run
        logs.
        """
        step_metrics = {
            definition.step_metric
            for definition in self._definitions.values()
            if definition.step_metric
        }
        self._last_values.update(
            (name, value) for name, value in row.values.items() if name in step_metrics
        )
        # After a non-finite or non-scalar value (or one River could not track)
        # W&B carries that value, not an older number, so later rows have no
        # River coordinate either.
        for name in row.unmirrored:
            self._last_values.pop(name, None)

    def _current_definition_version(self) -> int | None:
        """Create a revision only when the effective definitions changed."""
        if not self._definitions_changed:
            return self._definition_version
        self._definitions_changed = False
        snapshot = tuple(sorted(self._definitions.items()))
        if snapshot != self._emitted_snapshot:
            self._emitted_snapshot = snapshot
            self._definition_version = (self._definition_version or 0) + 1
            self._uploader.add_definition(
                self._definition_version,
                {
                    "metrics": [
                        definition.payload(name) for name, definition in snapshot
                    ]
                },
            )
        return self._definition_version


def _first(value: Any, default: Any) -> Any:
    return value if value is not None else default


def _stream(run: Any, *, fallback: bool) -> dict[str, Any]:
    stream: dict[str, Any] = {
        "stream_id": str(uuid.uuid4()),
        "source": "wandb",
        "started_at": metric_events.format_timestamp(time.time()),
    }
    # A fallback run exists only locally; never present it as a W&B run.
    if fallback:
        return stream
    settings = getattr(run, "_settings", None)
    for key, attribute in (
        ("external_instance", "base_url"),
        ("external_entity", "entity"),
        ("external_project", "project"),
        ("external_run_id", "run_id"),
        ("external_run_name", "run_name"),
    ):
        value = getattr(settings, attribute, None)
        if isinstance(value, str) and value and len(value.encode()) <= MAX_NAME_BYTES:
            stream[key] = value
    return stream
