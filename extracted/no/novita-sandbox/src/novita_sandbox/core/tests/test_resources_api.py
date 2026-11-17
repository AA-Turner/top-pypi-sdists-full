import json

from types import SimpleNamespace
from typing import Any, Dict

import pytest

from novita_sandbox.core.api.client.models import SandboxDetail
from novita_sandbox.core.connection_config import ConnectionConfig
from novita_sandbox.core.exceptions import (
    AuthenticationException,
    SandboxException,
    SandboxNotFoundException,
)
from novita_sandbox.core.sandbox.sandbox_api import (
    SandboxInfo,
    resize_result_from_api,
    resource_targets_to_api,
)
from novita_sandbox.core.sandbox_async.main import AsyncSandbox
from novita_sandbox.core.sandbox_async.sandbox_api import SandboxApi as AsyncApi
from novita_sandbox.core.sandbox_sync.main import Sandbox
from novita_sandbox.core.sandbox_sync.sandbox_api import SandboxApi as SyncApi

DOMAIN = "us-phx-1.sandbox.novita.ai"


class Response:
    status_code = 200

    def __init__(self, payload: Dict[str, Any], status_code: int = 200) -> None:
        self.payload = payload
        self.status_code = status_code
        self.content = json.dumps(payload)

    def json(self) -> Dict[str, Any]:
        return self.payload


def sync_client(handler):
    class Http:
        def post(self, path, json=None, timeout=None):
            return handler(path, json, timeout)

    class Client:
        def get_httpx_client(self):
            return Http()

    return Client()


def async_client(handler):
    class Http:
        async def post(self, path, json=None, timeout=None):
            return handler(path, json, timeout)

    class Client:
        def get_async_httpx_client(self):
            return Http()

    return Client()


def test_targets_convert_gib_to_mib():
    assert resource_targets_to_api({"cpu": 4, "memory_gib": 2, "disk_gib": 4}) == {
        "vcpu": 4,
        "memory_mb": 2048,
        "disk_size_mb": 4096,
    }
    # A template disk can be a non-integral number of GiB but a whole number
    # of MiB; the request still carries the exact MiB value.
    assert resource_targets_to_api({"disk_gib": 2669 / 1024}) == {"disk_size_mb": 2669}


def test_targets_reject_values_that_are_not_exact_mib():
    with pytest.raises(ValueError, match="exact number of MiB"):
        resource_targets_to_api({"memory_gib": 1.1})
    with pytest.raises(ValueError, match="positive"):
        resource_targets_to_api({"cpu": 0})
    with pytest.raises(ValueError, match="positive whole number"):
        resource_targets_to_api({"cpu": 1.5})
    with pytest.raises(ValueError, match="at least one"):
        resource_targets_to_api({})


def test_result_maps_memory_and_disk_to_gib_but_keeps_cpu_cores():
    result = resize_result_from_api(
        {
            "cpu": {
                "status": "applied",
                "requested": 4,
                "previous": 2,
                "current": 4,
                "code": 200,
            },
            "disk": {
                "status": "skipped",
                "requested": 2669,
                "previous": 2669,
                "current": 2669,
                "code": 200,
                "reason": "unchanged",
            },
        }
    )
    assert result["cpu"]["current"] == 4
    assert result["disk"]["current"] == pytest.approx(2669 / 1024)
    assert result["cpu"]["unit"] == "cores"
    assert result["disk"]["unit"] == "GiB"
    assert result["disk"]["reason"] == "unchanged"
    assert "memory" not in result


def test_sync_resize_posts_mib_and_returns_gib(monkeypatch):
    sent: Dict[str, Any] = {}

    def handler(path, body, timeout):
        sent.update(path=path, body=body)
        return Response(
            {
                "cpu": {
                    "status": "applied",
                    "requested": 4,
                    "previous": 2,
                    "current": 4,
                    "code": 200,
                },
                "memory": {
                    "status": "applied",
                    "requested": 2048,
                    "previous": 1024,
                    "current": 2048,
                    "code": 200,
                },
            }
        )

    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        lambda config: sync_client(handler),
    )
    result = SyncApi._cls_resize("sbx", cpu=4, memory_gib=2, disk_gib=4, domain=DOMAIN)
    assert sent["path"] == "/sandboxes/sbx/resize"
    assert sent["body"] == {"vcpu": 4, "memory_mb": 2048, "disk_size_mb": 4096}
    assert result["cpu"]["current"] == 4
    assert result["memory"]["current"] == 2


