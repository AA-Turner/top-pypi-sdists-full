# ruff: noqa: ARG001, ARG005, D205
"""Tests for RestClient v0.2 object-storage-backed task reads."""

from __future__ import annotations

import gzip
import json
from typing import Any
from uuid import uuid4

import httpx
import pytest

from edison_client.clients.rest_client import RestClient, TaskFetchError
from edison_client.models.app import (
    LiteTaskResponse,
    Stage,
    TaskResponse,
    TaskResponseVerbose,
)

BLOB_HOST = "signed.example"
STATE_URL = f"https://{BLOB_HOST}/agent-state-blob"
FRAME_URL = f"https://{BLOB_HOST}/environment-frame-blob"

AGENT_STATE = {"messages": [{"role": "user", "content": "hi"}]}
ENVIRONMENT_FRAME = {"state": {"state": {"answer": "42"}}}


@pytest.fixture(name="task_id")
def fixture_task_id() -> str:
    return str(uuid4())


@pytest.fixture(name="rest_client")
def fixture_rest_client() -> RestClient:
    return RestClient(stage=Stage.LOCAL, api_key="test-key", cleanup_on_exit=False)


def _v0d2_payload(
    task_id: str,
    *,
    agent_state_row: dict[str, Any] | None = None,
    frame_row: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """A v0.2 GET body: offloaded rows carry a URL, not a state."""
    return {
        "id": task_id,
        "task": "what is the answer?",
        "crow": "job-futurehouse-dummy-env",
        "status": "success",
        "share_status": "private",
        "created_at": "2026-06-22T20:34:36Z",
        "agent_state": [
            agent_state_row
            if agent_state_row is not None
            else {
                "id": "state-row-1",
                "step": "after_transition",
                "trajectory_timestep": 0,
                "state": None,
                "download_url": STATE_URL,
                "content_encoding": "gzip",
            }
        ],
        "environment_frame": frame_row
        if frame_row is not None
        else {
            "id": "frame-row-1",
            "state": None,
            "download_url": FRAME_URL,
            "content_encoding": "gzip",
        },
    }


class _Recorder:
    """Captures every request the client makes, for later assertion."""

    def __init__(self) -> None:
        self.requests: list[httpx.Request] = []

    @property
    def paths(self) -> list[str]:
        return [r.url.path for r in self.requests]


def _blob_response(payload: Any, *, gzip_header: bool = False) -> httpx.Response:
    """A storage response: gzipped JSON, exactly as the writer PUT it.

    ``gzip_header`` models whether the provider tags the object with
    ``Content-Encoding: gzip`` on the way back out. When it does, httpx
    gunzips the body before the reader sees it; when it does not, the raw
    compressed bytes arrive. Both happen in practice — see
    `test_get_task_decodes_blobs_regardless_of_transport_decompression`.
    """
    headers = {"Content-Encoding": "gzip"} if gzip_header else {}
    return httpx.Response(
        200,
        content=gzip.compress(json.dumps(payload).encode()),
        headers=headers,
    )


def _install(
    monkeypatch: pytest.MonkeyPatch,
    rest_client: RestClient,
    handler: Any,
) -> _Recorder:
    """Route both the API client and the blob client at ``handler``.

    The API transport is injected by replacing ``get_client``, which both
    the ``client`` and ``async_client`` properties funnel through. The blob
    downloads build their own short-lived clients inside ``state_blobs``
    (they must not carry our auth headers to a signed URL), so those are
    intercepted at the constructor — the same seam ``test_job_client``
    uses for the upload leg.
    """
    recorder = _Recorder()

    async def async_handler(request: httpx.Request) -> httpx.Response:
        await request.aread()
        recorder.requests.append(request)
        return handler(request)

    def sync_handler(request: httpx.Request) -> httpx.Response:
        request.read()
        recorder.requests.append(request)
        return handler(request)

    api_sync = httpx.Client(
        base_url=Stage.LOCAL.value, transport=httpx.MockTransport(sync_handler)
    )
    api_async = httpx.AsyncClient(
        base_url=Stage.LOCAL.value, transport=httpx.MockTransport(async_handler)
    )

    def fake_get_client(
        content_type: str | None = "application/json",
        authenticated: bool = True,
        async_client: bool = False,
        timeout: float | None = None,
    ) -> httpx.Client | httpx.AsyncClient:
        return api_async if async_client else api_sync

    monkeypatch.setattr(rest_client, "get_client", fake_get_client)
    # Bind the real constructors before patching: the factories below call
    # them, and reading through the patched name would recurse.
    real_client, real_async_client = httpx.Client, httpx.AsyncClient

    def blob_client(*args: Any, **kwargs: Any) -> httpx.Client:
        # ``follow_redirects`` is forwarded, not dropped, so the redirect
        # behavior under test is the real one.
        return real_client(
            transport=httpx.MockTransport(sync_handler),
            follow_redirects=kwargs.get("follow_redirects", False),
        )

    def async_blob_client(*args: Any, **kwargs: Any) -> httpx.AsyncClient:
        return real_async_client(
            transport=httpx.MockTransport(async_handler),
            follow_redirects=kwargs.get("follow_redirects", False),
        )

    monkeypatch.setattr("edison_client.clients.state_blobs.httpx.Client", blob_client)
    monkeypatch.setattr(
        "edison_client.clients.state_blobs.httpx_aiohttp.HttpxAiohttpClient",
        async_blob_client,
    )
    return recorder


def _happy_path_handler(task_id: str, *, gzip_header: bool = False) -> Any:
    def handle(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if request.url.host == BLOB_HOST:
            if url == STATE_URL:
                return _blob_response(AGENT_STATE, gzip_header=gzip_header)
            if url == FRAME_URL:
                return _blob_response(ENVIRONMENT_FRAME, gzip_header=gzip_header)
        if request.url.path == f"/v0.2/trajectories/{task_id}":
            return httpx.Response(200, json=_v0d2_payload(task_id))
        return httpx.Response(500, json={"detail": f"unmatched in test: {url}"})

    return handle


def test_get_task_reads_v0d2_and_materializes_blobs(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    """Happy path: one v0.2 GET, then the blobs straight from storage."""
    recorder = _install(monkeypatch, rest_client, _happy_path_handler(task_id))

    task = rest_client.get_task(task_id, verbose=True)

    assert isinstance(task, TaskResponseVerbose)
    api_request = recorder.requests[0]
    assert api_request.url.path == f"/v0.2/trajectories/{task_id}"
    assert dict(api_request.url.params) == {"history": "false", "lite": "false"}

    blob_requests = [r for r in recorder.requests if r.url.host == BLOB_HOST]
    assert {str(r.url) for r in blob_requests} == {STATE_URL, FRAME_URL}
    # Auth must NOT leak to the signed URL — GCS / S3 reject Bearer tokens
    # presented alongside signed credentials.
    for request in blob_requests:
        assert "authorization" not in {k.lower() for k in request.headers}

    assert task.agent_state is not None
    assert task.agent_state[0]["state"] == AGENT_STATE
    assert task.environment_frame is not None
    assert task.environment_frame["state"] == ENVIRONMENT_FRAME

    # v0.2-only pointer fields are dropped, so the object handed back is
    # shape-identical to a v0.1 read and existing consumers see no change.
    assert "download_url" not in task.agent_state[0]
    assert "content_encoding" not in task.agent_state[0]


@pytest.mark.parametrize("gzip_header", [True, False])
def test_get_task_decodes_blobs_regardless_of_transport_decompression(
    monkeypatch: pytest.MonkeyPatch,
    rest_client: RestClient,
    task_id: str,
    gzip_header: bool,
):
    """Both blob wire formats decode to the same state.

    Whether a blob comes back tagged ``Content-Encoding: gzip`` is
    provider-dependent: the upload leg does not fold that header into the
    signature (``generate_state_upload_url`` passes no ``signed_headers``),
    so GCS and S3 are each free to store it or not. Tagged, the HTTP stack
    gunzips before the reader sees the body — httpx does this directly, and
    httpx-aiohttp configures aiohttp with ``auto_decompress=False`` so the
    decoding happens in httpx there too, never twice. Untagged, the raw
    compressed bytes arrive. Sniffing the gzip magic header covers both,
    which is what keeps the reader portable across clouds.
    """
    _install(
        monkeypatch, rest_client, _happy_path_handler(task_id, gzip_header=gzip_header)
    )

    task = rest_client.get_task(task_id, verbose=True)

    assert isinstance(task, TaskResponseVerbose)
    assert task.agent_state is not None
    assert task.agent_state[0]["state"] == AGENT_STATE
    assert task.environment_frame is not None
    assert task.environment_frame["state"] == ENVIRONMENT_FRAME


@pytest.mark.asyncio
@pytest.mark.parametrize("gzip_header", [True, False])
async def test_aget_task_decodes_blobs_regardless_of_transport_decompression(
    monkeypatch: pytest.MonkeyPatch,
    rest_client: RestClient,
    task_id: str,
    gzip_header: bool,
):
    """Async counterpart: see the sync test for why both cases exist."""
    _install(
        monkeypatch, rest_client, _happy_path_handler(task_id, gzip_header=gzip_header)
    )

    task = await rest_client.aget_task(task_id, verbose=True)

    assert isinstance(task, TaskResponseVerbose)
    assert task.agent_state is not None
    assert task.agent_state[0]["state"] == AGENT_STATE


def test_get_task_follows_a_storage_redirect(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    """S3 answers a regional-endpoint mismatch with a 307 rather than the
    object, so blob GETs follow redirects (httpx would not by default).
    """
    redirect_target = f"https://{BLOB_HOST}/regional/agent-state-blob"

    def handle(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if url == STATE_URL:
            return httpx.Response(307, headers={"Location": redirect_target})
        if url == redirect_target:
            return _blob_response(AGENT_STATE)
        if url == FRAME_URL:
            return _blob_response(ENVIRONMENT_FRAME)
        if request.url.path == f"/v0.2/trajectories/{task_id}":
            return httpx.Response(200, json=_v0d2_payload(task_id))
        return httpx.Response(500, json={"detail": f"unmatched in test: {url}"})

    recorder = _install(monkeypatch, rest_client, handle)

    task = rest_client.get_task(task_id, verbose=True)

    assert isinstance(task, TaskResponseVerbose)
    assert task.agent_state is not None
    assert task.agent_state[0]["state"] == AGENT_STATE
    assert redirect_target in {str(r.url) for r in recorder.requests}


def test_get_task_pairs_every_blob_with_its_own_row(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    """A history read fans many blobs out across the thread pool at once.

    Results are zipped back onto ``pending`` positionally, so anything that
    reorders completions (``as_completed``, say) would silently give a row
    another row's state — a wrong answer that still validates. Distinct
    payloads per row catch that.
    """
    rows = 12

    def handle(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if request.url.host == BLOB_HOST:
            index = int(url.rsplit("/", 1)[1])
            return _blob_response({"index": index})
        if request.url.path == f"/v0.2/trajectories/{task_id}":
            payload = _v0d2_payload(task_id)
            payload["agent_state"] = [
                {
                    "id": f"state-row-{i}",
                    "trajectory_timestep": i,
                    "state": None,
                    "download_url": f"https://{BLOB_HOST}/{i}",
                }
                for i in range(rows)
            ]
            payload["environment_frame"] = None
            return httpx.Response(200, json=payload)
        return httpx.Response(500, json={"detail": f"unmatched in test: {url}"})

    _install(monkeypatch, rest_client, handle)

    task = rest_client.get_task(task_id, history=True, verbose=True)

    assert isinstance(task, TaskResponseVerbose)
    assert task.agent_state is not None
    assert [row["state"] for row in task.agent_state] == [
        {"index": i} for i in range(rows)
    ]


def test_get_task_passes_history_through_to_v0d2(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    recorder = _install(monkeypatch, rest_client, _happy_path_handler(task_id))

    rest_client.get_task(task_id, history=True, verbose=True)

    assert dict(recorder.requests[0].url.params) == {
        "history": "true",
        "lite": "false",
    }


def test_get_task_returns_inline_rows_verbatim(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    """Legacy pre-v0.2 rows come back with ``state`` already populated;
    v0.2 returns them untouched and no blob fetch should happen.
    """
    inline_state = {"messages": ["already here"]}

    def handle(request: httpx.Request) -> httpx.Response:
        if request.url.path == f"/v0.2/trajectories/{task_id}":
            return httpx.Response(
                200,
                json=_v0d2_payload(
                    task_id,
                    agent_state_row={
                        "id": "state-row-1",
                        "state": inline_state,
                        "download_url": None,
                    },
                    frame_row={
                        "id": "frame-row-1",
                        "state": ENVIRONMENT_FRAME,
                        "download_url": None,
                    },
                ),
            )
        return httpx.Response(500, json={"detail": "unmatched in test"})

    recorder = _install(monkeypatch, rest_client, handle)

    task = rest_client.get_task(task_id, verbose=True)

    assert isinstance(task, TaskResponseVerbose)
    assert task.agent_state is not None
    assert task.agent_state[0]["state"] == inline_state
    assert all(r.url.host != BLOB_HOST for r in recorder.requests)
    assert "download_url" not in task.agent_state[0]


def test_get_task_skips_rows_with_neither_state_nor_url(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    """A row the server could not sign is left as ``state: None`` — v0.1
    reads of the same row are stateless too, so this is not an error.
    """

    def handle(request: httpx.Request) -> httpx.Response:
        if request.url.path == f"/v0.2/trajectories/{task_id}":
            return httpx.Response(
                200,
                json=_v0d2_payload(
                    task_id,
                    agent_state_row={
                        "id": "state-row-1",
                        "state": None,
                        "download_url": None,
                    },
                    frame_row={
                        "id": "frame-row-1",
                        "state": None,
                        "download_url": None,
                    },
                ),
            )
        return httpx.Response(500, json={"detail": "unmatched in test"})

    recorder = _install(monkeypatch, rest_client, handle)

    task = rest_client.get_task(task_id, verbose=True)

    assert isinstance(task, TaskResponseVerbose)
    assert task.agent_state is not None
    assert task.agent_state[0]["state"] is None
    assert all(r.url.host != BLOB_HOST for r in recorder.requests)


def test_get_task_raises_when_a_blob_cannot_be_read(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    """A failed blob download is loud. Silently returning the task with an
    empty ``state`` would look valid to every downstream consumer.
    """

    def handle(request: httpx.Request) -> httpx.Response:
        if request.url.host == BLOB_HOST:
            # 403 is what an expired signed URL returns: permanent, so the
            # per-blob retry does not fire.
            return httpx.Response(403, text="expired")
        if request.url.path == f"/v0.2/trajectories/{task_id}":
            return httpx.Response(200, json=_v0d2_payload(task_id))
        return httpx.Response(500, json={"detail": "unmatched in test"})

    _install(monkeypatch, rest_client, handle)

    with pytest.raises(TaskFetchError, match="state blob"):
        rest_client.get_task(task_id, verbose=True)


def test_get_task_does_not_fall_back_when_v0d2_is_missing(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    """No silent downgrade to v0.1 — a missing route is a real error.

    Every deployment has served the v0.2 GET for months, so quietly
    retrying on the deprecated inline route would hide a broken deployment
    behind a slower path instead of surfacing it. Callers that genuinely
    want v0.1 ask for it explicitly via ``_get_task_v0d1``.
    """

    def handle(request: httpx.Request) -> httpx.Response:
        if "/v0.2/" in str(request.url):
            return httpx.Response(404, json={"detail": "Not Found"})
        return httpx.Response(500, json={"detail": "unmatched in test"})

    recorder = _install(monkeypatch, rest_client, handle)

    with pytest.raises(httpx.HTTPStatusError):
        rest_client.get_task(task_id, verbose=True)

    assert recorder.paths == [f"/v0.2/trajectories/{task_id}"]


def test_get_task_raises_on_unknown_task_id(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    """An application 404 propagates, with a readable body on the error."""

    def handle(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            404,
            json={
                "detail": f"Task not found associated with the provided job id {task_id}"
            },
        )

    recorder = _install(monkeypatch, rest_client, handle)

    with pytest.raises(httpx.HTTPStatusError) as excinfo:
        rest_client.get_task(task_id, verbose=True)

    # The streamed body is read before raising, so the detail is inspectable.
    assert "Task not found" in excinfo.value.response.text
    assert all("/v0.1/" not in p for p in recorder.paths)


def test_get_task_lite_reads_v0d2_without_touching_storage(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    recorder = _install(monkeypatch, rest_client, _happy_path_handler(task_id))

    task = rest_client.get_task(task_id, lite=True)

    assert isinstance(task, LiteTaskResponse)
    assert str(task.task_id) == task_id
    assert task.status == "success"
    # One request, to v0.2, and not a single blob fetch.
    assert recorder.paths == [f"/v0.2/trajectories/{task_id}"]
    assert all(r.url.host != BLOB_HOST for r in recorder.requests)
    # ``lite`` goes to the server, which serves it from one row read. An
    # older server without the param ignores it and answers in full; the
    # client projects locally and still skips hydration.
    assert dict(recorder.requests[0].url.params) == {
        "history": "false",
        "lite": "true",
    }


@pytest.mark.asyncio
async def test_aget_task_lite_reads_v0d2_without_touching_storage(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    recorder = _install(monkeypatch, rest_client, _happy_path_handler(task_id))

    task = await rest_client.aget_task(task_id, lite=True)

    assert isinstance(task, LiteTaskResponse)
    assert recorder.paths == [f"/v0.2/trajectories/{task_id}"]
    assert all(r.url.host != BLOB_HOST for r in recorder.requests)


def test_cancel_task_reads_status_lite(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    """Cancel only needs ``.status``; it must not hydrate state blobs."""
    posts: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            posts.append(request)
            return httpx.Response(200, json={})
        if request.url.path == f"/v0.2/trajectories/{task_id}":
            payload = _v0d2_payload(task_id)
            payload["status"] = "cancelled" if posts else "in progress"
            return httpx.Response(200, json=payload)
        return httpx.Response(500, json={"detail": "unmatched in test"})

    recorder = _install(monkeypatch, rest_client, handle)

    assert rest_client.cancel_task(task_id) is True
    assert [r.url.path for r in posts] == [f"/v0.1/trajectories/{task_id}/cancel"]
    # Two status reads, zero blob downloads.
    assert all(r.url.host != BLOB_HOST for r in recorder.requests)


def test_get_task_raises_permission_error_on_403(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    """403 keeps its pre-migration behavior on the new route."""
    _install(
        monkeypatch,
        rest_client,
        lambda request: httpx.Response(403, json={"detail": "nope"}),
    )

    with pytest.raises(PermissionError, match="Permission denied"):
        rest_client.get_task(task_id, verbose=True)


def test_v0d1_task_get_escape_hatch_emits_deprecation(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    """The deprecated v0.1 read still works for callers pinning to it."""
    inline_payload = _v0d2_payload(
        task_id,
        agent_state_row={"id": "state-row-1", "state": AGENT_STATE},
        frame_row={"id": "frame-row-1", "state": ENVIRONMENT_FRAME},
    )

    def handle(request: httpx.Request) -> httpx.Response:
        assert request.url.path == f"/v0.1/trajectories/{task_id}"
        return httpx.Response(200, json=inline_payload)

    recorder = _install(monkeypatch, rest_client, handle)

    with pytest.warns(DeprecationWarning, match="get_task"):
        task = rest_client._get_task_v0d1(task_id, verbose=True)

    assert isinstance(task, TaskResponseVerbose)
    assert recorder.paths == [f"/v0.1/trajectories/{task_id}"]


def test_get_task_non_verbose_returns_job_specific_response(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    """The v0.2 payload feeds the job-specific model the same way v0.1 did —
    including fields the model digs out of the materialized frame blob.
    """
    _install(monkeypatch, rest_client, _happy_path_handler(task_id))

    task = rest_client.get_task(task_id)

    assert isinstance(task, TaskResponse)
    assert not isinstance(task, TaskResponseVerbose)
    assert task.status == "success"
    assert task.job_name == "job-futurehouse-dummy-env"


@pytest.mark.asyncio
async def test_aget_task_reads_v0d2_and_materializes_blobs(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    recorder = _install(monkeypatch, rest_client, _happy_path_handler(task_id))

    task = await rest_client.aget_task(task_id, verbose=True)

    assert isinstance(task, TaskResponseVerbose)
    assert recorder.requests[0].url.path == f"/v0.2/trajectories/{task_id}"
    assert dict(recorder.requests[0].url.params) == {
        "history": "false",
        "lite": "false",
    }
    assert task.agent_state is not None
    assert task.agent_state[0]["state"] == AGENT_STATE
    assert task.environment_frame is not None
    assert task.environment_frame["state"] == ENVIRONMENT_FRAME
    assert "download_url" not in task.agent_state[0]

    blob_requests = [r for r in recorder.requests if r.url.host == BLOB_HOST]
    assert {str(r.url) for r in blob_requests} == {STATE_URL, FRAME_URL}
    for request in blob_requests:
        assert "authorization" not in {k.lower() for k in request.headers}


@pytest.mark.asyncio
async def test_aget_task_does_not_fall_back_when_v0d2_is_missing(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    def handle(request: httpx.Request) -> httpx.Response:
        if "/v0.2/" in str(request.url):
            return httpx.Response(404, json={"detail": "Not Found"})
        return httpx.Response(500, json={"detail": "unmatched in test"})

    recorder = _install(monkeypatch, rest_client, handle)

    with pytest.raises(httpx.HTTPStatusError):
        await rest_client.aget_task(task_id, verbose=True)

    assert recorder.paths == [f"/v0.2/trajectories/{task_id}"]


@pytest.mark.asyncio
async def test_aget_task_raises_when_a_blob_cannot_be_read(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    def handle(request: httpx.Request) -> httpx.Response:
        if request.url.host == BLOB_HOST:
            return httpx.Response(403, text="expired")
        if request.url.path == f"/v0.2/trajectories/{task_id}":
            return httpx.Response(200, json=_v0d2_payload(task_id))
        return httpx.Response(500, json={"detail": "unmatched in test"})

    _install(monkeypatch, rest_client, handle)

    with pytest.raises(TaskFetchError, match="state blob"):
        await rest_client.aget_task(task_id, verbose=True)


@pytest.mark.asyncio
async def test_av0d1_task_get_escape_hatch_emits_deprecation(
    monkeypatch: pytest.MonkeyPatch, rest_client: RestClient, task_id: str
):
    inline_payload = _v0d2_payload(
        task_id,
        agent_state_row={"id": "state-row-1", "state": AGENT_STATE},
        frame_row={"id": "frame-row-1", "state": ENVIRONMENT_FRAME},
    )

    def handle(request: httpx.Request) -> httpx.Response:
        assert request.url.path == f"/v0.1/trajectories/{task_id}"
        return httpx.Response(200, json=inline_payload)

    _install(monkeypatch, rest_client, handle)

    with pytest.warns(DeprecationWarning, match="aget_task"):
        task = await rest_client._aget_task_v0d1(task_id, verbose=True)

    assert isinstance(task, TaskResponseVerbose)
