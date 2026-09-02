"""
Regression test for a TypeError that crashed board summary data assembly
whenever a ticket's completed_at/updated_at was naive (no tzinfo) -- older
synced tickets can have this, while the endpoint's `now` is always
UTC-aware. The coercion is `as_utc` in src/utils/time_windows.py; boards.py
carried a byte-equivalent private copy, `_as_utc_aware`, until #622 collapsed
the two.

HS-297: the original server-side-Anthropic `summarize_board_tickets`
endpoint this test exercised has been replaced by the two-step
get_board_summary_data (data-only) / save_board_summary (persistence)
flow. The naive-datetime regression this test guards lives in the shared
`_assemble_board_summary_data` data assembly, now exercised via
`get_board_summary_data`.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from src.domain.board import BoardRegistration, BoardType
from src.domain.summary import SummaryType
from src.domain.ticket import Ticket, TicketStatus


@pytest.fixture
def board_registration(db_session, org, project):
    b = BoardRegistration(
        id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        board_name="Test Board",
        board_type=BoardType.JIRA,
        board_url="https://example.atlassian.net",
        board_external_id="1",
    )
    db_session.add(b)
    db_session.commit()
    db_session.refresh(b)
    return b


def _make_ticket(
    org_id, board_id, project_id, *, status, completed_at=None, updated_at=None
):
    t = Ticket(
        organization_id=org_id,
        project_id=project_id,
        board_registration_id=board_id,
        summary="Test ticket",
        status=status,
        completed_at=completed_at,
    )
    if updated_at is not None:
        t.updated_at = updated_at
    return t


@pytest.mark.asyncio
async def test_summarize_survives_naive_completed_at(
    db_session, org, project, board_registration
):
    """A DONE ticket with a naive completed_at must not raise TypeError."""
    naive_done = _make_ticket(
        org.id,
        board_registration.id,
        project.id,
        status=TicketStatus.DONE,
        completed_at=datetime.utcnow(),  # naive -- no tzinfo
    )
    aware_in_progress = _make_ticket(
        org.id,
        board_registration.id,
        project.id,
        status=TicketStatus.IN_PROGRESS,
        updated_at=datetime.now(timezone.utc) - timedelta(days=1),
    )
    db_session.add_all([naive_done, aware_in_progress])
    db_session.commit()

    from src.routers.boards import get_board_summary_data

    current_user = MagicMock()
    current_user.id = "test-user"

    with patch("src.routers.boards.require_org_role"):
        result = await get_board_summary_data(
            organization_id=org.id,
            board_id=board_registration.id,
            summary_type=SummaryType.STATUS,
            since_version=None,
            github_org=None,
            session=db_session,
            current_user=current_user,
        )

    assert result["stats"]["completed_7d"] == 1
    assert result["stats"]["in_progress"] == 1


def test_as_utc_normalizes_naive_datetime():
    # Imported through `src.routers.boards` on purpose: what this file guards is
    # the coercion *this module* applies, whoever owns the implementation.
    from src.routers.boards import as_utc

    naive = datetime(2026, 1, 1, 12, 0, 0)
    result = as_utc(naive)
    assert result.tzinfo == timezone.utc
    assert result.replace(tzinfo=None) == naive


def test_as_utc_leaves_aware_datetime_untouched():
    from src.routers.boards import as_utc

    aware = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    assert as_utc(aware) is aware


def test_as_utc_passes_through_none():
    from src.routers.boards import as_utc

    assert as_utc(None) is None


def test_boards_uses_the_shared_coercion_and_not_a_second_copy():
    """#622: one datetime coercion, not two.

    `_as_utc_aware` was behaviourally identical to `as_utc` -- same None
    handling, same "naive means UTC" rule, same pass-through for an aware value
    -- in a codebase where mixing naive and aware datetimes has already cost a
    production fix. Two copies is two places for the rule to change.

    Asserted on identity rather than on the source text, so re-declaring the
    helper under the shared name would fail here too.
    """
    from src.routers import boards
    from src.utils.time_windows import as_utc

    assert boards.as_utc is as_utc
    assert not hasattr(boards, "_as_utc_aware")
