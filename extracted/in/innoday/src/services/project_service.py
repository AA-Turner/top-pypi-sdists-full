"""Project service for managing projects and their components."""

import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from sqlmodel import Session, select

from src.domain.board import BoardRegistration
from src.domain.organization import OrganizationMembership
from src.domain.project import (
    Project,
    ProjectPriority,
    ProjectRepository,
    ProjectStatus,
    RepositoryLayer,
)
from src.domain.repository_issue import RepositoryIssue
from src.domain.ticket import Ticket, TicketStatus

# The overview's buckets, as sets of the **enum**, never of string literals.
#
# They were literals -- `["OPEN", "TODO"]`, `"IN_PROGRESS"`, `["DONE",
# "COMPLETED", "CLOSED"]` -- and `TicketStatus`'s values are lowercase (`"todo"`,
# `"in progress"`, `"done"`), with `OPEN`/`COMPLETED`/`CLOSED` not existing at
# all. Every comparison was therefore False and three of the four counts were
# permanently 0, while `total` looked right and made the zeros read as "no work"
# rather than as a bug.
#
# Derived from the enum so the next status added or renamed is a type error or a
# visible omission here, not another silent zero.
_OPEN_STATUSES = frozenset(
    {TicketStatus.DRAFT, TicketStatus.BACKLOG, TicketStatus.TODO}
)
#: Review is work in flight, not work waiting -- a ticket in review has been
#: started and is not done, which is exactly what this bucket means.
_IN_PROGRESS_STATUSES = frozenset({TicketStatus.IN_PROGRESS, TicketStatus.IN_REVIEW})
# CANCELLED is in `total` and in no bucket, deliberately: it is neither open,
# nor in flight, nor completed, and folding it into any of the three would
# overstate that bucket.


