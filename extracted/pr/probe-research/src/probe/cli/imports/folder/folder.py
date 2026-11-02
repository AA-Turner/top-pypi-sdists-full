"""`probe wizard` -> Import existing work: point one agent at one folder.

The wizard cannot read a research folder. Forty files -- a report, a config,
three CSVs, a training script -- are an experiment to a person and an
undifferentiated pile to `find`, and the mapping from file to experiment is
exactly the judgment nobody wrote down at the time. So the wizard does the two
things a program is better at and hands the middle to an agent:

* ENUMERATE (here, deterministic): walk the folder, count files and bytes.
  That count is the DENOMINATOR, and it is trustworthy precisely because no
  model produced it. Silent 2% coverage that reads as "done" is the failure
  mode this whole module exists to make impossible.
* DECIDE (the agent): which project each file belongs to, what is not
  research, and one line on what each file that matters is -- all SELECTED
  through `probe-backfill-plan`, never written back. Code splits a large
  folder into slices and units, uploads every file and creates every project.
* RECONCILE (here, deterministic): what landed, against what was counted.

The agent is launched with a FIXED anchor. It may decide what a folder means;
it may not decide what the folder is called. A second run inventing a second
project slug is the one mistake in this flow nobody can undo, so the slug is
resolved by code before the agent starts and passed in as a given.

stdlib plus a lazy questionary/client import, like the rest of cli/ -- `probe
log` runs inside training loops and must not pay for any of this.
"""

from __future__ import annotations
from probe.foundation.compat.compat import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from probe.analytics import TelemetryContext


class FolderImportMode(StrEnum):
    REVIEW_FIRST = "review_first"
    AUTOMATIC = "automatic"


class StartedFolderImport(list[str]):
    """Report lines plus proof that a resumable folder job was registered."""

    def __init__(self, job: dict, lines):
        super().__init__(lines)
        self.job = job

    @classmethod
    def status_unavailable(cls, job: dict, error: Exception):
        return cls(
            job,
            [
                f"Folder import was saved, but its status is unavailable ({type(error).__name__}).",
                "Open Existing imports to view its progress or resume it.",
            ],
        )


def _unstarted_import(lines):
    """Keep an unregistered attempt visible until retried, skipped, or backed out."""
    from ...wizard import terminal as tui

    action = tui.review(
        "Folder import did not start",
        lines or ["No files were queued for import."],
        [("Retry", "retry"), ("Skip folder", tui.SKIP), ("Back", tui.BACK)],
    )
    if action is None:
        raise KeyboardInterrupt
    return action


