from __future__ import annotations

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import pytest
from fastapi.testclient import TestClient
from matrx_connect import ScopedTokenIssuer

from matrx_scraper.cloud_browser.worker.auth import Es256WorkerTokenVerifier
from matrx_scraper.cloud_browser.worker.errors import WorkerProtocolError
from matrx_scraper.cloud_browser.worker import http_app
from matrx_scraper.cloud_browser.worker.http_app import create_worker_app
from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker


def _issuer() -> ScopedTokenIssuer:
    key = ec.generate_private_key(ec.SECP256R1())
    pem = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode()
    return ScopedTokenIssuer(issuer="browser-manager", private_key_pem=pem)


def _mint(
    issuer: ScopedTokenIssuer, *, worker_id: str, op: str = "heartbeat", ttl: int = 60
) -> str:
    token, _ = issuer.mint(
        user_id="run:00000000-0000-0000-0000-000000000001",
        audience=f"worker:{worker_id}",
        tier_policy="none",
        ttl_seconds=ttl,
        extra_claims={
            "run_id": "00000000-0000-0000-0000-000000000001",
            "profile_id": "00000000-0000-0000-0000-000000000002",
            "mtx_op": op,
        },
    )
    return token


def test_public_key_verifier_accepts_once_and_rejects_replay() -> None:
    issuer = _issuer()
    verifier = Es256WorkerTokenVerifier("browser-manager", issuer.public_key_pem)
    token = _mint(issuer, worker_id="worker-a")

    credential = verifier.verify(token, worker_id="worker-a", op="heartbeat")
    assert credential.profile_id == "00000000-0000-0000-0000-000000000002"
    with pytest.raises(WorkerProtocolError, match="credential_replayed"):
        verifier.verify(token, worker_id="worker-a", op="heartbeat")


def test_public_key_verifier_rejects_wrong_worker_and_operation() -> None:
    issuer = _issuer()
    verifier = Es256WorkerTokenVerifier("browser-manager", issuer.public_key_pem)
    token = _mint(issuer, worker_id="worker-a")

    with pytest.raises(WorkerProtocolError, match="audience_mismatch"):
        verifier.verify(token, worker_id="worker-b", op="heartbeat")
    with pytest.raises(WorkerProtocolError, match="unauthorized_worker_call"):
        verifier.verify(token, worker_id="worker-a", op="shutdown")


def test_http_app_exposes_health_and_all_worker_operations() -> None:
    worker = BrowserWorker(worker_id="worker-a")
    client = TestClient(create_worker_app(worker))
    assert client.get("/health").json() == {
        "status": "starting",
        "worker_id": "worker-a",
        "stream_rtc_config": False,
    }
    paths = {route.path for route in client.app.routes}
    assert {
        "/bootstrap",
        "/heartbeat",
        "/command",
        "/observe",
        "/capture",
        "/controller-transition",
        "/checkpoint",
        "/shutdown",
    } <= paths


@pytest.mark.asyncio
async def test_sigterm_shutdown_failure_is_owned_and_still_chains_shutdown(monkeypatch) -> None:
    worker = BrowserWorker(worker_id="browser-worker-harbor-dental")
    previous_calls: list[int] = []

    async def fail_termination(*, reason: str) -> None:
        assert reason == "sigterm"
        raise OSError("profile volume became read-only")

    worker.terminate_gracefully = fail_termination  # type: ignore[method-assign]

    class Loop:
        callback = None

        def add_signal_handler(self, _signal, callback) -> None:  # noqa: ANN001
            self.callback = callback

        def create_task(self, coro, *, name=None):  # noqa: ANN001, ANN202
            return __import__("asyncio").create_task(coro, name=name)

        def remove_signal_handler(self, _signal) -> bool:  # noqa: ANN001
            return True

    loop = Loop()

    monkeypatch.setattr(http_app.asyncio, "get_running_loop", lambda: loop)
    monkeypatch.setattr(
        http_app.signal,
        "getsignal",
        lambda _signal: lambda signum, _frame: previous_calls.append(signum),
    )

    with pytest.raises(OSError, match="profile volume became read-only"):
        async with http_app._termination_lifespan(worker, None)(create_worker_app(worker)):
            assert loop.callback is not None
            loop.callback()

    assert previous_calls == [http_app.signal.SIGTERM]


def test_rtc_preparation_failure_refuses_before_fence_or_human_state_changes() -> None:
    """A failing config write must not create a durable-looking human driver."""
    from datetime import UTC, datetime, timedelta

    from matrx_scraper.cloud_browser.worker import models as M

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
        update={"state": "handoff_requested", "controller_kind": "none", "fencing_revision": 1}
    )

    def fail_prepare(_config: M.RtcConfig) -> None:
        raise OSError("read-only config path")

    worker.set_human_control_preparer(fail_prepare)
    request = M.ControllerTransitionRequest(
        run_id="run-a",
        profile_id="profile-a",
        fencing_token="fence-a",
        fencing_revision=1,
        sequence=10,
        idempotency_key="control-10",
        issued_at=datetime.now(UTC),
        to_state="human_control",
        reason="control_transition",
        new_fencing_token="run-a:2",
        new_fencing_revision=2,
        handoff_id="handoff-a",
        enable_human_input=True,
        rtc_config=M.RtcConfig(
            iceServers=[
                M.RtcIceServer(urls=["turn:relay.example:3478"], username="u", credential="c")
            ],
            expires_at=datetime.now(UTC) + timedelta(minutes=2),
        ),
    )

    response = __import__("asyncio").run(worker.controller_transition(request))

    assert response.ok is False
    assert response.error and response.error.code == "reopen_required"
    assert worker.fencing_revision == 1
    assert worker._controller.state == "handoff_requested"
    assert worker._controller.human_input_enabled is False
    assert worker._last_applied is None


