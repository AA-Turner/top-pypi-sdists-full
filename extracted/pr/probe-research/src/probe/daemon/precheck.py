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
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from probe.daemon.approvals import short_id
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
    "backfill": RESEARCHER, "bundle": READ, "commits": READ,
    "companion authorize": SETUP, "companion feedback": RESEARCHER, "companion log": READ,
    "companion report": READ, "companion trace": READ,
    "context delete": SETUP, "context list": READ, "context show": READ, "context use": SETUP,
    "coordinates": READ, "doctor": READ,
    "daemon worker": SETUP, "daemon status": READ, "daemon install": SETUP, "daemon override": DAEMON,
    "approvals": RESEARCHER, "deny": RESEARCHER,
    # The main agent's question to the daemon's reader: never the writer's.
    "ask": RESEARCHER,
    "edge add": DAEMON, "edge remove": DAEMON, "events": READ, "exec": SDK,
    "experiment create": DAEMON, "experiment delete": DAEMON, "experiment edges": READ,
    "experiment freeze": DAEMON, "experiment get": READ, "experiment list": READ,
    "experiment reproduce": READ, "experiment set": DAEMON, "experiment tag": DAEMON,
    "flush": SDK, "sync": SDK, "get": READ, "group create": DAEMON, "group get": READ, "group list": READ, "group set": DAEMON,
    "import wandb": RESEARCHER, "install": SETUP, "link": RESEARCHER, "log": SDK, "login": SETUP, "logout": SETUP,
    "mcp env": SETUP, "mcp headers": SETUP, "mcp status": SETUP, "mcp token set": SETUP, "mcp token unset": SETUP,
    "metrics backfill": RESEARCHER, "metrics delete": RESEARCHER, "metrics export": READ, "metrics grouped": READ,
    "metrics plot": READ, "metrics wide": READ,
    "notes append": DAEMON, "notes audit-advisory": READ, "notes checkout": DAEMON, "notes create": DAEMON,
    "notes delete": DAEMON, "notes edit": DAEMON, "notes list": READ, "notes push": DAEMON, "notes rename": DAEMON,
    "notes show": READ, "notes status": READ,
    "notes sync": DAEMON, "notes team": READ, "notes write": RESEARCHER,
    "outbox discard": SDK, "outbox drain": SDK, "outbox pause": SDK, "outbox resume": SDK, "outbox retry": SDK,
    "outbox status": READ, "outbox watch": READ,
    "paper add": DAEMON, "paper citations": READ, "paper edges": READ, "paper graph": READ,
    "paper list": READ, "paper remove": DAEMON, "paper tag": DAEMON, "paper update": DAEMON,
    "project code attach": DAEMON, "project code confirm": DAEMON, "project code detach": DAEMON,
    "project code list": READ, "project contributors": READ, "project create": DAEMON, "project delete": DAEMON,
    "project get": READ, "project list": READ, "project move": DAEMON, "project patch": DAEMON,
    "project reference add": DAEMON, "project reference remove": DAEMON, "project set": DAEMON,
    "project tag": DAEMON, "project use": RESEARCHER,
    "run check": READ, "run child": SDK, "run delete": DAEMON, "run end": DAEMON,
    # What a run read and built on: facts to label (lineage plan L5). Correcting a
    # read's match is the researcher's (the plan's decided default).
    "run inputs": READ, "run upstream": READ,
    "run input dismiss": RESEARCHER, "run input pin": RESEARCHER, "run input reset": RESEARCHER,
    # A declared range emails the run's creator when crossed: the researcher's call.
    "run expect": RESEARCHER, "run fork": SDK, "run get": READ,
    "run list": READ, "run metrics": READ, "run move": DAEMON, "run reproduce": READ, "run series": READ,
    "run set": DAEMON, "run start": SDK, "run tag": DAEMON,
    "series latest": READ,
    "session default": SWITCH, "session initialize": SWITCH, "session state": SWITCH, "session status": READ,
    "session toggle": SWITCH, "session track": SWITCH, "session untrack": SWITCH,
    "setup": SETUP, "wizard": SETUP, "update": SETUP,
    "shared add": RESEARCHER, "shared delete": RESEARCHER, "shared download": RESEARCHER, "shared list": READ,
    "shared share": RESEARCHER, "shared unshare": RESEARCHER,
    "snapshot": SDK, "snapshot-prune-refs": RESEARCHER, "snapshot-restore": RESEARCHER,
    "snapshot-show": READ,
    "span add": SDK, "span get": READ, "span list": READ,
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
    "workspace create": RESEARCHER, "workspace delete": RESEARCHER, "workspace get": READ, "workspace list": READ,
    "workspace rename": RESEARCHER, "workspace use": RESEARCHER, "workspace writers set": RESEARCHER,
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
ASYNC_REFUSED = "`--async` would queue the write without waiting for Probe's answer - run it without `--async`"
#: Per-command options the daemon may never pass, with why.
_SUMMARY_IS_THE_RESEARCHERS = ("`--summary` is the researcher's own Markdown on the Overview page - the daemon "
                               "never writes it; notes are yours")
#: A description written through the CLI is stamped `description_customized`,
#: which locks the server's `description` lane out of it for good
#: (`app/generation/kinds/description.py`): the server writes a project's and a
#: run's one-line description itself. An experiment's is its `--question`, which
#: stays the daemon's (the lane skips experiments).
_PROJECT_DESCRIPTION_IS_THE_SERVERS = "a project's description is written by the server once a run finishes under it"
_RUN_DESCRIPTION_IS_THE_SERVERS = "a run's description is written by the server once the run finishes"
_TEAM_NOTE_IS_A_QUESTION = ("`--team` writes the team note directly; change it in its file instead, where "
                            "the researcher sees each change first")
