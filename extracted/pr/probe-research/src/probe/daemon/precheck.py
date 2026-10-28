"""The checks before the daemon runs a `probe` command (daemon v2, D14 / D18).

The daemon records with the same `probe` CLI the coding agent uses. Every
command it proposes is parsed with the CLI's OWN parser (click, from
`probe.cli.main`) and checked in plain code first, because the checks need the
session and the CLI cannot see it:

    1. allowed for the daemon?   the owner table below (D18); a command with no
                                 owner fails `test_daemon_owner_table_covers_the_cli`
    2. secret scan               the text it sends and the files it uploads
                                 (the one detector, R4)
    3. an approval policy?       a delete that reaches another researcher's data,
                                 and every delete with no trash behind it
                                 (`PERMANENT_DELETES`), is held for the
                                 researcher (D22); every delete is
                                 refused outright while the server declares no
                                 trash (`check(..., trash=False)`): an irreversible
                                 delete stays the researcher's

Every check is exact; none judges meaning (the "names only real things",
"exact repeat" and "numbers match" checks were removed by Richard on
2026-09-26). A failed check comes back to the model as the command's output,
"not run (block 4a1c07e2): <why>", so it fixes and retries in the same bite, or asks
for an override with `probe daemon override 4a1c07e2 --why "..."` (policy
`check.override`). A passing command runs the real CLI with the daemon's key and
an Idempotency-Key (R12); its output goes back to the model.
"""

from __future__ import annotations

import importlib
import json
import math
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from probe.daemon.approvals import short_id
from probe.sdk.upload_limits import AUTO_UPLOAD_MAX_BYTES, SCAN_PREFIX_BYTES
from probe.tap_core import secrets

# ---------------------------------------------------------------------------
# D18: every CLI command has one owner.
# ---------------------------------------------------------------------------

READ = "read"  # no side effect: always allowed
DAEMON = "daemon"  # the daemon's to write
SDK = "sdk"  # the run's own code (run start, log, span, trials, exec, snapshot)
RESEARCHER = "researcher"  # importing history, crediting contributors, local files, sharing
SETUP = "setup"  # credentials, contexts, installs: never the daemon's
SWITCH = "switch"  # the probe switch is the researcher's (never moved by an agent)
SERVER = "server"  # the server does it on its own

