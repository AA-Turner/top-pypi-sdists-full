"""The worker's half of residential egress — the loopback adapter on the launch.

Contract: ``common-docs/systems/platform/residential-egress/FEATURE.md``.
The adapter itself (``matrx_scraper.egress_adapter.EgressAdapter``) is the
scraper's; what is proven here is the worker's contract WITH it: start it before
Chromium, launch through its loopback proxy, keep one adapter across the
live-checkpoint relaunch, close it on every exit, and never run the
public-routability gate against it.

The adapter is imported lazily inside ``_ensure_egress_adapter``, so these tests
install a recording stand-in at ``matrx_scraper.egress_adapter`` — which is also
why they keep working before that module lands.
"""

from __future__ import annotations

import sys
import types

import pytest

from matrx_scraper.cloud_browser.worker import models as M
from matrx_scraper.utils.proxy import playwright_proxy


class _RecordingAdapter:
    instances: list[_RecordingAdapter] = []

    def __init__(self, ticket: str, consume_url: str) -> None:
        self.ticket = ticket
        self.consume_url = consume_url
        self.proxy_url = f"http://127.0.0.1:{45000 + len(self.instances)}"
        self.closed = False

    @classmethod
    async def start(cls, ticket: str, consume_url: str) -> _RecordingAdapter:
        adapter = cls(ticket, consume_url)
        cls.instances.append(adapter)
        return adapter

    async def close(self) -> None:
        self.closed = True


@pytest.fixture
def recording_adapter(monkeypatch: pytest.MonkeyPatch):
    _RecordingAdapter.instances = []
    module = types.ModuleType("matrx_scraper.egress_adapter")
    module.EgressAdapter = _RecordingAdapter  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "matrx_scraper.egress_adapter", module)
    return _RecordingAdapter


def _worker():
    from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker

    return BrowserWorker.__new__(BrowserWorker)


def _blank(worker) -> None:  # noqa: ANN001
    worker._egress_adapter = None
    worker._egress_ticket = None
    worker.egress_device_name = None


def policy(**kw) -> M.LaunchPolicy:
    return M.LaunchPolicy(run_mode="automation_only", **kw)


EGRESS = {
    "ticket": "mxt_t1_secret",
    "consume_url": "wss://server.example/egress/consume",
    "device_name": "Arman's MacBook Pro",
}


@pytest.mark.asyncio
async def test_no_egress_policy_means_no_adapter(recording_adapter):
    worker = _worker()
    _blank(worker)

    assert await worker._ensure_egress_adapter(policy()) is None
    assert recording_adapter.instances == []


@pytest.mark.asyncio
async def test_the_launch_goes_through_the_adapters_loopback_proxy(recording_adapter):
    worker = _worker()
    _blank(worker)

    url = await worker._ensure_egress_adapter(policy(egress=EGRESS))

    assert len(recording_adapter.instances) == 1
    adapter = recording_adapter.instances[0]
    assert adapter.ticket == "mxt_t1_secret"
    assert adapter.consume_url == EGRESS["consume_url"]
    assert url == adapter.proxy_url
    assert url.startswith("http://127.0.0.1:")
    assert worker.egress_device_name == "Arman's MacBook Pro"


@pytest.mark.asyncio
async def test_the_same_ticket_reuses_one_adapter_across_a_relaunch(recording_adapter):
    """The live-checkpoint path closes and RELAUNCHES the context. Restarting the
    adapter there would need a ticket that may already have expired."""
    worker = _worker()
    _blank(worker)

    first = await worker._ensure_egress_adapter(policy(egress=EGRESS))
    second = await worker._ensure_egress_adapter(policy(egress=EGRESS))

    assert first == second
    assert len(recording_adapter.instances) == 1
    assert recording_adapter.instances[0].closed is False


@pytest.mark.asyncio
async def test_a_new_ticket_replaces_and_closes_the_old_adapter(recording_adapter):
    worker = _worker()
    _blank(worker)

    await worker._ensure_egress_adapter(policy(egress=EGRESS))
    await worker._ensure_egress_adapter(policy(egress={**EGRESS, "ticket": "mxt_t2_secret"}))

    assert len(recording_adapter.instances) == 2
    assert recording_adapter.instances[0].closed is True
    assert recording_adapter.instances[1].closed is False


