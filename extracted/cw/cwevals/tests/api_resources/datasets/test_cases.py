# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from coreweave_evaluations import Client, AsyncClient
from coreweave_evaluations.types.datasets import CaseAddResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCases:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_add(self, client: Client) -> None:
        case = client.datasets.cases.add(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            cases=[{}],
        )
        assert_matches_type(CaseAddResponse, case, path=["response"])

    @parametrize
    def test_method_add_with_all_params(self, client: Client) -> None:
        case = client.datasets.cases.add(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            cases=[
                {
                    "attributes": {"foo": "bar"},
                    "example_key": "x",
                    "input": {
                        "foo": {
                            "extension_type": "wandb-image",
                            "format": "x",
                            "schema_version": 1,
                            "sha256": "210b9798eb53baa4e69d31c1071cf03d212b8ad0ca30cf321e0ea82e120aac26",
                            "size": 0,
                            "uri": "x",
                            "wb_media_type": "image-file",
                            "boxes": {
                                "foo": {
                                    "sha256": "210b9798eb53baa4e69d31c1071cf03d212b8ad0ca30cf321e0ea82e120aac26",
                                    "size": 0,
                                    "uri": "x",
                                    "_type": "boxes2D",
                                }
                            },
                            "caption": "caption",
                            "height": 0,
                            "masks": {
                                "foo": {
                                    "sha256": "210b9798eb53baa4e69d31c1071cf03d212b8ad0ca30cf321e0ea82e120aac26",
                                    "size": 0,
                                    "uri": "x",
                                    "_type": "mask",
                                }
                            },
                            "width": 0,
                        }
                    },
                    "output": {
                        "foo": {
                            "extension_type": "wandb-image",
                            "format": "x",
                            "schema_version": 1,
                            "sha256": "210b9798eb53baa4e69d31c1071cf03d212b8ad0ca30cf321e0ea82e120aac26",
                            "size": 0,
                            "uri": "x",
                            "wb_media_type": "image-file",
                            "boxes": {
                                "foo": {
                                    "sha256": "210b9798eb53baa4e69d31c1071cf03d212b8ad0ca30cf321e0ea82e120aac26",
                                    "size": 0,
                                    "uri": "x",
                                    "_type": "boxes2D",
                                }
                            },
                            "caption": "caption",
                            "height": 0,
                            "masks": {
                                "foo": {
                                    "sha256": "210b9798eb53baa4e69d31c1071cf03d212b8ad0ca30cf321e0ea82e120aac26",
                                    "size": 0,
                                    "uri": "x",
                                    "_type": "mask",
                                }
                            },
                            "width": 0,
                        }
                    },
                    "trajectory_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "variant": "x",
                }
            ],
            example_key_fields=["input"],
        )
        assert_matches_type(CaseAddResponse, case, path=["response"])

    @parametrize
    def test_raw_response_add(self, client: Client) -> None:
        response = client.datasets.cases.with_raw_response.add(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            cases=[{}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        case = response.parse()
        assert_matches_type(CaseAddResponse, case, path=["response"])

    @parametrize
    def test_streaming_response_add(self, client: Client) -> None:
        with client.datasets.cases.with_streaming_response.add(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            cases=[{}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            case = response.parse()
            assert_matches_type(CaseAddResponse, case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_add(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.datasets.cases.with_raw_response.add(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
                cases=[{}],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.datasets.cases.with_raw_response.add(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
                cases=[{}],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            client.datasets.cases.with_raw_response.add(
                dataset_id="",
                namespace="wandb",
                scope_id="scope_id",
                cases=[{}],
            )


class TestAsyncCases:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_add(self, async_client: AsyncClient) -> None:
        case = await async_client.datasets.cases.add(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            cases=[{}],
        )
        assert_matches_type(CaseAddResponse, case, path=["response"])

    @parametrize
    async def test_method_add_with_all_params(self, async_client: AsyncClient) -> None:
        case = await async_client.datasets.cases.add(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            cases=[
                {
                    "attributes": {"foo": "bar"},
                    "example_key": "x",
                    "input": {
                        "foo": {
                            "extension_type": "wandb-image",
                            "format": "x",
                            "schema_version": 1,
                            "sha256": "210b9798eb53baa4e69d31c1071cf03d212b8ad0ca30cf321e0ea82e120aac26",
                            "size": 0,
                            "uri": "x",
                            "wb_media_type": "image-file",
                            "boxes": {
                                "foo": {
                                    "sha256": "210b9798eb53baa4e69d31c1071cf03d212b8ad0ca30cf321e0ea82e120aac26",
                                    "size": 0,
                                    "uri": "x",
                                    "_type": "boxes2D",
                                }
                            },
                            "caption": "caption",
                            "height": 0,
                            "masks": {
                                "foo": {
                                    "sha256": "210b9798eb53baa4e69d31c1071cf03d212b8ad0ca30cf321e0ea82e120aac26",
                                    "size": 0,
                                    "uri": "x",
                                    "_type": "mask",
                                }
                            },
                            "width": 0,
                        }
                    },
                    "output": {
                        "foo": {
                            "extension_type": "wandb-image",
                            "format": "x",
                            "schema_version": 1,
                            "sha256": "210b9798eb53baa4e69d31c1071cf03d212b8ad0ca30cf321e0ea82e120aac26",
                            "size": 0,
                            "uri": "x",
                            "wb_media_type": "image-file",
                            "boxes": {
                                "foo": {
                                    "sha256": "210b9798eb53baa4e69d31c1071cf03d212b8ad0ca30cf321e0ea82e120aac26",
                                    "size": 0,
                                    "uri": "x",
                                    "_type": "boxes2D",
                                }
                            },
                            "caption": "caption",
                            "height": 0,
                            "masks": {
                                "foo": {
                                    "sha256": "210b9798eb53baa4e69d31c1071cf03d212b8ad0ca30cf321e0ea82e120aac26",
                                    "size": 0,
                                    "uri": "x",
                                    "_type": "mask",
                                }
                            },
                            "width": 0,
                        }
                    },
                    "trajectory_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "variant": "x",
                }
            ],
            example_key_fields=["input"],
        )
        assert_matches_type(CaseAddResponse, case, path=["response"])

    @parametrize
    async def test_raw_response_add(self, async_client: AsyncClient) -> None:
        response = await async_client.datasets.cases.with_raw_response.add(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            cases=[{}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        case = await response.parse()
        assert_matches_type(CaseAddResponse, case, path=["response"])

    @parametrize
    async def test_streaming_response_add(self, async_client: AsyncClient) -> None:
        async with async_client.datasets.cases.with_streaming_response.add(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            cases=[{}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            case = await response.parse()
            assert_matches_type(CaseAddResponse, case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_add(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.datasets.cases.with_raw_response.add(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
                cases=[{}],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.datasets.cases.with_raw_response.add(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
                cases=[{}],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            await async_client.datasets.cases.with_raw_response.add(
                dataset_id="",
                namespace="wandb",
                scope_id="scope_id",
                cases=[{}],
            )
