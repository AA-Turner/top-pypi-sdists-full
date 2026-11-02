"""the folder import's choices: browse to the folder, pick the agent (installed and new enough), the mode, a connected W&B source."""

from __future__ import annotations

import os
from pathlib import Path


def subdirectories(root: Path) -> list[Path]:
    """The browsable children of `root`. ALL of them, and no counting.

    This used to return a census per child, and the picker showed it as a label.
    Two problems fell out of that, and deleting the counting deletes both:

    * Every child was walked RECURSIVELY before the screen could draw. On a
      network mount with a dataset directory that is the slowest moment in the
      whole flow, paid again on every keypress that changes directory.
    * Because that was expensive, the picker capped the list at 40 children and
      said nothing about the rest. A workspace with sixty researcher folders
      showed forty, with no scrollbar, no count and no hint -- so a folder you
      could not see read as a folder that was not there.

    The counts were justified as "knowing `checkpoints/` is 2.9 TB before
    pointing an importer at it". They do not earn their cost: this is a folder
    picker, the import runs one uncapped census afterwards where precision
    actually matters, and anything over the reference threshold uploads as a
    path rather than bytes anyway.

    `os.scandir`, not `iterdir()` + `is_dir()`: the latter costs one `lstat`
    per child on top of reading the directory. 44 us/child locally is nothing,
    but a thousand children on a slow mount is seconds of pure listing before
    a row is drawn.

    FOLLOWING links, on purpose. `is_dir()` follows by default and so did the
    `Path` version this replaces, so a symlinked directory has always been a
    browsable row here. `follow_symlinks=False` would be faster still and would
    silently drop those rows -- a speedup is not a licence to change what the
    picker shows.
    """
    try:
        with os.scandir(root) as it:
            entries = [
                Path(e.path)
                for e in it
                if not e.name.startswith(".") and e.name not in SKIP_DIRS and _entry_is_dir(e)
            ]
    except OSError:
        return []
    return sorted(entries)


def _entry_is_dir(entry) -> bool:
    """`entry.is_dir()`, with an unreadable entry treated as not-a-directory."""
    try:
        return entry.is_dir()
    except OSError:
        return False


# -- the folder picker ------------------------------------------------------


def choose_directory(start: Path):
    """Browse to the folder to import. Returns a Path, None (quit), or tui.BACK.

    THIS SCREEN DOES NOT WALK THE TREE. It reads one directory, one level deep,
    and draws. It used to census the folder you were standing in before it could
    render a single row -- a full recursive stat walk, capped at 20,000 files,
    paid again on every `cd`, and `../` paid it on a bigger tree. On a research
    drive that is minutes of blank terminal to produce a label reading
    "20,000+ files", which is barely a signal and cost the whole screen.

    What that label was for -- not pointing an importer at 2.9 TB unawares --
    is answered better and later: the import's own walk reports a live count as
    it runs, and it runs before anything is written or any agent starts, so
    Ctrl-C there costs walk time and nothing else.
    """
    from ....wizard.terminal.directory_picker import DirectoryPicker

    return DirectoryPicker(start, subdirectories).run()


# -- the wizard action ------------------------------------------------------


def choose_agent(available: list[Agent], *, selected: Agent | None = None):
    """Pick the agent. Returns an Agent, None (quit), or tui.BACK.

    Only ever reached with a real choice to make -- `resolve_agent` answers it
    without asking when one agent is installed, which is the common case.
    """
    import questionary

    from probe.cli.wizard import terminal as tui

    choices: list = [questionary.Separator(" ")]
    for index, agent in enumerate(available):
        if index:
            choices.append(questionary.Separator(" "))
        choices.append(questionary.Choice(title=AGENT_COPY[agent][0], value=agent))

    message = tui.framed(
        # Count-aware because a third agent can be installed; the importer
        # only ever reaches this with two, so its screen is unchanged.
        "Both agents are installed here."
        if len(available) == 2
        else f"{len(available)} coding agents are installed here.",
        tui.wrap("Choose the coding agent that will read this folder and import its contents."),
        "Which agent should read it?",
    )
    return tui.ask(
        tui.select(
            message,
            choices=choices,
            instruction="(arrow keys, enter to choose, esc goes back)",
            **({"default": selected} if selected in available else {}),
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
        ),
        height=tui.content_height(message, choices),
    )


