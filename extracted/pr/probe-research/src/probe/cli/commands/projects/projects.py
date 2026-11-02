"""probe project create/list/get/lineage/branches/contributors/use/set/tag/move/delete and the closed ProjectKind vocabulary."""

from __future__ import annotations
import sys
from enum import Enum
from typing import Any

import typer
# The option enums only, from `_generated.enums` rather than `probe.models`: that
# seam builds every wire model, ~0.5 s that every command paid at startup -- the
# wizard, the hooks and the status line included -- whether or not it sent one.
# `tests/test_cli_startup_imports.py` holds the CLI to this.
from ....generated.enums import (
    MetricGoal,
    MetricReduce)
from ....sdk.settings.settings import (
    load_context,
    save_context)
from ....shared.reads import reads
from probe.cli.commands.entity_text import (
    AuthoredBy,
    _authored_by_value,
    authored_by_opt,
    description_opt,
    entity_markdown_opt,
)
from probe.cli.commands.json_print import _FIELDS_OPTION, _emit, _print_json, _print_link, _select_fields
from probe.cli.commands.metric_pick import (
    _declare,
    _metric_args,
    _pick_args,
    best_opt,
    goal_opt,
    metric_opt,
    pick_reason_opt,
    reduce_opt,
)
from probe.cli.commands.refs import _api, _bare_id, _project_id, _ref, _resolve_workspace, slug_ref
from probe.cli.commands.tags import (
    _set_verb_tags,
    _tag_flags_given,
    _tag_verb_flow,
    add_tag_opt,
    remove_tag_opt,
    set_tags_opt,
)


# -- projects ---------------------------------------------------------------
project_app = typer.Typer(no_args_is_help=True, help="projects — the top of the data model")


class ProjectKind(str, Enum):
    """The closed kind vocabulary; the server refuses anything else.

    weights MOVE -> training · frozen weights (sweeps, evals) -> evaluation ·
    papers, design, theory -> research · everything else -> general.
    A SWEEP is an experiment: `experiment` is a STRUCTURAL kind for a leaf
    under one of the four, carrying the question it answers in --description.
    """

    training = "training"
    evaluation = "evaluation"
    research = "research"
    general = "general"
    experiment = "experiment"


#: Old spellings `--kind` still ACCEPTS but no longer offers (Track E, 2026-10-04:
#: `inference` became `evaluation`). Installed skills and agents' habits still
#: type the old word, and refusing it would fail a create the server itself
#: accepts (it bridges `inference` forever, logged `project_kind_bridged`). The
#: CLI translates here, so a current CLI never sends the old spelling and the
#: server's bridge count measures only old CLIs and SDK code passing the string
#: itself -- the callers a future refusal would actually break.
#:
#: Through click's `token_normalize_func` (the `context_settings` below), which
#: the Choice applies to the typed value before matching: the alias resolves to
#: its canonical member while help, the choice list in a usage error and
#: the assistant's synopsis (app/assistant/cli_tool.py reads
#: `param.type.choices`) all keep naming the canonical five only.
LEGACY_PROJECT_KIND_ALIASES = {"inference": ProjectKind.evaluation.value}

_PROJECT_KIND_CONTEXT = {
    "token_normalize_func": lambda token: LEGACY_PROJECT_KIND_ALIASES.get(token, token)
}


