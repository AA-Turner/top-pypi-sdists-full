"""probe outbox status/drain/watch/retry/discard/pause/resume and its `probe flush` alias: the durable write queue."""

from __future__ import annotations
import dataclasses
import os
import sys
from typing import Any, Optional

import typer

from probe.cli.commands.commands import register_group
from ....sdk import session_marker
from ....shared.reads import reads
from probe.cli.cli import app


# -- outbox (the async write journal) ---------------------------------------
outbox_app = typer.Typer(no_args_is_help=True, help="the durable async write outbox")

#: `probe outbox --help` order (outbox and outbox_adopt register them).
OUTBOX_GROUP = register_group(
    outbox_app,
    (
        "status", "drain", "watch", "retry", "discard", "adopt", "pause", "resume",
    ),
)


def _fold_drain_reports(parts: list) -> Any:
    """One report for `drain --all`. One journal's comes back untouched; for
    more, EVERY field folds -- counts add, flags OR, lists merge without
    repeats, sets and dicts merge, an optional value keeps its first -- so a
    field a later change adds to `DrainReport` (#2041's ``credential_held`` and
    ``held_reasons``) reaches the output instead of being dropped by a copy of
    the six this command used to know."""
    import dataclasses

    if len(parts) == 1:
        return parts[0]
    combined = type(parts[0])()
    for part in parts:
        for spec in dataclasses.fields(combined):
            mine, theirs = getattr(combined, spec.name), getattr(part, spec.name)
            if theirs is None:
                continue
            if isinstance(theirs, bool):
                setattr(combined, spec.name, mine or theirs)
            elif isinstance(theirs, set):
                setattr(combined, spec.name, (mine or set()) | theirs)
            elif spec.default is None:
                # Optional: auth_status/auth_message/auth_context stay ONE
                # refusal's, never a mix of two.
                if mine is None:
                    setattr(combined, spec.name, theirs)
            elif isinstance(theirs, list):
                mine.extend(item for item in theirs if item not in mine)
            elif isinstance(theirs, dict):
                for key, value in theirs.items():
                    mine.setdefault(key, value)
            elif isinstance(theirs, (int, float)):
                setattr(combined, spec.name, mine + theirs)
            elif hasattr(theirs, "merge"):  # a `DiscardCounts` (T24's `superseded`)
                mine.merge(theirs)
    return combined


def _drain_foreground(run_ref: str | None = None, *, every_dir: bool = False) -> None:
    """Shared body of `probe outbox drain` and its `probe flush` alias.
    ``every_dir``: every outbox of this user on this machine (plan 1.5)."""
    from .... import analytics as telemetry
    from ....sdk.delivery.journal.failures.discards import DiscardCounts
    from ....sdk.delivery.outbox.drain.drain import drain
    from ....sdk.delivery.journal.paths import prune_credential_queues

    journals = _outbox_journals() if every_dir else [_journal()]
    parts = []
    for journal in journals:
        try:  # idle credential queues (#2041 round 3); never fails the drain
            relocated = DiscardCounts()
            prune_credential_queues(journal.dir, counts=relocated)
            telemetry.emit_outbox_discarded(relocated, reason=telemetry.DiscardReason.RELOCATED)
        except Exception:  # noqa: BLE001
            pass
        part = drain(journal, run_ref=run_ref)
        parts.append(part)
        if every_dir and len(journals) > 1:
            print(
                f"{journal.dir}: delivered {part.delivered}; "
                f"{part.dead_lettered} dead-lettered; {part.remaining} remaining"
            )
    report = _fold_drain_reports(parts)
    scope = f" for run {run_ref}" if run_ref else ""
    print(
        f"delivered {report.delivered}{scope}; "
        f"{report.dead_lettered} dead-lettered; {report.remaining} remaining"
    )
    if report.superseded.writes:
        # Gone from the queue without landing: said, so it never reads as delivered.
        print(
            f"{report.superseded.writes} write(s) set aside: a newer attempt took their run over, "
            "so the server refuses them for good (kept in the outbox's discarded/ folder)"
        )
    if report.credential_held or getattr(report, "close_held", 0):
        # The drain's own reasons: "another job's PROBE_TOKEN" is one of
        # several, and naming it for a re-login it cannot match misled people
        # (#2041 re-review).
        reasons = getattr(report, "held_reasons", None) or [
            "queued with a credential this shell does not have (another job's PROBE_TOKEN, "
            "or a token passed in code)"
        ]
        permanent = getattr(report, "permanently_held", 0)
        typer.echo(
            f"{report.credential_held + getattr(report, 'close_held', 0)} kept: {reasons[0]}"
            + "".join(f"\n  also: {reason}" for reason in reasons[1:])
            + (
                f"\n  ({permanent} of them no credential here will send: "
                "`probe outbox discard --held` drops those)"
                if permanent
                else ""
            ),
            err=True,
        )
        try:
            from ....sdk.delivery.journal.journal import Journal

            held_ops = [
                op for journal in journals for q in journal.namespaces() for _, op in q.pending()
            ]
            status = Journal.read_status(journals[0].dir) or {}
            _print_held_credentials(_held_credentials(held_ops, status, network=True))
        except Exception:  # noqa: BLE001 -- advice only; the counts above stand
            pass
    if report.auth_blocked:
        typer.echo(
            f"auth-blocked: {report.errors[-1] if report.errors else '401/403'} "
            f"— sign in again ({session_marker.WIZARD_HINT}); queued items were kept",
            err=True,
        )
    elif report.stopped_transient and report.errors:
        typer.echo(f"stopped on transient failure: {report.errors[-1]}", err=True)
    elif report.errors:
        # Dead-letter-only failures: every cause still reaches stderr.
        typer.echo(f"dead-lettered: {report.errors[-1]}", err=True)
    for message in report.errors[:-1] if report.errors else []:
        typer.echo(f"  {message}", err=True)
    if not report.clean:
        raise typer.Exit(2)


