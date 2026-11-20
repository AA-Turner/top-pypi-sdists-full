"""Exercise project and session operations through the HTTP transport."""

import inspect
import json
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Any, Protocol
from uuid import uuid4

import httpx
import pytest
from openai import Timeout
from tenacity import wait_none

from edison_client.clients.rest_client import ProjectError, RestClient
from edison_client.clients.session_methods import SessionFetchError
from edison_client.models.session import SessionType


class _Invoke(Protocol):
    def __call__(
        self, method: str, *args: object, **kwargs: object
    ) -> Awaitable[Any]: ...


_Connect = Callable[
    [Callable[[httpx.Request], httpx.Response]], AbstractAsyncContextManager[_Invoke]
]


@pytest.fixture(name="invoke", params=[False, True], ids=["sync", "async"])
def fixture_invoke(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch
) -> _Connect:
    @asynccontextmanager
    async def connect(
        handler: Callable[[httpx.Request], httpx.Response],
    ) -> AsyncGenerator[_Invoke]:
        transport = httpx.MockTransport(handler)
        with httpx.Client(base_url="https://example.com", transport=transport) as sync:
            async with httpx.AsyncClient(
                base_url="https://example.com", transport=transport
            ) as async_client:
                monkeypatch.setattr(RestClient, "client", property(lambda _: sync))
                monkeypatch.setattr(
                    RestClient, "async_client", property(lambda _: async_client)
                )
                client = RestClient(api_key="test-key", cleanup_on_exit=False)

                async def call(method: str, *args: object, **kwargs: object) -> object:
                    name = f"a{method}" if request.param else method
                    operation = getattr(RestClient, name).retry_with(wait=wait_none())
                    result = operation(client, *args, **kwargs)
                    return await result if inspect.isawaitable(result) else result

                yield call

    return connect


@pytest.mark.parametrize("persona_owned", [False, True])
@pytest.mark.parametrize("timeout", [None, 120.0, httpx.Timeout(120, connect=10)])
async def test_creation_timeout_and_existing_payload(
    invoke: _Connect, persona_owned: bool, timeout: Timeout | float | None
) -> None:
    project_id, persona_id = uuid4(), uuid4()
    requests = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        expected = (
            f"/v0.1/personas/{persona_id}/projects"
            if persona_owned
            else "/v0.1/projects"
        )
        assert request.url.path == expected
        body = json.loads(request.content)
        assert body["name"] == "worker"
        assert body["metadata"] == {"caller_session_id": "caller"}
        assert "timeout" not in body
        if persona_owned:
            assert body["job_name"] == "analysis-chat"
            assert body["handoff_message"] == "Analyze the data"
        expected_timeout = (
            timeout
            if isinstance(timeout, httpx.Timeout)
            else httpx.Timeout(timeout or 5)
        )
        assert request.extensions["timeout"] == expected_timeout.as_dict()
        return httpx.Response(
            201, json={"id": str(project_id)} if persona_owned else str(project_id)
        )

    kwargs: dict[str, object] = {"timeout": timeout} if timeout is not None else {}
    if persona_owned:
        kwargs.update(
            persona_id=persona_id,
            job_name="analysis-chat",
            handoff_message="Analyze the data",
        )
    async with invoke(handle) as call:
        assert (
            await call(
                "create_project",
                "worker",
                metadata={"caller_session_id": "caller"},
                **kwargs,
            )
            == project_id
        )
    assert len(requests) == 1


async def test_get_project(invoke: _Connect) -> None:
    project_id = uuid4()
    payload = {"id": str(project_id), "metadata": {"caller_session_id": "caller"}}

    def handle(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == f"/v0.1/projects/{project_id}"
        return httpx.Response(200, json=payload)

    async with invoke(handle) as call:
        assert await call("get_project", project_id) == payload


@pytest.mark.parametrize("heartbeat", [None, False, True])
async def test_update_heartbeat_preserves_omitted_fields(
    invoke: _Connect, heartbeat: bool | None
) -> None:
    project_id = uuid4()

    def handle(request: httpx.Request) -> httpx.Response:
        assert request.method == "PATCH"
        assert request.url.path == f"/v0.1/projects/{project_id}"
        expected: dict[str, object] = {"name": "renamed"}
        if heartbeat is not None:
            expected["heartbeat"] = {"enabled": heartbeat}
        assert json.loads(request.content) == expected
        return httpx.Response(202)

    async with invoke(handle) as call:
        await call("update_project", project_id, name="renamed", heartbeat=heartbeat)


@pytest.mark.parametrize("failure", [httpx.ConnectTimeout, httpx.ReadTimeout, 503])
async def test_heartbeat_retry_does_not_recreate_project(
    invoke: _Connect, failure: int | type[httpx.TransportError]
) -> None:
    project_id, persona_id = uuid4(), uuid4()
    creates, updates = [], []

    def handle(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            creates.append(request)
            return httpx.Response(201, json={"id": str(project_id)})
        assert request.method == "PATCH"
        assert request.url.path == f"/v0.1/projects/{project_id}"
        assert json.loads(request.content) == {"heartbeat": {"enabled": False}}
        updates.append(request)
        if len(updates) == 1:
            if isinstance(failure, int):
                return httpx.Response(failure)
            raise failure("heartbeat update failed", request=request)
        return httpx.Response(202)

    async with invoke(handle) as call:
        created_id = await call("create_project", "worker", persona_id=persona_id)
        await call("update_project", created_id, heartbeat=False)
    assert len(creates) == 1
    assert len(updates) == 2


@pytest.mark.parametrize("filtered", [False, True])
async def test_list_sessions_filters_and_typed_response(
    invoke: _Connect, filtered: bool
) -> None:
    session_id, project_id = uuid4(), uuid4()

    def handle(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/v0.1/sessions"
        expected = {"limit": "5", "offset": "0"}
        if filtered:
            expected = {
                "limit": "2",
                "offset": "3",
                "type_id": str(project_id),
                "type": "project",
                "source": "web",
            }
        assert dict(request.url.params) == expected
        return httpx.Response(
            200,
            json=[
                {
                    "id": str(session_id),
                    "type_id": str(project_id),
                    "type": "project",
                    "source": "web",
                }
            ],
        )

    kwargs = (
        {
            "limit": 2,
            "offset": 3,
            "type_id": project_id,
            "session_type": SessionType.PROJECT,
            "source": "web",
        }
        if filtered
        else {}
    )
    async with invoke(handle) as call:
        (session,) = await call("list_sessions", **kwargs)
    assert session.id == session_id
    assert session.type_id == project_id
    assert session.type == SessionType.PROJECT
    assert session.source == "web"


async def test_list_sessions_empty_and_retry(invoke: _Connect) -> None:
    requests = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if len(requests) == 1:
            return httpx.Response(503)
        assert request.url.params["type"] == "conversation"
        return httpx.Response(200, json=[])

    async with invoke(handle) as call:
        assert await call("list_sessions", session_type="conversation") == []
    assert len(requests) == 2


@pytest.mark.parametrize("status", [403, 404, 422])
@pytest.mark.parametrize(
    "operation", ["get_project", "update_project", "list_sessions"]
)
async def test_http_failures_surface(
    invoke: _Connect, status: int, operation: str
) -> None:
    requests = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(status, json={"detail": "rejected"})

    error = SessionFetchError if operation == "list_sessions" else ProjectError
    args = [] if operation == "list_sessions" else [uuid4()]
    async with invoke(handle) as call:
        with pytest.raises(error):
            await call(operation, *args)
    assert len(requests) == 1
