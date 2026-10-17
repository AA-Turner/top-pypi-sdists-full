# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from langsmith import Langsmith, AsyncLangsmith
from tests.utils import assert_matches_type
from langsmith.types import SnapshotResponse
from langsmith.pagination import SyncItemsCursorGetPagination, AsyncItemsCursorGetPagination
from langsmith.types.sandboxes import SnapshotRetrieveByNameResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSnapshots:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create(self, client: Langsmith) -> None:
        snapshot = client.sandboxes.snapshots.create(
            docker_image="docker_image",
            fs_capacity_bytes=0,
            name="name",
        )
        assert_matches_type(SnapshotResponse, snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Langsmith) -> None:
        snapshot = client.sandboxes.snapshots.create(
            docker_image="docker_image",
            fs_capacity_bytes=0,
            name="name",
            description="description",
            labels={"foo": "string"},
            registry_id="registry_id",
            run_config={
                "env_vars": {"foo": "string"},
                "user": "user",
                "work_dir": "work_dir",
            },
            tag="tag",
        )
        assert_matches_type(SnapshotResponse, snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Langsmith) -> None:

        response = client.sandboxes.snapshots.with_raw_response.create(
            docker_image="docker_image",
            fs_capacity_bytes=0,
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snapshot = response.parse()
        assert_matches_type(SnapshotResponse, snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Langsmith) -> None:
        with client.sandboxes.snapshots.with_streaming_response.create(
            docker_image="docker_image",
            fs_capacity_bytes=0,
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snapshot = response.parse()
            assert_matches_type(SnapshotResponse, snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Langsmith) -> None:
        snapshot = client.sandboxes.snapshots.retrieve(
            "snapshot_id",
        )
        assert_matches_type(SnapshotResponse, snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Langsmith) -> None:

        response = client.sandboxes.snapshots.with_raw_response.retrieve(
            "snapshot_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snapshot = response.parse()
        assert_matches_type(SnapshotResponse, snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Langsmith) -> None:
        with client.sandboxes.snapshots.with_streaming_response.retrieve(
            "snapshot_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snapshot = response.parse()
            assert_matches_type(SnapshotResponse, snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Langsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `snapshot_id` but received ''"):
            client.sandboxes.snapshots.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Langsmith) -> None:
        snapshot = client.sandboxes.snapshots.list()
        assert_matches_type(SyncItemsCursorGetPagination[SnapshotResponse], snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Langsmith) -> None:
        snapshot = client.sandboxes.snapshots.list(
            created_by="created_by",
            cursor="cursor",
            label=["string"],
            limit=0,
            name_contains="name_contains",
            offset=0,
            page_size=0,
            sort_by="sort_by",
            sort_direction="sort_direction",
            sort_order="sort_order",
            status="status",
        )
        assert_matches_type(SyncItemsCursorGetPagination[SnapshotResponse], snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Langsmith) -> None:

        response = client.sandboxes.snapshots.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snapshot = response.parse()
        assert_matches_type(SyncItemsCursorGetPagination[SnapshotResponse], snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Langsmith) -> None:
        with client.sandboxes.snapshots.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snapshot = response.parse()
            assert_matches_type(SyncItemsCursorGetPagination[SnapshotResponse], snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete(self, client: Langsmith) -> None:
        snapshot = client.sandboxes.snapshots.delete(
            "snapshot_id",
        )
        assert snapshot is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Langsmith) -> None:

        response = client.sandboxes.snapshots.with_raw_response.delete(
            "snapshot_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snapshot = response.parse()
        assert snapshot is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Langsmith) -> None:
        with client.sandboxes.snapshots.with_streaming_response.delete(
            "snapshot_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snapshot = response.parse()
            assert snapshot is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Langsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `snapshot_id` but received ''"):
            client.sandboxes.snapshots.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_by_name(self, client: Langsmith) -> None:
        snapshot = client.sandboxes.snapshots.retrieve_by_name(
            "name",
        )
        assert_matches_type(SnapshotRetrieveByNameResponse, snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve_by_name(self, client: Langsmith) -> None:

        response = client.sandboxes.snapshots.with_raw_response.retrieve_by_name(
            "name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snapshot = response.parse()
        assert_matches_type(SnapshotRetrieveByNameResponse, snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve_by_name(self, client: Langsmith) -> None:
        with client.sandboxes.snapshots.with_streaming_response.retrieve_by_name(
            "name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snapshot = response.parse()
            assert_matches_type(SnapshotRetrieveByNameResponse, snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve_by_name(self, client: Langsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            client.sandboxes.snapshots.with_raw_response.retrieve_by_name(
                "",
            )


class TestAsyncSnapshots:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncLangsmith) -> None:
        snapshot = await async_client.sandboxes.snapshots.create(
            docker_image="docker_image",
            fs_capacity_bytes=0,
            name="name",
        )
        assert_matches_type(SnapshotResponse, snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncLangsmith) -> None:
        snapshot = await async_client.sandboxes.snapshots.create(
            docker_image="docker_image",
            fs_capacity_bytes=0,
            name="name",
            description="description",
            labels={"foo": "string"},
            registry_id="registry_id",
            run_config={
                "env_vars": {"foo": "string"},
                "user": "user",
                "work_dir": "work_dir",
            },
            tag="tag",
        )
        assert_matches_type(SnapshotResponse, snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.sandboxes.snapshots.with_raw_response.create(
            docker_image="docker_image",
            fs_capacity_bytes=0,
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snapshot = await response.parse()
        assert_matches_type(SnapshotResponse, snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncLangsmith) -> None:
        async with async_client.sandboxes.snapshots.with_streaming_response.create(
            docker_image="docker_image",
            fs_capacity_bytes=0,
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snapshot = await response.parse()
            assert_matches_type(SnapshotResponse, snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncLangsmith) -> None:
        snapshot = await async_client.sandboxes.snapshots.retrieve(
            "snapshot_id",
        )
        assert_matches_type(SnapshotResponse, snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.sandboxes.snapshots.with_raw_response.retrieve(
            "snapshot_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snapshot = await response.parse()
        assert_matches_type(SnapshotResponse, snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncLangsmith) -> None:
        async with async_client.sandboxes.snapshots.with_streaming_response.retrieve(
            "snapshot_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snapshot = await response.parse()
            assert_matches_type(SnapshotResponse, snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncLangsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `snapshot_id` but received ''"):
            await async_client.sandboxes.snapshots.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncLangsmith) -> None:
        snapshot = await async_client.sandboxes.snapshots.list()
        assert_matches_type(AsyncItemsCursorGetPagination[SnapshotResponse], snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncLangsmith) -> None:
        snapshot = await async_client.sandboxes.snapshots.list(
            created_by="created_by",
            cursor="cursor",
            label=["string"],
            limit=0,
            name_contains="name_contains",
            offset=0,
            page_size=0,
            sort_by="sort_by",
            sort_direction="sort_direction",
            sort_order="sort_order",
            status="status",
        )
        assert_matches_type(AsyncItemsCursorGetPagination[SnapshotResponse], snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.sandboxes.snapshots.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snapshot = await response.parse()
        assert_matches_type(AsyncItemsCursorGetPagination[SnapshotResponse], snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncLangsmith) -> None:
        async with async_client.sandboxes.snapshots.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snapshot = await response.parse()
            assert_matches_type(AsyncItemsCursorGetPagination[SnapshotResponse], snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncLangsmith) -> None:
        snapshot = await async_client.sandboxes.snapshots.delete(
            "snapshot_id",
        )
        assert snapshot is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.sandboxes.snapshots.with_raw_response.delete(
            "snapshot_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snapshot = await response.parse()
        assert snapshot is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncLangsmith) -> None:
        async with async_client.sandboxes.snapshots.with_streaming_response.delete(
            "snapshot_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snapshot = await response.parse()
            assert snapshot is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncLangsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `snapshot_id` but received ''"):
            await async_client.sandboxes.snapshots.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_by_name(self, async_client: AsyncLangsmith) -> None:
        snapshot = await async_client.sandboxes.snapshots.retrieve_by_name(
            "name",
        )
        assert_matches_type(SnapshotRetrieveByNameResponse, snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve_by_name(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.sandboxes.snapshots.with_raw_response.retrieve_by_name(
            "name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snapshot = await response.parse()
        assert_matches_type(SnapshotRetrieveByNameResponse, snapshot, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve_by_name(self, async_client: AsyncLangsmith) -> None:
        async with async_client.sandboxes.snapshots.with_streaming_response.retrieve_by_name(
            "name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snapshot = await response.parse()
            assert_matches_type(SnapshotRetrieveByNameResponse, snapshot, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve_by_name(self, async_client: AsyncLangsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            await async_client.sandboxes.snapshots.with_raw_response.retrieve_by_name(
                "",
            )
