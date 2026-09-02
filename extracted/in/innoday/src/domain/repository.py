"""Repository domain models for GitHub synchronization."""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel

from src.domain._base import TimestampMixin

if TYPE_CHECKING:
    from .organization import Organization

# Re-export RepositoryIssue for import convenience


class Repository(TimestampMixin, table=True):
    """Represents a GitHub repository with synced metadata and README content."""

    __tablename__ = "repositories"

    # Primary key using GitHub repo ID
    id: str = Field(primary_key=True, description="GitHub repository ID")

    # Core repository information
    name: str = Field(index=True, description="Repository name")
    full_name: str = Field(index=True, description="Full name (org/repo)")
    url: str = Field(description="GitHub repository URL")
    github_url: Optional[str] = Field(default=None, description="Direct GitHub URL")
    description: Optional[str] = Field(
        default=None, description="Repository description"
    )

    # Additional metadata
    technologies: List[str] = Field(
        default_factory=list, sa_column=Column(JSON), description="Technologies used"
    )
    is_active: bool = Field(default=True, description="Whether repository is active")
    external_id: Optional[str] = Field(
        default=None, description="External system identifier"
    )
    layer: Optional[str] = Field(
        default=None,
        description="Architectural layer (ui, api, data, ai, legacy, unassigned)",
    )

    # Repository content
    readme_content: Optional[str] = Field(
        default=None, description="Synced README content"
    )

    # Repository metadata
    language: Optional[str] = Field(
        default=None, description="Primary programming language"
    )
    stars: int = Field(default=0, description="Star count")
    forks: int = Field(default=0, description="Fork count")
    # GitHub's own `open_issues_count`, which counts issues **and** pull requests
    # together -- it is not a PR count and cannot be made into one by subtraction.
    open_issues_count: int = Field(default=0, description="Open issues count")

    # Open pull requests, counted separately because the field above cannot answer
    # it. Populated by the project sync via GET /repos/{o}/{r}/pulls?state=open.
    # None means "never counted", which is different from zero and is rendered
    # differently -- a repo with no PRs and a repo nobody has ever synced should
    # not look the same.
    open_pr_count: Optional[int] = Field(
        default=None, description="Open pull requests at last sync"
    )
    # When the count above was last successfully read, and the **only** field the
    # dashboard badge may use to say how old that number is.
    #
    # It carries its own timestamp rather than borrowing `last_synced_at` because
    # the two are written by different code on different occasions and mean
    # different things. `last_synced_at` is stamped by the repository *metadata*
    # passes -- `sync_project_repositories` and the `refresh=true` branch of
    # `GET .../repositories` -- neither of which reads a pull request, so a
    # five-day-old count would have rendered as "read 3 min ago": a false claim
    # about provenance, and worse than the unqualified number it replaced. (A third
    # such writer, the org-wide registration sync, stamped it on every repository in
    # the organization while leaving `open_pr_count` untouched; #658 deleted it.)
    #
    # Written by `_refresh_open_pr_counts` alone -- the single writer of
    # `open_pr_count` -- and only on a read that succeeded. NULL therefore means
    # the age of the count is genuinely unknown: it predates this column, or the
    # count came from something that does not stamp it. The badge renders that as
    # unknown rather than substituting a timestamp that means something else.
    open_pr_counted_at: Optional[datetime] = Field(
        default=None,
        description="When open_pr_count was last read from GitHub; NULL if unknown",
    )

    # Whether the last attempt to reach this repository on GitHub failed, and
    # when. NULL means "the last attempt succeeded", which is a different state
    # from "never attempted" -- but only one of them needs recording, because a
    # repo that has never synced has no `last_synced_at` either.
    #
    # **Set on failure, cleared on success.** The clearing half is what makes the
    # field trustworthy: a flag that only ever gets set turns into a permanent
    # red mark for one bad afternoon, and people learn to ignore it. See #499.
    errored_at: Optional[datetime] = Field(
        default=None,
        description="When the last sync of this repository failed; NULL if it succeeded",
    )
    error_message: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Why the last sync failed, truncated; NULL if it succeeded",
    )

    # Repository status
    is_private: bool = Field(default=False, description="Private repository flag")
    archived: bool = Field(default=False, description="Archived repository flag")
    archived_at: Optional[datetime] = Field(
        default=None, description="When the repository was archived"
    )
    deleted: bool = Field(default=False, description="Deleted repository flag")
    deleted_at: Optional[datetime] = Field(
        default=None, description="When the repository was deleted"
    )

    # client_id has been removed - use organization_id instead

    # NEW: Primary foreign key going forward
    organization_id: str = Field(
        foreign_key="organizations.id",
        index=True,
        description="Organization this repository belongs to",
    )
    # **Nothing writes a value here any more.** Its only writer was
    # `RepositorySyncService`, deleted in #658; the surviving repository writer
    # (`GitHubConnectService`) leaves it NULL, because a repository reaches InnoDay
    # through a *project's* GitHub topic and no registration is in scope. Kept for
    # now because rows created before #658 carry a real link, and dropping the
    # column would discard it -- read it as history, never as the way a repository
    # got here.
    github_org_registration_id: Optional[str] = Field(
        default=None,
        foreign_key="github_org_registrations.id",
        index=True,
        description="Registration a pre-#658 sync created this row under; NULL otherwise",
    )

    # Timestamps
    last_synced_at: Optional[datetime] = Field(
        default=None, description="Last sync timestamp"
    )

    # GitHub timestamps
    github_created_at: Optional[datetime] = Field(
        default=None, description="Repository creation on GitHub"
    )
    github_updated_at: Optional[datetime] = Field(
        default=None, description="Last update on GitHub"
    )

    # Issue sync configuration
    issue_sync_enabled: bool = Field(
        default=False, description="Enable GitHub issue synchronization"
    )
    sync_closed_issues: bool = Field(
        default=False, description="Include closed issues in sync"
    )
    issue_sync_interval_hours: int = Field(
        default=24, description="Hours between automatic issue syncs"
    )

    # Issue sync tracking
    last_issue_sync_at: Optional[datetime] = Field(
        default=None, description="Last time issues were synced"
    )
    last_issue_sync_count: Optional[int] = Field(
        default=None, description="Number of issues synced in last operation"
    )
    total_issues_synced: Optional[int] = Field(
        default=None, description="Total number of issues ever synced"
    )

    # Relationships
    organization: Optional["Organization"] = Relationship(back_populates="repositories")


