"""Read-only tools over what the platform observed of a workspace's pipelines."""

from __future__ import annotations

# Python internals
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Literal, Mapping, Optional

# Other libraries
from dlt.common.typing import Annotated

# Current package
from dlthub_mcp._access import CONTEXT_READ
from dlthub_mcp._client import tool, tool_error, workspace
from dlthub_mcp._paging import PAGE_SIZE, page, skip
from dlthub_sdk import (
    DatasetActivity,
    PipelineActivity,
    PipelineRun,
    PipelineRunStatus,
    Sync,
)
from dlthub_sdk.domain.telemetry import FILTERABLE_STATUSES

#: Days an activity listing covers when the caller does not say.
ACTIVITY_DAYS = 30
#: Rows an activity listing returns when the caller does not say.
ACTIVITY_PAGE_SIZE = 50
#: Days a listing covers when the caller does not say, and the ceiling.
WINDOW_DAYS = 7
MAX_WINDOW_DAYS = 365
#: Characters of trace returned when the caller does not say, and the ceiling.
TRACE_CHARS = 20_000
MAX_TRACE_CHARS = 200_000
#: The dlt steps a trace can carry, in the order they run.
TRACE_STEPS = ("extract", "normalize", "load")
#: What a step carries beyond its own outcome: metrics and load packages, whose
#: flattened schema update is one object per column of every table.
_STEP_BULK = "step_info"
#: Resolved config. dlt blanks the value of a *secret-hinted* field only, and
#: `PipelineTrace.asdict` never applies the entry's own value-dropping asdict, so
#: a credential resolved into a plain string arrives with its value intact.
_CONFIG = "resolved_config_values"
#: The fields of a resolved config entry that carry the value itself.
_CONFIG_VALUES = ("value", "default_value")
#: How a step ended, led with so a cut step still says that much.
_STEP_LEAD = ("step", "step_exception", "exception_traces")


def _window(days: int) -> tuple[datetime, datetime]:
    """Turn a day count into the window the platform requires.

    Args:
        days: How far back to look.

    Returns:
        The start and end of the window, in UTC.
    """
    end = datetime.now(timezone.utc)
    return end - timedelta(days=max(1, min(days, MAX_WINDOW_DAYS))), end


def _status(status: Optional[str]) -> Optional[PipelineRunStatus]:
    """Read a status filter, refusing one the platform cannot filter on.

    Args:
        status: What the caller asked for.

    Returns:
        The status, or ``None`` when the caller named none.

    Raises:
        Exception: A ``ToolError`` naming what is filterable.
    """
    if status is None:
        return None
    filterable = sorted(s.value for s in FILTERABLE_STATUSES)
    wanted = PipelineRunStatus(status)
    if wanted not in FILTERABLE_STATUSES:
        raise tool_error(
            f"{status!r} is not a status the platform filters on. "
            f"Use one of: {', '.join(filterable)}."
        )
    return wanted


@dataclass(frozen=True)
class PipelineRunTraceText:
    """One pipeline run's dlt trace, as text an agent can read.

    Served as text rather than as a structure: the platform stores the trace
    verbatim and declares no shape for it, and truncating a nested object would
    produce something that no longer parses.

    Attributes:
        pipeline_run_id: The pipeline run it belongs to.
        detail: Which slice of the trace this is.
        step: The step it was narrowed to, or ``None`` for all of them.
        trace: The requested slice as indented JSON, cut to ``max_chars``.
        truncated: Whether anything was cut. The steps are a list and a failing
            step is usually the last, so a cut trace may be missing the very
            exception you want — narrow ``step`` before raising ``max_chars``.
        total_chars: How long the requested slice is in full.
        omitted: What this slice left out, and how to ask for it. Empty for
            ``full``.
    """

    pipeline_run_id: str
    detail: str
    step: str | None
    trace: str
    truncated: bool
    total_chars: int
    omitted: tuple[str, ...]


def _without_values(entry: Any) -> Any:
    """Strip the value from one resolved config entry.

    Args:
        entry: One entry of a trace's resolved config.

    Returns:
        The entry without its value fields, or unchanged when it is not an
        object and there is no field to name.
    """
    if not isinstance(entry, dict):
        return entry
    return {k: v for k, v in entry.items() if k not in _CONFIG_VALUES}