@project_app.command("create", context_settings=_PROJECT_KIND_CONTEXT)
def project_create(
    slug: str = typer.Argument(..., help="url-safe identifier, unique per tenant"),
    kind: ProjectKind = typer.Option(
        ...,
        "--kind",
        help=(
            "what the project is FOR; structures its page. weights move ->"
            " training; sweeps/evals -> evaluation; papers/design -> research;"
            " else general"
        ),
    ),
    name: str = typer.Option(
        None, "--name", help="display name; omit it and the row reads as its slug"
    ),
    part_of: list[str] = typer.Option(
        None,
        "--part-of",
        help="the bigger effort this project is a part of (slug or id:<uuid>; repeatable)",
    ),
    # 0401: the older spelling of --part-of, kept so scripts and installed
    # skills that still type it keep working. It sends the same `part_of`.
    parent: str = typer.Option(None, "--parent", hidden=True),
    description: str = description_opt(),
    summary: str = entity_markdown_opt(),
    tag: list[str] = typer.Option(None, "--tag", help="tag at creation (repeatable)"),
    workspace: str = typer.Option(
        None, "--workspace", help="workspace slug (or id:<uuid>); defaults to the active one"
    ),
    authored_by: AuthoredBy = authored_by_opt(),
) -> None:
    """Create a project.

    This is what the CLI was missing: creating a project used to require starting a run,
    which forced an experiment and an invented question into existence alongside it.

    --kind is REQUIRED (0149): the creator declares intent, before content
    exists. Projects are flat: a phase of a bigger effort is its own project
    linked --part-of it, and nothing moves or is inherited. With --part-of and
    no --workspace it is filed in the first target's workspace.
    """
    from . import filed_workspace

    targets = list(dict.fromkeys([*(part_of or []), *([parent] if parent else [])]))
    with _client() as c:
        created = c.create_project(
            slug,
            name,
            kind=kind.value,
            part_of=[_project_id(c, target) for target in targets] or None,
            # Only resolve the ambient default for an unlinked create: a linked
            # one with no explicit workspace is filed beside its first target,
            # server-side.
            workspace_id=(_resolve_workspace(c, workspace) if workspace or not targets else None),
            description=description,
            document=_text_value(summary),
            tags=tag or None,
            authored_by=_authored_by_value(authored_by),
        )
        # The JSON first: the name read is bounded, but never between a
        # successful create and the id a script waits for.
        _print_json(created)
        _print_link("project", created.get("id"))
        filed_workspace.say_filed(c, created)


@project_app.command("list")
def project_list(
    workspace: str = typer.Option(
        None, "--workspace", help="workspace slug (or id:<uuid>); defaults to the active one"
    ),
    all_workspaces: bool = typer.Option(
        False, "--all", help="every workspace you can see (ignores --workspace and context)"
    ),
    tag: list[str] = typer.Option(
        None, "--tag", help="filter: project must carry ALL (repeatable)"
    ),
    part_of: str = typer.Option(
        None,
        "--part-of",
        help="only the projects linked as a part of this one (slug or id:<uuid>)",
    ),
    # 0401: the older spelling of --part-of, kept for scripts that type it.
    parent: str = typer.Option(None, "--parent", hidden=True),
    limit: int = typer.Option(50, "--limit", min=1, max=200),
    cursor: str = typer.Option(None, "--cursor", help="keyset cursor from a previous page"),
    fields: str = _FIELDS_OPTION,
) -> None:
    """List projects in a workspace, or across all of them with --all.

    `--part-of P` answers "what are the parts of P?": the projects linked
    `--part-of` it, one hop, in any workspace. Ask again on a part for its own.
    """
    parameters: dict[str, Any] = {"limit": limit}
    if cursor:
        parameters["cursor"] = cursor
    # Omitting workspace_id IS "all workspaces" — the server has no all-sentinel, so
    # --all means "send no filter" rather than some magic value.
    whole = part_of or parent
    with _client() as c:
        # A part is asked for by what it is part of, and a link crosses
        # workspaces -- so --part-of carries its own scope, and the active
        # workspace beside it would hide the parts filed elsewhere.
        workspace_id = None if (all_workspaces or whole) else _resolve_workspace(c, workspace)
        page = c.list_projects(
            workspace_id=workspace_id,
            tags=tag or None,
            part_of=_project_id(c, whole) if whole else None,
            **parameters,
        )
    _print_json(_select_fields({"items": page.items, "next_cursor": page.next_cursor}, fields))


@project_app.command("get")
def project_get(
    project_id: str = slug_ref("project"),
    fields: str = _FIELDS_OPTION,
) -> None:
    """Show one project."""
    with _client() as c:
        _emit(reads.project_get(_api(c, pretty=sys.stdout.isatty()), project_id, fields))


