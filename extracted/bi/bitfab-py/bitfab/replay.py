"""Replay historical traces through a function and create an experiment."""

from __future__ import annotations

import asyncio
import contextlib
import inspect
import json
import logging
import math
import os
import sys
import time
import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Literal, Protocol, TypedDict

from typing_extensions import NotRequired

from bitfab.constants import _replay_context, _seed_context
from bitfab.git_command import run_git
from bitfab.mock_matching import MATCHER
from bitfab.mock_override import (
    MockOverride,
    MockOverrideInput,
    normalize_mock_overrides,
)
from bitfab.replay_branch import DbBranchOptions
from bitfab.replay_heartbeat import replay_heartbeat
from bitfab.replay_interrupt import (
    ReplayInterrupt,
    ReplayInterruptHandlers,
    interrupt_replay_on_early_exit,
)
from bitfab.replay_invocation import (
    build_replay_invocation,
    flags_for_invocation,
    safe_replay_invocation,
)
from bitfab.selective_replay import (
    SelectiveReplayOptions,
    SelectiveReplayRuntime,
    wire_options,
)
from bitfab.serialize import deserialize_value
from bitfab.simulation_plan import plan_wait_slice
from bitfab.warn_once import warn_once

if TYPE_CHECKING:
    from bitfab.client import Bitfab

logger = logging.getLogger(__name__)

MockStrategy = Literal["none", "all", "marked"]
ConcurrencyPrimitive = Literal["async", "process"]
_REPLAY_PERSISTENCE_TIMEOUT_SECONDS = 30.0
JUDGE_ASSERTIONS_DEPRECATION = (
    "judge_assertions is deprecated. Assertion judging is on by default; pass "
    "skip_assertion_judging=True (--skip-assertion-judging) to turn it off."
)
_MAX_REPLAY_ATTEMPTS = 100
_DEFAULT_MAX_CONCURRENCY = 10
_DEFAULT_PROCESS_MAX_CONCURRENCY = 4


class _ConcurrencyUnset:
    pass


_CONCURRENCY_UNSET = _ConcurrencyUnset()


def _validate_attempts(attempts: Any) -> None:
    if (
        not isinstance(attempts, int)
        or isinstance(attempts, bool)
        or not 1 <= attempts <= _MAX_REPLAY_ATTEMPTS
    ):
        raise ValueError(
            f"attempts must be an integer between 1 and {_MAX_REPLAY_ATTEMPTS} "
            f"(got {attempts!r})."
        )


def _validate_max_concurrency(max_concurrency: Any) -> None:
    if max_concurrency is None:
        return
    if (
        not isinstance(max_concurrency, int)
        or isinstance(max_concurrency, bool)
        or max_concurrency < 1
    ):
        raise ValueError(
            "max_concurrency must be a positive integer, or None for unlimited "
            f"(got {max_concurrency!r})."
        )


@dataclass(frozen=True)
class ReplayConcurrency:
    attempts: int = 1
    primitive: ConcurrencyPrimitive = "async"
    max_concurrency: int | _ConcurrencyUnset | None = _CONCURRENCY_UNSET
    on_item_finish_in_child_process: Callable[[ReplayItemFinishEvent], None] | None = (
        None
    )
    memory_throttle: bool | _ConcurrencyUnset = _CONCURRENCY_UNSET
    child_delivery_timeout: float | None | _ConcurrencyUnset = _CONCURRENCY_UNSET

    def __post_init__(self) -> None:
        _validate_attempts(self.attempts)
        if self.primitive not in ("async", "process"):
            raise ValueError(
                "concurrency primitive must be 'async' or 'process' "
                f"(got {self.primitive!r})."
            )
        if isinstance(self.max_concurrency, _ConcurrencyUnset):
            object.__setattr__(
                self,
                "max_concurrency",
                _DEFAULT_PROCESS_MAX_CONCURRENCY
                if self.primitive == "process"
                else _DEFAULT_MAX_CONCURRENCY,
            )
        _validate_max_concurrency(self.max_concurrency)
        if self.primitive == "process" and self.max_concurrency is None:
            raise ValueError(
                "max_concurrency=None means unlimited, and under "
                "primitive='process' that starts one interpreter per work item "
                "at once. Set a positive bound instead."
            )
        if isinstance(self.memory_throttle, _ConcurrencyUnset):
            object.__setattr__(self, "memory_throttle", self.primitive == "process")
        elif not isinstance(self.memory_throttle, bool):
            raise ValueError(
                f"memory_throttle must be a boolean (got {self.memory_throttle!r})."
            )
        elif self.memory_throttle and self.primitive != "process":
            raise ValueError(
                "memory_throttle holds back child interpreters before they are "
                "launched, and only primitive='process' launches any. Under "
                "primitive='async' every item shares this process, so lower "
                "max_concurrency instead."
            )
        self._resolve_child_delivery_timeout()
        if self.on_item_finish_in_child_process is None:
            return
        if not callable(self.on_item_finish_in_child_process):
            raise ValueError(
                "concurrency on_item_finish_in_child_process must be callable."
            )
        if self.primitive != "process":
            raise ValueError(
                "on_item_finish_in_child_process needs a child process to run in, "
                "and only primitive='process' creates one. To grade in the process "
                "that owns the run, set on_item_finish on the registry entry "
                "instead."
            )

    def _resolve_child_delivery_timeout(self) -> None:
        timeout = self.child_delivery_timeout
        if isinstance(timeout, _ConcurrencyUnset):
            object.__setattr__(
                self,
                "child_delivery_timeout",
                _REPLAY_PERSISTENCE_TIMEOUT_SECONDS
                if self.primitive == "process"
                else None,
            )
            return
        if timeout is None and self.primitive != "process":
            return
        if (
            not isinstance(timeout, (int, float))
            or isinstance(timeout, bool)
            or not math.isfinite(timeout)
            or timeout <= 0
        ):
            raise ValueError(
                "child_delivery_timeout must be a positive number of seconds "
                f"(got {timeout!r})."
            )
        if self.primitive != "process":
            raise ValueError(
                "child_delivery_timeout bounds how long a child process waits "
                "for its spans to reach Bitfab, and only primitive='process' "
                "creates one. Under primitive='async' the run's own delivery "
                "wait applies."
            )


ReplayWorkItem = tuple[dict[str, Any], int]


class ProcessLauncher(Protocol):
    def __call__(
        self,
        work_items: list[ReplayWorkItem],
        experiment_id: str | None,
        replayed_trace_ids: list[str],
        carried_over_items: list[ReplayItem] = ...,
        db_branch: DbBranchOptions | bool | None = ...,
    ) -> list[ReplayItem]: ...


def _resolve_concurrency(
    concurrency: ReplayConcurrency | None,
    attempts: int | _ConcurrencyUnset,
    max_concurrency: int | _ConcurrencyUnset | None,
) -> ReplayConcurrency:
    if concurrency is None:
        return ReplayConcurrency(
            attempts=1 if isinstance(attempts, _ConcurrencyUnset) else attempts,
            max_concurrency=max_concurrency,
        )
    if not isinstance(concurrency, ReplayConcurrency):
        raise TypeError(
            "concurrency must be a ReplayConcurrency "
            f"(got {type(concurrency).__name__})."
        )
    superseded = [
        name
        for name, value in (
            ("attempts", attempts),
            ("max_concurrency", max_concurrency),
        )
        if not isinstance(value, _ConcurrencyUnset)
    ]
    if superseded:
        raise ValueError(
            f"concurrency= already carries {' and '.join(superseded)}; passing "
            f"{' and '.join(f'{name}=' for name in superseded)} alongside it is "
            "ambiguous. Move the value into ReplayConcurrency(...)."
        )
    return concurrency


class TokenUsage(TypedDict):
    """Per-item token usage from the replayed run (this item's new execution)."""

    input: int | None
    output: int | None
    cached: int | None
    total: int | None


class ReplayItem(TypedDict):
    """A single item from a replay execution."""

    input: list[Any]
    result: Any
    original_output: Any
    # Backward-compatible message for either error kind.
    error: str | None
    # The actual exception raised by the replayed customer function.
    trace_error: BaseException | None
    # The actual exception raised while Bitfab prepared this replay item.
    replay_error: BaseException | None
    # How long the replayed function took on this run, in ms. None if the item
    # failed before it ran. Compare against original_duration_ms.
    duration_ms: int | None
    # The ORIGINAL trace's duration, tokens, and model. Prefixed because the
    # item also carries replay-side measurements: an unprefixed ``tokens``
    # beside an unprefixed ``duration_ms`` gave no way to tell which run
    # either described.
    original_duration_ms: int | None
    original_tokens: TokenUsage | None
    original_model: str | None
    ingestion_type: str | None
    # The REPLAYED run's token usage, filled in by ``replay()`` from the
    # complete-replay response. Unprefixed because the replay is this item's
    # subject; anything describing the trace being replayed carries ``original``.
    tokens: TokenUsage | None
    # Deprecated: the original's model; no replay equivalent exists.
    model: str | None
    trace_id: str | None
    # Bitfab trace id of the original (historical) trace being replayed.
    original_trace_id: str | None
    # External span id the recorded inputs were read from (the original root span).
    original_span_id: str | None
    # Deprecated aliases for original_trace_id/original_span_id.
    source_trace_id: str | None
    source_span_id: str | None
    db_snapshot_ref: dict[str, Any] | None
    attempt: int
    # How long this item's DB branch took to provision, per phase, measured
    # server-side. Present whenever a branch was attempted, on both outcomes:
    # complete on success, partial up to the failing phase when the resolve
    # failed. None when no branch was asked for, when the source trace carried
    # no snapshot ref, or against a server that predates timings.
    db_branch_timings: dict[str, Any] | None
    carried_over: bool
    selective_replay: NotRequired[dict[str, Any]]


class ReplayResult(TypedDict):
    """Result from a replay execution.

    Attributes:
        items: One entry per replayed work item.
        experiment_id: The experiment this replay created. None for a dry
            run, which executes nothing and so creates no experiment.
        experiment_url: Link to the experiment in the Bitfab dashboard. None
            for a dry run.
        test_run_id: Deprecated alias for ``experiment_id``.
        test_run_url: Deprecated alias for ``experiment_url``.
        attempts: How many times each source trace was replayed.
    """

    items: list[ReplayItem]
    experiment_id: str | None
    experiment_url: str | None
    # Deprecated aliases for experiment_id/experiment_url.
    test_run_id: str | None
    test_run_url: str | None
    attempts: int


def _replay_result(
    items: list[ReplayItem],
    experiment_id: str | None,
    experiment_url: str | None,
    attempts: int,
) -> ReplayResult:
    return ReplayResult(
        items=items,
        experiment_id=experiment_id,
        experiment_url=experiment_url,
        test_run_id=experiment_id,
        test_run_url=experiment_url,
        attempts=attempts,
    )


class ReplayExperimentStart(TypedDict):
    """The experiment a replay created, reported before any item runs.

    Attributes:
        experiment_id: The experiment this replay created.
        experiment_url: Link to the experiment in the Bitfab dashboard.
    """

    experiment_id: str
    experiment_url: str


class ReseedResult(TypedDict):
    trace_id: str
    previous_run_trace_id: str


class ReplayError(RuntimeError):
    """Whole-run failure with every replay item collected before it failed.

    ``experiment_id`` and ``experiment_url`` identify the experiment the run
    created, so it can still be opened after the failure. ``test_run_id`` and
    ``test_run_url`` are deprecated aliases carrying the same values.
    """

    def __init__(
        self,
        message: str,
        *,
        items: list[ReplayItem],
        cause: BaseException,
        experiment_id: str | None = None,
        experiment_url: str | None = None,
        test_run_id: str | None = None,
        test_run_url: str | None = None,
    ) -> None:
        super().__init__(message)
        resolved_id = experiment_id if experiment_id is not None else test_run_id
        resolved_url = experiment_url if experiment_url is not None else test_run_url
        if resolved_id is None or resolved_url is None:
            raise ValueError("ReplayError requires experiment_id and experiment_url.")
        self.items = items
        self.experiment_id: str = resolved_id
        self.experiment_url: str = resolved_url
        self.cause = cause

    @property
    def test_run_id(self) -> str:
        """Deprecated alias for ``experiment_id``."""
        warn_once(
            "deprecated-replay-error-test-run-id",
            "ReplayError.test_run_id is deprecated; read experiment_id instead.",
        )
        return self.experiment_id

    @property
    def test_run_url(self) -> str:
        """Deprecated alias for ``experiment_url``."""
        warn_once(
            "deprecated-replay-error-test-run-url",
            "ReplayError.test_run_url is deprecated; read experiment_url instead.",
        )
        return self.experiment_url