OWNERS: dict[str, str] = {
    "access-group add": RESEARCHER, "access-group create": RESEARCHER, "access-group delete": RESEARCHER,
    "access-group list": READ, "access-group remove": RESEARCHER, "access-group rename": RESEARCHER,
    "agent-rules refresh": SETUP,
    "artifact add": DAEMON, "artifact delete": DAEMON, "artifact download": RESEARCHER,
    "artifact gc-uploads": SERVER, "artifact list": READ, "artifact move": DAEMON, "artifact pin-impact": READ,
    "artifact set": DAEMON, "artifact tree": READ, "artifact version-add": DAEMON, "artifact versions": READ,
    "backfill": RESEARCHER, "bundle": READ,
    # Hidden: what an old Capy timer still runs; it takes down what Capy left (capy_retire).
    "capy disconnect": SETUP, "capy sync": RESEARCHER,
    "commits": READ,
    "companion authorize": SETUP, "companion feedback": RESEARCHER, "companion log": READ,
    "companion report": READ, "companion trace": READ,
    "context delete": SETUP, "context list": READ, "context show": READ, "context use": SETUP,
    "coordinates": READ, "doctor": READ,
    # The data catalog (data-catalog C5): registering a dataset by identity, a
    # source, and what a run used are the daemon's; downloading bytes is the
    # researcher's, and so is hosting them (`dataset add --upload`, below).
    "checkpoint list": READ, "checkpoint use": DAEMON,
    "dataset add": DAEMON, "dataset download": RESEARCHER, "dataset list": READ, "dataset show": READ,
    "dataset use": DAEMON, "provenance": READ,
    "source add": DAEMON, "source list": READ, "source show": READ,
    "daemon worker": SETUP, "daemon status": READ, "daemon install": SETUP, "daemon override": DAEMON,
    # The daemon's own look at its session store, answered in its own process
    # (`local_commands`), like an override.
    "daemon session": READ,
    # A child agent for one long read (`agent.run_task`): it runs reads only.
    "daemon task": READ,
    # A local draft changed in place, a local data file previewed (the `bash`
    # tool set's `edit` and `read`; the daemon answers both itself).
    "draft edit": DAEMON, "file preview": READ,
    "approvals": RESEARCHER, "deny": RESEARCHER,
    # The main agent's question to the daemon's reader: never the writer's.
    "ask": RESEARCHER,
    "edge add": DAEMON, "edge remove": DAEMON, "events": READ, "exec": SDK,
    "feedback send": DAEMON, "feedback flush": SETUP,
    "experiment branch": READ,
    "experiment create": DAEMON, "experiment delete": DAEMON, "experiment edges": READ,
    "experiment fork": DAEMON, "experiment inherited": READ,
    "experiment freeze": DAEMON, "experiment get": READ, "experiment lineage": READ, "experiment list": READ,
    "experiment move": DAEMON,
    "experiment reproduce": READ, "experiment set": DAEMON, "experiment tag": DAEMON,
    "flush": SDK, "sync": SDK, "get": READ, "group create": DAEMON, "group get": READ, "group list": READ, "group set": DAEMON,
    "import wandb": RESEARCHER, "install": SETUP, "link": RESEARCHER, "log": SDK, "login": SETUP, "logout": SETUP,
    "mcp env": SETUP, "mcp headers": SETUP, "mcp status": SETUP, "mcp token set": SETUP, "mcp token unset": SETUP,
    # `/probe inline`'s read bridge: the main agent's, never the daemon's (it reads the MCP itself).
    "mcp call": RESEARCHER, "mcp tools": RESEARCHER,
    "metrics backfill": RESEARCHER, "metrics delete": RESEARCHER, "metrics export": READ, "metrics grouped": READ,
    "metrics plot": READ, "metrics wide": READ,
    "notes append": DAEMON, "notes audit-advisory": READ, "notes checkout": DAEMON, "notes create": DAEMON,
    "notes delete": DAEMON, "notes edit": DAEMON, "notes find": READ, "notes list": READ, "notes push": DAEMON, "notes rename": DAEMON,
    "notes show": READ, "notes status": READ,
    "notes sync": DAEMON, "notes team": READ, "notes write": RESEARCHER,
    "outbox adopt": SDK, "outbox discard": SDK, "outbox drain": SDK, "outbox pause": SDK, "outbox resume": SDK, "outbox retry": SDK,
    "outbox status": READ, "outbox watch": READ,
    "paper add": DAEMON, "paper citations": READ, "paper edges": READ, "paper find": READ, "paper graph": READ,
    "paper list": READ, "paper remove": DAEMON, "paper tag": DAEMON, "paper update": DAEMON,
    "project branches": READ,
    "project code attach": DAEMON, "project code confirm": DAEMON, "project code detach": DAEMON,
    "project code list": READ, "project contributors": READ, "project create": DAEMON, "project delete": DAEMON,
    "project get": READ, "project lineage": READ, "project list": READ, "project move": DAEMON, "project patch": DAEMON,
    "project reference add": DAEMON, "project reference remove": DAEMON, "project set": DAEMON,
    "project tag": DAEMON, "project use": RESEARCHER,
    "run check": READ, "run child": SDK, "run delete": DAEMON, "run end": DAEMON,
    # What a run read and built on: facts to label (lineage plan L5).
    "run inputs": READ, "run upstream": READ,
    # A declared range emails the run's creator when crossed: the researcher's call.
    "run expect": RESEARCHER, "run fork": SDK, "run get": READ,
    "run list": READ, "run metrics": READ, "run move": DAEMON, "run reproduce": READ, "run series": READ,
    "run set": DAEMON, "run start": SDK, "run tag": DAEMON,
    # A remote job's one-run token: minted at launch, extended when it nears expiry.
    "run token": SDK,
    "series latest": READ,
    "session default": SWITCH, "session initialize": SWITCH, "session state": SWITCH, "session status": READ,
    # `.probe.config`: testing a path is a local read; the answer about files
    # above the launch folder is the researcher's, recorded with `--directed`.
    "ignore check": READ, "session parent": RESEARCHER,
    "session toggle": SWITCH, "session track": SWITCH, "session untrack": SWITCH,
    "session export": RESEARCHER,
    # A message to one of the researcher's own running sessions (G7): an
    # orchestrator's, never the daemon's (it would speak into another session).
    "session send": RESEARCHER,
    "setup": SETUP, "wizard": SETUP, "update": SETUP, "uninstall": SETUP,
    # `probe repair`: the install pipeline in repair mode -- the machine's plumbing.
    "repair": SETUP,
    "shared add": RESEARCHER, "shared delete": RESEARCHER, "shared download": RESEARCHER, "shared list": READ,
    "shared share": RESEARCHER, "shared unshare": RESEARCHER,
    "snapshot": SDK, "snapshot-prune-refs": RESEARCHER, "snapshot-restore": RESEARCHER,
    "snapshot-show": READ,
    # `probe status`: this device's install as data (the desktop app's read);
    # `--refresh` asks the agents' CLIs and the server, and writes nothing.
    "status": READ,
    # The desktop app's JSON interface: it previews and starts the researcher's
    # history imports on their own computer (like `backfill`), and cancels them.
    "desktop request": RESEARCHER,
    # The machine-wide Probe service: its status is a read; starting or
    # stopping it is the machine's plumbing, never the daemon's.
    "service status": READ, "service start": SETUP, "service stop": SETUP, "service check-now": SETUP,
    "span add": SDK, "span get": READ, "span list": READ,
    # A project's or experiment's summary and its Metrics-center visuals
    # (writer-owns-summary): the recorder's. A checkout and `visuals options`
    # write a local draft, like `notes checkout`.
    "summary checkout": DAEMON, "summary push": DAEMON,
    # One-command edits with no draft, for a caller with no files between
    # commands (the dashboard assistant, acting for the researcher). The
    # daemon keeps the draft flow its summaries-owed bookkeeping reads.
    "summary append": RESEARCHER, "summary edit": RESEARCHER,
    "visuals options": DAEMON, "visuals set": DAEMON,
    "statusline install": SETUP, "statusline show": READ, "statusline status": READ, "statusline uninstall": SETUP,
    "token create": SETUP, "token list": SETUP, "token revoke": SETUP,
    "trial add": SDK, "trial drain": SDK, "trial expand": SDK, "trial export": SDK, "trial get": READ,
    "trial list": READ, "trial reconcile": SDK, "trial set": SDK, "trial stage": SDK, "trial watch": SDK,
    "version create": DAEMON, "version list": READ,
    "views create": DAEMON, "views data": READ, "views delete": DAEMON, "views list": READ, "views preview": READ,
    "views rename": DAEMON, "views show": READ, "views update": DAEMON,
    "wandb discover": RESEARCHER, "wandb import-hosted": RESEARCHER, "wandb import-local": RESEARCHER,
    "wandb key set": SETUP, "wandb key status": SETUP,
    "whoami": READ,
    "workspace create": RESEARCHER, "workspace delete": RESEARCHER,
    "workspace get": READ, "workspace list": READ,
    # `workspace limit` narrows what EVERY Probe client on this computer reads,
    # the daemon's own included: the researcher's, like `workspace use` (D-d).
    "workspace limit": RESEARCHER,
    "workspace rename": RESEARCHER, "workspace use": RESEARCHER, "workspace writers set": RESEARCHER,
    # The workspace's best pick, as `project set --best` is the project's: a
    # recorded judgement with its reason; a person's pick is never written over.
    "workspace set": DAEMON,
    "workspace writers show": READ,
}