_FORBIDDEN_OPTIONS = {
    ("notes push", "force"): "`--force` overwrites what others wrote since the checkout - push merges without it",
    ("notes checkout", "steal"): "`--steal` discards another writer's unpushed edits",
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
    ("run set", "description"): _RUN_DESCRIPTION_IS_THE_SERVERS,
    # D6: every team-note change is shown to the researcher first. The daemon
    # changes it through its file, where each write is held as a question with
    # its diff; `--team` would write it directly and skip that.
    **{(path, "team"): _TEAM_NOTE_IS_A_QUESTION for path in ("notes append", "notes edit")},
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
}
#: A manifest: a local JSON-lines file whose rows each name a file to upload.
MANIFEST_PARAMS = {("artifact add", "from_manifest")}
#: File-shaped names that are NOT local files, with what they are.
NOT_FILES: dict[tuple[str, str], str] = {
    ("commits", "path"): "a path filter the server applies to the repository's history",
    ("commits", "source"): "a code source id",
    ("project code attach", "path"): "a subtree of the GitHub repository, read by the server",
    ("project code detach", "source_id"): "a code source id",
    ("project code confirm", "source_id"): "a code source id",
    ("notes audit-advisory", "source"): "the harness whose note budget to read",
    ("edge add", "source"): "an entity ref (`run:<id>`)",
    ("artifact version-add", "from_artifact"): "an artifact id",
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

    @property
    def owner(self) -> str | None:
        return OWNERS.get(self.path)


@dataclass
class Block:
    """A failed check: shown to the model as "not run (block <id>): <why>"."""

    id: str
    why: str
    check: str  # "allowed" | "secret" | "parse" | "option" | "no_trash" | "document"
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


def _root():
    global _ROOT
    if _ROOT is None:
        import typer.main

        _ROOT = typer.main.get_command(importlib.import_module("probe.cli.main").app)
    return _ROOT


def parse(argv: list[str]) -> Parsed:
    """Resolve `argv` (the words after `probe`) with the CLI's own parser, without running it."""
    import click

    root = _root()
    args = list(argv)
    root_options: list[str] = []
    while args and args[0].startswith("-"):
        option = args.pop(0)
        root_options.append(option)
        if option in ("--base-url", "--spool-dir") and args:
            args.pop(0)
    path: list[str] = []
    cmd: Any = root
    while hasattr(cmd, "commands") and args and not args[0].startswith("-"):
        name = args[0]
        sub = cmd.commands.get(name)
        if sub is None:
            break
        path.append(name)
        cmd = sub
        args.pop(0)
    if not path:
        raise ParseError(f"`probe {' '.join(argv[:2])}` is not a probe command")
    if getattr(cmd, "commands", None):
        raise ParseError(f"`probe {' '.join(path)}` needs a subcommand: {', '.join(sorted(cmd.commands))}")
    try:
        ctx = cmd.make_context(" ".join(path), args, resilient_parsing=True)
    except click.ClickException as exc:
        raise ParseError(str(exc.format_message())) from None
    return Parsed(path=" ".join(path), params=dict(ctx.params), root_options=root_options, argv=list(argv))


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
    if parsed.path in DELETES:
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
    if parsed.path == "run set" and parsed.params.get("authored_by") in ("human",):
        return Block(new_block_id(), "the daemon can't mark its own words as a human's (use `--authored-by agent`)",
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
    for path in _files_it_reads(parsed):
        block = _check_file(_resolve(path, cwd), parsed)
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
    Not the document `notes push` / `notes sync` send (their argv never names it:
    `tools` resolves that). Unreadable manifests add nothing."""
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
        for text in _strings(row.get("path")):
            if text and text != "-":
                block = _check_file(_resolve(text, cwd), parsed)
                if block:
                    return block
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
MAX_UPLOAD_BYTES = 50 * 1024 * 1024
MAX_TEXT_UPLOAD_BYTES = 10 * 1024 * 1024
_PRINTABLE_RUN = re.compile(rb"[\t\x20-\x7e]{8,}")


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


def _check_file(path: Path, parsed: Parsed) -> Block | None:
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
    data = resolved.read_bytes() if size <= MAX_UPLOAD_BYTES else b""
    if size > MAX_UPLOAD_BYTES:
        return Block(new_block_id(), f"{resolved.name} is {size // (1 << 20)} MB, over the 50 MB limit",
                     "secret", argv=parsed.argv)
    head = data[:8192]
    is_text = b"\0" not in head
    if is_text:
        try:
            decoded = data.decode("utf-8")
        except UnicodeDecodeError:
            decoded = data.decode("utf-8", "replace")
        if size > MAX_TEXT_UPLOAD_BYTES:
            return Block(new_block_id(), f"{resolved.name} is a text file over 10 MB",
                         "secret", argv=parsed.argv)
    else:
        runs = _PRINTABLE_RUN.findall(data) + _PRINTABLE_RUN.findall(data.replace(b"\x00", b""))
        decoded = b"\n".join(runs).decode("ascii", "replace")
    found = secrets.scan(decoded)
    if found:
        return Block(new_block_id(), f"{resolved.name} looks like it contains a credential ({found[0].rule})",
                     "secret", flagged=f"{resolved.name}: {_mask_finding(decoded, found[0])}", argv=parsed.argv)
    return None
