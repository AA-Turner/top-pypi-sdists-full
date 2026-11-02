"""Opt-in E2E coverage for runtime policies against RUNTA_ENDPOINT.

Run with: python -m pytest tests/test_runtime_policies_live.py --live -s
Only resources with this run's unique name prefix are modified or deleted.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
import inspect
import json
import os
import time
import uuid

import pytest
import pytest_asyncio

from runta import ApiError, AsyncRunta, Runta, RuntimeStatus


pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.skipif(
        os.getenv("RUNTA_PYTEST_LIVE") != "1", reason="pass --live to run hosted E2E"
    ),
]
TCP_HOST = "ssh.github.com:443"
TCP_PROBE = """
import json, socket
address = None
try:
    address = socket.getaddrinfo('ssh.github.com', 443, socket.AF_INET, socket.SOCK_STREAM)[0][4]
    with socket.create_connection(address, timeout=4) as connection:
        banner = connection.recv(128).decode(errors='replace')
    print(json.dumps({'allowed': banner.startswith('SSH-2.0-'), 'banner': banner, 'address': address[0]}))
except OSError as error:
    print(json.dumps({'allowed': False, 'error': type(error).__name__, 'address': address[0] if address else None}))
"""


async def result(value):
    return await value if inspect.isawaitable(value) else value


def log(message):
    print(f"[{datetime.now(timezone.utc).isoformat()}] {message}", flush=True)


async def eventually(operation, predicate, *, timeout=120, label):
    deadline = time.monotonic() + timeout
    previous = object()
    while True:
        value = await operation()
        if value != previous:
            log(f"{label}: {value}")
            previous = value
        if predicate(value):
            return value
        if time.monotonic() >= deadline:
            raise AssertionError(f"{label} timed out; last value: {value}")
        await asyncio.sleep(2)


class Resources:
    def __init__(self, client):
        self.client = client
        self.prefix = f"sdk-policies-e2e-{uuid.uuid4().hex[:10]}"

    async def create(self, suffix, **options):
        # Register by unique prefix before waiting; teardown also finds resources
        # when creation succeeds server-side but its response or readiness fails.
        runtime = await result(
            self.client.runtimes.create(
                f"{self.prefix}-{suffix}",
                wait=False,
                **options,
            )
        )
        log(f"created {runtime.id} ({runtime.name})")
        return runtime

    async def running(self, runtime):
        info = await result(runtime.refresh_info())
        if info.status == RuntimeStatus.SHUTDOWN:
            await result(runtime.boot(timeout=240))
        else:
            await result(runtime.wait_until_ready(timeout=240))
        log(f"running {runtime.id}")

    async def absent(self, runtime_id):
        async def check():
            try:
                # Use the ID-only HTTP route; manager.get also searches by name.
                await result(self.client._http.get_runtime(runtime_id))
                return False
            except ApiError as error:
                if error.status_code != 404:
                    raise
                return True

        await eventually(check, bool, timeout=180, label=f"deleted {runtime_id}")

    async def cleanup(self):
        owned = [
            r
            for r in await result(self.client.runtimes.list())
            if r.name.startswith(self.prefix)
        ]
        for runtime in owned:
            await result(runtime.delete())
        for runtime in owned:
            await self.absent(runtime.id)
        for checkpoint in await result(self.client.checkpoints.list()):
            if checkpoint.display_name.startswith(self.prefix):
                await result(self.client.checkpoints.delete(checkpoint.id))
        remaining = [
            r.id
            for r in await result(self.client.runtimes.list())
            if r.name.startswith(self.prefix)
        ]
        checkpoints = [
            c.id
            for c in await result(self.client.checkpoints.list())
            if c.display_name.startswith(self.prefix)
        ]
        assert remaining == checkpoints == []
        log(f"cleanup {self.prefix}: runtimes=0 checkpoints=0")


@pytest_asyncio.fixture
async def resources(request):
    client_class = getattr(request, "param", AsyncRunta)
    client = client_class(timeout=30, retry_max_attempts=2)
    resources = Resources(client)
    before = {r.id for r in await result(client.runtimes.list())}
    log(f"endpoint={client._http.endpoint}; pre-existing runtime IDs={sorted(before)}")
    try:
        yield resources
    finally:
        try:
            await resources.cleanup()
            after = {r.id for r in await result(client.runtimes.list())}
            log(
                f"inventory: before={len(before)} after={len(after)} "
                f"added={sorted(after - before)} missing={sorted(before - after)}"
            )
            assert before <= after, "a pre-existing runtime disappeared during testing"
        finally:
            await result(client.close())


async def assert_tcp(runtime, allowed):
    async def probe():
        command = await result(runtime.exec(["python3", "-c", TCP_PROBE], timeout=15))
        assert command.exit_code == 0, command.stderr_text
        return json.loads(command.stdout_text)

    await eventually(
        probe,
        lambda value: value["allowed"] is allowed,
        timeout=90,
        label=f"TCP allowed={allowed}",
    )


@pytest.mark.parametrize(
    "resources", [Runta, AsyncRunta], indirect=True, ids=["sync", "async"]
)
async def test_policy_roundtrip_and_actual_tcp_enforcement(resources):
    runtime = await resources.create(
        "roundtrip",
        auto_shutdown_after_secs=600,
        auto_delete_after_secs=120,
        tcp_allowlist=[TCP_HOST],
    )
    await resources.running(runtime)
    info = await result(runtime.refresh_info())
    assert info.auto_shutdown_after_secs == 600
    assert info.auto_delete_after_secs == 120
    assert (
        info.auto_shutdown_at is not None and info.auto_shutdown_at.tzinfo is not None
    )
    assert info.auto_delete_at is None
    deadline = info.auto_shutdown_at
    assert await result(runtime.egress.get_tcp_allowlist()) == [TCP_HOST]
    await assert_tcp(runtime, True)

    info = await result(runtime.egress.set_tcp_allowlist([]))
    assert info.tcp_allowlist == []
    assert info.auto_shutdown_at == deadline
    await assert_tcp(runtime, False)
    await result(runtime.egress.set_tcp_allowlist([TCP_HOST]))
    await assert_tcp(runtime, True)

    info = await result(runtime.update_timeout_policies(auto_delete_after_secs=180))
    assert info.auto_delete_after_secs == 180
    assert info.auto_shutdown_at == deadline
    info = await result(runtime.update_timeout_policies(auto_shutdown_after_secs=900))
    assert info.auto_shutdown_at > deadline
    assert info.auto_delete_after_secs == 180
    info = await result(
        runtime.update_timeout_policies(
            auto_shutdown_after_secs=0,
            auto_delete_after_secs=0,
        )
    )
    assert info.auto_shutdown_after_secs == info.auto_delete_after_secs == 0
    assert info.auto_shutdown_at is info.auto_delete_at is None
    log(
        "PASS policy roundtrip, selective clock reset, disable, and TCP allow/deny/allow"
    )


async def test_checkpoint_tcp_inheritance(resources):
    runtime = await resources.create(
        "lifecycle",
        auto_shutdown_after_secs=600,
        auto_delete_after_secs=120,
        tcp_allowlist=[TCP_HOST],
    )
    await resources.running(runtime)
    marker = await runtime.exec(
        ["sh", "-c", "printf policy-checkpoint > /tmp/policy-e2e"], timeout=30
    )
    assert marker.exit_code == 0, marker.stderr_text
    checkpoint = await runtime.checkpoints.create(
        name=f"{resources.prefix}-checkpoint",
        timeout=600,
    )
    log(f"checkpoint ready {checkpoint.id}")
    for suffix, options, expected in [
        ("inherit", {}, [TCP_HOST]),
        ("empty-inherits", {"tcp_allowlist": []}, [TCP_HOST]),
        ("override", {"tcp_allowlist": ["github.com:443"]}, ["github.com:443"]),
    ]:
        restored = await resources.create(
            suffix,
            checkpoint_id=checkpoint.id,
            auto_shutdown_after_secs=600,
            auto_delete_after_secs=120,
            **options,
        )
        log(
            f"restore {suffix}: initial tcp_allowlist={restored.cached_info.tcp_allowlist}"
        )
        await resources.running(restored)
        info = await restored.refresh_info()
        log(f"restore {suffix}: ready tcp_allowlist={info.tcp_allowlist}")
        assert info.tcp_allowlist == expected
        assert info.auto_shutdown_after_secs == 600
        assert info.auto_delete_after_secs == 120
        command = await restored.exec(["cat", "/tmp/policy-e2e"], timeout=30)
        assert command.exit_code == 0 and command.stdout_text == "policy-checkpoint"
        await restored.egress.set_tcp_allowlist([])
        assert await restored.egress.get_tcp_allowlist() == []
        await restored.delete()
        await resources.absent(restored.id)
    log(
        "PASS checkpoint restore: omitted/empty inherit; nonempty overrides; clear after restore"
    )


async def test_automatic_shutdown_delete(resources):
    runtime = await resources.create(
        "automatic", auto_shutdown_after_secs=600, auto_delete_after_secs=120
    )
    await resources.running(runtime)
    info = await runtime.update_timeout_policies(
        auto_shutdown_after_secs=12,
        auto_delete_after_secs=45,
    )
    assert info.auto_shutdown_at is not None
    await eventually(
        runtime.status,
        lambda status: status == RuntimeStatus.SHUTDOWN,
        timeout=180,
        label="automatic shutdown",
    )
    info = await runtime.refresh_info()
    assert info.auto_delete_at is not None and info.auto_delete_at.tzinfo is not None
    old_deletion = info.auto_delete_at
    # Disable only shutdown so the restarted runtime remains running while we
    # cross its previous deletion deadline. The retention policy stays enabled.
    await runtime.update_timeout_policies(auto_shutdown_after_secs=0)
    await runtime.boot(timeout=240)
    info = await runtime.refresh_info()
    assert info.auto_delete_after_secs == 45 and info.auto_delete_at is None
    while datetime.now(timezone.utc) <= old_deletion:
        await asyncio.sleep(2)
    assert await runtime.status() == RuntimeStatus.RUNNING
    log("PASS starting canceled deletion, runtime survived its former deadline")
    await runtime.shutdown()
    await eventually(
        runtime.status,
        lambda status: status == RuntimeStatus.SHUTDOWN,
        timeout=180,
        label="confirmed shutdown for deletion",
    )
    info = await runtime.refresh_info()
    assert info.auto_delete_at is not None
    await resources.absent(runtime.id)
    log("PASS actual automatic shutdown and automatic deletion")
