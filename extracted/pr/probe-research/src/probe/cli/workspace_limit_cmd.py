"""`probe workspace limit`: set, clear and show this computer's workspace limit.

One implementation for every surface that changes it: the CLI command, the Probe
service's `workspace_limit` action (`probe.core.actions`) and so the desktop app's
Settings row. What the limit is and how it travels: `probe.sdk.workspace_limit`.

    probe workspace limit <id|slug|name> [--team-items show|hide] [--yes] [--json]
    probe workspace limit --team [--json]
    probe workspace limit [--json]                      # the current value

The workspace is looked up in `GET /v1/workspaces` WITHOUT the limit header, so every
workspace can be picked whatever the current limit is. Setting a limit also sets the
filing pin (`workspace.id`) to it: new projects go where the computer can see them.
`--team` clears the limit and keeps the pin. `--json` prints ONE object:

    {"ok": true, "workspace_limit": {"id", "name", "slug", "team_items"} | null}
    {"ok": false, "code": "...", "message": "..."}       (exit non-zero)

After a change, the static copies of the MCP headers (Codex's config.toml, Kimi
Code's manifest) are re-rendered, as a token rotation re-renders them, and with team
items hidden the team-note block leaves CLAUDE.md / AGENTS.md (the next sync puts it
back once they show again).
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass, field

from probe._compat import StrEnum
from probe.sdk import workspace_limit as wl


class Code(StrEnum):
    """`--json`'s failure `code`."""

    USAGE = "usage"
    NOT_SIGNED_IN = "not_signed_in"
    WORKSPACE_NOT_FOUND = "workspace_not_found"
    WORKSPACE_AMBIGUOUS = "workspace_ambiguous"
    CONFIG_UNREADABLE = "config_unreadable"
    API_ERROR = "api_error"