@pytest.mark.asyncio
async def test_dropping_the_policy_stops_carrying_the_persons_traffic(recording_adapter):
    worker = _worker()
    _blank(worker)
    await worker._ensure_egress_adapter(policy(egress=EGRESS))

    assert await worker._ensure_egress_adapter(policy()) is None
    assert recording_adapter.instances[0].closed is True
    assert worker.egress_device_name is None


@pytest.mark.asyncio
async def test_close_is_idempotent_and_survives_a_broken_adapter(recording_adapter):
    """Every exit path calls it, including after a crash. It may never raise."""
    worker = _worker()
    _blank(worker)

    class _Broken(_RecordingAdapter):
        async def close(self) -> None:
            raise RuntimeError("socket already gone")

    worker._egress_adapter = _Broken("t", "wss://x")
    worker._egress_ticket = "t"
    await worker._close_egress_adapter()
    await worker._close_egress_adapter()

    assert worker._egress_adapter is None


def test_the_ticket_never_appears_in_a_repr():
    """The policy is logged through model reprs all over the worker."""
    assert "mxt_t1_secret" not in repr(policy(egress=EGRESS))
    assert "mxt_t1_secret" not in repr(policy(egress=EGRESS).egress)


# ── the credentialed-proxy gap this change also closed ──────────────────────


def test_a_credentialed_proxy_url_keeps_its_credentials():
    """🚨 Playwright strips ``user:password@`` from ``server`` WITHOUT moving it
    into username/password, so a credentialed proxy launched UNAUTHENTICATED and
    every page failed with a proxy 407 that named nothing. ``playwright_proxy``
    is the one translation and the worker now uses it."""
    options = playwright_proxy("http://bob:s3cr3t@proxy.example:8080")

    assert options == {
        "server": "http://proxy.example:8080",
        "username": "bob",
        "password": "s3cr3t",
    }


# ── the real ``_launch_context``, with Playwright stubbed at its own seam ────


class _FakePage:
    url = "about:blank"

    def on(self, *_args, **_kwargs) -> None:  # noqa: D102
        return None


class _FakeContext:
    browser = None

    def __init__(self) -> None:
        self.pages: list[_FakePage] = [_FakePage()]

    def on(self, *_args, **_kwargs) -> None:  # noqa: D102
        return None

    async def add_init_script(self, *_args, **_kwargs) -> None:  # noqa: D102
        return None


class _FakePlaywright:
    def __init__(self, recorder: dict) -> None:
        self._recorder = recorder
        self.chromium = self

    async def launch_persistent_context(self, **kwargs):  # noqa: ANN003, D102
        self._recorder.update(kwargs)
        return _FakeContext()

    async def stop(self) -> None:  # noqa: D102
        return None


async def _launch_and_capture(monkeypatch: pytest.MonkeyPatch, policy_in: M.LaunchPolicy) -> dict:
    """Run the REAL ``_launch_context`` and return the launch kwargs it built."""
    import playwright.async_api as pw_api

    from matrx_scraper.cloud_browser.worker import runtime as rt

    recorder: dict = {}

    class _Starter:
        async def start(self):  # noqa: ANN202
            return _FakePlaywright(recorder)

    monkeypatch.setattr(pw_api, "async_playwright", lambda: _Starter())
    monkeypatch.setattr(rt, "install_egress_guard", _noop_guard)

    worker = rt.BrowserWorker(worker_id="worker-egress-test")
    worker.run_mode = "automation_only"
    worker.run_id = "run-egress-test"
    worker._user_data_dir = "/tmp/egress-test-profile"
    await worker._launch_context(policy_in, None)
    return recorder


async def _noop_guard(_context) -> None:  # noqa: ANN001
    return None


@pytest.mark.asyncio
async def test_launch_context_really_hands_chromium_the_loopback_proxy(
    monkeypatch: pytest.MonkeyPatch, recording_adapter
):
    kwargs = await _launch_and_capture(monkeypatch, policy(egress=EGRESS))

    adapter = recording_adapter.instances[0]
    assert kwargs["proxy"] == {"server": adapter.proxy_url}


@pytest.mark.asyncio
async def test_launch_context_keeps_a_credentialed_proxys_credentials(
    monkeypatch: pytest.MonkeyPatch, recording_adapter
):
    kwargs = await _launch_and_capture(
        monkeypatch, policy(proxy="http://bob:s3cr3t@proxy.example:8080")
    )

    assert kwargs["proxy"] == {
        "server": "http://proxy.example:8080",
        "username": "bob",
        "password": "s3cr3t",
    }
    assert recording_adapter.instances == []
