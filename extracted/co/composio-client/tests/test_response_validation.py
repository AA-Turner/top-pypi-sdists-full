"""Response parsing preserves the Stainless strictness contract."""

from __future__ import annotations

import httpx
import pytest
from pydantic import BaseModel, RootModel, ValidationError, field_validator

from composio_client import APIResponseValidationError, AsyncComposio, Composio, ProjectAuth
from composio_client._generated import pydantic_gen as generated
from composio_client._models import SessionConfigHistoryResponse


class ExampleResponse(BaseModel):
    count: int


class NestedResponse(BaseModel):
    example: ExampleResponse


class ListResponse(RootModel[list[ExampleResponse]]):
    pass


class ValidatorTypeErrorResponse(BaseModel):
    count: int

    @field_validator("count")
    @classmethod
    def reject_count(cls, value: int) -> int:
        raise TypeError("validator failed")


GENERATED_RESPONSE = {
    "items": [
        {
            "version": 1,
            "created_at": "not-a-date",
            "config": {
                "user_id": "user-1",
                "tools": {"github": {"disabled": ["GITHUB_DELETE_REPOSITORY"]}},
                "preload": {"tools": []},
                "search": {},
                "execute": {},
            },
            "is_current": True,
        }
    ],
    "next_cursor": None,
}


def test_default_response_parsing_constructs_models_without_validation() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={"count": "not-an-integer"}))

    with Composio(
        auth=ProjectAuth("key"),
        base_url="https://client.invalid",
        http_client=httpx.Client(transport=transport),
    ) as client:
        response = client._request("GET", "/example", cast_to=ExampleResponse)

    assert isinstance(response, ExampleResponse)
    assert response.count == "not-an-integer"  # type: ignore[comparison-overlap]


def test_default_response_parsing_constructs_nested_and_root_models() -> None:
    responses = iter(
        [
            httpx.Response(200, json={"example": {"count": "not-an-integer"}}),
            httpx.Response(200, json=[{"count": "not-an-integer"}]),
        ]
    )
    transport = httpx.MockTransport(lambda request: next(responses))

    with Composio(
        auth=ProjectAuth("key"),
        base_url="https://client.invalid",
        http_client=httpx.Client(transport=transport),
    ) as client:
        nested = client._request("GET", "/nested", cast_to=NestedResponse)
        listed = client._request("GET", "/listed", cast_to=ListResponse)

    assert isinstance(nested.example, ExampleResponse)
    assert nested.example.count == "not-an-integer"  # type: ignore[comparison-overlap]
    assert isinstance(listed.root[0], ExampleResponse)
    assert listed.root[0].count == "not-an-integer"  # type: ignore[comparison-overlap]


def test_default_response_parsing_constructs_generated_union_and_dictionary_tree() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=GENERATED_RESPONSE))

    with Composio(
        auth=ProjectAuth("key"),
        base_url="https://client.invalid",
        http_client=httpx.Client(transport=transport),
    ) as client:
        response = client._request(
            "GET",
            "/config-history",
            cast_to=SessionConfigHistoryResponse,
        )

    item = response.root.items[0]
    tool_filter = item.config.tools["github"]  # type: ignore[index]
    assert isinstance(
        tool_filter,
        generated.ToolRouterSessionV31ConfigHistoryListResponseItemsConfigToolsValue_,
    )
    assert tool_filter.disabled == ["GITHUB_DELETE_REPOSITORY"]
    assert item.created_at == "not-a-date"


def test_strict_response_validation_maps_pydantic_errors() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={"count": "not-an-integer"}))

    with Composio(
        auth=ProjectAuth("key"),
        base_url="https://client.invalid",
        http_client=httpx.Client(transport=transport),
        _strict_response_validation=True,
    ) as client:
        with pytest.raises(APIResponseValidationError) as raised:
            client._request("GET", "/example", cast_to=ExampleResponse)

    assert raised.value.body == {"count": "not-an-integer"}
    assert raised.value.status_code == 200
    assert isinstance(raised.value.__cause__, ValidationError)


def test_strict_response_validation_does_not_swallow_validator_type_errors() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={"count": 1}))

    with Composio(
        auth=ProjectAuth("key"),
        base_url="https://client.invalid",
        http_client=httpx.Client(transport=transport),
        _strict_response_validation=True,
    ) as client:
        with pytest.raises(TypeError, match="validator failed"):
            client._request("GET", "/example", cast_to=ValidatorTypeErrorResponse)


@pytest.mark.asyncio
async def test_async_default_response_parsing_constructs_models_without_validation() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={"count": "not-an-integer"}))

    async with AsyncComposio(
        auth=ProjectAuth("key"),
        base_url="https://client.invalid",
        http_client=httpx.AsyncClient(transport=transport),
    ) as client:
        response = await client._request("GET", "/example", cast_to=ExampleResponse)

    assert isinstance(response, ExampleResponse)
    assert response.count == "not-an-integer"  # type: ignore[comparison-overlap]


@pytest.mark.asyncio
async def test_async_strict_response_validation_maps_pydantic_errors() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={"count": "not-an-integer"}))

    async with AsyncComposio(
        auth=ProjectAuth("key"),
        base_url="https://client.invalid",
        http_client=httpx.AsyncClient(transport=transport),
        _strict_response_validation=True,
    ) as client:
        with pytest.raises(APIResponseValidationError) as raised:
            await client._request("GET", "/example", cast_to=ExampleResponse)

    assert raised.value.body == {"count": "not-an-integer"}
    assert raised.value.status_code == 200
    assert isinstance(raised.value.__cause__, ValidationError)


@pytest.mark.asyncio
async def test_async_strict_validation_does_not_swallow_validator_type_errors() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={"count": 1}))

    async with AsyncComposio(
        auth=ProjectAuth("key"),
        base_url="https://client.invalid",
        http_client=httpx.AsyncClient(transport=transport),
        _strict_response_validation=True,
    ) as client:
        with pytest.raises(TypeError, match="validator failed"):
            await client._request("GET", "/example", cast_to=ValidatorTypeErrorResponse)
