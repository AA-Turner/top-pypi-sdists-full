"""
Tests for release auto-creation during board sync (_ensure_release_exists)
and Release router behaviour.
"""

import ast
import inspect
from pathlib import Path
from uuid import uuid4

import pytest
from sqlmodel import Session, select

from src.domain.board import BoardRegistration, BoardType
from src.domain.organization import Organization
from src.domain.project import Project
from src.domain.release import Release, ReleaseStatus
from src.domain.ticket import Ticket, TicketStatus
from src.services.board_sync_service import BoardSyncService
from tests.db_helpers import build_test_engine


@pytest.fixture
def db_session():
    engine = build_test_engine()
    with Session(engine) as session:
        yield session


@pytest.fixture
def org(db_session):
    o = Organization(id=str(uuid4()), name="Test Org")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


@pytest.fixture
def project(db_session, org):
    p = Project(
        id=str(uuid4()),
        organization_id=org.id,
        alias=f"T{str(uuid4())[:6]}".upper(),
        name="Test Project",
        description="Test project",
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


@pytest.fixture
def board(db_session, org, project):
    b = BoardRegistration(
        id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        board_name="Test Board",
        board_type=BoardType.JIRA,
        board_url="https://test.atlassian.net",
        board_external_id="test",
    )
    db_session.add(b)
    db_session.commit()
    db_session.refresh(b)
    return b


class TestBoardSyncNoLongerInventsReleases:
    """Board sync used to open a PLANNED Release for any version-shaped label.

    That let a label on anyone's ticket invent a version, which is how BPAI
    accumulated forty-odd rows on versioning lines it had long left -- the mess
    the high-water-mark rule in `release_planning` exists to survive. A project's
    releases are now a managed two-slot pipeline with a single writer, so the
    version string lands on the ticket and stops there.
    """

    def test_a_version_label_records_on_the_ticket_but_creates_no_release(
        self, db_session, org, project
    ):
        linear_board = BoardRegistration(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            board_name="Linear Board",
            board_type=BoardType.LINEAR,
            board_url="https://linear.app/eng",
            board_external_id="team-abc",
        )
        db_session.add(linear_board)
        db_session.commit()

        service = BoardSyncService.__new__(BoardSyncService)

        # A ticket as the Linear adapter produces it: release set from a v1.0.0
        # label. Round-trip it through the sync transform.
        ticket = Ticket(
            summary="Ship the thing",
            status=TicketStatus.IN_REVIEW,
            external_ticket_id="ENG-1",
            organization_id=org.id,
            project_id=project.id,
            board_registration_id=linear_board.id,
            source_platform="linear",
            release="v1.0.0",
        )
        external = service._ticket_to_external_dict(ticket, linear_board)
        service._create_or_update_ticket(external, linear_board, db_session, project.id)
        db_session.commit()

        # The join still works from the ticket's side -- that is what the
        # Releases tab and `_bulk_close_tickets_for_release` read.
        saved = db_session.exec(
            select(Ticket).where(Ticket.external_ticket_id == "ENG-1")
        ).first()
        assert saved.release == "v1.0.0"

        # But no release was invented for it.
        assert (
            db_session.exec(
                select(Release).where(Release.project_id == project.id)
            ).all()
            == []
        )

    def test_the_creating_helper_is_gone_not_merely_uncalled(self):
        """Left in place, it would be called again by the next person who wanted
        a release row from a sync -- which is exactly how this started."""
        assert not hasattr(BoardSyncService, "_ensure_release_exists")


def _sync_service(session):
    """A GitHubConnectService with only the session wired up.

    Its __init__ builds API clients this test has no use for, and the method
    under test touches nothing else.
    """
    from src.services.github_connect_service import GitHubConnectService

    service = GitHubConnectService.__new__(GitHubConnectService)
    service.session = session
    return service


class TestSyncRepairsThePipeline:
    """Repository sync runs the same invariant the release router does, so a
    rotation that failed partway is put right rather than leaving the project
    with nothing upcoming."""

    def test_sync_opens_both_slots_for_a_project_that_has_only_shipped(
        self, db_session, org, project
    ):
        db_session.add(
            Release(
                id=str(uuid4()),
                organization_id=org.id,
                project_id=project.id,
                version="v1.8.0",
                status=ReleaseStatus.RELEASED,
            )
        )
        db_session.commit()

        service = _sync_service(db_session)
        releases = list(
            db_session.exec(
                select(Release).where(Release.project_id == project.id)
            ).all()
        )
        opened = service._ensure_release_pipeline(org.id, project.id, releases)
        db_session.commit()

        assert opened == 2
        rows = {
            r.version: r.status
            for r in db_session.exec(
                select(Release).where(Release.project_id == project.id)
            ).all()
        }
        assert rows == {
            "v1.8.0": ReleaseStatus.RELEASED,
            "v1.9.0": ReleaseStatus.IN_PROGRESS,
            "v1.10.0": ReleaseStatus.PLANNED,
        }

    def test_sync_promotes_a_half_rotated_pipeline(self, db_session, org, project):
        """The release was recorded but the call that should have advanced the
        pipeline never landed: one PLANNED row above the high-water mark and
        nothing in progress. Sync promotes it and opens the slot above."""
        for version, status in (
            ("v1.9.0", ReleaseStatus.RELEASED),
            ("v1.10.0", ReleaseStatus.PLANNED),
        ):
            db_session.add(
                Release(
                    id=str(uuid4()),
                    organization_id=org.id,
                    project_id=project.id,
                    version=version,
                    status=status,
                )
            )
        db_session.commit()

        service = _sync_service(db_session)
        releases = list(
            db_session.exec(
                select(Release).where(Release.project_id == project.id)
            ).all()
        )
        service._ensure_release_pipeline(org.id, project.id, releases)
        db_session.commit()

        rows = {
            r.version: r.status
            for r in db_session.exec(
                select(Release).where(Release.project_id == project.id)
            ).all()
        }
        assert rows["v1.10.0"] == ReleaseStatus.IN_PROGRESS
        assert rows["v1.11.0"] == ReleaseStatus.PLANNED


class TestReleaseDomain:
    """Tests for Release model status transitions."""

    def test_release_status_values(self):
        assert ReleaseStatus.PLANNED.value == "planned"
        assert ReleaseStatus.IN_PROGRESS.value == "in_progress"
        assert ReleaseStatus.RELEASED.value == "released"
        assert ReleaseStatus.ARCHIVED.value == "archived"

    def test_release_creation_defaults(self, db_session, org, project):
        release = Release(
            organization_id=org.id,
            project_id=project.id,
            version="v3.0.0",
            status=ReleaseStatus.PLANNED,
        )
        db_session.add(release)
        db_session.commit()
        db_session.refresh(release)

        assert release.id is not None
        assert release.released_at is None
        assert release.notes is None


class TestSyncWritesExternalVersionsAndNeverValidates:
    """The regression that matters.

    Boards name versions InnoDay has no `Release` row for -- Jira `fixVersions`
    is free text. Sync writes through the session and never reaches the router,
    so the ticket-release validator cannot apply to it; these tests prove that
    rather than assuming it.
    """

    @pytest.fixture
    def pipeline(self, db_session, org, project):
        for version, status in (
            ("v1.10.0", ReleaseStatus.IN_PROGRESS),
            ("v1.11.0", ReleaseStatus.PLANNED),
        ):
            db_session.add(
                Release(
                    id=str(uuid4()),
                    organization_id=org.id,
                    project_id=project.id,
                    version=version,
                    status=status,
                )
            )
        db_session.commit()

    def test_an_unmatched_jira_fix_version_is_written_verbatim(
        self, db_session, org, project, board, pipeline
    ):
        service = BoardSyncService.__new__(BoardSyncService)
        external = {
            "id": "JIRA-1",
            "summary": "Hotfix from Jira",
            "status": "To Do",
            "fields": {"fixVersions": [{"name": "2026.08-hotfix"}]},
        }
        service._create_or_update_ticket(external, board, db_session, project.id)
        db_session.commit()

        saved = db_session.exec(
            select(Ticket).where(Ticket.external_ticket_id == "JIRA-1")
        ).first()
        assert saved.release == "2026.08-hotfix"

        # And no Release row was invented for it.
        assert {
            r.version
            for r in db_session.exec(
                select(Release).where(Release.project_id == project.id)
            ).all()
        } == {"v1.10.0", "v1.11.0"}

    def test_an_existing_synced_ticket_moves_to_another_unmatched_version(
        self, db_session, org, project, board, pipeline
    ):
        service = BoardSyncService.__new__(BoardSyncService)
        for version in ("2026.08-hotfix", "2026.09-hotfix"):
            service._create_or_update_ticket(
                {
                    "id": "JIRA-2",
                    "summary": "Moving hotfix",
                    "status": "To Do",
                    "fields": {"fixVersions": [{"name": version}]},
                },
                board,
                db_session,
                project.id,
            )
            db_session.commit()

        saved = db_session.exec(
            select(Ticket).where(Ticket.external_ticket_id == "JIRA-2")
        ).all()
        assert len(saved) == 1
        assert saved[0].release == "2026.09-hotfix"

    def test_the_sync_path_never_invokes_the_ticket_release_validator(self):
        """Sync must not validate, and the reason is structural, not behavioural.

        This was originally written as `patch("src.services.ticket_release.
        resolve_ticket_release", side_effect=AssertionError(...))` plus
        `assert_not_called()` -- which **could not fail**. `board_sync_service`
        contains no reference to `ticket_release` at all, so the patch intercepted
        nothing and the assertion was trivially true. Worse, it stayed vacuous
        under the exact change it claimed to guard: a
        `from ... import resolve_ticket_release` added to sync would hold its own
        binding, which patching the *definition* module does not reach.

        So assert the real invariant instead -- sync does not reference the
        validator -- against the module source. That fails the moment someone adds
        an import or a call, which is the only thing that could make sync start
        validating.
        """
        source = Path(inspect.getfile(BoardSyncService)).read_text()
        tree = ast.parse(source)

        offenders = set()
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Attribute)
                and node.attr == "resolve_ticket_release"
            ):
                offenders.add("attribute access")
            elif isinstance(node, ast.Name) and node.id == "resolve_ticket_release":
                offenders.add("bare name")
            elif isinstance(node, ast.ImportFrom) and (node.module or "").endswith(
                "ticket_release"
            ):
                offenders.add(f"from {node.module} import ...")
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.endswith("ticket_release"):
                        offenders.add(f"import {alias.name}")

        assert not offenders, (
            "board_sync_service now reaches the interactive release validator "
            f"({sorted(offenders)}). Board sync must keep writing whatever the "
            "external board says -- Jira fixVersions and Linear labels are not "
            "drawn from InnoDay's outstanding releases, so validating them would "
            "make sync fail on any version InnoDay has no Release row for."
        )


