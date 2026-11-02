"""Public sync/async policy APIs exercised through encoded REST requests."""

from datetime import datetime, timedelta, timezone
import inspect
import json
from unittest.mock import patch

import httpx
import pytest
import pytest_asyncio

from http_mock import set_handler
from test_openapi_transport import _runtime_json
from runta import ApiError, AsyncRunta, EgressPolicy, Runta, RuntimeInfo
from runta._internal.openapi.models import Runtime as OpenApiRuntime
from runta._internal.transport import runtime_info, tcp_allowlist_to_openapi


async def result(value):
    return await value if inspect.isawaitable(value) else value


@pytest_asyncio.fixture(params=[Runta, AsyncRunta], ids=["sync", "async"])
async def client(request):
    sdk = request.param(endpoint="http://runta.test", token="rt_test")
    try:
        yield sdk
    finally:
        await result(sdk.close())


def mock_runtime(client, *, initial=None, conflict=False):
    state = _runtime_json() | (initial or {})
    writes = []

    def handler(request):
        if request.method == "GET":
            return httpx.Response(200, json={"data": state})
        body = json.loads(request.content)
        writes.append((request.method, body))
        if request.method == "PATCH":
            assert request.url.params["expected_revision"] == str(state["revision"])
            if conflict:
                return httpx.Response(
                    409,
                    json={
                        "error": {
                            "code": "failed_precondition",
                            "message": "runtime revision conflict: concurrent update",
                        },
                        "request_id": "test",
                    },
                )
        for name in ("auto_shutdown_policy", "auto_delete_policy", "tcp_allowlist"):
            if name in body:
                if (
                    name == "tcp_allowlist"
                    and body.get("checkpoint_id")
                    and not body[name]
                ):
                    continue  # The server inherits the snapshot for empty restores.
                state[name] = body[name]
        return httpx.Response(
            201 if request.method == "POST" else 200, json={"data": state}
        )

    set_handler(client._http, handler)
    return state, writes


@pytest.mark.asyncio
@pytest.mark.parametrize("checkpoint_id", [None, "checkpoint-1"])
@pytest.mark.parametrize("seconds", [None, 0, 1, 2147483647])
async def test_create_and_restore_timeout_wire_shape(client, checkpoint_id, seconds):
    _, writes = mock_runtime(client)
    runtime = await result(
        client.runtimes.create(
            checkpoint_id=checkpoint_id,
            auto_shutdown_after_secs=seconds,
            auto_delete_after_secs=seconds,
            wait=False,
        )
    )
    body = writes[0][1]
    for name in ("auto_shutdown_policy", "auto_delete_policy"):
        if seconds is None:
            assert name not in body
        else:
            assert body[name] == (
                {"mode": "disabled"}
                if seconds == 0
                else {"mode": "enabled", "after_seconds": seconds}
            )
    assert runtime.cached_info.auto_shutdown_after_secs == (seconds or 0)
    assert runtime.cached_info.auto_delete_after_secs == (seconds or 0)
    assert body.get("checkpoint_id") == checkpoint_id
    assert "tcp_allowlist" not in body


@pytest.mark.asyncio
@pytest.mark.parametrize("checkpoint_id", [None, "checkpoint-1"])
@pytest.mark.parametrize("hosts", [None, [], ["db.example.com:5432"]])
async def test_create_and_restore_tcp_wire_shape(client, checkpoint_id, hosts):
    inherited = ["inherited.example.com:443"] if checkpoint_id else []
    _, writes = mock_runtime(client, initial={"tcp_allowlist": inherited})
    runtime = await result(
        client.runtimes.create(
            checkpoint_id=checkpoint_id,
            tcp_allowlist=hosts,
            wait=False,
        )
    )
    body = writes[0][1]
    if hosts is None:
        assert "tcp_allowlist" not in body
        assert runtime.cached_info.tcp_allowlist == inherited
    else:
        assert body["tcp_allowlist"] == hosts
    # Verify the SDK leaves checkpoint inheritance to the server, without
    # translating the empty list to a different request value.
    assert "auto_shutdown_policy" not in body
    assert "auto_delete_policy" not in body
    assert runtime.cached_info.tcp_allowlist == (hosts or inherited)


