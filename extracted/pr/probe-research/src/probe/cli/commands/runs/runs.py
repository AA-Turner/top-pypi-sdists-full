"""probe run start/fork/child/set/move/list/tag/expect/delete and probe link: open, file and amend runs."""

from __future__ import annotations
import math
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from probe import analytics as probe_telemetry
    from ....sdk.client.client import Client
else:
    #: The SDK client class: a module global so the CLI package can monkeypatch
    #: it in tests, and None until then. The SDK client imports every wire model,
    #: so a command imports it when it builds one (`_client_class`), not at start.
    Client = None

import typer

from probe.cli.commands.commands import register_group

from .... import errors
from ....sdk.errors import NotFoundError
from .. import ref_syntax as refs
from probe.cli.cli import app
from probe.cli.commands.entity_text import (
    AuthoredBy,
    _authored_by_value,
    authored_by_opt,
    description_opt,
    notes_opt,
)
from probe.cli.commands.json_print import _FIELDS_OPTION, _print_json, _print_link, _select_fields
from probe.cli.commands.refs import _ambient_project, _project_id, _project_slug, _ref, run_ref


# -- enums (choices) --------------------------------------------------------
# `Scope` is not redefined here: it is imported from the generated contract models,
# so `make regen` picks up a new backend scope for free instead of drifting.
class Relation(str, Enum):
    fork = "fork"
    resume = "resume"
    retry = "retry"
    branch = "branch"


class RunCorrection(str, Enum):
    """What `run set --status` may record: a FINISHED run's status.

    Not the route's whole vocabulary. `created`/`running` on a finished run skip
    the reopen guard, and the reaper later marks it crashed and emails the
    launcher; `untracked` is the reaper's own verdict, not a correction.
    """

    completed = "completed"
    failed = "failed"
    crashed = "crashed"
    canceled = "canceled"


def run_lock_touch_lease(run_id: str, *, write_epoch: int | None = None) -> None:
    """Best-effort lease write; the lease tier must never break the command."""
    try:
        from probe.foundation.durable import run_lock

        run_lock.touch_lease(run_id, write_epoch=write_epoch)
    except Exception:  # noqa: BLE001
        pass


def _container(client: Client, ref: str) -> tuple[str, str]:
    """A project OR experiment ref (slug, or ``id:<uuid>``) -> ``(id, kind)``,
    kind ``project`` or ``experiment``, for a verb that files something in
    either (``run move --to``).

    One ``GET /v1/scopes`` places either: slugs are one tenant-wide namespace
    shared by projects and experiments, so this never leans on the projects
    list answering an experiment row (the leaf door, removed at R6). A
    ``name:`` ref, and a server older than ``/v1/scopes?slug=``, fall back to
    the project resolver (kind ``project``: that server files by project id)."""
    bare, how = refs.split_selector(ref)
    if how == "name":
        return _project_id(client, ref), "project"
    try:
        scope = client.get_scope(bare) if how == "id" else client.get_scope_by_slug(bare)
    except errors.CapabilityUnavailable:
        return _project_id(client, ref), "project"
    except NotFoundError:
        raise typer.BadParameter(f"no project or experiment {ref!r}") from None
    if scope.get("kind") not in ("project", "experiment"):
        raise typer.BadParameter(
            f"{ref!r} is a {scope.get('kind')}: name a project or an experiment"
        )
    return str(scope["id"]), str(scope["kind"])


# -- run lifecycle ----------------------------------------------------------
run_app = typer.Typer(no_args_is_help=True, help="run lifecycle")

#: `probe run --help` order (runs, run_end, tokens, reads and snapshots/restore register them).
RUN_GROUP = register_group(
    run_app,
    (
        "start", "fork", "child", "set", "move", "list", "tag", "expect", "end", "token", "check",
        "reproduce", "delete", "series", "metrics", "inputs", "upstream", "get",
    ),
)


