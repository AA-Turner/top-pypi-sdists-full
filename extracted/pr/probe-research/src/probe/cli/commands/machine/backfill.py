"""probe backfill: point an agent at a folder of past work (the folder import's entry command)."""

from __future__ import annotations
from pathlib import Path
from typing import Optional

import typer
from ....sdk.settings.settings import resolve
from probe.cli.cli import app


@app.command()
def backfill(
    folder: str = typer.Argument(None, help="folder to import; omit to pick one interactively"),
    agent: str = typer.Option(
        None,
        "--agent",
        # pi is no longer named: it was here only because the transcripts lane
        # would take it to write summaries, and that lane is gone. The folder
        # importer refuses it -- `resolve_agent` explains why (no shell, so
        # `probe artifact add` has nowhere to run) -- so no lane accepts it now.
        help="claude | codex — omit to use whichever is installed, or be asked",
    ),
    project: str = typer.Option(
        None,
        "--project",
        help="import into this existing project; omit to review proposed projects",
    ),
    source_id: str = typer.Option(
        None,
        "--source-id",
        help="resume a saved source after moving its folder, within the same destination scope",
    ),
    import_changed: bool = typer.Option(
        False,
        "--import-changed",
        help="review changed content for import; may create new artifact identities",
    ),
    import_unverified: bool = typer.Option(
        False,
        "--import-unverified",
        help="review unresolved legacy paths for import after reading the reconciliation report",
    ),
    retry_dead: bool = typer.Option(
        False, "--retry-dead", help="plan files again that failed every attempt on an earlier run"
    ),
    review_excluded: bool = typer.Option(
        False, "--review-excluded",
        help="classify files an earlier plan left out as not research again",
    ),
    transcripts: bool = typer.Option(
        None,
        "--transcripts/--no-transcripts",
        help="also import this machine's agent sessions (interactive: asked at a gate)",
    ),
    transcripts_only: bool = typer.Option(
        False,
        "--transcripts-only",
        help="import ONLY this machine's agent sessions; read no folder",
    ),
    transcripts_budget_mb: int = typer.Option(
        None, "--transcripts-budget-mb", help="stop after roughly this many MB of sessions"
    ),
    include_hidden: Optional[list[str]] = typer.Option(  # noqa: UP007 - typer needs Optional
        None,
        "--include-hidden",
        help="also import this hidden folder (e.g. .claude), wherever it sits; repeatable. "
        "Hidden folders are skipped except .hydra, .dvc, .aim and .neptune",
    ),
) -> None:
    """Import work you have already done: point an agent at a folder.

    It uploads what it finds, describes each artifact, and reports how much of
    the folder it accounted for. Large files (checkpoints, datasets) are
    recorded as references, not copied.

    This is the command the dashboard hands you: `npx probe-research backfill`
    forwards straight here. The same thing is in `probe wizard` under
    `Import research work`.
    """
    from pathlib import Path

    from probe.cli.imports import folder as backfill_impl
    from probe.cli import wizard as wizard
    from probe.cli.wizard import terminal as tui

    # BEFORE anything else, and for a stronger reason than the wizard has:
    # `npx probe-research backfill` reaches us through an EPHEMERAL `uv tool
    # run` / `pipx run`, and the agent we are about to launch does its work by
    # shelling out to `probe artifact add`. With no persistent binary on PATH
    # every one of those calls fails, so the agent reads the whole folder and
    # lands nothing.
    from probe.cli.install.bootstrap import ensure_persistent_install

    try:
        chosen = backfill_impl.Agent(agent) if agent else None
    except ValueError:
        raise typer.BadParameter(
            f"unknown agent {agent!r}; expected one of: "
            f"{', '.join(a.value for a in backfill_impl.Agent)}"
        ) from None
    try:
        # Typer hands a called-directly function its OptionInfo default.
        hidden = backfill_impl.hidden_includes(include_hidden if isinstance(include_hidden, list) else ())
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from None

    from probe import analytics as telemetry_mod

    # Pre-bootstrap, like the wizard's `wizard.invoked` (D7/R4): this is the
    # command the dashboard hands out via npx, and a bootstrap death must
    # still enter the funnel.
    tel = telemetry_mod.TelemetryContext.start(
        via=telemetry_mod.Via.COMMAND,
        interactive=wizard.interactive(),
        base_url=resolve(base_url=_conn.base_url).base_url,
    )
    tel.emit(
        telemetry_mod.EVENT_BACKFILL_INVOKED,
        interactive=wizard.interactive(),
    )

    boot = ensure_persistent_install()
    if boot.message:
        print(boot.message)

    # Typer fills these in only when it PARSES the argv. Called directly --
    # which the tests do, and which `--action backfill` effectively does -- the
    # declared defaults arrive as OptionInfo sentinels, so anything that
    # computes with them has to normalise first or multiply a sentinel by 1024.
    budget_mb = transcripts_budget_mb if isinstance(transcripts_budget_mb, int) else None
    budget = budget_mb * 1024 * 1024 if budget_mb else None
    only_transcripts = transcripts_only is True

    # THE DEFAULT DIFFERS BY MODE, deliberately. Interactively the lane offers
    # itself at its own gate, so an unset flag means "ask". Headlessly there is
    # no gate and no one to ask, and uploading a machine's conversation history
    # because a script ran is exactly the scope change this feature exists to
    # make deliberate -- so it stays OFF unless the flag says otherwise.
    want_transcripts = transcripts if isinstance(transcripts, bool) else wizard.interactive()

    if only_transcripts:
        from probe.cli.imports import transcripts as transcripts_mod

        # NO AGENT IS RESOLVED HERE ANY MORE. This lane used to pick a local
        # coding agent to write summaries with; the digest lane was retired
        # server-side, so the lane uploads and nothing else, and `--agent` is
        # the folder importer's alone.
        lines = transcripts_mod.run_lane(
            client=_backfill_client(),
            interactive=wizard.interactive(),
            budget_bytes=budget,
        )
    else:
        lines = backfill_impl.run(
            client_factory=_backfill_client,
            folder=Path(folder) if folder else None,
            project=project,
            interactive=wizard.interactive(),
            agent=chosen,
            telemetry=tel,
            transcripts=want_transcripts,
            transcripts_budget=budget,
            source_id=source_id if isinstance(source_id, str) else None,
            import_changed=import_changed is True,
            import_unverified=import_unverified is True,
            retry_dead=retry_dead is True,
            review_excluded=review_excluded is True,
            include_hidden=hidden,
        )
    if lines:
        tui.page(lines) if wizard.interactive() else print("\n".join(lines))
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _backfill_client, _conn  # noqa: E402 -- pieces need each other; the front door loads this one first
