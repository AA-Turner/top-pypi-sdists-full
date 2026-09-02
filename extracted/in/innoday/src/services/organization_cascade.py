"""
Organization Cascade Deletion

Shared helper for deleting an organization and all of its child data in
FK-safe order. Used by both the owner-facing delete endpoint
(`src/routers/organizations.py`) and the platform-admin delete endpoint
(`src/routers/admin.py`) so the two code paths cannot diverge again.
"""

from sqlmodel import Session, select
from sqlmodel import delete as sql_delete
from sqlmodel import update as sql_update

from src.domain.board import BoardMetadata, BoardRegistration, BoardSyncHistory
from src.domain.container_execution import ContainerExecution
from src.domain.license import LicenseAuditLog, UsageTracking
from src.domain.organization import OrganizationLicense, OrganizationMembership
from src.domain.organization_invite import OrganizationInvite
from src.domain.project import Project, ProjectRepository
from src.domain.project_timeline import ProjectTimeline
from src.domain.project_update import ProjectUpdate
from src.domain.release import Release
from src.domain.repository import (
    GitHubOrgRegistration,
    GitHubSyncHistory,
    Repository,
)
from src.domain.repository_issue import RepositoryIssue
from src.domain.scope_document import ScopeDocument
from src.domain.scope_ticket_generation import ScopeTicketGeneration
from src.domain.summary import Summary, SummaryItem
from src.domain.ticket import Ticket, TicketComment
from src.domain.user import User
from src.domain.user_identity import UserIdentity


