# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from coreweave_evaluations import Client, AsyncClient
from coreweave_evaluations.types.evaluations import ScorerAddResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestScorers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_add(self, client: Client) -> None:
        scorer = client.evaluations.scorers.add(
            evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            scorers=[
                {
                    "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                }
            ],
        )
        assert_matches_type(ScorerAddResponse, scorer, path=["response"])

    @parametrize
    def test_raw_response_add(self, client: Client) -> None:
        response = client.evaluations.scorers.with_raw_response.add(
            evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            scorers=[
                {
                    "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scorer = response.parse()
        assert_matches_type(ScorerAddResponse, scorer, path=["response"])

    @parametrize
    def test_streaming_response_add(self, client: Client) -> None:
        with client.evaluations.scorers.with_streaming_response.add(
            evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            scorers=[
                {
                    "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scorer = response.parse()
            assert_matches_type(ScorerAddResponse, scorer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_add(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.evaluations.scorers.with_raw_response.add(
                evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
                scorers=[
                    {
                        "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    }
                ],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.evaluations.scorers.with_raw_response.add(
                evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
                scorers=[
                    {
                        "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    }
                ],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.scorers.with_raw_response.add(
                evaluation_id="",
                namespace="wandb",
                scope_id="scope_id",
                scorers=[
                    {
                        "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    }
                ],
            )


class TestAsyncScorers:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_add(self, async_client: AsyncClient) -> None:
        scorer = await async_client.evaluations.scorers.add(
            evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            scorers=[
                {
                    "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                }
            ],
        )
        assert_matches_type(ScorerAddResponse, scorer, path=["response"])

    @parametrize
    async def test_raw_response_add(self, async_client: AsyncClient) -> None:
        response = await async_client.evaluations.scorers.with_raw_response.add(
            evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            scorers=[
                {
                    "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scorer = await response.parse()
        assert_matches_type(ScorerAddResponse, scorer, path=["response"])

    @parametrize
    async def test_streaming_response_add(self, async_client: AsyncClient) -> None:
        async with async_client.evaluations.scorers.with_streaming_response.add(
            evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            scorers=[
                {
                    "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scorer = await response.parse()
            assert_matches_type(ScorerAddResponse, scorer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_add(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.evaluations.scorers.with_raw_response.add(
                evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
                scorers=[
                    {
                        "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    }
                ],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.evaluations.scorers.with_raw_response.add(
                evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
                scorers=[
                    {
                        "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    }
                ],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.scorers.with_raw_response.add(
                evaluation_id="",
                namespace="wandb",
                scope_id="scope_id",
                scorers=[
                    {
                        "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    }
                ],
            )
