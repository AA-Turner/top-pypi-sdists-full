from __future__ import annotations

import asyncio
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest

from superdoc import AsyncSuperDocClient, CollaborationAuth, SuperDocClient, SuperDocError


TOKEN: CollaborationAuth = {
    'type': 'token',
    'token': 'python-client-auth-sentinel-b3982e',
}
SECOND_TOKEN: CollaborationAuth = {
    'type': 'token',
    'token': 'python-client-auth-second-sentinel-0fc86e',
}


def test_sync_client_forwards_auth_only_on_open() -> None:
    client = SuperDocClient(document_host_path='/unused')
    calls: list[tuple[str, dict, dict]] = []

    def invoke(operation_id: str, params: dict, **options: object) -> dict:
        calls.append((operation_id, params, options))
        return {'contextId': 'sync-session'}

    client._runtime.invoke = invoke  # type: ignore[method-assign]
    document = client.open({'doc': 'fixture.docx'}, collaboration_auth=TOKEN)

    assert document.session_id == 'sync-session'
    assert calls == [(
        'doc.open',
        {'doc': 'fixture.docx'},
        {'timeout_ms': None, 'stdin_bytes': None, 'collaboration_auth': TOKEN},
    )]


def test_sync_client_reserves_an_explicit_session_during_open() -> None:
    client = SuperDocClient(document_host_path='/unused')
    first_open_started = threading.Event()
    release_first_open = threading.Event()
    calls: list[CollaborationAuth] = []
    calls_lock = threading.Lock()

    def invoke(_operation_id: str, _params: dict, **options: object) -> dict:
        with calls_lock:
            calls.append(options['collaboration_auth'])  # type: ignore[arg-type]
            call_number = len(calls)
        if call_number == 1:
            first_open_started.set()
            assert release_first_open.wait(timeout=5)
        return {'contextId': 'shared-sync-session'}

    client._runtime.invoke = invoke  # type: ignore[method-assign]
    params = {'doc': 'fixture.docx', 'sessionId': 'shared-sync-session'}

    with ThreadPoolExecutor(max_workers=2) as executor:
        first_open = executor.submit(client.open, params, collaboration_auth=TOKEN)
        assert first_open_started.wait(timeout=5)
        second_open = executor.submit(client.open, params, collaboration_auth=SECOND_TOKEN)
        try:
            with pytest.raises(SuperDocError) as error:
                second_open.result(timeout=5)
        finally:
            release_first_open.set()
        document = first_open.result(timeout=5)

    assert error.value.code == 'SESSION_ALREADY_OPEN'
    assert error.value.details == {'sessionId': 'shared-sync-session'}
    assert document.session_id == 'shared-sync-session'
    assert calls == [TOKEN]


def test_sync_client_releases_an_explicit_session_when_open_fails() -> None:
    client = SuperDocClient(document_host_path='/unused')
    attempts = 0

    def invoke(_operation_id: str, _params: dict, **_options: object) -> dict:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise SuperDocError('authentication rejected', code='COLLABORATION_AUTH_FAILED')
        return {'contextId': 'sync-retry-session'}

    client._runtime.invoke = invoke  # type: ignore[method-assign]
    params = {'doc': 'fixture.docx', 'sessionId': 'sync-retry-session'}

    with pytest.raises(SuperDocError, match='authentication rejected'):
        client.open(params, collaboration_auth=TOKEN)
    document = client.open(params, collaboration_auth=SECOND_TOKEN)

    assert document.session_id == 'sync-retry-session'
    assert attempts == 2


@pytest.mark.asyncio
async def test_async_client_forwards_auth_only_on_open() -> None:
    client = AsyncSuperDocClient(document_host_path='/unused')
    calls: list[tuple[str, dict, dict]] = []

    async def invoke(operation_id: str, params: dict, **options: object) -> dict:
        calls.append((operation_id, params, options))
        return {'contextId': 'async-session'}

    client._runtime.invoke = invoke  # type: ignore[method-assign]
    document = await client.open({'doc': 'fixture.docx'}, collaboration_auth=TOKEN)

    assert document.session_id == 'async-session'
    assert calls == [(
        'doc.open',
        {'doc': 'fixture.docx'},
        {'timeout_ms': None, 'stdin_bytes': None, 'collaboration_auth': TOKEN},
    )]


@pytest.mark.asyncio
async def test_async_client_reserves_an_explicit_session_during_open() -> None:
    client = AsyncSuperDocClient(document_host_path='/unused')
    first_open_started = asyncio.Event()
    release_first_open = asyncio.Event()
    calls: list[CollaborationAuth] = []

    async def invoke(_operation_id: str, _params: dict, **options: object) -> dict:
        calls.append(options['collaboration_auth'])  # type: ignore[arg-type]
        if len(calls) == 1:
            first_open_started.set()
            await release_first_open.wait()
        return {'contextId': 'shared-async-session'}

    client._runtime.invoke = invoke  # type: ignore[method-assign]
    params = {'doc': 'fixture.docx', 'sessionId': 'shared-async-session'}
    first_open = asyncio.create_task(client.open(params, collaboration_auth=TOKEN))
    await asyncio.wait_for(first_open_started.wait(), timeout=5)
    second_open = asyncio.create_task(client.open(params, collaboration_auth=SECOND_TOKEN))
    await asyncio.sleep(0)
    release_first_open.set()

    first_result, second_result = await asyncio.gather(first_open, second_open, return_exceptions=True)

    assert first_result.session_id == 'shared-async-session'  # type: ignore[union-attr]
    assert isinstance(second_result, SuperDocError)
    assert second_result.code == 'SESSION_ALREADY_OPEN'
    assert second_result.details == {'sessionId': 'shared-async-session'}
    assert calls == [TOKEN]


@pytest.mark.asyncio
async def test_async_client_releases_an_explicit_session_when_open_fails() -> None:
    client = AsyncSuperDocClient(document_host_path='/unused')
    attempts = 0

    async def invoke(_operation_id: str, _params: dict, **_options: object) -> dict:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise SuperDocError('authentication rejected', code='COLLABORATION_AUTH_FAILED')
        return {'contextId': 'async-retry-session'}

    client._runtime.invoke = invoke  # type: ignore[method-assign]
    params = {'doc': 'fixture.docx', 'sessionId': 'async-retry-session'}

    with pytest.raises(SuperDocError, match='authentication rejected'):
        await client.open(params, collaboration_auth=TOKEN)
    document = await client.open(params, collaboration_auth=SECOND_TOKEN)

    assert document.session_id == 'async-retry-session'
    assert attempts == 2
