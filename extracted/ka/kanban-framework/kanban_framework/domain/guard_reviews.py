"""Review and conflict guard checks — plan quality, spec, parallel/cross-task conflicts.

Extracted from guard.py. These methods validate plan artifacts, test spec coverage,
and detect file ownership conflicts within and across tasks.
"""
from __future__ import annotations

from pathlib import Path

from kanban_framework.types import Task
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.config import Config
from kanban_framework.domain.guard import CheckResult


class GuardReviews:
    """Plan review, spec review, and conflict detection checks."""

    def __init__(self, fs: Filesystem, config: Config):
        self._fs = fs
        self._cfg = config

    def check_plan_quality(self, task: Task, report_dir: Path) -> CheckResult:
        import json as _json
        td = self._fs.task_dir(task.id)
        spec_file = td / "spec.md"
        breakdown_file = td / "task_breakdown.json"
        index_file = td / "plan" / "index.md"

        failures: list[str] = []

        # File existence
        if not self._fs.file_exists(spec_file):
            failures.append("spec.md missing")
        if not self._fs.file_exists(breakdown_file):
            failures.append("task_breakdown.json missing")
        if not self._fs.file_exists(index_file):
            failures.append("plan/index.md missing")

        if failures:
            return CheckResult(passed=False, failures=failures)

        # Parse task_breakdown.json
        try:
            breakdown_data = _json.loads(breakdown_file.read_text(encoding="utf-8"))
        except (ValueError, OSError) as e:
            return CheckResult(passed=False, failures=[f"task_breakdown.json invalid: {e}"])

        subtasks = breakdown_data.get("subtasks", [])
        if not subtasks:
            failures.append("task_breakdown.json has no subtasks")

        # Verify each subtask has a plan file
        plan_dir = td / "plan"
        subtask_ids = []
        for st in subtasks:
            st_id = st.get("id", "")
            if not st_id:
                failures.append("subtask missing 'id' field")
                continue
            subtask_ids.append(st_id)
            # Check plan file exists (ST-NNN_*.md pattern)
            plan_files = list(plan_dir.glob(f"{st_id}_*.md"))
            if not plan_files:
                failures.append(f"plan/{st_id}_*.md missing for subtask {st_id}")

        # Verify index.md references subtasks
        try:
            index_content = index_file.read_text(encoding="utf-8")
        except OSError:
            index_content = ""
        if subtask_ids and index_content:
            for st_id in subtask_ids:
                if st_id not in index_content:
                    failures.append(f"index.md missing reference to {st_id}")
                    break

        # Check for circular dependencies
        if subtask_ids:
            dep_graph = {st_id: [] for st_id in subtask_ids}
            for st in subtasks:
                st_id = st.get("id", "")
                for dep in st.get("dependencies", []):
                    if dep in dep_graph:
                        dep_graph[st_id].append(dep)
            if _has_cycle(dep_graph):
                failures.append("circular dependency detected in task_breakdown.json")

        return CheckResult(passed=len(failures) == 0, failures=failures)

    def check_spec(self, task: Task, report_dir: Path) -> CheckResult:
        spec_file = self._fs.task_dir(task.id) / "test_spec.md"
        if not self._fs.file_exists(spec_file):
            return CheckResult(passed=False, failures=["test_spec.md missing"])
        if spec_file.stat().st_size == 0:
            return CheckResult(passed=False, failures=["test_spec.md is empty"])
        # IR-119: verify acceptance criteria have test case coverage
        task_spec_file = self._fs.task_dir(task.id) / "spec.md"
        if self._fs.file_exists(task_spec_file):
            import re
            spec_content = spec_file.read_text(encoding="utf-8")
            req_content = task_spec_file.read_text(encoding="utf-8")
            warnings: list[str] = []
            ac_section = re.search(r'## 验收标准\n\n(.*?)(?:\n##|\Z)', req_content, re.DOTALL)
            if ac_section:
                for line in ac_section.group(1).split('\n'):
                    line = line.strip()
                    if line.startswith('- AC-'):
                        ac_id = line.split(':', 1)[0].lstrip('- ').strip()
                        ac_text = line.split(':', 1)[1].strip()[:60] if ':' in line else line
                        if ac_text.lower() not in spec_content.lower():
                            warnings.append(f"{ac_id} not covered by test spec")
            if warnings:
                return CheckResult(passed=True, warnings=warnings)
        return CheckResult(passed=True)

    def check_parallel_conflicts(self, task: Task) -> CheckResult:
        breakdown_file = self._fs.task_dir(task.id) / "task_breakdown.json"
        if not self._fs.file_exists(breakdown_file):
            return CheckResult(passed=False, failures=["task_breakdown.json missing"])

        import json
        data = json.loads(breakdown_file.read_text(encoding="utf-8"))
        subtasks = data.get("subtasks", [])

        parallelizable = [
            s for s in subtasks
            if s.get("parallelizable") and not s.get("dependencies")
        ]
        conflicts = []
        for i in range(len(parallelizable)):
            for j in range(i + 1, len(parallelizable)):
                a_files = set(parallelizable[i].get("file_ownership", []))
                b_files = set(parallelizable[j].get("file_ownership", []))
                overlap = a_files & b_files
                if overlap:
                    conflicts.append(
                        f"{parallelizable[i]['id']} <-> {parallelizable[j]['id']}: "
                        f"{', '.join(sorted(overlap))}"
                    )

        if conflicts:
            return CheckResult(
                passed=False,
                failures=[f"parallel conflict: {c}" for c in conflicts],
            )
        return CheckResult(passed=True)

    def check_cross_task_conflicts(self) -> CheckResult:
        """Check file ownership conflicts across all active (non-archived) tasks."""
        import json
        conflicts = []
        task_files = {}

        # Scan all task.json files in tasks/ directory
        tasks_dir = self._fs.kanban_dir / "tasks"
        if not tasks_dir.exists():
            return CheckResult(passed=True, warnings=["no tasks directory"])

        for tf in tasks_dir.glob("TASK-*.json"):
            data = json.loads(tf.read_text(encoding="utf-8"))
            tid = data.get("id", tf.stem)
            status = data.get("status", "")
            if status in ("archived", "cancelled"):
                continue

            bf = self._fs.task_dir(tid) / "task_breakdown.json"
            if not self._fs.file_exists(bf):
                continue
            breakdown = json.loads(bf.read_text(encoding="utf-8"))
            all_files = set()
            for st in breakdown.get("subtasks", []):
                for f in st.get("file_ownership", []):
                    all_files.add(f)
            if all_files:
                task_files[tid] = all_files

        tids = sorted(task_files.keys())
        for i in range(len(tids)):
            for j in range(i + 1, len(tids)):
                overlap = task_files[tids[i]] & task_files[tids[j]]
                if overlap:
                    conflicts.append(
                        f"{tids[i]} <-> {tids[j]}: {', '.join(sorted(overlap))}"
                    )

        if conflicts:
            return CheckResult(
                passed=False,
                failures=[f"cross-task conflict: {c}" for c in conflicts],
            )
        return CheckResult(passed=True)


def _has_cycle(graph: dict[str, list[str]]) -> bool:
    visited: set[str] = set()
    stack: set[str] = set()

    def dfs(node: str) -> bool:
        if node in stack:
            return True
        if node in visited:
            return False
        visited.add(node)
        stack.add(node)
        for dep in graph.get(node, []):
            if dfs(dep):
                return True
        stack.remove(node)
        return False

    return any(dfs(n) for n in graph)
