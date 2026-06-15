"""LLM call stats — parse Claude Code JSONL logs for per-task + per-mode attribution.

Attribution strategy: **command-segment based on kanban CLI invocations**.

Each Claude Code session is one JSONL file (filename = sessionId). We walk
through entries in chronological order. Each `kanban <cmd> TASK-NNN`
invocation switches the "current task" for that session. All subsequent
assistant entries (LLM calls) are attributed to the current task until the
next kanban command switches it again.

This handles multi-task sessions correctly: if a user works on TASK-001
then TASK-002 in the same session, each task gets credit only for the
LLM calls that happened during its "ownership" of the session.
"""
from __future__ import annotations

import json
import re
import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

# Match TASK-NNN (any digit count).
_TASK_ID_RE = re.compile(r"\b(TASK-\d+)\b")

# Kanban CLI command prefixes — anything starting with these counts as a
# lifecycle event. Task reference extracted from the command body.
# Includes both `kanban <subcmd>` (installed CLI) and `kanban_framework`
# (python -m form). Multi-line bash scripts containing these match too.
# v0.189.3 (#650): expanded from 8 to ALL kanban subcommands to prevent
# attribution undercounting. Previously stats/benchmark/knowledge/init/etc
# were missed, causing LLM efficiency stats to show ~4% of real calls.
_KANBAN_CMD_PATTERN_STR = (
    r"create|task\s+create|workflow|decide|clean|run|show|task\s+edit|time"
    r"|stats|benchmark|knowledge|init|version|update"
    r"|inbox|subtask|dashboard|worktree|scan|nlp"
    r"|recover|resume|rollback|promote|guard|framework"
    r"|plan|evaluator|hook|check-env|evolve-skills|codebase"
)
_KANBAN_CMD_PATTERNS = (
    re.compile(r"\bkanban\s+(?:" + _KANBAN_CMD_PATTERN_STR + r")\b"),
    re.compile(r"\bkanban_framework\b\s+.*--?(json|text)?"),
)

# Extract a single kanban subcommand from a multi-line / multi-cmd bash script.
# Returns just the kanban portion + 1-2 args after, for readable display.
# Captures both `kanban <subcmd>` and `python -m kanban_framework <subcmd>` forms.
_KANBAN_SUBCMD_RE = re.compile(
    r"(?:python\s+-m\s+)?kanban(?:_framework)?\s+"
    r"(?:--?\S+\s+)*"  # skip flags like --json, --status completed
    r"((" + _KANBAN_CMD_PATTERN_STR + r")"
    r"(?:\s+[\w\-./]+){0,4})",
    re.MULTILINE,
)

# Ownership release triggers — when these appear, current task attribution ends.
# 30 min idle: task work that hasn't touched kanban in 30 min is considered done.
_IDLE_RELEASE_SECONDS = 30 * 60
# Archive signals: explicit "task finished" commands.
# Matches both full form (`kanban decide TASK-X --action approve_and_archive`)
# and sub-command form (`decide TASK-X --action approve_and_archive`).
_ARCHIVE_CMD_RE = re.compile(
    r"(?:^|\b)(?:kanban\s+)?(?:decide\s+\S+\s+--action\s+(?:approve_and_archive|abort)|clean\s+\S+)"
)


def _parse_ts(ts_str: str):
    """Parse ISO 8601 timestamp from Claude Code JSONL. Returns datetime or None."""
    if not ts_str:
        return None
    try:
        from datetime import datetime
        return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def _is_archive_signal(cmd: str) -> bool:
    """Check if a kanban (sub-)command signals task completion (releases ownership).

    Accepts both full form (`kanban decide TASK-X --action approve_and_archive`)
    and sub-command form (`decide TASK-X --action approve_and_archive`).
    """
    return bool(_ARCHIVE_CMD_RE.search(cmd))


@dataclass
class TaskLLMStats:
    """Aggregated LLM stats for one kanban task."""

    task_id: str
    total_calls: int = 0
    main_agent_calls: int = 0
    sub_agent_calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    models: dict[str, int] = field(default_factory=dict)
    sessions_count: int = 0
    first_activity_at: str = ""
    last_activity_at: str = ""
    kanban_commands: int = 0

    def to_dict(self) -> dict:
        # Effective input includes cache_read — Claude Code JSONL records
        # cache hits separately from input_tokens, so raw input_tokens
        # understates true prompt size by orders of magnitude when cache
        # is warm (typical: 99%+ hit rate). Ratios must use effective_input
        # or they give nonsensical results (e.g. output > input → ratio >100%).
        effective_input = self.input_tokens + self.cache_read_tokens
        return {
            "task_id": self.task_id,
            "total_calls": self.total_calls,
            "main_agent_calls": self.main_agent_calls,
            "sub_agent_calls": self.sub_agent_calls,
            "tokens": {
                "input": self.input_tokens,
                "output": self.output_tokens,
                "cache_read": self.cache_read_tokens,
                "effective_input": effective_input,
                "total": self.input_tokens + self.output_tokens,
            },
            "output_effective_ratio_pct": round(
                self.output_tokens / effective_input * 100, 2
            ) if effective_input else 0.0,
            "models": dict(self.models),
            "sessions_count": self.sessions_count,
            "first_activity_at": self.first_activity_at,
            "last_activity_at": self.last_activity_at,
            "kanban_commands": self.kanban_commands,
        }


