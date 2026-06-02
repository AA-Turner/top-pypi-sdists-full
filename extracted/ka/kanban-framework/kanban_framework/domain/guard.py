"""Guard — quality gate checks for kanban task phases.

Public API: Guard class with check_* methods. Internal checks are delegated
to guard_checks.GuardChecks and guard_reviews.GuardReviews.
"""
from __future__ import annotations

import json
from pathlib import Path
from dataclasses import dataclass, field

from kanban_framework.types import Task, Phase
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.config import Config
from kanban_framework.infra.scheduler import Scheduler


@dataclass
class CheckResult:
    passed: bool
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @staticmethod
    def combine(results: list[CheckResult]) -> CheckResult:
        all_failures: list[str] = []
        all_warnings: list[str] = []
        for r in results:
            all_failures.extend(r.failures)
            all_warnings.extend(r.warnings)
        return CheckResult(
            passed=len(all_failures) == 0,
            failures=all_failures,
            warnings=all_warnings,
        )


def _first_score(data: dict) -> float | int | None:
    """Extract score from report dict, trying all known key names.

    Uses ``is not None`` instead of truthiness so 0.0 is accepted (#356).
    """
    for key in ("score", "total", "total_score", "overall", "overall_score", "average"):
        v = data.get(key)
        if v is not None:
            try:
                return float(v)
            except (ValueError, TypeError):
                continue
    return None


def _first_history_score(entry: dict) -> float | int | None:
    """Extract score from score_history entry (#356).

    Uses ``is not None`` so 0.0 is not treated as falsy.
    """
    for key in ("average", "overall", "score"):
        v = entry.get(key)
        if v is not None:
            try:
                return float(v)
            except (ValueError, TypeError):
                continue
    return None


def _auto_collect_scores(fs: Filesystem, task_id: str, iteration: int) -> dict | None:
    """Auto-collect evaluation scores from review report files.

    Searches iteration dir for *_report.json files and averages their scores.
    """
    import json
    report_dir = fs.report_dir(task_id, iteration)
    if not report_dir.exists():
        return None

    score_entries: list[float] = []
    search_dirs = [report_dir / "reviews", report_dir]

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        for report_file in sorted(search_dir.glob("*_report.json")):
            try:
                data = json.loads(report_file.read_text(encoding="utf-8"))
                total = _first_score(data)
                if total is not None:
                    score_entries.append(float(total))
            except (ValueError, OSError, TypeError):
                continue

    if not score_entries:
        return None

    avg = sum(score_entries) / len(score_entries)
    return {"iteration": iteration, "average": round(avg, 2)}


