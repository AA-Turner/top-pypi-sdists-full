# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Optional, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import (
    Task,
    EvaluationListResponse,
    EvaluationCreateResponse,
    EvaluationUpdateResponse,
    EvaluationRetrieveResponse,
)
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.shared import GenericDeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvaluations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_method_create_overload_1(self, client: SGPClient) -> None:
        evaluation = client.evaluations.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            application_variant_id="application_variant_id",
            description="description",
            evaluation_dataset_id="evaluation_dataset_id",
            name="name",
        )
        assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: SGPClient) -> None:
        evaluation = client.evaluations.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            application_variant_id="application_variant_id",
            description="description",
            evaluation_dataset_id="evaluation_dataset_id",
            name="name",
            annotation_config={
                "components": [
                    [
                        {
                            "data_loc": ["string"],
                            "label": "label",
                            "optional": True,
                        }
                    ]
                ],
                "direction": "col",
                "llm_prompt": {
                    "template": "template",
                    "variables": [
                        {
                            "data_loc": ["string"],
                            "name": "name",
                            "optional": True,
                        }
                    ],
                },
            },
            application_test_case_output_group_id="application_test_case_output_group_id",
            evaluation_config={"foo": "bar"},
            evaluation_config_id="evaluation_config_id",
            evaluation_dataset_version=0,
            inline_evaluation_config={
                "account_id": "account_id",
                "question_set_id": "question_set_id",
                "auto_evaluation_model": "llama-3-1-70b-instruct",
                "auto_evaluation_parameters": {
                    "batch_size": 1,
                    "temperature": 0,
                },
                "evaluation_type": "llm_auto",
                "studio_project_id": "studio_project_id",
            },
            metric_config={
                "components": [
                    {
                        "name": "name",
                        "type": "rouge",
                        "mappings": {"foo": ["string"]},
                        "params": {"foo": "bar"},
                    }
                ]
            },
            question_id_to_annotation_config={
                "foo": {
                    "annotation_config_type": "generation",
                    "components": [
                        [
                            {
                                "data_loc": ["string"],
                                "label": "label",
                                "optional": True,
                            }
                        ]
                    ],
                    "direction": "col",
                    "llm_prompt": {
                        "template": "template",
                        "variables": [
                            {
                                "data_loc": ["string"],
                                "name": "name",
                                "optional": True,
                            }
                        ],
                    },
                }
            },
            tags={"foo": "bar"},
            type="builder",
        )
        assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_raw_response_create_overload_1(self, client: SGPClient) -> None:
        response = client.evaluations.with_raw_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            application_variant_id="application_variant_id",
            description="description",
            evaluation_dataset_id="evaluation_dataset_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_streaming_response_create_overload_1(self, client: SGPClient) -> None:
        with client.evaluations.with_streaming_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            application_variant_id="application_variant_id",
            description="description",
            evaluation_dataset_id="evaluation_dataset_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_method_create_overload_2(self, client: SGPClient) -> None:
        evaluation = client.evaluations.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            description="description",
            name="name",
        )
        assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: SGPClient) -> None:
        evaluation = client.evaluations.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            description="description",
            name="name",
            annotation_config={
                "components": [
                    [
                        {
                            "data_loc": ["string"],
                            "label": "label",
                            "optional": True,
                        }
                    ]
                ],
                "direction": "col",
                "llm_prompt": {
                    "template": "template",
                    "variables": [
                        {
                            "data_loc": ["string"],
                            "name": "name",
                            "optional": True,
                        }
                    ],
                },
            },
            application_variant_id="application_variant_id",
            evaluation_config={"foo": "bar"},
            evaluation_config_id="evaluation_config_id",
            metric_config={
                "components": [
                    {
                        "name": "name",
                        "type": "rouge",
                        "mappings": {"foo": ["string"]},
                        "params": {"foo": "bar"},
                    }
                ]
            },
            question_id_to_annotation_config={
                "foo": {
                    "annotation_config_type": "generation",
                    "components": [
                        [
                            {
                                "data_loc": ["string"],
                                "label": "label",
                                "optional": True,
                            }
                        ]
                    ],
                    "direction": "col",
                    "llm_prompt": {
                        "template": "template",
                        "variables": [
                            {
                                "data_loc": ["string"],
                                "name": "name",
                                "optional": True,
                            }
                        ],
                    },
                }
            },
            tags={"foo": "bar"},
            type="default",
        )
        assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_raw_response_create_overload_2(self, client: SGPClient) -> None:
        response = client.evaluations.with_raw_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            description="description",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_streaming_response_create_overload_2(self, client: SGPClient) -> None:
        with client.evaluations.with_streaming_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            description="description",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        evaluation = client.evaluations.retrieve(
            evaluation_id="evaluation_id",
        )
        assert_matches_type(EvaluationRetrieveResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGPClient) -> None:
        evaluation = client.evaluations.retrieve(
            evaluation_id="evaluation_id",
            view=["ApplicationSpec"],
        )
        assert_matches_type(EvaluationRetrieveResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.evaluations.with_raw_response.retrieve(
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationRetrieveResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.evaluations.with_streaming_response.retrieve(
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationRetrieveResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.with_raw_response.retrieve(
                evaluation_id="",
            )

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_method_update_overload_1(self, client: SGPClient) -> None:
        evaluation = client.evaluations.update(
            evaluation_id="evaluation_id",
        )
        assert_matches_type(EvaluationUpdateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_method_update_with_all_params_overload_1(self, client: SGPClient) -> None:
        evaluation = client.evaluations.update(
            evaluation_id="evaluation_id",
            annotation_config={
                "components": [
                    [
                        {
                            "data_loc": ["string"],
                            "label": "label",
                            "optional": True,
                        }
                    ]
                ],
                "direction": "col",
                "llm_prompt": {
                    "template": "template",
                    "variables": [
                        {
                            "data_loc": ["string"],
                            "name": "name",
                            "optional": True,
                        }
                    ],
                },
            },
            application_spec_id="application_spec_id",
            application_variant_id="application_variant_id",
            description="description",
            evaluation_config={"foo": "bar"},
            evaluation_config_id="evaluation_config_id",
            evaluation_type="llm_benchmark",
            name="name",
            question_id_to_annotation_config={
                "foo": {
                    "annotation_config_type": "generation",
                    "components": [
                        [
                            {
                                "data_loc": ["string"],
                                "label": "label",
                                "optional": True,
                            }
                        ]
                    ],
                    "direction": "col",
                    "llm_prompt": {
                        "template": "template",
                        "variables": [
                            {
                                "data_loc": ["string"],
                                "name": "name",
                                "optional": True,
                            }
                        ],
                    },
                }
            },
            restore=False,
            tags={"foo": "bar"},
        )
        assert_matches_type(EvaluationUpdateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_raw_response_update_overload_1(self, client: SGPClient) -> None:
        response = client.evaluations.with_raw_response.update(
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationUpdateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_streaming_response_update_overload_1(self, client: SGPClient) -> None:
        with client.evaluations.with_streaming_response.update(
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationUpdateResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_path_params_update_overload_1(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.with_raw_response.update(
                evaluation_id="",
            )

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_method_update_overload_2(self, client: SGPClient) -> None:
        evaluation = client.evaluations.update(
            evaluation_id="evaluation_id",
            restore=True,
        )
        assert_matches_type(EvaluationUpdateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_raw_response_update_overload_2(self, client: SGPClient) -> None:
        response = client.evaluations.with_raw_response.update(
            evaluation_id="evaluation_id",
            restore=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationUpdateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_streaming_response_update_overload_2(self, client: SGPClient) -> None:
        with client.evaluations.with_streaming_response.update(
            evaluation_id="evaluation_id",
            restore=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationUpdateResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_path_params_update_overload_2(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.with_raw_response.update(
                evaluation_id="",
                restore=True,
            )

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        evaluation = client.evaluations.list()
        assert_matches_type(SyncPageResponse[EvaluationListResponse], evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        evaluation = client.evaluations.list(
            account_id="account_id",
            application_spec_id=0,
            include_archived=True,
            limit=1,
            page=1,
            sort_by=["status:asc"],
            view=["ApplicationSpec"],
        )
        assert_matches_type(SyncPageResponse[EvaluationListResponse], evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.evaluations.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(SyncPageResponse[EvaluationListResponse], evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.evaluations.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(SyncPageResponse[EvaluationListResponse], evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        evaluation = client.evaluations.delete(
            "evaluation_id",
        )
        assert_matches_type(GenericDeleteResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.evaluations.with_raw_response.delete(
            "evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(GenericDeleteResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.evaluations.with_streaming_response.delete(
            "evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(GenericDeleteResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_claim_task(self, client: SGPClient) -> None:
        evaluation = client.evaluations.claim_task(
            evaluation_id="evaluation_id",
        )
        assert_matches_type(Optional[Task], evaluation, path=["response"])

    @parametrize
    def test_method_claim_task_with_all_params(self, client: SGPClient) -> None:
        evaluation = client.evaluations.claim_task(
            evaluation_id="evaluation_id",
            task_type="EVALUATION_ANNOTATION",
            skip_current=True,
        )
        assert_matches_type(Optional[Task], evaluation, path=["response"])

    @parametrize
    def test_raw_response_claim_task(self, client: SGPClient) -> None:
        response = client.evaluations.with_raw_response.claim_task(
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(Optional[Task], evaluation, path=["response"])

    @parametrize
    def test_streaming_response_claim_task(self, client: SGPClient) -> None:
        with client.evaluations.with_streaming_response.claim_task(
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(Optional[Task], evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_claim_task(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.with_raw_response.claim_task(
                evaluation_id="",
            )


class TestAsyncEvaluations:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            application_variant_id="application_variant_id",
            description="description",
            evaluation_dataset_id="evaluation_dataset_id",
            name="name",
        )
        assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            application_variant_id="application_variant_id",
            description="description",
            evaluation_dataset_id="evaluation_dataset_id",
            name="name",
            annotation_config={
                "components": [
                    [
                        {
                            "data_loc": ["string"],
                            "label": "label",
                            "optional": True,
                        }
                    ]
                ],
                "direction": "col",
                "llm_prompt": {
                    "template": "template",
                    "variables": [
                        {
                            "data_loc": ["string"],
                            "name": "name",
                            "optional": True,
                        }
                    ],
                },
            },
            application_test_case_output_group_id="application_test_case_output_group_id",
            evaluation_config={"foo": "bar"},
            evaluation_config_id="evaluation_config_id",
            evaluation_dataset_version=0,
            inline_evaluation_config={
                "account_id": "account_id",
                "question_set_id": "question_set_id",
                "auto_evaluation_model": "llama-3-1-70b-instruct",
                "auto_evaluation_parameters": {
                    "batch_size": 1,
                    "temperature": 0,
                },
                "evaluation_type": "llm_auto",
                "studio_project_id": "studio_project_id",
            },
            metric_config={
                "components": [
                    {
                        "name": "name",
                        "type": "rouge",
                        "mappings": {"foo": ["string"]},
                        "params": {"foo": "bar"},
                    }
                ]
            },
            question_id_to_annotation_config={
                "foo": {
                    "annotation_config_type": "generation",
                    "components": [
                        [
                            {
                                "data_loc": ["string"],
                                "label": "label",
                                "optional": True,
                            }
                        ]
                    ],
                    "direction": "col",
                    "llm_prompt": {
                        "template": "template",
                        "variables": [
                            {
                                "data_loc": ["string"],
                                "name": "name",
                                "optional": True,
                            }
                        ],
                    },
                }
            },
            tags={"foo": "bar"},
            type="builder",
        )
        assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.with_raw_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            application_variant_id="application_variant_id",
            description="description",
            evaluation_dataset_id="evaluation_dataset_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.with_streaming_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            application_variant_id="application_variant_id",
            description="description",
            evaluation_dataset_id="evaluation_dataset_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            description="description",
            name="name",
        )
        assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            description="description",
            name="name",
            annotation_config={
                "components": [
                    [
                        {
                            "data_loc": ["string"],
                            "label": "label",
                            "optional": True,
                        }
                    ]
                ],
                "direction": "col",
                "llm_prompt": {
                    "template": "template",
                    "variables": [
                        {
                            "data_loc": ["string"],
                            "name": "name",
                            "optional": True,
                        }
                    ],
                },
            },
            application_variant_id="application_variant_id",
            evaluation_config={"foo": "bar"},
            evaluation_config_id="evaluation_config_id",
            metric_config={
                "components": [
                    {
                        "name": "name",
                        "type": "rouge",
                        "mappings": {"foo": ["string"]},
                        "params": {"foo": "bar"},
                    }
                ]
            },
            question_id_to_annotation_config={
                "foo": {
                    "annotation_config_type": "generation",
                    "components": [
                        [
                            {
                                "data_loc": ["string"],
                                "label": "label",
                                "optional": True,
                            }
                        ]
                    ],
                    "direction": "col",
                    "llm_prompt": {
                        "template": "template",
                        "variables": [
                            {
                                "data_loc": ["string"],
                                "name": "name",
                                "optional": True,
                            }
                        ],
                    },
                }
            },
            tags={"foo": "bar"},
            type="default",
        )
        assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.with_raw_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            description="description",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.with_streaming_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            description="description",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.retrieve(
            evaluation_id="evaluation_id",
        )
        assert_matches_type(EvaluationRetrieveResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.retrieve(
            evaluation_id="evaluation_id",
            view=["ApplicationSpec"],
        )
        assert_matches_type(EvaluationRetrieveResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.with_raw_response.retrieve(
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationRetrieveResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.with_streaming_response.retrieve(
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationRetrieveResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.with_raw_response.retrieve(
                evaluation_id="",
            )

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_method_update_overload_1(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.update(
            evaluation_id="evaluation_id",
        )
        assert_matches_type(EvaluationUpdateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_method_update_with_all_params_overload_1(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.update(
            evaluation_id="evaluation_id",
            annotation_config={
                "components": [
                    [
                        {
                            "data_loc": ["string"],
                            "label": "label",
                            "optional": True,
                        }
                    ]
                ],
                "direction": "col",
                "llm_prompt": {
                    "template": "template",
                    "variables": [
                        {
                            "data_loc": ["string"],
                            "name": "name",
                            "optional": True,
                        }
                    ],
                },
            },
            application_spec_id="application_spec_id",
            application_variant_id="application_variant_id",
            description="description",
            evaluation_config={"foo": "bar"},
            evaluation_config_id="evaluation_config_id",
            evaluation_type="llm_benchmark",
            name="name",
            question_id_to_annotation_config={
                "foo": {
                    "annotation_config_type": "generation",
                    "components": [
                        [
                            {
                                "data_loc": ["string"],
                                "label": "label",
                                "optional": True,
                            }
                        ]
                    ],
                    "direction": "col",
                    "llm_prompt": {
                        "template": "template",
                        "variables": [
                            {
                                "data_loc": ["string"],
                                "name": "name",
                                "optional": True,
                            }
                        ],
                    },
                }
            },
            restore=False,
            tags={"foo": "bar"},
        )
        assert_matches_type(EvaluationUpdateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_raw_response_update_overload_1(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.with_raw_response.update(
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationUpdateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_streaming_response_update_overload_1(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.with_streaming_response.update(
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationUpdateResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_path_params_update_overload_1(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.with_raw_response.update(
                evaluation_id="",
            )

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_method_update_overload_2(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.update(
            evaluation_id="evaluation_id",
            restore=True,
        )
        assert_matches_type(EvaluationUpdateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_raw_response_update_overload_2(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.with_raw_response.update(
            evaluation_id="evaluation_id",
            restore=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationUpdateResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_streaming_response_update_overload_2(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.with_streaming_response.update(
            evaluation_id="evaluation_id",
            restore=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationUpdateResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_path_params_update_overload_2(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.with_raw_response.update(
                evaluation_id="",
                restore=True,
            )

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.list()
        assert_matches_type(AsyncPageResponse[EvaluationListResponse], evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.list(
            account_id="account_id",
            application_spec_id=0,
            include_archived=True,
            limit=1,
            page=1,
            sort_by=["status:asc"],
            view=["ApplicationSpec"],
        )
        assert_matches_type(AsyncPageResponse[EvaluationListResponse], evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(AsyncPageResponse[EvaluationListResponse], evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(AsyncPageResponse[EvaluationListResponse], evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.delete(
            "evaluation_id",
        )
        assert_matches_type(GenericDeleteResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.with_raw_response.delete(
            "evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(GenericDeleteResponse, evaluation, path=["response"])

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.with_streaming_response.delete(
            "evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(GenericDeleteResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="question_id_to_annotation_config response body fails validation")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_claim_task(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.claim_task(
            evaluation_id="evaluation_id",
        )
        assert_matches_type(Optional[Task], evaluation, path=["response"])

    @parametrize
    async def test_method_claim_task_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation = await async_client.evaluations.claim_task(
            evaluation_id="evaluation_id",
            task_type="EVALUATION_ANNOTATION",
            skip_current=True,
        )
        assert_matches_type(Optional[Task], evaluation, path=["response"])

    @parametrize
    async def test_raw_response_claim_task(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluations.with_raw_response.claim_task(
            evaluation_id="evaluation_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(Optional[Task], evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_claim_task(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluations.with_streaming_response.claim_task(
            evaluation_id="evaluation_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(Optional[Task], evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_claim_task(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.with_raw_response.claim_task(
                evaluation_id="",
            )
