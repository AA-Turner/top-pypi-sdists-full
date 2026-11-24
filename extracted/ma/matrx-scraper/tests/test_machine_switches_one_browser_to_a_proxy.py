"""Switching ONE browser on a Cloud Computer to the paid exit (W7 §2.5).

The manager's switch is: stop the run's browser (``shutdown reason=moved``),
then bootstrap the SAME run again with ``LaunchPolicy.proxy`` + credentials.
On a machine hosting several browsers that must relaunch only that browser.

Breaks each test catches:
- the manager's shutdown word is refused by the S2 wire (2026-11-09 live:
  ``replaced`` failed to build and the browser never moved);
- A's re-bootstrap is refused (``already_bootstrapped`` / a new worker) instead
  of relaunching A in place;
- A relaunches but not through the proxy, or around the metered loopback
  (no bytes for the run's meter);
- A loses its profile (a cookie set before the switch is gone after it);
- B, on the same machine, is restarted, stopped or moved to the proxy.

Real Chromium (headless ``automation_only``) and a real upstream proxy on
loopback; no fakes of the worker itself.
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

import pytest

pytest.importorskip("playwright", reason="playwright not installed (browser extra)")

from matrx_scraper.cloud_browser.worker import BrowserWorker, StubControlPlane  # noqa: E402
from matrx_scraper.cloud_browser.worker import models as M  # noqa: E402
from matrx_scraper.cloud_browser.worker import runtime  # noqa: E402
from matrx_scraper.ai_browser import url_guard  # noqa: E402
from matrx_scraper.cloud_browser.worker.machine_browsers import MachineBrowsers  # noqa: E402

CHROMIUM = pytest.mark.skipif(
    not any(Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")).glob("chromium-*")),
    reason="no chromium browser binary",
)

#: The site A browses. It is never reached: the stand-in gateway answers for it.
SITE_HOST = "example.com"
#: On a NON-default port: Google Chrome (the worker's binary wherever the image ships it, as the CI
#: runner image does at /opt/google/chrome/chrome) upgrades a port-80 ``http://`` navigation to
#: ``https://`` (HTTPS-Upgrades), sending a CONNECT the plain-HTTP stand-in gateway cannot serve, and
#: the page failed ERR_BLOCKED_BY_CLIENT (nightly 2026-11-16 and 44130408582). Chrome never upgrades
#: an explicit non-default port, so the request reaches the gateway as plain HTTP on every binary.
SITE_URL = f"http://{SITE_HOST}:8080/"

PAGE = b"<html><head><title>through-the-paid-exit</title></head><body>ok</body></html>"


class _UpstreamProxy:
    """A forward proxy standing in for the paid gateway: answers every
    absolute-URL request itself and records the auth header it was sent."""

    def __init__(self) -> None:
        self.seen: list[tuple[str, str | None]] = []
        self.server: asyncio.AbstractServer | None = None
        self.port = 0

    async def start(self) -> None:
        self.server = await asyncio.start_server(self._handle, host="127.0.0.1", port=0)
        self.port = self.server.sockets[0].getsockname()[1]

    async def _handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            head = await reader.readuntil(b"\r\n\r\n")
            lines = head.decode("latin-1").split("\r\n")
            auth = next(
                (ln.split(":", 1)[1].strip() for ln in lines if ln.lower().startswith("proxy-authorization:")),
                None,
            )
            self.seen.append((lines[0], auth))
            writer.write(
                b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n"
                + f"Content-Length: {len(PAGE)}\r\n\r\n".encode()
                + PAGE
            )
            await writer.drain()
        except Exception:
            pass
        finally:
            writer.close()

    async def close(self) -> None:
        if self.server is not None:
            self.server.close()
            await self.server.wait_closed()


def _host() -> MachineBrowsers:
    def new() -> BrowserWorker:
        return BrowserWorker(worker_id="machine-worker")

    return MachineBrowsers(new(), factory=new, max_browsers=4)


async def _boot_through_proxy(stub: StubControlPlane, user_data_dir: str, proxy: str):  # noqa: ANN202
    """The manager's replacement bootstrap: same run, same activation, the
    paid grant on ``LaunchPolicy.proxy`` + credentials (worker_client.bootstrap)."""
    req = M.BootstrapRequest(
        **stub._env(sequenced=False),  # noqa: SLF001
        mount=M.ProfileMount(user_data_dir=user_data_dir, source="active_volume", profile_format_version=1),
        policy=M.LaunchPolicy(
            run_mode="automation_only",
            proxy=proxy,
            proxy_username="login",
            proxy_password="pw",
        ),
        activation_key=stub.activation_key,
        initial_fencing_token=stub.fencing_token,
        sequence_base=stub.sequence_base + 1,
        callback_url="stub://events",
        callback_token="cbt_switch",
    )
    response = await stub.worker.bootstrap(req)
    if response.ok and response.accepted:
        await stub.heartbeat()
    return response


@CHROMIUM
@pytest.mark.asyncio
async def test_switching_one_browser_relaunches_only_it_through_the_metered_proxy(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def loopback_allowed(_proxy):  # noqa: ANN001
        return None

    async def site_is_public(url: str) -> str:
        # The egress guard (url_guard.install_egress_guard) still runs on every
        # request; only its DNS lookup is answered here. Left to the runner's
        # resolver, a CI box that cannot resolve the site aborted the page with
        # ERR_BLOCKED_BY_CLIENT before it reached the proxy. The test never
        # touches the internet: the gateway below answers for the site.
        from urllib.parse import urlparse

        if urlparse(url).hostname != SITE_HOST:
            raise ValueError(f"not the test site: {url}")
        return url

    # The gate refuses a non-public proxy; the stand-in gateway is on loopback.
    monkeypatch.setattr(runtime, "guard_proxy", loopback_allowed)
    monkeypatch.setattr(url_guard, "validate_public_http_url", site_is_public)
    upstream = _UpstreamProxy()
    await upstream.start()
    host = _host()
    a = StubControlPlane(host, profile_id="prof_a")  # type: ignore[arg-type]
    b = StubControlPlane(host, profile_id="prof_b")  # type: ignore[arg-type]
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    try:
        assert (await a.bootstrap(user_data_dir=str(tmp_path / "a"))).accepted
        assert (await b.bootstrap(user_data_dir=str(tmp_path / "b"))).accepted
        worker_a, worker_b = host._route(a.run_id), host._route(b.run_id)  # noqa: SLF001
        await worker_a.context.add_cookies(
            [{"name": "session", "value": "kept", "domain": SITE_HOST, "path": "/",
              "expires": 4102444800}]
        )
        pid_a = runtime._profile_lock_holder(str(tmp_path / "a"))  # noqa: SLF001
        pid_b = runtime._profile_lock_holder(str(tmp_path / "b"))  # noqa: SLF001

        # 1. Stop A with the manager's word for "continues elsewhere".
        stopped = await a.shutdown(reason="moved")
        assert stopped.ok, stopped.error

        # 2. Re-bootstrap A through the paid exit.
        boot = await _boot_through_proxy(a, str(tmp_path / "a"), f"http://127.0.0.1:{upstream.port}")
        assert boot.accepted, boot.error
        assert host._route(a.run_id) is worker_a, "A relaunches in its own worker"  # noqa: SLF001
        assert len(host.workers) == 2
        holder_a = runtime._profile_lock_holder(str(tmp_path / "a"))  # noqa: SLF001
        if sys.platform.startswith("linux"):
            # Linux Chromium claims the profile with SingletonLock -> <host>-<pid>:
            # a relaunch is a NEW browser process holding A's profile.
            assert pid_a is not None and holder_a not in {None, pid_a}
        else:
            # Headless Chromium on macOS writes no SingletonLock, so there is no
            # holder before or after; the relaunch is proven by the page below.
            assert pid_a is None and holder_a is None

        # The session survived the relaunch (same profile directory).
        cookies = await worker_a.context.cookies("http://example.com/")
        assert {c["name"]: c["value"] for c in cookies}.get("session") == "kept"

        # 3. A's traffic leaves through the metered loopback to the gateway.
        page = worker_a.page_object(worker_a.active_page_id)
        await page.goto(SITE_URL, wait_until="load")
        assert await page.title() == "through-the-paid-exit"
        to_site = [(line, auth) for line, auth in upstream.seen if "example.com" in line]
        assert to_site, upstream.seen
        assert all(auth is not None and auth.startswith("Basic ") for _, auth in to_site)
        beat = await a.heartbeat()
        assert beat.ok and (beat.proxy_bytes or 0) > 0

        # 4. B: same Chrome, same exit, still serving.
        assert runtime._profile_lock_holder(str(tmp_path / "b")) == pid_b  # noqa: SLF001
        assert worker_b.proxy_bytes is None
        assert (await b.heartbeat()).ok
    finally:
        await host.terminate_gracefully(reason="test")
        await upstream.close()