@pytest.mark.asyncio
async def test_restore_handle_forwards_options(client):
    _, writes = mock_runtime(client)
    runtime = await result(client.runtimes.get("sb-1"))
    await result(
        runtime.restore(
            "checkpoint-1",
            auto_shutdown_after_secs=60,
            auto_delete_after_secs=120,
            tcp_allowlist=["db.example.com:5432"],
            wait=False,
        )
    )
    body = writes[0][1]
    assert body["checkpoint_id"] == "checkpoint-1"
    assert body["auto_shutdown_policy"] == {"mode": "enabled", "after_seconds": 60}
    assert body["auto_delete_policy"] == {"mode": "enabled", "after_seconds": 120}
    assert body["tcp_allowlist"] == ["db.example.com:5432"]


@pytest.mark.asyncio
async def test_updates_cache_and_preserves_omitted_policy(client):
    state, writes = mock_runtime(
        client,
        initial={
            "auto_shutdown_policy": {"mode": "enabled", "after_seconds": 60},
            "auto_delete_policy": {"mode": "enabled", "after_seconds": 120},
            "auto_shutdown_at": "2026-10-29T01:00:00Z",
            "auto_delete_at": "2026-10-29T02:00:00+08:00",
        },
    )
    runtime = await result(client.runtimes.get("sb-1"))
    info = await result(runtime.update_timeout_policies(auto_shutdown_after_secs=0))
    assert info is runtime.cached_info
    assert writes[-1][1] == {"auto_shutdown_policy": {"mode": "disabled"}}
    assert info.auto_shutdown_after_secs == 0
    assert info.auto_delete_after_secs == 120
    assert info.auto_shutdown_at == datetime(2026, 10, 29, 1, tzinfo=timezone.utc)
    assert info.auto_delete_at.utcoffset() == timedelta(hours=8)
    await result(runtime.update_timeout_policies(auto_delete_after_secs=300))
    assert writes[-1][1] == {
        "auto_delete_policy": {"mode": "enabled", "after_seconds": 300}
    }
    assert runtime.cached_info.auto_delete_after_secs == 300
    await result(runtime.egress.set_tcp_allowlist(["db.example.com:5432"]))
    assert writes[-1][1] == {"tcp_allowlist": ["db.example.com:5432"]}
    assert runtime.cached_info.tcp_allowlist == state["tcp_allowlist"]
    returned = await result(runtime.egress.get_tcp_allowlist())
    returned.clear()
    assert runtime.cached_info.tcp_allowlist == ["db.example.com:5432"]
    await result(runtime.egress.set_tcp_allowlist([]))
    assert writes[-1][1] == {"tcp_allowlist": []}
    assert runtime.cached_info.tcp_allowlist == []
    await result(runtime.update_timeout_policies())
    assert writes[-1][1] == {}


@pytest.mark.asyncio
async def test_other_patches_do_not_reset_policies(client):
    _, writes = mock_runtime(client)
    runtime = await result(client.runtimes.get("sb-1"))
    await result(runtime.resize_memory(2048))
    await result(runtime.egress.set_policy(EgressPolicy()))
    for _, body in writes:
        assert "auto_shutdown_policy" not in body
        assert "auto_delete_policy" not in body
        assert "tcp_allowlist" not in body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field", ["auto_shutdown_after_secs", "auto_delete_after_secs"]
)
@pytest.mark.parametrize("invalid", [True, False, 1.5, "60", -1, 2147483648])
async def test_invalid_seconds_rejected_before_requests(client, field, invalid):
    _, writes = mock_runtime(client)
    runtime = await result(client.runtimes.get("sb-1"))
    with pytest.raises(ValueError, match="timeout seconds"):
        await result(client.runtimes.create(**{field: invalid}, wait=False))
    with pytest.raises(ValueError, match="timeout seconds"):
        await result(runtime.update_timeout_policies(**{field: invalid}))
    assert not writes


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "invalid", ["db.example.com:5432", [""], [" "], [123], ["db.example.com:5432"] * 17]
)
async def test_invalid_tcp_allowlist(client, invalid):
    _, writes = mock_runtime(client)
    runtime = await result(client.runtimes.get("sb-1"))
    with pytest.raises(ValueError, match="tcp_allowlist"):
        await result(client.runtimes.create(tcp_allowlist=invalid, wait=False))
    with pytest.raises(ValueError, match="tcp_allowlist"):
        await result(runtime.egress.set_tcp_allowlist(invalid))
    assert not writes