def resolve_agent(
    requested: Agent | None, *, interactive: bool, chooser=None
) -> tuple[object, str | None]:
    """Which agent runs, as ``(choice, error)``.

    A TUPLE rather than a union return, because `Agent` is a `StrEnum` and
    therefore IS a str: an `isinstance(result, str)` check meant to catch the
    error case swallows every successful one too, and `run` then returns the
    enum where the caller expected output lines. Separate slots cannot be
    confused that way.

    `choice` is an Agent, None (quit), or tui.BACK. An explicit `--agent` wins
    and is NOT silently downgraded when that agent is missing: someone who named
    one wants that one, and quietly running the other over their filesystem is
    the wrong kind of helpful.
    """
    from probe.cli.wizard import terminal as tui

    if requested is not None:
        if requested not in IMPORTER_AGENTS:
            # `--agent pi` reaches here because the enum parses it. Running it
            # would be the module's own failure mode: pi's allowlist has no
            # shell, so every `probe artifact add` the import depends on has
            # nowhere to run and the folder reads back as imported and empty.
            return None, (
                f"`{requested.value}` cannot run a folder import — its tool allowlist has no "
                f"shell, and the import files what it finds through the probe CLI. Use "
                f"{' or '.join(a.value for a in IMPORTER_AGENTS)}."
            )
        binary = which_agent(requested)
        if binary is None:
            name = AGENT_COPY[requested][0]
            return None, (
                f"`{requested.value}` is not on PATH — install {name}, or drop --agent to pick."
            )
        # BEFORE THE WALK. On PATH is not the same as able to run this, and
        # finding out afterwards costs the whole traversal -- then repeats the
        # same message once per slice. See `too_old`.
        stale = too_old(requested, binary)
        if stale:
            return None, stale
        return requested, None

    available = available_agents()
    if not available:
        return None, (
            "No coding agent found. Backfill needs Claude Code or Codex on PATH — "
            "the agent is what reads the folder."
        )
    # An agent too old to run the import is not a choice worth offering. If
    # that leaves nothing, say WHY rather than "no coding agent found" -- the
    # binary is right there on PATH and a reader who is told it is absent will
    # go and install what they already have.
    usable = [a for a in available if too_old(a, which_agent(a) or "") is None]
    if not usable:
        reasons = [too_old(a, which_agent(a) or "") for a in available]
        return None, " ".join(r for r in reasons if r)
    if len(usable) == 1 or not interactive:
        return usable[0], None
    tui.clear()
    return (chooser or choose_agent)(usable), None


def choose_import_mode(folder: Path, agent: Agent, *, wandb_source=None):
    """Offer automatic planning only as an explicit alternative to review."""
    from ....wizard import terminal as tui

    if wandb_source is not None:
        return tui.review(
            "Import files and W&B history",
            [
                f"Folder: {folder}",
                f"W&B project: {wandb_source['external_id']}",
                "Automatic import runs in the background without file review.",
                "Choose one Probe project for both files and W&B history next.",
            ],
            [
                ("Review the plan first", FolderImportMode.REVIEW_FIRST),
                ("Scan and import in background", FolderImportMode.AUTOMATIC),
                ("Skip folder", tui.SKIP),
            ],
        )

    return tui.review(
        "Import this folder",
        [
            f"Folder: {folder}",
            f"{AGENT_COPY[agent][0]} will scan the files and propose an import plan.",
            "Review it first, or let Probe apply the resulting plan and upload",
            "the files automatically in the background.",
        ],
        [
            ("Review the plan first", FolderImportMode.REVIEW_FIRST),
            ("Scan and import in background", FolderImportMode.AUTOMATIC),
            ("Skip folder", tui.SKIP),
        ],
    )


def choose_folder_wandb(client_factory, *, default=None):
    """Offer a connected W&B source before scanning; no destination is approved."""
    from ..sources import wandb as backfill_wandb
    from ....wizard import terminal as tui

    while True:
        try:
            with client_factory() as client:
                with tui.working("Checking W&B connection"):
                    accounts = backfill_wandb.eligible_connections(client)
                if not accounts:
                    return None, False
                return backfill_wandb.choose_source(
                    client, accounts=accounts, default=default
                ), True
        except Exception as exc:
            action = tui.review(
                "W&B connection unavailable",
                [
                    f"Could not check connected W&B accounts ({type(exc).__name__}).",
                    "Retry the W&B check or continue with files.",
                ],
                [("Retry", "retry"), ("Continue with files", "files"), ("Back", tui.BACK)],
                default="files",
            )
            if action is None:
                raise KeyboardInterrupt
            if action == "retry":
                continue
            return (tui.BACK if action is tui.BACK else None), True
from probe.cli.imports.folder.agents.agents import AGENT_COPY, Agent, IMPORTER_AGENTS, available_agents, which_agent  # noqa: E402 -- an import cycle: bound once this module's names exist
from probe.cli.imports.folder.agents.flags import too_old  # noqa: E402 -- an import cycle: bound once this module's names exist
from probe.cli.imports.folder.folder import FolderImportMode  # noqa: E402 -- an import cycle: bound once this module's names exist
from probe.cli.imports.folder.walk.skip_rules import SKIP_DIRS  # noqa: E402 -- an import cycle: bound once this module's names exist
