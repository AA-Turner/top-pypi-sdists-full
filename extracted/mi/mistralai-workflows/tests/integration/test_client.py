from typing import AsyncGenerator

import pytest
from mistralai.client import Mistral

from mistralai.workflows.client import get_mistral_client
from mistralai.workflows.examples.workflow_activity_kwargs import SearchParams
from mistralai.workflows.testing.constants import TEST_TASK_QUEUE

WORKFLOW_IDENTIFIER = "example-activity-kwargs"
WORKFLOW_PARAMS = SearchParams(query="chicken")
INPUT_PARAMS = [
    pytest.param(WORKFLOW_PARAMS, id="basemodel"),
    pytest.param(WORKFLOW_PARAMS.model_dump(mode="json"), id="dict"),
]


@pytest.fixture
async def mistral_client(server_url) -> AsyncGenerator[Mistral, None]:
    async with get_mistral_client(server_url=server_url) as client:
        yield client


@pytest.mark.integration
class TestExecuteWorkflowAndWait:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("input_data", INPUT_PARAMS)
    async def test_async(self, mistral_client: Mistral, input_data: SearchParams | dict) -> None:
        result = await mistral_client.workflows.execute_workflow_and_wait_async(
            workflow_identifier=WORKFLOW_IDENTIFIER,
            input=input_data,
            use_api_sync=True,
            timeout_seconds=30,
            task_queue=TEST_TASK_QUEUE,
        )

        assert result is not None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("input_data", INPUT_PARAMS)
    async def test_sync(self, mistral_client: Mistral, input_data: SearchParams | dict) -> None:
        result = mistral_client.workflows.execute_workflow_and_wait(
            workflow_identifier=WORKFLOW_IDENTIFIER,
            input=input_data,
            use_api_sync=True,
            timeout_seconds=30,
            task_queue=TEST_TASK_QUEUE,
        )

        assert result is not None