@dataclass
class ModeLLMStats:
    """Aggregated LLM stats across all tasks of one workflow mode."""

    mode: str
    task_count: int = 0
    total_calls: int = 0
    main_agent_calls: int = 0
    sub_agent_calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0

    @property
    def avg_calls_per_task(self) -> float:
        return round(self.total_calls / self.task_count, 1) if self.task_count else 0.0

    @property
    def avg_tokens_per_task(self) -> int:
        if not self.task_count:
            return 0
        return (self.input_tokens + self.output_tokens) // self.task_count

    def to_dict(self) -> dict:
        return {
            "mode": self.mode,
            "task_count": self.task_count,
            "total_calls": self.total_calls,
            "main_agent_calls": self.main_agent_calls,
            "sub_agent_calls": self.sub_agent_calls,
            "avg_calls_per_task": self.avg_calls_per_task,
            "tokens": {
                "input": self.input_tokens,
                "output": self.output_tokens,
                "cache_read": self.cache_read_tokens,
                "total": self.input_tokens + self.output_tokens,
            },
            "avg_tokens_per_task": self.avg_tokens_per_task,
        }


@dataclass
class SessionAttribution:
    """Per-session attribution result for one task.

    Each session where the task appeared contributes:
    - assistant_calls: LLM calls during this task's "ownership" segments
    - command_count: how many kanban commands in this session referenced the task
    - first_ts / last_ts: time range of attribution (for diagnostics)
    """

    session_id: str
    assistant_calls: int = 0
    command_count: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    models: dict[str, int] = field(default_factory=dict)
    main_calls: int = 0
    sub_calls: int = 0
    first_ts: str = ""
    last_ts: str = ""


