"""Assemble what a release contains, here, with the organisation's credential.

**Why this is server-side.** The release engine used to find all of this itself,
from wherever it happened to be running: about thirty-five GitHub calls across a
seven-repository project. That meant whoever ran a release had to supply a GitHub
token, and the one closest to hand is a *personal* one — the wrong credential for
a release, carrying whatever scopes that account happens to have. Worse, needing
it at all hid the real gap: the credential the release should use is already
here, in the Vault, and this is where every other GitHub read in the platform
already happens.

So the platform assembles and hands the engine a finished answer. A preview then
needs no credential on the client at all.

**Deliberately not reading stored rows.** `RepositoryPullRequest` keeps merged
pull requests now, but only since the sync started marking them, and there is no
commit model at all — so a window reaching back three months finds nothing. This
relocates the GitHub calls to the side that holds the credential rather than
eliminating them, which is the whole of what was needed.
"""

from __future__ import annotations

import asyncio
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from src.adapters.board_assignee import BoardAssignee
from src.api.github_api import GitHubAPI
from src.domain.project import Project, ProjectRepository, RepositoryLayer
from src.domain.release import (
    Recommendation,
    Release,
    ReleaseStatus,
    ReleaseVerdict,
)
from src.domain.repository import Repository
from src.domain.summary import Summary, SummaryItem
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User
from src.domain.user_identity import IdentityPlatform
from src.services.code_activity import (
    CodeActivityFetcher,
    _owner_and_name,
    ticket_ref_pattern,
)
from src.services.identity_resolution import IdentityResolutionService
from src.services.release_planning import is_semver, latest_release, semver_key
from src.services.summary_service import release_spec
from src.services.ticket_matching import (
    attached_pull_requests,
    colliding_refs,
    ref_prefixes,
    ticket_for_pull_request,
    tickets_by_ref,
)
from src.services.ticket_release import _project_releases, current_release_version
from src.utils.time_windows import parse_iso_utc

logger = logging.getLogger(__name__)


@dataclass
class _RepoActivity:
    """One repository's pull requests, split by what actually happened to them.

    A tuple did this before and had grown to four positions; a fifth (abandoned
    pull requests) is what tipped it over. Named fields also stop the two
    same-shaped lists being swapped at a call site, which a tuple cannot.
    """

    repo: str
    merged: List[Dict[str, Any]] = field(default_factory=list)
    opened: List[Dict[str, Any]] = field(default_factory=list)
    #: Closed without merging. Shipped nothing, but is not the same as no code.
    abandoned: List[Dict[str, Any]] = field(default_factory=list)
    commit_count: int = 0
    #: Paging ran out before the repository did, so these lists are short.
    truncated: bool = False


#: The move a verdict implies, where it implies one. Absent means the decision is
#: a judgement about what two pieces of English mean -- an unticketed pull request
#: pairing with an existing ticket, joining a grouping, or getting one of its own
#: -- and this service states facts it can defend. The narrator proposes those.
_IMPLIED: Dict[str, str] = {
    ReleaseVerdict.SHIPPED.value: Recommendation.NONE.value,
    ReleaseVerdict.NOT_MERGED.value: Recommendation.NONE.value,
    ReleaseVerdict.PARTLY_MERGED.value: Recommendation.SPLIT.value,
    ReleaseVerdict.SHIPPED_UNTAGGED.value: (
        Recommendation.ATTACH_TICKET_TO_RELEASE.value
    ),
    ReleaseVerdict.RELEASE_CANDIDATE.value: (
        Recommendation.ATTACH_TICKET_TO_RELEASE.value
    ),
    ReleaseVerdict.STARTED_UNTAGGED.value: (
        Recommendation.ATTACH_TICKET_TO_RELEASE.value
    ),
    ReleaseVerdict.ON_SHIPPED_RELEASE.value: Recommendation.MOVE_TO_RELEASE.value,
}


def _recommend(state: str) -> Optional[str]:
    """The move this verdict implies, or `None` where it implies none.

    **`no_code` deliberately implies nothing.** It is the verdict that most looks
    like it wants `drop_from_release`, and on a design ticket that is the wrong
    answer: design work lands in the design repositories and is reported under
    `design`, never against the ticket, so a design ticket reads `no_code` while
    its pull request sits one bucket away. BPAI-411 was recommended for dropping
    off v1.11.0 while bps-ui-demo #31 -- the ticket's own sentence, verbatim --
    had merged inside the same window.

    And this service cannot tell the two apart from a ticket row. `is_design` on
    an item is computed from its pull requests, so a ticket with none is never
    design by that test, which is exactly the case that matters. Rather than
    guess, `no_code` carries no recommendation and the reviewer checks
    `design.unticketed` first -- which is what the release-review skill now
    requires before anything is dropped.
    """
    return _IMPLIED.get(state)


def _contest(
    entry: Dict[str, Any], ticket: Ticket, people: "_PeopleIndex"
) -> Dict[str, Any]:
    """Whether a resolved match actually looks like this ticket's work.

    A reference resolving is not the same as it being right. bps-ui-v2 #241 --
    the whole content of BPAI's v1.11.1 hotfix -- is branched
    `bpai_409_small_ui_items` and titled "Bpai 409 small UI items", so it matched
    BPAI-409 cleanly. BPAI-409 is "Incorporate ESC-Utility-Rates", assigned to
    somebody else entirely; the work is small UI items, which is BPAI-407 and
    BPAI-421, both assigned to the person who opened the pull request. Attaching
    it credits one person's ticket with another's work, and every rule in this
    service would have done exactly that.

    Two disagreements are cheap to test and both are already loaded: who owns the
    ticket against who opened the pull request, and whether any meaningful word
    of the title is shared. Neither is conclusive alone -- people hand work over,
    and a good title need not repeat the ticket's -- so this **flags, and never
    re-matches**. The service states the disagreement; a person decides, and the
    decision lands on `RepositoryPullRequest.ticket_id` like every other
    confirmation here.
    """
    owner = people.name_for_ticket(ticket)
    author = entry.get("person")
    reasons: List[str] = []

    # **Both names have to be resolved to the same kind of thing.**
    # `name_for_ticket` returns a `User`'s short name; `name_for` returns one too
    # *if the GitHub login maps to a user*, and the raw login otherwise. So a
    # ticket assigned to a mapped user whose GitHub identity is unmapped
    # contested every time -- "the ticket belongs to Jasminder S., the pull
    # request is jasminder's" -- which is the commonest configuration there is,
    # not a disagreement. Asymmetric resolution says nothing about ownership.
    if owner and author and people.is_resolved(author) and owner != author:
        reasons.append(f"the ticket belongs to {owner}, the pull request is {author}'s")

    # **A pull request named after nothing but its ticket is the clearest match
    # there is.** `BPAI-412` shares no word with "Add jurisdiction filter", and
    # neither does GitHub's own "Merge pull request #12 from acme/bpai-412", so
    # the subject test contested the two least ambiguous titles in the repo.
    title = entry.get("title")
    if not _is_bare_reference(title) and not _shares_a_word(title, ticket.summary):
        reasons.append("the titles have no significant word in common")

    if not reasons:
        return {}
    # Grounded on the row as well as in prose, so the verdict is a value a caller
    # can filter on rather than the presence of a key.
    return {"contested": reasons, "state": ReleaseVerdict.CONTESTED.value}


def _is_bare_reference(title: Optional[str]) -> bool:
    """Whether a title says nothing except which ticket it is.

    `BPAI-412`, `Bpai 412`, `feat(BPAI-412)`, and GitHub's own
    `Merge pull request #12 from acme/bpai-412` all name the ticket and describe
    nothing, so there is no subject to disagree about. Treating them as a subject
    mismatch contested the most unambiguous matches in the repository.
    """
    text = (title or "").strip()
    if not text:
        return True
    stripped = re.sub(r"\b[A-Za-z]{2,}[-_ ]?\d+\b", " ", text, flags=re.I)
    stripped = re.sub(r"merge pull request|from\s+\S+|#\d+", " ", stripped, flags=re.I)
    return not {
        w
        for w in re.findall(r"[a-z0-9]+", stripped.lower())
        if len(w) > 2 and w not in _NOISE
    }


#: Words too common to mean two titles are about the same thing. Deliberately
#: short: this exists to stop "the" and "for" carrying a match, not to do
#: linguistics.
_NOISE = {
    "a",
    "an",
    "and",
    "the",
    "to",
    "of",
    "in",
    "on",
    "for",
    "from",
    "with",
    "add",
    "adds",
    "update",
    "updates",
    "fix",
    "fixes",
    "feat",
    "chore",
    "implement",
    "implements",
    "new",
    "into",
    "at",
    "by",
    "or",
    "is",
    "it",
}


