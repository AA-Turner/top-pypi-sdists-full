# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from boltz_api import Boltz, AsyncBoltz
from tests.utils import assert_matches_type
from boltz_api.pagination import SyncCursorPage, AsyncCursorPage
from boltz_api.types.protein import (
    LibraryScreenListResponse,
    LibraryScreenStopResponse,
    LibraryScreenStartResponse,
    LibraryScreenResumeResponse,
    LibraryScreenRetrieveResponse,
    LibraryScreenDeleteDataResponse,
    LibraryScreenListResultsResponse,
    LibraryScreenEstimateCostResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestLibraryScreen:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Boltz) -> None:
        library_screen = client.protein.library_screen.retrieve(
            id="id",
        )
        assert_matches_type(LibraryScreenRetrieveResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Boltz) -> None:
        library_screen = client.protein.library_screen.retrieve(
            id="id",
            workspace_id="workspace_id",
        )
        assert_matches_type(LibraryScreenRetrieveResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Boltz) -> None:
        response = client.protein.library_screen.with_raw_response.retrieve(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = response.parse()
        assert_matches_type(LibraryScreenRetrieveResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Boltz) -> None:
        with client.protein.library_screen.with_streaming_response.retrieve(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            library_screen = response.parse()
            assert_matches_type(LibraryScreenRetrieveResponse, library_screen, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.protein.library_screen.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Boltz) -> None:
        library_screen = client.protein.library_screen.list()
        assert_matches_type(SyncCursorPage[LibraryScreenListResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Boltz) -> None:
        library_screen = client.protein.library_screen.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
            workspace_id="workspace_id",
        )
        assert_matches_type(SyncCursorPage[LibraryScreenListResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Boltz) -> None:
        response = client.protein.library_screen.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = response.parse()
        assert_matches_type(SyncCursorPage[LibraryScreenListResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Boltz) -> None:
        with client.protein.library_screen.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            library_screen = response.parse()
            assert_matches_type(SyncCursorPage[LibraryScreenListResponse], library_screen, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete_data(self, client: Boltz) -> None:
        library_screen = client.protein.library_screen.delete_data(
            "id",
        )
        assert_matches_type(LibraryScreenDeleteDataResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete_data(self, client: Boltz) -> None:
        response = client.protein.library_screen.with_raw_response.delete_data(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = response.parse()
        assert_matches_type(LibraryScreenDeleteDataResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete_data(self, client: Boltz) -> None:
        with client.protein.library_screen.with_streaming_response.delete_data(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            library_screen = response.parse()
            assert_matches_type(LibraryScreenDeleteDataResponse, library_screen, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete_data(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.protein.library_screen.with_raw_response.delete_data(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_estimate_cost(self, client: Boltz) -> None:
        library_screen = client.protein.library_screen.estimate_cost(
            proteins=[
                {
                    "entities": [
                        {
                            "chain_ids": ["string"],
                            "type": "protein",
                            "value": "value",
                        }
                    ]
                }
            ],
            target={
                "chain_selection": {
                    "A": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    }
                },
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
        )
        assert_matches_type(LibraryScreenEstimateCostResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_estimate_cost_with_all_params(self, client: Boltz) -> None:
        library_screen = client.protein.library_screen.estimate_cost(
            proteins=[
                {
                    "entities": [
                        {
                            "chain_ids": ["string"],
                            "type": "protein",
                            "value": "value",
                            "cyclic": True,
                            "modifications": [
                                {
                                    "residue_index": 0,
                                    "type": "ccd",
                                    "value": "value",
                                }
                            ],
                        }
                    ],
                    "id": "id",
                }
            ],
            target={
                "chain_selection": {
                    "A": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                        "epitope_residues": [10, 11, 12],
                        "flexible_residues": [5, 6, 7],
                        "non_binding_residues": [0, 1, 2],
                    }
                },
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(LibraryScreenEstimateCostResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_estimate_cost(self, client: Boltz) -> None:
        response = client.protein.library_screen.with_raw_response.estimate_cost(
            proteins=[
                {
                    "entities": [
                        {
                            "chain_ids": ["string"],
                            "type": "protein",
                            "value": "value",
                        }
                    ]
                }
            ],
            target={
                "chain_selection": {
                    "A": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    }
                },
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = response.parse()
        assert_matches_type(LibraryScreenEstimateCostResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_estimate_cost(self, client: Boltz) -> None:
        with client.protein.library_screen.with_streaming_response.estimate_cost(
            proteins=[
                {
                    "entities": [
                        {
                            "chain_ids": ["string"],
                            "type": "protein",
                            "value": "value",
                        }
                    ]
                }
            ],
            target={
                "chain_selection": {
                    "A": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    }
                },
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            library_screen = response.parse()
            assert_matches_type(LibraryScreenEstimateCostResponse, library_screen, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_results(self, client: Boltz) -> None:
        library_screen = client.protein.library_screen.list_results(
            id="id",
        )
        assert_matches_type(SyncCursorPage[LibraryScreenListResultsResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_results_with_all_params(self, client: Boltz) -> None:
        library_screen = client.protein.library_screen.list_results(
            id="id",
            after_id="after_id",
            before_id="before_id",
            ids="ids",
            limit=1,
            workspace_id="workspace_id",
        )
        assert_matches_type(SyncCursorPage[LibraryScreenListResultsResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list_results(self, client: Boltz) -> None:
        response = client.protein.library_screen.with_raw_response.list_results(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = response.parse()
        assert_matches_type(SyncCursorPage[LibraryScreenListResultsResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list_results(self, client: Boltz) -> None:
        with client.protein.library_screen.with_streaming_response.list_results(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            library_screen = response.parse()
            assert_matches_type(SyncCursorPage[LibraryScreenListResultsResponse], library_screen, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_list_results(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.protein.library_screen.with_raw_response.list_results(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_resume(self, client: Boltz) -> None:
        library_screen = client.protein.library_screen.resume(
            "id",
        )
        assert_matches_type(LibraryScreenResumeResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_resume(self, client: Boltz) -> None:
        response = client.protein.library_screen.with_raw_response.resume(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = response.parse()
        assert_matches_type(LibraryScreenResumeResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_resume(self, client: Boltz) -> None:
        with client.protein.library_screen.with_streaming_response.resume(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            library_screen = response.parse()
            assert_matches_type(LibraryScreenResumeResponse, library_screen, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_resume(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.protein.library_screen.with_raw_response.resume(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start(self, client: Boltz) -> None:
        library_screen = client.protein.library_screen.start(
            proteins=[
                {
                    "entities": [
                        {
                            "chain_ids": ["string"],
                            "type": "protein",
                            "value": "value",
                        }
                    ]
                }
            ],
            target={
                "chain_selection": {
                    "A": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    }
                },
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
        )
        assert_matches_type(LibraryScreenStartResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start_with_all_params(self, client: Boltz) -> None:
        library_screen = client.protein.library_screen.start(
            proteins=[
                {
                    "entities": [
                        {
                            "chain_ids": ["string"],
                            "type": "protein",
                            "value": "value",
                            "cyclic": True,
                            "modifications": [
                                {
                                    "residue_index": 0,
                                    "type": "ccd",
                                    "value": "value",
                                }
                            ],
                        }
                    ],
                    "id": "id",
                }
            ],
            target={
                "chain_selection": {
                    "A": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                        "epitope_residues": [10, 11, 12],
                        "flexible_residues": [5, 6, 7],
                        "non_binding_residues": [0, 1, 2],
                    }
                },
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(LibraryScreenStartResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_start(self, client: Boltz) -> None:
        response = client.protein.library_screen.with_raw_response.start(
            proteins=[
                {
                    "entities": [
                        {
                            "chain_ids": ["string"],
                            "type": "protein",
                            "value": "value",
                        }
                    ]
                }
            ],
            target={
                "chain_selection": {
                    "A": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    }
                },
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = response.parse()
        assert_matches_type(LibraryScreenStartResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_start(self, client: Boltz) -> None:
        with client.protein.library_screen.with_streaming_response.start(
            proteins=[
                {
                    "entities": [
                        {
                            "chain_ids": ["string"],
                            "type": "protein",
                            "value": "value",
                        }
                    ]
                }
            ],
            target={
                "chain_selection": {
                    "A": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    }
                },
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            library_screen = response.parse()
            assert_matches_type(LibraryScreenStartResponse, library_screen, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_stop(self, client: Boltz) -> None:
        library_screen = client.protein.library_screen.stop(
            "id",
        )
        assert_matches_type(LibraryScreenStopResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_stop(self, client: Boltz) -> None:
        response = client.protein.library_screen.with_raw_response.stop(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = response.parse()
        assert_matches_type(LibraryScreenStopResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_stop(self, client: Boltz) -> None:
        with client.protein.library_screen.with_streaming_response.stop(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            library_screen = response.parse()
            assert_matches_type(LibraryScreenStopResponse, library_screen, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_stop(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.protein.library_screen.with_raw_response.stop(
                "",
            )


class TestAsyncLibraryScreen:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.protein.library_screen.retrieve(
            id="id",
        )
        assert_matches_type(LibraryScreenRetrieveResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.protein.library_screen.retrieve(
            id="id",
            workspace_id="workspace_id",
        )
        assert_matches_type(LibraryScreenRetrieveResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.library_screen.with_raw_response.retrieve(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = await response.parse()
        assert_matches_type(LibraryScreenRetrieveResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.library_screen.with_streaming_response.retrieve(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            library_screen = await response.parse()
            assert_matches_type(LibraryScreenRetrieveResponse, library_screen, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.protein.library_screen.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.protein.library_screen.list()
        assert_matches_type(AsyncCursorPage[LibraryScreenListResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.protein.library_screen.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
            workspace_id="workspace_id",
        )
        assert_matches_type(AsyncCursorPage[LibraryScreenListResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.library_screen.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = await response.parse()
        assert_matches_type(AsyncCursorPage[LibraryScreenListResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.library_screen.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            library_screen = await response.parse()
            assert_matches_type(AsyncCursorPage[LibraryScreenListResponse], library_screen, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete_data(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.protein.library_screen.delete_data(
            "id",
        )
        assert_matches_type(LibraryScreenDeleteDataResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete_data(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.library_screen.with_raw_response.delete_data(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = await response.parse()
        assert_matches_type(LibraryScreenDeleteDataResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete_data(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.library_screen.with_streaming_response.delete_data(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            library_screen = await response.parse()
            assert_matches_type(LibraryScreenDeleteDataResponse, library_screen, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete_data(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.protein.library_screen.with_raw_response.delete_data(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_estimate_cost(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.protein.library_screen.estimate_cost(
            proteins=[
                {
                    "entities": [
                        {
                            "chain_ids": ["string"],
                            "type": "protein",
                            "value": "value",
                        }
                    ]
                }
            ],
            target={
                "chain_selection": {
                    "A": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    }
                },
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
        )
        assert_matches_type(LibraryScreenEstimateCostResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_estimate_cost_with_all_params(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.protein.library_screen.estimate_cost(
            proteins=[
                {
                    "entities": [
                        {
                            "chain_ids": ["string"],
                            "type": "protein",
                            "value": "value",
                            "cyclic": True,
                            "modifications": [
                                {
                                    "residue_index": 0,
                                    "type": "ccd",
                                    "value": "value",
                                }
                            ],
                        }
                    ],
                    "id": "id",
                }
            ],
            target={
                "chain_selection": {
                    "A": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                        "epitope_residues": [10, 11, 12],
                        "flexible_residues": [5, 6, 7],
                        "non_binding_residues": [0, 1, 2],
                    }
                },
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(LibraryScreenEstimateCostResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_estimate_cost(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.library_screen.with_raw_response.estimate_cost(
            proteins=[
                {
                    "entities": [
                        {
                            "chain_ids": ["string"],
                            "type": "protein",
                            "value": "value",
                        }
                    ]
                }
            ],
            target={
                "chain_selection": {
                    "A": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    }
                },
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = await response.parse()
        assert_matches_type(LibraryScreenEstimateCostResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_estimate_cost(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.library_screen.with_streaming_response.estimate_cost(
            proteins=[
                {
                    "entities": [
                        {
                            "chain_ids": ["string"],
                            "type": "protein",
                            "value": "value",
                        }
                    ]
                }
            ],
            target={
                "chain_selection": {
                    "A": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    }
                },
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            library_screen = await response.parse()
            assert_matches_type(LibraryScreenEstimateCostResponse, library_screen, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_results(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.protein.library_screen.list_results(
            id="id",
        )
        assert_matches_type(AsyncCursorPage[LibraryScreenListResultsResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_results_with_all_params(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.protein.library_screen.list_results(
            id="id",
            after_id="after_id",
            before_id="before_id",
            ids="ids",
            limit=1,
            workspace_id="workspace_id",
        )
        assert_matches_type(AsyncCursorPage[LibraryScreenListResultsResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list_results(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.library_screen.with_raw_response.list_results(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = await response.parse()
        assert_matches_type(AsyncCursorPage[LibraryScreenListResultsResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list_results(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.library_screen.with_streaming_response.list_results(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            library_screen = await response.parse()
            assert_matches_type(AsyncCursorPage[LibraryScreenListResultsResponse], library_screen, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_list_results(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.protein.library_screen.with_raw_response.list_results(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_resume(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.protein.library_screen.resume(
            "id",
        )
        assert_matches_type(LibraryScreenResumeResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_resume(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.library_screen.with_raw_response.resume(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = await response.parse()
        assert_matches_type(LibraryScreenResumeResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_resume(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.library_screen.with_streaming_response.resume(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            library_screen = await response.parse()
            assert_matches_type(LibraryScreenResumeResponse, library_screen, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_resume(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.protein.library_screen.with_raw_response.resume(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.protein.library_screen.start(
            proteins=[
                {
                    "entities": [
                        {
                            "chain_ids": ["string"],
                            "type": "protein",
                            "value": "value",
                        }
                    ]
                }
            ],
            target={
                "chain_selection": {
                    "A": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    }
                },
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
        )
        assert_matches_type(LibraryScreenStartResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start_with_all_params(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.protein.library_screen.start(
            proteins=[
                {
                    "entities": [
                        {
                            "chain_ids": ["string"],
                            "type": "protein",
                            "value": "value",
                            "cyclic": True,
                            "modifications": [
                                {
                                    "residue_index": 0,
                                    "type": "ccd",
                                    "value": "value",
                                }
                            ],
                        }
                    ],
                    "id": "id",
                }
            ],
            target={
                "chain_selection": {
                    "A": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                        "epitope_residues": [10, 11, 12],
                        "flexible_residues": [5, 6, 7],
                        "non_binding_residues": [0, 1, 2],
                    }
                },
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(LibraryScreenStartResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_start(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.library_screen.with_raw_response.start(
            proteins=[
                {
                    "entities": [
                        {
                            "chain_ids": ["string"],
                            "type": "protein",
                            "value": "value",
                        }
                    ]
                }
            ],
            target={
                "chain_selection": {
                    "A": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    }
                },
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = await response.parse()
        assert_matches_type(LibraryScreenStartResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_start(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.library_screen.with_streaming_response.start(
            proteins=[
                {
                    "entities": [
                        {
                            "chain_ids": ["string"],
                            "type": "protein",
                            "value": "value",
                        }
                    ]
                }
            ],
            target={
                "chain_selection": {
                    "A": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    }
                },
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            library_screen = await response.parse()
            assert_matches_type(LibraryScreenStartResponse, library_screen, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_stop(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.protein.library_screen.stop(
            "id",
        )
        assert_matches_type(LibraryScreenStopResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_stop(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.library_screen.with_raw_response.stop(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = await response.parse()
        assert_matches_type(LibraryScreenStopResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_stop(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.library_screen.with_streaming_response.stop(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            library_screen = await response.parse()
            assert_matches_type(LibraryScreenStopResponse, library_screen, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_stop(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.protein.library_screen.with_raw_response.stop(
                "",
            )
