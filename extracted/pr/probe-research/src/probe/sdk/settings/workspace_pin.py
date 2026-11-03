"""This computer's filing pin (`workspace.id` in the context file) under a workspace limit: what
`probe workspace use`, `probe project use` and a run's project prompt may move. Moved here from
`probe.cli.commands.account.workspace_limit` so the SDK can save a default project too."""

from __future__ import annotations

from probe.sdk.settings import workspace_limit as wl


def stored_limit(context: str | None = None) -> wl.WorkspaceLimit | None:
    """The limit the active context's file stores (environment ignored): what the pin
    commands must not move out from under."""
    from probe.sdk.settings.settings import load_context

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


def keep_limit_keys(new_anchor: dict | None) -> dict | None:
    """`new_anchor` (a pin about to be saved) with the stored limit carried over, when
    it still names the limited workspace. `probe workspace use W` and `probe project
    use` rebuild the whole object; this keeps them from dropping the limit."""
    from probe.sdk.settings.settings import load_context

    anchor = load_context().get("workspace")
    if not isinstance(new_anchor, dict) or not isinstance(anchor, dict) or anchor.get(wl.LIMIT_KEY) is not True:
        return new_anchor
    if wl.as_uuid(new_anchor.get("id")) != wl.as_uuid(anchor.get("id")):
        return new_anchor
    return {**new_anchor, **{key: anchor[key] for key in wl.LIMIT_KEYS if key in anchor}}