def _slice(
    trace: Mapping[str, Any], detail: str, step: Optional[str]
) -> tuple[dict[str, Any], tuple[str, ...]]:
    """Cut a trace down to what was asked for.

    Args:
        trace: The trace as the platform stored it.
        detail: ``summary``, ``config`` or ``full``.
        step: One dlt step, or ``None`` for all of them.

    Returns:
        The slice, and a note of what it left out.
    """
    held = dict(trace)
    omitted: list[str] = []

    steps = held.get("steps")
    if isinstance(steps, list):
        wanted = [
            s
            for s in steps
            if step is None or (isinstance(s, dict) and s.get("step") == step)
        ]
        if step is not None:
            dropped = len(steps) - len(wanted)
            if dropped:
                omitted.append(f"{dropped} other step(s); pass step=None for all")
        if detail != "full":
            # Asked of the kept steps, not every step: a step nobody asked for
            # would otherwise send the agent to fetch `full` for no gain.
            dropping = any(isinstance(s, dict) and s.get(_STEP_BULK) for s in wanted)
            wanted = [
                {k: v for k, v in s.items() if k != _STEP_BULK}
                if isinstance(s, dict)
                else s
                for s in wanted
            ]
            if dropping:
                omitted.append("per-step metrics and load packages; pass detail='full'")
        held["steps"] = wanted

    config = held.get(_CONFIG)
    if detail == "summary" and config:
        del held[_CONFIG]
        omitted.append("resolved config; pass detail='config'")
    elif isinstance(config, list):
        held[_CONFIG] = [_without_values(entry) for entry in config]

    return held, tuple(omitted)


def _ordered_step(step: Mapping[str, Any]) -> dict[str, Any]:
    """Lead a step with how it ended.

    Args:
        step: One step of a trace.

    Returns:
        The step, its outcome first and the rest alphabetical.
    """
    lead = {k: step[k] for k in _STEP_LEAD if k in step}
    return {**lead, **{k: v for k, v in sorted(step.items()) if k not in lead}}


def _ordered(trace: Mapping[str, Any]) -> dict[str, Any]:
    """Lead a trace with its steps, because truncation cuts the tail.

    Args:
        trace: A trace slice.

    Returns:
        The slice with ``steps`` first and the rest alphabetical.
    """
    steps = trace.get("steps")
    if isinstance(steps, list):
        steps = [_ordered_step(s) if isinstance(s, dict) else s for s in steps]
    lead = {"steps": steps} if "steps" in trace else {}
    return {**lead, **{k: v for k, v in sorted(trace.items()) if k != "steps"}}


@dataclass(frozen=True)
class TelemetryStatusInfo:
    """How current this workspace's telemetry is.

    Attributes:
        updated_at: When telemetry last recorded anything, or ``None`` when it
            never has.
        stale_seconds: How long ago that was, or ``None`` when nothing has been
            recorded. A large number means the reading stopped moving, not that
            nothing ran.
        reporting: Whether telemetry has ever recorded anything here at all.
    """

    updated_at: datetime | None
    stale_seconds: float | None
    reporting: bool


@tool
def dlthub_telemetry_status() -> Annotated[TelemetryStatusInfo, CONTEXT_READ]:
    """When telemetry last recorded anything for this workspace.

    Reach for this before trusting a zero from any other telemetry answer: an
    empty pipeline list means "nothing ran" only if telemetry is current. If
    this is stale or has never reported, a zero says nothing about what the
    workspace actually did, and reporting that distinction is more useful than
    reporting the zero.

    Returns:
        The watermark, how old it is, and whether telemetry has ever reported.

    Raises:
        Exception: A ``ToolError`` when the caller may not read this
            workspace's telemetry.
    """
    status = workspace().telemetry.status()
    updated_at = status.updated_at
    stale = None
    if updated_at is not None:
        # tzinfo is passed through, not defaulted: mixing naive and aware raises.
        stale = (datetime.now(updated_at.tzinfo) - updated_at).total_seconds()
    return TelemetryStatusInfo(
        updated_at=updated_at,
        stale_seconds=stale,
        reporting=updated_at is not None,
    )