@project_app.command("lineage")
def project_lineage(project_id: str = slug_ref("project")) -> None:
    """Print the project's OWN links: what it came from and what came from it.

    Its links in and out (stored, then "built on" derived from what its runs
    used, `derived: true`), its `origin` and its direct children. An experiment's own
    links are `experiment lineage`. Look here before linking it to anything.
    """
    with _client() as c:
        _print_json(c.project_lineage(_project_id(c, project_id)))


@project_app.command("branches")
def project_branches(project_id: str = slug_ref("project")) -> None:
    """Print the project's lines of work: best value, rank, effort, state."""
    with _client() as c:
        _print_json(c.project_branches(_project_id(c, project_id)))


@project_app.command("contributors")
def project_contributors(
    project_id: str = slug_ref("project"),
    add: str = typer.Option(None, "--add", help="credit this user id"),
    remove: str = typer.Option(None, "--remove", help="drop this user id's credit"),
    fields: str = _FIELDS_OPTION,
) -> None:
    """Who worked on this project.

    A project shows up in the workspace of everyone credited here. Credit is
    recorded automatically by writing under the project or its experiments,
    and is always the project's own. `--add` is for someone who has not
    written anything yet; `--remove` drops a credit and is not a ban.
    """
    if add and remove:
        typer.echo("--add and --remove are separate calls; pass one", err=True)
        raise typer.Exit(2)
    with _client() as c:
        pid = _project_id(c, project_id)
        if add:
            _print_json(c.add_project_contributor(pid, add))
            return
        if remove:
            c.remove_project_contributor(pid, remove)
            return
        _print_json(_select_fields({"items": c.list_project_contributors(pid)}, fields))


@project_app.command("use")
def project_use(
    project_id: str = typer.Argument(..., help="project slug to make active (or id:<uuid>)"),
) -> None:
    """Set the active project for this context, so `run start` and friends default to it."""
    with _client() as c:
        proj = c.get_project(_project_id(c, project_id))
        # The FILE pin this overwrites, not PROBE_WORKSPACE (which only overrides
        # a shell): that is what "this computer's workspace" means.
        saved = load_context().get("workspace")
        before = _bare_id(saved.get("id")) if isinstance(saved, dict) else None
        if before is None and not proj.get("workspace_id"):
            before = _resolve_workspace(c, None)
        # Pin the project under the workspace that actually owns it, not the ambient
        # one: selecting a project from another workspace should move the anchor, not
        # create a mismatched pair. workspace_id is nullable on legacy rows — fall
        # back to ambient.
        owner = proj.get("workspace_id") or before
        moved = owner is not None and str(owner) != str(before or "")
        from ..account import workspace_limit as workspace_limit_cmd

        # Selecting a project from another workspace would move the pin (and so
        # where new projects go) out of this computer's workspace limit (D-g).
        refused = workspace_limit_cmd.refusal_for_pin_move(
            str(owner) if owner else None, what=f"`probe project use {project_id}` (its workspace is another)"
        )
        if refused:
            print(f"error: {refused}", file=sys.stderr)
            raise typer.Exit(1)
        name = c.get_workspace(str(owner)).get("name") if moved else None
    # Stored in the explicit `id:` form: an id survives a rename where a slug does
    # not, but a BARE id would read as a slug when it flows back in as a default.
    save_context(
        {
            "workspace": workspace_limit_cmd.keep_limit_keys(
                {"id": str(owner) if owner else None, "project": f"id:{proj['id']}"}
            )
        }
    )
    print(f"active project: {proj.get('slug')} ({proj['id']})")
    if moved:
        # The pin is also where this computer's NEW projects go (CLI, daemon, SDK
        # runs), so moving it is said out loud rather than left implied.
        print(
            f"this computer's workspace is now {name or owner}: new projects go there "
            "(`probe workspace use <slug>` changes it)",
            file=sys.stderr,
        )


