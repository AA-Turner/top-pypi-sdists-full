"""Guards action — evaluates all safety guards."""

from __future__ import annotations

from typing import Literal

from agentic_devtools.cli.ci.guards import (
    check_docker_files,
    check_exclusion_labels,
    check_fork_pr,
    check_privileged_paths,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState, get_latest_session_state
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.pipeline.title_utils import is_wip_title
from agentic_devtools.cli.ci.provider import CIPlatformProvider


class GuardsAction:
    """Evaluate safety and progression guards that gate the pipeline.

    Guards are fail-closed: any exception blocks the entire pipeline.
    """

    def __init__(self, phase: Literal["all", "safety", "progression"] = "all") -> None:
        if phase not in {"all", "safety", "progression"}:
            raise ValueError("phase must be 'all', 'safety', or 'progression'")
        self._phase = phase

    @property
    def name(self) -> str:
        return "safety_guards" if self._phase == "safety" else "guards"

    def evaluate(self, snapshot: PRStateSnapshot, derived: DerivedState) -> ActionResult:
        """Evaluate the selected guard phase. Returns BLOCKED if a guard fails."""
        preconditions: dict[str, bool] = {}

        if self._phase in {"all", "progression"}:
            # WIP title check — matches legacy orchestrator _is_wip_title() gate
            is_wip = is_wip_title(snapshot.title)
            session_state = derived.get("latest_session_state")
            if is_wip and not isinstance(session_state, SessionState):
                provider = derived.get("provider")
                if provider is not None:
                    session_state = get_latest_session_state(
                        provider,
                        snapshot.pr_number,
                        repo=snapshot.base_repo_full_name,
                        head_branch=snapshot.head_branch,
                        pr_id=snapshot.pr_id,
                        head_sha=snapshot.head_sha,
                    )
                    derived.set("latest_session_state", session_state)
            finished_wip_recovery = (
                is_wip
                and derived.is_draft
                and bool(snapshot.files)
                and isinstance(session_state, SessionState)
                and session_state.outcome is SessionOutcome.FINISHED
            )
            preconditions["not_wip"] = not is_wip or finished_wip_recovery
            if is_wip and not finished_wip_recovery:
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.BLOCKED,
                    preconditions=preconditions,
                    details="PR title is marked WIP",
                )

            # No-changes check — matches legacy orchestrator no_changes gate
            has_changes = bool(snapshot.files)
            preconditions["has_changes"] = has_changes
            if not has_changes:
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.BLOCKED,
                    preconditions=preconditions,
                    details="PR has no file changes",
                )

        if self._phase in {"all", "safety"}:
            # Fork check
            is_fork = check_fork_pr(snapshot.head_repo_full_name, snapshot.base_repo_full_name)
            preconditions["not_fork"] = not is_fork
            if is_fork:
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.BLOCKED,
                    preconditions=preconditions,
                    details="PR is from a fork",
                )

            # Exclusion labels
            should_skip, _flag = check_exclusion_labels(snapshot.labels)
            preconditions["no_exclusion_label"] = not should_skip
            if should_skip:
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.BLOCKED,
                    preconditions=preconditions,
                    details="PR has exclusion label",
                )

            # Privileged paths
            has_privileged = check_privileged_paths(snapshot.files)
            preconditions["no_privileged_paths"] = not has_privileged
            if has_privileged:
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.BLOCKED,
                    preconditions=preconditions,
                    details="PR touches privileged paths",
                )

            # Docker files
            has_docker = check_docker_files(snapshot.files)
            preconditions["no_docker_files"] = not has_docker
            if has_docker:
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.BLOCKED,
                    preconditions=preconditions,
                    details="PR touches Docker files",
                )

        # All guards passed
        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            preconditions=preconditions,
            details="All guards passed",
        )

    def execute(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
    ) -> ActionResult:
        """Guards have no execution — evaluation is the entire action."""
        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            details="All guards passed",
        )
