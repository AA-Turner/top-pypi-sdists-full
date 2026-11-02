"""probe doctor (--fix, --send, --bundle) and probe status: diagnose this machine's Probe and send a report."""

from __future__ import annotations

import contextlib
import json
import sys
from pathlib import Path

import typer
from ....shared.reads import reads
from probe.cli.cli import app


@app.command()
def doctor(
    fix: bool = typer.Option(
        False,
        "--fix",
        help="approve Probe's own hooks in Codex again (a plugin change switches them off), turn retired "
        "folder defaults (`<folder>/.probe/config.json`) into `.probe.config` files, and set aside "
        "dead-lettered writes that can never be delivered (a newer attempt took their run over, or "
        "the run no longer exists)",
    ),
    send: bool = typer.Option(
        False,
        "--send",
        help="send the Probe team a diagnostic report of this machine (logs, versions, the service's "
        "state; no credentials, no conversation) and print its id; with --bundle, send the debug log",
    ),
    bundle: bool = typer.Option(
        False,
        "--bundle",
        help="save the full debug log (a zip of Probe's logs, settings and this system's state, "
        "credentials and conversations left out) and print where; --send also sends it",
    ),
    out: Path = typer.Option(
        None, "--out", help="--bundle: the folder to save the zip in (default: Probe's own debug folder)"
    ),
    as_json: bool = typer.Option(
        False, "--json", help="--bundle: the last stdout line is one JSON object, for a program"
    ),
) -> None:
    """Diagnostic: what is installed, on, and whether auto-update works.

    Prints the LAST UPDATE ATTEMPT, which is the only way to notice a detached
    auto-updater that has been silently failing. Read-only, except `--fix`,
    which approves Probe's hooks in Codex again, converts retired folder
    defaults and sets aside dead letters no retry can deliver. `--send` sends the Probe team a
    small diagnostic report; `--bundle` saves (and with `--send` sends) the
    full debug log.
    """
    from probe.shared.harness.harnesses.codex.hook_fix import _doctor_fix_codex_hooks
    if bundle:
        if fix:
            raise typer.BadParameter("--fix does not combine with --bundle")
        _doctor_bundle(send=send, out=out, as_json=as_json)
        return
    if out is not None or as_json:
        raise typer.BadParameter("--out and --json go with --bundle")
    if send:
        if fix:
            raise typer.BadParameter("--fix does not combine with --send")
        _doctor_send()
        return
    # Imported inside the body, not at module scope: cli/__init__ eagerly loads
    # this module, and `probe log` runs inside training loops.
    from probe.cli.wizard import doctor as doctor_impl

    from probe.cli.wizard.state.mcp_checks import refresh_mcp_token_verdict

    from probe.cli.lifecycle import service_calls

    refresh_mcp_token_verdict()  # one /v1/me: a refused read token reads "login needed"
    # Before the report, so its "Codex hooks" rows say what the fix left.
    codex_fixed = _doctor_fix_codex_hooks() if fix else []
    # And its outbox counts what `--fix` left: dead letters that can never land
    # (a superseded attempt's, a run that is gone) nag every session start.
    outbox_fixed = doctor_impl.drop_unrecoverable_dead_letters() if fix else []
    caps = doctor_impl.collect()
    # `probe doctor` fixes what it can: writes stranded under a dead credential
    # of this account are rescued now (never from `collect`, which `probe
    # status` runs on every focus of the desktop app).
    rescue = doctor_impl.rescue_outbox()
    if rescue and isinstance(caps.outbox_status, dict):
        caps.outbox_status = {**caps.outbox_status, "rescue": rescue}
    # So is the lifeboat (plan fool-proof-updates B4), with the keeper's
    # guards: installed or refreshed here too, where no Probe service ever runs
    # to do it at its start (a pod under no_new_privs).
    with contextlib.suppress(Exception):
        from probe.service import keeper

        keeper.refresh_lifeboat()
    from probe.cli.install import uninstall as uninstall_mod

    halfway = uninstall_mod.halfway_notice()  # first: it is why nothing of Probe starts or updates
    if halfway:
        print(f"{halfway}\n")
    print(
        doctor_impl.render(
            caps, codex_hooks=doctor_impl.codex_hook_rows(caps), service=service_calls.view()
        )
    )
    if codex_fixed:
        print("\n".join(["", "Codex hooks (--fix)", *(f"  {line}" for line in codex_fixed)]))
    if outbox_fixed:
        print("\n".join(["", "Outbox (--fix)", *(f"  {line}" for line in outbox_fixed)]))
    from probe.cli.wizard.doctor import probe_config_check as probe_config_cli

    rows = probe_config_cli.doctor_rows(fix=fix)
    if rows:
        print("\n".join(["", "Retired folder defaults", *rows]))


