"""matrx_connect.warm: sort, throttle, run detached under the caller's context, never raise."""

from __future__ import annotations

import asyncio
import contextvars
import logging
from collections.abc import Iterator

import pytest
import pytest_asyncio

from matrx_connect import warm
from matrx_connect.context.app_context import (
    AppContext,
    clear_app_context,
    get_app_context,
    set_app_context,
)
from matrx_connect.emitters import ConsoleEmitter

ORG = "0b5b1c9e-1d8c-4d37-9a11-3a2f7c1e9d01"


@pytest.fixture(autouse=True)
def _clean_registry() -> Iterator[None]:
    saved = warm.registered_warmers()
    for key in list(saved):
        warm.unregister_warmer(key)
    warm.reset_warm_throttle()
    yield
    for key in list(warm.registered_warmers()):
        warm.unregister_warmer(key)
    for key, w in saved.items():
        warm.register_warmer(key, w.fn, scope=w.scope, needs_id=w.needs_id, timeout_s=w.timeout_s, fill=w.fill)
    warm.reset_warm_throttle()


def _ctx(user_id: str = "person-a") -> AppContext:
    return AppContext(
        emitter=ConsoleEmitter("test", accumulate=False),
        user_id=user_id,
        auth_type="token",
        is_authenticated=True,
        organization_id=ORG,
        request_id="req-warm",
    )


@pytest.mark.asyncio
async def test_known_items_run_concurrently_under_the_callers_context() -> None:
    seen: list[tuple[str, str | None, str]] = []
    both_started = asyncio.Event()
    started = 0

    async def core(_: str | None) -> None:
        nonlocal started
        started += 1
        if started == 2:
            both_started.set()
        await asyncio.wait_for(both_started.wait(), 1.0)  # proves the two run side by side
        seen.append(("core", None, get_app_context().user_id))

    async def agent(item_id: str | None) -> None:
        nonlocal started
        started += 1
        if started == 2:
            both_started.set()
        await asyncio.wait_for(both_started.wait(), 1.0)
        seen.append(("agent", item_id, get_app_context().user_id))

    warm.register_warmer("core", core)
    warm.register_warmer("agent", agent, scope="shared", needs_id=True)

    token = set_app_context(_ctx())
    try:
        result = warm.run_warm(
            [{"key": "core"}, {"key": "agent", "id": "a-1"}, {"key": "dashboard"}, {"key": "agent"}]
        )
    finally:
        clear_app_context(token)
    assert [i.key for i in result.accepted] == ["core", "agent"]
    assert [(i.key, i.id) for i in result.unknown] == [("dashboard", None), ("agent", None)]
    assert result.task is not None
    await result.task
    assert sorted(seen) == [("agent", "a-1", "person-a"), ("core", None, "person-a")]


@pytest.mark.asyncio
async def test_the_same_person_and_item_is_warmed_once_per_window() -> None:
    calls: list[str] = []

    async def core(_: str | None) -> None:
        calls.append(get_app_context().user_id)

    warm.register_warmer("core", core)
    for user in ("person-a", "person-a", "person-b"):
        token = set_app_context(_ctx(user))
        try:
            result = warm.run_warm([{"key": "core"}])
        finally:
            clear_app_context(token)
        if result.task:
            await result.task
    assert calls == ["person-a", "person-b"]
    token = set_app_context(_ctx("person-a"))
    try:
        again = warm.run_warm([{"key": "core"}])
    finally:
        clear_app_context(token)
    assert [i.key for i in again.accepted] == ["core"]
    assert [i.key for i in again.throttled] == ["core"]
    assert again.task is None


@pytest.mark.asyncio
async def test_a_failing_or_hanging_warmer_never_raises_and_never_blocks_the_others(
    caplog: pytest.LogCaptureFixture,
) -> None:
    done: list[str] = []

    async def broken(_: str | None) -> None:
        raise RuntimeError("database hiccup")

    async def hangs(_: str | None) -> None:
        await asyncio.sleep(30)

    async def fine(_: str | None) -> None:
        done.append("fine")

    warm.register_warmer("broken", broken)
    warm.register_warmer("hangs", hangs, timeout_s=0.05)
    warm.register_warmer("fine", fine)
    token = set_app_context(_ctx())
    try:
        result = warm.run_warm([{"key": "broken"}, {"key": "hangs"}, {"key": "fine"}])
    finally:
        clear_app_context(token)
    assert result.task is not None
    with caplog.at_level(logging.WARNING, logger="matrx_connect.warm"):
        await asyncio.wait_for(result.task, 1.0)
    assert done == ["fine"]
    text = caplog.text
    assert "broken failed" in text and "hangs timed out" in text