@pytest.mark.asyncio
async def test_async_resize_posts_mib_and_returns_gib(monkeypatch):
    sent: Dict[str, Any] = {}

    def handler(path, body, timeout):
        sent.update(path=path, body=body)
        return Response(
            {
                "disk": {
                    "status": "applied",
                    "requested": 4096,
                    "previous": 2669,
                    "current": 4096,
                    "code": 200,
                }
            }
        )

    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_async.sandbox_api.get_api_client",
        lambda config: async_client(handler),
    )
    result = await AsyncApi._cls_resize("sbx", disk_gib=4, domain=DOMAIN)
    assert sent["body"] == {"disk_size_mb": 4096}
    assert result["disk"]["current"] == 4
    assert result["disk"]["previous"] == pytest.approx(2669 / 1024)


def test_sync_resize_reports_partial_success_without_raising(monkeypatch):
    def handler(path, body, timeout):
        return Response(
            {
                "cpu": {
                    "status": "applied",
                    "requested": 6,
                    "previous": 4,
                    "current": 6,
                    "code": 200,
                },
                "memory": {
                    "status": "failed",
                    "requested": 9217,
                    "previous": 1024,
                    "current": 1024,
                    "code": 400,
                    "reason": "exceeds_sandbox_limit",
                    "message": "requested 9217 MiB memory exceeds the maximum",
                },
            },
            status_code=207,
        )

    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        lambda config: sync_client(handler),
    )
    result = SyncApi._cls_resize("sbx", cpu=6, memory_gib=9217 / 1024, domain=DOMAIN)
    assert result["cpu"]["status"] == "applied"
    assert result["memory"]["status"] == "failed"
    assert result["memory"]["code"] == 400
    assert result["memory"]["reason"] == "exceeds_sandbox_limit"
    assert result["memory"]["current"] == 1


@pytest.mark.parametrize(
    "reason",
    [
        "invalid_value",
        "decrease_not_supported",
        "exceeds_sandbox_limit",
        "record_pending",
    ],
)
def test_resize_result_keeps_failure_reason(reason):
    result = resize_result_from_api(
        {
            "memory": {
                "status": "failed",
                "requested": 1024,
                "previous": 2048,
                "current": 2048,
                "code": 400,
                "reason": reason,
            }
        }
    )
    assert result["memory"]["reason"] == reason
    assert result["memory"]["current"] == 2


def test_resize_keeps_an_unconfirmed_resource_visible():
    result = resize_result_from_api(
        {
            "memory": {
                "status": "unknown",
                "requested": 2048,
                "previous": 2048,
                "current": 2048,
                "code": 207,
                "reason": "record_pending",
            }
        }
    )
    assert result["memory"]["status"] == "unknown"
    assert result["memory"]["reason"] == "record_pending"
    assert result["memory"]["current"] == 2


def test_resize_rejects_empty_and_invalid_targets_before_http(monkeypatch):
    called: list[Any] = []
    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        lambda config: called.append(config),
    )
    with pytest.raises(ValueError, match="at least one"):
        SyncApi._cls_resize("sbx", domain=DOMAIN)
    with pytest.raises(ValueError, match="positive"):
        SyncApi._cls_resize("sbx", memory_gib=0, domain=DOMAIN)
    with pytest.raises(ValueError, match="exact number of MiB"):
        SyncApi._cls_resize("sbx", memory_gib=1.1, domain=DOMAIN)
    assert called == []


def _resize_target() -> SimpleNamespace:
    return SimpleNamespace(
        sandbox_id="sbx",
        connection_config=ConnectionConfig(domain=DOMAIN),
    )


