"""Stats backend abstraction — pluggable token/time statistics providers.

Same middleware pattern as knowledge_backend.py:
  Dashboard / CLI commands (unchanged)
        ↓
  StatsBackend (Protocol)
    ├─ NativeBackend  → read Claude Code JSONL directly, zero deps
    └─ CodeBurnBackend → delegate to codeburn CLI for aggregated analytics

Switch via config.json: {"stats": {"backend": "native"}}
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol, runtime_checkable

# Re-export NativeBackend for backward compatibility
from kanban_framework.infra.stats_native import NativeBackend  # noqa: F401


@runtime_checkable
class StatsBackend(Protocol):
    """Protocol for token/time statistics backends."""

    def get_stats(self, days: int = 30) -> dict:
        """Return aggregated global stats for the last N days."""
        ...

    def get_task_stats(self, task_id: str) -> dict:
        """Return per-task statistics.

        Returns:
            {
                "total_tokens": int,
                "total_prompts": int,
                "phases": {ph: tokens},
                "agents": {ag: tokens},
                "models": {m: tokens},
                "phase_duration": {ph: seconds},
                "phase_api_calls": {ph: count},
                "step_api_calls": {step_id: count},
                "real_api_calls": int,
                "source": str,
                "note": str
            }
        """
        ...


class CodeBurnBackend:
    """Delegate to codeburn CLI for aggregated analytics.

    Requires: codeburn (brew install codeburn or pip install codeburn)
    Falls back to NativeBackend if codeburn is not installed.
    """

    def __init__(self, project_root: Path):
        self._root = Path(project_root)
        self._native = NativeBackend(project_root)

    def get_stats(self, days: int = 30) -> dict:
        import subprocess
        try:
            period = f"{days}days"
            result = subprocess.run(
                ["codeburn", "report", "-p", period, "--format", "json"],
                capture_output=True, text=True, timeout=15,
                cwd=str(self._root),
            )
            if result.returncode == 0 and result.stdout.strip():
                data = json.loads(result.stdout)
                overview = data.get("overview", {})
                tokens_info = overview.get("tokens", {})
                daily_raw = data.get("daily", [])
                daily = [{
                    "date": d.get("date", ""),
                    "calls": d.get("calls", 0),
                    "tokens": (d.get("inputTokens", 0) + d.get("outputTokens", 0)),
                } for d in daily_raw]
                return {
                    "total_tokens": tokens_info.get("input", 0) + tokens_info.get("output", 0),
                    "total_input": tokens_info.get("input", 0),
                    "total_output": tokens_info.get("output", 0),
                    "total_prompt_calls": overview.get("calls", 0),
                    "total_duration_seconds": 0,
                    "sessions": overview.get("sessions", 0),
                    "by_model": data.get("models", {}),
                    "daily": daily,
                    "source": "codeburn",
                }
        except Exception:
            pass
        return self._native.get_stats(days)

    def get_task_stats(self, task_id: str) -> dict:
        return self._native.get_task_stats(task_id)


# Registry
STATS_BACKEND_REGISTRY = {
    "native": NativeBackend,
    "codeburn": CodeBurnBackend,
}


def resolve_stats_backend(name: str, project_root: Path) -> StatsBackend:
    """Resolve a stats backend by name. Falls back to native."""
    cls = STATS_BACKEND_REGISTRY.get(name)
    if cls is None:
        import warnings
        warnings.warn(f"Unknown stats backend '{name}', falling back to native")
        cls = NativeBackend
    return cls(project_root)
