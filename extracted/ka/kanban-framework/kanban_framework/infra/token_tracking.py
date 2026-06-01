from __future__ import annotations
import json
import os
from pathlib import Path


def _read_budget_from_config(data_file: Path) -> int:
    """Read per_task budget from .kanban/config.json, falling back to 200000."""
    try:
        kanban_dir = data_file.parent.parent
        config_path = kanban_dir / "config.json"
        if config_path.is_file():
            raw = json.loads(config_path.read_text(encoding="utf-8"))
            budget_cfg = raw.get("budget", {})
            if isinstance(budget_cfg, dict):
                return budget_cfg.get("per_task", 200000)
    except Exception:
        pass
    return 200000


def _find_jsonl_files(project_root: Path) -> list[Path]:
    """Find Claude Code JSONL session files for the given project."""
    claude_projects = Path.home() / ".claude" / "projects"
    if not claude_projects.is_dir():
        return []

    root_name = str(project_root.resolve()).replace("/", "-").replace("_", "-")
    if root_name.startswith("-"):
        root_name = root_name[1:]

    best_dir = None
    best_count = 0
    for proj_dir in claude_projects.iterdir():
        if not proj_dir.is_dir():
            continue
        if root_name in proj_dir.name or proj_dir.name in root_name:
            count = len(list(proj_dir.glob("*.jsonl")))
            if count > best_count:
                best_dir = proj_dir
                best_count = count

    if best_dir is None:
        return []
    return sorted(f for f in best_dir.glob("*.jsonl") if "subagents" not in str(f))


def _extract_tokens_from_jsonl(jsonl_files: list[Path],
                                t_min: float | None = None,
                                t_max: float | None = None) -> dict:
    """Extract token usage from JSONL files within optional time window.

    Returns:
        {"total_tokens": int, "input_tokens": int, "output_tokens": int,
         "turns": int, "models": set, "prompt_count": int}
    """
    total_input = 0
    total_output = 0
    turns = 0
    prompts = 0
    models: set[str] = set()

    for jf in jsonl_files:
        try:
            for line in jf.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = entry.get("message", {})
                usage = msg.get("usage", {})
                if not usage:
                    continue
                ts = entry.get("timestamp")
                if ts is not None:
                    if isinstance(ts, str):
                        from datetime import datetime
                        try:
                            ts = datetime.fromisoformat(ts).timestamp()
                        except (ValueError, TypeError):
                            ts = None
                    if ts is not None and t_min is not None and ts < t_min:
                        continue
                    if ts is not None and t_max is not None and ts > t_max:
                        continue
                total_input += usage.get("input_tokens", 0)
                total_output += usage.get("output_tokens", 0)
                turns += 1
                prompts += 1
                model = entry.get("model", "")
                if model:
                    models.add(model)
        except OSError:
            continue

    return {
        "total_tokens": total_input + total_output,
        "input_tokens": total_input,
        "output_tokens": total_output,
        "turns": turns,
        "models": models,
        "prompt_count": prompts,
    }


class TokenTracker:
    def __init__(self, data_file: Path, budget: int | None = None):
        self._file = Path(data_file)
        self._budget = budget if budget is not None else _read_budget_from_config(self._file)
        self._data = self._load()

    def track(self, task_id: str, tokens: int, phase: str, agent: str = "",
              model: str = "", duration_seconds: float = 0.0) -> None:
        entry = self._data.setdefault(task_id, {"by_phase": {}, "by_agent": {}})
        entry["by_phase"][phase] = entry["by_phase"].get(phase, 0) + tokens
        entry["total_tokens"] = entry.get("total_tokens", 0) + tokens
        # Prompt count: each track() call = one agent spawn (#222)
        entry.setdefault("prompt_count", {})
        entry["prompt_count"][phase] = entry["prompt_count"].get(phase, 0) + 1
        entry["total_prompts"] = entry.get("total_prompts", 0) + 1
        # Duration tracking
        if duration_seconds > 0:
            entry.setdefault("phase_duration", {})
            entry["phase_duration"][phase] = entry["phase_duration"].get(phase, 0) + duration_seconds
        # Model tracking
        if model:
            entry.setdefault("by_model", {})
            entry["by_model"][model] = entry["by_model"].get(model, 0) + tokens
        if agent:
            by_ag = entry.setdefault("by_agent", {})
            by_ag.setdefault(phase, {})
            by_ag[phase][agent] = by_ag[phase].get(agent, 0) + tokens
            ag_totals = entry.setdefault("agent_totals", {})
            ag_totals[agent] = ag_totals.get(agent, 0) + tokens
        self._save()

    def report(self, task_id: str) -> dict:
        entry = self._data.get(task_id, {"total_tokens": 0, "by_phase": {}, "by_agent": {},
              "agent_totals": {}, "prompt_count": {}, "total_prompts": 0, "by_model": {},
              "phase_duration": {}})
        entry["within_budget"] = entry.get("total_tokens", 0) <= self._budget
        return entry

    def check_budget(self, task_id: str) -> bool:
        return self.report(task_id)["total_tokens"] <= self._budget

    def auto_collect(self, task_id: str, phase: str,
                     t_min: float | None = None,
                     t_max: float | None = None) -> dict:
        """Auto-collect token usage from JSONL files for a task phase. (#298)

        Scans ~/.claude/projects/<hash>/*.jsonl within the given time window
        and records aggregated token counts for the specified task and phase.
        Uses the project root derived from the data file path.

        Returns the collected stats dict or empty dict on failure.
        """
        # Derive project root: .kanban/reports/token_tracking.json → go up 3 levels
        project_root = self._file.parent.parent.parent
        jsonl_files = _find_jsonl_files(project_root)
        if not jsonl_files:
            return {}

        stats = _extract_tokens_from_jsonl(jsonl_files, t_min, t_max)
        if stats["total_tokens"] == 0:
            return stats

        # Record via track() for consistent accounting
        self.track(
            task_id, stats["total_tokens"], phase,
            agent="auto-collect",
            model=",".join(sorted(stats["models"])) if stats["models"] else "",
        )

        # Store prompt count separately (track() counts 1 prompt)
        entry = self._data.setdefault(task_id, {"by_phase": {}, "by_agent": {}})
        actual_prompts = stats["prompt_count"]
        if actual_prompts > 1:
            entry["prompt_count"][phase] = actual_prompts
            entry["total_prompts"] = entry.get("total_prompts", 0) + actual_prompts - 1
            self._save()

        # Store input/output split
        entry.setdefault("input_tokens", {})
        entry.setdefault("output_tokens", {})
        entry["input_tokens"][phase] = stats["input_tokens"]
        entry["output_tokens"][phase] = stats["output_tokens"]
        self._save()

        return stats

    def _load(self) -> dict:
        if self._file.exists():
            return json.loads(self._file.read_text(encoding="utf-8"))
        return {}

    def _save(self) -> None:
        self._file.parent.mkdir(parents=True, exist_ok=True)
        self._file.write_text(json.dumps(self._data, indent=2), encoding="utf-8")
