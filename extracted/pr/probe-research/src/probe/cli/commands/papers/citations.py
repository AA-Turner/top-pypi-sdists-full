"""probe paper citations / graph: one paper's citation links and a project's citation graph as terminal tables."""

from __future__ import annotations
import re
from typing import Any

import typer
# The option enums only, from `_generated.enums` rather than `probe.models`: that
# seam builds every wire model, ~0.5 s that every command paid at startup -- the
# wizard, the hooks and the status line included -- whether or not it sent one.
# `tests/test_cli_startup_imports.py` holds the CLI to this.
from ....generated.enums import AppPapersCitationStoreDirection as CitationDirection
from .. import ref_syntax as refs
from ....shared.reads import reads
from probe.cli.commands.papers.papers import paper_app


#: C1 controls + bidi overrides: the display-manipulation characters JSON
#: leaves raw under ensure_ascii=False. They only ever occur inside string
#: values (JSON structure is ASCII), so re-escaping them keeps the output
#: valid JSON byte-for-byte parse-equivalent.
_DISPLAY_CONTROLS = reads.DISPLAY_CONTROLS


# -- citation links (citation graph, Track C) ---------------------------------
#
# Two READS of what the server already holds: no provider is called. Both print
# a table by default and the server's response with --json.

#: Every display-control character a third-party title or bibliography entry
#: could carry: `_DISPLAY_CONTROLS` (C1 and the bidi embeddings, overrides and
#: isolates `_print_json` escapes), plus C0 and DEL, plus the three bidi MARKS
#: (LRM U+200E, RLM U+200F, ALM U+061C), which reorder a line as surely as an
#: override. Built from the shared class so the two cannot drift. A table cell
#: is one line, so they are removed rather than escaped.
_CITE_CONTROLS = re.compile(
    "[\x00-\x1f\x7f\u200e\u200f\u061c" + _DISPLAY_CONTROLS.pattern[1:-1] + "]"
)

#: Only a server from before the per-tenant citation flag was removed (task
#: C13) answers `state: disabled`; a current one serves every team. Kept so a
#: CLI pointed at such a server says so plainly instead of an empty table.
_CITATIONS_DISABLED = (
    "citation links are not switched on for your team (state: disabled); "
    "nothing has been read for these papers"
)


def _cite_cell(value: Any, width: int | None = None) -> str:
    """One table cell: one line, display controls removed, cut to `width`."""
    if value is None or value == "":
        return "-"
    text = _CITE_CONTROLS.sub("", " ".join(str(value).split()))
    if width is not None and len(text) > width:
        text = text[: width - 1] + "…"
    return text


def _cite_table(headers: list[str], rows: list[list[str]], indent: str = "  ") -> None:
    """Left-aligned columns padded to their widest cell; the last one ragged."""
    widths = [max([len(h)] + [len(r[i]) for r in rows]) for i, h in enumerate(headers)]
    for line in [headers, *rows]:
        cells = [cell.ljust(widths[i]) for i, cell in enumerate(line[:-1])]
        print(indent + "  ".join([*cells, line[-1]]).rstrip())


def _cite_when(value: Any) -> str:
    return str(value)[:10] if value else "never"


def _cite_titled(title: Any, year: Any, width: int = 70) -> str:
    return _cite_cell(f"{title} ({year})" if title and year else title, width)


def _cite_sync_lines(sync: dict | None) -> list[str]:
    """The two fetch statuses of one paper, with their counts."""
    if not sync:
        return ["references: pending · citers: pending (nothing fetched yet)"]
    refs = (
        f"references: {sync.get('references')} · "
        f"{sync.get('references_total') or 0} entries, "
        f"{sync.get('references_linked') or 0} linked · "
        f"fetched {_cite_when(sync.get('references_fetched_at'))}"
    )
    citers = (
        f"citers: {sync.get('citers')} · {sync.get('citers_nominated') or 0} nominated, "
        f"{sync.get('citers_proven') or 0} proven, {sync.get('citers_unchecked') or 0} unchecked"
    )
    if sync.get("citers_not_reconfirmed"):
        citers += f", {sync['citers_not_reconfirmed']} not reconfirmed"
    if sync.get("citers_capped"):
        citers += f", {sync['citers_capped']} dropped at the cap"
    citers += f" · fetched {_cite_when(sync.get('citers_fetched_at'))}"
    lines = [refs, citers]
    if sync.get("stale"):
        lines.append("stale: the paper's ids changed since the last fetch; a refetch is due")
    return lines


