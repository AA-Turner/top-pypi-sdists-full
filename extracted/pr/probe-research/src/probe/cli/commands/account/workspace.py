"""probe workspace list/get/rename/set/create/delete/use/limit."""

from __future__ import annotations
import sys

import typer

from .... import errors
from ....sdk.settings.settings import (
    WORKSPACE_CLEAR_RESET,
    WORKSPACE_CLEARED,
    WORKSPACE_HANDOVER,
    load_context,
    save_context)
from probe.cli.commands.metric_pick import _declare, _pick_args, pick_reason_opt


# -- workspaces -------------------------------------------------------------
workspace_app = typer.Typer(
    no_args_is_help=True, help="workspaces — folders for projects and files"
)


def _workspace_row(ws: dict, here: str | None = None, home: dict | None = None) -> dict:
    """Show the same filing-location fields for every workspace."""
    return {
        "id": ws.get("id"),
        "name": ws.get("name"),
        "slug": ws.get("slug"),
        "projects": ws.get("project_count", 0),
        # Where this computer's new projects go (`probe workspace use`).
        "this_computer": here is not None and str(ws.get("id")) == here,
        # Your home (per person, `get_home_row`): where a computer with none set files.
        "home": ws is home,
    }


@workspace_app.command("list")
def workspace_list(
    raw: bool = typer.Option(False, "--raw", help="full API objects instead of the summary"),
) -> None:
    """List every workspace alphabetically in server order."""
    with _client() as c:
        rows = c.list_workspaces()
        if raw:
            _print_json(rows)
            return
        try:
            here = _resolve_workspace(c, None)
        except errors.ValidationError:
            here = None  # a PROBE_WORKSPACE slug this team has no workspace for
    if not rows:
        print("no workspaces yet — a Default workspace is created on your first write")
        return
    from ....sdk.client.resources.workspaces import get_home_row

    home = get_home_row(rows)
    _print_json([_workspace_row(w, here, home) for w in rows])


@workspace_app.command("get")
def workspace_get(
    workspace_id: str = typer.Argument(..., help="workspace slug (or id:<uuid>)"),
) -> None:
    """Show one workspace."""
    with _client() as c:
        _print_json(c.get_workspace(_ref(c, "workspace", workspace_id).id))


@workspace_app.command("rename")
def workspace_rename(
    workspace_id: str = typer.Argument(..., help="workspace slug (or id:<uuid>)"),
    name: str = typer.Option(..., "--name", help="new display name"),
) -> None:
    """Rename a workspace. Name is the only editable field.

    The slug stays unchanged. Any team member may rename any workspace.
    """
    with _client() as c:
        _print_json(c.rename_workspace(_ref(c, "workspace", workspace_id).id, name))


@workspace_app.command("set")
def workspace_set(
    workspace_id: str = typer.Argument(..., help="workspace slug (or id:<uuid>)"),
    best: str = typer.Option(..., "--best", help='best experiment (slug or id:<uuid>); "" clears'),
    reason: str = pick_reason_opt(),
) -> None:
    """Set the workspace's best experiment. A person's pick can't be replaced."""
    clears = _pick_args(best, reason)
    with _client() as c:
        wid = _ref(c, "workspace", workspace_id).id
        if clears:
            _declare(lambda: c.clear_workspace_best(wid, reason=reason))
        else:
            experiment = _ref(c, "experiment", best).id
            _declare(lambda: c.pick_workspace_best(wid, experiment, reason=reason))


