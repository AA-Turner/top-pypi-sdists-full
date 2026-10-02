# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from boltz_api import Boltz, AsyncBoltz
from tests.utils import assert_matches_type
from boltz_api.pagination import SyncCursorPage, AsyncCursorPage
from boltz_api.types.protein import (
    SequenceRedesignListResponse,
    SequenceRedesignStopResponse,
    SequenceRedesignStartResponse,
    SequenceRedesignResumeResponse,
    SequenceRedesignRetrieveResponse,
    SequenceRedesignDeleteDataResponse,
    SequenceRedesignListResultsResponse,
    SequenceRedesignEstimateCostResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSequenceRedesign:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Boltz) -> None:
        sequence_redesign = client.protein.sequence_redesign.retrieve(
            id="id",
        )
        assert_matches_type(SequenceRedesignRetrieveResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Boltz) -> None:
        sequence_redesign = client.protein.sequence_redesign.retrieve(
            id="id",
            workspace_id="workspace_id",
        )
        assert_matches_type(SequenceRedesignRetrieveResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Boltz) -> None:
        response = client.protein.sequence_redesign.with_raw_response.retrieve(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = response.parse()
        assert_matches_type(SequenceRedesignRetrieveResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Boltz) -> None:
        with client.protein.sequence_redesign.with_streaming_response.retrieve(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = response.parse()
            assert_matches_type(SequenceRedesignRetrieveResponse, sequence_redesign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.protein.sequence_redesign.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Boltz) -> None:
        sequence_redesign = client.protein.sequence_redesign.list()
        assert_matches_type(SyncCursorPage[SequenceRedesignListResponse], sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Boltz) -> None:
        sequence_redesign = client.protein.sequence_redesign.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
            workspace_id="workspace_id",
        )
        assert_matches_type(SyncCursorPage[SequenceRedesignListResponse], sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Boltz) -> None:
        response = client.protein.sequence_redesign.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = response.parse()
        assert_matches_type(SyncCursorPage[SequenceRedesignListResponse], sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Boltz) -> None:
        with client.protein.sequence_redesign.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = response.parse()
            assert_matches_type(SyncCursorPage[SequenceRedesignListResponse], sequence_redesign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete_data(self, client: Boltz) -> None:
        sequence_redesign = client.protein.sequence_redesign.delete_data(
            "id",
        )
        assert_matches_type(SequenceRedesignDeleteDataResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete_data(self, client: Boltz) -> None:
        response = client.protein.sequence_redesign.with_raw_response.delete_data(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = response.parse()
        assert_matches_type(SequenceRedesignDeleteDataResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete_data(self, client: Boltz) -> None:
        with client.protein.sequence_redesign.with_streaming_response.delete_data(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = response.parse()
            assert_matches_type(SequenceRedesignDeleteDataResponse, sequence_redesign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete_data(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.protein.sequence_redesign.with_raw_response.delete_data(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_estimate_cost_overload_1(self, client: Boltz) -> None:
        sequence_redesign = client.protein.sequence_redesign.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="binder",
        )
        assert_matches_type(SequenceRedesignEstimateCostResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_estimate_cost_with_all_params_overload_1(self, client: Boltz) -> None:
        sequence_redesign = client.protein.sequence_redesign.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
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
        assert_matches_type(SequenceRedesignEstimateCostResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_estimate_cost_overload_1(self, client: Boltz) -> None:
        response = client.protein.sequence_redesign.with_raw_response.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="binder",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = response.parse()
        assert_matches_type(SequenceRedesignEstimateCostResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_estimate_cost_overload_1(self, client: Boltz) -> None:
        with client.protein.sequence_redesign.with_streaming_response.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="binder",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = response.parse()
            assert_matches_type(SequenceRedesignEstimateCostResponse, sequence_redesign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_estimate_cost_overload_2(self, client: Boltz) -> None:
        sequence_redesign = client.protein.sequence_redesign.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="generic",
        )
        assert_matches_type(SequenceRedesignEstimateCostResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_estimate_cost_with_all_params_overload_2(self, client: Boltz) -> None:
        sequence_redesign = client.protein.sequence_redesign.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "type": "from_template",
                    "design_motifs": [
                        {
                            "filters": [
                                {
                                    "amino_acids": ["I"],
                                    "type": "excluded_amino_acids",
                                }
                            ],
                            "residues": [0],
                            "type": "residues",
                        }
                    ],
                }
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="generic",
            global_design_filters=[
                {
                    "amino_acids": ["I"],
                    "type": "excluded_amino_acids",
                }
            ],
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(SequenceRedesignEstimateCostResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_estimate_cost_overload_2(self, client: Boltz) -> None:
        response = client.protein.sequence_redesign.with_raw_response.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="generic",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = response.parse()
        assert_matches_type(SequenceRedesignEstimateCostResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_estimate_cost_overload_2(self, client: Boltz) -> None:
        with client.protein.sequence_redesign.with_streaming_response.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="generic",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = response.parse()
            assert_matches_type(SequenceRedesignEstimateCostResponse, sequence_redesign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_results(self, client: Boltz) -> None:
        sequence_redesign = client.protein.sequence_redesign.list_results(
            id="id",
        )
        assert_matches_type(SyncCursorPage[SequenceRedesignListResultsResponse], sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_results_with_all_params(self, client: Boltz) -> None:
        sequence_redesign = client.protein.sequence_redesign.list_results(
            id="id",
            after_id="after_id",
            before_id="before_id",
            ids="ids",
            limit=1,
            workspace_id="workspace_id",
        )
        assert_matches_type(SyncCursorPage[SequenceRedesignListResultsResponse], sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list_results(self, client: Boltz) -> None:
        response = client.protein.sequence_redesign.with_raw_response.list_results(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = response.parse()
        assert_matches_type(SyncCursorPage[SequenceRedesignListResultsResponse], sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list_results(self, client: Boltz) -> None:
        with client.protein.sequence_redesign.with_streaming_response.list_results(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = response.parse()
            assert_matches_type(
                SyncCursorPage[SequenceRedesignListResultsResponse], sequence_redesign, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_list_results(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.protein.sequence_redesign.with_raw_response.list_results(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_resume(self, client: Boltz) -> None:
        sequence_redesign = client.protein.sequence_redesign.resume(
            "id",
        )
        assert_matches_type(SequenceRedesignResumeResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_resume(self, client: Boltz) -> None:
        response = client.protein.sequence_redesign.with_raw_response.resume(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = response.parse()
        assert_matches_type(SequenceRedesignResumeResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_resume(self, client: Boltz) -> None:
        with client.protein.sequence_redesign.with_streaming_response.resume(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = response.parse()
            assert_matches_type(SequenceRedesignResumeResponse, sequence_redesign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_resume(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.protein.sequence_redesign.with_raw_response.resume(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start_overload_1(self, client: Boltz) -> None:
        sequence_redesign = client.protein.sequence_redesign.start(
            entities=[
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="binder",
        )
        assert_matches_type(SequenceRedesignStartResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start_with_all_params_overload_1(self, client: Boltz) -> None:
        sequence_redesign = client.protein.sequence_redesign.start(
            entities=[
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
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
        assert_matches_type(SequenceRedesignStartResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_start_overload_1(self, client: Boltz) -> None:
        response = client.protein.sequence_redesign.with_raw_response.start(
            entities=[
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="binder",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = response.parse()
        assert_matches_type(SequenceRedesignStartResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_start_overload_1(self, client: Boltz) -> None:
        with client.protein.sequence_redesign.with_streaming_response.start(
            entities=[
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="binder",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = response.parse()
            assert_matches_type(SequenceRedesignStartResponse, sequence_redesign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start_overload_2(self, client: Boltz) -> None:
        sequence_redesign = client.protein.sequence_redesign.start(
            entities=[
                {
                    "chain_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="generic",
        )
        assert_matches_type(SequenceRedesignStartResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_start_with_all_params_overload_2(self, client: Boltz) -> None:
        sequence_redesign = client.protein.sequence_redesign.start(
            entities=[
                {
                    "chain_id": "x",
                    "type": "from_template",
                    "design_motifs": [
                        {
                            "filters": [
                                {
                                    "amino_acids": ["I"],
                                    "type": "excluded_amino_acids",
                                }
                            ],
                            "residues": [0],
                            "type": "residues",
                        }
                    ],
                }
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="generic",
            global_design_filters=[
                {
                    "amino_acids": ["I"],
                    "type": "excluded_amino_acids",
                }
            ],
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(SequenceRedesignStartResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_start_overload_2(self, client: Boltz) -> None:
        response = client.protein.sequence_redesign.with_raw_response.start(
            entities=[
                {
                    "chain_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="generic",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = response.parse()
        assert_matches_type(SequenceRedesignStartResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_start_overload_2(self, client: Boltz) -> None:
        with client.protein.sequence_redesign.with_streaming_response.start(
            entities=[
                {
                    "chain_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="generic",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = response.parse()
            assert_matches_type(SequenceRedesignStartResponse, sequence_redesign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_stop(self, client: Boltz) -> None:
        sequence_redesign = client.protein.sequence_redesign.stop(
            "id",
        )
        assert_matches_type(SequenceRedesignStopResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_stop(self, client: Boltz) -> None:
        response = client.protein.sequence_redesign.with_raw_response.stop(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = response.parse()
        assert_matches_type(SequenceRedesignStopResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_stop(self, client: Boltz) -> None:
        with client.protein.sequence_redesign.with_streaming_response.stop(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = response.parse()
            assert_matches_type(SequenceRedesignStopResponse, sequence_redesign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_stop(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.protein.sequence_redesign.with_raw_response.stop(
                "",
            )


class TestAsyncSequenceRedesign:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncBoltz) -> None:
        sequence_redesign = await async_client.protein.sequence_redesign.retrieve(
            id="id",
        )
        assert_matches_type(SequenceRedesignRetrieveResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncBoltz) -> None:
        sequence_redesign = await async_client.protein.sequence_redesign.retrieve(
            id="id",
            workspace_id="workspace_id",
        )
        assert_matches_type(SequenceRedesignRetrieveResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.sequence_redesign.with_raw_response.retrieve(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = await response.parse()
        assert_matches_type(SequenceRedesignRetrieveResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.sequence_redesign.with_streaming_response.retrieve(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = await response.parse()
            assert_matches_type(SequenceRedesignRetrieveResponse, sequence_redesign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.protein.sequence_redesign.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncBoltz) -> None:
        sequence_redesign = await async_client.protein.sequence_redesign.list()
        assert_matches_type(AsyncCursorPage[SequenceRedesignListResponse], sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncBoltz) -> None:
        sequence_redesign = await async_client.protein.sequence_redesign.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
            workspace_id="workspace_id",
        )
        assert_matches_type(AsyncCursorPage[SequenceRedesignListResponse], sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.sequence_redesign.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = await response.parse()
        assert_matches_type(AsyncCursorPage[SequenceRedesignListResponse], sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.sequence_redesign.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = await response.parse()
            assert_matches_type(AsyncCursorPage[SequenceRedesignListResponse], sequence_redesign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete_data(self, async_client: AsyncBoltz) -> None:
        sequence_redesign = await async_client.protein.sequence_redesign.delete_data(
            "id",
        )
        assert_matches_type(SequenceRedesignDeleteDataResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete_data(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.sequence_redesign.with_raw_response.delete_data(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = await response.parse()
        assert_matches_type(SequenceRedesignDeleteDataResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete_data(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.sequence_redesign.with_streaming_response.delete_data(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = await response.parse()
            assert_matches_type(SequenceRedesignDeleteDataResponse, sequence_redesign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete_data(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.protein.sequence_redesign.with_raw_response.delete_data(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_estimate_cost_overload_1(self, async_client: AsyncBoltz) -> None:
        sequence_redesign = await async_client.protein.sequence_redesign.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="binder",
        )
        assert_matches_type(SequenceRedesignEstimateCostResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_estimate_cost_with_all_params_overload_1(self, async_client: AsyncBoltz) -> None:
        sequence_redesign = await async_client.protein.sequence_redesign.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
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
        assert_matches_type(SequenceRedesignEstimateCostResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_estimate_cost_overload_1(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.sequence_redesign.with_raw_response.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="binder",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = await response.parse()
        assert_matches_type(SequenceRedesignEstimateCostResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_estimate_cost_overload_1(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.sequence_redesign.with_streaming_response.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="binder",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = await response.parse()
            assert_matches_type(SequenceRedesignEstimateCostResponse, sequence_redesign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_estimate_cost_overload_2(self, async_client: AsyncBoltz) -> None:
        sequence_redesign = await async_client.protein.sequence_redesign.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="generic",
        )
        assert_matches_type(SequenceRedesignEstimateCostResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_estimate_cost_with_all_params_overload_2(self, async_client: AsyncBoltz) -> None:
        sequence_redesign = await async_client.protein.sequence_redesign.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "type": "from_template",
                    "design_motifs": [
                        {
                            "filters": [
                                {
                                    "amino_acids": ["I"],
                                    "type": "excluded_amino_acids",
                                }
                            ],
                            "residues": [0],
                            "type": "residues",
                        }
                    ],
                }
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="generic",
            global_design_filters=[
                {
                    "amino_acids": ["I"],
                    "type": "excluded_amino_acids",
                }
            ],
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(SequenceRedesignEstimateCostResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_estimate_cost_overload_2(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.sequence_redesign.with_raw_response.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="generic",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = await response.parse()
        assert_matches_type(SequenceRedesignEstimateCostResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_estimate_cost_overload_2(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.sequence_redesign.with_streaming_response.estimate_cost(
            entities=[
                {
                    "chain_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="generic",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = await response.parse()
            assert_matches_type(SequenceRedesignEstimateCostResponse, sequence_redesign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_results(self, async_client: AsyncBoltz) -> None:
        sequence_redesign = await async_client.protein.sequence_redesign.list_results(
            id="id",
        )
        assert_matches_type(AsyncCursorPage[SequenceRedesignListResultsResponse], sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_results_with_all_params(self, async_client: AsyncBoltz) -> None:
        sequence_redesign = await async_client.protein.sequence_redesign.list_results(
            id="id",
            after_id="after_id",
            before_id="before_id",
            ids="ids",
            limit=1,
            workspace_id="workspace_id",
        )
        assert_matches_type(AsyncCursorPage[SequenceRedesignListResultsResponse], sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list_results(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.sequence_redesign.with_raw_response.list_results(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = await response.parse()
        assert_matches_type(AsyncCursorPage[SequenceRedesignListResultsResponse], sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list_results(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.sequence_redesign.with_streaming_response.list_results(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = await response.parse()
            assert_matches_type(
                AsyncCursorPage[SequenceRedesignListResultsResponse], sequence_redesign, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_list_results(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.protein.sequence_redesign.with_raw_response.list_results(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_resume(self, async_client: AsyncBoltz) -> None:
        sequence_redesign = await async_client.protein.sequence_redesign.resume(
            "id",
        )
        assert_matches_type(SequenceRedesignResumeResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_resume(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.sequence_redesign.with_raw_response.resume(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = await response.parse()
        assert_matches_type(SequenceRedesignResumeResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_resume(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.sequence_redesign.with_streaming_response.resume(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = await response.parse()
            assert_matches_type(SequenceRedesignResumeResponse, sequence_redesign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_resume(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.protein.sequence_redesign.with_raw_response.resume(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start_overload_1(self, async_client: AsyncBoltz) -> None:
        sequence_redesign = await async_client.protein.sequence_redesign.start(
            entities=[
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="binder",
        )
        assert_matches_type(SequenceRedesignStartResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start_with_all_params_overload_1(self, async_client: AsyncBoltz) -> None:
        sequence_redesign = await async_client.protein.sequence_redesign.start(
            entities=[
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
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
        assert_matches_type(SequenceRedesignStartResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_start_overload_1(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.sequence_redesign.with_raw_response.start(
            entities=[
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="binder",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = await response.parse()
        assert_matches_type(SequenceRedesignStartResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_start_overload_1(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.sequence_redesign.with_streaming_response.start(
            entities=[
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
                {
                    "chain_id": "x",
                    "role": "target",
                    "type": "from_template",
                },
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="binder",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = await response.parse()
            assert_matches_type(SequenceRedesignStartResponse, sequence_redesign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start_overload_2(self, async_client: AsyncBoltz) -> None:
        sequence_redesign = await async_client.protein.sequence_redesign.start(
            entities=[
                {
                    "chain_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="generic",
        )
        assert_matches_type(SequenceRedesignStartResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_start_with_all_params_overload_2(self, async_client: AsyncBoltz) -> None:
        sequence_redesign = await async_client.protein.sequence_redesign.start(
            entities=[
                {
                    "chain_id": "x",
                    "type": "from_template",
                    "design_motifs": [
                        {
                            "filters": [
                                {
                                    "amino_acids": ["I"],
                                    "type": "excluded_amino_acids",
                                }
                            ],
                            "residues": [0],
                            "type": "residues",
                        }
                    ],
                }
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="generic",
            global_design_filters=[
                {
                    "amino_acids": ["I"],
                    "type": "excluded_amino_acids",
                }
            ],
            idempotency_key="idempotency_key",
            workspace_id="workspace_id",
        )
        assert_matches_type(SequenceRedesignStartResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_start_overload_2(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.sequence_redesign.with_raw_response.start(
            entities=[
                {
                    "chain_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="generic",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = await response.parse()
        assert_matches_type(SequenceRedesignStartResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_start_overload_2(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.sequence_redesign.with_streaming_response.start(
            entities=[
                {
                    "chain_id": "x",
                    "type": "from_template",
                }
            ],
            num_proteins=1,
            structure={
                "type": "url",
                "url": "https://example.com",
            },
            type="generic",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = await response.parse()
            assert_matches_type(SequenceRedesignStartResponse, sequence_redesign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_stop(self, async_client: AsyncBoltz) -> None:
        sequence_redesign = await async_client.protein.sequence_redesign.stop(
            "id",
        )
        assert_matches_type(SequenceRedesignStopResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_stop(self, async_client: AsyncBoltz) -> None:
        response = await async_client.protein.sequence_redesign.with_raw_response.stop(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sequence_redesign = await response.parse()
        assert_matches_type(SequenceRedesignStopResponse, sequence_redesign, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_stop(self, async_client: AsyncBoltz) -> None:
        async with async_client.protein.sequence_redesign.with_streaming_response.stop(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sequence_redesign = await response.parse()
            assert_matches_type(SequenceRedesignStopResponse, sequence_redesign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_stop(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.protein.sequence_redesign.with_raw_response.stop(
                "",
            )
