"""exec(timeout=N) is a total deadline on the streaming path too.

The executor sends an SSE keepalive every 10 s, so the per-read httpx timeout
alone never fires while a silent command runs: the budget must be enforced on
top of it, and the stream closed so the executor stops the command.
"""

import asyncio
import inspect
import time
import unittest
from unittest.mock import patch

import httpx

from koyeb.sandbox.errors import SandboxTimeoutError
from koyeb.sandbox.exec import AsyncSandboxExecutor, SandboxExecutor
from koyeb.sandbox.executor_client import (
    AsyncSandboxClient,
    ConnectionInfo,
    SandboxClient,
)

_CONN = ConnectionInfo(public_url="https://sb.example", routing_key=None, secret="s")
_KEEPALIVE = b":keepalive\n\n"
_DONE = (
    b'data: {"stream": "stdout", "data": "hi"}\n\ndata: {"code": 0, "error": false}\n\n'
)


class _SyncStream(httpx.SyncByteStream):
    """Sends a keepalive every `interval` seconds, `count` times, then ends."""

    def __init__(self, interval, count, tail=b""):
        self.interval, self.count, self.tail = interval, count, tail
        self.closed = False

    def __iter__(self):
        for _ in range(self.count):
            yield _KEEPALIVE
            time.sleep(self.interval)
        yield self.tail

    def close(self):
        self.closed = True


class _AsyncStream(httpx.AsyncByteStream):
    """Async twin of _SyncStream."""

    def __init__(self, interval, count, tail=b""):
        self.interval, self.count, self.tail = interval, count, tail
        self.closed = False

    async def __aiter__(self):
        for _ in range(self.count):
            yield _KEEPALIVE
            await asyncio.sleep(self.interval)
        yield self.tail

    async def aclose(self):
        self.closed = True


def _sync_client(stream):
    client = SandboxClient(_CONN)
    client._client = httpx.Client(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(200, stream=stream)
        )
    )
    return client


def _async_client(stream):
    client = AsyncSandboxClient(_CONN)
    client._client = httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(200, stream=stream)
        )
    )
    return client


async def _collect(agen):
    return [event async for event in agen]


class TestSyncStreamingDeadline(unittest.TestCase):
    def test_keepalives_do_not_extend_timeout(self):
        stream = _SyncStream(interval=0.05, count=200)
        client = _sync_client(stream)
        start = time.monotonic()
        with self.assertRaises(SandboxTimeoutError):
            list(client.run_streaming("sleep 60", timeout=0.3))
        self.assertLess(time.monotonic() - start, 1.0)
        self.assertTrue(stream.closed)

    def test_without_timeout_stream_runs_to_the_end(self):
        client = _sync_client(_SyncStream(interval=0.05, count=4, tail=_DONE))
        events = list(client.run_streaming("echo hi"))
        self.assertEqual(events[-1], {"code": 0, "error": False})

    def test_exec_timeout_raises_while_only_keepalives_arrive(self):
        stream = _SyncStream(interval=0.05, count=200)
        executor = SandboxExecutor(None)
        with patch.object(
            SandboxExecutor, "_get_client", return_value=_sync_client(stream)
        ):
            start = time.monotonic()
            with self.assertRaises(SandboxTimeoutError):
                executor("sleep 60", timeout=1)
        self.assertLess(time.monotonic() - start, 2.0)
        self.assertTrue(stream.closed)

    def test_exec_within_timeout_returns_result(self):
        stream = _SyncStream(interval=0.05, count=4, tail=_DONE)
        executor = SandboxExecutor(None)
        with patch.object(
            SandboxExecutor, "_get_client", return_value=_sync_client(stream)
        ):
            result = executor("echo hi", timeout=1)
        self.assertEqual((result.stdout, result.exit_code), ("hi\n", 0))


