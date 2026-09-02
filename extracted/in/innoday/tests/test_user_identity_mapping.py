"""User identity mapping — board assignee → InnoDay user (PF-398, issue #468).

`Ticket.assignee` is the board's own display-name string and stays that way.
`Ticket.assigned_to` is an FK to `users.id` that nothing used to write, which is
why `check_status`'s assigned-ticket count compared a UUID against a display
name and never matched.

These tests pin the three halves of the fix:

* `user_identity` rows map a board handle to a user, per project or globally;
* `IdentityResolutionService` resolves email-then-handle and returns None
  rather than guessing (no fuzzy display-name matching, ever);
* board sync populates both columns from the board — `assignee` with the raw
  display name, `assigned_to` with the resolved FK — and never fails a sync
  because an assignee could not be resolved.
"""

from types import SimpleNamespace
from uuid import uuid4

import pytest
from sqlmodel import select

from src.adapters.board_assignee import BoardAssignee, attach_board_assignee
from src.domain.board import BoardRegistration, BoardType
from src.domain.organization import Organization, OrganizationMembership
from src.domain.project import Project
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User
from src.domain.user_identity import IdentityPlatform, MatchSource, UserIdentity
from src.services.board_sync_service import BoardSyncService
from src.services.identity_resolution import (
    HandleAlreadyClaimedError,
    IdentityResolutionService,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def org(db_session):
    o = Organization(id=str(uuid4()), name="Example Org")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


@pytest.fixture
def project(db_session, org):
    p = Project(
        id=str(uuid4()),
        organization_id=org.id,
        name="Core Platform",
        description="Main platform project",
        alias="PF",
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


@pytest.fixture
def other_project(db_session, org):
    p = Project(
        id=str(uuid4()),
        organization_id=org.id,
        name="Side Project",
        description="A second project",
        alias="SP",
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


def _make_user(db_session, email: str, name: str, org=None, **extra) -> User:
    # No `username=`: User has no such field, and SQLModel drops an unknown
    # kwarg silently, so passing one reads like a column that isn't there.
    u = User(
        id=str(uuid4()),
        email=email,
        full_name=name.title(),
        **extra,
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    # Resolution is org-scoped: a user with no active membership in the org
    # being synced is never a match, so every user meant to resolve needs one.
    if org is not None:
        _add_membership(db_session, u, org)
    return u


def _add_membership(db_session, user: User, org, *, is_active: bool = True):
    m = OrganizationMembership(
        user_id=user.id, organization_id=org.id, is_active=is_active
    )
    db_session.add(m)
    db_session.commit()
    db_session.refresh(m)
    return m


@pytest.fixture
def alice(db_session, org):
    return _make_user(db_session, "Alice@Example.com", "alice", org=org)


@pytest.fixture
def bob(db_session, org):
    return _make_user(db_session, "bob@example.com", "bob", org=org)


def _board(db_session, org, project, board_type: BoardType) -> BoardRegistration:
    b = BoardRegistration(
        id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        board_name=f"{board_type.value} board",
        board_type=board_type,
        board_url="https://example.invalid",
        board_external_id="EX",
    )
    db_session.add(b)
    db_session.commit()
    db_session.refresh(b)
    return b


@pytest.fixture
def linear_board(db_session, org, project):
    return _board(db_session, org, project, BoardType.LINEAR)


@pytest.fixture
def trello_board(db_session, org, project):
    return _board(db_session, org, project, BoardType.TRELLO)


def _external(external_id: str, **extra) -> dict:
    base = {
        "id": external_id,
        "summary": "Do the thing",
        "description": None,
        "status": "To Do",
        "assignee": None,
        "url": None,
        "source_platform": None,
        "priority": None,
        "parent_external_id": None,
    }
    base.update(extra)
    return base


# ---------------------------------------------------------------------------
# Resolution order
# ---------------------------------------------------------------------------


def test_email_match_is_case_insensitive(db_session, org, project, alice):
    """`Alice@Example.com` on the user, `alice@EXAMPLE.COM` from the board."""
    match = IdentityResolutionService.resolve(
        db_session,
        organization_id=org.id,
        project_id=project.id,
        platform=IdentityPlatform.LINEAR,
        assignee=BoardAssignee(display_name="A. Lice", email="alice@EXAMPLE.COM"),
    )
    assert match is not None
    assert match.user.id == alice.id
    assert match.match_source == MatchSource.EMAIL


def test_email_match_also_considers_the_users_jira_email(db_session, org, project):
    """`users.jira_email` exists because the two addresses differ on Jira.

    An Atlassian account is routinely a different address from the InnoDay
    login — which is the main case the email path has to cover on the one
    board type that supplies an email at all.
    """
    carol = _make_user(
        db_session,
        "carol@innoday.example",
        "carol",
        org=org,
        jira_email="Carol.Atlassian@client.example",
    )

    match = IdentityResolutionService.resolve(
        db_session,
        organization_id=org.id,
        project_id=project.id,
        platform=IdentityPlatform.JIRA,
        assignee=BoardAssignee(
            display_name="C. Arol", email="carol.atlassian@CLIENT.example"
        ),
    )
    assert match is not None
    assert match.user.id == carol.id
    assert match.match_source == MatchSource.EMAIL


def test_handle_match_uses_global_row_when_no_project_override(
    db_session, org, project, alice
):
    IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.LINEAR,
        handle="A. Lice",
        project_id=None,
    )
    match = IdentityResolutionService.resolve(
        db_session,
        organization_id=org.id,
        project_id=project.id,
        platform=IdentityPlatform.LINEAR,
        assignee=BoardAssignee(display_name="A. Lice"),
    )
    assert match is not None
    assert match.user.id == alice.id
    assert match.match_source == MatchSource.HANDLE


def test_the_project_scoped_row_is_the_one_that_answers(
    db_session, org, project, other_project, alice
):
    """Which row won, not just which user.

    Both rows name the same user — the claim rule guarantees that, so a
    `match.user.id` assertion passes whichever row is picked and proves
    nothing. `project_scoped` is the observable that distinguishes them: True
    inside the project that has its own row, False for a project that falls
    back to the global one.
    """
    IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.LINEAR,
        handle="shared-handle",
        project_id=None,
    )
    # Same user, same handle, scoped to one project.
    IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.LINEAR,
        handle="shared-handle",
        project_id=project.id,
    )
    rows = db_session.exec(
        select(UserIdentity).where(UserIdentity.handle == "shared-handle")
    ).all()
    assert len(rows) == 2

    def resolve_for(project_id):
        return IdentityResolutionService.resolve(
            db_session,
            organization_id=org.id,
            project_id=project_id,
            platform=IdentityPlatform.LINEAR,
            assignee=BoardAssignee(display_name="shared-handle"),
        )

    scoped = resolve_for(project.id)
    assert scoped is not None
    assert scoped.user.id == alice.id
    assert scoped.project_scoped is True

    # A project with no row of its own falls back to the global one, and says
    # so — and says the same thing every time, not whatever the database
    # happened to return first.
    fallbacks = [resolve_for(other_project.id) for _ in range(3)]
    assert all(m is not None and m.user.id == alice.id for m in fallbacks)
    assert [m.project_scoped for m in fallbacks] == [False, False, False]


def test_unknown_display_name_is_unmatched_not_fuzzy_matched(
    db_session, org, project, alice
):
    """`alice` exists; the board says `Alice Smith`. That is NOT a match."""
    match = IdentityResolutionService.resolve(
        db_session,
        organization_id=org.id,
        project_id=project.id,
        platform=IdentityPlatform.LINEAR,
        assignee=BoardAssignee(display_name="Alice Smith"),
    )
    assert match is None


def test_board_with_no_email_is_unmatched_without_error(
    db_session, org, project, alice
):
    """Trello exposes no member email — unmatched is the correct outcome."""
    match = IdentityResolutionService.resolve(
        db_session,
        organization_id=org.id,
        project_id=project.id,
        platform=IdentityPlatform.TRELLO,
        assignee=BoardAssignee(display_name="alice", email=None),
    )
    assert match is None


def test_handle_of_another_platform_does_not_match(db_session, org, project, alice):
    IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.JIRA,
        handle="A. Lice",
    )
    match = IdentityResolutionService.resolve(
        db_session,
        organization_id=org.id,
        project_id=project.id,
        platform=IdentityPlatform.LINEAR,
        assignee=BoardAssignee(display_name="A. Lice"),
    )
    assert match is None