@run_app.command("start")
def run_start(
    experiment: str = typer.Option(
        None,
        "--experiment",
        help="slug of an EXISTING experiment; omit for a PROJECT-DIRECT run (W&B shape)",
    ),
    name: str = typer.Option(
        None,
        "--name",
        help="defaults to the run's slug, or a server petname when there is none, "
        "which a generated title then replaces once the run ends",
    ),
    slug: str = typer.Option(
        None,
        "--slug",
        help="this run's slug; omit and the server mints a petname (a taken one is an error)",
    ),
    description: str = description_opt(),
    project: str = typer.Option(
        None,
        "--project",
        help="project slug (or id:<uuid>); defaults to the active one (`probe project use`)",
    ),
    group: str = typer.Option(None, "--group", help="run group id (see `probe group create`)"),
    source: str = typer.Option("api", "--source"),
    external_id: str = typer.Option(None, "--external-id"),
    config: list[str] = typer.Option(None, "--config", metavar="k=v"),
    tag: list[str] = typer.Option(None, "--tag"),
    rewind_to_step: int = typer.Option(
        None,
        "--rewind-to-step",
        min=0,
        help="relaunch of --external-id from a checkpoint: DISCARD its record "
        "from this step onward and rewrite it (0185). Unlocks a completed "
        "incumbent; without this flag nothing is ever deleted.",
    ),
    intent: str = typer.Option(
        None, "--intent", help="what this run is meant to show (free text, kept in its metadata)"
    ),
    authored_by: AuthoredBy = authored_by_opt(),
) -> None:
    """Open a run inside an EXISTING experiment, or directly under a project.

    This no longer creates the experiment or project. Create them first with
    `probe project create` / `probe experiment create`; an unknown slug now errors
    and names the closest existing ones instead of minting a second identity.
    Without --experiment the run attaches straight to the project (--project or
    the active one) with no experiment at all — the W&B model. With neither and
    no active project it refuses before anything is sent: every run has a project.
    """
    # This is what makes `probe project use` mean something: without it the ambient
    # project would be stored and displayed but never actually applied to a write.
    # Explicit flag still wins, so scripts never depend on a developer's context.
    resolved_project = _ambient_project(project)
    if rewind_to_step is not None and not external_id:
        # A rewind resumes an EXISTING identity; without the key there is no
        # incumbent to rewind and the flag would silently do nothing.
        raise errors.ValidationError(
            "--rewind-to-step needs --external-id: the rewind targets the "
            "existing run that identity names"
        )
    # 0205, DEPRECATION RELEASE. A bare `run start` opens a row that nothing
    # owns: this process exits immediately, never beats, and the run survives
    # only until the reaper notices. Measured on one tenant: 41 of 41 runs
    # opened this way, 3 with any owner heartbeat, 8 ended 'untracked' ~16
    # minutes into work that was still running. The next release refuses it; for
    # now it warns and creates, so nobody's script breaks on the release that
    # tells them.
    typer.echo(
        "probe: `run start` opens a run nothing owns -- it will be marked "
        "'untracked' once it goes quiet, even if the work is fine.\n"
        "       probe exec [--project P] -- CMD      wrap the process; status from its exit code\n"
        "       probe.init() inside the job          attaches via PROBE_RUN_ID; heartbeats\n"
        "       connect W&B in the dashboard         a connector owns the run\n"
        "       This command is refused in the next release.",
        err=True,
    )
    from ....sdk.client.resources.runs.reopen.conflict import Rewind

    with _client() as c:
        run = c.run(
            experiment=experiment,
            on_conflict=(Rewind(step=rewind_to_step) if rewind_to_step is not None else "auto"),
            name=name,
            # Omitted = the server mints a petname, unchanged. Naming it is what
            # lets a nightly job address the same run every time.
            slug=slug,
            description=description,
            # run() resolves by SLUG, so an id has to be translated first or the
            # lookup misses and reports a real project as absent.
            project=_project_slug(c, resolved_project),
            group_id=group,
            source=source,
            external_id=external_id,
            config=_kv_pairs(config) if config else None,
            tags=tag or None,
            intent=intent,
            # A CLI-opened run is detached: this process exits immediately and the
            # run is closed later by `probe run end`. Beating here would stop the
            # moment we exit and get the run reaped mid-flight (see heartbeat_run).
            heartbeat=False,
            # Reaches the run AND, through run()'s ensure_* paths, any project or
            # experiment auto-created alongside it.
            authored_by=_authored_by_value(authored_by),
        )
        # Pin this bracket's writer generation in the auto-update lease (0185):
        # every later run-scoped CLI write stamps this epoch, so a bracket
        # superseded by a reopen elsewhere is refused instead of splicing.
        run_lock_touch_lease(run.id, write_epoch=run.write_epoch)
    print(run.id)
    _print_link("run", run.id)


