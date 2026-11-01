"""redact a command line by the argv rule (program kept, flags kept, values dropped)."""

from __future__ import annotations
import re
import shlex
from probe.shared.reports.reports import Scope


# ---------------------------------------------------------------------------
# The argv rule: a command line keeps its program and its flag names
# ---------------------------------------------------------------------------
# One rule for every command line a report or the debug log carries -- a
# process's argv, a config's `command`/`args`/`notify`, the service's facts:
#
#   * leading `NAME=value` words      -> `NAME=<arg>`
#   * the program (argv[0])           -> its basename, scrubbed; not a string -> `<arg>`
#   * a flag                          -> its NAME (`--json`, `-p`); `--x=v` -> `--x=<arg>`, `-pv` -> `-p<arg>`
#   * EVERY flag value and positional -> `<arg>`
#   * except, for a Python program, `-m probe` / `-m probe.<x>` (the module),
#     and ONE subcommand word: the first positional after the program (or after
#     a Probe module) with no flag before it, and only when it is one of
#     `PROBE_SUBCOMMANDS`.
#
# Nothing else is kept: a prompt (`claude -p "..."`, `probe ask "..."`), a
# password (`mysql -phunter2`), a model name alike.

#: What replaces every positional argument and flag value of a command line.
ARG = "<arg>"
#: The words a Probe command line may keep as its subcommand: the CLI's
#: top-level commands (`probe.cli.main.app`) and `probe.core.run`'s actions
#: (`ActionName`). `tests/test_core_report.py` derives the set from the code and
#: holds this copy to it (importing the CLI here would load all of it).
PROBE_SUBCOMMANDS = frozenset({
    "access-group", "agent-rules", "approvals", "artifact", "ask", "backfill", "bundle", "capy", "checkpoint",
    "codex_trust", "commits", "companion", "configure", "context", "coordinates", "daemon", "dataset", "deny", "desktop",
    "docs", "doctor", "draft", "edge", "events", "exec", "experiment", "feedback", "file", "flush", "get", "group",
    "ignore", "import", "install", "link", "log", "login", "logout", "mcp", "metrics", "notes", "outbox", "paper",
    "project", "provenance", "recorder", "repair", "report", "run", "series", "service", "session", "session_default",
    "setup", "shared", "snapshot", "snapshot-prune-refs", "snapshot-restore", "snapshot-show", "source", "span",
    "status", "statusline", "summary", "sync", "token", "trial", "uninstall", "update", "version", "views",
    "visuals", "wandb", "whoami", "wizard", "workspace", "workspace_limit",
})
#: `python`, `python3.12`, `pythonw.exe`: whose `-m <module>` names the program run.
_PYTHON = re.compile(r"^python[0-9.]*w?(\.exe)?$", re.IGNORECASE)
#: `-m probe` or `-m probe.<module>`.
_PROBE_MODULE = re.compile(r"^probe(\.[a-z_][a-z0-9_]*)*$")
#: A leading `NAME=value` word: an environment assignment before the program.
_ASSIGNMENT = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=")


def program_name(arg0: object, scope: Scope = Scope.LOCAL) -> str:
    """argv[0] as its program's basename, scrubbed: `/usr/local/bin/claude` ->
    `claude`, `C:\\Program Files\\nodejs\\node.exe` -> `node.exe` (one path,
    spaces and all). Not a string: `<arg>`."""
    if not isinstance(arg0, str):
        return ARG
    return re.split(r"[\\/]", scrub_for(arg0.strip(), scope))[-1] or ARG


def redact_argv(argv: list | tuple, scope: Scope | None = None) -> list[str]:
    """A command line by the argv rule (above). A one-word argv with spaces (a
    rewritten process title) is split; a real argv[0] never is."""
    scope = scope or Scope.LOCAL
    words = list(argv)
    if len(words) == 1 and isinstance(words[0], str) and len(words[0].split()) > 1:
        words = words[0].split()
    out = _leading_assignments(words)
    rest = words[len(out):]
    if not rest:
        return out
    program = program_name(rest[0], scope)
    return [*out, program, *redact_args(rest[1:], program=program)]


def redact_args(args: list | tuple, *, program: str = "") -> list[str]:
    """The arguments after the program by the argv rule; `program` is its name
    ("" for an MCP server's `args`, which keeps no subcommand)."""
    python = bool(_PYTHON.match(program))
    slot = program.lower() in ("probe", "probe.exe")  # the subcommand slot is open
    module_next = False
    out: list[str] = []
    for arg in args:
        if not isinstance(arg, str):
            out.append(ARG)
            slot = module_next = False
            continue
        if module_next:  # the word after a Python program's `-m`
            module_next = False
            if _PROBE_MODULE.match(arg):
                out.append(arg)
                slot = True
            else:
                out.append(ARG)
            continue
        if arg == "--":
            out.append(arg)
            slot = False
        elif arg.startswith("--"):
            name, eq, _value = arg.partition("=")
            out.append(f"{name}={ARG}" if eq else name)
            slot = False
        elif arg.startswith("-") and len(arg) > 1:
            out.append(arg[:2] if len(arg) == 2 else arg[:2] + ARG)  # `-phunter2`: a glued value
            module_next = python and arg == "-m"
            slot = False
        else:
            out.append(arg if slot and arg in PROBE_SUBCOMMANDS else ARG)
            slot = False
    return out


def _leading_assignments(words: list) -> list[str]:
    out = []
    for word in words:
        match = _ASSIGNMENT.match(word) if isinstance(word, str) else None
        if not match:
            break
        out.append(f"{match.group(1)}={ARG}")
    return out


def redact_command(value: str | list | tuple, *, program: bool, scope: Scope = Scope.LOCAL) -> str | list[str]:
    """A command in a config (`command`, `args`, Codex's `notify`) by the argv
    rule: a list keeps its shape (every item counts, numbers included); a
    string is split like a shell would (`shlex`, so a quoted value is one
    word) and rejoined. `args` (`program` False) has no program word."""
    if isinstance(value, str):
        try:
            words: list = shlex.split(value)
        except ValueError:
            words = value.split()
    else:
        words = list(value)
    if program:
        out = redact_argv(words, scope) if words else []
    else:
        out = redact_args(words)
    return " ".join(out) if isinstance(value, str) else out
from probe.shared.reports.scrub import scrub_for  # noqa: E402 -- pieces need each other; the front door loads this one first
