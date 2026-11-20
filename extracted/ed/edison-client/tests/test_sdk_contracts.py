"""Exercise SDK contracts at HTTP and serialization boundaries."""

import json
from collections.abc import Iterator
from contextlib import closing
from uuid import UUID

import httpx
import pytest
from aviary.core import ToolCall, ToolRequestMessage, ToolResponseMessage
from aviary.message import Message
from pydantic import JsonValue, ValidationError

from edison_client.clients.multipart_upload import _aupload_one_part, _upload_one_part
from edison_client.clients.rest_client import RestClient, WorldModelFetchError
from edison_client.models import WorldModelSearchResult
from edison_client.models.app import AuthType, Stage
from edison_client.models.client import (
    BeforeTransitionState,
    EnvResetState,
    EnvStepState,
    GlobalState,
)
from edison_client.utils.auth import RefreshingJWT

WORLD_MODEL_ID = UUID("df91c7de-86af-49a1-ac19-bf6fe41f4ee9")


@pytest.fixture
def rest_client(
    monkeypatch: pytest.MonkeyPatch, payload: JsonValue
) -> Iterator[RestClient]:
    def handle_request(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v0.1/world-models/search"
        return httpx.Response(
            200,
            content=json.dumps(payload),
            headers={"Content-Type": "application/json"},
        )

    with (
        httpx.Client(
            base_url=Stage.LOCAL.value, transport=httpx.MockTransport(handle_request)
        ) as http_client,
        closing(
            RestClient(
                stage=Stage.LOCAL,
                auth_type=AuthType.JWT,
                jwt="test-token",
                cleanup_on_exit=False,
            )
        ) as client,
    ):
        monkeypatch.setattr(client.client, "send", http_client.send)
        yield client


@pytest.mark.parametrize(
    "payload",
    [
        [{"id": str(WORLD_MODEL_ID), "name": "Research"}],
        [
            {
                "id": str(WORLD_MODEL_ID),
                "name": "Research",
                "description": "Findings",
                "created_at": "2026-11-08T12:00:00Z",
                "project_id": None,
                "trajectory_id": None,
            }
        ],
        [],
    ],
)
def test_world_model_search_returns_summaries(
    rest_client: RestClient, payload: list[dict[str, str | None]]
) -> None:
    results = rest_client.search_world_models()
    for model, expected in zip(results, payload, strict=True):
        assert isinstance(model, WorldModelSearchResult)
        assert model.id == WORLD_MODEL_ID
        assert model.name == "Research"
        assert model.model_dump(mode="json", exclude_unset=True) == expected


@pytest.mark.parametrize("payload", [[{"name": "Missing ID"}], {}, None])
def test_world_model_search_rejects_malformed_summary(rest_client: RestClient) -> None:
    with pytest.raises(WorldModelFetchError) as exc_info:
        rest_client.search_world_models()
    assert isinstance(exc_info.value.__cause__, ValidationError)


@pytest.mark.parametrize("token", [None, 123, ""])
def test_auth_rejects_invalid_token(token: int | str | None) -> None:
    transport = httpx.MockTransport(
        lambda _request: httpx.Response(200, json={"access_token": token})
    )
    with (
        httpx.Client(base_url="https://auth.example", transport=transport) as client,
        pytest.raises(Exception, match="Failed to authenticate") as exc_info,
    ):
        RefreshingJWT(client, api_key="test-key")
    assert isinstance(exc_info.value.__cause__, ValueError)


def test_auth_accepts_string_token() -> None:
    def handle_request(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/auth/login":
            return httpx.Response(200, json={"access_token": "test-token"})
        return httpx.Response(200, text=request.headers["Authorization"])

    transport = httpx.MockTransport(handle_request)
    with httpx.Client(base_url="https://auth.example", transport=transport) as client:
        auth = RefreshingJWT(client, api_key="test-key")
        assert client.get("/resource", auth=auth).text == "Bearer test-token"


@pytest.mark.parametrize(
    ("state_type", "fields"),
    [
        (GlobalState, {}),
        (BeforeTransitionState, {"current_state": None}),
        (EnvResetState, {"tools": []}),
        (EnvStepState, {"reward": 0.0, "done": False, "trunc": False}),
    ],
)
def test_state_observations_round_trip(
    state_type: type[
        GlobalState | BeforeTransitionState | EnvResetState | EnvStepState
    ],
    fields: dict[str, object],
) -> None:
    call = ToolCall.from_name("search", id="call-1", query="proteins")
    messages = [
        Message(role="user", content="hello", info={"is_human": True}),
        ToolRequestMessage(tool_calls=[call]),
        ToolResponseMessage(content="result", name="search", tool_call_id="call-1"),
    ]
    state = state_type.model_validate_json(
        state_type.model_validate({"observations": messages, **fields}).model_dump_json(
            context={"include_info": True}
        )
    )
    assert state.observations == messages


def test_part_upload_requires_etag() -> None:
    transport = httpx.MockTransport(lambda _request: httpx.Response(200))
    with (
        httpx.Client(transport=transport) as client,
        pytest.raises(KeyError, match="etag"),
    ):
        _upload_one_part(client, "https://storage.example/part", b"part", "checksum", 1)


@pytest.mark.asyncio
async def test_async_part_upload_requires_etag() -> None:
    transport = httpx.MockTransport(lambda _request: httpx.Response(200))
    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(KeyError, match="etag"):
            await _aupload_one_part(
                client, "https://storage.example/part", b"part", "checksum", 1
            )
