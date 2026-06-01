"""End-to-end tests for handler validation.

These tests verify that workflow handlers (signals, queries, updates, entrypoints)
properly validate inputs at runtime when invoked through the actual API.
"""

import asyncio

import httpx
import pytest

from mistralai.workflows.testing import execute_workflow, min_api_version, poll_workflow_status


class TestEntrypointValidationE2E:
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_entrypoint_with_valid_input(self, api_client: httpx.AsyncClient) -> None:
        async with api_client:
            execution_id = await execute_workflow(api_client, "test-validation-workflow", {"initial_value": 42})
            await asyncio.sleep(1)

            # Send the complete signal to finish the workflow
            response = await api_client.post(
                f"/v1/workflows/executions/{execution_id}/signals",
                json={"name": "complete", "input": {}},
            )
            response.raise_for_status()

            result = await poll_workflow_status(api_client, execution_id, "COMPLETED", timeout_seconds=30)
            assert result["status"] == "COMPLETED"

    @min_api_version("2026-5")
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_entrypoint_with_wrong_types(self, api_client: httpx.AsyncClient) -> None:
        async with api_client:
            with pytest.raises(httpx.HTTPStatusError) as exc_info:
                await execute_workflow(
                    api_client,
                    "test-validation-workflow",
                    {"initial_value": "not_a_number"},
                )
            assert exc_info.value.response.status_code in (400, 422)

    @min_api_version("2026-5")
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_entrypoint_with_extra_fields(self, api_client: httpx.AsyncClient) -> None:
        async with api_client:
            with pytest.raises(httpx.HTTPStatusError) as exc_info:
                await execute_workflow(
                    api_client,
                    "test-validation-workflow",
                    {"initial_value": 42, "extra_field": "should_fail"},
                )
            assert exc_info.value.response.status_code in (400, 422)


class TestSignalValidationE2E:
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_signal_with_valid_input(self, api_client: httpx.AsyncClient) -> None:
        async with api_client:
            execution_id = await execute_workflow(api_client, "test-validation-workflow", {"initial_value": 10})
            await asyncio.sleep(1)

            response = await api_client.post(
                f"/v1/workflows/executions/{execution_id}/signals",
                json={"name": "process_signal", "input": {"name": "test", "count": 5}},
            )
            response.raise_for_status()

    @min_api_version("2026-5")
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_signal_with_wrong_types(self, api_client: httpx.AsyncClient) -> None:
        async with api_client:
            execution_id = await execute_workflow(api_client, "test-validation-workflow", {"initial_value": 10})
            await asyncio.sleep(1)

            response = await api_client.post(
                f"/v1/workflows/executions/{execution_id}/signals",
                json={"name": "process_signal", "input": {"name": "test", "count": "not_a_number"}},
            )
            assert response.status_code in (400, 422)

    @min_api_version("2026-5")
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_signal_with_extra_fields(self, api_client: httpx.AsyncClient) -> None:
        async with api_client:
            execution_id = await execute_workflow(api_client, "test-validation-workflow", {"initial_value": 10})
            await asyncio.sleep(1)

            response = await api_client.post(
                f"/v1/workflows/executions/{execution_id}/signals",
                json={
                    "name": "process_signal",
                    "input": {"name": "test", "count": 5, "extra": "should_fail"},
                },
            )
            assert response.status_code in (400, 422)


class TestQueryValidationE2E:
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_query_with_valid_input(self, api_client: httpx.AsyncClient) -> None:
        async with api_client:
            execution_id = await execute_workflow(api_client, "test-validation-workflow", {"initial_value": 10})
            await asyncio.sleep(1)

            response = await api_client.post(
                f"/v1/workflows/executions/{execution_id}/queries",
                json={"name": "get_state", "input": {"include_details": True}},
            )
            response.raise_for_status()

    @min_api_version("2026-5")
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_query_with_extra_fields(self, api_client: httpx.AsyncClient) -> None:
        async with api_client:
            execution_id = await execute_workflow(api_client, "test-validation-workflow", {"initial_value": 10})
            await asyncio.sleep(1)

            response = await api_client.post(
                f"/v1/workflows/executions/{execution_id}/queries",
                json={
                    "name": "get_state",
                    "input": {"include_details": True, "extra": "should_fail"},
                },
            )
            assert response.status_code in (400, 422)


class TestUpdateValidationE2E:
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_update_with_valid_input(self, api_client: httpx.AsyncClient) -> None:
        async with api_client:
            execution_id = await execute_workflow(api_client, "test-validation-workflow", {"initial_value": 10})
            await asyncio.sleep(1)

            response = await api_client.post(
                f"/v1/workflows/executions/{execution_id}/updates",
                json={"name": "update_config", "input": {"new_value": 100}},
            )
            response.raise_for_status()

    @min_api_version("2026-5")
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_update_with_extra_fields(self, api_client: httpx.AsyncClient) -> None:
        async with api_client:
            execution_id = await execute_workflow(api_client, "test-validation-workflow", {"initial_value": 10})
            await asyncio.sleep(1)

            response = await api_client.post(
                f"/v1/workflows/executions/{execution_id}/updates",
                json={
                    "name": "update_config",
                    "input": {"new_value": 100, "extra": "should_fail"},
                },
            )
            assert response.status_code in (400, 422)


class TestComplexTypeValidationE2E:
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_complex_types_with_valid_input(self, api_client: httpx.AsyncClient) -> None:
        async with api_client:
            execution_id = await execute_workflow(
                api_client, "test-complex-validation", {"config": {"key": "value", "number": 42}}
            )
            result = await poll_workflow_status(api_client, execution_id, "COMPLETED", timeout_seconds=30)
            assert result["status"] == "COMPLETED"

    @min_api_version("2026-5")
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_complex_types_with_invalid_input(self, api_client: httpx.AsyncClient) -> None:
        async with api_client:
            with pytest.raises(httpx.HTTPStatusError) as exc_info:
                await execute_workflow(
                    api_client,
                    "test-complex-validation",
                    {"config": "not_a_dict"},
                )
            assert exc_info.value.response.status_code in (400, 422)
