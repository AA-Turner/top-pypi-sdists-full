"""Session bootstrap and agent-turn metrics, Registry skill metrics, completion band resolution metrics and
sandbox metrics, for the Agents SDK worker."""

import functools
import os
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Literal

import structlog
from opentelemetry.metrics import Counter, Histogram, get_meter

from mistralai.vibe.harness.runtime.hosts.workflows import workflow_is_replaying
from mistralai.vibe.harness.runtime.session.turns import (
    TurnCompleted,
    TurnContinuationRequested,
    TurnFailed,
    TurnInterrupted,
    TurnRunResult,
)
from mistralai.vibe_agents import __version__
from mistralai.vibe_agents.sdk.app import config
from mistralai.vibe_agents.sdk.assembly.skill_metrics import (
    SkillCatalogOutcome,
    SkillCatalogReason,
    SkillLoadSource,
    SkillMaterializationOutcome,
    SkillMaterializationReason,
)
from mistralai.vibe_agents.sdk.sandbox.metrics import (
    SandboxCreateOutcome,
    SandboxCreateReason,
    SandboxCreateSource,
    SandboxExecOutcome,
    SandboxKind,
)

logger = structlog.get_logger(__name__)

CompletionOrgTierOutcome = Literal["resolved", "missing", "unknown", "error"]
"""``resolved``: a known band reached the gateway. ``missing``: Albe has no row or no tier. ``unknown``: a band
``OrgTier`` does not list. ``error``: Albe could not be read. ``missing`` and ``unknown`` schedule the completion as
free; ``error`` fails it."""

# Names, units, buckets and labels mirror Nuage's AgentRuntimeMetrics so dashboards read both engines alike.
_METER_NAME = "agent_runtime"
_SERVICE_NAME = "agent_runtime"
_NAMESPACE = "agents_platform.agent_runtime"
AGENT_ENGINE = "agents_sdk"

_MINUTE = 60.0
_HOUR = 60 * _MINUTE
_COMPLETION_LATENCY_SECONDS_BUCKETS = [0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 120.0, 180.0, 300.0, 600.0]
_AGENT_TURN_DURATION_SECONDS_BUCKETS = [
    *_COMPLETION_LATENCY_SECONDS_BUCKETS,
    15 * _MINUTE,
    20 * _MINUTE,
    30 * _MINUTE,
    45 * _MINUTE,
    _HOUR,
    90 * _MINUTE,
    2 * _HOUR,
    3 * _HOUR,
    4 * _HOUR,
]
_SESSION_BOOTSTRAP_DURATION_SECONDS_BUCKETS = [
    0.1,
    0.25,
    0.5,
    1.0,
    2.5,
    5.0,
    10.0,
    30.0,
    60.0,
    120.0,
    300.0,
    600.0,
    900.0,
    1800.0,
    3600.0,
]

_SANDBOX_DURATION_SECONDS_BUCKETS = [0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0, 600.0, 1800.0]


@dataclass(frozen=True, slots=True)
class _Instruments:
    agent_loop_started: Counter
    continue_as_new_requested: Counter
    agent_turn_duration_seconds: Histogram
    session_bootstrap_duration_seconds: Histogram
    skill_loads: Counter
    skill_registry_catalog_results: Counter
    skill_materialization_results: Counter
    completion_org_tier_resolved: Counter
    sandbox_create_duration_seconds: Histogram
    sandbox_exec_duration_seconds: Histogram


