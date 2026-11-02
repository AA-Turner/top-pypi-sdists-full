from __future__ import annotations

from importlib.metadata import version

import json
import unittest
from collections.abc import Awaitable, Callable
from typing import Any
from unittest.mock import AsyncMock, patch

import httpx

from http_mock import set_handler

from runta import (
    ApiError,
    AsyncRunta,
    CommandResult,
    CreateRuntimeResourceRequests,
    CreateRuntimeResources,
    EgressMode,
    EgressPolicy,
    PatchRuntimeResourceRequests,
    PatchRuntimeResources,
    RuntimeResourceLimits,
    Runta,
)
from runta._internal.async_http import _AsyncHttpClient
from runta._internal.sync_http import _SyncHttpClient

AsyncHandler = Callable[[httpx.Request], Awaitable[httpx.Response]]


def _restore_resource_cases() -> list[tuple[Any, dict[str, Any] | None]]:
    return [
        (None, None),
        (
            {"requests": {"vcpus": 2, "memory_mib": 2048}},
            {"requests": {"vcpus": 2, "memory_mib": 2048}},
        ),
        (
            CreateRuntimeResources(
                requests=CreateRuntimeResourceRequests(vcpus=4, memory_mib=3072),
                limits=RuntimeResourceLimits(memory_mib=6144),
            ),
            {
                "requests": {"vcpus": 4, "memory_mib": 3072},
                "limits": {"memory_mib": 6144},
            },
        ),
    ]


