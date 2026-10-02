"""The normalized events every harness adapter emits (daemon v2, D23).

The daemon's core sees only these: never a harness's raw line. Each event
carries a stable id (`<stream>:<offset>:<index>`), so a re-read of the same
bytes yields the same ids and the store ignores the duplicate.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field


class Kind(str, enum.Enum):
    PROMPT = "prompt"  # a person typed it
    AGENT_TEXT = "agent_text"
    AGENT_REASONING = "agent_reasoning"  # plain-text thinking, where the harness keeps it
    TOOL_CALL = "tool_call"
    TOOL_OUTPUT = "tool_output"  # inline text, or a pointer to a side file
    SUBAGENT = "subagent"  # a helper agent started (its own events follow on its stream)
    TURN_END = "turn_end"
    COMPACTION = "compaction"  # the harness summarised its context
    META = "meta"  # task notices and other user-role lines no person typed
    # Not from the harness: the daemon's own observations, queued like the rest.
    FILE_CHANGE = "file_change"  # the folder check found a new or changed file
    RUN_EVENT = "run_event"  # the SDK announced a run start / end over the local socket


MAIN_STREAM = "main"


@dataclass
class Event:
    kind: Kind
    stream: str
    offset: int  # end offset of the source line in its file
    index: int = 0  # position among the events of that line
    ts: str | None = None
    text: str = ""
    tool: str | None = None
    call_id: str | None = None
    tool_input: dict = field(default_factory=dict)
    is_error: bool = False
    side_file: str | None = None  # a persisted output's full text lives here (E4)
    parent: str | None = None  # a subagent's parent tool call
    cwd: str | None = None

    @property
    def event_id(self) -> str:
        return f"{self.stream}:{self.offset}:{self.index}"

    def command(self) -> str:
        """The shell command a tool call ran ("" for anything else)."""
        for key in ("command", "cmd", "input"):
            value = self.tool_input.get(key)
            if isinstance(value, str):
                return value
        return ""
