from __future__ import annotations

import asyncio
import json
import os
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest

from superdoc import AsyncSuperDocClient, CollaborationAuth, SuperDocClient, SuperDocError

from test_transport import _cleanup_wrapper, _mock_cli_bin


TOKEN: CollaborationAuth = {
    'type': 'token',
    'token': 'python-client-auth-sentinel-b3982e',
}
SECOND_TOKEN: CollaborationAuth = {
    'type': 'token',
    'token': 'python-client-auth-second-sentinel-0fc86e',
}
AUTH_REJECTED = {
    'error': {
        'code': -32000,
        'message': 'authentication rejected',
        'data': {'cliCode': 'COLLABORATION_AUTH_FAILED', 'message': 'authentication rejected'},
    },
}


class _RecordingHost:
    def __init__(self, responses: list) -> None:
        log = tempfile.NamedTemporaryFile(prefix='mock_host_requests_', suffix='.jsonl', delete=False)
        log.close()
        self.log = log.name
        self.release_file = f'{self.log}.release'
        held = [
            {**response, 'release_file': self.release_file} if response.pop('held', False) else response
            for response in responses
        ]
        self.cli = _mock_cli_bin({'handshake': 'ok', 'request_log': self.log, 'responses': held})

    def requests(self) -> list:
        with open(self.log, encoding='utf-8') as log:
            return [json.loads(line) for line in log if line.strip()]

    def wait_for_requests(self, count: int) -> None:
        deadline = time.monotonic() + 5
        while len(self.requests()) < count:
            assert time.monotonic() < deadline
            time.sleep(0.01)

    def release(self) -> None:
        with open(self.release_file, 'w', encoding='utf-8'):
            pass

    def close(self) -> None:
        _cleanup_wrapper(self.cli)
        for path in (self.log, self.release_file):
            if os.path.exists(path):
                os.unlink(path)


@pytest.fixture
def host_with():
    hosts: list[_RecordingHost] = []

    def start(*responses: dict) -> _RecordingHost:
        hosts.append(_RecordingHost(list(responses)))
        return hosts[-1]

    yield start
    for host in hosts:
        host.close()


def _open_request(doc: str, auth: CollaborationAuth, session_id: str | None = None) -> dict:
    session = [] if session_id is None else ['--session', session_id]
    return {
        'method': 'cli.invoke',
        'params': {
            'argv': ['open', doc, *session, '--output', 'json'],
            'stdinBase64': '',
            'collaborationAuth': auth,
        },
    }


def test_sync_client_forwards_auth_only_on_open(host_with) -> None:
    host = host_with({'data': {'contextId': 'sync-session'}})
    client = SuperDocClient(env={'SUPERDOC_CLI_BIN': host.cli})
    try:
        document = client.open({'doc': 'fixture.docx'}, collaboration_auth=TOKEN)
    finally:
        client.dispose()

    assert document.session_id == 'sync-session'
    assert host.requests() == [_open_request('fixture.docx', TOKEN)]


def test_sync_client_reserves_an_explicit_session_during_open(host_with) -> None:
    host = host_with({'held': True, 'data': {'contextId': 'shared-sync-session'}})
    client = SuperDocClient(env={'SUPERDOC_CLI_BIN': host.cli})
    params = {'doc': 'fixture.docx', 'sessionId': 'shared-sync-session'}

    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            first_open = executor.submit(client.open, params, collaboration_auth=TOKEN)
            host.wait_for_requests(1)
            try:
                with pytest.raises(SuperDocError) as error:
                    client.open(params, collaboration_auth=SECOND_TOKEN)
                assert not first_open.done()
            finally:
                host.release()
            document = first_open.result(timeout=5)
    finally:
        client.dispose()

    assert error.value.code == 'SESSION_ALREADY_OPEN'
    assert error.value.details == {'sessionId': 'shared-sync-session'}
    assert document.session_id == 'shared-sync-session'
    assert host.requests() == [_open_request('fixture.docx', TOKEN, 'shared-sync-session')]


def test_sync_client_releases_an_explicit_session_when_open_fails(host_with) -> None:
    host = host_with(AUTH_REJECTED, {'data': {'contextId': 'sync-retry-session'}})
    client = SuperDocClient(env={'SUPERDOC_CLI_BIN': host.cli})
    params = {'doc': 'fixture.docx', 'sessionId': 'sync-retry-session'}

    try:
        with pytest.raises(SuperDocError, match='authentication rejected'):
            client.open(params, collaboration_auth=TOKEN)
        document = client.open(params, collaboration_auth=SECOND_TOKEN)
    finally:
        client.dispose()

    assert document.session_id == 'sync-retry-session'
    assert host.requests() == [
        _open_request('fixture.docx', TOKEN, 'sync-retry-session'),
        _open_request('fixture.docx', SECOND_TOKEN, 'sync-retry-session'),
    ]


@pytest.mark.asyncio
async def test_async_client_forwards_auth_only_on_open(host_with) -> None:
    host = host_with({'data': {'contextId': 'async-session'}})
    client = AsyncSuperDocClient(env={'SUPERDOC_CLI_BIN': host.cli})
    try:
        document = await client.open({'doc': 'fixture.docx'}, collaboration_auth=TOKEN)
    finally:
        await client.dispose()

    assert document.session_id == 'async-session'
    assert host.requests() == [_open_request('fixture.docx', TOKEN)]


@pytest.mark.asyncio
async def test_async_client_reserves_an_explicit_session_during_open(host_with) -> None:
    host = host_with({'held': True, 'data': {'contextId': 'shared-async-session'}})
    client = AsyncSuperDocClient(env={'SUPERDOC_CLI_BIN': host.cli})
    params = {'doc': 'fixture.docx', 'sessionId': 'shared-async-session'}

    try:
        first_open = asyncio.create_task(client.open(params, collaboration_auth=TOKEN))
        await asyncio.to_thread(host.wait_for_requests, 1)
        try:
            with pytest.raises(SuperDocError) as error:
                await client.open(params, collaboration_auth=SECOND_TOKEN)
            assert not first_open.done()
        finally:
            host.release()
        document = await first_open
    finally:
        await client.dispose()

    assert error.value.code == 'SESSION_ALREADY_OPEN'
    assert error.value.details == {'sessionId': 'shared-async-session'}
    assert document.session_id == 'shared-async-session'
    assert host.requests() == [_open_request('fixture.docx', TOKEN, 'shared-async-session')]


@pytest.mark.asyncio
async def test_async_client_releases_an_explicit_session_when_open_fails(host_with) -> None:
    host = host_with(AUTH_REJECTED, {'data': {'contextId': 'async-retry-session'}})
    client = AsyncSuperDocClient(env={'SUPERDOC_CLI_BIN': host.cli})
    params = {'doc': 'fixture.docx', 'sessionId': 'async-retry-session'}

    try:
        with pytest.raises(SuperDocError, match='authentication rejected'):
            await client.open(params, collaboration_auth=TOKEN)
        document = await client.open(params, collaboration_auth=SECOND_TOKEN)
    finally:
        await client.dispose()

    assert document.session_id == 'async-retry-session'
    assert host.requests() == [
        _open_request('fixture.docx', TOKEN, 'async-retry-session'),
        _open_request('fixture.docx', SECOND_TOKEN, 'async-retry-session'),
    ]