@tool
def dlthub_list_pipeline_runs(
    run_id: Optional[str] = None,
    pipeline_name: Optional[str] = None,
    status: Optional[Literal["succeeded", "failed"]] = None,
    dataset: Optional[str] = None,
    destination: Optional[str] = None,
    empty_only: bool = False,
    days: int = WINDOW_DAYS,
    limit: int = PAGE_SIZE,
    offset: int = 0,
) -> Annotated[list[PipelineRun[Sync]], CONTEXT_READ]:
    """The dlt pipeline runs telemetry recorded, newest first.

    **The only source of a pipeline run id**, which is what
    ``dlthub_get_pipeline_run`` and ``dlthub_get_pipeline_run_trace`` need. A
    pipeline run id is not a job run id and the two are not interchangeable.

    Pass ``run_id`` to see what one job run executed — the usual way in when a
    run failed. Omit it to ask across the workspace: which pipelines failed this
    week, what wrote to a dataset, which runs loaded nothing.

    Check ``dlthub_telemetry_status`` before trusting an empty result: telemetry
    that is stale or silent returns nothing regardless of what actually ran.

    Args:
        run_id: A job run's uuid, from ``dlthub_list_runs``.
        pipeline_name: Narrow to one dlt pipeline.
        status: Narrow to one outcome. ``succeeded`` and ``failed`` are the only
            two the platform filters on, so a run still going matches neither.
        dataset: Narrow to runs that wrote to one dataset.
        destination: Narrow to runs that wrote to one destination.
        empty_only: Only runs that loaded nothing, which is how a silently
            no-op pipeline shows up.
        days: How far back to look, at most 365. Every read covers a window
            because the platform requires one.
        limit: How many runs to return, at most 100.
        offset: How many to skip, for paging.

    Returns:
        Pipeline runs with their id, pipeline, status, row counts, timings and
        the step that broke when one did. Tables and load packages are read
        only by ``dlthub_get_pipeline_run``.

    Raises:
        Exception: A ``ToolError`` for a status the platform cannot filter on.
    """
    since, until = _window(days)
    runs = workspace().telemetry.pipeline_runs.list(
        job_run_id=run_id,
        pipeline_name=pipeline_name,
        status=_status(status),
        dataset=dataset,
        destination=destination,
        empty_only=True if empty_only else None,
        since=since,
        until=until,
        limit=page(limit),
        offset=skip(offset),
    )
    return list(runs)


@tool
def dlthub_get_pipeline_run(
    pipeline_run_id: str,
) -> Annotated[PipelineRun[Sync], CONTEXT_READ]:
    """One pipeline run in full: the tables it wrote and the packages it loaded.

    Reach for this once a listing names a pipeline run worth understanding. It
    adds what the listing withholds — rows per table, write dispositions, and
    the load packages, which is where a partial failure shows up as some
    packages complete and others not.

    For *why* it failed rather than *what* it wrote, read
    ``dlthub_get_pipeline_run_trace``.

    Args:
        pipeline_run_id: The pipeline run's uuid, from
            ``dlthub_list_pipeline_runs``. A job run id will not resolve.

    Returns:
        The pipeline run, with its tables and load packages.

    Raises:
        Exception: A ``ToolError`` when no such pipeline run exists, or the id
            is not a uuid.
    """
    return workspace().telemetry.pipeline_runs.get(id=pipeline_run_id)


@tool
def dlthub_get_pipeline_run_trace(
    pipeline_run_id: str,
    detail: Literal["summary", "config", "full"] = "summary",
    step: Optional[Literal["extract", "normalize", "load"]] = None,
    max_chars: int = TRACE_CHARS,
) -> Annotated[PipelineRunTraceText, CONTEXT_READ]:
    """The dlt trace of one pipeline run — where the exception actually is.

    The end of the diagnosis chain and usually the answer. A trace holds one
    entry per dlt step (``extract``, ``normalize``, ``load``) with its timings,
    the exception that stopped it, and the exception chain beneath that. Reach
    for it once ``dlthub_list_pipeline_runs`` shows a failure, rather than
    inferring one from row counts.

    **Start with the default.** ``summary`` carries every step, its timings, its
    exception and the exception chain — the whole diagnosis — while dropping the
    one part that makes a trace enormous: each step's metrics and load packages,
    whose flattened schema update is a separate object for *every column of
    every table*. A wide schema turns that into thousands of entries, and none
    of them say why anything failed. Ask for ``full`` only when you actually
    need per-table load detail, and prefer narrowing ``step`` first.

    A cut trace keeps the diagnosis: the steps come first, each led by how it
    ended, so truncation spends what is left on config and metrics rather than
    on an exception. Narrowing ``step`` still beats raising ``max_chars`` when
    ``truncated`` is True — with several steps the last one can still be cut,
    and it is cheaper either way. ``omitted`` says what was left out and how to
    ask for it.

    Args:
        pipeline_run_id: The pipeline run's uuid, from
            ``dlthub_list_pipeline_runs``. A job run id will not resolve.
        detail: How much to return. ``summary`` is every step without its
            metrics and load packages. ``config`` adds the resolved config
            entries — their keys, sections and providers, never their values:
            dlt blanks the value of a secret-hinted field and this strips the
            rest, so a credential that reached the pipeline as a plain string
            does not leak either. ``full`` adds each step's metrics and load
            packages on top, and can be very large.
        step: Narrow to one dlt step. Reach for this when a listing already
            named the failing step — a ``load`` failure rarely needs the
            ``extract`` metrics beside it.
        max_chars: Ceiling on the text returned, at most 200000. A backstop,
            not a strategy: narrow ``detail`` or ``step`` instead.

    Returns:
        The requested slice as indented JSON, whether it was cut, how long the
        slice is in full, and what was omitted.

    Raises:
        Exception: A ``ToolError`` when no such pipeline run exists, or it has
            no stored trace — one the platform never linked to a job run has
            none.
    """
    held = workspace().telemetry.pipeline_runs.trace(id=pipeline_run_id)
    sliced, omitted = _slice(held.trace, detail, step)
    limit = max(1, min(max_chars, MAX_TRACE_CHARS))
    text = json.dumps(_ordered(sliced), indent=2, default=str)
    return PipelineRunTraceText(
        pipeline_run_id=pipeline_run_id,
        detail=detail,
        step=step,
        trace=text[:limit],
        truncated=len(text) > limit,
        total_chars=len(text),
        omitted=omitted,
    )


