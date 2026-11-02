"""`probe` - the Probe Research CLI implementation, built on typer.

Thin wrapper over the SDK. The write path a coding agent (or a shell script) calls
to record experiment data. A data write Probe did not answer is queued in the local
outbox and delivered later (the command says `queued`); one Probe refused fails, exit 1.
Read convenience verbs (`get`, `bundle`) wrap the same read service the MCP tools use.

Connection flags (`--base-url/--token/--ingest-token/--hmac-secret`) are global and
go before the command: `probe --token probe_pat_x log RUN loss=0.1`. `login` also accepts
them directly so `probe login --token ...` works. Config lives in ~/.config/probe/config.json.

Auth: `probe login --device` runs the browser handoff (RFC 8628) and captures the
`probe_pat_...` token; `probe login --token probe_pat_...` is the air-gap paste path.
"""

from __future__ import annotations

import importlib
import os
import sys
from typing import Optional

import typer
from pydantic import ValidationError

from .. import __version__, errors
from ..sdk import agent_session, session_marker
from ..shared.reads import reads
# Printed by `reads.report_error`; re-exported here, where callers and tests read it.
from ..sdk.settings.key_refusal import KEY_REFUSED_LINE  # noqa: F401
from probe.cli.cli import app
from probe.cli.commands.commands import COMMAND_GROUPS
from probe.cli.commands.account.access import access_group_app, writers_app
from probe.cli.commands.account.context import context_app
from probe.cli.commands.account.mcp import mcp_app
from probe.cli.commands.account.token import token_app
from probe.cli.commands.account.workspace import workspace_app
from probe.cli.commands.artifacts.artifacts import artifact_app
from probe.cli.commands.artifacts.shared_folder import shared_app
from probe.cli.commands.machine.json_command import _JsonCommand
from probe.cli.commands.machine.outbox import outbox_app
from probe.cli.commands.machine.wizard import wizard
from probe.cli.commands.metrics.metrics import metrics_app, series_app
from probe.cli.commands.metrics.views import views_app
from probe.cli.commands.notes.agent_rules import rules_app
from probe.cli.commands.notes.notes import notes_app
from probe.cli.commands.papers.papers import paper_app
from probe.cli.commands.projects.experiments import experiment_app, version_app
from probe.cli.commands.projects.lineage import edge_app
from probe.cli.commands.projects.projects import project_app
from probe.cli.commands.projects.run_groups import group_app
from probe.cli.commands.projects.sources import code_app, reference_app
from probe.cli.commands.runs.runs import run_app
from probe.cli.commands.runs.spans import span_app
from probe.cli.commands.runs.trial import trial_app
from probe.cli.commands.session.probe_config import ignore_app
from probe.cli.commands.session.session import session_app
from probe.cli.commands.session.statusline import statusline_app


if __name__ == "__main__":  # run as a script: call the one module every piece shares,
    import importlib  # not a second copy of this door (its mounts would run twice)

    raise SystemExit(importlib.import_module("probe.cli.main").main())

# -- every piece of the old module, loaded first
#: The old module's pieces, in the split's load order: a write through the door reaches these only.
_PIECES = (
    "probe.cli.commands.commands",
    "probe.cli.cli",
    "probe.cli.commands.metric_pick",
    "probe.cli.commands.artifacts.manifest",
    "probe.cli.connection",
    "probe.cli.commands.artifacts.artifacts",
    "probe.cli.commands.entity_text",
    "probe.cli.commands.json_print",
    "probe.cli.commands.machine.json_command",
    "probe.cli.wizard.agent_flags",
    "probe.cli.commands.machine.outbox",
    "probe.cli.commands.refs",
    "probe.cli.commands.notes.notes",
    "probe.cli.commands.papers.papers",
    "probe.cli.commands.tags",
    "probe.cli.commands.runs.runs",
    "probe.cli.commands.session.session",
    "probe.cli.lifecycle.update_spawn",
    "probe.cli.commands.account.access",
    "probe.cli.commands.account.account",
    "probe.cli.commands.account.context",
    "probe.cli.commands.account.mcp",
    "probe.cli.commands.account.token",
    "probe.cli.commands.account.workspace",
    "probe.cli.commands.artifacts.anchors",
    "probe.cli.commands.artifacts.download",
    "probe.cli.commands.artifacts.enqueue",
    "probe.cli.commands.artifacts.manage",
    "probe.cli.commands.artifacts.multipart",
    "probe.cli.commands.artifacts.row_checks",
    "probe.cli.commands.artifacts.shared_folder",
    "probe.cli.commands.delete",
    "probe.cli.commands.docs.docs",
    "probe.cli.commands.flag_values",
    "probe.cli.commands.machine.backfill",
    "probe.cli.commands.machine.doctor",
    "probe.cli.commands.machine.machine",
    "probe.cli.commands.machine.offline_sync",
    "probe.cli.commands.machine.outbox_adopt",
    "probe.cli.commands.machine.wizard",
    "probe.cli.commands.metrics.log",
    "probe.cli.commands.metrics.metrics",
    "probe.cli.commands.metrics.views",
    "probe.cli.commands.notes.agent_rules",
    "probe.cli.commands.notes.edit",
    "probe.cli.commands.notes.fullness",
    "probe.cli.commands.notes.rewrite",
    "probe.cli.commands.notes.sub_notes",
    "probe.cli.commands.notes.targets",
    "probe.cli.commands.notes.team_note",
    "probe.cli.commands.papers.citations",
    "probe.cli.commands.papers.find",
    "probe.cli.commands.projects.experiments",
    "probe.cli.commands.projects.lineage",
    "probe.cli.commands.projects.projects",
    "probe.cli.commands.projects.run_groups",
    "probe.cli.commands.projects.sources",
    "probe.cli.commands.run_handle",
    "probe.cli.commands.runs.exec",
    "probe.cli.commands.runs.exec_launchers",
    "probe.cli.commands.runs.reads",
    "probe.cli.commands.runs.run_end",
    "probe.cli.commands.runs.spans",
    "probe.cli.commands.runs.tokens",
    "probe.cli.commands.runs.trial",
    "probe.cli.commands.session.initialize",
    "probe.cli.commands.session.probe_config",
    "probe.cli.commands.session.records",
    "probe.cli.commands.session.statusline",
    "probe.cli.commands.session.switch",
    "probe.cli.commands.snapshots.restore",
    "probe.cli.commands.snapshots.snapshots",
    "probe.cli.lifecycle.after_command",
    "probe.cli.lifecycle.lifecycle",
    "probe.cli.lifecycle.notices.capture",
    "probe.cli.lifecycle.notices.capture_repair",
    "probe.cli.lifecycle.notices.outbox",
    "probe.cli.lifecycle.notices.remote_update",
    "probe.cli.lifecycle.notices.settings_request",
    "probe.cli.lifecycle.notices.version",
    "probe.cli.wizard.account.device_prompt",
    "probe.cli.wizard.account.website_onboarding",
    "probe.cli.wizard.actions.account",
    "probe.cli.wizard.actions.actions",
    "probe.cli.wizard.actions.capabilities",
    "probe.cli.wizard.actions.configure",
    "probe.cli.wizard.actions.defaults",
    "probe.cli.wizard.actions.recorder",
    "probe.cli.wizard.actions.result_rows",
    "probe.cli.wizard.actions.settings",
    "probe.cli.wizard.actions.uninstall",
    "probe.cli.wizard.session.device_actions",
    "probe.cli.wizard.session.import_offer",
    "probe.cli.wizard.session.install",
    "probe.cli.wizard.session.run_lock",
    "probe.cli.wizard.session.session",
    "probe.cli.wizard.session.start",
    "probe.cli.wizard.session.update",
    "probe.cli.wizard.state.token_verify",
    "probe.shared.harness.harnesses.codex.env_warning",
    "probe.shared.harness.harnesses.codex.hook_fix",
    "probe.shared.harness.harnesses.pi.session_pin",
)
#: Pieces only some commands call (the wizard's and harnesses' helpers): read or written
#: through the door, they load then; the old module defined them as plain functions.
_DEFERRED = (
    "probe.cli.wizard.account.device_prompt",
    "probe.cli.wizard.account.website_onboarding",
    "probe.cli.wizard.actions.account",
    "probe.cli.wizard.actions.actions",
    "probe.cli.wizard.actions.capabilities",
    "probe.cli.wizard.actions.configure",
    "probe.cli.wizard.actions.defaults",
    "probe.cli.wizard.actions.recorder",
    "probe.cli.wizard.actions.result_rows",
    "probe.cli.wizard.actions.settings",
    "probe.cli.wizard.actions.uninstall",
    "probe.cli.wizard.session.device_actions",
    "probe.cli.wizard.session.import_offer",
    "probe.cli.wizard.session.install",
    "probe.cli.wizard.session.run_lock",
    "probe.cli.wizard.session.session",
    "probe.cli.wizard.session.start",
    "probe.cli.wizard.session.update",
    "probe.cli.wizard.state.token_verify",
    "probe.shared.harness.harnesses.codex.env_warning",
    "probe.shared.harness.harnesses.codex.hook_fix",
    "probe.shared.harness.harnesses.pi.session_pin",
)

