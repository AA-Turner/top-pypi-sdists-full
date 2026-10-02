# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from boltz_api import Boltz, AsyncBoltz
from tests.utils import assert_matches_type
from boltz_api.pagination import SyncCursorPage, AsyncCursorPage
from boltz_api.types.predictions import (
    StructureAndBindingListResponse,
    StructureAndBindingStartResponse,
    StructureAndBindingRetrieveResponse,
    StructureAndBindingDeleteDataResponse,
    StructureAndBindingEstimateCostResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestStructureAndBinding:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Boltz) -> None:
        structure_and_binding = client.predictions.structure_and_binding.retrieve(
            id="sab_pred_2X7Ab9Cd3Ef6Gh1JkLmN",
        )
        assert_matches_type(StructureAndBindingRetrieveResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Boltz) -> None:
        structure_and_binding = client.predictions.structure_and_binding.retrieve(
            id="sab_pred_2X7Ab9Cd3Ef6Gh1JkLmN",
            workspace_id="workspace_id",
        )
        assert_matches_type(StructureAndBindingRetrieveResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Boltz) -> None:
        response = client.predictions.structure_and_binding.with_raw_response.retrieve(
            id="sab_pred_2X7Ab9Cd3Ef6Gh1JkLmN",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        structure_and_binding = response.parse()
        assert_matches_type(StructureAndBindingRetrieveResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Boltz) -> None:
        with client.predictions.structure_and_binding.with_streaming_response.retrieve(
            id="sab_pred_2X7Ab9Cd3Ef6Gh1JkLmN",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            structure_and_binding = response.parse()
            assert_matches_type(StructureAndBindingRetrieveResponse, structure_and_binding, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.predictions.structure_and_binding.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Boltz) -> None:
        structure_and_binding = client.predictions.structure_and_binding.list()
        assert_matches_type(SyncCursorPage[StructureAndBindingListResponse], structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Boltz) -> None:
        structure_and_binding = client.predictions.structure_and_binding.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
            workspace_id="workspace_id",
        )
        assert_matches_type(SyncCursorPage[StructureAndBindingListResponse], structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Boltz) -> None:
        response = client.predictions.structure_and_binding.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        structure_and_binding = response.parse()
        assert_matches_type(SyncCursorPage[StructureAndBindingListResponse], structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Boltz) -> None:
        with client.predictions.structure_and_binding.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            structure_and_binding = response.parse()
            assert_matches_type(
                SyncCursorPage[StructureAndBindingListResponse], structure_and_binding, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete_data(self, client: Boltz) -> None:
        structure_and_binding = client.predictions.structure_and_binding.delete_data(
            "sab_pred_2X7Ab9Cd3Ef6Gh1JkLmN",
        )
        assert_matches_type(StructureAndBindingDeleteDataResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete_data(self, client: Boltz) -> None:
        response = client.predictions.structure_and_binding.with_raw_response.delete_data(
            "sab_pred_2X7Ab9Cd3Ef6Gh1JkLmN",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        structure_and_binding = response.parse()
        assert_matches_type(StructureAndBindingDeleteDataResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete_data(self, client: Boltz) -> None:
        with client.predictions.structure_and_binding.with_streaming_response.delete_data(
            "sab_pred_2X7Ab9Cd3Ef6Gh1JkLmN",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            structure_and_binding = response.parse()
            assert_matches_type(StructureAndBindingDeleteDataResponse, structure_and_binding, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete_data(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.predictions.structure_and_binding.with_raw_response.delete_data(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_estimate_cost(self, client: Boltz) -> None:
        structure_and_binding = client.predictions.structure_and_binding.estimate_cost(
            input={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
            model="boltz-2.1",
        )
        assert_matches_type(StructureAndBindingEstimateCostResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_estimate_cost_with_all_params(self, client: Boltz) -> None:
        structure_and_binding = client.predictions.structure_and_binding.estimate_cost(
            input={
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
                        "msa": {
                            "format": "a3m",
                            "source": {
                                "type": "url",
                                "url": "https://example.com",
                            },
                            "type": "custom",
                        },
                    }
                ],
                "binding": {
                    "binder_chain_id": "binder_chain_id",
                    "type": "ligand_protein_binding",
                },
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
                "model_options": {
                    "recycling_steps": 1,
                    "sampling_steps": 50,
                    "step_scale": 1.3,
                },
                "num_samples": 1,
                "templates": [
                    {
                        "template_chains": [
                            {
                                "input_chain_id": "input_chain_id",
                                "template_chain_id": "template_chain_id",
                            }
                        ],
                        "template_structure": {
                            "type": "url",
                            "url": "https://example.com",
                        },
                        "force_threshold_angstroms": 0,
                    }
                ],
            },
            model="boltz-2.1",
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(StructureAndBindingEstimateCostResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_estimate_cost(self, client: Boltz) -> None:
        response = client.predictions.structure_and_binding.with_raw_response.estimate_cost(
            input={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
            model="boltz-2.1",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        structure_and_binding = response.parse()
        assert_matches_type(StructureAndBindingEstimateCostResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_estimate_cost(self, client: Boltz) -> None:
        with client.predictions.structure_and_binding.with_streaming_response.estimate_cost(
            input={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
            model="boltz-2.1",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            structure_and_binding = response.parse()
            assert_matches_type(StructureAndBindingEstimateCostResponse, structure_and_binding, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start(self, client: Boltz) -> None:
        structure_and_binding = client.predictions.structure_and_binding.start(
            input={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
            model="boltz-2.1",
        )
        assert_matches_type(StructureAndBindingStartResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start_with_all_params(self, client: Boltz) -> None:
        structure_and_binding = client.predictions.structure_and_binding.start(
            input={
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
                        "msa": {
                            "format": "a3m",
                            "source": {
                                "type": "url",
                                "url": "https://example.com",
                            },
                            "type": "custom",
                        },
                    }
                ],
                "binding": {
                    "binder_chain_id": "binder_chain_id",
                    "type": "ligand_protein_binding",
                },
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
                "model_options": {
                    "recycling_steps": 1,
                    "sampling_steps": 50,
                    "step_scale": 1.3,
                },
                "num_samples": 1,
                "templates": [
                    {
                        "template_chains": [
                            {
                                "input_chain_id": "input_chain_id",
                                "template_chain_id": "template_chain_id",
                            }
                        ],
                        "template_structure": {
                            "type": "url",
                            "url": "https://example.com",
                        },
                        "force_threshold_angstroms": 0,
                    }
                ],
            },
            model="boltz-2.1",
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(StructureAndBindingStartResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_start(self, client: Boltz) -> None:
        response = client.predictions.structure_and_binding.with_raw_response.start(
            input={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
            model="boltz-2.1",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        structure_and_binding = response.parse()
        assert_matches_type(StructureAndBindingStartResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_start(self, client: Boltz) -> None:
        with client.predictions.structure_and_binding.with_streaming_response.start(
            input={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
            model="boltz-2.1",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            structure_and_binding = response.parse()
            assert_matches_type(StructureAndBindingStartResponse, structure_and_binding, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncStructureAndBinding:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncBoltz) -> None:
        structure_and_binding = await async_client.predictions.structure_and_binding.retrieve(
            id="sab_pred_2X7Ab9Cd3Ef6Gh1JkLmN",
        )
        assert_matches_type(StructureAndBindingRetrieveResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncBoltz) -> None:
        structure_and_binding = await async_client.predictions.structure_and_binding.retrieve(
            id="sab_pred_2X7Ab9Cd3Ef6Gh1JkLmN",
            workspace_id="workspace_id",
        )
        assert_matches_type(StructureAndBindingRetrieveResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncBoltz) -> None:
        response = await async_client.predictions.structure_and_binding.with_raw_response.retrieve(
            id="sab_pred_2X7Ab9Cd3Ef6Gh1JkLmN",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        structure_and_binding = await response.parse()
        assert_matches_type(StructureAndBindingRetrieveResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncBoltz) -> None:
        async with async_client.predictions.structure_and_binding.with_streaming_response.retrieve(
            id="sab_pred_2X7Ab9Cd3Ef6Gh1JkLmN",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            structure_and_binding = await response.parse()
            assert_matches_type(StructureAndBindingRetrieveResponse, structure_and_binding, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.predictions.structure_and_binding.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncBoltz) -> None:
        structure_and_binding = await async_client.predictions.structure_and_binding.list()
        assert_matches_type(AsyncCursorPage[StructureAndBindingListResponse], structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncBoltz) -> None:
        structure_and_binding = await async_client.predictions.structure_and_binding.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
            workspace_id="workspace_id",
        )
        assert_matches_type(AsyncCursorPage[StructureAndBindingListResponse], structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncBoltz) -> None:
        response = await async_client.predictions.structure_and_binding.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        structure_and_binding = await response.parse()
        assert_matches_type(AsyncCursorPage[StructureAndBindingListResponse], structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncBoltz) -> None:
        async with async_client.predictions.structure_and_binding.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            structure_and_binding = await response.parse()
            assert_matches_type(
                AsyncCursorPage[StructureAndBindingListResponse], structure_and_binding, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete_data(self, async_client: AsyncBoltz) -> None:
        structure_and_binding = await async_client.predictions.structure_and_binding.delete_data(
            "sab_pred_2X7Ab9Cd3Ef6Gh1JkLmN",
        )
        assert_matches_type(StructureAndBindingDeleteDataResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete_data(self, async_client: AsyncBoltz) -> None:
        response = await async_client.predictions.structure_and_binding.with_raw_response.delete_data(
            "sab_pred_2X7Ab9Cd3Ef6Gh1JkLmN",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        structure_and_binding = await response.parse()
        assert_matches_type(StructureAndBindingDeleteDataResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete_data(self, async_client: AsyncBoltz) -> None:
        async with async_client.predictions.structure_and_binding.with_streaming_response.delete_data(
            "sab_pred_2X7Ab9Cd3Ef6Gh1JkLmN",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            structure_and_binding = await response.parse()
            assert_matches_type(StructureAndBindingDeleteDataResponse, structure_and_binding, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete_data(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.predictions.structure_and_binding.with_raw_response.delete_data(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_estimate_cost(self, async_client: AsyncBoltz) -> None:
        structure_and_binding = await async_client.predictions.structure_and_binding.estimate_cost(
            input={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
            model="boltz-2.1",
        )
        assert_matches_type(StructureAndBindingEstimateCostResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_estimate_cost_with_all_params(self, async_client: AsyncBoltz) -> None:
        structure_and_binding = await async_client.predictions.structure_and_binding.estimate_cost(
            input={
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
                        "msa": {
                            "format": "a3m",
                            "source": {
                                "type": "url",
                                "url": "https://example.com",
                            },
                            "type": "custom",
                        },
                    }
                ],
                "binding": {
                    "binder_chain_id": "binder_chain_id",
                    "type": "ligand_protein_binding",
                },
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
                "model_options": {
                    "recycling_steps": 1,
                    "sampling_steps": 50,
                    "step_scale": 1.3,
                },
                "num_samples": 1,
                "templates": [
                    {
                        "template_chains": [
                            {
                                "input_chain_id": "input_chain_id",
                                "template_chain_id": "template_chain_id",
                            }
                        ],
                        "template_structure": {
                            "type": "url",
                            "url": "https://example.com",
                        },
                        "force_threshold_angstroms": 0,
                    }
                ],
            },
            model="boltz-2.1",
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(StructureAndBindingEstimateCostResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_estimate_cost(self, async_client: AsyncBoltz) -> None:
        response = await async_client.predictions.structure_and_binding.with_raw_response.estimate_cost(
            input={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
            model="boltz-2.1",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        structure_and_binding = await response.parse()
        assert_matches_type(StructureAndBindingEstimateCostResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_estimate_cost(self, async_client: AsyncBoltz) -> None:
        async with async_client.predictions.structure_and_binding.with_streaming_response.estimate_cost(
            input={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
            model="boltz-2.1",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            structure_and_binding = await response.parse()
            assert_matches_type(StructureAndBindingEstimateCostResponse, structure_and_binding, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start(self, async_client: AsyncBoltz) -> None:
        structure_and_binding = await async_client.predictions.structure_and_binding.start(
            input={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
            model="boltz-2.1",
        )
        assert_matches_type(StructureAndBindingStartResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start_with_all_params(self, async_client: AsyncBoltz) -> None:
        structure_and_binding = await async_client.predictions.structure_and_binding.start(
            input={
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
                        "msa": {
                            "format": "a3m",
                            "source": {
                                "type": "url",
                                "url": "https://example.com",
                            },
                            "type": "custom",
                        },
                    }
                ],
                "binding": {
                    "binder_chain_id": "binder_chain_id",
                    "type": "ligand_protein_binding",
                },
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
                "model_options": {
                    "recycling_steps": 1,
                    "sampling_steps": 50,
                    "step_scale": 1.3,
                },
                "num_samples": 1,
                "templates": [
                    {
                        "template_chains": [
                            {
                                "input_chain_id": "input_chain_id",
                                "template_chain_id": "template_chain_id",
                            }
                        ],
                        "template_structure": {
                            "type": "url",
                            "url": "https://example.com",
                        },
                        "force_threshold_angstroms": 0,
                    }
                ],
            },
            model="boltz-2.1",
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(StructureAndBindingStartResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_start(self, async_client: AsyncBoltz) -> None:
        response = await async_client.predictions.structure_and_binding.with_raw_response.start(
            input={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
            model="boltz-2.1",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        structure_and_binding = await response.parse()
        assert_matches_type(StructureAndBindingStartResponse, structure_and_binding, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_start(self, async_client: AsyncBoltz) -> None:
        async with async_client.predictions.structure_and_binding.with_streaming_response.start(
            input={
                "entities": [
                    {
                        "chain_ids": ["string"],
                        "type": "protein",
                        "value": "value",
                    }
                ]
            },
            model="boltz-2.1",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            structure_and_binding = await response.parse()
            assert_matches_type(StructureAndBindingStartResponse, structure_and_binding, path=["response"])

        assert cast(Any, response.is_closed) is True
