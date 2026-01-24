# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from patronus_api import PatronusAPI, AsyncPatronusAPI
from patronus_api.types import (
    ExperimentListResponse,
    ExperimentCreateResponse,
    ExperimentUpdateResponse,
    ExperimentRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestExperiments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: PatronusAPI) -> None:
        experiment = client.experiments.create(
            name="x",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ExperimentCreateResponse, experiment, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: PatronusAPI) -> None:
        experiment = client.experiments.create(
            name="x",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            metadata={},
            tags={},
        )
        assert_matches_type(ExperimentCreateResponse, experiment, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: PatronusAPI) -> None:
        response = client.experiments.with_raw_response.create(
            name="x",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = response.parse()
        assert_matches_type(ExperimentCreateResponse, experiment, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: PatronusAPI) -> None:
        with client.experiments.with_streaming_response.create(
            name="x",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = response.parse()
            assert_matches_type(ExperimentCreateResponse, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: PatronusAPI) -> None:
        experiment = client.experiments.retrieve(
            "id",
        )
        assert_matches_type(ExperimentRetrieveResponse, experiment, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: PatronusAPI) -> None:
        response = client.experiments.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = response.parse()
        assert_matches_type(ExperimentRetrieveResponse, experiment, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: PatronusAPI) -> None:
        with client.experiments.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = response.parse()
            assert_matches_type(ExperimentRetrieveResponse, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: PatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.experiments.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: PatronusAPI) -> None:
        experiment = client.experiments.update(
            id="id",
            metadata={},
        )
        assert_matches_type(ExperimentUpdateResponse, experiment, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: PatronusAPI) -> None:
        response = client.experiments.with_raw_response.update(
            id="id",
            metadata={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = response.parse()
        assert_matches_type(ExperimentUpdateResponse, experiment, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: PatronusAPI) -> None:
        with client.experiments.with_streaming_response.update(
            id="id",
            metadata={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = response.parse()
            assert_matches_type(ExperimentUpdateResponse, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: PatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.experiments.with_raw_response.update(
                id="",
                metadata={},
            )

    @parametrize
    def test_method_list(self, client: PatronusAPI) -> None:
        experiment = client.experiments.list()
        assert_matches_type(ExperimentListResponse, experiment, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: PatronusAPI) -> None:
        experiment = client.experiments.list(
            limit=1,
            offset=0,
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ExperimentListResponse, experiment, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: PatronusAPI) -> None:
        response = client.experiments.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = response.parse()
        assert_matches_type(ExperimentListResponse, experiment, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: PatronusAPI) -> None:
        with client.experiments.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = response.parse()
            assert_matches_type(ExperimentListResponse, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: PatronusAPI) -> None:
        experiment = client.experiments.delete(
            "id",
        )
        assert experiment is None

    @parametrize
    def test_raw_response_delete(self, client: PatronusAPI) -> None:
        response = client.experiments.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = response.parse()
        assert experiment is None

    @parametrize
    def test_streaming_response_delete(self, client: PatronusAPI) -> None:
        with client.experiments.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = response.parse()
            assert experiment is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: PatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.experiments.with_raw_response.delete(
                "",
            )


class TestAsyncExperiments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncPatronusAPI) -> None:
        experiment = await async_client.experiments.create(
            name="x",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ExperimentCreateResponse, experiment, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        experiment = await async_client.experiments.create(
            name="x",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            metadata={},
            tags={},
        )
        assert_matches_type(ExperimentCreateResponse, experiment, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.experiments.with_raw_response.create(
            name="x",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = await response.parse()
        assert_matches_type(ExperimentCreateResponse, experiment, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.experiments.with_streaming_response.create(
            name="x",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = await response.parse()
            assert_matches_type(ExperimentCreateResponse, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncPatronusAPI) -> None:
        experiment = await async_client.experiments.retrieve(
            "id",
        )
        assert_matches_type(ExperimentRetrieveResponse, experiment, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.experiments.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = await response.parse()
        assert_matches_type(ExperimentRetrieveResponse, experiment, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.experiments.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = await response.parse()
            assert_matches_type(ExperimentRetrieveResponse, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncPatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.experiments.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncPatronusAPI) -> None:
        experiment = await async_client.experiments.update(
            id="id",
            metadata={},
        )
        assert_matches_type(ExperimentUpdateResponse, experiment, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.experiments.with_raw_response.update(
            id="id",
            metadata={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = await response.parse()
        assert_matches_type(ExperimentUpdateResponse, experiment, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.experiments.with_streaming_response.update(
            id="id",
            metadata={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = await response.parse()
            assert_matches_type(ExperimentUpdateResponse, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncPatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.experiments.with_raw_response.update(
                id="",
                metadata={},
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncPatronusAPI) -> None:
        experiment = await async_client.experiments.list()
        assert_matches_type(ExperimentListResponse, experiment, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        experiment = await async_client.experiments.list(
            limit=1,
            offset=0,
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ExperimentListResponse, experiment, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.experiments.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = await response.parse()
        assert_matches_type(ExperimentListResponse, experiment, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.experiments.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = await response.parse()
            assert_matches_type(ExperimentListResponse, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncPatronusAPI) -> None:
        experiment = await async_client.experiments.delete(
            "id",
        )
        assert experiment is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.experiments.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = await response.parse()
        assert experiment is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.experiments.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = await response.parse()
            assert experiment is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncPatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.experiments.with_raw_response.delete(
                "",
            )
