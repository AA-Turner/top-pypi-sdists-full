"""Bounded recovery consumer for independently admitted initial-delivery evidence."""

from __future__ import annotations

import hashlib
import re
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from agentic_devtools.cli.ci.guards import AGENT_RETRY_CONFIRMATION_WINDOW
from agentic_devtools.cli.ci.initial_delivery_claims import InitialDeliveryClaims
from agentic_devtools.cli.ci.models import AgentTaskInventoryAvailability
from agentic_devtools.cli.ci.pipeline.delivery import (
    InitialDeliveryEvidence,
    InitialDeliveryOutcome,
    classify_initial_delivery_with_head,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.session_detector import (
    SessionOutcome,
    SessionState,
    get_latest_session_state,
    is_copilot_session_active_via_agent_task,
)
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.pipeline.snapshot_utils import _raise_if_rate_limit
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.pipeline.actions.retry_failed_session import RetryFailedSessionAction


class InitialDeliveryRecovery:
    """Consume one original-delivery claim, never a terminal-event or per-SHA cap."""

    def __init__(self, action: RetryFailedSessionAction) -> None:
        self._action = action
        self._provider = action._provider

    def _result(self, decision: ActionDecision, details: str) -> ActionResult:
        return ActionResult(name=self._action.name, decision=decision, details=details)

    def evaluate_session(
        self, snapshot: PRStateSnapshot, derived: DerivedState, state: SessionState
    ) -> ActionResult | None:
        """Route terminal admission without changing the existing session guards."""
        if state.outcome is SessionOutcome.UNKNOWN:
            return ActionResult(
                name=self._action.name,
                decision=ActionDecision.BLOCKED,
                preconditions={"session_outcome_known": False},
                details="Latest Copilot session outcome is unknown",
            )
        if state.outcome is SessionOutcome.ACTIVE:
            return ActionResult(
                name=self._action.name,
                decision=ActionDecision.BLOCKED,
                preconditions={"session_active": True},
                details="Active Copilot session blocks retry and subsequent pipeline actions",
            )
        if snapshot.initial_delivery is not None:
            result = self.evaluate(snapshot, derived, state)
            if result is not None:
                return result
        if state.outcome is not SessionOutcome.FAILED:
            return ActionResult(
                name=self._action.name,
                decision=ActionDecision.SKIP,
                preconditions={"session_failed": False},
                details=f"Latest Copilot session outcome is {state.outcome.value}",
            )
        return None

    @staticmethod
    def _identity(evidence: object) -> str:
        if (
            not isinstance(evidence, InitialDeliveryEvidence)
            or not isinstance(evidence.outcome, InitialDeliveryOutcome)
            or not isinstance(evidence.initial_task_id, str)
            or re.fullmatch(r"[A-Za-z0-9_-]{1,200}", evidence.initial_task_id) is None
            or not isinstance(evidence.initial_plan_sha, str)
            or re.fullmatch(r"[0-9a-f]{40}", evidence.initial_plan_sha) is None
            or not isinstance(evidence.head_sha, str)
            or re.fullmatch(r"[0-9a-f]{40}", evidence.head_sha) is None
        ):
            return ""
        return hashlib.sha256(f"{evidence.initial_task_id}\n{evidence.initial_plan_sha}".encode()).hexdigest()

    def _observe(self, snapshot: PRStateSnapshot, state: SessionState) -> InitialDeliveryOutcome | None:
        evidence = snapshot.initial_delivery
        if (
            not self._identity(evidence)
            or evidence is None
            or evidence.head_sha != snapshot.head_sha
            or state.inventory_availability is not AgentTaskInventoryAvailability.COMPLETE
            or state.outcome not in {SessionOutcome.FINISHED, SessionOutcome.FAILED}
            or not isinstance(state.task_id, str)
            or not state.task_id
        ):
            return None
        live = self._provider.get_pr_metadata(snapshot.pr_number)
        if (
            live.head_sha != snapshot.head_sha
            or live.head_branch != snapshot.head_branch
            or live.head_repo_full_name != snapshot.head_repo_full_name
            or live.base_repo_full_name != snapshot.base_repo_full_name
            or live.labels != snapshot.labels
            or self._has_active_session(snapshot)
        ):
            return None
        observed_head, outcome = classify_initial_delivery_with_head(
            self._provider,
            snapshot.pr_number,
            completion_confirmed=state.outcome is SessionOutcome.FINISHED,
            initial_plan_sha=evidence.initial_plan_sha,
        )
        if observed_head and observed_head != snapshot.head_sha:
            return None
        if self._provider.get_pr_metadata(snapshot.pr_number) != live:
            return None
        return outcome

    def _has_active_session(self, snapshot: PRStateSnapshot) -> bool:
        """Invalidate cached lifecycle and writer inventories before every safety check."""
        self._provider.invalidate_agent_task_inventory(snapshot.pr_number)
        return (
            is_copilot_session_active_via_agent_task(
                snapshot.base_repo_full_name,
                snapshot.pr_number,
                provider=self._provider,
                head_branch=snapshot.head_branch,
                pr_id=snapshot.pr_id,
                head_sha=snapshot.head_sha,
            )
            is not False
        )

    @staticmethod
    def _matches_delivered_handoff(
        claim: object,
        evidence: InitialDeliveryEvidence,
    ) -> bool:
        """Match a persisted completed recovery to its exact source, task and head."""
        return (
            isinstance(claim, dict)
            and claim.get("initial_task_id") == evidence.initial_task_id
            and claim.get("initial_plan_sha") == evidence.initial_plan_sha
            and claim.get("head") == evidence.head_sha
            and isinstance(claim.get("task_id"), str)
            and re.fullmatch(r"[A-Za-z0-9_-]{1,200}", claim["task_id"]) is not None
        )

    @staticmethod
    def _delivered_receipt_key(key: str, evidence: InitialDeliveryEvidence, task_id: str | None = None) -> str:
        """Index immutable delivery receipts by admission, head, and optional task."""
        return hashlib.sha256("\n".join(filter(None, (key, evidence.head_sha, task_id))).encode()).hexdigest()

    def _record_delivered_handoff(
        self,
        store: InitialDeliveryClaims,
        snapshot: PRStateSnapshot,
        key: str,
        evidence: InitialDeliveryEvidence,
        task_id: str,
    ) -> bool:
        """Persist the exact verified task/head that completed initial-delivery recovery."""
        record = {
            "head": evidence.head_sha,
            "initial_task_id": evidence.initial_task_id,
            "initial_plan_sha": evidence.initial_plan_sha,
            "task_id": task_id,
        }
        receipt_key = self._delivered_receipt_key(key, evidence)
        if store.claim(snapshot.pr_number, receipt_key, "delivered", record):
            return True
        existing = store.read(snapshot.pr_number, receipt_key, "delivered")
        if (
            existing is None
            or not self._matches_delivered_handoff(existing, evidence)
            or existing.get("head") != snapshot.head_sha
        ):
            return False
        if existing.get("task_id") == task_id:
            return True
        task_receipt_key = self._delivered_receipt_key(key, evidence, task_id)
        if store.claim(snapshot.pr_number, task_receipt_key, "delivered", record):
            return True
        task_receipt = store.read(snapshot.pr_number, task_receipt_key, "delivered")
        return (
            task_receipt is not None
            and self._matches_delivered_handoff(task_receipt, evidence)
            and task_receipt.get("head") == snapshot.head_sha
            and task_receipt.get("task_id") == task_id
        )

    def _should_defer_failed_task(
        self,
        store: InitialDeliveryClaims,
        claim: dict | None,
        snapshot: PRStateSnapshot,
        key: str,
        state: SessionState,
    ) -> bool | None:
        """Route unrelated failures normally and fence tasks already recorded delivered."""
        if state.outcome is not SessionOutcome.FAILED:
            return False
        if claim is None:
            return True
        evidence = snapshot.initial_delivery
        if (
            not isinstance(state.task_id, str)
            or re.fullmatch(r"[A-Za-z0-9_-]{1,200}", state.task_id) is None
            or evidence is None
        ):
            return None
        receipt_key = self._delivered_receipt_key(key, evidence)
        delivered = store.read(snapshot.pr_number, receipt_key, "delivered")
        if (
            delivered is None
            or not self._matches_delivered_handoff(delivered, evidence)
            or delivered.get("head") != snapshot.head_sha
        ):
            return False
        if state.task_id == delivered.get("task_id"):
            return None
        task_receipt_key = self._delivered_receipt_key(key, evidence, state.task_id)
        task_receipt = store.read(snapshot.pr_number, task_receipt_key, "delivered")
        if (
            task_receipt is not None
            and self._matches_delivered_handoff(task_receipt, evidence)
            and task_receipt.get("head") == snapshot.head_sha
            and task_receipt.get("task_id") == state.task_id
        ):
            return None
        return True

    def _handle_unknown_failed_task(
        self,
        store: InitialDeliveryClaims,
        claim: dict | None,
        snapshot: PRStateSnapshot,
        key: str,
        state: SessionState,
        outcome: InitialDeliveryOutcome | None,
    ) -> tuple[bool, ActionResult | None]:
        defer = (
            self._should_defer_failed_task(store, claim, snapshot, key, state)
            if outcome is InitialDeliveryOutcome.UNKNOWN
            else False
        )
        return defer is not False, self._result(
            ActionDecision.BLOCKED, "A previously delivered task cannot re-enter recovery"
        ) if defer is None else None

    def _delivered_result(
        self,
        store: InitialDeliveryClaims,
        claim: dict | None,
        snapshot: PRStateSnapshot,
        key: str,
        evidence: InitialDeliveryEvidence | None,
        state: SessionState,
    ) -> ActionResult:
        """Persist claimed recovery completion before returning to normal pipeline gates."""
        if state.outcome is not SessionOutcome.FINISHED:
            return self._result(ActionDecision.BLOCKED, "Delivery requires a completed task")
        if claim is not None and (
            evidence is None
            or not isinstance(state.task_id, str)
            or re.fullmatch(r"[A-Za-z0-9_-]{1,200}", state.task_id) is None
            or not self._record_delivered_handoff(store, snapshot, key, evidence, state.task_id)
        ):
            return self._result(ActionDecision.BLOCKED, "Verified recovery handoff could not be persisted")
        return self._result(ActionDecision.SKIP, "Fresh complete non-empty delivery returns to normal PR gates")

    @staticmethod
    def _mode(claim: dict | None, state: SessionState, evidence: InitialDeliveryEvidence) -> str:
        if claim is None:
            return (
                "retry"
                if state.outcome is SessionOutcome.FINISHED and state.task_id == evidence.initial_task_id
                else "invalid"
            )
        if (
            state.task_id == evidence.initial_task_id
            and datetime.now(UTC) - datetime.fromisoformat(claim["created_at"]) < AGENT_RETRY_CONFIRMATION_WINDOW
        ):
            return "wait"
        return "escalate"

    def evaluate(self, snapshot: PRStateSnapshot, derived: DerivedState, state: SessionState) -> ActionResult | None:
        """Fail closed without admission; preserve ordinary true-FAILED handling."""
        try:
            key = self._identity(snapshot.initial_delivery)
            if not key:
                return self._result(ActionDecision.BLOCKED, "Initial-delivery admission is malformed")
            store = self._provider._get_initial_delivery_claims()
            claim = store.read(snapshot.pr_number, key, "recovery")
            evidence = snapshot.initial_delivery
            if claim is None and state.outcome is SessionOutcome.FAILED:
                return None
            outcome = self._observe(snapshot, state)
            if outcome is None or (outcome is InitialDeliveryOutcome.UNKNOWN and claim is None):
                return self._result(ActionDecision.BLOCKED, "Initial-delivery evidence is unknown, active or stale")
            handled, failed_task_result = self._handle_unknown_failed_task(store, claim, snapshot, key, state, outcome)
            if handled:
                return failed_task_result
            if outcome is InitialDeliveryOutcome.DELIVERED:
                return self._delivered_result(store, claim, snapshot, key, evidence, state)
            evidence = snapshot.initial_delivery
            assert evidence is not None
            if claim is None and evidence.outcome is not InitialDeliveryOutcome.NO_DELIVERY:
                return self._result(ActionDecision.BLOCKED, "Recovery requires typed NO_DELIVERY admission")
            mode = self._mode(claim, state, evidence)
            if mode in {"wait", "invalid"}:
                return self._result(
                    ActionDecision.BLOCKED, "Recovery claimed or original task identity changed; waiting"
                )
            derived.set("initial_delivery_mode", mode)
            derived.set("initial_delivery_key", key)
            derived.set("initial_delivery_session", state)
            return self._result(ActionDecision.EXECUTE, f"Initial-delivery recovery: {mode}")
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            return self._result(ActionDecision.BLOCKED, "Initial-delivery evidence or durable claims unavailable")

    def execute(self, provider: CIPlatformProvider, snapshot: PRStateSnapshot, derived: DerivedState) -> ActionResult:
        """Revalidate before each mutation; a lost response never releases a claim."""
        try:
            state = get_latest_session_state(
                provider,
                snapshot.pr_number,
                repo=snapshot.base_repo_full_name,
                head_branch=snapshot.head_branch,
                pr_id=snapshot.pr_id,
                head_sha=snapshot.head_sha,
            )
            outcome = self._observe(snapshot, state)
            if (
                state != derived.get("initial_delivery_session")
                or outcome is None
                or outcome is InitialDeliveryOutcome.DELIVERED
            ):
                return self._result(ActionDecision.BLOCKED, "Initial-delivery head, diff or lifecycle changed")
            if derived.get("initial_delivery_mode") == "escalate":
                return self._escalate(provider, snapshot, derived, "One-attempt recovery budget exhausted")
            if outcome is not InitialDeliveryOutcome.NO_DELIVERY:
                return self._result(ActionDecision.BLOCKED, "Initial-delivery classification became unknown")
            key = derived.get("initial_delivery_key")
            evidence = snapshot.initial_delivery
            assert evidence is not None
            # Build context before claiming so failures here cannot consume a dispatch.
            derived.set("agent_retry_task_id", evidence.initial_task_id)
            prompt = self._action._build_retry_prompt(snapshot, derived, key, 1, 1)
            prompt = prompt.replace("agdt:agent-retry:", "agdt:initial-delivery-retry:")
            prompt = prompt.replace(
                f"Copilot session {key} failed.",
                "The initial implementation completed with verified NO_DELIVERY.",
            )
            store = provider._get_initial_delivery_claims()
            if not store.claim(
                snapshot.pr_number,
                key,
                "recovery",
                {
                    "head": snapshot.head_sha,
                    "initial_task_id": evidence.initial_task_id,
                    "diff": "ZERO_DIFF",
                },
            ):
                return self._result(ActionDecision.BLOCKED, "Another worker already consumed the recovery claim")
            # Check again after the durable write, immediately before the non-idempotent call.
            latest = get_latest_session_state(
                provider,
                snapshot.pr_number,
                repo=snapshot.base_repo_full_name,
                head_branch=snapshot.head_branch,
                pr_id=snapshot.pr_id,
                head_sha=snapshot.head_sha,
            )
            if latest != state or self._observe(snapshot, latest) is not InitialDeliveryOutcome.NO_DELIVERY:
                return self._result(ActionDecision.BLOCKED, "Recovery claim retained; evidence changed before dispatch")
            try:
                receipt = provider._dispatch_agent_retry(snapshot.pr_number, prompt, key, initial_delivery=True)
            except Exception as exc:
                _raise_if_rate_limit(exc)
                return self._escalate(
                    provider, snapshot, derived, "Recovery dispatch failed or acceptance is uncertain"
                )
            if not isinstance(receipt, int) or isinstance(receipt, bool) or receipt <= 0:
                return self._escalate(provider, snapshot, derived, "Recovery dispatch acceptance is uncertain")
            return ActionResult(
                name=self._action.name,
                decision=ActionDecision.EXECUTE,
                preconditions={"retry_dispatched": True},
                details="Dispatched the single initial-delivery recovery",
            )
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            return self._result(
                ActionDecision.FAILED, "Recovery stopped; durable claim/evidence unavailable, no resend"
            )

    def validate_escalation(self, snapshot: PRStateSnapshot, derived: DerivedState) -> None:
        """Refuse initial-delivery notifications or exclusion after a lifecycle change."""
        if not self._escalation_is_safe(snapshot, derived):
            raise RuntimeError("Recovery lifecycle or delivery changed; escalation stopped without exclusion")

    def _escalation_is_safe(self, snapshot: PRStateSnapshot, derived: DerivedState) -> bool:
        """Return whether the current delivery and task lifecycle still allow escalation."""
        if not derived.get("initial_delivery_mode"):
            return True
        state = get_latest_session_state(
            self._provider,
            snapshot.pr_number,
            repo=snapshot.base_repo_full_name,
            head_branch=snapshot.head_branch,
            pr_id=snapshot.pr_id,
            head_sha=snapshot.head_sha,
        )
        outcome = self._observe(snapshot, state)
        return outcome is not None and outcome is not InitialDeliveryOutcome.DELIVERED

    def _escalate(
        self, provider: CIPlatformProvider, snapshot: PRStateSnapshot, derived: DerivedState, reason: str
    ) -> ActionResult:
        """Serialize notification attempts too; retain ambiguous notices for manual inspection."""
        evidence = snapshot.initial_delivery
        assert evidence is not None
        state = get_latest_session_state(
            provider,
            snapshot.pr_number,
            repo=snapshot.base_repo_full_name,
            head_branch=snapshot.head_branch,
            pr_id=snapshot.pr_id,
            head_sha=snapshot.head_sha,
        )
        outcome = self._observe(snapshot, state)
        if outcome is None or outcome is InitialDeliveryOutcome.DELIVERED:
            return self._result(ActionDecision.BLOCKED, "Recovery may be active; retain claim without escalation")
        key = derived.get("initial_delivery_key")
        comments = provider.list_issue_comments(snapshot.pr_number)
        login = provider.get_dispatch_login()
        if not isinstance(login, str) or not login:
            return self._result(ActionDecision.FAILED, "Escalation identity unavailable; recovery claim retained")
        diagnostics = evidence.push_diagnostics[:2000] if isinstance(evidence.push_diagnostics, str) else ""
        diagnostics = re.sub(r"@copilot", "Copilot", diagnostics, flags=re.IGNORECASE)
        diff = "ZERO_DIFF" if outcome is InitialDeliveryOutcome.NO_DELIVERY else "UNKNOWN"
        body = (
            f"{reason}. Original task: `{evidence.initial_task_id}`. "
            f"Observed head: `{snapshot.head_sha}`; diff: `{diff}`; "
            "initial-delivery recovery budget: one (consumed). "
            f"Push cause: {'available evidence below' if diagnostics else 'unknown'}.\n\n"
            f"{diagnostics}\n\n"
            "Inspect the original task and any local unpushed work, then recover manually. "
            "Removing `ai-pr-loop:agent-failed` does not reset this durable recovery budget."
        )
        # A prior generic failure notice does not contain this delivery's head/diff evidence.
        comments = [comment for comment in comments if key in self._action._escalation_identities([comment], login)]
        derived.set("agent_retry_comments", comments)
        derived.set("agent_retry_dispatch_login", login)
        derived.set(
            "initial_delivery_escalation_body",
            f"<!-- agdt:agent-retry-escalation:{key} -->\n\n{body}",
        )
        if not comments:
            if not self._escalation_is_safe(snapshot, derived):
                return self._result(ActionDecision.BLOCKED, "Recovery may be active; do not reserve escalation")
            claims = provider._get_initial_delivery_claims()
            owner_token = uuid4().hex
            if not claims._reserve_escalation(
                snapshot.pr_number,
                key,
                {"head": snapshot.head_sha, "diff": diff, "notice": body},
                owner_token,
            ):
                return self._result(
                    ActionDecision.FAILED,
                    "Escalation already attempted; inspect durable escalation evidence, no resend",
                )
            if not self._escalation_is_safe(snapshot, derived):
                if claims._transition_escalation(snapshot.pr_number, key, owner_token, "reserved", "retryable"):
                    return self._result(
                        ActionDecision.BLOCKED,
                        "Recovery became active before notice send; reservation released for safe retry",
                    )
                return self._result(
                    ActionDecision.FAILED,
                    "Pre-send abort could not verify escalation reservation ownership; no notice sent",
                )
            if not claims._transition_escalation(snapshot.pr_number, key, owner_token, "reserved", "attempted"):
                return self._result(
                    ActionDecision.FAILED,
                    "Escalation send attempt could not be durably fenced; no notice sent",
                )
        return self._action._escalate(provider, snapshot, derived, key)
