# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from boltz_api import Boltz, AsyncBoltz
from tests.utils import assert_matches_type
from boltz_api.pagination import SyncCursorPage, AsyncCursorPage
from boltz_api.types.predictions import (
    AdmeListResponse,
    AdmeStartResponse,
    AdmeRetrieveResponse,
    AdmeDeleteDataResponse,
    AdmeEstimateCostResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAdme:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Boltz) -> None:
        adme = client.predictions.adme.retrieve(
            id="id",
        )
        assert_matches_type(AdmeRetrieveResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Boltz) -> None:
        adme = client.predictions.adme.retrieve(
            id="id",
            workspace_id="workspace_id",
        )
        assert_matches_type(AdmeRetrieveResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Boltz) -> None:
        response = client.predictions.adme.with_raw_response.retrieve(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        adme = response.parse()
        assert_matches_type(AdmeRetrieveResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Boltz) -> None:
        with client.predictions.adme.with_streaming_response.retrieve(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            adme = response.parse()
            assert_matches_type(AdmeRetrieveResponse, adme, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.predictions.adme.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Boltz) -> None:
        adme = client.predictions.adme.list()
        assert_matches_type(SyncCursorPage[AdmeListResponse], adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Boltz) -> None:
        adme = client.predictions.adme.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
            workspace_id="workspace_id",
        )
        assert_matches_type(SyncCursorPage[AdmeListResponse], adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Boltz) -> None:
        response = client.predictions.adme.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        adme = response.parse()
        assert_matches_type(SyncCursorPage[AdmeListResponse], adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Boltz) -> None:
        with client.predictions.adme.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            adme = response.parse()
            assert_matches_type(SyncCursorPage[AdmeListResponse], adme, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete_data(self, client: Boltz) -> None:
        adme = client.predictions.adme.delete_data(
            "id",
        )
        assert_matches_type(AdmeDeleteDataResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete_data(self, client: Boltz) -> None:
        response = client.predictions.adme.with_raw_response.delete_data(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        adme = response.parse()
        assert_matches_type(AdmeDeleteDataResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete_data(self, client: Boltz) -> None:
        with client.predictions.adme.with_streaming_response.delete_data(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            adme = response.parse()
            assert_matches_type(AdmeDeleteDataResponse, adme, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete_data(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.predictions.adme.with_raw_response.delete_data(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_estimate_cost(self, client: Boltz) -> None:
        adme = client.predictions.adme.estimate_cost(
            input={"molecules": [{"smiles": "x"}]},
            model="adme-v1",
        )
        assert_matches_type(AdmeEstimateCostResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_estimate_cost_with_all_params(self, client: Boltz) -> None:
        adme = client.predictions.adme.estimate_cost(
            input={
                "molecules": [
                    {
                        "smiles": "x",
                        "id": "x",
                    }
                ]
            },
            model="adme-v1",
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(AdmeEstimateCostResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_estimate_cost(self, client: Boltz) -> None:
        response = client.predictions.adme.with_raw_response.estimate_cost(
            input={"molecules": [{"smiles": "x"}]},
            model="adme-v1",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        adme = response.parse()
        assert_matches_type(AdmeEstimateCostResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_estimate_cost(self, client: Boltz) -> None:
        with client.predictions.adme.with_streaming_response.estimate_cost(
            input={"molecules": [{"smiles": "x"}]},
            model="adme-v1",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            adme = response.parse()
            assert_matches_type(AdmeEstimateCostResponse, adme, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start(self, client: Boltz) -> None:
        adme = client.predictions.adme.start(
            input={"molecules": [{"smiles": "x"}]},
            model="adme-v1",
        )
        assert_matches_type(AdmeStartResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start_with_all_params(self, client: Boltz) -> None:
        adme = client.predictions.adme.start(
            input={
                "molecules": [
                    {
                        "smiles": "x",
                        "id": "x",
                    }
                ]
            },
            model="adme-v1",
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(AdmeStartResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_start(self, client: Boltz) -> None:
        response = client.predictions.adme.with_raw_response.start(
            input={"molecules": [{"smiles": "x"}]},
            model="adme-v1",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        adme = response.parse()
        assert_matches_type(AdmeStartResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_start(self, client: Boltz) -> None:
        with client.predictions.adme.with_streaming_response.start(
            input={"molecules": [{"smiles": "x"}]},
            model="adme-v1",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            adme = response.parse()
            assert_matches_type(AdmeStartResponse, adme, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAdme:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncBoltz) -> None:
        adme = await async_client.predictions.adme.retrieve(
            id="id",
        )
        assert_matches_type(AdmeRetrieveResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncBoltz) -> None:
        adme = await async_client.predictions.adme.retrieve(
            id="id",
            workspace_id="workspace_id",
        )
        assert_matches_type(AdmeRetrieveResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncBoltz) -> None:
        response = await async_client.predictions.adme.with_raw_response.retrieve(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        adme = await response.parse()
        assert_matches_type(AdmeRetrieveResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncBoltz) -> None:
        async with async_client.predictions.adme.with_streaming_response.retrieve(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            adme = await response.parse()
            assert_matches_type(AdmeRetrieveResponse, adme, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.predictions.adme.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncBoltz) -> None:
        adme = await async_client.predictions.adme.list()
        assert_matches_type(AsyncCursorPage[AdmeListResponse], adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncBoltz) -> None:
        adme = await async_client.predictions.adme.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
            workspace_id="workspace_id",
        )
        assert_matches_type(AsyncCursorPage[AdmeListResponse], adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncBoltz) -> None:
        response = await async_client.predictions.adme.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        adme = await response.parse()
        assert_matches_type(AsyncCursorPage[AdmeListResponse], adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncBoltz) -> None:
        async with async_client.predictions.adme.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            adme = await response.parse()
            assert_matches_type(AsyncCursorPage[AdmeListResponse], adme, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete_data(self, async_client: AsyncBoltz) -> None:
        adme = await async_client.predictions.adme.delete_data(
            "id",
        )
        assert_matches_type(AdmeDeleteDataResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete_data(self, async_client: AsyncBoltz) -> None:
        response = await async_client.predictions.adme.with_raw_response.delete_data(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        adme = await response.parse()
        assert_matches_type(AdmeDeleteDataResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete_data(self, async_client: AsyncBoltz) -> None:
        async with async_client.predictions.adme.with_streaming_response.delete_data(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            adme = await response.parse()
            assert_matches_type(AdmeDeleteDataResponse, adme, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete_data(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.predictions.adme.with_raw_response.delete_data(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_estimate_cost(self, async_client: AsyncBoltz) -> None:
        adme = await async_client.predictions.adme.estimate_cost(
            input={"molecules": [{"smiles": "x"}]},
            model="adme-v1",
        )
        assert_matches_type(AdmeEstimateCostResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_estimate_cost_with_all_params(self, async_client: AsyncBoltz) -> None:
        adme = await async_client.predictions.adme.estimate_cost(
            input={
                "molecules": [
                    {
                        "smiles": "x",
                        "id": "x",
                    }
                ]
            },
            model="adme-v1",
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(AdmeEstimateCostResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_estimate_cost(self, async_client: AsyncBoltz) -> None:
        response = await async_client.predictions.adme.with_raw_response.estimate_cost(
            input={"molecules": [{"smiles": "x"}]},
            model="adme-v1",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        adme = await response.parse()
        assert_matches_type(AdmeEstimateCostResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_estimate_cost(self, async_client: AsyncBoltz) -> None:
        async with async_client.predictions.adme.with_streaming_response.estimate_cost(
            input={"molecules": [{"smiles": "x"}]},
            model="adme-v1",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            adme = await response.parse()
            assert_matches_type(AdmeEstimateCostResponse, adme, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start(self, async_client: AsyncBoltz) -> None:
        adme = await async_client.predictions.adme.start(
            input={"molecules": [{"smiles": "x"}]},
            model="adme-v1",
        )
        assert_matches_type(AdmeStartResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start_with_all_params(self, async_client: AsyncBoltz) -> None:
        adme = await async_client.predictions.adme.start(
            input={
                "molecules": [
                    {
                        "smiles": "x",
                        "id": "x",
                    }
                ]
            },
            model="adme-v1",
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(AdmeStartResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_start(self, async_client: AsyncBoltz) -> None:
        response = await async_client.predictions.adme.with_raw_response.start(
            input={"molecules": [{"smiles": "x"}]},
            model="adme-v1",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        adme = await response.parse()
        assert_matches_type(AdmeStartResponse, adme, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_start(self, async_client: AsyncBoltz) -> None:
        async with async_client.predictions.adme.with_streaming_response.start(
            input={"molecules": [{"smiles": "x"}]},
            model="adme-v1",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            adme = await response.parse()
            assert_matches_type(AdmeStartResponse, adme, path=["response"])

        assert cast(Any, response.is_closed) is True
