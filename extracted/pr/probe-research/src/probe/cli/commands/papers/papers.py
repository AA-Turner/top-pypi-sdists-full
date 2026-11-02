"""probe paper add/edges/list/update/tag/remove: the literature a project records."""

from __future__ import annotations

import typer

from probe.cli.commands.commands import register_group
from probe.cli.commands.json_print import _FIELDS_OPTION, _print_json, _select_fields
from probe.cli.commands.refs import _project_id, slug_ref


# -- papers (0152) -----------------------------------------------------------
paper_app = typer.Typer(
    no_args_is_help=True,
    help=(
        "The literature a research project was built from: what each paper "
        "says, the repo read alongside it, and where the two disagree. "
        "Record DURING a review and again at its end."
    ),
)

#: `probe paper --help` order (papers, citations and find register them).
PAPER_GROUP = register_group(
    paper_app,
    ("add", "edges", "list", "update", "tag", "remove", "citations", "graph", "find"),
)


@paper_app.command("add")
def paper_add(
    project_id: str = slug_ref("project"),
    title: str = typer.Argument(..., help="the paper's title"),
    authors: str = typer.Option(None, "--authors", help='free text, e.g. "Vaswani et al."'),
    source: str = typer.Option(
        ...,
        "--source",
        "--url",
        help="paper URL or local file path (--url remains an alias)",
    ),
    repo: str = typer.Option(None, "--repo", help="the repository read alongside it"),
    summary: str = typer.Option(
        None, "--summary", help="the paper's main idea, in your words (@file.md works)"
    ),
    discrepancies: str = typer.Option(
        None,
        "--discrepancies",
        help="what the repo does that the paper does not say (@file.md works)",
    ),
    tag: list[str] = typer.Option(None, "--tag", help="concept tag (repeatable)"),
    via: str = typer.Option(
        None,
        "--via",
        help=(
            "how you got here: the paper id you followed, or 'none' if you came "
            "to this one directly. Omit only if you genuinely cannot say."
        ),
    ),
    via_provenance: str = typer.Option(
        None,
        "--via-provenance",
        help=(
            "required with --via <id>: observed_call | provider_citation (you found "
            "it in a reference list) | human | inferred"
        ),
    ),
    via_reason: str = typer.Option(
        None, "--via-reason", help="one sentence on why that paper led to this one"
    ),
    relates_to: str = typer.Option(
        None,
        "--relates-to",
        help=(
            "the earlier paper in this project this one connects to (its id), chosen by "
            "what the papers say, never the paper added last; 'none' for the first paper"
        ),
    ),
    relates_reason: str = typer.Option(
        None,
        "--relates-reason",
        help="required with --relates-to <id>: one or two sentences on how the two papers relate",
    ),
    relates_provenance: str = typer.Option(
        "inferred",
        "--relates-provenance",
        help=(
            "how the link is known: inferred (your judgment, the default) | human "
            "(someone said so) | observed_call | provider_citation"
        ),
    ),
) -> None:
    """Record one paper against a project.

    The authored title and source are required; `paper update` amends the rest
    later. Provider metadata is captured separately and never rewrites either
    the title or the reviewer's summary.
    --discrepancies is what nothing else captures: censored code, a missing
    ablation, a hyperparameter the repo contradicts.

    --tag is the CONCEPTS this paper is about, in your vocabulary — the axis a
    forty-paper review is grouped on, and the judgement only the reader can
    make. Separate from the provider's own categories, which arrive by
    themselves. Repeat the flag per tag; `paper tag` amends them later.

    NO DEDUPE — two adds of one URL make two rows, so `paper list` first.
    Adding counts as activity on the project; editing and removing do not.

    --via RECORDS THE CHAIN, and it has three answers, not two.
    `--via <paper id>` says you followed that paper to this one.
    `--via none` says you came to this one directly — a bare search, or someone
    handed you the link. OMITTING IT ENTIRELY says you cannot tell, which is a
    different and weaker answer that renders differently.

    Never pass the paper you happened to add last. Read order is not derivation,
    and a chain that quietly encodes it is worse than no chain.

    `--via-provenance provider_citation` means you FOUND this paper in a
    reference list (the parent's, or a provider's list of who cites it). Like
    every --via it records your path through the literature, not the
    literature itself: whether one paper's bibliography names another is a
    `cites` link, which the server reads from the bibliographies on its own
    (`probe paper citations`, `probe paper graph`).

    --relates-to is the earlier paper in this project the new one connects to,
    with --relates-reason saying how the two relate; `none` for the project's
    first paper. `paper edges` lists the links already made.
    """
    relation = None
    if relates_to is not None:
        if relates_to.strip().lower() == "none":
            relation = {"paper": None}
        else:
            # Checked here so the failure names the flag; the server refuses a
            # link without a reason too.
            if not (relates_reason or "").strip():
                raise typer.BadParameter(
                    "--relates-to <id> needs --relates-reason: one or two sentences on "
                    "how the two papers relate.",
                    param_hint="--relates-reason",
                )
            relation = {
                "paper": relates_to,
                "reason": relates_reason,
                "provenance": relates_provenance,
            }
    elif relates_reason:
        raise typer.BadParameter(
            "--relates-reason goes with --relates-to <paper id>: name the paper it describes.",
            param_hint="--relates-reason",
        )
    lineage = None
    if via is not None:
        if via.strip().lower() == "none":
            lineage = {"via": None}
        else:
            # Checked here so the failure names the flag the user typed. The
            # server refuses it too -- this is the friendlier copy of the same
            # rule, never the only one.
            if not via_provenance:
                raise typer.BadParameter(
                    "--via <id> needs --via-provenance: an edge you watched a tool "
                    "make and one a model guessed are different claims, and the "
                    "reader has to be able to tell them apart. Use one of: "
                    "observed_call, provider_citation, human, inferred.",
                    param_hint="--via-provenance",
                )
            lineage = {"via": via, "provenance": via_provenance}
            if via_reason:
                lineage["reason"] = via_reason
    with _client() as c:
        created = c.add_paper(
            _project_id(c, project_id),
            title=title,
            source_url=source,
            authors=authors,
            repo_url=repo,
            summary_md=_text_value(summary),
            discrepancies_md=_text_value(discrepancies),
            tags=list(tag) if tag else None,
            lineage=lineage,
            relates_to=relation,
        )
    _print_json(created)


