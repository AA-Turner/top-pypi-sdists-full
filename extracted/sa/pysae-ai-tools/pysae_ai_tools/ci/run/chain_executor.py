"""CI job chain orchestration: play jobs, poll for completion, aggregate.

This is the impure half of the runner: it talks to GitLab (via
:mod:`.gitlab_api`), waits on job/pipeline state and logs progress. The clock
(``monotonic``/``sleep``) and the logger are injectable so the orchestration
can be driven in tests without real time passing or real output — the pure
graph/gate resolution lives in :mod:`.deps_resolver` and :mod:`.gating`.

Main entry points: :func:`run_job_chain` (one target and its chain),
:func:`run_jobs` (several concurrent chains), and their read-only twins
:func:`follow_job_chain` / :func:`follow_jobs`.
"""

import sys
import threading
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field

from .deps_resolver import _stage_order_from_jobs, resolve_deps_from_yaml, resolve_target_job
from .gating import add_manual_gates
from .gitlab_api import (
    Job,
    Pipeline,
    PipelineContext,
    create_pipeline,
    describe_context,
    find_pipeline,
    get_environment_url,
    get_job,
    get_pipeline,
    list_jobs,
    play_job,
    retry_job,
)

POLL_INTERVAL = 10  # seconds between status checks
PLAY_WAIT_INTERVAL = 5  # seconds between checks for created→manual transition
PLAY_WAIT_TIMEOUT = 120  # max seconds to wait for created→manual
DEFAULT_TIMEOUT = 1800  # 30 min max wait per job

Logger = Callable[[str], None]


@dataclass
class Clock:
    """Injectable time source so polling loops can be driven without real waits."""

    monotonic: Callable[[], float] = time.monotonic
    sleep: Callable[[float], None] = time.sleep


_DEFAULT_CLOCK = Clock()


def _stderr_logger(prefix: str = "") -> Logger:
    """Build a logger that writes ``prefix``-tagged lines to stderr."""

    def _log(msg: str) -> None:
        print(f"{prefix}{msg}", file=sys.stderr)

    return _log


@dataclass
class JobResult:
    """Result of running a single job."""

    job: Job
    action: str  # "played", "retried", "skipped", "waited", "failed"


@dataclass
class ChainResult:
    """Result of running a full dependency chain."""

    pipeline: Pipeline
    results: list[JobResult] = field(default_factory=list)
    target_job: Job | None = None
    environment_url: str = ""
    success: bool = False
    error: str = ""


@dataclass
class MultiChainResult:
    """Aggregated result of running several target chains concurrently."""

    pipeline: Pipeline
    targets: list[str] = field(default_factory=list)
    results: list[JobResult] = field(default_factory=list)
    target_jobs: list[Job] = field(default_factory=list)
    environment_urls: dict[str, str] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    success: bool = False
    error: str = ""