# ---------------------------------------------------------------------------
# Organization scope
#
# Every case below builds both organizations explicitly rather than leaning on
# whatever memberships happen to exist: on dev every user is a platform member,
# so the boundary these tests describe is not observable there by accident.
# ---------------------------------------------------------------------------


@pytest.fixture
def other_org(db_session):
    o = Organization(id=str(uuid4()), name="Someone Else Entirely Ltd")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


def test_email_of_a_user_in_another_organization_is_unmatched(
    db_session, org, other_org, project
):
    """The tenancy leak this scoping closes.

    `users.email` is globally unique, so the address does identify the right
    human — but they belong to another org, and syncing org A's board must
    never write their id into org A's tickets.
    """
    outsider = _make_user(db_session, "dave@other.example", "dave", org=other_org)

    match = IdentityResolutionService.resolve(
        db_session,
        organization_id=org.id,
        project_id=project.id,
        platform=IdentityPlatform.LINEAR,
        assignee=BoardAssignee(display_name="D. Ave", email="dave@other.example"),
    )
    assert match is None

    # Same person, same email, resolved for the org they are actually in.
    match = IdentityResolutionService.resolve(
        db_session,
        organization_id=other_org.id,
        project_id=None,
        platform=IdentityPlatform.LINEAR,
        assignee=BoardAssignee(display_name="D. Ave", email="dave@other.example"),
    )
    assert match is not None
    assert match.user.id == outsider.id