@pytest.mark.asyncio
async def test_a_warmer_never_inherits_the_requests_transaction_state() -> None:
    txn: contextvars.ContextVar[str | None] = contextvars.ContextVar("txn", default=None)
    seen: list[str | None] = []

    async def core(_: str | None) -> None:
        seen.append(txn.get())

    warm.register_warmer("core", core)
    ctx_token = set_app_context(_ctx())
    txn_token = txn.set("request-connection")
    try:
        result = warm.run_warm([{"key": "core"}])
    finally:
        txn.reset(txn_token)
        clear_app_context(ctx_token)
    assert result.task is not None
    await result.task
    assert seen == [None]


# ── fan-out: process-fill warmers reach every server ──────────────────────────

import json  # noqa: E402
import os  # noqa: E402
import sys  # noqa: E402
import tempfile  # noqa: E402
from collections.abc import AsyncIterator  # noqa: E402

from matrx_utils.cache import configure_cache, reset_cache_runtime, stop_cache_bus  # noqa: E402


class _RecordingBackend:
    """Shared tier that only records publishes (subscriptions stay silent)."""

    def __init__(self) -> None:
        self.published: list[tuple[str, dict]] = []

    async def get(self, key: str) -> bytes | None:
        return None

    async def set(self, key: str, value: bytes, ttl_ms: int) -> None:
        return None

    async def delete(self, *keys: str) -> None:
        return None

    async def delete_prefix(self, prefix: str) -> int:
        return 0

    async def publish(self, channel: str, message: bytes) -> None:
        self.published.append((channel, json.loads(message)))

    async def subscribe(self, channel: str) -> AsyncIterator[bytes]:
        yield b""
        await asyncio.sleep(3600)


@pytest_asyncio.fixture
async def recording_bus() -> AsyncIterator[_RecordingBackend]:
    backend = _RecordingBackend()
    reset_cache_runtime()
    configure_cache(backend=backend)
    yield backend
    await stop_cache_bus()
    reset_cache_runtime()


@pytest.mark.asyncio
async def test_only_process_fill_items_are_published_with_the_callers_identity(recording_bus) -> None:
    async def noop(_: str | None) -> None:
        return None

    warm.register_warmer("agent", noop, scope="shared", needs_id=True, fill="process")
    warm.register_warmer("core", noop, fill="shared")
    token = set_app_context(_ctx())
    try:
        result = warm.run_warm([{"key": "agent", "id": "a-9"}, {"key": "core"}])
    finally:
        clear_app_context(token)
    assert result.task is not None
    await result.task
    fanout = [m for ch, m in recording_bus.published if ch == warm.FANOUT_CHANNEL]
    assert len(fanout) == 1
    assert fanout[0]["items"] == [{"key": "agent", "id": "a-9"}], "a shared-cache warmer never fans out"
    assert fanout[0]["u"] == "person-a" and fanout[0]["g"] == ORG


@pytest.mark.asyncio
async def test_a_peer_message_runs_the_warmer_as_that_person_once_and_never_its_own() -> None:
    seen: list[tuple[str | None, str, str | None]] = []

    async def conversation(item_id: str | None) -> None:
        ctx = get_app_context()
        seen.append((item_id, str(ctx.user_id), str(ctx.organization_id)))

    async def catalogue(_: str | None) -> None:
        seen.append(("catalogue", "", None))

    warm.register_warmer("conversation", conversation, needs_id=True, fill="process")
    warm.register_warmer("core", catalogue, fill="shared")

    def message(origin: str) -> bytes:
        return json.dumps(
            {"o": origin, "u": "person-b", "g": ORG, "items": [{"key": "conversation", "id": "c-1"}, {"key": "core"}]}
        ).encode()

    warm._on_fanout(message(warm._PROCESS_ID))  # our own publish comes back: skipped
    warm._on_fanout(message("another-server"))
    warm._on_fanout(message("another-server"))  # same person, same item, inside the window
    for task in list(warm._background):
        await task
    assert seen == [("c-1", "person-b", ORG)]


_REAL_URL = os.environ.get("MATRX_CACHE_TEST_URL")

_PEER_SERVER = r"""
import asyncio, sys
from matrx_connect import warm
from matrx_connect.context.app_context import get_app_context
from matrx_utils.cache import channel_connected, configure_cache

url, out_path = sys.argv[1], sys.argv[2]

async def agent(item_id):
    ctx = get_app_context()
    with open(out_path, "a") as fh:
        fh.write(f"{item_id}|{ctx.user_id}|{ctx.organization_id}\n")

async def main():
    configure_cache(url=url)
    warm.register_warmer("agent", agent, scope="shared", needs_id=True, fill="process")
    warm.start_warm_fanout()
    for _ in range(100):
        if channel_connected(warm.FANOUT_CHANNEL):
            break
        await asyncio.sleep(0.05)
    print("ready", flush=True)
    await asyncio.sleep(float(sys.argv[3]))

asyncio.run(main())
"""