def _shares_a_word(left: Optional[str], right: Optional[str]) -> bool:
    """Whether two titles share any word that carries meaning.

    Cheap on purpose. The question is only "could these plausibly be about the
    same thing", and one shared noun answers it well enough to decide whether a
    human should look. Short tokens go with the noise words: `v2` and `UI` are
    real, but they are also everywhere.
    """

    def words(text: Optional[str]) -> Set[str]:
        return {
            w
            for w in re.findall(r"[a-z0-9]+", (text or "").lower())
            if len(w) > 2 and w not in _NOISE
        }

    a, b = words(left), words(right)
    if not a or not b:
        # Nothing to disagree about. An empty title is a separate problem and
        # not one this should report as a contested match.
        return True
    return bool(a & b)


def _matched_by(pr: Dict[str, Any], by_ref: Dict[str, Any], pattern: Any) -> str:
    """Which of the three sources produced the match.

    Recorded because they are not equally trustworthy. A branch reference is a
    deliberate act; a reference found in a description may be a passing mention
    that happened to be the only one. A reader deciding whether to believe an
    attribution should be able to see where it came from -- and a summary should
    say so rather than asserting every match with the same confidence.
    """
    from src.services.ticket_matching import ticket_for_pull_request

    if ticket_for_pull_request(pr.get("branch"), None, by_ref, pattern) is not None:
        return "branch"
    if ticket_for_pull_request(None, pr.get("title"), by_ref, pattern) is not None:
        return "title"
    return "body"


def _public(pr: Dict[str, Any]) -> Dict[str, Any]:
    """A pull request entry with its description removed.

    `body` is matching input, not report content: it is the third place a pull
    request names its ticket and is routinely thousands of words of checklist.
    Emitting it would bury the report it exists to inform, so it is stripped on
    the way out of every bucket the payload carries.
    """
    return {k: v for k, v in pr.items() if k != "body"}


def _entry(pr: Dict[str, Any]) -> Dict[str, Any]:
    """The fields of a pull request a release actually needs.

    `branch` and `url` are the two that used to be dropped. Both arrive on the
    payload already, so keeping them costs nothing -- and without `branch` a
    pull request cannot be tied to its ticket at all, since the branch name is
    the only field on a pull request that names one.
    """
    return {
        "number": pr.get("number"),
        "title": pr.get("title") or "",
        "author": ((pr.get("user") or {}).get("login")) or None,
        "branch": ((pr.get("head") or {}).get("ref")) or None,
        "url": pr.get("html_url") or pr.get("url") or None,
        # Carried for matching, not for display -- a description is the third
        # place a pull request names its ticket, and often the only one. It
        # arrives on the list payload already, so keeping it costs no request.
        "body": pr.get("body") or None,
    }


#: Item verdicts that mean the release still owes an answer for this ticket.
_UNRESOLVED_ITEM_STATES = frozenset(
    {ReleaseVerdict.NO_CODE.value, ReleaseVerdict.NOT_STARTED.value}
)

#: The two off-release verdicts that can be proposed into the release being cut.
#: `RELEASE_CANDIDATE` split off `STARTED_UNTAGGED` once open pull requests were
#: attached, so every count over "candidates" has to span both or it silently
#: stops counting the half with code in flight.
_CANDIDATE_STATES = frozenset(
    {ReleaseVerdict.STARTED_UNTAGGED.value, ReleaseVerdict.RELEASE_CANDIDATE.value}
)

#: Statuses that mean the work is finished enough for a release to claim it.
#: There is no TEST status: Linear's "in test", "internal review" and "code
#: review" all normalise to IN_REVIEW, so a summary cannot tell testing from
#: review, and both count.
_FINISHED = {TicketStatus.IN_REVIEW.value, TicketStatus.DONE.value}

#: Statuses that mean nobody has picked it up yet.
_NOT_STARTED = {
    TicketStatus.DRAFT.value,
    TicketStatus.BACKLOG.value,
    TicketStatus.TODO.value,
}


@dataclass
class ReleaseWindow:
    """When this release's window opens, and where that boundary came from.

    **The boundary is derived, not typed.** It used to be a required argument,
    and a hand-typed date nineteen days early produced a report claiming 93
    merged pull requests instead of 34, with 21 tickets wrongly flagged as
    shipped outside a release. Nothing caught it: every number was internally
    consistent and confidently wrong.

    `source` is on the payload for that reason. A boundary the platform computed
    from its own release records is a different kind of claim from one somebody
    passed in, and a reader deserves to know which they are looking at.
    """

    since: Optional[datetime]
    previous_version: Optional[str]
    label: Optional[str]
    source: str
    warning: Optional[str] = None
    #: When the window *closes*, for a version that has already shipped.
    #:
    #: `None` for the release in flight, which is still accumulating and has no
    #: end. A named past version does have one, and without it the window ran
    #: from that version's predecessor to *now* -- so a summary of v1.10.0 also
    #: contained everything in v1.11.0. That is the same unbounded-window
    #: failure the `since` boundary was derived to prevent, arriving from the
    #: other end.
    until: Optional[datetime] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "since": self.since.isoformat() if self.since else None,
            "until": self.until.isoformat() if self.until else None,
            "previous_version": self.previous_version,
            "label": self.label,
            "source": self.source,
        }


def _as_utc(stamp: Optional[datetime]) -> Optional[datetime]:
    """Attach UTC when the column gives a timestamp back naive.

    `released_at` is a plain `DateTime` in both dialects, so it round-trips
    without a timezone, while GitHub's `merged_at` is parsed as aware --
    comparing the two raises `TypeError: can't compare offset-naive and
    offset-aware datetimes` in the middle of assembling a release. The supplied
    path never hit this because it arrives as an ISO string and is parsed aware.
    """
    if stamp is not None and stamp.tzinfo is None:
        return stamp.replace(tzinfo=timezone.utc)
    return stamp


