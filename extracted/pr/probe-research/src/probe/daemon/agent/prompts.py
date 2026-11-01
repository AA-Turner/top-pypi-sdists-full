"""the tool descriptions and Probe MCP guide each agent's model reads."""

from __future__ import annotations
import os
from typing import Any
from pydantic_ai import RunContext
from probe.daemon.agent import toolset, tools
# The Probe MCP's address, shared with the CLI's `probe mcp tools|call` (`/probe inline`).
from probe.sdk.settings.settings import STOCK_MCP_URL, mcp_url  # noqa: F401 -- STOCK_MCP_URL re-exported

#: The `shell` tool's description, as the researcher wrote it.
SHELL_DESCRIPTION = (
    "Run a generic bash command in the session's working folders. \n"
    "\n"
    " - Commands are checked against a safe list: a safe command runs at once, anything else waits for the "
    "researcher's yes (in bypass mode, it runs)\n"
    " - Commands are chainable (`cd x && probe ...`, `probe ... | jq ...`)\n"
    " - `why`: one line on why you run it."
)

#: The writer's `bash` command map (`toolset.command_map`), after a blank line
#: under the tool's description: only the skills folder's path; its commands are
#: in track-work's `versions/commands.writer.md` (`bite.writer_skill`; thin
#: harness, fat skills, 10-19). Wording NEW
#: (fixtures/daemon_prompts/tools/bash-command-map.NEW.md); `{skills}` is the
#: skills folder.
COMMAND_MAP = "The skills folder: `{skills}`."
#: The reader's `bash` (NEW, fixtures/daemon_prompts/reads/tools/bash.NEW.md). Its
#: job text names `probe feedback send` and `probe daemon session open`.
READER_BASH_DESCRIPTION = (
    "Run a read-only bash command in the session's working folders; anything off the safe list is refused. "
    "Chainable (`cd x && probe ...`, `probe ... | jq ...`). `why`: one line on why you run it.")
READER_COMMAND_MAP = (
    "Read: `cat <path>`; a data file: `probe file preview <path>`; a note, whole or the paragraphs that mention some "
    "words: `probe notes show|find --project|--experiment|--run <slug> [--note <title>] [<words>]`; the session: "
    "`probe daemon session open|outline|search|logbook`; Probe's records: `probe mcp call <tool> '<json>'` "
    "(`probe mcp tools` lists them).")
#: The audit's (NEW, fixtures/daemon_prompts/tools/audit-command-map.NEW.md).
AUDIT_COMMAND_MAP = (
    "Read: `cat <path>`; a data file: `probe file preview <path>`; Probe's records: `probe mcp call <tool> '<json>'` "
    "(`probe mcp tools` lists them).")
#: The paragraph after the reader's command map while tasks are on
#: (`toolset.tasks`; NEW, fixtures/daemon_prompts/tools/task-command.NEW.md). The
#: heredoc, never `probe daemon task "<question>"`: a question with a backtick or
#: `$` in double quotes is refused. The writer's is track-work's
#: `versions/task.writer.md` (`bite.writer_skill`).
TASK_CLAUSE = ("A big read: `probe daemon task` (it only reads; only its answer comes back):\n"
               "```bash\nprobe daemon task <<'EOF'\n<question>\nEOF\n```")
#: The last paragraph of every `bash` description while calls run together
#: (`toolset.parallel`; NEW, fixtures/daemon_prompts/tools/parallel.NEW.md).
PARALLEL_LINE = "Calls in one response that only read run together (up to 4); a write runs alone, in the order sent."


def bash_description(base: str, command_map: str, *, tasks: bool = False) -> str:
    """A `bash` tool's description: `base`, the command map unless it is off
    (then TASK_CLAUSE when `tasks` and tasks are on), and PARALLEL_LINE while
    calls run together, each a paragraph."""
    text = base
    if toolset.command_map():
        from probe.daemon.worker.bite.bite import skills_root

        text += f"\n\n{command_map.replace('{skills}', str(skills_root() or '<skills folder>'))}"
        if tasks and toolset.tasks():
            text += f"\n\n{TASK_CLAUSE}"
    return f"{text}\n\n{PARALLEL_LINE}" if toolset.parallel() else text


def _native_mcp(capabilities: list, what: str, headers: dict | None = None) -> None:
    """Today's Probe MCP, loaded natively (the classic tool set only)."""
    try:
        from pydantic_ai.capabilities.mcp import MCP

        from probe.daemon.worker.env import probe_env

        env = probe_env("")
        key = env.get("PROBE_TOKEN", "")
        url = mcp_url(env.get("PROBE_BASE_URL", ""))
        if key and url and os.environ.get("PROBE_DAEMON_MCP", "1") != "0":
            # This computer's workspace limit rides every MCP request (the hosted
            # MCP forwards it), beside whatever the caller's own headers say.
            from probe.sdk.settings.workspace_limit import ambient_headers

            headers = {**(headers or {}), **ambient_headers(env.get("PROBE_BASE_URL") or None, bearer=key)}
            # Loaded from the start: no round to load it before the first read.
            extra = {"headers": headers} if headers else {}
            capabilities.append(MCP(url=url, authorization_token=f"Bearer {key}", id="probe", defer_loading=False,
                                    **extra))
    except Exception as exc:  # noqa: BLE001
        log.warning("Probe MCP unavailable%s: %s", what, exc)


def _mcp_guide(agent: Any) -> None:
    """The `bash` tool set: the Probe MCP's instructions in the agent's
    instructions, as the native MCP put them there (its tools are `probe mcp
    call`). Fetched once per process; none when the MCP cannot be reached."""

    @agent.instructions
    async def probe_mcp_instructions(ctx: RunContext[tools.Deps]) -> str:
        if ctx.deps is None or os.environ.get("PROBE_DAEMON_MCP", "1") == "0":
            return ""
        from probe.daemon.shell import local_commands

        return await local_commands.mcp_guide(ctx.deps)

#: The `read` tool's description.
READ_DESCRIPTION = (
    "Read a file - nothing runs. Any file in the session's working folders or the skills folder (e.g. "
    "`track-work/reference.md`).\n"
    "\n"
    "`offset` / `limit`: a range of lines (at most 2000). Neither: a preview of a CSV/TSV, JSON, Parquet or "
    "NumPy file. Never a pickle or an image."
)

#: The `edit` tool's description (ARTIFACT-PAGES P3). Wording NEW
#: (fixtures/daemon_prompts/tools/edit.NEW.md).
EDIT_DESCRIPTION = (
    "Change a checked-out summary or note draft in place. `path`: the draft (`probe summary checkout` or `probe "
    "notes checkout` printed it); `old`: text copied exactly from it, found once; `new`: its replacement.\n"
    "\n"
    "`read` that part first (`offset` / `limit`). `probe summary push` sends the draft: once a run, not per edit."
)

#: The `session` tool's description.
SESSION_DESCRIPTION = (
    "Look at the session, or your own record of it. `op` picks what:\n"
    "\n"
    "- `open` - one event in full (`event_id`), or a whole turn (`turn`); long text comes in pages (`page`).\n"
    "- `outline` - one line per turn (`page`).\n"
    "- `search` - words across the WHOLE session (`query`; narrow with `kind`, `turn_from`, `turn_to`).\n"
    "- `logbook` - words across your own past writes and lookups (`query`).\n"
    "- `status` - what is recorded, what failed or waits for the researcher, and how much of the session you "
    "have not been shown.\n"
    "\n"
    "Each `op` takes only its own options."
)
from probe.daemon.agent.guards import log  # noqa: E402 -- pieces need each other; the front door loads this one first