def test_email_of_a_deactivated_member_is_unmatched(db_session, org, project):
    """A membership row is not enough — it has to be active.

    Deactivating is how someone leaves an org without erasing their history;
    resolving to them again would quietly undo that.
    """
    erin = _make_user(db_session, "erin@example.com", "erin")
    _add_membership(db_session, erin, org, is_active=False)

    match = IdentityResolutionService.resolve(
        db_session,
        organization_id=org.id,
        project_id=project.id,
        platform=IdentityPlatform.LINEAR,
        assignee=BoardAssignee(display_name="E. Rin", email="erin@example.com"),
    )
    assert match is None


def test_a_non_member_cannot_shadow_a_member_on_jira_email(
    db_session, org, other_org, project
):
    """Why membership is a JOIN and not a check on the result.

    `users.email` is unique but `users.jira_email` is not, so two users can
    answer one Atlassian address. Filtering after `.first()` would let the
    outsider win the ordering and turn a real match into None.
    """
    shared = "shared.atlassian@client.example"
    _make_user(
        db_session,
        "outsider@other.example",
        "outsider",
        org=other_org,
        jira_email=shared,
    )
    insider = _make_user(
        db_session, "insider@example.com", "insider", org=org, jira_email=shared
    )

    match = IdentityResolutionService.resolve(
        db_session,
        organization_id=org.id,
        project_id=project.id,
        platform=IdentityPlatform.JIRA,
        assignee=BoardAssignee(display_name="S. Hared", email=shared),
    )
    assert match is not None
    assert match.user.id == insider.id


def test_a_global_handle_row_does_not_reach_across_organizations(
    db_session, org, other_org, project
):
    """A `project_id IS NULL` row is cross-project, not cross-organization.

    It is the easier way in of the two — one row, claimed once, answering for
    every board on the platform — so it gets the same membership rule as the
    email path rather than a weaker one.
    """
    frank = _make_user(db_session, "frank@other.example", "frank", org=other_org)
    IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=frank.id,
        platform=IdentityPlatform.LINEAR,
        handle="F. Rank",
        project_id=None,
    )

    assert (
        IdentityResolutionService.resolve(
            db_session,
            organization_id=org.id,
            project_id=project.id,
            platform=IdentityPlatform.LINEAR,
            assignee=BoardAssignee(display_name="F. Rank"),
        )
        is None
    )

    # The row still does its job for the org Frank belongs to.
    match = IdentityResolutionService.resolve(
        db_session,
        organization_id=other_org.id,
        project_id=None,
        platform=IdentityPlatform.LINEAR,
        assignee=BoardAssignee(display_name="F. Rank"),
    )
    assert match is not None
    assert match.user.id == frank.id


def test_sync_does_not_assign_a_ticket_to_a_user_from_another_org(
    db_session, org, other_org, project, linear_board
):
    """End to end through board sync, not just the resolver."""
    _make_user(db_session, "grace@other.example", "grace", org=other_org)

    _, ticket = BoardSyncService()._create_or_update_ticket(
        _external(
            "PF-20",
            assignee="G. Race",
            assignee_email="grace@other.example",
        ),
        linear_board,
        db_session,
        project_id=project.id,
    )

    assert ticket.assignee == "G. Race"  # the board's word is still recorded
    assert ticket.assigned_to is None


# ---------------------------------------------------------------------------
# Claiming a handle
# ---------------------------------------------------------------------------


def test_claim_refuses_handle_already_held_by_another_user(
    db_session, org, project, other_project, alice, bob
):
    IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.LINEAR,
        handle="A. Lice",
        project_id=project.id,
    )

    # A different project does not make it available to someone else: the
    # claim is checked across every project.
    with pytest.raises(HandleAlreadyClaimedError):
        IdentityResolutionService.claim_identity(
            db_session,
            organization_id=org.id,
            user_id=bob.id,
            platform=IdentityPlatform.LINEAR,
            handle="A. Lice",
            project_id=other_project.id,
        )

    rows = db_session.exec(
        select(UserIdentity).where(UserIdentity.handle == "A. Lice")
    ).all()
    assert len(rows) == 1
    assert rows[0].user_id == alice.id  # not overwritten


