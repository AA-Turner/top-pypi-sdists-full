"""Pull requests, kept rather than counted -- and kept after they merge.

``GitHubAPI.count_open_pull_requests`` fetched every open PR object for a repo
and returned ``len(prs)`` -- discarding the title, number, url, author, assignees
and draft state it had just been handed. So "your open pull requests" looked like
it needed a new GitHub integration, when in fact the data was already crossing
the wire on every sync and being thrown away (#500).

This table is where it lands. Nothing new is fetched: the same call that used to
produce an integer now produces rows, and ``Repository.open_pr_count`` is derived
from them so the count and the list cannot disagree.

**Merged pull requests stay.** Until now this held only what GitHub currently
reported as *open*, and the sync deleted every row it no longer saw. So a pull
request's link to its ticket -- ``head_ref``, the only field on a PR that names
one -- existed for exactly as long as the PR was unmerged, and vanished at the
moment it became part of a release. "Which pull requests shipped PF-1268?" was
unanswerable the day after it shipped.

Rows are now marked rather than removed: ``state`` says whether GitHub still has
it open, and ``merged_at`` separates *merged* from *abandoned*, which matters
because only the first shipped anything. ``Repository.open_pr_count`` and every
"open pull requests" view filter on ``state``, so what they show is unchanged.

Separate from ``RepositoryIssue`` on purpose. That model is GitHub *issues* --
no author, no assignee, no draft state, and no way to tell a PR from an issue.
GitHub's own ``open_issues_count`` conflates the two, which is exactly the
confusion ``open_pr_count`` was added to escape; folding PRs into the issue table
would walk back into it.
"""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4

from sqlalchemy import JSON, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .repository import Repository


class RepositoryPullRequest(SQLModel, table=True):
    """One open pull request on one repository, as GitHub last reported it."""

    __tablename__ = "repository_pull_requests"
    __table_args__ = (
        # One row per PR per repo. The sync upserts on this rather than deleting
        # and re-inserting, so a PR keeps its identity across runs.
        UniqueConstraint("repository_id", "number", name="uq_repo_pr_number"),
    )

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        sa_column=Column(String, primary_key=True),
    )
    repository_id: str = Field(
        sa_column=Column(
            String,
            ForeignKey("repositories.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )

    #: GitHub's per-repo PR number -- the "#488" people say out loud. Not the
    #: global node id, which is unique but which nobody can read.
    number: int = Field(nullable=False)
    title: str = Field(max_length=500, nullable=False)
    url: str = Field(max_length=500, nullable=False)

    #: The login that opened it. Matched against ``users.github_username``, which
    #: is the column the profile page already writes -- so attribution needs no
    #: new mapping table and no second place for a handle to live.
    author_login: Optional[str] = Field(default=None, max_length=255, index=True)

    #: The branch the PR was opened *from* (`head.ref`), which is the only thing
    #: on a pull request that names a ticket.
    #:
    #: Without it nothing could answer "which pull requests belong to this
    #: ticket": this table stored no branch and no ticket reference, so the
    #: summary panel could show at most the one `pr_url` a `SummaryItem` happened
    #: to carry, and a ticket with work in three repositories looked like a ticket
    #: with work in one (#579, blocking the per-repo icons asked for in #574).
    #:
    #: Matched through `ticket_matching.tickets_by_ref`, the same index code
    #: activity already resolves through -- so a branch name and a stand-up line
    #: cannot disagree about which ticket `PF-7` is. Nullable because a branch
    #: naming no ticket is the common case and must link to nothing rather than
    #: guess.
    head_ref: Optional[str] = Field(default=None, max_length=255, index=True)

    #: Every assigned login. A list because GitHub allows several, and picking
    #: one would silently drop a PR off somebody's list. JSON rather than a join
    #: table: it is read whole, never queried across, and a table would be three
    #: more things to keep in step for no question anyone asks.
    assignee_logins: List[str] = Field(default_factory=list, sa_column=Column(JSON))

    is_draft: bool = Field(default=False)

    #: ``"open"`` or ``"closed"`` -- GitHub's own word, so there is nothing to
    #: translate. A merged pull request is ``closed`` here *and* carries
    #: ``merged_at``; GitHub models it the same way and inventing a third state
    #: would mean two vocabularies for one fact.
    state: str = Field(default="open", max_length=16, index=True)

    #: When it merged, or ``None`` if it closed unmerged **or if we have not been
    #: able to ask**. Those two are deliberately not distinguished: both mean
    #: "this did not demonstrably ship", which is the only question asked of it.
    merged_at: Optional[datetime] = Field(default=None)

    #: When this row stopped being open, by our clock. Not GitHub's ``closed_at``
    #: -- that is a fact about the pull request, this is a fact about when the
    #: sync noticed, and conflating them would date a row by an event we may have
    #: seen days later.
    closed_seen_at: Optional[datetime] = Field(default=None)

    #: GitHub's own timestamps, not ours. A PR's age is a fact about the PR, and
    #: stamping it with the sync instant would make every PR look brand new after
    #: a re-sync -- the same bug #503 fixed for Linear tickets.
    github_created_at: Optional[datetime] = Field(default=None)
    github_updated_at: Optional[datetime] = Field(default=None)

    #: A ticket somebody attached this pull request to **by hand**.
    #:
    #: Everything else about the ticket link is derived per request, from the
    #: branch, the title, then the description. That works when a pull request
    #: says which ticket it belongs to -- and on a real release ten of
    #: thirty-four said it nowhere. `fix/roi-multiplier-null` / "stop reporting
    #: a baseline ROI multiplier" is plainly "Stop showing a 0.0x return when a
    #: scenario loses money" and names it in no branch, title or body.
    #:
    #: Nothing infers this. A summary proposes a match from the commits, a
    #: person confirms it, and the confirmation is what lands here -- because a
    #: link the platform guessed and stored is indistinguishable, a week later,
    #: from one somebody meant.
    ticket_id: Optional[int] = Field(
        default=None, sa_column=Column(Integer, ForeignKey("ticket.id"), index=True)
    )

    last_synced_at: datetime = Field(default_factory=datetime.utcnow)

    repository: Optional["Repository"] = Relationship()

    def __repr__(self) -> str:
        return f"<RepositoryPullRequest {self.repository_id}#{self.number}>"