_WHY_NOT = {
    SDK: "the run's own code records this",
    RESEARCHER: "only the researcher does this",
    SETUP: "credentials, contexts and installs aren't the daemon's",
    SWITCH: "the probe switch is the researcher's",
    SERVER: "the server does this itself",
}

#: Deletes. Only against a server that declares a trash (`GET /v1/server/features`
#: lists "trash") does a delete go to the 30-day trash, may need the researcher
#: (D16, D22), and run at all; anywhere else the daemon never deletes.
DELETES = {"run delete", "project delete", "experiment delete", "artifact delete", "notes delete", "paper remove",
           "views delete", "edge remove", "project reference remove", "project code detach"}
#: The entity-delete commands whose cascade can reach another researcher's data.
CASCADE_DELETES = {"run delete": "run", "project delete": "project", "experiment delete": "experiment"}
#: Every other delete: the server keeps no trash copy, so it cannot be undone, and
#: each one is a question (`delete.permanent`, what it deletes) unless bypass mode.
PERMANENT_DELETES = {
    "artifact delete": "an artifact (its file and every version)",
    "notes delete": "a sub-note and its version history",
    "paper remove": "a recorded paper",
    "views delete": "a view",
    "edge remove": "a lineage edge",
    "project reference remove": "a reference between two projects",
    "project code detach": "a repository's link to a project",
}
NO_TRASH = "the server has no trash yet, so deletes stay the researcher's"
#: Probe could not be asked whether it has the trash (offline, or an error).
TRASH_UNKNOWN = "couldn't reach Probe to check for the trash"

#: Root options the daemon may pass; `--base-url` would send its key elsewhere.
_ROOT_OK = {"--sync"}
#: `--async` (root, or after `run end` / `artifact add`) queues the write and
#: exits 0 before Probe answers: the logbook files it `ran`, and a refusal later
#: dead-letters in the outbox where nothing tells the daemon (lineage plan L14).
#: The daemon's commands run with PROBE_ASYNC=0 to wait for the answer; this
#: keeps a flag from undoing that. No override: the same command without it runs.
#: One exception, made by the CLI and not by a flag: a RUN file over 64 MiB is
#: queued in parts even under PROBE_ASYNC=0 (a multi-gigabyte transfer cannot
#: land inside a 180 s call). The CLI reads the run first, so a wrong id still
#: fails here; a later refusal dead-letters with a reference row.
ASYNC_REFUSED = "`--async` would queue the write without waiting for Probe's answer - run it without `--async`"
#: Per-command options the daemon may never pass, with why.
_SUMMARY_IS_THE_RESEARCHERS = ("`--summary` is the researcher's own block on the summary - the daemon never "
                               "writes it; the rest of the summary is yours: `probe summary checkout`, edit, "
                               "`probe summary push`")
#: The server writes a project's one-line description itself
#: (`app/generation/kinds/description.py`). An experiment's is its `--question`,
#: which stays the daemon's (the lane skips experiments). A RUN's is the daemon's
#: from the moment it starts (track-work): its writes go as `authored_by=agent`
#: (`agent_session.default_authorship`), so the lane still replaces it when the
#: run finishes.
_PROJECT_DESCRIPTION_IS_THE_SERVERS = "a project's description is written by the server once a run finishes under it"
_HOSTING_IS_THE_RESEARCHERS = ("`--upload` stores the dataset's bytes in Probe against the team's hosted-data cap: "
                               "that is the researcher's call - register it as a reference without it")
_TEAM_NOTE_IS_A_QUESTION = ("`--team` writes the team note directly; change it in its file instead, where "
                            "the researcher sees each change first")
