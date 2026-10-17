# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from langsmith import Langsmith, AsyncLangsmith
from tests.utils import assert_matches_type
from langsmith.pagination import SyncItemsCursorPostPagination, AsyncItemsCursorPostPagination
from langsmith.types.datasets import ExperimentRunQueryResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestExperimentRuns:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_query(self, client: Langsmith) -> None:
        experiment_run = client.datasets.experiment_runs.query(
            dataset_id="dataset_id",
        )
        assert_matches_type(
            SyncItemsCursorPostPagination[ExperimentRunQueryResponse], experiment_run, path=["response"]
        )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_query_with_all_params(self, client: Langsmith) -> None:
        experiment_run = client.datasets.experiment_runs.query(
            dataset_id="dataset_id",
            comparative_experiment_id="comparative_experiment_id",
            cursor="cursor",
            example_ids=["string"],
            experiment_ids=["string"],
            filters={"foo": ["string"]},
            page_size=0,
            selects=["ID"],
            sort={
                "by": "by",
                "order": "order",
            },
        )
        assert_matches_type(
            SyncItemsCursorPostPagination[ExperimentRunQueryResponse], experiment_run, path=["response"]
        )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_query(self, client: Langsmith) -> None:

        response = client.datasets.experiment_runs.with_raw_response.query(
            dataset_id="dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment_run = response.parse()
        assert_matches_type(
            SyncItemsCursorPostPagination[ExperimentRunQueryResponse], experiment_run, path=["response"]
        )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_query(self, client: Langsmith) -> None:
        with client.datasets.experiment_runs.with_streaming_response.query(
            dataset_id="dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment_run = response.parse()
            assert_matches_type(
                SyncItemsCursorPostPagination[ExperimentRunQueryResponse], experiment_run, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_query(self, client: Langsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            client.datasets.experiment_runs.with_raw_response.query(
                dataset_id="",
            )


class TestAsyncExperimentRuns:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_query(self, async_client: AsyncLangsmith) -> None:
        experiment_run = await async_client.datasets.experiment_runs.query(
            dataset_id="dataset_id",
        )
        assert_matches_type(
            AsyncItemsCursorPostPagination[ExperimentRunQueryResponse], experiment_run, path=["response"]
        )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_query_with_all_params(self, async_client: AsyncLangsmith) -> None:
        experiment_run = await async_client.datasets.experiment_runs.query(
            dataset_id="dataset_id",
            comparative_experiment_id="comparative_experiment_id",
            cursor="cursor",
            example_ids=["string"],
            experiment_ids=["string"],
            filters={"foo": ["string"]},
            page_size=0,
            selects=["ID"],
            sort={
                "by": "by",
                "order": "order",
            },
        )
        assert_matches_type(
            AsyncItemsCursorPostPagination[ExperimentRunQueryResponse], experiment_run, path=["response"]
        )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_query(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.datasets.experiment_runs.with_raw_response.query(
            dataset_id="dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment_run = await response.parse()
        assert_matches_type(
            AsyncItemsCursorPostPagination[ExperimentRunQueryResponse], experiment_run, path=["response"]
        )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_query(self, async_client: AsyncLangsmith) -> None:
        async with async_client.datasets.experiment_runs.with_streaming_response.query(
            dataset_id="dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment_run = await response.parse()
            assert_matches_type(
                AsyncItemsCursorPostPagination[ExperimentRunQueryResponse], experiment_run, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_query(self, async_client: AsyncLangsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            await async_client.datasets.experiment_runs.with_raw_response.query(
                dataset_id="",
            )
