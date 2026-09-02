"""The adapter cache must not hand back a detached ORM row.

`BoardSyncService` is a module-level singleton and caches adapters in
`self.adapters` for the life of the process. Every adapter retains the
`BoardRegistration` it was built with, so once the session that produced that row
commits (expiring its attributes) and closes, the retained instance is both
detached and expired -- and the next `self.board_registration.<attr>` raises
`DetachedInstanceError`.

On dev this surfaced as `Failed to fetch Linear issues: Instance
<BoardRegistration ...> is not bound`, because `LinearBoardAdapter._issue_to_ticket`
reads `self.board_registration.organization_id` inside `get_tickets`' try block --
reporting a local session-lifecycle bug as an upstream Linear API failure.
"""

from __future__ import annotations

import pytest
from sqlmodel import Session

from src.adapters.base_adapter import BaseBoardAdapter
from src.domain import BoardRegistration
from src.services.board_sync_service import BoardSyncService
from tests.db_helpers import build_test_engine


class _StubAdapter(BaseBoardAdapter):
    """Minimal adapter: only the retained registration matters here."""

    async def initialize(self, token):  # pragma: no cover - not exercised
        return None

    async def validate_connection(self):  # pragma: no cover
        return True

    async def get_tickets(self, board_id, since=None):  # pragma: no cover
        return []

    async def get_ticket(self, ticket_id):  # pragma: no cover
        return None

    async def create_ticket(self, board_id, ticket_data):  # pragma: no cover
        return None

    async def update_ticket(self, ticket, updates):  # pragma: no cover
        return None

    async def update_ticket_status(self, ticket, new_status):  # pragma: no cover
        return None

    async def add_comment(self, ticket, comment):  # pragma: no cover
        return True

    async def get_board_metadata(self):  # pragma: no cover
        return {}


@pytest.fixture
def engine():
    eng = build_test_engine()
    return eng


def _registration(session: Session) -> BoardRegistration:
    reg = BoardRegistration(
        id="brd-1",
        organization_id="org-1",
        project_id="proj-1",
        board_name="PixelFuel",
        board_url="https://linear.app/havilandsoftware/team/PF",
        board_type="linear",
        board_external_id="TEAM-1",
        is_active=True,
    )
    session.add(reg)
    session.commit()
    session.refresh(reg)
    return reg


@pytest.mark.asyncio
async def test_cached_adapter_gets_the_live_registration(engine, monkeypatch):
    """A cache hit must rebind to the caller's row, not keep the stale one."""
    service = BoardSyncService()

    with Session(engine) as first_session:
        first = _registration(first_session)
        service.adapters[(first.id, "tok")] = _StubAdapter(first)
        # Commit + close is what poisons the retained instance: commit expires
        # every attribute, close detaches it.
        first_session.commit()

    # `first` is now detached with expired attributes -- reading it raises, which
    # is precisely the production failure.
    from sqlalchemy.orm.exc import DetachedInstanceError

    with pytest.raises(DetachedInstanceError):
        _ = first.organization_id

    with Session(engine) as second_session:
        live = second_session.get(BoardRegistration, "brd-1")
        adapter = await service._get_adapter(live, "tok", second_session)

        # Same cached object (the cache still works) ...
        assert adapter is service.adapters[("brd-1", "tok")]
        # ... but bound to a row that can actually be read.
        assert adapter.board_registration is live
        assert adapter.board_registration.organization_id == "org-1"