def test_same_user_may_hold_one_handle_in_two_projects(
    db_session, org, project, other_project, alice
):
    first = IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.LINEAR,
        handle="A. Lice",
        project_id=project.id,
    )
    second = IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.LINEAR,
        handle="A. Lice",
        project_id=other_project.id,
    )
    assert first.id != second.id
    assert {first.project_id, second.project_id} == {project.id, other_project.id}


def test_the_database_refuses_a_second_global_owner_for_one_handle(
    db_session, alice, bob
):
    """The Python claim rule is not the only thing holding this up.

    `claim_identity` checks for a conflicting row and then inserts, with no
    lock between the two — so two concurrent claims can both pass the check.
    `UNIQUE(project_id, platform, handle)` does not catch it either: NULLs
    never compare equal, so two global rows for one handle naming different
    users used to commit happily. The partial unique index is what makes that
    impossible.
    """
    from sqlalchemy.exc import IntegrityError

    db_session.add(
        UserIdentity(
            user_id=alice.id,
            project_id=None,
            platform=IdentityPlatform.LINEAR,
            handle="contested",
        )
    )
    db_session.commit()

    db_session.add(
        UserIdentity(
            user_id=bob.id,
            project_id=None,
            platform=IdentityPlatform.LINEAR,
            handle="contested",
        )
    )
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_a_project_row_does_not_collide_with_the_global_one(
    db_session, org, project, alice
):
    """The index is partial: it must not reach project-scoped rows."""
    IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.LINEAR,
        handle="A. Lice",
        project_id=None,
    )
    IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.LINEAR,
        handle="A. Lice",
        project_id=project.id,
    )
    db_session.commit()

    rows = db_session.exec(
        select(UserIdentity).where(UserIdentity.handle == "A. Lice")
    ).all()
    assert len(rows) == 2


def test_reclaiming_the_same_row_is_idempotent(db_session, org, project, alice):
    first = IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.LINEAR,
        handle="A. Lice",
        project_id=project.id,
    )
    second = IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.LINEAR,
        handle="A. Lice",
        project_id=project.id,
        board_user_id="lin_123",
    )
    assert first.id == second.id
    assert second.board_user_id == "lin_123"


# ---------------------------------------------------------------------------
# Board sync wiring
# ---------------------------------------------------------------------------


def test_sync_populates_assigned_to_for_a_mapped_user(
    db_session, org, project, linear_board, alice
):
    IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.LINEAR,
        handle="A. Lice",
    )

    _, ticket = BoardSyncService()._create_or_update_ticket(
        _external("PF-1", assignee="A. Lice"),
        linear_board,
        db_session,
        project_id=project.id,
    )

    assert ticket.assigned_to == alice.id


def test_sync_leaves_assigned_to_null_for_an_unmapped_assignee(
    db_session, project, linear_board
):
    _, ticket = BoardSyncService()._create_or_update_ticket(
        _external("PF-2", assignee="Nobody In Particular"),
        linear_board,
        db_session,
        project_id=project.id,
    )

    assert ticket.assigned_to is None


def test_sync_matches_on_email_supplied_by_the_board(
    db_session, project, linear_board, alice
):
    _, ticket = BoardSyncService()._create_or_update_ticket(
        _external(
            "PF-3",
            assignee="Whatever Linear Calls Her",
            assignee_email="ALICE@example.com",
        ),
        linear_board,
        db_session,
        project_id=project.id,
    )

    assert ticket.assigned_to == alice.id


def test_sync_of_a_trello_ticket_without_email_is_unmatched_and_does_not_raise(
    db_session, project, trello_board, alice
):
    _, ticket = BoardSyncService()._create_or_update_ticket(
        _external("TR-1", assignee="alice"),
        trello_board,
        db_session,
        project_id=project.id,
    )

    assert ticket.assigned_to is None


def test_resolution_failure_never_fails_the_sync(
    db_session, project, linear_board, monkeypatch
):
    def boom(*args, **kwargs):
        raise RuntimeError("identity backend exploded")

    monkeypatch.setattr(IdentityResolutionService, "resolve", boom)

    _, ticket = BoardSyncService()._create_or_update_ticket(
        _external("PF-4", assignee="A. Lice"),
        linear_board,
        db_session,
        project_id=project.id,
    )

    assert ticket.assigned_to is None
    assert ticket.summary == "Do the thing"


def test_resync_updates_assigned_to_on_an_existing_ticket(
    db_session, org, project, linear_board, alice
):
    service = BoardSyncService()
    _, ticket = service._create_or_update_ticket(
        _external("PF-5", assignee="A. Lice"),
        linear_board,
        db_session,
        project_id=project.id,
    )
    db_session.commit()
    assert ticket.assigned_to is None  # not mapped yet

    IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.LINEAR,
        handle="A. Lice",
    )

    was_created, ticket = service._create_or_update_ticket(
        _external("PF-5", assignee="A. Lice"),
        linear_board,
        db_session,
        project_id=project.id,
    )
    assert was_created is False
    assert ticket.assigned_to == alice.id