class LimitRefused(Exception):
    """Nothing was changed: a usage error or a lookup that failed."""

    def __init__(self, code: Code, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message

    def as_json(self) -> dict:
        return {"ok": False, "code": str(self.code), "message": self.message}


@dataclass
class Outcome:
    """What `apply` did: the JSON object, and the lines a person reads."""

    limit: wl.WorkspaceLimit | None
    lines: list[str] = field(default_factory=list)
    changed: bool = False

    def as_json(self) -> dict:
        return {"ok": True, "workspace_limit": None if self.limit is None else self.limit.as_json()}


def effective(environ: Mapping[str, str] | None = None) -> wl.WorkspaceLimit | None:
    """The limit this computer's processes run under: the active context's, unless
    `PROBE_WORKSPACE_LIMIT` overrides it. Local only, no network."""
    from probe.sdk.config import load_context

    return wl.resolve_limit(load_context(), os.environ if environ is None else environ)


def stored_limit(context: str | None = None) -> wl.WorkspaceLimit | None:
    """The limit the active context's file stores (environment ignored): what the pin
    commands must not move out from under."""
    from probe.sdk.config import load_context

    return wl.stored(load_context(context))


def refusal_for_pin_move(target_id: str | None, *, what: str) -> str | None:
    """The refusal for a command that would move the filing pin (`probe workspace use`,
    `--clear`, `workspace create --use`, `project use`) while this computer is limited,
    or None when it may: no limit, or the pin stays on the limited workspace."""
    limit = stored_limit()
    if limit is None:
        return None
    if target_id is not None and limit.id is not None and wl.as_uuid(target_id) == limit.id:
        return None
    return (
        f"this computer is limited to workspace {limit.label}, so {what} cannot move its "
        f"workspace elsewhere. Change the limit with `{wl.COMMAND} <workspace>`, or "
        f"`{wl.TEAM_COMMAND}` to see the whole team first."
    )


def names_limited_workspace(ref: str, limit: wl.WorkspaceLimit) -> bool:
    """Does `ref` (as `probe workspace use` takes it: an id, `id:`, a slug, `slug:`)
    name the limited workspace, by what the config knows of it? Local: a limited
    computer's workspace list shows only that workspace anyway."""
    text = ref.strip()
    if limit.id is not None and wl.as_uuid(text) == limit.id:
        return True
    slug = text[5:] if text.startswith("slug:") else text
    return bool(limit.slug) and slug == limit.slug


def keep_limit_keys(new_anchor: dict | None) -> dict | None:
    """`new_anchor` (a pin about to be saved) with the stored limit carried over, when
    it still names the limited workspace. `probe workspace use W` and `probe project
    use` rebuild the whole object; this keeps them from dropping the limit."""
    from probe.sdk.config import load_context

    anchor = load_context().get("workspace")
    if not isinstance(new_anchor, dict) or not isinstance(anchor, dict) or anchor.get(wl.LIMIT_KEY) is not True:
        return new_anchor
    if wl.as_uuid(new_anchor.get("id")) != wl.as_uuid(anchor.get("id")):
        return new_anchor
    return {**new_anchor, **{key: anchor[key] for key in wl.LIMIT_KEYS if key in anchor}}


def _find(rows: list, ref: str) -> dict:
    """The workspace `ref` names: an id (bare or `id:`), else a slug (bare or
    `slug:`), else a display name (case-insensitive; one match only)."""
    text = ref.strip()
    if not text:
        raise LimitRefused(Code.USAGE, "pass a workspace id, slug or name")
    rows = [row for row in rows if isinstance(row, dict) and row.get("id")]
    ident = wl.as_uuid(text)
    if ident is not None:
        for row in rows:
            if wl.as_uuid(row["id"]) == ident:
                return row
    slug = text[5:] if text.startswith("slug:") else text
    for row in rows:
        if row.get("slug") == slug:
            return row
    named = [row for row in rows if str(row.get("name") or "").strip().lower() == text.lower()]
    if len(named) == 1:
        return named[0]
    if len(named) > 1:
        choices = ", ".join(f"{row.get('slug')} ({row['id']})" for row in named)
        raise LimitRefused(
            Code.WORKSPACE_AMBIGUOUS, f"{len(named)} workspaces are named {text!r}: {choices}. Pass its slug."
        )
    # Named from this (unlimited) list: under a limit `probe workspace list` shows
    # only the limited workspace, so pointing there would hide the choices.
    slugs = sorted(str(row.get("slug")) for row in rows if row.get("slug"))
    shown = ", ".join(slugs[:20]) + (f" and {len(slugs) - 20} more" if len(slugs) > 20 else "")
    raise LimitRefused(
        Code.WORKSPACE_NOT_FOUND,
        f"{text!r} is not a workspace on this team" + (f"; its workspaces: {shown}" if shown else ""),
    )


def list_workspaces(client) -> list:
    """Every workspace on the team, whatever this computer's limit: the picker's list."""
    with wl.without_limit():
        rows = client.list_workspaces()
    return rows if isinstance(rows, list) else []


def _save_anchor(anchor: dict | None) -> None:
    from probe.sdk.config import save_context

    save_context({"workspace": anchor or None})


def resync_copies() -> list[str]:
    """Re-render every static copy of the limit (Codex's config.toml, Kimi Code's
    manifest) from what the config stores NOW. EVERY path that changes or clears the
    stored limit calls it -- this command, `probe workspace delete`, the wizard's
    stale-limit recovery -- or those clients keep sending a limit that is gone (and
    answered 422). Idempotent: nothing to do is nothing written. Never raises."""
    try:
        from probe.cli import setup as wizard

        return list(wizard.sync_mcp_token())
    except Exception as exc:  # noqa: BLE001 - a static copy is repaired by the next run
        return [f"! could not update the MCP header copies in other agents' configs ({type(exc).__name__})"]


def _after_change(limit: wl.WorkspaceLimit | None) -> list[str]:
    """Re-render what holds a copy of the limit. Never raises: the change is saved."""
    lines = resync_copies()
    if limit is not None and limit.hides_team_items:
        try:
            from probe.cli import team_note_file

            removed = team_note_file.remove_blocks()
            if removed:
                lines.append(f"team note taken out of {', '.join(removed)} (team-wide items are hidden)")
        except Exception as exc:  # noqa: BLE001 - the next sync removes it
            lines.append(f"! could not take the team note out of the instruction files ({type(exc).__name__})")
    return lines


def _env_note(limit_now: wl.WorkspaceLimit | None) -> list[str]:
    raw = (os.environ.get(wl.LIMIT_ENV) or "").strip()
    if raw:
        return [f"! {wl.LIMIT_ENV}={raw} overrides this computer's setting in this shell"]
    if (os.environ.get(wl.TEAM_ITEMS_ENV) or "").strip() and limit_now is not None:
        return [f"! {wl.TEAM_ITEMS_ENV} overrides the team-items choice in this shell"]
    return []


def describe(limit: wl.WorkspaceLimit | None) -> list[str]:
    """What a person reads about a limit: what Probe sees and what it hides."""
    if limit is None:
        return ["not limited: Probe on this computer sees the whole team"]
    where = limit.label
    if limit.slug and limit.slug != where:
        where = f"{where} ({limit.slug})"
    team = "hidden" if limit.hides_team_items else "shown"
    return [
        f"limited to workspace {where}: the CLI, SDK runs, the Probe daemon and the Probe MCP on this "
        "computer read only its projects, experiments, runs, papers and notes; every other workspace is hidden",
        f"team-wide items (the team note, the All workspaces summary, GitHub docs) are {team}; "
        "the shared folder and datasets stay visible",
        f"new projects go into {limit.label}; `{wl.TEAM_COMMAND}` sees the whole team again",
    ]


def apply(
    ref: str | None,
    *,
    team: bool = False,
    team_items: str | None = None,
    client_factory=None,
) -> Outcome:
    """Show (nothing passed), set (`ref`), change team items only (`team_items`
    alone, while limited) or clear (`team`). Raises LimitRefused; saves nothing then."""
    from probe.sdk import errors
    from probe.sdk.config import ConfigUnreadable, load_context, load_file

    items = None
    if team_items is not None:
        items = str(team_items).strip().lower()
        if items not in (wl.TeamItems.SHOW.value, wl.TeamItems.HIDE.value):
            raise LimitRefused(Code.USAGE, f"--team-items must be show or hide, got {team_items!r}")
    if team and ref is not None:
        raise LimitRefused(Code.USAGE, "pass a workspace to limit to, or --team, not both")
    if team and items is not None:
        raise LimitRefused(Code.USAGE, "--team-items goes with a workspace; --team shows everything")
    try:
        load_file(strict=True)
    except ConfigUnreadable as exc:
        raise LimitRefused(Code.CONFIG_UNREADABLE, str(exc)) from None

    context = load_context()
    anchor = context.get("workspace") if isinstance(context.get("workspace"), dict) else {}
    current = wl.stored(context)

    if team:
        if current is None:
            # Nothing stored, but a copy may still carry an old limit (a crash
            # between the save and the re-render, an older CLI's delete): repair.
            now = effective()
            return Outcome(limit=now, lines=[*describe(now), *resync_copies(), *_env_note(now)])
        kept = {key: value for key, value in anchor.items() if key not in wl.LIMIT_KEYS}
        _save_anchor(kept)
        now = effective()
        pin = anchor.get("name") or anchor.get("slug") or anchor.get("id")
        lines = ["Probe on this computer sees the whole team again"]
        if pin:
            lines.append(f"new projects still go into {pin} (`probe workspace use <slug>` changes it)")
        return Outcome(limit=now, lines=[*lines, *_after_change(None), *_env_note(now)], changed=True)

    if ref is None and items is None:
        now = effective()
        return Outcome(limit=now, lines=[*describe(now), *_env_note(now)])

    if ref is None:
        # Team items alone: only while limited.
        if current is None:
            raise LimitRefused(
                Code.USAGE,
                "this computer has no workspace limit: pass the workspace to limit to "
                f"(`{wl.COMMAND} <workspace> --team-items {items}`)",
            )
        if current.checked_team_items() == items:
            now = effective()
            return Outcome(limit=now, lines=[*describe(now), *_env_note(now)])
        _save_anchor({**anchor, wl.TEAM_ITEMS_KEY: items})
        now = effective()
        return Outcome(limit=now, lines=[*describe(now), *_after_change(now), *_env_note(now)], changed=True)

    from probe.sdk.config import resolve

    settings = resolve()
    if not settings.token:
        from probe.sdk import session_marker

        raise LimitRefused(Code.NOT_SIGNED_IN, f"not signed in: {session_marker.WIZARD_HINT}")
    if client_factory is None:
        import importlib

        # The CLI's own client (its surface, its outbox, what tests stand in for).
        client_factory = importlib.import_module("probe.cli.main")._client

    try:
        with client_factory() as client:
            row = _find(list_workspaces(client), ref)
    except errors.RosError as exc:
        raise LimitRefused(Code.API_ERROR, str(exc)) from None

    chosen = str(row["id"])
    same = wl.as_uuid(anchor.get("id")) == wl.as_uuid(chosen)
    keep_items = current.team_items if current is not None and current.id == wl.as_uuid(chosen) else None
    new_anchor = {**anchor} if same else {}
    new_anchor.update(
        {
            "id": chosen,
            # A project belongs to one workspace: kept only when the pin stays put.
            "project": anchor.get("project") if same else None,
            wl.LIMIT_KEY: True,
            wl.TEAM_ITEMS_KEY: items or keep_items or wl.TeamItems.SHOW.value,
            wl.NAME_KEY: row.get("name") or None,
            wl.SLUG_KEY: row.get("slug") or None,
        }
    )
    new_anchor = {key: value for key, value in new_anchor.items() if value is not None or key == "project"}
    unchanged = current is not None and new_anchor == anchor
    if not unchanged:
        _save_anchor(new_anchor)
    now = effective()
    lines = list(describe(now))
    if not same and anchor.get("project"):
        lines.append("active project cleared: it belongs to the workspace this computer used before")
    if not unchanged:
        lines.extend(_after_change(now))
    return Outcome(limit=now, lines=[*lines, *_env_note(now)], changed=not unchanged)


def confirm_text(ref: str, team_items: str | None) -> str:
    items = team_items or wl.TeamItems.SHOW.value
    return (
        f"Limit Probe on this computer to workspace {ref!r}? It will read only that workspace "
        f"(team-wide items {'hidden' if items == wl.TeamItems.HIDE.value else 'shown'}); "
        "nothing on the server changes"
    )