def test_tcp_allowlist_copies_input_and_accepts_boundary():
    hosts = [f"db{i}.example.com:5432" for i in range(16)]
    encoded = tcp_allowlist_to_openapi(hosts)
    hosts.clear()
    assert len(encoded) == 16
    assert tcp_allowlist_to_openapi(tuple(encoded)) == encoded


def test_response_defaults_and_list_copy():
    payload = _runtime_json()
    info = runtime_info(OpenApiRuntime.from_dict(payload))
    assert info.auto_shutdown_after_secs == info.auto_delete_after_secs == 0
    assert info.auto_shutdown_at is info.auto_delete_at is None
    assert info.tcp_allowlist == []
    payload["tcp_allowlist"] = ["db.example.com:5432"]
    direct = RuntimeInfo.from_json(payload)
    payload["tcp_allowlist"].clear()
    assert direct.tcp_allowlist == ["db.example.com:5432"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field", ["auto_shutdown_after_secs", "auto_delete_after_secs"]
)
@pytest.mark.parametrize("seconds", [0, 60])
async def test_policy_conflict_requires_proof_of_save(client, field, seconds):
    wire = field.replace("_after_secs", "_policy")
    _, writes = mock_runtime(
        client,
        initial={
            wire: {"mode": "disabled"}
            if seconds == 0
            else {"mode": "enabled", "after_seconds": seconds}
        },
        conflict=True,
    )
    runtime = await result(client.runtimes.get("sb-1"))
    if seconds:
        with pytest.raises(ApiError, match="revision conflict"):
            await result(runtime.update_timeout_policies(**{field: seconds}))
    else:
        info = await result(runtime.update_timeout_policies(**{field: seconds}))
        assert getattr(info, field) == 0
    assert len(writes) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("current", [[], ["db.example.com:5432"]])
async def test_tcp_conflict_checks_current_configuration(client, current):
    _, writes = mock_runtime(client, initial={"tcp_allowlist": current}, conflict=True)
    runtime = await result(client.runtimes.get("sb-1"))
    if current:
        with pytest.raises(ApiError, match="revision conflict"):
            await result(runtime.egress.set_tcp_allowlist([]))
    else:
        info = await result(runtime.egress.set_tcp_allowlist([]))
        assert info.tcp_allowlist == []
    assert len(writes) == 1


@pytest.mark.asyncio
async def test_lost_tcp_patch_response_recovers_without_overwriting(client):
    writes = []
    state = _runtime_json()

    def handler(request):
        if request.method == "GET":
            return httpx.Response(200, json={"data": state})
        writes.append(
            (request.url.params["expected_revision"], json.loads(request.content))
        )
        if len(writes) == 1:
            state.update(tcp_allowlist=["db.example.com:5432"], revision=2)
            raise httpx.ReadError("response lost", request=request)
        return httpx.Response(
            409,
            json={
                "error": {
                    "code": "failed_precondition",
                    "message": "runtime revision conflict: expected 1, current 2",
                },
                "request_id": "test",
            },
        )

    set_handler(client._http, handler)
    runtime = await result(client.runtimes.get("sb-1"))
    with patch("runta._internal.retry.random.uniform", return_value=0):
        info = await result(runtime.egress.set_tcp_allowlist(["db.example.com:5432"]))
    assert info.tcp_allowlist == ["db.example.com:5432"]
    assert len(writes) == 2
    assert writes[0] == writes[1]


@pytest.mark.parametrize(
    "timestamp,offset",
    [
        ("2026-10-29T01:00:00Z", timedelta(0)),
        ("2026-10-29T01:00:00.123456Z", timedelta(0)),
        ("2026-10-29T01:00:00+08:00", timedelta(hours=8)),
        ("2026-10-29T01:00:00", timedelta(0)),
    ],
)
def test_deadlines_always_have_a_timezone(timestamp, offset):
    payload = _runtime_json() | {
        "auto_shutdown_at": timestamp,
        "auto_delete_at": timestamp,
    }
    info = runtime_info(OpenApiRuntime.from_dict(payload))
    assert info.auto_shutdown_at.utcoffset() == offset
    assert info.auto_delete_at.utcoffset() == offset