# ---------------------------------------------------------------------------
# Adapters surface the board's email where the board has one
# ---------------------------------------------------------------------------


def test_linear_adapter_query_requests_the_assignee_email():
    """Without `email` in the selection set Linear simply omits it."""
    from src.api.linear_api import _ISSUE_FIELDS

    selection = " ".join(_ISSUE_FIELDS.split())
    assert "assignee { id name email }" in selection


def test_jira_adapter_surfaces_email_address(db_session, org, project):
    from src.adapters.board_assignee import read_board_assignee
    from src.adapters.jira_adapter import JiraBoardAdapter

    registration = _board(db_session, org, project, BoardType.JIRA)
    adapter = JiraBoardAdapter.__new__(JiraBoardAdapter)
    adapter.board_registration = registration
    adapter.board_id = "EX"
    adapter.api = SimpleNamespace(base_url="https://example.atlassian.net")

    ticket = adapter._issue_to_ticket(
        {
            "key": "EX-1",
            "fields": {
                "summary": "A jira issue",
                "status": {"name": "To Do"},
                "assignee": {
                    "displayName": "A. Lice",
                    "emailAddress": "alice@example.com",
                    "accountId": "acct-1",
                },
            },
        }
    )

    assert ticket.assignee == "A. Lice"
    surfaced = read_board_assignee(ticket)
    assert surfaced is not None
    assert surfaced.email == "alice@example.com"
    assert surfaced.board_user_id == "acct-1"


def test_jira_adapter_tolerates_a_privacy_hidden_email(db_session, org, project):
    from src.adapters.board_assignee import read_board_assignee
    from src.adapters.jira_adapter import JiraBoardAdapter

    registration = _board(db_session, org, project, BoardType.JIRA)
    adapter = JiraBoardAdapter.__new__(JiraBoardAdapter)
    adapter.board_registration = registration
    adapter.board_id = "EX"
    adapter.api = SimpleNamespace(base_url="https://example.atlassian.net")

    ticket = adapter._issue_to_ticket(
        {
            "key": "EX-2",
            "fields": {
                "summary": "A jira issue",
                "status": {"name": "To Do"},
                "assignee": {"displayName": "A. Lice"},
            },
        }
    )

    assert ticket.assignee == "A. Lice"
    assert read_board_assignee(ticket).email is None


@pytest.mark.asyncio
async def test_jira_raw_fetch_carries_the_same_assignee_fields_as_the_adapter(
    monkeypatch,
):
    """`_fetch_jira_issues` bypasses the adapter, so it has to agree with it.

    It already carried `assignee_email`; without `assignee_board_user_id` the
    raw-fetch path handed the resolver a differently-shaped assignee from the
    adapter path for the same board.
    """
    import httpx

    issue = {
        "key": "EX-1",
        "fields": {
            "summary": "A jira issue",
            "status": {"name": "To Do"},
            "assignee": {
                "displayName": "A. Lice",
                "emailAddress": "alice@example.com",
                "accountId": "acct-1",
            },
        },
    }

    class _Response:
        status_code = 200

        @staticmethod
        def json():
            return {"issues": [issue]}

    class _Client:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return False

        async def get(self, *args, **kwargs):
            return _Response()

    monkeypatch.setattr(httpx, "AsyncClient", lambda *a, **k: _Client())

    api_client = SimpleNamespace(
        base_url="https://example.atlassian.net", auth=None, headers={}
    )
    issues = await BoardSyncService()._fetch_jira_issues(api_client, "EX", "tok")

    assert len(issues) == 1
    assert issues[0]["assignee"] == "A. Lice"
    assert issues[0]["assignee_email"] == "alice@example.com"
    assert issues[0]["assignee_board_user_id"] == "acct-1"


def test_external_dict_carries_the_board_email_through_to_sync():
    from src.domain.board import BoardType as BT

    ticket = Ticket(
        summary="s",
        organization_id="o",
        project_id="p",
        assignee="A. Lice",
        external_ticket_id="PF-9",
        status=TicketStatus.TODO,
    )
    attach_board_assignee(
        ticket, BoardAssignee(display_name="A. Lice", email="alice@example.com")
    )

    class _Reg:
        board_type = BT.LINEAR

    external = BoardSyncService._ticket_to_external_dict(ticket, _Reg())
    assert external["assignee"] == "A. Lice"
    assert external["assignee_email"] == "alice@example.com"


# ---------------------------------------------------------------------------
# check_status's assigned-ticket count
# ---------------------------------------------------------------------------


