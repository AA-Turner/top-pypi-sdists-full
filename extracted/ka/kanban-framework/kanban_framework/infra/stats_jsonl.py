"""JSONL scanning utilities for stats backends.

Provides reusable helpers for finding and scanning Claude Code JSONL
session files within time windows. Used by NativeBackend and CodeBurnBackend.
"""

from __future__ import annotations

import json
from datetime import datetime as _dt
from pathlib import Path


def find_project_jsonl_files(claude_dir: Path, project_root: Path) -> list[Path]:
    """Find JSONL session files for a specific project.

    Claude Code organizes sessions under:
      ~/.claude/projects/<project-name-hash>/<uuid>.jsonl
    """
    files: list[Path] = []
    projects_dir = claude_dir / "projects"
    if not projects_dir.is_dir():
        return files

    resolved = project_root.resolve()
    if resolved.name == ".kanban":
        resolved = resolved.parent

    root_name = str(resolved).replace("\\", "-").replace("/", "-").replace("_", "-")
    if root_name.startswith("-"):
        root_name = root_name[1:]

    best_dir = None
    for proj_dir in projects_dir.iterdir():
        if not proj_dir.is_dir():
            continue
        dir_name = proj_dir.name
        if root_name in dir_name or dir_name in root_name:
            if best_dir is None or len(list(proj_dir.glob("*.jsonl"))) > len(list(best_dir.glob("*.jsonl"))):
                best_dir = proj_dir

    if best_dir is not None:
        for jf in sorted(best_dir.glob("*.jsonl")):
            if "subagents" not in str(jf):
                files.append(jf)

    return files


def parse_entry_timestamp(ts) -> float | None:
    """Parse a JSONL entry timestamp to unix epoch float."""
    if not ts:
        return None
    try:
        if isinstance(ts, (int, float)):
            return float(ts)
        return _dt.fromisoformat(str(ts).replace("Z", "+00:00")).timestamp()
    except (ValueError, TypeError):
        return None


def count_window(jsonl_files: list[Path], t_min: float, t_max: float) -> int:
    """Count JSONL entries within a time window."""
    count = 0
    for jf in jsonl_files:
        try:
            for line in jf.read_text(errors="replace").strip().splitlines():
                if not line.strip():
                    continue
                try:
                    e = json.loads(line)
                    t = parse_entry_timestamp(e.get("timestamp"))
                    if t is None:
                        continue
                except Exception:
                    continue
                if t_min <= t <= t_max:
                    count += 1
        except Exception:
            pass
    return count


def find_last_timestamp(jsonl_files: list[Path], t_min: float, t_max: float) -> float | None:
    """Find the latest JSONL timestamp within a time window."""
    last = None
    for jf in jsonl_files:
        try:
            for line in jf.read_text(errors="replace").strip().splitlines():
                if not line.strip():
                    continue
                try:
                    e = json.loads(line)
                    t = parse_entry_timestamp(e.get("timestamp"))
                    if t is None:
                        continue
                    if t_min <= t <= t_max:
                        if last is None or t > last:
                            last = t
                except Exception:
                    continue
        except Exception:
            pass
    return last


def count_subagent(claude_dir: Path, subagent_id: str) -> int:
    """Count entries in a subagent JSONL file."""
    projects_dir = claude_dir / "projects"
    if not projects_dir.is_dir():
        return 0
    for proj_dir in projects_dir.iterdir():
        if not proj_dir.is_dir():
            continue
        for session_dir in proj_dir.iterdir():
            if not session_dir.is_dir():
                continue
            target = session_dir / "subagents" / f"{subagent_id}.jsonl"
            if target.is_file():
                try:
                    return len([l for l in target.read_text(errors="replace").strip().splitlines() if l.strip()])
                except Exception:
                    return 0
    return 0


# ── Task history estimation ───────────────────────────────────────────

_FALLBACK_WINDOW_PAD = 60
_TOKENS_PER_CALL_ESTIMATE = 800
_STEP_LOOKBACK = 300


def estimate_task_from_history(
    task_json: Path, task_dir: Path, jsonl_files: list[Path], result: dict,
) -> None:
    """Estimate task stats from task.json history + JSONL file scanning."""
    try:
        task = json.loads(task_json.read_text(encoding="utf-8"))
        history = task.get("history", [])
        if not history:
            return
        _estimate_global_window(history, jsonl_files, result)
        _estimate_phase_windows(history, jsonl_files, result)
        _estimate_step_calls(task_dir, jsonl_files, result)
    except Exception:
        pass