def _print_paper_citations(out: dict) -> None:
    state = out.get("state")
    if state == "disabled":
        print(_CITATIONS_DISABLED)
        return
    print(f"paper {out.get('paper_id')} · state: {state}")
    keys = _cite_cell(", ".join(out.get("keys") or []))
    print(f"keys: {'none (no id to read a bibliography for)' if keys == '-' else keys}")
    for line in _cite_sync_lines(out.get("sync")):
        print(line)
    lists = out.get("reference_lists") or []
    if lists:
        print("bibliographies read:")
        _cite_table(
            ["SOURCE", "OWNER", "STATUS", "ENTRIES", "LINKED", "URL"],
            [
                [
                    _cite_cell(item.get("source")),
                    _cite_cell(item.get("owner_key")),
                    _cite_cell(item.get("status")),
                    _cite_cell(item.get("total")),
                    _cite_cell(item.get("linked")),
                    _cite_cell(item.get("url")),
                ]
                for item in lists
            ],
        )
    links = out.get("links") or []
    if not links:
        print("no citation links stored for this paper")
        return
    print()
    rows = []
    for link in links:
        text = _cite_titled(link.get("title"), link.get("year")) if link.get("title") else None
        if text is None:
            text = _cite_cell(link.get("raw_reference"), 70)
        reason = (link.get("detail") or {}).get("reason")
        if link.get("resolution") == "unresolved" and reason:
            text = f"{text} [{_cite_cell(reason)}]"
        rows.append(
            [
                _cite_cell(link.get("direction")),
                _cite_cell(link.get("resolution")),
                _cite_cell(link.get("work_key"), 40),
                _cite_cell(link.get("ordinal")),
                text,
            ]
        )
    _cite_table(["DIRECTION", "PROOF", "WORK", "ENTRY", "TITLE OR ENTRY TEXT"], rows, indent="")
    if out.get("truncated"):
        print(f"truncated: showing {len(links)} rows; raise --limit (max 2000) for the rest")


def _print_citation_graph(out: dict) -> None:
    state = out.get("state")
    if state == "disabled":
        print(_CITATIONS_DISABLED)
        return
    nodes = out.get("nodes") or []
    edges = out.get("edges") or []
    done = out.get("completeness") or {}
    primaries = [n for n in nodes if n.get("kind") == "primary"]
    works = [n for n in nodes if n.get("kind") == "suggested"]
    # Short labels, so an edge reads `P1 cites W3` instead of two uuids.
    label = {n["id"]: f"P{i}" for i, n in enumerate(primaries, 1)}
    label.update({n["id"]: f"W{i}" for i, n in enumerate(works, 1)})
    print(f"project {out.get('project_id')} · state: {state}")
    print(
        f"{done.get('primaries_returned', len(primaries))} of "
        f"{done.get('primaries_total', len(primaries))} papers "
        f"({done.get('primaries_without_id', 0)} without an id, "
        f"{done.get('primaries_pending', 0)} pending) · "
        f"{done.get('suggested_returned', len(works))} of "
        f"{done.get('suggested_candidates', len(works))} suggested works · {len(edges)} edges"
    )
    print(
        f"not linked: {done.get('unresolved_references', 0)} bibliography entries printed no id"
        f" · {done.get('unchecked_citers', 0)} citers unchecked"
        f" · {done.get('not_reconfirmed_citers', 0)} citers not reconfirmed"
    )
    if done.get("truncated"):
        print("truncated: the project has more papers or link rows than one graph reads")
    if not primaries:
        print("no papers in this project")
        return
    print("\nPAPERS")
    rows = []
    for node in primaries:
        sync = node.get("sync") or {}
        stale = " (stale)" if sync.get("stale") else ""
        rows.append(
            [
                label[node["id"]],
                f"{sync.get('references', 'pending')} "
                f"{sync.get('references_linked') or 0}/{sync.get('references_total') or 0}{stale}",
                f"{sync.get('citers', 'pending')} "
                f"{sync.get('citers_proven') or 0}/{sync.get('citers_nominated') or 0}",
                _cite_cell(", ".join(node.get("keys") or []), 40),
                _cite_cell(node.get("paper_id")),
                _cite_titled(node.get("title"), node.get("year"), 60),
            ]
        )
    _cite_table(
        ["#", "REFS LINKED/TOTAL", "CITERS PROVEN/NOMINATED", "KEYS", "PAPER ID", "TITLE"], rows
    )
    if works:
        print("\nSUGGESTED WORKS (ranked by how many of these papers link to each)")
        _cite_table(
            ["#", "LINKS", "CITED BY", "KEY", "TITLE"],
            [
                [
                    label[node["id"]],
                    _cite_cell(node.get("linked_primaries")),
                    _cite_cell(node.get("cited_by_count")),
                    _cite_cell(", ".join(node.get("keys") or []), 40),
                    _cite_titled(node.get("title"), node.get("year"), 60),
                ]
                for node in works
            ],
        )
    if edges:
        print("\nEDGES")
        rows = []
        for edge in edges:
            if edge.get("relation") == "cites":
                evidence = edge.get("evidence") or []
                first = evidence[0] if evidence else {}
                proof = (
                    f"{first.get('direction')} · {first.get('list_source')} "
                    f"#{first.get('ordinal')} · {first.get('resolution')}"
                    if first
                    else "-"
                )
                if len(evidence) > 1:
                    proof += f" (+{len(evidence) - 1} more)"
            else:
                proof = _cite_cell(
                    f"{edge.get('provenance')}: {edge.get('reason')}"
                    if edge.get("reason")
                    else edge.get("provenance"),
                    70,
                )
            rows.append(
                [
                    label.get(edge.get("source"), _cite_cell(edge.get("source"))),
                    _cite_cell(edge.get("relation")),
                    label.get(edge.get("target"), _cite_cell(edge.get("target"))),
                    proof,
                ]
            )
        _cite_table(["SOURCE", "RELATION", "TARGET", "PROOF"], rows)
    unresolved = [(n, n.get("unresolved_references") or []) for n in primaries]
    if any(entries for _, entries in unresolved):
        print("\nUNRESOLVED ENTRIES (no id printed; never an edge)")
        _cite_table(
            ["PAPER", "LIST", "ENTRY", "TEXT"],
            [
                [
                    label[node["id"]],
                    _cite_cell(entry.get("list_owner_key")),
                    _cite_cell(entry.get("ordinal")),
                    _cite_cell(entry.get("raw_reference"), 90),
                ]
                for node, entries in unresolved
                for entry in entries
            ],
        )


