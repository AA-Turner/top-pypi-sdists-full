"""Which tools the daemon's agents get: ONE `bash` tool, or today's set.

    bash (default)   writer, reader and audit each get `bash` and their output
                     tool (`final_result`), nothing else. What the other tools
                     did is a command:
                       read     -> `cat` / `sed -n` / `head` / `tail` (the skills
                                   folder is on the safe list, read-only) and
                                   `probe file preview <path>` for a data file
                       edit     -> `probe draft edit <path>` with the change on
                                   stdin (`drafts.EDIT_FORMAT`)
                       session  -> `probe daemon session <op> ...`
                       feedback -> `probe feedback send "<text>"` (the reader)
                       Probe MCP-> `probe mcp call <tool> '<json>'`, `probe mcp tools`
                     The daemon answers those `probe` commands itself, in its own
                     process (`tools._local_command`), as it answers `probe daemon
                     override`: no CLI process, no key on a command line.
    classic          the set before this change: `shell`, `read`, `edit`,
                     `session` (the writer), `read`, `session`, `feedback` (the
                     reader), `shell`, `read` (the audit), each with the Probe MCP
                     loaded natively. The kill switch, and the bench's control arm
                     from the same tree.

`PROBE_DAEMON_TOOLS=classic` picks the old set; anything else is `bash`. Read at
call time: a test or the bench sets it per process.

`PROBE_DAEMON_COMMAND_MAP=0` leaves the one-line command map out of the `bash`
tool's description (`agent.COMMAND_MAP`); it is in by default.

`PROBE_DAEMON_PARALLEL=0` runs the `bash` calls of one model response one at a
time, in order, as before (`agent.CallOrder`); by default the calls that only
read run together (at most `agent.PARALLEL_READS` at once) and each call that
writes runs alone, in the order the model made it.

`PROBE_DAEMON_TASKS=0` turns `probe daemon task` off (`agent.run_task`): the
command answers that it is off, and no description, nor the writer's skill
(`bite.writer_skill`), names it.

The writer's commands are in its skill (track-work's `versions/commands.writer.md`),
shown only with the `bash` set (`bite.writer_skill`).
"""

from __future__ import annotations

import os

from probe._compat import StrEnum

TOOLS_ENV = "PROBE_DAEMON_TOOLS"
COMMAND_MAP_ENV = "PROBE_DAEMON_COMMAND_MAP"
PARALLEL_ENV = "PROBE_DAEMON_PARALLEL"
TASKS_ENV = "PROBE_DAEMON_TASKS"
_OFF = ("0", "off", "false", "no")


class Toolset(StrEnum):
    BASH = "bash"
    CLASSIC = "classic"


def current() -> Toolset:
    """The tool set this process runs with (`TOOLS_ENV`; default `bash`)."""
    raw = (os.environ.get(TOOLS_ENV) or "").strip().lower()
    return Toolset.CLASSIC if raw == Toolset.CLASSIC else Toolset.BASH


def bash_only() -> bool:
    return current() == Toolset.BASH


def command_map() -> bool:
    """Whether the `bash` description carries the command map (`COMMAND_MAP_ENV`)."""
    return (os.environ.get(COMMAND_MAP_ENV) or "1").strip().lower() not in _OFF


def parallel() -> bool:
    """Whether the `bash` calls of one response that only read run together
    (`PARALLEL_ENV`; default on). Only the `bash` tool set: the classic set keeps
    Pydantic AI's own `sequential` tools."""
    return bash_only() and (os.environ.get(PARALLEL_ENV) or "1").strip().lower() not in _OFF


def tasks() -> bool:
    """Whether `probe daemon task` runs (`TASKS_ENV`; default on). Only the `bash` tool set."""
    return bash_only() and (os.environ.get(TASKS_ENV) or "1").strip().lower() not in _OFF


#: The shell tool's name in each set.
def shell_tool() -> str:
    return "bash" if bash_only() else "shell"


def pick(classic: str, bash: str) -> str:
    """The text of the running set: `classic`'s words, or `bash`'s."""
    return bash if bash_only() else classic
