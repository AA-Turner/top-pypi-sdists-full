# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import (
    EvaluationGroup,
    EvaluationGroupRetrieveSchemaResponse,
)
from scale_gp_beta.pagination import SyncCursorPage, AsyncCursorPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvaluationGroups:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        evaluation_group = client.evaluation_groups.create(
            evaluation_ids=["string"],
            name="name",
        )
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        evaluation_group = client.evaluation_groups.create(
            evaluation_ids=["string"],
            name="name",
            description="description",
            metadata={
                "project": "bar",
                "team": "bar",
            },
            row_identifiers={
                "eval-123": "user_id",
                "eval-456": "customer_id",
            },
            tags=["string"],
        )
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.evaluation_groups.with_raw_response.create(
            evaluation_ids=["string"],
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_group = response.parse()
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.evaluation_groups.with_streaming_response.create(
            evaluation_ids=["string"],
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_group = response.parse()
            assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        evaluation_group = client.evaluation_groups.retrieve(
            group_id="group_id",
        )
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGPClient) -> None:
        evaluation_group = client.evaluation_groups.retrieve(
            group_id="group_id",
            include_deleted=True,
            views=["members"],
        )
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.evaluation_groups.with_raw_response.retrieve(
            group_id="group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_group = response.parse()
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.evaluation_groups.with_streaming_response.retrieve(
            group_id="group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_group = response.parse()
            assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `group_id` but received ''"):
            client.evaluation_groups.with_raw_response.retrieve(
                group_id="",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        evaluation_group = client.evaluation_groups.update(
            group_id="group_id",
        )
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        evaluation_group = client.evaluation_groups.update(
            group_id="group_id",
            description="description",
            metadata={"foo": "bar"},
            name="name",
            row_identifiers={"foo": "string"},
            tags=["string"],
        )
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.evaluation_groups.with_raw_response.update(
            group_id="group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_group = response.parse()
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.evaluation_groups.with_streaming_response.update(
            group_id="group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_group = response.parse()
            assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `group_id` but received ''"):
            client.evaluation_groups.with_raw_response.update(
                group_id="",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        evaluation_group = client.evaluation_groups.list()
        assert_matches_type(SyncCursorPage[EvaluationGroup], evaluation_group, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        evaluation_group = client.evaluation_groups.list(
            ending_before="ending_before",
            evaluation_id="evaluation_id",
            include_deleted=True,
            limit=1,
            name="name",
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
            tags=["string"],
            views=["members"],
        )
        assert_matches_type(SyncCursorPage[EvaluationGroup], evaluation_group, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.evaluation_groups.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_group = response.parse()
        assert_matches_type(SyncCursorPage[EvaluationGroup], evaluation_group, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.evaluation_groups.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_group = response.parse()
            assert_matches_type(SyncCursorPage[EvaluationGroup], evaluation_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_archive(self, client: SGPClient) -> None:
        evaluation_group = client.evaluation_groups.archive(
            "group_id",
        )
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: SGPClient) -> None:
        response = client.evaluation_groups.with_raw_response.archive(
            "group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_group = response.parse()
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: SGPClient) -> None:
        with client.evaluation_groups.with_streaming_response.archive(
            "group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_group = response.parse()
            assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `group_id` but received ''"):
            client.evaluation_groups.with_raw_response.archive(
                "",
            )

    @parametrize
    def test_method_replace(self, client: SGPClient) -> None:
        evaluation_group = client.evaluation_groups.replace(
            group_id="group_id",
        )
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    def test_method_replace_with_all_params(self, client: SGPClient) -> None:
        evaluation_group = client.evaluation_groups.replace(
            group_id="group_id",
            description="description",
            evaluation_ids=["string"],
            metadata={"foo": "bar"},
            name="name",
            row_identifiers={"foo": "string"},
            tags=["string"],
        )
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    def test_raw_response_replace(self, client: SGPClient) -> None:
        response = client.evaluation_groups.with_raw_response.replace(
            group_id="group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_group = response.parse()
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    def test_streaming_response_replace(self, client: SGPClient) -> None:
        with client.evaluation_groups.with_streaming_response.replace(
            group_id="group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_group = response.parse()
            assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_replace(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `group_id` but received ''"):
            client.evaluation_groups.with_raw_response.replace(
                group_id="",
            )

    @parametrize
    def test_method_retrieve_schema(self, client: SGPClient) -> None:
        evaluation_group = client.evaluation_groups.retrieve_schema(
            group_id="group_id",
        )
        assert_matches_type(EvaluationGroupRetrieveSchemaResponse, evaluation_group, path=["response"])

    @parametrize
    def test_method_retrieve_schema_with_all_params(self, client: SGPClient) -> None:
        evaluation_group = client.evaluation_groups.retrieve_schema(
            group_id="group_id",
            include_archived=True,
        )
        assert_matches_type(EvaluationGroupRetrieveSchemaResponse, evaluation_group, path=["response"])

    @parametrize
    def test_raw_response_retrieve_schema(self, client: SGPClient) -> None:
        response = client.evaluation_groups.with_raw_response.retrieve_schema(
            group_id="group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_group = response.parse()
        assert_matches_type(EvaluationGroupRetrieveSchemaResponse, evaluation_group, path=["response"])

    @parametrize
    def test_streaming_response_retrieve_schema(self, client: SGPClient) -> None:
        with client.evaluation_groups.with_streaming_response.retrieve_schema(
            group_id="group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_group = response.parse()
            assert_matches_type(EvaluationGroupRetrieveSchemaResponse, evaluation_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve_schema(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `group_id` but received ''"):
            client.evaluation_groups.with_raw_response.retrieve_schema(
                group_id="",
            )


class TestAsyncEvaluationGroups:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        evaluation_group = await async_client.evaluation_groups.create(
            evaluation_ids=["string"],
            name="name",
        )
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation_group = await async_client.evaluation_groups.create(
            evaluation_ids=["string"],
            name="name",
            description="description",
            metadata={
                "project": "bar",
                "team": "bar",
            },
            row_identifiers={
                "eval-123": "user_id",
                "eval-456": "customer_id",
            },
            tags=["string"],
        )
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_groups.with_raw_response.create(
            evaluation_ids=["string"],
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_group = await response.parse()
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_groups.with_streaming_response.create(
            evaluation_ids=["string"],
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_group = await response.parse()
            assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        evaluation_group = await async_client.evaluation_groups.retrieve(
            group_id="group_id",
        )
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation_group = await async_client.evaluation_groups.retrieve(
            group_id="group_id",
            include_deleted=True,
            views=["members"],
        )
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_groups.with_raw_response.retrieve(
            group_id="group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_group = await response.parse()
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_groups.with_streaming_response.retrieve(
            group_id="group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_group = await response.parse()
            assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `group_id` but received ''"):
            await async_client.evaluation_groups.with_raw_response.retrieve(
                group_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        evaluation_group = await async_client.evaluation_groups.update(
            group_id="group_id",
        )
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation_group = await async_client.evaluation_groups.update(
            group_id="group_id",
            description="description",
            metadata={"foo": "bar"},
            name="name",
            row_identifiers={"foo": "string"},
            tags=["string"],
        )
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_groups.with_raw_response.update(
            group_id="group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_group = await response.parse()
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_groups.with_streaming_response.update(
            group_id="group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_group = await response.parse()
            assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `group_id` but received ''"):
            await async_client.evaluation_groups.with_raw_response.update(
                group_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        evaluation_group = await async_client.evaluation_groups.list()
        assert_matches_type(AsyncCursorPage[EvaluationGroup], evaluation_group, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation_group = await async_client.evaluation_groups.list(
            ending_before="ending_before",
            evaluation_id="evaluation_id",
            include_deleted=True,
            limit=1,
            name="name",
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
            tags=["string"],
            views=["members"],
        )
        assert_matches_type(AsyncCursorPage[EvaluationGroup], evaluation_group, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_groups.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_group = await response.parse()
        assert_matches_type(AsyncCursorPage[EvaluationGroup], evaluation_group, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_groups.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_group = await response.parse()
            assert_matches_type(AsyncCursorPage[EvaluationGroup], evaluation_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_archive(self, async_client: AsyncSGPClient) -> None:
        evaluation_group = await async_client.evaluation_groups.archive(
            "group_id",
        )
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_groups.with_raw_response.archive(
            "group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_group = await response.parse()
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_groups.with_streaming_response.archive(
            "group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_group = await response.parse()
            assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `group_id` but received ''"):
            await async_client.evaluation_groups.with_raw_response.archive(
                "",
            )

    @parametrize
    async def test_method_replace(self, async_client: AsyncSGPClient) -> None:
        evaluation_group = await async_client.evaluation_groups.replace(
            group_id="group_id",
        )
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    async def test_method_replace_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation_group = await async_client.evaluation_groups.replace(
            group_id="group_id",
            description="description",
            evaluation_ids=["string"],
            metadata={"foo": "bar"},
            name="name",
            row_identifiers={"foo": "string"},
            tags=["string"],
        )
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    async def test_raw_response_replace(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_groups.with_raw_response.replace(
            group_id="group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_group = await response.parse()
        assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

    @parametrize
    async def test_streaming_response_replace(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_groups.with_streaming_response.replace(
            group_id="group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_group = await response.parse()
            assert_matches_type(EvaluationGroup, evaluation_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_replace(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `group_id` but received ''"):
            await async_client.evaluation_groups.with_raw_response.replace(
                group_id="",
            )

    @parametrize
    async def test_method_retrieve_schema(self, async_client: AsyncSGPClient) -> None:
        evaluation_group = await async_client.evaluation_groups.retrieve_schema(
            group_id="group_id",
        )
        assert_matches_type(EvaluationGroupRetrieveSchemaResponse, evaluation_group, path=["response"])

    @parametrize
    async def test_method_retrieve_schema_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation_group = await async_client.evaluation_groups.retrieve_schema(
            group_id="group_id",
            include_archived=True,
        )
        assert_matches_type(EvaluationGroupRetrieveSchemaResponse, evaluation_group, path=["response"])

    @parametrize
    async def test_raw_response_retrieve_schema(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_groups.with_raw_response.retrieve_schema(
            group_id="group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_group = await response.parse()
        assert_matches_type(EvaluationGroupRetrieveSchemaResponse, evaluation_group, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve_schema(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_groups.with_streaming_response.retrieve_schema(
            group_id="group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_group = await response.parse()
            assert_matches_type(EvaluationGroupRetrieveSchemaResponse, evaluation_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve_schema(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `group_id` but received ''"):
            await async_client.evaluation_groups.with_raw_response.retrieve_schema(
                group_id="",
            )
