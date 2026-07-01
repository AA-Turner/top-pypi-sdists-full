# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Optional, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import Task

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTasks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        task = client.evaluations.tasks.update(
            task_id="task_id",
            evaluation_id="evaluation_id",
        )
        assert_matches_type(Optional[Task], task, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        task = client.evaluations.tasks.update(
            task_id="task_id",
            evaluation_id="evaluation_id",
            assigned_to="assigned_to",
        )
        assert_matches_type(Optional[Task], task, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.evaluations.tasks.with_raw_response.update(
            task_id="task_id",
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(Optional[Task], task, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.evaluations.tasks.with_streaming_response.update(
            task_id="task_id",
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(Optional[Task], task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.tasks.with_raw_response.update(
                task_id="task_id",
                evaluation_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.evaluations.tasks.with_raw_response.update(
                task_id="",
                evaluation_id="evaluation_id",
            )


class TestAsyncTasks:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        task = await async_client.evaluations.tasks.update(
            task_id="task_id",
            evaluation_id="evaluation_id",
        )
        assert_matches_type(Optional[Task], task, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        task = await async_client.evaluations.tasks.update(
            task_id="task_id",
            evaluation_id="evaluation_id",
            assigned_to="assigned_to",
        )
        assert_matches_type(Optional[Task], task, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.tasks.with_raw_response.update(
            task_id="task_id",
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(Optional[Task], task, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.tasks.with_streaming_response.update(
            task_id="task_id",
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(Optional[Task], task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.tasks.with_raw_response.update(
                task_id="task_id",
                evaluation_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            await async_client.evaluations.tasks.with_raw_response.update(
                task_id="",
                evaluation_id="evaluation_id",
            )