#: Options that turn a read into a write of a local file the command is pointed
#: at, anywhere on the machine (`--export ~/.bashrc`): with one, the command is
#: the researcher's (`Parsed.owner`), refused for the daemon's writer and reader.
WRITING_OPTIONS = frozenset({("run reproduce", "export"), ("run reproduce", "materialize")})
_FORBIDDEN_OPTIONS = {
    ("notes push", "force"): "`--force` overwrites what others wrote since the checkout - push merges without it",
    ("notes checkout", "steal"): "`--steal` discards another writer's unpushed edits",
    # Not `summary checkout --steal`: the daemon's summary drafts are its own,
    # one per session (`<session>.daemon.*`), so `--steal` discards only its
    # own unpushed edits -- and since a checkout never replaces those without
    # it (review of #3034, finding 3), it is the way back after an erasure
    # refused a push (`erased_since_checkout`).
    ("run set", "authored_by"): None,  # checked by value below
    # `--summary` is `document`: the Markdown block inside the Overview page, which
    # track-work names the researcher's ("never write it"). A bench daemon wrote its
    # verdicts there instead of in notes (2026-09-27).
    **{(path, "summary"): _SUMMARY_IS_THE_RESEARCHERS
       for path in ("project create", "project set", "project patch", "experiment create", "experiment set")},
    # Lineage plan L15 (G4): the old daemon wrote a project description every
    # session, and each one locked the server's lane out of that project.
    **{(path, "description"): _PROJECT_DESCRIPTION_IS_THE_SERVERS
       for path in ("project create", "project set", "project patch")},
    # D6: every team-note change is shown to the researcher first. The daemon
    # changes it through its file, where each write is held as a question with
    # its diff; `--team` would write it directly and skip that.
    **{(path, "team"): _TEAM_NOTE_IS_A_QUESTION for path in ("notes append", "notes edit")},
    # C8: hosting puts the bytes in Probe, against the team's hosted-data cap.
    ("dataset add", "upload"): _HOSTING_IS_THE_RESEARCHERS,
}
#: Per command, the parameters whose value is a local file the command reads and
#: sends (uploads, or reads as a body). Named by the command's MEANING, not by a
#: parameter's name: `artifact add` with an anchor flag reads its FILE from the
#: `run` slot, and `--from-manifest` names every file on its own rows.
#: `tests/test_daemon_guards.py` walks the click tree and fails on any file-shaped
#: parameter of a command the daemon may run that is in neither table below.
FILE_PARAMS: dict[str, tuple[str, ...]] = {
    "artifact add": ("path",),
    "notes create": ("file",),
    "views create": ("spec_file",),
    "views preview": ("spec_file",),
    "views update": ("spec_file",),
    "paper add": ("source",),  # a URL, or a local file path
    "paper update": ("source",),
    "visuals set": ("file",),  # the visuals JSON (default: the draft `visuals options` wrote)
}
#: A manifest: a local JSON-lines file whose rows each name a file to upload.
MANIFEST_PARAMS = {("artifact add", "from_manifest")}
#: File-shaped names that are NOT local files, with what they are.
NOT_FILES: dict[tuple[str, str], str] = {
    ("commits", "path"): "a path filter the server applies to the repository's history",
    ("draft edit", "path"): ("a checked-out draft, changed in place and never sent (the daemon answers it in "
                             "its own process, `local_commands`, by `probe.drafts`' own folder rule)"),
    ("file preview", "path"): ("a local file shown, never sent (the daemon answers it in its own process, by the "
                               "read rules, `tools.read_check`)"),
    ("ignore check", "paths"): "paths tested against the local `.probe.config` files; nothing is read or sent",
    ("commits", "source"): "a code source id",
    ("project code attach", "path"): "a subtree of the GitHub repository, read by the server",
    ("project code detach", "source_id"): "a code source id",
    ("project code confirm", "source_id"): "a code source id",
    ("notes audit-advisory", "source"): "the harness whose note budget to read",
    ("edge add", "source"): "an entity ref (`run:<id>`)",
    ("experiment fork", "source"): "the experiment to fork (a slug or id)",
    ("artifact version-add", "from_artifact"): "an artifact id",
    ("dataset add", "path"): "a file, folder or uri recorded by identity (path, size, sha256); its bytes are sent "
                             "only with --upload, which the daemon never passes, and the CLI uploads no preview "
                             "sample when the daemon runs it (PROBE_DAEMON_SESSION)",
    ("dataset add", "from_ref"): "a dataset version ref the step read",
}
#: Text the CLI takes LITERALLY, never as `@file` or `-`: the text-only notes
#: writes. A value here starting with `@` is still scanned as the text it is,
#: and never read as a file the command would send.
LITERAL_TEXT: frozenset[tuple[str, str]] = frozenset(
    {("notes append", "text"), ("notes edit", "old"), ("notes edit", "new")}
)
#: `artifact add` anchor flags: with one, the RUN slot holds the FILE.
_ARTIFACT_ANCHORS = ("project", "experiment", "workspace", "shared")

#: Text a command sends: long enough to hold a credential.
_MIN_SCAN_CHARS = 8


@dataclass
class Parsed:
    path: str  # "run tag"
    params: dict[str, Any]
    root_options: list[str]
    argv: list[str]
    #: click takes `--help` here as the help flag: the CLI prints the command's
    #: help and does nothing else, so it is a read whoever owns the command. Never
    #: when `--help` is an option's value (`notes delete --note --help --yes`
    #: deletes the note titled `--help`).
    help: bool = False

    @property
    def owner(self) -> str | None:
        if self.help:
            return READ
        # A read whose option writes a file anywhere it is pointed (`run reproduce
        # --export FILE`, `--materialize DIR`) is the researcher's, not a read.
        if any(self.params.get(param) for path, param in WRITING_OPTIONS if path == self.path):
            return RESEARCHER
        return OWNERS.get(self.path)


@dataclass
class Block:
    """A failed check: shown to the model as "not run (block <id>): <why>"."""

    id: str
    why: str
    check: str  # "allowed" | "secret" | "parse" | "option" | "no_trash" | "document" | "probe_config"
    flagged: str | None = None  # the masked secret, for an override question
    argv: list[str] = field(default_factory=list)
    overridable: bool = True  # False: no `probe daemon override` for this one
    cwd: str | None = None  # the folder the blocked command ran in (a compound's `cd`)

    def message(self) -> str:
        if not self.overridable:
            return f"not run (block {self.id}): {self.why}. This check has no override."
        return (f"not run (block {self.id}): {self.why}. To ask the researcher to allow it: "
                f"`probe daemon override {self.id} --why \"...\"`")


class ParseError(Exception):
    pass


_ROOT = None
_LIVE_ROOT = None


def _live_root():
    """The CLI's own tree, imported (35 MB): only when no spec can be had for the
    installed CLI -- neither the shipped `cli_spec.json` nor the copy a child writes
    into the daemon's state folder (`cli_spec.load`) -- or the CLI is loaded already."""
    global _LIVE_ROOT
    if _LIVE_ROOT is None:
        import typer.main

        _LIVE_ROOT = typer.main.get_command(importlib.import_module("probe.cli.main").app)
    return _LIVE_ROOT


def _root():
    """The CLI's command tree: rebuilt from `cli_spec.json` (the CLI's own tree as
    data, kept equal to it by a test), so the daemon never imports the whole CLI
    to check a command (plan M1); the CLI's own when that file cannot be read."""
    global _ROOT
    if _ROOT is None:
        from probe.daemon import cli_spec

        root = cli_spec.load()
        _ROOT = root if root is not None else _live_root()
    return _ROOT