#: What `probe doctor --send` says for each reason a report did not land.
_REPORT_FAILURES = {
    "offline": "Probe could not be reached",
    "rate_limited": "too many reports were sent from this account in the last hour",
    "too_large": "the report was too large",
    "server": "the server could not take it",
    "unauthorized": "this machine is not signed in to Probe (`probe login`)",
}


def _doctor_send() -> None:
    """`probe doctor --send`: one manual diagnostic report (`probe.shared.reports`)."""
    from probe.shared import reports as report

    answer = report.send(auto=False, family=report.MANUAL_FAMILY, reason=report.MANUAL_REASON)
    if answer.sent:
        print(f"Sent diagnostic report {answer.id} to the Probe team")
        return
    why = _REPORT_FAILURES.get(answer.skipped or "", answer.skipped or "it was not sent")
    print(f"Could not send the diagnostic report: {why}.", file=sys.stderr)
    if answer.path:
        print(f"A copy is at {answer.path}", file=sys.stderr)
    raise typer.Exit(1)


def _doctor_bundle(*, send: bool, out: Path | None, as_json: bool) -> None:
    """`probe doctor --bundle [--send] [--out DIR] [--json]`: the debug log
    (`probe.core.debug_bundle`). With `--json`, every other line goes to stderr
    and the last stdout line is the contract's one object."""
    from probe.core import debug_bundle, events

    def human(size: int) -> str:
        return f"{size / (1024 * 1024):.1f} MB" if size >= 1024 * 1024 else f"{max(1, size // 1024)} KB"

    with contextlib.ExitStack() as stack:
        stream = stack.enter_context(events.redirect_stdout()) if as_json else sys.stdout
        try:
            built = debug_bundle.build(out_dir=out)
        except Exception as exc:  # noqa: BLE001 -- the app still gets its last line
            if as_json:
                stream.write(json.dumps({"error": "server", "status": None, "retry_after": None, "path": None})
                             + "\n")
            print(f"Could not write the debug log: {type(exc).__name__}: {exc}", file=sys.stderr)
            raise typer.Exit(1) from None
        if not send:
            if as_json:
                stream.write(json.dumps({"id": None, "bytes": built.bytes, "files": built.files,
                                         "skipped": built.skipped, "path": str(built.path)}) + "\n")
            else:
                print(f"Saved the debug log to {built.path} ({human(built.bytes)}, {built.files} files)")
                if built.skipped:
                    print(f"Skipped: {', '.join(built.skipped)} (README.txt says why)")
            return
        result, stage = debug_bundle.send_with_stage(built)
        if as_json:
            stream.write(json.dumps(result) + "\n")
        if "id" in result:
            if not as_json:
                print(f"Sent debug log {result['id']} ({human(result['bytes'])}) to the Probe team")
                print(f"A copy is at {result['path']}")
            return
        why = _REPORT_FAILURES.get(result["error"], result["error"])
        if stage is debug_bundle.Stage.UPLOAD and result["status"] == 401:
            why = "the upload expired; try again"  # a 401 on the slot, not the login
        print(f"Could not send the debug log: {why}. It is saved at {result['path']}", file=sys.stderr)
        raise typer.Exit(1)


@app.command("status")
def status_command(
    as_json: bool = typer.Option(
        False, "--json", help="one JSON object on stdout, for a program (schema: `probe.cli.status`)"
    ),
    refresh: bool = typer.Option(
        False,
        "--refresh",
        help="also ask the agents' own CLIs, the server and the MCP token check, all within --timeout",
    ),
    timeout: float = typer.Option(
        None,
        "--timeout",
        min=0.1,
        help="--refresh: seconds the whole read may take, every check included (default 10)",
    ),
) -> None:
    """This device's Probe install as one snapshot: account, agents, who records,
    the new-session default, auto-update, versions, the daemon, and whether a
    `probe wizard` is running. What the wizard's menu shows, as data.

    Local only by default: files, no network and no subprocess, so a program can
    ask on every focus. `--refresh` adds the slow checks the menu makes, all
    within one `--timeout` budget, each reported as {state, checked, error}.
    Exits 0 whatever the state; 2 for a usage error. The `--json` schema is
    `probe.cli.status`'s docstring.
    """
    from probe.cli.wizard.state import status as status_impl
    from probe.core import reads

    limit = status_impl.DEFAULT_TIMEOUT_S if timeout is None else timeout
    if not as_json:
        from probe.cli.install import uninstall as uninstall_mod

        halfway = uninstall_mod.halfway_notice()  # first: it is why nothing of Probe starts or updates
        if halfway:
            print(halfway)
        for line in status_impl.human_lines(reads.status(refresh=refresh, timeout=limit)):
            print(line)
        return
    # The one object on stdout, as `python -m probe.core.run status` writes it.
    reads.print_status(refresh=refresh, timeout=limit)
from probe.cli.commands.runs.reads import bundle, events  # noqa: E402 -- pieces need each other; the front door loads this one first
