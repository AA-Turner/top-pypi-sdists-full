import httpx
import pytest

from mistralai.workflows.testing import (
    execute_workflow_and_wait,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_workflow_activity_optional_arg(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "activity-optional-arg-workflow",
            {"name": "abc"},
        )

        assert result["status"] == "COMPLETED"
        assert result["result"]["result"] == "Hello abc, your ID is 123"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_workflow_activity_optional_arg_model(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "activity-optional-arg-workflow-model",
            {"name": "abc"},
        )

        assert result["status"] == "COMPLETED"
        assert result["result"]["result"] == "Hello abc, your ID is 123"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_workflow_optional_arg(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "optional-arg-workflow",
            {"name": "abc"},
        )

        assert result["status"] == "COMPLETED"
        assert result["result"]["result"] == "Hello abc, your ID is 123"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_workflow_optional_arg_model(api_client: httpx.AsyncClient) -> None:
    async with api_client:
        result = await execute_workflow_and_wait(
            api_client,
            "optional-arg-workflow-model",
            {"name": {"name": "abc"}},
        )

        assert result["status"] == "COMPLETED"
        assert result["result"]["result"] == "Hello abc, your ID is 123"