class LLMStatsReader:
    """Walk Claude Code JSONL logs to compute per-task + per-mode LLM stats.

    Algorithm:
      1. For each JSONL file (session), single-pass scan to track which task
         "owns" each segment between kanban commands.
      2. Every assistant entry is attributed to the current owning task.
      3. Per-task: aggregate across all sessions where task appeared.
      4. Per-mode: read task.json for mode, sum task stats.

    Usage:
        reader = LLMStatsReader(project_root=Path("/path/to/project"))
        task_stats = reader.get_task_stats("TASK-001")
        mode_stats = reader.get_mode_stats()
    """

    def __init__(self, project_root: Path):
        self._project_root = Path(project_root).resolve()
        self._claude_dir = Path.home() / ".claude" / "projects"
        self._project_hash = self._compute_project_hash(self._project_root)

    @staticmethod
    def _compute_project_hash(project_root: Path) -> str:
        """Claude Code stores logs under ~/.claude/projects/{path-with-dashes}.

        Both `/` and `_` are replaced with `-`.
        """
        return str(project_root).replace("/", "-").replace("_", "-")

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
            name = d.name.lower().replace("-", "").replace("_", "")
            if name == target:
                return d
        return None

    def _iter_jsonl_files(self) -> Iterator[Path]:
        log_dir = self._project_log_dir()
        if log_dir is None:
            return
        yield from sorted(log_dir.glob("*.jsonl"))

    # ── Core algorithm: build attribution map (one pass over JSONL) ───────

    def _build_attribution_map(self) -> dict[str, dict[str, SessionAttribution]]:
        """Single pass over all JSONL files to attribute every assistant entry.

        Returns: {task_id: {session_id: SessionAttribution}}

        Per session, we walk entries chronologically:
        - Maintain `current_task` (the task "owning" the current segment)
        - When assistant entry seen AND current_task is set: attribute to it
        - When kanban command seen: update current_task to the referenced task

        An assistant entry that contains a kanban tool_use is attributed to
        the NEW task (the one the command references), since the command
        initiates a new segment.

        Ownership release conditions (prevent inflated attribution):
        - 30-min idle: no kanban command in the last 30 min → release
        - Archive signal: `kanban decide --action approve_and_archive` or
          `kanban clean TASK-NNN` → release immediately
        """
        from datetime import datetime, timedelta, timezone

        attribution: dict[str, dict[str, SessionAttribution]] = {}

        for path in self._iter_jsonl_files():
            session_id = path.stem  # filename without .jsonl
            current_task: str | None = None
            last_cmd_ts: datetime | None = None
            try:
                with path.open(encoding="utf-8") as f:
                    for line in f:
                        try:
                            entry = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if entry.get("type") != "assistant":
                            continue

                        ts_str = entry.get("timestamp", "")
                        ts_dt = _parse_ts(ts_str)

                        # Release ownership if idle too long (avoids absorbing
                        # unrelated later activity into a finished task).
                        if (
                            current_task
                            and last_cmd_ts
                            and ts_dt
                            and (ts_dt - last_cmd_ts).total_seconds()
                            > _IDLE_RELEASE_SECONDS
                        ):
                            current_task = None
                            last_cmd_ts = None

                        # Extract ALL kanban sub-commands in this entry.
                        # A single Bash tool_use may contain a multi-line
                        # script running N kanban calls (for-loop, &&, ;).
                        # Each counts toward command_count; the LAST task
                        # referenced wins ownership for the entry's LLM call.
                        sub_cmds = _extract_kanban_commands(entry)
                        if sub_cmds:
                            for sc in sub_cmds:
                                if _is_archive_signal(sc):
                                    current_task = None
                                    last_cmd_ts = None
                                    break
                                tid = _find_task_id(sc)
                                if tid:
                                    current_task = tid
                                    last_cmd_ts = ts_dt or last_cmd_ts

                        if current_task is None:
                            continue

                        # Attribute this assistant entry to current_task
                        attribution.setdefault(current_task, {})
                        if session_id not in attribution[current_task]:
                            attribution[current_task][session_id] = SessionAttribution(
                                session_id=session_id
                            )
                        attr = attribution[current_task][session_id]
                        # Count every kanban sub-command, not just the entry.
                        # Critical for accurate attribution when users batch
                        # mark-step calls via `for` loops.
                        attr.command_count += len(sub_cmds)
                        _tally_into_attr(entry, attr)
            except (OSError, UnicodeDecodeError):
                continue
        return attribution

    # ── Per-task stats ────────────────────────────────────────────────────

    def get_task_stats(self, task_id: str) -> TaskLLMStats:
        """Aggregate LLM calls attributable to one task.

        Uses two-step algorithm (region + API filter) for accurate counts.
        Callers that need command-segment granularity use get_task_breakdown().
        """
        stats = TaskLLMStats(task_id=task_id)
        if not task_id or not task_id.startswith("TASK-"):
            return stats

        # Delegate to two-step algorithm, then populate TaskLLMStats object
        data = self.get_task_api_calls(task_id)
        stats.total_calls = data.get("total_calls", 0)
        stats.main_agent_calls = data.get("main_agent_calls", 0)
        stats.sub_agent_calls = data.get("sub_agent_calls", 0)
        tokens = data.get("tokens", {})
        stats.input_tokens = tokens.get("input", 0)
        stats.output_tokens = tokens.get("output", 0)
        stats.cache_read_tokens = tokens.get("cache_read", 0)
        stats.sessions_count = data.get("sessions_count", 0)
        stats.first_activity_at = data.get("first_activity_at", "")
        stats.last_activity_at = data.get("last_activity_at", "")
        stats.kanban_commands = data.get("kanban_commands", 0)
        stats.models = data.get("models", {})
        return stats

    # ── Per-task breakdown ───────────────────────────────────────────────

    def get_task_breakdown(self, task_id: str) -> dict:
        """Return per-command-segment breakdown for one task.

        For each kanban CLI command that referenced this task, count the
        assistant entries (LLM calls) that happened between it and the
        next kanban command for ANY task. Helps identify which commands
        triggered expensive work.

        Returns:
            {
                "task_id": str,
                "segments": [
                    {
                        "index": int,
                        "timestamp": str,
                        "command": str,        # truncated for readability
                        "calls": int,          # LLM calls in this segment
                        "input_tokens": int,
                        "output_tokens": int,
                        "cache_read_tokens": int,
                    },
                    ...
                ],
                "total_calls": int,
                "total_tokens": int,
                "average_calls_per_segment": float,
                "max_segment_calls": int,
                "max_segment_command": str,
            }
        """
        breakdown: dict = {
            "task_id": task_id,
            "segments": [],
            "total_calls": 0,
            "total_tokens": 0,
            "average_calls_per_segment": 0.0,
            "max_segment_calls": 0,
            "max_segment_command": "",
        }
        if not task_id or not task_id.startswith("TASK-"):
            return breakdown

        segments: list[dict] = []
        from datetime import datetime, timedelta

        for path in self._iter_jsonl_files():
            current: dict | None = None  # reset per session file
            last_cmd_ts = None
            try:
                with path.open(encoding="utf-8") as f:
                    for line in f:
                        try:
                            entry = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if entry.get("type") != "assistant":
                            continue

                        ts_str = entry.get("timestamp", "")
                        ts_dt = _parse_ts(ts_str)

                        # Idle release
                        if (
                            current
                            and last_cmd_ts
                            and ts_dt
                            and (ts_dt - last_cmd_ts).total_seconds()
                            > _IDLE_RELEASE_SECONDS
                        ):
                            segments.append(current)
                            current = None
                            last_cmd_ts = None

                        sub_cmds = _extract_kanban_commands(entry)
                        msg = entry.get("message", {})
                        usage = msg.get("usage", {}) or {}
                        in_tok = int(usage.get("input_tokens", 0) or 0)
                        out_tok = int(usage.get("output_tokens", 0) or 0)
                        cache_tok = int(usage.get("cache_read_input_tokens", 0) or 0)

                        entry_handled = False  # set True if this entry started/closed a segment
                        if sub_cmds:
                            # Process all sub-commands; LAST matching task_id wins
                            # for segment routing.
                            for sc in sub_cmds:
                                if _is_archive_signal(sc):
                                    if current:
                                        segments.append(current)
                                    current = None
                                    last_cmd_ts = None
                                    entry_handled = True
                                    break
                                tid = _find_task_id(sc)
                                if tid == task_id:
                                    if current:
                                        segments.append(current)
                                    current = {
                                        "index": len(segments) + 1,
                                        "timestamp": ts_str,
                                        "command": sc[:80],
                                        "calls": 1,
                                        "input_tokens": in_tok,
                                        "output_tokens": out_tok,
                                        "cache_read_tokens": cache_tok,
                                        "sub_command_count": len(sub_cmds),
                                    }
                                    last_cmd_ts = ts_dt
                                    entry_handled = True
                                    break  # one entry = one segment
                                elif tid and tid != task_id:
                                    if current:
                                        segments.append(current)
                                    current = None
                                    last_cmd_ts = None
                                    entry_handled = True
                                    break

                        # Only add to current segment if entry didn't start/close one
                        if not entry_handled and current is not None:
                            current["calls"] += 1
                            current["input_tokens"] += in_tok
                            current["output_tokens"] += out_tok
                            current["cache_read_tokens"] += cache_tok
            except (OSError, UnicodeDecodeError):
                continue

            # End of file: close any open segment
            if current:
                segments.append(current)
                current = None

        total_calls = sum(s["calls"] for s in segments)
        total_tokens = sum(s["input_tokens"] + s["output_tokens"] for s in segments)
        max_seg = max(segments, key=lambda x: x["calls"]) if segments else None

        breakdown["segments"] = segments
        breakdown["total_calls"] = total_calls
        breakdown["total_tokens"] = total_tokens
        breakdown["average_calls_per_segment"] = (
            round(total_calls / len(segments), 1) if segments else 0.0
        )
        if max_seg:
            breakdown["max_segment_calls"] = max_seg["calls"]
            breakdown["max_segment_command"] = max_seg["command"]
        return breakdown

    # ── Framework issues scan ─────────────────────────────────────────────

    # Error patterns to scan for in tool_result content
    _ERROR_PATTERNS = [
        re.compile(r'"success"\s*:\s*false', re.IGNORECASE),
        re.compile(r'Traceback \(most recent call last\)'),
        re.compile(r'GuardError|guard check failed', re.IGNORECASE),
        re.compile(r'AttributeError|TypeError|NameError|ValueError|KeyError'),
        re.compile(r'WARNING:.*guard|WARNING:.*failed|WARNING:.*missing', re.IGNORECASE),
    ]

    def get_task_issues(self, task_id: str) -> dict:
        """Scan JSONL logs for framework-level issues during a task's execution.

        Pure read-only analysis of Claude Code JSONL — zero LLM cost.
        Walks the same attribution windows as get_task_stats, but inspects
        tool_result content for error patterns instead of counting calls.

        Returns:
            {
                "task_id": str,
                "total_issues": int,
                "issues": [
                    {
                        "timestamp": str,
                        "session_id": str,
                        "severity": "error" | "warning",
                        "type": "cli_error" | "traceback" | "guard_error" | "exception" | "warning",
                        "message": str (first 200 chars),
                        "kanban_command": str | None (the command that triggered it),
                    }
                ],
                "summary": {
                    "errors": int,
                    "warnings": int,
                    "unique_types": list[str],
                }
            }
        """
        result: dict = {
            "task_id": task_id,
            "total_issues": 0,
            "issues": [],
            "summary": {"errors": 0, "warnings": 0, "unique_types": []},
        }
        if not task_id or not task_id.startswith("TASK-"):
            return result

        # Reuse attribution map to know which sessions/timestamps belong to task
        amap = self._build_attribution_map()
        task_sessions = amap.get(task_id, {})
        if not task_sessions:
            return result

        # Build timestamp windows per session
        windows = {
            sid: (attr.first_ts, attr.last_ts)
            for sid, attr in task_sessions.items()
        }

        seen_types: set[str] = set()

        for path in self._iter_jsonl_files():
            session_id = path.stem
            try:
                with path.open(encoding="utf-8") as f:
                    prev_cmd = None
                    for line in f:
                        try:
                            entry = json.loads(line)
                        except json.JSONDecodeError:
                            continue

                        # Track kanban commands from assistant entries
                        if entry.get("type") == "assistant":
                            sub_cmds = _extract_kanban_commands(entry)
                            if sub_cmds:
                                for sc in sub_cmds:
                                    if _find_task_id(sc) == task_id:
                                        prev_cmd = _short_cmd(sc)
                            continue

                        # Check tool_result in user entries for error patterns
                        if entry.get("type") != "user":
                            continue
                        sid = entry.get("sessionId", "")
                        if sid not in windows:
                            continue
                        ts = entry.get("timestamp", "")
                        first_ts, last_ts = windows[sid]
                        if not (first_ts <= ts <= last_ts):
                            continue

                        # Extract tool_result content
                        content = entry.get("message", {}).get("content", "")
                        if isinstance(content, list):
                            # Flatten list-of-blocks (tool_result with content array)
                            parts = []
                            for block in content:
                                if isinstance(block, dict):
                                    t = block.get("text") or block.get("content") or ""
                                    if isinstance(t, str):
                                        parts.append(t)
                                elif isinstance(block, str):
                                    parts.append(block)
                            content = "\n".join(parts)
                        if not isinstance(content, str) or not content:
                            continue

                        # Scan for error patterns
                        for pat in self._ERROR_PATTERNS:
                            m = pat.search(content)
                            if not m:
                                continue
                            matched = m.group(0)
                            # Classify
                            if "success" in matched.lower():
                                issue_type, severity = "cli_error", "error"
                            elif "Traceback" in matched:
                                issue_type, severity = "traceback", "error"
                            elif "guard" in matched.lower():
                                issue_type, severity = "guard_error", "error"
                            elif "Warning" in matched:
                                issue_type, severity = "warning", "warning"
                            else:
                                issue_type, severity = "exception", "error"

                            # Extract surrounding context (first 200 chars around match)
                            start = max(0, m.start() - 50)
                            end = min(len(content), m.end() + 150)
                            snippet = content[start:end].replace("\n", " ").strip()[:200]

                            result["issues"].append({
                                "timestamp": ts,
                                "session_id": sid[:12],
                                "severity": severity,
                                "type": issue_type,
                                "message": snippet,
                                "kanban_command": prev_cmd,
                            })
                            seen_types.add(issue_type)
                            if severity == "error":
                                result["summary"]["errors"] += 1
                            else:
                                result["summary"]["warnings"] += 1
                            break  # one issue per entry, don't double-count
            except (OSError, UnicodeDecodeError):
                continue

        # Deduplicate: same message + type within 5 seconds = same issue
        result["issues"] = _dedupe_issues(result["issues"])
        result["total_issues"] = len(result["issues"])
        result["summary"]["unique_types"] = sorted(seen_types)
        return result

    def export_task_logs(self, task_id: str, output_dir: Path) -> dict:
        """Export ALL log data for a task to output_dir for offline analysis.

        Creates 5 files:
          llm_stats.json       — calls/tokens/models breakdown
          breakdown.json       — per-command-segment detail
          framework_issues.json — error/exception scan results
          raw_jsonl.jsonl       — every JSONL line attributed to this task
          summary.md            — human-readable combined report

        Returns dict with file paths + counts.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        files_written: dict[str, str] = {}

        # 1. LLM stats
        stats = self.get_task_stats(task_id)
        stats_path = output_dir / "llm_stats.json"
        stats_path.write_text(
            json.dumps(stats.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        files_written["llm_stats"] = str(stats_path)

        # 2. Breakdown
        breakdown = self.get_task_breakdown(task_id)
        bd_path = output_dir / "breakdown.json"
        bd_path.write_text(
            json.dumps(breakdown, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        files_written["breakdown"] = str(bd_path)

        # 3. Framework issues
        issues = self.get_task_issues(task_id)
        issues_path = output_dir / "framework_issues.json"
        issues_path.write_text(
            json.dumps(issues, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        files_written["framework_issues"] = str(issues_path)

        # 4. Raw JSONL — every entry in the task's attribution windows
        amap = self._build_attribution_map()
        task_sessions = amap.get(task_id, {})
        raw_lines: list[str] = []
        if task_sessions:
            windows = {
                sid: (attr.first_ts, attr.last_ts)
                for sid, attr in task_sessions.items()
            }
            for path in self._iter_jsonl_files():
                session_id = path.stem
                if session_id not in windows:
                    continue
                first_ts, last_ts = windows[session_id]
                try:
                    with path.open(encoding="utf-8") as f:
                        for line in f:
                            try:
                                entry = json.loads(line)
                            except json.JSONDecodeError:
                                continue
                            ts = entry.get("timestamp", "")
                            if first_ts <= ts <= last_ts:
                                raw_lines.append(line.rstrip("\n"))
                except (OSError, UnicodeDecodeError):
                    continue
        raw_path = output_dir / "raw_jsonl.jsonl"
        raw_path.write_text("\n".join(raw_lines), encoding="utf-8")
        files_written["raw_jsonl"] = str(raw_path)

        # 5. Summary markdown — human-readable combined report
        summary_lines = [
            f"# Task Log Export — {task_id}",
            "",
            f"> Generated: {time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime())}",
            "",
            "## LLM 调用统计",
            "",
            f"| 指标 | 值 |",
            f"|------|-----|",
            f"| 总调用 | {stats.total_calls} |",
            f"| Kanban 命令 | {stats.kanban_commands} |",
            f"| Sessions | {stats.sessions_count} |",
            f"| Tokens (in+out) | {stats.input_tokens + stats.output_tokens:,} |",
            f"| Cache tokens | {stats.cache_read_tokens:,} |",
            f"| 模型 | {', '.join(f'{m}({n})' for m, n in stats.models.items())} |",
            f"| 首次活动 | {stats.first_activity_at} |",
            f"| 末次活动 | {stats.last_activity_at} |",
            "",
        ]
        # Breakdown summary
        if breakdown.get("segments"):
            summary_lines.extend([
                "## 命令段细分",
                "",
                f"| # | Calls | Tokens | 命令 |",
                f"|---|-------|--------|------|",
            ])
            for seg in breakdown["segments"]:
                tokens = seg.get("input_tokens", 0) + seg.get("output_tokens", 0)
                summary_lines.append(
                    f"| {seg['index']} | {seg['calls']} | {tokens:,} | {seg['command'][:50]} |"
                )
            summary_lines.append("")
        # Issues summary
        if issues.get("issues"):
            summary_lines.extend([
                "## 框架问题",
                "",
                f"| 严重度 | 类型 | 消息 |",
                f"|--------|------|------|",
            ])
            for iss in issues["issues"]:
                summary_lines.append(
                    f"| {iss['severity']} | {iss['type']} | {iss['message'][:80]} |"
                )
            summary_lines.append("")
        else:
            summary_lines.extend(["## 框架问题", "", "✓ 无框架问题检测到", ""])
        # Raw JSONL summary
        summary_lines.extend([
            "## 原始日志",
            "",
            f"- `{raw_path.name}`: {len(raw_lines)} 条 JSONL 记录",
            f"- 详见同目录下的 JSON / JSONL 文件",
            "",
        ])
        summary_path = output_dir / "summary.md"
        summary_path.write_text("\n".join(summary_lines), encoding="utf-8")
        files_written["summary"] = str(summary_path)

        return {
            "task_id": task_id,
            "output_dir": str(output_dir),
            "files": files_written,
            "raw_jsonl_lines": len(raw_lines),
            "total_issues": issues.get("total_issues", 0),
            "total_llm_calls": stats.total_calls,
        }

    def _entry_mentions_task(self, entry: dict, task_id: str) -> bool:
        """Check if an entry references task_id anywhere (command, content, prompt).

        Broader than kanban CLI command matching — catches cases where
        the agent discusses the task in text without running a kanban command.
        """
        # Quick check on raw line for TASK-NNN string
        text = json.dumps(entry, ensure_ascii=False)
        return task_id in text

    def get_task_api_calls(self, task_id: str) -> dict:
        """Two-step accurate API call counting (v0.192 hybrid algorithm).

        Step 1: Task Region Detection (assistant-only mentions)
            Scan ASSISTANT entries for TASK-NNN in tool_use commands.
            User entries (tool_results) are excluded — they echo CLI output
            that may contain OTHER task_ids, causing window overlap (#652).

        Step 2: API Call Filtering
            Within the task region, count entries with real model usage.

        Returns same shape as TaskLLMStats.to_dict() for compatibility.
        """
        stats = TaskLLMStats(task_id=task_id)
        if not task_id or not task_id.startswith("TASK-"):
            return stats.to_dict()

        # Step 1: Find task region per session
        # ONLY scan assistant entries (tool_use), NOT user entries (tool_results).
        # This prevents benchmark output (which lists multiple task_ids) from
        # inflating the region window.
        task_windows: dict[str, tuple[str, str]] = {}

        for path in self._iter_jsonl_files():
            session_id = path.stem
            first_ts = None
            last_ts = None
            try:
                with path.open(encoding="utf-8") as f:
                    for line in f:
                        try:
                            entry = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        # Only assistant entries can actively reference a task
                        # via tool_use (kanban commands). User entries echo
                        # tool_results which contain output from commands that
                        # may list multiple task_ids (#652).
                        if entry.get("type") != "assistant":
                            continue
                        # Check if this assistant entry references task_id
                        # in a tool_use command (not just any text mention)
                        sub_cmds = _extract_kanban_commands(entry)
                        mentions_task = False
                        if sub_cmds:
                            for sc in sub_cmds:
                                if task_id in sc:
                                    mentions_task = True
                                    break
                        if not mentions_task:
                            continue
                        ts = entry.get("timestamp", "")
                        if not ts:
                            continue
                        if not first_ts or ts < first_ts:
                            first_ts = ts
                        if not last_ts or ts > last_ts:
                            last_ts = ts
            except (OSError, UnicodeDecodeError):
                continue
            if first_ts and last_ts:
                task_windows[session_id] = (first_ts, last_ts)

        if not task_windows:
            return stats.to_dict()

        # Step 2: Within task region, count only real API calls
        stats.sessions_count = len(task_windows)
        all_ts: list[str] = []

        for path in self._iter_jsonl_files():
            session_id = path.stem
            if session_id not in task_windows:
                continue
            first_ts, last_ts = task_windows[session_id]
            try:
                with path.open(encoding="utf-8") as f:
                    for line in f:
                        try:
                            entry = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if entry.get("type") != "assistant":
                            continue
                        ts = entry.get("timestamp", "")
                        if not (first_ts <= ts <= last_ts):
                            continue

                        # Step 2 filter: only real API calls
                        msg = entry.get("message", {})
                        if not isinstance(msg, dict):
                            continue
                        usage = msg.get("usage", {})
                        if not usage or not isinstance(usage, dict):
                            continue

                        inp = int(usage.get("input_tokens", 0) or 0)
                        out = int(usage.get("output_tokens", 0) or 0)
                        if inp == 0 and out == 0:
                            continue

                        model = msg.get("model", "unknown")
                        cache = int(usage.get("cache_read_input_tokens", 0) or 0)

                        stats.total_calls += 1
                        if entry.get("isSidechain"):
                            stats.sub_agent_calls += 1
                        else:
                            stats.main_agent_calls += 1
                        stats.models[model] = stats.models.get(model, 0) + 1
                        stats.input_tokens += inp
                        stats.output_tokens += out
                        stats.cache_read_tokens += cache

                        sub_cmds = _extract_kanban_commands(entry)
                        if sub_cmds:
                            stats.kanban_commands += len(sub_cmds)

                        if ts:
                            all_ts.append(ts)
            except (OSError, UnicodeDecodeError):
                continue

        if all_ts:
            stats.first_activity_at = min(all_ts)
            stats.last_activity_at = max(all_ts)

        result = stats.to_dict()
        result["algorithm"] = "hybrid_assistant_region_filter"
        result["method"] = (
            "Step 1: task region by ASSISTANT tool_use mentions only (not tool_results); "
            "Step 2: filter to real API calls (usage > 0)"
        )
        return result

    # ── Per-mode stats ────────────────────────────────────────────────────

    def get_mode_stats(self) -> dict[str, ModeLLMStats]:
        tasks_by_mode: dict[str, list[str]] = defaultdict(list)
        scan_dirs = [
            self._project_root / ".kanban" / "tasks",
            self._project_root / ".kanban" / "archive",
        ]
        if not any(d.is_dir() for d in scan_dirs):
            return {}

        for tasks_dir in scan_dirs:
            if not tasks_dir.is_dir():
                continue
            for task_dir in tasks_dir.iterdir():
                if not task_dir.is_dir():
                    continue
                task_json = task_dir / "task.json"
                if not task_json.is_file():
                    continue
                try:
                    data = json.loads(task_json.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError):
                    continue
                mode = data.get("mode") or "unknown"
                tasks_by_mode[mode].append(task_dir.name)

        amap = self._build_attribution_map()
        result: dict[str, ModeLLMStats] = {}
        for mode, task_ids in tasks_by_mode.items():
            mode_stat = ModeLLMStats(mode=mode)
            for tid in task_ids:
                sessions = amap.get(tid, {})
                if not sessions:
                    continue
                mode_stat.task_count += 1
                for attr in sessions.values():
                    mode_stat.total_calls += attr.assistant_calls
                    mode_stat.main_agent_calls += attr.main_calls
                    mode_stat.sub_agent_calls += attr.sub_calls
                    mode_stat.input_tokens += attr.input_tokens
                    mode_stat.output_tokens += attr.output_tokens
                    mode_stat.cache_read_tokens += attr.cache_read_tokens
            result[mode] = mode_stat
        return result

    # ── Discovery ─────────────────────────────────────────────────────────

    def list_attributable_tasks(self) -> dict[str, int]:
        """Return {task_id: total_attributed_calls} for tasks with >0 calls."""
        amap = self._build_attribution_map()
        return {
            tid: sum(a.assistant_calls for a in sessions.values())
            for tid, sessions in amap.items()
        }


# ── Helpers ────────────────────────────────────────────────────────────────


def _extract_kanban_commands(entry: dict) -> list[str]:
    """Return ALL kanban sub-commands invoked by this assistant entry.

    A single Bash tool_use may contain a multi-line script that runs
    multiple kanban calls (e.g., `for step in ...; do kanban mark-step ...; done`
    or `kanban workflow next-step TASK-A && kanban workflow mark-step TASK-A`).
    This function extracts each kanban invocation as a separate string.

    Returns:
        List of kanban sub-command strings (e.g.,
        ["workflow next-step TASK-001", "workflow mark-step TASK-001 plan.A"]).
        Empty list if the entry has no kanban tool_use.

    The returned strings are the SUB-COMMAND portion (without `kanban` prefix
    or `python -m kanban_framework` wrapper), suitable for attribution and
    breakdown display.
    """
    content = entry.get("message", {}).get("content", [])
    if not isinstance(content, list):
        return []
    sub_cmds: list[str] = []
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") != "tool_use":
            continue
        inp = block.get("input")
        if not isinstance(inp, dict):
            continue
        cmd = inp.get("command")
        if not isinstance(cmd, str):
            continue
        # Fast check: any kanban reference at all?
        if not any(pat.search(cmd) for pat in _KANBAN_CMD_PATTERNS):
            continue
        # Extract each individual sub-command via the more precise regex
        for m in _KANBAN_SUBCMD_RE.finditer(cmd):
            sub_cmds.append(m.group(1).strip())
    return sub_cmds


def _extract_kanban_command(entry: dict) -> str | None:
    """Backward-compat: return the FULL bash command string if entry has any
    kanban invocation. Prefer `_extract_kanban_commands` for accurate counts.
    """
    content = entry.get("message", {}).get("content", [])
    if not isinstance(content, list):
        return None
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") != "tool_use":
            continue
        inp = block.get("input")
        if not isinstance(inp, dict):
            continue
        cmd = inp.get("command")
        if not isinstance(cmd, str):
            continue
        if any(pat.search(cmd) for pat in _KANBAN_CMD_PATTERNS):
            return cmd
    return None


def _find_task_id(command: str) -> str | None:
    """Extract the first TASK-NNNN reference from a kanban CLI command."""
    m = _TASK_ID_RE.search(command)
    return m.group(1) if m else None


def _dedupe_issues(issues: list[dict]) -> list[dict]:
    """Remove duplicate issues: same type + similar message within 5 seconds."""
    if not issues:
        return issues
    result: list[dict] = []
    for issue in issues:
        is_dup = False
        for existing in result[-5:]:  # check last 5
            if (
                existing["type"] == issue["type"]
                and existing["message"][:80] == issue["message"][:80]
            ):
                is_dup = True
                break
        if not is_dup:
            result.append(issue)
    return result


def _short_cmd(cmd: str) -> str:
    """Extract the kanban portion from a multi-line bash script for readability.

    Looks for `kanban ...` or `kanban_framework ...` and returns the first
    3-4 tokens following it (subcommand + args), truncated to 80 chars.
    """
    for line in cmd.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.search(
            r"(kanban(?:_framework)?\s+(?:--?\S+\s+)*[\w\d./-]+(?:\s+[\w\d./-]+){0,4})",
            line,
        )
        if m:
            return m.group(1).strip()[:80]
    return cmd.strip().split("\n")[0][:80]


def _tally_into_attr(entry: dict, attr: SessionAttribution) -> None:
    """Extract model + tokens from an assistant entry into SessionAttribution."""
    msg = entry.get("message", {})
    if not isinstance(msg, dict):
        return
    model = msg.get("model", "unknown")
    usage = msg.get("usage", {}) or {}

    attr.assistant_calls += 1
    if entry.get("isSidechain"):
        attr.sub_calls += 1
    else:
        attr.main_calls += 1
    attr.models[model] = attr.models.get(model, 0) + 1
    attr.input_tokens += int(usage.get("input_tokens", 0) or 0)
    attr.output_tokens += int(usage.get("output_tokens", 0) or 0)
    attr.cache_read_tokens += int(usage.get("cache_read_input_tokens", 0) or 0)

    ts = entry.get("timestamp", "")
    if ts:
        if not attr.first_ts or ts < attr.first_ts:
            attr.first_ts = ts
        if not attr.last_ts or ts > attr.last_ts:
            attr.last_ts = ts


# Backward-compat helper retained for tests that import it directly
def _tally_assistant(entry: dict, stats: TaskLLMStats) -> None:
    msg = entry.get("message", {})
    if not isinstance(msg, dict):
        return
    model = msg.get("model", "unknown")
    usage = msg.get("usage", {}) or {}
    stats.total_calls += 1
    if entry.get("isSidechain"):
        stats.sub_agent_calls += 1
    else:
        stats.main_agent_calls += 1
    stats.models[model] = stats.models.get(model, 0) + 1
    stats.input_tokens += int(usage.get("input_tokens", 0) or 0)
    stats.output_tokens += int(usage.get("output_tokens", 0) or 0)
    stats.cache_read_tokens += int(usage.get("cache_read_input_tokens", 0) or 0)