def _held_credentials(ops: list, status: dict, *, network: bool) -> list[dict]:
    """Per env/code credential whose queued writes nothing here holds
    (`reads.held_credentials`, over this process's environment)."""
    return reads.held_credentials(ops, status, network=network, env=os.environ)


def _print_held_credentials(entries: list[dict]) -> None:
    for entry in entries:
        holders = entry["holders"]
        who = (
            "; ".join(
                f"pid {h['pid']} ({' '.join(x for x in (h.get('program'), h.get('script')) if x)}"
                f", sdk {h.get('sdk') or '?'}) {h['state']}"
                for h in holders[-3:]
            )
            if holders
            else "holder unknown (its release records none)"
        )
        refused = f", refused {entry['refused_at']}" if entry.get("refused_at") else ""
        typer.echo(
            f"  credential {entry['fingerprint']} ({entry['source']}): {entry['writes']} write(s)"
            f"{refused}; {who}\n    next: {entry['next']}",
            err=True,
        )


@outbox_app.command("status")
def outbox_status(
    verbose: bool = typer.Option(False, "--verbose", help="list every queued/failed op"),
    run: Optional[str] = typer.Option(None, "--run", help="scope counts and ops to one run"),
) -> None:
    """Outbox summary. Exit 0 when everything is delivered, 2 otherwise."""
    _emit(reads.outbox_status(_api(None, pretty=sys.stdout.isatty()), _journal(), _outbox_journals()[1:],
                              verbose, run))


@outbox_app.command("drain")
def outbox_drain(
    run: Optional[str] = typer.Option(None, "--run", help="drain only this run's ops"),
    every_dir: bool = typer.Option(
        False, "--all", help="every outbox on this machine (rank-* dirs, the $TMPDIR fallback)"
    ),
) -> None:
    """Deliver everything queued, in order, and wait for it (the sync barrier)."""
    _drain_foreground(run, every_dir=every_dir)


@outbox_app.command("watch")
def outbox_watch(
    interval: float = typer.Option(5.0, "--interval", min=0.1),
    once: bool = typer.Option(False, "--once", help="drain once and exit"),
) -> None:
    """Continuously drain the outbox in the foreground."""
    from ....sdk.delivery.outbox.drain.drain import drain
    from ..runs.watch_loop import watch

    journal = _journal()

    def one_pass() -> dict:
        report = drain(journal)
        # Adapt to the shared watch contract: {"counts": {...}, "failed": [...]}.
        return {
            "counts": {"completed": report.delivered, "failed": report.dead_lettered},
            "failed": report.errors if not report.clean else [],
            "remaining": report.remaining,
            "auth_blocked": report.auth_blocked,
        }

    watch(one_pass, interval=interval, once=once, report=_print_json)


@outbox_app.command("retry")
def outbox_retry(
    op_id: Optional[str] = typer.Argument(None, help="a dead-lettered op id (omit for all)"),
    run: Optional[str] = typer.Option(None, "--run", help="requeue only this run's dead letters"),
    every_dir: bool = typer.Option(
        False, "--all", help="every outbox on this machine (rank-* dirs, the $TMPDIR fallback)"
    ),
) -> None:
    """Requeue dead-lettered op(s) and kick the drainer."""
    from ....sdk.delivery import outbox as outbox_worker

    moved = 0
    for journal in _outbox_journals() if every_dir else [_journal()]:
        moved += journal.retry_failed(op_id, run_ref=run)
        # An explicit retry is a statement that the blocker (often credentials)
        # was dealt with -- forget the auth block so the drainer spawns again.
        journal.clear_auth_block()
        if every_dir:
            try:
                outbox_worker.maybe_spawn(str(journal.dir))
            except Exception:  # noqa: BLE001 -- best-effort; `drain --all` is the barrier
                pass
    _kick_drainer()
    print(f"requeued {moved} op(s)")
    if op_id is not None and moved == 0:
        raise typer.Exit(1)


