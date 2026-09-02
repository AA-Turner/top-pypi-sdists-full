"""`innoday summary` -- what happened, for you, since you last looked (PF-398).

**One command, and the common case takes no flags.** `innoday summary` is you,
over the last three days. `--scrum` widens it to the whole team and starts
showing who owns what. Everything else is a default worth overriding rarely.

**Assembly is server-side; narration is not.** This command calls
``GET .../projects/{p}/summary-data`` -- the engine -- and renders the
structured result it hands back, plus whatever prose is already cached against
that window. It never writes prose, because a bare CLI invocation has no Claude
session attached to write any; that is what `/innoday:summary` is for. Same
split `innoday board summarize` already documents (see
`src/cli/commands/boards.py`), and the same reason.

What the layout is trying to say, in order:

* **Active** -- work that actually moved in the window, newest first, capped by
  the engine at `ACTIVE_CAP`. The footer says how many were left out.
* **No work detected** -- assigned, open, and nothing happened. An explicit
  "nothing", not an omission, and it never consumes one of the active slots.
* **Unassigned -- work happening** -- the board named nobody but commits landed,
  so the code's author is shown instead, marked as such.
* **Up next** -- what the board says is queued for you. Personal mode only:
  authorship records what someone did and cannot predict what they have lined
  up, so the team view has nothing honest to put here.

``--window release`` is not a window at all: it scopes the summary to one
release, so tickets on any other release -- and tickets on none, which is most of
them -- are not in it. Every label describing an *absence* then names the
release, and the summary states that boundary once at the top, because a slice
reported without one is a subset presented as the whole.

An unmapped assignee renders as ``@Name (unmapped)`` rather than being dropped:
the board named a real person, and hiding that would make a summary look empty
when it is really unmapped. If the *caller* is the one who is unmapped, the
command stops with the fix rather than an empty result -- an empty personal
summary and "InnoDay does not know which board handle is you" look identical
from the outside, and only one of them is actionable.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from rich.console import Console
from rich.markup import escape

from src.cli.client import APIError, InnoDayAPIClient
from src.cli.utils.formatters import (
    ProgressReporter,
    enum_key,
    format_error,
    format_warning,
)
from src.cli.utils.project_context import load_project_context
from src.services import summary_line
from src.services.ticket_release import CURRENT_RELEASE
from src.utils.time_windows import (
    WINDOW_GRAMMAR_HINT,
    format_note_date,
    normalize_window,
)

console = Console()


class SummaryWindow(str, Enum):
    """The *named* windows `--window` accepts, beyond the duration grammar.

    This is no longer the whole vocabulary and is deliberately not an argparse
    `choices` list any more. A fixed list here meant `--window 2w` was rejected
    while the engine accepted it happily, and `--window day` was accepted here
    while the engine answered 422 -- one concept, two vocabularies, disagreeing
    in both directions. `--window` now takes the shared grammar
    (`src/utils/time_windows.py`), of which `day`/`week` are aliases; `release`
    is the only member that is not a duration at all.
    """

    DAY = "day"
    WEEK = "week"
    RELEASE = "release"


# What `--window release` asks the engine to scope to is the server's sentinel,
# `src/services/ticket_release.py`'s CURRENT_RELEASE -- **imported**, not
# re-declared. The CLI never has to know which version is current: it used to work
# that out here, from `max(released_at)` over the project's releases, and that was
# the whole of the bug -- a *day count* came back, the release's identity was
# thrown away before the engine saw it, and nothing downstream could filter by it.
# This file also carried its own `CURRENT_RELEASE = "current"` afterwards, which is
# the same divergence one step smaller: two literals that must stay equal with
# nothing pinning them, while `src/cli/commands/tickets.py` imported the real one.

DEFAULT_WINDOW = "3d"


def release_to_scope(
    version: Any,
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """`--release`'s value → the same `(window_spec, release, note)` a window gives.

    One function for three callers -- `--release`, `--window release`, and
    `innoday releases summarize` -- because the note is the part that gets
    forgotten. It is the line that states the boundary, and a release summary
    printed without it is a slice presented as the whole project.

    `True` (the bare flag) means the release being cut, and stays the server's
    `CURRENT_RELEASE` sentinel rather than a version resolved here: the CLI
    working out which release is current, from its own rule, is the bug #563
    removed. An explicit version is passed through untouched -- the engine keys
    the summary on it, so normalising case or prefix here would mint a second
    cache key for one release.
    """
    if version is True or version is None:
        return (
            None,
            CURRENT_RELEASE,
            "Scoped to this project's current release — tickets on no "
            "release are not included.",
        )
    return (
        None,
        str(version),
        f"Scoped to release {version} — tickets on any other release, and "
        "tickets on no release, are not included.",
    )


def parse_window_arg(value: str) -> str:
    """argparse `type=` for `--window`: an alias, a duration, or `release`.

    Returns the value in the vocabulary `window_to_scope` expects rather than
    resolving it here -- `release` is a scope rather than a duration, so this
    stage can only say "that is a window I recognise".
    """
    candidate = str(value or "").strip().lower()
    if candidate == SummaryWindow.RELEASE.value:
        return candidate
    try:
        canonical = normalize_window(candidate)
    except ValueError as exc:  # parses, covers less than one unit
        raise argparse.ArgumentTypeError(str(exc))
    if canonical is None:
        raise argparse.ArgumentTypeError(
            f"invalid window {value!r}: expected {WINDOW_GRAMMAR_HINT}, "
            f"or '{SummaryWindow.RELEASE.value}'"
        )
    return canonical


#: Status → glyph. Keyed by `enum_key`, because the same status arrives as
#: `"in review"` from the API and `"IN_REVIEW"` from the database.
STATUS_ICONS: Dict[str, str] = {
    "DRAFT": "⚪",
    "BACKLOG": "⚪",
    "TODO": "⚪",
    "IN_PROGRESS": "🔵",
    "IN_REVIEW": "🟢",
    "DONE": "✅",
    "CANCELLED": "⛔",
}


# ------------------------------------------------------------------ rendering


def _status_label(status: Optional[str]) -> str:
    if not status:
        return ""
    key = enum_key(status)
    icon = STATUS_ICONS.get(key, "•")
    return f"{icon} {key.replace('_', ' ').title()}"


def _owner_label(line: Dict[str, Any], scrum: bool) -> str:
    """`@who`, or nothing at all in personal mode.

    Personal mode is already scoped to one person, so repeating their name on
    every row is noise. The one exception the server bakes in -- an unmapped
    assignee -- keeps the server's own decoration (`owner_label`) rather than
    being re-derived here, so the two can't drift.
    """
    if not scrum:
        return ""
    if line.get("assignee_unmapped") and line.get("assignee_display"):
        return str(line.get("owner_label") or f"@{line['assignee_display']} (unmapped)")
    display = line.get("assignee_display")
    if not display:
        return ""
    if line.get("attribution") == "code":
        return f"@{display} (from commits)"
    return f"@{display}"


def _ticket_title(line: Dict[str, Any], *, plain: bool = False) -> str:
    """The ticket's own name.

    `plain=True` skips the Rich escaping, for callers that put the result through
    `summary_line` and escape the whole line once at the end -- escaping twice
    turns a literal bracket in a ticket title into markup a second time.

    The ref is no longer glued to the front for those callers: it has its own slot
    in the provenance line now, and printing it in both places was the old layout
    showing through the new one.
    """
    summary = line.get("summary") or ""
    if plain:
        return str(summary or line.get("ticket_ref") or "")
    ref = line.get("ticket_ref") or ""
    if ref and summary:
        return f"{escape(ref)} — {escape(summary)}"
    return escape(ref or summary or "(untitled)")


def _when(value: Optional[str]) -> str:
    """`2026-08-05T09:40:00+00:00` → `Aug 5, 09:40`. Never raises on junk."""
    if not value:
        return ""
    try:
        moment = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return ""
    return f"{moment:%b} {moment.day}, {moment:%H:%M}"


def _pr_label(line: Dict[str, Any]) -> str:
    """`→ PR #412 (open)`.

    Only what the engine actually knows: a URL and a state. No approval count
    and no title -- `SummaryLine` carries neither, and inventing them here
    would put fiction in a status report.
    """
    url = line.get("pr_url")
    if not url:
        return ""
    number = str(url).rstrip("/").rsplit("/", 1)[-1]
    label = f"PR #{number}" if number.isdigit() else escape(str(url))
    state = line.get("pr_state")
    return f"{label} ({escape(str(state))})" if state else label


def _context_line(line: Dict[str, Any], scrum: bool) -> str:
    """`Aug 5, 09:40 · innoday · PF-118-audit-retention   @karl`."""
    parts = [
        p
        for p in (
            _when(line.get("occurred_at")),
            escape(str(line["repo"])) if line.get("repo") else "",
            escape(str(line["branch"])) if line.get("branch") else "",
        )
        if p
    ]
    context = " · ".join(parts)
    owner = _owner_label(line, scrum)
    if context and owner:
        return f"{context}   {owner}"
    return context or owner


def _render_active(line: Dict[str, Any], scrum: bool) -> List[str]:
    """One line, in the shape every summary uses.

    **A stand-up line and a release note are the same line.** This used to render
    `▸ ref — title` over a status icon, a date, a branch and a separate pull
    request row, while a release note rendered prose over
    `ref · people · PRs · verdict`. Same data, two layouts, and a team reading
    both could not tell it was one system. The layout now comes from
    `src/services/summary_line.py`, which both go through.

    What scope still changes is `when`: a stand-up covers a stretch of days, so
    *when* something moved inside it is information. A release's header already
    says which release, so it is left off there.

    **The status chip came off the heading.** It was the last thing that made
    these two look like different systems: a stand-up read `▸ prose  🟢 In Review`
    and a release note read `▸ prose`, so the same data had a field in a place the
    other layout had nothing at all. Where a ticket stands is one slot in the
    provenance line now -- fourth, where a release puts its verdict -- and
    `_standing` is what fills it.
    """
    prose = summary_line.headline(
        line.get("body_markdown"), _ticket_title(line, plain=True)
    )
    head = f"[bold]{escape(prose)}[/bold]" if prose else ""
    tail = summary_line.provenance(
        ticket_ref=_ref_for_line(line),
        people=_people_for_line(line, scrum),
        prs=_prs_for_line(line),
        verdict=_standing(line),
        when=_when(line.get("occurred_at")) or None,
        icon=True,
    )
    out = [f"▸ {head}".rstrip()]
    if tail:
        out.append(f"  [dim]{escape(tail)}[/dim]")
    return out


def _standing(line: Dict[str, Any]) -> Optional[str]:
    """Where the thing stands: the verdict if one was judged, else the board.

    **One slot, sourced by precedence.** A verdict is what a release concluded
    about the code -- shipped, partly merged, no code -- and it exists only on a
    row some release scope has judged. A plain window's stand-up has no verdict
    and does have a board column, and "in review" answers the same question the
    reader is asking. Rendering them as two separate fields gave the stand-up a
    chip nothing else had and gave the release a slot every stand-up left empty.

    The status is passed already labelled (`🟢 In Review`), and `verdict_label`
    returns an unrecognised value unchanged -- which is what makes one slot able
    to carry either vocabulary without a second parameter deciding which.
    """
    judged = line.get("verdict") or line.get("state")
    if judged:
        return str(judged)
    return _status_label(line.get("status")) or None


def _ref_for_line(line: Dict[str, Any]) -> Optional[str]:
    ref = line.get("ticket_ref") or line.get("ref")
    return str(ref) if ref else None


def _people_for_line(line: Dict[str, Any], scrum: bool) -> List[str]:
    """Everyone credited, or nobody in personal mode.

    Personal mode is already scoped to one person, so naming them on every line
    is noise -- the same reason `_owner_label` drops the `@name` there.
    """
    if not scrum:
        return []
    people = [str(p) for p in (line.get("people") or []) if p]
    if len(people) > 1:
        return people
    # **One owner keeps its decoration.** `_owner_label` is where
    # `@Name (unmapped)` and `@Name (from commits)` come from, and neither is an
    # ornament: the first says the board named somebody InnoDay cannot identify,
    # the second says nobody was assigned at all and the name came from the
    # commits. A bare display name loses both distinctions silently.
    #
    # A credited *list* is a different thing and gets no `@`: the handle marks
    # one board-attributed owner, and `@Unurbat T., @George M.` is neither those
    # people's handles nor an owner.
    decorated = _owner_label(line, scrum)
    if decorated:
        return [decorated]
    return people


def _prs_for_line(line: Dict[str, Any]) -> List[Dict[str, Any]]:
    """The line's pull requests, however many the payload carried.

    A stand-up line carries one `pr_url` and a release line carries a list; both
    arrive here as a list so the rendered provenance cannot differ by scope.
    """
    prs = line.get("prs")
    if prs:
        return [pr for pr in prs if isinstance(pr, dict)]
    if not line.get("pr_url") and line.get("branch"):
        # **The slot holds "the code", and a branch is the code when there is no
        # pull request yet.** Somebody who has pushed a branch and not opened a
        # PR is the case where the branch name is the only thing to go on, and
        # the old layout printed it beside every PR it was redundant with.
        return [{"repo": line.get("repo"), "branch": line.get("branch")}]
    if line.get("pr_url"):
        return [
            {
                "repo": line.get("repo"),
                "number": None,
                "url": line.get("pr_url"),
                "merged": (line.get("pr_state") or "").lower() == "merged",
                "state": line.get("pr_state"),
            }
        ]
    return []


def _render_compact(line: Dict[str, Any], scrum: bool) -> str:
    """A one-line row for the idle / unassigned / up-next blocks."""
    ref = escape(str(line.get("ticket_ref") or ""))
    summary = escape(str(line.get("summary") or ""))
    owner = _owner_label(line, scrum)
    row = f"  {ref}  {summary}".rstrip()
    return f"{row}   {owner}" if owner else row


def _note_heading(updated_at: Optional[str]) -> str:
    """`── Note (9 Aug) ──`, dated when we know when it was written.

    A note outlives the summary it was attached to -- it is inherited by every
    regeneration until someone clears it -- so an undated one gives a reader no
    way to tell "still true" from "nobody has got round to deleting this".

    Same `9 Aug` order as the dashboard, deliberately: the two render the same
    field beside the same prose, and `Aug 9` here against `9 Aug` there reads as
    two different pieces of data rather than one.

    **The year appears once the note is not from this one.** Indefinite
    inheritance is exactly the case where a bare `9 Aug` is worst -- a note from
    last August is the one most likely to be acted on wrongly, and the one a
    year-less date disguises best.
    """
    if not updated_at:
        return "── Note ──"
    try:
        moment = datetime.fromisoformat(str(updated_at).replace("Z", "+00:00"))
    except ValueError:
        return "── Note ──"
    return f"── Note ({format_note_date(moment)}) ──"


def _prose_block(text: Optional[str], *, heading: Optional[str] = None) -> List[str]:
    """Escaped, indented paragraphs for a block of prose -- or nothing at all.

    Shared by the generated summary and the human note so the two cannot drift
    in how they escape or indent: they sit next to each other, and a difference
    between them would read as meaning rather than as an oversight.
    """
    if not text or not str(text).strip():
        return []
    out: List[str] = []
    if heading:
        out.append(f"  [bold]{escape(heading)}[/bold]")
    out.extend(f"  {escape(prose)}" for prose in str(text).strip().splitlines())
    out.append("")
    return out


def _release(payload: Dict[str, Any]) -> Optional[str]:
    """The release this summary is scoped to, or None for the whole project."""
    release = payload.get("release")
    return str(release) if release else None


def _scope_suffix(payload: Dict[str, Any]) -> str:
    """`` on v1.9.0``, for the labels that describe an **absence**.

    `no_work_detected` and `unassigned_idle_count` are defined by nothing having
    happened, so under a release scope they have to name the release: unlabelled,
    a quiet release reports project-wide silence on a project that is busy
    everywhere else.
    """
    release = _release(payload)
    return f" on {escape(release)}" if release else ""


def _boundary(payload: Dict[str, Any]) -> List[str]:
    """The one line a release-scoped summary owes the reader.

    Most tickets carry no release at all -- it is only set by sync from a
    `fixVersions`/label or an explicit `tickets update --release` -- so a release
    summary is a **slice**, and a slice reported without its boundary is a subset
    presented as the whole. Said once, at the top, where it changes how the rest
    is read.

    This is the summary describing its own scope, which is exactly what a reader
    needs; it is not the platform-housekeeping prose that has no business in a
    work summary.

    **It also owes the reader the fourth field.** The assembled payload carries a
    board column and no verdict -- `SummaryLine` has `status` and `pr_state` and
    nothing that says whether the code landed -- so where `releases summarize`
    prints `○ not merged`, this prints `🟢 In Review`. Both are true and they
    answer different questions, and the one a release reader is asking is the
    first. Deriving a verdict here would be a second answer to it, which is the
    defect this whole line-shape exists to prevent, so the scope says which
    question it is answering and names the command that answers the other.
    """
    release = _release(payload)
    if not release:
        return []
    covered = int(payload.get("release_ticket_count") or 0)
    excluded = payload.get("tickets_without_release_count")
    sentence = (
        f"Covers only the {covered} ticket{'s' if covered != 1 else ''} on "
        f"{escape(release)}."
    )
    if excluded is not None:
        sentence += (
            f" {excluded} of this project's tickets are on no release and are "
            "not included."
        )
    return [
        f"[dim]{sentence}[/dim]",
        "[dim]Each line ends with its board column. Whether the code actually "
        "merged is a verdict, and it comes from `innoday releases "
        "summarize`.[/dim]",
        "",
    ]


def _footer(payload: Dict[str, Any], org_alias: str) -> str:
    parts = [str(payload.get("footer") or "")]
    idle = int(payload.get("unassigned_idle_count") or 0)
    if idle:
        parts.append(f"{idle} unassigned idle{_scope_suffix(payload)}")
    unmapped = int(payload.get("unmapped_assignee_count") or 0)
    if unmapped:
        parts.append(
            f"{unmapped} assignee{'s' if unmapped != 1 else ''} unmapped — "
            f"map at /ui/{escape(org_alias)}/profile"
        )
    return " · ".join(p for p in parts if p)


def render_summary(
    payload: Dict[str, Any],
    *,
    scrum: bool,
    org_alias: str,
    project_label: str,
) -> str:
    """The whole rendered summary, as Rich markup.

    Pure: everything it needs is in `payload`. That is what makes the layout
    rules -- the active/idle split, the cap, who gets an `@`, how an unmapped
    assignee reads -- testable without a server.
    """
    scope = "Team" if scrum else "You"
    # A release scope is not a duration and must not be captioned as one:
    # "last release:v1.9.0" reads as a window someone mis-typed.
    release = _release(payload)
    window = (
        f"release {escape(release)}"
        if release
        else f"last {escape(str(payload.get('window_spec')))}"
    )
    lines: List[str] = [
        f"[bold cyan]{scope}[/bold cyan] · {window}"
        f" · {escape(project_label)}"
        f"  [dim]({escape(str(payload.get('outcome') or 'assembled'))})[/dim]",
        "",
    ]
    lines.extend(_boundary(payload))

    # A summary assembled over tickets the board never delivered is not wrong
    # so much as *unmarked*, and that is the dangerous shape: it reads exactly
    # like a quiet week. Say it at the top, where it changes how the rest is
    # read, rather than in the footer where it looks like a note.
    sync_error = payload.get("sync_error")
    if sync_error:
        lines.append(
            f"[yellow]⚠ Board sync failed — this covers stale tickets.[/yellow] "
            f"[dim]{escape(str(sync_error))}[/dim]"
        )
        lines.append("")

    # The cached narrative, when a gate short-circuited and there is one. It
    # covers the whole window rather than one row -- `summary-data` returns a
    # single `body_markdown`, and per-item prose lives in `summary_items`,
    # reachable only per ticket. Rendering it once, up front, is the honest
    # shape of the data we have.
    lines.extend(_prose_block(payload.get("body_markdown")))

    # A person's note, labelled and visually distinct from the generated prose
    # above it. Rendering the two as one block would be worse than not showing
    # the note at all: the reader could no longer tell which half a sentence
    # came from, and the whole reason the note lives in its own column is that
    # the two have different authors.
    lines.extend(
        _prose_block(
            payload.get("notes_markdown"),
            heading=_note_heading(payload.get("notes_updated_at")),
        )
    )

    active = payload.get("active") or []
    for line in active:
        lines.extend(_render_active(line, scrum))
        lines.append("")

    no_work = payload.get("no_work_detected") or []
    if no_work:
        lines.append(f"  [dim]── No work detected{_scope_suffix(payload)} ──[/dim]")
        lines.extend(_render_compact(line, scrum) for line in no_work)
        lines.append("")

    unassigned = payload.get("unassigned_work_happening") or []
    if unassigned:
        lines.append("  [dim]── Unassigned — work happening ──[/dim]")
        lines.extend(_render_compact(line, scrum) for line in unassigned)
        lines.append("")

    # Personal mode only, and the engine only fills it in personal mode -- the
    # guard here is belt and braces so a widened payload can never leak a
    # "what's queued for you" block into a team roll-up.
    up_next = payload.get("up_next") or []
    if up_next and not scrum:
        lines.append("  [dim]── Up next ──[/dim]")
        lines.extend(_render_compact(line, scrum=False) for line in up_next)
        lines.append("")

    if not active and not no_work and not unassigned and not up_next:
        # Under a release scope this is the release's silence, not the project's.
        quiet = (
            f"Nothing on {escape(release)} moved in this window."
            if release
            else "Nothing moved in this window."
        )
        lines.append(f"  [dim]{quiet}[/dim]")
        lines.append("")

    lines.append(f"[dim]{_footer(payload, org_alias)}[/dim]")
    return "\n".join(lines)


def no_identity_message(
    *, project_label: str, org_alias: str, candidate_count: int
) -> str:
    """The dead end that is actually a fix.

    An unmapped caller and a genuinely quiet three days produce the same empty
    personal summary, and only one of them is the user's to act on -- so say
    which, and say how many names the board *did* offer, so "map it" reads as a
    task with a known size rather than a shrug.
    """
    message = (
        f"No board identity for you on {project_label} — map it with:\n"
        f"  innoday auth identity --set <your-github-login>\n"
        f"or in the browser at /ui/{org_alias}/profile"
    )
    if candidate_count:
        message += (
            f"\n{candidate_count} unmapped name"
            f"{'s' if candidate_count != 1 else ''} seen on this project's board."
        )
    return message


# ------------------------------------------------------------------- commands


class SummaryCommands:
    """`innoday summary` — one command, no flags in the common case."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--scrum",
            action="store_true",
            help="Summarise the whole team, showing who owns each item",
        )
        parser.add_argument(
            "--me",
            dest="summary_me",
            action="store_true",
            # **The default said out loud.** A bare `innoday summary` has always
            # meant your own work, and it still does -- but the scope was the one
            # thing a reader could not see in what they typed, so
            # `/innoday:summary` and `/innoday:summary --scrum` looked like the
            # same command with an option rather than two different questions.
            # Now each scope has a word: `--me`, `--scrum`, `--release`.
            help="Summarise just your own work. The default, named so a command "
            "says which of the three scopes it asked for.",
        )
        parser.add_argument(
            "--window",
            # Validated, not enumerated: a `choices` list here could only ever
            # be a subset of the grammar the engine accepts. See
            # `SummaryWindow`'s docstring for what that cost.
            type=parse_window_arg,
            metavar="WINDOW",
            # argparse does not pass `default` through `type`, so this must
            # already be in canonical form rather than relying on a conversion
            # that never runs for the default case.
            default=DEFAULT_WINDOW,
            # `release` is not a duration and this string must not imply it is.
            # It used to read "to measure from the project's last release", which
            # described the behaviour #563 removed: `release` was translated into
            # a day count and the release identity thrown away. It is now a
            # *scope* -- tickets on any other release, and tickets on no release
            # at all, are not assembled. A reader who trusts the old wording asks
            # for a period and gets a filter.
            help=f"How far back to look (default: {DEFAULT_WINDOW}) — "
            f"{WINDOW_GRAMMAR_HINT}. Or 'release' to scope to the release being "
            "cut instead: that narrows the summary to tickets carrying that "
            "version, rather than covering a span of time.",
        )
        parser.add_argument(
            "--release",
            dest="summary_release",
            nargs="?",
            const=True,
            default=None,
            metavar="VERSION",
            # `--scrum --window release` was two flags saying one thing, and that
            # pair is what people typed every time: a release summary *is* a team
            # summary, because "what is in this release" is never a question about
            # one person's slice of it. `--release` is the pair, said once.
            #
            # The bare word is the point, so VERSION is optional and omitting it
            # means the release being cut -- the same default `innoday releases
            # content` already uses, rather than a second rule for what "no
            # version" means.
            #
            # `--window release` is untouched and still reaches a *personal*
            # release view, which this flag deliberately cannot express.
            help="Summarise the release being cut: the whole team, scoped to "
            "tickets carrying that version. Shorthand for '--scrum --window "
            "release'. Pass VERSION to scope to some other release.",
        )
        parser.add_argument(
            "--project",
            dest="summary_project",
            metavar="REF",
            help="Project alias or id (default: the project resolved from the "
            "cwd's .innoday/project.yml)",
        )
        parser.add_argument(
            "--json",
            dest="summary_json",
            action="store_true",
            help="Print the raw assembled payload instead of the rendered summary",
        )

    # ------------------------------------------------------------------- scope

    @staticmethod
    def window_to_scope(
        window: str,
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Window → `(window_spec, release, note)`.

        **Not** `SummaryService.resolve_scope`, which it used to share a name with
        while doing something else entirely: that one turns *wire params* into a
        resolved scope (a concrete release version and a `period_start`, against
        the database). This one turns an *argparse value* into the wire params to
        send. Two functions, one name, opposite ends of the same call -- a trap
        rather than a parallel.

        Two kinds of scope, and exactly one of the first two values is set.
        `release` is not a duration at all: it narrows *which tickets exist* for
        this summary, so it goes to the engine as a release and the engine keys
        the summary on the release. A duration cannot express "these tickets",
        which is why the old shape -- fetch the project's releases, take
        `max(released_at)`, return "N days" -- discarded the only part that
        mattered before the engine ever saw it.

        **Nothing about the release is resolved here.** `current` is the server's
        sentinel, resolved by the same helper the `?release=` ticket filter uses
        (`current_release_version`); a second copy of it, computed client-side from
        a different rule, is precisely what shipped the wrong answer. It also
        means this needs no HTTP call and no project id, so the
        `?project_id=<alias>` mismatch that silently matched zero releases -- and
        fell back to a week -- has no code left to live in.

        Durations are normalised through the shared grammar rather than a
        CLI-local lookup table -- one table here plus one grammar in the engine
        was the divergence itself. It is normalised again even though
        `parse_window_arg` already did: this is reachable directly, and an alias
        leaking through would be sent as the cache key verbatim.
        """
        if window == SummaryWindow.RELEASE.value:
            return release_to_scope(True)
        return normalize_window(window) or window, None, None

    # ----------------------------------------------------------------- execute

    @staticmethod
    async def execute(args: argparse.Namespace, config) -> int:
        org_alias = config.get_current_organization()
        if not org_alias:
            console.print(
                format_error(
                    "No project in this directory. The organization and "
                    "project come from `.innoday/project.yml` in the working "
                    "directory, so run this from a project workspace, or pass "
                    "--dir <path>.\n"
                    "If you are redirecting output somewhere else, redirect to "
                    "that path rather than changing directory into it."
                )
            )
            return 1
        org_id = config.get_organization_id(org_alias)
        if not org_id:
            console.print(
                format_error(
                    f"Organization '{org_alias}' is not in your local config. "
                    "Run 'innoday orgs list' to refresh."
                )
            )
            return 1

        project_ref = getattr(args, "summary_project", None) or (
            config.get_current_project_id()
        )
        # What to *call* the project on screen. A ref resolved from project.yml
        # is a UUID, and printing that in the header tells the reader nothing,
        # so the alias is read from the same file the id came from.
        #
        # **Only when the ref actually IS that project.** There are two
        # `--project` flags -- the global one on the entrypoint and this
        # subcommand's -- and this used to check the subcommand's alone. So
        #
        #     cd ~/workspaces/hs/pf
        #     innoday --organization bp --project BPCL summary --scrum
        #
        # summarised BPCL (correctly: the payload carried BPCL's project_id) and
        # titled it **PF**, because the global flag left `summary_project` unset
        # and the label fell through to the working directory's alias. A summary
        # that attributes one client's work to another client's project is not a
        # mislabelled report, it is a wrong one -- and it made phantom data
        # problems look real when reading across projects.
        # ...and from the directory the caller pointed at. `config` honours
        # `--dir`; this call did not, so under `--dir` the ids never matched and
        # the header fell back to printing a UUID.
        project_label = str(project_ref)
        context_dir = getattr(args, "dir", None)
        context = load_project_context(Path(context_dir) if context_dir else None) or {}
        if project_ref and project_ref == context.get("project_id"):
            project_label = (
                context.get("project_alias")
                or context.get("project_name")
                or project_label
            )
        if not project_ref:
            console.print(
                format_error(
                    "No project. Run this from inside a project directory (one "
                    "with .innoday/project.yml), or pass --project <alias>."
                )
            )
            return 1

        release_arg = getattr(args, "summary_release", None)
        if getattr(args, "summary_me", False) and (
            release_arg is not None or getattr(args, "scrum", False)
        ):
            # Three scopes, one question. Silently letting one win would leave
            # the caller reading a summary they did not ask for.
            console.print(
                format_error(
                    "--me is the personal scope, so it cannot be combined with "
                    "--scrum or --release. Pick one."
                )
            )
            return 1
        # `--release` implies the team view, and implies it *silently* rather than
        # erroring when `--scrum` is also given: the two say the same thing, and
        # rejecting the redundant pair would break the very spelling this flag
        # replaces.
        scrum = bool(getattr(args, "scrum", False)) or release_arg is not None
        as_json = bool(getattr(args, "summary_json", False)) or (
            getattr(args, "format", None) == "json"
        )

        if release_arg is not None:
            window_spec, release, note = release_to_scope(release_arg)
        else:
            window_spec, release, note = SummaryCommands.window_to_scope(
                getattr(args, "window", DEFAULT_WINDOW)
            )
        # `CURRENT_RELEASE` is a sentinel the server resolves, so printing it
        # verbatim gave "Assembling release current...". Nothing is resolved here
        # -- the label just says what was asked for.
        if release == CURRENT_RELEASE:
            scope_label = "the release being cut"
        elif release:
            scope_label = f"release {release}"
        else:
            scope_label = f"the last {window_spec}"

        async with InnoDayAPIClient(config) as client:
            try:
                params = _summary_params(
                    window_spec=window_spec, release=release, scrum=scrum
                )

                with ProgressReporter(f"Assembling {scope_label}..."):
                    response = await client.get(
                        f"/organizations/{org_id}/projects/{project_ref}/summary-data",
                        params=params,
                    )
            except APIError as exc:
                console.print(format_error(str(exc)))
                return 1

        if response.status_code != 200:
            console.print(
                format_error(
                    f"Could not assemble a summary: HTTP {response.status_code} — "
                    f"{response.text[:300]}"
                )
            )
            return 1

        payload = response.json()

        if as_json:
            print(json.dumps(payload, indent=2, default=str))
            return 0

        if not scrum and _has_no_work(payload):
            unmapped = payload.get("unmapped_assignees") or []
            if not await SummaryCommands._caller_has_identity(config):
                console.print(
                    format_warning(
                        no_identity_message(
                            project_label=project_label,
                            org_alias=org_alias,
                            candidate_count=len(unmapped),
                        )
                    )
                )
                return 1

        if note:
            console.print(f"[dim]{note}[/dim]")
        console.print(
            render_summary(
                payload,
                scrum=scrum,
                org_alias=org_alias,
                project_label=project_label,
            )
        )
        return 0

    @staticmethod
    async def _caller_has_identity(config) -> bool:
        """Does the caller have any `user_identity` row at all?

        Only asked when a personal summary came back empty, so the common path
        pays nothing for it. `/auth/me` reports the caller's own mappings; a
        transport failure answers "yes" so a network blip degrades to a plain
        empty summary rather than a confident, wrong instruction to go and map
        an identity that already exists.
        """
        try:
            async with InnoDayAPIClient(config) as client:
                response = await client.get("/auth/me")
            if response.status_code != 200:
                return True
            return bool((response.json() or {}).get("identities"))
        except (APIError, ValueError):
            return True


def _summary_params(
    *, window_spec: Optional[str], release: Optional[str], scrum: bool
) -> Dict[str, Any]:
    """The query the engine is actually asked, kept pure so it is testable.

    **A release and a window are alternatives, and only one is sent.** They are
    two different scopes -- one narrows which tickets exist, the other how far
    back to look -- so sending both would leave which one won up to the server to
    decide, and a reader with no way to tell which they got.

    `--json` (and therefore the `/innoday:summary` skill, which shells out to
    this command) goes through here. A scope that never reaches these params
    never reaches the engine, whatever the MCP tool sends.
    """
    params: Dict[str, Any] = {"summary_type": "scrum" if scrum else "personal"}
    if release:
        params["release"] = release
    else:
        params["window_spec"] = window_spec
    if not scrum:
        # The engine resolves 'me' against the bearer token, so the CLI never has
        # to know its own user id.
        params["user_id"] = "me"
    return params


def _is_empty(payload: Dict[str, Any]) -> bool:
    return not any(
        payload.get(key)
        for key in (
            "active",
            "no_work_detected",
            "unassigned_work_happening",
            "up_next",
            "body_markdown",
            # A note is content: a payload whose only substance is something a
            # person wrote must still render. It is deliberately NOT part of
            # `_has_no_work` below -- see there.
            "notes_markdown",
        )
    )


def _has_no_work(payload: Dict[str, Any]) -> bool:
    """Nothing about *work* in this payload, whatever else it carries.

    Separate from `_is_empty` because the two questions diverged the moment
    notes existed. Rendering asks "is there anything to show?"; the unmapped-
    caller diagnostic asks "is their work missing?" -- and a note is not work.

    Folding the note into one predicate meant an inherited note, which persists
    across every regeneration until someone clears it, permanently suppressed
    the one message that tells an unmapped person why their tickets never
    appear. The note made the summary look answered while the actual problem
    stayed invisible.
    """
    return not any(
        payload.get(key)
        for key in (
            "active",
            "no_work_detected",
            "unassigned_work_happening",
            "up_next",
            "body_markdown",
        )
    )