@run_app.command("fork")
def run_fork(
    source: str = typer.Argument(..., help="source run (slug or id:<uuid>)"),
    step: int = typer.Option(
        None, "--step", min=0, help="the checkpoint step this fork continues from"
    ),
    name: str = typer.Option(None, "--name", help="defaults to <source>-fork"),
    authored_by: AuthoredBy = authored_by_opt(),
) -> None:
    """Open a NEW run continuing SOURCE from --step; SOURCE stays untouched.

    The keep-both alternative to `run start --rewind-to-step`: the fork logs
    from the checkpoint onward under its own identity (parent_relation="fork" +
    fork_of/fork_step foreign keys) and the source keeps its whole curve,
    unmarked — unlike supersede, this is not a correction of anything.
    """
    with _client() as c:
        run = c.fork_run(
            str(_ref(c, "run", source).id),
            step=step,
            name=name,
            # Detached like `run start`: this process exits immediately.
            heartbeat=False,
            authored_by=_authored_by_value(authored_by),
        )
        run_lock_touch_lease(run.id, write_epoch=run.write_epoch)
    print(run.id)
    _print_link("run", run.id)


@run_app.command("child")
def run_child(
    run: str = run_ref(),
    name: str = typer.Option(None, "--name", help="omit it: the server mints a name"),
    description: str = description_opt(),
    # REQUIRED. Defaulted to `fork` until the lineage audit: the four relations
    # mean different things, and a default writes the most common one onto every
    # caller who did not think about it.
    relation: Relation = typer.Option(..., "--relation"),
    source: str = typer.Option("api", "--source"),
    external_id: str = typer.Option(None, "--external-id"),
    authored_by: AuthoredBy = authored_by_opt(),
) -> None:
    """Open a sub-run under an existing run.

    The child inherits the parent's attachment: its experiment when it has one,
    else its project (a project-direct parent begets a project-direct child). An
    unfiled parent (an older CLI made it) is refused: move it first.
    """
    # 0205, same rule as `run start` (D30): a child is its own row and the
    # reaper judges it on its own signals. Inheriting the parent's beats would
    # make a dead child read 'running' for as long as the parent lives, which is
    # the hollow row one level down.
    typer.echo(
        "probe: `run child` opens a run nothing owns. Wrap the child's process "
        "with `probe exec`, or let it attach from inside via PROBE_RUN_ID.\n"
        "       This command is refused in the next release.",
        err=True,
    )
    with _client() as c:
        parent = _ref(c, "run", run).row
        common = dict(
            # The parent's ID, not the ref the caller typed. `parent_run_id` is a
            # UUID field, so a petname here reached the server as one and was
            # rejected -- and the row was already in hand to answer it.
            parent_run_id=parent["id"],
            parent_relation=relation.value,
            description=description,
            source=source,
            external_id=external_id,
            heartbeat=False,  # detached, same as `run start`
            authored_by=_authored_by_value(authored_by),
        )
        if parent.get("experiment_id"):
            child = c.create_run(
                parent["experiment_id"], name, project_id=parent.get("project_id"), **common
            )
        elif parent.get("project_id"):
            child = c.create_project_run(parent["project_id"], name, **common)
        elif "project_id" in parent:
            # Unfiled (an older CLI made it): no home to inherit.
            raise errors.build_unfiled_parent_error(run)
        else:
            # A pre-0054 backend's run rows carry no project_id field at all;
            # a KeyError traceback here would say nothing actionable.
            raise errors.ValidationError(
                f"run {run} reports neither an experiment nor a project — this "
                "research-os backend predates project-direct runs (0054). "
                "Upgrade the backend, or open the child under an experiment "
                "with `probe run start --experiment`."
            )
    print(child.id)