def _release_facts(
    releases: List[Release], version: Optional[str], items: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Version, whether it shipped, and how many of its tickets are still open.

    `open` counts tickets that have not reached review or done -- the figure a
    person means by "how much of this release is still moving", which is not the
    same as `with_gaps` next door: a ticket can be Done and still carry a gap
    (nobody attached the pull request), and one In Review with everything merged
    is complete but not closed.
    """
    row = _release_row(releases, version)
    return {
        "version": version,
        "status": (row.status.value if row is not None and row.status else None),
        "released_at": (
            _as_utc(row.released_at).isoformat()
            if row is not None and row.released_at is not None
            else None
        ),
        "tickets": len(items),
        "open": sum(1 for i in items if (i.get("status") or "") not in _FINISHED),
    }


def _version_key(version: Optional[str]) -> Optional[tuple]:
    """One comparable identity for a version string, semver-aware.

    `_release_row`, `_shipped_at` and `_predecessor` all compare with
    `semver_key` because "`1.11.0` and `v1.11.0` name one release, and a
    byte-exact lookup finds neither when the caller spells it the other way".
    Two sets built below did not, and both reopened the exact bug they were added
    to close: a release row spelled `1.13.0` against a ticket tagged `v1.13.0`
    made the ticket look untagged, so the report offered to overwrite a version
    somebody had set on purpose. Non-semver tags keep their own stripped string --
    `rancher-FINAL` has no numeric identity but is still equal to itself.
    """
    if version is None:
        return None
    text = version.strip()
    if not text:
        return None
    return semver_key(text) if is_semver(text) else ("literal", text)


def _is_planned(releases: List[Release], version: Optional[str]) -> bool:
    """Whether `version` is the slot being filled rather than the one being cut.

    Only ``PLANNED`` counts. A version with no row at all is *not* planned -- an
    unknown version is a question about a window, and answering it with an empty
    ticket list would report "nothing in this release" for what is really "no
    such release here".
    """
    row = _release_row(releases, version)
    return row is not None and row.status == ReleaseStatus.PLANNED


def _release_row(releases: List[Release], version: Optional[str]) -> Optional[Release]:
    """The row for `version` itself, semver-compared rather than string-matched.

    Same reasoning as `_shipped_at`: `1.11.0` and `v1.11.0` name one release, and
    a byte-exact lookup finds neither when the caller spells it the other way.
    """
    if version is None or not is_semver(version):
        return None
    wanted = semver_key(version)
    for r in releases:
        if is_semver(r.version) and semver_key(r.version) == wanted:
            return r
    return None


def _predecessor(releases: List[Release], version: Optional[str]) -> Optional[Release]:
    """The shipped release immediately *behind* `version`, by semver.

    For the release in flight this is `latest_release` and nothing changes --
    everything shipped is behind it. It differs for a version that has already
    gone out, and that difference is the whole point: `latest_release` is then
    the named version itself, so the window opened at the moment the release
    being summarised ended, and the report came back with nothing in it.
    """
    if version is None or not is_semver(version):
        return latest_release(releases)
    ceiling = semver_key(version)
    behind = [
        r
        for r in releases
        if r.status == ReleaseStatus.RELEASED
        and is_semver(r.version)
        and semver_key(r.version) < ceiling
    ]
    if not behind:
        return None
    return max(behind, key=lambda r: semver_key(r.version))


def _shipped_at(releases: List[Release], version: Optional[str]) -> Optional[datetime]:
    """When `version` itself shipped, or `None` if it has not.

    The release in flight has no end, so its window stays open. One that has
    shipped does, and leaving it open is how a summary of a past release quietly
    absorbs the release that followed it.
    """
    if version is None or not is_semver(version):
        return None
    # Semver-compared, not string-matched: `v1.11.0` and `1.11.0` are the same
    # release, and a byte-exact lookup silently finds neither when the caller
    # spells it the other way -- which reads as "this release has not shipped",
    # the exact answer that leaves the window open.
    wanted = semver_key(version)
    for r in releases:
        if (
            r.status == ReleaseStatus.RELEASED
            and is_semver(r.version)
            and semver_key(r.version) == wanted
        ):
            return _as_utc(r.released_at)
    return None


def resolve_window(
    session: Session,
    *,
    organization_id: str,
    project_id: str,
    since: Optional[datetime] = None,
    window_label: Optional[str] = None,
    version: Optional[str] = None,
) -> ReleaseWindow:
    """The window a release covers: from the release behind it, to when it shipped.

    A supplied `since` wins and is marked `supplied` -- a caller may override
    the boundary, but must never be *required* to supply one, because being
    required to is how a wrong one gets typed.

    **`version` moves both ends.** Without it the window is the one in flight:
    from the last shipped release to now. Naming a version that has already gone
    out asks a different question -- what was *in* that release -- and answering
    it with the in-flight window is not an approximation, it is a different
    release. Summarising BPAI v1.11.0 an hour after it shipped returned its ten
    tickets against a window that opened when it ended: zero merged pull
    requests, every ticket flagged as having no code.

    Ordered by semver rather than by date, following `latest_release`: several
    repositories publish the same cross-repo version minutes apart, so the
    highest version is a steadier answer than the most recent timestamp.
    """
    releases = _project_releases(session, organization_id, project_id)
    # **The closing bound survives an override, because `--since` overrides the
    # *start*.** That is what the flag says it does, and the two boundaries
    # answer different questions: choosing where to begin counting is not a
    # statement that a release which shipped three weeks ago should keep
    # absorbing everything merged since.
    until = _shipped_at(releases, version)

    if since is not None:
        return ReleaseWindow(
            since=since,
            previous_version=None,
            label=window_label,
            source="supplied",
            until=until,
        )

    previous = _predecessor(releases, version)
    if previous is None:
        # A first release legitimately has nothing behind it.
        return ReleaseWindow(
            since=None,
            previous_version=None,
            label=window_label or "everything so far (no previous release)",
            source="derived",
            until=until,
        )
    if previous.released_at is None:
        # **Say so rather than silently covering all of history.** A row marked
        # released with no date cannot bound anything, and treating that as
        # "since the beginning of time" is precisely the failure this function
        # exists to prevent -- it just arrives from the data instead of from a
        # keyboard.
        return ReleaseWindow(
            since=None,
            previous_version=previous.version,
            label=window_label or f"everything so far ({previous.version} has no date)",
            source="derived",
            warning=(
                f"{previous.version} is marked released but has no release date, "
                "so this window is unbounded and covers work from earlier "
                "releases. Set its date to bound the window."
            ),
            until=until,
        )

    stamped = _as_utc(previous.released_at)
    assert stamped is not None  # guarded by the `released_at is None` branch above
    if until is not None:
        derived_label = f"{previous.version} \u2192 {version}"
    else:
        derived_label = f"since {previous.version} ({stamped.date().isoformat()})"
    return ReleaseWindow(
        since=stamped,
        previous_version=previous.version,
        label=window_label or derived_label,
        source="derived",
        until=until,
    )


class _NarrativeIndex:
    """The prose a Claude session wrote about each ticket on this release.

    **The one field in a release summary with no other source.** Everything
    else on an item -- who worked on it, which pull requests carried it, whether
    they merged -- is a fact this service derives. The sentence explaining what
    the change *meant to somebody using the product* is written by a narrator
    and stored on `summary_items`, and nothing can re-derive it.

    Joined back on read rather than frozen into the release. A release summary
    is narrated once and then the facts around it keep improving: somebody
    attaches a pull request the matcher missed, an assignee gets mapped to a
    real person. Freezing the whole line at save time would preserve the
    typos along with the prose, and the closing window boundary already makes a
    shipped release's facts stable -- see `resolve_window`.

    Read inside a SAVEPOINT, and failure is a missing narrative rather than a
    broken release report: on Postgres a failed statement aborts the enclosing
    transaction, so an image running ahead of `alembic upgrade head` would
    otherwise poison the caller's session rather than merely losing the prose.
    """

    def __init__(self, session: Session, *, project_id: str, version: Optional[str]):
        self._by_ticket: Dict[int, str] = {}
        if not version:
            return
        try:
            with session.begin_nested():
                summary = session.exec(
                    select(Summary)
                    .where(
                        Summary.project_id == project_id,
                        Summary.window_spec == release_spec(version),
                        Summary.superseded_by_id.is_(None),
                    )
                    .order_by(Summary.created_at.desc())
                ).first()
                if summary is None:
                    return
                rows = session.exec(
                    select(SummaryItem).where(SummaryItem.summary_id == summary.id)
                ).all()
        except SQLAlchemyError as exc:
            logger.warning("Release narrative lookup failed: %s", exc)
            return
        for row in rows:
            if row.ticket_id is not None and row.body_markdown:
                self._by_ticket[row.ticket_id] = row.body_markdown

    def for_ticket(self, ticket_id: Optional[int]) -> Optional[str]:
        if ticket_id is None:
            return None
        return self._by_ticket.get(ticket_id)


def _display_ref(project: Project, ticket: Ticket) -> str:
    """What to print, and what a reader can follow.

    **The board's key wins.** Both names format as `ALIAS-123`, and they are
    different tickets: of BPAI's 221 tickets, 22 strings name one issue in
    Linear and another one here. A customer following the internal number lands
    on the wrong ticket, so the reference shown is the one their board agrees
    with. The other name is still carried, on `innoday_ref`.
    """
    if ticket.external_ticket_id:
        return ticket.external_ticket_id
    if project.alias and ticket.project_ref_number is not None:
        return f"{project.alias}-{ticket.project_ref_number}"
    return str(ticket.id)


class _PeopleIndex:
    """GitHub logins and board names to "Alex Y.", resolved once per release.

    A handle is not a person. `(kengsc)` in a release summary tells a customer
    nothing, and the mapping to say otherwise already exists -- it was simply
    never consulted on this path.

    Memoised because the same few authors appear on most pull requests, and
    every lookup that misses is a query. An unresolved login is returned as
    itself rather than dropped: somebody whose credit cannot be rendered is
    still somebody, and the raw handle showing up is the signal that identity
    mapping needs attention.
    """

    def __init__(self, session: Session, organization_id: str) -> None:
        self._session = session
        self._org = organization_id
        self._by_login: Dict[str, Optional[str]] = {}

    def name_for(self, login: Optional[str]) -> Optional[str]:
        if not login:
            return None
        if login not in self._by_login:
            self._by_login[login] = self._lookup(login)
        return self._by_login[login]

    def is_resolved(self, name: Optional[str]) -> bool:
        """Whether `name` is a real person's name rather than a raw GitHub login.

        `name_for` falls back to the login when a login maps to nobody, so its
        answer is two different kinds of thing wearing one type. Comparing it
        against `name_for_ticket`'s resolved short name then disagreed on every
        project where the ticket side is mapped and the GitHub side is not --
        the commonest configuration, and never evidence about who owns the work.

        Answered from the cache `name_for` already filled, so no extra query.
        """
        if not name:
            return False
        return name in {
            resolved for login, resolved in self._by_login.items() if resolved != login
        }

    def name_for_ticket(self, ticket: Ticket) -> Optional[str]:
        """The ticket's owner, resolved if we can and the board's word if not."""
        if ticket.assigned_to:
            try:
                with self._session.begin_nested():
                    user = self._session.get(User, ticket.assigned_to)
                    if user is not None:
                        return user.get_short_name()
            except SQLAlchemyError as exc:
                logger.warning("Could not resolve assignee: %s", exc)
        return ticket.assignee or None

    def _lookup(self, login: str) -> str:
        """Resolve one login, and never let the attempt cost anything.

        Inside a SAVEPOINT because a failed statement poisons a Postgres
        transaction: without it, one bad lookup would abort the whole release
        assembly at whatever the *next* query happened to be, and the traceback
        would point somewhere unrelated.

        Falling back to the raw login rather than raising, for the same reason
        a repository that fails to fetch renders as quiet: putting a name on a
        credit line is the least important thing this service does, and it must
        not be able to lose the release.
        """
        try:
            with self._session.begin_nested():
                match = IdentityResolutionService.resolve(
                    self._session,
                    organization_id=self._org,
                    project_id=None,
                    platform=IdentityPlatform.GITHUB,
                    assignee=BoardAssignee(
                        display_name=login, email=None, board_user_id=None
                    ),
                )
                if match is not None:
                    return match.user.get_short_name()
        except SQLAlchemyError as exc:
            # **Database errors only.** A broader `except Exception` here
            # swallowed an AttributeError -- this code read `match.user_id`,
            # which does not exist -- and turned a straightforward crash into
            # every credit line silently falling back to the raw handle. A
            # wrong answer that looks like a missing mapping is far worse than
            # a traceback; only a test caught it.
            logger.warning("Could not resolve GitHub login %s: %s", login, exc)
        return login


class NoGitHubCredential(Exception):
    """The organisation has no usable GitHub credential.

    Its own exception rather than an empty result, because "nothing shipped" and
    "we cannot see GitHub" must never render as the same report. The first is a
    quiet release; the second is a setup problem, and a release built on it
    would confidently claim an empty window.
    """


class ReleaseContentService:
    """Builds the `content` block a release brief carries."""

    def __init__(
        self,
        session: Session,
        *,
        client_factory=None,
    ) -> None:
        self.session = session
        # Same resolution every other GitHub read here uses, and injectable for
        # the same reason: a test needs neither Vault nor a network.
        self._fetcher = CodeActivityFetcher(session, client_factory=client_factory)

    def repositories(self, project_id: str) -> List[Repository]:
        """The project's repositories, from the persisted link.

        **Not a topic search.** Topics are how a repository is *discovered* and
        attached; `project_repositories` is what it is actually attached to. A
        release should tag what belongs to the project, not what currently
        happens to match a string.
        """
        return self._fetcher.project_repositories(project_id)

    def coverage_warning(
        self,
        *,
        project_id: str,
        organization_id: str,
        covering: List[str],
        previous_version: Optional[str],
    ) -> Optional[str]:
        """Named repositories the last release had and this one does not.

        **A release covering less than the last one is the loudest signal
        available that something is wrong, and it costs nothing to say.** One
        covered six repositories instead of seven, dropped thirteen merged pull
        requests, and reported the smaller number in silence, because a sync had
        deactivated a project link seven minutes earlier.

        Only a shrink is reported. Growing is ordinary -- a repository joins a
        project and the next release covers it -- and warning about that would
        train people to ignore the warning that matters.

        Silent when the previous release predates `repo_names`, which is every
        release shipped before it existed. A record of what a release contained
        cannot be reconstructed afterwards: the live links have moved on, which
        is the whole problem. Guessing from them would manufacture the agreement
        this is testing for.
        """
        if not previous_version:
            return None
        previous = self.session.exec(
            select(Release).where(
                Release.project_id == project_id,
                Release.organization_id == organization_id,
                Release.version == previous_version,
                Release.deleted_at.is_(None),
            )
        ).first()
        if previous is None or not previous.repo_names:
            return None

        missing = sorted(set(previous.repo_names) - set(covering))
        if not missing:
            return None
        return (
            f"{previous_version} covered {len(previous.repo_names)} repositories "
            f"and this release covers {len(covering)}. Missing: "
            f"{', '.join(missing)}. Check the project's repository links before "
            "cutting -- a sync can deactivate one."
        )

    def design_repositories(self, project_id: str) -> Set[str]:
        """Names of repositories this project classifies as design work.

        They are still released and still tagged -- what changes is where their
        work is narrated. A demo repository's layout experiments belong in a
        section of their own, not folded into the story of what shipped to
        customers.

        The layer is read from the project link, not the repository: a repo can
        be a demo to one project and the real thing to another.
        """
        rows = self.session.exec(
            select(Repository.name)
            .join(ProjectRepository, ProjectRepository.repository_id == Repository.id)
            .where(
                ProjectRepository.project_id == project_id,
                ProjectRepository.is_active.is_(True),
                ProjectRepository.layer == RepositoryLayer.DESIGN,
            )
        ).all()
        return {name for name in rows}

    def project_tickets(self, project_id: str) -> List[Ticket]:
        """Every live ticket in the project, for resolving what a branch names.

        Wider than the release on purpose: see `_ticket_view`.
        """
        return list(
            self.session.exec(
                select(Ticket).where(
                    Ticket.project_id == project_id,
                    Ticket.deleted_at.is_(None),
                )
            ).all()
        )

    def candidate_tickets(self, project_id: str) -> List[Ticket]:
        """Started tickets carrying **no release at all**, for proposing against.

        The other half of the proposal loop. A pull request with no ticket needs
        a ticket suggested; a ticket whose work plainly shipped needs adding to
        the release. "Implement Small UI Items v1.11.0" sat In Test, on no
        release, while four of its checklist items merged inside this window --
        and nothing in the report could mention it, because a payload built from
        pull requests only ever sees tickets that pull requests point at.

        **Carrying no release, not "a release other than this one".** The filter
        used to be ``release != version``, which swept in every ticket correctly
        tagged for the *next* release and offered a remedy that would overwrite
        it: asked about BPAI v1.12.0 it proposed moving BPAI-410 off v1.12.0 --
        the release it already belonged to -- and asked about v1.11.0, which had
        shipped three days earlier, it proposed adding twenty-five tickets to it.
        A ticket that carries a different real version is either correctly placed
        or a *conflict*; neither is a candidate. See `conflicted_tickets`.

        Scoped to started work: a backlog of two hundred planned tickets is not
        a list of candidates, it is noise. Finished tickets are not scoped here
        either, but they are not missed -- a `done` ticket on no release whose
        code merged in the window arrives through the pull-request side as
        `shipped_untagged`, which is the louder finding of the two.

        Takes no version, and that is the point: "started, on no release" is a
        fact about the project, not about the version being asked after. It is
        the caller that decides the answer only belongs to the release being cut.
        """
        started = {TicketStatus.IN_PROGRESS.value, TicketStatus.IN_REVIEW.value}
        rows = self.session.exec(
            select(Ticket).where(
                Ticket.project_id == project_id,
                Ticket.deleted_at.is_(None),
            )
        ).all()
        return [
            t
            for t in rows
            if (t.status.value if t.status else "") in started
            and not (t.release or "").strip()
        ]

    def conflicted_tickets(
        self, project_id: str, shipped_versions: Set[tuple]
    ) -> List[Ticket]:
        """Unfinished tickets pointing at a version that has already shipped.

        Shipping a version deliberately touches no ticket -- `_shipped_stamp`
        records what it found rather than closing the work, so `open_ticket_count`
        keeps answering "how much of this was never finished". The cost is that
        nothing then *says* a ticket is stranded on a release that went out
        without it. BPAI-407 and BPAI-411 sat In Review and In Progress on
        v1.11.0 for three days after it shipped, and every report described them
        as candidates for the release being cut -- which is the one thing they
        were not, because they already carried a version.

        Not an error to correct automatically. Whether the ticket moves forward
        or is split apart is a judgement about the work, so this states the
        situation and leaves the decision.
        """
        finished = {TicketStatus.DONE.value, TicketStatus.CANCELLED.value}
        rows = self.session.exec(
            select(Ticket).where(
                Ticket.project_id == project_id,
                Ticket.deleted_at.is_(None),
            )
        ).all()
        return [
            t
            for t in rows
            if _version_key(t.release) in shipped_versions
            and (t.status.value if t.status else "") not in finished
        ]

    def release_tickets(self, project_id: str, version: Optional[str]) -> List[Ticket]:
        """Tickets carrying this release's version.

        Byte-exact on `Ticket.release`, the same loose join the rest of the
        platform uses -- there is no foreign key between a ticket and a release.
        No version means no ticket scope at all, which is a real case: a hotfix
        targets a commit, not a planned set of work.
        """
        if not version:
            return []
        return list(
            self.session.exec(
                select(Ticket).where(
                    Ticket.project_id == project_id,
                    Ticket.release == version,
                    Ticket.deleted_at.is_(None),
                )
            ).all()
        )

    async def assemble(
        self,
        *,
        project: Project,
        organization_id: str,
        since: Optional[datetime] = None,
        window_label: Optional[str] = None,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        api = self._fetcher._client_factory(organization_id)
        if api is None:
            raise NoGitHubCredential(
                "This organization has no GitHub credential stored, so the "
                "release cannot be assembled here."
            )

        repos = self.repositories(project.id)
        if not repos:
            raise NoGitHubCredential(
                "No repositories are linked to this project, so there is "
                "nothing to release. Run `innoday sync` to attach them."
            )

        # **The version is resolved first, because the window depends on it.**
        # It used to be resolved after, which was harmless only while the window
        # ignored it: naming an already-shipped version then produced that
        # release's tickets measured against the *current* window.
        # **Whether the caller named the version decides two things below**, so it
        # is recorded before resolution overwrites the answer.
        named = version is not None
        if version is None:
            version = current_release_version(
                self.session,
                organization_id=organization_id,
                project_id=project.id,
            )

        # **A release being *planned* gets no window, and that is the whole
        # separation.** A window is derived from dates, and two unreleased
        # versions occupy the same dates: `_predecessor` returns the same newest
        # released row for both and `_shipped_at` returns `None` for both, so
        # slot 1 and slot 2 were handed byte-identical windows and therefore
        # byte-identical `included`, `unticketed` and `commit_count`. BPAI's
        # v1.12.0 and v1.13.0 differed only in which tickets carried the string.
        #
        # Slot 2 is what is being *filled*, not what is being cut. Its content is
        # exactly the tickets somebody has put on it -- membership, which is
        # unambiguous -- and nothing derived from a stretch of time it shares
        # with the release ahead of it. So the pull-request pass is skipped
        # entirely: no GitHub calls, no window, no candidates.
        # **Only a version the caller *named*.** `current_release_version` prefers
        # IN_PROGRESS but falls back to the lowest PLANNED above the high-water
        # mark, and `releases create` defaults to PLANNED -- so on a project whose
        # next release has not been started, the unversioned call resolved to a
        # planned version and short-circuited. Every merged pull request,
        # candidate and unticketed pull request vanished from the default report,
        # which is the "nothing shipped" and "we could not look" collapse this
        # module exists to prevent. Asking for the release in flight must answer
        # about the window even when the slot is only planned.
        if named and _is_planned(
            _project_releases(self.session, organization_id, project.id), version
        ):
            return self._planned_only(
                project=project,
                organization_id=organization_id,
                version=version,
                repos=repos,
                since=since,
                window_label=window_label,
            )

        # **The window is derived here, not required from the caller.** A
        # hand-typed boundary nineteen days early once produced a report
        # claiming 93 merged pull requests instead of 34; a supplied one still
        # wins, and the payload says which kind it got.
        window = resolve_window(
            self.session,
            organization_id=organization_id,
            project_id=project.id,
            since=since,
            window_label=window_label,
            version=version,
        )
        since = window.since
        window_label = window.label

        design = self.design_repositories(project.id)
        results = await asyncio.gather(
            *(self._one(api, repo, since, window.until) for repo in repos)
        )
        # **A design repository's pull requests are reported under `design`, and
        # only there.** `included` was every merged pull request in the window
        # with no filter at all, so bps-ui-demo's thirteen contributed to BPAI
        # v1.11.0's thirty-five "merged pull requests" *and* appeared in full
        # beneath `design` -- the same work counted twice, and a reader of
        # `included` seeing layout experiments as shipped product. Twenty-two
        # shipped. `commit_count`, `repos` and `truncated_repos` deliberately
        # still span every repository: what the release *touched* is a different
        # question from what it shipped as product, and narrowing both would
        # hide a design repo that failed to fetch.

        included: List[Dict[str, Any]] = []
        outstanding: List[Dict[str, Any]] = []
        abandoned: List[Dict[str, Any]] = []
        truncated_repos: List[str] = []
        total_commits = 0
        for activity in results:
            if activity.merged and activity.repo not in design:
                included.append(
                    {
                        "repo": activity.repo,
                        "commit_count": activity.commit_count,
                        "prs": [_public(pr) for pr in activity.merged],
                    }
                )
            if activity.opened:
                outstanding.append(
                    {
                        "repo": activity.repo,
                        "prs": [_public(pr) for pr in activity.opened],
                    }
                )
            if activity.abandoned:
                abandoned.append(
                    {
                        "repo": activity.repo,
                        "prs": [_public(pr) for pr in activity.abandoned],
                    }
                )
            if activity.truncated:
                truncated_repos.append(activity.repo)
            total_commits += activity.commit_count

        payload: Dict[str, Any] = {
            "window": window.as_dict(),
            "window_label": window_label,
            "commit_count": total_commits,
            # **Every repository, not just the ones with something in them.** A
            # repo that was quiet this window still gets tagged, so a report
            # that omitted it would understate what the release touches.
            "repos": [r.name for r in repos],
            "included": included,
            "outstanding": outstanding,
            # Closed without merging. Not part of the release; reported because
            # "this ticket's only pull request was abandoned" and "nobody wrote
            # any code for this ticket" are different problems.
            "abandoned": abandoned,
        }
        warnings: List[str] = []
        if window.warning:
            warnings.append(window.warning)
        shrink = self.coverage_warning(
            project_id=project.id,
            organization_id=organization_id,
            covering=[r.name for r in repos],
            previous_version=window.previous_version,
        )
        if shrink:
            warnings.append(shrink)
        if warnings:
            payload["warnings"] = warnings

        if truncated_repos:
            # Named, not counted. A number says the report is short; the names
            # say which repository to go and look at.
            payload["truncated_repos"] = sorted(truncated_repos)

        # The key a saved summary is filed under. Emitted rather than left to
        # the narrator to construct: a re-spelling is a permanent cache miss,
        # and `release:v1.11.0` is not a shape anybody should be assembling by
        # hand from two other fields.
        payload["window_spec"] = release_spec(version) if version else None

        payload.update(
            await self._ticket_view(
                project=project,
                organization_id=organization_id,
                version=version,
                results=results,
                design=design,
                api=api,
                repos=repos,
                named=named,
            )
        )
        return payload

    def _planned_only(
        self,
        *,
        project: Project,
        organization_id: str,
        version: Optional[str],
        repos: List[Repository],
        since: Optional[datetime] = None,
        window_label: Optional[str] = None,
    ) -> Dict[str, Any]:
        """The planned release: its tickets, and deliberately nothing else.

        Same keys as a full assembly so no caller has to branch on shape, but the
        window-derived halves are empty rather than absent -- `included: []` says
        "nothing has been attributed to this yet", which is true, where a missing
        key says "this payload is a different kind" and invites a `KeyError`.

        No GitHub call is made at all. That is not only an economy: any window
        this could ask for is the window of the release ahead of it, and
        answering with it is exactly the bug.
        """
        tickets = self.release_tickets(project.id, version)
        all_tickets = self.project_tickets(project.id)
        people = _PeopleIndex(self.session, organization_id)
        narrative = _NarrativeIndex(
            self.session, project_id=project.id, version=version
        )
        releases = _project_releases(self.session, organization_id, project.id)
        every_item = [
            self._item(project, ticket, [], people, narrative) for ticket in tickets
        ]
        items = [i for i in every_item if not i["is_design"]]
        design_items = sorted(
            (i for i in every_item if i["is_design"]), key=lambda i: i["ref"]
        )
        items.sort(key=lambda i: (i["state"] != ReleaseVerdict.SHIPPED, i["ref"]))
        conflicts = self._conflicts(
            project=project, releases=releases, people=people, version=version
        )
        # **Counted from the items, not written as zeroes.** They were literals,
        # so a planned release carrying two tickets that each had gaps reported
        # `tickets: 2, complete: 0, with_gaps: 0` -- arithmetic that cannot be
        # true, on the field the MCP tool tells callers to drive to zero before
        # cutting. Every planned release read as ready to ship.
        complete = sum(1 for i in items if not i["gaps"])
        unresolved = [i for i in items if i["state"] in _UNRESOLVED_ITEM_STATES]
        warnings: List[str] = []
        if since is not None or window_label:
            # The route accepts `--since`; this path has no window to apply it to.
            # Ignoring it silently is how a caller who overrode the boundary comes
            # to believe it was honoured.
            warnings.append(
                f"{version} is planned, so it has no window: it is the slot being "
                "filled, not the one being cut. The boundary you supplied was not "
                "applied -- ask about the release in progress to use it."
            )
        payload: Dict[str, Any] = {
            "window": None,
            "window_label": None,
            "commit_count": 0,
            "repos": [r.name for r in repos],
            "included": [],
            "outstanding": [],
            "abandoned": [],
            "window_spec": release_spec(version) if version else None,
            "release": version,
            "items": items,
            "unticketed": [],
            "off_release": [],
            "conflicts": conflicts,
            # A named planned version resolved to a row, by definition -- so this
            # is always null here. Present because the shape must match, which is
            # the promise this method's docstring makes.
            "unknown_version": None,
            "design": {"items": design_items, "unticketed": []},
            "ref_collisions": [
                {"ref": ref, "board": board.summary, "internal": internal.summary}
                for ref, board, internal in colliding_refs(
                    project.alias or "", all_tickets
                )
            ],
            "unresolved": {
                "tickets_without_code": [
                    {"ref": i["ref"], "title": i["title"], "status": i["status"]}
                    for i in unresolved
                ],
                "pull_requests_without_tickets": [],
                "tickets_without_release": [],
            },
            "release_record": _release_facts(releases, version, items),
            "totals": {
                "tickets": len(items),
                "complete": complete,
                "with_gaps": len(items) - complete,
                "shipped_untagged": 0,
                "off_release": 0,
                "candidates": 0,
                "conflicts": len(conflicts),
                "unticketed": 0,
                "unresolved": len(unresolved),
            },
            "planned": True,
        }
        if warnings:
            payload["warnings"] = warnings
        return payload

    async def _one(
        self,
        api: GitHubAPI,
        repo: Repository,
        since: Optional[datetime],
        until: Optional[datetime] = None,
    ) -> "_RepoActivity":
        addressed = _owner_and_name(repo)
        if addressed is None:
            return _RepoActivity(repo.name)
        owner, name = addressed

        # Three calls rather than one, because the three buckets have genuinely
        # different windows.
        #
        # *Closed* is windowed: a pull request merged before this window belongs
        # to the previous release, and counting it again is the double-counting
        # this seam keeps producing.
        #
        # *Open* is not windowed. A pull request nobody has touched in four
        # months is still outstanding -- arguably the most outstanding thing
        # there is -- and filtering open ones by `updated_at` hid exactly those.
        #
        # `count_commits` is a single request; see its docstring.
        closed, opened, commit_count = await asyncio.gather(
            api.list_pull_requests(owner, name, state="closed", since=since),
            api.list_pull_requests(owner, name, state="open", since=None),
            api.count_commits(owner, name, since=since, until=until),
            return_exceptions=True,
        )
        # One repository failing must not lose the whole release report. It
        # renders as a quiet repo, which is wrong but visible next to its
        # siblings -- an exception here would show nothing at all.
        truncated = False
        if isinstance(closed, BaseException):
            logger.warning("PR fetch failed for %s/%s: %s", owner, name, closed)
            closed_prs: List[Dict[str, Any]] = []
        else:
            closed_prs, closed_truncated = closed
            truncated = truncated or closed_truncated
        if isinstance(opened, BaseException):
            logger.warning("Open PR fetch failed for %s/%s: %s", owner, name, opened)
            open_prs: List[Dict[str, Any]] = []
        else:
            open_prs, open_truncated = opened
            truncated = truncated or open_truncated
        if isinstance(commit_count, BaseException):
            logger.warning(
                "Commit count failed for %s/%s: %s", owner, name, commit_count
            )
            commit_count = 0

        activity = _RepoActivity(repo.name, commit_count=commit_count)
        activity.truncated = truncated

        for pr in closed_prs:
            merged_at = parse_iso_utc(pr.get("merged_at"))
            if merged_at is None:
                # Closed without merging. It shipped nothing, so it is not part
                # of the release -- but it is not *nothing* either: a ticket
                # whose only pull request was abandoned used to be
                # indistinguishable from a ticket with no code written at all,
                # and those two need different conversations.
                activity.abandoned.append(_entry(pr))
            elif (since is None or merged_at >= since) and (
                until is None or merged_at <= until
            ):
                # `until` is set only for a version that has already shipped.
                # Without it, summarising a past release swept in everything
                # merged since -- the release that followed it, reported as part
                # of the one before.
                activity.merged.append(_entry(pr))

        for pr in open_prs:
            activity.opened.append(_entry(pr))

        return activity

    # ------------------------------------------------------------- tickets

    async def _ticket_view(
        self,
        *,
        project: Project,
        organization_id: str,
        version: Optional[str],
        results: List["_RepoActivity"],
        design: Set[str],
        api: Optional[GitHubAPI] = None,
        repos: Optional[List[Repository]] = None,
        named: bool = False,
    ) -> Dict[str, Any]:
        """The release as tickets, which is how a person reads one.

        Everything above this is organised by repository, because that is how
        GitHub is organised. Nobody outside the team thinks in repositories: a
        single change routinely spans three, and one repository routinely holds
        four unrelated changes. So the release is re-expressed with the ticket
        as the unit, each carrying the pull requests that delivered it.

        Three groups fall out of the join, and all three matter:

        * **items** -- tickets on this release. Including the ones with no
          merged code, which were previously invisible: the payload was built
          from pull requests, so a ticket nobody had written code for simply did
          not appear anywhere.
        * **off_release** -- tickets that are not on this release at all, each
          with its own verdict. Work that merged in this window against an
          untagged ticket is `shipped_untagged`, which is delivered work missing
          from the notes; a started ticket with nothing merged here is only a
          candidate. They were one flat list until a ticket that was In Test, on
          no release, with code merged to main read exactly like one where
          nothing had happened.
        * **unticketed** -- merged pull requests naming no ticket at all.
        """
        tickets = self.release_tickets(project.id, version)
        # **Index every ticket in the project, not just this release's.**
        # Mis-tagged work is a pull request naming a ticket that is *not* on the
        # release, so an index built from the release's own tickets can never
        # find one -- it would fall through to "unticketed" and look like work
        # nobody had filed, which is a different and less alarming problem.
        all_tickets = self.project_tickets(project.id)
        by_ref = tickets_by_ref(project.alias or "", all_tickets)
        # Every prefix the index answers to, not just the project's alias: a
        # board key need not share it (a Linear `ZZ-9` on a project aliased
        # something else is ordinary).
        pattern = ticket_ref_pattern(*ref_prefixes(by_ref), project.alias or "")
        on_this_release = {t.id for t in tickets}

        people = _PeopleIndex(self.session, organization_id)
        # Read before any derivation: somebody attached these by hand, and no
        # pattern match should be able to overrule that.
        attached = attached_pull_requests(self.session, project.id)
        by_id = {t.id: t for t in all_tickets}
        prs_for: Dict[int, List[Dict[str, Any]]] = {}
        mis_tagged: Dict[str, Dict[str, Any]] = {}
        unticketed: List[Dict[str, Any]] = []
        design_entries: List[Dict[str, Any]] = []

        for activity in results:
            is_design = activity.repo in design

            for pr, merged in [(pr, True) for pr in activity.merged] + [
                (pr, False) for pr in activity.opened
            ]:
                # **`body` is deliberately not copied.** It is matching input,
                # sometimes thousands of words of checklist, and putting it in
                # the payload would bury the report it is meant to inform.
                entry = {
                    "repo": activity.repo,
                    "number": pr.get("number"),
                    "title": pr.get("title"),
                    "url": pr.get("url"),
                    "branch": pr.get("branch"),
                    "merged": merged,
                    "design": is_design,
                    "person": people.name_for(pr.get("author")),
                }
                manual = attached.get((activity.repo, pr.get("number")))
                if manual is not None:
                    ticket = by_id.get(manual)
                    entry["matched_by"] = "manual"
                else:
                    ticket = ticket_for_pull_request(
                        pr.get("branch"),
                        pr.get("title"),
                        by_ref,
                        pattern,
                        body=pr.get("body"),
                    )
                    if ticket is not None:
                        entry["matched_by"] = _matched_by(pr, by_ref, pattern)
                if ticket is not None and manual is None:
                    # **Never a hand-attached link.** Somebody pinned that one
                    # deliberately, and the comment above says no pattern match
                    # may overrule it -- contesting it is exactly that.
                    entry.update(_contest(entry, ticket, people))
                if ticket is not None and ticket.id in on_this_release:
                    prs_for.setdefault(ticket.id, []).append(entry)
                elif ticket is not None:
                    # **Named a ticket that is not on this release -- open or
                    # merged.** Only merged ones used to reach here, so an open
                    # pull request against an untagged ticket fell through every
                    # branch below and landed in no bucket at all. That is 23 of
                    # BPAI's 35 open pull requests, across 17 tickets, and it is
                    # exactly the evidence "a pull request is active against a
                    # ticket with no release" needs: without it the report cannot
                    # tell a ticket somebody is working on from one nobody has
                    # touched. It also makes the `started_untagged` arm of
                    # `_off_release` reachable, which it never was before.
                    ref = _display_ref(project, ticket)
                    row = mis_tagged.setdefault(
                        ref,
                        {
                            "ref": ref,
                            # **The id, not only the command that uses it.** The
                            # remedy string carries `--ticket-id 1422` and a
                            # caller that is not a shell cannot act on a
                            # sentence: the UI had to either parse the command
                            # back apart or offer nothing but a copyable
                            # instruction. `items` has carried `ticket_id` all
                            # along; these rows are the same tickets seen from
                            # the other side.
                            "ticket_id": ticket.id,
                            "url": ticket.url,
                            "title": ticket.summary,
                            "release": ticket.release,
                            "prs": [],
                            "remedy": (
                                f"innoday tickets update --ticket-id {ticket.id} "
                                f"--release {version}"
                                if version
                                else "set this ticket's release"
                            ),
                        },
                    )
                    row["prs"].append(entry)
                elif merged:
                    # The description travels here and nowhere else: it is the
                    # evidence a proposal is argued from, and trimmed because a
                    # checklist can run to thousands of words.
                    proposal_entry = dict(entry)
                    proposal_entry["description"] = (pr.get("body") or "")[:600] or None
                    # The verdict, on the row, rather than implied by which list
                    # the row landed in. A caller reading `design.unticketed`
                    # had to know that being in it *was* the verdict.
                    proposal_entry["state"] = (
                        ReleaseVerdict.UNTICKETED_DESIGN.value
                        if is_design
                        else ReleaseVerdict.UNTICKETED.value
                    )
                    (design_entries if is_design else unticketed).append(proposal_entry)

        # **Evidence, only for the ones that need it.** A pull request that
        # matched nothing still says what it did, most plainly in its commits.
        # Fetching them for the whole release would be thirty-four extra
        # requests to enrich seven that already resolved; fetching them for the
        # unmatched bounds the cost by the size of the problem.
        if api is not None and unticketed:
            await self._add_commits(api, repos or [], unticketed)

        narrative = _NarrativeIndex(
            self.session, project_id=project.id, version=version
        )
        every_item = [
            self._item(project, ticket, prs_for.get(ticket.id, []), people, narrative)
            for ticket in tickets
        ]
        # **A design ticket is still a ticket.** Skipping design repositories in
        # the join made tickets like "Design Small UI Items" report `no_code` --
        # a gap to go and chase that was really seventeen merged pull requests
        # sitting one bucket away. Match everything, then split by where the
        # work landed: an item is design work when every pull request on it is.
        items = [i for i in every_item if not i["is_design"]]
        design_items = sorted(
            (i for i in every_item if i["is_design"]), key=lambda i: i["ref"]
        )
        items.sort(key=lambda i: (i["state"] != ReleaseVerdict.SHIPPED, i["ref"]))

        complete = sum(1 for i in items if not i["gaps"])
        releases = _project_releases(self.session, organization_id, project.id)
        row = _release_row(releases, version)
        # **Only the release being cut may take a candidate.** A version that has
        # shipped cannot absorb anything, and the one being planned is not the
        # one being filled -- offering either the same list is what made three
        # different releases answer with the same report.
        #
        # **A version with no row still gets them.** Suppressing on an absent row
        # would read "this release takes no candidates" for what is really "this
        # project has no release records", and would empty the most useful half
        # of the payload for every project that has never registered one --
        # which is most of them. The claim being made is narrow and evidenced:
        # candidates are withheld only where a row positively says the version
        # has already gone out, or is the slot behind the one being cut.
        unknown_version: Optional[str] = None
        if row is not None:
            cutting = row.status == ReleaseStatus.IN_PROGRESS
        else:
            # **Two situations produce no row, and only one is a mistake.** A
            # project that has never registered a release has nothing to check a
            # version against, and withholding candidates there would empty the
            # most useful half of the payload for most projects. A project that
            # *does* keep releases, asked about a version not among them, was
            # handed a typo's worth of authority: `--version v9.9.9` returned the
            # in-flight window branded with the typo, and a copy-pasteable command
            # tagging real tickets onto a phantom version.
            has_records = any(r.version for r in releases)
            cutting = not (named and has_records)
            if not cutting:
                unknown_version = version
        off_release = self._off_release(
            project=project,
            version=version,
            matched=mis_tagged,
            people=people,
            propose=cutting,
            outstanding_versions={
                key
                for key in (
                    _version_key(r.version)
                    for r in releases
                    if r.status in (ReleaseStatus.PLANNED, ReleaseStatus.IN_PROGRESS)
                )
                if key is not None
            },
        )
        conflicts = self._conflicts(
            project=project, releases=releases, people=people, version=version
        )
        return {
            "release": version,
            "items": items,
            "unticketed": unticketed,
            # **Every ticket gets a verdict, including the ones off the
            # release.** These used to be two lists with no state between them:
            # `mis_tagged` for work that merged naming an untagged ticket, and
            # `candidates` for started tickets nobody had tagged. A ticket that
            # is In Test, on no release, and has code merged to main is the
            # loudest thing in a release report -- and it was a flat entry in a
            # list of fifteen, indistinguishable from a ticket where nothing had
            # happened at all.
            "off_release": off_release,
            # **Tickets carrying a version that already shipped, still unfinished.**
            # Neither members nor candidates: they have a release, so nothing here
            # should propose giving them one, and the release they have has gone
            # out without them. Kept in its own list because conflating it with
            # candidates is what produced a remedy offering to overwrite a
            # correctly-set version.
            "conflicts": conflicts,
            # **Named, when the version asked for is not one this project keeps.**
            # The window is still a real answer about the repositories, so the
            # report stands -- but nothing is proposed onto a version that does
            # not exist, and the reader is told which version that was.
            "unknown_version": unknown_version,
            "design": {
                # Tickets whose work is entirely design, plus merged design
                # pull requests naming no ticket. Still released, still tagged
                # -- narrated apart so layout experiments do not read as
                # shipped product.
                "items": design_items,
                "unticketed": design_entries,
            },
            "ref_collisions": [
                {"ref": ref, "board": board.summary, "internal": internal.summary}
                for ref, board, internal in colliding_refs(
                    project.alias or "", all_tickets
                )
            ],
            # **The connections still to be made, gathered in one place.**
            #
            # Every loose end in a release is one of three shapes, and they are
            # the same problem seen from different sides: a ticket on the
            # release with no code, a merged pull request with no ticket, and a
            # started ticket carrying no release. A summary that reports them in
            # three separate sections leaves the reader to notice that the
            # pull request in one is plainly the missing code in another.
            #
            # Deliberately *not* paired here. Pairing is a judgement about what
            # two pieces of English mean, and this service only states facts it
            # can defend -- a link it guessed and stored would be
            # indistinguishable, a week later, from one somebody meant. The
            # narrator proposes; a person confirms; the confirmation lands on
            # `RepositoryPullRequest.ticket_id`.
            "unresolved": {
                "tickets_without_code": [
                    {"ref": i["ref"], "title": i["title"], "status": i["status"]}
                    for i in items
                    if i["state"] in _UNRESOLVED_ITEM_STATES
                ],
                "pull_requests_without_tickets": [
                    {
                        "repo": pr["repo"],
                        "number": pr["number"],
                        "title": pr["title"],
                        "commits": pr.get("commits") or [],
                    }
                    for pr in unticketed
                ],
                "tickets_without_release": [
                    {"ref": r["ref"], "title": r["title"], "status": r.get("status")}
                    for r in off_release
                    if r["state"] in _CANDIDATE_STATES
                ],
            },
            # **The release row's own facts, so a reader does not have to run
            # `releases list` beside this.** A release summary opens by saying
            # which release, whether it has gone out and when -- none of which
            # is derivable from the tickets and pull requests below it.
            "release_record": _release_facts(releases, version, items),
            "totals": {
                "tickets": len(items),
                "complete": complete,
                "with_gaps": len(items) - complete,
                "shipped_untagged": sum(
                    1
                    for t in off_release
                    if t["state"] == ReleaseVerdict.SHIPPED_UNTAGGED
                ),
                "off_release": len(off_release),
                "candidates": sum(
                    1 for t in off_release if t["state"] in _CANDIDATE_STATES
                ),
                "conflicts": len(conflicts),
                "unticketed": len(unticketed),
                "unresolved": (
                    sum(1 for i in items if i["state"] in _UNRESOLVED_ITEM_STATES)
                    + len(unticketed)
                ),
            },
        }

    def _off_release(
        self,
        *,
        project: Project,
        version: Optional[str],
        matched: Dict[str, Dict[str, Any]],
        people: "_PeopleIndex",
        propose: bool,
        outstanding_versions: Set[tuple],
    ) -> List[Dict[str, Any]]:
        """Tickets that are not on this release, each with a verdict.

        Two very different situations were being reported as one flat list:

        * **shipped_untagged** -- code merged in this window against a ticket on
          no release. That is delivered work missing from the notes, and it is
          the loudest thing a release report can say.
        * **started_untagged** -- started, on no release, nothing merged here.
          A candidate: probably belongs on the release, worth proposing, not
          worth alarming anybody about.

        Ordered so the first kind is read first. A summary that buries "this
        shipped and is not in your release" among fourteen quiet candidates has
        technically reported it.

        **`propose` gates the second kind, not the first.** "Started, on no
        release" is a fact about the project rather than about any version, so
        every release was being handed the same list -- BPAI returned an
        identical twenty-four candidates for the version that shipped three days
        ago, the one being cut, and the one being planned, which is a large part
        of why those three reports read alike. Only the release actually being
        cut can take a candidate, so only it is offered them. Work that *shipped*
        untagged is reported either way: that is a statement about what went out
        in this window, and it is true of a released version too.
        """
        rows: Dict[str, Dict[str, Any]] = {}

        for ref, row in matched.items():
            # **A ticket already tagged for another release that has not gone
            # out is correctly placed, not off-release.** It arrived here only
            # because its pull request merged inside this window, which is a
            # fact about timing rather than attribution: work planned for the
            # release *after* this one still lands on main first. Calling that
            # `shipped_untagged` -- "delivered work missing from the notes" --
            # is backwards, and the remedy offered to overwrite a version
            # somebody had set on purpose.
            #
            # A ticket pointing at a version that has already **shipped** is a
            # different matter and stays: its code merged after that release
            # went out, so the ticket names a release it cannot have been in,
            # and this window is where the work actually landed.
            other = _version_key(row.get("release"))
            if (
                other is not None
                and other != _version_key(version)
                and other in outstanding_versions
            ):
                continue
            merged = [pr for pr in row["prs"] if pr.get("merged")]
            rows[ref] = {
                **row,
                "state": (
                    ReleaseVerdict.SHIPPED_UNTAGGED.value
                    if merged
                    # **An open pull request is work in flight, not silence.**
                    # Both used to read `started_untagged`, so a ticket somebody
                    # was actively pushing to looked identical to one nobody had
                    # touched -- and the difference is the whole of whether it
                    # can make the release being cut.
                    else ReleaseVerdict.RELEASE_CANDIDATE.value
                ),
                "people": sorted(
                    {pr["person"] for pr in row["prs"] if pr.get("person")}
                ),
            }
            rows[ref]["recommendation"] = _recommend(rows[ref]["state"])

        for ticket in self.candidate_tickets(project.id) if propose else []:
            ref = _display_ref(project, ticket)
            if ref in rows:
                continue
            owner = people.name_for_ticket(ticket)
            rows[ref] = {
                "ref": ref,
                "ticket_id": ticket.id,
                "url": ticket.url,
                "title": ticket.summary,
                "status": ticket.status.value if ticket.status else None,
                "release": ticket.release,
                "state": ReleaseVerdict.STARTED_UNTAGGED.value,
                "recommendation": _recommend(ReleaseVerdict.STARTED_UNTAGGED.value),
                "people": [owner] if owner else [],
                "prs": [],
                "remedy": (
                    f"innoday tickets update --ticket-id {ticket.id} "
                    f"--release {version}"
                    if version
                    else None
                ),
            }

        if not propose:
            # A pull request may still have put a started, untagged ticket in
            # `matched`; without a slot to propose it into, saying so is noise.
            rows = {
                ref: row
                for ref, row in rows.items()
                if row["state"] == ReleaseVerdict.SHIPPED_UNTAGGED
            }

        return sorted(
            rows.values(),
            key=lambda r: (r["state"] != ReleaseVerdict.SHIPPED_UNTAGGED, r["ref"]),
        )

    def _conflicts(
        self,
        *,
        project: Project,
        releases: List[Release],
        people: "_PeopleIndex",
        version: Optional[str],
    ) -> List[Dict[str, Any]]:
        """Unfinished tickets stranded on a version that has already gone out.

        Reported for every release rather than only the one being cut, because
        the fact belongs to the ticket: v1.11.0 shipping without BPAI-407 is
        equally true whichever version you ask about.

        **Except the release under examination.** Asked about v1.11.0 itself, a
        ticket on v1.11.0 is a *member* -- it appears in `items` with its own
        verdict -- and listing it again here made one ticket two rows across two
        counters, with a `detail` reading "v1.11.0 shipped without this finished.
        Move it to the release being cut" about the very release being reported.

        Reported separately from candidates because the remedy differs: a
        candidate needs adding, a conflict needs a decision about work that has
        already missed a boat. No remedy string is offered -- moving it forward
        and splitting the unfinished part out are both reasonable and this cannot
        tell which the work wants.
        """
        asked = _version_key(version)
        shipped = {
            key
            for key in (
                _version_key(r.version)
                for r in releases
                if r.status == ReleaseStatus.RELEASED
            )
            if key is not None and key != asked
        }
        if not shipped:
            return []
        out: List[Dict[str, Any]] = []
        for ticket in self.conflicted_tickets(project.id, shipped):
            owner = people.name_for_ticket(ticket)
            out.append(
                {
                    "ref": _display_ref(project, ticket),
                    "ticket_id": ticket.id,
                    "url": ticket.url,
                    "title": ticket.summary,
                    "status": ticket.status.value if ticket.status else None,
                    "release": ticket.release,
                    "state": ReleaseVerdict.ON_SHIPPED_RELEASE.value,
                    "recommendation": _recommend(
                        ReleaseVerdict.ON_SHIPPED_RELEASE.value
                    ),
                    "people": [owner] if owner else [],
                    "detail": (
                        f"{ticket.release} shipped without this finished. "
                        "Move it to the release being cut, or split out what is left."
                    ),
                }
            )
        return sorted(out, key=lambda r: r["ref"])

    async def _add_commits(
        self,
        api: GitHubAPI,
        repos: List[Repository],
        entries: List[Dict[str, Any]],
    ) -> None:
        """Attach commit subjects to each entry, in place, best-effort.

        Best-effort on purpose: commits are what a proposal is argued from, and
        failing to fetch them costs a suggestion, not the release.
        """
        addressed = {}
        for repo in repos:
            pair = _owner_and_name(repo)
            if pair is not None:
                addressed[repo.name] = pair

        async def one(entry: Dict[str, Any]) -> None:
            pair = addressed.get(entry.get("repo"))
            if pair is None:
                return
            owner, name = pair
            try:
                entry["commits"] = await api.pull_request_commits(
                    owner, name, entry["number"]
                )
            except Exception as exc:  # noqa: BLE001 - a proposal is not worth a 500
                logger.warning(
                    "Commits unavailable for %s#%s: %s",
                    entry.get("repo"),
                    entry.get("number"),
                    exc,
                )

        await asyncio.gather(*(one(entry) for entry in entries))

    def _item(
        self,
        project: Project,
        ticket: Ticket,
        prs: List[Dict[str, Any]],
        people: "_PeopleIndex",
        narrative: Optional["_NarrativeIndex"] = None,
    ) -> Dict[str, Any]:
        """One ticket, judged against what a finished one looks like.

        Complete means: code exists, it merged, the ticket has moved to review
        or done, and somebody is attached to it. Anything short of that is a
        gap -- reported with the thing to do about it, never a blocker. A
        release ships with gaps; what it must not do is hide them.
        """
        merged = [pr for pr in prs if pr["merged"]]
        open_prs = [pr for pr in prs if not pr["merged"]]
        status = (ticket.status.value if ticket.status else "") or ""

        if merged and not open_prs:
            state = ReleaseVerdict.SHIPPED
        elif merged:
            state = ReleaseVerdict.PARTLY_MERGED
        elif open_prs:
            state = ReleaseVerdict.NOT_MERGED
        elif status in _NOT_STARTED:
            state = ReleaseVerdict.NOT_STARTED
        else:
            state = ReleaseVerdict.NO_CODE

        gaps: List[Dict[str, str]] = []
        if state == ReleaseVerdict.NO_CODE:
            gaps.append(
                {
                    "kind": "no_code",
                    "detail": "no pull request names this ticket",
                    "remedy": (
                        "name the branch or the pull request title after the "
                        "ticket, or drop it from the release"
                    ),
                }
            )
        if state == ReleaseVerdict.NOT_STARTED:
            gaps.append(
                {
                    "kind": "not_started",
                    "detail": f"on the release but still {status}",
                    "remedy": "start it, or move it to the next release",
                }
            )
        if open_prs:
            gaps.append(
                {
                    "kind": "not_merged",
                    "detail": "%s still open"
                    % ", ".join(f"{pr['repo']}#{pr['number']}" for pr in open_prs),
                    "remedy": "merge it, or drop the ticket from this release",
                }
            )
        if merged and status not in _FINISHED:
            gaps.append(
                {
                    "kind": "status_behind",
                    "detail": f"code merged but the ticket is {status or 'unset'}",
                    "remedy": "move it to Test or Done",
                }
            )

        # Assignee first, then whoever wrote the code -- the owner, then the
        # hands. Deduplicated, because they are usually the same person.
        credited: List[str] = []
        owner = people.name_for_ticket(ticket)
        if owner:
            credited.append(owner)
        for pr in prs:
            if pr.get("person") and pr["person"] not in credited:
                credited.append(pr["person"])
        if not credited:
            gaps.append(
                {
                    "kind": "unattributed",
                    "detail": "nobody is mapped to this work",
                    "remedy": "claim the handle with `innoday auth identity --set`",
                }
            )

        return {
            "ref": _display_ref(project, ticket),
            # **The ids the save path needs, carried from the start.**
            # `save_project_summary` ties each line of prose to a ticket and a
            # person through these; a line that arrives without them is stored
            # as work on no ticket, owned by nobody, and shown that way. They
            # were missing, which made a release summary look unsavable when it
            # was only unattributable.
            "ticket_id": ticket.id,
            "assignee_user_id": ticket.assigned_to,
            #: Every pull request on this ticket landed in a design repository.
            #: A ticket with no code at all is not design work -- it is
            #: unstarted, and calling it design would hide that.
            "is_design": bool(prs) and all(pr.get("design") for pr in prs),
            # **Both names, always.** The board key is what a customer can
            # follow and the internal number is what InnoDay's own surfaces
            # show, and the two spell the same string for different tickets
            # often enough that carrying only one loses the link between them.
            "board_ref": ticket.external_ticket_id,
            "innoday_ref": (
                f"{project.alias}-{ticket.project_ref_number}"
                if project.alias and ticket.project_ref_number is not None
                else None
            ),
            "url": ticket.url,
            "title": ticket.summary,
            "status": status,
            "state": state.value,
            "recommendation": _recommend(state.value),
            "people": credited,
            "prs": prs,
            "gaps": gaps,
            # **The narrator's sentence, or nothing.** Absent until somebody has
            # written a summary for this release; a renderer falls back to the
            # ticket's own title, which says what the work *was* but never what
            # it meant to a person using the product.
            "narrative": (
                narrative.for_ticket(ticket.id) if narrative is not None else None
            ),
        }