# Every other piece loads here, as the old module ran whole on import.
for _piece in _PIECES:
    if _piece not in _DEFERRED:
        importlib.import_module(_piece)
del _piece


def _version_cb(value: bool) -> None:
    if value:
        typer.echo(f"probe {__version__}")
        raise typer.Exit()


@app.callback()
def _root(
    ctx: typer.Context,
    base_url: str = typer.Option(None, "--base-url"),
    spool_dir: str = typer.Option(
        None, "--spool-dir", help="outbox journal directory (or PROBE_OUTBOX_DIR)"
    ),
    write_mode: Optional[bool] = typer.Option(
        None,
        "--async/--sync",
        help="queue data writes to the local outbox and return immediately, or "
        "--sync to block until the server answers. Queueing is the DEFAULT for "
        "`log`, `span add` and RUN-anchored `artifact add`; PROBE_ASYNC=0 turns "
        "it off for those. `run end` is the delivery barrier and BLOCKS unless "
        "you pass --async. Every other command is always synchronous. Also "
        "accepted AFTER the subcommand, where it wins.",
    ),
    version: bool = typer.Option(
        False, "--version", callback=_version_cb, is_eager=True, help="show version"
    ),
) -> None:
    begin_command(base_url=base_url, spool_dir=spool_dir, write_mode=write_mode)
    if ctx.invoked_subcommand in _READ_ONLY_COMMANDS or _uninstall_invoked(ctx.invoked_subcommand):
        # An uninstall starts nothing either: no refresher, no update hand-off,
        # no capture heal, each of which would race what it removes.
        # No banner, no background refresher, no auto-update, no capture heal:
        # each of those can start a process or a request, and `probe status`
        # promises neither (the desktop app asks it on every focus).
        return
    _outbox_notice(lift=ctx.invoked_subcommand != "outbox")
    # The CLI's own auto-update trigger. Before this existed, auto-update fired
    # from exactly one place -- the Claude Code plugin's SessionStart hook -- so a
    # user who never started a session never updated, and a headless box never
    # updated at all. Both of these are read-only-and-spawn on the fast path; see
    # _version_notice for why its gate order is what it is.
    _version_notice()
    # Probe staff asked this machine to update now (research-os control/071).
    _remote_update_notice()
    # Probe staff opened a capture repair for this machine (research-os control/073).
    _capture_repair_notice()
    # Probe staff changed a setting on this machine (research-os control/074).
    _settings_request_notice()
    # Trigger surface B: the one place that runs exactly once per CLI
    # invocation. NOT transport.py's `agent_session_headers()`, which fires
    # per HTTP request and would ask this question many times per command.
    # Bounded internally to one spawn attempt per session per ten minutes.
    _ensure_capture_notice(ctx.invoked_subcommand)


# `probe setup` must keep working: it is printed on the live connect page, in
# shipped plugin copy, and in every PR description written before the rename.
# Registering the SAME function under both names means the alias can never drift
# from the real command's options.
app.command(name="setup", hidden=True, cls=_JsonCommand)(wizard)

# -- history import (0108) ---------------------------------------------------
from .commands.data.import_wandb import import_app  # noqa: E402 -- registration, not use

# -- the Probe daemon's key and record ----------------------------------------
from .commands.daemon.companion import companion_app  # noqa: E402 -- registration, not use

# -- the daemon itself (v2) and the questions it holds for the researcher -----
from .commands.daemon.daemon import approvals_cmd, ask_cmd, daemon_app, deny_cmd  # noqa: E402 -- registration, not use

# -- the machine-wide Probe service (plan T3) -----------------------------------
from .commands.machine.service import service_app  # noqa: E402 -- registration, not use

from .imports.desktop import app as desktop_app  # noqa: E402 -- registration, not use

# -- feedback about Probe, sent with the person's yes ----------------------------
from .commands.machine.feedback import feedback_app  # noqa: E402 -- registration, not use

# -- the data catalog: sources, datasets, checkpoints, provenance (data-catalog C5)
from .commands.data.data import checkpoint_app, dataset_app, source_app  # noqa: E402 -- registration, not use
from .commands.data.data import provenance as provenance_cmd  # noqa: E402 -- registration, not use
# Capy support was removed: `probe capy sync` is what an old Capy timer still runs.
from .install.capy_retire import capy_app  # noqa: E402 -- registration, not use

# -- summaries and Metrics-center visuals, kept by the recorder (writer-owns-summary)
from ..shared.notes.summary.checkout_push import summary_app  # noqa: E402 -- registration, not use
from ..shared.notes.summary.visuals import visuals_app  # noqa: E402 -- registration, not use

# -- local files: a draft changed in place, a data file previewed (daemon `bash`)
from .commands.notes.drafts import draft_app, file_app  # noqa: E402 -- registration, not use

app.add_typer(import_app, name="import")

app.add_typer(companion_app, name="companion")

app.add_typer(daemon_app, name="daemon")

app.add_typer(service_app, name="service")

app.add_typer(desktop_app, name="desktop")

app.add_typer(feedback_app, name="feedback")

app.add_typer(source_app, name="source")
app.add_typer(dataset_app, name="dataset")
app.add_typer(checkpoint_app, name="checkpoint")
app.command("provenance")(provenance_cmd)

app.add_typer(capy_app, name="capy", hidden=True)
app.command("approvals")(approvals_cmd)

app.add_typer(summary_app, name="summary")
app.add_typer(visuals_app, name="visuals")

app.add_typer(draft_app, name="draft")
app.add_typer(file_app, name="file")
app.command("deny")(deny_cmd)
app.command("ask")(ask_cmd)

app.add_typer(mcp_app, name="mcp")
app.add_typer(context_app, name="context")
app.add_typer(workspace_app, name="workspace")
app.add_typer(project_app, name="project")
app.add_typer(access_group_app, name="access-group")
workspace_app.add_typer(writers_app, name="writers")
app.add_typer(paper_app, name="paper")
project_app.add_typer(reference_app, name="reference")
project_app.add_typer(code_app, name="code")
app.add_typer(token_app, name="token")
app.add_typer(run_app, name="run")
app.add_typer(metrics_app, name="metrics")
app.add_typer(statusline_app, name="statusline")
app.add_typer(session_app, name="session")
app.add_typer(ignore_app, name="ignore")
app.add_typer(views_app, name="views")
app.add_typer(series_app, name="series")
app.add_typer(span_app, name="span")
app.add_typer(artifact_app, name="artifact")
app.add_typer(shared_app, name="shared")
app.add_typer(trial_app, name="trial")
app.add_typer(outbox_app, name="outbox")
app.add_typer(notes_app, name="notes")
app.add_typer(rules_app, name="agent-rules")
app.add_typer(experiment_app, name="experiment")
app.add_typer(group_app, name="group")
app.add_typer(edge_app, name="edge")
app.add_typer(version_app, name="version")

# W&B import. Its own module because it owns a third-party dependency the rest of
# the CLI does not have: `wandb` is optional, and its absence must degrade the
# import rather than break `probe log`.
from .commands.data.wandb import app as wandb_app  # noqa: E402

app.add_typer(wandb_app, name="wandb")

# Every piece has registered its commands: each group lists them as `--help` always has.
for _group in COMMAND_GROUPS:
    _group.put_commands_in_order()
del _group

#: What a loose-file write prints once the server has frozen them (C6).
FILES_FROZEN = (
    "error: the team's loose workspace and Shared files are read-only now (list, download and delete "
    "still work). Register data as a team dataset with `probe dataset add PATH --name NAME`, or file "
    "the file under a run or project: `probe artifact add RUN FILE`, `probe artifact add FILE --project P`."
)

#: The loose-file writes the freeze refuses: `shared add|share|unshare`, and
#: `artifact add|version-add` aimed at a workspace or the Shared folder.
_LOOSE_FILE_VERBS = frozenset({("shared", "add"), ("shared", "share"), ("shared", "unshare")})
_LOOSE_FILE_FLAGS = frozenset({"--workspace", "--shared"})


def _loose_file_write(args: list[str], exc: errors.RosError) -> bool:
    """Was this 410 the freeze refusing a loose workspace or Shared file? A
    command that names one (`shared add|share|unshare`, `artifact add
    --workspace|--shared`), or the server's own `client_too_old` on an
    `artifact version-add` (whose target's anchor the command does not show:
    any other 410 there is the server's to explain)."""
    words = tuple(session_marker.command_words(list(args))[:2])
    if words in _LOOSE_FILE_VERBS:
        return True
    if words == ("artifact", "add"):
        own = args[: args.index("--")] if "--" in args else args
        return any(a in _LOOSE_FILE_FLAGS or a.split("=", 1)[0] in _LOOSE_FILE_FLAGS for a in own)
    return words == ("artifact", "version-add") and isinstance(exc, errors.ClientTooOldError)


