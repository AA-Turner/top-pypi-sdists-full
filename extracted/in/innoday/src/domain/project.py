"""Project domain models for organizing development work."""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from uuid import uuid4

from sqlalchemy import (
    JSON,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlmodel import Column, Field, Relationship, SQLModel

from src.domain._base import TimestampMixin

if TYPE_CHECKING:
    from src.domain.board import BoardRegistration
    from src.domain.organization import Organization
    from src.domain.project_timeline import ProjectTimeline
    from src.domain.project_update import ProjectUpdate
    from src.domain.release import Release
    from src.domain.repository import Repository
    from src.domain.scope_document import ScopeDocument
    from src.domain.ticket import Ticket  # noqa: F401


class ProjectStatus(str, Enum):
    """Project lifecycle status"""

    PLANNING = "planning"
    ACTIVE = "active"
    ARCHIVED = "archived"


class ProjectPriority(str, Enum):
    """Project priority levels"""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RepositoryLayer(str, Enum):
    """Architectural layer classification for repositories.

    The member *values* are lowercase; Postgres stores the member *names*
    (``UI``, ``API``, …) because ``project_repositories.layer`` is a real enum
    type built from the Python names. ``repositories.layer`` is a plain varchar
    holding the lowercase values. Both are read through ``_layer_of`` in
    ``src/routers/webui/data.py``, which normalises them.
    """

    UI = "ui"  # Frontend, mobile apps, web interfaces
    API = "api"  # Backend services, REST/GraphQL APIs
    DATA = "data"  # Databases, data pipelines, analytics
    AI = "ai"  # ML models, AI services, training pipelines
    INFRA = "infra"  # Terraform, CI/CD, deploy tooling, environment config
    LEGACY = "legacy"  # Deprecated/maintenance-only code
    #: Prototypes, demos and design explorations. A design repository is still
    #: part of the project and is still tagged by a release -- what it is *not*
    #: is part of the release's feature story, so a release summary gives it its
    #: own section rather than mixing its work into what shipped to customers.
    #:
    #: This member exists because there was previously no way to say that. The
    #: only way to keep a demo repository out of the release notes was to
    #: deactivate its ``project_repositories`` link, which also silently removed
    #: it from the tag set -- a release covered six repositories instead of
    #: seven and reported the smaller number with no warning.
    DESIGN = "design"
    UNASSIGNED = "unassigned"  # Not yet classified


class Project(TimestampMixin, table=True):
    """
    Central organizing unit for development work within an organization.

    Projects group related repositories, boards, and work under
    a unified structure with clear goals and scope.
    """

    __tablename__ = "projects"

    # alias is unique per-organization, not globally: two different orgs may
    # each have a project aliased "PF", but one org cannot have two.
    __table_args__ = (
        UniqueConstraint("organization_id", "alias", name="uq_project_org_alias"),
    )

    # Identity
    id: str = Field(
        default_factory=lambda: str(uuid4()), sa_column=Column(String, primary_key=True)
    )
    organization_id: str = Field(
        sa_column=Column(String, ForeignKey("organizations.id"), index=True)
    )
    alias: str = Field(
        max_length=10,
        sa_column=Column(String, index=True, nullable=False),
        description="Short uppercase code used as ticket prefix (e.g. BP, PF, HS). "
        "Unique within an organization, NOT globally -- two different orgs may "
        "each have a project aliased 'PF'. This is DIFFERENT from "
        "Organization.alias, which is globally unique (it replaced the org "
        "slug) -- see src/domain/organization.py. Uniqueness is enforced by "
        "the uq_project_org_alias composite constraint below.",
    )

    # Basic Information
    name: str = Field(max_length=255)
    description: str = Field(max_length=2000)
    goals: Optional[str] = Field(
        default=None, description="Markdown-formatted goals and milestones"
    )
    scope_limitations: Optional[str] = Field(
        default=None, description="What's explicitly out of scope for this project"
    )
    # Both are unbounded prose (a paragraph; a full markdown block), and the
    # migration built them as TEXT. SQLModel's default for `str` is VARCHAR,
    # so without an explicit column they under-declare production.
    spec: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
        description="One-paragraph plain-language description of the project",
    )
    # The two halves of a workspace CLAUDE.md, stored separately because they
    # have opposite ownership and opposite sync directions.
    #
    # `project_context` is GENERATED -- the deterministic header `innoday
    # init`/`refresh` renders from InnoDay + GitHub state. It is stored so the
    # UI can show a project's context without a workspace, and is *never*
    # handed back to a client: a CLI writes the version of the template it
    # ships with, and pulling a newer server copy down would leave a file the
    # local CLI cannot regenerate. Push is gated on
    # `project_context_version` (see below) so an older CLI cannot overwrite a
    # newer generation.
    #
    # `additional_context` is HAND-WRITTEN -- everything below the
    # `innoday:end-generated` marker. It is the one part of the file a person
    # authored, so it is the one part that must survive a machine being wiped,
    # and it syncs both ways (union-merged; see
    # `src/cli/commands/workspace.py`).
    project_context: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
        description="Generated workspace context header (UI view; push-only, never pulled)",
    )
    project_context_version: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, nullable=True),
        description="CONTEXT_TEMPLATE_VERSION of the CLI that last wrote project_context. "
        "A push is accepted only when the client's version is >= this, so an "
        "older CLI cannot regress a newer generation. Deliberately an integer "
        "bumped only when the template changes -- NOT the CLI semver, which "
        "moves for unrelated reasons and is ambiguous across -beta/dev builds.",
    )
    additional_context: Optional[str] = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
        description="Hand-written notes kept below the innoday:end-generated marker, "
        "synced both ways so they survive a re-clone or a new machine",
    )

    # Project Management
    status: ProjectStatus = Field(default=ProjectStatus.PLANNING)
    priority: ProjectPriority = Field(default=ProjectPriority.MEDIUM)

    # Whether this project's last GitHub repository sync failed, and why. Set on
    # failure, cleared on success, so NULL means "the last attempt succeeded" --
    # named and typed to mirror `BoardRegistration.errored_at`/`error_message`,
    # since the two feed the same pair of status icons and a reader should not
    # have to learn two shapes for one idea.
    #
    # It lives here rather than on `GitHubOrgRegistration` because the credential
    # is org-level but the *outcome* is not: a project whose topic resolves to a
    # renamed GitHub org fails while its siblings sync fine. Recorded org-wide,
    # one project's bad override would red every card in the org (#640).
    #
    # Distinct from `Repository.errored_at`, which says "part of what you see
    # could not be read" and needs a repo row to hang a failure on. A sync that
    # died in discovery never produced one, which is exactly the case this covers.
    github_errored_at: Optional[datetime] = Field(default=None)
    github_error_message: Optional[str] = Field(default=None, max_length=500)

    # Metadata
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    ticket_creation_config: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="Board destination, labels, issue type, and optional parent epic for quick-tickets",
    )

    # Relationships
    organization: Optional["Organization"] = Relationship(back_populates="projects")
    # A project has at most one board (enforced by a unique constraint on
    # BoardRegistration.project_id) -- modeled as a list because SQLAlchemy's
    # relationship() naturally maps the "many" side of a one-to-many FK, but
    # application code should treat this as 0 or 1 entries, never more.
    boards: List["BoardRegistration"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={
            "foreign_keys": "[BoardRegistration.project_id]",
        },
    )
    repositories: List["ProjectRepository"] = Relationship(back_populates="project")
    scope_documents: List["ScopeDocument"] = Relationship(back_populates="project")
    updates: List["ProjectUpdate"] = Relationship(back_populates="project")
    tickets: List["Ticket"] = Relationship(back_populates="project")
    releases: List["Release"] = Relationship(back_populates="project")
    timeline_entries: List["ProjectTimeline"] = Relationship(back_populates="project")

    def get_repositories_by_layer(
        self, layer: RepositoryLayer
    ) -> List["ProjectRepository"]:
        """Get all repositories in a specific layer"""
        return [r for r in self.repositories if r.layer == layer]

    def get_primary_repository(self) -> Optional["ProjectRepository"]:
        """Get the primary repository for this project"""
        for repo in self.repositories:
            if repo.is_primary:
                return repo
        return None

    def get_current_scope(self) -> Optional["ScopeDocument"]:
        """Get the current active scope document"""
        for scope in self.scope_documents:
            if scope.is_current:
                return scope
        return None

    def get_pending_updates(self) -> List["ProjectUpdate"]:
        """Get unprocessed project updates"""
        return [u for u in self.updates if not u.processed]