class GitHubOrgRegistration(TimestampMixin, table=True):
    """A record that somebody connected this organization to a GitHub org.

    **Not an import mechanism.** Repositories arrive one way only: a project's
    GitHub topic (its alias, lowercased), through
    `POST .../projects/{id}/repositories/discover` and
    `GitHubConnectService.sync_project_repositories`. InnoDay never pulls every
    repository an organization owns. The route and service that did --
    `POST .../github-registrations/{id}/sync` and `RepositorySyncService` -- were
    deleted in #658, having produced 0 of 36 repositories in dev while topic
    discovery produced all 36.

    What the row is still for is the connect/disconnect flow in
    `routers/integrations.py`: which GitHub org this tenant named, and whether the
    connection is `active`. It is **not** where the credential lives -- that is
    Vault, via `org_credentials` -- and it is not required for a sync: it is
    written only when a `user_id` is attributable, so an organization can discover
    and sync repositories daily with no row here at all. That is why
    `GET .../integrations` answers `connected` from the credential rather than
    from this row's existence.

    One row per organization, enforced by a unique index on `organization_id`
    since #658. It was unenforced before, and dev held two identical `hs ->
    havilandsoftware` rows as a result.
    """

    __tablename__ = "github_org_registrations"

    # Primary key
    id: str = Field(primary_key=True, description="Registration UUID")

    # Registration details
    user_id: str = Field(
        foreign_key="users.id", index=True, description="User who registered"
    )
    # client_id has been removed - use organization_id instead

    # **Unique**, added by #658. Nothing enforced one row per organization before,
    # and dev held two identical `hs -> havilandsoftware` rows: `.first()` on an
    # unordered query then returned whichever the planner felt like, so which GitHub
    # org a tenant was "connected" to depended on the query plan. NULLs are still
    # unconstrained -- Postgres treats them as distinct in a unique index -- which is
    # correct here: a row with no organization is a legacy row, not a second
    # connection.
    organization_id: Optional[str] = Field(
        default=None,
        foreign_key="organizations.id",
        index=True,
        unique=True,
        description="Organization this GitHub registration belongs to",
    )
    organization: str = Field(index=True, description="GitHub organization name")

    # Sync configuration
    sync_enabled: bool = Field(default=True, description="Enable automatic sync")
    sync_readme: bool = Field(
        default=True, description="Include README content in sync"
    )
    sync_interval_minutes: int = Field(
        default=60, description="Sync interval in minutes"
    )

    # Registration status
    status: str = Field(
        default="active", description="Registration status (active, paused, error)"
    )
    last_error: Optional[str] = Field(
        default=None, description="Last sync error message"
    )

    # Sync tracking -- **historical only, nothing writes these any more.**
    # `RepositorySyncService` was their sole writer and #658 deleted it, so on any
    # organization connected after that they stay NULL for good. `status` and
    # `last_error` above are in the same position. `GET .../integrations` already
    # answers `last_sync` from `Repository.last_synced_at` and `error` from
    # `Project.github_error_message` for exactly this reason -- it read these two
    # columns first and reported "connected, never synced" for every org, because
    # they were accurate and simply never written. Do not add a reader that trusts
    # them; they are kept only so a pre-#658 row is not silently rewritten as
    # never-synced.
    last_sync_at: Optional[datetime] = Field(
        default=None, description="Last successful sync"
    )
    last_sync_repos_count: Optional[int] = Field(
        default=None, description="Repos synced in last sync"
    )
    total_repos_count: Optional[int] = Field(
        default=None, description="Total repos in organization"
    )


