"""Pins the raw-bytes /files transport on the executor clients.

The streamed routes (executor v0.0.24+) are a
raw-HTTP contract: query-parameter routes, real status codes with
``{"error": ...}`` bodies, and raw byte streams. These tests pin the client
side of that contract against httpx.MockTransport, the way
test_executor_retry.py pins the retry seam.
"""

import json
import unittest
from unittest.mock import patch

import httpx

from koyeb.sandbox.executor_client import (
    AsyncSandboxClient,
    ConnectionInfo,
    DEFAULT_HTTP_TIMEOUT,
    SandboxClient,
    _FILES_TIMEOUT,
)
from koyeb.sandbox.errors import (
    SandboxError,
    SandboxRequestError,
    SandboxServiceError,
    SandboxTimeoutError,
)

_CONN = ConnectionInfo(public_url="https://sb.example", routing_key=None, secret="s")


def _make_sync_client(handler):
    client = SandboxClient(_CONN)
    client._client = httpx.Client(transport=httpx.MockTransport(handler))
    return client


def _make_async_client(handler):
    client = AsyncSandboxClient(_CONN)
    client._client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return client


def _request_spy(client, seen):
    """Record the timeout kwarg the client's httpx request receives."""
    real = client._client.request

    def spy(method, url, **kwargs):
        seen["timeout"] = kwargs.get("timeout")
        return real(method, url, **kwargs)

    return patch.object(client._client, "request", side_effect=spy)


def _async_request_spy(client, seen):
    """Record the timeout kwarg the async client's httpx request receives."""
    real = client._client.request

    async def spy(method, url, **kwargs):
        seen["timeout"] = kwargs.get("timeout")
        return await real(method, url, **kwargs)

    return patch.object(client._client, "request", side_effect=spy)


def _stream_spy(client, seen):
    """Record the timeout kwarg the client's stream call receives.

    Works for both clients: httpx's stream() builds the context manager
    synchronously on the sync and the async client alike.
    """
    real = client._client.stream

    def spy(method, url, **kwargs):
        seen["timeout"] = kwargs.get("timeout")
        return real(method, url, **kwargs)

    return patch.object(client._client, "stream", side_effect=spy)


