"""probe experiment ... (create, fork, inherited, reproduce, freeze, get, set, move, list, delete, edges, lineage, branch) and its immutable versions (probe version)."""

from __future__ import annotations
import sys

import typer

from .... import errors
# The option enums only, from `_generated.enums` rather than `probe.models`: that
# seam builds every wire model, ~0.5 s that every command paid at startup -- the
# wizard, the hooks and the status line included -- whether or not it sent one.
# `tests/test_cli_startup_imports.py` holds the CLI to this.
from ....generated.enums import (
    MetricGoal,
    MetricReduce)
from ....shared.reads import reads
from probe.cli.commands.entity_text import AuthoredBy, _authored_by_value, authored_by_opt, entity_markdown_opt
from probe.cli.commands.metric_pick import _declare, _metric_args, goal_opt, metric_opt, reduce_opt
from probe.cli.commands.refs import (
    _ambient_project,
    _api,
    _filed_under,
    _project_id,
    _project_slug,
    _ref,
    slug_ref,
)


# -- experiment maintenance ---------------------------------------------------
experiment_app = typer.Typer(no_args_is_help=True, help="experiment maintenance")

#: Why every experiment tag flag is refused. The server keeps an experiment's
#: tags read-only since the light experiments gave it its own record (R3), and
#: the experiment API carries none -- so a tag write could only ever fail there.
_EXPERIMENT_TAGS_READ_ONLY = (
    "an experiment's tags are read-only since experiments moved to their own record; "
    "tag the project instead (`probe project tag`), or say it in the question or notes"
)
#: 0231: an experiment's description is its question. Refused before any call,
#: as a usage error: the SDK's ValueError reached `experiment create` as a crash
#: (Tokenless 2026-10-26: 14 of them in one import, whose prompt asked for it).
_EXPERIMENT_DESCRIPTION_RETIRED = (
    "an experiment's description was replaced by its QUESTION (0231). Use "
    "--question for what the experiment is testing, or --summary for prose "
    "about it -- which is where existing descriptions were moved."
)


@experiment_app.command("create")
def experiment_create(
    slug: str = typer.Argument(..., help="url-safe identifier, unique per tenant"),
    question: str = typer.Option(..., "--question", help="the one question it answers"),
    name: str = typer.Option(
        None, "--name", help="display name; omit it and the row reads as its slug"
    ),
    project: str = typer.Option(
        None, "--project", help="project slug; defaults to the active one (`probe project use`)"
    ),
    summary: str = entity_markdown_opt(),
    #: RETIRED, both declared so they can be REFUSED with the reason (Typer's
    #: "no such option" reads as a typo).
    description: str = typer.Option(
        None,
        "--description",
        help="RETIRED: an experiment's description is now its --question",
        hidden=True,
    ),
    tag: list[str] = typer.Option(
        None, "--tag", help="RETIRED: an experiment's tags are read-only", hidden=True
    ),
    authored_by: AuthoredBy = authored_by_opt(),
) -> None:
    """Create an experiment in a project.

    The counterpart to `probe project create`. Both exist because `probe run start`
    no longer creates its parents: it used to get-or-create the whole chain, so a
    typo'd slug minted a second identity instead of erroring, and an omitted
    question minted a permanent `[auto]` placeholder.

    `--question` is required here for that reason — this is the moment you know
    what you are testing, and nothing later goes back to fill it in.
    """
    if description is not None:
        raise typer.BadParameter(_EXPERIMENT_DESCRIPTION_RETIRED, param_hint="--description")
    if tag:
        raise typer.BadParameter(_EXPERIMENT_TAGS_READ_ONLY, param_hint="--tag")
    resolved_project = _ambient_project(project)
    if not resolved_project:
        raise errors.ValidationError(
            "pass --project, or set an active project with `probe project use`"
        )
    with _client() as c:
        # Same resolver as `run start`, so "no such project" is one error with
        # one exit code, and the message names the SLUG that was looked up rather
        # than the raw ambient value (which is an id).
        project_id = c.resolve_or_raise("project", _project_slug(c, resolved_project))["id"]
        created = c.create_experiment(
            slug,
            name,
            question=question,
            project_id=project_id,
            document=_text_value(summary),
            authored_by=_authored_by_value(authored_by),
        )
    _print_json(created)
    _print_link("experiment", created.get("id"))


