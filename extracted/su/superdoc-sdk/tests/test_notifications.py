from __future__ import annotations

import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest

import superdoc.transport as transport_module
from superdoc.errors import HOST_DISCONNECTED, NOTIFICATIONS_LAGGED, SuperDocError
from superdoc.notifications import NotificationHub
from superdoc.protocol import JsonRpcNotification, parse_jsonrpc_line
from superdoc.transport import AsyncHostTransport, SyncHostTransport

from test_transport import _TEST_OP, _TEST_OPEN_OP, _cleanup_wrapper, _mock_cli_bin

CLAIM_SENTINEL = 'python-identity-claim-sentinel-58aa31'


def _change(seq: int) -> dict:
    return {
        'jsonrpc': '2.0',
        'method': 'event.change',
        'params': {'sessionId': 'room', 'records': [{'id': f'change-{seq}', 'seq': seq}]},
    }


def _message(frame: dict) -> JsonRpcNotification:
    parsed = parse_jsonrpc_line(json.dumps(frame))
    assert isinstance(parsed, JsonRpcNotification)
    return parsed


class TestNotificationHub:
    def test_sync_subscribers_receive_identical_frames_in_order(self):
        hub = NotificationHub()
        first = hub.subscribe_sync()
        second = hub.subscribe_sync()
        hub.publish(_message(_change(1)))
        hub.publish(_message(_change(2)))
        for subscription in (first, second):
            assert subscription.recv(timeout=1) == _change(1)
            assert subscription.recv(timeout=1) == _change(2)
            assert subscription.recv(timeout=0.01) is None

    def test_sync_lag_is_explicit_and_reading_continues(self):
        hub = NotificationHub()
        subscription = hub.subscribe_sync(capacity=2)
        for seq in range(1, 6):
            hub.publish(_message(_change(seq)))
        with pytest.raises(SuperDocError) as lagged:
            subscription.recv(timeout=1)
        assert lagged.value.code == NOTIFICATIONS_LAGGED
        assert lagged.value.details['skipped'] == 3
        assert 'changes.list' in lagged.value.details['resync']
        assert [subscription.recv(timeout=1), subscription.recv(timeout=1)] == [_change(4), _change(5)]

    def test_sync_iteration_stops_after_close(self):
        hub = NotificationHub()
        subscription = hub.subscribe_sync()
        hub.publish(_message(_change(1)))
        hub.close()
        assert list(subscription) == []
        hub.publish(_message(_change(2)))
        assert subscription.closed

    def test_rejects_invalid_capacity(self):
        with pytest.raises(SuperDocError) as error:
            NotificationHub().subscribe_sync(capacity=0)
        assert error.value.code == 'INVALID_ARGUMENT'

    @pytest.mark.asyncio
    async def test_async_lag_disconnect_and_close(self):
        hub = NotificationHub()
        subscription = hub.subscribe_async(capacity=1)
        pending = asyncio.ensure_future(subscription.recv())
        await asyncio.sleep(0)
        hub.publish(_message(_change(1)))
        assert await asyncio.wait_for(pending, 1) == _change(1)
        hub.publish(_message(_change(2)))
        hub.publish(_message(_change(3)))
        with pytest.raises(SuperDocError) as lagged:
            await subscription.recv()
        assert lagged.value.code == NOTIFICATIONS_LAGGED
        assert await subscription.recv() == _change(3)
        hub.disconnect(SuperDocError('Host process disconnected.', code=HOST_DISCONNECTED))
        with pytest.raises(SuperDocError) as disconnected:
            await subscription.recv(timeout=1)
        assert disconnected.value.code == HOST_DISCONNECTED
        assert await subscription.recv(timeout=0.01) is None
        hub.close()
        assert [frame async for frame in subscription] == []