def run(
    *,
    client_factory,
    start: Path | None = None,
    folder: Path | None = None,
    project: str | None = None,
    interactive: bool = True,
    agent: Agent | None = None,
    yes: bool = False,
    concurrency: int | None = None,
    telemetry: "TelemetryContext | None" = None,
    transcripts: bool = False,
    transcripts_budget: int | None = None,
    source_id: str | None = None,
    import_changed: bool = False,
    import_unverified: bool = False,
    retry_dead: bool = False,
    review_excluded: bool = False,
    background: bool = False,
    back_to_selection: bool = False,
    include_hidden: tuple[str, ...] = (),
):
    """The `Import existing work` action. Returns the lines the wizard pages,
    or None for a pure back-out -- the wizard loop's signal to skip the result
    page, the press-enter pause, and the per-agent state re-read.

    With ``back_to_selection``, Back revisits the previous visible form and
    returns ``tui.BACK`` from the first one; Skip still advances with None.
    Interactive background attempts that do not register a job ask for Retry,
    Skip, or Back here, before their caller can finish onboarding.

    Delegates to :func:`probe.cli.imports.folder.flow.plan_run.execute`, which is the two-pass
    flow: classify once over evidence, review, then import in resumable units.
    This function is the door -- the picker, the agent choice, and the shape the
    wizard expects back.

    `folder` skips the picker and `agent` skips the agent prompt, which is what
    makes this reachable from `--action backfill` on a box with no TTY. `yes`
    accepts the classification without review. Interactive background imports
    offer review first by default, with an explicit automatic-plan alternative.
    """
    from probe.cli import backfill_run
    from probe.cli.wizard import terminal as tui

    target = folder
    picker_start = start or Path.cwd()
    previous_agent = None
    mode_only = False
    retry_mode = None
    resolve_outcome = interactive and background and back_to_selection
    wandb_choices = {}
    wandb_shown = {}
    wandb_approvals = {}
    revisit_wandb = False
    while True:
        if target is None:
            if not interactive:
                return ["Backfill needs a folder. Re-run interactively, or pass --folder."]
            picked = choose_directory(picker_start)
            if picked is None:
                raise KeyboardInterrupt  # quit the installer, not just this import
            if picked is tui.BACK and back_to_selection:
                return tui.BACK
            if picked is tui.BACK or picked is tui.SKIP:
                return None  # backed out: nothing happened, nothing to pause on
            target = picked

        target = Path(target).resolve()
        if not target.is_dir():
            lines = [f"{target} is not a directory."]
            if not resolve_outcome:
                return lines
            action = _unstarted_import(lines)
            if action == "retry":
                continue
            if action is tui.SKIP:
                return None
            if folder is not None:
                return tui.BACK
            target = None
            mode_only = False
            retry_mode = None
            continue
        picker_start = target
        if interactive and not yes and (target not in wandb_choices or revisit_wandb):
            pending, shown = choose_folder_wandb(client_factory, default=wandb_choices.get(target))
            revisit_wandb = False
            if pending is tui.BACK:
                if folder is not None:
                    return tui.BACK if back_to_selection else None
                revisit_wandb = True
                target = None
                continue
            if wandb_choices.get(target) != pending:
                wandb_approvals.pop(target, None)
            wandb_choices[target] = pending
            wandb_shown[target] = shown
        if not mode_only:
            agent_screen_shown = False

            def pick_agent(available):
                nonlocal agent_screen_shown
                agent_screen_shown = True
                return (
                    choose_agent(available, selected=previous_agent)
                    if previous_agent is not None
                    else choose_agent(available)
                )

            chosen, agent_error = resolve_agent(
                agent,
                interactive=interactive,
                **({"chooser": pick_agent} if back_to_selection else {}),
            )
            if agent_error:
                if not resolve_outcome:
                    return [agent_error]
                action = _unstarted_import([agent_error])
                if action == "retry":
                    continue
                if action is tui.SKIP:
                    return None
                if wandb_shown.get(target):
                    revisit_wandb = True
                    continue
                if folder is not None:
                    return tui.BACK
                target = None
                continue
            if chosen is None and back_to_selection:
                raise KeyboardInterrupt
            if chosen is tui.BACK and back_to_selection:
                if wandb_shown.get(target):
                    revisit_wandb = True
                    continue
                if folder is None:
                    target = None
                    continue
                return tui.BACK
            if chosen is None or chosen is tui.BACK:
                return None
            previous_agent = chosen

        mode_only = False

        if interactive and background and not yes:
            mode = retry_mode or choose_import_mode(
                target,
                chosen,
                **({"wandb_source": wandb_choices[target]} if wandb_choices.get(target) else {}),
            )
            retry_mode = None
            if mode is None:
                raise KeyboardInterrupt
            if mode is tui.BACK and back_to_selection:
                wandb_approvals.pop(target, None)
                if agent_screen_shown:
                    continue
                if wandb_shown.get(target):
                    revisit_wandb = True
                    continue
                if folder is None:
                    target = None
                    continue
                return tui.BACK
            if mode is tui.BACK or mode is tui.SKIP:
                return None
            if mode == FolderImportMode.AUTOMATIC:
                from . import flow as backfill_import
                from .sources import wandb as backfill_wandb
                from ..jobs import ui as import_jobs_ui
                from .coverage.coverage import CoverageError
                from ..jobs.messages import enqueue_report

                try:
                    if wandb_choices.get(target) and target not in wandb_approvals:
                        with client_factory() as client:
                            approval = backfill_wandb.choose_automatic_destination(
                                client,
                                folder=target,
                                wandb_source=wandb_choices[target],
                                project=project,
                            )
                            if approval is tui.BACK:
                                mode_only = True
                                continue
                            if approval is None:
                                wandb_choices[target] = None
                            else:
                                wandb_approvals[target] = approval
                    job = backfill_import.enqueue_auto_import(
                        client_factory=client_factory,
                        folder=target,
                        agent=chosen,
                        auto_approve=True,
                        project=project,
                        concurrency=concurrency,
                        source_id=source_id,
                        import_changed=import_changed,
                        import_unverified=import_unverified,
                        retry_dead=retry_dead,
                        review_excluded=review_excluded,
                        **(
                            {"wandb_approval": wandb_approvals[target]}
                            if target in wandb_approvals
                            else {}
                        ),
                    )
                except CoverageError as exc:
                    lines = [f"Folder import could not start: {exc}"]
                except Exception as exc:
                    lines = [
                        f"Folder import could not start ({type(exc).__name__}).",
                        "Check Existing imports before trying again.",
                    ]
                else:
                    registered_job = job
                    try:
                        job = import_jobs_ui.show_started_import(job)
                        lines = StartedFolderImport(job, enqueue_report(job, "Folder import"))
                        if transcripts:
                            from .. import transcripts as backfill_transcripts

                            with client_factory() as client:
                                lines.extend(
                                    backfill_transcripts.run_lane(
                                        client=client,
                                        interactive=True,
                                        background=True,
                                        budget_bytes=transcripts_budget,
                                    )
                                )
                        return lines
                    except Exception as exc:
                        return StartedFolderImport.status_unavailable(registered_job, exc)
                if not resolve_outcome:
                    return lines
                action = _unstarted_import(lines)
                if action is tui.SKIP:
                    return None
                mode_only = True
                if action == "retry":
                    retry_mode = FolderImportMode.AUTOMATIC
                else:
                    wandb_approvals.pop(target, None)
                continue

        result = backfill_run.execute(
            client_factory=client_factory,
            folder=target,
            agent=chosen,
            project=project,
            interactive=interactive,
            yes=yes,
            concurrency=concurrency,
            telemetry=telemetry,
            transcripts=transcripts,
            transcripts_budget=transcripts_budget,
            source_id=source_id,
            import_changed=import_changed,
            import_unverified=import_unverified,
            retry_dead=retry_dead,
            review_excluded=review_excluded,
            background=background,
            include_hidden=include_hidden,
            **(
                {"wandb_source": wandb_choices[target], "offer_wandb": False}
                if target in wandb_choices
                else {}
            ),
            **({"back_to_selection": True} if back_to_selection else {}),
        )

        if result is tui.BACK and back_to_selection:
            if interactive and background and not yes:
                mode_only = True
                continue
            if agent_screen_shown:
                continue
            if folder is None and interactive:
                target = None
                continue
            return tui.BACK
        if resolve_outcome and result is not None and not isinstance(result, StartedFolderImport):
            action = _unstarted_import(result)
            if action is tui.SKIP:
                return None
            if action == "retry":
                mode_only = True
                retry_mode = FolderImportMode.REVIEW_FIRST
                continue
            if interactive and background and not yes:
                mode_only = True
                continue
            if agent_screen_shown:
                continue
            if folder is None:
                target = None
                continue
            return tui.BACK
        return result
from probe.cli.imports.folder.agents.agents import Agent  # noqa: E402 -- an import cycle: bound once this module's names exist
from probe.cli.imports.folder.flow.choices import (  # noqa: E402 -- an import cycle: bound once this module's names exist
    choose_agent,
    choose_directory,
    choose_folder_wandb,
    choose_import_mode,
    resolve_agent,
)