class GitHubSyncHistory(SQLModel, table=True):
    """One GitHub repository-sync attempt for one project.

    **One writer, one grain.** `GitHubConnectService._record_sync_history` writes
    a row per finished topic-discovery run, scoped to a `project_id`, and nothing
    else writes here. That is what #658 settled: the table previously also took
    rows from the org-wide registration sync
    (`POST .../github-registrations/{id}/sync` and `RepositorySyncService`),
    keyed on a registration and covering every repository that registration
    reached. Two grains in one table meant an org-wide count of 40 and a project
    count of 8 sat side by side in one history list, where the difference read as
    32 repositories vanishing between syncs. Deleting the org-wide import
    dissolved that: no reader split, no CHECK constraint, and no FK pointing at
    whichever sibling registration happened to be oldest.

    `GET .../projects/{project_id}/repositories/sync-history` reads the rows back.

    Rows are terminal-state only: no `in_progress` row is committed up front. An
    up-front row needs a reaper to close out attempts whose process died -- board
    sync only got one in #613, after a deploy landing mid-sync disabled sync for a
    board twice in four days -- and an `in_progress` row with no reaper is worse
    than no row, because it claims a sync is running. A sync killed mid-flight
    therefore leaves nothing here, which reads as "no record" rather than "still
    going".
    """

    __tablename__ = "github_sync_history"

    # Primary key
    id: str = Field(primary_key=True, description="Sync history UUID")

    #: The tenant, and the only key the RLS policy needs. Nullable only because a
    #: row predating #650 has nothing to backfill it from: the column it could
    #: have been derived from (`github_org_registrations.organization_id`) is
    #: itself nullable, so a NOT NULL promotion would have to invent a value or
    #: delete an audit row. Every writer sets it.
    organization_id: Optional[str] = Field(
        default=None,
        foreign_key="organizations.id",
        index=True,
        description="Organization whose repositories were synced",
    )
    #: Which project's repositories this attempt covered. NULL for an org-wide
    #: sync -- the grain the registration FK describes -- rather than a stand-in
    #: for "unknown".
    project_id: Optional[str] = Field(
        default=None,
        foreign_key="projects.id",
        index=True,
        description="Project synced, for a project-scoped sync",
    )

    # Sync details
    started_at: datetime = Field(description="Sync start timestamp")
    completed_at: Optional[datetime] = Field(
        default=None, description="Sync completion timestamp"
    )

    # Sync results
    status: str = Field(
        description="Sync status (pending, in_progress, completed, failed)"
    )
    repositories_synced: int = Field(
        default=0, description="Number of repositories synced"
    )
    repositories_created: int = Field(default=0, description="New repositories created")
    repositories_updated: int = Field(
        default=0, description="Existing repositories updated"
    )
    repositories_failed: int = Field(default=0, description="Failed repository syncs")
    readmes_synced: int = Field(default=0, description="README files synced")

    # Error tracking
    error_message: Optional[str] = Field(
        default=None, description="Error message if failed"
    )
    error_details: Optional[str] = Field(
        default=None, description="Detailed error information"
    )

    # Performance metrics
    duration_seconds: Optional[float] = Field(
        default=None, description="Sync duration in seconds"
    )
    api_calls_made: Optional[int] = Field(
        default=None, description="Number of API calls made"
    )