@experiment_app.command("fork")
def experiment_fork(
    source: str = slug_ref("experiment"),
    slug: str = typer.Argument(..., help="the fork's slug, unique per tenant"),
    question: str = typer.Option(
        ..., "--question", help="the fork's own question: what it tries that the source did not"
    ),
    name: str = typer.Option(
        None, "--name", help="display name; omit it and the row reads as its slug"
    ),
    authored_by: AuthoredBy = authored_by_opt(),
) -> None:
    """Fork an experiment: a new experiment in the same project that starts where SOURCE is.

    Copies SOURCE's notes (opening with a line naming it), sub-notes, page
    document, tags, chart settings and its own files (nothing is uploaded
    again), links the fork `forked_from` SOURCE, and reads SOURCE's runs and
    their files live until one changes on SOURCE's side, when the fork keeps
    its own copy. List what it reads with `probe experiment inherited SLUG`.
    Use it instead of `experiment create` + `edge add` when the new experiment
    starts from another one's notes and files.
    """
    with _client() as c:
        target = _ref(c, "experiment", source)
        created = c.fork_experiment(
            target.id,
            slug,
            question=question,
            name=name,
            project_id=_filed_under(target),
            authored_by=_authored_by_value(authored_by),
        )
    _print_json(created)
    _print_link("experiment", created.get("id"))


@experiment_app.command("inherited")
def experiment_inherited(
    experiment_id: str = slug_ref("experiment"),
    runs: bool = typer.Option(False, "--runs", help="list the runs instead of their files"),
    after: str = typer.Option(None, "--after", help="`next_after` of the previous page"),
    limit: int = typer.Option(None, "--limit", min=1, max=1000, help="page size (default 200)"),
) -> None:
    """Print what a fork reads live from its source: the source chain, then
    the source runs' files (or `--runs`) as they were at the fork. A file id
    here is the source run's own: `probe artifact download` reads it as is."""
    with _client() as c:
        target = _ref(c, "experiment", experiment_id)
        _print_json(
            c.experiment_inherited(
                target.id, runs=runs, after=after, limit=limit, project_id=_filed_under(target)
            )
        )


@experiment_app.command("reproduce")
def experiment_reproduce(
    experiment_id: str = slug_ref("experiment"),
    version: int = typer.Option(
        None, "--version", help="pin against a minted experiment version (else live rows)"
    ),
) -> None:
    """Pull per-run reproduction summaries for an experiment.

    A MAP, not N full assemblies: each summary carries a `reproduce_url` — drill
    into one run with `probe run reproduce RUN`. `--version N` reads a frozen
    `experiment freeze` manifest instead of the live run set.
    """
    with _client() as c:
        _print_json(
            c.experiment_reproduce(_ref(c, "experiment", experiment_id).id, version=version)
        )


@experiment_app.command("freeze")
def experiment_freeze(
    experiment_id: str = slug_ref("experiment"),
    label: str = typer.Option(None, "--label", help="a human name for this frozen manifest"),
) -> None:
    """Freeze the experiment: mint an immutable version pinning its current run set.

    An ergonomic alias for `probe version create` — the moment you publish or hand
    off an experiment, this pins exactly which runs and artifacts it comprised, so
    `experiment reproduce --version N` resolves against that manifest forever. No
    new backend: it mints the same `experiment_versions` row.
    """
    with _client() as c:
        _print_json(c.experiment_version(_ref(c, "experiment", experiment_id).id, label=label))


@experiment_app.command("get")
def experiment_get(experiment_id: str = slug_ref("experiment")) -> None:
    """Show one experiment.

    Experiments were the only addressable kind with NO read verb: projects,
    workspaces, runs and groups all had one, and `experiment list` was the whole
    surface. Reading one back after a `set` meant listing its siblings and
    filtering by eye.
    """
    with _client() as c:
        _emit(reads.experiment_get(_api(c, pretty=sys.stdout.isatty()), experiment_id))


