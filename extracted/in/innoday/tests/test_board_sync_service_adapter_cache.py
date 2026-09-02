"""_get_adapter cached by board_id alone, so a rotated credential (innoday
board set-credential) was silently ignored for the life of the process --
the first adapter ever built for a board kept being reused with its
original, stale token. Cache key must include the token."""

from unittest.mock import Mock

import pytest

from src.domain.board import BoardType
from src.services.board_sync_service import BoardSyncService


def _make_jira_registration(board_id="board-1"):
    registration = Mock()
    registration.id = board_id
    registration.board_type = BoardType.JIRA
    registration.board_url = (
        "https://example.atlassian.net/jira/software/c/projects/X/boards/1"
    )
    registration.organization = None
    return registration


@pytest.mark.asyncio
class TestGetAdapterCache:
    async def test_rotated_token_builds_a_new_adapter_not_the_stale_cached_one(self):
        service = BoardSyncService()
        registration = _make_jira_registration()
        session = Mock()

        old_adapter = await service._get_adapter(
            registration, "old@example.com:old-token", session
        )
        new_adapter = await service._get_adapter(
            registration, "new@example.com:new-token", session
        )

        assert new_adapter is not old_adapter
        assert new_adapter.api.auth == ("new@example.com", "new-token")

    async def test_same_token_reuses_the_cached_adapter(self):
        service = BoardSyncService()
        registration = _make_jira_registration()
        session = Mock()

        first = await service._get_adapter(
            registration, "dev@example.com:secret-token", session
        )
        second = await service._get_adapter(
            registration, "dev@example.com:secret-token", session
        )

        assert first is second