def _walk(argv: list[str], root: Any = None) -> tuple[list[str], list[str], list[str], Any]:
    """`(root options, command words, the words after them, the click command or
    group they name)` for `argv`, the words after `probe`."""
    args = list(argv)
    root_options: list[str] = []
    while args and args[0].startswith("-"):
        option = args.pop(0)
        root_options.append(option)
        if option in ("--base-url", "--spool-dir") and args:
            args.pop(0)
    path: list[str] = []
    cmd: Any = _root() if root is None else root
    while hasattr(cmd, "commands") and args and not args[0].startswith("-"):
        name = args[0]
        sub = cmd.commands.get(name)
        if sub is None:
            break
        path.append(name)
        cmd = sub
        args.pop(0)
    return root_options, path, args, cmd


def _help_flag(cmd: Any, ctx: Any) -> bool:
    """Asked of click, never of the words: `--help` given as `cmd`'s help flag is
    the one way its parameter source reads COMMANDLINE (by name: typer may carry
    its own copy of click). `probe artifact delete --help` was held twice as a
    delete that cannot be undone, and `notes delete --note --help --yes` deletes."""
    option = cmd.get_help_option(ctx)
    source = ctx.get_parameter_source(option.name) if option is not None else None
    return getattr(source, "name", None) == "COMMANDLINE"


def parse(argv: list[str]) -> Parsed:
    """Resolve `argv` (the words after `probe`) with the CLI's own parser, without running it."""
    return _parse(argv, _root())


def _parse(argv: list[str], root: Any) -> Parsed:
    import click

    root_options, path, args, cmd = _walk(argv, root)
    if not path:
        raise ParseError(f"`probe {' '.join(argv[:2])}` is not a probe command")
    if getattr(cmd, "commands", None):
        raise ParseError(f"`probe {' '.join(path)}` needs a subcommand: {', '.join(sorted(cmd.commands))}")
    try:
        ctx = cmd.make_context(" ".join(path), args, resilient_parsing=True)
    except click.ClickException as exc:
        raise ParseError(str(exc.format_message())) from None
    return Parsed(path=" ".join(path), params=dict(ctx.params), root_options=root_options, argv=list(argv),
                  help=_help_flag(cmd, ctx))


def asks_help(argv: list[str]) -> bool:
    """Does `probe <argv>` only print help? click takes `--help` as the help flag
    of the command or group it names, or of `probe` itself. The one help check:
    `Parsed.help` for the daemon, this for the agent's write gate
    (`cli/write_gate.py`). Anything click cannot place is not help, so the gate
    applies to it."""
    try:
        root_options, path, args, cmd = _walk(argv)
        if "--help" in root_options:
            return True
        return _help_flag(cmd, cmd.make_context(" ".join(path) or "probe", args, resilient_parsing=True))
    except Exception:  # noqa: BLE001 - not help: the gate decides
        return False


def command(path: str) -> Any:
    """The click command for "run tag", from the CLI's own tree."""
    cmd: Any = _root()
    for name in path.split():
        cmd = cmd.commands[name]
    return cmd


def delete_target(parsed: Parsed) -> str | None:
    """The entity a CASCADE delete names: its first positional argument, under the
    name the CLI's parser binds it to (`project delete` -> `project_id`). None when
    it cannot be read, and the caller then refuses: a delete never runs unchecked."""
    for param in command(parsed.path).params:
        # typer carries its own copy of click, so the kind is read by name, not by class.
        if getattr(param, "param_type_name", None) == "argument":
            return next((v for v in _strings(parsed.params.get(param.name)) if v.strip()), None)
    return None


def _strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple)):
        return [v for item in value for v in _strings(item)]
    return []


def new_block_id() -> str:
    return short_id()


def _claims_human(parsed: Parsed) -> bool:
    """`--authored-by human` anywhere in the command, parsed or not.

    The parser is resilient: it stops at an option it does not know, so a
    flag before `--authored-by` would leave `authored_by` unparsed while the
    CLI still applies it. Read the raw argv too, both spellings.
    """
    if parsed.params.get("authored_by") in ("human",):
        return True
    argv = [str(token) for token in parsed.argv]
    for i, token in enumerate(argv):
        if token == "--authored-by" and i + 1 < len(argv) and argv[i + 1].strip().lower() == "human":
            return True
        if token.lower().startswith("--authored-by=") and token.split("=", 1)[1].strip().lower() == "human":
            return True
    return False