@functools.cache
def _instruments() -> _Instruments:
    meter = get_meter(_METER_NAME)
    return _Instruments(
        agent_loop_started=meter.create_counter(f"{_NAMESPACE}.agent_loop.started", description="Agent loop started."),
        continue_as_new_requested=meter.create_counter(
            f"{_NAMESPACE}.continue_as_new.requested",
            description="Continue-as-new requested at the end of an agent turn.",
        ),
        agent_turn_duration_seconds=meter.create_histogram(
            f"{_NAMESPACE}.agent_turn.duration_seconds",
            unit="s",
            description="Agent turn duration in seconds.",
            explicit_bucket_boundaries_advisory=_AGENT_TURN_DURATION_SECONDS_BUCKETS,
        ),
        session_bootstrap_duration_seconds=meter.create_histogram(
            f"{_NAMESPACE}.session.bootstrap.duration_seconds",
            unit="s",
            description="Time from persisted session creation until the first LLM completion request starts.",
            explicit_bucket_boundaries_advisory=_SESSION_BOOTSTRAP_DURATION_SECONDS_BUCKETS,
        ),
        skill_loads=meter.create_counter(
            f"{_NAMESPACE}.skill.loads",
            unit="{load}",
            description="Skills the skill tool loaded, by where their files came from.",
        ),
        skill_registry_catalog_results=meter.create_counter(
            f"{_NAMESPACE}.skill.registry_catalog.results",
            unit="{listing}",
            description="Registry skill catalogue listings at Session start, by outcome and bounded reason.",
        ),
        skill_materialization_results=meter.create_counter(
            f"{_NAMESPACE}.skill.materialization.results",
            unit="{materialization}",
            description="Discovered Registry skill installs on first use, by outcome and bounded reason.",
        ),
        completion_org_tier_resolved=meter.create_counter(
            f"{_NAMESPACE}.completion_org_tier.resolved",
            unit="{resolution}",
            description="Completion band reads from Albe customer metadata, by outcome and forwarded band.",
        ),
        sandbox_create_duration_seconds=meter.create_histogram(
            f"{_NAMESPACE}.sandbox.create.duration_seconds",
            unit="s",
            description="Sandbox creates for a Session, by sandbox, source, outcome and bounded reason.",
            explicit_bucket_boundaries_advisory=_SANDBOX_DURATION_SECONDS_BUCKETS,
        ),
        sandbox_exec_duration_seconds=meter.create_histogram(
            f"{_NAMESPACE}.sandbox.exec.duration_seconds",
            unit="s",
            description="Sandbox command executions, by sandbox and outcome.",
            explicit_bucket_boundaries_advisory=_SANDBOX_DURATION_SECONDS_BUCKETS,
        ),
    )


def _attributes(**extra: str) -> dict[str, str | int]:
    return {
        "service": _SERVICE_NAME,
        "version": __version__,
        "worker_id": os.getpid(),
        "agent_engine": AGENT_ENGINE,
        **extra,
    }


def _record(metric: str, record: Callable[[_Instruments], None]) -> None:
    if workflow_is_replaying():
        return
    try:
        record(_instruments())
    except Exception as error:
        logger.warning("Failed to record agent runtime metric", metric=metric, error_type=type(error).__name__)


def _record_if_enabled(metric: str, record: Callable[[_Instruments], None]) -> None:
    # The worker builds its skill observer at import, before it reads settings, so each sample reads the switch.
    def record_enabled(instruments: _Instruments) -> None:
        if config.get_app_settings().runtime_metrics_enabled:
            record(instruments)

    _record(metric, record_enabled)


class WorkerSkillMetrics:
    """Record Registry skill metrics on a worker that enables runtime metrics."""

    def record_skill_load(self, source: SkillLoadSource) -> None:
        _record_if_enabled(
            "skill.loads", lambda instruments: instruments.skill_loads.add(1, _attributes(source=source))
        )

    def record_skill_registry_catalog(self, outcome: SkillCatalogOutcome, reason: SkillCatalogReason) -> None:
        _record_if_enabled(
            "skill.registry_catalog.results",
            lambda instruments: instruments.skill_registry_catalog_results.add(
                1, _attributes(outcome=outcome, reason=reason)
            ),
        )

    def record_skill_materialization(
        self, outcome: SkillMaterializationOutcome, reason: SkillMaterializationReason
    ) -> None:
        _record_if_enabled(
            "skill.materialization.results",
            lambda instruments: instruments.skill_materialization_results.add(
                1, _attributes(outcome=outcome, reason=reason)
            ),
        )


class WorkerSandboxMetrics:
    """Record sandbox metrics on a worker that enables runtime metrics."""

    def record_sandbox_create(
        self,
        *,
        sandbox: SandboxKind,
        source: SandboxCreateSource,
        outcome: SandboxCreateOutcome,
        reason: SandboxCreateReason,
        duration_seconds: float,
    ) -> None:
        _record_if_enabled(
            "sandbox.create.duration_seconds",
            lambda instruments: instruments.sandbox_create_duration_seconds.record(
                duration_seconds, _attributes(sandbox=sandbox, source=source, outcome=outcome, reason=reason)
            ),
        )

    def record_sandbox_exec(
        self, *, sandbox: SandboxKind, outcome: SandboxExecOutcome, duration_seconds: float
    ) -> None:
        _record_if_enabled(
            "sandbox.exec.duration_seconds",
            lambda instruments: instruments.sandbox_exec_duration_seconds.record(
                duration_seconds, _attributes(sandbox=sandbox, outcome=outcome)
            ),
        )


def record_agent_loop_started() -> None:
    _record("agent_loop.started", lambda instruments: instruments.agent_loop_started.add(1, _attributes()))


def record_continue_as_new_requested() -> None:
    _record(
        "continue_as_new.requested",
        lambda instruments: instruments.continue_as_new_requested.add(1, _attributes()),
    )


