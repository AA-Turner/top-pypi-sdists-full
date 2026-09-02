"""Code activity in a summary window -- fetched live, never persisted (PF-398).

There is deliberately **no `code_activity` table**. A summary window is a few
days wide and the answer is only interesting while the window is open; storing
it would mean a second copy of GitHub's data to keep in sync, with its own
staleness rules, for a read that happens a handful of times a day. Fetch it,
use it, throw it away. (A persisted mirror is v2, if per-commit history ever
becomes a read path of its own.)

**How code is linked to tickets.** A ticket reference like ``PF-398`` appears in
three places a branch's work naturally leaves it: the branch name, the pull
request title, and -- because a squash merge uses the PR title as its commit
message -- the commit subject on the default branch. All three are parsed. The
prefix is **derived from the project's alias**, never hardcoded: ``PF`` is one
project among several, and a regex pinned to it would silently find nothing for
every other one.

**Why both PRs and commits are fetched.** They answer different questions and
neither is sufficient alone:

* PRs carry the branch, the review state, and a URL -- the things a reader wants
  to click. They do not carry commit SHAs.
* Commits carry the SHAs the summary's `source_fingerprint` is built from. A
  fingerprint over PRs alone would call a day of pushes to an open PR
  "unchanged" as long as the PR's own metadata stood still.

Repos come from ``project_repositories`` (active links only), and the per-repo
fetches are gathered concurrently -- a project with a dozen repos otherwise
spends a dozen round trips in series for one summary.
"""

from __future__ import annotations

import asyncio
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from sqlmodel import Session, select

from src.api.github_api import GitHubAPI
from src.domain.organization import Organization
from src.domain.project import Project, ProjectRepository
from src.domain.repository import Repository
from src.services.org_credential_service import get_github_credentials
from src.utils.time_windows import parse_iso_utc

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CodeActivity:
    """One piece of work that happened in a repo during the window."""

    repo: str
    ticket_ref: Optional[str] = None
    branch: Optional[str] = None
    pr_url: Optional[str] = None
    pr_state: Optional[str] = None
    title: Optional[str] = None
    author_handle: Optional[str] = None
    occurred_at: Optional[datetime] = None
    commit_shas: Tuple[str, ...] = field(default_factory=tuple)


def ticket_ref_pattern(*aliases: str) -> re.Pattern:
    r"""A regex matching ticket references, e.g. ``PF-398``.

    Derived from aliases rather than a literal, because every project has its
    own. Case-insensitive on the way in -- branch names are frequently lowercase
    -- and the caller upper-cases what comes back so `pf-398` and `PF-398` are
    one key.

    A ticket answers to two names and branches use whichever the person saw: the
    board's own key (``PF-398`` from Linear, held in `external_ticket_id`) and
    the internal display number ``{project alias}-{project_ref_number}``. Both
    are prefixed by the *project* alias now that `project_ref_number` is
    project-scoped (`UniqueConstraint("project_id", "project_ref_number")`), so
    one alias covers both -- this used to need the organization's alias as well,
    back when the internal number was org-scoped.

    Still variadic: callers may pass several aliases, and duplicates collapse.
    Longest-first alternation so an alias that prefixes another still matches in
    full.

    **The number ends at `(?!\d)`, not at `\b`.** A word boundary after the
    digits fails when the next character is an underscore, because `_` is a word
    character -- so `bpai-409-small-ui` matched and `bpai_409_small_ui_items`
    did not. Underscore-separated branch names are an ordinary convention and
    every one of them was silently invisible: the work merged, the ticket showed
    "no pull request names this ticket", and nothing indicated the reference was
    right there in the branch. `(?!\d)` still refuses to split `BPAI-4091` into
    `BPAI-409`, which is the only thing the boundary was protecting.
    """
    unique = [a for a in dict.fromkeys(a for a in aliases if a)]
    if not unique:
        # Matches nothing, rather than the empty alternation `()` -- which
        # matches everywhere and would tag every number in every branch name.
        return re.compile(r"(?!)")
    alternation = "|".join(re.escape(a) for a in sorted(unique, key=len, reverse=True))
    return re.compile(rf"\b({alternation})[-_ ]?(\d+)(?!\d)", re.IGNORECASE)


