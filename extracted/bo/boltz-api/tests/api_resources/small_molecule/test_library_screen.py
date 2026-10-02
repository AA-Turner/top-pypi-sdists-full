# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from boltz_api import Boltz, AsyncBoltz
from tests.utils import assert_matches_type
from boltz_api.pagination import SyncCursorPage, AsyncCursorPage
from boltz_api.types.small_molecule import (
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
        library_screen = client.small_molecule.library_screen.retrieve(
            id="id",
        )
        assert_matches_type(LibraryScreenRetrieveResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Boltz) -> None:
        library_screen = client.small_molecule.library_screen.retrieve(
            id="id",
            workspace_id="workspace_id",
        )
        assert_matches_type(LibraryScreenRetrieveResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Boltz) -> None:
        response = client.small_molecule.library_screen.with_raw_response.retrieve(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = response.parse()
        assert_matches_type(LibraryScreenRetrieveResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Boltz) -> None:
        with client.small_molecule.library_screen.with_streaming_response.retrieve(
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
            client.small_molecule.library_screen.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Boltz) -> None:
        library_screen = client.small_molecule.library_screen.list()
        assert_matches_type(SyncCursorPage[LibraryScreenListResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Boltz) -> None:
        library_screen = client.small_molecule.library_screen.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
            workspace_id="workspace_id",
        )
        assert_matches_type(SyncCursorPage[LibraryScreenListResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Boltz) -> None:
        response = client.small_molecule.library_screen.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = response.parse()
        assert_matches_type(SyncCursorPage[LibraryScreenListResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Boltz) -> None:
        with client.small_molecule.library_screen.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            library_screen = response.parse()
            assert_matches_type(SyncCursorPage[LibraryScreenListResponse], library_screen, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete_data(self, client: Boltz) -> None:
        library_screen = client.small_molecule.library_screen.delete_data(
            "id",
        )
        assert_matches_type(LibraryScreenDeleteDataResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete_data(self, client: Boltz) -> None:
        response = client.small_molecule.library_screen.with_raw_response.delete_data(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = response.parse()
        assert_matches_type(LibraryScreenDeleteDataResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete_data(self, client: Boltz) -> None:
        with client.small_molecule.library_screen.with_streaming_response.delete_data(
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
            client.small_molecule.library_screen.with_raw_response.delete_data(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_estimate_cost(self, client: Boltz) -> None:
        library_screen = client.small_molecule.library_screen.estimate_cost(
            molecules=[{"smiles": "smiles"}],
            target={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
        )
        assert_matches_type(LibraryScreenEstimateCostResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_estimate_cost_with_all_params(self, client: Boltz) -> None:
        library_screen = client.small_molecule.library_screen.estimate_cost(
            molecules=[
                {
                    "smiles": "smiles",
                    "id": "id",
                }
            ],
            target={
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
                "bonds": [
                    {
                        "atom1": {
                            "atom_name": "atom_name",
                            "chain_id": "chain_id",
                            "residue_index": 0,
                            "type": "polymer_atom",
                        },
                        "atom2": {
                            "atom_name": "atom_name",
                            "chain_id": "chain_id",
                            "residue_index": 0,
                            "type": "polymer_atom",
                        },
                    }
                ],
                "constraints": [
                    {
                        "binder_chain_id": "binder_chain_id",
                        "contact_residues": {"A": [42, 43, 44, 67, 68, 69]},
                        "max_distance_angstrom": 0,
                        "type": "pocket",
                        "force": True,
                    }
                ],
                "pocket_residues": {"A": [42, 43, 44, 67, 68, 69]},
                "reference_ligands": ["string"],
                "type": "no_template",
            },
            idempotency_key="idempotency_key",
            molecule_filters={
                "boltz_smarts_catalog_filter_level": "recommended",
                "custom_filters": [
                    {
                        "max_hba": 0,
                        "max_hbd": 0,
                        "max_logp": 0,
                        "max_mw": 0,
                        "type": "lipinski_filter",
                        "allow_single_violation": True,
                    }
                ],
            },
            workspace_id="workspace_id",
        )
        assert_matches_type(LibraryScreenEstimateCostResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_estimate_cost(self, client: Boltz) -> None:
        response = client.small_molecule.library_screen.with_raw_response.estimate_cost(
            molecules=[{"smiles": "smiles"}],
            target={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = response.parse()
        assert_matches_type(LibraryScreenEstimateCostResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_estimate_cost(self, client: Boltz) -> None:
        with client.small_molecule.library_screen.with_streaming_response.estimate_cost(
            molecules=[{"smiles": "smiles"}],
            target={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
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
        library_screen = client.small_molecule.library_screen.list_results(
            id="id",
        )
        assert_matches_type(SyncCursorPage[LibraryScreenListResultsResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_results_with_all_params(self, client: Boltz) -> None:
        library_screen = client.small_molecule.library_screen.list_results(
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
        response = client.small_molecule.library_screen.with_raw_response.list_results(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = response.parse()
        assert_matches_type(SyncCursorPage[LibraryScreenListResultsResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list_results(self, client: Boltz) -> None:
        with client.small_molecule.library_screen.with_streaming_response.list_results(
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
            client.small_molecule.library_screen.with_raw_response.list_results(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_resume(self, client: Boltz) -> None:
        library_screen = client.small_molecule.library_screen.resume(
            "id",
        )
        assert_matches_type(LibraryScreenResumeResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_resume(self, client: Boltz) -> None:
        response = client.small_molecule.library_screen.with_raw_response.resume(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = response.parse()
        assert_matches_type(LibraryScreenResumeResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_resume(self, client: Boltz) -> None:
        with client.small_molecule.library_screen.with_streaming_response.resume(
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
            client.small_molecule.library_screen.with_raw_response.resume(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start(self, client: Boltz) -> None:
        library_screen = client.small_molecule.library_screen.start(
            molecules=[{"smiles": "smiles"}],
            target={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
        )
        assert_matches_type(LibraryScreenStartResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start_with_all_params(self, client: Boltz) -> None:
        library_screen = client.small_molecule.library_screen.start(
            molecules=[
                {
                    "smiles": "smiles",
                    "id": "id",
                }
            ],
            target={
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
                "bonds": [
                    {
                        "atom1": {
                            "atom_name": "atom_name",
                            "chain_id": "chain_id",
                            "residue_index": 0,
                            "type": "polymer_atom",
                        },
                        "atom2": {
                            "atom_name": "atom_name",
                            "chain_id": "chain_id",
                            "residue_index": 0,
                            "type": "polymer_atom",
                        },
                    }
                ],
                "constraints": [
                    {
                        "binder_chain_id": "binder_chain_id",
                        "contact_residues": {"A": [42, 43, 44, 67, 68, 69]},
                        "max_distance_angstrom": 0,
                        "type": "pocket",
                        "force": True,
                    }
                ],
                "pocket_residues": {"A": [42, 43, 44, 67, 68, 69]},
                "reference_ligands": ["string"],
                "type": "no_template",
            },
            idempotency_key="idempotency_key",
            molecule_filters={
                "boltz_smarts_catalog_filter_level": "recommended",
                "custom_filters": [
                    {
                        "max_hba": 0,
                        "max_hbd": 0,
                        "max_logp": 0,
                        "max_mw": 0,
                        "type": "lipinski_filter",
                        "allow_single_violation": True,
                    }
                ],
            },
            workspace_id="workspace_id",
        )
        assert_matches_type(LibraryScreenStartResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_start(self, client: Boltz) -> None:
        response = client.small_molecule.library_screen.with_raw_response.start(
            molecules=[{"smiles": "smiles"}],
            target={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = response.parse()
        assert_matches_type(LibraryScreenStartResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_start(self, client: Boltz) -> None:
        with client.small_molecule.library_screen.with_streaming_response.start(
            molecules=[{"smiles": "smiles"}],
            target={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
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
        library_screen = client.small_molecule.library_screen.stop(
            "id",
        )
        assert_matches_type(LibraryScreenStopResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_stop(self, client: Boltz) -> None:
        response = client.small_molecule.library_screen.with_raw_response.stop(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = response.parse()
        assert_matches_type(LibraryScreenStopResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_stop(self, client: Boltz) -> None:
        with client.small_molecule.library_screen.with_streaming_response.stop(
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
            client.small_molecule.library_screen.with_raw_response.stop(
                "",
            )


class TestAsyncLibraryScreen:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.small_molecule.library_screen.retrieve(
            id="id",
        )
        assert_matches_type(LibraryScreenRetrieveResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.small_molecule.library_screen.retrieve(
            id="id",
            workspace_id="workspace_id",
        )
        assert_matches_type(LibraryScreenRetrieveResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncBoltz) -> None:
        response = await async_client.small_molecule.library_screen.with_raw_response.retrieve(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = await response.parse()
        assert_matches_type(LibraryScreenRetrieveResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncBoltz) -> None:
        async with async_client.small_molecule.library_screen.with_streaming_response.retrieve(
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
            await async_client.small_molecule.library_screen.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.small_molecule.library_screen.list()
        assert_matches_type(AsyncCursorPage[LibraryScreenListResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.small_molecule.library_screen.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
            workspace_id="workspace_id",
        )
        assert_matches_type(AsyncCursorPage[LibraryScreenListResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncBoltz) -> None:
        response = await async_client.small_molecule.library_screen.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = await response.parse()
        assert_matches_type(AsyncCursorPage[LibraryScreenListResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncBoltz) -> None:
        async with async_client.small_molecule.library_screen.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            library_screen = await response.parse()
            assert_matches_type(AsyncCursorPage[LibraryScreenListResponse], library_screen, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete_data(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.small_molecule.library_screen.delete_data(
            "id",
        )
        assert_matches_type(LibraryScreenDeleteDataResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete_data(self, async_client: AsyncBoltz) -> None:
        response = await async_client.small_molecule.library_screen.with_raw_response.delete_data(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = await response.parse()
        assert_matches_type(LibraryScreenDeleteDataResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete_data(self, async_client: AsyncBoltz) -> None:
        async with async_client.small_molecule.library_screen.with_streaming_response.delete_data(
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
            await async_client.small_molecule.library_screen.with_raw_response.delete_data(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_estimate_cost(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.small_molecule.library_screen.estimate_cost(
            molecules=[{"smiles": "smiles"}],
            target={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
        )
        assert_matches_type(LibraryScreenEstimateCostResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_estimate_cost_with_all_params(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.small_molecule.library_screen.estimate_cost(
            molecules=[
                {
                    "smiles": "smiles",
                    "id": "id",
                }
            ],
            target={
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
                "bonds": [
                    {
                        "atom1": {
                            "atom_name": "atom_name",
                            "chain_id": "chain_id",
                            "residue_index": 0,
                            "type": "polymer_atom",
                        },
                        "atom2": {
                            "atom_name": "atom_name",
                            "chain_id": "chain_id",
                            "residue_index": 0,
                            "type": "polymer_atom",
                        },
                    }
                ],
                "constraints": [
                    {
                        "binder_chain_id": "binder_chain_id",
                        "contact_residues": {"A": [42, 43, 44, 67, 68, 69]},
                        "max_distance_angstrom": 0,
                        "type": "pocket",
                        "force": True,
                    }
                ],
                "pocket_residues": {"A": [42, 43, 44, 67, 68, 69]},
                "reference_ligands": ["string"],
                "type": "no_template",
            },
            idempotency_key="idempotency_key",
            molecule_filters={
                "boltz_smarts_catalog_filter_level": "recommended",
                "custom_filters": [
                    {
                        "max_hba": 0,
                        "max_hbd": 0,
                        "max_logp": 0,
                        "max_mw": 0,
                        "type": "lipinski_filter",
                        "allow_single_violation": True,
                    }
                ],
            },
            workspace_id="workspace_id",
        )
        assert_matches_type(LibraryScreenEstimateCostResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_estimate_cost(self, async_client: AsyncBoltz) -> None:
        response = await async_client.small_molecule.library_screen.with_raw_response.estimate_cost(
            molecules=[{"smiles": "smiles"}],
            target={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = await response.parse()
        assert_matches_type(LibraryScreenEstimateCostResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_estimate_cost(self, async_client: AsyncBoltz) -> None:
        async with async_client.small_molecule.library_screen.with_streaming_response.estimate_cost(
            molecules=[{"smiles": "smiles"}],
            target={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
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
        library_screen = await async_client.small_molecule.library_screen.list_results(
            id="id",
        )
        assert_matches_type(AsyncCursorPage[LibraryScreenListResultsResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_results_with_all_params(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.small_molecule.library_screen.list_results(
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
        response = await async_client.small_molecule.library_screen.with_raw_response.list_results(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = await response.parse()
        assert_matches_type(AsyncCursorPage[LibraryScreenListResultsResponse], library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list_results(self, async_client: AsyncBoltz) -> None:
        async with async_client.small_molecule.library_screen.with_streaming_response.list_results(
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
            await async_client.small_molecule.library_screen.with_raw_response.list_results(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_resume(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.small_molecule.library_screen.resume(
            "id",
        )
        assert_matches_type(LibraryScreenResumeResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_resume(self, async_client: AsyncBoltz) -> None:
        response = await async_client.small_molecule.library_screen.with_raw_response.resume(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = await response.parse()
        assert_matches_type(LibraryScreenResumeResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_resume(self, async_client: AsyncBoltz) -> None:
        async with async_client.small_molecule.library_screen.with_streaming_response.resume(
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
            await async_client.small_molecule.library_screen.with_raw_response.resume(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.small_molecule.library_screen.start(
            molecules=[{"smiles": "smiles"}],
            target={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
        )
        assert_matches_type(LibraryScreenStartResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start_with_all_params(self, async_client: AsyncBoltz) -> None:
        library_screen = await async_client.small_molecule.library_screen.start(
            molecules=[
                {
                    "smiles": "smiles",
                    "id": "id",
                }
            ],
            target={
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
                "bonds": [
                    {
                        "atom1": {
                            "atom_name": "atom_name",
                            "chain_id": "chain_id",
                            "residue_index": 0,
                            "type": "polymer_atom",
                        },
                        "atom2": {
                            "atom_name": "atom_name",
                            "chain_id": "chain_id",
                            "residue_index": 0,
                            "type": "polymer_atom",
                        },
                    }
                ],
                "constraints": [
                    {
                        "binder_chain_id": "binder_chain_id",
                        "contact_residues": {"A": [42, 43, 44, 67, 68, 69]},
                        "max_distance_angstrom": 0,
                        "type": "pocket",
                        "force": True,
                    }
                ],
                "pocket_residues": {"A": [42, 43, 44, 67, 68, 69]},
                "reference_ligands": ["string"],
                "type": "no_template",
            },
            idempotency_key="idempotency_key",
            molecule_filters={
                "boltz_smarts_catalog_filter_level": "recommended",
                "custom_filters": [
                    {
                        "max_hba": 0,
                        "max_hbd": 0,
                        "max_logp": 0,
                        "max_mw": 0,
                        "type": "lipinski_filter",
                        "allow_single_violation": True,
                    }
                ],
            },
            workspace_id="workspace_id",
        )
        assert_matches_type(LibraryScreenStartResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_start(self, async_client: AsyncBoltz) -> None:
        response = await async_client.small_molecule.library_screen.with_raw_response.start(
            molecules=[{"smiles": "smiles"}],
            target={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = await response.parse()
        assert_matches_type(LibraryScreenStartResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_start(self, async_client: AsyncBoltz) -> None:
        async with async_client.small_molecule.library_screen.with_streaming_response.start(
            molecules=[{"smiles": "smiles"}],
            target={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
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
        library_screen = await async_client.small_molecule.library_screen.stop(
            "id",
        )
        assert_matches_type(LibraryScreenStopResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_stop(self, async_client: AsyncBoltz) -> None:
        response = await async_client.small_molecule.library_screen.with_raw_response.stop(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        library_screen = await response.parse()
        assert_matches_type(LibraryScreenStopResponse, library_screen, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_stop(self, async_client: AsyncBoltz) -> None:
        async with async_client.small_molecule.library_screen.with_streaming_response.stop(
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
            await async_client.small_molecule.library_screen.with_raw_response.stop(
                "",
            )
