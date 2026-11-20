# ruff: file-ignore[unused-function-argument, hardcoded-password-func-arg, unused-async, missing-blank-line-after-summary, multiple-starts-ends-with]
"""Tests for JobClient v0.2 object-storage write paths."""

from __future__ import annotations

import gzip
import json
from collections.abc import Callable, Coroutine
from uuid import UUID, uuid4

import httpx
import pytest
from aviary.env import Frame
from tenacity import RetryError

from edison_client.clients.job_client import JobClient
from edison_client.models.app import Stage


@pytest.fixture(name="trajectory_id")
def fixture_trajectory_id() -> str:
    return str(uuid4())


@pytest.fixture(autouse=True)
def fixture_no_retry_backoff(monkeypatch: pytest.MonkeyPatch) -> None:
    """Skip tenacity's backoff so exhausting JobClient's retries stays fast."""

    async def no_sleep(_seconds: float) -> None:
        return None

    for method in (
        JobClient._post_state_init,
        JobClient._put_state_blob,
        JobClient._post_state_finalize,
        JobClient._store_agent_state_inline,
        JobClient._store_environment_frame_inline,
    ):
        monkeypatch.setattr(method.retry, "sleep", no_sleep)  # ty: ignore[missing-attribute]


@pytest.fixture(name="job_client")
def fixture_job_client(trajectory_id: str) -> JobClient:
    return JobClient(
        environment="test_env",
        agent="test_agent",
        auth_token="test-token",
        base_uri=Stage.LOCAL.value,
        trajectory_id=trajectory_id,
    )


def _patch_httpx_aiohttp(
    monkeypatch: pytest.MonkeyPatch, transport: httpx.MockTransport
) -> None:
    """Swap ``HttpxAiohttpClient`` with a vanilla ``httpx.AsyncClient`` wired
    to ``transport`` so tests can mock the network without spinning up aiohttp.
    """

    def factory(*args: object, **kwargs: object) -> httpx.AsyncClient:
        kwargs.pop("timeout", None)
        return httpx.AsyncClient(transport=transport, timeout=10.0)

    monkeypatch.setattr(
        "edison_client.clients.job_client.httpx_aiohttp.HttpxAiohttpClient", factory
    )


class _Recorder:
    """Captures every request the client makes for later assertion."""

    def __init__(self) -> None:
        self.requests: list[httpx.Request] = []

    def handler(
        self, init_response_id: UUID
    ) -> Callable[[httpx.Request], Coroutine[None, None, httpx.Response]]:
        async def _read(request: httpx.Request) -> bytes:
            await request.aread()
            return request.content

        async def handle(request: httpx.Request) -> httpx.Response:
            await _read(request)
            self.requests.append(request)
            url = str(request.url)
            if "/v0.2/" in url and url.endswith("/finalize"):
                return httpx.Response(204)
            if "/v0.2/" in url and (
                url.endswith("/agent-state") or url.endswith("/environment-frame")
            ):
                return httpx.Response(
                    201,
                    json={
                        "id": str(init_response_id),
                        "upload_url": "https://signed.example/upload",
                        "object_path": "trajectories/x/agent-state/y.json.gz",
                        "expires_in_seconds": 3600,
                    },
                )
            if request.url.host == "signed.example":
                return httpx.Response(200)
            return httpx.Response(500, json={"detail": "unmatched in test"})

        return handle


