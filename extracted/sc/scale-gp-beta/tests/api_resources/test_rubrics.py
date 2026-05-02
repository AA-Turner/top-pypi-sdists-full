# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import (
    RubricResponse,
    RubricArchiveResponse,
)
from scale_gp_beta.pagination import SyncCursorPage, AsyncCursorPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRubrics:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        rubric = client.rubrics.create(
            title="x",
        )
        assert_matches_type(RubricResponse, rubric, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        rubric = client.rubrics.create(
            title="x",
            criteria=[
                {
                    "title": "x",
                    "annotations": {"foo": "bar"},
                    "weight": 0,
                }
            ],
            tags=["string"],
        )
        assert_matches_type(RubricResponse, rubric, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.rubrics.with_raw_response.create(
            title="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rubric = response.parse()
        assert_matches_type(RubricResponse, rubric, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.rubrics.with_streaming_response.create(
            title="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rubric = response.parse()
            assert_matches_type(RubricResponse, rubric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        rubric = client.rubrics.retrieve(
            "rubric_id",
        )
        assert_matches_type(RubricResponse, rubric, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.rubrics.with_raw_response.retrieve(
            "rubric_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rubric = response.parse()
        assert_matches_type(RubricResponse, rubric, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.rubrics.with_streaming_response.retrieve(
            "rubric_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rubric = response.parse()
            assert_matches_type(RubricResponse, rubric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rubric_id` but received ''"):
            client.rubrics.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        rubric = client.rubrics.update(
            rubric_id="rubric_id",
            rubric={},
        )
        assert_matches_type(RubricResponse, rubric, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        rubric = client.rubrics.update(
            rubric_id="rubric_id",
            rubric={
                "tags": ["string"],
                "title": "x",
            },
        )
        assert_matches_type(RubricResponse, rubric, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.rubrics.with_raw_response.update(
            rubric_id="rubric_id",
            rubric={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rubric = response.parse()
        assert_matches_type(RubricResponse, rubric, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.rubrics.with_streaming_response.update(
            rubric_id="rubric_id",
            rubric={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rubric = response.parse()
            assert_matches_type(RubricResponse, rubric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rubric_id` but received ''"):
            client.rubrics.with_raw_response.update(
                rubric_id="",
                rubric={},
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        rubric = client.rubrics.list()
        assert_matches_type(SyncCursorPage[RubricResponse], rubric, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        rubric = client.rubrics.list(
            ending_before="ending_before",
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
            tags=["string"],
            title="title",
        )
        assert_matches_type(SyncCursorPage[RubricResponse], rubric, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.rubrics.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rubric = response.parse()
        assert_matches_type(SyncCursorPage[RubricResponse], rubric, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.rubrics.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rubric = response.parse()
            assert_matches_type(SyncCursorPage[RubricResponse], rubric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_archive(self, client: SGPClient) -> None:
        rubric = client.rubrics.archive(
            "rubric_id",
        )
        assert_matches_type(RubricArchiveResponse, rubric, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: SGPClient) -> None:
        response = client.rubrics.with_raw_response.archive(
            "rubric_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rubric = response.parse()
        assert_matches_type(RubricArchiveResponse, rubric, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: SGPClient) -> None:
        with client.rubrics.with_streaming_response.archive(
            "rubric_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rubric = response.parse()
            assert_matches_type(RubricArchiveResponse, rubric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rubric_id` but received ''"):
            client.rubrics.with_raw_response.archive(
                "",
            )


class TestAsyncRubrics:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        rubric = await async_client.rubrics.create(
            title="x",
        )
        assert_matches_type(RubricResponse, rubric, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        rubric = await async_client.rubrics.create(
            title="x",
            criteria=[
                {
                    "title": "x",
                    "annotations": {"foo": "bar"},
                    "weight": 0,
                }
            ],
            tags=["string"],
        )
        assert_matches_type(RubricResponse, rubric, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.rubrics.with_raw_response.create(
            title="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rubric = await response.parse()
        assert_matches_type(RubricResponse, rubric, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.rubrics.with_streaming_response.create(
            title="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rubric = await response.parse()
            assert_matches_type(RubricResponse, rubric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        rubric = await async_client.rubrics.retrieve(
            "rubric_id",
        )
        assert_matches_type(RubricResponse, rubric, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.rubrics.with_raw_response.retrieve(
            "rubric_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rubric = await response.parse()
        assert_matches_type(RubricResponse, rubric, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.rubrics.with_streaming_response.retrieve(
            "rubric_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rubric = await response.parse()
            assert_matches_type(RubricResponse, rubric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rubric_id` but received ''"):
            await async_client.rubrics.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        rubric = await async_client.rubrics.update(
            rubric_id="rubric_id",
            rubric={},
        )
        assert_matches_type(RubricResponse, rubric, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        rubric = await async_client.rubrics.update(
            rubric_id="rubric_id",
            rubric={
                "tags": ["string"],
                "title": "x",
            },
        )
        assert_matches_type(RubricResponse, rubric, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.rubrics.with_raw_response.update(
            rubric_id="rubric_id",
            rubric={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rubric = await response.parse()
        assert_matches_type(RubricResponse, rubric, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.rubrics.with_streaming_response.update(
            rubric_id="rubric_id",
            rubric={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rubric = await response.parse()
            assert_matches_type(RubricResponse, rubric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rubric_id` but received ''"):
            await async_client.rubrics.with_raw_response.update(
                rubric_id="",
                rubric={},
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        rubric = await async_client.rubrics.list()
        assert_matches_type(AsyncCursorPage[RubricResponse], rubric, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        rubric = await async_client.rubrics.list(
            ending_before="ending_before",
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
            tags=["string"],
            title="title",
        )
        assert_matches_type(AsyncCursorPage[RubricResponse], rubric, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.rubrics.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rubric = await response.parse()
        assert_matches_type(AsyncCursorPage[RubricResponse], rubric, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.rubrics.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rubric = await response.parse()
            assert_matches_type(AsyncCursorPage[RubricResponse], rubric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_archive(self, async_client: AsyncSGPClient) -> None:
        rubric = await async_client.rubrics.archive(
            "rubric_id",
        )
        assert_matches_type(RubricArchiveResponse, rubric, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.rubrics.with_raw_response.archive(
            "rubric_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rubric = await response.parse()
        assert_matches_type(RubricArchiveResponse, rubric, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncSGPClient) -> None:
        async with async_client.rubrics.with_streaming_response.archive(
            "rubric_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rubric = await response.parse()
            assert_matches_type(RubricArchiveResponse, rubric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rubric_id` but received ''"):
            await async_client.rubrics.with_raw_response.archive(
                "",
            )