class Guard:
    def __init__(self, fs: Filesystem, config: Config):
        self._fs = fs
        self._cfg = config
        from kanban_framework.domain.guard_checks import GuardChecks
        from kanban_framework.domain.guard_reviews import GuardReviews
        self._checks = GuardChecks(fs, config)
        self._reviews = GuardReviews(fs, config)

    # Hardcoded fallback when workflow.json lacks required_artifacts
    _DEFAULT_ARTIFACTS: dict[str, list[str]] = {
        "plan": ["spec.md", "task_breakdown.json", "plan/index.md", "plan/knowledge_used.json"],
        "plan_review": ["plan_review_report.json"],
        "qa_spec": ["test_spec.md"],
        "spec_review": ["spec_review_report.json"],
        "execute": ["execution_summary.md", "execution_pitfalls.md", "execution_decisions.md"],
        "retrospective": ["retrospective.md", "acceptance.md"],
    }

    # Hardcoded checks per phase — fallback when workflow.json lacks guard.checks
    _HARDCODED_CHECKS: dict[str, list[str]] = {
        "plan": ["knowledge_references"],
        "execute": ["test_files", "tdd_evidence", "test_spec_coverage", "knowledge_artifact"],
        "retrospective": ["knowledge_artifact"],
    }

    def _get_phase_guard(self, phase_str: str, mode: str | None = None) -> dict:
        """Read guard config for a phase.

        Priority: modes.<mode>.phases[].guard → .kanban/workflows/<mode>.json
        → top-level phases[].guard → {}
        """
        workflow = self._cfg.workflow
        # Priority 1: per-mode guard from workflow.json
        if mode:
            modes_cfg = workflow.get("modes", {})
            mode_cfg = modes_cfg.get(mode, {}) if isinstance(modes_cfg, dict) else {}
            mode_phases = mode_cfg.get("phases", []) if isinstance(mode_cfg, dict) else []
            for p in mode_phases:
                if isinstance(p, dict) and p.get("id") == phase_str:
                    g = p.get("guard")
                    if isinstance(g, dict):
                        return g
        # Priority 2: per-mode guard from .kanban/workflows/<mode>.json
        if mode:
            try:
                wf_file = self._fs.kanban_dir / "workflows" / f"{mode}.json"
                if wf_file.is_file():
                    mode_data = json.loads(wf_file.read_text(encoding="utf-8"))
                    for p in mode_data.get("phases", []):
                        if isinstance(p, dict) and p.get("id") == phase_str:
                            g = p.get("guard")
                            if isinstance(g, dict):
                                return g
            except Exception:
                pass
        # Priority 3: top-level phases[].guard
        for p in workflow.get("phases", []):
            if isinstance(p, dict) and p.get("id") == phase_str:
                g = p.get("guard")
                if isinstance(g, dict):
                    return g
        return {}

    def _get_phase_checks(self, phase_str: str, mode: str | None = None) -> list[str]:
        """Read guard checks list from workflow.json; fall back to hardcoded."""
        guard_cfg = self._get_phase_guard(phase_str, mode)
        if "checks" in guard_cfg:
            return guard_cfg["checks"]
        return self._HARDCODED_CHECKS.get(phase_str, [])

    def _get_required_artifacts(self, phase, lightweight: bool = False) -> list[str]:
        """Read required_artifacts from workflow.json; fall back to hardcoded defaults."""
        phase_str = phase.value if isinstance(phase, Phase) else str(phase)
        workflow = self._cfg.workflow
        phases = workflow.get("phases", [])
        if not isinstance(phases, list):
            phases = []
        for p in phases:
            if isinstance(p, dict) and p.get("id") == phase_str:
                artifacts = p.get("required_artifacts")
                if artifacts:
                    return self._lightweight_reduce(phase_str, artifacts, lightweight)
        # Check workflow extensions for custom phase artifacts
        from kanban_framework.domain.workflow_extensions import WorkflowExtension
        ext = WorkflowExtension(workflow)
        custom_artifacts = ext.get_required_artifacts(phase_str)
        if custom_artifacts:
            return self._lightweight_reduce(phase_str, custom_artifacts, lightweight)
        if lightweight and phase_str == Phase.EXECUTE.value:
            return ["execution_summary.md"]
        return self._DEFAULT_ARTIFACTS.get(phase_str, [])

    @staticmethod
    def _lightweight_reduce(phase_str: str, artifacts: list[str], lightweight: bool) -> list[str]:
        """Reduce artifact requirements for lightweight/quick mode execute phase."""
        if lightweight and phase_str == Phase.EXECUTE.value:
            return [a for a in artifacts if a == "execution_summary.md"] or ["execution_summary.md"]
        return artifacts

    _KNOWLEDGE_ARTIFACT_HINTS: dict[str, tuple[str, str]] = {
        "execute":        ("execution_pitfalls.md",
                           "Execute phase should produce at least one pitfall note. "
                           "Write execution_pitfalls.md or use kanban knowledge add."),
        "retrospective":  ("knowledge_extracted.json",
                           "Retrospective phase should produce knowledge_extracted.json. "
                           "Run kanban knowledge extract."),
    }

    def _dispatch_check(self, name: str, task: Task, phase_str: str) -> CheckResult | None:
        """Run a single named check; returns None for unknown / no-op names."""
        if name == "knowledge_references":
            return self._checks.check_knowledge_references(task)
        if name == "test_files":
            return self._checks.check_test_files(task)
        if name == "tdd_evidence":
            return self._checks.check_tdd_evidence(task)
        if name == "test_spec_coverage":
            return self._checks.check_test_spec_coverage(task)
        if name == "knowledge_artifact":
            fname, hint = self._KNOWLEDGE_ARTIFACT_HINTS.get(
                phase_str, ("knowledge_artifact.json", "Knowledge artifact expected."))
            return self._checks.check_knowledge_artifact(task, fname, hint)
        if name == "quick_scope":
            if getattr(task, 'mode', '') == 'quick':
                return self._checks.check_quick_scope(task)
            return None
        if name == "evaluation_reports":
            return self.check_evaluation(task, task.iteration)
        if name == "evaluation_score":
            return self.check_evaluation_score(task)
        return None

    def check_artifacts(self, task: Task, phase: Phase, lightweight: bool = False) -> CheckResult:
        if task.status.value == "draft":
            return CheckResult(passed=True)
        # Evaluate phase: only check evaluation reports (acceptance.md checked in retrospective)
        if phase == Phase.EVALUATE:
            return self.check_evaluation(task, task.iteration, lightweight=lightweight)

        required = self._get_required_artifacts(phase, lightweight=lightweight)
        if not required:
            return CheckResult(passed=True)

        phase_str = phase.value if isinstance(phase, Phase) else str(phase)
        results = [self._checks.check_file(task, filename) for filename in required]
        for name in self._get_phase_checks(phase_str, getattr(task, 'mode', None)):
            r = self._dispatch_check(name, task, phase_str)
            if r:
                results.append(r)
        combined = CheckResult.combine(results)

        if phase_str == "execute" and task.worktree_path is None:
            # Check if project is a git repo at all (#210)
            is_git_repo = (self._fs._root / ".git").is_dir()
            if not is_git_repo:
                combined.warnings.append(
                    "project is not a git repo — git checkpoint skipped. "
                    "Run `git init && git add -A && git commit -m 'init'` to enable version control."
                )
            elif not self._cfg.worktree_enabled:
                combined.warnings.append("worktree not set (disabled by config)")
            elif task.lightweight:
                combined.warnings.append("worktree not set (lightweight mode)")
            else:
                combined.failures.append(
                    "worktree not set — config has worktree.enabled=true "
                    "but no worktree was created for this task."
                )

        return combined

    def check_step(self, task: Task, step: dict) -> CheckResult:
        """Run guard checks defined on a checkpoint step.

        Reads guard.checks and guard.required_artifacts from the step dict.
        Returns passed=True for non-checkpoint steps.
        """
        guard_cfg = step.get("guard")
        if not guard_cfg or step.get("type") != "checkpoint":
            return CheckResult(passed=True)
        results = []
        artifacts = guard_cfg.get("required_artifacts", [])
        for filename in artifacts:
            results.append(self._checks.check_file(task, filename))
        check_names = guard_cfg.get("checks", [])
        phase_str = step.get("phase", "")
        for name in check_names:
            r = self._dispatch_check(name, task, phase_str)
            if r:
                results.append(r)
        return CheckResult.combine(results)

    def check_evaluation(self, task: Task, iteration: int, lightweight: bool = False) -> CheckResult:
        missing = []
        report_dir = self._fs.report_dir(task.id, iteration)
        task_dir = self._fs.task_dir(task.id)
        for role_def in Scheduler.eval_roles(lightweight=lightweight):
            role = role_def["name"]
            filename = f"{role}_report.json"
            # Search all known evaluate report locations
            search_paths = [
                report_dir / "reviews" / filename,
                report_dir / filename,
                report_dir / "evaluate" / filename,
                task_dir / "reviews" / filename,
                task_dir / "evaluate" / filename,
                task_dir / filename,
            ]
            found = any(self._fs.file_exists(p) for p in search_paths)
            if not found:
                missing.append(filename)

        if missing:
            return CheckResult(passed=False, failures=[f"missing {r} report" for r in missing])
        return CheckResult(passed=True)

    def check_plan_quality(self, task: Task, report_dir: Path) -> CheckResult:
        return self._reviews.check_plan_quality(task, report_dir)

    def check_spec(self, task: Task, report_dir: Path) -> CheckResult:
        return self._reviews.check_spec(task, report_dir)

    def check_parallel_conflicts(self, task: Task) -> CheckResult:
        return self._reviews.check_parallel_conflicts(task)

    def check_cross_task_conflicts(self) -> CheckResult:
        return self._reviews.check_cross_task_conflicts()

    def check_phase_completeness(self, task: Task, lightweight: bool = False) -> CheckResult:
        """Verify no phases were skipped in the task's history."""
        from kanban_framework.infra.scheduler import Scheduler
        if getattr(task, 'mode', '') == 'quick':
            order = Scheduler.QUICK_PHASE_ORDER
        elif lightweight:
            order = Scheduler.LIGHTWEIGHT_PHASE_ORDER
        else:
            order = Scheduler.PHASE_ORDER
        completed_phases = {
            h["phase"] for h in task.history
            if h.get("status") == "completed"
        }
        missing = []
        for p in order:
            if p == task.phase:
                break
            if p.value not in completed_phases:
                missing.append(p.value)

        if missing:
            return CheckResult(
                passed=False,
                failures=[f"skipped phases: {', '.join(missing)}"],
            )
        return CheckResult(passed=True)

    def check_brainstorming(self, task: Task) -> CheckResult:
        """IR-16: Verify brainstorming was completed — spec.md must exist and be non-empty."""
        spec_file = self._fs.task_dir(task.id) / "spec.md"
        if not self._fs.file_exists(spec_file):
            return CheckResult(
                passed=False,
                failures=["spec.md missing — Plan Step A (superpowers:brainstorming) must be completed before plan_review"],
            )
        if spec_file.stat().st_size == 0:
            return CheckResult(
                passed=False,
                failures=["spec.md is empty — brainstorming must produce a non-empty spec document"],
            )
        return CheckResult(passed=True)

    def check_retrospective(self, task: Task) -> CheckResult:
        retro_file = self._fs.task_dir(task.id) / "retrospective.md"
        accept_file = self._fs.task_dir(task.id) / "acceptance.md"

        failures = []
        if not self._fs.file_exists(retro_file):
            failures.append("retrospective.md missing")
        elif retro_file.stat().st_size == 0:
            failures.append("retrospective.md is empty")

        if not self._fs.file_exists(accept_file):
            failures.append("acceptance.md missing")
        elif accept_file.stat().st_size == 0:
            failures.append("acceptance.md is empty")

        return CheckResult(passed=len(failures) == 0, failures=failures)

    def check_evaluation_score(self, task: Task) -> CheckResult:
        """Check if evaluation score meets pass_threshold.

        Uses IterationDecider to determine action:
        - PASS → passed=True
        - MAX_ITER → passed=True (forced user_decision per IR-17)
        - HOT/FULL → passed=False with iteration suggestion
        """
        from kanban_framework.domain.self_improve import IterationDecider

        if not task.score_history:
            # Auto-collect scores from review reports (fix #210)
            entry = _auto_collect_scores(self._fs, task.id, task.iteration)
            if entry:
                task.score_history.append(entry)
            else:
                return CheckResult(passed=False, failures=["no score_history recorded"])

        entry = task.score_history[-1]
        # Support multiple key names (#181): average, overall, score
        avg_score = _first_history_score(entry)
        if avg_score is None:
            return CheckResult(passed=False, failures=[
                f"score_history entry missing score key (tried 'average'/'overall'/'score'), "
                f"got keys: {sorted(entry.keys())}"
            ])
        pass_threshold = self._cfg.pass_threshold
        max_iterations = self._cfg.max_iterations

        action = IterationDecider.decide(
            avg_score, task.iteration, max_iterations, pass_threshold
        )

        if action.value in ("user_decision", "max_iterations", "retrospective"):
            warnings = []
            if action.value == "max_iterations":
                warnings.append(
                    f"max iterations ({max_iterations}) reached, forcing user_decision"
                )
            return CheckResult(passed=True, warnings=warnings)

        return CheckResult(
            passed=False,
            failures=[
                f"score {avg_score} < threshold {pass_threshold}, "
                f"auto-iteration required: {action.value}"
            ],
        )

    def batch_check(
        self, task: Task, report_dir: Path
    ) -> dict[str, CheckResult]:
        """Run multiple independent guard checks and return results by name.

        Each check runs independently -- one failure does not block others.
        """
        return {
            "check_artifacts": self.check_artifacts(task, task.phase, lightweight=task.lightweight),
            "check_plan_quality": self.check_plan_quality(task, report_dir),
            "check_parallel_conflicts": self.check_parallel_conflicts(task),
            "check_phase_completeness": self.check_phase_completeness(task, lightweight=task.lightweight),
            "check_brainstorming": self.check_brainstorming(task),
        }

    def batch_check_combined(
        self, task: Task, report_dir: Path
    ) -> CheckResult:
        """Run batch_check and combine all results into single CheckResult."""
        results = self.batch_check(task, report_dir)
        return CheckResult.combine(list(results.values()))