class OpenApiTransportTests(unittest.IsolatedAsyncioTestCase):
    async def asyncTearDown(self) -> None:
        http = getattr(self, "http", None)
        if http is not None:
            await http.close()

    def _http(self, handler: AsyncHandler) -> _AsyncHttpClient:
        http = _AsyncHttpClient("http://runta.test", "rt_test", timeout=12)
        set_handler(http, handler)
        self.http = http
        return http

    async def test_lists_all_cursor_pages_without_changing_public_methods(
        self,
    ) -> None:
        calls: list[tuple[str, dict[str, str]]] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            params = dict(request.url.params)
            calls.append((request.url.path, params))
            if request.url.path == "/v2/runtimes":
                if params.get("after") == "runtime-cursor":
                    return _json_response(
                        {
                            "data": [_runtime_json() | {"id": "runtime-1"}],
                            "pagination": {
                                "next_cursor": None,
                                "has_more": False,
                            },
                        }
                    )
                return _json_response(
                    {
                        "data": [_runtime_json() | {"id": "runtime-2"}],
                        "pagination": {
                            "next_cursor": "runtime-cursor",
                            "has_more": True,
                        },
                    }
                )
            if params.get("after") == "checkpoint-cursor":
                return _json_response(
                    {
                        "data": [_checkpoint_json() | {"id": "checkpoint-1"}],
                        "pagination": {
                            "next_cursor": None,
                            "has_more": False,
                        },
                    }
                )
            return _json_response(
                {
                    "data": [_checkpoint_json() | {"id": "checkpoint-2"}],
                    "pagination": {
                        "next_cursor": "checkpoint-cursor",
                        "has_more": True,
                    },
                }
            )

        http = self._http(handler)

        runtimes = await http.list_runtimes("running")
        checkpoints = await http.list_checkpoints()

        self.assertEqual(
            [runtime.id for runtime in runtimes], ["runtime-2", "runtime-1"]
        )
        self.assertEqual(
            [checkpoint.id for checkpoint in checkpoints],
            ["checkpoint-2", "checkpoint-1"],
        )
        self.assertEqual(
            calls,
            [
                ("/v2/runtimes", {"status": "running", "limit": "100"}),
                (
                    "/v2/runtimes",
                    {
                        "status": "running",
                        "limit": "100",
                        "after": "runtime-cursor",
                    },
                ),
                (
                    "/v2/checkpoints",
                    {"limit": "100"},
                ),
                (
                    "/v2/checkpoints",
                    {
                        "limit": "100",
                        "after": "checkpoint-cursor",
                    },
                ),
            ],
        )

    async def test_rejects_invalid_and_repeated_cursor_pages(self) -> None:
        async def missing_handler(_request: httpx.Request) -> httpx.Response:
            return _json_response(
                {
                    "data": [],
                    "pagination": {"next_cursor": None, "has_more": True},
                }
            )

        http = self._http(missing_handler)
        with self.assertRaisesRegex(ApiError, "Invalid pagination cursor"):
            await http.list_runtimes()

        responses = iter(
            [
                _json_response(
                    {
                        "data": [],
                        "pagination": {"next_cursor": "same", "has_more": True},
                    }
                ),
                _json_response(
                    {
                        "data": [],
                        "pagination": {"next_cursor": "same", "has_more": True},
                    }
                ),
            ]
        )

        async def repeated_handler(_request: httpx.Request) -> httpx.Response:
            return next(responses)

        await http.close()
        http = self._http(repeated_handler)
        with self.assertRaisesRegex(ApiError, "Repeated pagination cursor"):
            await http.list_runtimes()

    async def test_exec_uses_streaming_transport(self) -> None:
        result = CommandResult(exit_code=0, stdout=b"ok", stderr=b"", duration=0.1)
        execute = AsyncMock(return_value=result)
        http = self._http(AsyncMock())

        with patch("runta._internal.streaming_transfer.async_execute", execute):
            returned = await http.execute("runtime-1", "echo", ["ok"], timeout=10)

        self.assertIs(returned, result)
        execute.assert_awaited_once_with(
            "http://runta.test",
            "rt_test",
            "runtime-1",
            "echo",
            ["ok"],
            env=None,
            stdin=None,
            timeout=10,
            max_output_bytes=None,
            connect_timeout=12,
            idle_timeout=None,
            _tls=http._websocket_tls,
        )

    async def test_create_runtime_sends_generated_nested_resource_body_and_auth(
        self,
    ) -> None:
        seen: dict[str, Any] = {}

        async def handler(request: httpx.Request) -> httpx.Response:
            seen["method"] = request.method
            seen["path"] = request.url.path
            seen["headers"] = request.headers
            seen["json"] = _json(request)
            body = seen["json"]
            return _json_response(
                {
                    "data": _runtime_json(
                        vcpus=body["resources"]["requests"]["vcpus"],
                        memory_mib=body["resources"]["requests"]["memory_mib"],
                        limit_memory_mib=body["resources"]["limits"]["memory_mib"],
                        ingress_specs=body["ingress_specs"],
                        egress_policy=body["egress_policy"],
                    )
                },
                status_code=201,
            )

        http = self._http(handler)
        info = await http.create_runtime(
            "sb-create",
            vcpus=2,
            memory_mib=1536,
            memory_max_mib=4096,
            ingress_specs=[{"protocol": "http", "runtime_port": 8080}],
            egress_policy=EgressPolicy(
                mode=EgressMode.ALLOWLIST,
                allowed_hosts=["pypi.org"],
                denied_hosts=["example.org"],
            ),
            idle_suspend_after_secs=60,
        )

        self.assertEqual(seen["method"], "POST")
        self.assertEqual(seen["path"], "/v2/runtimes")
        self.assertEqual(seen["headers"]["authorization"], "Bearer rt_test")
        self.assertIn(
            f"runta-python-sdk/{version('runta-sdk')}", seen["headers"]["user-agent"]
        )
        self.assertEqual(
            seen["json"],
            {
                "egress_policy": {
                    "allowed_hosts": ["pypi.org"],
                    "mode": "allowlist",
                },
                "idle_policy": {
                    "mode": "suspend_and_wakeup",
                    "suspend_after_secs": 60,
                },
                "ingress_specs": [{"protocol": "http", "runtime_port": 8080}],
                "llm_tool_io_capture_enabled": False,
                "llm_session_content_capture_enabled": False,
                "name": "sb-create",
                "resources": {
                    "limits": {"memory_mib": 4096},
                    "requests": {"memory_mib": 1536, "vcpus": 2},
                },
                "vnc_enabled": False,
            },
        )
        self.assertEqual(info.resources.requests.vcpus, 2)
        self.assertEqual(info.resources.requests.memory_mib, 1536)
        self.assertEqual(info.resources.limits.memory_mib, 4096)

    async def test_create_runtime_rejects_memory_max_below_initial_memory(
        self,
    ) -> None:
        http = self._http(lambda _request: None)

        with self.assertRaisesRegex(ValueError, "memory_max_mib"):
            await http.create_runtime(memory_mib=2048, memory_max_mib=1024)

    async def test_create_lost_response_reuses_key_and_body(self) -> None:
        seen: list[tuple[str, dict[str, Any]]] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            seen.append((request.headers["idempotency-key"], _json(request)))
            if len(seen) == 1:
                raise httpx.ReadError("response lost", request=request)
            return _json_response({"data": _runtime_json()}, status_code=201)

        http = self._http(handler)
        with patch("runta._internal.retry.random.uniform", return_value=0):
            info = await http.create_runtime("created")
        self.assertEqual(info.id, "sb-1")
        self.assertEqual(len(seen), 2)
        self.assertEqual(seen[0], seen[1])

    async def test_patch_lost_response_checks_egress_after_conflict(self) -> None:
        policy = {"mode": "allowlist", "allowed_hosts": ["example.com"]}
        patches: list[tuple[str, dict[str, Any]]] = []
        revision = 1

        async def handler(request: httpx.Request) -> httpx.Response:
            nonlocal revision
            if request.method == "GET":
                current = _runtime_json(egress_policy=policy if revision == 2 else None)
                current["revision"] = revision
                return _json_response({"data": current})
            patches.append((request.url.params["expected_revision"], _json(request)))
            if len(patches) == 1:
                revision = 2
                raise httpx.ReadError("response lost", request=request)
            return _json_response(
                {
                    "error": {
                        "code": "failed_precondition",
                        "message": "runtime revision conflict: expected 1, current 2",
                    },
                    "request_id": "request-1",
                },
                status_code=409,
            )

        http = self._http(handler)
        with patch("runta._internal.retry.random.uniform", return_value=0):
            info = await http.patch_runtime(
                "sb-1",
                egress_policy=EgressPolicy(
                    mode=EgressMode.ALLOWLIST, allowed_hosts=["example.com"]
                ),
            )
        self.assertEqual(info.egress_policy.allowed_hosts, ["example.com"])
        self.assertEqual(patches[0], patches[1])

    async def test_patch_retries_initial_metadata_get(self) -> None:
        gets = 0
        patches: list[str] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            nonlocal gets
            if request.method == "GET":
                gets += 1
                if gets == 1:
                    return httpx.Response(503, text="temporarily unavailable")
                return _json_response({"data": _runtime_json()})
            patches.append(request.url.params["expected_revision"])
            return _json_response({"data": _runtime_json(memory_mib=2048)})

        http = self._http(handler)
        with patch("runta._internal.retry.random.uniform", return_value=0):
            info = await http.patch_runtime(
                "sb-1",
                resources=PatchRuntimeResources(
                    requests=PatchRuntimeResourceRequests(memory_mib=2048)
                ),
            )
        self.assertEqual(info.resources.requests.memory_mib, 2048)
        self.assertEqual(gets, 2)
        self.assertEqual(patches, ["1"])

    async def test_patch_conflict_with_different_state_does_not_overwrite(self) -> None:
        patches: list[str] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            if request.method == "GET":
                current = _runtime_json()
                current["revision"] = 2 if patches else 1
                return _json_response({"data": current})
            patches.append(request.url.params["expected_revision"])
            return _json_response(
                {
                    "error": {
                        "code": "failed_precondition",
                        "message": "runtime revision conflict: expected 1, current 2",
                    },
                    "request_id": "request-1",
                },
                status_code=409,
            )

        http = self._http(handler)
        with self.assertRaisesRegex(ApiError, "revision conflict"):
            await http.patch_runtime(
                "sb-1",
                resources=PatchRuntimeResources(
                    requests=PatchRuntimeResourceRequests(memory_mib=2048)
                ),
            )
        self.assertEqual(patches, ["1"])

    async def test_restore_runtime_uses_checkpoint_request_without_resources(
        self,
    ) -> None:
        seen: dict[str, Any] = {}

        async def handler(request: httpx.Request) -> httpx.Response:
            seen["json"] = _json(request)
            return _json_response({"data": _runtime_json()}, status_code=201)

        http = self._http(handler)
        await http.create_runtime(
            "restored",
            checkpoint_id="checkpoint-1",
            vcpus=8,
            memory_mib=8192,
            memory_max_mib=16384,
        )

        self.assertEqual(seen["json"]["checkpoint_id"], "checkpoint-1")
        self.assertNotIn("resources", seen["json"])

    async def test_public_restore_preserves_explicit_resources(self) -> None:
        for resources, expected in _restore_resource_cases():
            with self.subTest(resources=resources):
                bodies: list[dict[str, Any]] = []

                async def handler(request: httpx.Request) -> httpx.Response:
                    self.assertEqual(request.method, "POST")
                    self.assertEqual(request.url.path, "/v2/runtimes")
                    bodies.append(_json(request))
                    return _json_response({"data": _runtime_json()}, status_code=201)

                async with AsyncRunta(
                    endpoint="http://runta.test", token="rt_test"
                ) as client:
                    set_handler(client._http, handler)
                    runtime = await client.runtimes.create(
                        checkpoint_id="checkpoint-1", resources=resources, wait=False
                    )
                    self.assertEqual(runtime.id, "sb-1")
                self.assertEqual(len(bodies), 1)
                self.assertEqual(bodies[0]["checkpoint_id"], "checkpoint-1")
                if expected is None:
                    self.assertNotIn("resources", bodies[0])
                else:
                    self.assertEqual(bodies[0]["resources"], expected)

    async def test_create_runtime_accepts_advanced_resources_shape(self) -> None:
        seen: dict[str, Any] = {}

        async def handler(request: httpx.Request) -> httpx.Response:
            seen["json"] = _json(request)
            body = seen["json"]
            return _json_response(
                {
                    "data": _runtime_json(
                        vcpus=body["resources"]["requests"]["vcpus"],
                        memory_mib=body["resources"]["requests"]["memory_mib"],
                        limit_memory_mib=body["resources"]["limits"]["memory_mib"],
                    )
                },
                status_code=201,
            )

        http = self._http(handler)
        info = await http.create_runtime(
            "sb-advanced",
            vcpus=99,
            memory_mib=99,
            resources=CreateRuntimeResources(
                requests=CreateRuntimeResourceRequests(memory_mib=3072, vcpus=4),
                limits=RuntimeResourceLimits(memory_mib=6144),
            ),
        )

        self.assertEqual(
            seen["json"]["resources"],
            {
                "limits": {"memory_mib": 6144},
                "requests": {"memory_mib": 3072, "vcpus": 4},
            },
        )
        self.assertEqual(info.resources.requests.vcpus, 4)
        self.assertEqual(info.resources.requests.memory_mib, 3072)
        self.assertEqual(info.resources.limits.memory_mib, 6144)

    async def test_patch_runtime_maps_resources_to_nested_resources(self) -> None:
        bodies: list[dict[str, Any]] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            if request.method == "GET":
                return _json_response({"data": _runtime_json()})
            self.assertEqual(request.method, "PATCH")
            self.assertEqual(request.url.path, "/v2/runtimes/sb-1")
            self.assertEqual(request.url.params["expected_revision"], "1")
            body = _json(request)
            bodies.append(body)
            requests = body["resources"].get("requests", {"memory_mib": 1024})
            limits = body["resources"].get("limits", {"memory_mib": 4096})
            return _json_response(
                {
                    "data": _runtime_json(
                        memory_mib=requests["memory_mib"],
                        limit_memory_mib=limits["memory_mib"],
                    )
                }
            )

        http = self._http(handler)
        await http.patch_runtime(
            "sb-1",
            resources=PatchRuntimeResources(
                requests=PatchRuntimeResourceRequests(memory_mib=2048),
                limits=RuntimeResourceLimits(memory_mib=4096),
            ),
        )

        self.assertEqual(
            bodies,
            [
                {
                    "resources": {
                        "limits": {"memory_mib": 4096},
                        "requests": {"memory_mib": 2048},
                    }
                }
            ],
        )

    async def test_patch_runtime_sends_new_egress_policy_shape(self) -> None:
        bodies: list[dict[str, Any]] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            if request.method == "GET":
                return _json_response({"data": _runtime_json()})
            self.assertEqual(request.method, "PATCH")
            self.assertEqual(request.url.path, "/v2/runtimes/sb-1")
            self.assertEqual(request.url.params["expected_revision"], "1")
            body = _json(request)
            bodies.append(body)
            return _json_response(
                {"data": _runtime_json(egress_policy=body["egress_policy"])}
            )

        http = self._http(handler)
        info = await http.patch_runtime(
            "sb-1",
            egress_policy=EgressPolicy(
                mode=EgressMode.DENYLIST,
                allowed_hosts=["api.example.com"],
                denied_hosts=["ads.example.com"],
            ),
        )

        self.assertEqual(info.egress_policy.mode, EgressMode.DENYLIST)
        self.assertEqual(
            bodies,
            [
                {
                    "egress_policy": {
                        "denied_hosts": ["ads.example.com"],
                        "mode": "denylist",
                    }
                }
            ],
        )

    async def test_runtime_mutations_fetch_and_send_current_revision(self) -> None:
        mutations: list[tuple[str, str, str | None]] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            if request.method == "GET":
                return _json_response({"data": _runtime_json()})
            mutations.append(
                (
                    request.method,
                    request.url.path,
                    request.url.params.get("expected_revision"),
                )
            )
            if request.method == "DELETE":
                return httpx.Response(204)
            return _json_response({"data": _runtime_json()})

        http = self._http(handler)
        await http.update_runtime_status("sb-1", "pause")
        await http.delete_runtime("sb-1")

        self.assertEqual(
            mutations,
            [
                ("POST", "/v2/runtimes/sb-1/pause", "1"),
                ("DELETE", "/v2/runtimes/sb-1", "1"),
            ],
        )

    async def test_files_secrets_and_checkpoints_use_generated_routes(
        self,
    ) -> None:
        calls: list[tuple[str, str, dict[str, str], Any]] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            body = (
                _json(request)
                if request.headers.get("content-type") == "application/json"
                else request.content
            )
            calls.append(
                (request.method, request.url.path, dict(request.url.params), body)
            )
            path = request.url.path
            if request.method == "GET" and path == "/v2/runtimes/sb-1/files":
                return httpx.Response(
                    200,
                    content=b"file-bytes",
                    headers={"content-type": "application/octet-stream"},
                )
            if request.method == "PUT" and path == "/v2/runtimes/sb-1/files":
                return httpx.Response(204)
            if request.method == "PUT" and path == "/v2/secrets/secret":
                return _json_response({"data": _secret_json()})
            if request.method == "GET" and path == "/v2/secrets":
                return _json_response({"data": [_secret_json()]})
            if request.method == "GET" and path == "/v2/secrets/secret-1":
                return _json_response({"data": _secret_json()})
            if request.method == "POST" and path == "/v2/runtimes/sb-1/checkpoints":
                return _json_response({"data": _checkpoint_json()})
            if request.method == "GET" and path == "/v2/checkpoints":
                return _json_response(
                    {
                        "data": [_checkpoint_json()],
                        "pagination": {"next_cursor": None, "has_more": False},
                    }
                )
            raise AssertionError(f"unexpected request: {request.method} {request.url}")

        http = self._http(handler)
        content = await http.read_file("sb-1", "/tmp/in.txt")
        await http.write_file("sb-1", "/tmp/out.txt", b"out")
        await http.set_secret("secret", "value")
        await http.list_secrets()
        await http.get_secret("secret-1")
        await http.create_checkpoint("sb-1", "checkpoint-name")
        await http.list_checkpoints()

        self.assertEqual(content, b"file-bytes")
        self.assertEqual(
            calls[0],
            ("GET", "/v2/runtimes/sb-1/files", {"path": "/tmp/in.txt"}, b""),
        )
        self.assertEqual(
            calls[1],
            ("PUT", "/v2/runtimes/sb-1/files", {"path": "/tmp/out.txt"}, b"out"),
        )
        self.assertEqual(calls[2][3], {"cache_ttl_secs": 0, "value": "value"})
        self.assertEqual(calls[5][0:2], ("POST", "/v2/runtimes/sb-1/checkpoints"))
        self.assertEqual(calls[6][2], {"limit": "100"})

    async def test_error_envelope_converts_to_api_error(self) -> None:
        async def handler(request: httpx.Request) -> httpx.Response:
            return _json_response(
                {
                    "error": {"code": "not_found", "message": "missing runtime"},
                    "request_id": "request-1",
                },
                status_code=404,
            )

        http = self._http(handler)

        with self.assertRaises(ApiError) as ctx:
            await http.get_runtime("missing")

        self.assertEqual(ctx.exception.status_code, 404)
        self.assertEqual(ctx.exception.code, "not_found")
        self.assertIn("missing runtime", str(ctx.exception))

    async def test_non_json_error_body_converts_to_api_error(self) -> None:
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                503,
                text="<html>maintenance</html>",
                headers={"content-type": "text/html"},
            )

        http = self._http(handler)
        http.retry_max_attempts = 1

        with self.assertRaises(ApiError) as ctx:
            await http.get_runtime("sb-1")

        self.assertEqual(ctx.exception.status_code, 503)
        self.assertIn("maintenance", str(ctx.exception))