#: Did Probe refuse the credential itself (`reads.key_refused`)?
_key_refused = reads.key_refused


def _report_error(exc: BaseException) -> int:
    """`reads.report_error` on this process's stderr: the daemon's own `probe`
    commands carry `PROBE_DAEMON_SESSION`."""
    code = reads.report_error(exc, daemon_session=bool(os.environ.get("PROBE_DAEMON_SESSION")))
    assert code is not None, exc
    return code


def main(argv: list[str] | None = None) -> int:
    """Run the CLI, returning a process exit code (never calls sys.exit itself)."""
    from .commands.machine import service as service_cli
    from .lifecycle import write_gate

    # The CLI's interpreter, for whatever has to start the Probe service (a tap,
    # pi, the app): one small read when it is already recorded.
    service_cli.record_runtime()
    args, directed = write_gate.split_directed(sys.argv[1:] if argv is None else argv)
    command = session_marker.command_words(args)[:1]
    if command and command[0] in _READ_ONLY_COMMANDS:
        # `probe status` reads no session and must start no process: finding
        # one walks this process's ancestors, which is `ps` where there is no
        # /proc (macOS), and the desktop app asks on every focus.
        agent_session.forgo_harness_process_session()
    else:
        # A harness that puts no session id in its shells (Kimi Code): find the
        # session from the harness process before the write gate reads it.
        agent_session.adopt_harness_process_session()
    _conn.directed = directed
    excluded = write_gate.excluded_refusal(args)
    if excluded is not None:
        message, child = excluded
        print(message, file=sys.stderr)
        if child is not None:
            try:
                os.execvp(child[0], child)
            except OSError as exc:
                print(f"could not run {child[0]!r}: {exc}", file=sys.stderr)
                return 127
        return write_gate.EXIT_REFUSED
    refused = write_gate.refusal(args, directed=directed)
    if refused:
        child = write_gate.exec_child(args)
        if child is not None:
            state = session_marker.session_state(agent_session.session_id_from_env() or "")
            print(
                write_gate.EXEC_UNRECORDED.format(state=session_marker.state_label(state)),
                file=sys.stderr,
            )
            try:
                os.execvp(child[0], child)
            except OSError as exc:
                print(f"could not run {child[0]!r}: {exc}", file=sys.stderr)
                return 127
        print(refused, file=sys.stderr)
        return write_gate.EXIT_REFUSED
    try:
        result = app(args=args, prog_name="probe", standalone_mode=False)
        # NB: --help/--version/explicit typer.Exit don't raise here — click catches
        # Exit internally (standalone_mode=False) and RETURNS the code, so it flows
        # through the `return result` below. The except clauses catch what actually
        # propagates: usage errors (ClickException), Abort, model ValidationError.
    except typer.Exit as exc:  # defensive: a typer.Exit that does propagate
        return int(exc.exit_code)
    except typer.Abort:
        print("aborted", file=sys.stderr)
        return 1
    except errors.RosError as exc:
        if exc.status == 410 and not getattr(exc, "in_trash", False) and _loose_file_write(args, exc):
            # The freeze (data-catalog C6): the server answers a new loose
            # workspace or Shared file with an "upgrade" 410 meant for older
            # clients. This one already knows where the file goes instead.
            print(FILES_FROZEN, file=sys.stderr)
            return 1
        # A plan limit (402) says its ceiling and how to lift it; any other Probe
        # error is one `error:` line, and under the daemon a refused key adds the
        # line it stops on (`reads.report_error`, shared with the daemon host).
        return _report_error(exc)
    except (ClickException, ValidationError, OSError) as exc:
        # Usage errors (exit 2), a CLI string the generated model refused (2), a
        # bad local path (1): never a traceback.
        return _report_error(exc)
    except SystemExit as exc:  # defensive: coerce any stray SystemExit to a code
        code = exc.code
        if isinstance(code, int):
            return code
        if code is not None:
            print(str(code), file=sys.stderr)
            return 1
        return 0
    except Exception as exc:
        # Everything a user can do wrong has a branch above, so reaching here
        # means a BUG. Report it, then RE-RAISE: the traceback is what the
        # operator debugs from, and swallowing it to file a report would trade
        # their diagnosis for ours.
        from probe.cli import telemetry as telemetry_mod

        telemetry_mod.report_crash(exc, surface="cli", base_url=_conn.base_url)
        raise
    code = result if isinstance(result, int) else 0
    if code == 0 and _UNDELIVERED.lost:
        # A write that reached neither Probe nor the outbox: the command did
        # not do its job, whatever it printed (`_report_undelivered` said so).
        return 1
    if code == 0 and not _UNDELIVERED.total:
        _label_status_line(args)
    if code == 0:
        _remind_summary(args, offline=bool(_UNDELIVERED.total))
    return code
from probe.cli.commands.commands import ClickException  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _UNDELIVERED, _conn, begin_command  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.lifecycle.after_command import _label_status_line, _remind_summary  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.lifecycle.lifecycle import _READ_ONLY_COMMANDS, _uninstall_invoked  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.lifecycle.notices.capture import _ensure_capture_notice  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.lifecycle.notices.capture_repair import _capture_repair_notice  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.lifecycle.notices.outbox import _outbox_notice  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.lifecycle.notices.remote_update import _remote_update_notice  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.lifecycle.notices.settings_request import _settings_request_notice  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.lifecycle.notices.version import _version_notice  # noqa: E402 -- pieces need each other; the front door loads this one first