def test_sync_resize_rejects_removed_resource_alias_before_http(monkeypatch):
    called: list[Any] = []
    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        lambda config: called.append(config),
    )
    with pytest.raises(TypeError, match="memory_mib"):
        Sandbox.resize(_resize_target(), cpu=4, memory_mib=2048)
    assert called == []


@pytest.mark.asyncio
async def test_async_resize_rejects_removed_resource_alias_before_http(monkeypatch):
    called: list[Any] = []
    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_async.sandbox_api.get_api_client",
        lambda config: called.append(config),
    )
    with pytest.raises(TypeError, match="memory_mib"):
        await AsyncSandbox.resize(_resize_target(), cpu=4, memory_mib=2048)
    assert called == []


def test_resize_maps_not_found(monkeypatch):
    def handler(path, body, timeout):
        return Response({"code": 404, "message": "sandbox not found"}, status_code=404)

    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        lambda config: sync_client(handler),
    )
    with pytest.raises(SandboxNotFoundException):
        SyncApi._cls_resize("sbx", cpu=2, domain=DOMAIN)


def test_resize_maps_unauthorized(monkeypatch):
    def handler(path, body, timeout):
        return Response({"code": 401, "message": "unauthorized"}, status_code=401)

    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        lambda config: sync_client(handler),
    )
    with pytest.raises(AuthenticationException):
        SyncApi._cls_resize("sbx", cpu=2, domain=DOMAIN)


def test_resize_maps_conflict(monkeypatch):
    def handler(path, body, timeout):
        return Response(
            {"code": 409, "message": "another resize is in progress"},
            status_code=409,
        )

    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        lambda config: sync_client(handler),
    )
    with pytest.raises(SandboxException, match="409"):
        SyncApi._cls_resize("sbx", cpu=2, domain=DOMAIN)


def test_create_posts_to_custom_endpoint_with_mib(monkeypatch):
    sent: Dict[str, Any] = {}

    def handler(path, body, timeout):
        sent.update(path=path, body=body, timeout=timeout)
        return Response(
            {
                "sandboxID": "sbx",
                "templateID": "base",
                "envdVersion": "0.5.14",
                "resources": {"vcpu": 8, "memory_mb": 1024, "disk_size_mb": 4096},
            },
            status_code=201,
        )

    def fail_post(*args, **kwargs):
        raise AssertionError("custom creation must not use POST /sandboxes")

    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        lambda config: sync_client(handler),
    )
    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.post_sandboxes.sync_detailed",
        fail_post,
    )

    created = SyncApi._create_sandbox(
        template="base",
        timeout=300,
        auto_pause=None,
        allow_internet_access=True,
        metadata=None,
        env_vars=None,
        secure=True,
        resources={"cpu": 8, "disk_gib": 4},
        domain=DOMAIN,
    )
    assert created.sandbox_id == "sbx"
    assert sent["path"] == "/sandboxes/custom"
    assert sent["body"]["resources"] == {"vcpu": 8, "disk_size_mb": 4096}
    assert sent["timeout"] is not None and sent["timeout"] >= 360


def test_create_defaults_to_the_six_minute_timeout(monkeypatch):
    sent: Dict[str, Any] = {}

    def handler(path, body, timeout):
        sent["timeout"] = timeout
        return Response({"sandboxID": "sbx", "envdVersion": "0.5.14"}, status_code=201)

    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        lambda config: sync_client(handler),
    )
    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.post_sandboxes.sync_detailed",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("custom creation must not use POST /sandboxes")
        ),
    )
    SyncApi._create_sandbox(
        template="base",
        timeout=300,
        auto_pause=None,
        allow_internet_access=True,
        metadata=None,
        env_vars=None,
        secure=True,
        resources={"memory_gib": 2},
        domain=DOMAIN,
    )
    assert sent["timeout"] == 360.0


def test_create_honors_an_explicit_request_timeout(monkeypatch):
    sent: Dict[str, Any] = {}

    def handler(path, body, timeout):
        sent["timeout"] = timeout
        return Response({"sandboxID": "sbx", "envdVersion": "0.5.14"}, status_code=201)

    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        lambda config: sync_client(handler),
    )
    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.post_sandboxes.sync_detailed",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("custom creation must not use POST /sandboxes")
        ),
    )
    SyncApi._create_sandbox(
        template="base",
        timeout=300,
        auto_pause=None,
        allow_internet_access=True,
        metadata=None,
        env_vars=None,
        secure=True,
        resources={"memory_gib": 2},
        request_timeout=12,
        domain=DOMAIN,
    )
    assert sent["timeout"] == 12