def test_sync_writes_the_board_assignee_string_and_keeps_it_current(
    db_session, org, project, linear_board, alice
):
    """`Ticket.assignee` records the board's raw display name, on both paths.

    The two columns are independent: `assignee` is what the board said,
    `assigned_to` is the resolved FK. A board reassignment must move both —
    leaving the previous name behind would make the row disagree with the
    board it mirrors.
    """
    IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.LINEAR,
        handle="A. Lice",
    )
    service = BoardSyncService()

    _, created = service._create_or_update_ticket(
        _external("PF-7", assignee="A. Lice"),
        linear_board,
        db_session,
        project_id=project.id,
    )
    assert created.assignee == "A. Lice"
    assert created.assigned_to == alice.id
    db_session.commit()

    # The board reassigns to someone InnoDay does not know.
    _, updated = service._create_or_update_ticket(
        _external("PF-7", assignee="Someone Else Entirely"),
        linear_board,
        db_session,
        project_id=project.id,
    )
    assert updated.assignee == "Someone Else Entirely"
    assert updated.assigned_to is None

    # And unassigning on the board clears both, rather than stranding a name.
    _, cleared = service._create_or_update_ticket(
        _external("PF-7", assignee=None),
        linear_board,
        db_session,
        project_id=project.id,
    )
    assert cleared.assignee is None
    assert cleared.assigned_to is None


def test_ticket_assignee_string_holds_the_display_name_not_a_user_id(
    db_session, org, project, linear_board, alice
):
    """The bug this slice fixes, pinned.

    `assignee` now holds a real value, and it is the board's display name —
    so filtering on `Ticket.assignee == <user uuid>`, what check_status used
    to do, still finds nothing. `assigned_to` is the column that answers
    "assigned to me".
    """
    IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.LINEAR,
        handle="A. Lice",
    )
    BoardSyncService()._create_or_update_ticket(
        _external("PF-6", assignee="A. Lice"),
        linear_board,
        db_session,
        project_id=project.id,
    )
    db_session.commit()

    by_string = db_session.exec(select(Ticket).where(Ticket.assignee == alice.id)).all()
    by_display_name = db_session.exec(
        select(Ticket).where(Ticket.assignee == "A. Lice")
    ).all()
    by_fk = db_session.exec(select(Ticket).where(Ticket.assigned_to == alice.id)).all()

    assert len(by_display_name) == 1, "the column must actually be populated"
    assert by_string == [], "and what it holds is never a user id"
    assert len(by_fk) == 1


@pytest.fixture
def synced_tickets(db_session, org, project, linear_board, alice):
    """One ticket resolved to alice, one assigned to a stranger."""
    IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.LINEAR,
        handle="A. Lice",
    )
    service = BoardSyncService()
    for external_id, assignee in (("PF-10", "A. Lice"), ("PF-11", "A. Stranger")):
        service._create_or_update_ticket(
            _external(external_id, assignee=assignee),
            linear_board,
            db_session,
            project_id=project.id,
        )
    db_session.commit()


@pytest.mark.asyncio
async def test_project_route_filters_on_the_assigned_to_fk(
    db_session, org, project, alice, synced_tickets
):
    """The route the CLI's `status` calls: a user id must filter on the FK."""
    from src.routers.tickets import get_project_tickets

    async def fetch(**filters):
        return await get_project_tickets(
            organization_id=org.id,
            project_id=project.id,
            current_user=alice,
            session=db_session,
            **filters,
        )

    assert len(await fetch()) == 2

    by_fk = await fetch(assigned_to=alice.id)
    assert [t.external_ticket_id for t in by_fk] == ["PF-10"]

    # The old CLI behaviour: a user id sent as `assignee` matches nothing.
    assert await fetch(assignee=alice.id) == []

    by_name = await fetch(assignee="A. Lice")
    assert [t.external_ticket_id for t in by_name] == ["PF-10"]


@pytest.mark.asyncio
async def test_org_route_filters_on_the_assigned_to_fk(
    db_session, org, alice, synced_tickets
):
    """The org-level `assigned_to` filter, which nothing covered."""
    from src.routers.tickets import get_all_organization_tickets

    async def fetch(**filters):
        return await get_all_organization_tickets(
            organization_id=org.id,
            current_user=alice,
            session=db_session,
            **filters,
        )

    assert len(await fetch()) == 2

    by_fk = await fetch(assigned_to=alice.id)
    assert [t.external_ticket_id for t in by_fk] == ["PF-10"]

    assert await fetch(assignee=alice.id) == []
    assert [t.external_ticket_id for t in await fetch(assignee="A. Stranger")] == [
        "PF-11"
    ]


