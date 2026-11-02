"""The setup wizard's "Where should this computer's work go?" step.

Each computer files its new projects into ONE workspace: the one picked here,
saved as this context's pin (what `probe workspace use` writes). Every client on
the computer reads it -- the CLI, the Probe daemon and SDK runs -- and a team
with several workspaces and none set is refused (422 `workspace_required`)
rather than guessed for. The pin is this computer's; the person's HOME workspace
(`is_default`, one per member) is where the picker starts.

Unattended (`--yes`, explicit flags, no TTY -- an agent running the install),
it keeps a pin the computer already has, else pins the home, else pins the
team's newest workspace the member could make their home and says so (never
saved as their home). After `probe workspace use --clear` it pins nothing.

The step is fail-open in every direction: a wizard that cannot list workspaces
still finishes the install, says so, and leaves `probe workspace use` to pick
later.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from datetime import datetime, timezone

#: The picker's "make one" row; never a workspace id.
NEW_WORKSPACE = "__new_workspace__"

QUESTION = "Where should this computer's work go?"


def _created_at(row: dict) -> datetime:
    raw = row.get("created_at")
    try:
        when = raw if isinstance(raw, datetime) else datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)
    return when if when.tzinfo else when.replace(tzinfo=timezone.utc)


def _get_newest_eligible_row(rows: Sequence[dict]) -> dict | None:
    """The newest workspace the member could make their home (`home_eligible`), or None."""
    eligible = [r for r in rows if r.get("home_eligible") is True]
    return max(eligible, key=lambda r: (_created_at(r), str(r["id"])), default=None)


def _saved_pin() -> str | None:
    """This context's saved workspace id -- the FILE, never PROBE_WORKSPACE: the
    wizard sets the computer's choice, which an env var only overrides per shell."""
    from probe.sdk.settings.settings import load_context

    saved = load_context().get("workspace")
    ref = saved.get("id") if isinstance(saved, dict) else None
    if not ref:
        return None
    ref = str(ref)
    return ref[3:] if ref.startswith("id:") else ref


def preselect(rows: Sequence[dict], *, pinned: str | None) -> str | None:
    """The row the picker starts on: this computer's pin, else the member's home,
    else the newest workspace they could make their home, else None (the top row)."""
    from probe.sdk.client.resources.workspaces import get_home_row

    if pinned and pinned in {str(r["id"]) for r in rows}:
        return pinned
    start = get_home_row(rows) or _get_newest_eligible_row(rows)
    return None if start is None else str(start["id"])


def run_picker(rows: Sequence[dict], selected: str | None):
    """Ask. Returns a workspace id, NEW_WORKSPACE, tui.BACK, or None (Ctrl-C)."""
    import questionary

    from probe.cli.wizard import terminal as tui

    choices: list = [questionary.Separator(" ")]
    for row in sorted(rows, key=lambda r: (str(r.get("name") or "").lower(), str(r["id"]))):
        count = row.get("project_count") or 0
        detail = f"{count} project{'s' if count != 1 else ''}"
        choices.append(
            questionary.Choice(title=f"{row.get('name')}  ({detail})", value=str(row["id"]))
        )
    choices.append(questionary.Separator(" "))
    choices.append(questionary.Choice(title="Create a new workspace", value=NEW_WORKSPACE))
    message = tui.framed(
        "This computer's workspace.",
        tui.wrap(
            "Every project made on this computer -- from the CLI, your coding agents and "
            "training scripts -- goes into this workspace. `probe workspace use` changes it later."
        ),
        QUESTION,
    )
    return tui.ask(
        tui.select(
            message,
            choices=choices,
            default=selected,
            instruction="(arrow keys, enter to choose)",
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
        ),
        height=tui.content_height(message, choices),
    )