@paper_app.command("citations")
def paper_citations(
    paper_id: str = typer.Argument(..., help="paper id (from `probe paper list`)"),
    direction: CitationDirection = typer.Option(
        None,
        "--direction",
        help="reference: what this paper cites; citer: who cites it. Both when omitted.",
    ),
    include_unresolved: bool = typer.Option(
        True,
        "--include-unresolved/--no-include-unresolved",
        help="bibliography entries that printed no id (kept as text, never an edge)",
    ),
    limit: int = typer.Option(
        None, "--limit", min=1, max=2000, help="at most this many rows (server default 500)"
    ),
    as_json: bool = typer.Option(False, "--json", help="print the server's response as JSON"),
) -> None:
    """One paper's citation links, each with the bibliography entry that proves it.

    A `cites` link is a fact about the literature: this paper's reference list
    names that work (`reference`), or that work's list names this paper
    (`citer`). PROOF says how it is known -- `printed_id` (the id is printed in
    the entry), `publisher_id` (the publisher deposited it) or `unresolved` (no
    id: kept as text, never an edge). Nothing is ever linked by a title match.

    Not the same thing as `--via` on `paper add`, which records how YOU got to a
    paper. Read-only: the server fetches bibliographies on its own after a paper
    is recorded.
    """
    with _client() as c:
        out = c.paper_citations(
            paper_id,
            direction=direction.value if direction is not None else None,
            include_unresolved=include_unresolved,
            limit=limit,
        )
    if as_json:
        _print_json(out)
        return
    _print_paper_citations(out)


@paper_app.command("graph")
def paper_graph(
    project: str = typer.Option(
        None,
        "--project",
        help="project slug (or id:<uuid>); defaults to the active one (`probe project use`)",
    ),
    suggested: int = typer.Option(
        None,
        "--suggested",
        min=0,
        max=200,
        help="how many suggested works, ranked by linking papers (server default 50; 0 for none)",
    ),
    direction: CitationDirection = typer.Option(
        None,
        "--direction",
        help="reference: what the papers cite; citer: who cites them. Both when omitted.",
    ),
    min_links: int = typer.Option(
        None,
        "--min-links",
        min=1,
        help="a suggested work needs at least this many of the project's papers linking to it",
    ),
    include_discovery: bool = typer.Option(
        False,
        "--include-discovery",
        help=(
            "also show the recorded discovered_via and relates_to links among the papers "
            "(how you got to each, and how each relates to an earlier one)"
        ),
    ),
    include_unresolved: bool = typer.Option(
        False,
        "--include-unresolved",
        help="also list each paper's bibliography entries that printed no id",
    ),
    as_json: bool = typer.Option(False, "--json", help="print the server's response as JSON"),
) -> None:
    """A project's citation graph: its papers, the works they cite or are cited
    by, and the `cites` edges among them.

    SUGGESTED WORKS are works the project has not recorded that its papers link
    to, ranked by how many of THIS project's papers do, then by citation count,
    and capped (never padded). Every `cites` edge carries the bibliography entry
    that proves it: an id printed in the entry or deposited by the publisher,
    never a title match or a provider's guess. To record a suggested work, use
    `probe paper add` with its URL.

    `discovered_via` and `relates_to` links (with --include-discovery) are the
    recorded ones, shown as stored and never as `cites`. Read-only: nothing here
    calls a provider.
    """
    resolved = _ambient_project(project)
    if resolved is None:
        raise typer.BadParameter(
            "no project: pass --project, or set one with `probe project use`",
            param_hint="--project",
        )
    with _client() as c:
        out = c.citation_graph(
            _project_id(c, resolved),
            suggested=suggested,
            directions=[direction.value] if direction is not None else None,
            min_links=min_links,
            include_discovery=include_discovery or None,
            include_unresolved=include_unresolved or None,
        )
    if as_json:
        _print_json(out)
        return
    _print_citation_graph(out)
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.refs import _ambient_project, _project_id  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.runs.runs import link  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
