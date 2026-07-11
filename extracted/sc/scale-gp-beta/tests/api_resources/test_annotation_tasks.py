# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import AnnotationTaskBatchUpdateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAnnotationTasks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_batch_update(self, client: SGPClient) -> None:
        annotation_task = client.annotation_tasks.batch_update()
        assert_matches_type(AnnotationTaskBatchUpdateResponse, annotation_task, path=["response"])

    @parametrize
    def test_method_batch_update_with_all_params(self, client: SGPClient) -> None:
        annotation_task = client.annotation_tasks.batch_update(
            assigned_to="assigned_to",
            audit_assignment={
                "evaluation_id": "evaluation_id",
                "evaluation_item_ids": ["string"],
                "queue_id": "queue_id",
                "level_1_assigned_to": "level_1_assigned_to",
                "level_2_assigned_to": "level_2_assigned_to",
            },
            ids=["string"],
            status="PENDING_REDO",
        )
        assert_matches_type(AnnotationTaskBatchUpdateResponse, annotation_task, path=["response"])

    @parametrize
    def test_raw_response_batch_update(self, client: SGPClient) -> None:
        response = client.annotation_tasks.with_raw_response.batch_update()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        annotation_task = response.parse()
        assert_matches_type(AnnotationTaskBatchUpdateResponse, annotation_task, path=["response"])

    @parametrize
    def test_streaming_response_batch_update(self, client: SGPClient) -> None:
        with client.annotation_tasks.with_streaming_response.batch_update() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            annotation_task = response.parse()
            assert_matches_type(AnnotationTaskBatchUpdateResponse, annotation_task, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAnnotationTasks:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_batch_update(self, async_client: AsyncSGPClient) -> None:
        annotation_task = await async_client.annotation_tasks.batch_update()
        assert_matches_type(AnnotationTaskBatchUpdateResponse, annotation_task, path=["response"])

    @parametrize
    async def test_method_batch_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        annotation_task = await async_client.annotation_tasks.batch_update(
            assigned_to="assigned_to",
            audit_assignment={
                "evaluation_id": "evaluation_id",
                "evaluation_item_ids": ["string"],
                "queue_id": "queue_id",
                "level_1_assigned_to": "level_1_assigned_to",
                "level_2_assigned_to": "level_2_assigned_to",
            },
            ids=["string"],
            status="PENDING_REDO",
        )
        assert_matches_type(AnnotationTaskBatchUpdateResponse, annotation_task, path=["response"])

    @parametrize
    async def test_raw_response_batch_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.annotation_tasks.with_raw_response.batch_update()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        annotation_task = await response.parse()
        assert_matches_type(AnnotationTaskBatchUpdateResponse, annotation_task, path=["response"])

    @parametrize
    async def test_streaming_response_batch_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.annotation_tasks.with_streaming_response.batch_update() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            annotation_task = await response.parse()
            assert_matches_type(AnnotationTaskBatchUpdateResponse, annotation_task, path=["response"])

        assert cast(Any, response.is_closed) is True