def test_rtc_wire_models_never_reveal_ephemeral_turn_credentials_in_repr_or_validation() -> None:
    from datetime import UTC, datetime, timedelta

    from pydantic import ValidationError

    from matrx_scraper.cloud_browser.worker import models as M

    config = M.RtcConfig(
        iceServers=[
            M.RtcIceServer(
                urls=["turn:relay.example:3478"],
                username="ephemeral-user",
                credential="ephemeral-secret",
            )
        ],
        expires_at=datetime.now(UTC) + timedelta(minutes=2),
    )
    assert "ephemeral-user" not in repr(config)
    assert "ephemeral-secret" not in repr(config)
    with pytest.raises(ValidationError) as failure:
        M.RtcConfig.model_validate({"iceServers": [{"urls": []}], "expires_at": "not-a-date"})
    assert "ephemeral-user" not in str(failure.value)
    assert "ephemeral-secret" not in str(failure.value)


def test_http_wrapper_does_not_start_replayed_human_media_after_ack() -> None:
    """A retried durable transition is successful only when media is actually live."""
    from datetime import UTC, datetime

    from matrx_scraper.cloud_browser.worker import models as M

    class Stream:
        def __init__(self) -> None:
            self.calls: list[str] = []

        def configure_rtc(self, _config) -> None:  # noqa: ANN001
            self.calls.append("configure")

        def clear_rtc(self) -> None:
            self.calls.append("clear")

        def start(self) -> None:
            self.calls.append("start")

        def stop(self) -> None:
            self.calls.append("stop")

    class ReplayingWorker:
        worker_id = "worker-a"
        health = "healthy"

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
                    state="human_control",
                    controller_kind="human",
                    controller_ref=None,
                    fencing_revision=2,
                    handoff_id="h-1",
                    since=datetime.now(UTC),
                    human_input_enabled=True,
                ),
                fencing_revision=2,
                replayed=True,
                from_state="human_control",
                to_state="human_control",
                human_input_enabled=True,
            )

    stream = Stream()
    client = TestClient(create_worker_app(ReplayingWorker(), stream=stream))
    response = client.post(
        "/controller-transition",
        json={
            "run_id": "run-a",
            "profile_id": "profile-a",
            "fencing_token": "run-a:1",
            "fencing_revision": 1,
            "sequence": 2,
            "idempotency_key": "same-transition",
            "issued_at": datetime.now(UTC).isoformat(),
            "to_state": "human_control",
            "reason": "control_transition",
            "new_fencing_token": "run-a:2",
            "new_fencing_revision": 2,
            "handoff_id": "h-1",
            "enable_human_input": True,
            "rtc_config": {
                "iceServers": [
                    {"urls": ["turn:relay.example:3478"], "username": "u", "credential": "c"}
                ],
                "expires_at": datetime.now(UTC).isoformat(),
            },
        },
    )

    assert response.status_code == 200
    assert stream.calls == []


@pytest.mark.asyncio
async def test_cancelled_rtc_preparation_keeps_observe_behind_the_control_gate() -> None:
    """A cancelled request cannot unlock while its thread can still start media."""
    import asyncio
    import threading
    from datetime import UTC, datetime, timedelta

    from matrx_scraper.cloud_browser.worker import models as M

    worker = BrowserWorker(worker_id="worker-a")
    worker._bootstrapped = True
    worker.health = "healthy"
    worker.run_id, worker.profile_id = "run-a", "profile-a"
    worker.run_mode, worker.fencing_token, worker.fencing_revision = "handoff_capable", "fence-a", 1
    worker._lease_expires_at = datetime.now(UTC) + timedelta(minutes=1)
    worker.queue_state = "open"
    worker._controller = worker._controller.model_copy(
        update={"state": "handoff_requested", "controller_kind": "none", "fencing_revision": 1}
    )
    started, release = threading.Event(), threading.Event()
    cleanup: list[str] = []

    def blocked_prepare(_config: M.RtcConfig) -> None:
        started.set()
        assert release.wait(2)

    worker.set_human_control_preparer(blocked_prepare, lambda: cleanup.append("cleared"))
    transition = M.ControllerTransitionRequest(
        run_id="run-a",
        profile_id="profile-a",
        fencing_token="fence-a",
        fencing_revision=1,
        sequence=10,
        idempotency_key="control-10",
        issued_at=datetime.now(UTC),
        to_state="human_control",
        reason="control_transition",
        new_fencing_token="run-a:2",
        new_fencing_revision=2,
        handoff_id="handoff-a",
        enable_human_input=True,
        rtc_config=M.RtcConfig(
            iceServers=[M.RtcIceServer(urls=["turn:relay:3478"])],
            expires_at=datetime.now(UTC) + timedelta(minutes=2),
        ),
    )
    task = asyncio.create_task(worker.controller_transition(transition))
    await asyncio.wait_for(asyncio.to_thread(started.wait), timeout=1)
    observe = asyncio.create_task(
        worker.observe(
            M.ObserveRequest(
                run_id="run-a",
                profile_id="profile-a",
                fencing_token="fence-a",
                fencing_revision=1,
                issued_at=datetime.now(UTC),
                include=["pages"],
            )
        )
    )
    await asyncio.sleep(0)
    assert not observe.done()
    task.cancel()
    release.set()
    with pytest.raises(asyncio.CancelledError):
        await task
    snapshot = await observe
    assert snapshot.controller.state == "handoff_requested"
    assert worker.fencing_revision == 1
    assert cleanup == ["cleared"]


