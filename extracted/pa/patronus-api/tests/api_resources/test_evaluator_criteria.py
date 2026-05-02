# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from patronus_api import PatronusAPI, AsyncPatronusAPI
from patronus_api.types import (
    EvaluatorCriterionListResponse,
    EvaluatorCriterionCreateResponse,
    EvaluatorCriterionArchiveResponse,
    EvaluatorCriterionAddRevisionResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvaluatorCriteria:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: PatronusAPI) -> None:
        evaluator_criterion = client.evaluator_criteria.create(
            config={},
            evaluator_family="evaluator_family",
            name="name",
        )
        assert_matches_type(EvaluatorCriterionCreateResponse, evaluator_criterion, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: PatronusAPI) -> None:
        evaluator_criterion = client.evaluator_criteria.create(
            config={},
            evaluator_family="evaluator_family",
            name="name",
            description="description",
        )
        assert_matches_type(EvaluatorCriterionCreateResponse, evaluator_criterion, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: PatronusAPI) -> None:
        response = client.evaluator_criteria.with_raw_response.create(
            config={},
            evaluator_family="evaluator_family",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluator_criterion = response.parse()
        assert_matches_type(EvaluatorCriterionCreateResponse, evaluator_criterion, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: PatronusAPI) -> None:
        with client.evaluator_criteria.with_streaming_response.create(
            config={},
            evaluator_family="evaluator_family",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluator_criterion = response.parse()
            assert_matches_type(EvaluatorCriterionCreateResponse, evaluator_criterion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: PatronusAPI) -> None:
        evaluator_criterion = client.evaluator_criteria.list()
        assert_matches_type(EvaluatorCriterionListResponse, evaluator_criterion, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: PatronusAPI) -> None:
        evaluator_criterion = client.evaluator_criteria.list(
            enabled=True,
            evaluator_family="evaluator_family",
            get_last_revision=True,
            is_patronus_managed=True,
            limit=0,
            name="name",
            offset=0,
            public_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            revision=0,
        )
        assert_matches_type(EvaluatorCriterionListResponse, evaluator_criterion, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: PatronusAPI) -> None:
        response = client.evaluator_criteria.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluator_criterion = response.parse()
        assert_matches_type(EvaluatorCriterionListResponse, evaluator_criterion, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: PatronusAPI) -> None:
        with client.evaluator_criteria.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluator_criterion = response.parse()
            assert_matches_type(EvaluatorCriterionListResponse, evaluator_criterion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_add_revision(self, client: PatronusAPI) -> None:
        evaluator_criterion = client.evaluator_criteria.add_revision(
            public_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={},
        )
        assert_matches_type(EvaluatorCriterionAddRevisionResponse, evaluator_criterion, path=["response"])

    @parametrize
    def test_method_add_revision_with_all_params(self, client: PatronusAPI) -> None:
        evaluator_criterion = client.evaluator_criteria.add_revision(
            public_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={},
            description="description",
        )
        assert_matches_type(EvaluatorCriterionAddRevisionResponse, evaluator_criterion, path=["response"])

    @parametrize
    def test_raw_response_add_revision(self, client: PatronusAPI) -> None:
        response = client.evaluator_criteria.with_raw_response.add_revision(
            public_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluator_criterion = response.parse()
        assert_matches_type(EvaluatorCriterionAddRevisionResponse, evaluator_criterion, path=["response"])

    @parametrize
    def test_streaming_response_add_revision(self, client: PatronusAPI) -> None:
        with client.evaluator_criteria.with_streaming_response.add_revision(
            public_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluator_criterion = response.parse()
            assert_matches_type(EvaluatorCriterionAddRevisionResponse, evaluator_criterion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_add_revision(self, client: PatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `public_id` but received ''"):
            client.evaluator_criteria.with_raw_response.add_revision(
                public_id="",
                config={},
            )

    @parametrize
    def test_method_archive(self, client: PatronusAPI) -> None:
        evaluator_criterion = client.evaluator_criteria.archive(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(EvaluatorCriterionArchiveResponse, evaluator_criterion, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: PatronusAPI) -> None:
        response = client.evaluator_criteria.with_raw_response.archive(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluator_criterion = response.parse()
        assert_matches_type(EvaluatorCriterionArchiveResponse, evaluator_criterion, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: PatronusAPI) -> None:
        with client.evaluator_criteria.with_streaming_response.archive(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluator_criterion = response.parse()
            assert_matches_type(EvaluatorCriterionArchiveResponse, evaluator_criterion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: PatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `public_id` but received ''"):
            client.evaluator_criteria.with_raw_response.archive(
                "",
            )


class TestAsyncEvaluatorCriteria:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncPatronusAPI) -> None:
        evaluator_criterion = await async_client.evaluator_criteria.create(
            config={},
            evaluator_family="evaluator_family",
            name="name",
        )
        assert_matches_type(EvaluatorCriterionCreateResponse, evaluator_criterion, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        evaluator_criterion = await async_client.evaluator_criteria.create(
            config={},
            evaluator_family="evaluator_family",
            name="name",
            description="description",
        )
        assert_matches_type(EvaluatorCriterionCreateResponse, evaluator_criterion, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.evaluator_criteria.with_raw_response.create(
            config={},
            evaluator_family="evaluator_family",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluator_criterion = await response.parse()
        assert_matches_type(EvaluatorCriterionCreateResponse, evaluator_criterion, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.evaluator_criteria.with_streaming_response.create(
            config={},
            evaluator_family="evaluator_family",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluator_criterion = await response.parse()
            assert_matches_type(EvaluatorCriterionCreateResponse, evaluator_criterion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncPatronusAPI) -> None:
        evaluator_criterion = await async_client.evaluator_criteria.list()
        assert_matches_type(EvaluatorCriterionListResponse, evaluator_criterion, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        evaluator_criterion = await async_client.evaluator_criteria.list(
            enabled=True,
            evaluator_family="evaluator_family",
            get_last_revision=True,
            is_patronus_managed=True,
            limit=0,
            name="name",
            offset=0,
            public_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            revision=0,
        )
        assert_matches_type(EvaluatorCriterionListResponse, evaluator_criterion, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.evaluator_criteria.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluator_criterion = await response.parse()
        assert_matches_type(EvaluatorCriterionListResponse, evaluator_criterion, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.evaluator_criteria.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluator_criterion = await response.parse()
            assert_matches_type(EvaluatorCriterionListResponse, evaluator_criterion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_add_revision(self, async_client: AsyncPatronusAPI) -> None:
        evaluator_criterion = await async_client.evaluator_criteria.add_revision(
            public_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={},
        )
        assert_matches_type(EvaluatorCriterionAddRevisionResponse, evaluator_criterion, path=["response"])

    @parametrize
    async def test_method_add_revision_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        evaluator_criterion = await async_client.evaluator_criteria.add_revision(
            public_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={},
            description="description",
        )
        assert_matches_type(EvaluatorCriterionAddRevisionResponse, evaluator_criterion, path=["response"])

    @parametrize
    async def test_raw_response_add_revision(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.evaluator_criteria.with_raw_response.add_revision(
            public_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluator_criterion = await response.parse()
        assert_matches_type(EvaluatorCriterionAddRevisionResponse, evaluator_criterion, path=["response"])

    @parametrize
    async def test_streaming_response_add_revision(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.evaluator_criteria.with_streaming_response.add_revision(
            public_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluator_criterion = await response.parse()
            assert_matches_type(EvaluatorCriterionAddRevisionResponse, evaluator_criterion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_add_revision(self, async_client: AsyncPatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `public_id` but received ''"):
            await async_client.evaluator_criteria.with_raw_response.add_revision(
                public_id="",
                config={},
            )

    @parametrize
    async def test_method_archive(self, async_client: AsyncPatronusAPI) -> None:
        evaluator_criterion = await async_client.evaluator_criteria.archive(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(EvaluatorCriterionArchiveResponse, evaluator_criterion, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.evaluator_criteria.with_raw_response.archive(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluator_criterion = await response.parse()
        assert_matches_type(EvaluatorCriterionArchiveResponse, evaluator_criterion, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.evaluator_criteria.with_streaming_response.archive(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluator_criterion = await response.parse()
            assert_matches_type(EvaluatorCriterionArchiveResponse, evaluator_criterion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncPatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `public_id` but received ''"):
            await async_client.evaluator_criteria.with_raw_response.archive(
                "",
            )
