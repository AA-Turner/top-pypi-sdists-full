# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Optional, cast

import pytest

from boltz_api import Boltz, AsyncBoltz
from tests.utils import assert_matches_type
from boltz_api.pagination import SyncCursorPage, AsyncCursorPage
from boltz_api.types.admin import (
    WorkspaceListResponse,
    WorkspaceCreateResponse,
    WorkspaceUpdateResponse,
    WorkspaceArchiveResponse,
    WorkspaceRetrieveResponse,
    WorkspaceSetSpendingLimitResponse,
    WorkspaceRetrieveSpendingLimitResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWorkspaces:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create(self, client: Boltz) -> None:
        workspace = client.admin.workspaces.create()
        assert_matches_type(WorkspaceCreateResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Boltz) -> None:
        workspace = client.admin.workspaces.create(
            data_retention={
                "unit": "hours",
                "value": 1,
            },
            name="x",
            spending_limit={
                "limit": {
                    "amount": 5000,
                    "currency": "MILLI_USD",
                },
                "type": "lifetime",
            },
        )
        assert_matches_type(WorkspaceCreateResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Boltz) -> None:
        response = client.admin.workspaces.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(WorkspaceCreateResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Boltz) -> None:
        with client.admin.workspaces.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(WorkspaceCreateResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Boltz) -> None:
        workspace = client.admin.workspaces.retrieve(
            "workspace_id",
        )
        assert_matches_type(WorkspaceRetrieveResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Boltz) -> None:
        response = client.admin.workspaces.with_raw_response.retrieve(
            "workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(WorkspaceRetrieveResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Boltz) -> None:
        with client.admin.workspaces.with_streaming_response.retrieve(
            "workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(WorkspaceRetrieveResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.admin.workspaces.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update(self, client: Boltz) -> None:
        workspace = client.admin.workspaces.update(
            workspace_id="workspace_id",
        )
        assert_matches_type(WorkspaceUpdateResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_with_all_params(self, client: Boltz) -> None:
        workspace = client.admin.workspaces.update(
            workspace_id="workspace_id",
            data_retention={
                "unit": "hours",
                "value": 1,
            },
            name="x",
        )
        assert_matches_type(WorkspaceUpdateResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_update(self, client: Boltz) -> None:
        response = client.admin.workspaces.with_raw_response.update(
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(WorkspaceUpdateResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_update(self, client: Boltz) -> None:
        with client.admin.workspaces.with_streaming_response.update(
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(WorkspaceUpdateResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_update(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.admin.workspaces.with_raw_response.update(
                workspace_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Boltz) -> None:
        workspace = client.admin.workspaces.list()
        assert_matches_type(SyncCursorPage[WorkspaceListResponse], workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Boltz) -> None:
        workspace = client.admin.workspaces.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
            name="x",
        )
        assert_matches_type(SyncCursorPage[WorkspaceListResponse], workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Boltz) -> None:
        response = client.admin.workspaces.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(SyncCursorPage[WorkspaceListResponse], workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Boltz) -> None:
        with client.admin.workspaces.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(SyncCursorPage[WorkspaceListResponse], workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_archive(self, client: Boltz) -> None:
        workspace = client.admin.workspaces.archive(
            "workspace_id",
        )
        assert_matches_type(WorkspaceArchiveResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_archive(self, client: Boltz) -> None:
        response = client.admin.workspaces.with_raw_response.archive(
            "workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(WorkspaceArchiveResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_archive(self, client: Boltz) -> None:
        with client.admin.workspaces.with_streaming_response.archive(
            "workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(WorkspaceArchiveResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_archive(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.admin.workspaces.with_raw_response.archive(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_spending_limit(self, client: Boltz) -> None:
        workspace = client.admin.workspaces.retrieve_spending_limit(
            "workspace_id",
        )
        assert_matches_type(Optional[WorkspaceRetrieveSpendingLimitResponse], workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve_spending_limit(self, client: Boltz) -> None:
        response = client.admin.workspaces.with_raw_response.retrieve_spending_limit(
            "workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(Optional[WorkspaceRetrieveSpendingLimitResponse], workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve_spending_limit(self, client: Boltz) -> None:
        with client.admin.workspaces.with_streaming_response.retrieve_spending_limit(
            "workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(Optional[WorkspaceRetrieveSpendingLimitResponse], workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve_spending_limit(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.admin.workspaces.with_raw_response.retrieve_spending_limit(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_set_spending_limit(self, client: Boltz) -> None:
        workspace = client.admin.workspaces.set_spending_limit(
            workspace_id="workspace_id",
            limit={
                "amount": 5000,
                "currency": "MILLI_USD",
            },
            type="lifetime",
        )
        assert_matches_type(Optional[WorkspaceSetSpendingLimitResponse], workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_set_spending_limit(self, client: Boltz) -> None:
        response = client.admin.workspaces.with_raw_response.set_spending_limit(
            workspace_id="workspace_id",
            limit={
                "amount": 5000,
                "currency": "MILLI_USD",
            },
            type="lifetime",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(Optional[WorkspaceSetSpendingLimitResponse], workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_set_spending_limit(self, client: Boltz) -> None:
        with client.admin.workspaces.with_streaming_response.set_spending_limit(
            workspace_id="workspace_id",
            limit={
                "amount": 5000,
                "currency": "MILLI_USD",
            },
            type="lifetime",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(Optional[WorkspaceSetSpendingLimitResponse], workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_set_spending_limit(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.admin.workspaces.with_raw_response.set_spending_limit(
                workspace_id="",
                limit={
                    "amount": 5000,
                    "currency": "MILLI_USD",
                },
                type="lifetime",
            )


class TestAsyncWorkspaces:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncBoltz) -> None:
        workspace = await async_client.admin.workspaces.create()
        assert_matches_type(WorkspaceCreateResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncBoltz) -> None:
        workspace = await async_client.admin.workspaces.create(
            data_retention={
                "unit": "hours",
                "value": 1,
            },
            name="x",
            spending_limit={
                "limit": {
                    "amount": 5000,
                    "currency": "MILLI_USD",
                },
                "type": "lifetime",
            },
        )
        assert_matches_type(WorkspaceCreateResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncBoltz) -> None:
        response = await async_client.admin.workspaces.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(WorkspaceCreateResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncBoltz) -> None:
        async with async_client.admin.workspaces.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(WorkspaceCreateResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncBoltz) -> None:
        workspace = await async_client.admin.workspaces.retrieve(
            "workspace_id",
        )
        assert_matches_type(WorkspaceRetrieveResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncBoltz) -> None:
        response = await async_client.admin.workspaces.with_raw_response.retrieve(
            "workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(WorkspaceRetrieveResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncBoltz) -> None:
        async with async_client.admin.workspaces.with_streaming_response.retrieve(
            "workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(WorkspaceRetrieveResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.admin.workspaces.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update(self, async_client: AsyncBoltz) -> None:
        workspace = await async_client.admin.workspaces.update(
            workspace_id="workspace_id",
        )
        assert_matches_type(WorkspaceUpdateResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncBoltz) -> None:
        workspace = await async_client.admin.workspaces.update(
            workspace_id="workspace_id",
            data_retention={
                "unit": "hours",
                "value": 1,
            },
            name="x",
        )
        assert_matches_type(WorkspaceUpdateResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncBoltz) -> None:
        response = await async_client.admin.workspaces.with_raw_response.update(
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(WorkspaceUpdateResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncBoltz) -> None:
        async with async_client.admin.workspaces.with_streaming_response.update(
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(WorkspaceUpdateResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_update(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.admin.workspaces.with_raw_response.update(
                workspace_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncBoltz) -> None:
        workspace = await async_client.admin.workspaces.list()
        assert_matches_type(AsyncCursorPage[WorkspaceListResponse], workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncBoltz) -> None:
        workspace = await async_client.admin.workspaces.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
            name="x",
        )
        assert_matches_type(AsyncCursorPage[WorkspaceListResponse], workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncBoltz) -> None:
        response = await async_client.admin.workspaces.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(AsyncCursorPage[WorkspaceListResponse], workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncBoltz) -> None:
        async with async_client.admin.workspaces.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(AsyncCursorPage[WorkspaceListResponse], workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_archive(self, async_client: AsyncBoltz) -> None:
        workspace = await async_client.admin.workspaces.archive(
            "workspace_id",
        )
        assert_matches_type(WorkspaceArchiveResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncBoltz) -> None:
        response = await async_client.admin.workspaces.with_raw_response.archive(
            "workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(WorkspaceArchiveResponse, workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncBoltz) -> None:
        async with async_client.admin.workspaces.with_streaming_response.archive(
            "workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(WorkspaceArchiveResponse, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_archive(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.admin.workspaces.with_raw_response.archive(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_spending_limit(self, async_client: AsyncBoltz) -> None:
        workspace = await async_client.admin.workspaces.retrieve_spending_limit(
            "workspace_id",
        )
        assert_matches_type(Optional[WorkspaceRetrieveSpendingLimitResponse], workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve_spending_limit(self, async_client: AsyncBoltz) -> None:
        response = await async_client.admin.workspaces.with_raw_response.retrieve_spending_limit(
            "workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(Optional[WorkspaceRetrieveSpendingLimitResponse], workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve_spending_limit(self, async_client: AsyncBoltz) -> None:
        async with async_client.admin.workspaces.with_streaming_response.retrieve_spending_limit(
            "workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(Optional[WorkspaceRetrieveSpendingLimitResponse], workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve_spending_limit(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.admin.workspaces.with_raw_response.retrieve_spending_limit(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_set_spending_limit(self, async_client: AsyncBoltz) -> None:
        workspace = await async_client.admin.workspaces.set_spending_limit(
            workspace_id="workspace_id",
            limit={
                "amount": 5000,
                "currency": "MILLI_USD",
            },
            type="lifetime",
        )
        assert_matches_type(Optional[WorkspaceSetSpendingLimitResponse], workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_set_spending_limit(self, async_client: AsyncBoltz) -> None:
        response = await async_client.admin.workspaces.with_raw_response.set_spending_limit(
            workspace_id="workspace_id",
            limit={
                "amount": 5000,
                "currency": "MILLI_USD",
            },
            type="lifetime",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(Optional[WorkspaceSetSpendingLimitResponse], workspace, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_set_spending_limit(self, async_client: AsyncBoltz) -> None:
        async with async_client.admin.workspaces.with_streaming_response.set_spending_limit(
            workspace_id="workspace_id",
            limit={
                "amount": 5000,
                "currency": "MILLI_USD",
            },
            type="lifetime",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(Optional[WorkspaceSetSpendingLimitResponse], workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_set_spending_limit(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.admin.workspaces.with_raw_response.set_spending_limit(
                workspace_id="",
                limit={
                    "amount": 5000,
                    "currency": "MILLI_USD",
                },
                type="lifetime",
            )