def extract_ticket_ref(text: Optional[str], pattern: re.Pattern) -> Optional[str]:
    """The first ticket reference in `text`, normalised to ``ALIAS-123``."""
    if not text:
        return None
    match = pattern.search(text)
    if not match:
        return None
    return f"{match.group(1).upper()}-{match.group(2)}"


def _parse_github_time(value: Optional[str]) -> Optional[datetime]:
    """GitHub's ISO-8601-with-Z, as an aware UTC datetime.

    A thin alias now: this was the third byte-identical ISO coercion in the
    codebase. Kept as a name because the call sites read better for it.
    """
    return parse_iso_utc(value)


def _owner_and_name(repo: Repository) -> Optional[Tuple[str, str]]:
    """``(owner, name)`` from ``full_name``, or None when it is not owner/repo.

    A repo row whose `full_name` was never populated cannot be addressed on the
    GitHub API, and guessing an owner would query someone else's repository.
    """
    full_name = (repo.full_name or "").strip("/")
    if "/" not in full_name:
        return None
    owner, _, name = full_name.partition("/")
    if not owner or not name:
        return None
    return owner, name


class CodeActivityFetcher:
    """Live GitHub activity for a project's repos over one window."""

    def __init__(
        self,
        session: Session,
        *,
        client_factory: Optional[Callable[[str], Optional[GitHubAPI]]] = None,
    ) -> None:
        self.session = session
        # Injectable so tests -- and any caller with a client already built --
        # need neither Vault nor a network. The default resolves the per-org
        # token the same way GitHubConnectService does.
        self._client_factory = client_factory or self._client_for_org

    # ------------------------------------------------------------------ setup

    def _client_for_org(self, organization_id: str) -> Optional[GitHubAPI]:
        """A GitHub client for this org, or None when it has no credential."""
        org = self.session.get(Organization, organization_id)
        if org is None:
            return None
        creds = get_github_credentials(self.session, organization_id)
        if not creds or not creds.get("token"):
            return None
        return GitHubAPI(creds["token"])

    def project_repositories(self, project_id: str) -> List[Repository]:
        """Active, non-archived repos linked to the project."""
        rows = self.session.exec(
            select(Repository)
            .join(ProjectRepository, ProjectRepository.repository_id == Repository.id)
            .where(
                ProjectRepository.project_id == project_id,
                ProjectRepository.is_active.is_(True),
            )
        ).all()
        return [r for r in rows if not r.archived and not r.deleted]

    # ------------------------------------------------------------------ fetch

    async def fetch(
        self,
        *,
        project: Project,
        since: datetime,
        until: Optional[datetime] = None,
    ) -> List[CodeActivity]:
        """Everything that happened in the project's repos between the bounds.

        Never raises for a single repo's sake: one repo the token cannot see
        must not cost the whole summary, so a failed fetch is logged and that
        repo contributes nothing.
        """
        api = self._client_factory(project.organization_id)
        if api is None:
            logger.info(
                "No GitHub credential for org %s -- summary has no code activity",
                project.organization_id,
            )
            return []

        repos = self.project_repositories(project.id)
        if not repos:
            return []

        # One alias is enough: both names a ticket answers to -- the board key
        # and the internal `project_ref_number` -- are prefixed by the project
        # alias now that the number is project-scoped.
        pattern = ticket_ref_pattern(project.alias)
        results = await asyncio.gather(
            *(self._fetch_one(api, repo, pattern, since, until) for repo in repos),
            return_exceptions=True,
        )

        activities: List[CodeActivity] = []
        for repo, result in zip(repos, results):
            if isinstance(result, BaseException):
                logger.warning(
                    "Code activity fetch failed for %s: %s", repo.name, result
                )
                continue
            activities.extend(result)
        return activities

    async def _fetch_one(
        self,
        api: GitHubAPI,
        repo: Repository,
        pattern: re.Pattern,
        since: datetime,
        until: Optional[datetime],
    ) -> List[CodeActivity]:
        addressed = _owner_and_name(repo)
        if addressed is None:
            logger.debug("Repo %s has no owner/name in full_name; skipped", repo.id)
            return []
        owner, name = addressed

        prs, commits = await asyncio.gather(
            api.get_pull_requests(owner, name, state="all", since=since),
            api.get_commits(owner, name, since=since, until=until),
            return_exceptions=True,
        )
        if isinstance(prs, BaseException):
            logger.warning("PR fetch failed for %s/%s: %s", owner, name, prs)
            prs = []
        if isinstance(commits, BaseException):
            logger.warning("Commit fetch failed for %s/%s: %s", owner, name, commits)
            commits = []

        return self._to_activities(repo.name, prs, commits, pattern, since, until)

    # -------------------------------------------------------------- shaping

    @staticmethod
    def _to_activities(
        repo_name: str,
        prs: Sequence[Dict],
        commits: Sequence[Dict],
        pattern: re.Pattern,
        since: datetime,
        until: Optional[datetime],
    ) -> List[CodeActivity]:
        """Turn raw GitHub payloads into `CodeActivity`, bounded by the window.

        Commits are folded into the PR that owns their branch where the ref
        matches, so a ticket with a PR and five commits is one row carrying five
        SHAs rather than six competing rows. Commits whose ref matches no PR
        stand alone -- work pushed straight to the default branch is still work.
        """
        by_ref_commits: Dict[str, List[Dict]] = {}
        loose: List[CodeActivity] = []

        for commit in commits:
            sha = (commit.get("sha") or "")[:40]
            if not sha:
                continue
            detail = commit.get("commit") or {}
            when = _parse_github_time((detail.get("author") or {}).get("date"))
            if when is not None and (
                when < since or (until is not None and when > until)
            ):
                continue
            message = (detail.get("message") or "").splitlines()
            subject = message[0] if message else ""
            ref = extract_ticket_ref(subject, pattern)
            author = (commit.get("author") or {}).get("login") or (
                detail.get("author") or {}
            ).get("name")
            record = {"sha": sha, "when": when, "author": author, "subject": subject}
            if ref:
                by_ref_commits.setdefault(ref, []).append(record)
            else:
                loose.append(
                    CodeActivity(
                        repo=repo_name,
                        author_handle=author,
                        occurred_at=when,
                        title=subject,
                        commit_shas=(sha,),
                    )
                )

        activities: List[CodeActivity] = []
        claimed: set = set()
        for pr in prs:
            updated = _parse_github_time(pr.get("updated_at"))
            if updated is not None and (
                updated < since or (until is not None and updated > until)
            ):
                continue
            branch = ((pr.get("head") or {}).get("ref")) or None
            title = pr.get("title")
            ref = extract_ticket_ref(branch, pattern) or extract_ticket_ref(
                title, pattern
            )
            owned = by_ref_commits.get(ref, []) if ref else []
            if ref:
                claimed.add(ref)
            activities.append(
                CodeActivity(
                    repo=repo_name,
                    ticket_ref=ref,
                    branch=branch,
                    pr_url=pr.get("html_url"),
                    # `merged_at` beats `state`: GitHub reports a merged PR as
                    # "closed", which reads to a summary reader as abandoned.
                    pr_state="merged" if pr.get("merged_at") else pr.get("state"),
                    title=title,
                    author_handle=(pr.get("user") or {}).get("login"),
                    occurred_at=updated,
                    commit_shas=tuple(c["sha"] for c in owned),
                )
            )

        # Commits carrying a ref no PR claimed -- merged straight to the
        # default branch, or the PR fell outside the window.
        for ref, records in by_ref_commits.items():
            if ref in claimed:
                continue
            newest = max(
                records,
                key=lambda r: r["when"] or datetime.min.replace(tzinfo=timezone.utc),
            )
            activities.append(
                CodeActivity(
                    repo=repo_name,
                    ticket_ref=ref,
                    title=newest["subject"],
                    author_handle=newest["author"],
                    occurred_at=newest["when"],
                    commit_shas=tuple(r["sha"] for r in records),
                )
            )

        return activities + loose
