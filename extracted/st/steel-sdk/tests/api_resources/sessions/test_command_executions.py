# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from steel import Steel, AsyncSteel
from tests.utils import assert_matches_type
from steel.types.sessions import CommandExecutionCancelResponse, CommandExecutionRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCommandExecutions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Steel) -> None:
        command_execution = client.sessions.command_executions.retrieve(
            execution_id="executionId",
            session_id="sessionId",
        )
        assert_matches_type(CommandExecutionRetrieveResponse, command_execution, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Steel) -> None:
        response = client.sessions.command_executions.with_raw_response.retrieve(
            execution_id="executionId",
            session_id="sessionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        command_execution = response.parse()
        assert_matches_type(CommandExecutionRetrieveResponse, command_execution, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Steel) -> None:
        with client.sessions.command_executions.with_streaming_response.retrieve(
            execution_id="executionId",
            session_id="sessionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            command_execution = response.parse()
            assert_matches_type(CommandExecutionRetrieveResponse, command_execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.command_executions.with_raw_response.retrieve(
                execution_id="executionId",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `execution_id` but received ''"):
            client.sessions.command_executions.with_raw_response.retrieve(
                execution_id="",
                session_id="sessionId",
            )

    @parametrize
    def test_method_cancel(self, client: Steel) -> None:
        command_execution = client.sessions.command_executions.cancel(
            execution_id="executionId",
            session_id="sessionId",
        )
        assert_matches_type(CommandExecutionCancelResponse, command_execution, path=["response"])

    @parametrize
    def test_raw_response_cancel(self, client: Steel) -> None:
        response = client.sessions.command_executions.with_raw_response.cancel(
            execution_id="executionId",
            session_id="sessionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        command_execution = response.parse()
        assert_matches_type(CommandExecutionCancelResponse, command_execution, path=["response"])

    @parametrize
    def test_streaming_response_cancel(self, client: Steel) -> None:
        with client.sessions.command_executions.with_streaming_response.cancel(
            execution_id="executionId",
            session_id="sessionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            command_execution = response.parse()
            assert_matches_type(CommandExecutionCancelResponse, command_execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_cancel(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.command_executions.with_raw_response.cancel(
                execution_id="executionId",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `execution_id` but received ''"):
            client.sessions.command_executions.with_raw_response.cancel(
                execution_id="",
                session_id="sessionId",
            )


class TestAsyncCommandExecutions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSteel) -> None:
        command_execution = await async_client.sessions.command_executions.retrieve(
            execution_id="executionId",
            session_id="sessionId",
        )
        assert_matches_type(CommandExecutionRetrieveResponse, command_execution, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.command_executions.with_raw_response.retrieve(
            execution_id="executionId",
            session_id="sessionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        command_execution = await response.parse()
        assert_matches_type(CommandExecutionRetrieveResponse, command_execution, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.command_executions.with_streaming_response.retrieve(
            execution_id="executionId",
            session_id="sessionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            command_execution = await response.parse()
            assert_matches_type(CommandExecutionRetrieveResponse, command_execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.command_executions.with_raw_response.retrieve(
                execution_id="executionId",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `execution_id` but received ''"):
            await async_client.sessions.command_executions.with_raw_response.retrieve(
                execution_id="",
                session_id="sessionId",
            )

    @parametrize
    async def test_method_cancel(self, async_client: AsyncSteel) -> None:
        command_execution = await async_client.sessions.command_executions.cancel(
            execution_id="executionId",
            session_id="sessionId",
        )
        assert_matches_type(CommandExecutionCancelResponse, command_execution, path=["response"])

    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.command_executions.with_raw_response.cancel(
            execution_id="executionId",
            session_id="sessionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        command_execution = await response.parse()
        assert_matches_type(CommandExecutionCancelResponse, command_execution, path=["response"])

    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.command_executions.with_streaming_response.cancel(
            execution_id="executionId",
            session_id="sessionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            command_execution = await response.parse()
            assert_matches_type(CommandExecutionCancelResponse, command_execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.command_executions.with_raw_response.cancel(
                execution_id="executionId",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `execution_id` but received ''"):
            await async_client.sessions.command_executions.with_raw_response.cancel(
                execution_id="",
                session_id="sessionId",
            )
