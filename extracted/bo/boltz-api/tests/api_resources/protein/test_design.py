# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from boltz_api import Boltz, AsyncBoltz
from tests.utils import assert_matches_type
from boltz_api.pagination import SyncCursorPage, AsyncCursorPage
from boltz_api.types.protein import (
    DesignListResponse,
    DesignStopResponse,
    DesignStartResponse,
    DesignResumeResponse,
    DesignRetrieveResponse,
    DesignDeleteDataResponse,
    DesignListResultsResponse,
    DesignEstimateCostResponse,
    DesignListCuratedSpecificationsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDesign:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Boltz) -> None:
        design = client.protein.design.retrieve(
            id="id",
        )
        assert_matches_type(DesignRetrieveResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Boltz) -> None:
        design = client.protein.design.retrieve(
            id="id",
            workspace_id="workspace_id",
        )
        assert_matches_type(DesignRetrieveResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Boltz) -> None:
        response = client.protein.design.with_raw_response.retrieve(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = response.parse()
        assert_matches_type(DesignRetrieveResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Boltz) -> None:
        with client.protein.design.with_streaming_response.retrieve(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = response.parse()
            assert_matches_type(DesignRetrieveResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.protein.design.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Boltz) -> None:
        design = client.protein.design.list()
        assert_matches_type(SyncCursorPage[DesignListResponse], design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Boltz) -> None:
        design = client.protein.design.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
            workspace_id="workspace_id",
        )
        assert_matches_type(SyncCursorPage[DesignListResponse], design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Boltz) -> None:
        response = client.protein.design.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = response.parse()
        assert_matches_type(SyncCursorPage[DesignListResponse], design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Boltz) -> None:
        with client.protein.design.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = response.parse()
            assert_matches_type(SyncCursorPage[DesignListResponse], design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete_data(self, client: Boltz) -> None:
        design = client.protein.design.delete_data(
            "id",
        )
        assert_matches_type(DesignDeleteDataResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete_data(self, client: Boltz) -> None:
        response = client.protein.design.with_raw_response.delete_data(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = response.parse()
        assert_matches_type(DesignDeleteDataResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete_data(self, client: Boltz) -> None:
        with client.protein.design.with_streaming_response.delete_data(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = response.parse()
            assert_matches_type(DesignDeleteDataResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete_data(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.protein.design.with_raw_response.delete_data(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_estimate_cost_overload_1(self, client: Boltz) -> None:
        design = client.protein.design.estimate_cost(
            binder_specification={
                "chain_selection": {
                    "B": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    }
                },
                "modality": "peptide",
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
            num_proteins=10,
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
        assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_estimate_cost_with_all_params_overload_1(self, client: Boltz) -> None:
        design = client.protein.design.estimate_cost(
            binder_specification={
                "chain_selection": {
                    "B": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                        "design_motifs": [
                            {
                                "design_length_range": {
                                    "max": 8,
                                    "min": 4,
                                },
                                "end_index": 5,
                                "start_index": 0,
                                "type": "replacement",
                            }
                        ],
                    }
                },
                "modality": "peptide",
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
                "rules": {
                    "excluded_amino_acids": ["x"],
                    "excluded_sequence_motifs": ["string"],
                    "max_hydrophobic_fraction": 0,
                },
            },
            num_proteins=10,
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
        assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_estimate_cost_overload_1(self, client: Boltz) -> None:
        response = client.protein.design.with_raw_response.estimate_cost(
            binder_specification={
                "chain_selection": {
                    "B": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    }
                },
                "modality": "peptide",
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
            num_proteins=10,
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
        design = response.parse()
        assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_estimate_cost_overload_1(self, client: Boltz) -> None:
        with client.protein.design.with_streaming_response.estimate_cost(
            binder_specification={
                "chain_selection": {
                    "B": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    }
                },
                "modality": "peptide",
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
            num_proteins=10,
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

            design = response.parse()
            assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_estimate_cost_overload_2(self, client: Boltz) -> None:
        design = client.protein.design.estimate_cost(
            binder={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ],
                "modality": "peptide",
            },
            num_proteins=10,
            target={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ]
            },
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="binder",
        )
        assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_estimate_cost_with_all_params_overload_2(self, client: Boltz) -> None:
        design = client.protein.design.estimate_cost(
            binder={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                        "design_motifs": [
                            {
                                "design_length_range": {
                                    "max": 1,
                                    "min": 1,
                                },
                                "end_index": 0,
                                "filters": [
                                    {
                                        "amino_acids": ["I"],
                                        "type": "excluded_amino_acids",
                                    }
                                ],
                                "start_index": 0,
                                "type": "replacement",
                            }
                        ],
                    }
                ],
                "modality": "peptide",
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
            },
            num_proteins=10,
            target={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                        "epitope_residues": [0],
                        "flexible_residues": [0],
                        "non_binding_residues": [0],
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
            },
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="binder",
            global_design_filters=[
                {
                    "amino_acids": ["I"],
                    "type": "excluded_amino_acids",
                }
            ],
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_estimate_cost_overload_2(self, client: Boltz) -> None:
        response = client.protein.design.with_raw_response.estimate_cost(
            binder={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ],
                "modality": "peptide",
            },
            num_proteins=10,
            target={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ]
            },
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="binder",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = response.parse()
        assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_estimate_cost_overload_2(self, client: Boltz) -> None:
        with client.protein.design.with_streaming_response.estimate_cost(
            binder={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ],
                "modality": "peptide",
            },
            num_proteins=10,
            target={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ]
            },
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="binder",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = response.parse()
            assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_estimate_cost_overload_3(self, client: Boltz) -> None:
        design = client.protein.design.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "crop_residues": "all",
                    "template_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=10,
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="generic",
        )
        assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_estimate_cost_with_all_params_overload_3(self, client: Boltz) -> None:
        design = client.protein.design.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "crop_residues": "all",
                    "template_id": "x",
                    "type": "from_template",
                    "design_motifs": [
                        {
                            "design_length_range": {
                                "max": 1,
                                "min": 1,
                            },
                            "end_index": 0,
                            "filters": [
                                {
                                    "amino_acids": ["I"],
                                    "type": "excluded_amino_acids",
                                }
                            ],
                            "start_index": 0,
                            "type": "replacement",
                        }
                    ],
                }
            ],
            num_proteins=10,
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="generic",
            bonds=[
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
            global_design_filters=[
                {
                    "amino_acids": ["I"],
                    "type": "excluded_amino_acids",
                }
            ],
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_estimate_cost_overload_3(self, client: Boltz) -> None:
        response = client.protein.design.with_raw_response.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "crop_residues": "all",
                    "template_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=10,
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="generic",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = response.parse()
        assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_estimate_cost_overload_3(self, client: Boltz) -> None:
        with client.protein.design.with_streaming_response.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "crop_residues": "all",
                    "template_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=10,
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="generic",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = response.parse()
            assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_curated_specifications(self, client: Boltz) -> None:
        design = client.protein.design.list_curated_specifications(
            type="nanobody",
        )
        assert_matches_type(DesignListCuratedSpecificationsResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list_curated_specifications(self, client: Boltz) -> None:
        response = client.protein.design.with_raw_response.list_curated_specifications(
            type="nanobody",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = response.parse()
        assert_matches_type(DesignListCuratedSpecificationsResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list_curated_specifications(self, client: Boltz) -> None:
        with client.protein.design.with_streaming_response.list_curated_specifications(
            type="nanobody",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = response.parse()
            assert_matches_type(DesignListCuratedSpecificationsResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_results(self, client: Boltz) -> None:
        design = client.protein.design.list_results(
            id="id",
        )
        assert_matches_type(SyncCursorPage[DesignListResultsResponse], design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_results_with_all_params(self, client: Boltz) -> None:
        design = client.protein.design.list_results(
            id="id",
            after_id="after_id",
            before_id="before_id",
            ids="ids",
            limit=1,
            workspace_id="workspace_id",
        )
        assert_matches_type(SyncCursorPage[DesignListResultsResponse], design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list_results(self, client: Boltz) -> None:
        response = client.protein.design.with_raw_response.list_results(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = response.parse()
        assert_matches_type(SyncCursorPage[DesignListResultsResponse], design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list_results(self, client: Boltz) -> None:
        with client.protein.design.with_streaming_response.list_results(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = response.parse()
            assert_matches_type(SyncCursorPage[DesignListResultsResponse], design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_list_results(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.protein.design.with_raw_response.list_results(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_resume(self, client: Boltz) -> None:
        design = client.protein.design.resume(
            "id",
        )
        assert_matches_type(DesignResumeResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_resume(self, client: Boltz) -> None:
        response = client.protein.design.with_raw_response.resume(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = response.parse()
        assert_matches_type(DesignResumeResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_resume(self, client: Boltz) -> None:
        with client.protein.design.with_streaming_response.resume(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = response.parse()
            assert_matches_type(DesignResumeResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_resume(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.protein.design.with_raw_response.resume(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start_overload_1(self, client: Boltz) -> None:
        design = client.protein.design.start(
            binder_specification={
                "chain_selection": {
                    "B": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    }
                },
                "modality": "peptide",
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
            num_proteins=10,
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
        assert_matches_type(DesignStartResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start_with_all_params_overload_1(self, client: Boltz) -> None:
        design = client.protein.design.start(
            binder_specification={
                "chain_selection": {
                    "B": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                        "design_motifs": [
                            {
                                "design_length_range": {
                                    "max": 8,
                                    "min": 4,
                                },
                                "end_index": 5,
                                "start_index": 0,
                                "type": "replacement",
                            }
                        ],
                    }
                },
                "modality": "peptide",
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
                "rules": {
                    "excluded_amino_acids": ["x"],
                    "excluded_sequence_motifs": ["string"],
                    "max_hydrophobic_fraction": 0,
                },
            },
            num_proteins=10,
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
        assert_matches_type(DesignStartResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_start_overload_1(self, client: Boltz) -> None:
        response = client.protein.design.with_raw_response.start(
            binder_specification={
                "chain_selection": {
                    "B": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    }
                },
                "modality": "peptide",
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
            num_proteins=10,
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
        design = response.parse()
        assert_matches_type(DesignStartResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_start_overload_1(self, client: Boltz) -> None:
        with client.protein.design.with_streaming_response.start(
            binder_specification={
                "chain_selection": {
                    "B": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    }
                },
                "modality": "peptide",
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
            num_proteins=10,
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

            design = response.parse()
            assert_matches_type(DesignStartResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start_overload_2(self, client: Boltz) -> None:
        design = client.protein.design.start(
            binder={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ],
                "modality": "peptide",
            },
            num_proteins=10,
            target={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ]
            },
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="binder",
        )
        assert_matches_type(DesignStartResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start_with_all_params_overload_2(self, client: Boltz) -> None:
        design = client.protein.design.start(
            binder={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                        "design_motifs": [
                            {
                                "design_length_range": {
                                    "max": 1,
                                    "min": 1,
                                },
                                "end_index": 0,
                                "filters": [
                                    {
                                        "amino_acids": ["I"],
                                        "type": "excluded_amino_acids",
                                    }
                                ],
                                "start_index": 0,
                                "type": "replacement",
                            }
                        ],
                    }
                ],
                "modality": "peptide",
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
            },
            num_proteins=10,
            target={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                        "epitope_residues": [0],
                        "flexible_residues": [0],
                        "non_binding_residues": [0],
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
            },
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="binder",
            global_design_filters=[
                {
                    "amino_acids": ["I"],
                    "type": "excluded_amino_acids",
                }
            ],
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(DesignStartResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_start_overload_2(self, client: Boltz) -> None:
        response = client.protein.design.with_raw_response.start(
            binder={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ],
                "modality": "peptide",
            },
            num_proteins=10,
            target={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ]
            },
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="binder",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = response.parse()
        assert_matches_type(DesignStartResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_start_overload_2(self, client: Boltz) -> None:
        with client.protein.design.with_streaming_response.start(
            binder={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ],
                "modality": "peptide",
            },
            num_proteins=10,
            target={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ]
            },
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="binder",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = response.parse()
            assert_matches_type(DesignStartResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start_overload_3(self, client: Boltz) -> None:
        design = client.protein.design.start(
            entities=[
                {
                    "chain_id": "x",
                    "crop_residues": "all",
                    "template_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=10,
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="generic",
        )
        assert_matches_type(DesignStartResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start_with_all_params_overload_3(self, client: Boltz) -> None:
        design = client.protein.design.start(
            entities=[
                {
                    "chain_id": "x",
                    "crop_residues": "all",
                    "template_id": "x",
                    "type": "from_template",
                    "design_motifs": [
                        {
                            "design_length_range": {
                                "max": 1,
                                "min": 1,
                            },
                            "end_index": 0,
                            "filters": [
                                {
                                    "amino_acids": ["I"],
                                    "type": "excluded_amino_acids",
                                }
                            ],
                            "start_index": 0,
                            "type": "replacement",
                        }
                    ],
                }
            ],
            num_proteins=10,
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="generic",
            bonds=[
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
            global_design_filters=[
                {
                    "amino_acids": ["I"],
                    "type": "excluded_amino_acids",
                }
            ],
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(DesignStartResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_start_overload_3(self, client: Boltz) -> None:
        response = client.protein.design.with_raw_response.start(
            entities=[
                {
                    "chain_id": "x",
                    "crop_residues": "all",
                    "template_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=10,
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="generic",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = response.parse()
        assert_matches_type(DesignStartResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_start_overload_3(self, client: Boltz) -> None:
        with client.protein.design.with_streaming_response.start(
            entities=[
                {
                    "chain_id": "x",
                    "crop_residues": "all",
                    "template_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=10,
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="generic",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = response.parse()
            assert_matches_type(DesignStartResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_stop(self, client: Boltz) -> None:
        design = client.protein.design.stop(
            "id",
        )
        assert_matches_type(DesignStopResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_stop(self, client: Boltz) -> None:
        response = client.protein.design.with_raw_response.stop(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = response.parse()
        assert_matches_type(DesignStopResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_stop(self, client: Boltz) -> None:
        with client.protein.design.with_streaming_response.stop(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = response.parse()
            assert_matches_type(DesignStopResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_stop(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.protein.design.with_raw_response.stop(
                "",
            )


class TestAsyncDesign:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.retrieve(
            id="id",
        )
        assert_matches_type(DesignRetrieveResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.retrieve(
            id="id",
            workspace_id="workspace_id",
        )
        assert_matches_type(DesignRetrieveResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.design.with_raw_response.retrieve(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = await response.parse()
        assert_matches_type(DesignRetrieveResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.design.with_streaming_response.retrieve(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = await response.parse()
            assert_matches_type(DesignRetrieveResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.protein.design.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.list()
        assert_matches_type(AsyncCursorPage[DesignListResponse], design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
            workspace_id="workspace_id",
        )
        assert_matches_type(AsyncCursorPage[DesignListResponse], design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.design.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = await response.parse()
        assert_matches_type(AsyncCursorPage[DesignListResponse], design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.design.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = await response.parse()
            assert_matches_type(AsyncCursorPage[DesignListResponse], design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete_data(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.delete_data(
            "id",
        )
        assert_matches_type(DesignDeleteDataResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete_data(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.design.with_raw_response.delete_data(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = await response.parse()
        assert_matches_type(DesignDeleteDataResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete_data(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.design.with_streaming_response.delete_data(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = await response.parse()
            assert_matches_type(DesignDeleteDataResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete_data(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.protein.design.with_raw_response.delete_data(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_estimate_cost_overload_1(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.estimate_cost(
            binder_specification={
                "chain_selection": {
                    "B": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    }
                },
                "modality": "peptide",
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
            num_proteins=10,
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
        assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_estimate_cost_with_all_params_overload_1(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.estimate_cost(
            binder_specification={
                "chain_selection": {
                    "B": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                        "design_motifs": [
                            {
                                "design_length_range": {
                                    "max": 8,
                                    "min": 4,
                                },
                                "end_index": 5,
                                "start_index": 0,
                                "type": "replacement",
                            }
                        ],
                    }
                },
                "modality": "peptide",
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
                "rules": {
                    "excluded_amino_acids": ["x"],
                    "excluded_sequence_motifs": ["string"],
                    "max_hydrophobic_fraction": 0,
                },
            },
            num_proteins=10,
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
        assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_estimate_cost_overload_1(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.design.with_raw_response.estimate_cost(
            binder_specification={
                "chain_selection": {
                    "B": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    }
                },
                "modality": "peptide",
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
            num_proteins=10,
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
        design = await response.parse()
        assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_estimate_cost_overload_1(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.design.with_streaming_response.estimate_cost(
            binder_specification={
                "chain_selection": {
                    "B": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    }
                },
                "modality": "peptide",
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
            num_proteins=10,
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

            design = await response.parse()
            assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_estimate_cost_overload_2(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.estimate_cost(
            binder={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ],
                "modality": "peptide",
            },
            num_proteins=10,
            target={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ]
            },
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="binder",
        )
        assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_estimate_cost_with_all_params_overload_2(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.estimate_cost(
            binder={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                        "design_motifs": [
                            {
                                "design_length_range": {
                                    "max": 1,
                                    "min": 1,
                                },
                                "end_index": 0,
                                "filters": [
                                    {
                                        "amino_acids": ["I"],
                                        "type": "excluded_amino_acids",
                                    }
                                ],
                                "start_index": 0,
                                "type": "replacement",
                            }
                        ],
                    }
                ],
                "modality": "peptide",
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
            },
            num_proteins=10,
            target={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                        "epitope_residues": [0],
                        "flexible_residues": [0],
                        "non_binding_residues": [0],
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
            },
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="binder",
            global_design_filters=[
                {
                    "amino_acids": ["I"],
                    "type": "excluded_amino_acids",
                }
            ],
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_estimate_cost_overload_2(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.design.with_raw_response.estimate_cost(
            binder={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ],
                "modality": "peptide",
            },
            num_proteins=10,
            target={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ]
            },
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="binder",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = await response.parse()
        assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_estimate_cost_overload_2(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.design.with_streaming_response.estimate_cost(
            binder={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ],
                "modality": "peptide",
            },
            num_proteins=10,
            target={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ]
            },
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="binder",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = await response.parse()
            assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_estimate_cost_overload_3(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "crop_residues": "all",
                    "template_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=10,
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="generic",
        )
        assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_estimate_cost_with_all_params_overload_3(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "crop_residues": "all",
                    "template_id": "x",
                    "type": "from_template",
                    "design_motifs": [
                        {
                            "design_length_range": {
                                "max": 1,
                                "min": 1,
                            },
                            "end_index": 0,
                            "filters": [
                                {
                                    "amino_acids": ["I"],
                                    "type": "excluded_amino_acids",
                                }
                            ],
                            "start_index": 0,
                            "type": "replacement",
                        }
                    ],
                }
            ],
            num_proteins=10,
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="generic",
            bonds=[
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
            global_design_filters=[
                {
                    "amino_acids": ["I"],
                    "type": "excluded_amino_acids",
                }
            ],
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_estimate_cost_overload_3(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.design.with_raw_response.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "crop_residues": "all",
                    "template_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=10,
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="generic",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = await response.parse()
        assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_estimate_cost_overload_3(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.design.with_streaming_response.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "crop_residues": "all",
                    "template_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=10,
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="generic",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = await response.parse()
            assert_matches_type(DesignEstimateCostResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_curated_specifications(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.list_curated_specifications(
            type="nanobody",
        )
        assert_matches_type(DesignListCuratedSpecificationsResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list_curated_specifications(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.design.with_raw_response.list_curated_specifications(
            type="nanobody",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = await response.parse()
        assert_matches_type(DesignListCuratedSpecificationsResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list_curated_specifications(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.design.with_streaming_response.list_curated_specifications(
            type="nanobody",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = await response.parse()
            assert_matches_type(DesignListCuratedSpecificationsResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_results(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.list_results(
            id="id",
        )
        assert_matches_type(AsyncCursorPage[DesignListResultsResponse], design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_results_with_all_params(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.list_results(
            id="id",
            after_id="after_id",
            before_id="before_id",
            ids="ids",
            limit=1,
            workspace_id="workspace_id",
        )
        assert_matches_type(AsyncCursorPage[DesignListResultsResponse], design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list_results(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.design.with_raw_response.list_results(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = await response.parse()
        assert_matches_type(AsyncCursorPage[DesignListResultsResponse], design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list_results(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.design.with_streaming_response.list_results(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = await response.parse()
            assert_matches_type(AsyncCursorPage[DesignListResultsResponse], design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_list_results(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.protein.design.with_raw_response.list_results(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_resume(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.resume(
            "id",
        )
        assert_matches_type(DesignResumeResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_resume(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.design.with_raw_response.resume(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = await response.parse()
        assert_matches_type(DesignResumeResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_resume(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.design.with_streaming_response.resume(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = await response.parse()
            assert_matches_type(DesignResumeResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_resume(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.protein.design.with_raw_response.resume(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start_overload_1(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.start(
            binder_specification={
                "chain_selection": {
                    "B": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    }
                },
                "modality": "peptide",
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
            num_proteins=10,
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
        assert_matches_type(DesignStartResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start_with_all_params_overload_1(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.start(
            binder_specification={
                "chain_selection": {
                    "B": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                        "design_motifs": [
                            {
                                "design_length_range": {
                                    "max": 8,
                                    "min": 4,
                                },
                                "end_index": 5,
                                "start_index": 0,
                                "type": "replacement",
                            }
                        ],
                    }
                },
                "modality": "peptide",
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
                "rules": {
                    "excluded_amino_acids": ["x"],
                    "excluded_sequence_motifs": ["string"],
                    "max_hydrophobic_fraction": 0,
                },
            },
            num_proteins=10,
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
        assert_matches_type(DesignStartResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_start_overload_1(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.design.with_raw_response.start(
            binder_specification={
                "chain_selection": {
                    "B": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    }
                },
                "modality": "peptide",
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
            num_proteins=10,
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
        design = await response.parse()
        assert_matches_type(DesignStartResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_start_overload_1(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.design.with_streaming_response.start(
            binder_specification={
                "chain_selection": {
                    "B": {
                        "chain_type": "polymer",
                        "crop_residues": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    }
                },
                "modality": "peptide",
                "structure": {
                    "type": "url",
                    "url": "https://example.com",
                },
                "type": "structure_template",
            },
            num_proteins=10,
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

            design = await response.parse()
            assert_matches_type(DesignStartResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start_overload_2(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.start(
            binder={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ],
                "modality": "peptide",
            },
            num_proteins=10,
            target={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ]
            },
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="binder",
        )
        assert_matches_type(DesignStartResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start_with_all_params_overload_2(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.start(
            binder={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                        "design_motifs": [
                            {
                                "design_length_range": {
                                    "max": 1,
                                    "min": 1,
                                },
                                "end_index": 0,
                                "filters": [
                                    {
                                        "amino_acids": ["I"],
                                        "type": "excluded_amino_acids",
                                    }
                                ],
                                "start_index": 0,
                                "type": "replacement",
                            }
                        ],
                    }
                ],
                "modality": "peptide",
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
            },
            num_proteins=10,
            target={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                        "epitope_residues": [0],
                        "flexible_residues": [0],
                        "non_binding_residues": [0],
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
            },
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="binder",
            global_design_filters=[
                {
                    "amino_acids": ["I"],
                    "type": "excluded_amino_acids",
                }
            ],
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(DesignStartResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_start_overload_2(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.design.with_raw_response.start(
            binder={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ],
                "modality": "peptide",
            },
            num_proteins=10,
            target={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ]
            },
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="binder",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = await response.parse()
        assert_matches_type(DesignStartResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_start_overload_2(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.design.with_streaming_response.start(
            binder={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ],
                "modality": "peptide",
            },
            num_proteins=10,
            target={
                "entities": [
                    {
                        "chain_id": "x",
                        "crop_residues": "all",
                        "template_id": "x",
                        "type": "from_template",
                    }
                ]
            },
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="binder",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = await response.parse()
            assert_matches_type(DesignStartResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start_overload_3(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.start(
            entities=[
                {
                    "chain_id": "x",
                    "crop_residues": "all",
                    "template_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=10,
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="generic",
        )
        assert_matches_type(DesignStartResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start_with_all_params_overload_3(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.start(
            entities=[
                {
                    "chain_id": "x",
                    "crop_residues": "all",
                    "template_id": "x",
                    "type": "from_template",
                    "design_motifs": [
                        {
                            "design_length_range": {
                                "max": 1,
                                "min": 1,
                            },
                            "end_index": 0,
                            "filters": [
                                {
                                    "amino_acids": ["I"],
                                    "type": "excluded_amino_acids",
                                }
                            ],
                            "start_index": 0,
                            "type": "replacement",
                        }
                    ],
                }
            ],
            num_proteins=10,
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="generic",
            bonds=[
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
            global_design_filters=[
                {
                    "amino_acids": ["I"],
                    "type": "excluded_amino_acids",
                }
            ],
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(DesignStartResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_start_overload_3(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.design.with_raw_response.start(
            entities=[
                {
                    "chain_id": "x",
                    "crop_residues": "all",
                    "template_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=10,
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="generic",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = await response.parse()
        assert_matches_type(DesignStartResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_start_overload_3(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.design.with_streaming_response.start(
            entities=[
                {
                    "chain_id": "x",
                    "crop_residues": "all",
                    "template_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=10,
            templates=[
                {
                    "id": "x",
                    "type": "url",
                    "url": "https://example.com",
                }
            ],
            type="generic",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = await response.parse()
            assert_matches_type(DesignStartResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_stop(self, async_client: AsyncBoltz) -> None:
        design = await async_client.protein.design.stop(
            "id",
        )
        assert_matches_type(DesignStopResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_stop(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.design.with_raw_response.stop(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        design = await response.parse()
        assert_matches_type(DesignStopResponse, design, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_stop(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.design.with_streaming_response.stop(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            design = await response.parse()
            assert_matches_type(DesignStopResponse, design, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_stop(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.protein.design.with_raw_response.stop(
                "",
            )