def delete_organization_cascade(session: Session, organization_id: str) -> None:
    """Delete an organization and all child rows in FK-safe order. Caller commits."""
    oid = organization_id

    # Level 1: leaf children of tickets
    session.exec(
        sql_delete(TicketComment).where(
            TicketComment.ticket_id.in_(
                select(Ticket.id).where(Ticket.organization_id == oid)
            )
        )
    )
    # `summary_items.ticket_id` is a plain FK with no ON DELETE, so a single
    # saved summary line pointing at one of this org's tickets makes the DELETE
    # below a `summary_items_ticket_id_fkey` violation -- i.e. the whole org
    # delete 500s the moment anyone uses the summary feature at all. The rows
    # are deleted here rather than beside `summaries` (which comes later, and
    # is fine there) purely because of that FK. This was invisible to review
    # because the cascade's only test ran on SQLite, which does not enforce
    # foreign keys; `test_delete_organization_cascade_on_postgres` is the
    # version that can actually fail.
    session.exec(
        sql_delete(SummaryItem).where(
            SummaryItem.summary_id.in_(
                select(Summary.id).where(Summary.organization_id == oid)
            )
        )
    )
    # Level 2: tickets
    session.exec(sql_delete(Ticket).where(Ticket.organization_id == oid))
    session.exec(
        sql_delete(ScopeTicketGeneration).where(
            ScopeTicketGeneration.organization_id == oid
        )
    )

    # Level 3: board children
    board_ids = select(BoardRegistration.id).where(
        BoardRegistration.organization_id == oid
    )
    session.exec(
        sql_delete(BoardSyncHistory).where(
            BoardSyncHistory.board_registration_id.in_(board_ids)
        )
    )
    session.exec(
        sql_delete(BoardMetadata).where(
            BoardMetadata.board_registration_id.in_(board_ids)
        )
    )
    # Summary items are already gone (level 1 -- they had to precede tickets).
    session.exec(sql_delete(Summary).where(Summary.organization_id == oid))

    # Level 4: project children
    project_ids = select(Project.id).where(Project.organization_id == oid)
    session.exec(
        sql_delete(ScopeDocument).where(ScopeDocument.project_id.in_(project_ids))
    )
    session.exec(
        sql_delete(ProjectUpdate).where(ProjectUpdate.project_id.in_(project_ids))
    )

    # Level 5b: GitHub sync history, then registrations
    #
    # **`organization_id` is the whole key**, and it has to be matched: this used to
    # match on `github_org_registration_id` alone, which was the table's only key
    # until #650 -- and every row the project sync writes has it NULL, so they all
    # survived the cascade and their `organization_id` FK then refused the
    # `organizations` delete at level 8, failing the org delete with an integrity
    # error naming a table nobody would think to look at. #658 deleted that column
    # with the org-wide sync it belonged to, so there is one key left; the migration
    # backfills `organization_id` from the registration first, so a pre-#658 row is
    # matched here too rather than orphaned.
    session.exec(
        sql_delete(GitHubSyncHistory).where(GitHubSyncHistory.organization_id == oid)
    )
    session.exec(
        sql_delete(GitHubOrgRegistration).where(
            GitHubOrgRegistration.organization_id == oid
        )
    )

    # Level 6: repository children, then project_repositories junction
    repo_ids = select(Repository.id).where(Repository.organization_id == oid)
    session.exec(
        sql_delete(RepositoryIssue).where(RepositoryIssue.repository_id.in_(repo_ids))
    )
    session.exec(
        sql_delete(ProjectRepository).where(
            ProjectRepository.project_id.in_(project_ids)
        )
    )

    # Level 6b: timeline entries reference projects, so they must go before
    # Level 7 deletes the projects themselves. (project_timeline's FK is
    # NO ACTION at the DB level, so an orphan here blocks the whole delete.)
    session.exec(
        sql_delete(ProjectTimeline).where(ProjectTimeline.organization_id == oid)
    )

    # Level 6c: project-scoped identity mappings, same reason -- NO ACTION on
    # `user_identity.project_id`. Latent until the profile page shipped, since
    # nothing wrote these rows; it does now, so a single claimed handle blocks
    # both the project delete and the org delete. Rows with `project_id IS
    # NULL` are the *global* handles, which belong to no organisation and are
    # deliberately left alone.
    session.exec(
        sql_delete(UserIdentity).where(UserIdentity.project_id.in_(project_ids))
    )

    # Level 6d: releases. Org-scoped, but `releases.project_id` is another
    # NO ACTION FK, so they cannot wait for level 8 with the rest of the
    # org-level tables -- the projects delete below would fail first. Found by
    # the Postgres cascade test the moment it existed; the SQLite one had been
    # asserting the rows were gone without ever executing this ordering.
    session.exec(sql_delete(Release).where(Release.organization_id == oid))

    # Level 7: boards, repositories, projects
    session.exec(
        sql_delete(BoardRegistration).where(BoardRegistration.organization_id == oid)
    )
    session.exec(sql_delete(Repository).where(Repository.organization_id == oid))
    session.exec(sql_delete(Project).where(Project.organization_id == oid))

    # Level 8: org-level tables
    session.exec(
        sql_delete(ContainerExecution).where(ContainerExecution.organization_id == oid)
    )
    session.exec(sql_delete(UsageTracking).where(UsageTracking.organization_id == oid))
    session.exec(
        sql_delete(LicenseAuditLog).where(LicenseAuditLog.organization_id == oid)
    )
    session.exec(
        sql_delete(OrganizationLicense).where(
            OrganizationLicense.organization_id == oid
        )
    )
    session.exec(
        sql_delete(OrganizationMembership).where(
            OrganizationMembership.organization_id == oid
        )
    )
    # A pending invite is enough to block the whole delete: its FK is NO ACTION
    # with no ondelete, so `DELETE /organizations/{id}` 500s with an
    # IntegrityError. This is the long-standing "BUG 3" in CLAUDE.md.
    session.exec(
        sql_delete(OrganizationInvite).where(OrganizationInvite.organization_id == oid)
    )
    # users.default_organization_id is a nullable FK with no ondelete — null it
    # out rather than deleting the user, who may belong to other orgs.
    session.exec(
        sql_update(User)
        .where(User.default_organization_id == oid)
        .values(default_organization_id=None)
    )