class SyncOpenApiTransportTests(unittest.TestCase):
    def test_public_restore_preserves_explicit_resources(self) -> None:
        for resources, expected in _restore_resource_cases():
            with self.subTest(resources=resources):
                bodies: list[dict[str, Any]] = []

                def handler(request: httpx.Request) -> httpx.Response:
                    self.assertEqual(request.method, "POST")
                    self.assertEqual(request.url.path, "/v2/runtimes")
                    bodies.append(_json(request))
                    return _json_response({"data": _runtime_json()}, status_code=201)

                with Runta(endpoint="http://runta.test", token="rt_test") as client:
                    set_handler(client._http, handler)
                    runtime = client.runtimes.create(
                        checkpoint_id="checkpoint-1", resources=resources, wait=False
                    )
                    self.assertEqual(runtime.id, "sb-1")
                self.assertEqual(len(bodies), 1)
                self.assertEqual(bodies[0]["checkpoint_id"], "checkpoint-1")
                if expected is None:
                    self.assertNotIn("resources", bodies[0])
                else:
                    self.assertEqual(bodies[0]["resources"], expected)

    def test_patch_retries_initial_metadata_get(self) -> None:
        gets = 0
        patches: list[str] = []

        def handler(request: httpx.Request) -> httpx.Response:
            nonlocal gets
            if request.method == "GET":
                gets += 1
                if gets == 1:
                    return httpx.Response(503, text="temporarily unavailable")
                return _json_response({"data": _runtime_json()})
            patches.append(request.url.params["expected_revision"])
            return _json_response({"data": _runtime_json(memory_mib=2048)})

        http = _SyncHttpClient("http://runta.test", "rt_test")
        http._client._httpx_args["transport"] = httpx.MockTransport(handler)
        try:
            with patch("runta._internal.retry.random.uniform", return_value=0):
                info = http.patch_runtime(
                    "sb-1",
                    resources=PatchRuntimeResources(
                        requests=PatchRuntimeResourceRequests(memory_mib=2048)
                    ),
                )
        finally:
            http.close()
        self.assertEqual(info.resources.requests.memory_mib, 2048)
        self.assertEqual(gets, 2)
        self.assertEqual(patches, ["1"])

    def test_create_lost_response_reuses_key_and_body(self) -> None:
        seen: list[tuple[str, dict[str, Any]]] = []

        def handler(request: httpx.Request) -> httpx.Response:
            seen.append((request.headers["idempotency-key"], _json(request)))
            if len(seen) == 1:
                raise httpx.ReadError("response lost", request=request)
            return _json_response({"data": _runtime_json()}, status_code=201)

        http = _SyncHttpClient("http://runta.test", "rt_test")
        http._client._httpx_args["transport"] = httpx.MockTransport(handler)
        try:
            with patch("runta._internal.retry.random.uniform", return_value=0):
                self.assertEqual(http.create_runtime("created").id, "sb-1")
        finally:
            http.close()
        self.assertEqual(len(seen), 2)
        self.assertEqual(seen[0], seen[1])

    def test_patch_lost_response_checks_resources_after_conflict(self) -> None:
        patches: list[tuple[str, dict[str, Any]]] = []

        def handler(request: httpx.Request) -> httpx.Response:
            if request.method == "GET":
                current = _runtime_json(memory_mib=2048 if patches else 1024)
                current["revision"] = 2 if patches else 1
                return _json_response({"data": current})
            patches.append((request.url.params["expected_revision"], _json(request)))
            if len(patches) == 1:
                raise httpx.ReadError("response lost", request=request)
            return _json_response(
                {
                    "error": {
                        "code": "failed_precondition",
                        "message": "runtime revision conflict: expected 1, current 2",
                    },
                    "request_id": "request-1",
                },
                status_code=409,
            )

        http = _SyncHttpClient("http://runta.test", "rt_test")
        http._client._httpx_args["transport"] = httpx.MockTransport(handler)
        try:
            with patch("runta._internal.retry.random.uniform", return_value=0):
                info = http.patch_runtime(
                    "sb-1",
                    resources=PatchRuntimeResources(
                        requests=PatchRuntimeResourceRequests(memory_mib=2048)
                    ),
                )
        finally:
            http.close()
        self.assertEqual(info.resources.requests.memory_mib, 2048)
        self.assertEqual(patches[0], patches[1])

    def test_non_json_error_body_converts_to_api_error(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                503,
                text="proxy unavailable",
                headers={"content-type": "text/plain"},
            )

        http = _SyncHttpClient(
            "http://runta.test", "rt_test", timeout=12, retry_max_attempts=1
        )
        http._client._httpx_args["transport"] = httpx.MockTransport(handler)
        try:
            with self.assertRaises(ApiError) as ctx:
                http.get_runtime("sb-1")
        finally:
            http.close()

        self.assertEqual(ctx.exception.status_code, 503)
        self.assertIn("proxy unavailable", str(ctx.exception))