@run_app.command("set")
def run_set(
    run: str = run_ref(),
    name: str = typer.Option(None, "--name"),
    description: str = description_opt(),
    notes: str = notes_opt(),
    status: RunCorrection = typer.Option(
        None,
        "--status",
        help=(
            "correct a finished run's status; start and end times are kept. `failed` "
            "emails the run's launcher. To close a running run, `run end`"
        ),
    ),
    authored_by: AuthoredBy = authored_by_opt(),
) -> None:
    """Update a run's human title, description, notes or status.

    `--status` corrects a FINISHED run's record and sends no start or end time,
    so the run's duration stays as recorded. Only finished statuses are taken:
    `running` or `created` on a finished run would skip the reopen guard, and
    the reaper would later mark it crashed and email the launcher. `probe run
    end --status` is not the same thing: it stamps the end time NOW, which
    rewrites the duration of a run that finished long ago.

    `--notes` is NOT a second description, and the difference decides which one a
    caveat goes in. A description says what the run IS and is written before it
    runs; notes say what a later reader should DISTRUST about it, and are nearly
    always learned after it finished -- a broken verifier, an environment that
    was not what it claimed, a number that means less than it looks like it does.
    Writing the caveat into the description means destroying the description to
    keep it.

    A run scored 0.0 by a broken harness is the case this exists for: tag it
    (`probe run tag RUN invalid`) so a reader is warned, and write the notes so
    they know why.
    """
    if name is None and description is None and notes is None and status is None:
        raise typer.BadParameter("pass at least one of --name/--description/--notes/--status")
    with _client() as c:
        # PATCH /v1/runs/{run_id} is UUID-typed, so a petname has to be resolved
        # before it is sent -- unresolved it 422s with a raw pydantic uuid dump.
        # Same reason `run delete` resolves; this verb was missed by that pass.
        run_id = _ref(c, "run", run).id
        _print_json(
            c.update_run(
                run_id,
                name=name,
                description=description,
                notes=_text_value(notes),
                status=status.value if status is not None else None,
                authored_by=_authored_by_value(authored_by),
            )
        )
    if notes:
        _note_landed("run", run_id)


@run_app.command("move")
def run_move(
    run: str = run_ref(),
    to: str = typer.Option(..., "--to", help="the project or experiment to file the run in (slug or id:<uuid>)"),
    group: str = typer.Option(None, "--group", help="a sweep group inside that experiment (group id)"),
) -> None:
    """File a run in a project or experiment (and optionally a sweep group).

    Moves a run to another home. Its metrics, files, notes and lineage move
    with it. Every run has a home: there is no unfiling."""
    with _client() as c:
        run_id = _ref(c, "run", run).id
        target, kind = _container(c, to)
        # An experiment goes as an experiment (`experiment_id`), never as a
        # project id: that address is the leaf door R6 removes.
        if kind == "experiment":
            _print_json(c.move_run(run_id, experiment_id=target, group_id=group))
        else:
            _print_json(c.move_run(run_id, project_id=target, group_id=group))


@run_app.command("list")
def run_list(
    experiment: str = typer.Option(None, "--experiment", help="experiment slug (or id:<uuid>)"),
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    direct: bool = typer.Option(False, "--direct", help="only project-direct runs"),
    tag: list[str] = typer.Option(None, "--tag", help="filter: run must carry ALL (repeatable)"),
    limit: int = typer.Option(50, "--limit", min=1, max=200),
    cursor: str = typer.Option(None, "--cursor", help="keyset cursor from a previous page"),
    fields: str = _FIELDS_OPTION,
) -> None:
    """List runs, filterable by experiment, project, and tags (AND semantics)."""
    parameters: dict[str, Any] = {"limit": limit}
    if cursor:
        parameters["cursor"] = cursor
    with _client() as c:
        page = c.list_runs(
            # Resolved, not passed through: experiment_id is a UUID-typed query
            # param, so a slug used to come back as a raw pydantic uuid_parsing
            # dump rather than a listing.
            experiment_id=_ref(c, "experiment", experiment).id if experiment else None,
            project_id=_project_id(c, project) if project else None,
            direct=direct,
            tags=tag or None,
            **parameters,
        )
    _print_json(_select_fields({"items": page.items, "next_cursor": page.next_cursor}, fields))


