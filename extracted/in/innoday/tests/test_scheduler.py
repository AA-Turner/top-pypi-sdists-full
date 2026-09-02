"""Tests for the board sync scheduler."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.cli.commands.scheduler import SchedulerCommands, _BoardSyncScheduler


@pytest.fixture
def config():
    cfg = MagicMock()
    cfg.get_api_url.return_value = "http://localhost:8002"
    cfg.get_cli_token.return_value = "idt_test0.secret"
    cfg.get_team_secret.return_value = None
    cfg.get_current_organization.return_value = "example"
    cfg._config = {"organizations": {"example": {"id": "org-abc"}}}
    return cfg


@pytest.fixture
def scheduler():
    return _BoardSyncScheduler(
        api_url="http://localhost:8002",
        org_id="org-abc",
        interval_minutes=1,
        cli_token="idt_test0.secret",
    )


class TestBoardSyncScheduler:
    @pytest.mark.asyncio
    async def test_list_boards_list_response(self, scheduler):
        boards = [{"id": "b1", "board_name": "Board 1", "board_type": "jira"}]
        mock_resp = MagicMock()
        mock_resp.json.return_value = boards
        mock_resp.raise_for_status = MagicMock()

        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_resp)

        result = await scheduler._list_boards(mock_client)
        assert result == boards

    @pytest.mark.asyncio
    async def test_list_boards_dict_response(self, scheduler):
        boards = [{"id": "b2", "board_name": "Board 2", "board_type": "linear"}]
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"boards": boards}
        mock_resp.raise_for_status = MagicMock()

        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_resp)

        result = await scheduler._list_boards(mock_client)
        assert result == boards

    @pytest.mark.asyncio
    async def test_sync_board_success(self, scheduler):
        mock_resp = MagicMock()
        mock_resp.status_code = 202
        mock_resp.is_success = True

        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_resp)

        result = await scheduler._sync_board(mock_client, {"id": "b1"})
        assert result["ok"] is True
        assert result["status_code"] == 202

    @pytest.mark.asyncio
    async def test_sync_board_failure(self, scheduler):
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.is_success = False

        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_resp)

        result = await scheduler._sync_board(mock_client, {"id": "b1"})
        assert result["ok"] is False
        assert result["status_code"] == 404

    @pytest.mark.asyncio
    async def test_run_once_success(self, scheduler):
        boards = [{"id": "b1", "board_name": "Test", "board_type": "jira"}]
        with (
            patch.object(scheduler, "_list_boards", AsyncMock(return_value=boards)),
            patch.object(
                scheduler,
                "_sync_board",
                AsyncMock(
                    return_value={"ok": True, "status_code": 202, "board_id": "b1"}
                ),
            ),
            patch("httpx.AsyncClient") as mock_client_cls,
        ):
            mock_client_cls.return_value.__aenter__ = AsyncMock(
                return_value=MagicMock()
            )
            mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)
            # Use internal _sync_all directly to avoid httpx context manager complexity
            with patch.object(scheduler, "_sync_all", AsyncMock()):
                rc = await scheduler.run_once()
        assert rc == 0

    @pytest.mark.asyncio
    async def test_run_once_api_error(self, scheduler):
        with patch.object(
            scheduler, "_sync_all", AsyncMock(side_effect=Exception("conn refused"))
        ):
            rc = await scheduler.run_once()
        assert rc == 1


class TestSchedulerCommands:
    @pytest.mark.asyncio
    async def test_execute_no_command(self, config):
        args = MagicMock()
        args.scheduler_command = None
        rc = await SchedulerCommands.execute(args, config)
        assert rc == 1

    @pytest.mark.asyncio
    async def test_execute_missing_org(self, config):
        config.get_current_organization.return_value = None
        config._config = {}
        args = MagicMock()
        args.scheduler_command = "start"
        args.api_url = None
        args.org_id = None
        rc = await SchedulerCommands.execute(args, config)
        assert rc == 1

    @pytest.mark.asyncio
    async def test_execute_run_once(self, config):
        args = MagicMock()
        args.scheduler_command = "start"
        args.api_url = "http://localhost:8002"
        args.org_id = "org-abc"
        args.interval = 30
        args.run_once = True

        with patch.object(_BoardSyncScheduler, "run_once", AsyncMock(return_value=0)):
            rc = await SchedulerCommands.execute(args, config)
        assert rc == 0
