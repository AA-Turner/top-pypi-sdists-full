"""Keep hand-written SDK adapters compatible with the refreshed contract."""

import inspect
import json

import httpx
import pytest
import pytest_asyncio

from http_mock import set_handler
from test_openapi_transport import _runtime_json
from runta import (
    AsyncRunta,
    IngressSpec,
    PatchRuntimeResources,
    Runta,
    RuntimeResourceLimits,
    RuntimeStatus,
)


async def result(value):
    return await value if inspect.isawaitable(value) else value


@pytest_asyncio.fixture(params=[Runta, AsyncRunta], ids=["sync", "async"])
async def client(request):
    sdk = request.param(endpoint="http://runta.test", token="rt_test")
    try:
        yield sdk
    finally:
        await result(sdk.close())


@pytest.mark.asyncio
async def test_deleted_runtime_get_and_mixed_list(client):
    deleted = _runtime_json() | {"status": "deleted", "desired_status": "shutdown"}
    running = _runtime_json() | {"id": "sb-2"}

    def handler(request):
        if request.url.path == "/v2/runtimes":
            assert request.url.params["status"] == "deleted,running"
            return httpx.Response(
                200,
                json={
                    "data": [deleted, running],
                    "pagination": {"has_more": False, "next_cursor": None},
                },
            )
        return httpx.Response(200, json={"data": deleted})

    set_handler(client._http, handler)
    runtime = await result(client.runtimes.get("sb-1"))
    assert runtime.cached_info.status is RuntimeStatus.DELETED
    runtimes = await result(client.runtimes.list(status=["deleted", "running"]))
    assert [item.cached_info.status for item in runtimes] == [
        RuntimeStatus.DELETED,
        RuntimeStatus.RUNNING,
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize("typed", [False, True])
async def test_custom_hostname_create_restore_and_read(client, typed):
    rule = {"protocol": "http", "runtime_port": 8080, "hostname_label": "foxden"}
    ingress = IngressSpec.from_json(rule) if typed else rule
    bodies = []

    def handler(request):
        body = json.loads(request.content)
        bodies.append(body)
        assert body["ingress_specs"] == [rule]
        return httpx.Response(201, json={"data": _runtime_json(ingress_specs=[rule])})

    set_handler(client._http, handler)
    for options in ({}, {"checkpoint_id": "checkpoint-1"}):
        runtime = await result(
            client.runtimes.create(ingress_specs=[ingress], wait=False, **options)
        )
        assert runtime.cached_info.ingress_specs[0].to_json() == rule
    assert "resources" in bodies[0]
    assert "resources" not in bodies[1]


def test_legacy_fields_remain_omitted():
    rule = {"protocol": "http", "runtime_port": 8080}
    assert IngressSpec.from_json(rule).to_json() == rule
    from runta._internal.transport import ingress_spec_to_openapi

    assert ingress_spec_to_openapi(rule).to_dict() == rule
    limits = {"memory_mib": 2048}
    assert RuntimeResourceLimits.from_json(limits).to_json() == limits


@pytest.mark.asyncio
async def test_cpu_limit_update_and_reads(client):
    state = _runtime_json()
    writes = []

    def handler(request):
        if request.method == "PATCH":
            body = json.loads(request.content)
            writes.append(body)
            state["resources"]["limits"].update(body["resources"]["limits"])
        if request.url.path == "/v2/runtimes":
            return httpx.Response(
                200,
                json={
                    "data": [state],
                    "pagination": {"has_more": False, "next_cursor": None},
                },
            )
        return httpx.Response(200, json={"data": state})

    set_handler(client._http, handler)
    runtime = await result(client.runtimes.get("sb-1"))
    info = await result(
        runtime.update_resources(
            PatchRuntimeResources(
                limits=RuntimeResourceLimits(memory_mib=2048, vcpus=4)
            )
        )
    )
    assert writes[0]["resources"]["limits"] == {"memory_mib": 2048, "vcpus": 4}
    assert info.resources.limits.vcpus == 4
    runtime = await result(client.runtimes.get("sb-1"))
    assert runtime.cached_info.resources.limits.vcpus == 4
    listed = await result(client.runtimes.list())
    assert listed[0].cached_info.resources.limits.to_json() == {
        "memory_mib": 2048,
        "vcpus": 4,
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "override",
    [
        {"resources": {}},
        {"vcpus": 1},
        {"vcpus": 8},
        {"memory_mib": 1024},
        {"memory_mib": 8192},
        {"memory_max_mib": 4096},
    ],
)
async def test_restore_rejects_overrides_without_network(client, override):
    def handler(request):
        pytest.fail("Restore overrides must be rejected before any HTTP request")

    set_handler(client._http, handler)
    with pytest.raises(ValueError, match="preserve recorded"):
        await result(
            client.runtimes.create(checkpoint_id="checkpoint-1", wait=False, **override)
        )