@workspace_app.command("create")
def workspace_create(
    slug: str = typer.Argument(..., help="handle for the new workspace, e.g. engineering"),
    name: str | None = typer.Option(None, "--name", help="display label (default: the slug)"),
    use: bool = typer.Option(False, "--use", help="also make it this context's active workspace"),
) -> None:
    """Create a workspace — "engineering", "wandb-imports".

    Anyone on the team can rename it, file into it, and delete it while it is empty.
    Use `--use` to select it for this context, or `--workspace` on a project create.
    New projects go into this computer's workspace (`probe workspace use`, or the
    setup wizard's choice); a team with several workspaces and none set files into
    your home workspace, and is refused when you have none.
    """
    if use:
        from . import workspace_limit as workspace_limit_cmd

        refused = workspace_limit_cmd.refusal_for_pin_move(None, what="`probe workspace create --use`")
        if refused:
            print(f"error: {refused}", file=sys.stderr)
            raise typer.Exit(1)
    with _client() as c:
        ws = c.create_workspace(slug, name)
    if use:
        save_context({"workspace": {"id": str(ws["id"]), "project": None}})
    _print_json(ws)
    if use:
        print(f"active workspace: {ws.get('name')} ({ws['id']}) — project cleared")


@workspace_app.command("delete")
def workspace_delete(
    workspace_id: str = typer.Argument(..., help="workspace slug (or id:<uuid>)"),
    yes: bool = typer.Option(False, "--yes", "-y", help="skip the confirmation prompt"),
) -> None:
    """Delete an empty workspace.

    The server refuses while it holds projects or files, or an integration targets
    it. Move work out first (`probe project move <project> --workspace <other>`).
    If no workspaces remain, the next write without a workspace creates a Default
    workspace. Deleting the selected workspace clears this context's local pin.
    """
    with _client() as c:
        ws = c.get_workspace(_ref(c, "workspace", workspace_id).id)
        if not yes:
            typer.confirm(f"delete workspace {ws.get('name')} ({ws.get('slug')})?", abort=True)
        c.delete_workspace(str(ws["id"]))
    # Read the saved pin directly: an environment override is still an explicit
    # destination, and must not make deleting another workspace clear this one.
    anchor = load_context().get("workspace")
    pinned_id = anchor.get("id") if isinstance(anchor, dict) else None
    if isinstance(pinned_id, str) and _bare_id(pinned_id) == str(ws["id"]):
        limited = isinstance(anchor, dict) and anchor.get("limit") is True
        # Lost, not cleared: a fresh computer's home rule applies again.
        save_context({"workspace": None, **WORKSPACE_CLEAR_RESET})
        if limited:
            # A limit naming a deleted workspace would refuse every request; the
            # copies other agents hold (Codex, Kimi Code) go with it.
            from . import workspace_limit as workspace_limit_cmd

            print("this computer's workspace limit named it, so Probe here sees the whole team again", file=sys.stderr)
            for line in workspace_limit_cmd.resync_copies():
                print(line, file=sys.stderr)
    print(f"deleted workspace {ws.get('name')} ({ws['id']})")


