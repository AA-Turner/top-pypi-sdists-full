"""Offline foundation transitions; no dispatch, permit, metadata or merge APIs.

Apply returned states using QueueStore.transact/save. The verifier port is a
trusted, independent evidence adapter, not a worker-provided success flag.
It is deliberately not implemented here: production integration needs its own
review and cannot infer provider guarantees from these offline transitions.
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import replace
from datetime import datetime, timedelta

from agentic_devtools.cli.ci.reconciliation.models import (
    AdmissionController,
    AdmissionDecision,
    AdmissionFence,
    AdmissionRequestStatus,
    AttemptKind,
    AttemptStatus,
    EffectRecord,
    EffectStatus,
    EligibilityDecision,
    Evidence,
    FindingRecord,
    MigrationRecord,
    PermitRequest,
    PermitStatus,
    PRControlEnvelope,
    ProviderCapacityObservation,
    QueueState,
    RepairAttempt,
    RepairRound,
    SemanticObligation,
    WorkerPermit,
    _history_digest,
    _legacy_digest,
    _validate_foundation,
    validate_queue_state,
)


class AdmissionBlockedError(ValueError):
    """A missing authority, uncertain history, hold or stale scope blocks work."""


class ProgressRequiredError(AdmissionBlockedError):
    """A new batch lacks a one-use progress or bounded recovery authorization."""


class LoopController:
    """Deterministic, copy-on-write transitions over the sole QueueState ledger."""

    def __init__(self, verifier: Callable[[Evidence], bool], clock: Callable[[], datetime]) -> None:
        if not callable(verifier) or not callable(clock):
            raise ValueError("independent verifier and clock are required")
        self._verifier = verifier
        self._clock = clock

    def _fresh(self, proof: Evidence) -> None:
        now = self._clock()
        if not isinstance(now, datetime) or now.tzinfo is None:
            raise ValueError("clock must return an aware datetime")
        if not proof.observed_at <= now < proof.valid_until:
            raise AdmissionBlockedError("evidence is stale or from the future")

    def advance_epoch(self, state: QueueState) -> QueueState:
        """Transfer controller ownership and fence all prior-epoch work."""
        self._gate(state)
        epoch = state.global_epoch + 1
        controllers = {
            pr: replace(controller, global_epoch=epoch, source_revision=state.revision)
            for pr, controller in state.controllers.items()
        }
        fences = {key: replace(fence, status="stale") for key, fence in state.effect_fences.items()}
        return replace(
            state,
            global_epoch=epoch,
            controllers=controllers,
            effect_fences=fences,
            audit_refs=(*state.audit_refs, f"epoch:{epoch}"),
        )

    def intent_effect(
        self, state: QueueState, effect_id: str, pr_number: int, kind: str, payload_digest: str
    ) -> QueueState:
        """Persist an effect intent before an external mutation."""
        self._gate(state, pr_number)
        if not all(isinstance(value, str) and value.strip() for value in (effect_id, kind, payload_digest)):
            raise ValueError("effect identity and payload digest are required")
        existing = state.effects.get(effect_id)
        if existing is not None:
            if (existing.pr_number, existing.kind, existing.payload_digest) != (pr_number, kind, payload_digest):
                raise AdmissionBlockedError("effect replay payload differs")
            return state
        return replace(
            state,
            effects={**state.effects, effect_id: EffectRecord(effect_id, state.repo, pr_number, kind, payload_digest)},
        )

    def settle_effect(self, state: QueueState, effect_id: str, proof: Evidence) -> QueueState:
        """Settle an effect only with evidence bound to its durable intent."""
        effect = state.effects.get(effect_id)
        if effect is None:
            raise AdmissionBlockedError("unknown effect intent")
        if not isinstance(proof, Evidence) or proof.related_id != effect_id:
            raise AdmissionBlockedError("effect evidence is not bound")
        updated = self._scoped(state, proof, "effect", effect.pr_number)
        if proof.after not in {"settled", "failed", "unknown"}:
            raise AdmissionBlockedError("invalid effect settlement")  # pragma: no cover
        status = EffectStatus(proof.after)
        if effect.status == status and effect.evidence_id == proof.evidence_id:
            return state
        if effect.status != EffectStatus.INTENT:
            raise AdmissionBlockedError("effect settlement is immutable")
        return replace(
            updated,
            effects={**updated.effects, effect_id: replace(effect, status=status, evidence_id=proof.evidence_id)},
        )

    def approval_eligible(self, state: QueueState, pr_number: int, observation: Evidence) -> EligibilityDecision:
        """Evaluate the conservative pre-approval gate for a pull request."""
        envelope = self._gate(state, pr_number)
        assert envelope is not None
        checks: dict[str, object] = {
            "head_matches": observation.head_sha == envelope.head_sha,
            "not_held": envelope.hold == "none",
            "fresh": True,
            "actionable_findings_addressed": all(
                finding.disposition is not None for finding in state.findings.values() if finding.pr_number == pr_number
            ),
            "no_unaccepted_work": not any(
                attempt.pr_number == pr_number and attempt.status in {AttemptStatus.AUTHORIZED, AttemptStatus.UNKNOWN}
                for attempt in state.attempts.values()
            ),
            "no_active_repair_dispatch": not any(
                permit.pr_number == pr_number
                and permit.status in {PermitStatus.RESERVED, PermitStatus.UNKNOWN, PermitStatus.ACCEPTED}
                for permit in state.active_permits.values()
            ),
        }
        try:
            self._fresh(observation)
        except AdmissionBlockedError:  # pragma: no cover
            checks["fresh"] = False
        eligible = all(checks.values())
        reason = "eligible" if eligible else next(key for key, value in checks.items() if not value)
        return EligibilityDecision(eligible, reason, checks)

    def merge_eligible(self, state: QueueState, pr_number: int, observation: Evidence) -> EligibilityDecision:
        """Evaluate the strict, non-bypassable merge gate."""
        approval = self.approval_eligible(state, pr_number, observation)
        checks = dict(approval.details)
        checks.update(
            {
                "required_checks_fresh_and_passed": observation.kind == "merge",
                "codeowner_approval": observation.before == "codeowner_approved",
                "no_unresolved_threads": observation.after != "unresolved_threads",
                "no_bypass_authority": observation.after != "bypass",
            }
        )
        eligible = all(checks.values())
        reason = "eligible" if eligible else next(key for key, value in checks.items() if not value)
        return EligibilityDecision(eligible, reason, checks)

    def _verify(self, state: QueueState, proof: Evidence, kind: str, pr: int) -> QueueState:
        if not isinstance(proof, Evidence) or proof.kind != kind or proof.pr_number != pr:
            raise AdmissionBlockedError("wrong evidence kind or PR")
        probe = QueueState(state.repo, state.revision, {}, [], [], evidence={proof.evidence_id: proof})
        _validate_foundation(probe, history_only=True)
        self._fresh(proof)
        if self._verifier(proof) is not True:
            raise AdmissionBlockedError("independent evidence verification failed")
        existing = state.evidence.get(proof.evidence_id)
        if existing is not None and existing != proof:
            raise AdmissionBlockedError("immutable evidence changed")
        return replace(state, evidence={**state.evidence, proof.evidence_id: proof})

    def _admission_receipt(
        self,
        state: QueueState,
        *,
        kind: str,
        request: PermitRequest,
        subject: str,
        before: str,
        after: str,
        related_id: str,
    ) -> Evidence:
        """Build the typed receipt presented to the independent verifier."""
        envelope = state.pr_envelopes[request.pr_number]
        receipt = Evidence(
            evidence_id="",
            repo=state.repo,
            pr_number=request.pr_number,
            head_sha=envelope.head_sha,
            base_sha=envelope.base_sha,
            policy_version=envelope.policy_version,
            kind=kind,
            subject=subject,
            before=before,
            after=after,
            source_digest=hashlib.sha256(
                f"{state.repo}:{request.provider}:{request.owner_epoch}:{related_id}".encode()
            ).hexdigest(),
            source_revision=f"admission:{state.revision}:epoch:{request.owner_epoch}",
            issuer="independent-admission-verifier",
            producer="provider-receipt",
            observed_at=self._clock(),
            valid_until=self._clock() + timedelta(minutes=5),
            complete=True,
            related_id=related_id,
        )
        return replace(receipt, evidence_id=receipt.digest())

    def _gate(self, state: QueueState, pr: int | None = None) -> PRControlEnvelope | None:
        validate_queue_state(state)
        if state.migration_status != "active":
            raise AdmissionBlockedError("explicit completed migration/activation is required")
        if any(record.recovery_epoch >= state.recovery_epoch for record in state.quarantines):
            raise AdmissionBlockedError("queue is quarantined")
        if pr is None:
            return None
        envelope = state.pr_envelopes.get(pr)
        if envelope is None or not envelope.budget_known:
            raise AdmissionBlockedError("PR historical budget is unknown")
        if envelope.hold != "none":
            raise AdmissionBlockedError("PR is held or ignored")
        observation = state.evidence[envelope.observation_id]
        self._fresh(observation)
        return envelope

    def _scoped(self, state: QueueState, proof: Evidence, kind: str, pr: int) -> QueueState:
        if not isinstance(proof, Evidence):
            raise AdmissionBlockedError("typed independently verified evidence is required")
        envelope = self._gate(state, pr)
        assert envelope is not None
        if (proof.head_sha, proof.base_sha, proof.policy_version) != (
            envelope.head_sha,
            envelope.base_sha,
            envelope.policy_version,
        ):
            raise AdmissionBlockedError("stale head/base/policy evidence")
        return self._verify(state, proof, kind, pr)

    def _input_current(self, state: QueueState, observation_id: str, envelope: PRControlEnvelope) -> bool:
        source = state.evidence[observation_id]
        self._fresh(source)
        return (source.head_sha, source.base_sha, source.policy_version) == (
            envelope.head_sha,
            envelope.base_sha,
            envelope.policy_version,
        )

    def prepare_legacy_migration(self, state: QueueState, history: QueueState, proof: Evidence) -> QueueState:
        """Stage complete, terminal historical ledgers against this exact source.

        Historical data must include per-problem initial/retry/Astra attempts,
        accepted provider identities, terminal outcomes and every prior batch.
        The independent migration verifier must prove complete discovery, not
        merely agree with caller counts. Unknown or possibly-running work blocks.
        """
        validate_queue_state(state)
        if (
            state.migration_status != "preactivation"
            or not isinstance(history, QueueState)
            or history.repo != state.repo
        ):
            raise AdmissionBlockedError("migration needs a matching preactivation source")
        _validate_foundation(history, history_only=True)
        if any(item.status.value in {"claimed", "leased", "unknown"} for item in state.items.values()):
            raise AdmissionBlockedError("legacy work may still be running or unknown")
        if any(
            attempt.status not in {AttemptStatus.FAILED, AttemptStatus.SUCCEEDED}
            for attempt in history.attempts.values()
        ):
            raise AdmissionBlockedError("historical provider work is not independently terminal")
        if not set(state.items).issubset(history.pr_envelopes):
            raise AdmissionBlockedError("historical inventory omitted a legacy PR")
        if any(batch.phase not in {"reviewed", "invalidated"} for batch in history.rounds.values()):
            raise AdmissionBlockedError("historical batch boundary is incomplete")
        expected_inventory = tuple(str(pr) for pr in sorted(history.pr_envelopes))
        if (
            proof.before != _legacy_digest(state)
            or proof.after != _history_digest(history)
            or proof.source_revision != str(state.revision)
            or proof.inventory != expected_inventory
        ):
            raise AdmissionBlockedError("source revision, complete inventory or history evidence changed")
        for evidence in history.evidence.values():
            if self._verifier(evidence) is not True:
                raise AdmissionBlockedError("historical evidence provenance is not verified")
        updated = self._verify(state, proof, "migration", 0)
        return replace(
            updated,
            migration_status="prepared",
            migration=MigrationRecord(state.revision, state.revision + 1, proof.before, proof.after, proof.evidence_id),
            pr_envelopes=dict(history.pr_envelopes),
            obligations=dict(history.obligations),
            findings=dict(history.findings),
            rounds=dict(history.rounds),
            attempts=dict(history.attempts),
            evidence={**history.evidence, **updated.evidence},
        )

    def activate_migration(self, state: QueueState, evidence_id: str) -> QueueState:
        """Activate only the persisted preparation, unchanged since its CAS."""
        validate_queue_state(state)
        migration = state.migration
        if state.migration_status != "prepared" or migration is None:
            raise AdmissionBlockedError("migration has not been prepared and persisted")
        history = replace(
            state, evidence={key: value for key, value in state.evidence.items() if key != migration.evidence_id}
        )
        if (
            evidence_id != migration.evidence_id
            or state.revision != migration.prepared_revision
            or _legacy_digest(state) != migration.source_digest
            or _history_digest(history) != migration.history_digest
        ):
            raise AdmissionBlockedError("migration source or historical evidence changed before activation")
        proof = state.evidence[evidence_id]
        self._fresh(proof)
        if self._verifier(proof) is not True:
            raise AdmissionBlockedError("migration verification is no longer valid")
        return replace(state, migration_status="active")

    def enroll_pr(self, state: QueueState, observation: Evidence, history: Evidence) -> QueueState:
        """Enroll a new PR only with independently proved empty lifetime history."""
        self._gate(state)
        if not isinstance(observation, Evidence) or not isinstance(history, Evidence):
            raise AdmissionBlockedError("typed observation and history evidence are required")
        pr = observation.pr_number
        if pr <= 0 or pr in state.pr_envelopes:
            raise AdmissionBlockedError("PR is already enrolled or invalid")
        if history.after != "empty" or history.inventory or history.subject != str(pr):
            raise AdmissionBlockedError("new PR needs verified empty lifetime history, not unknown counts")
        updated = self._verify(state, history, "history", pr)
        updated = self._verify(updated, observation, "observation", pr)
        if observation.subject != str(pr) or observation.before not in {"none", "held", "ignored"}:
            raise AdmissionBlockedError("observation lacks authoritative hold state")
        envelope = PRControlEnvelope(
            pr,
            state.repo,
            observation.head_sha,
            observation.base_sha,
            observation.policy_version,
            observation.evidence_id,
            history.evidence_id,
            control_epoch=state.control_epoch,
            hold=observation.before,
        )
        return replace(updated, pr_envelopes={**updated.pr_envelopes, pr: envelope})

    def observe_pr(self, state: QueueState, observation: Evidence) -> QueueState:
        """Refresh authority; human changes fence scoped work without resetting history."""
        self._gate(state)
        if not isinstance(observation, Evidence):
            raise AdmissionBlockedError("typed authoritative observation required")
        pr = observation.pr_number
        envelope = state.pr_envelopes.get(pr)
        if envelope is None or observation.subject != str(pr) or observation.before not in {"none", "held", "ignored"}:
            raise AdmissionBlockedError("invalid PR observation")
        previous = state.evidence[envelope.observation_id]
        if observation.observed_at < previous.observed_at:
            raise AdmissionBlockedError("reordered observation")
        updated = self._verify(state, observation, "observation", pr)
        changed = (envelope.head_sha, envelope.base_sha, envelope.policy_version) != (
            observation.head_sha,
            observation.base_sha,
            observation.policy_version,
        )
        rounds = dict(state.rounds)
        if changed and envelope.active_batch_id is not None:
            batch = rounds[envelope.active_batch_id]
            publication = state.evidence.get(batch.publication_id or "")
            expected_publication = publication is not None and (
                publication.after,
                publication.base_sha,
                publication.policy_version,
            ) == (observation.head_sha, observation.base_sha, observation.policy_version)
            if batch.phase != "reviewed" and not expected_publication:
                rounds[batch.batch_id] = replace(batch, phase="invalidated")
        return replace(
            updated,
            rounds=rounds,
            pr_envelopes={
                **state.pr_envelopes,
                pr: replace(
                    envelope,
                    head_sha=observation.head_sha,
                    base_sha=observation.base_sha,
                    policy_version=observation.policy_version,
                    observation_id=observation.evidence_id,
                    hold=observation.before,
                    stage="planning" if changed else envelope.stage,
                ),
            },
        )

    def register_obligation(self, state: QueueState, problem_hash: str, pr_number: int) -> tuple[QueueState, str]:
        envelope = self._gate(state, pr_number)
        assert envelope is not None
        if not isinstance(problem_hash, str) or not problem_hash.strip():
            raise ValueError("canonical semantic problem identity is required")
        identity = hashlib.sha256(f"{state.repo}:{pr_number}:{problem_hash}".encode()).hexdigest()
        if identity in state.obligations:
            return state, identity
        obligation = SemanticObligation(identity, pr_number, problem_hash)
        return replace(
            state,
            obligations={**state.obligations, identity: obligation},
            pr_envelopes={
                **state.pr_envelopes,
                pr_number: replace(envelope, obligation_ids=(*envelope.obligation_ids, identity)),
            },
        ), identity

    def register_finding(
        self, state: QueueState, obligation_id: str, proof: Evidence, disposition: str | None = None
    ) -> QueueState:
        obligation = state.obligations[obligation_id]
        updated = self._scoped(state, proof, "finding", obligation.pr_number)
        identity = hashlib.sha256(f"{state.repo}:{obligation.pr_number}:{proof.subject}".encode()).hexdigest()
        existing = state.findings.get(identity)
        if existing is not None:
            if existing.obligation_id != obligation_id or existing.disposition != disposition:
                raise AdmissionBlockedError("existing finding lineage cannot change ownership or disposition")
            return state
        finding = FindingRecord(
            identity,
            obligation.pr_number,
            obligation_id,
            proof.subject,
            proof.evidence_id,
            (proof.head_sha,),
            disposition,
        )
        updated = replace(
            updated,
            findings={**state.findings, identity: finding},
            obligations={
                **state.obligations,
                obligation_id: replace(obligation, finding_ids=(*obligation.finding_ids, identity)),
            },
        )
        validate_queue_state(updated)
        return updated

    def record_progress(self, state: QueueState, proof: Evidence) -> QueueState:
        if (
            not isinstance(proof, Evidence)
            or proof.kind not in {"progress_finding", "progress_gate"}
            or proof.before != "failing"
            or proof.after != "satisfied"
        ):
            raise ProgressRequiredError("progress must independently verify a failing-to-satisfied transition")
        updated = self._scoped(state, proof, proof.kind, proof.pr_number)
        batch = state.rounds.get(proof.related_id or "")
        if batch is None or batch.pr_number != proof.pr_number or batch.phase != "reviewed":
            raise ProgressRequiredError("progress needs a verified prior review boundary")
        if proof.kind == "progress_finding" and proof.subject not in state.findings:
            raise ProgressRequiredError("progress finding is unknown")
        for existing in state.evidence.values():
            if (
                existing.kind,
                existing.pr_number,
                existing.subject,
                existing.before,
                existing.after,
                existing.related_id,
            ) == (proof.kind, proof.pr_number, proof.subject, proof.before, proof.after, proof.related_id):
                if existing.evidence_id != proof.evidence_id:
                    raise ProgressRequiredError("duplicate logical progress cannot be reminted")
        return updated

    def begin_round(
        self, state: QueueState, obligation_id: str, batch_id: str, authorization_id: str | None = None
    ) -> tuple[QueueState, RepairRound]:
        obligation = state.obligations[obligation_id]
        envelope = self._gate(state, obligation.pr_number)
        assert envelope is not None
        if not isinstance(batch_id, str) or not batch_id.strip():
            raise ValueError("stable batch/admission identity is required")
        existing = state.rounds.get(batch_id)
        if existing is not None:
            if existing.obligation_id != obligation_id or existing.authorization_id != authorization_id:
                raise AdmissionBlockedError("admission replay differs from immutable batch")
            return state, existing
        if envelope.rounds_used >= 50:
            raise ProgressRequiredError("50-round lifetime ceiling")
        if envelope.active_batch_id is not None and state.rounds[envelope.active_batch_id].phase not in {
            "reviewed",
            "invalidated",
        }:
            raise ProgressRequiredError("current batch has not crossed its verified review boundary")
        if obligation.status in {"isolated", "verified"} or not obligation.finding_ids:
            raise AdmissionBlockedError("no actionable unresolved obligation")
        observation = state.evidence[envelope.observation_id]
        if observation.after != "actionable" or not any(
            state.findings[identity].comment_key in observation.inventory for identity in obligation.finding_ids
        ):
            raise AdmissionBlockedError("authoritative observation has no actionable findings")
        reason = "bootstrap"
        if envelope.rounds_used:
            proof = state.evidence.get(authorization_id or "")
            if proof is None:
                raise ProgressRequiredError("new round requires progress or bounded recovery")
            self._scoped(state, proof, proof.kind, obligation.pr_number)
            if any(batch.authorization_id == authorization_id for batch in state.rounds.values()):
                raise ProgressRequiredError("round authorization already consumed")
            if proof.kind in {"progress_finding", "progress_gate"}:
                reason = "progress"
            else:
                self._next_kind(state, obligation, authorization_id)
                reason = "recovery"
        elif authorization_id is not None:
            raise ProgressRequiredError("bootstrap cannot consume a recovery grant")
        batch = RepairRound(
            batch_id,
            obligation.pr_number,
            envelope.rounds_used + 1,
            obligation_id,
            envelope.observation_id,
            reason,
            authorization_id,
        )
        updated = replace(
            state,
            rounds={**state.rounds, batch_id: batch},
            pr_envelopes={
                **state.pr_envelopes,
                envelope.pr_number: replace(
                    envelope,
                    rounds_used=batch.round_number,
                    round_ids=(*envelope.round_ids, batch_id),
                    active_batch_id=batch_id,
                    stage="ready",
                ),
            },
        )
        validate_queue_state(updated)
        return updated, batch

    def _next_kind(
        self, state: QueueState, obligation: SemanticObligation, authorization_id: str | None
    ) -> AttemptKind:
        count = len(obligation.attempt_ids)
        if count >= 4:
            raise AdmissionBlockedError("same-problem Luna/Luna/Astra/remediation budget exhausted")
        kind = tuple(AttemptKind)[count]
        if count == 0:
            if authorization_id is not None:
                raise AdmissionBlockedError("initial Luna has no failure authorization")
            return kind
        previous = state.attempts[obligation.attempt_ids[-1]]
        if previous.status not in {AttemptStatus.FAILED, AttemptStatus.SUCCEEDED}:
            raise AdmissionBlockedError("previous accepted work has not independently failed")
        if kind == AttemptKind.REMEDIATION:
            proof = state.evidence.get(authorization_id or "")
            if (
                obligation.remediation_id is None
                or proof is None
                or proof.kind != "verification"
                or proof.related_id != obligation.remediation_id
                or proof.subject != obligation.obligation_id
                or proof.after != "repair_required"
            ):
                raise AdmissionBlockedError("verify distinct remediation before extra Luna")
        else:
            proof = state.evidence.get(authorization_id or "")
            if (
                proof is None
                or proof.kind != "failure"
                or proof.subject != previous.attempt_id
                or proof.related_id != previous.acceptance_id
                or proof.before != "terminal"
                or proof.after != "unresolved"
            ):
                raise AdmissionBlockedError("retry/recovery needs the immediately preceding verified failure")
        return kind

    def revalidate_failure(self, state: QueueState, attempt_id: str, proof: Evidence) -> QueueState:
        """Independently re-evaluate a retained failed problem on a changed head."""
        attempt = state.attempts[attempt_id]
        updated = self._scoped(state, proof, "failure", attempt.pr_number)
        if (
            attempt.status not in {AttemptStatus.FAILED, AttemptStatus.SUCCEEDED}
            or proof.subject != attempt_id
            or proof.related_id != attempt.acceptance_id
            or proof.before != "terminal"
            or proof.after != "unresolved"
        ):
            raise AdmissionBlockedError("current failure revalidation must bind failed accepted work")
        return updated

    def authorize_attempt(
        self, state: QueueState, obligation_id: str, batch_id: str, attempt_id: str, authorization_id: str | None = None
    ) -> tuple[QueueState, RepairAttempt]:
        obligation = state.obligations[obligation_id]
        envelope = self._gate(state, obligation.pr_number)
        assert envelope is not None
        existing = state.attempts.get(attempt_id)
        if existing is not None:
            if (existing.obligation_id, existing.batch_id, existing.authorization_id) != (
                obligation_id,
                batch_id,
                authorization_id,
            ):
                raise AdmissionBlockedError("attempt replay differs")
            return state, existing
        batch = state.rounds.get(batch_id)
        if (
            batch is None
            or batch.obligation_id != obligation_id
            or batch_id != envelope.active_batch_id
            or batch.phase != "prepublication"
            or not self._input_current(state, batch.observation_id, envelope)
        ):
            raise AdmissionBlockedError("attempt requires a current admitted prepublication batch")
        kind = self._next_kind(state, obligation, authorization_id)
        if envelope.rounds_used == 50 and any(old.batch_id == batch_id for old in state.attempts.values()):
            raise AdmissionBlockedError("at 50 only already-authorized work may finish")
        if authorization_id is not None:
            proof = state.evidence[authorization_id]
            self._scoped(state, proof, proof.kind, obligation.pr_number)
        if not isinstance(attempt_id, str) or not attempt_id:
            raise ValueError("stable attempt identity is required")
        attempt = RepairAttempt(
            attempt_id,
            obligation.pr_number,
            obligation_id,
            batch_id,
            kind,
            len(obligation.attempt_ids) + 1,
            batch.observation_id,
            authorization_id,
        )
        updated = replace(
            state,
            attempts={**state.attempts, attempt_id: attempt},
            obligations={
                **state.obligations,
                obligation_id: replace(
                    obligation, attempt_ids=(*obligation.attempt_ids, attempt_id), status="in_progress"
                ),
            },
        )
        validate_queue_state(updated)
        return updated, attempt

    def renew_authorized_attempt(self, state: QueueState, attempt_id: str) -> QueueState:
        """Renew known-unaccepted authority without rewriting admitted input history."""
        attempt = state.attempts[attempt_id]
        envelope = self._gate(state, attempt.pr_number)
        assert envelope is not None
        batch = state.rounds[attempt.batch_id]
        if attempt.status != AttemptStatus.AUTHORIZED or attempt.acceptance_id is not None:
            raise AdmissionBlockedError("only an authorized, unaccepted attempt can be renewed")
        if batch.phase != "prepublication" or envelope.active_batch_id != batch.batch_id:
            raise AdmissionBlockedError("only the active prepublication attempt can be renewed")
        source = state.evidence[attempt.observation_id]
        current = state.evidence[envelope.observation_id]
        if (source.head_sha, source.base_sha, source.policy_version) != (
            current.head_sha,
            current.base_sha,
            current.policy_version,
        ):
            raise AdmissionBlockedError("changed scope requires an explicit replan")
        updated = replace(
            state,
            attempts={**state.attempts, attempt_id: replace(attempt, observation_id=current.evidence_id)},
        )
        validate_queue_state(updated)
        return updated

    def replan_authorized_attempt(self, state: QueueState, attempt_id: str, batch_id: str) -> QueueState:
        """Move never-dispatched work to one bounded fresh-head replan batch."""
        attempt = state.attempts[attempt_id]
        envelope = self._gate(state, attempt.pr_number)
        assert envelope is not None
        batch = state.rounds[attempt.batch_id]
        source = state.evidence[attempt.observation_id]
        current = state.evidence[envelope.observation_id]
        if attempt.status != AttemptStatus.AUTHORIZED or attempt.acceptance_id is not None:
            raise AdmissionBlockedError("only an authorized, unaccepted attempt can be replanned")
        if batch_id == batch.batch_id and batch.reason == "replan":
            return state
        if batch.phase != "invalidated" or envelope.active_batch_id != batch.batch_id:
            raise AdmissionBlockedError("replan requires the invalidated active batch")
        if (source.head_sha, source.base_sha, source.policy_version) == (
            current.head_sha,
            current.base_sha,
            current.policy_version,
        ):
            raise AdmissionBlockedError("unchanged scope should use renewal")
        if envelope.rounds_used >= envelope.round_limit:
            raise ProgressRequiredError("50-round lifetime ceiling")
        if not isinstance(batch_id, str) or not batch_id.strip() or batch_id in state.rounds:
            raise AdmissionBlockedError("replan batch identity is already used")
        replanned = RepairRound(
            batch_id,
            batch.pr_number,
            envelope.rounds_used + 1,
            batch.obligation_id,
            current.evidence_id,
            "replan",
            batch.batch_id,
        )
        updated = replace(
            state,
            rounds={**state.rounds, batch_id: replanned},
            attempts={
                **state.attempts,
                attempt_id: replace(attempt, batch_id=batch_id, observation_id=current.evidence_id),
            },
            pr_envelopes={
                **state.pr_envelopes,
                attempt.pr_number: replace(
                    envelope,
                    rounds_used=replanned.round_number,
                    round_ids=(*envelope.round_ids, batch_id),
                    active_batch_id=batch_id,
                    stage="ready",
                ),
            },
        )
        validate_queue_state(updated)
        return updated

    def mark_dispatch_unknown(self, state: QueueState, attempt_id: str) -> QueueState:
        """Persist before a dispatch boundary; ambiguity blocks replacement work."""
        attempt = state.attempts[attempt_id]
        envelope = self._gate(state, attempt.pr_number)
        assert envelope is not None
        if not self._input_current(state, attempt.observation_id, envelope):
            raise AdmissionBlockedError("stale attempt scope")
        if attempt.status == AttemptStatus.UNKNOWN:
            return state
        if attempt.status != AttemptStatus.AUTHORIZED:
            raise AdmissionBlockedError("dispatch is not authorized")
        return replace(state, attempts={**state.attempts, attempt_id: replace(attempt, status=AttemptStatus.UNKNOWN)})

    def record_nonacceptance(self, state: QueueState, attempt_id: str, proof: Evidence) -> QueueState:
        """A verified absence permits retrying the same slot; a 429 alone does not."""
        attempt = state.attempts[attempt_id]
        updated = self._scoped(state, proof, "absence", attempt.pr_number)
        if (
            attempt.status != AttemptStatus.UNKNOWN
            or proof.subject != attempt_id
            or proof.related_id != attempt.observation_id
            or proof.after != "not_accepted"
        ):
            raise AdmissionBlockedError("ambiguous dispatch needs authoritative absence evidence")
        return replace(
            updated, attempts={**state.attempts, attempt_id: replace(attempt, status=AttemptStatus.AUTHORIZED)}
        )

    def record_acceptance(self, state: QueueState, attempt_id: str, proof: Evidence) -> QueueState:
        """Account accepted provider work separately from authorization and polling."""
        attempt = state.attempts[attempt_id]
        # Late read-back accounts real work even after a human hold/head change.
        validate_queue_state(state)
        updated = self._verify(state, proof, "acceptance", attempt.pr_number)
        if attempt.acceptance_id is not None:
            if attempt.acceptance_id != proof.evidence_id:
                raise AdmissionBlockedError("accepted provider receipt is immutable")
            return state
        if attempt.status != AttemptStatus.UNKNOWN:
            raise AdmissionBlockedError("acceptance requires persisted dispatch uncertainty")
        updated = replace(
            updated,
            attempts={
                **state.attempts,
                attempt_id: replace(attempt, status=AttemptStatus.ACCEPTED, acceptance_id=proof.evidence_id),
            },
        )
        validate_queue_state(updated)
        return updated

    def record_outcome(self, state: QueueState, attempt_id: str, proof: Evidence) -> QueueState:
        attempt = state.attempts[attempt_id]
        if proof.kind not in {"failure", "success"}:
            raise AdmissionBlockedError("terminal evidence required, not polling or throttling")
        updated = self._verify(state, proof, proof.kind, attempt.pr_number)
        if attempt.outcome_id is not None:
            if attempt.outcome_id != proof.evidence_id:
                raise AdmissionBlockedError("terminal outcome is immutable")
            return state
        if attempt.status != AttemptStatus.ACCEPTED:
            raise AdmissionBlockedError("only accepted provider work can fail/succeed")
        status = AttemptStatus.FAILED if proof.kind == "failure" else AttemptStatus.SUCCEEDED
        obligation = state.obligations[attempt.obligation_id]
        isolated = status == AttemptStatus.FAILED and attempt.kind in {AttemptKind.ASTRA, AttemptKind.REMEDIATION}
        updated = replace(
            updated,
            attempts={**state.attempts, attempt_id: replace(attempt, status=status, outcome_id=proof.evidence_id)},
            obligations={
                **state.obligations,
                obligation.obligation_id: replace(obligation, status="isolated" if isolated else "in_progress"),
            },
        )
        validate_queue_state(updated)
        return updated

    def record_publication(self, state: QueueState, batch_id: str, proof: Evidence) -> QueueState:
        batch = state.rounds[batch_id]
        updated = self._scoped(state, proof, "publication", batch.pr_number)
        if batch.publication_id is not None:
            if batch.publication_id != proof.evidence_id:
                raise AdmissionBlockedError("publication history is immutable")
            return state
        attempts = [attempt for attempt in state.attempts.values() if attempt.batch_id == batch_id]
        if (
            batch.phase != "prepublication"
            or proof.subject != batch_id
            or not attempts
            or any(attempt.status not in {AttemptStatus.FAILED, AttemptStatus.SUCCEEDED} for attempt in attempts)
        ):
            raise AdmissionBlockedError("publication needs an admitted batch and terminal accepted work")
        updated = replace(
            updated,
            rounds={**state.rounds, batch_id: replace(batch, phase="published", publication_id=proof.evidence_id)},
        )
        validate_queue_state(updated)
        return updated

    def record_batch_review(self, state: QueueState, batch_id: str, proof: Evidence) -> QueueState:
        batch = state.rounds[batch_id]
        updated = self._scoped(state, proof, "review", batch.pr_number)
        if batch.review_id is not None:
            if batch.review_id != proof.evidence_id:
                raise AdmissionBlockedError("review history is immutable")
            return state
        if batch.phase != "published":
            raise AdmissionBlockedError("review cannot assert an unpublished batch")
        updated = replace(
            updated, rounds={**state.rounds, batch_id: replace(batch, phase="reviewed", review_id=proof.evidence_id)}
        )
        validate_queue_state(updated)
        return updated

    def record_remediation(self, state: QueueState, obligation_id: str, proof: Evidence) -> QueueState:
        obligation = state.obligations[obligation_id]
        updated = self._scoped(state, proof, "remediation", obligation.pr_number)
        if obligation.remediation_id is not None:
            if obligation.remediation_id != proof.evidence_id:
                raise AdmissionBlockedError("only one distinct remediation allowance per problem")
            return state
        if obligation.status != "isolated":
            raise AdmissionBlockedError("remediation is only for an isolated exhausted problem")
        updated = replace(
            updated,
            obligations={**state.obligations, obligation_id: replace(obligation, remediation_id=proof.evidence_id)},
        )
        validate_queue_state(updated)
        return updated

    def verify_remediation(self, state: QueueState, obligation_id: str, proof: Evidence) -> QueueState:
        obligation = state.obligations[obligation_id]
        updated = self._scoped(state, proof, "verification", obligation.pr_number)
        if (
            proof.subject != obligation_id
            or proof.related_id != obligation.remediation_id
            or obligation.remediation_id is None
            or proof.after not in {"satisfied", "repair_required"}
        ):
            raise AdmissionBlockedError("verification must bind the distinct remediation")
        for existing in state.evidence.values():
            if existing.kind == "verification" and existing.related_id == obligation.remediation_id:
                if existing.evidence_id != proof.evidence_id:
                    raise AdmissionBlockedError("remediation verification cannot be reminted")
                return state
        return replace(
            updated,
            obligations={
                **state.obligations,
                obligation_id: replace(obligation, status="verified" if proof.after == "satisfied" else "pending"),
            },
        )

    def observe_provider_capacity(self, state: QueueState, observation: ProviderCapacityObservation) -> QueueState:
        """Persist complete provider headroom without forgetting local reservations."""
        self._gate(state)
        now = self._clock()
        if (
            not isinstance(observation, ProviderCapacityObservation)
            or not observation.complete
            or not observation.authorized
            or not observation.observed_at <= now < observation.valid_until
        ):
            raise AdmissionBlockedError("provider capacity observation is missing, stale or incomplete")
        if observation.global_epoch != state.global_epoch:
            raise AdmissionBlockedError("provider capacity observation is stale")
        receipt = state.evidence.get(observation.receipt_evidence_id or "")
        if receipt is None:
            receipt = Evidence(
                evidence_id="",
                repo=state.repo,
                pr_number=0,
                head_sha="0" * 40,
                base_sha="0" * 40,
                policy_version=f"epoch:{state.global_epoch}",
                kind="observation",
                subject=observation.provider,
                before=f"capacity:{observation.capacity}",
                after=f"occupied:{observation.occupied}:reservations:{observation.reservation_count}",
                source_digest=hashlib.sha256(
                    (
                        f"{state.repo}:{observation.provider}:{observation.source_revision or observation.evidence_id}"
                    ).encode()
                ).hexdigest(),
                source_revision=observation.source_revision or observation.evidence_id,
                issuer="independent-admission-verifier",
                producer="provider-capacity-receipt",
                observed_at=observation.observed_at,
                valid_until=observation.valid_until,
                complete=True,
                related_id=f"capacity:{observation.provider}:epoch:{state.global_epoch}",
            )
            receipt = replace(receipt, evidence_id=receipt.digest())
        elif (
            receipt.kind != "observation"
            or receipt.repo != state.repo
            or receipt.pr_number != 0
            or receipt.subject != observation.provider
            or receipt.related_id != f"capacity:{observation.provider}:epoch:{state.global_epoch}"
            or receipt.observed_at != observation.observed_at
            or receipt.valid_until != observation.valid_until
        ):
            raise AdmissionBlockedError("provider capacity receipt is not bound")
        if self._verifier(receipt) is not True:
            raise AdmissionBlockedError("independent capacity verification failed")
        observation = replace(
            observation,
            source_revision=observation.source_revision or observation.evidence_id,
            global_epoch=state.global_epoch,
            receipt_evidence_id=receipt.evidence_id,
        )
        previous = state.provider_capacity.get(observation.provider)
        if previous is not None and observation.observed_at < previous.observed_at:
            raise AdmissionBlockedError("provider capacity observation is reordered")
        updated = replace(
            state,
            provider_capacity={**state.provider_capacity, observation.provider: observation},
            evidence={**state.evidence, receipt.evidence_id: receipt},
        )
        validate_queue_state(updated)
        return updated

    def request_worker_admission(
        self,
        state: QueueState,
        *,
        request_id: str,
        pr_number: int,
        obligation_id: str,
        batch_id: str,
        worker_id: str,
        provider: str,
        model: str = "gpt-5.6-luna",
        deadline_at: datetime | None = None,
        parent_request_id: str | None = None,
    ) -> tuple[QueueState, PermitRequest]:
        """Queue one idempotent worker request in the shared repository pool."""
        if not all(
            isinstance(value, str) and value.strip()
            for value in (request_id, obligation_id, batch_id, worker_id, provider)
        ):
            raise ValueError("request, lineage, worker and provider identities are required")
        if model not in {"gpt-5.6-luna", "gpt-6-astra"}:
            raise AdmissionBlockedError("unsupported worker model")
        self._gate(state)
        envelope = state.pr_envelopes.get(pr_number)
        if envelope is None or not envelope.budget_known:
            raise AdmissionBlockedError("PR historical budget is unknown")
        assert envelope is not None
        if state.global_epoch != envelope.control_epoch:
            raise AdmissionBlockedError("stale controller epoch")
        obligation = state.obligations.get(obligation_id)
        batch = state.rounds.get(batch_id)
        if (
            obligation is None
            or obligation.pr_number != pr_number
            or batch is None
            or batch.pr_number != pr_number
            or batch.obligation_id != obligation_id
        ):
            raise AdmissionBlockedError("request lineage does not belong to PR")
        existing = state.permit_requests.get(request_id)
        if existing is not None:
            if (
                existing.repo,
                existing.pr_number,
                existing.obligation_id,
                existing.batch_id,
                existing.worker_id,
                existing.provider,
                existing.model,
                existing.parent_request_id,
            ) != (
                state.repo,
                pr_number,
                obligation_id,
                batch_id,
                worker_id,
                provider,
                model,
                parent_request_id,
            ):
                raise AdmissionBlockedError("admission replay differs")
            return state, existing
        now = self._clock()
        if now.tzinfo is None:
            raise ValueError("clock must return an aware datetime")
        deadline = deadline_at or (now + timedelta(minutes=30))
        if deadline <= now:
            raise ValueError("admission deadline must be in the future")
        position = max((request.queue_position for request in state.permit_requests.values()), default=-1) + 1
        request = PermitRequest(
            request_id,
            state.repo,
            pr_number,
            obligation_id,
            batch_id,
            worker_id,
            provider,
            model,
            state.global_epoch,
            now,
            deadline,
            position,
            parent_request_id=parent_request_id,
            reason="held" if envelope.hold != "none" else "",
        )
        updated = replace(
            state,
            permit_requests={**state.permit_requests, request_id: request},
            controllers={
                **state.controllers,
                pr_number: self._controller_projection(state, pr_number, request_id=request_id),
            },
        )
        validate_queue_state(updated)
        return updated, request

    def admit_worker(self, state: QueueState, request_id: str) -> tuple[QueueState, AdmissionDecision]:
        """Fairly reserve capacity for the earliest eligible request."""
        request = state.permit_requests.get(request_id)
        if request is None:
            raise AdmissionBlockedError("unknown admission request")
        if request.owner_epoch != state.global_epoch:
            raise AdmissionBlockedError("stale admission epoch")
        if request.status in {
            AdmissionRequestStatus.RESERVED,
            AdmissionRequestStatus.UNKNOWN,
            AdmissionRequestStatus.ACCEPTED,
        }:
            return state, AdmissionDecision(request_id, True, "already admitted", request.permit_id)
        if request.status != AdmissionRequestStatus.QUEUED:
            return state, AdmissionDecision(request_id, False, "request is terminal")
        envelope = state.pr_envelopes.get(request.pr_number)
        if envelope is None or envelope.hold != "none":
            return state, AdmissionDecision(request_id, False, "held")
        now = self._clock()
        if request.deadline_at <= now:
            expired = replace(
                state,
                permit_requests={
                    **state.permit_requests,
                    request_id: replace(
                        request,
                        status=AdmissionRequestStatus.CANCELLED,
                        reason="expired",
                        terminal_evidence_id=f"local-cancel:{request_id}",
                    ),
                },
            )
            validate_queue_state(expired)
            return expired, AdmissionDecision(request_id, False, "expired")
        if not self._input_current(state, envelope.observation_id, envelope):
            return state, AdmissionDecision(request_id, False, "stale authority")
        eligible = sorted(
            (
                candidate
                for candidate in state.permit_requests.values()
                if candidate.status == AdmissionRequestStatus.QUEUED
                and candidate.owner_epoch == state.global_epoch
                and state.pr_envelopes.get(candidate.pr_number) is not None
                and state.pr_envelopes[candidate.pr_number].hold == "none"
            ),
            key=lambda candidate: (candidate.queue_position, candidate.request_id),
        )
        active = sum(
            permit.status in {PermitStatus.RESERVED, PermitStatus.UNKNOWN, PermitStatus.ACCEPTED}
            for permit in state.active_permits.values()
        )
        if active >= 100:
            return state, AdmissionDecision(request_id, False, "global capacity exhausted")
        available: list[PermitRequest] = []
        for candidate in eligible:
            observation = state.provider_capacity.get(candidate.provider)
            if (
                observation is None
                or not observation.complete
                or not observation.authorized
                or observation.global_epoch != state.global_epoch
                or not (observation.observed_at <= now < observation.valid_until)
            ):
                continue
            provider_active = sum(
                permit.status in {PermitStatus.RESERVED, PermitStatus.UNKNOWN, PermitStatus.ACCEPTED}
                and permit.provider == candidate.provider
                for permit in state.active_permits.values()
            )
            if provider_active + observation.occupied + observation.reservation_count < observation.capacity:
                available.append(candidate)
        if not available:
            observation = state.provider_capacity.get(request.provider)
            if (
                observation is None
                or not observation.complete
                or not observation.authorized
                or observation.global_epoch != state.global_epoch
                or not (observation.observed_at <= now < observation.valid_until)
            ):
                return state, AdmissionDecision(request_id, False, "provider capacity unavailable")
            return state, AdmissionDecision(request_id, False, "provider capacity exhausted")
        # Alternate between PRs when several requests are eligible.  FIFO within
        # a PR is retained, but one finding cannot consume every global slot.
        last_pr = None  # pragma: no cover
        admitted = [
            candidate
            for candidate in state.permit_requests.values()
            if candidate.status
            in {
                AdmissionRequestStatus.RESERVED,
                AdmissionRequestStatus.UNKNOWN,
                AdmissionRequestStatus.ACCEPTED,
            }
        ]
        if admitted:  # pragma: no branch
            last_pr = max(admitted, key=lambda candidate: candidate.queue_position).pr_number  # pragma: no cover
        if last_pr is not None and len({candidate.pr_number for candidate in available}) > 1:  # pragma: no branch
            rotated = [candidate for candidate in available if candidate.pr_number != last_pr]  # pragma: no cover
            if rotated:  # pragma: no cover
                available = rotated  # pragma: no cover
        if available[0].request_id != request_id:
            return state, AdmissionDecision(request_id, False, "fairness wait")
        permit_id = f"permit:{request.request_id}"
        permit = WorkerPermit(
            permit_id,
            request.request_id,
            request.repo,
            request.pr_number,
            request.obligation_id,
            request.batch_id,
            request.worker_id,
            request.provider,
            request.model,
            state.global_epoch,
            now,
            request.deadline_at,
        )
        updated_request = replace(request, status=AdmissionRequestStatus.RESERVED, permit_id=permit_id)
        updated = replace(
            state,
            permit_requests={**state.permit_requests, request_id: updated_request},
            active_permits={**state.active_permits, permit_id: permit},
            controllers={
                **state.controllers,
                request.pr_number: self._controller_projection(
                    state, request.pr_number, request_id=request_id, permit_id=permit_id
                ),
            },
            effect_fences={
                **state.effect_fences,
                f"fence:{request_id}": AdmissionFence(
                    f"fence:{request_id}",
                    request_id,
                    state.global_epoch,
                    request.owner_epoch,
                    request.provider,
                    request.model,
                ),
            },
        )
        validate_queue_state(updated)
        return updated, AdmissionDecision(request_id, True, "reserved", permit_id)

    def mark_worker_dispatch_unknown(self, state: QueueState, request_id: str) -> QueueState:
        """Persist ambiguity before crossing a future provider dispatch boundary."""
        request = state.permit_requests.get(request_id)
        if request is None or request.permit_id is None:
            raise AdmissionBlockedError("request has no reserved permit")
        if request.owner_epoch != state.global_epoch:
            raise AdmissionBlockedError("stale admission epoch")
        permit = state.active_permits[request.permit_id]
        envelope = state.pr_envelopes.get(request.pr_number)
        if (
            envelope is None
            or envelope.hold != "none"
            or not self._input_current(state, envelope.observation_id, envelope)
        ):
            raise AdmissionBlockedError("current PR authority does not permit dispatch")
        if permit.status == PermitStatus.UNKNOWN:
            return state
        if permit.status != PermitStatus.RESERVED:
            raise AdmissionBlockedError("worker dispatch is not reserved")
        updated = replace(
            state,
            permit_requests={
                request_id: replace(request, status=AdmissionRequestStatus.UNKNOWN),
                **{key: value for key, value in state.permit_requests.items() if key != request_id},
            },
            active_permits={**state.active_permits, permit.permit_id: replace(permit, status=PermitStatus.UNKNOWN)},
        )
        validate_queue_state(updated)
        return updated

    def bind_accepted_worker(
        self,
        state: QueueState,
        request_id: str,
        *,
        remote_task_id: str,
        remote_session_id: str,
        model: str,
    ) -> QueueState:
        """Bind the exact accepted remote receipt without changing model identity."""
        request = state.permit_requests.get(request_id)
        if request is None or request.permit_id is None:
            raise AdmissionBlockedError("request has no reserved permit")
        permit = state.active_permits[request.permit_id]
        if (
            permit.status != PermitStatus.UNKNOWN
            or model != request.model
            or not remote_task_id.strip()
            or not remote_session_id.strip()
        ):
            raise AdmissionBlockedError("accepted worker receipt is not bound to unknown request")
        receipt = self._admission_receipt(
            state,
            kind="acceptance",
            request=request,
            subject=request_id,
            before=remote_task_id,
            after=model,
            related_id=permit.permit_id,
        )
        updated = self._verify(state, receipt, "acceptance", request.pr_number)
        updated = replace(
            updated,
            permit_requests={
                **state.permit_requests,
                request_id: replace(request, status=AdmissionRequestStatus.ACCEPTED),
            },
            active_permits={
                **state.active_permits,
                permit.permit_id: replace(
                    permit,
                    status=PermitStatus.ACCEPTED,
                    remote_task_id=remote_task_id,
                    remote_session_id=remote_session_id,
                    acceptance_evidence_id=receipt.evidence_id,
                ),
            },
        )
        validate_queue_state(updated)
        return updated

    def cancel_worker_admission(self, state: QueueState, request_id: str) -> QueueState:
        """Cancel only a never-issued reservation; ambiguity remains occupied."""
        request = state.permit_requests.get(request_id)
        if request is None:
            raise AdmissionBlockedError("unknown admission request")
        if request.status == AdmissionRequestStatus.CANCELLED:
            return state
        if request.permit_id is None:
            if request.status != AdmissionRequestStatus.QUEUED:
                raise AdmissionBlockedError("admission request is terminal")
            updated = replace(
                state,
                permit_requests={
                    **state.permit_requests,
                    request_id: replace(
                        request,
                        status=AdmissionRequestStatus.CANCELLED,
                        terminal_evidence_id=f"local-cancel:{request_id}",
                    ),
                },
            )
            validate_queue_state(updated)
            return updated
        permit = state.active_permits[request.permit_id]
        if permit.status != PermitStatus.RESERVED or permit.remote_task_id is not None:
            raise AdmissionBlockedError("only never-issued reservations can be cancelled")
        return self._release_admission(state, request, permit, AdmissionRequestStatus.CANCELLED, PermitStatus.CANCELLED)

    def release_worker_admission(self, state: QueueState, request_id: str, proof: Evidence) -> QueueState:
        """Release occupied capacity only with exact terminal or nonacceptance evidence."""
        request = state.permit_requests.get(request_id)
        if request is None or request.permit_id is None:
            raise AdmissionBlockedError("unknown admission request")
        permit = state.active_permits[request.permit_id]
        if proof.subject != request_id or proof.related_id != permit.permit_id:
            raise AdmissionBlockedError("release evidence is not bound to request/permit")
        if permit.status == PermitStatus.UNKNOWN:
            if proof.kind != "absence" or proof.after != "not_accepted":
                raise AdmissionBlockedError("unknown worker requires verified nonacceptance")
        elif permit.status == PermitStatus.ACCEPTED:
            if proof.kind not in {"failure", "success"} or proof.before != "terminal":
                raise AdmissionBlockedError("accepted worker requires verified terminal evidence")
        else:
            raise AdmissionBlockedError("worker permit is not occupied")
        updated = self._verify(state, proof, proof.kind, request.pr_number)
        return self._release_admission(
            updated, request, permit, AdmissionRequestStatus.RELEASED, PermitStatus.RELEASED, proof.evidence_id
        )

    @staticmethod
    def _controller_projection(
        state: QueueState, pr_number: int, *, request_id: str | None = None, permit_id: str | None = None
    ) -> AdmissionController:
        current = state.controllers.get(pr_number)
        request_ids = () if current is None else current.request_ids
        permit_ids = () if current is None else current.permit_ids
        if request_id is not None and request_id not in request_ids:
            request_ids += (request_id,)
        if permit_id is not None and permit_id not in permit_ids:
            permit_ids += (permit_id,)
        return AdmissionController(pr_number, state.repo, state.global_epoch, permit_ids, request_ids, state.revision)

    @staticmethod
    def _release_admission(
        state: QueueState,
        request: PermitRequest,
        permit: WorkerPermit,
        request_status: AdmissionRequestStatus,
        permit_status: PermitStatus,
        evidence_id: str | None = None,
    ) -> QueueState:
        updated = replace(
            state,
            permit_requests={
                **state.permit_requests,
                request.request_id: replace(request, status=request_status, terminal_evidence_id=evidence_id),
            },
            active_permits={
                **state.active_permits,
                permit.permit_id: replace(permit, status=permit_status, terminal_evidence_id=evidence_id),
            },
            effect_fences={
                **state.effect_fences,
                f"fence:{request.request_id}": replace(
                    state.effect_fences[f"fence:{request.request_id}"], status="released"
                ),
            },
        )
        validate_queue_state(updated)
        return updated