@pytest.mark.asyncio
@pytest.mark.skipif(not _REAL_URL, reason="set MATRX_CACHE_TEST_URL (e.g. docker run -p 6390:6379 valkey/valkey)")
async def test_real_valkey_a_warm_on_server_a_also_warms_server_b() -> None:
    assert _REAL_URL
    from matrx_utils.cache import channel_connected

    reset_cache_runtime()
    configure_cache(url=_REAL_URL)
    local_runs: list[str | None] = []

    async def agent(item_id: str | None) -> None:
        local_runs.append(item_id)

    warm.register_warmer("agent", agent, scope="shared", needs_id=True, fill="process")
    with tempfile.TemporaryDirectory() as scratch:
        out_path = os.path.join(scratch, "server_b.txt")
        peer = await asyncio.create_subprocess_exec(
            sys.executable, "-c", _PEER_SERVER, _REAL_URL, out_path, "4",
            stdout=asyncio.subprocess.PIPE,
        )
        try:
            assert peer.stdout is not None
            assert (await asyncio.wait_for(peer.stdout.readline(), 15)).strip() == b"ready"
            warm.start_warm_fanout()  # server A hears the channel too (and must skip its own)
            for _ in range(100):
                if channel_connected(warm.FANOUT_CHANNEL):
                    break
                await asyncio.sleep(0.05)
            token = set_app_context(_ctx())
            try:
                result = warm.run_warm([{"key": "agent", "id": "agent-42"}])
            finally:
                clear_app_context(token)
            assert result.task is not None
            await result.task
            for _ in range(60):
                if os.path.exists(out_path):
                    break
                await asyncio.sleep(0.05)
            await asyncio.sleep(0.3)  # an own-message re-run would land in this window
            with open(out_path) as fh:
                assert fh.read().splitlines() == [f"agent-42|person-a|{ORG}"], "server B ran it once, as the person"
            assert local_runs == ["agent-42"], "server A ran it once and skipped its own fan-out"
        finally:
            if peer.returncode is None:
                peer.kill()
            await peer.wait()
            await stop_cache_bus()
            reset_cache_runtime()


# ── review fixes: reason, abuse bound, shutdown ──────────────────────────────


@pytest.mark.asyncio
async def test_reason_and_keys_are_counted() -> None:
    async def noop(_: str | None) -> None:
        return None

    warm.register_warmer("core", noop)
    warm.register_warmer("agent", noop, scope="shared", needs_id=True)
    before = warm.warm_stats()
    token = set_app_context(_ctx())
    try:
        result = warm.run_warm([{"key": "core"}, {"key": "agent", "id": "a-1"}], reason="org_change")
    finally:
        clear_app_context(token)
    if result.task:
        await result.task
    after = warm.warm_stats()
    assert after["by_reason"].get("org_change", 0) == before["by_reason"].get("org_change", 0) + 1
    assert after["by_key"]["core"] == before["by_key"].get("core", 0) + 1
    assert after["by_key"]["agent"] == before["by_key"].get("agent", 0) + 1


@pytest.mark.asyncio
async def test_fresh_ids_past_the_per_minute_cap_neither_run_nor_fan_out() -> None:
    ran: list[str | None] = []

    async def conversation(item_id: str | None) -> None:
        ran.append(item_id)

    warm.register_warmer("conversation", conversation, needs_id=True, fill="process")
    token = set_app_context(_ctx())
    try:
        result = warm.run_warm(
            [{"key": "conversation", "id": f"c-{n}"} for n in range(8)], max_new_ids_per_minute=3
        )
        again = warm.run_warm([{"key": "conversation", "id": "c-99"}], max_new_ids_per_minute=3)
    finally:
        clear_app_context(token)
    assert result.task is not None
    await result.task
    assert sorted(ran) == ["c-0", "c-1", "c-2"]
    assert [i.id for i in result.limited] == [f"c-{n}" for n in range(3, 8)]
    assert [i.id for i in again.limited] == ["c-99"] and again.task is None
    # A limited id was never marked warmed: once the window allows, it runs.
    warm._new_ids.clear()
    token = set_app_context(_ctx())
    try:
        later = warm.run_warm([{"key": "conversation", "id": "c-5"}], max_new_ids_per_minute=3)
    finally:
        clear_app_context(token)
    assert later.task is not None and not later.throttled


@pytest.mark.asyncio
async def test_stop_warm_cancels_what_is_still_running() -> None:
    finished: list[str] = []

    async def slow(_: str | None) -> None:
        await asyncio.sleep(30)
        finished.append("slow")

    warm.register_warmer("core", slow, timeout_s=60)
    token = set_app_context(_ctx())
    try:
        result = warm.run_warm([{"key": "core"}])
    finally:
        clear_app_context(token)
    assert result.task is not None
    started = asyncio.get_running_loop().time()
    await warm.stop_warm(timeout_s=0.05)
    assert asyncio.get_running_loop().time() - started < 1.0
    assert result.task.done() and finished == []