class TestSyncTransportNotifications:
    def test_interleaved_and_idle_notifications_reach_subscribers(self):
        cli = _mock_cli_bin({
            'handshake': 'ok',
            'responses': [{
                'data': {'ok': True},
                'notifications': [_change(1), _change(2)],
                'after': {'delay_ms': 100, 'notifications': [_change(3)]},
            }],
        })
        transport = SyncHostTransport(cli, startup_timeout_ms=5_000)
        subscription = transport.subscribe()
        try:
            assert transport.invoke(_TEST_OP, {'query': 'x'}) == {'ok': True}
            assert subscription.recv(timeout=5) == _change(1)
            assert subscription.recv(timeout=5) == _change(2)
            assert subscription.recv(timeout=5) == _change(3)
        finally:
            transport.dispose()
            _cleanup_wrapper(cli)
        assert list(subscription) == []

    def test_lag_is_reported_once(self):
        cli = _mock_cli_bin({
            'handshake': 'ok',
            'responses': [{'data': None, 'notifications': [_change(seq) for seq in range(1, 11)]}],
        })
        transport = SyncHostTransport(cli, startup_timeout_ms=5_000)
        subscription = transport.subscribe(capacity=4)
        try:
            transport.invoke(_TEST_OP, {'query': 'x'})
            with pytest.raises(SuperDocError) as lagged:
                subscription.recv(timeout=5)
            assert lagged.value.code == NOTIFICATIONS_LAGGED
            assert subscription.recv(timeout=5) == _change(7)
        finally:
            transport.dispose()
            _cleanup_wrapper(cli)

    def test_idle_host_exit_is_reported(self):
        cli = _mock_cli_bin({
            'handshake': 'ok',
            'responses': [{'data': None, 'after': {'delay_ms': 50, 'notifications': [_change(1)], 'exit': 3}}],
        })
        transport = SyncHostTransport(cli, startup_timeout_ms=5_000)
        subscription = transport.subscribe()
        try:
            transport.invoke(_TEST_OP, {'query': 'x'})
            assert subscription.recv(timeout=5) == _change(1)
            with pytest.raises(SuperDocError) as disconnected:
                subscription.recv(timeout=5)
            assert disconnected.value.code == HOST_DISCONNECTED
        finally:
            transport.dispose()
            _cleanup_wrapper(cli)

    def test_requests_still_work_after_notifications_and_reconnect(self):
        cli = _mock_cli_bin({
            'handshake': 'ok',
            'responses': [
                {'data': 1, 'notifications': [_change(1)]},
                {'crash': True},
            ],
        })
        transport = SyncHostTransport(cli, startup_timeout_ms=5_000)
        subscription = transport.subscribe()
        try:
            assert transport.invoke(_TEST_OP, {'query': 'x'}) == 1
            with pytest.raises(SuperDocError) as crashed:
                transport.invoke(_TEST_OP, {'query': 'x'})
            assert crashed.value.code == HOST_DISCONNECTED
            assert subscription.recv(timeout=5) == _change(1)
            with pytest.raises(SuperDocError) as disconnected:
                subscription.recv(timeout=5)
            assert disconnected.value.code == HOST_DISCONNECTED
            assert subscription.recv(timeout=0.05) is None
            assert transport.invoke(_TEST_OP, {'query': 'x'}) == 1
        finally:
            transport.dispose()
            _cleanup_wrapper(cli)


class TestAsyncTransportNotifications:
    @pytest.mark.asyncio
    async def test_interleaved_and_idle_notifications_reach_subscribers(self):
        cli = _mock_cli_bin({
            'handshake': 'ok',
            'responses': [{
                'data': {'ok': True},
                'notifications': [_change(1)],
                'after': {'delay_ms': 100, 'notifications': [_change(2)]},
            }],
        })
        transport = AsyncHostTransport(cli, startup_timeout_ms=5_000)
        subscription = transport.subscribe()
        try:
            assert await transport.invoke(_TEST_OP, {'query': 'x'}) == {'ok': True}
            assert await subscription.recv(timeout=5) == _change(1)
            assert await subscription.recv(timeout=5) == _change(2)
        finally:
            await transport.dispose()
            _cleanup_wrapper(cli)
        assert [frame async for frame in subscription] == []

    @pytest.mark.asyncio
    async def test_lag_and_disconnect_are_explicit(self):
        cli = _mock_cli_bin({
            'handshake': 'ok',
            'responses': [{
                'data': None,
                'notifications': [_change(seq) for seq in range(1, 11)],
                'after': {'delay_ms': 50, 'exit': 3},
            }],
        })
        transport = AsyncHostTransport(cli, startup_timeout_ms=5_000)
        subscription = transport.subscribe(capacity=4)
        try:
            await transport.invoke(_TEST_OP, {'query': 'x'})
            with pytest.raises(SuperDocError) as lagged:
                await subscription.recv(timeout=5)
            assert lagged.value.code == NOTIFICATIONS_LAGGED
            assert [await subscription.recv(timeout=5) for _ in range(4)] == [_change(seq) for seq in range(7, 11)]
            with pytest.raises(SuperDocError) as disconnected:
                await subscription.recv(timeout=5)
            assert disconnected.value.code == HOST_DISCONNECTED
        finally:
            await transport.dispose()
            _cleanup_wrapper(cli)