@pytest.mark.asyncio
async def test_check_status_count_filters_on_the_assigned_to_fk(monkeypatch):
    """`_get_assigned_tickets_count` must send `assigned_to`, not `assignee`."""
    from src.mcp import server

    captured = {}

    async def fake_get(path, params=None):
        captured["path"] = path
        captured["params"] = params or {}
        return []

    monkeypatch.setattr(server._api, "get", fake_get)
    monkeypatch.setattr(server.config, "user_id", "user-uuid-1", raising=False)

    await server._get_assigned_tickets_count("org-1")

    assert captured["params"].get("assigned_to") == "user-uuid-1"
    assert "assignee" not in captured["params"]


# ---------------------------------------------------------------------------
# The claim rule is intra-organisation
# ---------------------------------------------------------------------------


def test_two_organizations_may_independently_hold_the_same_handle(
    db_session, org, other_org, project, alice
):
    """Two tenants with a `Sam Patel` each is two people, not a collision.

    The conflict check used to match on `(platform, handle)` with no scope at
    all, so whichever org claimed a common display name first blocked every
    other org's member from the same string on a board they share nothing with
    -- and the refusal doubled as a readable "does anybody, anywhere, hold this?"
    oracle for tenants the caller cannot otherwise see.
    """
    outsider = _make_user(db_session, "sam@other.example", "sam patel", org=other_org)

    mine = IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.LINEAR,
        handle="Sam Patel",
        project_id=project.id,
    )
    theirs = IdentityResolutionService.claim_identity(
        db_session,
        organization_id=other_org.id,
        user_id=outsider.id,
        platform=IdentityPlatform.LINEAR,
        handle="Sam Patel",
    )

    assert mine.id != theirs.id
    assert mine.user_id == alice.id
    assert theirs.user_id == outsider.id


def test_within_one_organization_the_refusal_still_fires(
    db_session, org, project, other_project, alice, bob
):
    """Scoping the check must not weaken the rule where it means something."""
    IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.LINEAR,
        handle="Shared Name",
        project_id=project.id,
    )

    with pytest.raises(HandleAlreadyClaimedError):
        IdentityResolutionService.claim_identity(
            db_session,
            organization_id=org.id,
            user_id=bob.id,
            platform=IdentityPlatform.LINEAR,
            handle="Shared Name",
            # A *different* project in the same org: the rule is org-wide, not
            # project-wide, because the global fallback would be ambiguous.
            project_id=other_project.id,
        )


def test_a_departed_member_still_occupying_the_slot_is_refused(
    db_session, org, project, other_project, alice
):
    """Membership scopes the rule; it cannot be the whole of it.

    `UNIQUE(project_id, platform, handle)` means one row per scope, so whoever
    is in the scope being claimed is a conflict however their membership reads.
    Without this the caller was handed the *departed* user's row back as though
    the claim had succeeded -- a silent mis-mapping, which is worse than the
    refusal it replaced.
    """
    departed = _make_user(db_session, "gone@example.com", "gone", org=org)
    membership = db_session.exec(
        select(OrganizationMembership).where(
            OrganizationMembership.user_id == departed.id
        )
    ).one()
    IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=departed.id,
        platform=IdentityPlatform.LINEAR,
        handle="Reused Name",
        project_id=project.id,
    )
    membership.is_active = False
    db_session.add(membership)
    db_session.commit()

    with pytest.raises(HandleAlreadyClaimedError):
        IdentityResolutionService.claim_identity(
            db_session,
            organization_id=org.id,
            user_id=alice.id,
            platform=IdentityPlatform.LINEAR,
            handle="Reused Name",
            project_id=project.id,
        )

    # A different scope is free: nothing occupies it, and the departed member
    # has no active membership to scope the rule by.
    claimed = IdentityResolutionService.claim_identity(
        db_session,
        organization_id=org.id,
        user_id=alice.id,
        platform=IdentityPlatform.LINEAR,
        handle="Reused Name",
        project_id=other_project.id,
    )
    assert claimed.user_id == alice.id


# ---------------------------------------------------------------------------
# A commit handle mapped from the Team page must actually resolve (#569)
# ---------------------------------------------------------------------------


