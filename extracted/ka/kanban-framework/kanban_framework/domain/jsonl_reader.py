"""Read Claude Code JSONL session transcripts for token/time analytics.

Claude Code writes session data to ~/.claude/projects/<sanitized-cwd>/*.jsonl
Each assistant message contains message.usage with exact token counts.
"""

from __future__ import annotations
import json, os, time
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TurnRecord:
    timestamp: float = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read: int = 0
    cache_write: int = 0
    tool_names: list[str] = field(default_factory=list)
    model: str = ""


@dataclass
class SessionStats:
    session_id: str
    file_path: Path
    total_input: int = 0
    total_output: int = 0
    total_cache_read: int = 0
    total_cache_write: int = 0
    turn_count: int = 0
    tool_counts: dict[str, int] = field(default_factory=dict)
    models: list[str] = field(default_factory=list)
    first_ts: float = 0
    last_ts: float = 0
    turns: list[TurnRecord] = field(default_factory=list)

    @property
    def total_tokens(self) -> int:
        return self.total_input + self.total_output

    @property
    def duration_minutes(self) -> float:
        try:
            a, b = float(self.first_ts or 0), float(self.last_ts or 0)
            if a and b:
                return (b - a) / 60
        except (ValueError, TypeError):
            pass
        return 0


def find_session_dir(cwd: str | Path | None = None) -> Path:
    """Find the Claude Code session directory for the current project."""
    if cwd:
        project_path = Path(cwd).resolve()
    else:
        project_path = Path.cwd().resolve()

    projects_dir = Path.home() / ".claude" / "projects"
    if not projects_dir.is_dir():
        return projects_dir / "unknown"

    leaf = project_path.name
    # Find directory containing this project's leaf name with JSONL files
    for d in projects_dir.iterdir():
        if not d.is_dir():
            continue
        if leaf in d.name.split("-"):
            jsonl_files = list(d.glob("*.jsonl"))
            if jsonl_files:
                return d

    # Fallback: try sanitized full path
    sanitized = "".join(c if c.isalnum() else "-" for c in str(project_path))
    return projects_dir / sanitized


def parse_session(filepath: Path) -> Optional[SessionStats]:
    """Parse a single JSONL session file and extract token/tool stats."""
    if not filepath.is_file():
        return None
    sid = filepath.stem
    stats = SessionStats(session_id=sid, file_path=filepath)

    try:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue

                msg = d.get("message", {})
                if not isinstance(msg, dict):
                    continue

                usage = msg.get("usage")
                if not usage:
                    continue

                ts = d.get("timestamp", 0)
                turn = TurnRecord(
                    timestamp=ts,
                    input_tokens=usage.get("input_tokens", 0),
                    output_tokens=usage.get("output_tokens", 0),
                    cache_read=usage.get("cache_read_input_tokens", 0),
                    cache_write=usage.get("cache_creation_input_tokens", 0),
                    model=d.get("model", msg.get("model", "")),
                )

                # Extract tool names from content blocks
                content = msg.get("content", [])
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "tool_use":
                            tool_name = block.get("name", "unknown")
                            turn.tool_names.append(tool_name)
                            stats.tool_counts[tool_name] = stats.tool_counts.get(tool_name, 0) + 1

                stats.total_input += turn.input_tokens
                stats.total_output += turn.output_tokens
                stats.total_cache_read += turn.cache_read
                stats.total_cache_write += turn.cache_write
                stats.turn_count += 1
                stats.turns.append(turn)

                if turn.model and turn.model not in stats.models:
                    stats.models.append(turn.model)
                if ts:
                    if not stats.first_ts or ts < stats.first_ts:
                        stats.first_ts = ts
                    if not stats.last_ts or ts > stats.last_ts:
                        stats.last_ts = ts

    except (OSError, json.JSONDecodeError):
        pass

    if stats.turn_count == 0:
        return None
    return stats


def collect_all_sessions(cwd: str | Path | None = None, days: int = 30) -> list[SessionStats]:
    """Collect stats from all session files in the project directory."""
    session_dir = find_session_dir(cwd)
    if not session_dir.is_dir():
        return []

    cutoff = time.time() - days * 86400
    results: list[SessionStats] = []
    for f in sorted(session_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True):
        stat = parse_session(f)
        if stat:
            try:
                last = float(stat.last_ts) if stat.last_ts else 0
            except (ValueError, TypeError):
                last = 0
            if last >= cutoff or last == 0:
                results.append(stat)
    return results


