"""a project's links and code: probe project reference add/remove, project code attach/list/detach/confirm, probe commits."""

from __future__ import annotations

import typer
from probe.cli.cli import app
from probe.cli.commands.json_print import _FIELDS_OPTION, _print_json, _select_fields
from probe.cli.commands.refs import _project_id, slug_ref


# -- project references (0153) -----------------------------------------------
reference_app = typer.Typer(
    no_args_is_help=True,
    help=(
        "Links between projects, which are flat. A references B: a review "
        "informed a training run, or two efforts share a method. A is part "
        "of B (--part-of): a phase of a bigger effort. Cycles and any depth "
        "are fine."
    ),
)


@reference_app.command("add")
def project_reference_add(
    project_id: str = slug_ref("project"),
    to: str = typer.Option(..., "--to", help="the project it references (slug or id:<uuid>)"),
    part_of: bool = typer.Option(
        False, "--part-of", help="this project is a part of that one, not only drawing on it"
    ),
) -> None:
    """Record that this project references another, or is a part of it.

    Idempotent and DIRECTED: adding A->B does not add B->A. Neither project
    moves, and nothing is shared or deleted through the link. One link per
    pair: --part-of upgrades a reference, and a plain add never downgrades a
    part-of link. `project get` shows them apart: `references` and
    `part_of_links`.
    """
    from ....sdk.client.resources.projects.papers import ProjectRelation

    with _client() as c:
        c.add_project_reference(
            _project_id(c, project_id),
            _project_id(c, to),
            relation=ProjectRelation.PART_OF.value if part_of else None,
        )
    print("linked as a part" if part_of else "referenced")


@reference_app.command("remove")
def project_reference_remove(
    project_id: str = slug_ref("project"),
    to: str = typer.Option(..., "--to", help="the referenced project (slug or id:<uuid>)"),
) -> None:
    """Drop one directed link, a reference or a part-of; the opposite
    direction stays."""
    with _client() as c:
        c.remove_project_reference(_project_id(c, project_id), _project_id(c, to))
    print("removed")


# -- project code sources (0134) ---------------------------------------------
code_app = typer.Typer(
    no_args_is_help=True,
    help=(
        "The project's attached GitHub repositories. The commit timeline is "
        "read THROUGH GitHub by the backend — nothing is mirrored, so attach "
        "is cheap and detach loses nothing."
    ),
)


@code_app.command("attach")
def project_code_attach(
    project_id: str = slug_ref("project"),
    repo: str = typer.Argument(..., help="owner/name, or a github.com URL"),
    branch: str = typer.Option(
        None, "--branch", help="branch to follow; default: the repo's default branch"
    ),
    path: str = typer.Option(
        "", "--path", help="monorepo subtree, e.g. training/ (empty = whole repo)"
    ),
    start_sha: str = typer.Option(
        None, "--start-sha", help="history starts here (the project's first commit)"
    ),
    start_at: str = typer.Option(
        None, "--start-at", help="ISO timestamp lower bound (alternative to --start-sha)"
    ),
    readme_embed: bool = typer.Option(
        False,
        "--readme-embed",
        help="also add the [README](…) line to the project's Overview document",
    ),
    reason: str = typer.Option(
        None,
        "--reason",
        help=(
            "why this repo is this project's code — required when an agent "
            "attaches on its own judgment; rendered next to the attribution"
        ),
    ),
    via: str = typer.Option(
        "cli",
        "--via",
        help="attribution shown on the source: cli | agent | wizard",
        hidden=True,
    ),
) -> None:
    """Attach a repository (and branch) so its commit timeline shows on the project.

    Attaching grants no access: the repo must already be covered by the team's
    GitHub App installation, or be public. The strongest evidence is a run
    whose code snapshot names this remote — cite it in --reason.
    """
    with _client() as c:
        source = c.attach_project_code_source(
            _project_id(c, project_id),
            repo=repo,
            ref=branch,
            path_prefix=path or "",
            start_sha=start_sha,
            start_at=start_at,
            add_readme_embed=readme_embed,
            via=via if via in ("cli", "agent", "wizard") else "cli",
            reason=reason,
        )
    _print_json(source)


@code_app.command("list")
def project_code_list(
    project_id: str = slug_ref("project"),
    fields: str = _FIELDS_OPTION,
) -> None:
    """The attached repositories, with status (active / suggested / missing / revoked)."""
    with _client() as c:
        _print_json(_select_fields(c.list_project_code_sources(_project_id(c, project_id)), fields))


@code_app.command("detach")
def project_code_detach(
    project_id: str = slug_ref("project"),
    source_id: str = typer.Argument(..., help="code source id (from `project code list`)"),
) -> None:
    """Detach one repository. Loses nothing but the connection — nothing is mirrored."""
    with _client() as c:
        c.detach_project_code_source(_project_id(c, project_id), source_id)
    print("detached")


@code_app.command("confirm")
def project_code_confirm(
    project_id: str = slug_ref("project"),
    source_id: str = typer.Argument(..., help="suggested source id (from `project code list`)"),
) -> None:
    """Confirm a suggested source (one a run's code snapshot volunteered)."""
    with _client() as c:
        _print_json(c.confirm_project_code_source(_project_id(c, project_id), source_id))


@app.command("commits")
def commits(
    project_id: str = typer.Argument(..., help="project slug (or id:<uuid>)"),
    source: str = typer.Option(
        None, "--source", help="code source id, when several repos are attached"
    ),
    cursor: str = typer.Option(None, "--cursor", help="next-page cursor from a previous page"),
    author: str = typer.Option(None, "--author", help="GitHub login filter"),
    path: str = typer.Option(None, "--path", help="only commits touching this path"),
    limit: int = typer.Option(30, "--limit", min=1, max=50),
    include_excluded: bool = typer.Option(
        False, "--include-excluded", help="also show commits a person excluded"
    ),
    sha: str = typer.Option(
        None, "--sha", help="ONE commit in full (message body, files, linked runs)"
    ),
    fields: str = _FIELDS_OPTION,
) -> None:
    """One page of the project's commit timeline, newest first.

    Read THROUGH GitHub with an honest `state`: `stale` is real data GitHub
    could not refresh just now; `unavailable` means no answer (the reason says
    why) — never an empty history. A run count on a row means runs in this
    project were BASED ON that commit (nearest pushed ancestor).
    """
    with _client() as c:
        resolved = _project_id(c, project_id)
        if sha:
            _print_json(_select_fields(c.get_project_commit(resolved, sha, source), fields))
            return
        page = c.list_project_commits(
            resolved,
            source_id=source,
            cursor=cursor,
            author=author,
            path=path,
            limit=limit,
            include_excluded=include_excluded or None,
        )
    _print_json(_select_fields(page, fields))
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