def _slug(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug[:48] or "workspace"


def _create(client, *, default_name: str) -> dict | None:
    """Ask for a name and create the workspace; a taken slug takes the
    server's suggestion. None when the person backs out."""
    from probe.cli.wizard import terminal as tui
    from probe.sdk import errors

    name = tui.text(
        "Create a new workspace.",
        tui.wrap("Everyone on your team can see and use it."),
        "Workspace name:",
    )
    if name is None or name is tui.BACK:
        return None
    name = str(name).strip() or default_name
    try:
        return client.create_workspace(_slug(name), name)
    except errors.ConflictError as exc:
        if exc.suggestion:
            return client.create_workspace(str(exc.suggestion), name)
        raise


def _pin(row: dict, *, pinned: str | None, reset_project: bool = False) -> None:
    from probe.sdk.settings.settings import WORKSPACE_CLEAR_RESET, save_context
    from probe.cli.commands.account import workspace_limit as workspace_limit_cmd

    refused = workspace_limit_cmd.refusal_for_pin_move(str(row["id"]), what="this computer's workspace")
    if refused:
        raise ValueError(refused)
    if row.get("writable") is False:
        raise ValueError("Choose a workspace you can write to.")
    if pinned == str(row["id"]) and not reset_project:
        return  # already this computer's: keep any active project with it
    save_context({
        "workspace": workspace_limit_cmd.keep_limit_keys({"id": str(row["id"]), "project": None}),
        **WORKSPACE_CLEAR_RESET,  # a pick replaces an earlier `probe workspace use --clear`
    })


def _env_note(chosen: dict) -> list[str]:
    """A line when PROBE_WORKSPACE overrides the choice in this shell."""
    import os

    env = (os.environ.get("PROBE_WORKSPACE") or "").strip()
    if not env:
        return []
    bare = env[3:] if env.startswith("id:") else env[5:] if env.startswith("slug:") else env
    if bare in (str(chosen["id"]), chosen.get("slug")):
        return []
    return [f"! PROBE_WORKSPACE={env} overrides it in this shell"]


def choose(*, asking: bool) -> list[str]:
    """Run the step. Returns the lines to show; never raises.

    `asking` is False for `--yes`, no TTY, or explicit flags: then nothing is
    shown -- a computer keeps its workspace, else takes the member's home, else
    the newest one they could make their home (with a line), else stays unset.
    """
    from probe.cli.wizard import terminal as tui
    from probe.sdk import errors
    from probe.sdk.client.client import Client
    from probe.sdk.client.resources.workspaces import get_home_row
    from probe.sdk.settings.settings import resolve
    from probe.foundation.request_identity.surface import Surface

    from probe.sdk.settings.settings import (
        WORKSPACE_CLEAR_RESET,
        is_workspace_cleared,
        load_context,
        save_context,
    )

    from probe.sdk.settings import workspace_limit as wl

    later = "`probe workspace use <slug>` sets it later"
    changes = "`probe workspace use <slug>` changes it"
    settings = resolve()
    if not settings.token:
        return []
    limit = wl.stored(load_context())
    lifted: list[str] = []
    try:
        with Client(settings=settings, async_writes=False, surface=Surface.CLI.value) as client:
            # The picker's list: every workspace, whatever this computer's limit says.
            with wl.without_limit():
                listed = client.list_workspaces()
            rows = [r for r in listed if r.get("id")]
            if limit is not None:
                if limit.id is not None and limit.id in {wl.as_uuid(r["id"]) for r in rows}:
                    # Limited to one workspace (`probe workspace limit`): that is where
                    # this computer's work goes, and the pin may not move off it.
                    return [f"✔ this computer is limited to {limit.label}, and its work goes there "
                            f"(`{wl.COMMAND}` changes it)"]
                # Deleted, or another team's (a re-login): every request would be
                # refused under it, so it goes with its pin, and the step goes on.
                save_context({"workspace": None, **WORKSPACE_CLEAR_RESET})
                settings.workspace_limit = None  # this client's own requests too
                from probe.cli.commands.account import workspace_limit as workspace_limit_cmd

                lifted = [f"! this computer's workspace limit named {limit.label}, which this team does "
                          "not have: it was lifted", *workspace_limit_cmd.resync_copies()]
            by_id = {str(r["id"]): r for r in rows}
            saved = _saved_pin()
            pinned = saved if saved in by_id else None
            if saved and pinned is None:
                # Deleted, or another team's (a re-login): every create would be
                # refused with it, so it goes, and an older clear with it (the pin
                # was the later choice); the choice below replaces it.
                save_context({"workspace": None, **WORKSPACE_CLEAR_RESET})
            if not rows:
                return lifted  # the team's first project creates its first workspace
            home = get_home_row(rows)
            # After `probe workspace use --clear`, only a person's own pick pins one.
            is_cleared = not pinned and is_workspace_cleared(load_context())
            # Where an unasked or cancelled step leaves it: the pin, else the home.
            kept = by_id[pinned] if pinned else None if is_cleared else home
            is_own_pick = is_newest = False
            if len(rows) == 1:
                chosen, is_own_pick = rows[0], True  # nothing to choose between
            elif not asking:
                chosen = kept
                if chosen is None and not is_cleared:
                    # D-c: no home yet, so the newest it could be: said, never saved as home.
                    chosen, is_newest = _get_newest_eligible_row(rows), True
                if chosen is None:
                    return [*lifted, "! this team has several workspaces and this computer has "
                            f"none set yet; {later} (see `probe workspace list`)"]
            else:
                answer = run_picker(rows, preselect(rows, pinned=pinned))
                if answer == NEW_WORKSPACE:
                    # The server makes it the home of a member who has none.
                    chosen = _create(client, default_name="My workspace") or kept
                elif answer is None or answer is tui.BACK:
                    chosen = kept  # Ctrl-C or Back is never consent to a guess
                else:
                    chosen, is_own_pick = by_id[str(answer)], True
                if chosen is None:
                    gone = "no workspace created" if answer == NEW_WORKSPACE else "this computer has no workspace set yet"
                    return [*lifted, f"! {gone}; {later}"]
            _pin(chosen, pinned=pinned)
            not_home: list[str] = []
            if is_own_pick and home is None and chosen.get("home_eligible") is True:
                # A member with no home makes their own choice it (R8).
                try:
                    client.save_home_workspace(str(chosen["id"]))
                except errors.RosError as exc:  # the pin stands either way
                    not_home = [f"! could not also make it your home workspace ({type(exc).__name__}); "
                                "pick your home in the dashboard"]
            name = chosen.get("name")
            line = (f"! you have no home workspace yet, so this computer's work goes into the "
                    f"team's newest, {name}; {changes}") if is_newest else (
                    f"✔ this computer's work goes into {name} ({changes})")
            return [*lifted, line, *not_home, *_env_note(chosen)]
    except Exception as exc:  # noqa: BLE001 - setup must finish without it
        return [f"! could not set this computer's workspace ({type(exc).__name__}); {later}"]