@pytest.mark.asyncio
async def test_store_agent_state_runs_init_upload_finalize(
    monkeypatch: pytest.MonkeyPatch,
    job_client: JobClient,
    trajectory_id: str,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Happy path: three legs in order, payload gzipped on the upload."""
    state_id = uuid4()
    recorder = _Recorder()
    transport = httpx.MockTransport(recorder.handler(state_id))
    _patch_httpx_aiohttp(monkeypatch, transport)
    caplog.set_level("INFO", logger="edison_client.utils.monitoring")

    state = {"transition": {"timestep": 7, "agent_state": {"messages": ["hi"]}}}
    await job_client.store_agent_state(step="after_transition", state=state)

    assert len(recorder.requests) == 3
    init_req, upload_req, finalize_req = (
        recorder.requests[0],
        recorder.requests[1],
        recorder.requests[2],
    )

    # Leg 1: init carries metadata only, no state body
    assert init_req.method == "POST"
    assert init_req.url.path == f"/v0.2/trajectories/{trajectory_id}/agent-state"
    init_body = json.loads(init_req.content)
    assert init_body["agent_id"] == "test_agent"
    assert init_body["step"] == "after_transition"
    assert init_body["trajectory_timestep"] == 7
    assert init_body["content_encoding"] == "gzip"
    assert "state" not in init_body

    # Leg 2: PUT to signed URL with gzipped JSON
    assert upload_req.method == "PUT"
    assert str(upload_req.url) == "https://signed.example/upload"
    assert upload_req.headers["content-encoding"] == "gzip"
    # Auth must NOT leak to the signed URL — GCS / S3 reject Bearer tokens.
    assert "authorization" not in {k.lower() for k in upload_req.headers}
    decompressed = gzip.decompress(upload_req.content)
    # The blob is the bare state — GET readers splice it verbatim into the
    # row's ``state`` field, so any request-envelope wrapper would come
    # back double-nested. Envelope metadata travels in the init leg.
    assert json.loads(decompressed) == state

    # Leg 3: finalize, idempotent
    assert finalize_req.method == "POST"
    assert finalize_req.url.path.endswith(f"/agent-state/{state_id}/finalize")

    timings = {
        timing["operation"]: timing
        for record in caplog.records
        if record.getMessage().startswith("ROLLOUT_TIMING ")
        for timing in [json.loads(record.getMessage().removeprefix("ROLLOUT_TIMING "))]
    }
    assert all(t["trajectory_id"] == trajectory_id for t in timings.values())
    assert all(t["timestep"] == 7 and t["completed"] for t in timings.values())
    upload_timing = timings["store_agent_state.upload"]
    assert upload_timing["raw_bytes"] == len(decompressed)
    assert upload_timing["compressed_bytes"] == len(upload_req.content)
    assert (
        0
        <= timings["gzip"]["elapsed_seconds"]
        <= timings["agent_state.serialize_compress"]["elapsed_seconds"]
    )


@pytest.mark.asyncio
async def test_environment_frame_requires_agent_step(job_client: JobClient) -> None:
    with pytest.raises(ValueError, match="agent step"):
        await job_client.store_environment_frame(Frame())


@pytest.mark.asyncio
async def test_store_environment_frame_runs_init_upload_finalize(
    monkeypatch: pytest.MonkeyPatch, job_client: JobClient, trajectory_id: str
) -> None:
    frame_id = uuid4()
    recorder = _Recorder()
    transport = httpx.MockTransport(recorder.handler(frame_id))
    _patch_httpx_aiohttp(monkeypatch, transport)

    job_client.current_step = "after_transition"
    job_client.current_timestep = 3

    frame = Frame(state={"observation": "hello"})
    await job_client.store_environment_frame(state=frame)

    assert len(recorder.requests) == 3
    init_req, upload_req, finalize_req = (
        recorder.requests[0],
        recorder.requests[1],
        recorder.requests[2],
    )

    assert init_req.url.path == (
        f"/v0.2/trajectories/{trajectory_id}/environment-frame"
    )
    init_body = json.loads(init_req.content)
    assert init_body["agent_state_point_in_time"] == "test_agent-after_transition-3"
    assert init_body["current_agent_step"] == "after_transition"
    assert init_body["trajectory_timestep"] == 3
    assert init_body["content_encoding"] == "gzip"

    assert upload_req.method == "PUT"
    # Bare frame dump, no request-envelope wrapper (see agent-state test).
    assert json.loads(gzip.decompress(upload_req.content)) == frame.model_dump(
        mode="json"
    )

    assert finalize_req.url.path.endswith(f"/environment-frame/{frame_id}/finalize")


@pytest.mark.asyncio
async def test_store_agent_state_propagates_init_failure(
    monkeypatch: pytest.MonkeyPatch,
    job_client: JobClient,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """If init keeps returning 5xx, the per-leg @retry exhausts its attempts
    and the exception propagates to the caller.
    """

    async def always_500(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"detail": "boom"})

    transport = httpx.MockTransport(always_500)
    _patch_httpx_aiohttp(monkeypatch, transport)
    caplog.set_level("INFO", logger="edison_client.utils.monitoring")

    # Tenacity wraps the final exception once attempts are exhausted.
    with pytest.raises(RetryError) as excinfo:
        await job_client.store_agent_state(step="step", state={"k": "v"})
    assert isinstance(excinfo.value.last_attempt.exception(), httpx.HTTPStatusError)

    timings = [
        json.loads(record.getMessage().removeprefix("ROLLOUT_TIMING "))
        for record in caplog.records
        if record.getMessage().startswith("ROLLOUT_TIMING ")
    ]
    init_timing = next(t for t in timings if t["operation"] == "store_agent_state.init")
    assert not init_timing["completed"]
    assert init_timing["trajectory_id"] == job_client.trajectory_id


@pytest.mark.asyncio
async def test_store_agent_state_does_not_retry_client_errors(
    monkeypatch: pytest.MonkeyPatch, job_client: JobClient
) -> None:
    """4xx responses are final: no retry, no orphan re-init, original error."""
    requests: list[httpx.Request] = []

    async def always_403(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(403, json={"detail": "nope"})

    transport = httpx.MockTransport(always_403)
    _patch_httpx_aiohttp(monkeypatch, transport)

    with pytest.raises(httpx.HTTPStatusError):
        await job_client.store_agent_state(step="step", state={"k": "v"})
    assert len(requests) == 1


@pytest.mark.asyncio
async def test_store_agent_state_retries_proxy_error_without_reinit(
    monkeypatch: pytest.MonkeyPatch, job_client: JobClient
) -> None:
    """A proxy failure retries the same blob PUT without restarting the save."""
    state_id = uuid4()
    recorder = _Recorder()
    base_handle = recorder.handler(state_id)
    upload_attempts = 0

    async def handle(request: httpx.Request) -> httpx.Response:
        nonlocal upload_attempts
        response = await base_handle(request)
        if request.method == "PUT":
            upload_attempts += 1
            if upload_attempts == 1:
                raise httpx.ProxyError("503 Service Unavailable", request=request)
        return response

    _patch_httpx_aiohttp(monkeypatch, httpx.MockTransport(handle))
    state = {"transition": {"timestep": 7, "agent_state": {"messages": ["hi"]}}}

    await job_client.store_agent_state(step="after_transition", state=state)

    assert [r.method for r in recorder.requests] == ["POST", "PUT", "PUT", "POST"]
    init_req = recorder.requests[0]
    first_upload = recorder.requests[1]
    second_upload = recorder.requests[2]
    finalize_req = recorder.requests[3]
    assert init_req.url.path.endswith("/agent-state")
    assert str(first_upload.url) == "https://signed.example/upload"
    assert first_upload.url == second_upload.url
    assert first_upload.content == second_upload.content
    assert json.loads(gzip.decompress(second_upload.content)) == state
    assert finalize_req.url.path.endswith(f"/agent-state/{state_id}/finalize")


@pytest.mark.asyncio
async def test_store_agent_state_exhausts_proxy_error_retries(
    monkeypatch: pytest.MonkeyPatch, job_client: JobClient
) -> None:
    """Persistent proxy errors fail after the existing upload retry budget."""
    recorder = _Recorder()
    base_handle = recorder.handler(uuid4())

    async def handle(request: httpx.Request) -> httpx.Response:
        response = await base_handle(request)
        if request.method == "PUT":
            raise httpx.ProxyError("503 Service Unavailable", request=request)
        return response

    _patch_httpx_aiohttp(monkeypatch, httpx.MockTransport(handle))

    with pytest.raises(RetryError) as excinfo:
        await job_client.store_agent_state(step="after_transition", state={"k": "v"})

    assert isinstance(excinfo.value.last_attempt.exception(), httpx.ProxyError)
    expected_methods = ["POST"] + ["PUT"] * JobClient.MAX_RETRY_ATTEMPTS
    assert [r.method for r in recorder.requests] == expected_methods


@pytest.mark.asyncio
async def test_store_agent_state_retries_finalize_without_reinit(
    monkeypatch: pytest.MonkeyPatch, job_client: JobClient
) -> None:
    """A transient finalize failure retries just that leg — the init result
    is reused, so no second PENDING row and no blob re-upload.
    """
    state_id = uuid4()
    counts = {"init": 0, "upload": 0, "finalize": 0}

    async def handle(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if "/v0.2/" in url and url.endswith("/finalize"):
            counts["finalize"] += 1
            if counts["finalize"] == 1:
                return httpx.Response(503, json={"detail": "blip"})
            return httpx.Response(204)
        if "/v0.2/" in url and url.endswith("/agent-state"):
            counts["init"] += 1
            return httpx.Response(
                201,
                json={
                    "id": str(state_id),
                    "upload_url": "https://signed.example/upload",
                    "object_path": "trajectories/x/agent-state/y.json.gz",
                    "expires_in_seconds": 3600,
                },
            )
        if request.url.host == "signed.example":
            counts["upload"] += 1
            return httpx.Response(200)
        return httpx.Response(500, json={"detail": "unmatched in test"})

    transport = httpx.MockTransport(handle)
    _patch_httpx_aiohttp(monkeypatch, transport)

    await job_client.store_agent_state(step="step", state={"k": "v"})

    assert counts == {"init": 1, "upload": 1, "finalize": 2}


@pytest.mark.asyncio
async def test_store_agent_state_retries_init_on_429(
    monkeypatch: pytest.MonkeyPatch, job_client: JobClient
) -> None:
    """A 429 (e.g. Cloud Run with no free instance) is transient: init retries."""
    state_id = uuid4()
    counts = {"init": 0, "upload": 0, "finalize": 0}

    async def handle(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if "/v0.2/" in url and url.endswith("/finalize"):
            counts["finalize"] += 1
            return httpx.Response(204)
        if "/v0.2/" in url and url.endswith("/agent-state"):
            counts["init"] += 1
            if counts["init"] == 1:
                return httpx.Response(429, text="Rate exceeded.")
            return httpx.Response(
                201,
                json={
                    "id": str(state_id),
                    "upload_url": "https://signed.example/upload",
                    "object_path": "trajectories/x/agent-state/y.json.gz",
                    "expires_in_seconds": 3600,
                },
            )
        if request.url.host == "signed.example":
            counts["upload"] += 1
            return httpx.Response(200)
        return httpx.Response(500, json={"detail": "unmatched in test"})

    transport = httpx.MockTransport(handle)
    _patch_httpx_aiohttp(monkeypatch, transport)

    await job_client.store_agent_state(step="step", state={"k": "v"})

    assert counts == {"init": 2, "upload": 1, "finalize": 1}


@pytest.mark.asyncio
async def test_store_agent_state_init_carries_stable_idempotency_id(
    monkeypatch: pytest.MonkeyPatch, job_client: JobClient
) -> None:
    """A retried init resends the same client-supplied ``id`` so the server
    can dedupe it instead of orphaning a duplicate PENDING row.
    """
    state_id = uuid4()
    init_ids: list[str] = []

    async def handle(request: httpx.Request) -> httpx.Response:
        await request.aread()
        url = str(request.url)
        if "/v0.2/" in url and url.endswith("/agent-state"):
            init_ids.append(json.loads(request.content)["id"])
            if len(init_ids) == 1:
                return httpx.Response(503, json={"detail": "blip"})
            return httpx.Response(
                201,
                json={
                    "id": str(state_id),
                    "upload_url": "https://signed.example/upload",
                    "object_path": "trajectories/x/agent-state/y.json.gz",
                    "expires_in_seconds": 3600,
                },
            )
        if "/v0.2/" in url and url.endswith("/finalize"):
            return httpx.Response(204)
        if request.url.host == "signed.example":
            return httpx.Response(200)
        return httpx.Response(500, json={"detail": "unmatched in test"})

    transport = httpx.MockTransport(handle)
    _patch_httpx_aiohttp(monkeypatch, transport)

    await job_client.store_agent_state(step="step", state={"k": "v"})

    # Two init attempts (one 503, one 201), both carrying the same id.
    assert len(init_ids) == 2
    assert init_ids[0] == init_ids[1]
    assert UUID(init_ids[0]).version == 4  # well-formed uuid4


@pytest.mark.asyncio
async def test_store_agent_state_falls_back_to_v0d1_when_unsupported(
    monkeypatch: pytest.MonkeyPatch, job_client: JobClient, trajectory_id: str
) -> None:
    """A 404 on init means the server predates v0.2: the state goes out via
    the inline v0.1 endpoint instead, and subsequent stores skip the v0.2
    init round-trip entirely (the flag is sticky).
    """
    requests: list[httpx.Request] = []

    async def handle(request: httpx.Request) -> httpx.Response:
        await request.aread()
        requests.append(request)
        if "/v0.2/" in str(request.url):
            return httpx.Response(404, json={"detail": "Not Found"})
        assert request.url.path == f"/v0.1/trajectories/{trajectory_id}/agent-state"
        return httpx.Response(201, json=str(uuid4()))

    transport = httpx.MockTransport(handle)
    _patch_httpx_aiohttp(monkeypatch, transport)

    state = {"k": "v"}
    await job_client.store_agent_state(step="step", state=state)

    assert [r.url.path for r in requests] == [
        f"/v0.2/trajectories/{trajectory_id}/agent-state",
        f"/v0.1/trajectories/{trajectory_id}/agent-state",
    ]
    # The v0.1 body is the full request envelope (that's the v0.1 contract).
    inline_body = json.loads(gzip.decompress(requests[-1].content))
    assert inline_body["state"] == state
    assert inline_body["agent_id"] == "test_agent"

    # Second store: straight to v0.1, no v0.2 init attempt.
    await job_client.store_agent_state(step="step2", state=state)
    assert requests[-1].url.path == f"/v0.1/trajectories/{trajectory_id}/agent-state"
    assert all("/v0.2/" not in str(r.url) for r in requests[2:])


@pytest.mark.asyncio
async def test_small_state_posts_use_request_timeout(
    monkeypatch: pytest.MonkeyPatch, job_client: JobClient
) -> None:
    """Init and finalize use the short REQUEST_TIMEOUT, so one slow attempt
    against crow-service leaves room for retries.
    """
    read_timeouts: dict[str, float] = {}

    async def handle(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        timeout = request.extensions["timeout"]["read"]
        if "/v0.2/" in url and url.endswith("/finalize"):
            read_timeouts["finalize"] = timeout
            return httpx.Response(204)
        if "/v0.2/" in url and url.endswith("/agent-state"):
            read_timeouts["init"] = timeout
            return httpx.Response(
                201,
                json={
                    "id": str(uuid4()),
                    "upload_url": "https://signed.example/upload",
                    "object_path": "trajectories/x/agent-state/y.json.gz",
                    "expires_in_seconds": 3600,
                },
            )
        return httpx.Response(200)

    _patch_httpx_aiohttp(monkeypatch, httpx.MockTransport(handle))

    await job_client.store_agent_state(step="step", state={"k": "v"})

    assert read_timeouts == {
        "init": JobClient.REQUEST_TIMEOUT,
        "finalize": JobClient.REQUEST_TIMEOUT,
    }


@pytest.mark.asyncio
async def test_inline_agent_state_keeps_smaller_retry_budget(
    monkeypatch: pytest.MonkeyPatch, job_client: JobClient
) -> None:
    """Inline v0.1 POSTs have no idempotency key, so they retry at most
    INLINE_MAX_RETRY_ATTEMPTS times rather than the larger v0.2 budget.
    """
    inline_attempts = 0

    async def handle(request: httpx.Request) -> httpx.Response:
        nonlocal inline_attempts
        if "/v0.2/" in str(request.url):
            return httpx.Response(404, json={"detail": "Not Found"})
        inline_attempts += 1
        return httpx.Response(503, json={"detail": "blip"})

    _patch_httpx_aiohttp(monkeypatch, httpx.MockTransport(handle))

    with pytest.raises(RetryError):
        await job_client.store_agent_state(step="step", state={"k": "v"})
    assert inline_attempts == JobClient.INLINE_MAX_RETRY_ATTEMPTS


@pytest.mark.asyncio
async def test_application_404_does_not_disable_object_store(
    monkeypatch: pytest.MonkeyPatch, job_client: JobClient, trajectory_id: str
) -> None:
    """A v0.2 init 404 whose body is an application error (e.g. the trajectory
    does not exist yet) is a real failure, not a "no v0.2 routes" signal: it
    re-raises, leaves ``_object_store_supported`` set, and never falls back to
    the inline v0.1 path. A later store still attempts the v0.2 init, so the
    trajectory appearing recovers the object-store path.
    """
    state_id = uuid4()
    recorder = _Recorder()
    trajectory_missing = True

    base_handle = recorder.handler(state_id)

    async def handle(request: httpx.Request) -> httpx.Response:
        await request.aread()
        url = str(request.url)
        if trajectory_missing and url.endswith(f"/{trajectory_id}/agent-state"):
            recorder.requests.append(request)
            return httpx.Response(
                404, json={"detail": f"Trajectory not found ({trajectory_id})"}
            )
        return await base_handle(request)

    transport = httpx.MockTransport(handle)
    _patch_httpx_aiohttp(monkeypatch, transport)

    # The missing trajectory surfaces as an error rather than silently
    # downgrading to v0.1.
    with pytest.raises(httpx.HTTPStatusError):
        await job_client.store_agent_state(step="step", state={"k": "v"})

    assert job_client._object_store_supported is True
    assert all("/v0.1/" not in str(r.url) for r in recorder.requests)

    # Trajectory now exists: the next store still runs the full v0.2 flow
    # (init -> signed-URL upload -> finalize).
    trajectory_missing = False
    recorder.requests.clear()
    await job_client.store_agent_state(step="step2", state={"k": "v"})
    state_path = f"/v0.2/trajectories/{trajectory_id}/agent-state"
    assert [str(r.url) for r in recorder.requests] == [
        f"{Stage.LOCAL.value}{state_path}",
        "https://signed.example/upload",
        f"{Stage.LOCAL.value}{state_path}/{state_id}/finalize",
    ]


@pytest.mark.asyncio
async def test_v0d1_agent_state_escape_hatch_emits_deprecation(
    monkeypatch: pytest.MonkeyPatch, job_client: JobClient, trajectory_id: str
) -> None:
    """The deprecated v0.1 path still works for callers explicitly opting in."""

    async def handle(request: httpx.Request) -> httpx.Response:
        assert request.url.path == (f"/v0.1/trajectories/{trajectory_id}/agent-state")
        assert request.headers["content-encoding"] == "gzip"
        return httpx.Response(201, json=str(uuid4()))

    transport = httpx.MockTransport(handle)
    _patch_httpx_aiohttp(monkeypatch, transport)

    with pytest.warns(DeprecationWarning, match="store_agent_state"):
        await job_client._store_agent_state_v0d1(step="step", state={"k": "v"})
