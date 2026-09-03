"""Due-probe evaluator for waking up cooldown probes."""

from __future__ import annotations

import logging
import os
from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime, timedelta

from agentic_devtools.cli.ci.github_provider import _gh_api
from agentic_devtools.cli.ci.reconciliation import config
from agentic_devtools.cli.ci.reconciliation.metrics import MetricEventType, create_metric_event
from agentic_devtools.cli.ci.reconciliation.models import CooldownProbe, CooldownState, ProbeStatus, QueueState
from agentic_devtools.cli.ci.reconciliation.probes import CooldownProbeAdapter
from agentic_devtools.cli.ci.reconciliation.queue_store import ConcurrentModificationError, QueueStore
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError, calculate_rate_limit_delay

logger = logging.getLogger(__name__)

AvailabilityResult = bool | tuple[bool, datetime | None]
AvailabilityChecker = Callable[[CooldownProbe], AvailabilityResult]


class DueProbeEvaluator:
    """Evaluates and executes due cooldown probes."""

    def __init__(
        self,
        store: QueueStore,
        adapter: CooldownProbeAdapter,
        availability_checker: AvailabilityChecker | None = None,
    ) -> None:
        self._store = store
        self._adapter = adapter
        self._availability_checker = availability_checker

    def evaluate_due_probes(
        self,
        repo: str,
        now: datetime | None = None,
    ) -> list[CooldownProbe]:
        """Execute probes that are currently due and return their saved outcomes."""
        current = _resolve_now(now)
        state = self._store.load()
        if state.repo != repo:
            logger.warning("Loaded queue state for %s while evaluating %s", state.repo, repo)
            return []
        executed: list[CooldownProbe] = []
        for probe in [candidate for candidate in state.probes if self._adapter.is_due(candidate, current)]:
            try:
                executed.append(self.claim_and_execute_probe(repo, probe, current))
            except ConcurrentModificationError:
                logger.info("Skipping concurrently modified due probe %s", probe.probe_id)
        return executed

    def claim_and_execute_probe(self, repo: str, probe: CooldownProbe, now: datetime) -> CooldownProbe:
        """Persist an in-progress claim, execute the probe, and save the final outcome once."""
        current = _resolve_now(now)
        state = self._store.load()
        if state.repo != repo:
            raise ConcurrentModificationError(f"Loaded queue state for {state.repo!r} while evaluating {repo!r}")
        stored_probe = _find_probe(state, probe.probe_id)
        if stored_probe.status == ProbeStatus.IN_PROGRESS:
            claim_expired = stored_probe.claim_expires_at is None or stored_probe.claim_expires_at <= current
            if not claim_expired:
                raise ConcurrentModificationError(
                    f"Probe {probe.probe_id!r} has an unexpired active claim until {stored_probe.claim_expires_at}"
                )
            stored_probe = replace(stored_probe, status=ProbeStatus.PENDING, claim_expires_at=None)
            state = self._store.save(
                replace(state, probes=_replace_probe(state.probes, stored_probe.probe_id, stored_probe)),
                expected_revision=state.revision,
            )
        if not self._adapter.is_due(stored_probe, current):
            raise ConcurrentModificationError(f"Probe {probe.probe_id!r} is no longer due")
        claimed_probe = replace(
            stored_probe,
            status=ProbeStatus.IN_PROGRESS,
            claim_expires_at=current + timedelta(minutes=5),
        )
        claimed_state = replace(state, probes=_replace_probe(state.probes, stored_probe.probe_id, claimed_probe))
        claimed_state = self._store.save(claimed_state, expected_revision=state.revision)

        availability_result: AvailabilityResult = True
        if self._availability_checker is not None:
            try:
                availability_result = self._availability_checker(stored_probe)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Probe availability check failed for %s: %s", stored_probe.probe_id, exc)
                availability_result = False

        cooldown_state = _cooldown_state_from_probe(stored_probe)
        renewed_resume_at: datetime | None = None
        if isinstance(availability_result, tuple):
            available, renewed_resume_at = availability_result
        else:
            available = availability_result
        try:
            _cooldown_state, executed_probe = self._adapter.execute_probe(
                cooldown_state,
                claimed_probe,
                available,
                renewed_resume_at=renewed_resume_at,
                now=current,
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Probe execution failed for %s: %s", stored_probe.probe_id, exc)
            detail = str(exc).strip().replace("\n", " ")
            reason = f"probe_execution_failed:{type(exc).__name__}"
            if detail:
                reason = f"{reason}:{detail[:120]}"
            _failed_state, executed_probe = CooldownProbeAdapter().execute_probe(
                cooldown_state,
                claimed_probe,
                False,
                renewed_resume_at=None,
                now=current,
            )
            executed_probe = replace(executed_probe, alert_reason=reason)
        executed_probe = replace(executed_probe, claim_expires_at=None)
        final_state = replace(
            claimed_state,
            probes=_replace_probe(claimed_state.probes, stored_probe.probe_id, executed_probe),
            metric_events=[
                *claimed_state.metric_events,
                create_metric_event(
                    MetricEventType.PROBE,
                    repo,
                    {"probe_id": executed_probe.probe_id, "status": executed_probe.status},
                ),
            ][-500:],
        )
        self._store.save(final_state, expected_revision=claimed_state.revision)
        return executed_probe


def run_due_probe_wakeup(
    repo: str,
    store: QueueStore | None = None,
    cooldown_state: CooldownState | None = None,
) -> int:
    """Execute due probes and return the number saved."""
    if not config.ENABLE_DUE_PROBE_WAKEUP:
        logger.info("Due-probe wake-up disabled for %s", repo)
        return 0
    if store is None:
        store = QueueStore(repo=repo)
    adapter = CooldownProbeAdapter()
    if cooldown_state is not None:
        state = store.load()
        if not any(probe.cooldown_generation_id == cooldown_state.cooldown_generation_id for probe in state.probes):
            initial_probe = CooldownProbe(
                probe_id=adapter.generate_probe_id(),
                provider_identity=cooldown_state.provider_identity,
                credential_identity=cooldown_state.credential_identity,
                cooldown_generation_id=cooldown_state.cooldown_generation_id,
                status=ProbeStatus.PENDING,
                scheduled_at=cooldown_state.resume_at,
                resume_at=cooldown_state.resume_at,
            )
            store.save(replace(state, probes=[*state.probes, initial_probe]), expected_revision=state.revision)
    evaluator = DueProbeEvaluator(store=store, adapter=adapter, availability_checker=_build_availability_checker(repo))
    probes = evaluator.evaluate_due_probes(repo=repo, now=datetime.now(UTC))
    return len(probes)


def _resolve_now(now: datetime | None) -> datetime:
    current = now or datetime.now(UTC)
    if current.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    return current


def _find_probe(state: QueueState, probe_id: str) -> CooldownProbe:
    for probe in state.probes:
        if probe.probe_id == probe_id:
            return probe
    raise ConcurrentModificationError(f"Probe {probe_id!r} was not found in persisted queue state")


def _replace_probe(
    probes: list[CooldownProbe],
    original_probe_id: str,
    updated_probe: CooldownProbe,
) -> list[CooldownProbe]:
    return [updated_probe if probe.probe_id == original_probe_id else probe for probe in probes]


def _cooldown_state_from_probe(probe: CooldownProbe) -> CooldownState:
    resume_at = probe.resume_at or probe.scheduled_at
    return CooldownState(
        provider_identity=probe.provider_identity,
        credential_identity=probe.credential_identity,
        cooldown_generation_id=probe.cooldown_generation_id,
        resume_at=resume_at,
        probe_status=probe.status,
        retry_count=probe.retry_count,
        next_probe_at=probe.next_probe_at,
        reason=probe.alert_reason,
        max_retries=config.MAX_RETRY_ATTEMPTS,
    )


def _build_availability_checker(repo: str) -> AvailabilityChecker:
    """Return a per-run availability checker backed by live provider queries.

    The checker instance is created once per ``run_due_probe_wakeup`` invocation.
    It caches only a confirmed-available result for that invocation, while
    failures remain uncached so later probes can retry after transient outages.
    """
    confirmed_available_identities: set[tuple[str, str]] = set()

    def _checker(probe: CooldownProbe) -> AvailabilityResult:
        provider_identity = probe.provider_identity.strip().lower()
        credential_identity = probe.credential_identity.strip()
        identity_key = (provider_identity, credential_identity)
        if identity_key in confirmed_available_identities:
            return True
        if provider_identity not in {"gh", "github", "github_actions"}:
            logger.warning("Unsupported probe provider identity %r for %s", probe.provider_identity, repo)
            return False
        token = _resolve_probe_token(credential_identity)
        if not token:
            logger.warning(
                "Probe credential identity %r is not available in environment for %s",
                credential_identity,
                repo,
            )
            return False
        try:
            _gh_api(f"/repos/{repo}/pulls?state=open&per_page=1", token=token)
        except RetryableError as exc:
            if not exc.is_rate_limit:
                logger.warning("Provider availability check failed for %s: %s", repo, exc)
                return False
            logger.warning("Provider availability check failed for %s: %s", repo, exc)
            delay = calculate_rate_limit_delay(
                retry_after_seconds=exc.retry_after,
                reset_timestamp=exc.reset_timestamp,
            )
            return False, datetime.fromtimestamp(delay.resume_at, UTC)
        except ProviderRateLimitError as exc:
            logger.warning("Provider availability check failed for %s: %s", repo, exc)
            delay = calculate_rate_limit_delay(
                retry_after_seconds=exc.retry_after_seconds,
                reset_timestamp=exc.reset_timestamp,
            )
            return False, datetime.fromtimestamp(delay.resume_at, UTC)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Provider availability check failed for %s: %s", repo, exc)
            return False
        confirmed_available_identities.add(identity_key)
        return True

    return _checker


def _resolve_probe_token(credential_identity: str) -> str:
    """Return the token value for a probe's logical identity.

    ``AI_PR_LOOP_CREDENTIAL_IDENTITY`` can represent a logical identity while
    workflows inject the actual credential only as ``GH_TOKEN``.
    """
    token = os.environ.get(credential_identity, "").strip()
    if token:
        return token
    configured_identity = os.environ.get("AI_PR_LOOP_CREDENTIAL_IDENTITY", "").strip()
    if configured_identity and configured_identity == credential_identity:
        return os.environ.get("GH_TOKEN", "").strip()
    return ""
