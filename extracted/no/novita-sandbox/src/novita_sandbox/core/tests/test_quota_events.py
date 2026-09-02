import json
from http import HTTPStatus
from types import SimpleNamespace

import pytest

from novita_sandbox.core import AsyncSandbox, Sandbox, SandboxEventItem, SandboxQuota
from novita_sandbox.core.api.client.types import Response
from novita_sandbox.core.sandbox_sync import sandbox_api as sync_sandbox_api
from novita_sandbox.core.sandbox_async import sandbox_api as async_sandbox_api


EVENTS_RESPONSE = {
    "items": [
        {
            "eventID": "evt_001",
            "recordAt": 1766650000,
            "templateID": "tmpl_abc",
            "templateName": "ubuntu-base",
            "sandboxID": "i3vrzzatkxojecvfuesnz",
            "eventName": "create",
            "state": "success",
            "errorMsg": "",
            "statusCode": 200,
        },
        {
            "eventID": "evt_002",
            "recordAt": 1766650100,
            "templateID": "tmpl_abc",
            "templateName": "ubuntu-base",
            "sandboxID": "i3vrzzatkxojecvfuesnz",
            "eventName": "pause",
            "state": "success",
            "errorMsg": "",
            "statusCode": 204,
        },
    ],
    "total": 2,
    "hasMore": False,
}

QUOTA_RESPONSE = {
    "limit": {
        "concurrentInstances": 10,
        "concurrentVcpu": 20,
        "concurrentRamMb": 40,
        "maxLengthHours": 24,
        "diskMb": 10240,
        "maxVcpu": 4,
        "maxRamMb": 4096,
    },
    "usage": {
        "concurrentInstances": 3,
        "concurrentVcpu": 6,
        "concurrentRamMb": 12,
    },
}


# === Events tests ===


def test_sandbox_get_events_methods_exist():
    assert hasattr(Sandbox, "get_events")
    assert hasattr(AsyncSandbox, "get_events")


def test_sync_get_events_returns_parsed_events(monkeypatch):
    class FakeHttpxClient:
        def get(self, path, params=None):
            return Response(
                status_code=HTTPStatus.OK,
                content=json.dumps(EVENTS_RESPONSE).encode(),
                headers={},
                parsed=None,
            )

    monkeypatch.setattr(
        sync_sandbox_api,
        "get_api_client",
        lambda config: SimpleNamespace(get_httpx_client=lambda: FakeHttpxClient()),
    )

    result = Sandbox.get_events(limit=10, offset=0)

    assert result.total == 2
    assert result.has_more is False
    assert len(result.items) == 2

    evt = result.items[0]
    assert isinstance(evt, SandboxEventItem)
    assert evt.event_id == "evt_001"
    assert evt.event_name == "create"
    assert evt.state == "success"
    assert evt.sandbox_id == "i3vrzzatkxojecvfuesnz"
    assert evt.status_code == 200


def test_sync_get_events_passes_query_params(monkeypatch):
    captured = {}

    class FakeHttpxClient:
        def get(self, path, params=None):
            captured["path"] = path
            captured["params"] = params
            return Response(
                status_code=HTTPStatus.OK,
                content=json.dumps({"items": [], "total": 0, "hasMore": False}).encode(),
                headers={},
                parsed=None,
            )

    monkeypatch.setattr(
        sync_sandbox_api,
        "get_api_client",
        lambda config: SimpleNamespace(get_httpx_client=lambda: FakeHttpxClient()),
    )

    Sandbox.get_events(
        start_time=1766572800,
        end_time=1766659200,
        sandbox_id="iq721h44siv24wmyrh5oc",
        events="create,pause,resume",
        state="success",
        order_asc=True,
        offset=5,
        limit=20,
    )

    assert captured["path"] == "/sandboxes/events"
    assert captured["params"]["startTime"] == 1766572800
    assert captured["params"]["endTime"] == 1766659200
    assert captured["params"]["sandboxID"] == "iq721h44siv24wmyrh5oc"
    assert captured["params"]["events"] == "create,pause,resume"
    assert captured["params"]["state"] == "success"
    assert captured["params"]["orderAsc"] is True
    assert captured["params"]["offset"] == 5
    assert captured["params"]["limit"] == 20