@run_app.command("tag")
def run_tag(
    run: str = run_ref(),
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
    """Tag a run: positional args add, --remove drops, --set replaces; bare lists.

    Read-modify-write over PATCH's whole-list replace (the server normalizes to
    lowercase-kebab and 422s past the caps). Retro-tag runs the SDK is DONE
    with: a still-live run's next push replaces out-of-band edits (last writer
    wins — CONTRACT.md "tags")."""
    with _client() as c:
        handle = _run_handle(c, run)
        before = list(handle.tags or [])
        # strict=True: an interactive tag edit must fail loudly, never spool a
        # stale whole-list replace for delayed replay (review 2026-07-30).
        result = _tag_verb_flow(
            handle.id,
            handle.tags,
            add,
            remove,
            replace,
            lambda wanted: handle.set_tags(wanted, strict=True),
        )
        _print_json(result)
    from ....shared.notes import owed

    # A result tagged not to trust owes a note on what to believe instead (notes
    # parity N3); one no longer tagged so owes nothing (`--remove invalid`, `--set`).
    owed.after_tag(run, str(result.get("id") or handle.id), before, result.get("tags"))


@run_app.command("expect")
def run_expect(
    run: str = run_ref(),
    key: str = typer.Argument(..., help="metric key, e.g. val/acc"),
    minimum: Optional[float] = typer.Option(None, "--min", help="email when a value goes below this"),
    maximum: Optional[float] = typer.Option(None, "--max", help="email when a value goes above this"),
    clear: bool = typer.Option(False, "--clear", help="remove the range declared for KEY"),
) -> None:
    """Declare the range a metric should stay in; Probe emails the run's creator
    the first time a value leaves it.

    For a run already going -- no code change, no restart. A script declares the
    same thing with `probe.expect({...})`. Every value already logged for the key
    is judged too; the same range declared again does not re-send an email."""
    if clear and (minimum is not None or maximum is not None):
        raise typer.BadParameter("--clear takes no --min/--max")
    if not clear and minimum is None and maximum is None:
        raise typer.BadParameter("give --min, --max (or both), or --clear")
    for flag, bound in (("--min", minimum), ("--max", maximum)):
        if bound is not None and not math.isfinite(bound):
            raise typer.BadParameter(f"{flag} must be a finite number")
    if minimum is not None and maximum is not None and minimum > maximum:
        raise typer.BadParameter(f"--min {minimum} is above --max {maximum}")
    with _client() as c:
        handle = _run_handle(c, run)
        # strict=True: an interactive declaration must fail loudly, never spool.
        handle.expect({key: None if clear else (minimum, maximum)}, strict=True)
        _print_json(
            {"run": handle.id, "key": key, "removed": True}
            if clear
            else {"run": handle.id, "key": key, "min": minimum, "max": maximum}
        )


@run_app.command("delete")
def run_delete(
    run: str = run_ref(),
    yes: bool = typer.Option(False, "--yes", help="skip the confirmation prompt"),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="change nothing: print what the delete would take, whose it is and when it last changed",
    ),
) -> None:
    """Move a run and its telemetry to the trash (Probe support can restore
    it for 21 days, then it is deleted for good). A server without the trash
    deletes it permanently, and the prompt says so."""
    # No --by-* here: a slug is a server-minted petname, so it cannot be
    # UUID-shaped and cannot collide with an id. See refs.resolve_run.
    _confirmed_delete(
        "run", run, yes=yes, cascade="its spans, metrics and files go too", trash=True, dry_run=dry_run
    )


# -- link / snapshot / flush / reads ----------------------------------------
@app.command()
def link(
    run: str = typer.Argument(...),
    set_pairs: list[str] = typer.Option(..., "--set", metavar="k=v"),
) -> None:
    """Attach foreign keys (stored under metadata.foreign_keys)."""
    keys = _kv_pairs(set_pairs)
    with _client() as c:
        _run_handle(c, run).link(**keys)
    print(f"linked {', '.join(keys)} to {run}")
from probe.cli.commands.delete import _confirmed_delete  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.flag_values import _kv_pairs, _text_value  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.notes.targets import _note_landed  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.run_handle import _run_handle  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.tags import _tag_verb_flow  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
