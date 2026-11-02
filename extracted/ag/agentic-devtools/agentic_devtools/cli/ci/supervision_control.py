"""Fail-closed domain operations for the mutation-capable AI PR Loop supervisor."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass

from agentic_devtools.cli.ci.comment_format import normalize_ai_pr_loop_comment

CONTROL_MARKER = "<!-- ai-pr-loop-supervision:control:v1 -->"
IGNORE_LABEL = "ai-pr-loop-ignore"
SUPERVISED_LABEL = "ai-pr-loop-supervised"


class ControlError(ValueError):
    """Raised when a supervision mutation cannot be proven safe."""


@dataclass(frozen=True)
class PRObservation:
    """Current provider facts required for a guarded PR mutation."""

    number: int
    head_sha: str
    labels: frozenset[str]

    def __post_init__(self) -> None:
        if self.number <= 0 or not self.head_sha:
            raise ValueError("PR observation requires a positive number and head SHA")


@dataclass(frozen=True)
class QuarantineReceipt:
    """Receipt describing exactly which PR heads received quarantine labels.

    ``ignore_added`` records only the PR numbers where this run newly applied
    ``IGNORE_LABEL`` (it was absent from the observed labels at quarantine
    time). It is the sole authorization ``restore_prs`` uses to decide which
    PRs may have their ignore label removed, so a pre-existing/user-owned
    ignore label -- or a fully idempotent quarantine that changed nothing --
    can never be stripped by a later restore.
    """

    run_id: str
    changed: tuple[int, ...]
    heads: Mapping[int, str]
    ignore_added: tuple[int, ...] = ()


@dataclass(frozen=True)
class QuarantineResult:
    """Deterministic label projection for a guarded quarantine operation."""

    idempotency_key: str
    changed: tuple[int, ...]
    labels: Mapping[int, frozenset[str]]
    receipt: QuarantineReceipt


@dataclass(frozen=True)
class HoldReceipt:
    """Exact workflow state required to restore a verified global hold."""

    run_id: str
    changed_workflows: tuple[str, ...]
    previous_states: Mapping[str, bool]


@dataclass(frozen=True)
class HoldResult:
    """Deterministic hold projection paired with its durable idempotency key."""

    idempotency_key: str
    receipt: HoldReceipt


@dataclass(frozen=True)
class Checkpoint:
    """Compact durable run record encoded in the control issue comment."""

    run_id: str
    payload: Mapping[str, object]
    repository: str


class SupervisionControl:
    """Perform pure, provider-independent checks before mutation leaves run."""

    def quarantine(
        self,
        observations: tuple[PRObservation, ...] | list[PRObservation],
        expected_heads: Mapping[int, str],
        *,
        run_id: str,
    ) -> QuarantineResult | None:
        """Return a guarded label projection, or ``None`` when it is already applied."""
        if not run_id.strip():
            raise ControlError("run_id is required")
        if not observations:
            raise ControlError("at least one PR is required")
        changed: list[int] = []
        ignore_added: list[int] = []
        labels: dict[int, frozenset[str]] = {}
        heads: dict[int, str] = {}
        for observation in observations:
            expected = expected_heads.get(observation.number)
            if expected is None or expected != observation.head_sha:
                raise ControlError(f"stale head for PR #{observation.number}")
            projected = observation.labels | {IGNORE_LABEL, SUPERVISED_LABEL}
            labels[observation.number] = frozenset(projected)
            heads[observation.number] = observation.head_sha
            if projected != observation.labels:
                changed.append(observation.number)
            if IGNORE_LABEL not in observation.labels:
                ignore_added.append(observation.number)
        if not changed:
            return None
        changed_tuple = tuple(sorted(changed))
        receipt = QuarantineReceipt(run_id, changed_tuple, heads, tuple(sorted(ignore_added)))
        expected_json = json.dumps(sorted(expected_heads.items()), separators=(",", ":"))
        return QuarantineResult(
            f"{run_id}:quarantine:{hashlib.sha256(expected_json.encode()).hexdigest()}",
            changed_tuple,
            labels,
            receipt,
        )

    def restore_prs(
        self,
        observations: tuple[PRObservation, ...] | list[PRObservation],
        receipt: QuarantineReceipt,
    ) -> QuarantineResult:
        """Remove only ignore labels this run added, per the matching quarantine receipt.

        A receipt with an empty ``ignore_added`` never added ``IGNORE_LABEL`` to
        any PR -- either because quarantine was already fully applied
        (idempotent) or because every PR it touched already carried the ignore
        label beforehand. In both cases restoring must be a no-op: it must
        never strip a pre-existing/user-owned ignore label.
        """
        if not receipt.run_id.strip():
            raise ControlError("checkpoint receipt is missing its run ID")
        if not receipt.ignore_added:
            observed_heads = {observation.number: observation.head_sha for observation in observations}
            if any(observed_heads.get(number) != head for number, head in receipt.heads.items()):
                raise ControlError("stale or missing head in no-op restore receipt")
            return QuarantineResult(f"{receipt.run_id}:restore:noop", (), {}, receipt)
        owned = frozenset(receipt.ignore_added)
        changed: list[int] = []
        labels: dict[int, frozenset[str]] = {}
        for observation in observations:
            if observation.number not in owned:
                continue
            expected = receipt.heads.get(observation.number)
            if expected is None:
                continue
            if expected != observation.head_sha:
                raise ControlError(f"stale head for PR #{observation.number}")
            if IGNORE_LABEL in observation.labels:
                changed.append(observation.number)
            labels[observation.number] = frozenset(observation.labels - {IGNORE_LABEL})
        if not labels:
            raise ControlError("checkpoint does not own any observed PR")
        missing_owned = owned - labels.keys()
        if missing_owned:
            raise ControlError(f"checkpoint is missing owned PR observations: {sorted(missing_owned)}")
        changed_tuple = tuple(sorted(changed))
        return QuarantineResult(
            f"{receipt.run_id}:restore:{','.join(str(number) for number in changed_tuple)}",
            changed_tuple,
            labels,
            receipt,
        )

    def hold(self, workflow_states: Mapping[str, bool], *, run_id: str) -> HoldResult | None:
        """Create a receipt for disabling currently enabled loop workflows.

        Returns ``None`` when every observed workflow is already disabled, so the
        caller can treat the operation as idempotent and skip the mutation.
        """
        if not run_id.strip() or not workflow_states:
            raise ControlError("run_id and workflow states are required")
        if any(not isinstance(name, str) or not name.strip() for name in workflow_states):
            raise ControlError("workflow names must be non-empty strings")
        if any(type(enabled) is not bool for enabled in workflow_states.values()):
            raise ControlError("workflow states must be boolean")
        changed = tuple(sorted(name for name, enabled in workflow_states.items() if enabled))
        if not changed:
            return None
        receipt = HoldReceipt(run_id, changed, dict(workflow_states))
        return HoldResult(f"{run_id}:hold", receipt)

    def resume(self, current_states: Mapping[str, bool], receipt: HoldReceipt) -> dict[str, bool]:
        """Restore the receipt, allowing retries after partial restoration."""
        if not receipt.run_id.strip():
            raise ControlError("hold receipt is missing its run ID")
        expected_changed = tuple(sorted(name for name, enabled in receipt.previous_states.items() if enabled))
        if receipt.changed_workflows != expected_changed:
            raise ControlError("hold receipt changed workflows do not match previous states")
        for workflow, was_enabled in receipt.previous_states.items():
            current = current_states.get(workflow)
            if type(current) is not bool or (not was_enabled and current):
                raise ControlError(f"workflow state mismatch for {workflow}")
        return dict(receipt.previous_states)

    def encode_checkpoint(self, checkpoint: Checkpoint) -> str:
        """Serialize a checkpoint with a stable fingerprint and control marker."""
        if not checkpoint.run_id.strip() or not checkpoint.repository.strip():
            raise ControlError("checkpoint requires run ID and repository")
        body = {
            "run_id": checkpoint.run_id,
            "repository": checkpoint.repository,
            "payload": checkpoint.payload,
        }
        canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
        body["evidence_fingerprint"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return f"{CONTROL_MARKER}\n{json.dumps(body, sort_keys=True, separators=(',', ':'))}"

    def decode_checkpoint(self, text: str) -> Checkpoint:
        """Read and validate one control checkpoint comment."""
        normalized_text = normalize_ai_pr_loop_comment(text)
        if normalized_text is None:
            raise ControlError("checkpoint terminal label is malformed")
        if not normalized_text.startswith(f"{CONTROL_MARKER}\n"):
            raise ControlError("checkpoint marker is missing")
        try:
            body = json.loads(normalized_text.split("\n", 1)[1])
        except (json.JSONDecodeError, IndexError) as exc:
            raise ControlError("checkpoint JSON is invalid") from exc
        if not isinstance(body, dict) or not isinstance(body.get("payload"), dict):
            raise ControlError("checkpoint payload is invalid")
        run_id = body.get("run_id")
        repository = body.get("repository")
        fingerprint = body.get("evidence_fingerprint")
        if not all(isinstance(value, str) and value for value in (run_id, repository, fingerprint)):
            raise ControlError("checkpoint identity is incomplete")
        assert isinstance(run_id, str)
        assert isinstance(repository, str)
        assert isinstance(fingerprint, str)
        unsigned = {"run_id": run_id, "repository": repository, "payload": body["payload"]}
        expected = hashlib.sha256(json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        if fingerprint != expected:
            raise ControlError("checkpoint fingerprint mismatch")
        return Checkpoint(run_id, body["payload"], repository)