class TestFilesStat(unittest.TestCase):
    def test_sends_get_and_returns_entry(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            return httpx.Response(
                200,
                request=request,
                json={
                    "type": "file",
                    "size": 5,
                    "mode": "0644",
                    "mtime": "2026-10-27T10:00:00Z",
                },
            )

        entry = _make_sync_client(handler).files_stat("/tmp/a.txt")

        self.assertEqual(seen["method"], "GET")
        self.assertEqual(
            seen["url"], "https://sb.example/files/stat?path=%2Ftmp%2Fa.txt"
        )
        self.assertEqual(entry["type"], "file")
        self.assertEqual(entry["size"], 5)
        self.assertEqual(entry["mode"], "0644")

    def test_404_raises_request_error(self):
        def handler(request):
            return httpx.Response(
                404, request=request, json={"error": "file does not exist"}
            )

        with self.assertRaises(SandboxRequestError) as ctx:
            _make_sync_client(handler).files_stat("/tmp/missing.txt")

        self.assertEqual(ctx.exception.status_code, 404)

    def test_hash_param_requests_sha256(self):
        seen = {}

        def handler(request):
            seen["url"] = str(request.url)
            return httpx.Response(
                200,
                request=request,
                json={
                    "type": "file",
                    "size": 5,
                    "mode": "0644",
                    "mtime": "2026-10-27T10:00:00Z",
                    "sha256": "ab" * 32,
                },
            )

        entry = _make_sync_client(handler).files_stat("/tmp/a.txt", hash="sha256")

        self.assertEqual(
            seen["url"],
            "https://sb.example/files/stat?path=%2Ftmp%2Fa.txt&hash=sha256",
        )
        self.assertEqual(entry["sha256"], "ab" * 32)


class TestAsyncFilesStat(unittest.IsolatedAsyncioTestCase):
    async def test_sends_get_and_returns_entry(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            return httpx.Response(
                200,
                request=request,
                json={"type": "dir", "size": 0, "mode": "0755"},
            )

        entry = await _make_async_client(handler).files_stat("/tmp")

        self.assertEqual(seen["method"], "GET")
        self.assertEqual(seen["url"], "https://sb.example/files/stat?path=%2Ftmp")
        self.assertEqual(entry["type"], "dir")

    async def test_hash_param_requests_sha256(self):
        seen = {}

        def handler(request):
            seen["url"] = str(request.url)
            return httpx.Response(
                200,
                request=request,
                json={
                    "type": "file",
                    "size": 5,
                    "mode": "0644",
                    "mtime": "2026-10-27T10:00:00Z",
                    "sha256": "cd" * 32,
                },
            )

        entry = await _make_async_client(handler).files_stat(
            "/tmp/a.txt", hash="sha256"
        )

        self.assertTrue(seen["url"].endswith("&hash=sha256"), seen["url"])
        self.assertEqual(entry["sha256"], "cd" * 32)


class TestFilesPut(unittest.TestCase):
    def test_streams_body_and_returns_commit_reply(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            seen["content_type"] = request.headers.get("Content-Type")
            seen["sha_header"] = request.headers.get("X-Content-SHA256")
            seen["body"] = request.read()
            return httpx.Response(
                200, request=request, json={"size": 3, "sha256": "deadbeef"}
            )

        reply = _make_sync_client(handler).files_put(
            "/tmp/a.txt", b"xyz", mode="0600", parents=True, sha256="deadbeef"
        )

        self.assertEqual(seen["method"], "PUT")
        self.assertEqual(
            seen["url"],
            "https://sb.example/files?path=%2Ftmp%2Fa.txt&mode=0600&parents=1",
        )
        self.assertEqual(seen["content_type"], "application/octet-stream")
        self.assertEqual(seen["sha_header"], "deadbeef")
        self.assertEqual(seen["body"], b"xyz")
        self.assertEqual(reply, {"size": 3, "sha256": "deadbeef"})

    def test_accepts_iterable_content(self):
        seen = {}

        def handler(request):
            seen["body"] = request.read()
            return httpx.Response(
                200, request=request, json={"size": 6, "sha256": "sum"}
            )

        def chunks():
            yield b"ab"
            yield b"cdef"

        _make_sync_client(handler).files_put("/tmp/a.txt", chunks())

        self.assertEqual(seen["body"], b"abcdef")

    def test_mid_stream_failure_is_not_retried(self):
        calls = []

        def handler(request):
            calls.append(1)
            raise httpx.ReadError("reset mid-stream", request=request)

        with self.assertRaises(SandboxError):
            _make_sync_client(handler).files_put("/tmp/a.txt", b"xyz")

        # A streamed body cannot be replayed: only a connect-time failure
        # (the request never left) is retried.
        self.assertEqual(len(calls), 1)


class TestAsyncFilesPut(unittest.IsolatedAsyncioTestCase):
    async def test_streams_body_and_returns_commit_reply(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            seen["content_type"] = request.headers.get("Content-Type")
            seen["sha_header"] = request.headers.get("X-Content-SHA256")
            seen["body"] = request.read()
            return httpx.Response(
                200, request=request, json={"size": 3, "sha256": "deadbeef"}
            )

        reply = await _make_async_client(handler).files_put(
            "/tmp/a.txt", b"xyz", mode="0600", parents=True, sha256="deadbeef"
        )

        self.assertEqual(seen["method"], "PUT")
        self.assertEqual(
            seen["url"],
            "https://sb.example/files?path=%2Ftmp%2Fa.txt&mode=0600&parents=1",
        )
        self.assertEqual(seen["content_type"], "application/octet-stream")
        self.assertEqual(seen["sha_header"], "deadbeef")
        self.assertEqual(seen["body"], b"xyz")
        self.assertEqual(reply, {"size": 3, "sha256": "deadbeef"})

    async def test_accepts_iterable_content(self):
        seen = {}

        def handler(request):
            seen["body"] = request.read()
            return httpx.Response(
                200, request=request, json={"size": 6, "sha256": "sum"}
            )

        def chunks():
            yield b"ab"
            yield b"cdef"

        reply = await _make_async_client(handler).files_put("/tmp/a.txt", chunks())

        self.assertEqual(seen["body"], b"abcdef")
        self.assertEqual(reply, {"size": 6, "sha256": "sum"})

    async def test_accepts_file_object_content(self):
        import io

        seen = {}

        def handler(request):
            seen["body"] = request.read()
            return httpx.Response(
                200, request=request, json={"size": 3, "sha256": "sum"}
            )

        reply = await _make_async_client(handler).files_put(
            "/tmp/a.txt", io.BytesIO(b"xyz")
        )

        self.assertEqual(seen["body"], b"xyz")
        self.assertEqual(reply, {"size": 3, "sha256": "sum"})


class TestFilesRead(unittest.TestCase):
    def test_yields_chunks_from_get(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            return httpx.Response(200, request=request, content=b"abcdef")

        chunks = list(_make_sync_client(handler).files_read("/tmp/a.txt"))

        self.assertEqual(seen["method"], "GET")
        self.assertEqual(seen["url"], "https://sb.example/files?path=%2Ftmp%2Fa.txt")
        self.assertEqual(b"".join(chunks), b"abcdef")

    def test_404_raises_request_error(self):
        def handler(request):
            return httpx.Response(
                404, request=request, json={"error": "file does not exist"}
            )

        with self.assertRaises(SandboxRequestError) as ctx:
            list(_make_sync_client(handler).files_read("/tmp/missing.txt"))

        self.assertEqual(ctx.exception.status_code, 404)


class TestAsyncFilesRead(unittest.IsolatedAsyncioTestCase):
    async def test_yields_chunks_from_get(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            return httpx.Response(200, request=request, content=b"abcdef")

        chunks = []
        async for chunk in _make_async_client(handler).files_read("/tmp/a.txt"):
            chunks.append(chunk)

        self.assertEqual(seen["method"], "GET")
        self.assertEqual(seen["url"], "https://sb.example/files?path=%2Ftmp%2Fa.txt")
        self.assertEqual(b"".join(chunks), b"abcdef")


class TestHasFilesRoutes(unittest.TestCase):
    def test_404_means_legacy_cached_and_warned_once(self):
        calls = []

        def handler(request):
            calls.append(str(request.url))
            return httpx.Response(404, request=request, text="404 page not found")

        client = _make_sync_client(handler)

        with self.assertLogs("koyeb.sandbox.executor_client", level="WARNING") as logs:
            self.assertFalse(client.has_files_routes())
            self.assertFalse(client.has_files_routes())

        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0], "https://sb.example/files/stat")
        self.assertEqual(len([r for r in logs.output if "legacy" in r]), 1)

    def test_400_means_new_routes(self):
        def handler(request):
            return httpx.Response(
                400, request=request, json={"error": "path is required"}
            )

        client = _make_sync_client(handler)

        self.assertTrue(client.has_files_routes())
        self.assertTrue(client.has_files_routes())


class TestAsyncHasFilesRoutes(unittest.IsolatedAsyncioTestCase):
    async def test_404_means_legacy_cached_and_warned_once(self):
        calls = []

        def handler(request):
            calls.append(str(request.url))
            return httpx.Response(404, request=request, text="404 page not found")

        client = _make_async_client(handler)

        with self.assertLogs("koyeb.sandbox.executor_client", level="WARNING") as logs:
            self.assertFalse(await client.has_files_routes())
            self.assertFalse(await client.has_files_routes())

        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0], "https://sb.example/files/stat")
        self.assertEqual(len([r for r in logs.output if "legacy" in r]), 1)


class TestProbeTransientStatuses(unittest.TestCase):
    def test_429_raises_without_caching(self):
        calls = []

        def handler(request):
            calls.append(str(request.url))
            return httpx.Response(429, request=request, text="slow down")

        client = _make_sync_client(handler)
        for _ in range(2):
            with self.assertRaises(SandboxError):
                client.has_files_routes()
        # Uncached: an auth or rate-limit blip says nothing about the
        # routes, so every call probes again instead of poisoning the handle.
        self.assertEqual(len(calls), 2)


class TestAsyncProbeTransientStatuses(unittest.IsolatedAsyncioTestCase):
    async def test_401_raises_without_caching(self):
        calls = []

        def handler(request):
            calls.append(str(request.url))
            return httpx.Response(401, request=request, text="no")

        client = _make_async_client(handler)
        for _ in range(2):
            with self.assertRaises(SandboxError):
                await client.has_files_routes()
        self.assertEqual(len(calls), 2)


class TestHasFilesRoutesPositiveArms(unittest.TestCase):
    def test_2xx_means_routes_available(self):
        def handler(request):
            # Unexpected shape for a body-less stat, but a 2xx can only come
            # from a live /files/stat route.
            return httpx.Response(200, request=request, json={"type": "file"})

        client = _make_sync_client(handler)
        self.assertTrue(client.has_files_routes())


class TestAsyncHasFilesRoutesPositiveArms(unittest.IsolatedAsyncioTestCase):
    async def test_400_means_new_routes(self):
        def handler(request):
            return httpx.Response(
                400, request=request, json={"error": "path is required"}
            )

        client = _make_async_client(handler)
        self.assertTrue(await client.has_files_routes())
        self.assertTrue(await client.has_files_routes())

    async def test_2xx_means_routes_available(self):
        def handler(request):
            return httpx.Response(200, request=request, json={"type": "file"})

        client = _make_async_client(handler)
        self.assertTrue(await client.has_files_routes())


class TestFilesReadStatusArms(unittest.TestCase):
    def test_500_wraps_service_error(self):
        def handler(request):
            return httpx.Response(500, request=request, json={"error": "boom"})

        with self.assertRaises(SandboxServiceError) as cm:
            list(_make_sync_client(handler).files_read("/a"))

        self.assertEqual(cm.exception.status_code, 500)


class TestAsyncFilesReadStatusArms(unittest.IsolatedAsyncioTestCase):
    async def test_404_raises_request_error(self):
        def handler(request):
            return httpx.Response(
                404, request=request, json={"error": "file does not exist"}
            )

        client = _make_async_client(handler)
        with self.assertRaises(SandboxRequestError) as cm:
            async for _ in client.files_read("/missing"):
                pass
        self.assertEqual(cm.exception.status_code, 404)


class TestFilesRead400Boundary(unittest.TestCase):
    """A 400 is the probe's own answer code: the read stream must raise
    on it, not yield the error body as content."""

    def test_400_raises_request_error(self):
        def handler(request):
            return httpx.Response(
                400, request=request, json={"error": "path is required"}
            )

        with self.assertRaises(SandboxRequestError) as cm:
            list(_make_sync_client(handler).files_read("/a"))

        self.assertEqual(cm.exception.status_code, 400)


class TestAsyncFilesRead400Boundary(unittest.IsolatedAsyncioTestCase):
    async def test_400_raises_request_error(self):
        def handler(request):
            return httpx.Response(
                400, request=request, json={"error": "path is required"}
            )

        with self.assertRaises(SandboxRequestError) as cm:
            async for _ in _make_async_client(handler).files_read("/a"):
                pass

        self.assertEqual(cm.exception.status_code, 400)


class TestFilesPutParents(unittest.TestCase):
    def test_parents_flag_is_sent(self):
        seen = {}

        def handler(request):
            seen["url"] = str(request.url)
            return httpx.Response(
                200, request=request, json={"size": 3, "sha256": "sum"}
            )

        _make_sync_client(handler).files_put("/tmp/a/b.txt", b"abc", parents=True)

        self.assertEqual(
            seen["url"],
            "https://sb.example/files?path=%2Ftmp%2Fa%2Fb.txt&parents=1",
        )


class TestFilesRouteTimeouts(unittest.TestCase):
    """The timeout error names the bound that fired: the 60 s idle bound
    on the streamed /files routes, the 30 s total cap elsewhere."""

    def test_files_route_names_idle_bound(self):
        def handler(request):
            raise httpx.ReadTimeout("idle", request=request)

        with self.assertRaises(SandboxTimeoutError) as cm:
            _make_sync_client(handler).files_put("/a", b"abc")

        self.assertEqual(str(cm.exception), "Request timed out after 60s")

    def test_legacy_call_names_total_cap(self):
        def handler(request):
            raise httpx.ReadTimeout("slow", request=request)

        with self.assertRaises(SandboxTimeoutError) as cm:
            _make_sync_client(handler).read_file("/a")

        self.assertEqual(str(cm.exception), "Request timed out after 30s")


class TestAsyncFilesRouteTimeouts(unittest.IsolatedAsyncioTestCase):
    async def test_files_route_names_idle_bound(self):
        def handler(request):
            raise httpx.ReadTimeout("idle", request=request)

        with self.assertRaises(SandboxTimeoutError) as cm:
            await _make_async_client(handler).files_put("/a", b"abc")

        self.assertEqual(str(cm.exception), "Request timed out after 60s")


class TestFilesReadTimeouts(unittest.TestCase):
    """An idle stall mid-download is a timeout by name, not a generic
    connection failure; a reset mid-stream stays generic."""

    def test_idle_stall_names_the_bound(self):
        def handler(request):
            raise httpx.ReadTimeout("idle", request=request)

        with self.assertRaises(SandboxTimeoutError) as cm:
            list(_make_sync_client(handler).files_read("/a"))

        self.assertEqual(str(cm.exception), "Request timed out after 60s")

    def test_reset_mid_stream_wraps_generic(self):
        def handler(request):
            raise httpx.ReadError("reset", request=request)

        with self.assertRaises(SandboxError) as cm:
            list(_make_sync_client(handler).files_read("/a"))

        self.assertIn("Request to sandbox executor failed", str(cm.exception))


class TestAsyncFilesReadTimeouts(unittest.IsolatedAsyncioTestCase):
    async def test_idle_stall_names_the_bound(self):
        def handler(request):
            raise httpx.ReadTimeout("idle", request=request)

        with self.assertRaises(SandboxTimeoutError) as cm:
            async for _ in _make_async_client(handler).files_read("/a"):
                pass

        self.assertEqual(str(cm.exception), "Request timed out after 60s")

    async def test_reset_mid_stream_wraps_generic(self):
        def handler(request):
            raise httpx.ReadError("reset", request=request)

        with self.assertRaises(SandboxError) as cm:
            async for _ in _make_async_client(handler).files_read("/a"):
                pass

        self.assertIn("Request to sandbox executor failed", str(cm.exception))


class TestFilesUploadOpen(unittest.TestCase):
    def test_sends_post_and_returns_session(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            seen["body"] = json.loads(request.read())
            return httpx.Response(
                200,
                request=request,
                json={"upload_id": "u-1", "max_part_size": 104857600},
            )

        reply = _make_sync_client(handler).files_upload_open(
            "/tmp/a.bin", 1024, mode="0644", sha256="ab" * 32
        )

        self.assertEqual(seen["method"], "POST")
        self.assertEqual(seen["url"], "https://sb.example/files/uploads")
        self.assertEqual(
            seen["body"],
            {"path": "/tmp/a.bin", "size": 1024, "mode": "0644", "sha256": "ab" * 32},
        )
        self.assertEqual(reply, {"upload_id": "u-1", "max_part_size": 104857600})

    def test_500_is_not_retried(self):
        # An open creates executor state; a blind retry orphans a session.
        calls = []

        def handler(request):
            calls.append(request)
            return httpx.Response(500, request=request, json={"error": "boom"})

        with self.assertRaises(SandboxServiceError):
            _make_sync_client(handler).files_upload_open("/tmp/a.bin", 1024)

        self.assertEqual(len(calls), 1)

    def test_minimal_payload_omits_optionals(self):
        seen = {}

        def handler(request):
            seen["body"] = json.loads(request.read())
            return httpx.Response(
                200, request=request, json={"upload_id": "u-2", "max_part_size": 1}
            )

        _make_sync_client(handler).files_upload_open("/tmp/a.bin", 0)

        self.assertEqual(seen["body"], {"path": "/tmp/a.bin", "size": 0})


class TestAsyncFilesUploadOpen(unittest.IsolatedAsyncioTestCase):
    async def test_500_is_not_retried(self):
        # An open creates executor state; a blind retry orphans a session.
        calls = []

        def handler(request):
            calls.append(request)
            return httpx.Response(500, request=request, json={"error": "boom"})

        with self.assertRaises(SandboxServiceError):
            await _make_async_client(handler).files_upload_open("/tmp/b", 7)

        self.assertEqual(len(calls), 1)

    async def test_sends_post_and_returns_session(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            seen["body"] = json.loads(request.read())
            return httpx.Response(
                200, request=request, json={"upload_id": "u-3", "max_part_size": 5}
            )

        reply = await _make_async_client(handler).files_upload_open("/tmp/b", 7)

        self.assertEqual(seen["method"], "POST")
        self.assertEqual(seen["url"], "https://sb.example/files/uploads")
        self.assertEqual(seen["body"], {"path": "/tmp/b", "size": 7})
        self.assertEqual(reply, {"upload_id": "u-3", "max_part_size": 5})


class TestFilesUploadPart(unittest.TestCase):
    def test_writes_part_at_offset(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            seen["content_type"] = request.headers.get("Content-Type")
            seen["sha_header"] = request.headers.get("X-Content-SHA256")
            seen["body"] = request.read()
            return httpx.Response(204, request=request)

        _make_sync_client(handler).files_upload_part(
            "u-1", 50, b"abc", sha256="ab" * 32
        )

        self.assertEqual(seen["method"], "PUT")
        self.assertEqual(seen["url"], "https://sb.example/files/uploads/u-1?offset=50")
        self.assertEqual(seen["content_type"], "application/octet-stream")
        self.assertEqual(seen["sha_header"], "ab" * 32)
        self.assertEqual(seen["body"], b"abc")

    def test_unknown_session_raises_request_error(self):
        def handler(request):
            return httpx.Response(
                404, request=request, json={"error": "unknown upload session"}
            )

        with self.assertRaises(SandboxRequestError) as cm:
            _make_sync_client(handler).files_upload_part("gone", 0, b"abc")

        self.assertEqual(cm.exception.status_code, 404)


class TestAsyncFilesUploadPart(unittest.IsolatedAsyncioTestCase):
    async def test_writes_part_at_offset(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            seen["body"] = request.read()
            return httpx.Response(204, request=request)

        await _make_async_client(handler).files_upload_part("u-4", 0, b"xyz")

        self.assertEqual(seen["method"], "PUT")
        self.assertEqual(seen["url"], "https://sb.example/files/uploads/u-4?offset=0")
        self.assertEqual(seen["body"], b"xyz")


class TestFilesUploadStatus(unittest.TestCase):
    def test_returns_size_and_ranges(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            return httpx.Response(
                200,
                request=request,
                json={
                    "size": 10,
                    "ranges": [{"start": 0, "end": 4}, {"start": 6, "end": 10}],
                },
            )

        reply = _make_sync_client(handler).files_upload_status("u-1")

        self.assertEqual(seen["method"], "GET")
        self.assertEqual(seen["url"], "https://sb.example/files/uploads/u-1")
        self.assertEqual(
            reply,
            {"size": 10, "ranges": [{"start": 0, "end": 4}, {"start": 6, "end": 10}]},
        )


class TestAsyncFilesUploadStatus(unittest.IsolatedAsyncioTestCase):
    async def test_returns_size_and_ranges(self):
        def handler(request):
            return httpx.Response(200, request=request, json={"size": 3, "ranges": []})

        reply = await _make_async_client(handler).files_upload_status("u-5")

        self.assertEqual(reply, {"size": 3, "ranges": []})


class TestFilesUploadComplete(unittest.TestCase):
    def test_500_is_not_retried(self):
        # A complete commits the file; a blind retry hits a gone session
        # and would report a landed upload as lost.
        calls = []

        def handler(request):
            calls.append(request)
            return httpx.Response(500, request=request, json={"error": "boom"})

        with self.assertRaises(SandboxServiceError):
            _make_sync_client(handler).files_upload_complete("u-1")

        self.assertEqual(len(calls), 1)

    def test_returns_commit_reply(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            return httpx.Response(
                200, request=request, json={"size": 10, "sha256": "ab" * 32}
            )

        reply = _make_sync_client(handler).files_upload_complete("u-1")

        self.assertEqual(seen["method"], "POST")
        self.assertEqual(seen["url"], "https://sb.example/files/uploads/u-1/complete")
        self.assertEqual(reply, {"size": 10, "sha256": "ab" * 32})

    def test_missing_ranges_raise_409_with_ranges_in_body(self):
        def handler(request):
            return httpx.Response(
                409,
                request=request,
                json={
                    "error": "2 range(s) of the upload are still missing",
                    "ranges": [{"start": 0, "end": 2}, {"start": 8, "end": 10}],
                },
            )

        with self.assertRaises(SandboxRequestError) as cm:
            _make_sync_client(handler).files_upload_complete("u-1")

        self.assertEqual(cm.exception.status_code, 409)
        # The resume signal: the session stays live and the body carries
        # the missing spans.
        payload = json.loads(cm.exception.body)
        self.assertEqual(
            payload["ranges"], [{"start": 0, "end": 2}, {"start": 8, "end": 10}]
        )


class TestAsyncFilesUploadComplete(unittest.IsolatedAsyncioTestCase):
    async def test_500_is_not_retried(self):
        # A complete commits the file; a blind retry hits a gone session
        # and would report a landed upload as lost.
        calls = []

        def handler(request):
            calls.append(request)
            return httpx.Response(500, request=request, json={"error": "boom"})

        with self.assertRaises(SandboxServiceError):
            await _make_async_client(handler).files_upload_complete("u-6")

        self.assertEqual(len(calls), 1)

    async def test_returns_commit_reply(self):
        def handler(request):
            return httpx.Response(200, request=request, json={"size": 4})

        reply = await _make_async_client(handler).files_upload_complete("u-6")

        self.assertEqual(reply, {"size": 4})


class TestFilesUploadAbort(unittest.TestCase):
    def test_deletes_session(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            return httpx.Response(204, request=request)

        self.assertIsNone(_make_sync_client(handler).files_upload_abort("u-1"))

        self.assertEqual(seen["method"], "DELETE")
        self.assertEqual(seen["url"], "https://sb.example/files/uploads/u-1")


class TestAsyncFilesUploadAbort(unittest.IsolatedAsyncioTestCase):
    async def test_deletes_session(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            return httpx.Response(204, request=request)

        self.assertIsNone(await _make_async_client(handler).files_upload_abort("u-7"))

        self.assertEqual(seen["method"], "DELETE")


class TestFilesList(unittest.TestCase):
    def test_streams_ndjson_entries(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            body = (
                b'{"path": "a.txt", "type": "file", "size": 3, '
                b'"mode": "0644", "mtime": "2026-10-27T10:00:00Z"}\n'
                b'{"path": "sub", "type": "dir", "size": 0, '
                b'"mode": "0755", "mtime": "2026-10-27T10:00:00Z"}\n'
            )
            return httpx.Response(
                200,
                request=request,
                content=body,
                headers={"Content-Type": "application/x-ndjson"},
            )

        entries = list(_make_sync_client(handler).files_list("/tmp", recursive=True))

        self.assertEqual(seen["method"], "GET")
        self.assertEqual(
            seen["url"], "https://sb.example/files/list?path=%2Ftmp&recursive=1"
        )
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["path"], "a.txt")
        self.assertEqual(entries[0]["type"], "file")
        self.assertEqual(entries[1]["path"], "sub")
        self.assertEqual(entries[1]["type"], "dir")

    def test_recursive_flag_omitted_by_default(self):
        seen = {}

        def handler(request):
            seen["url"] = str(request.url)
            return httpx.Response(
                200,
                request=request,
                content=b"",
                headers={"Content-Type": "application/x-ndjson"},
            )

        list(_make_sync_client(handler).files_list("/tmp"))

        self.assertEqual(seen["url"], "https://sb.example/files/list?path=%2Ftmp")

    def test_error_entry_passes_through(self):
        def handler(request):
            body = (
                b'{"path": "a.txt", "type": "file", "size": 3, '
                b'"mode": "0644", "mtime": "2026-10-27T10:00:00Z"}\n'
                b'{"path": "b.txt", "error": "permission denied"}\n'
            )
            return httpx.Response(
                200,
                request=request,
                content=body,
                headers={"Content-Type": "application/x-ndjson"},
            )

        entries = list(_make_sync_client(handler).files_list("/tmp"))

        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[1], {"path": "b.txt", "error": "permission denied"})

    def test_404_raises_request_error(self):
        def handler(request):
            return httpx.Response(
                404, request=request, json={"error": "no such file or directory"}
            )

        with self.assertRaises(SandboxRequestError) as ctx:
            list(_make_sync_client(handler).files_list("/tmp/missing"))

        self.assertEqual(ctx.exception.status_code, 404)


class TestAsyncFilesList(unittest.IsolatedAsyncioTestCase):
    async def test_streams_ndjson_entries(self):
        seen = {}

        def handler(request):
            seen["url"] = str(request.url)
            body = (
                b'{"path": "a.txt", "type": "file", "size": 3, '
                b'"mode": "0644", "mtime": "2026-10-27T10:00:00Z"}\n'
            )
            return httpx.Response(
                200,
                request=request,
                content=body,
                headers={"Content-Type": "application/x-ndjson"},
            )

        entries = [
            e
            async for e in _make_async_client(handler).files_list(
                "/tmp", recursive=True
            )
        ]

        self.assertEqual(
            seen["url"], "https://sb.example/files/list?path=%2Ftmp&recursive=1"
        )
        self.assertEqual(
            entries,
            [
                {
                    "path": "a.txt",
                    "type": "file",
                    "size": 3,
                    "mode": "0644",
                    "mtime": "2026-10-27T10:00:00Z",
                }
            ],
        )

    async def test_400_raises_request_error(self):
        def handler(request):
            return httpx.Response(
                400, request=request, json={"error": "path is required"}
            )

        with self.assertRaises(SandboxRequestError) as ctx:
            async for _ in _make_async_client(handler).files_list("/tmp"):
                pass

        self.assertEqual(ctx.exception.status_code, 400)


class TestFilesListTimeouts(unittest.TestCase):
    def test_idle_stall_names_the_bound(self):
        def handler(request):
            raise httpx.ReadTimeout("idle", request=request)

        with self.assertRaises(SandboxTimeoutError) as cm:
            list(_make_sync_client(handler).files_list("/tmp"))

        self.assertEqual(str(cm.exception), "Request timed out after 60s")


class TestAsyncFilesListTimeouts(unittest.IsolatedAsyncioTestCase):
    async def test_idle_stall_names_the_bound(self):
        def handler(request):
            raise httpx.ReadTimeout("idle", request=request)

        with self.assertRaises(SandboxTimeoutError) as cm:
            async for _ in _make_async_client(handler).files_list("/tmp"):
                pass

        self.assertEqual(str(cm.exception), "Request timed out after 60s")


class TestFilesArchiveGet(unittest.TestCase):
    def test_streams_archive_bytes_with_excludes(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            return httpx.Response(
                200, request=request, content=b"\x1f\x8barchive-bytes"
            )

        chunks = list(
            _make_sync_client(handler).files_archive_get(
                "/tmp", exclude=("*.log", ".git")
            )
        )

        self.assertEqual(seen["method"], "GET")
        self.assertEqual(
            seen["url"],
            "https://sb.example/files/archive?path=%2Ftmp&exclude=%2A.log&exclude=.git",
        )
        self.assertEqual(b"".join(chunks), b"\x1f\x8barchive-bytes")

    def test_no_excludes_omits_param(self):
        seen = {}

        def handler(request):
            seen["url"] = str(request.url)
            return httpx.Response(200, request=request, content=b"")

        list(_make_sync_client(handler).files_archive_get("/tmp"))

        self.assertEqual(seen["url"], "https://sb.example/files/archive?path=%2Ftmp")

    def test_400_on_bad_pattern_raises(self):
        def handler(request):
            return httpx.Response(
                400, request=request, json={"error": 'bad exclude pattern "["'}
            )

        with self.assertRaises(SandboxRequestError) as ctx:
            list(_make_sync_client(handler).files_archive_get("/tmp", exclude=("[",)))

        self.assertEqual(ctx.exception.status_code, 400)


class TestAsyncFilesArchiveGet(unittest.IsolatedAsyncioTestCase):
    async def test_streams_archive_bytes_with_excludes(self):
        seen = {}

        def handler(request):
            seen["url"] = str(request.url)
            return httpx.Response(
                200, request=request, content=b"\x1f\x8barchive-bytes"
            )

        chunks = [
            c
            async for c in _make_async_client(handler).files_archive_get(
                "/tmp", exclude=("*.log",)
            )
        ]

        self.assertEqual(
            seen["url"],
            "https://sb.example/files/archive?path=%2Ftmp&exclude=%2A.log",
        )
        self.assertEqual(b"".join(chunks), b"\x1f\x8barchive-bytes")

    async def test_400_on_bad_pattern_raises(self):
        def handler(request):
            return httpx.Response(
                400, request=request, json={"error": 'bad exclude pattern "["'}
            )

        with self.assertRaises(SandboxRequestError) as ctx:
            async for _ in _make_async_client(handler).files_archive_get(
                "/tmp", exclude=("[",)
            ):
                pass

        self.assertEqual(ctx.exception.status_code, 400)


class TestFilesArchiveGetTimeouts(unittest.TestCase):
    def test_idle_stall_names_the_bound(self):
        def handler(request):
            raise httpx.ReadTimeout("idle", request=request)

        with self.assertRaises(SandboxTimeoutError) as cm:
            list(_make_sync_client(handler).files_archive_get("/tmp"))

        self.assertEqual(str(cm.exception), "Request timed out after 60s")


class TestAsyncFilesArchiveGetTimeouts(unittest.IsolatedAsyncioTestCase):
    async def test_idle_stall_names_the_bound(self):
        def handler(request):
            raise httpx.ReadTimeout("idle", request=request)

        with self.assertRaises(SandboxTimeoutError) as cm:
            async for _ in _make_async_client(handler).files_archive_get("/tmp"):
                pass

        self.assertEqual(str(cm.exception), "Request timed out after 60s")


class TestFilesArchivePut(unittest.TestCase):
    def test_streams_body_and_returns_counts(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            seen["content_type"] = request.headers.get("Content-Type")
            seen["body"] = request.read()
            return httpx.Response(200, request=request, json={"files": 2, "bytes": 10})

        reply = _make_sync_client(handler).files_archive_put("/tmp", b"tar-bytes")

        self.assertEqual(seen["method"], "PUT")
        self.assertEqual(seen["url"], "https://sb.example/files/archive?path=%2Ftmp")
        self.assertEqual(seen["content_type"], "application/octet-stream")
        self.assertEqual(seen["body"], b"tar-bytes")
        self.assertEqual(reply, {"files": 2, "bytes": 10})

    def test_accepts_iterable_content(self):
        seen = {}

        def handler(request):
            seen["body"] = request.read()
            return httpx.Response(200, request=request, json={"files": 0, "bytes": 0})

        def chunks():
            yield b"tar-"
            yield b"bytes"

        reply = _make_sync_client(handler).files_archive_put("/tmp", chunks())

        self.assertEqual(seen["body"], b"tar-bytes")
        self.assertEqual(reply, {"files": 0, "bytes": 0})

    def test_400_on_bad_gzip_raises(self):
        def handler(request):
            return httpx.Response(
                400,
                request=request,
                json={"error": "reading gzip stream: gzip: invalid header"},
            )

        with self.assertRaises(SandboxRequestError) as ctx:
            _make_sync_client(handler).files_archive_put("/tmp", b"not-gzip")

        self.assertEqual(ctx.exception.status_code, 400)

    def test_mid_stream_failure_is_not_retried(self):
        calls = []

        def handler(request):
            calls.append(1)
            raise httpx.ReadError("reset mid-stream", request=request)

        with self.assertRaises(SandboxError):
            _make_sync_client(handler).files_archive_put("/tmp", b"tar-bytes")

        # A consumed stream cannot replay; only a connect-time failure
        # (the request never left) is retried.
        self.assertEqual(len(calls), 1)

    def test_5xx_is_not_blindly_retried(self):
        calls = []

        def handler(request):
            calls.append(1)
            return httpx.Response(502, request=request, json={"error": "bad gateway"})

        with self.assertRaises(SandboxRequestError):
            _make_sync_client(handler).files_archive_put("/tmp", b"tar-bytes")

        self.assertEqual(len(calls), 1)


class TestAsyncFilesArchivePut(unittest.IsolatedAsyncioTestCase):
    async def test_streams_body_and_returns_counts(self):
        seen = {}

        def handler(request):
            seen["method"] = request.method
            seen["url"] = str(request.url)
            seen["body"] = request.read()
            return httpx.Response(200, request=request, json={"files": 1, "bytes": 5})

        reply = await _make_async_client(handler).files_archive_put(
            "/tmp", b"tar-bytes"
        )

        self.assertEqual(seen["method"], "PUT")
        self.assertEqual(seen["url"], "https://sb.example/files/archive?path=%2Ftmp")
        self.assertEqual(seen["body"], b"tar-bytes")
        self.assertEqual(reply, {"files": 1, "bytes": 5})

    async def test_accepts_async_iterable_content(self):
        seen = {}

        def handler(request):
            seen["body"] = request.read()
            return httpx.Response(200, request=request, json={"files": 0, "bytes": 0})

        async def chunks():
            yield b"tar-"
            yield b"bytes"

        await _make_async_client(handler).files_archive_put("/tmp", chunks())

        self.assertEqual(seen["body"], b"tar-bytes")

    async def test_accepts_file_object_content(self):
        import io

        seen = {}

        def handler(request):
            seen["body"] = request.read()
            return httpx.Response(200, request=request, json={"files": 0, "bytes": 0})

        await _make_async_client(handler).files_archive_put("/tmp", io.BytesIO(b"xyz"))

        self.assertEqual(seen["body"], b"xyz")

    async def test_mid_stream_failure_is_not_retried(self):
        calls = []

        def handler(request):
            calls.append(1)
            raise httpx.ReadError("reset mid-stream", request=request)

        with self.assertRaises(SandboxError):
            await _make_async_client(handler).files_archive_put("/tmp", b"tar-bytes")

        # A consumed stream cannot replay; only a connect-time failure
        # (the request never left) is retried.
        self.assertEqual(len(calls), 1)

    async def test_5xx_is_not_blindly_retried(self):
        calls = []

        def handler(request):
            calls.append(1)
            return httpx.Response(502, request=request, json={"error": "bad gateway"})

        with self.assertRaises(SandboxRequestError):
            await _make_async_client(handler).files_archive_put("/tmp", b"tar-bytes")

        self.assertEqual(len(calls), 1)


class TestFilesArchivePutTimeouts(unittest.TestCase):
    def test_names_idle_bound_on_timeout(self):
        def handler(request):
            raise httpx.ReadTimeout("idle", request=request)

        with self.assertRaises(SandboxTimeoutError) as cm:
            _make_sync_client(handler).files_archive_put("/tmp", b"tar")

        self.assertEqual(str(cm.exception), "Request timed out after 60s")


class TestAsyncFilesArchivePutTimeouts(unittest.IsolatedAsyncioTestCase):
    async def test_names_idle_bound_on_timeout(self):
        def handler(request):
            raise httpx.ReadTimeout("idle", request=request)

        with self.assertRaises(SandboxTimeoutError) as cm:
            await _make_async_client(handler).files_archive_put("/tmp", b"tar")

        self.assertEqual(str(cm.exception), "Request timed out after 60s")


class TestFilesPutTimeoutOverride(unittest.TestCase):
    """upload_file(timeout=) reaches the wire as the streamed PUT's bound."""

    def test_override_replaces_the_idle_bound(self):
        seen = {}

        def handler(request):
            return httpx.Response(
                200, request=request, json={"size": 3, "sha256": "ab" * 32}
            )

        client = _make_sync_client(handler)
        with _request_spy(client, seen):
            client.files_put("/a", b"xyz", timeout=90)

        self.assertEqual(
            seen["timeout"], httpx.Timeout(90, connect=DEFAULT_HTTP_TIMEOUT)
        )

    def test_default_keeps_the_files_idle_bound(self):
        seen = {}

        def handler(request):
            return httpx.Response(
                200, request=request, json={"size": 3, "sha256": "ab" * 32}
            )

        client = _make_sync_client(handler)
        with _request_spy(client, seen):
            client.files_put("/a", b"xyz")

        self.assertEqual(seen["timeout"], _FILES_TIMEOUT)


class TestAsyncFilesPutTimeoutOverride(unittest.IsolatedAsyncioTestCase):
    async def test_override_replaces_the_idle_bound(self):
        seen = {}

        def handler(request):
            return httpx.Response(
                200, request=request, json={"size": 3, "sha256": "ab" * 32}
            )

        client = _make_async_client(handler)
        with _async_request_spy(client, seen):
            await client.files_put("/a", b"xyz", timeout=90)

        self.assertEqual(
            seen["timeout"], httpx.Timeout(90, connect=DEFAULT_HTTP_TIMEOUT)
        )


class TestFilesReadTimeoutOverride(unittest.TestCase):
    def test_override_reaches_the_stream(self):
        seen = {}

        def handler(request):
            return httpx.Response(200, request=request, content=b"data")

        client = _make_sync_client(handler)
        with _stream_spy(client, seen):
            chunks = list(client.files_read("/a", timeout=90))

        self.assertEqual(chunks, [b"data"])
        self.assertEqual(
            seen["timeout"], httpx.Timeout(90, connect=DEFAULT_HTTP_TIMEOUT)
        )


class TestAsyncFilesReadTimeoutOverride(unittest.IsolatedAsyncioTestCase):
    async def test_override_reaches_the_stream(self):
        seen = {}

        def handler(request):
            return httpx.Response(200, request=request, content=b"data")

        client = _make_async_client(handler)
        with _stream_spy(client, seen):
            chunks = [c async for c in client.files_read("/a", timeout=90)]

        self.assertEqual(chunks, [b"data"])
        self.assertEqual(
            seen["timeout"], httpx.Timeout(90, connect=DEFAULT_HTTP_TIMEOUT)
        )


class TestFilesUploadTimeoutOverride(unittest.TestCase):
    """The multipart flow's calls take the per-call timeout override.

    Parts keep the idle-bound shape; the control calls (open, complete)
    get the override as their per-phase bound.
    """

    def test_part_override_reaches_the_wire(self):
        seen = {}

        def handler(request):
            return httpx.Response(204, request=request)

        client = _make_sync_client(handler)
        with _request_spy(client, seen):
            client.files_upload_part("u-1", 0, b"abc", timeout=90)

        self.assertEqual(
            seen["timeout"], httpx.Timeout(90, connect=DEFAULT_HTTP_TIMEOUT)
        )

    def test_part_default_keeps_the_files_idle_bound(self):
        seen = {}

        def handler(request):
            return httpx.Response(204, request=request)

        client = _make_sync_client(handler)
        with _request_spy(client, seen):
            client.files_upload_part("u-1", 0, b"abc")

        self.assertEqual(seen["timeout"], _FILES_TIMEOUT)

    def test_open_override_reaches_the_wire(self):
        seen = {}

        def handler(request):
            return httpx.Response(
                200, request=request, json={"upload_id": "u", "max_part_size": 1}
            )

        client = _make_sync_client(handler)
        with _request_spy(client, seen):
            client.files_upload_open("/a", 10, timeout=90)

        self.assertEqual(
            seen["timeout"], httpx.Timeout(90, connect=DEFAULT_HTTP_TIMEOUT)
        )

    def test_complete_override_reaches_the_wire(self):
        seen = {}

        def handler(request):
            return httpx.Response(
                200, request=request, json={"size": 10, "sha256": "ab" * 32}
            )

        client = _make_sync_client(handler)
        with _request_spy(client, seen):
            client.files_upload_complete("u-1", timeout=90)

        self.assertEqual(
            seen["timeout"], httpx.Timeout(90, connect=DEFAULT_HTTP_TIMEOUT)
        )


class TestAsyncFilesUploadTimeoutOverride(unittest.IsolatedAsyncioTestCase):
    async def test_part_override_reaches_the_wire(self):
        seen = {}

        def handler(request):
            return httpx.Response(204, request=request)

        client = _make_async_client(handler)
        with _async_request_spy(client, seen):
            await client.files_upload_part("u-1", 0, b"abc", timeout=90)

        self.assertEqual(
            seen["timeout"], httpx.Timeout(90, connect=DEFAULT_HTTP_TIMEOUT)
        )

    async def test_open_override_reaches_the_wire(self):
        seen = {}

        def handler(request):
            return httpx.Response(
                200, request=request, json={"upload_id": "u", "max_part_size": 1}
            )

        client = _make_async_client(handler)
        with _async_request_spy(client, seen):
            await client.files_upload_open("/a", 10, timeout=90)

        self.assertEqual(
            seen["timeout"], httpx.Timeout(90, connect=DEFAULT_HTTP_TIMEOUT)
        )

    async def test_complete_override_reaches_the_wire(self):
        seen = {}

        def handler(request):
            return httpx.Response(
                200, request=request, json={"size": 10, "sha256": "ab" * 32}
            )

        client = _make_async_client(handler)
        with _async_request_spy(client, seen):
            await client.files_upload_complete("u-1", timeout=90)

        self.assertEqual(
            seen["timeout"], httpx.Timeout(90, connect=DEFAULT_HTTP_TIMEOUT)
        )


if __name__ == "__main__":
    unittest.main()
