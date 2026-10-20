"""A watched stream (view mode) stays up whoever drives, and only that long.

Owner rules (2026-10-17): viewing starts the picture without pausing the agent;
releasing control returns the same connection to watching instead of ending it.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from matrx_scraper.cloud_browser.worker import models as M
from matrx_scraper.cloud_browser.worker.http_app import create_worker_app
from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker


def _rtc() -> M.RtcConfig:
    return M.RtcConfig(
        iceServers=[M.RtcIceServer(urls=["turn:relay.example:3478"], username="u", credential="c")],
        expires_at=datetime.now(UTC) + timedelta(minutes=2),
    )


def _agent_driven_worker() -> BrowserWorker:
    worker = BrowserWorker(worker_id="worker-a")
    worker._bootstrapped = True
    worker.health = "healthy"
    worker.run_id = "run-a"
    worker.profile_id = "profile-a"
    worker.run_mode = "handoff_capable"
    worker.fencing_token = "fence-a"
    worker.fencing_revision = 1
    worker._lease_expires_at = datetime.now(UTC) + timedelta(minutes=1)
    worker.queue_state = "open"
    worker._controller = worker._controller.model_copy(
        update={"state": "agent_control", "controller_kind": "agent", "fencing_revision": 1}
    )
    return worker


def _heartbeat(**extra) -> M.HeartbeatRequest:  # noqa: ANN003
    return M.HeartbeatRequest(
        run_id="run-a",
        profile_id="profile-a",
        fencing_token="fence-a",
        fencing_revision=1,
        issued_at=datetime.now(UTC),
        lease_expires_at=datetime.now(UTC) + timedelta(minutes=1),
        access_still_valid=True,
        **extra,
    )


def test_a_viewer_heartbeat_starts_the_stream_while_the_agent_keeps_driving() -> None:
    worker = _agent_driven_worker()
    prepared: list[M.RtcConfig] = []
    worker.set_human_control_preparer(prepared.append)

    plain = asyncio.run(worker.heartbeat(_heartbeat(rtc_config=_rtc())))
    assert plain.ok and prepared == []  # no viewer: an agent-driven heartbeat never streams
    assert worker.view_stream_live is False

    watched = asyncio.run(worker.heartbeat(_heartbeat(rtc_config=_rtc(), stream_view_seconds=60)))

    assert watched.ok
    assert len(prepared) == 1
    assert worker.view_stream_live is True
    # Watching changed nothing about who drives.
    assert worker._controller.state == "agent_control"
    assert worker._controller.human_input_enabled is False
    assert worker.queue_state == "open"


def test_the_view_hold_lapses_on_its_own() -> None:
    worker = _agent_driven_worker()
    worker.set_human_control_preparer(lambda _rtc: None)
    asyncio.run(worker.heartbeat(_heartbeat(rtc_config=_rtc(), stream_view_seconds=60)))
    worker._view_stream_until = datetime.now(UTC) - timedelta(seconds=1)
    assert worker.view_stream_live is False


class _Stream:
    def __init__(self) -> None:
        self.calls: list[str] = []
        self.running = True

    def configure_rtc(self, _config) -> None:  # noqa: ANN001
        self.calls.append("configure")

    def clear_rtc(self) -> None:
        self.calls.append("clear")

    def start(self) -> None:
        self.calls.append("start")

    def stop(self) -> None:
        self.calls.append("stop")


class _ReturningWorker:
    """Answers a successful hop out of human control (input now disabled)."""

    worker_id = "worker-a"
    health = "healthy"
    chrome_downgrade = None

    def __init__(self, *, watched: bool) -> None:
        self.view_stream_live = watched

    def set_human_control_preparer(self, _callback, _clear=None) -> None:  # noqa: ANN001
        pass

    async def controller_transition(self, _request, *, bearer=None):  # noqa: ANN001
        return M.ControllerTransitionResponse(
            ok=True,
            queue_depth=0,
            queue_state="open",
            run_mode="handoff_capable",
            worker_health="healthy",
            chromium_version="test",
            worker_version="test",
            observed_at=datetime.now(UTC),
            run_id="run-a",
            profile_id="profile-a",
            worker_id="worker-a",
            controller=M.ControllerState(
                state="agent_control",
                controller_kind="agent",
                controller_ref=None,
                fencing_revision=4,
                handoff_id=None,
                since=datetime.now(UTC),
                human_input_enabled=False,
            ),
            fencing_revision=4,
            replayed=False,
            from_state="resume_pending",
            to_state="agent_control",
            human_input_enabled=False,
        )


_RETURN_BODY = {
    "run_id": "run-a",
    "profile_id": "profile-a",
    "fencing_token": "run-a:3",
    "fencing_revision": 3,
    "sequence": 7,
    "idempotency_key": "return-7",
    "issued_at": datetime.now(UTC).isoformat(),
    "to_state": "agent_control",
    "reason": "control_transition",
    "new_fencing_token": "run-a:4",
    "new_fencing_revision": 4,
    "enable_human_input": False,
}


@pytest.mark.parametrize(("watched", "stopped"), [(True, False), (False, True)])
def test_releasing_control_keeps_the_picture_only_while_someone_watches(watched, stopped) -> None:
    stream = _Stream()
    client = TestClient(create_worker_app(_ReturningWorker(watched=watched), stream=stream))

    response = client.post("/controller-transition", json=_RETURN_BODY)

    assert response.status_code == 200
    assert ("stop" in stream.calls) is stopped


def test_health_advertises_the_view_stream_capability() -> None:
    client = TestClient(create_worker_app(_ReturningWorker(watched=False), stream=_Stream()))
    assert client.get("/health").json()["stream_view"] is True