class _Coordinator:
    """Shared claim registry so concurrent chains never double-trigger a job.

    When several targets run in parallel, their dependency chains often
    overlap (e.g. both test jobs need ``build``). The first chain to reach a
    shared job claims it and triggers it; the others see the claim fail and
    simply wait for it to finish instead of issuing a second play/retry.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._claimed: set[int] = set()

    def claim(self, job_id: int) -> bool:
        """Return True if the caller may trigger this job, False if already owned."""
        with self._lock:
            if job_id in self._claimed:
                return False
            self._claimed.add(job_id)
            return True


def ensure_pipeline(ctx: PipelineContext, *, allow_create: bool) -> Pipeline | None:
    """Resolve the pipeline for ``ctx``, optionally creating one when none exists.

    ``allow_create`` distinguishes the two flavours that used to be copied
    across the runner: the run/trigger path creates a pipeline when the branch
    has none yet (``allow_create=True``), while the read-only follow path never
    creates anything (``allow_create=False``).
    """
    pipeline = find_pipeline(ctx)
    if pipeline is None and allow_create:
        pipeline = create_pipeline(ctx)
    return pipeline


def poll_until(
    fetch: Callable[[], Job | Pipeline | None],
    done: Callable[[Job | Pipeline], bool],
    *,
    timeout: int,
    interval: float,
    clock: Clock = _DEFAULT_CLOCK,
    retry_on_missing: bool = False,
    on_tick: Callable[[Job | Pipeline, float], None] | None = None,
) -> tuple[Job | Pipeline | None, bool]:
    """Poll ``fetch`` until ``done`` is satisfied or ``timeout`` elapses.

    Returns ``(value, timed_out)``. When ``fetch`` returns ``None``:
    ``retry_on_missing`` keeps polling (transient API hiccup), otherwise the
    call returns ``(None, False)`` immediately. ``on_tick`` is invoked with the
    current value and elapsed seconds before each sleep.
    """
    start = clock.monotonic()
    while True:
        current = fetch()
        if current is None:
            if not retry_on_missing:
                return None, False
            clock.sleep(interval)
            continue
        if done(current):
            return current, False
        elapsed = clock.monotonic() - start
        if elapsed > timeout:
            return current, True
        if on_tick is not None:
            on_tick(current, elapsed)
        clock.sleep(interval)


def _blocking_failed_job(jobs: list[Job], target: Job) -> Job | None:
    """Return an upstream failure that keeps ``target`` from ever starting.

    A target still waiting to start (created/pending/manual) is doomed once a
    job in an earlier stage has failed or been canceled without
    ``allow_failure``: GitLab won't schedule a later stage past a stage failure,
    yet it leaves the downstream job dangling in a non-terminal state rather
    than skipping it — so polling the target alone would block until the
    timeout. Same-stage siblings never gate ``target`` and are ignored.
    """
    if target.is_terminal or target.status == "running":
        return None
    stage_order = _stage_order_from_jobs(jobs)
    if target.stage not in stage_order:
        return None
    target_rank = stage_order.index(target.stage)
    for job in jobs:
        if job.id == target.id or job.allow_failure or job.stage not in stage_order:
            continue
        if job.status in ("failed", "canceled") and stage_order.index(job.stage) < target_rank:
            return job
    return None


def _wait_for_job(
    ctx: PipelineContext,
    job_id: int,
    timeout: int = DEFAULT_TIMEOUT,
    *,
    pipeline_id: int | None = None,
    clock: Clock = _DEFAULT_CLOCK,
) -> tuple[Job, str | None]:
    """Poll a job until it is terminal, blocked by an upstream failure, or times out.

    When ``pipeline_id`` is set, each poll also inspects the surrounding
    pipeline: if the target still hasn't started and a job in an earlier stage
    has failed for good, the target will never run, so we stop right away
    instead of waiting out ``timeout``. Returns ``(job, blocked_reason)`` —
    ``blocked_reason`` is a human-readable cause when we bailed on such a
    blocker, ``None`` otherwise (normal terminal state or timeout).
    """
    blocker: dict[str, str] = {}

    def _done(current: Job | Pipeline) -> bool:
        assert isinstance(current, Job)
        if current.is_terminal:
            return True
        if pipeline_id is not None and current.status in ("created", "pending", "manual"):
            failed = _blocking_failed_job(list_jobs(ctx, pipeline_id), current)
            if failed is not None:
                blocker["reason"] = (
                    f"« {failed.name} » a échoué en amont ({failed.failure_reason or failed.status}) — "
                    f"« {current.name} » ne démarrera jamais"
                )
                return True
        return False

    result, timed_out = poll_until(
        lambda: get_job(ctx, job_id),
        _done,
        timeout=timeout,
        interval=POLL_INTERVAL,
        clock=clock,
        retry_on_missing=True,
    )
    if timed_out:
        print(f"Timeout waiting for job {job_id} after {timeout}s", file=sys.stderr)
    assert isinstance(result, Job)  # retry_on_missing guarantees a non-None Job
    return result, blocker.get("reason")


def _wait_for_playable(ctx: PipelineContext, job_id: int, *, clock: Clock = _DEFAULT_CLOCK) -> Job | None:
    """Wait for a created job to become manual (playable)."""
    start = clock.monotonic()
    while True:
        current = get_job(ctx, job_id)
        if not current:
            return None

        if current.status == "manual":
            return current
        if current.status in ("running", "pending", "success"):
            return current
        if current.is_terminal:
            return current

        if clock.monotonic() - start > PLAY_WAIT_TIMEOUT:
            return current

        clock.sleep(PLAY_WAIT_INTERVAL)


def wait_for_pipeline(
    ctx: PipelineContext,
    pipeline_id: int,
    *,
    timeout: int,
    interval: float,
    wait_manual: bool,
    clock: Clock = _DEFAULT_CLOCK,
    on_tick: Callable[[Pipeline, float], None] | None = None,
) -> tuple[Pipeline | None, bool]:
    """Poll a pipeline until it reaches a terminal state or ``timeout`` elapses.

    Terminal states are success/failed/canceled/skipped, plus ``manual`` unless
    ``wait_manual`` is set (a manual pipeline means the automatic part is done
    and a human play is pending, so further waiting would block indefinitely).
    Returns ``(pipeline, timed_out)``; ``pipeline`` is ``None`` when the status
    could not be fetched.
    """
    terminal_statuses = {"success", "failed", "canceled", "skipped"}
    if not wait_manual:
        terminal_statuses.add("manual")

    result, timed_out = poll_until(
        lambda: get_pipeline(ctx, pipeline_id),
        lambda p: p.status in terminal_statuses,
        timeout=timeout,
        interval=interval,
        clock=clock,
        retry_on_missing=False,
        on_tick=on_tick,  # type: ignore[arg-type]
    )
    assert result is None or isinstance(result, Pipeline)
    return result, timed_out


def run_job_chain(
    ctx: PipelineContext,
    target_name: str,
    pipeline: Pipeline | None = None,
    log_prefix: str = "",
    coordinator: _Coordinator | None = None,
    *,
    clock: Clock = _DEFAULT_CLOCK,
    log: Logger | None = None,
) -> ChainResult:
    """Run a full dependency chain for a target job.

    1. Find/create pipeline (or reuse ``pipeline`` when provided)
    2. List jobs, find target
    3. Resolve dependency chain
    4. Play/retry deps in order, wait for each
    5. Play target, wait
    6. Report

    ``log_prefix`` is prepended to every progress line (used to tag output per
    target when several chains run concurrently). ``coordinator``, when set,
    guards play/retry of shared dependency jobs so parallel chains don't
    trigger the same job twice — see :class:`_Coordinator`. ``clock`` and
    ``log`` are injectable for tests.
    """
    _log = log if log is not None else _stderr_logger(log_prefix)

    # 1. Find pipeline (reuse a pre-resolved one when provided, e.g. multi-job runs)
    if pipeline is None:
        pipeline = ensure_pipeline(ctx, allow_create=True)
    if not pipeline:
        return ChainResult(
            pipeline=Pipeline(id=0, status="error"),
            error="Impossible de trouver ou créer une pipeline",
        )

    # 2. List jobs and find target
    jobs = list_jobs(ctx, pipeline.id)
    if not jobs:
        return ChainResult(pipeline=pipeline, error="Aucun job trouvé dans la pipeline")

    target_job, match_error = resolve_target_job(target_name, jobs)
    if target_job is None:
        return ChainResult(pipeline=pipeline, error=match_error)

    # 3. Resolve dependency chain
    chain_names, needs_map = resolve_deps_from_yaml(target_job.name, jobs)
    chain_names = add_manual_gates(target_job.name, chain_names, jobs, needs_map=needs_map or None)
    jobs_by_name = {j.name: j for j in jobs}

    # Filter chain to jobs that exist in pipeline
    chain = [jobs_by_name[name] for name in chain_names if name in jobs_by_name]
    if not chain:
        chain = [target_job]

    # Print chain
    chain_display = " → ".join(f"`{j.name}`" for j in chain)
    _log(f"Chaîne de dépendances : {chain_display}")

    # 4. Run chain
    result = ChainResult(pipeline=pipeline, target_job=target_job)

    for i, job in enumerate(chain):
        # Refresh job status
        fresh = get_job(ctx, job.id)
        if not fresh:
            result.error = f"Impossible de récupérer le statut de {job.name}"
            return result
        job = fresh

        is_target = job.name == target_job.name
        step = f"({i + 1}/{len(chain)})"

        if job.status == "success":
            _log(f"  {step} {job.name} : déjà terminé ✓")
            result.results.append(JobResult(job=job, action="skipped"))
            continue

        # A shared dependency already claimed by another concurrent chain: don't
        # trigger it a second time, just fall through and wait for it to finish.
        owned_by_other = (
            coordinator is not None and not is_target and not coordinator.claim(job.id)
            if (job.needs_play or job.status in ("failed", "skipped"))
            else False
        )

        # Trigger
        if owned_by_other:
            _log(f"  {step} {job.name} : géré par une autre cible, attente...")
            result.results.append(JobResult(job=job, action="waited"))
        elif job.needs_play:
            _log(f"  {step} {job.name} : démarrage...")
            played = play_job(ctx, job.id)
            if played:
                result.results.append(JobResult(job=played, action="played"))
            else:
                result.error = f"Impossible de démarrer {job.name}"
                return result
        elif job.status in ("failed", "skipped"):
            _log(f"  {step} {job.name} : relance...")
            retried = retry_job(ctx, job.id)
            if retried:
                result.results.append(JobResult(job=retried, action="retried"))
            else:
                result.error = f"Impossible de relancer {job.name}"
                return result
        elif job.status == "created":
            if is_target and job.when == "manual":
                # Wait for deps to complete, then transition to manual
                _log(f"  {step} {job.name} : en attente de la transition manual...")
                playable = _wait_for_playable(ctx, job.id, clock=clock)
                if playable and playable.status == "manual":
                    played = play_job(ctx, playable.id)
                    if played:
                        result.results.append(JobResult(job=played, action="played"))
                    else:
                        result.error = f"Impossible de démarrer {job.name}"
                        return result
                elif playable and playable.is_terminal:
                    result.results.append(JobResult(job=playable, action="waited"))
                    if playable.status != "success":
                        result.error = f"{job.name} a échoué ({playable.status})"
                        return result
                    continue
                else:
                    result.error = f"{job.name} n'est pas devenu manual après {PLAY_WAIT_TIMEOUT}s"
                    return result
            else:
                _log(f"  {step} {job.name} : en attente (démarrage automatique)...")
                result.results.append(JobResult(job=job, action="waited"))
        else:
            _log(f"  {step} {job.name} : {job.status}...")
            result.results.append(JobResult(job=job, action="waited"))

        # Wait for completion
        _log(f"  {step} {job.name} : en cours...")
        final, blocked = _wait_for_job(ctx, job.id, pipeline_id=pipeline.id, clock=clock)
        if blocked:
            _log(f"  {step} {job.name} : bloqué ✗ ({blocked})")
            result.error = blocked
            result.target_job = final
            return result
        if final.status == "success":
            _log(f"  {step} {job.name} : terminé ✓")
        elif final.status == "failed":
            _log(f"  {step} {job.name} : échoué ✗ ({final.failure_reason})")
            result.error = f"{job.name} a échoué"
            result.target_job = final
            return result
        else:
            _log(f"  {step} {job.name} : {final.status}")

    # 5. Get environment URL if applicable
    final_target = get_job(ctx, target_job.id)
    if final_target:
        result.target_job = final_target
        if final_target.environment:
            result.environment_url = get_environment_url(ctx, final_target.environment)

    result.success = final_target is not None and final_target.status == "success"
    return result


def aggregate_chain_results(
    pipeline: Pipeline,
    target_names: list[str],
    chain_results: dict[str, ChainResult],
) -> MultiChainResult:
    """Merge per-target ChainResults into a single MultiChainResult (pure).

    Jobs shared across chains are de-duplicated by id. Overall success requires
    every target to have succeeded.
    """
    multi = MultiChainResult(pipeline=pipeline, targets=list(target_names))
    seen_job_ids: set[int] = set()
    for name in target_names:
        cr = chain_results.get(name)
        if cr is None:
            multi.errors.append(f"{name}: aucun résultat")
            continue
        if cr.target_job is not None:
            multi.target_jobs.append(cr.target_job)
            if cr.environment_url:
                multi.environment_urls[cr.target_job.name] = cr.environment_url
        for jr in cr.results:
            if jr.job.id not in seen_job_ids:
                seen_job_ids.add(jr.job.id)
                multi.results.append(jr)
        if cr.error:
            multi.errors.append(f"{name}: {cr.error}")
    multi.success = bool(target_names) and all(
        (chain_results.get(name) is not None and chain_results[name].success) for name in target_names
    )
    multi.error = "; ".join(multi.errors)
    return multi


def run_jobs(ctx: PipelineContext, target_names: list[str], *, clock: Clock = _DEFAULT_CLOCK) -> MultiChainResult:
    """Run several target chains concurrently and return when all are terminal.

    The pipeline is resolved once and shared, a single coordinator prevents
    double-triggering jobs common to several chains, and each chain logs under
    its own ``[target]`` prefix. Use this for "run the unit tests AND the
    integration tests, release when both are done".
    """
    # De-duplicate while preserving order.
    targets: list[str] = []
    for name in target_names:
        if name not in targets:
            targets.append(name)

    pipeline = ensure_pipeline(ctx, allow_create=True)
    if not pipeline:
        return MultiChainResult(
            pipeline=Pipeline(id=0, status="error"),
            targets=targets,
            error="Impossible de trouver ou créer une pipeline",
        )

    coordinator = _Coordinator()
    chain_results: dict[str, ChainResult] = {}
    with ThreadPoolExecutor(max_workers=len(targets)) as executor:
        futures = {
            executor.submit(
                run_job_chain,
                ctx,
                name,
                pipeline=pipeline,
                log_prefix=f"[{name}] ",
                coordinator=coordinator,
                clock=clock,
            ): name
            for name in targets
        }
        for future in as_completed(futures):
            name = futures[future]
            chain_results[name] = future.result()

    return aggregate_chain_results(pipeline, targets, chain_results)


def follow_job_chain(
    ctx: PipelineContext,
    target_name: str,
    pipeline: Pipeline | None = None,
    log_prefix: str = "",
    *,
    clock: Clock = _DEFAULT_CLOCK,
    log: Logger | None = None,
) -> ChainResult:
    """Follow an already-triggered job until it reaches a terminal state.

    Unlike :func:`run_job_chain`, this never plays, retries or creates
    anything, and never resolves the dependency chain: it locates the
    existing pipeline, matches the target job and waits for it to finish.
    Use it to track a job that was started elsewhere — auto-triggered,
    played by a teammate, or launched by another process.

    A target still awaiting a manual play (``needs_play``) is reported as an
    error rather than followed: it hasn't started, so there is nothing to
    follow — the caller should re-run without follow mode to trigger it.
    """
    _log = log if log is not None else _stderr_logger(log_prefix)

    if pipeline is None:
        pipeline = ensure_pipeline(ctx, allow_create=False)
    if not pipeline:
        return ChainResult(
            pipeline=Pipeline(id=0, status="error"),
            error=f"Aucune pipeline à suivre ({describe_context(ctx)})",
        )

    jobs = list_jobs(ctx, pipeline.id)
    if not jobs:
        return ChainResult(pipeline=pipeline, error="Aucun job trouvé dans la pipeline")

    target_job, match_error = resolve_target_job(target_name, jobs)
    if target_job is None:
        return ChainResult(pipeline=pipeline, error=match_error)

    result = ChainResult(pipeline=pipeline, target_job=target_job)

    fresh = get_job(ctx, target_job.id) or target_job
    result.target_job = fresh
    if fresh.needs_play:
        result.error = (
            f"{fresh.name} n'a pas encore démarré (status: {fresh.status}) — il attend une action manuelle. "
            "Relance sans --follow pour le déclencher."
        )
        return result

    if fresh.is_terminal:
        _log(f"{fresh.name} : déjà terminé ({fresh.status})")
        final = fresh
    else:
        _log(f"{fresh.name} : suivi en cours ({fresh.status})...")
        final, blocked = _wait_for_job(ctx, fresh.id, pipeline_id=pipeline.id, clock=clock)
        if blocked:
            _log(f"{fresh.name} : bloqué ✗ ({blocked})")
            result.results.append(JobResult(job=final, action="followed"))
            result.target_job = final
            result.error = blocked
            result.success = False
            return result

    result.results.append(JobResult(job=final, action="followed"))
    result.target_job = final
    if final.status == "success":
        _log(f"{final.name} : terminé ✓")
        if final.environment:
            result.environment_url = get_environment_url(ctx, final.environment)
    elif final.status == "failed":
        _log(f"{final.name} : échoué ✗ ({final.failure_reason})")
        result.error = f"{final.name} a échoué"
    else:
        _log(f"{final.name} : {final.status}")

    result.success = final.status == "success"
    return result


def follow_jobs(ctx: PipelineContext, target_names: list[str], *, clock: Clock = _DEFAULT_CLOCK) -> MultiChainResult:
    """Follow several already-started target jobs concurrently until all terminal.

    The existing pipeline is resolved once and shared; each target is polled
    on its own thread. Nothing is triggered — this is the read-only twin of
    :func:`run_jobs`.
    """
    targets: list[str] = []
    for name in target_names:
        if name not in targets:
            targets.append(name)

    pipeline = ensure_pipeline(ctx, allow_create=False)
    if not pipeline:
        return MultiChainResult(
            pipeline=Pipeline(id=0, status="error"),
            targets=targets,
            error=f"Aucune pipeline à suivre ({describe_context(ctx)})",
        )

    chain_results: dict[str, ChainResult] = {}
    with ThreadPoolExecutor(max_workers=len(targets)) as executor:
        futures = {
            executor.submit(follow_job_chain, ctx, name, pipeline=pipeline, log_prefix=f"[{name}] ", clock=clock): name
            for name in targets
        }
        for future in as_completed(futures):
            name = futures[future]
            chain_results[name] = future.result()

    return aggregate_chain_results(pipeline, targets, chain_results)


def get_pipeline_status(ctx: PipelineContext, pipeline_id: int) -> str:
    """Get a formatted status overview of all jobs in a pipeline."""
    jobs = list_jobs(ctx, pipeline_id)
    if not jobs:
        return "Aucun job trouvé"

    # Group by stage, maintaining stage order from job IDs
    stage_order: list[str] = []
    stages: dict[str, list[Job]] = {}
    for job in sorted(jobs, key=lambda j: j.id):
        if job.stage not in stage_order:
            stage_order.append(job.stage)
        stages.setdefault(job.stage, []).append(job)

    status_icons = {
        "success": "passed",
        "failed": "failed",
        "running": "in progress",
        "pending": "queued",
        "manual": "manual",
        "created": "not started",
        "skipped": "skipped",
        "canceled": "canceled",
    }

    lines: list[str] = []
    for stage in stage_order:
        lines.append(f"## {stage}")
        for job in stages[stage]:
            icon = status_icons.get(job.status, job.status)
            lines.append(f"  {icon} | {job.name}")
    return "\n".join(lines)