def test_a_github_login_resolves_through_users_github_username(
    db_session, org, project
):
    """The fix for a control that looked like it worked.

    The Team page's commit-handle mapping writes `users.github_username` and
    nothing else, while resolution read only `user_identity`. So mapping a handle
    stopped it appearing in the unmapped list — that list matches
    `github_username` — and every summary that followed still showed the author as
    unmapped. The mapping appeared to take and changed nothing that mattered.
    """
    dan = _make_user(
        db_session, "dan@innoday.example", "dan", org=org, github_username="dgillen27"
    )

    match = IdentityResolutionService.resolve(
        db_session,
        organization_id=org.id,
        project_id=project.id,
        platform=IdentityPlatform.GITHUB,
        assignee=BoardAssignee(display_name="dgillen27"),
    )
    assert match is not None
    assert match.user.id == dan.id
    # Not `HANDLE` -- that is the registered-row answer, and since the row was
    # made to beat this column (#593) the two had to stop sharing a label or
    # "the override fired" and "there was no override" read identically.
    assert match.match_source == MatchSource.GITHUB_USERNAME

    # Case-insensitive: a GitHub login is not case-sensitive, and a branch or a
    # commit author may carry either casing.
    assert (
        IdentityResolutionService.resolve(
            db_session,
            organization_id=org.id,
            project_id=project.id,
            platform=IdentityPlatform.GITHUB,
            assignee=BoardAssignee(display_name="DGillen27"),
        )
        is not None
    )


def test_a_github_username_does_not_cross_the_membership_boundary(
    db_session, org, project
):
    """Same rule as the email path, and for a sharper reason here.

    `github_username` carries no uniqueness constraint, so two users can hold the
    same login — filtering after a `.first()` would let a non-member shadow a
    member. The membership is a JOIN for exactly that reason.
    """
    _make_user(
        db_session, "outside@other.example", "outsider", github_username="shared"
    )

    assert (
        IdentityResolutionService.resolve(
            db_session,
            organization_id=org.id,
            project_id=project.id,
            platform=IdentityPlatform.GITHUB,
            assignee=BoardAssignee(display_name="shared"),
        )
        is None
    ), "a non-member holding the login is not a match"

    member = _make_user(
        db_session,
        "inside@innoday.example",
        "insider",
        org=org,
        github_username="shared",
    )
    match = IdentityResolutionService.resolve(
        db_session,
        organization_id=org.id,
        project_id=project.id,
        platform=IdentityPlatform.GITHUB,
        assignee=BoardAssignee(display_name="shared"),
    )
    assert match is not None and match.user.id == member.id


def test_github_username_is_not_consulted_for_another_platform(
    db_session, org, project
):
    """A Linear display name is not a GitHub login.

    Without the platform guard, somebody whose GitHub login happened to match
    another person's Linear display name would be credited with their board work.
    """
    _make_user(
        db_session,
        "ada@innoday.example",
        "ada",
        org=org,
        github_username="Ada Lovelace",
    )

    assert (
        IdentityResolutionService.resolve(
            db_session,
            organization_id=org.id,
            project_id=project.id,
            platform=IdentityPlatform.LINEAR,
            assignee=BoardAssignee(display_name="Ada Lovelace"),
        )
        is None
    )


def test_a_registered_user_identity_still_wins_for_a_project_override(
    db_session, org, project, alice
):
    """The explicit row beats the automatic column, both ways round.

    `users.github_username` is written without anybody deciding anything about
    attribution — the profile page sets it, and so does an account connection. A
    `user_identity` row is only ever created by somebody saying "this handle is
    that person". Reading the column first let the automatic value shadow the
    deliberate one, so a project-scoped override — made precisely because the
    generic answer was wrong — stopped answering the moment anyone's login
    happened to match.

    Asserted with both present and naming *different* people, which is the only
    arrangement that can tell which one answered.
    """
    bob = _make_user(db_session, "bob@innoday.example", "bob", org=org)
    db_session.add(
        UserIdentity(
            user_id=bob.id,
            project_id=project.id,
            platform=IdentityPlatform.GITHUB,
            handle="contested",
            match_source=MatchSource.MANUAL,
        )
    )
    alice.github_username = "contested"
    db_session.add(alice)
    db_session.commit()

    match = IdentityResolutionService.resolve(
        db_session,
        organization_id=org.id,
        project_id=project.id,
        platform=IdentityPlatform.GITHUB,
        assignee=BoardAssignee(display_name="contested"),
    )
    assert match is not None
    assert match.user.id == bob.id, "the row that somebody wrote on purpose wins"
    assert match.project_scoped is True
    assert match.match_source == MatchSource.HANDLE

    # And the column is still the answer where no row claims the handle — the
    # ordering must not turn into "the column is never read".
    alice.github_username = "uncontested"
    db_session.add(alice)
    db_session.commit()
    fallback = IdentityResolutionService.resolve(
        db_session,
        organization_id=org.id,
        project_id=project.id,
        platform=IdentityPlatform.GITHUB,
        assignee=BoardAssignee(display_name="uncontested"),
    )
    assert fallback is not None and fallback.user.id == alice.id

    # The two are told apart by the label alone: same platform, same shape of
    # answer, different store. Sharing `HANDLE` for both is what made "did the
    # deliberate override answer?" unanswerable once the row started winning.
    assert fallback.match_source == MatchSource.GITHUB_USERNAME
    assert fallback.match_source != match.match_source