def check(parsed: Parsed, *, cwd: Path, trash: bool | None = False) -> Block | None:
    """Checks 1 and 2 (allowed, secret scan). The approval check needs Probe reads (`tools`).

    `trash`: the server declares a trash (`probe_api.server_features`; None: it
    could not be asked). Without one every delete is refused, with no override:
    the daemon never makes an irreversible delete. A delete is checked FIRST, and
    none of its blocks has an override (G5): an overridable block before it (a
    root option) would let `probe daemon override` run the delete."""
    if "--async" in parsed.root_options or parsed.params.get("write_mode") is True:
        return Block(new_block_id(), ASYNC_REFUSED, "option", argv=parsed.argv, overridable=False)
    bad_root = [o for o in parsed.root_options if o not in _ROOT_OK]
    if parsed.path in DELETES and not parsed.help:  # a help request deletes nothing (`Parsed.help`)
        if trash is None:
            return Block(new_block_id(), TRASH_UNKNOWN, "no_trash", argv=parsed.argv, overridable=False)
        if not trash:
            return Block(new_block_id(), NO_TRASH, "no_trash", argv=parsed.argv, overridable=False)
        if bad_root:
            return Block(new_block_id(), f"a delete takes no root option ({bad_root[0]})",
                         "option", argv=parsed.argv, overridable=False)
    if bad_root:
        return Block(new_block_id(), f"the root option {bad_root[0]} isn't available to the daemon", "option",
                     argv=parsed.argv)
    owner = parsed.owner
    if owner is None:
        return Block(new_block_id(), f"`probe {parsed.path}` isn't in the daemon's table", "allowed",
                     argv=parsed.argv)
    if owner not in (READ, DAEMON):
        return Block(new_block_id(), f"`probe {parsed.path}` isn't the daemon's to run: {_WHY_NOT[owner]}",
                     "allowed", argv=parsed.argv)
    for (path, param), why in _FORBIDDEN_OPTIONS.items():
        if path == parsed.path and parsed.params.get(param) and why:
            return Block(new_block_id(), why, "option", argv=parsed.argv)
    # Every command that takes `--authored-by` (project create/set, experiment
    # create/fork/set, run set/start/...), not two of them: `human` locks a
    # name or description against generation forever, and that is the
    # researcher's claim to make. The override asks them.
    if _claims_human(parsed):
        return Block(new_block_id(), "the daemon can't mark its own words as a human's: words the researcher chose "
                     "go through the override, which asks them; for your own, use `--authored-by agent`",
                     "option", argv=parsed.argv)
    if owner == READ:
        # A read sends no text worth scanning, but a spec file it evaluates is uploaded.
        for path in _files_it_reads(parsed, text_refs=False):
            block = _check_file(_resolve(path, cwd), parsed)
            if block:
                return block
        return None
    # Secret scan: every string it sends, and every file it reads as a body or uploads.
    file_params = set(FILE_PARAMS.get(parsed.path, ())) | {n for c, n in MANIFEST_PARAMS if c == parsed.path}
    if parsed.path == "artifact add":
        file_params.add("run")  # the FILE, when an anchor flag is set (checked as a file below)
    for key, value in parsed.params.items():
        if key in file_params:
            continue
        for text in _strings(value):
            if len(text) < _MIN_SCAN_CHARS:
                continue
            if text.startswith("@") and (parsed.path, key) not in LITERAL_TEXT:
                continue  # a file reference: scanned as the file below
            found = secrets.scan(text)
            if found:
                return Block(new_block_id(), f"the text looks like it contains a credential ({found[0].rule})",
                             "secret", flagged=_mask_finding(text, found[0]), argv=parsed.argv)
    artifact = _artifact_file(parsed)
    pointer = _stays_a_pointer(parsed.params.get("reference"), parsed.params.get("kind"))
    for path in _files_it_reads(parsed):
        block = _check_file(_resolve(path, cwd), parsed, pointer=pointer and path == artifact)
        if block:
            return block
    for key in (n for c, n in MANIFEST_PARAMS if c == parsed.path):
        for manifest in _strings(parsed.params.get(key)):
            block = _check_manifest(_resolve(manifest, cwd), parsed, cwd)
            if block:
                return block
    return None


def _resolve(value: str, cwd: Path) -> Path:
    path = Path(os.path.expanduser(value))
    return path if path.is_absolute() else cwd / path


def _files_it_reads(parsed: Parsed, *, text_refs: bool = True) -> list[str]:
    """Local files the command sends: its file parameters (`FILE_PARAMS`), the FILE
    `artifact add` takes in the RUN slot when an anchor flag is set, and (unless
    `text_refs` is off) `@file` option values (the CLI reads `--notes @x.md` as
    x.md's text). A URL in a paper's `--source` is not a file."""
    out: list[str] = []
    file_params = list(FILE_PARAMS.get(parsed.path, ()))
    if parsed.path == "artifact add" and any(parsed.params.get(a) for a in _ARTIFACT_ANCHORS) \
            and not parsed.params.get("path"):
        file_params.append("run")
    for key, value in parsed.params.items():
        for text in _strings(value):
            if not text or text == "-":
                continue
            if key in file_params:
                if key == "source" and re.match(r"^[a-z][a-z0-9+.-]*://", text, re.I):
                    continue
                out.append(text)
            elif (text_refs and text.startswith("@") and len(text) > 1
                  and (parsed.path, key) not in LITERAL_TEXT):
                out.append(text[1:])
    return out


def files_sent(parsed: Parsed, cwd: Path) -> list[Path]:
    """Every local file the command sends, resolved against `cwd`, in a fixed
    order: the ones `check` scans (`_files_it_reads`: file parameters, `@file`
    values of a write), each `--from-manifest` file and the files its rows name.
    Not the document `notes push` / `notes sync` / `summary push` send, nor a
    `visuals set` with no `--file` (their argv never names it: `tools` resolves
    that). Unreadable manifests add nothing."""
    out = [_resolve(path, cwd) for path in _files_it_reads(parsed, text_refs=parsed.owner != READ)]
    for key in (n for c, n in MANIFEST_PARAMS if c == parsed.path):
        for manifest in _strings(parsed.params.get(key)):
            resolved = _resolve(manifest, cwd)
            out.append(resolved)
            try:
                lines = resolved.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeDecodeError):
                continue
            for line in lines:
                try:
                    row = json.loads(line) if line.strip() else None
                except ValueError:
                    continue
                if isinstance(row, dict):
                    out += [_resolve(t, cwd) for t in _strings(row.get("path")) if t and t != "-"]
    return out


def check_document(path: Path, parsed: Parsed) -> Block | None:
    """A document the command sends though its argv never names it (`notes push`
    sends the checked-out file, `notes sync` the team note): checked like any
    file it uploads."""
    return _check_file(path, parsed)