@project_app.command("set")
# `patch` was the original spelling and stays reachable so scripts do not break,
# but it is hidden: experiments, runs and groups all amend with `set`, and an
# agent that learned `experiment set` and guessed `project set` used to get
# `No such command`. One verb is discoverable; the other is a compatibility door.
@project_app.command("patch", hidden=True)
def project_set(
    project_id: str = slug_ref("project"),
    name: str = typer.Option(None, "--name"),
    description: str = description_opt(),
    summary: str = entity_markdown_opt(),
    workspace: str = typer.Option(None, "--workspace", help="not here — use `probe project move`"),
    add_tag: list[str] = add_tag_opt(),
    remove_tag: list[str] = remove_tag_opt(),
    set_tags: list[str] = set_tags_opt(),
    metric: str = metric_opt(),
    goal: MetricGoal = goal_opt(),
    reduce: MetricReduce = reduce_opt(),
    best: str = best_opt(),
    reason: str = pick_reason_opt(),
    authored_by: AuthoredBy = authored_by_opt(),
) -> None:
    """Update a project's display fields and tags, in one write.

    Or set its headline metric or best experiment, each alone. A person's
    metric or pick can't be replaced.
    """
    if workspace is not None:
        # Refused on purpose. Re-filing fans out a reindex across every descendant, so
        # it must be the thing you asked for, not a flag that rode along on an edit.
        print(
            "error: --workspace does not belong on `patch` — re-filing a project reindexes\n"
            "       all of its experiments and runs. Use `probe project move` to do that.",
            file=sys.stderr,
        )
        raise typer.Exit(1)
    fields = {"name": name, "description": description, "document": _text_value(summary)}
    retagging = _tag_flags_given(add_tag, remove_tag, set_tags)
    editing = retagging or any(value is not None for value in fields.values())
    if (goal is not None or reduce is not None) and metric is None:
        raise typer.BadParameter("--goal and --reduce need --metric")
    if reason is not None and best is None:
        raise typer.BadParameter("--reason needs --best")
    if sum((editing, metric is not None, best is not None)) > 1:
        raise typer.BadParameter("--metric, --best and field edits go in separate commands")
    if (metric is not None or best is not None) and authored_by is not None:
        raise typer.BadParameter("--authored-by does not apply to --metric or --best")
    if metric is not None:
        clears = _metric_args(metric, goal, reduce)
        with _client() as c:
            pid = _project_id(c, project_id)
            if clears:
                _declare(lambda: c.clear_project_metric(pid))
            else:
                _declare(
                    lambda: c.set_project_metric(
                        pid, metric, goal=goal.value, reduce=reduce.value if reduce else None
                    )
                )
        return
    if best is not None:
        clears = _pick_args(best, reason)
        with _client() as c:
            pid = _project_id(c, project_id)
            if clears:
                _declare(lambda: c.clear_project_best(pid, reason=reason))
            else:
                experiment = _ref(c, "experiment", best).id
                _declare(lambda: c.pick_project_best(pid, experiment, reason=reason))
        return
    if not editing:
        raise typer.BadParameter(
            "pass at least one of --name/--description/--summary/--add-tag/--remove-tag/--set-tags"
            "/--metric/--best"
        )
    with _client() as c:
        pid = _project_id(c, project_id)
        if retagging:
            current = c.get_project(pid)
            tags, changed = _set_verb_tags(current.get("tags"), add_tag, remove_tag, set_tags)
            if not changed and all(value is None for value in fields.values()):
                _print_json(current)  # the tags already read that way: nothing to write
                return
            fields["tags"] = tags
        _print_json(
            c.update_project(pid, **fields, authored_by=_authored_by_value(authored_by))
        )


