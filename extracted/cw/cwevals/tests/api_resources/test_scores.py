# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from coreweave_evaluations import Client, AsyncClient
from coreweave_evaluations.types import ScoreGetResponse, ScoreCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestScores:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Client) -> None:
        score = client.scores.create(
            namespace="wandb",
            scope_id="scope_id",
            scores=[
                {
                    "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "scorer_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "target": {
                        "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "kind": "case",
                    },
                    "value": {},
                }
            ],
        )
        assert_matches_type(ScoreCreateResponse, score, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Client) -> None:
        response = client.scores.with_raw_response.create(
            namespace="wandb",
            scope_id="scope_id",
            scores=[
                {
                    "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "scorer_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "target": {
                        "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "kind": "case",
                    },
                    "value": {},
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        score = response.parse()
        assert_matches_type(ScoreCreateResponse, score, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Client) -> None:
        with client.scores.with_streaming_response.create(
            namespace="wandb",
            scope_id="scope_id",
            scores=[
                {
                    "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "scorer_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "target": {
                        "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "kind": "case",
                    },
                    "value": {},
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            score = response.parse()
            assert_matches_type(ScoreCreateResponse, score, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.scores.with_raw_response.create(
                namespace="",
                scope_id="scope_id",
                scores=[
                    {
                        "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "scorer_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "target": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "kind": "case",
                        },
                        "value": {},
                    }
                ],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.scores.with_raw_response.create(
                namespace="wandb",
                scope_id="",
                scores=[
                    {
                        "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "scorer_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "target": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "kind": "case",
                        },
                        "value": {},
                    }
                ],
            )

    @parametrize
    def test_method_get(self, client: Client) -> None:
        score = client.scores.get(
            score_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )
        assert_matches_type(ScoreGetResponse, score, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Client) -> None:
        response = client.scores.with_raw_response.get(
            score_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        score = response.parse()
        assert_matches_type(ScoreGetResponse, score, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Client) -> None:
        with client.scores.with_streaming_response.get(
            score_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            score = response.parse()
            assert_matches_type(ScoreGetResponse, score, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.scores.with_raw_response.get(
                score_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.scores.with_raw_response.get(
                score_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `score_id` but received ''"):
            client.scores.with_raw_response.get(
                score_id="",
                namespace="wandb",
                scope_id="scope_id",
            )


class TestAsyncScores:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncClient) -> None:
        score = await async_client.scores.create(
            namespace="wandb",
            scope_id="scope_id",
            scores=[
                {
                    "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "scorer_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "target": {
                        "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "kind": "case",
                    },
                    "value": {},
                }
            ],
        )
        assert_matches_type(ScoreCreateResponse, score, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncClient) -> None:
        response = await async_client.scores.with_raw_response.create(
            namespace="wandb",
            scope_id="scope_id",
            scores=[
                {
                    "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "scorer_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "target": {
                        "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "kind": "case",
                    },
                    "value": {},
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        score = await response.parse()
        assert_matches_type(ScoreCreateResponse, score, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncClient) -> None:
        async with async_client.scores.with_streaming_response.create(
            namespace="wandb",
            scope_id="scope_id",
            scores=[
                {
                    "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "scorer_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "target": {
                        "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "kind": "case",
                    },
                    "value": {},
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            score = await response.parse()
            assert_matches_type(ScoreCreateResponse, score, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.scores.with_raw_response.create(
                namespace="",
                scope_id="scope_id",
                scores=[
                    {
                        "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "scorer_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "target": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "kind": "case",
                        },
                        "value": {},
                    }
                ],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.scores.with_raw_response.create(
                namespace="wandb",
                scope_id="",
                scores=[
                    {
                        "scorer_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "scorer_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "target": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "kind": "case",
                        },
                        "value": {},
                    }
                ],
            )

    @parametrize
    async def test_method_get(self, async_client: AsyncClient) -> None:
        score = await async_client.scores.get(
            score_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )
        assert_matches_type(ScoreGetResponse, score, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncClient) -> None:
        response = await async_client.scores.with_raw_response.get(
            score_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        score = await response.parse()
        assert_matches_type(ScoreGetResponse, score, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncClient) -> None:
        async with async_client.scores.with_streaming_response.get(
            score_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            score = await response.parse()
            assert_matches_type(ScoreGetResponse, score, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.scores.with_raw_response.get(
                score_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.scores.with_raw_response.get(
                score_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `score_id` but received ''"):
            await async_client.scores.with_raw_response.get(
                score_id="",
                namespace="wandb",
                scope_id="scope_id",
            )