@pytest.mark.asyncio
async def test_replayed_human_transition_with_failed_media_restart_never_reports_human_ready() -> (
    None
):
    """Cached controller receipts are not valid if their fresh RTC startup fails."""
    from datetime import UTC, datetime, timedelta

    from matrx_scraper.cloud_browser.worker import models as M

    worker = BrowserWorker(worker_id="worker-a")
    worker._bootstrapped = True
    worker.health = "healthy"
    worker.run_id, worker.profile_id = "run-a", "profile-a"
    worker.run_mode, worker.fencing_token, worker.fencing_revision = "handoff_capable", "run-a:2", 2
    worker._lease_expires_at = datetime.now(UTC) + timedelta(minutes=1)
    worker.queue_state = "open"
    worker._controller = worker._controller.model_copy(
        update={
            "state": "human_control",
            "controller_kind": "human",
            "handoff_id": "h-1",
            "fencing_revision": 2,
            "human_input_enabled": True,
        }
    )
    request = M.ControllerTransitionRequest(
        run_id="run-a",
        profile_id="profile-a",
        fencing_token="run-a:2",
        fencing_revision=2,
        sequence=10,
        idempotency_key="cached",
        issued_at=datetime.now(UTC),
        to_state="human_control",
        reason="control_transition",
        new_fencing_token="run-a:2",
        new_fencing_revision=2,
        handoff_id="h-1",
        enable_human_input=True,
        rtc_config=M.RtcConfig(
            iceServers=[M.RtcIceServer(urls=["turn:relay:3478"])],
            expires_at=datetime.now(UTC) + timedelta(minutes=2),
        ),
    )
    cached = M.ControllerTransitionResponse(
        **worker._reply_kwargs(),
        ok=True,
        sequence_applied=10,
        from_state="human_control",
        to_state="human_control",
        human_input_enabled=True,
    )
    worker._replay[(10, "cached")] = cached
    worker._seq_keys[10] = "cached"
    worker._last_applied = 10
    worker.set_human_control_preparer(lambda _rtc: (_ for _ in ()).throw(OSError("stream down")))

    response = await worker.controller_transition(request)

    assert response.ok is False and response.error and response.error.code == "worker_degraded"
    assert worker.health == "degraded"
    assert worker.queue_state == "closed"
    assert worker._controller.state == "failed"
    assert worker._controller.human_input_enabled is False


@pytest.mark.asyncio
async def test_new_sequence_same_revision_replay_requires_rtc_ready() -> None:
    from datetime import UTC, datetime, timedelta
    from matrx_scraper.cloud_browser.worker import models as M

    worker = BrowserWorker(worker_id="worker-a")
    worker._bootstrapped, worker.health = True, "healthy"
    worker.run_id, worker.profile_id, worker.run_mode = "run-a", "profile-a", "handoff_capable"
    worker.fencing_token, worker.fencing_revision = "run-a:2", 2
    worker._lease_expires_at, worker.queue_state = datetime.now(UTC) + timedelta(minutes=1), "open"
    worker._controller = worker._controller.model_copy(
        update={
            "state": "human_control",
            "controller_kind": "human",
            "fencing_revision": 2,
            "human_input_enabled": True,
        }
    )
    worker.set_human_control_preparer(lambda _rtc: (_ for _ in ()).throw(OSError("dead stream")))
    request = M.ControllerTransitionRequest(
        run_id="run-a",
        profile_id="profile-a",
        fencing_token="run-a:2",
        fencing_revision=2,
        sequence=11,
        idempotency_key="new-replay",
        issued_at=datetime.now(UTC),
        to_state="human_control",
        reason="control_transition",
        new_fencing_token="run-a:2",
        new_fencing_revision=2,
        enable_human_input=True,
        rtc_config=M.RtcConfig(
            iceServers=[M.RtcIceServer(urls=["turn:relay:3478"])],
            expires_at=datetime.now(UTC) + timedelta(minutes=2),
        ),
    )
    response = await worker.controller_transition(request)
    assert (
        response.ok is False
        and worker.health == "degraded"
        and worker._controller.human_input_enabled is False
    )