@workspace_app.command("use")
def workspace_use(
    workspace_id: str | None = typer.Argument(
        None, help="workspace slug to make active (or id:<uuid>)"
    ),
    clear: bool = typer.Option(
        False, "--clear", help="unset this computer's workspace"
    ),
) -> None:
    """Set this computer's workspace: where its new projects go. `--clear` unsets it.

    Clears the active project either way: a project belongs to exactly one workspace,
    so keeping the old one selected would leave the context pointing at a project that
    is not in the workspace you just switched to.

    Every client on this computer uses it: the CLI, the Probe daemon and SDK runs
    (`PROBE_WORKSPACE` or `workspace=` overrides it for one process or call). The
    setup wizard asks for it. It never changes your home workspace (per person,
    `"home"` in `probe workspace list`), where a computer with none set files.

    `--clear` removes it, and nothing re-pins your home here. Creates then carry
    no workspace: the server files into the team's only workspace, and refuses
    (`workspace_required`) when there are several.
    """
    if clear == (workspace_id is not None):
        raise typer.BadParameter("pass a workspace to switch to, or --clear, not both")
    from . import workspace_limit as workspace_limit_cmd

    if clear:
        refused = workspace_limit_cmd.refusal_for_pin_move(None, what="`probe workspace use --clear`")
        if refused:
            print(f"error: {refused}", file=sys.stderr)
            raise typer.Exit(1)
        # On purpose: nothing re-pins the home here (the legacy key becomes the new one).
        save_context({"workspace": None, WORKSPACE_CLEARED: True, WORKSPACE_HANDOVER: None})
        print("this computer's workspace cleared — new projects need a workspace on a team with several")
        return
    limit = workspace_limit_cmd.stored_limit()
    if limit is not None and not workspace_limit_cmd.names_limited_workspace(workspace_id, limit):
        # Before any lookup: under the limit the API lists only that workspace, so
        # resolving another would only fail with a vaguer "not found".
        print(f"error: {workspace_limit_cmd.refusal_for_pin_move(None, what='`probe workspace use`')}", file=sys.stderr)
        raise typer.Exit(1)
    with _client() as c:
        ws = c.get_workspace(_ref(c, "workspace", workspace_id).id)
    # While limited, the pin may only stay on the limited workspace (D-g): moving
    # it would file new work where this computer cannot see it.
    refused = workspace_limit_cmd.refusal_for_pin_move(str(ws["id"]), what="`probe workspace use`")
    if refused:
        print(f"error: {refused}", file=sys.stderr)
        raise typer.Exit(1)
    from ...wizard.account import computer_workspace

    computer_workspace._pin(ws, pinned=computer_workspace._saved_pin(), reset_project=True)
    print(f"active workspace: {ws.get('name')} ({ws['id']}) — project cleared")


@workspace_app.command("limit")
def workspace_limit(
    workspace_id: str | None = typer.Argument(
        None, help="the workspace to limit this computer to: its id, slug or name"
    ),
    team: bool = typer.Option(False, "--team", help="remove the limit: see the whole team again"),
    team_items: str | None = typer.Option(
        None,
        "--team-items",
        help="show|hide team-wide items under the limit: the team note, the All workspaces "
        "summary, GitHub docs (default show)",
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="skip the confirmation prompt"),
    json_output: bool = typer.Option(False, "--json", help="print one JSON object"),
) -> None:
    """Limit what Probe on this computer reads to ONE workspace. No arguments: show it.

    A limiter, not a lock: keys and permissions are unchanged and anyone on this
    computer can change it. Limited, the CLI, SDK runs, the Probe daemon and the
    Probe MCP read only that workspace's projects, experiments, runs, papers and
    notes; new projects go there (it also becomes `probe workspace use`'s
    workspace). The shared folder and datasets stay visible; `--team-items hide`
    also hides the team note, the All workspaces summary and GitHub docs.

    `--team` removes the limit and keeps this computer's workspace.
    `PROBE_WORKSPACE_LIMIT=<id|slug>` (or `team`) overrides it for one process.
    """
    from . import workspace_limit as cmd

    def fail(code: str, message: str, exit_code: int = 1) -> None:
        if json_output:
            _print_json({"ok": False, "code": code, "message": message})
        else:
            print(f"error: {message}", file=sys.stderr)
        raise typer.Exit(exit_code)

    if (
        workspace_id is not None
        and not yes
        and not json_output
        and sys.stdin.isatty()
        and not typer.confirm(cmd.confirm_text(workspace_id, team_items), default=True)
    ):
        print("aborted: nothing changed", file=sys.stderr)
        raise typer.Exit(1)
    try:
        outcome = cmd.apply(workspace_id, team=team, team_items=team_items, client_factory=_client)
    except cmd.LimitRefused as exc:
        fail(str(exc.code), exc.message, 2 if exc.code == cmd.Code.USAGE else 1)
        return
    if json_output:
        _print_json(outcome.as_json())
        return
    for line in outcome.lines:
        print(line)
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.refs import _bare_id, _ref, _resolve_workspace  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