class DbBranchReplayError(RuntimeError):
    """A requested replay database branch could not be resolved.

    ``code`` and the server's original message remain available without
    parsing the backward-compatible replay item ``error`` string.
    """

    def __init__(
        self,
        code: str,
        message: str,
        original_trace_id: str,
        *,
        cause: BaseException | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.original_trace_id = original_trace_id
        self.cause = cause


class ReplayProgressItem(TypedDict):
    """The single item that just finished to produce a lifecycle event.

    Attributes:
        trace_id: The server's assigned replay traces.id, read back off the
            ingest response and surfaced as this item finishes (its trace is
            flushed on finish). None only if that flush could not confirm
            delivery in time; the client-side correlation id is never surfaced.
        original_trace_id: The original (historical) trace that was replayed, so
            a UI can identify or link it. Pulled from the start-replay server
            item. ``source_trace_id`` is kept as a deprecated alias.
        original_span_id: The original root span the inputs were read from; the
            key verdict persistence is scoped by. ``source_span_id`` is kept as
            a deprecated alias.
        input: Deserialized inputs from the original trace.
        result: The result returned by the replayed function.
        original_output: The original output from the historical trace.
        error: That item's replay error (string), or None when it ran ok.
        duration_ms: How long this item took to replay, in milliseconds.
    """

    trace_id: str | None
    original_trace_id: str | None
    original_span_id: str | None
    # Deprecated aliases for original_trace_id/original_span_id.
    source_trace_id: str | None
    source_span_id: str | None
    input: list[Any]
    result: Any
    original_output: Any
    error: str | None
    trace_error: BaseException | None
    replay_error: BaseException | None
    # Mirrors ReplayItem field for field, so a progress UI and a final-result
    # UI read one contract.
    duration_ms: int | None
    original_duration_ms: int | None
    original_tokens: TokenUsage | None
    original_model: str | None
    ingestion_type: str | None
    # Always None here: the replayed run's usage is only known at completion.
    tokens: TokenUsage | None
    # Deprecated: the original's model; no replay equivalent exists.
    model: str | None
    db_snapshot_ref: dict[str, Any] | None
    db_branch_timings: dict[str, Any] | None
    attempt: int
    selective_replay: NotRequired[dict[str, Any]]


class _ReplayProgressBase(TypedDict):
    completed: int
    total: int
    succeeded: int
    errored: int


class ReplayItemFinishProgress(_ReplayProgressBase):
    """Running totals reported to a replay ``on_item_finish`` callback.

    Replay does not know pass/fail at this point (verdicts are assigned
    later), so the totals only distinguish items whose function ran
    (``succeeded``) from items that raised (``errored``).

    Attributes:
        completed: Items that have finished so far, whether they succeeded
            or errored.
        total: Total number of items in this replay run.
        succeeded: Of the completed items, how many ran without raising.
        errored: Of the completed items, how many raised (their ``error``
            field is set).
        experiment_id: The experiment this replay belongs to, so a consumer
            can poll the replay status endpoint and persist per-item verdicts
            before the run completes. None for a dry run, which creates no
            experiment.
        test_run_id: Deprecated alias for ``experiment_id``.
        item: The single item that just finished to produce this event. Lets
            a progress UI show per-trace pass/fail as the run streams,
            without waiting for the full :class:`ReplayResult`.
    """

    experiment_id: str | None
    # Deprecated alias for experiment_id.
    test_run_id: str | None
    item: ReplayProgressItem


class ReplayProgress(_ReplayProgressBase, total=False):
    """Deprecated progress shape, including the legacy terminal event."""

    type: Literal["item", "complete"]
    result: ReplayResult
    # None for a dry run, which creates no experiment.
    experiment_id: str | None
    # Deprecated alias for experiment_id.
    test_run_id: str | None
    item: ReplayProgressItem


class ReplayItemStartProgress(TypedDict):
    """Lifecycle event emitted when a replay worker starts an item.

    ``test_run_id`` is a deprecated alias for ``experiment_id``. Both are
    None for a dry run, which creates no experiment.
    """

    type: Literal["started"]
    experiment_id: str | None
    test_run_id: str | None
    started: int
    completed: int
    total: int
    succeeded: int
    errored: int
    item: dict[str, str | int | None]


class ReplayItemFinishEvent(TypedDict):
    """One finished item, reported from the child process that ran it.

    ``test_run_id`` is a deprecated alias for ``experiment_id``.
    """

    experiment_id: str
    test_run_id: str
    item: ReplayItem


BITFAB_PROGRESS_PREFIX = "@@bitfab:progress "


def report_replay_progress(
    progress: ReplayItemFinishProgress | ReplayItemStartProgress | ReplayProgress,
) -> None:
    """Write a replay lifecycle event using the Bitfab plugin wire protocol.

    Pass this as both ``on_item_start`` and ``on_item_finish`` to report in-flight
    and finished items. stdout remains available for direct-run ReplayResult JSON.
    Each line carries the experiment ID under ``experimentId``, and under the
    deprecated ``test_run_id`` for older plugins.
    Never raises because progress reporting must not crash a replay.
    """
    with contextlib.suppress(Exception):
        payload: dict[str, Any] = dict(progress)
        experiment_id = payload.get("experiment_id", payload.get("test_run_id"))
        if experiment_id is not None:
            payload["experimentId"] = experiment_id
        sys.stderr.write(
            f"{BITFAB_PROGRESS_PREFIX}{json.dumps(payload, default=_replay_json_default)}\n"
        )


def _replay_json_default(value: Any) -> Any:
    if isinstance(value, BaseException):
        serialized = {
            "type": type(value).__name__,
            "message": str(value),
        }
        if isinstance(value, DbBranchReplayError):
            serialized["code"] = value.code
            serialized["original_trace_id"] = value.original_trace_id
            if value.cause is not None:
                serialized["cause"] = value.cause
        return serialized
    return str(value)


def serialize_replay_result(result: ReplayResult) -> str:
    """Serialize a replay result while retaining structured exception fields."""
    return json.dumps(result, indent=2, default=_replay_json_default)


def serialize_replay_item(item: ReplayItem) -> str:
    """Serialize one replay item while retaining structured exception fields."""
    return json.dumps(item, default=_replay_json_default)


def failed_replay_item(
    server_item: dict[str, Any], attempt: int, message: str
) -> ReplayItem:
    """A work item that never produced a result, reported rather than dropped.

    A child process that dies before writing its item still owes the run an
    entry: silently returning N-1 items for N work items reads as a smaller
    run rather than a failed one.
    """
    original_trace_id = server_item.get("originalTraceId") or server_item.get(
        "sourceTraceId"
    )
    original_span_id = server_item.get("originalSpanId") or server_item.get(
        "sourceSpanId"
    )
    return ReplayItem(
        input=[],
        result=None,
        original_output=None,
        error=message,
        trace_error=None,
        replay_error=None,
        duration_ms=None,
        original_duration_ms=None,
        original_tokens=None,
        original_model=None,
        ingestion_type=None,
        tokens=None,
        model=None,
        trace_id=None,
        original_trace_id=original_trace_id,
        original_span_id=original_span_id,
        source_trace_id=original_trace_id,
        source_span_id=original_span_id,
        db_snapshot_ref=server_item.get("dbSnapshotRef"),
        db_branch_timings=None,
        attempt=attempt,
        carried_over=False,
    )


def _replay_item_error_message(error: BaseException) -> str:
    if isinstance(error, DbBranchReplayError):
        return (
            "Replay requested a database branch for trace "
            f"{error.original_trace_id} but it could not be resolved "
            f"({error.code}): {error}. The function was not run, because "
            "replaying it against the live database would produce a result that "
            "looks valid but did not use the historical data you asked for."
        )
    return str(error)


class AdaptContext(TypedDict):
    """Per-trace context passed to a replay ``adapt_inputs`` hook.

    Attributes:
        original_trace_id: Bitfab trace ID of the original (historical) trace
            being replayed. Lets a table-driven adapter look up adapted inputs
            per trace. ``source_trace_id`` is kept as a deprecated alias.
        original_span_id: External span ID the recorded inputs were read from.
            ``source_span_id`` is kept as a deprecated alias.
        metadata: The original trace's stored metadata (what ``seed_trace`` or
            ``get_current_trace().set_metadata`` recorded on it), so an adapter
            can read a seeded case's provenance without smuggling it through
            the recorded inputs. Empty when the trace carries none.
    """

    original_trace_id: str | None
    original_span_id: str
    metadata: dict[str, Any]
    # Deprecated aliases for original_trace_id/original_span_id.
    source_trace_id: str | None
    source_span_id: str


class CodeChangeFile(TypedDict):
    """A single file edited as part of a code change.

    Attributes:
        path: File path (relative to repo root, or any consistent root).
        before: File contents before the change ("" for newly created files).
        after: File contents after the change ("" for deleted files).
    """

    path: str
    before: str
    after: str


def _db_branch_enabled(db_branch: DbBranchOptions | bool | None) -> bool:
    """Whether the caller asked for database branching.

    ``True`` and a settings mapping both turn it on; ``False`` and ``None``
    leave it off. Kept separate from :func:`_db_branch_settings` because
    ``db_branch=True`` enables branching while contributing no settings, so the
    presence of settings can't stand in for the switch.
    """
    return db_branch is not None and db_branch is not False


def _db_branch_settings(
    db_branch: DbBranchOptions | bool | None,
) -> dict[str, Any] | None:
    """Convert the caller's branch options to the wire shape, or None when
    nothing is set.

    Dropping the object entirely keeps the request byte-identical to what
    older SDKs send. Booleans carry no settings: they only move the switch.
    """
    if db_branch is None or isinstance(db_branch, bool):
        return None
    settings: dict[str, Any] = {}
    if db_branch.get("min_cu") is not None:
        settings["minCu"] = db_branch["min_cu"]
    if db_branch.get("max_cu") is not None:
        settings["maxCu"] = db_branch["max_cu"]
    if db_branch.get("warmup_sql") is not None:
        settings["warmupSql"] = db_branch["warmup_sql"]
    return settings or None


class _CodeChangeUnset:
    pass


_CODE_CHANGE_UNSET = _CodeChangeUnset()


def _in_replay_item() -> bool:
    return _replay_context.get() is not None


def _in_seed_scope() -> bool:
    return _seed_context.get() is not None


def _find_bitfab_wrapper(fn: Callable) -> Callable | None:
    """Walk the __wrapped__ chain to find the innermost bitfab-decorated function.

    Handles nested decorators (e.g. @retry(@cache(@span(fn)))) by traversing
    through each layer's __wrapped__ attribute until it finds one with
    _bitfab_wrapped=True.
    """
    current = fn
    seen: set[int] = set()
    while current is not None:
        if id(current) in seen:
            break
        seen.add(id(current))
        if getattr(current, "_bitfab_wrapped", False):
            return current
        current = getattr(current, "__wrapped__", None)
    return None


def _resolve_dataset_ids(
    dataset_id: str | None, dataset_ids: list[str] | None
) -> list[str] | None:
    if dataset_id is not None and dataset_ids is not None:
        raise ValueError(
            "dataset_id and dataset_ids are the same selector: pass one dataset "
            "through dataset_id, or several through dataset_ids."
        )
    if dataset_id is not None:
        return [dataset_id]
    if dataset_ids is None:
        return None
    if not dataset_ids:
        raise ValueError("dataset_ids must contain at least one dataset ID.")
    return list(dict.fromkeys(dataset_ids))


def _resolve_replay_fn(
    client: Bitfab, fn: Callable, trace_function_key: str | None
) -> tuple[Callable, str, bool]:
    """Resolve the callable and trace function key for a replay run.

    Returns ``(fn, key, auto_wrapped)``. ``auto_wrapped`` is True only when
    ``fn`` was a plain callable wrapped here under an explicit key (the
    handler-instrumented path); it drives the dict-root-input semantics, so a
    decorated function behaves identically whether or not a redundant
    matching key is passed alongside it.
    """
    explicit_key = trace_function_key is not None
    wrapper = _find_bitfab_wrapper(fn)
    if wrapper is not None:
        decorated_key = wrapper._bitfab_trace_function_key
        if explicit_key and decorated_key != trace_function_key:
            raise ValueError(
                f"Function {getattr(fn, '__name__', repr(fn))} is decorated with trace "
                f"function key '{decorated_key}' but replay was called with "
                f"'{trace_function_key}'. Pass matching keys, or pass an undecorated "
                "callable to replay it under the explicit key."
            )
        return fn, decorated_key, False
    if explicit_key:
        # Plain callable replayed under an explicit key (e.g. a
        # handler-instrumented workflow with no decorated root in the app).
        # Wrap it so each replayed invocation records a trace under the same
        # key, exactly like the decorated path.
        #
        # Name the root span after the key (not the callable's __name__) so it
        # matches the production root span: handler-instrumented roots (Claude
        # Agent SDK, OpenAI Agents) are named after the trace function key, so
        # naming the auto-wrap after __name__ would make the replayed root read
        # differently from the trace it replays.
        assert trace_function_key is not None
        return (
            client._span_impl(
                trace_function_key,
                name=trace_function_key,
                type="agent",
                surface=None,
            )(fn),
            trace_function_key,
            True,
        )
    raise ValueError(
        f"Function {getattr(fn, '__name__', repr(fn))} must be decorated with "
        "@span, or pass an explicit trace function key: "
        'client.replay("<key>", fn). Handler-instrumented workflows '
        "(LangGraph/LangChain, Claude Agent SDK, OpenAI Agents) have no "
        "decorated root function; use the explicit-key form."
    )


def _explicit_replay_options(arguments: dict[str, Any]) -> dict[str, Any]:
    return {
        name: arguments[name]
        for name, parameter in inspect.signature(replay).parameters.items()
        if parameter.kind is inspect.Parameter.KEYWORD_ONLY
        and arguments[name] is not parameter.default
        and arguments[name] != parameter.default
    }


def replay(
    client: Bitfab,
    fn: Callable,
    *,
    trace_function_key: str | None = None,
    limit: int | None = None,
    trace_ids: list[str] | None = None,
    name: str | None = None,
    notes: str | None = None,
    metadata: dict[str, str] | None = None,
    max_concurrency: int | _ConcurrencyUnset | None = _CONCURRENCY_UNSET,
    code_change_description: str | _CodeChangeUnset | None = _CODE_CHANGE_UNSET,
    code_change_files: list[CodeChangeFile] | _CodeChangeUnset | None = (
        _CODE_CHANGE_UNSET
    ),
    experiment_group_id: str | None = None,
    dataset_id: str | None = None,
    dataset_ids: list[str] | None = None,
    grader_ids: list[str] | None = None,
    only_with_assertions: bool = False,
    skip_assertion_judging: bool = False,
    judge_assertions: bool | None = None,
    mock: MockStrategy = "marked",
    mock_override: MockOverrideInput | list[MockOverrideInput] | None = None,
    experimental_selective_replay: SelectiveReplayOptions | None = None,
    adapt_inputs: (
        Callable[
            [list[Any], dict[str, Any], AdaptContext], tuple[list[Any], dict[str, Any]]
        ]
        | None
    ) = None,
    db_branch: DbBranchOptions | bool | None = None,
    dry_run: bool = False,
    attempts: int | _ConcurrencyUnset = _CONCURRENCY_UNSET,
    concurrency: ReplayConcurrency | None = None,
    process_launcher: ProcessLauncher | None = None,
    on_item_start: Callable[[ReplayItemStartProgress], None] | None = None,
    on_item_finish: Callable[[ReplayItemFinishProgress], None] | None = None,
    on_progress: Callable[[ReplayProgress], None] | None = None,
    on_experiment_start: Callable[[ReplayExperimentStart], None] | None = None,
    resume: str | None = None,
    force: bool = False,
    on_interrupt: Callable[[ReplayInterrupt], None] | None = None,
) -> ReplayResult:
    """Replay historical traces through a function and create an experiment.

    Fetches the last N traces for the given trace function key, re-runs each
    through the provided function (wrapped with span decorator for tracing),
    and returns comparison data.

    The function is called through its full decorator chain (e.g. @retry,
    @cache): replay injects the experiment ID via context rather than re-wrapping.

    Args:
        client: The Bitfab client instance
        fn: The function to replay. Either a function decorated with @span
            (the trace function key is read from the decorator), or any plain
            callable when ``trace_function_key`` is passed explicitly.
        trace_function_key: Explicit trace function key to replay. Required
            when ``fn`` is not decorated with @span: handler-instrumented
            workflows (LangGraph/LangChain, Claude Agent SDK, OpenAI Agents)
            record traces under a key with no decorated root function in the
            app, and this parameter is how those traces are replayed. The SDK
            wraps ``fn`` in a span under this key internally so each replayed
            invocation records a trace tied to the experiment. When ``fn`` is a
            plain callable wrapped this way, a recorded dict root input (e.g.
            a LangGraph state) is passed to it as a single positional
            argument, matching the TypeScript SDK. A decorated ``fn`` keeps
            the decorated-path kwargs semantics whether or not a matching key
            is also passed.
        limit: Maximum number of traces to replay (default 5). Ignored when
            ``trace_ids``, ``dataset_id`` or ``dataset_ids`` is passed because
            either source already determines how many traces replay. Supplying
            ``trace_ids`` also emits a warning. To replay part of a dataset
            selection, name the members to run in ``trace_ids`` rather than
            bounding it here.
        trace_ids: Optional list of trace IDs to replay (max 100). Passed
            alongside ``dataset_id`` or ``dataset_ids`` it pins which members of
            that selection replay, and the server rejects any ID none of those
            datasets contains. On its own it selects by ID with no dataset
            attribution.
        name: What this run is testing, in a few words, such as
            'baseline' or 'shorter system prompt'. Bitfab records the
            commit, branch, tree state, datasets, and who ran it with every
            experiment, so do not repeat them here.
        notes: Run conditions Bitfab cannot see on its own, such as an
            environment override or a forced feature flag. Kept on the
            experiment next to its name.
        metadata: Caller-owned tags on the experiment, such as which
            schedule launched it. Read back and filtered on through
            ``client.experiments``.
        max_concurrency: Maximum number of items to process in parallel.
            Set to 1 for sequential execution, or None for unlimited. Defaults to 10.
        code_change_description: Optional rationale for the code change being
            tested in this replay. Stored on the resulting experiment. When
            supplied without ``code_change_files``, this text is preserved while
            the SDK automatically captures the files. Pass ``None`` when the
            replay should have no description; use ``code_change_files=None``
            to suppress automatic file capture.
        code_change_files: Optional list of files edited as part of this code
            change. Each entry is ``{"path", "before", "after"}`` with the file
            path and full ``before``/``after`` contents, typically captured by
            reading each file before and after editing. Use ``""`` for newly
            created (``before``) or deleted (``after``) files. Omit this
            argument to capture automatically, or pass ``None`` to suppress
            file capture for this replay.
        experiment_group_id: Optional UUID that groups multiple replay runs
            into a single experiment batch. The experiments page can stream
            results live by filtering on this ID.
        dataset_id: Optional UUID of the dataset this replay runs against.
            Mutually exclusive with ``dataset_ids``. Alone it replays the
            dataset's full membership, and with ``trace_ids`` it replays only
            those members. Stored on the resulting experiment for durable
            dataset attribution, so it appears under the dataset's experiments.
            Validated server-side.
        dataset_ids: Optional list of dataset UUIDs this replay runs against,
            for benchmarking one function against several corpora in a single
            run. Mutually exclusive with ``dataset_id``, so pass one dataset
            through ``dataset_id`` and several through this. The run replays the
            union of their traces, graded by the union of their graders, and is
            attributed to every one of them. Passing ``trace_ids`` alongside it
            narrows the run to those members. Validated server-side.
        grader_ids: Optional list of grader UUIDs attached directly to this
            experiment (max 100). At completion they are graded as the union with
            the dataset's runnable graders. Use it to grade a single run with a
            check you don't want to add permanently. Each must be an active/live
            grader in the same org and trace function, or the server rejects the
            replay.
        skip_assertion_judging: Don't judge approved assertions on each
            replay. Judging is on by default: every approved assertion is
            judged as its replay finishes and the verdict is saved as that
            assertion's agent label, and each judgement costs model calls.
        only_with_assertions: Replay only the selected traces that carry at
            least one approved assertion. Narrows whatever ``limit``,
            ``trace_ids`` or ``dataset_ids`` chose, so a run that measures
            assertion outcomes doesn't pay to re-execute traces nothing can
            grade. With ``limit`` it selects the N most recent traces that HAVE
            approved assertions, rather than filtering the N most recent down to
            however few do. An assertion still awaiting review doesn't count: a
            replay is only judged against assertions a person has approved, so a
            trace carrying nothing but drafts has nothing here to measure. A
            selection that narrows to nothing replays nothing.
        mock: Mock strategy for child spans during replay.

            * ``"marked"`` (default): only child spans declared with
              ``mock_on_replay=True`` on ``@client.span(...)`` return historical
              output; everything else runs real.
            * ``"none"``: every child span runs real code.
            * ``"all"``: every matched recorded child span returns its
              historical output; a missing occurrence fails the item closed.
        mock_override: Optional selective override(s) layered on top of ``mock``:
            a :class:`~bitfab.mock_override.MockOverride`, global resolver, or
            list. A resolver routes on ``ctx.node.trace_function_key`` and may
            return ``NO_MOCK_OVERRIDE`` to continue to lower-priority overrides
            and the base strategy. Per-call overrides here are
            tried before any registered via
            :meth:`~bitfab.client.Bitfab.register_mock_override`. Because they
            gate the span tree fetch, overrides fire even under ``mock="none"``
            (run everything real but replace node X). The root span is never
            overridden.
        experimental_selective_replay: Opt-in must_run manifest. The server
            protects required subtrees and ancestors, combining assertion targets
            and recorded reuse eligibility.
            Requires mock="marked", no overrides or resume, and in-process replay.
            Item selective_replay reports execution coverage, not verdicts.
        adapt_inputs: Optional hook to reshape recorded inputs before they are
            passed to ``fn``. Replay pulls each trace's inputs exactly as they
            were captured against the signature AT TRACE TIME; when the function's
            shape has since changed, the recorded ``(args, kwargs)`` no longer line
            up and ``fn(*args, **kwargs)`` raises. The hook receives the
            deserialized ``args`` and ``kwargs`` plus a per-trace
            :class:`AdaptContext` (so a table-driven adapter can look up adapted
            inputs by ``trace_id``) and returns the ``(args, kwargs)`` actually
            passed to ``fn``. The returned ``args`` (plus the kwargs dict
            appended, when kwargs are non-empty) is what
            ``ReplayItem["input"]`` reports. Runs per item; a raising adapter is
            surfaced on that item's ``error`` rather than crashing the run.
        db_branch: ``True`` to branch with the mirror project's own sizing, or a
            :class:`DbBranchOptions` mapping to tune how each branch is sized
            and warmed. ``False`` and omission leave branching off. The server
            resolves a per-trace branch from each source trace's
            ``db_snapshot_ref``; read it inside ``fn`` with
            :func:`bitfab.get_current_replay_branch`, and the SDK releases the
            branch after each item. Omit it for replays that don't need
            historical DB state.
        attempts: How many times each source trace is replayed in this run
            (1 to 100, default 1). Superseded by ``concurrency``.
        concurrency: Optional :class:`ReplayConcurrency` carrying ``attempts``,
            ``max_concurrency`` and the ``primitive`` that runs them. Passing it
            alongside the ``attempts``/``max_concurrency`` arguments is an error.
        on_item_finish: Optional callback invoked once per item as it finishes,
            in completion order (not input order), with running totals for the
            whole run and the required finished item (a
            :class:`ReplayItemFinishProgress`). It never receives a whole-run
            completion event. Use it to render replay progress, for example a
            terminal progress bar. Invoked on the event loop right after each
            item finishes, so keep it cheap. A raising callback never crashes
            the run: the error is swallowed so progress UI can't break replay.
        on_progress: Deprecated compatibility callback. It receives the same
            per-item events plus its legacy item-less terminal ``"complete"``
            event. Ignored when ``on_item_finish`` is also provided.
        on_item_start: Optional callback invoked when a worker begins processing
            each item, before replay setup and customer code run. Pair it with
            ``on_item_finish`` to distinguish queued work from in-flight work. A
            raising callback never crashes the run.
        on_experiment_start: Optional callback invoked once, as soon as the
            server has created the experiment and before any item runs, with
            its ``experiment_id`` and ``experiment_url``. Use it to show the
            experiment link even if the run later fails. A raising callback
            never crashes the run.
        resume: Experiment ID of a replay that stopped before every item
            finished. Runs only the traces and attempts that did not finish,
            in the same experiment, and returns the finished ones with
            ``carried_over=True`` and no payloads. The traces, attempts and
            graders come from that experiment, so passing ``trace_ids``,
            ``limit``, ``dataset_id``, ``dataset_ids``, ``attempts``,
            ``grader_ids``, ``only_with_assertions`` or ``dry_run`` with it is
            an error. Database branching and its settings also come from the
            experiment, so ``db_branch`` is ignored.
        force: Resume even when the experiment had activity in the last two
            minutes or its code change differs from the one it started with.
            Only valid with ``resume``.
        on_interrupt: Optional callback invoked when SIGINT (Ctrl-C) or SIGTERM
            stops the run after the experiment started, once replay has asked
            Bitfab to mark the experiment interrupted. It receives
            ``experiment_id``, ``experiment_url``, ``signal`` (``"SIGINT"`` or
            ``"SIGTERM"``) and ``marked_interrupted``, which is ``False`` when
            that request failed. When it is set, replay prints nothing itself.
            Without it, replay prints ``[replay] Experiment <id> interrupted.``,
            or says Bitfab could not mark it interrupted. Either way the signal
            then goes on to any handler installed before the run, or ends the
            process as it normally would.

    Returns:
        ReplayResult with items (input, result, original_output, error),
        experiment_id, and experiment_url (``test_run_id`` and
        ``test_run_url`` are deprecated aliases carrying the same values)
    """
    explicit_options = _explicit_replay_options(locals())
    if judge_assertions is not None:
        warn_once("deprecated-judge-assertions", JUDGE_ASSERTIONS_DEPRECATION)
        skip_assertion_judging = skip_assertion_judging or not judge_assertions
    if trace_ids is not None:
        if not trace_ids:
            raise ValueError("trace_ids must contain at least one trace ID.")
        if len(trace_ids) > 100:
            raise ValueError(
                f"trace_ids supports at most 100 trace IDs per replay (got {len(trace_ids)})."
            )
    if force and resume is None:
        raise ValueError("force only applies to resume: pass resume=<experiment ID>.")
    if resume is not None and not resume.strip():
        raise ValueError("resume needs the experiment ID of the replay to continue.")
    if resume is not None:
        _refuse_selection_with_resume(
            resume,
            limit=limit,
            trace_ids=trace_ids,
            dataset_id=dataset_id,
            dataset_ids=dataset_ids,
            attempts=attempts,
            grader_ids=grader_ids,
            only_with_assertions=only_with_assertions,
            dry_run=dry_run,
            experimental_selective_replay=experimental_selective_replay,
        )
    resolved_dataset_ids = _resolve_dataset_ids(dataset_id, dataset_ids)
    resolved_concurrency = _resolve_concurrency(concurrency, attempts, max_concurrency)
    resolved_attempts = resolved_concurrency.attempts
    resolved_max_concurrency = resolved_concurrency.max_concurrency
    in_process_mode = resolved_concurrency.primitive == "process"
    if in_process_mode and process_launcher is None:
        raise ValueError(
            "concurrency primitive 'process' runs one interpreter per work "
            "item, which only the bitfab-replay registry entrypoint can re-exec. "
            "replay() is handed a live function object and has no re-exec target, "
            "so run this pipeline through bitfab-replay --registry instead."
        )
    if limit is not None and trace_ids is not None:
        logger.warning(
            "limit is ignored when trace_ids is passed: the explicit trace ID list already determines how many traces replay."
        )
    fn, trace_function_key, auto_wrapped = _resolve_replay_fn(
        client, fn, trace_function_key
    )

    # Per-call overrides are tried first, then the ones registered on the
    # client, so a per-call override wins over a registered one for the same
    # span (first match wins downstream).
    resolved_mock_overrides = [
        *normalize_mock_overrides(mock_override),
        *client._mock_overrides,
    ]
    if experimental_selective_replay is not None:
        wire_options(experimental_selective_replay)
        if mock != "marked" or resolved_mock_overrides:
            raise ValueError(
                "experimental_selective_replay requires mock='marked' without mock overrides."
            )
        if in_process_mode:
            raise ValueError(
                "experimental_selective_replay currently supports in-process replay only, not the process registry launcher."
            )

    # limit is meaningless with explicit trace_ids (the ID list determines
    # the count), so it's omitted from the request entirely.
    effective_limit = (
        None if trace_ids is not None else (limit if limit is not None else 5)
    )

    # A dry run executes nothing, so a branch would be provisioned (and billed)
    # for code that never runs, and a seeded source's refusal would fail the item
    # before it could report its resolved inputs.
    include_db_branch_lease = _db_branch_enabled(db_branch) and not dry_run

    # code_change_files controls capture: omitted auto-captures, a list wins,
    # and explicit None opts out. Preserve a caller-supplied description while
    # filling only the omitted files.
    if code_change_files is _CODE_CHANGE_UNSET:
        captured = _resolve_auto_code_change(name)
        if captured is not None:
            code_change_files = captured[1]
            if code_change_description is _CODE_CHANGE_UNSET:
                code_change_description = captured[0]

    resolved_code_change_description = (
        None
        if code_change_description is _CODE_CHANGE_UNSET
        else code_change_description
    )
    resolved_code_change_files = (
        None if code_change_files is _CODE_CHANGE_UNSET else code_change_files
    )

    db_branch_settings = _db_branch_settings(db_branch)
    request_code_change_files = (
        [dict(f) for f in resolved_code_change_files]
        if resolved_code_change_files is not None
        else None
    )
    if resume is not None:
        replay_data = client.http_client.resume_replay(
            resume,
            trace_function_key,
            code_change_files=request_code_change_files,
            force=force,
        )
        stored_db_branch = _stored_db_branch(replay_data)
        if db_branch is not None and (
            _db_branch_enabled(db_branch) != _db_branch_enabled(stored_db_branch)
            or db_branch_settings != _db_branch_settings(stored_db_branch)
        ):
            logger.warning(
                "Bitfab: resume keeps experiment %s's database branch setting "
                "(db_branch=%r) and ignores the db_branch=%r passed now.",
                resume,
                stored_db_branch,
                db_branch,
            )
        db_branch = stored_db_branch
        include_db_branch_lease = _db_branch_enabled(db_branch)
        db_branch_settings = _db_branch_settings(db_branch)
    else:
        replay_data = client.http_client.start_replay(
            trace_function_key,
            effective_limit,
            trace_ids=trace_ids,
            name=name,
            notes=notes,
            metadata=metadata,
            code_change_description=resolved_code_change_description,
            code_change_files=request_code_change_files,
            experiment_group_id=experiment_group_id,
            include_db_branch_lease=include_db_branch_lease,
            include_original_metadata=adapt_inputs is not None,
            dataset_ids=resolved_dataset_ids,
            grader_ids=grader_ids,
            db_branch_settings=db_branch_settings,
            only_with_assertions=only_with_assertions,
            skip_assertion_judging=skip_assertion_judging,
            attempts=resolved_attempts,
            dry_run=dry_run,
            invocation=safe_replay_invocation(
                lambda: build_replay_invocation(flags_for_invocation(explicit_options))
            ),
            **(
                {
                    "experimental_selective_replay": wire_options(
                        experimental_selective_replay
                    )
                }
                if experimental_selective_replay is not None
                else {}
            ),
        )
    experiment_id: str | None
    full_experiment_url: str | None
    if dry_run and replay_data.get("experimentId", "") is None:
        # Current servers record no experiment for a dry run, so there is none
        # to keep alive, interrupt, or complete.
        experiment_id = None
        full_experiment_url = None
    else:
        experiment_id = replay_data.get("experimentId") or replay_data["testRunId"]
        experiment_url = replay_data.get("experimentUrl") or replay_data["testRunUrl"]
        full_experiment_url = f"{client.service_url}{experiment_url}"
    server_items = replay_data["items"]
    carried_over_items: list[ReplayItem] = []
    if resume is not None:
        resolved_attempts = int(replay_data.get("attempts") or resolved_attempts)
        work_items = _resumed_replay_work(server_items, replay_data.get("work") or [])
        carried_over_items = [
            _carried_over_item(finished)
            for finished in replay_data.get("finished") or []
        ]
        skipped = replay_data.get("skippedOriginalTraceIds") or []
        if skipped:
            logger.warning(
                "Bitfab: resuming experiment %s skipped %d trace(s) deleted since "
                "it started: %s",
                experiment_id,
                len(skipped),
                ", ".join(skipped),
            )
    else:
        work_items = _expand_replay_work(server_items, resolved_attempts)
    with contextlib.ExitStack() as stack:
        if experiment_id is not None and full_experiment_url is not None:
            live_experiment_id = experiment_id
            stop_heartbeat = stack.enter_context(
                replay_heartbeat(
                    lambda: client.http_client.heartbeat_replay(live_experiment_id)
                )
            )
            interrupt_handlers = stack.enter_context(
                interrupt_replay_on_early_exit(
                    live_experiment_id,
                    full_experiment_url,
                    lambda: _stop_heartbeat_then_interrupt(
                        stop_heartbeat, client, live_experiment_id
                    ),
                    on_interrupt,
                )
            )
        else:
            interrupt_handlers = ReplayInterruptHandlers(
                interrupted=lambda: False, remove=lambda: None
            )
        interrupted = interrupt_handlers.interrupted
        if (
            on_experiment_start is not None
            and experiment_id is not None
            and full_experiment_url is not None
        ):
            try:
                on_experiment_start(
                    ReplayExperimentStart(
                        experiment_id=experiment_id, experiment_url=full_experiment_url
                    )
                )
            except Exception:
                logger.debug(
                    "Bitfab: replay on_experiment_start callback raised", exc_info=True
                )

        result_items: list[ReplayItem] = []
        # One client-side correlation id per item. It tags that item's replay spans
        # during the run so the server can echo back the row id it minted (resolved
        # in the complete-replay loop below). Kept out of the public ReplayItem: it
        # is a correlation handle, never an id callers use.
        replayed_trace_ids = [str(uuid.uuid4()) for _ in work_items]
        # Declared before the first span is submitted: the transport records delivery
        # only for traces someone asked about, so anything submitted before this
        # would go untracked.
        if not in_process_mode:
            client.http_client.track_trace_deliveries(replayed_trace_ids)

        item_finish_callback = (
            on_item_finish if on_item_finish is not None else on_progress
        )
        if work_items and in_process_mode:
            assert process_launcher is not None
            result_items = process_launcher(
                work_items,
                experiment_id,
                replayed_trace_ids,
                carried_over_items,
                db_branch if resume is not None else None,
            )
        elif work_items:
            result_items = asyncio.run(
                _run_replay_async(
                    client,
                    server_items,
                    fn,
                    experiment_id,
                    resolved_max_concurrency,
                    mock,
                    adapt_inputs,
                    include_db_branch_lease,
                    db_branch_settings,
                    dict_input_as_positional=auto_wrapped,
                    on_item_start=on_item_start,
                    on_item_finish=item_finish_callback,
                    mock_overrides=resolved_mock_overrides,
                    replayed_trace_ids=replayed_trace_ids,
                    dry_run=dry_run,
                    attempts=resolved_attempts,
                    work_items=work_items,
                    carried_over_items=carried_over_items,
                    experimental_selective_replay=experimental_selective_replay,
                )
            )
        reported_items = [*carried_over_items, *result_items]

        if dry_run or experiment_id is None or full_experiment_url is None:
            # An older server still creates an experiment for a dry run, and
            # it is finalized so it does not sit unfinished in the list.
            if experiment_id is not None and full_experiment_url is not None:
                _raise_if_interrupted(
                    interrupted, reported_items, experiment_id, full_experiment_url
                )
                interrupt_handlers.remove()
                with contextlib.suppress(Exception):
                    client.http_client.complete_replay(experiment_id)
            dry_result = _replay_result(
                reported_items, experiment_id, full_experiment_url, resolved_attempts
            )
            _write_replay_result_file(dry_result)
            return dry_result

        try:
            delivered_trace_ids = (
                {}
                if in_process_mode
                else _wait_for_replay_persistence(
                    client,
                    experiment_id,
                    replayed_trace_ids,
                )
            )
        except Exception as cause:
            raise ReplayError(
                str(cause),
                items=reported_items,
                experiment_id=experiment_id,
                experiment_url=full_experiment_url,
                cause=cause,
            ) from cause

        # Primary source for item["trace_id"]: the server's assigned traces.id, read
        # back per trace off the ingest response during the flush above (server-
        # sourced, no polling, already in hand before complete_replay). The
        # complete_replay map below remains the fallback for servers that don't
        # return ids on ingest.
        for item, local_id in zip(result_items, replayed_trace_ids):
            read_back = delivered_trace_ids.get(local_id)
            if read_back is not None:
                item["trace_id"] = read_back

        _raise_if_interrupted(
            interrupted, reported_items, experiment_id, full_experiment_url
        )
        interrupt_handlers.remove()
        try:
            complete_result = client.http_client.complete_replay(experiment_id)
        except Exception as cause:
            raise ReplayError(
                str(cause),
                items=reported_items,
                experiment_id=experiment_id,
                experiment_url=full_experiment_url,
                cause=cause,
            ) from cause

    server_trace_ids: dict[str, str] | None = complete_result.get("traceIds")
    # Per-replay-trace token usage keyed by server trace id: the REPLAYED run's
    # tokens (span-aggregated server-side), used below to fill each item's tokens.
    replay_tokens: dict[str, Any] = complete_result.get("tokens") or {}

    if server_trace_ids is not None:
        missing = []
        completed_count = 0
        for item, local_id in zip(result_items, replayed_trace_ids):
            mapped = server_trace_ids.get(local_id)
            # Fallback fill for servers that did not return ids on the ingest
            # response; the read-back loop above already set it when they did, so
            # never overwrite a resolved id with None here.
            if item["trace_id"] is None:
                item["trace_id"] = mapped
            if item["error"] is None:
                completed_count += 1
                if mapped is None:
                    missing.append(local_id)
            if mapped is not None:
                item["tokens"] = replay_tokens.get(mapped)
        # ALL completed items missing -> systemic (the replayed function is not
        # decorated with @span, or uploads are wholesale broken). Raise; the
        # run's traces never persisted, so nothing can be labeled.
        if completed_count > 0 and len(missing) == completed_count:
            trace_count = complete_result.get("traceCount")
            server_count = (
                f" The server persisted {trace_count} trace(s) for this run."
                if trace_count is not None
                else ""
            )
            cause = RuntimeError(
                f"Replay completed but the server has no persisted trace "
                f"for any of the {completed_count} completed item(s) "
                f"(experiment {experiment_id}).{server_count} Trace uploads "
                f"were flushed, so either the uploads failed (check for "
                f"'Bitfab: Failed to send request' errors above) or the "
                f"replayed function is not decorated with @span."
            )
            raise ReplayError(
                str(cause),
                items=reported_items,
                experiment_id=experiment_id,
                experiment_url=full_experiment_url,
                cause=cause,
            ) from cause
        # SOME completed items missing -> per-item upload failure. Log it, but
        # return the run; the items that landed can still be labeled.
        if missing:
            logger.error(
                f"Bitfab: server has no persisted trace for {len(missing)} of "
                f"{completed_count} completed replay item(s) "
                f"(experiment {experiment_id}). Their replay token usage is "
                f"unavailable and they cannot be labeled."
            )

    result = _replay_result(
        reported_items, experiment_id, full_experiment_url, resolved_attempts
    )
    # Persist the enriched result so the Bitfab plugin never has to parse the
    # replay's stdout, which a dependency's logging can corrupt.
    _write_replay_result_file(result)
    # Preserve the legacy terminal event only for on_progress. on_item_finish is
    # strictly item-scoped, so every invocation always includes an item.
    if on_item_finish is None and on_progress is not None:
        errored = sum(1 for it in reported_items if it["error"] is not None)
        total = len(reported_items)
        try:
            on_progress(
                {
                    "type": "complete",
                    "experiment_id": experiment_id,
                    "test_run_id": experiment_id,
                    "completed": total,
                    "total": total,
                    "succeeded": total - errored,
                    "errored": errored,
                    "result": result,
                }
            )
        except Exception:
            logger.error("Bitfab: replay on_progress callback raised", exc_info=True)
    return result


_CC_MAX_FILES = 60
_CC_MAX_FILE_BYTES = 500_000
_CC_MAX_TOTAL_BYTES = 2_000_000


def _resolve_auto_code_change(
    label: str | None = None,
) -> tuple[str | None, list[CodeChangeFile] | None] | None:
    """Auto-capture the code change to attach when the caller passed none.

    Lives in ``replay()`` (the one call guaranteed to run on every replay) so it
    works no matter how the replay was launched. Precedence: a
    ``BITFAB_CODE_CHANGE_PATH`` override, else the ``git diff`` of the working
    tree vs HEAD (or vs the merge-base with ``BITFAB_CODE_CHANGE_BASE``). All
    best-effort: any failure yields ``None`` and the replay proceeds with no
    code change. An explicit ``code_change_files`` always wins over this.
    """
    if os.environ.get("BITFAB_DISABLE_CODE_CHANGE_CAPTURE"):
        return None
    from_env = _read_code_change_file()
    if from_env is not None:
        return from_env
    return _capture_code_change_from_git(os.getcwd(), label)


def _read_code_change_file() -> tuple[str | None, list[CodeChangeFile] | None] | None:
    path = os.environ.get("BITFAB_CODE_CHANGE_PATH")
    if not path:
        return None
    try:
        with open(path, encoding="utf-8") as f:
            parsed = json.load(f)
        files = parsed.get("files")
        if not isinstance(files, list) or not all(isinstance(x, dict) for x in files):
            # A malformed payload (non-list, or entries that aren't mappings)
            # must yield no code change, never crash replay() downstream.
            files = None
        description = parsed.get("description")
        if not isinstance(description, str):
            description = None
        if files is None and description is None:
            return None
        return description, files
    except Exception:
        return None


def _git(cwd: str, args: list[str]) -> str | None:
    return run_git(cwd, args, timeout=30)


def _cc_ref_exists(root: str, ref: str) -> bool:
    return _git(root, ["rev-parse", "--verify", f"{ref}^{{object}}"]) is not None


def _cc_resolve_base(root: str) -> tuple[str, str] | None:
    """Return (base, against): HEAD by default, so only uncommitted edits show.

    ``BITFAB_CODE_CHANGE_BASE`` moves the base to the merge-base with that ref.
    """
    forced = os.environ.get("BITFAB_CODE_CHANGE_BASE")
    if forced and _cc_ref_exists(root, forced):
        mb = _git(root, ["merge-base", "HEAD", forced])
        if mb and mb.strip():
            return mb.strip(), f"vs {forced}"
        rp = _git(root, ["rev-parse", "--verify", forced])
        return (rp.strip(), f"vs {forced}") if rp and rp.strip() else None
    return ("HEAD", "uncommitted (vs HEAD)") if _cc_ref_exists(root, "HEAD") else None


def _cc_blob_bytes(root: str, ref: str, path: str) -> int:
    out = _git(root, ["cat-file", "-s", f"{ref}:{path}"])
    try:
        return int(out.strip()) if out and out.strip() else 0
    except Exception:
        return 0


def _cc_working_bytes(root: str, path: str) -> int:
    try:
        return os.path.getsize(os.path.join(root, path))
    except Exception:
        return 0


def _capture_code_change_from_git(
    cwd: str, label: str | None = None
) -> tuple[str | None, list[CodeChangeFile] | None] | None:
    try:
        root = _git(cwd, ["rev-parse", "--show-toplevel"])
        if not root or not root.strip():
            return None
        root = root.strip()
        resolved = _cc_resolve_base(root)
        if not resolved:
            return None
        base, against = resolved

        tracked = (
            _git(
                root,
                [
                    "diff",
                    "--name-status",
                    "--find-renames",
                    "-z",
                    base,
                    "--",
                    ":!.bitfab",
                ],
            )
            or ""
        )
        untracked = (
            _git(
                root,
                ["ls-files", "--others", "--exclude-standard", "-z", "--", ":!.bitfab"],
            )
            or ""
        )
        entries = _cc_parse_name_status_z(tracked)
        entries += [("A", p, p) for p in untracked.split("\0") if p]
        if not entries:
            return None

        files: list[CodeChangeFile] = []
        total = 0
        for status, before_path, path in entries:
            if len(files) >= _CC_MAX_FILES:
                break
            # Skip oversized files by size BEFORE reading their full contents,
            # so a huge changed file can't OOM/stall replay just to be discarded.
            before_bytes = (
                0 if status == "A" else _cc_blob_bytes(root, base, before_path)
            )
            after_bytes = 0 if status == "D" else _cc_working_bytes(root, path)
            if before_bytes > _CC_MAX_FILE_BYTES or after_bytes > _CC_MAX_FILE_BYTES:
                continue
            # Normalize CRLF -> LF on both sides: git's blob is already
            # LF-normalized (autocrlf clean), so a raw CRLF working file would
            # otherwise skew every line as changed.
            before = (
                ""
                if status == "A"
                else (_git(root, ["show", f"{base}:{before_path}"]) or "")
            ).replace("\r\n", "\n")
            after = (
                "" if status == "D" else _cc_read_working_file(root, path)
            ).replace("\r\n", "\n")
            if before == after:
                continue
            # Bytes, not chars, to match Ruby's bytesize and the byte cap.
            size = len(before.encode("utf-8")) + len(after.encode("utf-8"))
            if (
                total + size > _CC_MAX_TOTAL_BYTES
                or _cc_looks_binary(before)
                or _cc_looks_binary(after)
            ):
                continue
            total += size
            files.append({"path": path, "before": before, "after": after})

        if not files:
            return None

        subject = _git(root, ["log", "-1", "--format=%s", "HEAD"])
        subject = subject.strip() if subject else ""
        head = (
            (label.strip() if label and label.strip() else "")
            or subject
            or "Working-tree change"
        )
        word = "file" if len(files) == 1 else "files"
        return f"{head} ({len(files)} {word} changed {against})", files
    except Exception:
        return None


def _cc_parse_name_status_z(raw: str) -> list[tuple[str, str, str]]:
    parts = [p for p in raw.split("\0") if p]
    out: list[tuple[str, str, str]] = []
    i = 0
    while i + 1 < len(parts):
        status = parts[i][0]
        before_path = parts[i + 1]
        i += 2
        if status in ("R", "C") and i < len(parts):
            out.append((status, before_path, parts[i]))
            i += 1
        else:
            out.append((status, before_path, before_path))
    return out


def _cc_read_working_file(root: str, path: str) -> str:
    try:
        with open(os.path.join(root, path), encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def _cc_looks_binary(s: str) -> bool:
    return "\0" in s[:8000]


def _absorb_persisted_trace_ids(
    read_back_trace_ids: dict[str, str],
    status: dict[str, Any],
) -> set[str]:
    trace_ids = status.get("traceIds")
    if not isinstance(trace_ids, dict):
        return set()
    for trace_id, server_trace_id in trace_ids.items():
        if isinstance(server_trace_id, str):
            read_back_trace_ids[trace_id] = server_trace_id
    return set(trace_ids)


def _wait_for_replay_persistence(
    client: Bitfab,
    experiment_id: str,
    replayed_trace_ids: list[str],
    timeout: float | None = None,
) -> dict[str, str]:
    """Block until the server has persisted every replay trace this run queued.

    In the normal case the verdict is local: ingestion commits a request's
    carriers before it answers, so a flush that delivered every carrier has
    already proven the traces are whole and polling only asked the server to
    repeat itself. Acks cannot settle a request that timed out client-side after
    the server committed, so anything short of fully delivered falls through to
    the server poll, which stays the authority there.

    Returns the server-assigned ``traces.id`` for each replay trace, keyed by
    the client-side replay trace id. It comes off the OTLP ingest response
    during the flush, or, for a trace that had to be polled for, off the status
    answer that found it. Empty when the server predates that field or nothing
    was delivered.
    """
    if timeout is None:
        timeout = _REPLAY_PERSISTENCE_TIMEOUT_SECONDS
    release = client.http_client.release_held_external_spans
    if release is not None:
        release(plan_wait_slice(timeout))

    # Checked before flushing: a run whose traces never closed submitted nothing
    # to wait on, and must not emit an export request just to discover that.
    if not client.http_client.has_closed_deliveries(replayed_trace_ids):
        client.http_client.take_trace_deliveries(replayed_trace_ids)
        return {}

    from bitfab.http import flush_traces

    # A failed flush is a hint, not a verdict. It means delivery was not
    # CONFIRMED within the deadline, which is not the same as lost: the export
    # timeout can fire while requests are still in flight and the server goes on
    # to persist every one of them. Failing here failed runs whose data had
    # fully landed.
    flushed = flush_traces(timeout)

    raw_deliveries = client.http_client.take_trace_deliveries(replayed_trace_ids)
    read_back_trace_ids: dict[str, str] = {}
    for trace_id, report in raw_deliveries.items():
        if report.server_trace_id is not None:
            read_back_trace_ids[trace_id] = report.server_trace_id
    deliveries = {
        trace_id: report for trace_id, report in raw_deliveries.items() if report.closed
    }
    expected_span_counts = {
        trace_id: report.span_count for trace_id, report in deliveries.items()
    }
    if not expected_span_counts or all(
        report.delivered for report in deliveries.values()
    ):
        return read_back_trace_ids

    deadline = time.monotonic() + timeout
    missing = set(expected_span_counts)

    while missing:
        status = client.http_client.get_replay_status(
            experiment_id,
            expected_span_counts,
        )
        ready = _absorb_persisted_trace_ids(read_back_trace_ids, status)
        missing = set(expected_span_counts) - ready
        if not missing:
            return read_back_trace_ids
        if time.monotonic() >= deadline:
            break
        time.sleep(min(0.1, max(0.0, deadline - time.monotonic())))

    cause = (
        ""
        if flushed
        else (
            " Delivery was also not confirmed before the flush deadline, so the "
            "spans likely never reached the server."
        )
    )
    raise RuntimeError(
        "Replay traces were not fully persisted before the delivery deadline "
        f"(experiment {experiment_id}, missing {len(missing)} of "
        f"{len(expected_span_counts)} trace(s)).{cause}"
    )


def execute_replay_item(
    client: Bitfab,
    fn: Callable,
    *,
    experiment_id: str | None,
    server_item: dict[str, Any],
    replayed_trace_id: str,
    attempt: int = 0,
    trace_function_key: str | None = None,
    mock: MockStrategy = "marked",
    mock_override: MockOverrideInput | list[MockOverrideInput] | None = None,
    adapt_inputs: (
        Callable[
            [list[Any], dict[str, Any], AdaptContext], tuple[list[Any], dict[str, Any]]
        ]
        | None
    ) = None,
    db_branch: DbBranchOptions | bool | None = None,
    dry_run: bool = False,
    delivery_timeout: float | None = None,
) -> ReplayItem:
    """Run one assigned work item against an experiment another process minted.

    The child half of ``primitive="process"``. It never starts a replay: the
    parent already called ``/replay/start`` and owns the run, so this executes
    exactly the item it was handed and returns it. Delivery is confirmed here,
    in the process that produced the spans, because the parent's transport
    never sees them.
    """
    fn, trace_function_key, auto_wrapped = _resolve_replay_fn(
        client, fn, trace_function_key
    )
    include_db_branch_lease = _db_branch_enabled(db_branch) and not dry_run
    client.http_client.track_trace_deliveries([replayed_trace_id])
    item, _had_error = asyncio.run(
        _process_item_async(
            client,
            server_item,
            fn,
            experiment_id,
            mock,
            adapt_inputs,
            include_db_branch_lease,
            _db_branch_settings(db_branch),
            dict_input_as_positional=auto_wrapped,
            mock_overrides=[
                *normalize_mock_overrides(mock_override),
                *client._mock_overrides,
            ],
            replayed_trace_id=replayed_trace_id,
            dry_run=dry_run,
            attempt=attempt,
        )
    )
    if not dry_run:
        # A delivery failure degrades this item rather than failing the run: the
        # parent still has the server's own map from complete_replay, and one
        # child that could not confirm must not take the other N-1 with it.
        try:
            delivered = _wait_for_replay_persistence(
                client, experiment_id, [replayed_trace_id], delivery_timeout
            )
        except Exception as cause:
            logger.warning(
                "Bitfab: replay item %s could not confirm trace delivery: %s",
                replayed_trace_id,
                cause,
            )
            delivered = {}
        read_back = delivered.get(replayed_trace_id)
        if read_back is not None:
            item["trace_id"] = read_back
    return item


def _write_replay_result_file(result: ReplayResult) -> None:
    result_path = os.environ.get("BITFAB_REPLAY_RESULT_PATH")
    if not result_path:
        return

    try:
        parent = os.path.dirname(result_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(result_path, "w", encoding="utf-8") as f:
            f.write(f"{serialize_replay_result(result)}\n")
    except Exception as exc:
        logger.warning(
            "Bitfab: failed to write replay result to "
            "BITFAB_REPLAY_RESULT_PATH (%s): %s",
            result_path,
            exc,
        )


def _expand_replay_work(
    server_items: list[dict[str, Any]], attempts: int
) -> list[tuple[dict[str, Any], int]]:
    return [
        (server_item, attempt)
        for attempt in range(attempts)
        for server_item in server_items
    ]


def _stored_db_branch(replay_data: dict[str, Any]) -> DbBranchOptions | bool:
    if not replay_data.get("includeDbBranchLease"):
        return False
    settings = replay_data.get("dbBranchSettings") or {}
    options = DbBranchOptions()
    if settings.get("minCu") is not None:
        options["min_cu"] = settings["minCu"]
    if settings.get("maxCu") is not None:
        options["max_cu"] = settings["maxCu"]
    if settings.get("warmupSql") is not None:
        options["warmup_sql"] = settings["warmupSql"]
    return options or True


def _stop_heartbeat_then_interrupt(
    stop_heartbeat: Callable[[], None], client: Bitfab, experiment_id: str
) -> bool:
    stop_heartbeat()
    return client.http_client.interrupt_replay(experiment_id)


def _raise_if_interrupted(
    interrupted: Callable[[], bool],
    items: list[ReplayItem],
    experiment_id: str,
    experiment_url: str,
) -> None:
    if not interrupted():
        return
    message = (
        f"Experiment {experiment_id} was interrupted, so it was not completed or "
        f'graded. Resume it by passing resume="{experiment_id}" to replay, or with '
        f"bitfab-replay --resume {experiment_id}."
    )
    cause = RuntimeError(message)
    raise ReplayError(
        message,
        items=items,
        experiment_id=experiment_id,
        experiment_url=experiment_url,
        cause=cause,
    ) from cause


def _resumed_replay_work(
    server_items: list[dict[str, Any]], work: list[dict[str, Any]]
) -> list[ReplayWorkItem]:
    return [(server_items[entry["itemIndex"]], entry["attempt"]) for entry in work]


def _carried_over_item(finished: dict[str, Any]) -> ReplayItem:
    original_trace_id = finished.get("originalTraceId")
    return ReplayItem(
        input=[],
        result=None,
        original_output=None,
        error=(
            "This item errored before the experiment was resumed."
            if finished.get("hasError")
            else None
        ),
        trace_error=None,
        replay_error=None,
        duration_ms=None,
        original_duration_ms=None,
        original_tokens=None,
        original_model=None,
        ingestion_type=None,
        tokens=None,
        model=None,
        trace_id=finished.get("traceId"),
        original_trace_id=original_trace_id,
        original_span_id=None,
        source_trace_id=original_trace_id,
        source_span_id=None,
        db_snapshot_ref=None,
        db_branch_timings=None,
        attempt=int(finished.get("attempt") or 0),
        carried_over=True,
    )


def carried_over_progress_counts(
    carried_over_items: list[ReplayItem],
) -> dict[str, int]:
    errored = sum(1 for item in carried_over_items if item["error"] is not None)
    finished = len(carried_over_items)
    return {
        "started": finished,
        "completed": finished,
        "succeeded": finished - errored,
        "errored": errored,
    }


def _refuse_selection_with_resume(
    resume: str,
    *,
    limit: int | None,
    trace_ids: list[str] | None,
    dataset_id: str | None,
    dataset_ids: list[str] | None,
    attempts: int | _ConcurrencyUnset,
    grader_ids: list[str] | None,
    only_with_assertions: bool,
    dry_run: bool,
    experimental_selective_replay: SelectiveReplayOptions | None,
) -> None:
    passed = [
        name
        for name, given in (
            ("trace_ids", trace_ids is not None),
            ("limit", limit is not None),
            ("dataset_id", dataset_id is not None),
            ("dataset_ids", dataset_ids is not None),
            ("attempts", not isinstance(attempts, _ConcurrencyUnset)),
            ("grader_ids", grader_ids is not None),
            ("only_with_assertions", only_with_assertions),
            ("dry_run", dry_run),
            (
                "experimental_selective_replay",
                experimental_selective_replay is not None,
            ),
        )
        if given
    ]
    if passed:
        raise ValueError(
            f"resume continues experiment {resume} with the traces, attempts and "
            "graders it was started with, so it cannot be combined with "
            f"{', '.join(passed)}. Drop them, or start a new replay."
        )


async def _run_replay_async(
    client: Bitfab,
    server_items: list[dict[str, Any]],
    fn: Callable,
    experiment_id: str | None,
    max_concurrency: int | None,
    mock: MockStrategy,
    adapt_inputs: (
        Callable[
            [list[Any], dict[str, Any], AdaptContext], tuple[list[Any], dict[str, Any]]
        ]
        | None
    ) = None,
    include_db_branch_lease: bool = False,
    db_branch_settings: dict[str, Any] | None = None,
    *,
    dict_input_as_positional: bool = False,
    on_item_start: Callable[[ReplayItemStartProgress], None] | None = None,
    on_item_finish: Callable[[ReplayItemFinishProgress], None] | None = None,
    mock_overrides: list[MockOverride] | None = None,
    replayed_trace_ids: list[str] | None = None,
    dry_run: bool = False,
    attempts: int = 1,
    work_items: list[ReplayWorkItem] | None = None,
    carried_over_items: list[ReplayItem] | None = None,
    experimental_selective_replay: SelectiveReplayOptions | None = None,
) -> list[ReplayItem]:
    """Process all replay items concurrently using asyncio.gather."""
    _validate_max_concurrency(max_concurrency)
    semaphore = (
        asyncio.Semaphore(max_concurrency) if max_concurrency is not None else None
    )
    if work_items is None:
        work_items = _expand_replay_work(server_items, attempts)
    carried_over_items = carried_over_items or []

    # One client-side correlation id per item, tagging that item's replay spans
    # so replay() can map it to the server row id. Supplied by replay(); only
    # generated here as a fallback for direct unit-test calls.
    if replayed_trace_ids is None:
        replayed_trace_ids = [str(uuid.uuid4()) for _ in work_items]

    total = len(work_items) + len(carried_over_items)
    # Mutated only from the single event loop below, so no lock is needed.
    counts = carried_over_progress_counts(carried_over_items)

    def report_start(server_item: dict[str, Any], attempt: int) -> None:
        counts["started"] += 1
        if on_item_start is None:
            return
        original_trace_id = server_item.get("originalTraceId") or server_item.get(
            "sourceTraceId"
        )
        original_span_id = server_item.get("originalSpanId") or server_item.get(
            "sourceSpanId"
        )
        try:
            on_item_start(
                ReplayItemStartProgress(
                    type="started",
                    experiment_id=experiment_id,
                    test_run_id=experiment_id,
                    started=counts["started"],
                    completed=counts["completed"],
                    total=total,
                    succeeded=counts["succeeded"],
                    errored=counts["errored"],
                    item={
                        "original_trace_id": original_trace_id,
                        "original_span_id": original_span_id,
                        "source_trace_id": original_trace_id,
                        "source_span_id": original_span_id,
                        "attempt": attempt,
                    },
                )
            )
        except Exception:
            logger.debug("Bitfab: replay on_item_start callback raised", exc_info=True)

    from bitfab.http import flush_traces

    # Flush an item's trace the moment it finishes, so its server traces.id is
    # read back off the ingest response and surfaced on the item as it settles,
    # instead of waiting for the end-of-run barrier. Waiting until the end is
    # worst at low concurrency: each trace is closed and ready when its item
    # finishes, but nothing fills a batch to force an export, so ready ids sit in
    # the queue for the whole run. Coalesced so a burst of concurrent finishes
    # shares one flush: while a flush runs, later finishers set ``pending`` and
    # await the same task, which loops once more to cover them.
    flush_state: dict[str, Any] = {"pending": False, "task": None}

    async def flush_finished_item_trace() -> None:
        flush_state["pending"] = True
        if flush_state["task"] is None:

            async def _run() -> None:
                try:
                    while flush_state["pending"]:
                        flush_state["pending"] = False
                        await asyncio.to_thread(
                            flush_traces, _REPLAY_PERSISTENCE_TIMEOUT_SECONDS
                        )
                finally:
                    flush_state["task"] = None

            flush_state["task"] = asyncio.ensure_future(_run())
        await flush_state["task"]

    async def report_finish(
        settled_item: ReplayItem,
        had_error: bool,
        replayed_trace_id: str,
        attempt: int,
    ) -> None:
        # Deliver this item's trace now, then read its server id back off the
        # ingest response. A flush failure never crashes the run: the id degrades
        # to None and the end-of-run barrier stays the authority on persistence.
        try:
            await flush_finished_item_trace()
            server_trace_id = client.http_client.peek_server_trace_id(replayed_trace_id)
        except Exception:
            logger.debug("Bitfab: replay per-item flush failed", exc_info=True)
            server_trace_id = None
        if server_trace_id is not None:
            settled_item["trace_id"] = server_trace_id
        # No await from here to the emit, so each event's running totals stay a
        # consistent snapshot even when items flush concurrently.
        counts["completed"] += 1
        if had_error:
            counts["errored"] += 1
        else:
            counts["succeeded"] += 1
        if on_item_finish is not None:
            try:
                on_item_finish(
                    ReplayItemFinishProgress(
                        experiment_id=experiment_id,
                        test_run_id=experiment_id,
                        completed=counts["completed"],
                        total=total,
                        succeeded=counts["succeeded"],
                        errored=counts["errored"],
                        # The server's assigned traces.id, read back off the
                        # ingest response and surfaced as this item finishes. None
                        # only if the per-item flush could not confirm delivery in
                        # time; the end-of-run barrier then fills the returned
                        # ReplayItem. original_trace_id is the historical trace, so
                        # a UI can identify what settled; source_* are its
                        # deprecated aliases.
                        item=ReplayProgressItem(
                            trace_id=settled_item.get("trace_id"),
                            original_trace_id=settled_item.get("original_trace_id"),
                            original_span_id=settled_item.get("original_span_id"),
                            source_trace_id=settled_item.get("original_trace_id"),
                            source_span_id=settled_item.get("original_span_id"),
                            input=settled_item["input"],
                            result=settled_item.get("result"),
                            original_output=settled_item["original_output"],
                            error=settled_item["error"],
                            trace_error=settled_item.get("trace_error"),
                            replay_error=settled_item.get("replay_error"),
                            duration_ms=settled_item.get("duration_ms"),
                            original_duration_ms=settled_item.get(
                                "original_duration_ms"
                            ),
                            original_tokens=settled_item.get("original_tokens"),
                            original_model=settled_item.get("original_model"),
                            ingestion_type=settled_item.get("ingestion_type"),
                            tokens=settled_item.get("tokens"),
                            model=settled_item.get("model"),
                            db_snapshot_ref=settled_item.get("db_snapshot_ref"),
                            db_branch_timings=settled_item.get("db_branch_timings"),
                            attempt=attempt,
                            **(
                                {"selective_replay": settled_item["selective_replay"]}
                                if "selective_replay" in settled_item
                                else {}
                            ),
                        ),
                    )
                )
            except Exception:
                # Progress UI must never crash the replay run.
                logger.debug(
                    "Bitfab: replay on_item_finish callback raised", exc_info=True
                )

    async def process_with_limit(
        server_item: dict[str, Any],
        attempt: int,
        replayed_trace_id: str,
    ) -> tuple[ReplayItem, bool]:
        # The whole per-item pipeline (start, run, flush, report) runs under the
        # concurrency limit, so the flush and its emit stay serialized with the
        # rest of the item exactly as the other SDKs do: an item's finish is fully
        # reported before the next item under a limit of one begins.
        async def run_one() -> tuple[ReplayItem, bool]:
            report_start(server_item, attempt)
            result = await _process_item_async(
                client,
                server_item,
                fn,
                experiment_id,
                mock,
                adapt_inputs,
                include_db_branch_lease,
                db_branch_settings,
                dict_input_as_positional=dict_input_as_positional,
                mock_overrides=mock_overrides,
                replayed_trace_id=replayed_trace_id,
                dry_run=dry_run,
                attempt=attempt,
                experimental_selective_replay=experimental_selective_replay,
            )
            await report_finish(result[0], result[1], replayed_trace_id, attempt)
            return result

        if semaphore:
            async with semaphore:
                return await run_one()
        return await run_one()

    results = await asyncio.gather(
        *(
            process_with_limit(item, attempt, tid)
            for (item, attempt), tid in zip(work_items, replayed_trace_ids)
        )
    )
    return [item for item, _ in results]


async def _process_item_async(
    client: Bitfab,
    server_item: dict[str, Any],
    fn: Callable,
    experiment_id: str | None,
    mock: MockStrategy,
    adapt_inputs: (
        Callable[
            [list[Any], dict[str, Any], AdaptContext], tuple[list[Any], dict[str, Any]]
        ]
        | None
    ) = None,
    include_db_branch_lease: bool = False,
    db_branch_settings: dict[str, Any] | None = None,
    *,
    dict_input_as_positional: bool = False,
    mock_overrides: list[MockOverride] | None = None,
    replayed_trace_id: str | None = None,
    dry_run: bool = False,
    attempt: int = 0,
    experimental_selective_replay: SelectiveReplayOptions | None = None,
) -> tuple[ReplayItem, bool]:
    """Fetch span data and execute a single replay item.

    Any error while fetching the span, building the mock tree, or
    deserializing inputs is captured on the returned item's ``error`` field
    rather than propagated, so one bad trace never aborts the whole replay
    run (mirrors the TypeScript SDK's per-item ``try/catch``).
    """
    metrics: dict[str, Any] | None = None
    # The server resolves a Neon preview branch per item during /replay/start
    # (only when include_db_branch_lease was sent). Release it in ``finally`` so
    # any throw (fetch, mock-tree build, or the customer fn) frees the Neon
    # resource. Items whose source trace had no snapshot ref arrive without a
    # lease (``get_current_replay_branch()`` returns None), so the app uses its
    # normal DB path. Unsafe calls on that path still require replay mocking.
    lease = server_item.get("dbBranchLease") if include_db_branch_lease else None
    # A resolve that was ATTEMPTED and failed is different: the caller asked for
    # a branch, so running their function against live data would produce a
    # result that looks valid and is not. Fail the item instead, loudly.
    lease_error = (
        server_item.get("dbBranchLeaseError") if include_db_branch_lease else None
    )
    db_snapshot_ref = server_item.get("dbSnapshotRef")
    # Reported whichever way the resolve went, so it is tracked separately from
    # both the lease and the error rather than hanging off either.
    db_branch_timings = (
        server_item.get("dbBranchTimings") if include_db_branch_lease else None
    )
    # The ORIGINAL (historical) trace/span this item replays. Canonical server
    # keys are originalTraceId/originalSpanId; older servers only send the
    # deprecated sourceTraceId/sourceSpanId aliases.
    original_trace_id = server_item.get("originalTraceId") or server_item.get(
        "sourceTraceId"
    )
    original_span_id = server_item.get("originalSpanId") or server_item.get(
        "sourceSpanId"
    )
    try:
        selective = (
            SelectiveReplayRuntime(
                server_item.get("selectiveReplayPlan"), experimental_selective_replay
            )
            if experimental_selective_replay is not None
            else None
        )
        if include_db_branch_lease and not lease and not lease_error:
            try:
                resolved = await asyncio.to_thread(
                    client.http_client.resolve_db_branch_lease,
                    experiment_id,
                    original_trace_id,
                    db_branch_settings,
                    attempt,
                )
            except Exception as cause:
                raise DbBranchReplayError(
                    "lease_request_failed",
                    f"Bitfab could not request the database branch: {cause}",
                    original_trace_id,
                    cause=cause,
                ) from cause
            lease = resolved.get("lease")
            lease_error = resolved.get("leaseError")
            db_snapshot_ref = resolved.get("dbSnapshotRef") or db_snapshot_ref
            db_branch_timings = resolved.get("timings") or db_branch_timings

        if lease_error:
            raise DbBranchReplayError(
                str(lease_error.get("code")),
                str(lease_error.get("message")),
                original_trace_id,
            )

        metrics = _extract_server_item_metrics(server_item)
        span = await asyncio.to_thread(
            client.http_client.get_external_span,
            original_span_id,
            replay_view=True,
        )
        item_data = _extract_span_data(span)

        # Fetch the span tree whenever it's needed: the "all"/"marked" base
        # strategies read recorded outputs from it, and overrides need it both
        # to resolve each node's source_span_id and to gate the per-(key, name)
        # call counter, so overrides can fire even under mock="none".
        #
        # Only "all" fetches outputs inline: when every span is mocked, one
        # bulk tree is cheaper than N lazy fetches, even when overrides exist.
        # Non-"all" runs that need a tree ("marked", or "none" with overrides)
        # fetch it payload-free and pull only the few outputs they mock, lazily.
        has_overrides = bool(mock_overrides)
        include_outputs = mock == "all"
        mock_tree: dict[str, dict[str, Any]] | None = None
        mock_tree_has_variants = False
        fetch_span_output: Callable[[str], Any] | None = None
        if selective is None and (mock == "all" or mock == "marked" or has_overrides):
            try:
                tree = await asyncio.to_thread(
                    client.http_client.get_span_tree,
                    original_span_id,
                    include_outputs,
                    False,
                )
                mock_tree = MATCHER.build_index(tree.get("root") or {})
                mock_tree_has_variants = MATCHER.records_variants(
                    tree.get("root") or {}
                )
            except Exception:
                if mock != "marked" or has_overrides:
                    raise
                # Keep an active empty tree so the root can still run, while
                # any marked child fails closed at its call site.
                mock_tree = {}
            # A memoized lazy fetcher is present only when outputs were NOT
            # fetched inline: its presence signals the mock path to fetch each
            # mocked span's recorded output on demand. Nodes that still carried
            # an inline output (older servers) are used directly, no fetch.
            if mock_tree is not None and not include_outputs:
                fetch_span_output = _make_span_output_fetcher(client)

        original_metadata = server_item.get("originalMetadata")
        adapt_ctx: AdaptContext = {
            "original_trace_id": original_trace_id,
            "original_span_id": original_span_id,
            # Deprecated aliases for original_trace_id/original_span_id.
            "source_trace_id": original_trace_id,
            "source_span_id": original_span_id,
            "metadata": dict(original_metadata)
            if isinstance(original_metadata, dict)
            else {},
        }

        return await _execute_item_async(
            item_data,
            fn,
            experiment_id,
            span["id"],
            metrics,
            input_source_trace_id=span.get("externalTraceId"),
            mock_strategy=mock,
            mock_tree=mock_tree,
            mock_tree_has_variants=mock_tree_has_variants,
            adapt_inputs=adapt_inputs,
            adapt_ctx=adapt_ctx,
            db_snapshot_ref=db_snapshot_ref,
            db_branch_lease=lease,
            db_branch_timings=db_branch_timings,
            source_bitfab_trace_id=original_trace_id,
            dict_input_as_positional=dict_input_as_positional,
            mock_overrides=mock_overrides,
            fetch_span_output=fetch_span_output,
            replayed_trace_id=replayed_trace_id,
            dry_run=dry_run,
            attempt=attempt,
            selective_replay=selective,
        )
    except Exception as e:
        logger.warning(
            f"Replay item for span {original_span_id} failed before execution: {e}"
        )
        failed_item = ReplayItem(
            input=[],
            result=None,
            original_output=None,
            error=_replay_item_error_message(e),
            trace_error=None,
            replay_error=e,
            duration_ms=None,
            original_duration_ms=metrics.get("original_duration_ms")
            if metrics
            else None,
            original_tokens=metrics.get("original_tokens") if metrics else None,
            original_model=metrics.get("original_model") if metrics else None,
            ingestion_type=metrics.get("ingestion_type") if metrics else None,
            tokens=metrics.get("tokens") if metrics else None,
            model=metrics.get("original_model") if metrics else None,
            trace_id=None,
            original_trace_id=original_trace_id,
            original_span_id=original_span_id,
            # Deprecated aliases for original_trace_id/original_span_id.
            source_trace_id=original_trace_id,
            source_span_id=original_span_id,
            db_snapshot_ref=db_snapshot_ref,
            db_branch_timings=db_branch_timings,
            attempt=attempt,
            carried_over=False,
        )
        return failed_item, True
    finally:
        if lease:
            await _release_lease(client, lease)


async def _release_lease(client: Bitfab, lease: dict[str, Any]) -> None:
    """Delete the per-item Neon preview branch. Best-effort: a failure is
    logged but never raised: the server-side TTL janitor reaps orphans.
    """
    neon_branch_id = lease.get("neonBranchId")
    if not neon_branch_id:
        return
    try:
        await asyncio.to_thread(
            client.http_client.release_db_branch_lease, neon_branch_id
        )
    except Exception as e:
        logger.warning(
            f"Bitfab: failed to release DB branch {neon_branch_id} "
            f"(TTL janitor will catch it): {e}"
        )


def _extract_server_item_metrics(
    server_item: dict[str, Any],
) -> dict[str, Any]:
    """Pull the original trace's duration / tokens / model from the start item.

    Falls back to the unprefixed keys a server that predates the rename sends.
    ``tokens`` stays None here: it is the REPLAYED run's, filled in by
    ``replay()`` from the complete-replay response once the spans are
    aggregated server-side.
    """
    return {
        "original_duration_ms": server_item.get("originalDurationMs")
        if server_item.get("originalDurationMs") is not None
        else server_item.get("durationMs"),
        "original_tokens": server_item.get("originalTokens")
        if server_item.get("originalTokens") is not None
        else server_item.get("tokens"),
        "original_model": server_item.get("originalModel")
        if server_item.get("originalModel") is not None
        else server_item.get("model"),
        "ingestion_type": server_item.get("ingestionType"),
        "tokens": None,
    }


def _extract_span_data(span: dict[str, Any]) -> dict[str, Any]:
    """Extract input/output data and span options from an external span's rawData."""
    raw_data = span.get("rawData") or {}
    span_data = raw_data.get("span_data") or {}

    return {
        "input": span_data.get("input"),
        "output": span_data.get("output"),
        "inputSerialized": span_data.get("input_serialized"),
        "outputSerialized": span_data.get("output_serialized"),
    }


def _deserialize_span_output(span: dict[str, Any]) -> Any:
    """Deserialize the recorded output from a fetched external span's rawData.

    Mirrors the inline deserialization the base ``mock`` path applies to a mock
    tree entry: use the serialized ``{json, meta}`` form when present, otherwise
    the raw JSON-safe output. Fetching a span this way produces the same value
    the eager tree would have carried inline, so lazy and inline resolution
    agree.
    """
    raw_data = span.get("rawData") or {}
    span_data = raw_data.get("span_data") or {}
    output_serialized = span_data.get("output_serialized")
    if (
        output_serialized
        and isinstance(output_serialized, dict)
        and "meta" in output_serialized
    ):
        # Fail open like the inline base path: a deserialization error falls
        # back to the raw JSON-safe output rather than aborting the replay.
        with contextlib.suppress(Exception):
            return deserialize_value(output_serialized)
    return span_data.get("output")


def _make_span_output_fetcher(client: Bitfab) -> Callable[[str], Any]:
    """Build a per-item memoized fetcher: ``external_span_id -> deserialized
    output``. Blocking (Python replay already does blocking HTTP). Memoized so a
    span read twice (a marked mock plus an override's ``get_original_output``)
    fetches once.
    """
    cache: dict[str, Any] = {}

    def fetch_span_output(external_span_id: str) -> Any:
        if external_span_id in cache:
            return cache[external_span_id]
        span = client.http_client.get_external_span(external_span_id, replay_view=True)
        value = _deserialize_span_output(span)
        cache[external_span_id] = value
        return value

    return fetch_span_output


async def _execute_item_async(
    item: dict[str, Any],
    fn: Callable,
    experiment_id: str | None,
    input_source_span_id: str | None = None,
    metrics: dict[str, Any] | None = None,
    input_source_trace_id: str | None = None,
    mock_strategy: MockStrategy = "marked",
    mock_tree: dict[str, dict[str, Any]] | None = None,
    mock_tree_has_variants: bool = False,
    adapt_inputs: (
        Callable[
            [list[Any], dict[str, Any], AdaptContext], tuple[list[Any], dict[str, Any]]
        ]
        | None
    ) = None,
    adapt_ctx: AdaptContext | None = None,
    db_snapshot_ref: dict[str, Any] | None = None,
    db_branch_lease: dict[str, Any] | None = None,
    db_branch_timings: dict[str, Any] | None = None,
    source_bitfab_trace_id: str | None = None,
    dict_input_as_positional: bool = False,
    mock_overrides: list[MockOverride] | None = None,
    fetch_span_output: Callable[[str], Any] | None = None,
    replayed_trace_id: str | None = None,
    dry_run: bool = False,
    attempt: int = 0,
    selective_replay: SelectiveReplayRuntime | None = None,
) -> tuple[ReplayItem, bool]:
    """Execute a single replay item: deserialize inputs, call fn with replay context.

    Sets the replay context so the existing @span decorator picks up
    experiment_id, input_source_span_id, and input_source_trace_id, then calls fn
    through its full decorator chain.

    Returns:
        Tuple of (ReplayItem, had_error)
    """
    args, kwargs = _deserialize_inputs(
        item, dict_input_as_positional=dict_input_as_positional
    )

    fn_result = None
    fn_error: BaseException | None = None
    replay_error: BaseException | None = None
    replay_duration_ms: int | None = None
    replay_started: float | None = None

    # Client-side correlation id that tags this item's replay spans so the
    # server can echo back the row id it minted (resolved in replay()'s
    # complete-replay loop). Supplied by the caller; only generated here as a
    # fallback for direct unit-test calls. Never surfaced as the item's trace_id.
    replayed_trace_id = replayed_trace_id or str(uuid.uuid4())
    replay_ctx: dict[str, Any] = {
        "experiment_id": experiment_id,
        "trace_id": replayed_trace_id,
        "replay_attempt": attempt,
    }
    if selective_replay is not None:
        replay_ctx["selective_replay"] = selective_replay
    if input_source_span_id is not None:
        replay_ctx["input_source_span_id"] = input_source_span_id
    if input_source_trace_id is not None:
        replay_ctx["input_source_trace_id"] = input_source_trace_id
    # The mock context is active when either the base strategy needs a tree
    # ("all"/"marked") or overrides are present. Overrides can fire under
    # mock="none" with no recorded tree, so the tree defaults to an empty dict
    # to keep the counter and lookup paths uniform.
    has_overrides = bool(mock_overrides)
    if mock_tree is not None or has_overrides:
        replay_ctx["mock_tree"] = mock_tree if mock_tree is not None else {}
        replay_ctx["mock_strategy"] = mock_strategy
        replay_ctx["call_counters"] = {}
        replay_ctx["mock_tree_has_variants"] = mock_tree_has_variants
        if has_overrides:
            replay_ctx["mock_overrides"] = mock_overrides
        # The memoized lazy output fetcher (payload-free tree path). Its
        # presence signals the mock path to fetch a mocked span's recorded
        # output on demand; absent under eager mock="all".
        if fetch_span_output is not None:
            replay_ctx["fetch_span_output"] = fetch_span_output
    # The per-trace DB branch (resolved server-side) and the Bitfab trace ID it
    # belongs to ride on the context so ReplayBranch can read them inside fn.
    # ReplayBranch sets "db_snapshot_accessed" on this context the first time
    # customer code actually obtains the branch URL (via the database_url
    # property). It is reported on the trace completion inside
    # db_snapshot_usage so the server can distinguish "branch was
    # provisioned and exposed" from "branch URL was actually consumed". Only an
    # explicit database_url read may set it. A path that hands the URL over by
    # other means (e.g. a process-isolated runner writing an env overlay) must
    # leave it alone: setting it there would make every such replay report
    # accessed for free, and the flag would stop separating "branch was used"
    # from "branch was offered".
    if db_branch_lease is not None:
        replay_ctx["db_branch_lease"] = db_branch_lease
    # Kept off ReplayBranch: customer code reads that mid-replay to reach the
    # branch, and provisioning latency is a property of the run, not of the
    # connection. It rides the context only to be echoed on the completion.
    if db_branch_timings is not None:
        replay_ctx["db_branch_timings"] = db_branch_timings
    if source_bitfab_trace_id is not None:
        replay_ctx["source_bitfab_trace_id"] = source_bitfab_trace_id
    token = _replay_context.set(replay_ctx)
    try:
        # Reshape recorded inputs onto the current signature when an adapter is
        # supplied. Inside the try so a raising adapter surfaces on this item's
        # error instead of crashing the gather; args is reported on the item.
        try:
            if adapt_inputs is not None:
                ctx: AdaptContext = adapt_ctx or {
                    "original_trace_id": None,
                    "original_span_id": input_source_span_id or "",
                    # Deprecated aliases for original_trace_id/original_span_id.
                    "source_trace_id": None,
                    "source_span_id": input_source_span_id or "",
                    "metadata": {},
                }
                args, kwargs = adapt_inputs(args, kwargs, ctx)
        except Exception as e:
            replay_error = e
        if replay_error is None and dry_run:
            # Inputs are resolved (fetch, deserialize, adapt) but nothing runs,
            # so the item reports the exact arguments fn would have received.
            pass
        elif replay_error is None:
            try:
                replay_started = time.perf_counter()
                if inspect.iscoroutinefunction(fn):
                    fn_result = await fn(*args, **kwargs)
                else:
                    fn_result = await asyncio.to_thread(fn, *args, **kwargs)
                replay_duration_ms = round(
                    (time.perf_counter() - replay_started) * 1000
                )
            except Exception as e:
                # The function ran and raised, so it still has a duration.
                if replay_started is not None:
                    replay_duration_ms = round(
                        (time.perf_counter() - replay_started) * 1000
                    )
                fn_error = e
    finally:
        if selective_replay is not None:
            try:
                selective_replay.assert_no_safety_conflict()
            except RuntimeError as error:
                replay_error = error
        _replay_context.reset(token)

    metrics = metrics or {}
    # Report kwargs alongside args: a kwargs-only call (e.g. a dict root
    # input splatted on the legacy path) would otherwise report input=[].
    reported_input = list(args) if not kwargs else [*args, kwargs]
    item_error = fn_error if fn_error is not None else replay_error
    replay_item = ReplayItem(
        input=reported_input,
        result=fn_result,
        original_output=item.get("output"),
        error=str(item_error) if item_error is not None else None,
        trace_error=fn_error,
        replay_error=replay_error,
        duration_ms=replay_duration_ms,
        original_duration_ms=metrics.get("original_duration_ms"),
        original_tokens=metrics.get("original_tokens"),
        original_model=metrics.get("original_model"),
        ingestion_type=metrics.get("ingestion_type"),
        tokens=metrics.get("tokens"),
        model=metrics.get("original_model"),
        # Written in by replay() from the complete-replay response once the
        # server has minted this replay trace's row. Null until then: the
        # client-side correlation id is never surfaced as the item's trace_id.
        trace_id=None,
        original_trace_id=source_bitfab_trace_id,
        original_span_id=input_source_span_id,
        # Deprecated aliases for original_trace_id/original_span_id.
        source_trace_id=source_bitfab_trace_id,
        source_span_id=input_source_span_id,
        db_snapshot_ref=db_snapshot_ref,
        db_branch_timings=db_branch_timings,
        attempt=attempt,
        carried_over=False,
    )
    if selective_replay is not None:
        replay_item["selective_replay"] = selective_replay.report()
    return replay_item, fn_error is not None or replay_error is not None


def _deserialize_inputs(
    item: dict[str, Any], *, dict_input_as_positional: bool = False
) -> tuple[list[Any], dict[str, Any]]:
    """Deserialize inputs from a replay item into (args, kwargs).

    ``inputSerialized`` is preferred whenever present, with or without type
    metadata: it is the only faithful record of the args/kwargs split, since
    the flat ``input`` appends kwargs as a trailing positional dict.

    A raw dict input with no serialization metadata is ambiguous: it's a
    kwargs mapping for decorator-recorded traces, but a single positional
    value for handler-recorded traces (the framework input, e.g. a LangGraph
    state). ``dict_input_as_positional`` (set when replay auto-wrapped a
    plain callable under an explicit key) resolves it as one positional
    argument, matching the TypeScript SDK; decorated functions always keep
    the kwargs splat.
    """
    input_serialized = item.get("inputSerialized")
    raw_input = item.get("input")

    if (
        input_serialized
        and isinstance(input_serialized, dict)
        and ("meta" in input_serialized or "json" in input_serialized)
    ):
        deserialized = deserialize_value(input_serialized)
        if isinstance(deserialized, dict):
            return deserialized.get("args", []), deserialized.get("kwargs", {})
        return [deserialized] if deserialized is not None else [], {}

    if isinstance(raw_input, list):
        return raw_input, {}
    if isinstance(raw_input, dict):
        if dict_input_as_positional:
            return [raw_input], {}
        return [], raw_input
    return [raw_input] if raw_input is not None else [], {}
