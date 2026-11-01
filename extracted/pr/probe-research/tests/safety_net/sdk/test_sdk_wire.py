"""Pins every request one scripted SDK session sends: online, and offline then `probe sync`."""

# Order: writes are synchronous (an injected transport keeps `Client` on its sync path), so the
# fake sees call order; only the parallel multipart part PUTs are sorted (`in_stable_order`).
# Ambient capture stays as the suite's autouse fixtures pin it, since it reads this machine:
# PROBE_HW=0 PROBE_CAPTURE_READS=0 PROBE_CAPTURE_OUTPUTS=0 PROBE_AUTO_SNAPSHOT=0 (no code/git
# snapshot) PROBE_HEARTBEAT_SECONDS=0 PROBE_TELEMETRY=off.

from __future__ import annotations

from pathlib import Path

import pytest

from tests.conftest import FakeApp, make_client
from tests.safety_net.sdk.sdk_session import child_env, cli, close_open_runs, run_session
from tests.safety_net.sdk.wire_recording import recording
from tests.served_fake_app import serve


@pytest.fixture(autouse=True)
def _no_bound_run(monkeypatch):
    monkeypatch.delenv("PROBE_RUN_ID", raising=False)
    close_open_runs()
    yield
    close_open_runs()


@pytest.fixture
def literals(tmp_path) -> dict[str, str]:
    return {str(tmp_path): "<tmp_path>"}


@pytest.fixture
def multipart_app() -> FakeApp:
    app = FakeApp()
    app.supports_artifact_multipart = True  # the presigned-parts door for the large file
    return app


def test_online_session_sends_these_requests(multipart_app, tmp_path: Path, baseline, literals):
    client = make_client(multipart_app, tmp_spool=tmp_path / "outbox")
    run_session(tmp_path / "files", client=client)
    baseline("wire_online", recording(multipart_app.requests, literals))


def test_offline_session_then_probe_sync_sends_these_requests(
    multipart_app, tmp_path: Path, baseline, literals, monkeypatch
):
    with serve(multipart_app) as url:
        # `probe sync` refuses a queue recorded against another server.
        monkeypatch.setenv("PROBE_BASE_URL", url)
        multipart_app.upload_base = url  # presigned PUTs come back to the served fake
        run_session(tmp_path / "files", mode="offline")
        assert multipart_app.requests == [], "recording offline sends nothing"
        done = cli(["sync"], child_env(url, tmp_path), tmp_path)
        assert done.returncode == 0, done.stdout + done.stderr
        requests = list(multipart_app.requests)
    baseline("wire_offline_sync", recording(requests, {url: "<server>", **literals}))
