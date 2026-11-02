# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from coreweave_evaluations import Client, AsyncClient
from coreweave_evaluations.types.datasets import (
    TrajectoryGetResponse,
    TrajectoryListResponse,
    TrajectoryCreateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTrajectories:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Client) -> None:
        trajectory = client.datasets.trajectories.create(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            trajectories=[
                {
                    "name": "x",
                    "root_case_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                }
            ],
        )
        assert_matches_type(TrajectoryCreateResponse, trajectory, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Client) -> None:
        response = client.datasets.trajectories.with_raw_response.create(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            trajectories=[
                {
                    "name": "x",
                    "root_case_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trajectory = response.parse()
        assert_matches_type(TrajectoryCreateResponse, trajectory, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Client) -> None:
        with client.datasets.trajectories.with_streaming_response.create(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            trajectories=[
                {
                    "name": "x",
                    "root_case_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trajectory = response.parse()
            assert_matches_type(TrajectoryCreateResponse, trajectory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.datasets.trajectories.with_raw_response.create(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
                trajectories=[
                    {
                        "name": "x",
                        "root_case_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    }
                ],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.datasets.trajectories.with_raw_response.create(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
                trajectories=[
                    {
                        "name": "x",
                        "root_case_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    }
                ],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            client.datasets.trajectories.with_raw_response.create(
                dataset_id="",
                namespace="wandb",
                scope_id="scope_id",
                trajectories=[
                    {
                        "name": "x",
                        "root_case_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    }
                ],
            )

    @parametrize
    def test_method_list(self, client: Client) -> None:
        trajectory = client.datasets.trajectories.list(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )
        assert_matches_type(TrajectoryListResponse, trajectory, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Client) -> None:
        trajectory = client.datasets.trajectories.list(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            cursor="cursor",
            limit=1,
        )
        assert_matches_type(TrajectoryListResponse, trajectory, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Client) -> None:
        response = client.datasets.trajectories.with_raw_response.list(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trajectory = response.parse()
        assert_matches_type(TrajectoryListResponse, trajectory, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Client) -> None:
        with client.datasets.trajectories.with_streaming_response.list(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trajectory = response.parse()
            assert_matches_type(TrajectoryListResponse, trajectory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.datasets.trajectories.with_raw_response.list(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.datasets.trajectories.with_raw_response.list(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            client.datasets.trajectories.with_raw_response.list(
                dataset_id="",
                namespace="wandb",
                scope_id="scope_id",
            )

    @parametrize
    def test_method_get(self, client: Client) -> None:
        trajectory = client.datasets.trajectories.get(
            trajectory_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )
        assert_matches_type(TrajectoryGetResponse, trajectory, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Client) -> None:
        response = client.datasets.trajectories.with_raw_response.get(
            trajectory_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trajectory = response.parse()
        assert_matches_type(TrajectoryGetResponse, trajectory, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Client) -> None:
        with client.datasets.trajectories.with_streaming_response.get(
            trajectory_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trajectory = response.parse()
            assert_matches_type(TrajectoryGetResponse, trajectory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.datasets.trajectories.with_raw_response.get(
                trajectory_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.datasets.trajectories.with_raw_response.get(
                trajectory_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `trajectory_id` but received ''"):
            client.datasets.trajectories.with_raw_response.get(
                trajectory_id="",
                namespace="wandb",
                scope_id="scope_id",
            )


class TestAsyncTrajectories:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncClient) -> None:
        trajectory = await async_client.datasets.trajectories.create(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            trajectories=[
                {
                    "name": "x",
                    "root_case_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                }
            ],
        )
        assert_matches_type(TrajectoryCreateResponse, trajectory, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncClient) -> None:
        response = await async_client.datasets.trajectories.with_raw_response.create(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            trajectories=[
                {
                    "name": "x",
                    "root_case_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trajectory = await response.parse()
        assert_matches_type(TrajectoryCreateResponse, trajectory, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncClient) -> None:
        async with async_client.datasets.trajectories.with_streaming_response.create(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            trajectories=[
                {
                    "name": "x",
                    "root_case_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trajectory = await response.parse()
            assert_matches_type(TrajectoryCreateResponse, trajectory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.datasets.trajectories.with_raw_response.create(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
                trajectories=[
                    {
                        "name": "x",
                        "root_case_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    }
                ],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.datasets.trajectories.with_raw_response.create(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
                trajectories=[
                    {
                        "name": "x",
                        "root_case_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    }
                ],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            await async_client.datasets.trajectories.with_raw_response.create(
                dataset_id="",
                namespace="wandb",
                scope_id="scope_id",
                trajectories=[
                    {
                        "name": "x",
                        "root_case_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    }
                ],
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncClient) -> None:
        trajectory = await async_client.datasets.trajectories.list(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )
        assert_matches_type(TrajectoryListResponse, trajectory, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncClient) -> None:
        trajectory = await async_client.datasets.trajectories.list(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            cursor="cursor",
            limit=1,
        )
        assert_matches_type(TrajectoryListResponse, trajectory, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncClient) -> None:
        response = await async_client.datasets.trajectories.with_raw_response.list(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trajectory = await response.parse()
        assert_matches_type(TrajectoryListResponse, trajectory, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncClient) -> None:
        async with async_client.datasets.trajectories.with_streaming_response.list(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trajectory = await response.parse()
            assert_matches_type(TrajectoryListResponse, trajectory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.datasets.trajectories.with_raw_response.list(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.datasets.trajectories.with_raw_response.list(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            await async_client.datasets.trajectories.with_raw_response.list(
                dataset_id="",
                namespace="wandb",
                scope_id="scope_id",
            )

    @parametrize
    async def test_method_get(self, async_client: AsyncClient) -> None:
        trajectory = await async_client.datasets.trajectories.get(
            trajectory_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )
        assert_matches_type(TrajectoryGetResponse, trajectory, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncClient) -> None:
        response = await async_client.datasets.trajectories.with_raw_response.get(
            trajectory_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trajectory = await response.parse()
        assert_matches_type(TrajectoryGetResponse, trajectory, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncClient) -> None:
        async with async_client.datasets.trajectories.with_streaming_response.get(
            trajectory_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trajectory = await response.parse()
            assert_matches_type(TrajectoryGetResponse, trajectory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.datasets.trajectories.with_raw_response.get(
                trajectory_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.datasets.trajectories.with_raw_response.get(
                trajectory_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `trajectory_id` but received ''"):
            await async_client.datasets.trajectories.with_raw_response.get(
                trajectory_id="",
                namespace="wandb",
                scope_id="scope_id",
            )