def _estimate_global_window(history: list, jsonl_files: list[Path], result: dict) -> None:
    ts = _extract_history_timestamps(history)
    if not ts:
        return
    t_min, t_max = min(ts) - _FALLBACK_WINDOW_PAD, max(ts) + _FALLBACK_WINDOW_PAD
    result["real_api_calls"] = count_window(jsonl_files, t_min, t_max)
    if result["real_api_calls"] > 0:
        result["total_tokens"] = round(result["real_api_calls"] * _TOKENS_PER_CALL_ESTIMATE)
        result["source"] = "jsonl_estimate"
        result["note"] = f"Estimated from {result['real_api_calls']} JSONL calls"


def _estimate_phase_windows(history: list, jsonl_files: list[Path], result: dict) -> None:
    pw = _build_phase_windows(history)
    _infer_phase_start_times(history, pw)
    _fill_missing_phase_ends(pw, jsonl_files)
    for ph, w in pw.items():
        if w["min"] < 1e99:
            pc = count_window(
                jsonl_files,
                w["min"] - _FALLBACK_WINDOW_PAD,
                w["max"] + _FALLBACK_WINDOW_PAD,
            )
            result["phase_api_calls"][ph] = pc
            result["phases"][ph] = round(pc * _TOKENS_PER_CALL_ESTIMATE)
            result["phase_duration"][ph] = round(w["max"] - w["min"])


def _build_phase_windows(history: list) -> dict:
    pw: dict[str, dict] = {}
    for h in history:
        ph = h.get("phase", "")
        if not ph:
            continue
        for k in ("started_at", "completed_at"):
            v = h.get(k)
            if v:
                try:
                    t = float(v)
                    pw.setdefault(ph, {"min": 1e99, "max": -1e99})
                    if t < pw[ph]["min"]:
                        pw[ph]["min"] = t
                    if t > pw[ph]["max"]:
                        pw[ph]["max"] = t
                except (ValueError, TypeError):
                    pass
    return pw


def _infer_phase_start_times(history: list, pw: dict) -> None:
    completed_at: dict[str, float] = {}
    for h in history:
        ph = h.get("phase", "")
        if not ph:
            continue
        v = h.get("completed_at")
        if v:
            try:
                t = float(v)
                if t > 0:
                    completed_at[ph] = t
            except (ValueError, TypeError):
                pass
    sorted_phases = sorted(completed_at.items(), key=lambda x: x[1])
    for i, (ph, _) in enumerate(sorted_phases):
        w = pw.get(ph)
        if not w:
            continue
        if w["max"] - w["min"] < 1 and i > 0:
            prev_end = sorted_phases[i - 1][1]
            w["min"] = prev_end


def _fill_missing_phase_ends(pw: dict, jsonl_files: list[Path]) -> None:
    for ph, w in pw.items():
        if w["min"] < 1e99 and w["max"] - w["min"] < 1:
            last = find_last_timestamp(
                jsonl_files, w["min"] - _FALLBACK_WINDOW_PAD,
                w["min"] + 3600,
            )
            if last and last > w["min"]:
                w["max"] = last


def _estimate_step_calls(task_dir: Path, jsonl_files: list[Path], result: dict) -> None:
    progress_file = task_dir / "progress.json"
    if not progress_file.is_file():
        return
    try:
        pg = json.loads(progress_file.read_text(encoding="utf-8"))
        for sid, si in pg.get("steps", {}).items():
            if si.get("status") != "completed":
                continue
            ut = si.get("updated_at")
            if ut:
                try:
                    t = float(ut)
                    result["step_api_calls"][sid] = count_window(
                        jsonl_files, t - _STEP_LOOKBACK, t + 10,
                    )
                except (ValueError, TypeError):
                    pass
    except Exception:
        pass


def _extract_history_timestamps(history: list) -> list[float]:
    ts: list[float] = []
    for h in history:
        for k in ("started_at", "completed_at"):
            v = h.get(k)
            if v:
                try:
                    ts.append(float(v))
                except (ValueError, TypeError):
                    pass
    return ts
