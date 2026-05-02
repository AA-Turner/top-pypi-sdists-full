# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import (
    ApplicationVariantPatchResponse,
    ApplicationVariantCreateResponse,
    ApplicationVariantRetrieveResponse,
)
from scale_gp._utils import parse_datetime
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.shared import GenericDeleteResponse
from scale_gp.types.paginated_application_variants import Item

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestApplicationVariants:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create_overload_1(self, client: SGPClient) -> None:
        application_variant = client.application_variants.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={
                "edges": [
                    {
                        "from_field": "from_field",
                        "from_node": "from_node",
                        "to_field": "to_field",
                        "to_node": "to_node",
                    }
                ],
                "nodes": [
                    {
                        "id": "id",
                        "application_node_schema_id": "text_input_schema",
                    }
                ],
            },
            name="name",
            version="V0",
        )
        assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: SGPClient) -> None:
        application_variant = client.application_variants.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={
                "edges": [
                    {
                        "from_field": "from_field",
                        "from_node": "from_node",
                        "to_field": "to_field",
                        "to_node": "to_node",
                    }
                ],
                "nodes": [
                    {
                        "id": "id",
                        "application_node_schema_id": "text_input_schema",
                        "configuration": {"foo": {"value": {}}},
                    }
                ],
                "metadata": {"foo": "bar"},
            },
            name="name",
            version="V0",
            description="description",
            draft=True,
            published_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

    @parametrize
    def test_raw_response_create_overload_1(self, client: SGPClient) -> None:
        response = client.application_variants.with_raw_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={
                "edges": [
                    {
                        "from_field": "from_field",
                        "from_node": "from_node",
                        "to_field": "to_field",
                        "to_node": "to_node",
                    }
                ],
                "nodes": [
                    {
                        "id": "id",
                        "application_node_schema_id": "text_input_schema",
                    }
                ],
            },
            name="name",
            version="V0",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = response.parse()
        assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_1(self, client: SGPClient) -> None:
        with client.application_variants.with_streaming_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={
                "edges": [
                    {
                        "from_field": "from_field",
                        "from_node": "from_node",
                        "to_field": "to_field",
                        "to_node": "to_node",
                    }
                ],
                "nodes": [
                    {
                        "id": "id",
                        "application_node_schema_id": "text_input_schema",
                    }
                ],
            },
            name="name",
            version="V0",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = response.parse()
            assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_overload_2(self, client: SGPClient) -> None:
        application_variant = client.application_variants.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={
                "params": {},
                "type": "WORKFLOW",
            },
            name="name",
            version="AGENTS_SERVICE",
        )
        assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: SGPClient) -> None:
        application_variant = client.application_variants.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={
                "params": {},
                "type": "WORKFLOW",
                "agent_service_errors": ["string"],
                "graph": {
                    "edges": [
                        {
                            "from_node": "from_node",
                            "to_node": "to_node",
                        }
                    ],
                    "nodes": [
                        {
                            "id": "id",
                            "name": "name",
                            "type": "type",
                            "config": {"foo": "bar"},
                            "edges": [
                                {
                                    "from_node": "from_node",
                                    "to_node": "to_node",
                                }
                            ],
                            "nodes": [],
                            "operation_type": "TEXT_INPUT",
                        }
                    ],
                },
                "inputs": [
                    {
                        "name": "name",
                        "type": "ShortText",
                        "default": "default",
                        "description": "description",
                        "examples": ["string"],
                        "required": True,
                        "title": "title",
                        "value_constraint": {
                            "potential_values": ["string"],
                            "selection_constraint_type": "single",
                            "value_type": "ShortText",
                            "max_items": 0,
                            "min_items": 0,
                        },
                    }
                ],
                "inputs_by_node": {
                    "foo": [
                        {
                            "name": "name",
                            "type": "ShortText",
                            "default": "default",
                            "description": "description",
                            "examples": ["string"],
                            "required": True,
                            "title": "title",
                            "value_constraint": {
                                "potential_values": ["string"],
                                "selection_constraint_type": "single",
                                "value_type": "ShortText",
                                "max_items": 0,
                                "min_items": 0,
                            },
                        }
                    ]
                },
                "metadata": {"foo": "bar"},
                "raw_configuration": "raw_configuration",
            },
            name="name",
            version="AGENTS_SERVICE",
            description="description",
            draft=True,
            published_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

    @parametrize
    def test_raw_response_create_overload_2(self, client: SGPClient) -> None:
        response = client.application_variants.with_raw_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={
                "params": {},
                "type": "WORKFLOW",
            },
            name="name",
            version="AGENTS_SERVICE",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = response.parse()
        assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_2(self, client: SGPClient) -> None:
        with client.application_variants.with_streaming_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={
                "params": {},
                "type": "WORKFLOW",
            },
            name="name",
            version="AGENTS_SERVICE",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = response.parse()
            assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_overload_3(self, client: SGPClient) -> None:
        application_variant = client.application_variants.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={},
            name="name",
            version="OFFLINE",
        )
        assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_3(self, client: SGPClient) -> None:
        application_variant = client.application_variants.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={"metadata": {"foo": "bar"}},
            name="name",
            version="OFFLINE",
            description="description",
            draft=True,
            published_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

    @parametrize
    def test_raw_response_create_overload_3(self, client: SGPClient) -> None:
        response = client.application_variants.with_raw_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={},
            name="name",
            version="OFFLINE",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = response.parse()
        assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_3(self, client: SGPClient) -> None:
        with client.application_variants.with_streaming_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={},
            name="name",
            version="OFFLINE",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = response.parse()
            assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        application_variant = client.application_variants.retrieve(
            "application_variant_id",
        )
        assert_matches_type(ApplicationVariantRetrieveResponse, application_variant, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.application_variants.with_raw_response.retrieve(
            "application_variant_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = response.parse()
        assert_matches_type(ApplicationVariantRetrieveResponse, application_variant, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.application_variants.with_streaming_response.retrieve(
            "application_variant_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = response.parse()
            assert_matches_type(ApplicationVariantRetrieveResponse, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            client.application_variants.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        application_variant = client.application_variants.list()
        assert_matches_type(SyncPageResponse[Item], application_variant, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        application_variant = client.application_variants.list(
            account_id="account_id",
            application_spec_id=0,
            limit=1,
            page=1,
        )
        assert_matches_type(SyncPageResponse[Item], application_variant, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.application_variants.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = response.parse()
        assert_matches_type(SyncPageResponse[Item], application_variant, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.application_variants.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = response.parse()
            assert_matches_type(SyncPageResponse[Item], application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        application_variant = client.application_variants.delete(
            "application_variant_id",
        )
        assert_matches_type(GenericDeleteResponse, application_variant, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.application_variants.with_raw_response.delete(
            "application_variant_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = response.parse()
        assert_matches_type(GenericDeleteResponse, application_variant, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.application_variants.with_streaming_response.delete(
            "application_variant_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = response.parse()
            assert_matches_type(GenericDeleteResponse, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            client.application_variants.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_patch(self, client: SGPClient) -> None:
        application_variant = client.application_variants.patch(
            application_variant_id="application_variant_id",
        )
        assert_matches_type(ApplicationVariantPatchResponse, application_variant, path=["response"])

    @parametrize
    def test_method_patch_with_all_params(self, client: SGPClient) -> None:
        application_variant = client.application_variants.patch(
            application_variant_id="application_variant_id",
            configuration={
                "metadata": {"foo": "bar"},
                "params": {},
                "raw_configuration": "raw_configuration",
                "type": "WORKFLOW",
            },
            description="description",
            name="name",
        )
        assert_matches_type(ApplicationVariantPatchResponse, application_variant, path=["response"])

    @parametrize
    def test_raw_response_patch(self, client: SGPClient) -> None:
        response = client.application_variants.with_raw_response.patch(
            application_variant_id="application_variant_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = response.parse()
        assert_matches_type(ApplicationVariantPatchResponse, application_variant, path=["response"])

    @parametrize
    def test_streaming_response_patch(self, client: SGPClient) -> None:
        with client.application_variants.with_streaming_response.patch(
            application_variant_id="application_variant_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = response.parse()
            assert_matches_type(ApplicationVariantPatchResponse, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_patch(self, client: SGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            client.application_variants.with_raw_response.patch(
                application_variant_id="",
            )

    @pytest.mark.skip(reason="additional_properties is an object")
    @parametrize
    def test_method_process(self, client: SGPClient) -> None:
        application_variant = client.application_variants.process(
            application_variant_id="application_variant_id",
            inputs={"foo": "bar"},
        )
        assert_matches_type(object, application_variant, path=["response"])

    @pytest.mark.skip(reason="additional_properties is an object")
    @parametrize
    def test_method_process_with_all_params(self, client: SGPClient) -> None:
        application_variant = client.application_variants.process(
            application_variant_id="application_variant_id",
            inputs={"foo": "bar"},
            history=[
                {
                    "request": "request",
                    "response": "response",
                    "session_data": {"foo": "bar"},
                }
            ],
            operation_metadata={"foo": "bar"},
            overrides={
                "concurrent": True,
                "initial_state": {
                    "current_node": "current_node",
                    "state": {"foo": "bar"},
                },
                "partial_trace": [
                    {
                        "duration_ms": 0,
                        "node_id": "node_id",
                        "operation_input": "operation_input",
                        "operation_output": "operation_output",
                        "operation_type": "operation_type",
                        "start_timestamp": "start_timestamp",
                        "workflow_id": "workflow_id",
                        "operation_metadata": {"foo": "bar"},
                    }
                ],
                "return_span": True,
                "use_channels": True,
            },
            stream=True,
        )
        assert_matches_type(object, application_variant, path=["response"])

    @pytest.mark.skip(reason="additional_properties is an object")
    @parametrize
    def test_raw_response_process(self, client: SGPClient) -> None:
        response = client.application_variants.with_raw_response.process(
            application_variant_id="application_variant_id",
            inputs={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = response.parse()
        assert_matches_type(object, application_variant, path=["response"])

    @pytest.mark.skip(reason="additional_properties is an object")
    @parametrize
    def test_streaming_response_process(self, client: SGPClient) -> None:
        with client.application_variants.with_streaming_response.process(
            application_variant_id="application_variant_id",
            inputs={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = response.parse()
            assert_matches_type(object, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="additional_properties is an object")
    @parametrize
    def test_path_params_process(self, client: SGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            client.application_variants.with_raw_response.process(
                application_variant_id="",
                inputs={"foo": "bar"},
            )


class TestAsyncApplicationVariants:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        application_variant = await async_client.application_variants.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={
                "edges": [
                    {
                        "from_field": "from_field",
                        "from_node": "from_node",
                        "to_field": "to_field",
                        "to_node": "to_node",
                    }
                ],
                "nodes": [
                    {
                        "id": "id",
                        "application_node_schema_id": "text_input_schema",
                    }
                ],
            },
            name="name",
            version="V0",
        )
        assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncSGPClient) -> None:
        application_variant = await async_client.application_variants.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={
                "edges": [
                    {
                        "from_field": "from_field",
                        "from_node": "from_node",
                        "to_field": "to_field",
                        "to_node": "to_node",
                    }
                ],
                "nodes": [
                    {
                        "id": "id",
                        "application_node_schema_id": "text_input_schema",
                        "configuration": {"foo": {"value": {}}},
                    }
                ],
                "metadata": {"foo": "bar"},
            },
            name="name",
            version="V0",
            description="description",
            draft=True,
            published_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_variants.with_raw_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={
                "edges": [
                    {
                        "from_field": "from_field",
                        "from_node": "from_node",
                        "to_field": "to_field",
                        "to_node": "to_node",
                    }
                ],
                "nodes": [
                    {
                        "id": "id",
                        "application_node_schema_id": "text_input_schema",
                    }
                ],
            },
            name="name",
            version="V0",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = await response.parse()
        assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_variants.with_streaming_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={
                "edges": [
                    {
                        "from_field": "from_field",
                        "from_node": "from_node",
                        "to_field": "to_field",
                        "to_node": "to_node",
                    }
                ],
                "nodes": [
                    {
                        "id": "id",
                        "application_node_schema_id": "text_input_schema",
                    }
                ],
            },
            name="name",
            version="V0",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = await response.parse()
            assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        application_variant = await async_client.application_variants.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={
                "params": {},
                "type": "WORKFLOW",
            },
            name="name",
            version="AGENTS_SERVICE",
        )
        assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncSGPClient) -> None:
        application_variant = await async_client.application_variants.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={
                "params": {},
                "type": "WORKFLOW",
                "agent_service_errors": ["string"],
                "graph": {
                    "edges": [
                        {
                            "from_node": "from_node",
                            "to_node": "to_node",
                        }
                    ],
                    "nodes": [
                        {
                            "id": "id",
                            "name": "name",
                            "type": "type",
                            "config": {"foo": "bar"},
                            "edges": [
                                {
                                    "from_node": "from_node",
                                    "to_node": "to_node",
                                }
                            ],
                            "nodes": [],
                            "operation_type": "TEXT_INPUT",
                        }
                    ],
                },
                "inputs": [
                    {
                        "name": "name",
                        "type": "ShortText",
                        "default": "default",
                        "description": "description",
                        "examples": ["string"],
                        "required": True,
                        "title": "title",
                        "value_constraint": {
                            "potential_values": ["string"],
                            "selection_constraint_type": "single",
                            "value_type": "ShortText",
                            "max_items": 0,
                            "min_items": 0,
                        },
                    }
                ],
                "inputs_by_node": {
                    "foo": [
                        {
                            "name": "name",
                            "type": "ShortText",
                            "default": "default",
                            "description": "description",
                            "examples": ["string"],
                            "required": True,
                            "title": "title",
                            "value_constraint": {
                                "potential_values": ["string"],
                                "selection_constraint_type": "single",
                                "value_type": "ShortText",
                                "max_items": 0,
                                "min_items": 0,
                            },
                        }
                    ]
                },
                "metadata": {"foo": "bar"},
                "raw_configuration": "raw_configuration",
            },
            name="name",
            version="AGENTS_SERVICE",
            description="description",
            draft=True,
            published_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_variants.with_raw_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={
                "params": {},
                "type": "WORKFLOW",
            },
            name="name",
            version="AGENTS_SERVICE",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = await response.parse()
        assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_variants.with_streaming_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={
                "params": {},
                "type": "WORKFLOW",
            },
            name="name",
            version="AGENTS_SERVICE",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = await response.parse()
            assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_overload_3(self, async_client: AsyncSGPClient) -> None:
        application_variant = await async_client.application_variants.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={},
            name="name",
            version="OFFLINE",
        )
        assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_3(self, async_client: AsyncSGPClient) -> None:
        application_variant = await async_client.application_variants.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={"metadata": {"foo": "bar"}},
            name="name",
            version="OFFLINE",
            description="description",
            draft=True,
            published_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_3(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_variants.with_raw_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={},
            name="name",
            version="OFFLINE",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = await response.parse()
        assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_3(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_variants.with_streaming_response.create(
            account_id="account_id",
            application_spec_id="application_spec_id",
            configuration={},
            name="name",
            version="OFFLINE",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = await response.parse()
            assert_matches_type(ApplicationVariantCreateResponse, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        application_variant = await async_client.application_variants.retrieve(
            "application_variant_id",
        )
        assert_matches_type(ApplicationVariantRetrieveResponse, application_variant, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_variants.with_raw_response.retrieve(
            "application_variant_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = await response.parse()
        assert_matches_type(ApplicationVariantRetrieveResponse, application_variant, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_variants.with_streaming_response.retrieve(
            "application_variant_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = await response.parse()
            assert_matches_type(ApplicationVariantRetrieveResponse, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            await async_client.application_variants.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        application_variant = await async_client.application_variants.list()
        assert_matches_type(AsyncPageResponse[Item], application_variant, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        application_variant = await async_client.application_variants.list(
            account_id="account_id",
            application_spec_id=0,
            limit=1,
            page=1,
        )
        assert_matches_type(AsyncPageResponse[Item], application_variant, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_variants.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = await response.parse()
        assert_matches_type(AsyncPageResponse[Item], application_variant, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_variants.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = await response.parse()
            assert_matches_type(AsyncPageResponse[Item], application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        application_variant = await async_client.application_variants.delete(
            "application_variant_id",
        )
        assert_matches_type(GenericDeleteResponse, application_variant, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_variants.with_raw_response.delete(
            "application_variant_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = await response.parse()
        assert_matches_type(GenericDeleteResponse, application_variant, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_variants.with_streaming_response.delete(
            "application_variant_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = await response.parse()
            assert_matches_type(GenericDeleteResponse, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            await async_client.application_variants.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_patch(self, async_client: AsyncSGPClient) -> None:
        application_variant = await async_client.application_variants.patch(
            application_variant_id="application_variant_id",
        )
        assert_matches_type(ApplicationVariantPatchResponse, application_variant, path=["response"])

    @parametrize
    async def test_method_patch_with_all_params(self, async_client: AsyncSGPClient) -> None:
        application_variant = await async_client.application_variants.patch(
            application_variant_id="application_variant_id",
            configuration={
                "metadata": {"foo": "bar"},
                "params": {},
                "raw_configuration": "raw_configuration",
                "type": "WORKFLOW",
            },
            description="description",
            name="name",
        )
        assert_matches_type(ApplicationVariantPatchResponse, application_variant, path=["response"])

    @parametrize
    async def test_raw_response_patch(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_variants.with_raw_response.patch(
            application_variant_id="application_variant_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = await response.parse()
        assert_matches_type(ApplicationVariantPatchResponse, application_variant, path=["response"])

    @parametrize
    async def test_streaming_response_patch(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_variants.with_streaming_response.patch(
            application_variant_id="application_variant_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = await response.parse()
            assert_matches_type(ApplicationVariantPatchResponse, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_patch(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            await async_client.application_variants.with_raw_response.patch(
                application_variant_id="",
            )

    @pytest.mark.skip(reason="additional_properties is an object")
    @parametrize
    async def test_method_process(self, async_client: AsyncSGPClient) -> None:
        application_variant = await async_client.application_variants.process(
            application_variant_id="application_variant_id",
            inputs={"foo": "bar"},
        )
        assert_matches_type(object, application_variant, path=["response"])

    @pytest.mark.skip(reason="additional_properties is an object")
    @parametrize
    async def test_method_process_with_all_params(self, async_client: AsyncSGPClient) -> None:
        application_variant = await async_client.application_variants.process(
            application_variant_id="application_variant_id",
            inputs={"foo": "bar"},
            history=[
                {
                    "request": "request",
                    "response": "response",
                    "session_data": {"foo": "bar"},
                }
            ],
            operation_metadata={"foo": "bar"},
            overrides={
                "concurrent": True,
                "initial_state": {
                    "current_node": "current_node",
                    "state": {"foo": "bar"},
                },
                "partial_trace": [
                    {
                        "duration_ms": 0,
                        "node_id": "node_id",
                        "operation_input": "operation_input",
                        "operation_output": "operation_output",
                        "operation_type": "operation_type",
                        "start_timestamp": "start_timestamp",
                        "workflow_id": "workflow_id",
                        "operation_metadata": {"foo": "bar"},
                    }
                ],
                "return_span": True,
                "use_channels": True,
            },
            stream=True,
        )
        assert_matches_type(object, application_variant, path=["response"])

    @pytest.mark.skip(reason="additional_properties is an object")
    @parametrize
    async def test_raw_response_process(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_variants.with_raw_response.process(
            application_variant_id="application_variant_id",
            inputs={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_variant = await response.parse()
        assert_matches_type(object, application_variant, path=["response"])

    @pytest.mark.skip(reason="additional_properties is an object")
    @parametrize
    async def test_streaming_response_process(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_variants.with_streaming_response.process(
            application_variant_id="application_variant_id",
            inputs={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_variant = await response.parse()
            assert_matches_type(object, application_variant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="additional_properties is an object")
    @parametrize
    async def test_path_params_process(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            await async_client.application_variants.with_raw_response.process(
                application_variant_id="",
                inputs={"foo": "bar"},
            )