@paper_app.command("edges")
def paper_edges(
    project_id: str = slug_ref("project"),
) -> None:
    """The recorded links among one project's papers: which paper led to which
    (`discovered_via`) and how each relates to an earlier one (`relates_to`,
    with its reason).

    Read it before adding a paper: the ids `--via` and `--relates-to` take are
    here.
    """
    with _client() as c:
        result = c.paper_edges(_project_id(c, project_id))
    _print_json(result)


@paper_app.command("list")
def paper_list(
    project_id: str = slug_ref("project"),
    limit: int = typer.Option(20, "--limit", help="page size (max 50)"),
    tag: list[str] = typer.Option(None, "--tag", help="filter: paper must carry ALL (repeatable)"),
    fields: str = _FIELDS_OPTION,
) -> None:
    """A project's papers, newest first; --tag narrows to a concept."""
    with _client() as c:
        page = c.list_papers(
            _project_id(c, project_id), limit=limit, tags=list(tag) if tag else None
        )
    _print_json(_select_fields(page.items, fields))


@paper_app.command("update")
def paper_update(
    paper_id: str = typer.Argument(..., help="paper id (from `probe paper list`)"),
    title: str = typer.Option(None, "--title", help="replace the title"),
    authors: str = typer.Option(None, "--authors", help="replace the author line"),
    source: str = typer.Option(
        None,
        "--source",
        "--url",
        help="replace the paper URL or local file path (--url remains an alias)",
    ),
    repo: str = typer.Option(None, "--repo", help="replace the repository URL"),
    summary: str = typer.Option(None, "--summary", help="replace the summary (@file.md works)"),
    discrepancies: str = typer.Option(
        None, "--discrepancies", help="replace the discrepancies (@file.md works)"
    ),
    tag: list[str] = typer.Option(
        None, "--tag", help="REPLACE the whole tag list (repeatable); `paper tag` amends"
    ),
) -> None:
    """Amend a recorded paper. Omitted fields are untouched; `""` clears any
    except --title and --source, which are required (an empty one is a 422).

    --tag here REPLACES the whole list, like every other `update` verb. Use
    `probe paper tag` to add or drop one tag without restating the rest."""
    with _client() as c:
        updated = c.update_paper(
            paper_id,
            title=title,
            authors=authors,
            source_url=source,
            repo_url=repo,
            summary_md=_text_value(summary),
            discrepancies_md=_text_value(discrepancies),
            tags=list(tag) if tag else None,
        )
    _print_json(updated)


@paper_app.command("tag")
def paper_tag(
    paper_id: str = typer.Argument(..., help="paper id (from `probe paper list`)"),
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
    """Tag a paper with CONCEPTS: positional args add, --remove drops, --set replaces.

    A bare invocation lists what the paper already carries. This is what makes a
    long reading list groupable — "which of these forty are about retrieval" —
    and it is the one label the reader supplies that the provider cannot: the
    paper's own `extracted_categories` are arXiv's taxonomy, not this lab's.

    Papers take NO author tag. The byline is already the paper's `authors`, and
    whoever recorded it is credited on the project.
    """
    with _client() as c:
        _print_json(
            _tag_verb_flow(
                paper_id,
                c.get_paper(paper_id).get("tags"),
                add,
                remove,
                replace,
                lambda wanted: c.update_paper(paper_id, tags=wanted),
            )
        )


@paper_app.command("remove")
def paper_remove(
    paper_id: str = typer.Argument(..., help="paper id (from `probe paper list`)"),
) -> None:
    """Remove a recorded paper."""
    with _client() as c:
        c.remove_paper(paper_id)
    print("removed")
from probe.cli.commands.flag_values import _text_value  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.tags import _tag_verb_flow  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
