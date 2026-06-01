from __future__ import annotations
import time

from kanban_framework.types import Task, Phase
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.config import Config
from kanban_framework.infra.scheduler import Scheduler
from kanban_framework.domain.guard import Guard, CheckResult
from kanban_framework.domain.self_improve import IterationDecider, IterationAction


class TransitionError(Exception):
    pass


class WorkflowEngine:
    def __init__(self, fs: Filesystem, config: Config, guard: Guard | None = None):
        self._fs = fs
        self._cfg = config
        self._guard = guard

    def transition(self, task: Task, target) -> str:
        lw = task.lightweight
        quick = getattr(task, 'mode', '') == 'quick'
        ext_order = self._get_effective_order(lw, quick=quick)
        if ext_order is None:
            base = Scheduler.LIGHTWEIGHT_PHASE_ORDER if lw else Scheduler.PHASE_ORDER
            ext_order = [p.value if isinstance(p, Phase) else str(p) for p in base]
        current_str = task.phase_id
        target_str = target.value if isinstance(target, Phase) else str(target)
        try:
            current_idx = ext_order.index(current_str)
            target_idx = ext_order.index(target_str)
        except ValueError:
            # Custom phase: allow forward transition
            current_idx = ext_order.index(current_str) if current_str in ext_order else -1
            target_idx = ext_order.index(target_str) if target_str in ext_order else current_idx + 1
        if target_idx == current_idx:
            self._ensure_phase_completed(task)
            return target_str
        if target_idx < current_idx:
            raise TransitionError(
                f"Cannot transition backward from {current_str} to {target_str}"
            )
        # Lightweight allows skipping phases (plan → execute)
        if not lw and target_idx > current_idx + 1:
            raise TransitionError(
                f"Cannot skip phase: {current_str} -> {target_str}"
            )

        # Complete current phase before transitioning forward
        self._ensure_phase_completed(task)

        # Built-in guard check (IR-01: Guard 不可绕过)
        if self._guard:
            guard_result = self._guard.check_artifacts(task, task.phase, lightweight=lw)
            if not guard_result.passed:
                raise TransitionError(
                    f"Guard blocked transition {current_str} -> {target_str}: "
                    + "; ".join(guard_result.failures)
                )
            phase_check = self._guard.check_phase_completeness(task, lw)
            if not phase_check.passed:
                raise TransitionError(
                    f"Phase completeness check failed: "
                    + "; ".join(phase_check.failures)
                )

        # Set phase: use Phase enum for built-in, string for custom
        try:
            task.phase = Phase(target_str)
        except ValueError:
            task.phase = target_str
        task.history.append({
            "phase": target_str,
            "status": "started",
            "started_at": time.time(),
        })
        return target_str

    def complete_phase(self, task: Task) -> Task:
        self._ensure_phase_completed(task)
        quick = getattr(task, 'mode', '') == 'quick'
        ext_order = self._get_effective_order(task.lightweight, quick=quick)
        next_p = Scheduler.next_phase(task.phase, lightweight=task.lightweight, quick=quick,
                                      custom_order=ext_order)
        if next_p:
            try:
                task.phase = Phase(next_p.value if isinstance(next_p, Phase) else str(next_p))
            except ValueError:
                task.phase = str(next_p)
        return task

    def _ensure_phase_completed(self, task: Task) -> None:
        """Add a 'completed' entry for current phase if one doesn't exist."""
        phase_str = task.phase_id
        for h in task.history:
            if h.get("phase") == phase_str and h.get("status") == "completed":
                return
        task.history.append({
            "phase": phase_str,
            "status": "completed",
            "completed_at": time.time(),
            "iteration": task.iteration,
        })

    def record_phase_handoff(
        self, task: Task, summary: str = "", metadata: dict | None = None
    ) -> dict:
        """Record structured handoff for the current phase.

        Returns the handoff dict for storage alongside phase completion.
        Call this after complete_phase() to persist structured context for
        downstream phases and retry attempts.
        """
        entry = {
            "phase": task.phase.value,
            "iteration": task.iteration,
            "completed_at": time.time(),
            "summary": summary,
            "metadata": metadata or {},
        }
        task.history.append(entry)
        return entry

    def next_phase(self, phase, lightweight: bool = False, quick: bool = False) -> str | None:
        ext_order = self._get_effective_order(lightweight, quick=quick)
        result = Scheduler.next_phase(phase, lightweight=lightweight, quick=quick,
                                      custom_order=ext_order)
        if result is None:
            return None
        return result.value if isinstance(result, Phase) else str(result)

    def _get_effective_order(self, lightweight: bool, quick: bool = False) -> list[str] | None:
        """Build effective phase order from workflow.json extensions."""
        if self._cfg is None:
            return None
        wf = self._cfg.workflow
        ext_data = wf.get("extensions")
        if not ext_data:
            return None
        from kanban_framework.domain.workflow_extensions import WorkflowExtension
        ext = WorkflowExtension(wf)
        if ext.validate():
            return None
        base_order = Scheduler.dispatch_order(lightweight=lightweight, quick=quick)
        str_order = [p.value if isinstance(p, Phase) else str(p) for p in base_order]
        return ext.build_phase_order(str_order)

    def is_terminal(self, phase) -> bool:
        phase_str = phase.value if isinstance(phase, Phase) else str(phase)
        return phase_str == Phase.ARCHIVE.value

    def self_improve_check(self, task: Task, avg_score: float) -> dict:
        # Use evaluate pass_threshold from workflow.json, fall back to config
        threshold = self._cfg.pass_threshold
        workflow = self._cfg.workflow
        for p in workflow.get("phases", []):
            if p.get("id") == "evaluate":
                threshold = p.get("pass_threshold", threshold)
                break
        action = IterationDecider.decide(
            avg_score,
            task.iteration,
            self._cfg.max_iterations,
            threshold,
        )
        return {"action": action.value, "reason": f"IterationAction.{action.name}",
                "pass_threshold": threshold, "avg_score": avg_score}

    def quality_gate_check(
        self,
        task: Task,
        score: float,
        gate_phase: Phase,
        round_num: int,
    ) -> dict:
        """Check quality gate result for plan_review or spec_review phases.

        Returns decision dict with action and whether to proceed, retry, or abort.
        """
        workflow = self._cfg.workflow
        phase_config = None
        for p in workflow.get("phases", []):
            if p.get("id") == gate_phase.value:
                phase_config = p
                break

        pass_threshold = 7.0
        max_rounds = 3
        if phase_config:
            pass_threshold = phase_config.get("pass_threshold", 7.0)
            max_rounds = phase_config.get("max_rounds", 3)

        action = IterationDecider.decide_quality_gate(
            score, round_num, max_rounds, pass_threshold
        )

        result = {
            "action": action.value,
            "score": score,
            "threshold": pass_threshold,
            "round": round_num,
            "max_rounds": max_rounds,
        }

        if action == IterationAction.PASS:
            result["next_phase"] = self.next_phase(gate_phase).value if self.next_phase(gate_phase) else None
        elif action == IterationAction.RETRY_PREV:
            # Go back to the phase before the gate
            try:
                idx = Scheduler.PHASE_ORDER.index(gate_phase)
                result["retry_phase"] = Scheduler.PHASE_ORDER[idx - 1].value
            except (ValueError, IndexError):
                result["retry_phase"] = Phase.PLAN.value
        elif action == IterationAction.MAX_ITER:
            result["next_phase"] = Phase.USER_DECISION.value

        return result

    def previous_phase(self, phase) -> str | None:
        ext_order = self._get_effective_order(False)
        base = Scheduler.dispatch_order()
        order = ext_order if ext_order is not None else [p.value if isinstance(p, Phase) else str(p) for p in base]
        phase_str = phase.value if isinstance(phase, Phase) else str(phase)
        try:
            idx = order.index(phase_str)
            if idx > 0:
                return order[idx - 1]
        except ValueError:
            pass
        return None
