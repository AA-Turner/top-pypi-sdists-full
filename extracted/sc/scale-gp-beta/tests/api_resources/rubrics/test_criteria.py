# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types.rubrics import (
    RubricCriteriaResponse,
    CriterionListVersionsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCriteria:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        criterion = client.rubrics.criteria.create(
            rubric_id="rubric_id",
            title="x",
        )
        assert_matches_type(RubricCriteriaResponse, criterion, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        criterion = client.rubrics.criteria.create(
            rubric_id="rubric_id",
            title="x",
            annotations={"foo": "bar"},
            weight=0,
        )
        assert_matches_type(RubricCriteriaResponse, criterion, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.rubrics.criteria.with_raw_response.create(
            rubric_id="rubric_id",
            title="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        criterion = response.parse()
        assert_matches_type(RubricCriteriaResponse, criterion, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.rubrics.criteria.with_streaming_response.create(
            rubric_id="rubric_id",
            title="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            criterion = response.parse()
            assert_matches_type(RubricCriteriaResponse, criterion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rubric_id` but received ''"):
            client.rubrics.criteria.with_raw_response.create(
                rubric_id="",
                title="x",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        criterion = client.rubrics.criteria.update(
            rubric_criteria_id="rubric_criteria_id",
            rubric_id="rubric_id",
        )
        assert_matches_type(RubricCriteriaResponse, criterion, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        criterion = client.rubrics.criteria.update(
            rubric_criteria_id="rubric_criteria_id",
            rubric_id="rubric_id",
            annotations={"foo": "bar"},
            title="x",
            weight=0,
        )
        assert_matches_type(RubricCriteriaResponse, criterion, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.rubrics.criteria.with_raw_response.update(
            rubric_criteria_id="rubric_criteria_id",
            rubric_id="rubric_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        criterion = response.parse()
        assert_matches_type(RubricCriteriaResponse, criterion, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.rubrics.criteria.with_streaming_response.update(
            rubric_criteria_id="rubric_criteria_id",
            rubric_id="rubric_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            criterion = response.parse()
            assert_matches_type(RubricCriteriaResponse, criterion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rubric_id` but received ''"):
            client.rubrics.criteria.with_raw_response.update(
                rubric_criteria_id="rubric_criteria_id",
                rubric_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rubric_criteria_id` but received ''"):
            client.rubrics.criteria.with_raw_response.update(
                rubric_criteria_id="",
                rubric_id="rubric_id",
            )

    @parametrize
    def test_method_list_versions(self, client: SGPClient) -> None:
        criterion = client.rubrics.criteria.list_versions(
            rubric_criteria_id="rubric_criteria_id",
            rubric_id="rubric_id",
        )
        assert_matches_type(CriterionListVersionsResponse, criterion, path=["response"])

    @parametrize
    def test_method_list_versions_with_all_params(self, client: SGPClient) -> None:
        criterion = client.rubrics.criteria.list_versions(
            rubric_criteria_id="rubric_criteria_id",
            rubric_id="rubric_id",
            ending_before="ending_before",
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(CriterionListVersionsResponse, criterion, path=["response"])

    @parametrize
    def test_raw_response_list_versions(self, client: SGPClient) -> None:
        response = client.rubrics.criteria.with_raw_response.list_versions(
            rubric_criteria_id="rubric_criteria_id",
            rubric_id="rubric_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        criterion = response.parse()
        assert_matches_type(CriterionListVersionsResponse, criterion, path=["response"])

    @parametrize
    def test_streaming_response_list_versions(self, client: SGPClient) -> None:
        with client.rubrics.criteria.with_streaming_response.list_versions(
            rubric_criteria_id="rubric_criteria_id",
            rubric_id="rubric_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            criterion = response.parse()
            assert_matches_type(CriterionListVersionsResponse, criterion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list_versions(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rubric_id` but received ''"):
            client.rubrics.criteria.with_raw_response.list_versions(
                rubric_criteria_id="rubric_criteria_id",
                rubric_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rubric_criteria_id` but received ''"):
            client.rubrics.criteria.with_raw_response.list_versions(
                rubric_criteria_id="",
                rubric_id="rubric_id",
            )


class TestAsyncCriteria:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        criterion = await async_client.rubrics.criteria.create(
            rubric_id="rubric_id",
            title="x",
        )
        assert_matches_type(RubricCriteriaResponse, criterion, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        criterion = await async_client.rubrics.criteria.create(
            rubric_id="rubric_id",
            title="x",
            annotations={"foo": "bar"},
            weight=0,
        )
        assert_matches_type(RubricCriteriaResponse, criterion, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.rubrics.criteria.with_raw_response.create(
            rubric_id="rubric_id",
            title="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        criterion = await response.parse()
        assert_matches_type(RubricCriteriaResponse, criterion, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.rubrics.criteria.with_streaming_response.create(
            rubric_id="rubric_id",
            title="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            criterion = await response.parse()
            assert_matches_type(RubricCriteriaResponse, criterion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rubric_id` but received ''"):
            await async_client.rubrics.criteria.with_raw_response.create(
                rubric_id="",
                title="x",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        criterion = await async_client.rubrics.criteria.update(
            rubric_criteria_id="rubric_criteria_id",
            rubric_id="rubric_id",
        )
        assert_matches_type(RubricCriteriaResponse, criterion, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        criterion = await async_client.rubrics.criteria.update(
            rubric_criteria_id="rubric_criteria_id",
            rubric_id="rubric_id",
            annotations={"foo": "bar"},
            title="x",
            weight=0,
        )
        assert_matches_type(RubricCriteriaResponse, criterion, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.rubrics.criteria.with_raw_response.update(
            rubric_criteria_id="rubric_criteria_id",
            rubric_id="rubric_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        criterion = await response.parse()
        assert_matches_type(RubricCriteriaResponse, criterion, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.rubrics.criteria.with_streaming_response.update(
            rubric_criteria_id="rubric_criteria_id",
            rubric_id="rubric_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            criterion = await response.parse()
            assert_matches_type(RubricCriteriaResponse, criterion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rubric_id` but received ''"):
            await async_client.rubrics.criteria.with_raw_response.update(
                rubric_criteria_id="rubric_criteria_id",
                rubric_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rubric_criteria_id` but received ''"):
            await async_client.rubrics.criteria.with_raw_response.update(
                rubric_criteria_id="",
                rubric_id="rubric_id",
            )

    @parametrize
    async def test_method_list_versions(self, async_client: AsyncSGPClient) -> None:
        criterion = await async_client.rubrics.criteria.list_versions(
            rubric_criteria_id="rubric_criteria_id",
            rubric_id="rubric_id",
        )
        assert_matches_type(CriterionListVersionsResponse, criterion, path=["response"])

    @parametrize
    async def test_method_list_versions_with_all_params(self, async_client: AsyncSGPClient) -> None:
        criterion = await async_client.rubrics.criteria.list_versions(
            rubric_criteria_id="rubric_criteria_id",
            rubric_id="rubric_id",
            ending_before="ending_before",
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(CriterionListVersionsResponse, criterion, path=["response"])

    @parametrize
    async def test_raw_response_list_versions(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.rubrics.criteria.with_raw_response.list_versions(
            rubric_criteria_id="rubric_criteria_id",
            rubric_id="rubric_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        criterion = await response.parse()
        assert_matches_type(CriterionListVersionsResponse, criterion, path=["response"])

    @parametrize
    async def test_streaming_response_list_versions(self, async_client: AsyncSGPClient) -> None:
        async with async_client.rubrics.criteria.with_streaming_response.list_versions(
            rubric_criteria_id="rubric_criteria_id",
            rubric_id="rubric_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            criterion = await response.parse()
            assert_matches_type(CriterionListVersionsResponse, criterion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list_versions(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rubric_id` but received ''"):
            await async_client.rubrics.criteria.with_raw_response.list_versions(
                rubric_criteria_id="rubric_criteria_id",
                rubric_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rubric_criteria_id` but received ''"):
            await async_client.rubrics.criteria.with_raw_response.list_versions(
                rubric_criteria_id="",
                rubric_id="rubric_id",
            )