@experiment_app.command("set")
def experiment_set(
    experiment_id: str = slug_ref("experiment"),
    question: str = typer.Option(None, "--question", help="replace the question"),
    conclusion: str = typer.Option(
        None, "--conclusion", help='the answer, once the work gives one ("" clears)'
    ),
    dead_end: str = typer.Option(
        None,
        "--dead-end",
        help="mark it a dead end and say why (@file and - read the reason); it still ranks",
    ),
    clear_dead_end: bool = typer.Option(
        False, "--clear-dead-end", help="clear its dead-end mark"
    ),
    name: str = typer.Option(None, "--name"),
    #: 0231: RETIRED, and declared so it can be REFUSED. Deleting the option
    #: makes Typer answer "no such option", which reads as a typo; this says
    #: what happened and which flag replaced it.
    description: str = typer.Option(
        None,
        "--description",
        help="RETIRED: an experiment's description is now its --question",
        hidden=True,
    ),
    summary: str = entity_markdown_opt(),
    #: RETIRED with the light experiments, like --description above.
    add_tag: list[str] = typer.Option(None, "--add-tag", hidden=True),
    remove_tag: list[str] = typer.Option(None, "--remove-tag", hidden=True),
    set_tags: list[str] = typer.Option(None, "--set-tags", hidden=True),
    metric: str = metric_opt(),
    goal: MetricGoal = goal_opt(),
    reduce: MetricReduce = reduce_opt(),
    authored_by: AuthoredBy = authored_by_opt(),
) -> None:
    """Amend an experiment's question, conclusion, name or visible Markdown, in one command.

    `--dead-end "<why>"` marks it a dead end (its branch reads `dead_end` until
    a run of it is live; it still ranks), `--clear-dead-end` clears the mark.
    Or, alone, override its project's headline metric. A person's metric or
    dead-end mark can't be replaced.
    """
    if description is not None:
        raise typer.BadParameter(_EXPERIMENT_DESCRIPTION_RETIRED, param_hint="--description")
    if _tag_flags_given(add_tag, remove_tag, set_tags):
        raise typer.BadParameter(_EXPERIMENT_TAGS_READ_ONLY)
    if [conclusion, summary, dead_end].count("-") > 1:
        # The second would read an emptied stdin as "" and clear its field.
        raise typer.BadParameter(
            "only one of --conclusion, --summary and --dead-end can read stdin (-)"
        )
    if dead_end is not None and clear_dead_end:
        raise typer.BadParameter("--dead-end marks it and --clear-dead-end clears it: pass one")
    if (goal is not None or reduce is not None) and metric is None:
        raise typer.BadParameter("--goal and --reduce need --metric")
    if metric is not None:
        if clear_dead_end or any(
            v is not None for v in (question, conclusion, name, summary, dead_end, authored_by)
        ):
            raise typer.BadParameter("--metric goes alone")
        clears = _metric_args(metric, goal, reduce)
        with _client() as c:
            target = _ref(c, "experiment", experiment_id)
            home = _filed_under(target)
            if clears:
                _declare(lambda: c.clear_experiment_metric(target.id, project_id=home))
            else:
                _declare(
                    lambda: c.set_experiment_metric(
                        target.id,
                        metric,
                        goal=goal.value,
                        reduce=reduce.value if reduce else None,
                        project_id=home,
                    )
                )
        return
    fields = {
        "question": question,
        "conclusion": _text_value(conclusion),
        "name": name,
        "document": _text_value(summary),
    }
    reason = _text_value(dead_end)
    if reason is not None and not reason.strip():
        raise typer.BadParameter("say why it is a dead end", param_hint="--dead-end")
    if all(value is None for value in fields.values()) and reason is None and not clear_dead_end:
        raise typer.BadParameter(
            "pass at least one of --question/--conclusion/--name/--summary/--dead-end/"
            "--clear-dead-end/--metric"
        )
    with _client() as c:
        target = _ref(c, "experiment", experiment_id)
        result = c.update_experiment(
            target.id,
            **fields,
            dead_end=reason.strip() if reason is not None else None,
            clear_dead_end=clear_dead_end,
            authored_by=_authored_by_value(authored_by),
            project_id=_filed_under(target),
        )
    _print_json(result)


@experiment_app.command("move")
def experiment_move(
    experiment_id: str = slug_ref("experiment"),
    to: str = typer.Option(..., "--to", help="the project to move it to (slug or id:<uuid>)"),
) -> None:
    """Move an experiment, with its runs, files and groups, to another project.

    One write on the server: everything filed under the experiment follows it
    in the same statement. Needs edit access on both projects. The experiment
    keeps its id and slug; address it under the new project afterwards.
    """
    with _client() as c:
        target = _ref(c, "experiment", experiment_id)
        _print_json(
            c.move_experiment(
                target.id,
                _project_id(c, to),
                from_project_id=_filed_under(target),
            )
        )


