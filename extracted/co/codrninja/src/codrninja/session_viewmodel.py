"""Central state model for the TUI — all UI components read from here."""

from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ToolCallEntry:
    call_id: str
    tool_name: str
    args: dict[str, Any]
    step: int
    # filled in when result arrives
    output: str = ""
    success: Optional[bool] = None
    duration_ms: int = 0
    _started_at: float = field(default_factory=time.monotonic, repr=False)
    collapsed: bool = True

    def finish(self, output: str, success: bool) -> None:
        self.output = output
        self.success = success
        self.duration_ms = int((time.monotonic() - self._started_at) * 1000)


@dataclass
class ArtifactEntry:
    path: str
    action: str          # "modify" | "command"
    diff: str = ""
    status: str = ""     # git status letter e.g. "M", "A", "D"


@dataclass
class SessionViewModel:
    """
    Single source of truth for the TUI.
    All events from the agent are written here first,
    then the UI reacts to changes.
    """
    session_name: str
    model: str
    provider: str

    tool_calls: list[ToolCallEntry] = field(default_factory=list)
    artifacts: list[ArtifactEntry] = field(default_factory=list)
    terminal_lines: list[str] = field(default_factory=list)

    current_steps: int = 0
    max_steps: int = 50
    tokens: int = 0
    status: str = "ready"

    # ── tool event helpers ───────────────────────────────────────────────────

    def on_tool_start(self, call_id: str, tool_name: str, args: dict[str, Any], step: int) -> ToolCallEntry:
        entry = ToolCallEntry(call_id=call_id, tool_name=tool_name, args=args, step=step)
        self.tool_calls.append(entry)
        self.current_steps = step
        if tool_name == "execute_command":
            cmd = args.get("command", "")
            self.terminal_lines.append(f"$ {cmd}")
        return entry

    def on_tool_result(self, call_id: str, output: str, success: bool) -> Optional[ToolCallEntry]:
        for entry in self.tool_calls:
            if entry.call_id == call_id:
                entry.finish(output, success)
                if entry.tool_name == "execute_command":
                    for line in output.splitlines()[:50]:
                        self.terminal_lines.append(line)
                elif entry.tool_name in ("write_file", "edit_file") and success:
                    path = entry.args.get("path", "")
                    if path:
                        self._refresh_artifact(path, "modify")
                return entry
        return None

    def get_tool_call(self, call_id: str) -> Optional[ToolCallEntry]:
        for entry in self.tool_calls:
            if entry.call_id == call_id:
                return entry
        return None

    # ── artifact helpers ─────────────────────────────────────────────────────

    def _refresh_artifact(self, path: str, action: str) -> None:
        diff = self._git_diff(path)
        status = self._git_status_letter(path)
        for existing in self.artifacts:
            if existing.path == path:
                existing.diff = diff
                existing.status = status
                existing.action = action
                return
        self.artifacts.append(ArtifactEntry(path=path, action=action, diff=diff, status=status))

    def refresh_all_artifacts(self) -> None:
        """Call after any mutating tool to sync artifacts from git."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, timeout=5,
            )
            seen: set[str] = set()
            for line in result.stdout.splitlines():
                if len(line) < 4:
                    continue
                letter = line[1].strip() or line[0].strip()
                path = line[3:].strip()
                seen.add(path)
                diff = self._git_diff(path)
                updated = False
                for existing in self.artifacts:
                    if existing.path == path:
                        existing.diff = diff
                        existing.status = letter
                        updated = True
                        break
                if not updated:
                    self.artifacts.append(ArtifactEntry(path=path, action="modify", diff=diff, status=letter))
            # remove artifacts no longer in git status
            self.artifacts = [a for a in self.artifacts if a.path in seen]
        except Exception:
            pass

    @staticmethod
    def _git_diff(path: str) -> str:
        try:
            result = subprocess.run(
                ["git", "diff", "HEAD", "--", path],
                capture_output=True, text=True, timeout=5,
            )
            return result.stdout[:8000]
        except Exception:
            return ""

    @staticmethod
    def _git_status_letter(path: str) -> str:
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain", "--", path],
                capture_output=True, text=True, timeout=5,
            )
            line = result.stdout.strip()
            if len(line) >= 2:
                return line[1].strip() or line[0].strip()
        except Exception:
            pass
        return "M"