class TestAsyncStreamingDeadline(unittest.TestCase):
    def test_keepalives_do_not_extend_timeout(self):
        stream = _AsyncStream(interval=0.05, count=200)
        client = _async_client(stream)
        start = time.monotonic()
        with self.assertRaises(SandboxTimeoutError):
            asyncio.run(_collect(client.run_streaming("sleep 60", timeout=0.3)))
        self.assertLess(time.monotonic() - start, 1.0)
        self.assertTrue(stream.closed)

    def test_timeout_fires_during_silence(self):
        # Async enforcement does not wait for the next line: one keepalive, then
        # a 10 s silence, still times out at the deadline.
        stream = _AsyncStream(interval=10, count=1)
        client = _async_client(stream)
        start = time.monotonic()
        with self.assertRaises(SandboxTimeoutError):
            asyncio.run(_collect(client.run_streaming("sleep 60", timeout=0.3)))
        self.assertLess(time.monotonic() - start, 1.0)
        self.assertTrue(stream.closed)

    def test_without_timeout_stream_runs_to_the_end(self):
        client = _async_client(_AsyncStream(interval=0.05, count=4, tail=_DONE))
        events = asyncio.run(_collect(client.run_streaming("echo hi")))
        self.assertEqual(events[-1], {"code": 0, "error": False})

    def test_exec_timeout_raises_while_only_keepalives_arrive(self):
        stream = _AsyncStream(interval=0.05, count=200)
        executor = AsyncSandboxExecutor(None)

        async def run():
            return await executor("sleep 60", timeout=1)

        with patch.object(
            AsyncSandboxExecutor,
            "_get_async_client",
            return_value=_async_client(stream),
        ):
            start = time.monotonic()
            with self.assertRaises(SandboxTimeoutError):
                asyncio.run(run())
        self.assertLess(time.monotonic() - start, 2.0)
        self.assertTrue(stream.closed)


class TestConnectTimeout(unittest.TestCase):
    def _client(self, handler):
        client = SandboxClient(_CONN)
        client._client = httpx.Client(transport=httpx.MockTransport(handler))
        return client

    def _timeouts(self, **kwargs):
        seen = {}

        def handler(request):
            seen.update(request.extensions["timeout"])
            return httpx.Response(200, content=_DONE)

        list(self._client(handler).run_streaming("echo hi", **kwargs))
        return seen

    def test_connect_defaults_to_ten_seconds(self):
        seen = self._timeouts(timeout=300)
        self.assertEqual((seen["connect"], seen["read"]), (10, 300))

    def test_connect_is_capped_by_timeout(self):
        self.assertEqual(self._timeouts(timeout=3)["connect"], 3)

    def test_connect_timeout_raises_sandbox_timeout(self):
        def handler(request):
            raise httpx.ConnectTimeout("timed out", request=request)

        client = self._client(handler)
        with self.assertRaisesRegex(SandboxTimeoutError, "Connection timed out"):
            list(client.run_streaming("echo hi", timeout=60, connect_timeout=2))


