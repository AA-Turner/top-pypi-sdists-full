"""Two renderings of one release summary: prose with its evidence, or a table.

**The ticket leads, and every line carries the same five things.** A release
summary answers "what changed, who did it, which pull requests carried it, and
did it land" -- and it answered them in four different places, so a reader had
to hold a ticket reference in their head while scrolling between sections to
assemble one row. Here each line is whole:

    ▸ Lumen now answers policy questions correctly — the assistant can see
      which jurisdiction a building falls under.
      BPAI-402 · Alex Y. · auditagent#124, bps-api#603 · partly merged

Prose, then reference, people, pull requests, verdict. The same five fields are
the table's five columns; `--table` picks that view. Neither is a summary of the
other -- they are the same rows, and which one reads better depends on whether
you are catching up (prose) or checking coverage (table).

**Only the prose has no other source.** The reference, the people, the pull
requests and the verdict are all derived by `ReleaseContentService` and can be
re-derived at any time. The sentence saying what a change meant to somebody
using the product is written by a Claude session and stored on `summary_items`;
where none has been written, these views fall back to the ticket's own title,
which says what the work *was* and never what it did for anyone.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from rich.markup import escape
from rich.table import Table

from src.services import summary_line

#: Re-exported so `releases summarize` and the tests keep one import path.
#:
#: **The vocabulary moved to `src/services/summary_line.py`** and the direction of
#: the import went with it. It used to live here and be imported *by* the shape
#: module -- a service reaching into `src/cli` for the words a verdict is spelled
#: with, which is backwards, and which meant the words could not be used anywhere
#: outside the CLI without dragging Rich along.
verdict_label = summary_line.verdict_label


def pr_refs(prs: List[Dict[str, Any]]) -> str:
    """`bps-api#587, bps-ui-v2#226`, with the unmerged ones marked.

    Repository and number, never the title: the title is the pull request's own
    account of itself, and the line above already says what the change did.

    **The labelling is `summary_line.pr_label`'s**, not a second copy of it. This
    function used to build the reference itself, and the copy had drifted twice
    over: it rendered `repo#None` for a pull request whose number lives only in
    its URL, and it marked *unknown* merge state as `(open)` -- an assertion
    rather than a reading, on the field the release line calls the most important
    thing on it.
    """
    labels = [summary_line.pr_label(pr) for pr in (prs or [])]
    return ", ".join(label for label in labels if label)


def people_list(people: Any) -> List[str]:
    """The credited names, in order, however the payload spells a person.

    Separate from `people_names` because `summary_line.provenance` joins the
    fields of a line itself: handing it a pre-joined string would nest one
    separator inside another, which is the reason the provenance line uses `·`
    between fields and `,` between people rather than commas throughout.
    """
    names: List[str] = []
    for person in people or []:
        if isinstance(person, dict):
            name = person.get("name") or person.get("handle") or person.get("login")
        else:
            name = person
        if name:
            names.append(str(name))
    return names


def people_names(people: Any) -> str:
    """`Alex Y., Ken S.` -- however the payload spells a person.

    `people` entries are already resolved names where InnoDay knows the person
    and a raw handle where it does not. Both print as given: inventing a name
    for an unmapped handle is worse than showing the handle.
    """
    return ", ".join(people_list(people))


def line_prose(item: Dict[str, Any]) -> str:
    """The narrator's sentence, or the ticket's title when nobody has written one."""
    return str(item.get("narrative") or item.get("title") or "").strip()


def _evidence(item: Dict[str, Any], *, icon: bool) -> str:
    """`BPAI-402 · Alex Y. · auditagent#124 · partly merged`, minus what is absent.

    **Assembled by `summary_line.provenance`, which is also what a stand-up line
    goes through.** It used to be assembled here, and the two implementations of
    "the same line" then disagreed about the two things they were most likely to:
    which separator went where, and what an absent field left behind. A stand-up
    and a release note are the same line -- they differ in scope, not in shape --
    so there is one function that builds it.

    Escaped once, at the end. Escaping each field and then joining is the same
    thing until a name contains a bracket, at which point it is not.
    """
    return escape(
        summary_line.provenance(
            ticket_ref=str(item.get("ref") or "") or None,
            people=people_list(item.get("people")),
            prs=item.get("prs") or [],
            verdict=item.get("state"),
            icon=icon,
        )
    )


def prose_lines(items: List[Dict[str, Any]], *, icon: bool = True) -> List[str]:
    """The reading view: one bullet per ticket, its evidence underneath."""
    out: List[str] = []
    for item in items:
        # Bold, like the stand-up's -- the prose is the one field a person wrote
        # and the one a reader is meant to land on first. It was plain here and
        # bold there, which is the sort of difference that reads as two systems
        # even once the fields have been made identical.
        out.append(f"▸ [bold]{escape(line_prose(item))}[/bold]")
        out.append(f"  [dim]{_evidence(item, icon=icon)}[/dim]")
        out.append("")
    return out


def summary_table(items: List[Dict[str, Any]]) -> Table:
    """The checking view: the same five fields as columns.

    `no_wrap` on the reference and the verdict, because those are the two a
    reader scans down -- letting them wrap turns the column into prose and the
    scan into reading.
    """
    table = Table(show_lines=False, header_style="bold")
    table.add_column("Ticket", no_wrap=True)
    table.add_column("Human summary")
    table.add_column("People")
    table.add_column("PRs")
    table.add_column("Verdict", no_wrap=True)
    for item in items:
        table.add_row(
            str(item.get("ref") or ""),
            line_prose(item),
            people_names(item.get("people")),
            pr_refs(item.get("prs")),
            verdict_label(item.get("state")),
        )
    return table


def header_lines(payload: Dict[str, Any], project_label: str) -> List[str]:
    """Which release, whether it shipped, how much of it is still moving.

    None of this is derivable from the tickets below it, and a reader who has to
    run `releases list` beside a release summary to find out whether the release
    has gone out is being handed half an answer.
    """
    record = payload.get("release_record") or {}
    version = record.get("version") or payload.get("release") or "the release in flight"
    window = payload.get("window") or {}
    out = [
        f"[bold]{escape(project_label)} {escape(str(version))}[/bold] — release summary",
        "",
    ]

    def row(label: str, value: str) -> None:
        if value:
            out.append(f"  [dim]{label:<11}[/dim] {escape(value)}")

    row("Status", str(record.get("status") or ""))
    row("Released", str(record.get("released_at") or "")[:10])
    total, still_open = record.get("tickets"), record.get("open")
    if total is not None:
        row("Tickets", f"{total} total, {still_open} open")
    commits = payload.get("commit_count")
    window_text = str(window.get("label") or "")
    if commits:
        window_text = f"{window_text} · {commits} commits".strip(" ·")
    row("Window", window_text)
    out.append("")
    return out


def unnarrated_notice(items: List[Dict[str, Any]]) -> Optional[str]:
    """One line when some tickets are showing their title instead of prose.

    Said rather than left to be noticed: a title reads like a summary, so a
    release nobody has narrated looks narrated and terse rather than unwritten.
    """
    missing = sum(1 for i in items if not (i.get("narrative") or "").strip())
    if not missing:
        return None
    noun = "ticket" if missing == 1 else "tickets"
    return (
        f"{missing} {noun} showing the ticket title — no summary has been "
        "written for them. Run /innoday:summary release to narrate this release."
    )
