from datetime import datetime, timezone

import pytest

from novita_sandbox.core import AsyncSandbox, AsyncTemplate, Sandbox, Template, Volume
from novita_sandbox.core.compat import should_use_legacy, resolve_domain
from novita_sandbox.core.sandbox_async import sandbox_api as sandbox_async_api
from novita_sandbox.core.sandbox_async import paginator as sandbox_async_paginator
from novita_sandbox.core.sandbox_sync import sandbox_api as sandbox_sync_api
from novita_sandbox.core.sandbox_sync import paginator as sandbox_sync_paginator
from novita_sandbox.core.template_async import main as template_async_main
from novita_sandbox.core.template_sync import main as template_sync_main


def _template_info_json():
    return {
        "templateID": "template-id",
        "buildID": "build-id",
        "aliases": ["snapshot-alias"],
        "names": ["team/snapshot-alias"],
        "templateType": "snapshot_template",
        "buildCount": 1,
        "cpuCount": 2,
        "memoryMB": 1024,
        "diskSizeMB": 4096,
        "spawnCount": 0,
        "envdVersion": "0.5.7",
        "public": False,
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-01-01T00:00:00Z",
        "lastSpawnedAt": None,
        "createdBy": None,
    }


def _sandbox_create_json():
    return {
        "sandboxID": "sandbox-id",
        "domain": "sandbox-domain",
        "envdVersion": "0.5.7",
        "envdAccessToken": "envd-access-token",
        "trafficAccessToken": "traffic-access-token",
    }


def test_should_use_legacy_prefers_explicit_domain(monkeypatch):
    monkeypatch.setenv("NOVITA_DOMAIN", "sandbox.novita.ai")

    assert should_use_legacy({"domain": "us-phx-1.sandbox.novita.ai"}) is False


def test_should_use_legacy_uses_env_domain(monkeypatch):
    monkeypatch.setenv("NOVITA_DOMAIN", "sandbox.novita.ai")

    assert should_use_legacy({}) is True


