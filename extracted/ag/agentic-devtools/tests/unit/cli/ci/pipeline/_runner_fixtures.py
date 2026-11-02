"""Reusable action doubles and persisted runner evidence."""

import base64
import json
import zlib

from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult


class _MockAction:
    """A mock action for testing the runner."""

    def __init__(
        self,
        name: str,
        eval_decision: ActionDecision,
        exec_decision: ActionDecision | None = None,
        definitive_no_mutation: bool = False,
        may_invalidate_snapshot: bool = False,
    ):
        self._name = name
        self._eval_decision = eval_decision
        self._exec_decision = exec_decision
        self._definitive_no_mutation = definitive_no_mutation
        self.may_invalidate_snapshot = may_invalidate_snapshot

    @property
    def name(self) -> str:
        return self._name

    def evaluate(self, snapshot, derived) -> ActionResult:
        return ActionResult(name=self._name, decision=self._eval_decision, details=f"eval_{self._name}")

    def execute(self, provider, snapshot, derived) -> ActionResult:
        decision = self._exec_decision or ActionDecision.EXECUTE
        return ActionResult(
            name=self._name,
            decision=decision,
            details=f"exec_{self._name}",
            definitive_no_mutation=self._definitive_no_mutation,
        )


def _diff_preservation_blocker_comment(payload: dict[str, object]) -> str:
    payload = {"allowed_removed_files": [], "baseline_base_sha": "", **payload}
    encoded = base64.urlsafe_b64encode(
        zlib.compress(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode(), level=9)
    ).decode()
    return f"<!-- agdt:diff-preservation-blocker:{encoded.rstrip('=')} -->"