@outbox_app.command("discard")
def outbox_discard(
    op_id: Optional[str] = typer.Argument(
        None, help="a dead-lettered op id (omit to discard ALL dead letters)"
    ),
    held: bool = typer.Option(
        False,
        "--held",
        help="instead: discard queued writes no credential here will send (a login whose "
        "account is unknown or another account's, or a refused login still stored)",
    ),
    credential: Optional[str] = typer.Option(
        None,
        "--credential",
        help="with --held: also discard the queued writes of this credential fingerprint "
        "(as `probe outbox drain` prints it), e.g. a PROBE_TOKEN job that is gone",
    ),
) -> None:
    """Tombstone dead letters into discarded/ (covers quarantined-corrupt
    files retry can never requeue). Their staged bytes are freed.

    `--held` tombstones QUEUED writes instead: those no credential on this
    machine will send as things stand (`probe outbox drain` says why). Another
    job's `PROBE_TOKEN` writes are left for that job, unless `--credential`
    names that credential's fingerprint. First, a dead credential of your own
    account hands its writes to your login, as the automatic rescue does: those
    are sent, not discarded."""
    from .... import analytics as telemetry
    from ....sdk.delivery import outbox as outbox_worker

    if credential is not None and not held:
        raise typer.BadParameter("--credential goes with --held")
    interactive = sys.stdin.isatty()
    if held:
        if op_id is not None:
            raise typer.BadParameter("--held discards every held write; it takes no op id")
        journal = _journal()
        kept = outbox_worker.adopt_before_discard(journal)
        counts = journal.discard_held_counts(credential=credential)
        telemetry.emit_outbox_discarded(
            counts,
            reason=telemetry.DiscardReason.CREDENTIAL if credential else telemetry.DiscardReason.HELD,
            interactive=interactive,
        )
        print(f"discarded {counts.writes} held write(s)")
        if kept:
            print(
                f"kept {kept} write(s) your login sends: their credential is dead and was your "
                "own account's"
            )
            _kick_drainer()
        return
    counts = _journal().discard_failed_counts(op_id)
    telemetry.emit_outbox_discarded(counts, reason=telemetry.DiscardReason.DEAD_LETTERS, interactive=interactive)
    print(f"discarded {counts.writes} op(s)")
    if op_id is not None and counts.writes == 0:
        raise typer.Exit(1)


@outbox_app.command("pause")
def outbox_pause(
    hours: Optional[float] = typer.Option(
        None, "--hours", help="how long to hold uploads (24 by default); they start again by themselves after"
    ),
    until_resume: bool = typer.Option(
        False, "--until-resume", help="hold uploads until `probe outbox resume`, however long that is"
    ),
) -> None:
    """Suspend background delivery from this machine (the outbox's own switch,
    not the capture killswitch) for --hours, 24 by default. Enqueues still work:
    every write made meanwhile, runs included, waits for the pause to end."""
    from ....sdk.delivery.journal.failures.pause import DEFAULT_PAUSE_HOURS, MAX_PAUSE_HOURS

    if hours is not None and not 0 < hours <= MAX_PAUSE_HOURS:
        raise typer.BadParameter(
            f"must be more than 0 and at most {MAX_PAUSE_HOURS:g}; --until-resume holds longer",
            param_hint="--hours",
        )
    if hours is not None and until_resume:
        raise typer.BadParameter("pass --hours or --until-resume, not both")
    marker = _journal().pause(None if until_resume else hours or DEFAULT_PAUSE_HOURS)
    if marker["until"]:
        print(f"outbox paused until {_utc_minute(marker['until'])} — `probe outbox resume` sends sooner")
    else:
        print("outbox paused until `probe outbox resume`")


@outbox_app.command("resume")
def outbox_resume() -> None:
    """Resume background delivery and kick the drainer."""
    from ....sdk.delivery import outbox as outbox_worker

    journal = _journal()
    journal.resume()
    journal.clear_auth_block()
    # A rescue that looked while it was paused put the next look off by hours.
    outbox_worker._rescue_stamp(journal).unlink(missing_ok=True)
    _kick_drainer()
    print("outbox resumed")


@app.command()
def flush() -> None:
    """Deliver everything queued and wait (alias of `probe outbox drain`)."""
    _drain_foreground()
from probe.cli.commands.json_print import _emit, _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.refs import _api, run_ref  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _journal, _kick_drainer, _outbox_journals  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.lifecycle.notices.outbox import _utc_minute  # noqa: E402 -- pieces need each other; the front door loads this one first
