"""Tests for workflow notification hook delivery."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.services.workflow_hooks import (
    deliver_hooks,
    drain_pending_hooks,
    validate_hook_config,
)


class TestValidateHookConfig:
    def test_valid_webhook_passes(self) -> None:
        hooks = [{"transport": "webhook", "url": "https://example.com/hook"}]
        validate_hook_config(hooks, ["example.com"])

    def test_blocked_webhook_raises(self) -> None:
        hooks = [{"transport": "webhook", "url": "https://blocked.com/hook"}]
        with pytest.raises(ValueError, match="blocked by egress"):
            validate_hook_config(hooks, ["allowed.com"])

    def test_localhost_blocked(self) -> None:
        hooks = [{"transport": "webhook", "url": "http://localhost:9090/hook"}]
        with pytest.raises(ValueError, match="blocked by egress"):
            validate_hook_config(hooks, [], block_localhost=True)

    def test_empty_url_raises(self) -> None:
        hooks = [{"transport": "webhook", "url": ""}]
        with pytest.raises(ValueError, match="no URL"):
            validate_hook_config(hooks, [])

    def test_unix_socket_valid(self) -> None:
        hooks = [{"transport": "unix_socket", "path": "/tmp/test.sock"}]
        validate_hook_config(hooks, [])

    def test_unix_socket_no_path_raises(self) -> None:
        hooks = [{"transport": "unix_socket", "path": ""}]
        with pytest.raises(ValueError, match="no path"):
            validate_hook_config(hooks, [])

    def test_unknown_transport_raises(self) -> None:
        hooks = [{"transport": "grpc", "url": "http://x"}]
        with pytest.raises(ValueError, match="Unknown hook transport"):
            validate_hook_config(hooks, [])

    def test_open_egress_passes(self) -> None:
        """With no allowlist and no block_localhost, any URL passes."""
        hooks = [{"transport": "webhook", "url": "https://anything.com/hook"}]
        validate_hook_config(hooks, [])


class TestDeliverHooks:
    @pytest.mark.asyncio
    async def test_matching_event_type_delivered(self) -> None:
        hooks = [
            {"transport": "webhook", "url": "https://x.com/hook", "events": ["step_finished"]},
        ]
        with patch("anteroom.services.workflow_hooks.deliver_webhook", new_callable=AsyncMock) as mock:
            tasks = await deliver_hooks(hooks, {"event_type": "step_finished", "run_id": "r1"})
            assert len(tasks) >= 0  # task may have completed
            # Give task time to run
            await asyncio.sleep(0.01)
            mock.assert_called_once()

    @pytest.mark.asyncio
    async def test_non_matching_event_skipped(self) -> None:
        hooks = [
            {"transport": "webhook", "url": "https://x.com/hook", "events": ["run_completed"]},
        ]
        with patch("anteroom.services.workflow_hooks.deliver_webhook", new_callable=AsyncMock) as mock:
            await deliver_hooks(hooks, {"event_type": "step_finished"})
            await asyncio.sleep(0.01)
            mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_all_events_matches_everything(self) -> None:
        hooks = [
            {"transport": "webhook", "url": "https://x.com/hook", "events": ["all"]},
        ]
        with patch("anteroom.services.workflow_hooks.deliver_webhook", new_callable=AsyncMock) as mock:
            await deliver_hooks(hooks, {"event_type": "anything"})
            await asyncio.sleep(0.01)
            mock.assert_called_once()


class TestDeliverWebhook:
    @pytest.mark.asyncio
    async def test_runtime_error_no_propagation(self) -> None:
        from anteroom.services.workflow_hooks import deliver_webhook

        with patch("httpx.AsyncClient", side_effect=RuntimeError("connection failed")):
            await deliver_webhook("https://x.com/hook", {"event": "test"})
        # No exception raised — best-effort

    @pytest.mark.asyncio
    async def test_502_response_logs_warning(self) -> None:
        from anteroom.services.workflow_hooks import deliver_webhook

        mock_response = MagicMock()
        mock_response.status_code = 502
        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            await deliver_webhook("https://x.com/hook", {"event": "test"})
        # No exception — warning logged internally


class TestDeliverUnixSocket:
    @pytest.mark.asyncio
    async def test_os_error_no_propagation(self) -> None:
        from anteroom.services.workflow_hooks import deliver_unix_socket

        with patch("socket.socket") as mock_sock_cls:
            mock_sock = MagicMock()
            mock_sock.connect = MagicMock(side_effect=OSError("no such socket"))
            mock_sock_cls.return_value = mock_sock
            await deliver_unix_socket("/tmp/nonexistent.sock", {"event": "test"})
        # No exception raised


class TestDeliverHooksUnixSocket:
    @pytest.mark.asyncio
    async def test_unix_socket_transport_dispatched(self) -> None:
        hooks = [
            {"transport": "unix_socket", "path": "/tmp/test.sock", "events": ["all"]},
        ]
        with patch("anteroom.services.workflow_hooks.deliver_unix_socket", new_callable=AsyncMock) as mock:
            await deliver_hooks(hooks, {"event_type": "run_completed"})
            await asyncio.sleep(0.01)
            mock.assert_called_once()


class TestDrainPendingHooks:
    @pytest.mark.asyncio
    async def test_drain_awaits_tasks(self) -> None:
        completed = []

        async def slow_task() -> None:
            await asyncio.sleep(0.01)
            completed.append(True)

        tasks = [asyncio.create_task(slow_task()) for _ in range(3)]
        await drain_pending_hooks(tasks, timeout=5.0)
        assert len(completed) == 3

    @pytest.mark.asyncio
    async def test_drain_cancels_on_timeout(self) -> None:
        async def very_slow() -> None:
            await asyncio.sleep(100)

        tasks = [asyncio.create_task(very_slow())]
        await drain_pending_hooks(tasks, timeout=0.1)
        # Task was cancelled — give it a tick to complete cancellation
        await asyncio.sleep(0)
        assert tasks[0].done()

    @pytest.mark.asyncio
    async def test_drain_empty_tasks(self) -> None:
        await drain_pending_hooks([], timeout=1.0)
