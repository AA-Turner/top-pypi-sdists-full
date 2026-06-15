"""Workflow statistics — measure workflow reliability from JSONL logs.

Scans Claude Code JSONL to extract structured lifecycle events for tasks
of a specific workflow. Computes success rates, per-step pass rates, and
failure analysis — all from JSONL (not .kanban/tasks/) because JSONL is
Claude Code's persistent memory that survives project moves and cleanup.

Algorithm: Event Extraction (not time-window counting)

  Step 1: Find tasks by workflow
    Scan for `kanban create --mode <workflow>` commands
    Build {task_id: workflow_name} mapping

  Step 2: Extract lifecycle events per task
    Scan for mark-step / next-step / decide / clean commands
    Build event timeline per task

  Step 3: Classify outcome
    success / aborted / stalled / never_started

  Step 4: Aggregate per-step metrics

  Step 5: Analyze failures
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TaskLifecycle:
    """Lifecycle events for one task, extracted from JSONL."""
    task_id: str
    workflow: str
    created_at: str = ""
    events: list[dict] = field(default_factory=list)
    # Derived
    outcome: str = "unknown"  # success / aborted / stalled / never_started
    last_completed_step: str = ""
    next_expected_step: str = ""

    def classify(self):
        """Determine outcome from events."""
        has_create = any(e["type"] == "created" for e in self.events)
        has_step = any(e["type"] in ("step_completed", "step_skipped") for e in self.events)
        has_success = any(e["type"] == "succeeded" for e in self.events)
        has_abort = any(e["type"] in ("aborted", "cleaned") for e in self.events)

        if has_success:
            self.outcome = "success"
        elif has_abort:
            self.outcome = "aborted"
        elif has_step:
            self.outcome = "stalled"
        elif has_create:
            self.outcome = "never_started"
        else:
            self.outcome = "unknown"

        # Find last completed step and next expected
        for e in reversed(self.events):
            if e["type"] == "step_completed":
                self.last_completed_step = e["step"]
                break
        for e in reversed(self.events):
            if e["type"] == "step_active":
                self.next_expected_step = e["step"]
                break


class WorkflowStatsReader:
    """Read workflow statistics from Claude Code JSONL logs.

    Usage:
        reader = WorkflowStatsReader(project_root=Path("."))
        stats = reader.get_workflow_summary("release")
        # → {"success_rate": 0.7, "step_stats": {...}, ...}
    """

    # Patterns for extracting events from JSONL command strings
    # Must handle: python -m kanban_framework ... create ... --mode X
    #          and: kanban create ... --mode X
    _CREATE_MODE_RE = re.compile(
        r"(?:python\s+-m\s+)?kanban(?:_framework)?\s+"
        r"(?:--?\S+\s+)*"
        r"create\s+.*?--mode\s+(\w+)",
        re.MULTILINE | re.DOTALL,
    )
    _TASK_ID_RE = re.compile(r"\b(TASK-\d+)\b")
    _MARK_STEP_RE = re.compile(
        r"mark-step\s+(TASK-\d+)\s+(\S+)"
    )
    _STATUS_RE = re.compile(
        r"--status\s+(\w+)"
    )
    _NEXT_STEP_RE = re.compile(
        r"next-step\s+(TASK-\d+)"
    )
    _DECIDE_RE = re.compile(
        r"decide\s+(TASK-\d+)\s+--action\s+(\w+)"
    )
    _CLEAN_RE = re.compile(
        r"clean\s+(TASK-\d+)"
    )
    # v0.195: Also detect git tag as success signal (release workflow uses
    # git tag directly without kanban decide in some configurations).
    _GIT_TAG_RE = re.compile(r"git\s+tag\s+v\d+\.\d+\.\d+")
    _GIT_PUSH_TAG_RE = re.compile(r"git\s+push\s+origin\s+v\d+\.\d+\.\d+")
    _RESPONSE_ID_RE = re.compile(r'"id"\s*:\s*"(TASK-[\w-]+)"')
    _RESPONSE_MODE_RE = re.compile(r'"mode"\s*:\s*"(\w+)"')
    _RESPONSE_STEP_RE = re.compile(r'"step_id"\s*:\s*"([^"]+)"')
    _GUARD_FAIL_RE = re.compile(r"guard check failed|GuardError", re.IGNORECASE)

    def __init__(self, project_root: Path):
        self._project_root = Path(project_root).resolve()
        self._claude_dir = Path.home() / ".claude" / "projects"
        self._project_hash = str(self._project_root).replace("/", "-").replace("_", "-")

    def _project_log_dir(self) -> Path | None:
        candidate = self._claude_dir / self._project_hash
        if candidate.is_dir():
            return candidate
        if not self._claude_dir.is_dir():
            return None
        target = self._project_hash.lower().replace("-", "").replace("_", "")
        for d in self._claude_dir.iterdir():
            if not d.is_dir():
                continue
            if d.name.lower().replace("-", "").replace("_", "") == target:
                return d
        return None

    def _iter_jsonl_files(self):
        log_dir = self._project_log_dir()
        if log_dir is None:
            return
        yield from sorted(log_dir.glob("*.jsonl"))

    def get_workflow_summary(self, workflow_name: str) -> dict:
        """Get success rate + step stats for a workflow.

        Returns:
            {
                "workflow": str,
                "total_tasks": int,
                "outcomes": {"success": N, "aborted": N, "stalled": N, ...},
                "success_rate": float,
                "step_stats": {step_id: {appeared, completed, skipped, pass_rate}},
                "bottleneck_step": str,  # step with lowest pass_rate
                "failure_analysis": [...],
                "data_source": "jsonl"
            }
        """
        lifecycles = self._extract_lifecycles(workflow_name)

        if not lifecycles:
            return {
                "workflow": workflow_name,
                "total_tasks": 0,
                "outcomes": {},
                "success_rate": 0.0,
                "step_stats": {},
                "failure_analysis": [],
                "data_source": "jsonl",
                "note": f"No tasks found with mode={workflow_name}",
            }

        # Classify outcomes
        for lc in lifecycles.values():
            lc.classify()

        # Aggregate outcomes
        outcome_counts: dict[str, int] = defaultdict(int)
        for lc in lifecycles.values():
            outcome_counts[lc.outcome] += 1

        total = len(lifecycles)
        success_count = outcome_counts.get("success", 0)
        success_rate = round(success_count / total, 2) if total else 0.0

        # Per-step stats
        step_appeared: dict[str, int] = defaultdict(int)
        step_completed: dict[str, int] = defaultdict(int)
        step_skipped: dict[str, int] = defaultdict(int)

        for lc in lifecycles.values():
            for e in lc.events:
                if e["type"] == "step_active":
                    step_appeared[e["step"]] += 1
                elif e["type"] == "step_completed":
                    step_completed[e["step"]] += 1
                elif e["type"] == "step_skipped":
                    step_skipped[e["step"]] += 1

        step_stats: dict[str, dict] = {}
        all_steps = set(step_appeared) | set(step_completed) | set(step_skipped)
        for step_id in all_steps:
            appeared = step_appeared.get(step_id, 0)
            completed = step_completed.get(step_id, 0)
            skipped = step_skipped.get(step_id, 0)
            pass_rate = round(completed / appeared, 2) if appeared else 1.0
            step_stats[step_id] = {
                "appeared": appeared,
                "completed": completed,
                "skipped": skipped,
                "pass_rate": pass_rate,
            }

        # Find bottleneck (lowest pass_rate with appeared > 0)
        bottleneck = None
        bottleneck_rate = 1.0
        for step_id, stats in step_stats.items():
            if stats["appeared"] > 0 and stats["pass_rate"] < bottleneck_rate:
                bottleneck = step_id
                bottleneck_rate = stats["pass_rate"]

        # Failure analysis
        failures = []
        for task_id, lc in lifecycles.items():
            if lc.outcome in ("aborted", "stalled"):
                # Find guard failures near the stall point
                guard_fails = [
                    e for e in lc.events if e["type"] == "guard_failure"
                ]
                fail_reason = "unknown"
                if guard_fails:
                    fail_reason = guard_fails[-1].get("message", "guard failure")
                failures.append({
                    "task_id": task_id,
                    "outcome": lc.outcome,
                    "last_completed_step": lc.last_completed_step,
                    "next_expected_step": lc.next_expected_step,
                    "failure_reason": fail_reason,
                })

        # Recommendation
        recommendation = ""
        if success_rate < 0.8 and bottleneck:
            recommendation = (
                f"瓶颈步骤: {bottleneck} (通过率 {bottleneck_rate*100:.0f}%)。"
                f"建议优化该步骤的 spawn_prompt 或 guard 配置。"
            )
        elif success_rate >= 0.8:
            recommendation = f"成功率 {success_rate*100:.0f}%，工作流状态良好。"

        return {
            "workflow": workflow_name,
            "total_tasks": total,
            "outcomes": dict(outcome_counts),
            "success_rate": success_rate,
            "step_stats": dict(sorted(step_stats.items())),
            "bottleneck_step": bottleneck,
            "failure_analysis": failures,
            "recommendation": recommendation,
            "data_source": "jsonl (~/.claude/projects/*.jsonl)",
        }

    def _extract_lifecycles(self, workflow_name: str) -> dict[str, TaskLifecycle]:
        """Single pass over JSONL to extract all lifecycle events.

        Returns {task_id: TaskLifecycle} for tasks created with workflow_name.
        """
        lifecycles: dict[str, TaskLifecycle] = {}
        # Track which tasks belong to this workflow
        workflow_tasks: set[str] = set()

        for path in self._iter_jsonl_files():
            try:
                with path.open(encoding="utf-8") as f:
                    for line in f:
                        try:
                            entry = json.loads(line)
                        except json.JSONDecodeError:
                            continue

                        content = self._extract_content_text(entry)
                        if not content:
                            continue

                        # Check for create commands with --mode
                        if "create" in content and "--mode" in content:
                            mode_match = self._CREATE_MODE_RE.search(content)
                            if mode_match and mode_match.group(1) == workflow_name:
                                task_match = self._RESPONSE_ID_RE.search(content)
                                if not task_match:
                                    task_match = self._TASK_ID_RE.search(content)
                                if task_match:
                                    tid = task_match.group(1)
                                    if tid not in lifecycles:
                                        lifecycles[tid] = TaskLifecycle(
                                            task_id=tid,
                                            workflow=workflow_name,
                                            created_at=entry.get("timestamp", ""),
                                        )
                                        workflow_tasks.add(tid)

                        # For known workflow tasks, extract events
                        for tid in list(workflow_tasks):
                            if tid not in content:
                                continue

                            lc = lifecycles[tid]
                            ts = entry.get("timestamp", "")

                            # Check for mark-step events
                            mark_match = self._MARK_STEP_RE.search(content)
                            if mark_match and mark_match.group(1) == tid:
                                step_id = mark_match.group(2)
                                status_match = self._STATUS_RE.search(content)
                                status = status_match.group(1) if status_match else "completed"
                                if "completed" in status:
                                    lc.events.append({
                                        "type": "step_completed",
                                        "step": step_id,
                                        "ts": ts,
                                    })
                                elif "skipped" in status:
                                    lc.events.append({
                                        "type": "step_skipped",
                                        "step": step_id,
                                        "ts": ts,
                                    })

                            # Check for next-step (what step is active)
                            next_match = self._NEXT_STEP_RE.search(content)
                            if next_match and next_match.group(1) == tid:
                                step_match = self._RESPONSE_STEP_RE.search(content)
                                if step_match:
                                    lc.events.append({
                                        "type": "step_active",
                                        "step": step_match.group(1),
                                        "ts": ts,
                                    })

                            # Check for decide
                            decide_match = self._DECIDE_RE.search(content)
                            if decide_match and decide_match.group(1) == tid:
                                action = decide_match.group(2)
                                if "approve_and_archive" in action:
                                    lc.events.append({
                                        "type": "succeeded",
                                        "ts": ts,
                                    })
                                elif "abort" in action:
                                    lc.events.append({
                                        "type": "aborted",
                                        "ts": ts,
                                    })

                            # Check for clean
                            clean_match = self._CLEAN_RE.search(content)
                            if clean_match and clean_match.group(1) == tid:
                                lc.events.append({
                                    "type": "cleaned",
                                    "ts": ts,
                                })

                            # v0.195: Detect git tag as success signal
                            # (release workflow may use git tag directly
                            # without kanban decide). Don't require tid in
                            # content — git push v0.X.Y won't contain TASK-NNN.
                            if self._GIT_PUSH_TAG_RE.search(content):
                                lc.events.append({
                                    "type": "succeeded",
                                    "ts": ts,
                                    "source": "git_push_tag",
                                })

                            # Check for guard failures in tool_result
                            if self._GUARD_FAIL_RE.search(content) and tid in content:
                                lc.events.append({
                                    "type": "guard_failure",
                                    "step": lc.last_completed_step or "unknown",
                                    "message": content[:200],
                                    "ts": ts,
                                })

                        # v0.195: Session-level git tag detection.
                        # git push origin v0.X.Y won't contain TASK-NNN,
                        # so check it outside the per-task loop. Apply to
                        # all active tasks in this session that don't yet
                        # have a terminal event.
                        if self._GIT_PUSH_TAG_RE.search(content):
                            for tid in workflow_tasks:
                                lc = lifecycles.get(tid)
                                if lc and not any(
                                    e["type"] in ("succeeded", "aborted", "cleaned")
                                    for e in lc.events
                                ):
                                    lc.events.append({
                                        "type": "succeeded",
                                        "ts": entry.get("timestamp", ""),
                                        "source": "git_push_tag",
                                    })

            except (OSError, UnicodeDecodeError):
                continue

        return lifecycles

    @staticmethod
    def _extract_content_text(entry: dict) -> str:
        """Extract readable text from a JSONL entry (assistant tool_use or tool_result)."""
        msg = entry.get("message", {})
        if not isinstance(msg, dict):
            return ""
        content = msg.get("content", "")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for block in content:
                if isinstance(block, dict):
                    # tool_use: input.command
                    if block.get("type") == "tool_use":
                        inp = block.get("input", {})
                        if isinstance(inp, dict):
                            cmd = inp.get("command", "")
                            if isinstance(cmd, str):
                                parts.append(cmd)
                    # tool_result: content
                    elif block.get("type") == "tool_result":
                        c = block.get("content", "")
                        if isinstance(c, str):
                            parts.append(c)
                        elif isinstance(c, list):
                            for sub in c:
                                if isinstance(sub, dict):
                                    t = sub.get("text", "")
                                    if isinstance(t, str):
                                        parts.append(t)
                    # text block
                    elif "text" in block:
                        parts.append(str(block["text"]))
            return "\n".join(parts)
        return ""