class TestSyncDoesNotEraseAReleaseTheBoardDoesNotKnowAbout:
    """`release` was written unconditionally, while `completed_at` six lines below
    carried an explicit "None means the board said nothing" guard. Linear's
    `_release_from_labels` returns None unless the issue carries a semver-shaped
    label, so the next sync of any Linear board erased a release set in InnoDay --
    and `POST /tickets` pushes to the board by default, making that the common
    path.
    """

    @pytest.fixture
    def linear_board(self, db_session, org, project):
        b = BoardRegistration(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            board_name="Linear Board",
            board_type=BoardType.LINEAR,
            board_url="https://linear.app/eng",
            board_external_id="team-abc",
        )
        db_session.add(b)
        db_session.commit()
        return b

    def _existing(self, db_session, org, project, linear_board, release):
        t = Ticket(
            summary="Set in InnoDay",
            status=TicketStatus.TODO,
            external_ticket_id="ENG-7",
            organization_id=org.id,
            project_id=project.id,
            board_registration_id=linear_board.id,
            source_platform="linear",
            release=release,
        )
        db_session.add(t)
        db_session.commit()
        db_session.refresh(t)
        return t

    def test_a_board_that_supplies_no_version_leaves_the_stored_one_alone(
        self, db_session, org, project, linear_board
    ):
        self._existing(db_session, org, project, linear_board, "v1.0.0")

        service = BoardSyncService.__new__(BoardSyncService)
        service._create_or_update_ticket(
            {
                "id": "ENG-7",
                "summary": "Set in InnoDay",
                "status": "Todo",
                # No `release`, no `fixVersions`: exactly what the Linear adapter
                # produces for an issue with no semver-shaped label.
            },
            linear_board,
            db_session,
            project.id,
        )
        db_session.commit()

        saved = db_session.exec(
            select(Ticket).where(Ticket.external_ticket_id == "ENG-7")
        ).first()
        assert saved.release == "v1.0.0"

    def test_a_board_that_does_supply_one_still_wins(
        self, db_session, org, project, linear_board
    ):
        self._existing(db_session, org, project, linear_board, "v1.0.0")

        service = BoardSyncService.__new__(BoardSyncService)
        service._create_or_update_ticket(
            {
                "id": "ENG-7",
                "summary": "Set in InnoDay",
                "status": "Todo",
                "release": "v1.2.0",
            },
            linear_board,
            db_session,
            project.id,
        )
        db_session.commit()

        saved = db_session.exec(
            select(Ticket).where(Ticket.external_ticket_id == "ENG-7")
        ).first()
        assert saved.release == "v1.2.0"