def _check_manifest(path: Path, parsed: Parsed, cwd: Path) -> Block | None:
    """A `--from-manifest` file: scanned itself (its rows carry notes), then every
    row's file. A row the daemon cannot read is refused, never skipped."""
    block = _check_file(path, parsed)
    if block:
        return block
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return None  # the CLI itself reports an unreadable manifest
    for lineno, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError:
            row = None
        if not isinstance(row, dict):
            return Block(new_block_id(), f"line {lineno} of the manifest isn't a JSON object",
                         "secret", argv=parsed.argv)
        # A row the CLI records as a pointer: `"reference": true`, or any file at
        # or over `--reference-over` (so every file over the upload cap, while that
        # is at most the cap) -- never a code kind, which is always stored, and
        # never by size on a workspace or Shared row, whose files ARE their bytes.
        over = parsed.params.get("reference_over")
        file_anchor = any(row.get(a) or parsed.params.get(a) for a in ("workspace", "shared"))
        big_rows_point = isinstance(over, int) and over <= MAX_UPLOAD_BYTES and not file_anchor
        pointer = _stays_a_pointer(row.get("reference") is True or big_rows_point, row.get("kind"))
        for text in _strings(row.get("path")):
            if text and text != "-":
                block = _check_file(_resolve(text, cwd), parsed, pointer=pointer)
                if block:
                    return block
    return None


#: A write that names a path a `.probe.config` keeps out of the record (`read`
#: or `off`): the folder file is the researcher's, so there is no override.
CONFIG_REFUSED = (
    "`{path}` is set to {level} by `{source}`, so `probe {command}` was refused: Probe records "
    "nothing about it. Do not retry"
)
#: A word in text the daemon sends that could name a place: it has a `/`.
_PATH_TOKEN_RE = re.compile(r"""[^\s'"()<>`,;|]+""")
#: Markdown and punctuation around a path in prose (`**secret/x**`, `[a/b](...)`):
#: never a leading `.` or `~`, which are part of `./x`, `../x`, `~/x`, `.hidden/x`.
_PATH_LEAD = "*_[{"
_PATH_TRAIL = "*_]}.:!?#"


def _path_tokens(text: str) -> list[str]:
    """Every word in `text` that could name a place (it has a `/`), unwrapped.
    No cap: each check is cheap, and an unchecked path would fail open."""
    out = []
    for token in _PATH_TOKEN_RE.findall(text):
        token = token.lstrip(_PATH_LEAD).rstrip(_PATH_TRAIL)
        if token.startswith("@"):
            token = token[1:]
        token = re.sub(r":\d+$", "", token)
        if "/" in token and "://" not in token and len(token) > 1:
            out.append(token)
    return out


def check_config(parsed: Parsed, *, cwd: Path, checker: Any, document: Path | None = None) -> Block | None:
    """A command that would record something about a path a `.probe.config` sets
    to `read` or `off`: a file it sends (a manifest's rows included), a path its
    text names (a write's options and arguments), or one its document names
    (`notes push`). `checker` is the session's `probe_config.Checker`."""

    def blocked(path: str) -> Block | None:
        verdict = checker.check(path)
        if not verdict.excluded:
            return None
        rule = verdict.rule
        source = ".probe.config"
        if rule is not None:
            from probe.sdk import probe_config as _pc

            where = _pc.shown(rule.source)
            source = f"{where}:{rule.line} ({rule.pattern})" if rule.line else f"{where} ({rule.pattern})"
        why = CONFIG_REFUSED.format(path=path, level=verdict.level, source=source, command=parsed.path)
        return Block(new_block_id(), why, "probe_config", argv=parsed.argv, overridable=False)

    for sent in files_sent(parsed, cwd):
        found = blocked(str(sent))
        if found:
            return found
    if parsed.owner != READ:
        file_params = set(FILE_PARAMS.get(parsed.path, ())) | {n for c, n in MANIFEST_PARAMS if c == parsed.path}
        for key, value in parsed.params.items():
            if key in file_params:
                continue
            for text in _strings(value):
                for token in _path_tokens(text):
                    found = blocked(str(_resolve(token, cwd)))
                    if found:
                        return found
    bodies = [document] if document is not None else []
    if parsed.owner != READ:  # `--notes @x.md`: the file's text is what is recorded
        file_params = set(FILE_PARAMS.get(parsed.path, ()))
        for key, value in parsed.params.items():
            if key in file_params:
                continue
            for text in _strings(value):
                if text.startswith("@") and len(text) > 1 and (parsed.path, key) not in LITERAL_TEXT:
                    bodies.append(_resolve(text[1:], cwd))
    for body in bodies:
        try:
            text = body.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue  # the CLI reports a file it cannot read
        for token in _path_tokens(text):
            found = blocked(str(_resolve(token, cwd)))
            if found:
                return found
    return None


def _mask_finding(text: str, finding: Any) -> str:
    from probe.daemon.approvals import mask

    start, end = getattr(finding, "start", None), getattr(finding, "end", None)
    if isinstance(start, int) and isinstance(end, int) and 0 <= start < end <= len(text):
        return mask(text[start:end])
    return mask(text)


