import asyncio
import gc
import threading

import httpx

from mistralai.workflows.core.worker_client import borrow_worker_client, get_worker_client, share_worker_client
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient


def _new_client() -> PrivateWorkerClient:
    return get_worker_client(base_url="http://localhost", api_key="test-key")


def _http_client(client: PrivateWorkerClient) -> httpx.AsyncClient:
    async_client = client.sdk_configuration.async_client
    assert isinstance(async_client, httpx.AsyncClient)
    return async_client


class TestBorrowWorkerClient:
    async def test_borrows_the_shared_client_without_closing_it(self) -> None:
        shared = _new_client()
        fallback_calls = 0

        def fallback() -> PrivateWorkerClient:
            nonlocal fallback_calls
            fallback_calls += 1
            return _new_client()

        async with shared, share_worker_client(shared):
            for _ in range(3):
                async with borrow_worker_client(fallback) as client:
                    assert client is shared
            assert not _http_client(shared).is_closed

        assert fallback_calls == 0

    async def test_closes_the_fallback_client_outside_a_worker(self) -> None:
        fallback_client = _new_client()
        http_client = _http_client(fallback_client)

        async with borrow_worker_client(lambda: fallback_client) as client:
            assert client is fallback_client
            assert not http_client.is_closed

        assert http_client.is_closed

    async def test_stops_sharing_when_the_worker_exits(self) -> None:
        shared = _new_client()
        async with shared, share_worker_client(shared):
            pass

        fallback_client = _new_client()
        async with borrow_worker_client(lambda: fallback_client) as client:
            assert client is fallback_client

    async def test_does_not_share_across_event_loops(self) -> None:
        shared = _new_client()
        borrowed: list[PrivateWorkerClient] = []

        async def borrow_in_other_loop() -> None:
            async with borrow_worker_client(_new_client) as client:
                borrowed.append(client)

        async with shared, share_worker_client(shared):
            thread = threading.Thread(target=asyncio.run, args=(borrow_in_other_loop(),))
            thread.start()
            await asyncio.to_thread(thread.join)

        assert len(borrowed) == 1
        assert borrowed[0] is not shared


class TestGetWorkerClient:
    async def test_dropping_the_client_closes_its_http_client(self) -> None:
        client = _new_client()
        http_client = _http_client(client)

        del client
        gc.collect()
        # The finalizer schedules aclose() on the loop; give it a few iterations to run.
        for _ in range(10):
            if http_client.is_closed:
                break
            await asyncio.sleep(0)

        assert http_client.is_closed
