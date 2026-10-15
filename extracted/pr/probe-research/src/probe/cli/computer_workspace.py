"""The setup wizard's "Where should this computer's work go?" step.

Each computer files its new projects into ONE workspace: the one picked here,
saved as this context's pin (what `probe workspace use` writes). Every client on
the computer reads it -- the CLI, the Probe daemon and SDK runs -- and a team
with several workspaces and none set is refused (422 `workspace_required`)
rather than guessed for. It is this computer's setting, never a person's.

Unattended (`--yes`, explicit flags, no TTY -- an agent running the install),
it never guesses between several: it keeps a pin the computer already has, or
takes the member's legacy saved workspace (`is_default`, 0354, the same one the
one-time handover would), and otherwise leaves it unset and says how to pick.

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


def _legacy(rows: Sequence[dict]) -> dict | None:
    """The member's legacy saved workspace (0354), when they may still write it."""
    return next(
        (r for r in rows if r.get("is_default") is True and r.get("writable") is not False),
        None,
    )


def _saved_pin() -> str | None:
    """This context's saved workspace id -- the FILE, never PROBE_WORKSPACE: the
    wizard sets the computer's choice, which an env var only overrides per shell."""
    from probe.sdk.config import load_context

    saved = load_context().get("workspace")
    ref = saved.get("id") if isinstance(saved, dict) else None
    if not ref:
        return None
    ref = str(ref)
    return ref[3:] if ref.startswith("id:") else ref


def preselect(rows: Sequence[dict], *, pinned: str | None, user_id: str | None) -> str | None:
    """The row the picker starts on: this computer's current pin, else the
    member's legacy saved workspace (`is_default`, 0354), else the newest
    workspace they created (their onboarding one), else the team's oldest."""
    ids = {str(r["id"]) for r in rows}
    if pinned and pinned in ids:
        return pinned
    legacy = _legacy(rows)
    if legacy is not None:
        return str(legacy["id"])
    if user_id:
        mine = [r for r in rows if r.get("created_by") == f"user:{user_id}"]
        if mine:
            return str(max(mine, key=_created_at)["id"])
    if not rows:
        return None
    return str(min(rows, key=lambda r: (_created_at(r), str(r["id"])))["id"])


def run_picker(rows: Sequence[dict], selected: str | None):
    """Ask. Returns a workspace id, NEW_WORKSPACE, tui.BACK, or None (Ctrl-C)."""
    import questionary

    from probe.cli import tui

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
    from probe.cli import tui
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


def _pin(row: dict, *, pinned: str | None) -> None:
    from probe.sdk.config import save_context

    if pinned == str(row["id"]):
        return  # already this computer's: keep any active project with it
    save_context({"workspace": {"id": str(row["id"]), "project": None}})


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
    shown and nothing is guessed -- a computer keeps its workspace, else takes
    the member's legacy saved one, else stays unset with a line saying how.
    """
    from probe.cli import tui
    from probe.sdk.client import Client
    from probe.sdk.config import resolve
    from probe.sdk.surface import Surface

    from probe.sdk.config import WORKSPACE_HANDOVER, load_context, save_context

    later = "`probe workspace use <slug>` sets it later"
    settings = resolve()
    if not settings.token:
        return []
    try:
        with Client(settings=settings, async_writes=False, surface=Surface.CLI.value) as client:
            rows = [r for r in client.list_workspaces() if r.get("id")]
            try:
                user_id = str(client.me().get("user_id") or "") or None
            except Exception:  # noqa: BLE001 - the preselection only
                user_id = None
            by_id = {str(r["id"]): r for r in rows}
            saved = _saved_pin()
            pinned = saved if saved in by_id else None
            if saved and pinned is None:
                # Deleted, or another team's (a re-login): every create would
                # be refused with it, so it goes; the choice below replaces it.
                save_context({"workspace": None})
            if not rows:
                return []  # the team's first project creates its first workspace
            start = preselect(rows, pinned=pinned, user_id=user_id)
            if len(rows) == 1:
                chosen = rows[0]
            elif not asking:
                # Never a guess between several: keep this computer's, else the
                # member's legacy saved one (never after an explicit `probe
                # workspace use --clear`), else leave it for a person to pick.
                legacy = None if load_context().get(WORKSPACE_HANDOVER) else _legacy(rows)
                chosen = by_id[pinned] if pinned else legacy
                if chosen is not None and not pinned:
                    save_context({WORKSPACE_HANDOVER: True})
                if chosen is None:
                    return [
                        "! this team has several workspaces and this computer has none "
                        f"set yet; {later} (see `probe workspace list`)"
                    ]
            else:
                answer = run_picker(rows, start)
                if answer is None or answer is tui.BACK:
                    if pinned in by_id:
                        return [f"✔ this computer's work goes into {by_id[pinned].get('name')}"]
                    return [f"! this computer has no workspace set yet; {later}"]
                if answer == NEW_WORKSPACE:
                    created = _create(client, default_name="My workspace")
                    if created is None:
                        return [f"! no workspace created; {later}"]
                    chosen = created
                else:
                    chosen = by_id[str(answer)]
            _pin(chosen, pinned=pinned)
            return [
                f"✔ this computer's work goes into {chosen.get('name')} "
                "(`probe workspace use <slug>` changes it)",
                *_env_note(chosen),
            ]
    except Exception as exc:  # noqa: BLE001 - setup must finish without it
        return [f"! could not set this computer's workspace ({type(exc).__name__}); {later}"]