class TestDisposeEndsSubscriptions:
    def test_sync_dispose_closes_subscriptions_when_shutdown_fails(self, monkeypatch):
        cli = _mock_cli_bin({'handshake': 'ok'})
        transport = SyncHostTransport(cli, startup_timeout_ms=5_000)
        subscription = transport.subscribe()
        original_cleanup = transport._cleanup

        def failing_cleanup() -> None:
            original_cleanup()
            raise RuntimeError('cleanup failed')

        try:
            transport.connect()
            monkeypatch.setattr(transport, '_cleanup', failing_cleanup)
            with pytest.raises(RuntimeError):
                transport.dispose()
            assert subscription.closed
            assert list(subscription) == []
        finally:
            _cleanup_wrapper(cli)

    @pytest.mark.asyncio
    async def test_async_dispose_ends_a_pending_subscription_when_shutdown_fails(self, monkeypatch):
        cli = _mock_cli_bin({'handshake': 'ok'})
        transport = AsyncHostTransport(cli, startup_timeout_ms=5_000)
        subscription = transport.subscribe()
        original_cleanup = transport._cleanup

        async def failing_cleanup(error):
            await original_cleanup(error)
            raise RuntimeError('cleanup failed')

        try:
            await transport.connect()
            pending = asyncio.ensure_future(subscription.__anext__())
            await asyncio.sleep(0)
            monkeypatch.setattr(transport, '_cleanup', failing_cleanup)
            with pytest.raises(RuntimeError):
                await transport.dispose()
            with pytest.raises(StopAsyncIteration):
                await asyncio.wait_for(pending, timeout=5)
        finally:
            _cleanup_wrapper(cli)


class TestIdentityClaim:
    def test_sync_sends_claim_in_sidecar_only(self, monkeypatch):
        monkeypatch.setattr(transport_module, 'IDENTITY_CLAIM_PER_OPEN_FEATURE', 'document.open.identityClaim')
        transport = SyncHostTransport('/unused')
        sent: list = []

        def send_request(method: str, params: dict, watchdog: int) -> dict:
            sent.append((method, params))
            return {'data': {}}

        monkeypatch.setattr(transport, '_ensure_connected', lambda: None)
        monkeypatch.setattr(transport, '_send_request', send_request)
        transport._host_features = {'cli.invoke', 'document.open.identityClaim'}
        transport.invoke(_TEST_OPEN_OP, {'doc': 'fixture.docx'}, identity_claim=CLAIM_SENTINEL)
        assert sent[0][1]['identityClaim'] == CLAIM_SENTINEL
        assert CLAIM_SENTINEL not in ' '.join(sent[0][1]['argv'])

    def test_sync_rejects_unsupported_hosts_and_other_operations(self, monkeypatch):
        monkeypatch.setattr(transport_module, 'IDENTITY_CLAIM_PER_OPEN_FEATURE', 'document.open.identityClaim')
        transport = SyncHostTransport('/unused')
        monkeypatch.setattr(transport, '_ensure_connected', lambda: None)
        transport._host_features = {'cli.invoke'}
        with pytest.raises(SuperDocError) as unsupported:
            transport.invoke(_TEST_OPEN_OP, {'doc': 'fixture.docx'}, identity_claim=CLAIM_SENTINEL)
        assert unsupported.value.code == 'CAPABILITY_UNSUPPORTED'
        with pytest.raises(SuperDocError) as wrong_operation:
            transport.invoke(_TEST_OP, {'query': 'x'}, identity_claim=CLAIM_SENTINEL)
        assert wrong_operation.value.code == 'INVALID_ARGUMENT'
        with pytest.raises(SuperDocError) as empty:
            transport.invoke(_TEST_OPEN_OP, {'doc': 'fixture.docx'}, identity_claim='')
        assert empty.value.code == 'INVALID_ARGUMENT'
        for error in (unsupported.value, wrong_operation.value, empty.value):
            assert CLAIM_SENTINEL not in str(error)

    @pytest.mark.asyncio
    async def test_async_sends_claim_to_a_capable_host(self, monkeypatch):
        monkeypatch.setattr(transport_module, 'IDENTITY_CLAIM_PER_OPEN_FEATURE', 'document.open.identityClaim')
        cli = _mock_cli_bin({'handshake': 'identity_claim', 'responses': [{'data': {'contextId': 'session-1'}}]})
        transport = AsyncHostTransport(cli, startup_timeout_ms=5_000)
        try:
            result = await transport.invoke(_TEST_OPEN_OP, {'doc': 'fixture.docx'}, identity_claim=CLAIM_SENTINEL)
            assert result == {'contextId': 'session-1'}
        finally:
            await transport.dispose()
            _cleanup_wrapper(cli)

    def test_clients_forward_claim_only_on_open(self, monkeypatch):
        from superdoc import SuperDocClient

        client = SuperDocClient(env={'SUPERDOC_CLI_BIN': '/missing/superdoc'})
        calls: list = []

        def invoke(operation_id: str, params: dict, **options: object) -> dict:
            calls.append((operation_id, options))
            return {'contextId': 'claim-session'}

        monkeypatch.setattr(client._runtime, 'invoke', invoke)
        client.open({'doc': 'fixture.docx'}, identity_claim=CLAIM_SENTINEL)
        assert calls == [(
            'doc.open',
            {'timeout_ms': None, 'stdin_bytes': None, 'collaboration_auth': None, 'identity_claim': CLAIM_SENTINEL},
        )]
