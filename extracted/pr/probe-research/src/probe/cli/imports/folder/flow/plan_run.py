"""the whole import: the scoped folder lane, then the past-sessions lane, and the report the caller pages."""

from __future__ import annotations
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from ... import folder as bf

if TYPE_CHECKING:
    from probe.analytics import TelemetryContext
from ..classify import plan as plan_mod


@dataclass
class Report:
    """What the caller pages at the end."""

    lines: list[str] = field(default_factory=list)
    projects: list[str] = field(default_factory=list)
    units_done: int = 0
    units_total: int = 0
    enqueued: int = 0

    def add(self, *lines: str) -> None:
        self.lines.extend(lines)


def execute(
    *,
    client_factory,
    folder: Path,
    agent: bf.Agent,
    project: str | None = None,
    interactive: bool = True,
    yes: bool = False,
    concurrency: int | None = None,
    telemetry: TelemetryContext | None = None,
    transcripts: bool = False,
    transcripts_budget: int | None = None,
    source_id: str | None = None,
    import_changed: bool = False,
    import_unverified: bool = False,
    retry_dead: bool = False,
    review_excluded: bool = False,
    background: bool = False,
    back_to_selection: bool = False,
    wandb_source: dict | None = None,
    offer_wandb: bool = True,
    include_hidden: tuple[str, ...] = (),
):
    """The whole import. Returns the lines the caller pages.

    Order is deliberate and each step is cheap-and-certain before the one after:
    census, evidence, classify, REVIEW, create projects, import, enqueue,
    reconcile. Nothing mutates anything server-side until the review has passed.

    LEAVING KILLS EVERY AGENT. `_execute` does the work; this wrapper only
    guarantees the cleanup, on every exit -- Ctrl-C, an exception, or a clean
    return. Belt and braces on purpose: the interrupt paths already call
    `stop_all`, and this is what catches the route nobody thought of. An agent
    that outlives the wizard is invisible, holds the folder, and keeps spending
    tokens with nothing left to report to.

    The OUTBOX is untouched. It is a background drainer with its own
    `probe outbox pause`, and files already queued are already the user's --
    abandoning those on the way out is the one thing leaving must not do.
    """
    from probe import analytics as telemetry_mod
    from ....wizard import terminal as tui

    tel = telemetry_mod.null_context() if telemetry is None else telemetry
    started_at = time.monotonic()
    # Shared with _execute's _summary: a run whose summary already went out
    # must not emit a SECOND one from the interrupt handler — Ctrl-C at the
    # post-success "watch them upload?" prompt is ordinary human use, and a
    # success + aborted pair would corrupt the funnel it reports on.
    summary_state = {"emitted": False}
    # THE CONVERSATIONS RUN HERE, not at the end of `_execute`, and that is not
    # tidiness: `_execute` returns early on nine paths -- an unreadable root, an
    # empty folder, an already-finished import, a refused project, an
    # untrustworthy plan -- and on every one of them a user who passed
    # --transcripts would have been told nothing about the sessions they
    # asked for. The two scopes are independent by design, so the folder half
    # failing must not cancel the machine half.
    lane_state: dict = {}
    try:
        lines = _execute(
            client_factory=client_factory, folder=folder, agent=agent,
            project=project, interactive=interactive, yes=yes,
            concurrency=concurrency, telemetry=tel, started_at=started_at,
            summary_state=summary_state, lane_state=lane_state,
            source_id=source_id, import_changed=import_changed, import_unverified=import_unverified,
            retry_dead=retry_dead, review_excluded=review_excluded,
            background=background,
            back_to_selection=back_to_selection,
            wandb_source=wandb_source, offer_wandb=offer_wandb,
            include_hidden=include_hidden,
        )
        if lines is tui.BACK or lines is None:
            return lines
        if transcripts:
            # Preserve StartedFolderImport's job metadata while appending the
            # independent session lane's report.
            lines.extend(["", *_run_transcript_lane(
                client_factory=client_factory,
                folder=folder,
                units=lane_state.get("units") or [],
                interactive=interactive,
                yes=yes,
                budget_bytes=transcripts_budget,
            )])
        return lines
    except KeyboardInterrupt:
        bf.stop_all()
        if not summary_state["emitted"]:
            tel.emit(
                telemetry_mod.EVENT_BACKFILL_SUMMARY,
                outcome=telemetry_mod.BackfillOutcome.ABORTED,
                duration_seconds=int(time.monotonic() - started_at),
            )
        if back_to_selection:
            raise
        from .....sdk.delivery.journal.failures.pause import DEFAULT_PAUSE_HOURS

        return ["Stopped. Nothing further was read or uploaded.",
                "Anything already queued keeps uploading — `probe outbox status` "
                "shows it. `probe outbox pause` holds every upload from this "
                f"machine, runs included, for {DEFAULT_PAUSE_HOURS:g} h."]
    except Exception:
        # Observe-and-re-raise, never swallow: a crash without a summary would
        # read as user abandonment in the funnel. No error text on the event —
        # exception strings can embed paths, and the property contract is
        # metadata-only.
        if not summary_state["emitted"]:
            tel.emit(
                telemetry_mod.EVENT_BACKFILL_SUMMARY,
                outcome=telemetry_mod.BackfillOutcome.ERROR,
                duration_seconds=int(time.monotonic() - started_at),
            )
        raise
    finally:
        bf.stop_all()


def _execute(**kwargs) -> list[str]:
    """Run the scoped folder importer; unit execution helpers remain in this module."""
    from .scoped import execute as execute_scoped

    return execute_scoped(**kwargs)


def _run_transcript_lane(
    *,
    client_factory,
    folder: Path,
    units: list[plan_mod.Unit],
    interactive: bool,
    yes: bool,
    budget_bytes: int | None,
) -> list[str]:
    """Import standalone sessions; file assignments establish no session link.

    No agent: the local summarizer this lane used to pick went with the
    server-side digest lane. The client STAYS. Uploads go through the capture
    credential's own Wire, but `run_lane` still asks the server about each
    session before importing it and pins the account a background import runs
    under, and both need the wizard's own client.
    """
    from ... import transcripts as transcripts_mod

    try:
        return transcripts_mod.run_lane(
            client=client_factory(),
            interactive=interactive,
            yes=yes,
            budget_bytes=budget_bytes,
        )
    except Exception as exc:  # the files already landed; never lose that report
        return [f"Could not import agent sessions: {exc}"]
