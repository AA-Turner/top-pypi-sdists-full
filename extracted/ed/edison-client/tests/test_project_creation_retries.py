"""Project creation must not repeat a POST whose outcome is uncertain."""

import inspect
from collections.abc import Awaitable, Callable
from typing import Never
from uuid import UUID, uuid4

import httpx
import pytest
from tenacity import wait_none

from edison_client.clients.rest_client import ProjectError, RestClient

_CreateProject = Callable[
    [Callable[[httpx.Request], httpx.Response], UUID | None], Awaitable[UUID]
]


@pytest.fixture(name="create_project", params=["create_project", "acreate_project"])
def fixture_create_project(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch
) -> _CreateProject:
    async def invoke(
        handler: Callable[[httpx.Request], httpx.Response], persona_id: UUID | None
    ) -> UUID:
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
                method = getattr(RestClient, request.param).retry_with(wait=wait_none())
                result = method(client, name="research", persona_id=persona_id)
                return await result if inspect.isawaitable(result) else result

    return invoke


@pytest.fixture(
    name="persona_id", params=[False, True], ids=["standalone", "persona-owned"]
)
def fixture_persona_id(request: pytest.FixtureRequest) -> UUID | None:
    return uuid4() if request.param else None


@pytest.mark.parametrize(
    "failure",
    [httpx.ReadTimeout, httpx.ReadError, httpx.RemoteProtocolError, 500, 502, 503, 504],
)
async def test_ambiguous_failure_does_not_create_another_project(
    create_project: _CreateProject,
    persona_id: UUID | None,
    failure: int | type[httpx.TransportError],
) -> None:
    created = []

    def handle(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        expected_path = (
            f"/v0.1/personas/{persona_id}/projects" if persona_id else "/v0.1/projects"
        )
        assert request.url.path == expected_path
        project_id = uuid4()
        created.append(project_id)
        if len(created) == 1:
            if isinstance(failure, int):
                return httpx.Response(failure, json={"detail": "response lost"})
            raise failure("response lost after creation", request=request)
        payload = {"id": str(project_id)} if persona_id else str(project_id)
        return httpx.Response(201, json=payload)

    error_type = ProjectError if isinstance(failure, int) else failure
    with pytest.raises(error_type):
        await create_project(handle, persona_id)
    assert len(created) == 1


@pytest.mark.parametrize("failure", [httpx.ConnectError, httpx.ConnectTimeout, 429])
async def test_unprocessed_request_is_retried(
    create_project: _CreateProject,
    persona_id: UUID | None,
    failure: int | type[httpx.TransportError],
) -> None:
    attempts = 0
    project_id = uuid4()

    def handle(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            if isinstance(failure, int):
                return httpx.Response(failure, json={"detail": "rate limited"})
            raise failure("connection not established", request=request)
        payload = {"id": str(project_id)} if persona_id else str(project_id)
        return httpx.Response(201, json=payload)

    assert await create_project(handle, persona_id) == project_id
    assert attempts == 2


async def test_safe_retries_are_bounded(
    create_project: _CreateProject, persona_id: UUID | None
) -> None:
    attempts = 0

    def handle(request: httpx.Request) -> Never:
        nonlocal attempts
        attempts += 1
        raise httpx.ConnectTimeout("connection not established", request=request)

    with pytest.raises(httpx.ConnectTimeout):
        await create_project(handle, persona_id)
    assert attempts == RestClient.MAX_RETRY_ATTEMPTS