def test_create_surfaces_a_rejected_resource(monkeypatch):
    def handler(path, body, timeout):
        return Response(
            {
                "code": 400,
                "message": "disk exceeds the sandbox limit",
                "item": "disk",
                "reason": "exceeds_sandbox_limit",
            },
            status_code=400,
        )

    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        lambda config: sync_client(handler),
    )
    with pytest.raises(SandboxException, match="exceeds the sandbox limit"):
        SyncApi._create_sandbox(
            template="base",
            timeout=300,
            auto_pause=None,
            allow_internet_access=True,
            metadata=None,
            env_vars=None,
            secure=True,
            resources={"disk_gib": 6},
            domain=DOMAIN,
        )


def _create_args(**kwargs: Any) -> Dict[str, Any]:
    return {
        "template": "base",
        "timeout": 300,
        "auto_pause": None,
        "allow_internet_access": True,
        "metadata": None,
        "env_vars": None,
        "secure": True,
        "domain": DOMAIN,
        **kwargs,
    }


def test_create_rejects_explicit_empty_resources_before_http(monkeypatch):
    called: list[Any] = []
    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        lambda config: called.append(config),
    )
    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.post_sandboxes.sync_detailed",
        lambda *args, **kwargs: pytest.fail(
            "empty resources must not fall back to a default create"
        ),
    )
    with pytest.raises(ValueError, match="at least one"):
        SyncApi._create_sandbox(**_create_args(resources={}))
    with pytest.raises(ValueError, match="must be a mapping"):
        SyncApi._create_sandbox(**_create_args(resources=[]))
    assert called == []


@pytest.mark.asyncio
async def test_async_create_rejects_explicit_empty_resources_before_http(monkeypatch):
    called: list[Any] = []
    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_async.sandbox_api.get_api_client",
        lambda config: called.append(config),
    )
    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_async.sandbox_api.post_sandboxes.asyncio_detailed",
        lambda *args, **kwargs: pytest.fail(
            "empty resources must not fall back to a default create"
        ),
    )
    with pytest.raises(ValueError, match="at least one"):
        await AsyncApi._create_sandbox(**_create_args(resources={}))
    with pytest.raises(ValueError, match="must be a mapping"):
        await AsyncApi._create_sandbox(**_create_args(resources=[]))
    assert called == []


@pytest.mark.asyncio
async def test_async_create_honors_an_explicit_request_timeout(monkeypatch):
    sent: Dict[str, Any] = {}

    def handler(path, body, timeout):
        sent["timeout"] = timeout
        return Response({"sandboxID": "sbx", "envdVersion": "0.5.14"}, status_code=201)

    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_async.sandbox_api.get_api_client",
        lambda config: async_client(handler),
    )
    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_async.sandbox_api.post_sandboxes.asyncio_detailed",
        lambda *args, **kwargs: pytest.fail(
            "custom creation must not use POST /sandboxes"
        ),
    )
    await AsyncApi._create_sandbox(
        **_create_args(resources={"memory_gib": 2}, request_timeout=12)
    )
    assert sent["timeout"] == 12


def test_info_reads_flat_totals_without_inventing_resources():
    detail = SandboxDetail.from_dict(
        {
            "clientID": "client",
            "cpuCount": 2,
            "diskSizeMB": 40960,
            "endAt": "2026-11-06T13:00:00Z",
            "envdVersion": "0.5.14",
            "memoryMB": 8192,
            "sandboxID": "sbx",
            "startedAt": "2026-11-06T12:00:00Z",
            "state": "running",
            "templateID": "base",
        }
    )
    info = SandboxInfo._from_sandbox_detail(detail)
    assert info.cpu_count == 2
    assert info.memory_mb == 8192
    assert info.disk_size_mb == 40960
    assert not hasattr(info, "resources")
