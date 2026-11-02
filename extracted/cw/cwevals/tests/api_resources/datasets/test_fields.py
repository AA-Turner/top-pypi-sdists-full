# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from coreweave_evaluations import Client, AsyncClient
from coreweave_evaluations.types.datasets import FieldCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFields:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Client) -> None:
        field = client.datasets.fields.create(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            fields=[
                {
                    "name": "x",
                    "source": "input",
                    "value_type": "boolean",
                }
            ],
        )
        assert_matches_type(FieldCreateResponse, field, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Client) -> None:
        response = client.datasets.fields.with_raw_response.create(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            fields=[
                {
                    "name": "x",
                    "source": "input",
                    "value_type": "boolean",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        field = response.parse()
        assert_matches_type(FieldCreateResponse, field, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Client) -> None:
        with client.datasets.fields.with_streaming_response.create(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            fields=[
                {
                    "name": "x",
                    "source": "input",
                    "value_type": "boolean",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            field = response.parse()
            assert_matches_type(FieldCreateResponse, field, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.datasets.fields.with_raw_response.create(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
                fields=[
                    {
                        "name": "x",
                        "source": "input",
                        "value_type": "boolean",
                    }
                ],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.datasets.fields.with_raw_response.create(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
                fields=[
                    {
                        "name": "x",
                        "source": "input",
                        "value_type": "boolean",
                    }
                ],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            client.datasets.fields.with_raw_response.create(
                dataset_id="",
                namespace="wandb",
                scope_id="scope_id",
                fields=[
                    {
                        "name": "x",
                        "source": "input",
                        "value_type": "boolean",
                    }
                ],
            )


class TestAsyncFields:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncClient) -> None:
        field = await async_client.datasets.fields.create(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            fields=[
                {
                    "name": "x",
                    "source": "input",
                    "value_type": "boolean",
                }
            ],
        )
        assert_matches_type(FieldCreateResponse, field, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncClient) -> None:
        response = await async_client.datasets.fields.with_raw_response.create(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            fields=[
                {
                    "name": "x",
                    "source": "input",
                    "value_type": "boolean",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        field = await response.parse()
        assert_matches_type(FieldCreateResponse, field, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncClient) -> None:
        async with async_client.datasets.fields.with_streaming_response.create(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            fields=[
                {
                    "name": "x",
                    "source": "input",
                    "value_type": "boolean",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            field = await response.parse()
            assert_matches_type(FieldCreateResponse, field, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.datasets.fields.with_raw_response.create(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
                fields=[
                    {
                        "name": "x",
                        "source": "input",
                        "value_type": "boolean",
                    }
                ],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.datasets.fields.with_raw_response.create(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
                fields=[
                    {
                        "name": "x",
                        "source": "input",
                        "value_type": "boolean",
                    }
                ],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            await async_client.datasets.fields.with_raw_response.create(
                dataset_id="",
                namespace="wandb",
                scope_id="scope_id",
                fields=[
                    {
                        "name": "x",
                        "source": "input",
                        "value_type": "boolean",
                    }
                ],
            )