class ProjectRepository(SQLModel, table=True):
    """
    Junction table linking projects to repositories with layer classification.

    This model manages the relationship between projects and repositories,
    including architectural layer classification.
    """

    __tablename__ = "project_repositories"

    id: str = Field(
        default_factory=lambda: str(uuid4()), sa_column=Column(String, primary_key=True)
    )
    project_id: str = Field(
        sa_column=Column(String, ForeignKey("projects.id"), index=True)
    )
    repository_id: str = Field(
        sa_column=Column(String, ForeignKey("repositories.id"), index=True)
    )

    # Layer classification
    layer: RepositoryLayer = Field(default=RepositoryLayer.UNASSIGNED)

    # Repository role in project
    is_primary: bool = Field(
        default=False, description="Main repository for the project"
    )

    #: Whether **this project is the repository's primary project** -- the one
    #: whose release path the repo's own GitHub Releases belong to.
    #:
    #: READ THE DIRECTION. This is not a variant of ``is_primary`` above, it is
    #: the other way round:
    #:
    #:   is_primary          -- this REPO is the PROJECT's main repo
    #:   is_primary_project  -- this PROJECT is the REPO's primary project
    #:
    #: A repository may belong to several projects; exactly one of those links
    #: may be its primary, enforced by ``uq_repo_primary_project`` below rather
    #: than by service code, because the invariant is what stops a repo's own
    #: version from being imported as another project's platform release.
    #:
    #: Why it exists: ``GithubConnectService._discover_releases`` imports a
    #: repo's published GitHub Releases as ``Release`` rows on the project being
    #: synced. Publishing ``innoday-blastoff`` v0.3.0 to PyPI requires a
    #: published GitHub Release, and because that repo carries PF's topic, the
    #: package version landed as a **PF platform release** -- which then became
    #: ``max(released)`` and collapsed the v1.0.0 changelog window from 171
    #: merged PRs to 5. A repo's package version and the cross-repo release it
    #: is tagged into are independent, and this column is what keeps them so.
    #:
    #: False on every link of a multi-project repo means "nobody has decided":
    #: release discovery skips it and names it in the log, rather than guessing.
    is_primary_project: bool = Field(
        default=False,
        description=(
            "This project is the repository's primary project — its releases "
            "govern the repo's release path. At most one per repository."
        ),
    )
    purpose: Optional[str] = Field(
        default=None, max_length=500, description="Specific purpose within the project"
    )

    # Soft-delete: set when a project sync no longer finds this repo tagged
    # with the project's GitHub topic label. Kept (not hard-deleted) so a
    # repo that later regains the topic reactivates this same row instead of
    # creating a duplicate (see uq_project_repository below).
    is_active: bool = Field(
        default=True, description="False if the repo lost the project's topic label"
    )
    removed_at: Optional[datetime] = Field(
        default=None, description="When this link was soft-deleted, if inactive"
    )

    # Timestamps
    added_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    project: Optional["Project"] = Relationship(back_populates="repositories")
    repository: Optional["Repository"] = Relationship()

    # Constraints
    __table_args__ = (
        UniqueConstraint("project_id", "repository_id", name="uq_project_repository"),
        # At most one primary project per repository. A partial unique index
        # rather than a plain one: only the True rows must be unique, and there
        # are legitimately many False rows per repository. Both dialects in play
        # support partial indexes (Postgres in deploys, SQLite in the test
        # fixtures), so the invariant holds in tests as well as in production --
        # which matters, because a service-layer-only check is exactly what let
        # the release-import bug this column exists to fix go unnoticed.
        Index(
            "uq_repo_primary_project",
            "repository_id",
            unique=True,
            postgresql_where=text("is_primary_project"),
            sqlite_where=text("is_primary_project"),
        ),
    )