class TestNoTimeout(unittest.TestCase):
    """exec(timeout=None) sets no deadline, streamed or not."""

    def test_sync_streaming_runs_past_any_deadline(self):
        stream = _SyncStream(interval=0.05, count=4, tail=_DONE)
        executor = SandboxExecutor(None)
        with patch.object(
            SandboxExecutor, "_get_client", return_value=_sync_client(stream)
        ):
            result = executor("echo hi", timeout=None)
        self.assertEqual((result.stdout, result.exit_code), ("hi\n", 0))

    def test_async_streaming_runs_past_any_deadline(self):
        stream = _AsyncStream(interval=0.05, count=4, tail=_DONE)
        executor = AsyncSandboxExecutor(None)
        with patch.object(
            AsyncSandboxExecutor,
            "_get_async_client",
            return_value=_async_client(stream),
        ):
            result = asyncio.run(executor("echo hi", timeout=None))
        self.assertEqual((result.stdout, result.exit_code), ("hi\n", 0))

    def test_run_has_no_request_timeout(self):
        # run() alone would fall back to the client's 30 s default.
        for timeout, expected in ((None, None), (120, 120)):
            seen = {}

            def handler(request):
                seen.update(request.extensions["timeout"])
                return httpx.Response(200, json={"stdout": "hi\n", "code": 0})

            client = SandboxClient(_CONN)
            client._client = httpx.Client(transport=httpx.MockTransport(handler))
            with patch.object(SandboxExecutor, "_get_client", return_value=client):
                SandboxExecutor(None)("echo hi", timeout=timeout, stream=False)
            self.assertEqual(seen["read"], expected, timeout)

    def test_async_run_has_no_request_timeout(self):
        seen = {}

        def handler(request):
            seen.update(request.extensions["timeout"])
            return httpx.Response(200, json={"stdout": "hi\n", "code": 0})

        client = AsyncSandboxClient(_CONN)
        client._client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        executor = AsyncSandboxExecutor(None)
        with patch.object(
            AsyncSandboxExecutor, "_get_async_client", return_value=client
        ):
            asyncio.run(executor("echo hi", timeout=None, stream=False))
        self.assertIsNone(seen["read"])


class TestTimeoutMessage(unittest.TestCase):
    """The deadline error says how to give the command more time."""

    _HINT = r"Command timed out after 1s \(pass a larger timeout, or timeout=None"

    def test_sync_streaming(self):
        stream = _SyncStream(interval=0.05, count=200)
        with patch.object(
            SandboxExecutor, "_get_client", return_value=_sync_client(stream)
        ):
            with self.assertRaisesRegex(SandboxTimeoutError, self._HINT):
                SandboxExecutor(None)("sleep 60", timeout=1)

    def test_async_streaming(self):
        stream = _AsyncStream(interval=10, count=1)
        with patch.object(
            AsyncSandboxExecutor,
            "_get_async_client",
            return_value=_async_client(stream),
        ):
            with self.assertRaisesRegex(SandboxTimeoutError, self._HINT):
                asyncio.run(AsyncSandboxExecutor(None)("sleep 60", timeout=1))

    def test_sync_run(self):
        def handler(request):
            raise httpx.ReadTimeout("timed out", request=request)

        client = SandboxClient(_CONN)
        client._client = httpx.Client(transport=httpx.MockTransport(handler))
        with patch.object(SandboxExecutor, "_get_client", return_value=client):
            with self.assertRaisesRegex(SandboxTimeoutError, self._HINT):
                SandboxExecutor(None)("sleep 60", timeout=1, stream=False)

    def test_async_run(self):
        def handler(request):
            raise httpx.ReadTimeout("timed out", request=request)

        client = AsyncSandboxClient(_CONN)
        client._client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        with patch.object(
            AsyncSandboxExecutor, "_get_async_client", return_value=client
        ):
            with self.assertRaisesRegex(SandboxTimeoutError, self._HINT):
                asyncio.run(
                    AsyncSandboxExecutor(None)("sleep 60", timeout=1, stream=False)
                )

    def test_connect_timeout_keeps_its_own_message(self):
        def handler(request):
            raise httpx.ConnectTimeout("timed out", request=request)

        client = SandboxClient(_CONN)
        client._client = httpx.Client(transport=httpx.MockTransport(handler))
        with patch.object(SandboxExecutor, "_get_client", return_value=client):
            with self.assertRaisesRegex(SandboxTimeoutError, "Connection timed out"):
                SandboxExecutor(None)("echo hi", timeout=60)


class TestDefaultTimeout(unittest.TestCase):
    def test_default_timeout_is_five_minutes(self):
        # Now that the budget covers the whole command, the default leaves
        # room for slow commands (package installs, builds, test suites).
        for executor in (SandboxExecutor, AsyncSandboxExecutor):
            default = inspect.signature(executor.__call__).parameters["timeout"].default
            self.assertEqual(default, 300, executor.__name__)


if __name__ == "__main__":
    unittest.main()