@project_app.command("tag")
def project_tag(
    project: str = typer.Argument(..., help="project slug (or id:<uuid>)"),
    add: list[str] = typer.Argument(None, help="tags to add"),
    remove: list[str] = typer.Option(
        None,
        "--remove",
        help="tag to remove; repeatable, ONE tag per flag (a bare word after options is an ADD)",
    ),
    replace: list[str] = typer.Option(
        None, "--set", help="replace the whole list (repeatable; --set '' clears all)"
    ),
) -> None:
    """Tag a project: positional args add, --remove drops, --set replaces; bare lists."""
    with _client() as c:
        pid = _project_id(c, project)
        _print_json(
            _tag_verb_flow(
                pid,
                c.get_project(pid).get("tags"),
                add,
                remove,
                replace,
                lambda wanted: c.update_project(pid, tags=wanted),
            )
        )


@project_app.command("move", context_settings=_PROJECT_KIND_CONTEXT)
def project_move(
    project_id: str = slug_ref("project"),
    # 0401: the older tree moves, kept so scripts that type them keep working.
    # They send what they always sent (PATCH parent_project_id, a uuid or
    # null); the server moves (or drops) the one `part_of` link that stands
    # for the old filing, and the project's other links stay.
    parent: str = typer.Option(None, "--parent", hidden=True),
    top_level: bool = typer.Option(False, "--top-level", hidden=True),
    workspace: str = typer.Option(
        None, "--workspace", help="destination workspace slug (or id:<uuid>)"
    ),
    kind: ProjectKind = typer.Option(
        None, "--kind", help="also re-declare what the project is for"
    ),
) -> None:
    """Move a project to another workspace.

    Projects are flat, so a project is never moved under another one: link it
    instead (`probe project reference add P --to BIG --part-of`). The move
    reindexes the project's live documents in the same transaction; projects
    linked to it stay where they are. ONE `move` command because Typer keeps
    only the LAST registration of a name: two `move` commands shipped once,
    and the first was silently unreachable.
    """
    destinations = [parent is not None, top_level, workspace is not None]
    if sum(destinations) != 1:
        raise typer.BadParameter(
            "pass --workspace; to say a project is part of another, "
            "`probe project reference add P --to BIG --part-of`"
        )
    with _client() as c:
        if workspace is not None:
            moved = c.move_project(_project_id(c, project_id), _ref(c, "workspace", workspace).id)
            if kind is not None:
                moved = c.update_project(_project_id(c, project_id), kind=kind.value)
            _print_json(moved)
            return
        kwargs: dict[str, Any] = {}
        if kind is not None:
            kwargs["kind"] = kind.value
        if top_level:
            kwargs["parent_project_id"] = None  # explicit null = detach
        else:
            kwargs["parent_project_id"] = _project_id(c, parent)
        _print_json(c.update_project(_project_id(c, project_id), **kwargs))


@project_app.command("delete")
def project_delete(
    project_id: str = slug_ref("project"),
    yes: bool = typer.Option(False, "--yes", help="skip the confirmation prompt"),
    # Kept for older scripts (0148's subtree delete), and changes nothing:
    # projects are flat, so no project is filed under another (the server
    # emptied and dropped the filing) and a `part_of` link never takes a
    # project with it. Still sent, and the server ignores it; the prompt says
    # the linked projects stay.
    recursive: bool = typer.Option(
        False,
        "--recursive",
        hidden=True,
        help=(
            "kept for older scripts; accepted and changes nothing: the projects "
            "linked to it (part_of or references) stay"
        ),
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="change nothing: print what the delete would take, whose it is and when it last changed",
    ),
) -> None:
    """Move a project and everything in it to the trash (Probe support can
    restore it for 21 days, then it is deleted for good). A server without the
    trash deletes it permanently, and the prompt says so.

    Deleting a project never deletes the projects linked to it (`--part-of`
    or references); they stay, without the link.
    """
    _confirmed_delete(
        "project",
        project_id,
        yes=yes,
        cascade=(
            "every experiment, run, metric and file inside it goes too"
            + (
                " (--recursive is accepted and changes nothing: the projects linked "
                "to it, part_of included, stay where they are)"
                if recursive
                else ""
            )
        ),
        delete_kwargs={"recursive": True} if recursive else None,
        trash=True,
        dry_run=dry_run,
    )
from probe.cli.commands.delete import _confirmed_delete  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.flag_values import _text_value  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