#: Never uploaded, whatever the model says: the names credentials live under (D4's safety stops).
SECRET_NAME_RE = re.compile(
    r"(^|/)(\.env.*|\.netrc|\.pgpass|id_[a-z0-9]+|.*\.pem|.*\.key|.*\.p12|.*\.pfx|.*\.jks|"
    r".*\.keystore|.*\.kdbx|.*\.keychain(-db)?|.*credential.*|.*secret.*|.*token.*|\.npmrc|\.pypirc|kubeconfig|"
    r".*\.tfstate(\..*)?|\.htpasswd|\.git-credentials|\.mcp\.json)$",
    re.IGNORECASE,
)
#: The most the daemon uploads (`AUTO_UPLOAD_MAX_BYTES`, 5 GiB), and how much of a
#: file it reads to scan for credentials before the command runs. Text: the
#: first `SCAN_BYTES` (16 MiB, the multipart verifier's inspection prefix) -- a
#: 64 MiB text scan took 35 s here, most of a 180 s call. Binary: the first
#: `BINARY_SCAN_BYTES` (64 MiB of printable runs took 2.6 s), so every binary
#: the old 50 MB cap let through is still scanned whole. Past those, the upload
#: gate redacts what it can replace in a file up to 64 MiB when the outbox sends
#: it; a bigger one goes up in parts, and only its first 16 MiB are scanned.
MAX_UPLOAD_BYTES = AUTO_UPLOAD_MAX_BYTES
SCAN_BYTES = SCAN_PREFIX_BYTES
BINARY_SCAN_BYTES = 64 * 1024 * 1024
_PRINTABLE_RUN = re.compile(rb"[\t\x20-\x7e]{8,}")


def _size(n: int) -> str:
    """Bytes as the researcher reads them: whole MB below 1 GB, else GB rounded
    UP to two decimals, so 5 GB + 1 byte never reads "5 GB, over the 5 GB limit"."""
    if n < 1 << 30:
        return f"{n // (1 << 20)} MB"
    return f"{math.ceil(n * 100 / (1 << 30)) / 100:g} GB"


def _note_dirs() -> list[Path]:
    """The only hidden folders the daemon uploads from: Probe's note checkouts and the team note."""
    from probe.daemon.folders import note_dirs

    out = []
    for folder in note_dirs():
        try:
            out.append(folder.resolve())
        except OSError:
            continue
    return out


def _protected() -> list[Path]:
    """Probe's config and key files, the daemon's own state, the approvals folder."""
    from probe.daemon.folders import protected_paths

    out = []
    for folder in protected_paths():
        try:
            out.append(folder.resolve())
        except (OSError, RuntimeError):
            continue
    return out


def _artifact_file(parsed: Parsed) -> str | None:
    """The FILE `artifact add` records: its PATH, or the RUN slot when an anchor
    flag is set (`_files_it_reads`)."""
    if parsed.path != "artifact add":
        return None
    return parsed.params.get("path") or parsed.params.get("run")


def _stays_a_pointer(reference: Any, kind: Any) -> bool:
    """`--reference` that the CLI keeps a pointer: it records where the bytes are
    and sends none. A code kind never is -- the CLI uploads it whatever
    `--reference` said (`_reference_after_code_check`)."""
    if reference is not True or not (kind is None or isinstance(kind, str)):
        return False  # a kind that is no string: the CLI refuses the row itself
    return not importlib.import_module("probe.cli.main")._is_code_kind(kind)


def _check_file(path: Path, parsed: Parsed, *, pointer: bool = False) -> Block | None:
    """The SAFETY stops on a file a command sends. There is deliberately no bound on
    WHERE it lives (Richard, 2026-09-25: the daemon may upload files adjacent to
    the session's work, relevance is the model's call): only Probe's own protected
    folders, hidden folders, credential-shaped names, size, and the secret scan."""
    try:
        resolved = path.resolve(strict=True)
    except (OSError, RuntimeError):
        return None  # the CLI itself reports a missing file
    if any(resolved == folder or resolved.is_relative_to(folder) for folder in _protected()):
        return Block(new_block_id(), f"{resolved.name} is in Probe's own config or state, which the daemon never "
                     "sends", "secret", argv=parsed.argv,
                     overridable=False)
    if resolved.is_dir():
        return Block(new_block_id(), f"{resolved.name} is a folder - the daemon sends single files",
                     "secret", argv=parsed.argv)
    if not resolved.is_file():
        return None
    try:
        shown = str(resolved.relative_to(Path.home().resolve()))
    except ValueError:
        shown = str(resolved)
    in_notes = any(resolved.is_relative_to(folder) for folder in _note_dirs())
    if any(part.startswith(".") for part in Path(shown).parts[:-1]) and not in_notes:
        return Block(new_block_id(), f"{shown} is in a hidden folder", "secret", argv=parsed.argv)
    if SECRET_NAME_RE.search("/" + resolved.name):  # the NAME: a folder called "test_secret_x" is no key
        return Block(new_block_id(), f"{resolved.name} has a name credentials are kept under", "secret",
                     argv=parsed.argv)
    size = resolved.stat().st_size
    # A pointer sends none of the bytes, so the upload cap is not its limit
    # (track-work: "Over 5 GB: `--reference`"). Its name and its first bytes
    # are still checked: a pointer to a credential is refused too.
    if size > MAX_UPLOAD_BYTES and not pointer:
        return Block(new_block_id(), f"{resolved.name} is {_size(size)}, over the {_size(MAX_UPLOAD_BYTES)} limit",
                     "secret", argv=parsed.argv)
    with resolved.open("rb") as handle:
        head = handle.read(8192)
        is_text = b"\0" not in head
        data = head + handle.read((SCAN_BYTES if is_text else BINARY_SCAN_BYTES) - len(head))
    if is_text:
        try:
            decoded = data.decode("utf-8")
        except UnicodeDecodeError:  # a cut at SCAN_BYTES can split a character too
            decoded = data.decode("utf-8", "replace")
    else:
        runs = _PRINTABLE_RUN.findall(data) + _PRINTABLE_RUN.findall(data.replace(b"\x00", b""))
        decoded = b"\n".join(runs).decode("ascii", "replace")
    found = secrets.scan(decoded)
    if found:
        return Block(new_block_id(), f"{resolved.name} looks like it contains a credential ({found[0].rule})",
                     "secret", flagged=f"{resolved.name}: {_mask_finding(decoded, found[0])}", argv=parsed.argv)
    return None
