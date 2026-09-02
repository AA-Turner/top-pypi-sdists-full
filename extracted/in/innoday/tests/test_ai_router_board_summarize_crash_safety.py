"""
`POST /api/v1/ai/boards/summarize` (src/routers/ai.py::summarize_board) is a
distinct, still-live server-side Anthropic-calling path -- separate from the
interactive board-summary flow in src/routers/boards.py that HS-297 replaces
with the two-step get_board_summary_data / save_board_summary flow.

There is no calling Claude Code session attached to this endpoint (it's a
generic AI endpoint, not part of the MCP/CLI interactive summarize flow),
so it keeps calling ClaudeAPI directly.

Two things are covered here, and the second exists because of the first.

**Crash safety (HS-297).** Any remaining server-side Anthropic path must catch
an invalid/missing API key cleanly and return a clear HTTP error rather than
crashing with an unhandled exception (e.g. a raw 401 from Anthropic).

**Persistence (PF-398).** The route's own `session.commit()` sits inside that
same `except` -- so *any* failure while building the row is laundered into a
generic 500 with the real cause only in the log line. That is precisely how the
route came to construct a `Summary` with `summary_text=`, a kwarg matching no
field on the model, and go unnoticed: the happy path was never tested, only the
two failure paths above, and the failure paths cannot tell "Anthropic refused"
apart from "the insert was invalid". The happy-path test below reads the row
back out of the database, which is the only assertion the broken versions could
not have passed.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from anthropic import APIStatusError
from fastapi import HTTPException
from sqlmodel import select

from src.domain.board import BoardRegistration, BoardType
from src.domain.summary import Summary
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


@pytest.fixture
def seeded_ticket(db_session, org, project, board_registration):
    t = Ticket(
        organization_id=org.id,
        project_id=project.id,
        board_registration_id=board_registration.id,
        summary="Test ticket",
        status=TicketStatus.IN_PROGRESS,
    )
    db_session.add(t)
    db_session.commit()
    return t


@pytest.mark.asyncio
async def test_returns_clean_error_on_invalid_api_key(
    db_session, org, board_registration, seeded_ticket
):
    """Invalid/missing CLAUDE_API_KEY must surface as a clean HTTPException,
    not an unhandled 401 exception from the Anthropic SDK."""
    from src.routers.ai import BoardSummaryRequest, summarize_board

    current_user = MagicMock()
    current_user.id = "test-user"

    request = BoardSummaryRequest(board_id=board_registration.id)

    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.request = MagicMock()

    with patch("src.routers.ai.ClaudeAPI") as mock_claude_cls:
        mock_claude_cls.side_effect = APIStatusError(
            "invalid x-api-key",
            response=mock_response,
            body={"error": {"message": "invalid x-api-key"}},
        )

        with pytest.raises(HTTPException) as exc_info:
            await summarize_board(
                request=request, session=db_session, current_user=current_user
            )

    # Must be a clean, structured error -- not a bare/unhandled exception.
    assert exc_info.value.status_code == 500
    assert "Failed to summarize board" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_returns_clean_error_on_missing_api_key(
    db_session, org, board_registration, seeded_ticket
):
    """A missing CLAUDE_API_KEY raises ValueError inside ClaudeAPI() -- must
    still be caught cleanly rather than crashing the request."""
    from src.routers.ai import BoardSummaryRequest, summarize_board

    current_user = MagicMock()
    current_user.id = "test-user"

    request = BoardSummaryRequest(board_id=board_registration.id)

    with patch("src.routers.ai.ClaudeAPI") as mock_claude_cls:
        mock_claude_cls.side_effect = ValueError(
            "Claude API key is required. Set CLAUDE_API_KEY in your environment."
        )

        with pytest.raises(HTTPException) as exc_info:
            await summarize_board(
                request=request, session=db_session, current_user=current_user
            )

    assert exc_info.value.status_code == 500
    assert "Failed to summarize board" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_the_generated_summary_is_actually_persisted(
    db_session, org, project, board_registration, seeded_ticket
):
    """The happy path: a row lands in `summaries` and holds the generated prose.

    Every column the model requires has to be supplied for this to pass.
    `motivational_quote` is NOT NULL and the route did not pass it, so the
    insert raised, the `except` turned it into a 500, and the route persisted
    nothing -- while a reader of the code saw a `session.commit()` and a
    comment claiming the persistence bug was already fixed.
    """
    from src.routers.ai import BoardSummaryRequest, summarize_board

    current_user = MagicMock()
    current_user.id = None  # created_by is a nullable FK; no seeded user here

    prose = "## Board Summary\n\nOne ticket is in progress."
    claude = MagicMock()
    claude.generate_response = AsyncMock(return_value=prose)

    with patch("src.routers.ai.ClaudeAPI", return_value=claude):
        response = await summarize_board(
            request=BoardSummaryRequest(board_id=board_registration.id),
            session=db_session,
            current_user=current_user,
        )

    assert response.success is True

    stored = db_session.exec(
        select(Summary).where(Summary.board_registration_id == board_registration.id)
    ).all()
    assert len(stored) == 1
    row = stored[0]
    assert row.id == response.result["summary_id"]
    assert row.body_markdown == prose
    assert row.organization_id == org.id
    assert row.project_id == project.id
    # The board-scoped sentinel, not a real window -- this route appends rather
    # than caching, so both live-uniqueness indexes must exempt its rows.
    assert row.window_spec == ""
    assert row.motivational_quote  # NOT NULL; the omission that broke the insert
    assert row.ticket_stats["total"] == 1


@pytest.mark.asyncio
async def test_repeated_summaries_of_one_board_all_persist(
    db_session, org, board_registration, seeded_ticket
):
    """Two calls, two rows -- the append path must not trip the unique indexes.

    This is what `window_spec=""` buys: the live-uniqueness rule keys on
    project+type+window, so without the exemption the second call would collide
    with the first and be laundered into the same generic 500.
    """
    from src.routers.ai import BoardSummaryRequest, summarize_board

    current_user = MagicMock()
    current_user.id = None

    claude = MagicMock()
    claude.generate_response = AsyncMock(return_value="prose")

    with patch("src.routers.ai.ClaudeAPI", return_value=claude):
        for _ in range(2):
            await summarize_board(
                request=BoardSummaryRequest(board_id=board_registration.id),
                session=db_session,
                current_user=current_user,
            )

    stored = db_session.exec(
        select(Summary).where(Summary.board_registration_id == board_registration.id)
    ).all()
    assert len(stored) == 2
