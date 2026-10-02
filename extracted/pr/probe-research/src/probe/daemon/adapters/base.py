"""The harness adapter contract (daemon v2, D23).

Everything harness-specific sits behind one `Adapter`: where the chat log and
its helper-agent logs live, how one raw line becomes normalized events, the
session facts (permission mode included), the instruction and memory files and
the question tool. The harness's hooks talk to the daemon through files, not
through the adapter (`plugins/probe-research/hooks/approvals_hook.py` writes the
permission mode and the answers; its SHIMS table carries the same facts).
The core reads normalized events and the `Capabilities` table and never a
harness name; `adapters.for_source` is the one place a name is looked up, and a
test fails on a harness name anywhere else in the core.

Adding a harness = one module here + three recorded, scrubbed fixtures + the
shared conformance suite (`agent/tests/test_daemon_adapter_conformance.py`).
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from probe.daemon.events import Event, Kind

#: Permission modes, normalized. `BYPASS` = the harness asks nothing (D22: the
#: daemon asks nothing either). `UNKNOWN` = the mode could not be read (the
#: daemon asks).
MODE_DEFAULT = "default"
MODE_BYPASS = "bypass"
MODE_UNKNOWN = "unknown"


@dataclass(frozen=True)
class Capabilities:
    """What a harness offers the daemon. The core branches on these, never on names."""

    watch_log: bool  # a chat log file the daemon can watch
    subagent_logs: bool
    hooks: bool  # start / end / prompt hooks
    inject_line: bool  # add one line to the agent's context at the next prompt
    question_tool: bool  # a question tool whose answer a hook can read
    permission_mode: bool  # the permission mode is visible (to hooks or in the log)
    instruction_files: tuple[str, ...] = ()
    #: Daemon reads: a `[Probe]` message can reach the agent after a tool call,
    #: mid-turn (not only at the next prompt).
    inject_tool: bool = False
    #: Daemon reads: a hook can wake the agent after its turn ended, to hand it
    #: the answer to an open ask (Claude Code's Stop hook with `asyncRewake`).
    wake: bool = False


@dataclass
class SessionFiles:
    main: Path
    subagents: list[Path] = field(default_factory=list)
    side_dir: Path | None = None  # where persisted outputs live


@dataclass
class ContextFile:
    """A harness file the daemon may open read-only (S7): data, never instructions."""

    label: str  # "project CLAUDE.md", "MEMORY.md", "skill: track-work"
    path: Path

    def describe(self) -> str:
        if self.path.is_dir():
            return self.label
        try:
            size = self.path.stat().st_size
        except OSError:
            return f"{self.label} (unreadable)"
        return f"{self.label} ~{max(1, size // 4 // 1000)}K tokens"


class Adapter:
    """Base class: subclasses fill in the harness-specific parts."""

    name: str = ""
    capabilities: Capabilities
    question_tool_name: str | None = None

    # -- reader --
    def session_files(self, transcript: Path) -> SessionFiles:
        return SessionFiles(main=transcript)

    def parse_line(self, obj: dict, *, stream: str, offset: int) -> list[Event]:
        raise NotImplementedError

    def parse_bytes(self, raw: bytes, *, stream: str, offset: int) -> list[Event]:
        try:
            obj = json.loads(raw)
        except ValueError:
            return []
        if not isinstance(obj, dict):
            return []
        events = self.parse_line(obj, stream=stream, offset=offset)
        for index, event in enumerate(events):
            event.index = index
        return events

    def subagent_event(self, path: Path) -> Event | None:
        """The SUBAGENT marker for a helper-agent log first seen at `path`."""
        return None

    # -- session facts --
    def permission_mode(self, obj: dict) -> str | None:
        """The mode a raw line announces, if it announces one."""
        return None

    # -- context (S7) --
    def context_files(self, cwd: Path, home: Path) -> list[ContextFile]:
        return []


# ---------------------------------------------------------------------------
# Shared helpers.
# ---------------------------------------------------------------------------

_PERSISTED_RE = re.compile(r"<persisted-output>.*?saved to:\s*(?P<path>\S+)", re.S)


def persisted_path(text: str, side_dir: Path | None = None) -> str | None:
    """A tool output the harness moved to a side file: its path (E4).

    The path is read from tool OUTPUT, which anything the agent ran can print,
    so it is kept only when it lands inside this session's own side folder
    (`side_dir`, symlinks and `..` resolved); with no side folder, never."""
    match = _PERSISTED_RE.search(text or "")
    if not match or side_dir is None:
        return None
    path = match.group("path")
    real = os.path.realpath(path)
    root = os.path.realpath(str(side_dir))
    return path if real.startswith(root.rstrip(os.sep) + os.sep) else None


def block_texts(content: object) -> list[str]:
    if isinstance(content, str):
        return [content]
    out: list[str] = []
    if isinstance(content, list):
        for block in content:
            if isinstance(block, str):
                out.append(block)
            elif isinstance(block, dict) and isinstance(block.get("text"), str):
                out.append(block["text"])
    return out


def existing(paths: Iterable[tuple[str, Path]]) -> list[ContextFile]:
    seen: set[Path] = set()
    found: list[ContextFile] = []
    for label, path in paths:
        try:
            resolved = path.resolve()
        except OSError:
            continue
        if resolved in seen or not path.is_file():
            continue
        seen.add(resolved)
        found.append(ContextFile(label, path))
    return found


def event(kind: Kind, stream: str, offset: int, **fields) -> Event:
    return Event(kind=kind, stream=stream, offset=offset, **fields)