def _json(request: httpx.Request) -> dict[str, Any]:
    return json.loads(request.content.decode())


def _json_response(data: dict[str, Any], *, status_code: int = 200) -> httpx.Response:
    return httpx.Response(status_code, json=data)


def _runtime_json(
    *,
    vcpus: int = 1,
    memory_mib: int = 1024,
    limit_memory_mib: int = 4096,
    ingress_specs: list[dict[str, Any]] | None = None,
    egress_policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "created_at": "2026-07-13T00:00:00Z",
        "can_manage": True,
        "degraded": False,
        "desired_status": "running",
        "display_name": "runtime",
        "environment_variables": {},
        "egress_policy": egress_policy or {"denied_hosts": [], "mode": "denylist"},
        "error_code": None,
        "id": "sb-1",
        "image_id": "default",
        "idle_policy": {"mode": "disabled"},
        "ingress_specs": ingress_specs or [],
        "llm_tool_io_capture_enabled": False,
        "llm_session_content_capture_enabled": False,
        "llm_token_saving_policy": {
            "git_diff_enabled": False,
            "json_array_enabled": False,
            "log_enabled": False,
            "search_results_enabled": False,
        },
        "resources": {
            "current": {"memory_mib": memory_mib, "observed_disk_gib": 16},
            "limits": {"memory_mib": limit_memory_mib},
            "requests": {"disk_gib": 16, "memory_mib": memory_mib, "vcpus": vcpus},
        },
        "owner_user_id": "user-1",
        "revision": 1,
        "secret_configuration": [],
        "ssh_enabled": False,
        "status": "running",
        "updated_at": "2026-07-13T00:01:00Z",
        "vnc_connection": {
            "hostname": "vnc.example.com",
            "port": 5900,
            "security_type": "X509Plain",
            "username": "runta",
        },
        "vnc_enabled": False,
        "vnc_error_code": None,
        "vnc_ready": False,
    }


def _secret_json() -> dict[str, Any]:
    return {"cache_ttl_secs": 0, "display_name": "secret", "id": "secret-1"}


def _checkpoint_json() -> dict[str, Any]:
    return {
        "created_at": "2026-07-13T00:00:00Z",
        "display_name": "checkpoint-name",
        "id": "checkpoint-1",
        "resources": {
            "current": {"memory_mib": 1024, "observed_disk_gib": 16},
            "limits": {"memory_mib": 4096},
            "requests": {"disk_gib": 16, "memory_mib": 1024, "vcpus": 1},
        },
        "state": "ready",
    }
