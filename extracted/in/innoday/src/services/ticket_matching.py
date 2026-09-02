"""Resolving which ticket a piece of code belongs to.

One index, one matcher, one place. These used to live in `summary_service` and
`routers/webui/data` -- the ticket index in the first, the branch-to-ticket
matcher in the second -- which meant the only working join between a ticket and
its pull requests sat inside the web UI, where neither the release path nor the
summary path could reach it. Both were rebuilding a worse version of it.

They also could not be brought together where they were: `summary_service`
imports `code_activity`, so `code_activity` cannot import back, and the matcher
needed the index that lived in `summary_service`. Hence a module of their own,
below both.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Sequence, Tuple

from sqlmodel import Session, select

from src.domain.project import Project, ProjectRepository
from src.domain.repository import Repository
from src.domain.repository_pull_request import RepositoryPullRequest
from src.domain.ticket import Ticket
from src.services.code_activity import extract_ticket_ref, ticket_ref_pattern


@dataclass
class TicketPullRequest:
    """One pull request that names a ticket, in its branch or its title.

    `merged_at`, `state` and `author_login` are carried because a release report
    needs all three and the original dataclass dropped them: whether the work
    shipped, whether it was abandoned, and who to credit. The web UI ignores
    them, which is why they were never missed.
    """

    repo: str
    number: int
    url: Optional[str]
    title: Optional[str]
    is_draft: bool = False
    #: Set only when the merge is confirmed. An abandoned pull request is also
    #: `closed`, and shipped nothing.
    merged_at: Optional[datetime] = None
    #: GitHub's own word: `open` or `closed`. A merged one is `closed`.
    state: Optional[str] = None
    author_login: Optional[str] = None

    @property
    def merged(self) -> bool:
        return self.merged_at is not None


def colliding_refs(
    project_alias: str, tickets: Sequence[Ticket]
) -> List[Tuple[str, Ticket, Ticket]]:
    """Strings that name one ticket on the board and a different one here.

    The two namespaces a ticket answers to share the project alias, so they
    spell the same strings for unrelated tickets. This is not hypothetical: of
    BPAI's 221 tickets, 22 strings collide -- `BPAI-169` is "Generate
    Suggestions for Measures" in Linear and "Design the Carbon Graph"
    internally.

    `tickets_by_ref` resolves the tie deterministically in the board key's
    favour, which is the right guess and still only a guess. Nothing removes the
    ambiguity, so the honest thing is to report it: a summary that cites
    `BPAI-169` is citing something a reader cannot resolve either.

    Returns `(ref, board_ticket, internal_ticket)`, sorted, for the strings where
    the two namespaces genuinely disagree.
    """
    if not project_alias:
        return []
    external: Dict[str, Ticket] = {}
    internal: Dict[str, Ticket] = {}
    for ticket in tickets:
        if ticket.external_ticket_id:
            external.setdefault(ticket.external_ticket_id.upper(), ticket)
        if ticket.project_ref_number is not None:
            internal.setdefault(
                f"{project_alias}-{ticket.project_ref_number}".upper(), ticket
            )
    clashes = []
    for ref, board_ticket in external.items():
        other = internal.get(ref)
        if other is not None and other.id != board_ticket.id:
            clashes.append((ref, board_ticket, other))
    return sorted(clashes, key=lambda row: row[0])


#: Board names that are safe to read as a ticket prefix in a branch.
#:
#: **Taken from the ticket's own `source_platform`, not from a fixed list.**
#: `linear_413_manage_org_small_fixes` is a real branch whose ticket sat on a
#: release reporting "no pull request names this ticket" -- people name branches
#: after the tool as readily as after the project.
#:
#: The first version of this listed "ticket" and "issue" too, which is too
#: promiscuous by half: "issue 12" and "ticket 5" are ordinary English, and
#: "issue 12" in a description almost always means a GitHub issue, not this
#: board's twelfth ticket. A platform name a ticket actually came from cannot
#: misfire that way.
_MATCHABLE_PLATFORMS = {"linear", "jira", "trello", "notion"}


def tickets_by_ref(project_alias: str, tickets: Sequence[Ticket]) -> Dict[str, Ticket]:
    """Every name a ticket answers to, upper-cased → the ticket.

    A reference resolves against two things a ticket can be called: the
    board's own key (`external_ticket_id`, e.g. `PF-7` from Linear) and the
    internal display number ``{project alias}-{project_ref_number}``. Both
    are real names for the same ticket and branches use whichever the person
    saw.

    Both now share one prefix -- the project alias -- so a board key and an
    internal number can spell the same string for *different* tickets (Linear
    `PF-7` vs internal PF ticket 7). External keys are inserted first and
    `setdefault` keeps the first writer, so the board's own key wins that tie
    deterministically: it is the name the board, the branch, and the person
    all already use. Previously the two namespaces were kept apart by
    prefixing internal numbers with the org alias instead, which cost a
    reference that no longer matched the project it belonged to.

    Shared by the two things that resolve a reference -- code activity on the
    assembled path, and a narrator's `ticket_ref` on the written one. One
    index, so a branch name and a stand-up line can never disagree about
    which ticket `PF-7` is.
    """
    by_ref: Dict[str, Ticket] = {}
    for ticket in tickets:
        if ticket.external_ticket_id:
            by_ref.setdefault(ticket.external_ticket_id.upper(), ticket)
    for ticket in tickets:
        if ticket.project_ref_number is not None and project_alias:
            by_ref.setdefault(
                f"{project_alias}-{ticket.project_ref_number}".upper(), ticket
            )
    # **The name people give a branch after the tool, not the project.**
    # `linear_413_manage_org_small_fixes` is a real branch on a real merged pull
    # request whose ticket sat on the release reporting "no pull request names
    # this ticket". The number after the tool name is the board's number, so the
    # ticket answers to it. Added last, so it can never shadow a real key.
    for ticket in tickets:
        number = _numeric_tail(ticket.external_ticket_id)
        if number is None:
            continue
        platform = (getattr(ticket, "source_platform", None) or "").lower()
        if platform in _MATCHABLE_PLATFORMS:
            by_ref.setdefault(f"{platform}-{number}".upper(), ticket)
    return by_ref


def _numeric_tail(ref: Optional[str]) -> Optional[str]:
    """The digits at the end of a board key: ``BPAI-413`` -> ``413``."""
    if not ref:
        return None
    match = re.search(r"(\d+)\s*$", ref)
    return match.group(1) if match else None


def ref_prefixes(by_ref: Dict[str, Ticket]) -> List[str]:
    """The alias part of every name the ticket index answers to.

    `PF-398` and `ZZ-9` contribute `PF` and `ZZ`. Duplicates collapse in
    `ticket_ref_pattern`, so this can be as loose as the index is.
    """
    prefixes = set()
    for key in by_ref:
        head, _, tail = key.rpartition("-")
        if head and tail.isdigit():
            prefixes.add(head)
    return sorted(prefixes)


#: A reference that is part of a filename or path is describing a *file*, not
#: claiming the work. `docs/BPAI-343-phase1-summary.md` in a README refresh
#: attributed that whole pull request to BPAI-343, which had nothing to do with
#: it. Matched before the reference and stripped, rather than excluded after,
#: because the rest of the text may still name a ticket properly.
_PATHY = re.compile(r"[`\"\'(\[]?\S*/\S+|\S+\.(?:md|py|ts|tsx|js|json|ya?ml|sql|txt)\b")


def _lists_numbers(text: str, pattern: "re.Pattern") -> bool:
    """True when a reference is immediately followed by another bare number.

    `linear_355_380_claude_rule` names two tickets, but only the first carries
    the prefix -- so counting references finds one and the branch reads as
    unambiguous. It is not: the pull request is a rule written while touching
    both, and crediting 355 reported that work as shipped outside its release.

    Numbers stacked directly after a reference are a list. Anything else after
    it -- `bpai_409_small_ui_items`, `BPAI-334/property-report` -- is a
    description, and the reference stands.
    """
    for match in pattern.finditer(text):
        if re.match(r"[-_ ]\d+", text[match.end() :]):
            return True
    return False


def _without_paths(text: str) -> str:
    """`text` with anything that looks like a file path or filename removed."""
    return _PATHY.sub(" ", text)


def _refs_in(text: str, pattern: "re.Pattern") -> set:
    """Every distinct ticket reference in `text`, normalised.

    `extract_ticket_ref` returns only the first. Counting them is what lets a
    title that mentions two tickets be recognised as ambiguous rather than
    silently attributed to whichever is written first.
    """
    return {
        f"{match.group(1).upper()}-{match.group(2)}" for match in pattern.finditer(text)
    }


#: `Closes BPAI-414`, `fixes #12`, `resolves BPAI-3` -- GitHub's own convention
#: for "this pull request delivers that". When a body says it, it is the answer,
#: however many other tickets the prose mentions in passing.
_CLOSING = re.compile(
    r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\b[^\n]{0,40}?"
    r"\b([A-Za-z]+[-_ ]?\d+)\b",
    re.IGNORECASE,
)


def _closing_ref(text: str, pattern: "re.Pattern") -> Optional[str]:
    """The ticket a body says it *closes*, if it says so at all.

    A description that mentions four tickets and closes one is not ambiguous --
    it is explicit. Checking the closing keyword before falling back to
    "exactly one reference" is what lets a thorough description still resolve.
    """
    for match in _CLOSING.finditer(text):
        ref = extract_ticket_ref(match.group(1), pattern)
        if ref is not None:
            return ref
    return None


def ticket_for_pull_request(
    head_ref: Optional[str],
    title: Optional[str],
    by_ref: Dict[str, Ticket],
    pattern: "re.Pattern",
    body: Optional[str] = None,
) -> Optional[Ticket]:
    """The ticket a pull request names, from its branch or its title.

    **The branch, then the title, and by the same rule as everywhere else.**
    This used to read the branch alone, with its own hand-rolled parser --
    splitting on separators and trying adjacent segment pairs. Meanwhile
    `code_activity` had already been consulting branch *and* title through the
    shared `ticket_ref_pattern`. Two matchers answering one question, and the
    release and summary views were using the weaker one: a pull request titled
    `BPAI-334: property report endpoint` was invisible to them, while a
    commit-activity row for the same work resolved fine.

    Sharing the pattern is the point. A ticket reference is one concept, and the
    version that knows about `PF 398` and `pf_398` should not be the one that
    only some readers get.

    **A title naming more than one ticket names none of them.** A branch belongs
    to one piece of work, so the first reference in it is the answer. A title is
    prose and can mention several: `docs(rules): add fix-as-you-touch rule for
    BPAI-355 & BPAI-380` is a documentation change *about* two tickets, and
    taking the first reference credited its work to BPAI-355 -- which then
    surfaced as "shipped outside a release", a finding that was not true. When
    the title is ambiguous the honest answer is no match; the work lands in
    unticketed, where it belongs.
    """
    # **A branch naming two tickets names neither, same as a title.**
    # `linear_355_380_claude_rule` delivers neither 355 nor 380 -- it is a rule
    # written while touching both -- and taking the first reference credited the
    # work to 355 and reported it as shipped outside its release.
    if (
        head_ref
        and len(_refs_in(head_ref, pattern)) == 1
        and not _lists_numbers(head_ref, pattern)
    ):
        ref = extract_ticket_ref(head_ref, pattern)
        if ref is not None:
            ticket = by_ref.get(ref)
            if ticket is not None:
                return ticket

    clean_title = _without_paths(title or "")
    if (
        clean_title
        and len(_refs_in(clean_title, pattern)) == 1
        and not _lists_numbers(clean_title, pattern)
    ):
        ref = extract_ticket_ref(clean_title, pattern)
        if ref is not None:
            ticket = by_ref.get(ref)
            if ticket is not None:
                return ticket

    # **The body, last.** A pull request titled "Label updates" on a branch
    # called `financial_summary_labels` says `BPAI-414` in its description, and
    # reading only the branch and the title made that work invisible -- the
    # ticket reported "no pull request names this ticket" while the pull request
    # was naming it plainly.
    #
    # Last, because a description is the loosest of the three: it quotes other
    # tickets, links related work, and pastes checklists. So a closing keyword
    # wins outright, and without one the body has to name exactly one ticket.
    clean_body = _without_paths(body or "")
    if clean_body:
        closing = _closing_ref(clean_body, pattern)
        if closing is not None:
            ticket = by_ref.get(closing)
            if ticket is not None:
                return ticket
        if len(_refs_in(clean_body, pattern)) == 1:
            ref = extract_ticket_ref(clean_body, pattern)
            if ref is not None:
                ticket = by_ref.get(ref)
                if ticket is not None:
                    return ticket
    # A branch that *is* the reference and nothing else, for an alias the
    # pattern cannot know about -- kept from the original matcher.
    return by_ref.get(head_ref.upper()) if head_ref else None


def attached_pull_requests(session: Session, project_id: str) -> Dict[tuple, int]:
    """`(repo name, pull request number)` -> ticket id, for hand-made links.

    Read before any derivation. A person who attached a pull request to a ticket
    has said something the branch, the title and the description do not, and no
    amount of pattern matching should be able to overrule it.
    """
    rows = session.exec(
        select(
            Repository.name,
            RepositoryPullRequest.number,
            RepositoryPullRequest.ticket_id,
        )
        .join(
            RepositoryPullRequest,
            RepositoryPullRequest.repository_id == Repository.id,
        )
        .join(ProjectRepository, ProjectRepository.repository_id == Repository.id)
        .where(
            ProjectRepository.project_id == project_id,
            ProjectRepository.is_active == True,  # noqa: E712
            RepositoryPullRequest.ticket_id.is_not(None),  # type: ignore[union-attr]
        )
    ).all()
    return {(name, number): ticket_id for name, number, ticket_id in rows}


def pull_requests_by_ticket(
    session: Session, project_id: str
) -> Dict[int, List[TicketPullRequest]]:
    """Ticket id → the **open** pull requests whose branch names it.

    Merged ones are kept in the table now but deliberately not shown here: this
    panel answers "what is in flight on this ticket", and a ticket with a year of
    shipped work would drown in it. `merged_pull_requests_by_ticket` is the other
    question.

    **A ticket's code can live in several repositories at once**, which is the
    whole reason this exists: the summary panel could previously show at most the
    one `pr_url` a `SummaryItem` happened to carry, so a ticket with work in three
    repos looked like a ticket with work in one (#574's per-repo icons, blocked on
    #579 until `head_ref` was stored).

    Matched through `tickets_by_ref` -- the same index code activity resolves
    through -- so a branch name and a stand-up line cannot disagree about which
    ticket `PF-7` is. A branch naming no ticket links to nothing rather than
    guessing.

    Two queries regardless of how many tickets or repositories a project has: one
    for its tickets, one for the pull requests on its repos.
    """
    return _pull_requests_by_ticket(session, project_id, merged=False)


def _pull_requests_by_ticket(
    session: Session, project_id: str, *, merged: bool
) -> Dict[int, List[TicketPullRequest]]:
    """Shared body for the open and merged views -- one query shape, one filter.

    Written once because the two differ only in that filter, and a second copy is
    a second place for the branch-to-ticket rule to drift.
    """
    project = session.get(Project, project_id)
    if project is None:
        return {}
    tickets = list(
        session.exec(
            select(Ticket).where(
                Ticket.project_id == project_id,
                Ticket.deleted_at.is_(None),  # type: ignore[union-attr]
            )
        ).all()
    )
    if not tickets:
        return {}
    by_ref = tickets_by_ref(project.alias or "", tickets)

    # **Open-ness is now explicit.** This table used to hold nothing else --
    # merged rows were deleted -- so "open" was implied by a row existing.
    state_filter = (
        RepositoryPullRequest.merged_at.is_not(None)  # type: ignore[union-attr]
        if merged
        else RepositoryPullRequest.state == "open"
    )

    rows = session.exec(
        select(RepositoryPullRequest, Repository.name)
        .join(Repository, Repository.id == RepositoryPullRequest.repository_id)
        .join(ProjectRepository, ProjectRepository.repository_id == Repository.id)
        .where(
            ProjectRepository.project_id == project_id,
            ProjectRepository.is_active == True,  # noqa: E712
            # **No `head_ref is not null` here.** It used to be, from when a
            # branch name was the only thing consulted -- which quietly meant a
            # pull request whose *title* names its ticket could never be
            # reached, however plainly it said so.
            state_filter,
        )
    ).all()

    found: Dict[int, List[TicketPullRequest]] = {}
    # **Every prefix the index actually answers to, not just the project's
    # alias.** A ticket answers to two names -- the board's own key and the
    # internal `{alias}-{number}` -- and a board key need not share the alias:
    # a Linear `ZZ-9` on a project aliased something else is ordinary. Building
    # the pattern from the project alias alone silently stopped matching those,
    # which the two-repos test caught.
    pattern = ticket_ref_pattern(*ref_prefixes(by_ref), project.alias or "")
    for pr, repo_name in rows:
        ticket = ticket_for_pull_request(pr.head_ref, pr.title, by_ref, pattern)
        if ticket is None or ticket.id is None:
            continue
        found.setdefault(ticket.id, []).append(
            TicketPullRequest(
                repo=repo_name,
                number=pr.number,
                url=pr.url,
                title=pr.title,
                is_draft=bool(pr.is_draft),
                merged_at=pr.merged_at,
                state=pr.state,
                author_login=pr.author_login,
            )
        )
    # One repo per icon, in a stable order, so the row does not reshuffle between
    # renders of the same data.
    for prs in found.values():
        prs.sort(key=lambda p: (p.repo.lower(), p.number))
    return found


def merged_pull_requests_by_ticket(
    session: Session, project_id: str
) -> Dict[int, List[TicketPullRequest]]:
    """Ticket id → the pull requests that **merged** for it.

    The question this whole change exists to make answerable. Until merged rows
    were kept, a ticket's link to the code that shipped it lasted exactly as long
    as the pull request was unmerged: `head_ref` is the only field on a pull
    request that names a ticket, and the row was deleted the moment it left the
    open list.

    ``merged_at``, not merely ``state == "closed"``. An abandoned pull request is
    also closed and shipped nothing; counting it here would put work in a release
    that never had it. A merge we could not confirm leaves ``merged_at`` unset and
    is likewise absent -- the safe direction, and the same rule the sync applies.
    """
    return _pull_requests_by_ticket(session, project_id, merged=True)