@tool
def dlthub_list_pipelines(
    pipeline_name: Optional[str] = None,
    status: Optional[Literal["succeeded", "failed"]] = None,
    destination: Optional[str] = None,
    days: int = WINDOW_DAYS,
    limit: int = ACTIVITY_PAGE_SIZE,
    offset: int = 0,
) -> Annotated[list[PipelineActivity], CONTEXT_READ]:
    """How each dlt pipeline has been doing — one row per pipeline, not per run.

    Reach for this for the shape of a workspace rather than the detail of one
    failure: which pipelines run here, how often, how much they move, and which
    are unreliable. ``failed`` and ``success_rate`` over a window are what turn
    "it failed once" into "it fails a third of the time", which
    ``dlthub_list_pipeline_runs`` cannot tell you without paging every run.

    Aggregated per pipeline, so it carries no pipeline run ids. Once a row looks
    wrong, ``dlthub_list_pipeline_runs(pipeline_name=...)`` is how you get to
    the individual runs and their ids.

    Check ``dlthub_telemetry_status`` before trusting a low count: a stale
    watermark looks exactly like a quiet week.

    Args:
        pipeline_name: Narrow to one pipeline.
        status: Narrow to pipelines whose most recent run ended this way.
        destination: Narrow to pipelines most recently writing here.
        days: How far back to aggregate, at most 365.
        limit: How many pipelines to return, at most 100.
        offset: How many to skip, for paging.

    Returns:
        One row per pipeline — run counts, failures, success rate, rows and
        bytes moved, average duration, and what its latest run did.

    Raises:
        Exception: A ``ToolError`` for a status the platform cannot filter on.
    """
    since, until = _window(days)
    return list(
        workspace().telemetry.pipelines(
            pipeline_name=pipeline_name,
            latest_status=_status(status),
            destination=destination,
            since=since,
            until=until,
            limit=page(limit),
            offset=skip(offset),
        )
    )


@tool
def dlthub_list_datasets(
    dataset_name: Optional[str] = None,
    status: Optional[Literal["succeeded", "failed"]] = None,
    destination: Optional[str] = None,
    days: int = ACTIVITY_DAYS,
    limit: int = ACTIVITY_PAGE_SIZE,
    offset: int = 0,
) -> Annotated[list[DatasetActivity], CONTEXT_READ]:
    """Where this workspace's data actually landed, one row per dataset.

    Reach for this to answer where data goes rather than what ran: which
    datasets exist, how much is in them, and how recently anything wrote.

    ``pipelines`` is the field worth reading twice — more than one means several
    pipelines share the dataset, so a table that looks wrong may have been
    written by a pipeline other than the one you are investigating. Chasing the
    wrong pipeline is the mistake this prevents.

    Aggregated per dataset, so it carries no pipeline run ids;
    ``dlthub_list_pipeline_runs(dataset=...)`` is the way down to the runs.
    Defaults to a longer window than the other listings, because a dataset that
    has not been written to in a fortnight is still a fact worth having.

    Args:
        dataset_name: Narrow to one dataset.
        status: Narrow to datasets whose most recent run ended this way.
        destination: Narrow to datasets most recently written here.
        days: How far back to aggregate, at most 365.
        limit: How many datasets to return, at most 100.
        offset: How many to skip, for paging.

    Returns:
        One row per dataset — how many pipelines write there, run counts,
        failures, rows and bytes landed, schema migrations, and what wrote last.

    Raises:
        Exception: A ``ToolError`` for a status the platform cannot filter on.
    """
    since, until = _window(days)
    return list(
        workspace().telemetry.datasets(
            dataset_name=dataset_name,
            latest_status=_status(status),
            destination=destination,
            since=since,
            until=until,
            limit=page(limit),
            offset=skip(offset),
        )
    )


__tools__ = (
    dlthub_telemetry_status,
    dlthub_list_pipeline_runs,
    dlthub_get_pipeline_run,
    dlthub_get_pipeline_run_trace,
    dlthub_list_pipelines,
    dlthub_list_datasets,
)
