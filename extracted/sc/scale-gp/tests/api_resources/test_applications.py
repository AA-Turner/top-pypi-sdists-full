# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import (
    ApplicationUploadFilesResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestApplications:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="additional_properties is an object")
    @parametrize
    def test_method_process(self, client: SGPClient) -> None:
        application = client.applications.process(
            edges=[
                {
                    "from_field": "from_field",
                    "from_node": "from_node",
                    "to_field": "to_field",
                    "to_node": "to_node",
                }
            ],
            inputs={"foo": {"foo": "bar"}},
            nodes=[
                {
                    "id": "id",
                    "application_node_schema_id": "text_input_schema",
                }
            ],
            version="V0",
        )
        assert_matches_type(object, application, path=["response"])

    @pytest.mark.skip(reason="additional_properties is an object")
    @parametrize
    def test_method_process_with_all_params(self, client: SGPClient) -> None:
        application = client.applications.process(
            edges=[
                {
                    "from_field": "from_field",
                    "from_node": "from_node",
                    "to_field": "to_field",
                    "to_node": "to_node",
                }
            ],
            inputs={"foo": {"foo": "bar"}},
            nodes=[
                {
                    "id": "id",
                    "application_node_schema_id": "text_input_schema",
                    "configuration": {"foo": {"value": {}}},
                }
            ],
            version="V0",
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
        assert_matches_type(object, application, path=["response"])

    @pytest.mark.skip(reason="additional_properties is an object")
    @parametrize
    def test_raw_response_process(self, client: SGPClient) -> None:
        response = client.applications.with_raw_response.process(
            edges=[
                {
                    "from_field": "from_field",
                    "from_node": "from_node",
                    "to_field": "to_field",
                    "to_node": "to_node",
                }
            ],
            inputs={"foo": {"foo": "bar"}},
            nodes=[
                {
                    "id": "id",
                    "application_node_schema_id": "text_input_schema",
                }
            ],
            version="V0",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application = response.parse()
        assert_matches_type(object, application, path=["response"])

    @pytest.mark.skip(reason="additional_properties is an object")
    @parametrize
    def test_streaming_response_process(self, client: SGPClient) -> None:
        with client.applications.with_streaming_response.process(
            edges=[
                {
                    "from_field": "from_field",
                    "from_node": "from_node",
                    "to_field": "to_field",
                    "to_node": "to_node",
                }
            ],
            inputs={"foo": {"foo": "bar"}},
            nodes=[
                {
                    "id": "id",
                    "application_node_schema_id": "text_input_schema",
                }
            ],
            version="V0",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application = response.parse()
            assert_matches_type(object, application, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    def test_method_upload_files(self, client: SGPClient) -> None:
        application = client.applications.upload_files(
            files=["string"],
        )
        assert_matches_type(ApplicationUploadFilesResponse, application, path=["response"])

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    def test_method_upload_files_with_all_params(self, client: SGPClient) -> None:
        application = client.applications.upload_files(
            files=["string"],
            account_id="account_id",
        )
        assert_matches_type(ApplicationUploadFilesResponse, application, path=["response"])

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    def test_raw_response_upload_files(self, client: SGPClient) -> None:
        response = client.applications.with_raw_response.upload_files(
            files=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application = response.parse()
        assert_matches_type(ApplicationUploadFilesResponse, application, path=["response"])

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    def test_streaming_response_upload_files(self, client: SGPClient) -> None:
        with client.applications.with_streaming_response.upload_files(
            files=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application = response.parse()
            assert_matches_type(ApplicationUploadFilesResponse, application, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_validate(self, client: SGPClient) -> None:
        application = client.applications.validate(
            edges=[
                {
                    "from_field": "from_field",
                    "from_node": "from_node",
                    "to_field": "to_field",
                    "to_node": "to_node",
                }
            ],
            nodes=[
                {
                    "id": "id",
                    "application_node_schema_id": "text_input_schema",
                }
            ],
            version="V0",
        )
        assert_matches_type(object, application, path=["response"])

    @parametrize
    def test_method_validate_with_all_params(self, client: SGPClient) -> None:
        application = client.applications.validate(
            edges=[
                {
                    "from_field": "from_field",
                    "from_node": "from_node",
                    "to_field": "to_field",
                    "to_node": "to_node",
                }
            ],
            nodes=[
                {
                    "id": "id",
                    "application_node_schema_id": "text_input_schema",
                    "configuration": {"foo": {"value": {}}},
                }
            ],
            version="V0",
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
        )
        assert_matches_type(object, application, path=["response"])

    @parametrize
    def test_raw_response_validate(self, client: SGPClient) -> None:
        response = client.applications.with_raw_response.validate(
            edges=[
                {
                    "from_field": "from_field",
                    "from_node": "from_node",
                    "to_field": "to_field",
                    "to_node": "to_node",
                }
            ],
            nodes=[
                {
                    "id": "id",
                    "application_node_schema_id": "text_input_schema",
                }
            ],
            version="V0",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application = response.parse()
        assert_matches_type(object, application, path=["response"])

    @parametrize
    def test_streaming_response_validate(self, client: SGPClient) -> None:
        with client.applications.with_streaming_response.validate(
            edges=[
                {
                    "from_field": "from_field",
                    "from_node": "from_node",
                    "to_field": "to_field",
                    "to_node": "to_node",
                }
            ],
            nodes=[
                {
                    "id": "id",
                    "application_node_schema_id": "text_input_schema",
                }
            ],
            version="V0",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application = response.parse()
            assert_matches_type(object, application, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncApplications:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="additional_properties is an object")
    @parametrize
    async def test_method_process(self, async_client: AsyncSGPClient) -> None:
        application = await async_client.applications.process(
            edges=[
                {
                    "from_field": "from_field",
                    "from_node": "from_node",
                    "to_field": "to_field",
                    "to_node": "to_node",
                }
            ],
            inputs={"foo": {"foo": "bar"}},
            nodes=[
                {
                    "id": "id",
                    "application_node_schema_id": "text_input_schema",
                }
            ],
            version="V0",
        )
        assert_matches_type(object, application, path=["response"])

    @pytest.mark.skip(reason="additional_properties is an object")
    @parametrize
    async def test_method_process_with_all_params(self, async_client: AsyncSGPClient) -> None:
        application = await async_client.applications.process(
            edges=[
                {
                    "from_field": "from_field",
                    "from_node": "from_node",
                    "to_field": "to_field",
                    "to_node": "to_node",
                }
            ],
            inputs={"foo": {"foo": "bar"}},
            nodes=[
                {
                    "id": "id",
                    "application_node_schema_id": "text_input_schema",
                    "configuration": {"foo": {"value": {}}},
                }
            ],
            version="V0",
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
        assert_matches_type(object, application, path=["response"])

    @pytest.mark.skip(reason="additional_properties is an object")
    @parametrize
    async def test_raw_response_process(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.applications.with_raw_response.process(
            edges=[
                {
                    "from_field": "from_field",
                    "from_node": "from_node",
                    "to_field": "to_field",
                    "to_node": "to_node",
                }
            ],
            inputs={"foo": {"foo": "bar"}},
            nodes=[
                {
                    "id": "id",
                    "application_node_schema_id": "text_input_schema",
                }
            ],
            version="V0",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application = await response.parse()
        assert_matches_type(object, application, path=["response"])

    @pytest.mark.skip(reason="additional_properties is an object")
    @parametrize
    async def test_streaming_response_process(self, async_client: AsyncSGPClient) -> None:
        async with async_client.applications.with_streaming_response.process(
            edges=[
                {
                    "from_field": "from_field",
                    "from_node": "from_node",
                    "to_field": "to_field",
                    "to_node": "to_node",
                }
            ],
            inputs={"foo": {"foo": "bar"}},
            nodes=[
                {
                    "id": "id",
                    "application_node_schema_id": "text_input_schema",
                }
            ],
            version="V0",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application = await response.parse()
            assert_matches_type(object, application, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    async def test_method_upload_files(self, async_client: AsyncSGPClient) -> None:
        application = await async_client.applications.upload_files(
            files=["string"],
        )
        assert_matches_type(ApplicationUploadFilesResponse, application, path=["response"])

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    async def test_method_upload_files_with_all_params(self, async_client: AsyncSGPClient) -> None:
        application = await async_client.applications.upload_files(
            files=["string"],
            account_id="account_id",
        )
        assert_matches_type(ApplicationUploadFilesResponse, application, path=["response"])

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    async def test_raw_response_upload_files(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.applications.with_raw_response.upload_files(
            files=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application = await response.parse()
        assert_matches_type(ApplicationUploadFilesResponse, application, path=["response"])

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    async def test_streaming_response_upload_files(self, async_client: AsyncSGPClient) -> None:
        async with async_client.applications.with_streaming_response.upload_files(
            files=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application = await response.parse()
            assert_matches_type(ApplicationUploadFilesResponse, application, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_validate(self, async_client: AsyncSGPClient) -> None:
        application = await async_client.applications.validate(
            edges=[
                {
                    "from_field": "from_field",
                    "from_node": "from_node",
                    "to_field": "to_field",
                    "to_node": "to_node",
                }
            ],
            nodes=[
                {
                    "id": "id",
                    "application_node_schema_id": "text_input_schema",
                }
            ],
            version="V0",
        )
        assert_matches_type(object, application, path=["response"])

    @parametrize
    async def test_method_validate_with_all_params(self, async_client: AsyncSGPClient) -> None:
        application = await async_client.applications.validate(
            edges=[
                {
                    "from_field": "from_field",
                    "from_node": "from_node",
                    "to_field": "to_field",
                    "to_node": "to_node",
                }
            ],
            nodes=[
                {
                    "id": "id",
                    "application_node_schema_id": "text_input_schema",
                    "configuration": {"foo": {"value": {}}},
                }
            ],
            version="V0",
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
        )
        assert_matches_type(object, application, path=["response"])

    @parametrize
    async def test_raw_response_validate(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.applications.with_raw_response.validate(
            edges=[
                {
                    "from_field": "from_field",
                    "from_node": "from_node",
                    "to_field": "to_field",
                    "to_node": "to_node",
                }
            ],
            nodes=[
                {
                    "id": "id",
                    "application_node_schema_id": "text_input_schema",
                }
            ],
            version="V0",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application = await response.parse()
        assert_matches_type(object, application, path=["response"])

    @parametrize
    async def test_streaming_response_validate(self, async_client: AsyncSGPClient) -> None:
        async with async_client.applications.with_streaming_response.validate(
            edges=[
                {
                    "from_field": "from_field",
                    "from_node": "from_node",
                    "to_field": "to_field",
                    "to_node": "to_node",
                }
            ],
            nodes=[
                {
                    "id": "id",
                    "application_node_schema_id": "text_input_schema",
                }
            ],
            version="V0",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application = await response.parse()
            assert_matches_type(object, application, path=["response"])

        assert cast(Any, response.is_closed) is True