def record_session_bootstrap(duration_seconds: float) -> None:
    _record(
        "session.bootstrap.duration_seconds",
        lambda instruments: instruments.session_bootstrap_duration_seconds.record(duration_seconds, _attributes()),
    )


def record_completion_org_tier(outcome: CompletionOrgTierOutcome, band: str = "") -> None:
    _record_if_enabled(
        "completion_org_tier.resolved",
        lambda instruments: instruments.completion_org_tier_resolved.add(1, _attributes(outcome=outcome, band=band)),
    )


def turn_outcome(result: TurnRunResult) -> str:
    match result:
        case TurnCompleted():
            return "completed"
        case TurnFailed():
            return "errored"
        case TurnInterrupted():
            return "cancelled"
        case TurnContinuationRequested():
            return "continued_as_new"


def record_agent_turn(outcome: str, duration_seconds: float) -> None:
    _record(
        "agent_turn.duration_seconds",
        lambda instruments: instruments.agent_turn_duration_seconds.record(
            duration_seconds, _attributes(outcome=outcome)
        ),
    )


def _never_raises[**P, R](default: R) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorate(method: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(method)
        def guarded(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return method(*args, **kwargs)
            except Exception as error:
                logger.warning(
                    "Failed to track agent runtime metrics", step=method.__name__, error_type=type(error).__name__
                )
                return default

        return guarded

    return decorate


class WorkflowRuntimeMetrics:
    """Own one Workflow run's agent-runtime metrics; the Session driver only forwards lifecycle events."""

    def __init__(
        self,
        *,
        now_unix_ms: Callable[[], int],
        session_created_at_unix_ms: Callable[[], int],
        turns_to_drive: Callable[[], Sequence[str]],
        active_turn_id: Callable[[], str | None],
    ) -> None:
        self._now_unix_ms = now_unix_ms
        self._session_created_at_unix_ms = session_created_at_unix_ms
        self._turns_to_drive = turns_to_drive
        self._active_turn_id = active_turn_id
        self._enabled = False
        self._bootstrap_pending = False
        self._run_started_unix_ms = now_unix_ms()
        self._drive_started_unix_ms: dict[str, int] = {}

    @_never_raises(None)
    def run_started(self, *, enabled: bool, bootstrap_pending: bool) -> None:
        self._enabled = enabled
        self._bootstrap_pending = enabled and bootstrap_pending
        if enabled:
            record_agent_loop_started()

    @_never_raises(None)
    def turn_seen(self, turn_id: str) -> None:
        # Command admission enters the same scope; serve() drives only the head of turns_to_drive.
        if not self._enabled:
            return
        turns_to_drive = self._turns_to_drive()
        if turn_id in self._drive_started_unix_ms or not turns_to_drive or turns_to_drive[0] != turn_id:
            return
        now = self._now_unix_ms()
        self._drive_started_unix_ms = {
            tracked: started for tracked, started in self._drive_started_unix_ms.items() if tracked in turns_to_drive
        }
        self._drive_started_unix_ms[turn_id] = now
        if self._bootstrap_pending:
            created_at = self._session_created_at_unix_ms()
            self._bootstrap_pending = False
            record_session_bootstrap(max(now - created_at, 0) / 1000)

    @_never_raises(None)
    def turn_finished(self, turn_id: str, result: TurnRunResult) -> None:
        if not self._enabled:
            return
        record_agent_turn(turn_outcome(result), self._segment_seconds(turn_id))

    @_never_raises(None)
    def run_ended(self, *, failed: bool) -> None:
        """Record any Turn still driving when the run ends without finishing it."""
        for turn_id in list(self._drive_started_unix_ms):
            record_agent_turn("errored" if failed else "cancelled", self._segment_seconds(turn_id))

    def continuation_requested(self) -> bool:
        """Record the run's end by Continue-As-New; return whether bootstrap is still owed to the next run."""
        if not self._enabled:
            return False
        self._record_continuation()
        self._enabled = False
        self._drive_started_unix_ms.clear()
        return self._bootstrap_pending

    @_never_raises(None)
    def _record_continuation(self) -> None:
        record_continue_as_new_requested()
        active_turn_id = self._active_turn_id()
        if active_turn_id is not None:
            record_agent_turn("continued_as_new", self._segment_seconds(active_turn_id))

    def _segment_seconds(self, turn_id: str) -> float:
        started = self._drive_started_unix_ms.pop(turn_id, self._run_started_unix_ms)
        return max(self._now_unix_ms() - started, 0) / 1000


__all__ = ["AGENT_ENGINE", "WorkerSandboxMetrics", "WorkerSkillMetrics", "WorkflowRuntimeMetrics", "turn_outcome"]