def aggregate_stats(sessions: list[SessionStats]) -> dict:
    """Aggregate stats across multiple sessions."""
    aggr = {
        "sessions": len(sessions),
        "total_input": 0,
        "total_output": 0,
        "total_cache_read": 0,
        "total_cache_write": 0,
        "total_turns": 0,
        "total_duration_minutes": 0.0,
        "tool_counts": {},
        "models": set(),
        "per_session": [],
    }
    for s in sessions:
        aggr["total_input"] += s.total_input
        aggr["total_output"] += s.total_output
        aggr["total_cache_read"] += s.total_cache_read
        aggr["total_cache_write"] += s.total_cache_write
        aggr["total_turns"] += s.turn_count
        aggr["total_duration_minutes"] += s.duration_minutes
        for tool, count in s.tool_counts.items():
            aggr["tool_counts"][tool] = aggr["tool_counts"].get(tool, 0) + count
        aggr["models"].update(s.models)
        aggr["per_session"].append({
            "id": s.session_id[:8],
            "turns": s.turn_count,
            "tokens": s.total_tokens,
            "input": s.total_input,
            "output": s.total_output,
            "duration_min": round(s.duration_minutes, 1),
        })
    aggr["models"] = sorted(aggr["models"])
    return aggr


def attribute_tokens_to_steps(
    cwd: str | Path | None = None, days: int = 30
) -> dict[str, dict[str, int]]:
    """
    Attribute JSONL token consumption to kanban steps by matching turn
    timestamps against step completion times in progress.json.

    Returns mapping of {task_id: {step_id: token_count}}.
    """
    from pathlib import Path as _Path

    sessions = collect_all_sessions(cwd=cwd, days=days)
    if not sessions:
        return {}

    # Build a sorted list of all turns with timestamps
    turns: list[dict] = []
    for s in sessions:
        for t in s.turns:
            if t.timestamp:
                ts = t.timestamp
                if isinstance(ts, str):
                    from datetime import datetime
                    try:
                        ts = datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
                    except (ValueError, TypeError):
                        continue
                else:
                    ts = float(ts) if ts else 0
                turns.append({
                    "ts": ts,
                    "tokens": t.input_tokens + t.output_tokens,
                })

    if not turns:
        return {}

    turns.sort(key=lambda x: x["ts"])

    # Walk through project tasks (active + archived) and match step boundaries
    result: dict[str, dict[str, int]] = {}
    project_root = _Path(cwd) if cwd else _Path.cwd()
    kanban_dir = project_root / ".kanban"

    import json as _json

    def _process_dir(base: _Path) -> None:
        if not base.is_dir():
            return
        for task_dir in sorted(base.iterdir()):
            if not task_dir.is_dir():
                continue
            _process_task(task_dir)

    def _process_task(task_dir: _Path) -> None:
        nonlocal result
        progress_file = task_dir / "progress.json"
        if not progress_file.is_file():
            return
        try:
            progress = _json.loads(progress_file.read_text(encoding="utf-8"))
        except (_json.JSONDecodeError, OSError):
            return

        steps = progress.get("steps", {})
        if not steps:
            return

        # Build step time boundaries
        boundaries: list[tuple[str, float, float]] = []
        prev_ts = turns[0]["ts"] if turns else 0
        sorted_steps = sorted(
            steps.items(),
            key=lambda x: x[1].get("updated_at", 0) if isinstance(x[1], dict) else 0,
        )
        for step_id, step_info in sorted_steps:
            if not isinstance(step_info, dict):
                continue
            ts = step_info.get("updated_at", 0)
            if not ts:
                continue
            boundaries.append((step_id, prev_ts, ts))
            prev_ts = ts

        # Add final boundary to catch remaining turns
        if boundaries:
            boundaries.append(("_remainder", prev_ts, float("inf")))

        # Attribute tokens
        task_tokens: dict[str, int] = {}
        for step_id, start, end in boundaries:
            step_tokens = sum(
                t["tokens"] for t in turns if start <= t["ts"] < end
            )
            if step_tokens > 0:
                task_tokens[step_id] = step_tokens

        if task_tokens:
            result[task_dir.name] = task_tokens

    # Scan both active tasks and archived tasks
    _process_dir(kanban_dir / "tasks")
    _process_dir(kanban_dir / "archive")
    return result
