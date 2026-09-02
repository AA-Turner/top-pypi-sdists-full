from packaging.version import Version
import pytest

from novita_sandbox.core import AsyncSandbox, Sandbox, SandboxNotFoundException
from novita_sandbox.core.connection_config import ConnectionConfig
from novita_sandbox.core.sandbox_async.sandbox_api import SandboxApi as AsyncSandboxApi
from novita_sandbox.core.sandbox_sync.sandbox_api import SandboxApi


class Response:
    status_code = 200
    text = ""
    content = b"{}"

    def json(self):
        return {}


def test_mount_volume_uses_connection_config_for_api_client(monkeypatch):
    configs = []

    class HttpxClient:
        def post(self, *args, **kwargs):
            return Response()

        def delete(self, *args, **kwargs):
            return Response()

    class ApiClient:
        def get_httpx_client(self):
            return HttpxClient()

    def get_api_client(config):
        configs.append(config)
        return ApiClient()

    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        get_api_client,
    )

    sandbox = Sandbox(
        sandbox_id="sandbox-id",
        sandbox_domain="us-phx-1.sandbox.novita.ai",
        envd_version=Version("0.0.1"),
        envd_access_token=None,
        traffic_access_token=None,
        connection_config=ConnectionConfig(api_key="test-api-key"),
    )
    try:
        sandbox.mount_volume("volume-name", "/mnt/vol", api_key="override-key")
        sandbox.unmount_volume("/mnt/vol", force=True, api_key="override-key")
    finally:
        sandbox._envd_api.close()

    assert all(isinstance(config, ConnectionConfig) for config in configs)
    assert [config.api_key for config in configs] == ["override-key", "override-key"]


def test_mount_volume_raises_sandbox_not_found_on_404(monkeypatch):
    class HttpxClient:
        def post(self, *args, **kwargs):
            response = Response()
            response.status_code = 404
            return response

        def delete(self, *args, **kwargs):
            response = Response()
            response.status_code = 404
            return response

    class ApiClient:
        def get_httpx_client(self):
            return HttpxClient()

    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_sync.sandbox_api.get_api_client",
        lambda config: ApiClient(),
    )

    with pytest.raises(SandboxNotFoundException, match="Sandbox sandbox-id not found"):
        SandboxApi._cls_mount_volume("sandbox-id", "volume-name", "/mnt/vol")

    with pytest.raises(SandboxNotFoundException, match="Sandbox sandbox-id not found"):
        SandboxApi._cls_unmount_volume("sandbox-id", "/mnt/vol")


@pytest.mark.asyncio
async def test_async_mount_volume_uses_connection_config_for_api_client(monkeypatch):
    configs = []

    class AsyncHttpxClient:
        async def post(self, *args, **kwargs):
            return Response()

        async def delete(self, *args, **kwargs):
            return Response()

    class ApiClient:
        def get_async_httpx_client(self):
            return AsyncHttpxClient()

    def get_api_client(config):
        configs.append(config)
        return ApiClient()

    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_async.sandbox_api.get_api_client",
        get_api_client,
    )

    sandbox = AsyncSandbox(
        sandbox_id="sandbox-id",
        sandbox_domain="us-phx-1.sandbox.novita.ai",
        envd_version=Version("0.0.1"),
        envd_access_token=None,
        traffic_access_token=None,
        connection_config=ConnectionConfig(api_key="test-api-key"),
    )
    try:
        await sandbox.mount_volume("volume-name", "/mnt/vol", api_key="override-key")
        await sandbox.unmount_volume("/mnt/vol", force=True, api_key="override-key")
    finally:
        await sandbox._envd_api.aclose()

    assert all(isinstance(config, ConnectionConfig) for config in configs)
    assert [config.api_key for config in configs] == ["override-key", "override-key"]


@pytest.mark.asyncio
async def test_async_mount_volume_raises_sandbox_not_found_on_404(monkeypatch):
    class AsyncHttpxClient:
        async def post(self, *args, **kwargs):
            response = Response()
            response.status_code = 404
            return response

        async def delete(self, *args, **kwargs):
            response = Response()
            response.status_code = 404
            return response

    class ApiClient:
        def get_async_httpx_client(self):
            return AsyncHttpxClient()

    monkeypatch.setattr(
        "novita_sandbox.core.sandbox_async.sandbox_api.get_api_client",
        lambda config: ApiClient(),
    )

    with pytest.raises(SandboxNotFoundException, match="Sandbox sandbox-id not found"):
        await AsyncSandboxApi._cls_mount_volume("sandbox-id", "volume-name", "/mnt/vol")

    with pytest.raises(SandboxNotFoundException, match="Sandbox sandbox-id not found"):
        await AsyncSandboxApi._cls_unmount_volume("sandbox-id", "/mnt/vol")