def test_sync_get_events_returns_empty(monkeypatch):
    class FakeHttpxClient:
        def get(self, path, params=None):
            return Response(
                status_code=HTTPStatus.OK,
                content=json.dumps({"items": [], "total": 0, "hasMore": False}).encode(),
                headers={},
                parsed=None,
            )

    monkeypatch.setattr(
        sync_sandbox_api,
        "get_api_client",
        lambda config: SimpleNamespace(get_httpx_client=lambda: FakeHttpxClient()),
    )

    result = Sandbox.get_events()

    assert len(result.items) == 0
    assert result.total == 0
    assert result.has_more is False


async def test_async_get_events_returns_parsed_events(monkeypatch):
    class FakeAsyncHttpxClient:
        async def get(self, path, params=None):
            return Response(
                status_code=HTTPStatus.OK,
                content=json.dumps(EVENTS_RESPONSE).encode(),
                headers={},
                parsed=None,
            )

    monkeypatch.setattr(
        async_sandbox_api,
        "get_api_client",
        lambda config: SimpleNamespace(get_async_httpx_client=lambda: FakeAsyncHttpxClient()),
    )

    result = await AsyncSandbox.get_events(limit=10)

    assert result.total == 2
    assert len(result.items) == 2
    assert result.items[0].event_id == "evt_001"


# === Quota tests ===


def test_sandbox_get_quota_methods_exist():
    assert hasattr(Sandbox, "get_quota")
    assert hasattr(AsyncSandbox, "get_quota")


def test_sync_get_quota_returns_parsed_quota(monkeypatch):
    class FakeHttpxClient:
        def get(self, path, params=None):
            return Response(
                status_code=HTTPStatus.OK,
                content=json.dumps(QUOTA_RESPONSE).encode(),
                headers={},
                parsed=None,
            )

    monkeypatch.setattr(
        sync_sandbox_api,
        "get_api_client",
        lambda config: SimpleNamespace(get_httpx_client=lambda: FakeHttpxClient()),
    )

    result = Sandbox.get_quota()

    assert isinstance(result, SandboxQuota)
    assert result.limit.concurrent_instances == 10
    assert result.limit.concurrent_vcpu == 20
    assert result.limit.concurrent_ram_mb == 40
    assert result.limit.max_length_hours == 24
    assert result.limit.disk_mb == 10240
    assert result.limit.max_vcpu == 4
    assert result.limit.max_ram_mb == 4096

    assert result.usage.concurrent_instances == 3
    assert result.usage.concurrent_vcpu == 6
    assert result.usage.concurrent_ram_mb == 12


def test_sync_get_quota_handles_missing_fields(monkeypatch):
    class FakeHttpxClient:
        def get(self, path, params=None):
            return Response(
                status_code=HTTPStatus.OK,
                content=b"{}",
                headers={},
                parsed=None,
            )

    monkeypatch.setattr(
        sync_sandbox_api,
        "get_api_client",
        lambda config: SimpleNamespace(get_httpx_client=lambda: FakeHttpxClient()),
    )

    result = Sandbox.get_quota()

    assert result.limit.concurrent_instances == 0
    assert result.limit.concurrent_vcpu == 0
    assert result.usage.concurrent_instances == 0


async def test_async_get_quota_returns_parsed_quota(monkeypatch):
    class FakeAsyncHttpxClient:
        async def get(self, path, params=None):
            return Response(
                status_code=HTTPStatus.OK,
                content=json.dumps(QUOTA_RESPONSE).encode(),
                headers={},
                parsed=None,
            )

    monkeypatch.setattr(
        async_sandbox_api,
        "get_api_client",
        lambda config: SimpleNamespace(get_async_httpx_client=lambda: FakeAsyncHttpxClient()),
    )

    result = await AsyncSandbox.get_quota()

    assert result.limit.concurrent_instances == 10
    assert result.usage.concurrent_vcpu == 6