class ProjectService:
    """Service for managing projects and their components"""

    def __init__(self, session: Session):
        self.session = session

    async def create_project(
        self,
        organization_id: str,
        name: str,
        description: str,
        alias: str,
        goals: Optional[str] = None,
        scope_limitations: Optional[str] = None,
        spec: Optional[str] = None,
        project_context: Optional[str] = None,
        priority: ProjectPriority = ProjectPriority.MEDIUM,
        status: ProjectStatus = ProjectStatus.PLANNING,
        tags: Optional[List[str]] = None,
    ) -> Project:
        """
        Create a new project with initial configuration.

        Args:
            organization_id: Organization this project belongs to
            name: Project name
            description: Project description
            goals: Markdown-formatted goals and milestones
            scope_limitations: What's out of scope
            spec: One-paragraph plain-language description of the project
            project_context: Full markdown block of repo summaries, active work, and conventions
            priority: Project priority level
            status: Initial project status
            tags: List of tags for categorization

        Returns:
            Created Project instance
        """
        # Normalize and validate the alias (required, unique within the org).
        normalized_alias = self._normalize_alias(alias, organization_id)

        # Create project
        project = Project(
            id=str(uuid4()),
            organization_id=organization_id,
            alias=normalized_alias,
            name=name,
            description=description,
            goals=goals,
            scope_limitations=scope_limitations,
            spec=spec,
            project_context=project_context,
            status=status,
            priority=priority,
            tags=tags or [],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        self.session.add(project)
        self._seed_default_project_if_first(organization_id, project.id)
        self.session.commit()
        self.session.refresh(project)
        return project

    def _seed_default_project_if_first(
        self, organization_id: str, project_id: str
    ) -> None:
        """Give every membership of a project-less org its first project.

        `OrganizationMembership.default_project_id` is what the workflow homepage
        lands on. An org with no projects has nothing to point at, so its
        memberships sit NULL -- and the moment the first project exists, every
        one of them has exactly one right answer. Waiting for each member to pick
        it by hand would mean the page opened empty for people who have only ever
        had one project to choose from.

        **Same transaction as the project insert, and that is the point.** The
        question "did this org have no projects?" is only answerable *before* the
        row lands, and a separate commit afterwards leaves a window in which the
        project exists while the defaults do not -- reached by any request in
        between, and left permanently wrong if the second commit fails.

        Only ever fills a NULL. A member who has deliberately chosen a project is
        not overwritten by an unrelated project being created; that cannot happen
        on the first project, but it is cheap to state and it keeps this correct
        if the guard is ever loosened.

        Does NOT commit -- the caller commits both halves together.
        """
        existing_other = self.session.exec(
            select(Project.id)
            .where(
                Project.organization_id == organization_id,
                Project.id != project_id,
            )
            .limit(1)
        ).first()
        if existing_other is not None:
            return

        memberships = self.session.exec(
            select(OrganizationMembership).where(
                OrganizationMembership.organization_id == organization_id,
                OrganizationMembership.default_project_id.is_(None),  # type: ignore[union-attr]
            )
        ).all()
        for membership in memberships:
            membership.default_project_id = project_id
            self.session.add(membership)

    async def attach_board(
        self,
        project_id: str,
        board_registration_id: str,
    ) -> None:
        """
        Attach an existing board to a project.

        Writes the canonical direction of the board<->project link:
        BoardRegistration.project_id. A project may have at most one board
        (enforced by a unique constraint) -- attaching a second board to a
        project that already has one raises rather than silently replacing it.

        Args:
            project_id: Project to attach board to
            board_registration_id: Board registration to attach
        """
        project = self.session.get(Project, project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        board = self.session.get(BoardRegistration, board_registration_id)
        if not board:
            raise ValueError(f"Board registration {board_registration_id} not found")

        # Check if board belongs to same organization
        if board.organization_id != project.organization_id:
            raise ValueError("Board and project must belong to same organization")

        existing = self.session.exec(
            select(BoardRegistration).where(
                BoardRegistration.project_id == project_id,
                BoardRegistration.id != board_registration_id,
            )
        ).first()
        if existing:
            raise ValueError(
                f"Project {project_id} already has a board attached "
                f"({existing.id}) -- a project may have at most one board"
            )

        board.project_id = project_id
        project.updated_at = datetime.now(timezone.utc)

        self.session.add(board)
        self.session.add(project)
        self.session.commit()

    async def get_project_overview(
        self,
        project_id: str,
    ) -> Dict[str, Any]:
        """
        Get complete project overview with all related data.

        Args:
            project_id: Project to get overview for

        Returns:
            Dictionary containing project overview data
        """
        # Get project with relationships
        project = self.session.get(Project, project_id)

        if not project:
            raise ValueError(f"Project {project_id} not found")

        # Load repositories (active links only -- soft-deleted repos that
        # lost the project's GitHub topic label are excluded from overviews)
        project_repos = self.session.exec(
            select(ProjectRepository).where(
                ProjectRepository.project_id == project_id,
                ProjectRepository.is_active == True,
            )
        ).all()

        # Get the project's board (0 or 1 -- enforced by a unique constraint
        # on BoardRegistration.project_id) and ticket counts from it
        board = self.session.exec(
            select(BoardRegistration).where(BoardRegistration.project_id == project_id)
        ).first()

        # Scoped by **project**, not by the board. The counts previously came
        # from `Ticket.board_registration_id == board.id` inside `if board:`, so
        # a project with no board registered got `{}` -- and a project *with* one
        # still missed every ticket created directly in InnoDay, which carry a
        # `project_id` and no board.
        tickets = self.session.exec(
            select(Ticket).where(
                Ticket.project_id == project_id,
                Ticket.deleted_at.is_(None),
            )
        ).all()

        ticket_stats = {
            "total": len(tickets),
            "open": sum(1 for t in tickets if t.status in _OPEN_STATUSES),
            "in_progress": sum(1 for t in tickets if t.status in _IN_PROGRESS_STATUSES),
            "completed": sum(1 for t in tickets if t.status == TicketStatus.DONE),
        }

        # Get repository issues by layer
        repos_by_layer = {}
        for layer in RepositoryLayer:
            layer_repos = [pr for pr in project_repos if pr.layer == layer]
            if layer_repos:
                repo_ids = [pr.repository_id for pr in layer_repos]
                issues = self.session.exec(
                    select(RepositoryIssue).where(
                        RepositoryIssue.repository_id.in_(repo_ids)
                    )
                ).all()

                repos_by_layer[layer.value] = {
                    "repositories": len(layer_repos),
                    "total_issues": len(issues),
                    "open_issues": sum(1 for i in issues if i.is_open),
                }

        # Find primary repository
        primary_repo = None
        for pr in project_repos:
            if pr.is_primary and pr.repository:
                primary_repo = {
                    "id": pr.repository_id,
                    "name": pr.repository.name,
                    "layer": pr.layer.value,
                }
                break

        # Build overview
        overview = {
            "project": {
                "id": project.id,
                # alias is the project's primary identifier (slug was retired),
                # so the overview has to carry it -- otherwise every consumer
                # renders the field it is most likely to key on as unknown.
                "alias": project.alias,
                "name": project.name,
                "description": project.description,
                "status": project.status.value,
                "priority": project.priority.value,
                "goals": project.goals,
                "scope_limitations": project.scope_limitations,
                "tags": project.tags,
                "created_at": project.created_at.isoformat(),
                "updated_at": project.updated_at.isoformat(),
            },
            "repositories": {
                "total": len(project_repos),
                "by_layer": repos_by_layer,
                "primary": primary_repo,
            },
            # Top level, because the counts are the *project's* and a project
            # need not have a board. They were reachable only through
            # `overview["board"]["tickets"]`, so a boardless project reported no
            # tickets at all -- not zero, absent.
            "tickets": ticket_stats,
            "board": None,
        }

        # Add board info if attached. `tickets` stays nested here as well: this
        # shape predates the top-level key and existing readers index into it.
        if board:
            overview["board"] = {
                "id": board.id,
                "name": board.board_name,
                "type": board.board_type.value,
                "tickets": ticket_stats,
            }

        return overview

    async def list_projects(
        self,
        organization_id: str,
        status: Optional[ProjectStatus] = None,
        priority: Optional[ProjectPriority] = None,
        tags: Optional[List[str]] = None,
    ) -> List[Project]:
        """List projects with optional filters"""
        query = select(Project).where(Project.organization_id == organization_id)

        if status:
            query = query.where(Project.status == status)

        if priority:
            query = query.where(Project.priority == priority)

        if tags:
            # Filter by any matching tag
            for tag in tags:
                query = query.where(Project.tags.contains([tag]))

        projects = self.session.exec(query.order_by(Project.created_at.desc())).all()
        return projects

    async def update_project(self, project_id: str, **updates) -> Project:
        """Update project fields"""
        project = self.session.get(Project, project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        # Update allowed fields
        #
        # **`alias` is here, and its absence was silent.** `ProjectUpdate.alias`
        # existed on the API model and the route passed it through, so the
        # request was accepted, answered 200, and the field was dropped on this
        # line -- an update that reported success and changed nothing. Renaming
        # a project appeared to work and did not.
        allowed_fields = [
            "name",
            "alias",
            "description",
            "goals",
            "scope_limitations",
            "spec",
            "project_context",
            "status",
            "priority",
            "tags",
            "ticket_creation_config",
        ]

        for field, value in updates.items():
            if field not in allowed_fields:
                continue
            if field == "alias" and value != project.alias:
                # Same normalisation and uniqueness check as creation, rather
                # than a second copy: an alias reached by rename must be as valid
                # as one reached by create, and `_normalize_alias` is where
                # "taken, including by an archived project" is explained.
                value = self._normalize_alias(value, project.organization_id)
            setattr(project, field, value)

        project.updated_at = datetime.now(timezone.utc)
        self.session.commit()
        self.session.refresh(project)
        return project

    async def delete_project(self, project_id: str) -> None:
        """Delete or archive a project"""
        project = self.session.get(Project, project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        # Archive instead of hard delete
        project.status = ProjectStatus.ARCHIVED
        project.updated_at = datetime.now(timezone.utc)
        self.session.commit()

    def _normalize_alias(self, alias: str, organization_id: str) -> str:
        """Normalize a project alias and enforce per-organization uniqueness.

        alias is the sole identifier for a project (slug was retired). It is
        uppercased and must be unique within the organization -- two orgs may
        share an alias, but one org may not have two projects with the same one.
        """
        if not alias or not alias.strip():
            raise ValueError("Project alias is required")

        normalized = alias.strip().upper()

        existing = self.session.exec(
            select(Project).where(
                Project.organization_id == organization_id,
                Project.alias == normalized,
            )
        ).first()
        if existing:
            # Archiving does not release the alias (the constraint is
            # unconditional), so the holder may be a project the caller was
            # told was "deleted". Point at reactivation: it is one call, and
            # it is almost always what they want -- creating a second project
            # under a new alias abandons the archived one's tickets, boards
            # and repos.
            if existing.status == ProjectStatus.ARCHIVED:
                raise ValueError(
                    f"Alias '{normalized}' is held by archived project "
                    f"{existing.id}. Reactivate it with `innoday projects "
                    f"update --project-id {existing.id} --status active`, "
                    f"or choose a different alias."
                )
            raise ValueError(
                f"Alias '{normalized}' is already used by another project in "
                f"this organization (project {existing.id})"
            )

        return normalized

    def _parse_github_url(self, url: str) -> Dict[str, str]:
        """Parse GitHub repository URL"""
        pattern = r"github\.com[/:]([^/]+)/([^/.]+)"
        match = re.search(pattern, url)

        if not match:
            raise ValueError(f"Invalid GitHub URL: {url}")

        return {
            "owner": match.group(1),
            "name": match.group(2),
            "full_name": f"{match.group(1)}/{match.group(2)}",
        }