@experiment_app.command("list")
def experiment_list(
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    #: RETIRED with the light experiments: an experiment's tags are read-only
    #: and the experiment list filters on none.
    tag: list[str] = typer.Option(None, "--tag", hidden=True),
    limit: int = typer.Option(50, "--limit", min=1, max=200),
    cursor: str = typer.Option(None, "--cursor", help="next_cursor from a previous page"),
) -> None:
    """List a project's experiments, newest first; without --project, every project's.

    Without --project this reads every project's list (one request each), so
    naming the project is faster.
    """
    if tag:
        raise typer.BadParameter(_EXPERIMENT_TAGS_READ_ONLY, param_hint="--tag")
    with _client() as c:
        page = c.list_experiments(
            project_id=_project_id(c, project) if project else None,
            limit=limit,
            cursor=cursor or None,
        )
    _print_json({"items": page.items, "next_cursor": page.next_cursor})


@experiment_app.command("tag", hidden=True)
def experiment_tag(
    experiment_id: str = slug_ref("experiment"),
    add: list[str] = typer.Argument(None, help="tags to add"),
    remove: list[str] = typer.Option(None, "--remove", help="tag to remove"),
    replace: list[str] = typer.Option(None, "--set", help="replace the whole list"),
) -> None:
    """RETIRED: an experiment's tags are read-only since it moved to its own record."""
    raise typer.BadParameter(_EXPERIMENT_TAGS_READ_ONLY)


@experiment_app.command("delete")
def experiment_delete(
    experiment_id: str = slug_ref("experiment"),
    yes: bool = typer.Option(False, "--yes", help="skip the confirmation prompt"),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="change nothing: print what the delete would take, whose it is and when it last changed",
    ),
) -> None:
    """Move an experiment and its runs to the trash (Probe support can
    restore it for 21 days, then it is deleted for good). A server without the
    trash deletes it permanently, and the prompt says so."""
    _confirmed_delete(
        "experiment",
        experiment_id,
        yes=yes,
        cascade="every run, metric and file inside it goes too",
        trash=True,
        dry_run=dry_run,
    )


@experiment_app.command("edges")
def experiment_edges(experiment_id: str = slug_ref("experiment")) -> None:
    """Print every lineage edge under an experiment.

    Takes the slug, like `experiment get` and every other verb here: this was the
    one that still demanded a raw UUID, so the handle people are given rejected
    them on exactly one command. A bare UUID now needs the `id:` spelling the
    slug-default rule asks for everywhere else (refs.py), and says so.
    """
    with _client() as c:
        _print_json(c.experiment_edges(_ref(c, "experiment", experiment_id).id))


@experiment_app.command("lineage")
def experiment_lineage(experiment_id: str = slug_ref("experiment")) -> None:
    """Print the experiment's OWN links: what it came from and what came from it.

    `experiment edges` is the graph AMONG its runs and files. This is the
    experiment as one node: its links in and out (stored, then "built on"
    derived from what its runs used, `derived: true`), its `origin` and its
    direct children. Look here before linking it to anything.
    """
    with _client() as c:
        target = _ref(c, "experiment", experiment_id)
        _print_json(c.experiment_lineage(target.id, project_id=_filed_under(target)))


@experiment_app.command("branch")
def experiment_branch(experiment_id: str = slug_ref("experiment")) -> None:
    """Print the experiment's line of work and the ones it split from."""
    with _client() as c:
        target = _ref(c, "experiment", experiment_id)
        _print_json(c.experiment_branch(target.id, project_id=_filed_under(target)))


# -- experiment versions (fold #6) ------------------------------------------
version_app = typer.Typer(no_args_is_help=True, help="immutable experiment version manifests")


@version_app.command("create")
def version_create(
    experiment_id: str = typer.Argument(...),
    label: str = typer.Option(None, "--label"),
) -> None:
    """Mint an immutable experiment version (launch-time manifest)."""
    with _client() as c:
        result = c.experiment_version(experiment_id, label=label)
    _print_json(result)


@version_app.command("list")
def version_list(experiment_id: str = typer.Argument(...)) -> None:
    """List an experiment's versions."""
    with _client() as c:
        _print_json(c.list_experiment_versions(experiment_id))
from probe.cli.commands.delete import _confirmed_delete  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.flag_values import _text_value  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.json_print import _emit, _print_json, _print_link  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.tags import _tag_flags_given  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