# -- front door: every piece's names, served live ---------------------------------
from probe.foundation.front_door.front_door import serve_pieces  # noqa: E402 -- after every piece loads

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    "contextlib": "probe.cli.commands.artifacts.enqueue",
    "contextvars": "probe.cli.wizard.session.run_lock",
    "dataclasses": "probe.cli.commands.machine.outbox",
    "hashlib": "probe.cli.commands.artifacts.download",
    "json": "probe.cli.commands.account.mcp",
    "math": "probe.cli.commands.notes.fullness",
    "os": "probe.cli.commands.account.mcp",
    "re": "probe.cli.commands.machine.outbox_adopt",
    "shlex": "probe.cli.commands.account.mcp",
    "subprocess": "probe.cli.lifecycle.update_spawn",
    "sys": "probe.cli.commands.account.account",
    "uuid": "probe.cli.commands.notes.notes",
    "wire_name": "probe.cli.commands.snapshots.restore",
    "tempfile": "probe.cli.commands.papers.find",
    "textwrap": "probe.cli.commands.notes.rewrite",
    "time": "probe.cli.connection",
    "Sequence": "probe.cli.wizard.actions.actions",
    "Callable": "probe.cli.commands.metric_pick",
    "dataclass": "probe.cli.connection",
    "Enum": "probe.cli.commands.metric_pick",
    "Path": "probe.cli.commands.account.mcp",
    "Optional": "probe.cli.commands.account.mcp",
    "Any": "probe.cli.commands.metric_pick",
    "TYPE_CHECKING": "probe.cli.commands.artifacts.anchors",
    "Client": "probe.cli.connection",
    "typer": "probe.cli.cli",
    "ValidationError": "probe.cli.commands.snapshots.snapshots",
    "errors": "probe.cli.commands.account.account",
    "client_version_headers": "probe.cli.connection",
    "Scope": "probe.cli.commands.account.token",
    "PaperMode": "probe.cli.commands.papers.find",
    "PaperExpansion": "probe.cli.commands.papers.find",
    "MetricReduce": "probe.cli.commands.metric_pick",
    "MetricGoal": "probe.cli.commands.metric_pick",
    "LineageRelation": "probe.cli.commands.projects.lineage",
    "LineageEntityType": "probe.cli.commands.projects.lineage",
    "CitationDirection": "probe.cli.commands.papers.citations",
    "AnchorLevel": "probe.cli.commands.artifacts.manage",
    "Anchor": "probe.cli.commands.artifacts.anchors",
    "_FILE_ANCHORS": "probe.cli.commands.artifacts.manifest",
    "use_context": "probe.cli.commands.account.account",
    "save_context": "probe.cli.commands.account.account",
    "resolve": "probe.cli.commands.account.account",
    "load_file": "probe.cli.commands.account.context",
    "load_context": "probe.cli.commands.account.account",
    "delete_context": "probe.cli.commands.account.context",
    "current_context_name": "probe.cli.commands.account.account",
    "config_path": "probe.cli.commands.account.mcp",
    "clear_context": "probe.cli.commands.account.account",
    "WORKSPACE_HANDOVER": "probe.cli.commands.account.workspace",
    "DEFAULT_BASE_URL": "probe.cli.commands.account.account",
    "session_marker": "probe.cli.commands.account.context",
    "agent_session": "probe.cli.commands.papers.find",
    "daemon_channel": "probe.cli.commands.runs.exec",
    "nonfinite_to_wire": "probe.cli.commands.metrics.metrics",
    "canonical_tags": "probe.cli.commands.tags",
    "hostname": "probe.cli.commands.account.mcp",
    "device_login": "probe.cli.commands.account.account",
    "device_authorize": "probe.cli.commands.account.mcp",
    "credentials_by_grant": "probe.cli.commands.account.mcp",
    "OnboardingRequired": "probe.cli.commands.account.account",
    "DevicePrompt": "probe.cli.wizard.account.device_prompt",
    "DeviceLoginError": "probe.cli.commands.account.account",
    "NotFoundError": "probe.cli.commands.runs.runs",
    "_checkpoints_sdk": "probe.cli.commands.artifacts.download",
    "normalize_artifact_kind": "probe.cli.commands.artifacts.row_checks",
    "ArtifactKind": "probe.cli.commands.artifacts.row_checks",
    "USER_ARTIFACT_KINDS": "probe.cli.commands.artifacts.artifacts",
    "DEFAULT_ARTIFACT_KIND": "probe.cli.commands.artifacts.manifest",
    "name_with_extension": "probe.cli.commands.artifacts.row_checks",
    "artifact_kind_for": "probe.cli.commands.artifacts.artifacts",
    "reference_fields": "probe.cli.commands.artifacts.artifacts",
    "GROUP_NOTES_REMOVED": "probe.cli.commands.projects.run_groups",
    "FILE_NOTES_REMOVED": "probe.cli.commands.artifacts.manage",
    "_SNAPSHOT_REFERENCE_OVER_BYTES": "probe.cli.commands.artifacts.manifest",
    "_UNRESOLVED_FALLBACK": "probe.cli.commands.snapshots.snapshots",
    "Surface": "probe.cli.connection",
    "plugin_cli": "probe.cli.wizard.actions.configure",
    "refs": "probe.cli.commands.artifacts.anchors",
    "statusline": "probe.cli.commands.session.statusline",
    "reads": "probe.cli.commands.json_print",
    "Conn": "probe.cli.connection",
    "_conn": "probe.cli.connection",
    "_resolve_write_mode": "probe.cli.connection",
    "write_mode_opt": "probe.cli.connection",
    "_IMPOSSIBLE_IN_A_REF": "probe.cli.commands.refs",
    "_check_ref_shape": "probe.cli.commands.refs",
    "Relation": "probe.cli.commands.runs.runs",
    "EndStatus": "probe.cli.commands.runs.run_end",
    "RunCorrection": "probe.cli.commands.runs.runs",
    "Agg": "probe.cli.commands.metrics.metrics",
    "AssetMode": "probe.cli.commands.artifacts.artifacts",
    "_kv_pairs": "probe.cli.commands.flag_values",
    "_json_value": "probe.cli.commands.flag_values",
    "_text_value": "probe.cli.commands.flag_values",
    "_warn_notes_ignored": "probe.cli.commands.flag_values",
    "_warn_file_notes_ignored": "probe.cli.commands.flag_values",
    "_DISPLAY_CONTROLS": "probe.cli.commands.papers.citations",
    "_print_json": "probe.cli.commands.json_print",
    "_print_rendered": "probe.cli.commands.json_print",
    "_select_fields": "probe.cli.commands.json_print",
    "_api": "probe.cli.commands.refs",
    "_emit": "probe.cli.commands.json_print",
    "_FIELDS_OPTION": "probe.cli.commands.json_print",
    "_print_link": "probe.cli.commands.json_print",
    "_show_device_prompt": "probe.cli.wizard.account.device_prompt",
    "_client_class": "probe.cli.connection",
    "_new_client": "probe.cli.connection",
    "_Undelivered": "probe.cli.connection",
    "_UNDELIVERED": "probe.cli.connection",
    "_report_undelivered": "probe.cli.connection",
    "_client": "probe.cli.connection",
    "_backfill_client": "probe.cli.connection",
    "_journal": "probe.cli.connection",
    "_outbox_journals": "probe.cli.connection",
    "_default_client": "probe.cli.connection",
    "_async_client": "probe.cli.connection",
    "_async_run": "probe.cli.commands.run_handle",
    "_kick_drainer": "probe.cli.connection",
    "_UPDATE_HOT_PATH_COMMANDS": "probe.cli.lifecycle.lifecycle",
    "_ASK_OUTSIDE_A_RUN": "probe.cli.lifecycle.lifecycle",
    "_RUN_ENV": "probe.cli.lifecycle.lifecycle",
    "_RUN_ANCESTORS_MAX": "probe.cli.lifecycle.lifecycle",
    "_WIZARD_COMMANDS": "probe.cli.lifecycle.lifecycle",
    "_READ_ONLY_COMMANDS": "probe.cli.lifecycle.lifecycle",
    "_uninstall_invoked": "probe.cli.lifecycle.lifecycle",
    "_SERVICE_ASK_EVERY_S": "probe.cli.lifecycle.update_spawn",
    "_SERVICE_ASK_STAMP": "probe.cli.lifecycle.update_spawn",
    "_SERVICE_COMMAND": "probe.cli.lifecycle.lifecycle",
    "_REMOTE_ASK_EVERY_S": "probe.cli.lifecycle.notices.remote_update",
    "_REMOTE_ASK_STAMP": "probe.cli.lifecycle.notices.remote_update",
    "_CAPTURE_REPAIR_EVERY_S": "probe.cli.lifecycle.notices.capture_repair",
    "_CAPTURE_REPAIR_STAMP": "probe.cli.lifecycle.notices.capture_repair",
    "CAPTURE_REPAIR_PATH": "probe.cli.lifecycle.notices.capture_repair",
    "CAPTURE_REPAIR_APPLIED_PATH": "probe.cli.lifecycle.notices.capture_repair",
    "_SETTINGS_REQUEST_EVERY_S": "probe.cli.lifecycle.notices.settings_request",
    "_SETTINGS_REQUEST_STAMP": "probe.cli.lifecycle.notices.settings_request",
    "_REMOTE_UPDATE_SKIP_COMMANDS": "probe.cli.lifecycle.lifecycle",
    "_DIAGNOSE_MAX_AGE_S": "probe.cli.wizard.session.session",
    "_ROOT_OPTIONS_WITH_VALUES": "probe.cli.lifecycle.lifecycle",
    "_invoked_command": "probe.cli.lifecycle.lifecycle",
    "_CLI_UPDATE_EVERY_S": "probe.cli.lifecycle.notices.version",
    "_CLI_UPDATE_STAMP": "probe.cli.lifecycle.notices.version",
    "_version_notice": "probe.cli.lifecycle.notices.version",
    "_update_trigger": "probe.cli.lifecycle.notices.version",
    "_retry_owed_pi_update": "probe.cli.lifecycle.notices.version",
    "_ensure_pi_pin": "probe.shared.harness.harnesses.pi.session_pin",
    "_extension_session_start": "probe.cli.lifecycle.notices.version",
    "_capture_block": "probe.cli.commands.session.session",
    "_effective": "probe.cli.commands.session.session",
    "_ensure_capture_notice": "probe.cli.lifecycle.notices.capture",
    "_spawn_detached": "probe.cli.lifecycle.update_spawn",
    "_spawn_version_refresh": "probe.cli.lifecycle.update_spawn",
    "_spawn_update": "probe.cli.lifecycle.update_spawn",
    "_service_owns_updates": "probe.cli.lifecycle.update_spawn",
    "_ask_service_to_update": "probe.cli.lifecycle.update_spawn",
    "_hand_update_to_service": "probe.cli.lifecycle.update_spawn",
    "_inside_a_run": "probe.cli.lifecycle.lifecycle",
    "_claim_window": "probe.cli.lifecycle.lifecycle",
    "_remote_update_notice": "probe.cli.lifecycle.notices.remote_update",
    "_capture_repair_notice": "probe.cli.lifecycle.notices.capture_repair",
    "_settings_request_notice": "probe.cli.lifecycle.notices.settings_request",
    "_repair_identity_is_the_files": "probe.cli.lifecycle.lifecycle",
    "_repair_requested_at": "probe.cli.lifecycle.notices.capture_repair",
    "_RepairApplied": "probe.cli.lifecycle.notices.capture_repair",
    "_apply_capture_repair": "probe.cli.lifecycle.notices.capture_repair",
    "_spawn_session_start_update": "probe.cli.lifecycle.update_spawn",
    "_spawn_autoupdate": "probe.cli.lifecycle.update_spawn",
    "_hold_run_with_service": "probe.cli.commands.runs.exec",
    "_release_run_with_service": "probe.cli.commands.runs.exec",
    "_apply_deferred_update": "probe.cli.lifecycle.update_spawn",
    "_utc_minute": "probe.cli.lifecycle.notices.outbox",
    "_lift_stale_pause": "probe.cli.lifecycle.notices.outbox",
    "_outbox_notice": "probe.cli.lifecycle.notices.outbox",
    "run_lock_touch_lease": "probe.cli.commands.runs.runs",
    "_SUBMIT_LAUNCHERS": "probe.cli.commands.runs.exec_launchers",
    "_LAUNCHER_ALIASES": "probe.cli.commands.runs.exec_launchers",
    "_launcher_name": "probe.cli.commands.runs.exec_launchers",
    "_launcher_key": "probe.cli.commands.runs.exec_launchers",
    "_submit_template": "probe.cli.commands.runs.exec_launchers",
    "_SUBMIT_LAUNCHERS_WITH_TOKEN": "probe.cli.commands.runs.exec_launchers",
    "_job_token_env": "probe.cli.commands.runs.tokens",
    "_predates_run_tokens": "probe.cli.commands.runs.tokens",
    "_mint_handoff_token": "probe.cli.commands.runs.tokens",
    "_forwarding_hint": "probe.cli.commands.runs.exec_launchers",
    "_is_submit_launcher": "probe.cli.commands.runs.exec_launchers",
    "_run_handle": "probe.cli.commands.run_handle",
    "_apply_tag_ops": "probe.cli.commands.tags",
    "_tag_flags_given": "probe.cli.commands.tags",
    "_set_verb_tags": "probe.cli.commands.tags",
    "_tag_verb_flow": "probe.cli.commands.tags",
    "ClickException": "probe.cli.commands.commands",
    "UsageError": "probe.cli.commands.commands",
    "app": "probe.cli.cli",
    "begin_command": "probe.cli.connection",
    "_finish_website_onboarding": "probe.cli.wizard.account.website_onboarding",
    "login": "probe.cli.commands.account.account",
    "_login": "probe.cli.commands.account.account",
    "_hold_daemon_key": "probe.cli.commands.account.account",
    "logout": "probe.cli.commands.account.account",
    "whoami": "probe.cli.commands.account.account",
    "backfill": "probe.cli.commands.machine.backfill",
    "update_compat": "probe.cli.commands.machine.wizard",
    "_update_action_trigger": "probe.cli.wizard.session.update",
    "_hand_off_update": "probe.cli.wizard.session.update",
    "_root_options": "probe.cli.wizard.session.update",
    "_update_argv": "probe.cli.wizard.session.update",
    "doctor": "probe.cli.commands.machine.doctor",
    "_doctor_fix_codex_hooks": "probe.shared.harness.harnesses.codex.hook_fix",
    "_REPORT_FAILURES": "probe.cli.commands.machine.doctor",
    "_doctor_send": "probe.cli.commands.machine.doctor",
    "_doctor_bundle": "probe.cli.commands.machine.doctor",
    "status_command": "probe.cli.commands.machine.doctor",
    "_installable_agent": "probe.cli.wizard.agent_flags",
    "_agent_flags": "probe.cli.wizard.agent_flags",
    "_AGENT_FLAGS": "probe.cli.wizard.agent_flags",
    "_AGENT_HELP": "probe.cli.wizard.agent_flags",
    "_JSON_HELP": "probe.cli.commands.machine.json_command",
    "_BOTH_AGENTS": "probe.cli.wizard.agent_flags",
    "_agent_values": "probe.cli.wizard.agent_flags",
    "_explicit_agent_sources": "probe.cli.wizard.agent_flags",
    "_wizard_changes_device": "probe.cli.wizard.session.run_lock",
    "_JsonCommand": "probe.cli.commands.machine.json_command",
    "uninstall_cmd": "probe.cli.commands.machine.machine",
    "_run_uninstall": "probe.cli.wizard.actions.uninstall",
    "install": "probe.cli.commands.machine.machine",
    "repair": "probe.cli.commands.machine.machine",
    "_clear_wizard_imports": "probe.cli.commands.account.account",
    "_exit_wizard": "probe.cli.wizard.session.session",
    "wizard": "probe.cli.commands.machine.wizard",
    "_wizard_on_service": "probe.cli.commands.machine.wizard",
    "_start_device_state": "probe.cli.wizard.session.session",
    "_RUN_LOCK": "probe.cli.wizard.session.run_lock",
    "_wizard_run_lock": "probe.cli.wizard.session.run_lock",
    "_update_forced_past_setup": "probe.cli.wizard.session.run_lock",
    "_menu_holds_update_off": "probe.cli.wizard.session.run_lock",
    "_release_for_menu": "probe.cli.wizard.session.run_lock",
    "_unmark_menu": "probe.cli.wizard.session.run_lock",
    "_hold_for_action": "probe.cli.wizard.session.run_lock",
    "_begin_wizard_session": "probe.cli.wizard.session.start",
    "_run_chosen_action": "probe.cli.wizard.session.device_actions",
    "_wizard_session": "probe.cli.wizard.session.session",
    "REFRESH_STEP_LABEL": "probe.cli.wizard.actions.actions",
    "_problems": "probe.cli.wizard.actions.actions",
    "_record_install": "probe.cli.wizard.actions.result_rows",
    "_run_summary": "probe.cli.wizard.actions.result_rows",
    "_UpdateProgress": "probe.cli.wizard.session.update",
    "_update_agents": "probe.cli.wizard.session.update",
    "_old_way_unless_answered": "probe.cli.wizard.actions.actions",
    "_installing": "probe.cli.wizard.session.install",
    "_install_plan": "probe.cli.wizard.session.install",
    "_install_grants_held": "probe.cli.wizard.session.install",
    "_shared_selection": "probe.cli.wizard.session.install",
    "_select_and_run_imports": "probe.cli.wizard.session.import_offer",
    "_run_selected_imports": "probe.cli.wizard.session.import_offer",
    "_import_past_sessions": "probe.cli.wizard.session.import_offer",
    "_run_wizard_action": "probe.cli.wizard.actions.actions",
    "_run_configure_action": "probe.cli.wizard.actions.configure",
    "_run_configure_steps": "probe.cli.wizard.actions.configure",
    "_capability_fields": "probe.cli.wizard.actions.result_rows",
    "_record_configure": "probe.cli.wizard.actions.result_rows",
    "_opens_onboarding": "probe.cli.wizard.session.session",
    "_save_session_default": "probe.cli.wizard.actions.defaults",
    "_apply_recorder_pick": "probe.cli.wizard.actions.defaults",
    "_run_defaults_action": "probe.cli.wizard.actions.defaults",
    "_run_settings_action": "probe.cli.wizard.actions.settings",
    "_capability_setting_now": "probe.cli.wizard.actions.settings",
    "_labelled_problems": "probe.cli.wizard.actions.settings",
    "_recorder_page": "probe.cli.wizard.actions.recorder",
    "_run_recorder_action": "probe.cli.wizard.actions.recorder",
    "_record_recorder": "probe.cli.wizard.actions.result_rows",
    "_record_update": "probe.cli.wizard.actions.result_rows",
    "_record_removal": "probe.cli.wizard.actions.result_rows",
    "_record_device_sign_in": "probe.cli.wizard.actions.result_rows",
    "_needs_for_this_run": "probe.cli.wizard.session.install",
    "_ensure_daemon": "probe.cli.wizard.actions.recorder",
    "_sign_in_mint_consent": "probe.cli.wizard.actions.recorder",
    "_daemon_key_refused": "probe.cli.wizard.actions.recorder",
    "_run_daemon_page": "probe.cli.wizard.actions.recorder",
    "_authorize_companion": "probe.cli.wizard.actions.recorder",
    "_apply_capability_settings": "probe.cli.wizard.actions.settings",
    "CAPTURE_QUESTION_ASKED_ENV": "probe.cli.wizard.actions.capabilities",
    "_confirm_pending_capture": "probe.cli.wizard.actions.capabilities",
    "_capture_answer": "probe.cli.wizard.actions.capabilities",
    "_apply_capability_targets": "probe.cli.wizard.actions.capabilities",
    "_run_account_action": "probe.cli.wizard.actions.account",
    "_InstallationCompletion": "probe.cli.wizard.session.install",
    "_probe_already_installed": "probe.cli.wizard.session.install",
    "_register_local_capabilities": "probe.cli.wizard.session.install",
    "_McpGroup": "probe.cli.commands.account.mcp",
    "mcp_app": "probe.cli.commands.account.mcp",
    "mcp_token_app": "probe.cli.commands.account.mcp",
    "_READ_ONLY_SCOPES": "probe.cli.commands.account.mcp",
    "_normalize_token": "probe.cli.wizard.state.token_verify",
    "_checked_token": "probe.cli.wizard.state.token_verify",
    "_fingerprint": "probe.cli.wizard.state.token_verify",
    "_verify": "probe.cli.wizard.state.token_verify",
    "_verify_read": "probe.cli.wizard.state.token_verify",
    "mcp_token_set": "probe.cli.commands.account.mcp",
    "mcp_token_unset": "probe.cli.commands.account.mcp",
    "mcp_headers": "probe.cli.commands.account.mcp",
    "mcp_env": "probe.cli.commands.account.mcp",
    "_stale_literal_copies": "probe.cli.commands.account.mcp",
    "mcp_status": "probe.cli.commands.account.mcp",
    "MCP_TOOLS_MATCHED": "probe.cli.commands.account.mcp",
    "MCP_CALL_MATCHED": "probe.cli.commands.account.mcp",
    "_mcp_bridge": "probe.cli.commands.account.mcp",
    "mcp_tools": "probe.cli.commands.account.mcp",
    "mcp_call": "probe.cli.commands.account.mcp",
    "context_app": "probe.cli.commands.account.context",
    "_redact": "probe.cli.commands.account.context",
    "_context_row": "probe.cli.commands.account.context",
    "context_list": "probe.cli.commands.account.context",
    "context_show": "probe.cli.commands.account.context",
    "context_use": "probe.cli.commands.account.context",
    "context_delete": "probe.cli.commands.account.context",
    "PersonsDeclaration": "probe.cli.commands.metric_pick",
    "metric_opt": "probe.cli.commands.metric_pick",
    "goal_opt": "probe.cli.commands.metric_pick",
    "reduce_opt": "probe.cli.commands.metric_pick",
    "best_opt": "probe.cli.commands.metric_pick",
    "pick_reason_opt": "probe.cli.commands.metric_pick",
    "_metric_args": "probe.cli.commands.metric_pick",
    "_pick_args": "probe.cli.commands.metric_pick",
    "_persons_declaration": "probe.cli.commands.metric_pick",
    "_declare": "probe.cli.commands.metric_pick",
    "workspace_app": "probe.cli.commands.account.workspace",
    "_workspace_row": "probe.cli.commands.account.workspace",
    "workspace_list": "probe.cli.commands.account.workspace",
    "workspace_get": "probe.cli.commands.account.workspace",
    "workspace_rename": "probe.cli.commands.account.workspace",
    "workspace_set": "probe.cli.commands.account.workspace",
    "workspace_create": "probe.cli.commands.account.workspace",
    "workspace_delete": "probe.cli.commands.account.workspace",
    "workspace_use": "probe.cli.commands.account.workspace",
    "workspace_limit": "probe.cli.commands.account.workspace",
    "project_app": "probe.cli.commands.projects.projects",
    "access_group_app": "probe.cli.commands.account.access",
    "writers_app": "probe.cli.commands.account.access",
    "access_group_list": "probe.cli.commands.account.access",
    "access_group_create": "probe.cli.commands.account.access",
    "access_group_rename": "probe.cli.commands.account.access",
    "access_group_delete": "probe.cli.commands.account.access",
    "access_group_add": "probe.cli.commands.account.access",
    "access_group_remove": "probe.cli.commands.account.access",
    "workspace_writers_show": "probe.cli.commands.account.access",
    "workspace_writers_set": "probe.cli.commands.account.access",
    "_resolve_workspace": "probe.cli.commands.refs",
    "_bare_id": "probe.cli.commands.refs",
    "_ref": "probe.cli.commands.refs",
    "_filed_under": "probe.cli.commands.refs",
    "_ambient_project": "probe.cli.commands.refs",
    "_project_id": "probe.cli.commands.refs",
    "_container": "probe.cli.commands.runs.runs",
    "_project_slug": "probe.cli.commands.refs",
    "TRASH_DAYS": "probe.cli.commands.delete",
    "_confirm_delete": "probe.cli.commands.delete",
    "_confirmed_delete": "probe.cli.commands.delete",
    "DESCRIPTION_HELP": "probe.cli.commands.entity_text",
    "NOTES_HELP": "probe.cli.commands.entity_text",
    "RUN_REF_HELP": "probe.cli.commands.refs",
    "slug_ref": "probe.cli.commands.refs",
    "run_ref": "probe.cli.commands.refs",
    "description_opt": "probe.cli.commands.entity_text",
    "notes_opt": "probe.cli.commands.entity_text",
    "add_tag_opt": "probe.cli.commands.tags",
    "remove_tag_opt": "probe.cli.commands.tags",
    "set_tags_opt": "probe.cli.commands.tags",
    "AUTHORED_BY_HELP": "probe.cli.commands.entity_text",
    "AuthoredBy": "probe.cli.commands.entity_text",
    "_authored_by_value": "probe.cli.commands.entity_text",
    "authored_by_opt": "probe.cli.commands.entity_text",
    "entity_markdown_opt": "probe.cli.commands.entity_text",
    "ProjectKind": "probe.cli.commands.projects.projects",
    "LEGACY_PROJECT_KIND_ALIASES": "probe.cli.commands.projects.projects",
    "_PROJECT_KIND_CONTEXT": "probe.cli.commands.projects.projects",
    "project_create": "probe.cli.commands.projects.projects",
    "project_list": "probe.cli.commands.projects.projects",
    "project_get": "probe.cli.commands.projects.projects",
    "project_lineage": "probe.cli.commands.projects.projects",
    "project_branches": "probe.cli.commands.projects.projects",
    "project_contributors": "probe.cli.commands.projects.projects",
    "project_use": "probe.cli.commands.projects.projects",
    "project_set": "probe.cli.commands.projects.projects",
    "project_tag": "probe.cli.commands.projects.projects",
    "project_move": "probe.cli.commands.projects.projects",
    "project_delete": "probe.cli.commands.projects.projects",
    "paper_app": "probe.cli.commands.papers.papers",
    "paper_add": "probe.cli.commands.papers.papers",
    "paper_edges": "probe.cli.commands.papers.papers",
    "paper_list": "probe.cli.commands.papers.papers",
    "paper_update": "probe.cli.commands.papers.papers",
    "paper_tag": "probe.cli.commands.papers.papers",
    "paper_remove": "probe.cli.commands.papers.papers",
    "_CITE_CONTROLS": "probe.cli.commands.papers.citations",
    "_CITATIONS_DISABLED": "probe.cli.commands.papers.citations",
    "_cite_cell": "probe.cli.commands.papers.citations",
    "_cite_table": "probe.cli.commands.papers.citations",
    "_cite_when": "probe.cli.commands.papers.citations",
    "_cite_titled": "probe.cli.commands.papers.citations",
    "_cite_sync_lines": "probe.cli.commands.papers.citations",
    "_print_paper_citations": "probe.cli.commands.papers.citations",
    "_print_citation_graph": "probe.cli.commands.papers.citations",
    "paper_citations": "probe.cli.commands.papers.citations",
    "paper_graph": "probe.cli.commands.papers.citations",
    "_PAPER_FIND_SCOPE": "probe.cli.commands.papers.find",
    "PAPER_FIND_SNAPSHOT_TTL_S": "probe.cli.commands.papers.find",
    "paper_find": "probe.cli.commands.papers.find",
    "_stamp_paper_find": "probe.cli.commands.papers.find",
    "_paper_find_snapshot_path": "probe.cli.commands.papers.find",
    "_snapshot_fresh": "probe.cli.commands.papers.find",
    "_read_paper_find_snapshot": "probe.cli.commands.papers.find",
    "_write_paper_find_snapshot": "probe.cli.commands.papers.find",
    "DOCS_PRINT_CHARS": "probe.cli.commands.docs.docs",
    "DOCS_QUERY_MAX_CHARS": "probe.cli.commands.docs.docs",
    "DocsState": "probe.cli.commands.docs.docs",
    "docs": "probe.cli.commands.docs.docs",
    "_docs_block": "probe.cli.commands.docs.docs",
    "reference_app": "probe.cli.commands.projects.sources",
    "project_reference_add": "probe.cli.commands.projects.sources",
    "project_reference_remove": "probe.cli.commands.projects.sources",
    "code_app": "probe.cli.commands.projects.sources",
    "project_code_attach": "probe.cli.commands.projects.sources",
    "project_code_list": "probe.cli.commands.projects.sources",
    "project_code_detach": "probe.cli.commands.projects.sources",
    "project_code_confirm": "probe.cli.commands.projects.sources",
    "commits": "probe.cli.commands.projects.sources",
    "token_app": "probe.cli.commands.account.token",
    "token_list": "probe.cli.commands.account.token",
    "token_create": "probe.cli.commands.account.token",
    "token_revoke": "probe.cli.commands.account.token",
    "run_app": "probe.cli.commands.runs.runs",
    "run_start": "probe.cli.commands.runs.runs",
    "run_fork": "probe.cli.commands.runs.runs",
    "run_child": "probe.cli.commands.runs.runs",
    "run_set": "probe.cli.commands.runs.runs",
    "run_move": "probe.cli.commands.runs.runs",
    "run_list": "probe.cli.commands.runs.runs",
    "run_tag": "probe.cli.commands.runs.runs",
    "run_expect": "probe.cli.commands.runs.runs",
    "run_end": "probe.cli.commands.runs.run_end",
    "_DURATION_RE": "probe.cli.commands.runs.tokens",
    "_DURATION_UNIT_S": "probe.cli.commands.runs.tokens",
    "_parse_duration": "probe.cli.commands.runs.tokens",
    "_when": "probe.cli.commands.runs.tokens",
    "_NO_RUN_TOKENS": "probe.cli.commands.runs.tokens",
    "run_token": "probe.cli.commands.runs.tokens",
    "run_check": "probe.cli.commands.runs.reads",
    "_materialize_record": "probe.cli.commands.snapshots.restore",
    "run_reproduce": "probe.cli.commands.snapshots.restore",
    "run_delete": "probe.cli.commands.runs.runs",
    "run_series": "probe.cli.commands.runs.reads",
    "run_metrics": "probe.cli.commands.runs.reads",
    "run_inputs": "probe.cli.commands.runs.reads",
    "run_upstream": "probe.cli.commands.runs.reads",
    "_RAW_ARGS": "probe.cli.commands.runs.exec",
    "_RawArgsCommand": "probe.cli.commands.runs.exec",
    "_positional_after_separator": "probe.cli.commands.runs.exec",
    "exec": "probe.cli.commands.runs.exec",
    "log": "probe.cli.commands.metrics.log",
    "metrics_app": "probe.cli.commands.metrics.metrics",
    "metrics_grouped": "probe.cli.commands.metrics.metrics",
    "metrics_wide": "probe.cli.commands.metrics.metrics",
    "metrics_export": "probe.cli.commands.metrics.metrics",
    "metrics_plot": "probe.cli.commands.metrics.metrics",
    "_derived_series_points": "probe.cli.commands.metrics.metrics",
    "metrics_backfill": "probe.cli.commands.metrics.metrics",
    "metrics_delete": "probe.cli.commands.metrics.metrics",
    "coordinates": "probe.cli.commands.runs.reads",
    "statusline_app": "probe.cli.commands.session.statusline",
    "statusline_install": "probe.cli.commands.session.statusline",
    "statusline_uninstall": "probe.cli.commands.session.statusline",
    "statusline_status": "probe.cli.commands.session.statusline",
    "statusline_show": "probe.cli.commands.session.statusline",
    "session_app": "probe.cli.commands.session.session",
    "_resolve_agent_session": "probe.cli.commands.session.session",
    "_daemon_session": "probe.cli.commands.session.session",
    "DAEMON_STATUS_NOTE": "probe.cli.commands.session.session",
    "_require_tracking_state": "probe.cli.commands.session.switch",
    "_require_state": "probe.cli.commands.session.switch",
    "_state_word": "probe.cli.commands.session.session",
    "_state_display": "probe.cli.commands.session.session",
    "_switch_word": "probe.cli.commands.session.switch",
    "_expected_state": "probe.cli.commands.session.switch",
    "_state_block": "probe.cli.commands.session.switch",
    "_daemon_block": "probe.cli.commands.session.session",
    "_refuse_switch_from_agent": "probe.cli.commands.session.switch",
    "INLINE_FROM_AGENT": "probe.cli.commands.session.switch",
    "session_state_cmd": "probe.cli.commands.session.switch",
    "_capture_switched": "probe.cli.commands.session.switch",
    "session_untrack": "probe.cli.commands.session.switch",
    "session_track": "probe.cli.commands.session.switch",
    "session_toggle": "probe.cli.commands.session.switch",
    "session_initialize": "probe.cli.commands.session.initialize",
    "_probe_config_start": "probe.cli.commands.session.initialize",
    "_initializing_agent": "probe.cli.commands.session.initialize",
    "session_owed": "probe.cli.commands.session.records",
    "session_export": "probe.cli.commands.session.records",
    "session_send": "probe.cli.commands.session.records",
    "SESSION_DELETE_FROM_AGENT": "probe.cli.commands.session.records",
    "_refuse_session_deletion_from_agent": "probe.cli.commands.session.records",
    "session_delete": "probe.cli.commands.session.records",
    "session_undelete": "probe.cli.commands.session.records",
    "session_status": "probe.cli.commands.session.session",
    "_codex_env_warning": "probe.shared.harness.harnesses.codex.env_warning",
    "_probe_config_block": "probe.cli.commands.session.session",
    "session_parent": "probe.cli.commands.session.probe_config",
    "ignore_app": "probe.cli.commands.session.probe_config",
    "ignore_check": "probe.cli.commands.session.probe_config",
    "session_default": "probe.cli.commands.session.switch",
    "views_app": "probe.cli.commands.metrics.views",
    "_read_spec": "probe.cli.commands.metrics.views",
    "views_list": "probe.cli.commands.metrics.views",
    "views_show": "probe.cli.commands.metrics.views",
    "views_create": "probe.cli.commands.metrics.views",
    "views_preview": "probe.cli.commands.metrics.views",
    "views_data": "probe.cli.commands.metrics.views",
    "views_rename": "probe.cli.commands.metrics.views",
    "views_update": "probe.cli.commands.metrics.views",
    "views_delete": "probe.cli.commands.metrics.views",
    "series_app": "probe.cli.commands.metrics.metrics",
    "series_latest": "probe.cli.commands.metrics.metrics",
    "span_app": "probe.cli.commands.runs.spans",
    "span_add": "probe.cli.commands.runs.spans",
    "span_list": "probe.cli.commands.runs.spans",
    "span_get": "probe.cli.commands.runs.spans",
    "artifact_app": "probe.cli.commands.artifacts.artifacts",
    "_SLUG_ANCHORS": "probe.cli.commands.artifacts.anchors",
    "_anchor_id_for": "probe.cli.commands.artifacts.anchors",
    "_pick_anchor": "probe.cli.commands.artifacts.anchors",
    "CODE_KINDS": "probe.cli.commands.artifacts.row_checks",
    "_is_code_kind": "probe.cli.commands.artifacts.row_checks",
    "_say_where_the_kind_went": "probe.cli.commands.artifacts.row_checks",
    "_reference_after_code_check": "probe.cli.commands.artifacts.row_checks",
    "_validate_artifact_row": "probe.cli.commands.artifacts.row_checks",
    "_ping_presign": "probe.cli.commands.artifacts.enqueue",
    "_PING_TIMEOUT_SECONDS": "probe.cli.commands.artifacts.enqueue",
    "_PING_MAX_RETRIES": "probe.cli.commands.artifacts.enqueue",
    "_artifact_enqueue": "probe.cli.commands.artifacts.enqueue",
    "_artifact_enqueue_multipart": "probe.cli.commands.artifacts.multipart",
    "_outbox_lasts": "probe.cli.commands.artifacts.multipart",
    "_queue_is_deliverable": "probe.cli.commands.artifacts.enqueue",
    "_goes_in_parts": "probe.cli.commands.artifacts.multipart",
    "_artifact_add_async": "probe.cli.commands.artifacts.enqueue",
    "_fail_if_dropped": "probe.cli.commands.metrics.log",
    "_queue_client_if_possible": "probe.cli.commands.artifacts.enqueue",
    "_drain_colliding_uploads": "probe.cli.commands.artifacts.enqueue",
    "_MANIFEST_KEYS": "probe.cli.commands.artifacts.manifest",
    "_MANIFEST_REFERENCE_OVER_BYTES": "probe.cli.commands.artifacts.manifest",
    "_manifest_field": "probe.cli.commands.artifacts.manifest",
    "_manifest_rows": "probe.cli.commands.artifacts.manifest",
    "_plan_manifest_row": "probe.cli.commands.artifacts.manifest",
    "_AnchorFailure": "probe.cli.commands.artifacts.anchors",
    "_artifact_add_manifest": "probe.cli.commands.artifacts.manifest",
    "_artifact_add_anchored_multipart": "probe.cli.commands.artifacts.multipart",
    "artifact_add": "probe.cli.commands.artifacts.artifacts",
    "artifact_set": "probe.cli.commands.artifacts.manage",
    "artifact_move": "probe.cli.commands.artifacts.manage",
    "artifact_list": "probe.cli.commands.artifacts.manage",
    "artifact_tree": "probe.cli.commands.artifacts.manage",
    "artifact_download": "probe.cli.commands.artifacts.download",
    "_download_run_checkpoint": "probe.cli.commands.artifacts.download",
    "_download_checkpoint_folder": "probe.cli.commands.artifacts.download",
    "artifact_versions": "probe.cli.commands.artifacts.manage",
    "artifact_pin_impact": "probe.cli.commands.artifacts.manage",
    "artifact_version_add": "probe.cli.commands.artifacts.manage",
    "artifact_delete": "probe.cli.commands.artifacts.manage",
    "artifact_gc_uploads": "probe.cli.commands.artifacts.manage",
    "shared_app": "probe.cli.commands.artifacts.shared_folder",
    "shared_list": "probe.cli.commands.artifacts.shared_folder",
    "shared_add": "probe.cli.commands.artifacts.shared_folder",
    "shared_share": "probe.cli.commands.artifacts.shared_folder",
    "shared_unshare": "probe.cli.commands.artifacts.shared_folder",
    "shared_download": "probe.cli.commands.artifacts.shared_folder",
    "shared_delete": "probe.cli.commands.artifacts.shared_folder",
    "trial_app": "probe.cli.commands.runs.trial",
    "trial_list": "probe.cli.commands.runs.trial",
    "trial_get": "probe.cli.commands.runs.trial",
    "trial_set": "probe.cli.commands.runs.trial",
    "_trial_result_summary": "probe.cli.commands.runs.trial",
    "trial_stage": "probe.cli.commands.runs.trial",
    "trial_add": "probe.cli.commands.runs.trial",
    "trial_reconcile": "probe.cli.commands.runs.trial",
    "trial_export": "probe.cli.commands.runs.trial",
    "trial_drain": "probe.cli.commands.runs.trial",
    "trial_watch": "probe.cli.commands.runs.trial",
    "trial_expand": "probe.cli.commands.runs.trial",
    "link": "probe.cli.commands.runs.runs",
    "snapshot": "probe.cli.commands.snapshots.snapshots",
    "_snapshot_ref_verdicts": "probe.cli.commands.snapshots.snapshots",
    "snapshot_prune_refs": "probe.cli.commands.snapshots.snapshots",
    "snapshot_show": "probe.cli.commands.snapshots.restore",
    "_capture_rows": "probe.cli.commands.snapshots.restore",
    "_code_bytes_row": "probe.cli.commands.snapshots.restore",
    "_restore_captured_tree": "probe.cli.commands.snapshots.restore",
    "snapshot_restore": "probe.cli.commands.snapshots.restore",
    "outbox_app": "probe.cli.commands.machine.outbox",
    "_fold_drain_reports": "probe.cli.commands.machine.outbox",
    "_drain_foreground": "probe.cli.commands.machine.outbox",
    "_stored_login": "probe.cli.commands.machine.outbox_adopt",
    "_held_credentials": "probe.cli.commands.machine.outbox",
    "_print_held_credentials": "probe.cli.commands.machine.outbox",
    "outbox_status": "probe.cli.commands.machine.outbox",
    "outbox_drain": "probe.cli.commands.machine.outbox",
    "outbox_watch": "probe.cli.commands.machine.outbox",
    "outbox_retry": "probe.cli.commands.machine.outbox",
    "outbox_discard": "probe.cli.commands.machine.outbox",
    "_ADOPT_LOCK_TIMEOUT_S": "probe.cli.commands.machine.outbox_adopt",
    "outbox_adopt": "probe.cli.commands.machine.outbox_adopt",
    "outbox_pause": "probe.cli.commands.machine.outbox",
    "outbox_resume": "probe.cli.commands.machine.outbox",
    "flush": "probe.cli.commands.machine.outbox",
    "sync_offline": "probe.cli.commands.machine.offline_sync",
    "get": "probe.cli.commands.runs.reads",
    "run_get": "probe.cli.commands.runs.reads",
    "bundle": "probe.cli.commands.runs.reads",
    "notes_app": "probe.cli.commands.notes.notes",
    "rules_app": "probe.cli.commands.notes.agent_rules",
    "agent_rules_refresh": "probe.cli.commands.notes.agent_rules",
    "_notes_project": "probe.cli.commands.notes.notes",
    "_entity_notes_row": "probe.cli.commands.notes.notes",
    "notes_show": "probe.cli.commands.notes.notes",
    "notes_find": "probe.cli.commands.notes.notes",
    "notes_checkout": "probe.cli.commands.notes.notes",
    "notes_push": "probe.cli.commands.notes.notes",
    "notes_write": "probe.cli.commands.notes.notes",
    "_NOTE_TARGETS": "probe.cli.commands.notes.targets",
    "_sub_note_row_for_headroom": "probe.cli.commands.notes.targets",
    "_stderr_line": "probe.cli.commands.notes.targets",
    "_sub_notes_supported": "probe.cli.commands.notes.targets",
    "_sub_note_id_ref": "probe.cli.commands.notes.targets",
    "_resolve_sub_note_by_title": "probe.cli.commands.notes.targets",
    "_note_target": "probe.cli.commands.notes.targets",
    "_headroom_fields": "probe.cli.commands.notes.targets",
    "_CAP_REFUSALS": "probe.cli.commands.notes.rewrite",
    "_note_landed": "probe.cli.commands.notes.targets",
    "_notes_write": "probe.cli.commands.notes.rewrite",
    "_report_notes_headroom": "probe.cli.commands.notes.targets",
    "notes_list": "probe.cli.commands.notes.sub_notes",
    "notes_create": "probe.cli.commands.notes.sub_notes",
    "_NOTE_REWRITE_ATTEMPTS": "probe.cli.commands.notes.rewrite",
    "_note_carrier": "probe.cli.commands.notes.rewrite",
    "_send_note": "probe.cli.commands.notes.rewrite",
    "_stored_form": "probe.cli.commands.notes.rewrite",
    "_is_version": "probe.cli.commands.notes.rewrite",
    "_refuse_scrubbed_old": "probe.cli.commands.notes.rewrite",
    "_read_note": "probe.cli.commands.notes.rewrite",
    "_Unconfirmed": "probe.cli.commands.notes.rewrite",
    "_NO_VERSION_REPLY": "probe.cli.commands.notes.rewrite",
    "_GATEWAY_STATUSES": "probe.cli.commands.notes.rewrite",
    "_settle_unconfirmed": "probe.cli.commands.notes.rewrite",
    "_unconfirmed_reason": "probe.cli.commands.notes.rewrite",
    "_refuse_over_cap": "probe.cli.commands.notes.rewrite",
    "_rewrite_note": "probe.cli.commands.notes.rewrite",
    "_TEAM_LABEL": "probe.cli.commands.notes.edit",
    "_team_only": "probe.cli.commands.notes.edit",
    "_team_topped_up": "probe.cli.commands.notes.edit",
    "_write_team_note": "probe.cli.commands.notes.edit",
    "_team_payload": "probe.cli.commands.notes.edit",
    "_refuse_edit_match": "probe.cli.commands.notes.edit",
    "notes_append": "probe.cli.commands.notes.edit",
    "notes_edit": "probe.cli.commands.notes.edit",
    "notes_rename": "probe.cli.commands.notes.sub_notes",
    "notes_delete": "probe.cli.commands.notes.sub_notes",
    "_NOTES_STATUS_MAX_PAGES": "probe.cli.commands.notes.fullness",
    "_NOTES_STATUS_PAGE_SIZE": "probe.cli.commands.notes.fullness",
    "_is_count": "probe.cli.commands.notes.fullness",
    "_notes_status_row": "probe.cli.commands.notes.fullness",
    "notes_status": "probe.cli.commands.notes.fullness",
    "notes_team": "probe.cli.commands.notes.team_note",
    "notes_audit_advisory": "probe.cli.commands.notes.team_note",
    "_daemon_records": "probe.cli.commands.notes.team_note",
    "notes_sync": "probe.cli.commands.notes.team_note",
    "events": "probe.cli.commands.runs.reads",
    "experiment_app": "probe.cli.commands.projects.experiments",
    "_EXPERIMENT_TAGS_READ_ONLY": "probe.cli.commands.projects.experiments",
    "_EXPERIMENT_DESCRIPTION_RETIRED": "probe.cli.commands.projects.experiments",
    "experiment_create": "probe.cli.commands.projects.experiments",
    "experiment_fork": "probe.cli.commands.projects.experiments",
    "experiment_inherited": "probe.cli.commands.projects.experiments",
    "experiment_reproduce": "probe.cli.commands.projects.experiments",
    "experiment_freeze": "probe.cli.commands.projects.experiments",
    "experiment_get": "probe.cli.commands.projects.experiments",
    "experiment_set": "probe.cli.commands.projects.experiments",
    "experiment_move": "probe.cli.commands.projects.experiments",
    "experiment_list": "probe.cli.commands.projects.experiments",
    "experiment_tag": "probe.cli.commands.projects.experiments",
    "experiment_delete": "probe.cli.commands.projects.experiments",
    "experiment_edges": "probe.cli.commands.projects.experiments",
    "experiment_lineage": "probe.cli.commands.projects.experiments",
    "experiment_branch": "probe.cli.commands.projects.experiments",
    "group_app": "probe.cli.commands.projects.run_groups",
    "group_create": "probe.cli.commands.projects.run_groups",
    "group_list": "probe.cli.commands.projects.run_groups",
    "group_get": "probe.cli.commands.projects.run_groups",
    "group_set": "probe.cli.commands.projects.run_groups",
    "_PROJECT_END_TYPES": "probe.cli.commands.projects.lineage",
    "_EDGE_END_TYPES": "probe.cli.commands.projects.lineage",
    "edge_app": "probe.cli.commands.projects.lineage",
    "_edge_end": "probe.cli.commands.projects.lineage",
    "edge_add": "probe.cli.commands.projects.lineage",
    "_EVENT_ID": "probe.cli.commands.projects.lineage",
    "_edge_evidence": "probe.cli.commands.projects.lineage",
    "edge_remove": "probe.cli.commands.projects.lineage",
    "version_app": "probe.cli.commands.projects.experiments",
    "version_create": "probe.cli.commands.projects.experiments",
    "version_list": "probe.cli.commands.projects.experiments",
    "_remind_summary": "probe.cli.lifecycle.after_command",
    "_label_session": "probe.cli.lifecycle.after_command",
    "_label_status_line": "probe.cli.lifecycle.after_command",
    "_label_status_line_soon": "probe.cli.lifecycle.after_command",
}

serve_pieces(__name__, _HOMES, pieces=_PIECES, deferred=_DEFERRED)
