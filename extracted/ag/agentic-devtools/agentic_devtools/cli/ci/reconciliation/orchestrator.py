"""Fail-closed orchestration for the AI PR loop reliability slice."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

from agentic_devtools.cli.ci.reconciliation.context_mapper import coalesce_event_contexts
from agentic_devtools.cli.ci.reconciliation.loop_control import AdmissionBlockedError, LoopController
from agentic_devtools.cli.ci.reconciliation.models import EligibilityDecision, Evidence, QueueState, RunEventContext
from agentic_devtools.cli.ci.reconciliation.queue_store import QueueStore
from agentic_devtools.cli.ci.reconciliation.status_reporter import StatusProvider, sync_status_comment
from agentic_devtools.cli.ci.reconciliation.wp3 import (
    DescriptionProvider,
    DispositionEvidence,
    EffectProvider,
    IssueEffectCoordinator,
    evaluate_disposition,
    update_description_guarded,
)


class PipelineProvider(Protocol):
    """Remote operations required after durable transitions."""

    def dispatch(self, pr_number: int) -> None: ...  # pragma: no cover

    def approval_observation(self, pr_number: int) -> Evidence: ...  # pragma: no cover

    def merge_observation(self, pr_number: int) -> Evidence: ...  # pragma: no cover


@dataclass(frozen=True)
class ReliabilitySliceEvent:
    """Immutable, authoritative input for one integrated wakeup."""

    context: RunEventContext
    observation: Evidence
    history: Evidence | None = None
    problem_hash: str | None = None
    finding_evidence: tuple[Evidence, ...] = ()
    dispositions: tuple[DispositionEvidence, ...] = ()
    description_edit: str = ""
    description_hash: str = ""
    thread_effects: tuple[dict[str, str], ...] = ()
    request_id: str | None = None
    obligation_id: str | None = None
    batch_id: str | None = None


@dataclass(frozen=True)
class ReliabilitySliceResult:
    """Durable outcome and gate decisions for one wakeup."""

    status: str
    state: QueueState
    phases: tuple[str, ...] = ()
    approval: EligibilityDecision | None = None
    merge: EligibilityDecision | None = None
    status_comment_id: int | None = None
    reason: str = ""


Transition = Callable[[QueueState], QueueState]


class IntegratedLoopOrchestrator:
    """Coordinate offline lifecycle transitions and provider projections.

    Every state mutation crosses ``QueueStore.transact``. Provider calls occur
    only after the corresponding transition is durable, and all kill switches
    are checked before either a mutation or a remote call.
    """

    def __init__(
        self,
        controller: LoopController,
        store: QueueStore,
        provider: PipelineProvider,
        *,
        global_hold: Callable[[], bool] = lambda: False,
        capacity_available: Callable[[QueueState, int], bool] = lambda state, pr: True,
    ) -> None:
        if not isinstance(controller, LoopController):
            raise ValueError("controller is required")
        if not isinstance(store, QueueStore):
            raise ValueError("queue store is required")
        if not callable(getattr(provider, "dispatch", None)):
            raise ValueError("provider dispatch capability is required")
        if not callable(global_hold) or not callable(capacity_available):
            raise ValueError("kill-switch callbacks must be callable")
        self._controller = controller
        self._store = store
        self._provider = provider
        self._global_hold = global_hold
        self._capacity_available = capacity_available

    def run(  # pragma: no cover - exercised by workflow integration tests
        self,
        event: ReliabilitySliceEvent,
        *,
        status_provider: StatusProvider | None = None,
        description_provider: DescriptionProvider | None = None,
        effect_provider: EffectProvider | None = None,
    ) -> ReliabilitySliceResult:
        """Replay one event idempotently, stopping closed on every unsafe gate."""
        if event.context.target_type != "pull_request" or event.context.target_id <= 0:
            return self._blocked("event does not target a pull request")
        if self._global_hold():
            return self._blocked("global hold is active")
        pr = event.context.target_id
        state = self._store.load()
        envelope = state.pr_envelopes.get(pr)
        if envelope is not None and envelope.hold != "none":
            return self._blocked("PR hold is active", state)
        if not self._capacity_available(state, pr):
            return self._blocked("worker capacity is unavailable", state)
        phases: list[str] = ["context_mapper"]

        try:
            if envelope is None:
                if event.history is None:
                    return self._blocked("enrollment history is missing", state)
                history = event.history
                state = self._store.transact(
                    lambda current: self._controller.enroll_pr(current, event.observation, history)
                )
                phases.append("enroll")
            else:
                state = self._store.transact(lambda current: self._controller.observe_pr(current, event.observation))
                phases.append("observe")
            if event.problem_hash:
                registered_state, registered_id = self._controller.register_obligation(state, event.problem_hash, pr)
                state = registered_state
                obligation_id: str | None = registered_id
                state = self._store.transact(lambda current: state)
                phases.append("queue_transaction")
            else:
                obligation_id = event.obligation_id
            if obligation_id:
                for proof in event.finding_evidence:

                    def register_finding(current: QueueState, proof: Evidence = proof) -> QueueState:
                        return self._controller.register_finding(current, obligation_id or "", proof)

                    state = self._store.transact(register_finding)
                if event.finding_evidence:
                    phases.append("findings")
            if event.request_id:
                if not event.batch_id or not obligation_id:
                    return self._blocked("dispatch lineage is incomplete", state, phases)

                def request_admission(current: QueueState) -> QueueState:
                    return self._controller.request_worker_admission(
                        current,
                        request_id=event.request_id or "",
                        pr_number=pr,
                        obligation_id=obligation_id or "",
                        batch_id=event.batch_id or "",
                        worker_id=f"pr-{pr}",
                        provider="github",
                        model="gpt-5.6-luna",
                    )[0]

                state = self._store.transact(request_admission)
                state, admission_decision = self._controller.admit_worker(state, event.request_id)
                if not admission_decision.admitted:
                    return self._blocked(admission_decision.reason, state, phases)
                state = self._store.transact(lambda current: state)
                phases.append("admission")
                state = self._store.transact(
                    lambda current: self._controller.mark_worker_dispatch_unknown(current, event.request_id or "")
                )
                self._provider.dispatch(pr)
                phases.append("dispatch")
            for evidence in event.dispositions:
                disposition_decision = evaluate_disposition(
                    evidence,
                    current_head_sha=event.observation.head_sha,
                    current_source_revision=event.observation.source_revision,
                )
                if not disposition_decision.accepted:
                    return self._blocked(disposition_decision.reason, state, phases)
            if event.dispositions:
                phases.append("disposition_verification")
            if effect_provider and event.thread_effects:
                coordinator = IssueEffectCoordinator(effect_provider)
                for effect in event.thread_effects:
                    coordinator.defer(**effect)
                phases.append("deferral_effects")
            if description_provider and event.description_edit:
                update_description_guarded(
                    description_provider,
                    pr_number=pr,
                    edit=event.description_edit,
                    expected_hash=event.description_hash,
                )
                phases.append("description")
            comment_id = sync_status_comment(status_provider, state, pr) if status_provider else None
            if status_provider:
                phases.append("status")
            approval = self._controller.approval_eligible(state, pr, self._provider.approval_observation(pr))
            merge = self._controller.merge_eligible(state, pr, self._provider.merge_observation(pr))
            phases.extend(("approval_gate", "merge_gate", "terminal_settlement"))
            return ReliabilitySliceResult(
                "settled" if merge.eligible else "blocked",
                state,
                tuple(phases),
                approval,
                merge,
                comment_id,
            )
        except AdmissionBlockedError as exc:
            return self._blocked(str(exc), self._store.load(), phases)

    @staticmethod
    def _blocked(
        reason: str, state: QueueState | None = None, phases: list[str] | None = None
    ) -> ReliabilitySliceResult:
        return ReliabilitySliceResult(
            "blocked", state or QueueState("", 0, {}, [], []), tuple(phases or ()), reason=reason
        )


def coalesce_wakeups(events: list[ReliabilitySliceEvent]) -> list[ReliabilitySliceEvent]:
    """Remove duplicate wakeups before they reach the orchestrator."""
    contexts = coalesce_event_contexts([event.context for event in events])
    result: list[ReliabilitySliceEvent] = []
    for event in events:
        if event.context in contexts:
            result.append(event)
            contexts.remove(event.context)
    return result
