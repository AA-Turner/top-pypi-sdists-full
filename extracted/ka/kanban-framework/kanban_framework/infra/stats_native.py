"""Native stats backend — reads Claude Code JSONL conversation logs.

Scans ~/.claude/projects/<project-hash>/*.jsonl for operation logs
and augments with global stats-cache.json counters (scoped to project).

Zero dependencies — data already exists on disk.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from kanban_framework.infra.stats_jsonl import (
    count_subagent,
    find_project_jsonl_files,
    estimate_task_from_history,
)

_CACHE_FILE = "stats-cache.json"


class NativeBackend:
    """Read Claude Code JSONL conversation logs for the current project."""

    def __init__(self, project_root: Path):
        self._root = Path(project_root).resolve()
        self._claude_dir = Path.home() / ".claude"

    @property
    def _jsonl_files(self) -> list[Path]:
        return find_project_jsonl_files(self._claude_dir, self._root)

    def get_stats(self, days: int = 30) -> dict:
        cutoff = time.time() - days * 86400

        stats: dict = {
            "total_tokens": 0, "total_input": 0, "total_output": 0,
            "total_prompt_calls": 0, "total_duration_seconds": 0.0,
            "sessions": 0, "by_model": {}, "daily": {},
            "source": "native",
        }

        seen_sessions: set[str] = set()

        for jf in self._jsonl_files:
            self._scan_jsonl_for_stats(jf, cutoff, stats, seen_sessions)

        stats["sessions"] = len(seen_sessions)
        self._augment_model_cache(stats)

        stats["daily"] = sorted(
            [{"date": k, **v} for k, v in stats["daily"].items()],
            key=lambda x: x["date"], reverse=True,
        )[:days]

        return stats

    def get_task_stats(self, task_id: str) -> dict:
        """Per-task stats from JSONL estimation."""
        from pathlib import Path as _Path
        from kanban_framework.infra.filesystem import Filesystem as _FS

        result = self._empty_task_result()
        kanban_dir = self._resolve_kanban_dir(_Path, _FS)
        task_dir, _ = self._resolve_task_dirs(kanban_dir, task_id)

        # JSONL estimation
        task_json = task_dir / "task.json"
        if task_json.is_file():
            estimate_task_from_history(task_json, task_dir, self._jsonl_files, result)

        return result

    # ── Global stats helpers ──────────────────────────────────────────

    def _scan_jsonl_for_stats(self, jf: Path, cutoff: float,
                              stats: dict, seen_sessions: set[str]) -> None:
        from datetime import datetime
        try:
            text = jf.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return
        for line in text.strip().splitlines():
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            from kanban_framework.infra.stats_jsonl import parse_entry_timestamp
            t = parse_entry_timestamp(entry.get("timestamp"))
            if t is None or t < cutoff:
                continue

            sid = entry.get("sessionId", "")
            if sid:
                seen_sessions.add(sid)

            stats["total_prompt_calls"] += 1

            usage = (entry.get("message") or {}).get("usage") or {}
            inp = usage.get("input_tokens") or usage.get("inputTokens") or 0
            out = usage.get("output_tokens") or usage.get("outputTokens") or 0
            tok = inp + out
            stats["total_tokens"] += tok
            stats["total_input"] += inp
            stats["total_output"] += out

            date_key = datetime.fromtimestamp(t).strftime("%Y-%m-%d")
            dd = stats["daily"].setdefault(date_key, {"tokens": 0, "calls": 0})
            dd["calls"] += 1
            dd["tokens"] += tok

    def _augment_model_cache(self, stats: dict) -> None:
        cache_file = self._claude_dir / _CACHE_FILE
        if not cache_file.is_file():
            return
        try:
            cache = json.loads(cache_file.read_text(encoding="utf-8"))
            model_usage = cache.get("modelUsage", {})
            if isinstance(model_usage, str):
                model_usage = json.loads(model_usage)
            for model, mu in model_usage.items():
                stats["by_model"][model] = {
                    "tokens": mu.get("inputTokens", 0) + mu.get("outputTokens", 0),
                    "calls": mu.get("messageCount", 0),
                }
        except Exception:
            pass

    # ── Task stats helpers ────────────────────────────────────────────

    @staticmethod
    def _empty_task_result() -> dict:
        return {
            "total_tokens": 0, "total_prompts": 0,
            "phases": {}, "agents": {}, "models": {},
            "phase_duration": {}, "phase_api_calls": {}, "step_api_calls": {},
            "real_api_calls": 0, "source": "native",
        }

    def _resolve_kanban_dir(self, _Path, _FS):
        kanban_dir = self._root / ".kanban"
        if kanban_dir.is_dir():
            return kanban_dir
        return _Path(_FS.find_project_root()) / ".kanban"

    @staticmethod
    def _resolve_task_dirs(kanban_dir: Path, task_id: str):
        task_dir = kanban_dir / "tasks" / task_id
        archive_dir = kanban_dir / "archive" / task_id
        if archive_dir.is_dir() and not task_dir.is_dir():
            task_dir = archive_dir
        return task_dir, archive_dir

    def _build_tracked_result(self, entry: dict, result: dict) -> dict:
        result["total_tokens"] = entry.get("total_tokens", 0)
        result["total_prompts"] = entry.get("total_prompts", 0)
        result["phases"] = entry.get("by_phase", {})
        result["agents"] = entry.get("agent_totals", {})
        result["models"] = entry.get("by_model", {})
        result["phase_duration"] = entry.get("phase_duration", {})

        session_steps = entry.get("session_steps", {})
        session_phases = entry.get("session_phases", {})
        total_calls = 0
        for step, sids in session_steps.items():
            step_calls = sum(count_subagent(self._claude_dir, sid) for sid in sids)
            result["step_api_calls"][step] = step_calls
            total_calls += step_calls
        for ph, sids in session_phases.items():
            result["phase_api_calls"][ph] = sum(
                count_subagent(self._claude_dir, sid) for sid in sids
            )
        result["real_api_calls"] = total_calls
        result["source"] = "subagent_tracked"
        return result
