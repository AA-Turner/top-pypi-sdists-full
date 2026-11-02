"""probe access-group ... and probe workspace writers ...: who may edit a workspace."""

from __future__ import annotations

import typer


# ---------------------------------------------------------------------------
# Who may EDIT a workspace (0214)
#
# THE INTERIM ADMIN SURFACE. The dashboard half ships in a later change, so
# until then these commands are the only way to restrict who may edit a
# workspace. Every mutation is owner/admin-only server-side.
#
# NOTHING HERE AFFECTS READS. A restricted workspace stays fully visible to
# every team member; only writes narrow. Say "restricted", never "private".
# ---------------------------------------------------------------------------
access_group_app = typer.Typer(
    no_args_is_help=True,
    help="access groups — named sets of people a workspace can grant edit access to",
)

writers_app = typer.Typer(
    no_args_is_help=True, help="who may edit a workspace (reads are never restricted)"
)


@access_group_app.command("list")
def access_group_list() -> None:
    """Every named group in the team, with its member user ids."""
    with _client() as c:
        _print_json(c.list_access_groups())


@access_group_app.command("create")
def access_group_create(
    name: str = typer.Argument(..., help='display name, e.g. "Lab"'),
) -> None:
    """Create a group. Owner/admin only."""
    with _client() as c:
        _print_json(c.create_access_group(name))


@access_group_app.command("rename")
def access_group_rename(
    group_id: str = typer.Argument(..., help="group id"),
    name: str = typer.Option(..., "--name", help="new display name"),
) -> None:
    """Rename a group. The id is what writer lists reference, so this moves nothing."""
    with _client() as c:
        _print_json(c.rename_access_group(group_id, name))


@access_group_app.command("delete")
def access_group_delete(
    group_id: str = typer.Argument(..., help="group id"),
) -> None:
    """Delete a group, dropping it from every writer list it guards.

    This can only NARROW access: a restricted workspace left with no writers is
    writable by nobody, never by everybody.
    """
    with _client() as c:
        c.delete_access_group(group_id)
    print("deleted")


@access_group_app.command("add")
def access_group_add(
    group_id: str = typer.Argument(..., help="group id"),
    user_id: str = typer.Argument(..., help="team member's user id"),
) -> None:
    """Add a member. Idempotent; a user may belong to several groups."""
    with _client() as c:
        c.add_access_group_member(group_id, user_id)
    print("added")


@access_group_app.command("remove")
def access_group_remove(
    group_id: str = typer.Argument(..., help="group id"),
    user_id: str = typer.Argument(..., help="team member's user id"),
) -> None:
    """Remove a member. Idempotent."""
    with _client() as c:
        c.remove_access_group_member(group_id, user_id)
    print("removed")


@writers_app.command("show")
def workspace_writers_show(
    workspace_id: str = typer.Argument(..., help="workspace slug (or id:<uuid>)"),
) -> None:
    """Who may edit this workspace. Readable by every member."""
    with _client() as c:
        _print_json(c.get_workspace_writers(_ref(c, "workspace", workspace_id).id))


@writers_app.command("set")
def workspace_writers_set(
    workspace_id: str = typer.Argument(..., help="workspace slug (or id:<uuid>)"),
    user: list[str] = typer.Option([], "--user", help="user id who may edit (repeatable)"),
    group: list[str] = typer.Option([], "--group", help="group id whose members may edit"),
    open_to_everyone: bool = typer.Option(
        False, "--open", help="remove the restriction: every team member may edit again"
    ),
) -> None:
    """Replace the WHOLE write state in one call. Owner/admin only.

    Whole-state rather than add/remove: "restrict this to the lab" as several
    requests can interleave with another admin's and commit a state neither
    asked for.

    `--open` restores the default. Restricting with NO subjects is legal and
    means NOBODY may edit -- which is the point of the explicit mode: removing
    the last writer must narrow access, never widen it.
    """
    mode = "open" if open_to_everyone else "restricted"
    with _client() as c:
        _print_json(
            c.set_workspace_writers(
                _ref(c, "workspace", workspace_id).id,
                mode=mode,
                users=list(user),
                groups=list(group),
            )
        )
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.refs import _ref  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