def test_sandbox_metrics_converts_legacy_memory_mib_fields(monkeypatch):
    calls = []

    class Response:
        status_code = 200
        content = b""

        @staticmethod
        def json():
            return [
                {
                    "cpuCount": 2,
                    "cpuUsedPct": 12.5,
                    "memTotalMiB": 1024,
                    "memUsedMiB": 512,
                    "timestamp": "2026-01-01T00:00:00Z",
                    "timestampUnix": 1767225600,
                }
            ]

    class HttpxClient:
        @staticmethod
        def get(*args, **kwargs):
            calls.append((args, kwargs))
            return Response()

    class ApiClient:
        @staticmethod
        def get_httpx_client():
            return HttpxClient()

    monkeypatch.setattr(
        sandbox_sync_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    end = datetime(2026, 1, 1, 0, 1, tzinfo=timezone.utc)
    result = Sandbox._cls_get_metrics(
        "sandbox-id",
        start=start,
        end=end,
        api_key="test-api-key",
        domain="sandbox.novita.ai",
    )

    assert len(result) == 1
    assert result[0].mem_total == 1024 * 1024 * 1024
    assert result[0].mem_used == 512 * 1024 * 1024
    assert result[0].disk_total == -1
    assert result[0].disk_used == -1
    assert calls[0][1]["params"] == {
        "start": 1767225600000,
        "end": 1767225660000,
    }


def test_sandbox_pause_legacy_accepts_sync(monkeypatch):
    calls = []

    class Response:
        status_code = 200
        content = b""

    class HttpxClient:
        @staticmethod
        def post(*args, **kwargs):
            calls.append((args, kwargs))
            return Response()

    class ApiClient:
        @staticmethod
        def get_httpx_client():
            return HttpxClient()

    monkeypatch.setattr(
        sandbox_sync_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    result = Sandbox.beta_pause(
        "sandbox-id",
        sync=True,
        api_key="test-api-key",
        domain="sandbox.novita.ai",
    )

    assert result == "sandbox-id"
    assert calls == [(("/sandboxes/sandbox-id/pause",), {"json": {"sync": True}})]


def test_sandbox_commit_allows_modern_domain(monkeypatch):
    calls = []

    class Response:
        status_code = 200
        content = b""

        @staticmethod
        def json():
            return _template_info_json()

    class HttpxClient:
        @staticmethod
        def post(*args, **kwargs):
            calls.append((args, kwargs))
            return Response()

    class ApiClient:
        @staticmethod
        def get_httpx_client():
            return HttpxClient()

    monkeypatch.setattr(
        sandbox_sync_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    result = Sandbox.commit(
        "sandbox-id",
        alias="snapshot-alias",
        api_key="test-api-key",
        domain="us-phx-1.sandbox.novita.ai",
    )

    assert result.template_id == "template-id"
    assert calls == [
        (("/sandboxes/sandbox-id/commit",), {"json": {"alias": "snapshot-alias"}})
    ]


def test_sandbox_beta_create_legacy_auto_pause_false_omits_lifecycle(monkeypatch):
    calls = []

    class Response:
        status_code = 200
        content = b""

        @staticmethod
        def json():
            return _sandbox_create_json()

    class HttpxClient:
        @staticmethod
        def post(*args, **kwargs):
            calls.append((args, kwargs))
            return Response()

    class ApiClient:
        @staticmethod
        def get_httpx_client():
            return HttpxClient()

    monkeypatch.setattr(
        sandbox_sync_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    sandbox = Sandbox.beta_create(
        template="base",
        auto_pause=False,
        api_key="test-api-key",
        domain="sandbox.novita.ai",
    )

    assert sandbox.sandbox_id == "sandbox-id"
    assert calls[0] == (
        ("/sandboxes",),
        {
            "json": {
                "templateID": "base",
                "autoPause": False,
                "metadata": {},
                "timeout": 300,
                "envVars": {},
                "secure": False,
                "allowInternetAccess": True,
            }
        },
    )


def test_sandbox_create_legacy_explicit_secure_true_is_preserved(monkeypatch):
    calls = []

    class Response:
        status_code = 200
        content = b""

        @staticmethod
        def json():
            return _sandbox_create_json()

    class HttpxClient:
        @staticmethod
        def post(*args, **kwargs):
            calls.append((args, kwargs))
            return Response()

    class ApiClient:
        @staticmethod
        def get_httpx_client():
            return HttpxClient()

    monkeypatch.setattr(
        sandbox_sync_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    Sandbox.create(
        template="base",
        secure=True,
        api_key="test-api-key",
        domain="sandbox.novita.ai",
    )

    assert calls[0][1]["json"]["secure"] is True


def test_sandbox_create_modern_default_secure_true_is_preserved(monkeypatch):
    calls = []

    class ParsedSandbox:
        sandbox_id = "sandbox-id"
        domain = "sandbox-domain"
        envd_version = "0.5.7"
        envd_access_token = "envd-access-token"
        traffic_access_token = "traffic-access-token"

    class Response:
        status_code = 200
        parsed = ParsedSandbox()

    monkeypatch.setattr(
        sandbox_sync_api.post_sandboxes,
        "sync_detailed",
        lambda *args, **kwargs: calls.append((args, kwargs)) or Response(),
    )

    Sandbox.create(
        template="base",
        api_key="test-api-key",
        domain="us-phx-1.sandbox.novita.ai",
    )

    assert calls[0][1]["body"].secure is True


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"mcp": {"server": {"run_cmd": "server"}}}, "mcp"),
        ({"network": {"allow_out": ["1.1.1.1"]}}, "network"),
        ({"volume_mounts": {"/mnt": "volume-name"}}, "volume_mounts"),
    ],
)
def test_sandbox_create_raises_for_legacy_2026_only_options(kwargs, message):
    with pytest.raises(NotImplementedError, match=message):
        Sandbox.create(
            domain="sandbox.novita.ai",
            api_key="test-api-key",
            **kwargs,
        )


def test_sandbox_create_legacy_ignores_lifecycle(monkeypatch):
    calls = []

    class Response:
        status_code = 200
        content = b""

        @staticmethod
        def json():
            return _sandbox_create_json()

    class HttpxClient:
        @staticmethod
        def post(*args, **kwargs):
            calls.append((args, kwargs))
            return Response()

    class ApiClient:
        @staticmethod
        def get_httpx_client():
            return HttpxClient()

    monkeypatch.setattr(
        sandbox_sync_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    sandbox = Sandbox.create(
        template="base",
        lifecycle={"on_timeout": "pause", "auto_resume": True},
        domain="sandbox.novita.ai",
        api_key="test-api-key",
    )

    assert sandbox.sandbox_id == "sandbox-id"
    assert "lifecycle" not in calls[0][1]["json"]
    assert calls[0][1]["json"]["secure"] is False


@pytest.mark.parametrize(
    ("auto_pause", "lifecycle", "expected_lifecycle"),
    [
        (False, None, None),
        (True, None, {"on_timeout": "pause", "auto_resume": False}),
        (
            False,
            {"on_timeout": "pause", "auto_resume": True},
            {"on_timeout": "pause", "auto_resume": True},
        ),
        (
            True,
            {"on_timeout": "pause", "auto_resume": True},
            {"on_timeout": "pause", "auto_resume": True},
        ),
    ],
)
def test_sandbox_create_passes_beta_equivalent_lifecycle_to_create(
    monkeypatch,
    auto_pause,
    lifecycle,
    expected_lifecycle,
):
    calls = []

    def fake_create(cls, **kwargs):
        calls.append(kwargs)
        return object()

    monkeypatch.setattr(Sandbox, "_create", classmethod(fake_create))

    Sandbox.create(
        template="base",
        auto_pause=auto_pause,
        lifecycle=lifecycle,
        api_key="test-api-key",
    )

    assert calls[0]["lifecycle"] == expected_lifecycle


def test_sandbox_api_create_sandbox_legacy_allows_lifecycle(monkeypatch):
    calls = []

    class Response:
        status_code = 200
        content = b""

        @staticmethod
        def json():
            return _sandbox_create_json()

    class HttpxClient:
        @staticmethod
        def post(*args, **kwargs):
            calls.append((args, kwargs))
            return Response()

    class ApiClient:
        @staticmethod
        def get_httpx_client():
            return HttpxClient()

    monkeypatch.setattr(
        sandbox_sync_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    sandbox = sandbox_sync_api.SandboxApi._create_sandbox(
        template="base",
        timeout=300,
        auto_pause=True,
        allow_internet_access=True,
        metadata=None,
        env_vars=None,
        secure=False,
        lifecycle={"on_timeout": "pause", "auto_resume": True},
        domain="sandbox.novita.ai",
        api_key="test-api-key",
    )

    assert sandbox.sandbox_id == "sandbox-id"
    assert "lifecycle" not in calls[0][1]["json"]
    assert calls[0][1]["json"]["secure"] is False


def test_sandbox_create_snapshot_rejects_legacy_domain(monkeypatch):
    calls = []

    class HttpxClient:
        @staticmethod
        def post(*args, **kwargs):
            calls.append((args, kwargs))

    class ApiClient:
        @staticmethod
        def get_httpx_client():
            return HttpxClient()

    monkeypatch.setattr(
        sandbox_sync_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    with pytest.raises(
        NotImplementedError,
        match="Sandbox.create_snapshot is not supported on legacy domains",
    ):
        Sandbox.create_snapshot(
            "sandbox-id",
            domain="sandbox.novita.ai",
            api_key="test-api-key",
        )

    assert calls == []


def test_sandbox_list_legacy_uses_raw_parser(monkeypatch):
    calls = []

    class Response:
        status_code = 200
        content = b""
        headers = {"x-next-token": "next-page"}

        @staticmethod
        def json():
            return [
                {
                    "sandboxID": "sandbox-id",
                    "templateID": "base",
                    "alias": "base",
                    "metadata": {"k": "v"},
                    "startedAt": "2026-01-01T00:00:00Z",
                    "endAt": "2026-01-01T00:05:00Z",
                    "state": "running",
                    "cpuCount": 2,
                    "memoryMB": 1024,
                    "envdVersion": "0.5.7",
                }
            ]

    class HttpxClient:
        @staticmethod
        def request(**kwargs):
            calls.append(kwargs)
            return Response()

    class ApiClient:
        @staticmethod
        def get_httpx_client():
            return HttpxClient()

    monkeypatch.setattr(
        sandbox_sync_paginator,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    paginator = Sandbox.list(
        domain="sandbox.novita.ai",
        api_key="test-api-key",
        limit=10,
    )
    result = paginator.next_items()

    assert result[0].sandbox_id == "sandbox-id"
    assert result[0].metadata == {"k": "v"}
    assert paginator.next_token == "next-page"
    assert calls == [
        {
            "method": "get",
            "url": "/v2/sandboxes",
            "params": {"limit": 10},
        }
    ]


@pytest.mark.asyncio
async def test_async_sandbox_metrics_converts_legacy_memory_mib_fields(monkeypatch):
    calls = []

    class Response:
        status_code = 200
        content = b""

        @staticmethod
        def json():
            return [
                {
                    "cpuCount": 2,
                    "cpuUsedPct": 12.5,
                    "memTotalMiB": 1024,
                    "memUsedMiB": 512,
                    "timestamp": "2026-01-01T00:00:00Z",
                    "timestampUnix": 1767225600,
                }
            ]

    class AsyncHttpxClient:
        @staticmethod
        async def get(*args, **kwargs):
            calls.append((args, kwargs))
            return Response()

    class ApiClient:
        @staticmethod
        def get_async_httpx_client():
            return AsyncHttpxClient()

    monkeypatch.setattr(
        sandbox_async_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    end = datetime(2026, 1, 1, 0, 1, tzinfo=timezone.utc)
    result = await AsyncSandbox._cls_get_metrics(
        "sandbox-id",
        start=start,
        end=end,
        api_key="test-api-key",
        domain="sandbox.novita.ai",
    )

    assert len(result) == 1
    assert result[0].mem_total == 1024 * 1024 * 1024
    assert result[0].mem_used == 512 * 1024 * 1024
    assert result[0].disk_total == -1
    assert result[0].disk_used == -1
    assert calls[0][1]["params"] == {
        "start": 1767225600000,
        "end": 1767225660000,
    }


@pytest.mark.asyncio
async def test_async_sandbox_pause_legacy_accepts_sync(monkeypatch):
    calls = []

    class Response:
        status_code = 200
        content = b""

    class AsyncHttpxClient:
        @staticmethod
        async def post(*args, **kwargs):
            calls.append((args, kwargs))
            return Response()

    class ApiClient:
        @staticmethod
        def get_async_httpx_client():
            return AsyncHttpxClient()

    monkeypatch.setattr(
        sandbox_async_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    result = await AsyncSandbox.beta_pause(
        "sandbox-id",
        sync=True,
        api_key="test-api-key",
        domain="sandbox.novita.ai",
    )

    assert result == "sandbox-id"
    assert calls == [(("/sandboxes/sandbox-id/pause",), {"json": {"sync": True}})]


@pytest.mark.asyncio
async def test_async_sandbox_commit_allows_modern_domain(monkeypatch):
    calls = []

    class Response:
        status_code = 200
        content = b""

        @staticmethod
        def json():
            return _template_info_json()

    class AsyncHttpxClient:
        @staticmethod
        async def post(*args, **kwargs):
            calls.append((args, kwargs))
            return Response()

    class ApiClient:
        @staticmethod
        def get_async_httpx_client():
            return AsyncHttpxClient()

    monkeypatch.setattr(
        sandbox_async_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    result = await AsyncSandbox.commit(
        "sandbox-id",
        alias="snapshot-alias",
        api_key="test-api-key",
        domain="us-phx-1.sandbox.novita.ai",
    )

    assert result.template_id == "template-id"
    assert calls == [
        (("/sandboxes/sandbox-id/commit",), {"json": {"alias": "snapshot-alias"}})
    ]


@pytest.mark.asyncio
async def test_async_sandbox_beta_create_legacy_auto_pause_false_omits_lifecycle(
    monkeypatch,
):
    calls = []

    class Response:
        status_code = 200
        content = b""

        @staticmethod
        def json():
            return _sandbox_create_json()

    class AsyncHttpxClient:
        @staticmethod
        async def post(*args, **kwargs):
            calls.append((args, kwargs))
            return Response()

    class ApiClient:
        @staticmethod
        def get_async_httpx_client():
            return AsyncHttpxClient()

    monkeypatch.setattr(
        sandbox_async_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    sandbox = await AsyncSandbox.beta_create(
        template="base",
        auto_pause=False,
        api_key="test-api-key",
        domain="sandbox.novita.ai",
    )

    assert sandbox.sandbox_id == "sandbox-id"
    assert calls[0] == (
        ("/sandboxes",),
        {
            "json": {
                "templateID": "base",
                "autoPause": False,
                "metadata": {},
                "timeout": 300,
                "envVars": {},
                "secure": False,
                "allowInternetAccess": True,
            }
        },
    )


@pytest.mark.asyncio
async def test_async_sandbox_create_legacy_explicit_secure_true_is_preserved(
    monkeypatch,
):
    calls = []

    class Response:
        status_code = 200
        content = b""

        @staticmethod
        def json():
            return _sandbox_create_json()

    class AsyncHttpxClient:
        @staticmethod
        async def post(*args, **kwargs):
            calls.append((args, kwargs))
            return Response()

    class ApiClient:
        @staticmethod
        def get_async_httpx_client():
            return AsyncHttpxClient()

    monkeypatch.setattr(
        sandbox_async_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    await AsyncSandbox.create(
        template="base",
        secure=True,
        api_key="test-api-key",
        domain="sandbox.novita.ai",
    )

    assert calls[0][1]["json"]["secure"] is True


@pytest.mark.asyncio
async def test_async_sandbox_create_modern_default_secure_true_is_preserved(
    monkeypatch,
):
    calls = []

    class ParsedSandbox:
        sandbox_id = "sandbox-id"
        domain = "sandbox-domain"
        envd_version = "0.5.7"
        envd_access_token = "envd-access-token"
        traffic_access_token = "traffic-access-token"

    class Response:
        status_code = 200
        parsed = ParsedSandbox()

    async def asyncio_detailed(*args, **kwargs):
        calls.append((args, kwargs))
        return Response()

    monkeypatch.setattr(
        sandbox_async_api.post_sandboxes,
        "asyncio_detailed",
        asyncio_detailed,
    )

    await AsyncSandbox.create(
        template="base",
        api_key="test-api-key",
        domain="us-phx-1.sandbox.novita.ai",
    )

    assert calls[0][1]["body"].secure is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"mcp": {"server": {"run_cmd": "server"}}}, "mcp"),
        ({"network": {"allow_out": ["1.1.1.1"]}}, "network"),
        ({"volume_mounts": {"/mnt": "volume-name"}}, "volume_mounts"),
    ],
)
async def test_async_sandbox_create_raises_for_legacy_2026_only_options(
    kwargs,
    message,
):
    with pytest.raises(NotImplementedError, match=message):
        await AsyncSandbox.create(
            domain="sandbox.novita.ai",
            api_key="test-api-key",
            **kwargs,
        )


@pytest.mark.asyncio
async def test_async_sandbox_create_legacy_ignores_lifecycle(monkeypatch):
    calls = []

    class Response:
        status_code = 200
        content = b""

        @staticmethod
        def json():
            return _sandbox_create_json()

    class AsyncHttpxClient:
        @staticmethod
        async def post(*args, **kwargs):
            calls.append((args, kwargs))
            return Response()

    class ApiClient:
        @staticmethod
        def get_async_httpx_client():
            return AsyncHttpxClient()

    monkeypatch.setattr(
        sandbox_async_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    sandbox = await AsyncSandbox.create(
        template="base",
        lifecycle={"on_timeout": "pause", "auto_resume": True},
        domain="sandbox.novita.ai",
        api_key="test-api-key",
    )

    assert sandbox.sandbox_id == "sandbox-id"
    assert "lifecycle" not in calls[0][1]["json"]


@pytest.mark.parametrize(
    ("auto_pause", "lifecycle", "expected_lifecycle"),
    [
        (False, None, None),
        (True, None, {"on_timeout": "pause", "auto_resume": False}),
        (
            False,
            {"on_timeout": "pause", "auto_resume": True},
            {"on_timeout": "pause", "auto_resume": True},
        ),
        (
            True,
            {"on_timeout": "pause", "auto_resume": True},
            {"on_timeout": "pause", "auto_resume": True},
        ),
    ],
)
@pytest.mark.asyncio
async def test_async_sandbox_create_passes_beta_equivalent_lifecycle_to_create(
    monkeypatch,
    auto_pause,
    lifecycle,
    expected_lifecycle,
):
    calls = []

    async def fake_create(cls, **kwargs):
        calls.append(kwargs)
        return object()

    monkeypatch.setattr(AsyncSandbox, "_create", classmethod(fake_create))

    await AsyncSandbox.create(
        template="base",
        auto_pause=auto_pause,
        lifecycle=lifecycle,
        api_key="test-api-key",
    )

    assert calls[0]["lifecycle"] == expected_lifecycle


@pytest.mark.asyncio
async def test_async_sandbox_api_create_sandbox_legacy_allows_lifecycle(monkeypatch):
    calls = []

    class Response:
        status_code = 200
        content = b""

        @staticmethod
        def json():
            return _sandbox_create_json()

    class AsyncHttpxClient:
        @staticmethod
        async def post(*args, **kwargs):
            calls.append((args, kwargs))
            return Response()

    class ApiClient:
        @staticmethod
        def get_async_httpx_client():
            return AsyncHttpxClient()

    monkeypatch.setattr(
        sandbox_async_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    sandbox = await sandbox_async_api.SandboxApi._create_sandbox(
        template="base",
        timeout=300,
        auto_pause=True,
        allow_internet_access=True,
        metadata=None,
        env_vars=None,
        secure=False,
        lifecycle={"on_timeout": "pause", "auto_resume": True},
        domain="sandbox.novita.ai",
        api_key="test-api-key",
    )

    assert sandbox.sandbox_id == "sandbox-id"
    assert "lifecycle" not in calls[0][1]["json"]


@pytest.mark.asyncio
async def test_async_sandbox_create_snapshot_rejects_legacy_domain(monkeypatch):
    calls = []

    class AsyncHttpxClient:
        @staticmethod
        async def post(*args, **kwargs):
            calls.append((args, kwargs))

    class ApiClient:
        @staticmethod
        def get_async_httpx_client():
            return AsyncHttpxClient()

    monkeypatch.setattr(
        sandbox_async_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    with pytest.raises(
        NotImplementedError,
        match="AsyncSandbox.create_snapshot is not supported on legacy domains",
    ):
        await AsyncSandbox.create_snapshot(
            "sandbox-id",
            domain="sandbox.novita.ai",
            api_key="test-api-key",
        )

    assert calls == []


@pytest.mark.asyncio
async def test_async_sandbox_list_legacy_uses_raw_parser(monkeypatch):
    calls = []

    class Response:
        status_code = 200
        content = b""
        headers = {"x-next-token": "next-page"}

        @staticmethod
        def json():
            return [
                {
                    "sandboxID": "sandbox-id",
                    "templateID": "base",
                    "alias": "base",
                    "metadata": {"k": "v"},
                    "startedAt": "2026-01-01T00:00:00Z",
                    "endAt": "2026-01-01T00:05:00Z",
                    "state": "running",
                    "cpuCount": 2,
                    "memoryMB": 1024,
                    "envdVersion": "0.5.7",
                }
            ]

    class AsyncHttpxClient:
        @staticmethod
        async def request(**kwargs):
            calls.append(kwargs)
            return Response()

    class ApiClient:
        @staticmethod
        def get_async_httpx_client():
            return AsyncHttpxClient()

    monkeypatch.setattr(
        sandbox_async_paginator,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    paginator = AsyncSandbox.list(
        domain="sandbox.novita.ai",
        api_key="test-api-key",
        limit=10,
    )
    result = await paginator.next_items()

    assert result[0].sandbox_id == "sandbox-id"
    assert result[0].metadata == {"k": "v"}
    assert paginator.next_token == "next-page"
    assert calls == [
        {
            "method": "get",
            "url": "/v2/sandboxes",
            "params": {"limit": 10},
        }
    ]


def test_template_list_allows_missing_build_status(monkeypatch):
    class Response:
        status_code = 200
        content = b""

        @staticmethod
        def json():
            return {
                "templates": [
                    {
                        "templateID": "template-id",
                        "buildID": "build-id",
                        "aliases": [],
                        "names": [],
                        "buildCount": 1,
                        "cpuCount": 2,
                        "memoryMB": 1024,
                        "diskSizeMB": 4096,
                        "spawnCount": 0,
                        "envdVersion": "0.5.7",
                        "public": False,
                        "metadata": {},
                        "createdAt": "2026-01-01T00:00:00Z",
                        "updatedAt": "2026-01-01T00:00:00Z",
                        "lastSpawnedAt": None,
                        "createdBy": None,
                    }
                ],
                "total": 1,
                "page": 1,
                "limit": 20,
                "totalPages": 1,
            }

    class HttpxClient:
        @staticmethod
        def request(**kwargs):
            return Response()

    class ApiClient:
        @staticmethod
        def get_httpx_client():
            return HttpxClient()

    monkeypatch.setattr(
        template_sync_main,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    result = Template.list(api_key="test-api-key")

    assert result.total == 1
    assert result.items[0].template_id == "template-id"
    assert result.items[0].build_status is None


@pytest.mark.asyncio
async def test_async_template_list_allows_missing_build_status(monkeypatch):
    class Response:
        status_code = 200
        content = b""

        @staticmethod
        def json():
            return {
                "templates": [
                    {
                        "templateID": "template-id",
                        "buildID": "build-id",
                        "aliases": [],
                        "names": [],
                        "buildCount": 1,
                        "cpuCount": 2,
                        "memoryMB": 1024,
                        "diskSizeMB": 4096,
                        "spawnCount": 0,
                        "envdVersion": "0.5.7",
                        "public": False,
                        "metadata": {},
                        "createdAt": "2026-01-01T00:00:00Z",
                        "updatedAt": "2026-01-01T00:00:00Z",
                        "lastSpawnedAt": None,
                        "createdBy": None,
                    }
                ],
                "total": 1,
                "page": 1,
                "limit": 20,
                "totalPages": 1,
            }

    class AsyncHttpxClient:
        @staticmethod
        async def request(**kwargs):
            return Response()

    class ApiClient:
        @staticmethod
        def get_async_httpx_client():
            return AsyncHttpxClient()

    monkeypatch.setattr(
        template_async_main,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    result = await AsyncTemplate.list(api_key="test-api-key")

    assert result.total == 1
    assert result.items[0].template_id == "template-id"
    assert result.items[0].build_status is None


# --- TemplateLegacy model tests ---


def test_template_legacy_from_dict_parses_camel_case_fields():
    data = {
        "templateID": "tmpl-123",
        "buildID": "bld-456",
        "aliases": ["my-template"],
        "buildCount": 3,
        "cpuCount": 2,
        "memoryMB": 1024,
        "diskSizeMB": 512,
        "spawnCount": 10,
        "envdVersion": "1.2.3",
        "public": True,
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-06-01T00:00:00Z",
        "lastSpawnedAt": "2024-05-15T12:00:00Z",
        "createdBy": {"id": "user-1", "email": "test@example.com"},
    }

    from novita_sandbox.core.api.client.models.template_legacy import TemplateLegacy

    result = TemplateLegacy.from_dict(data)

    assert result.template_id == "tmpl-123"
    assert result.build_id == "bld-456"
    assert result.aliases == ["my-template"]
    assert result.build_count == 3
    assert result.cpu_count == 2
    assert result.memory_mb == 1024
    assert result.disk_size_mb == 512
    assert result.spawn_count == 10
    assert result.envd_version == "1.2.3"
    assert result.public is True
    assert result.created_at is not None
    assert result.updated_at is not None
    assert result.last_spawned_at is not None


def test_template_legacy_from_dict_handles_null_last_spawned_at():
    data = {
        "templateID": "tmpl-123",
        "buildID": "bld-456",
        "aliases": ["my-template"],
        "buildCount": 3,
        "cpuCount": 2,
        "memoryMB": 1024,
        "diskSizeMB": 512,
        "spawnCount": 10,
        "envdVersion": "1.2.3",
        "public": True,
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-06-01T00:00:00Z",
        "lastSpawnedAt": None,
        "createdBy": None,
    }

    from novita_sandbox.core.api.client.models.template_legacy import TemplateLegacy

    result = TemplateLegacy.from_dict(data)

    assert result.last_spawned_at is None
    assert result.created_by is None


def test_template_legacy_from_dict_stores_unknown_fields_in_additional_properties():
    data = {
        "templateID": "tmpl-123",
        "buildID": "bld-456",
        "aliases": [],
        "buildCount": 0,
        "cpuCount": 1,
        "memoryMB": 512,
        "diskSizeMB": 256,
        "spawnCount": 0,
        "envdVersion": "1.0.0",
        "public": False,
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T00:00:00Z",
        "lastSpawnedAt": None,
        "createdBy": None,
        "customField": "custom-value",
    }

    from novita_sandbox.core.api.client.models.template_legacy import TemplateLegacy

    result = TemplateLegacy.from_dict(data)

    assert result.additional_properties.get("customField") == "custom-value"


def test_template_legacy_to_dict_roundtrip():
    data = {
        "templateID": "tmpl-123",
        "buildID": "bld-456",
        "aliases": ["my-template"],
        "buildCount": 3,
        "cpuCount": 2,
        "memoryMB": 1024,
        "diskSizeMB": 512,
        "spawnCount": 10,
        "envdVersion": "1.2.3",
        "public": True,
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-06-01T00:00:00Z",
        "lastSpawnedAt": "2024-05-15T12:00:00Z",
        "createdBy": {"id": "user-1", "email": "test@example.com"},
    }

    from novita_sandbox.core.api.client.models.template_legacy import TemplateLegacy

    obj = TemplateLegacy.from_dict(data)
    result = obj.to_dict()

    assert result["templateID"] == "tmpl-123"
    assert result["buildID"] == "bld-456"
    assert result["aliases"] == ["my-template"]


# --- connect legacy composite id tests ---


def _sandbox_connect_json():
    return {
        "sandboxID": "sandbox-id",
        "clientID": "client-id",
        "domain": "sandbox-domain",
        "envdVersion": "0.5.7",
        "envdAccessToken": "envd-access-token",
    }


def test_sandbox_connect_legacy_returns_composite_sandbox_id(monkeypatch):
    class Response:
        status_code = 200
        content = b""

        @staticmethod
        def json():
            return _sandbox_connect_json()

    class HttpxClient:
        @staticmethod
        def post(*args, **kwargs):
            return Response()

    class ApiClient:
        @staticmethod
        def get_httpx_client():
            return HttpxClient()

    monkeypatch.setattr(
        sandbox_sync_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    sandbox = Sandbox.connect(
        "sandbox-id-client-id",
        domain="sandbox.novita.ai",
        api_key="test-api-key",
    )

    assert sandbox.sandbox_id == "sandbox-id-client-id"


def test_sandbox_connect_legacy_without_client_id_returns_raw_sandbox_id(monkeypatch):
    class Response:
        status_code = 200
        content = b""

        @staticmethod
        def json():
            return {
                "sandboxID": "sandbox-id",
                "clientID": "",
                "domain": "sandbox-domain",
                "envdVersion": "0.5.7",
                "envdAccessToken": "envd-access-token",
            }

    class HttpxClient:
        @staticmethod
        def post(*args, **kwargs):
            return Response()

    class ApiClient:
        @staticmethod
        def get_httpx_client():
            return HttpxClient()

    monkeypatch.setattr(
        sandbox_sync_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    sandbox = Sandbox.connect(
        "sandbox-id",
        domain="sandbox.novita.ai",
        api_key="test-api-key",
    )

    assert sandbox.sandbox_id == "sandbox-id"


@pytest.mark.asyncio
async def test_async_sandbox_connect_legacy_returns_composite_sandbox_id(monkeypatch):
    class Response:
        status_code = 200
        content = b""

        @staticmethod
        def json():
            return _sandbox_connect_json()

    class AsyncHttpxClient:
        @staticmethod
        async def post(*args, **kwargs):
            return Response()

    class ApiClient:
        @staticmethod
        def get_async_httpx_client():
            return AsyncHttpxClient()

    monkeypatch.setattr(
        sandbox_async_api,
        "get_api_client",
        lambda *args, **kwargs: ApiClient(),
    )

    sandbox = await AsyncSandbox.connect(
        "sandbox-id-client-id",
        domain="sandbox.novita.ai",
        api_key="test-api-key",
    )

    assert sandbox.sandbox_id == "sandbox-id-client-id"


# --- NotImplementedError on legacy domain tests ---


def test_sandbox_set_network_raises_on_legacy():
    with pytest.raises(NotImplementedError, match="set_network"):
        Sandbox.set_network("sandbox-id", domain="sandbox.novita.ai")


def test_sandbox_hotplug_memory_raises_on_legacy(monkeypatch):
    # hotplug_memory is instance-only, but its _cls_hotplug_memory should raise
    from novita_sandbox.core.sandbox_sync.sandbox_api import SandboxApi

    with pytest.raises(NotImplementedError, match="hotplug_memory"):
        SandboxApi._cls_hotplug_memory("sandbox-id", domain="sandbox.novita.ai")


def test_sandbox_mount_volume_raises_on_legacy():
    from novita_sandbox.core.sandbox_sync.sandbox_api import SandboxApi

    with pytest.raises(NotImplementedError, match="mount_volume"):
        SandboxApi._cls_mount_volume("sandbox-id", "vol", "/mnt", domain="sandbox.novita.ai")


def test_sandbox_unmount_volume_raises_on_legacy():
    from novita_sandbox.core.sandbox_sync.sandbox_api import SandboxApi

    with pytest.raises(NotImplementedError, match="unmount_volume"):
        SandboxApi._cls_unmount_volume("sandbox-id", "/mnt", domain="sandbox.novita.ai")


def test_sandbox_list_snapshots_raises_on_legacy():
    from novita_sandbox.core.sandbox_sync import main as sync_main

    with pytest.raises(NotImplementedError, match="list_snapshots"):
        sync_main.Sandbox._cls_list_snapshots("sandbox-id", domain="sandbox.novita.ai")


def test_template_build_raises_on_legacy():

    class FakeTemplate:
        _base_image = None
        _base_template = None
        _instructions = []
        _force = False
        _force_next_layer = False
        _file_context_path = "."
        _file_ignore_patterns = []
        _logs_refresh_frequency = 200
        _stack_traces = []

    with pytest.raises(NotImplementedError, match="build"):
        Template.build(FakeTemplate(), name="test:latest", domain="sandbox.novita.ai")


def test_template_exists_raises_on_legacy():
    with pytest.raises(NotImplementedError, match="exists"):
        Template.exists("my-template", domain="sandbox.novita.ai")


def test_template_assign_tags_raises_on_legacy():
    with pytest.raises(NotImplementedError, match="assign_tags"):
        Template.assign_tags("name:tag", "prod", domain="sandbox.novita.ai")


def test_volume_create_raises_on_legacy():
    with pytest.raises(NotImplementedError, match="Volume.create"):
        Volume.create("my-volume", domain="sandbox.novita.ai")


def test_volume_list_raises_on_legacy():
    with pytest.raises(NotImplementedError, match="Volume.list"):
        Volume.list(domain="sandbox.novita.ai")


def test_volume_get_info_raises_on_legacy():
    with pytest.raises(NotImplementedError, match="Volume.get_info"):
        Volume.get_info("volume-id", domain="sandbox.novita.ai")


def test_volume_destroy_raises_on_legacy():
    with pytest.raises(NotImplementedError, match="Volume.destroy"):
        Volume.destroy("volume-id", domain="sandbox.novita.ai")


def test_volume_update_quota_raises_on_legacy():
    with pytest.raises(NotImplementedError, match="Volume.update_quota"):
        Volume.update_quota("volume-id", domain="sandbox.novita.ai")


@pytest.mark.asyncio
async def test_async_sandbox_set_network_raises_on_legacy():
    with pytest.raises(NotImplementedError, match="set_network"):
        await AsyncSandbox.set_network("sandbox-id", domain="sandbox.novita.ai")


@pytest.mark.asyncio
async def test_async_template_build_raises_on_legacy():

    class FakeTemplate:
        _base_image = None
        _base_template = None
        _instructions = []
        _force = False
        _force_next_layer = False
        _file_context_path = "."
        _file_ignore_patterns = []
        _logs_refresh_frequency = 200
        _stack_traces = []

    with pytest.raises(NotImplementedError, match="build"):
        await AsyncTemplate.build(FakeTemplate(), name="test:latest", domain="sandbox.novita.ai")


@pytest.mark.asyncio
async def test_async_volume_create_raises_on_legacy():
    from novita_sandbox.core.volume.volume_async import AsyncVolume

    with pytest.raises(NotImplementedError, match="AsyncVolume.create"):
        await AsyncVolume.create("my-volume", domain="sandbox.novita.ai")


# --- resolve_domain tests ---


def test_resolve_domain_returns_default_when_no_env(monkeypatch):
    monkeypatch.delenv("NOVITA_DOMAIN", raising=False)

    result = resolve_domain()

    assert result == "us-phx-1.sandbox.novita.ai"


def test_resolve_domain_prefers_explicit_over_env(monkeypatch):
    monkeypatch.setenv("NOVITA_DOMAIN", "sandbox.novita.ai")

    result = resolve_domain(domain="custom.example.com")

    assert result == "custom.example.com"


def test_resolve_domain_uses_env_when_no_explicit(monkeypatch):
    monkeypatch.setenv("NOVITA_DOMAIN", "sandbox.novita.ai")

    result = resolve_domain()

    assert result == "sandbox.novita.ai"


def test_resolve_domain_returns_default_when_explicit_empty(monkeypatch):
    monkeypatch.setenv("NOVITA_DOMAIN", "sandbox.novita.ai")

    result = resolve_domain(domain="")

    assert result == "sandbox.novita.ai"
