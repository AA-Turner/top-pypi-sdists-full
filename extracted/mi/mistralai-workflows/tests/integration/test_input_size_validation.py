import os

import pytest
from mistralai.client import Mistral
from pydantic import BaseModel

from mistralai.workflows.client import get_mistral_client
from mistralai.workflows.constants import MAX_INPUT_SIZE_BYTES
from mistralai.workflows.testing import (
    WORKFLOW_EXAMPLE_HELLO_WORLD,
    min_api_version,
)
from mistralai.workflows.testing.constants import TEST_TASK_QUEUE


class LargeInput(BaseModel):
    data: str


class HelloWorldInput(BaseModel):
    document_title: str


def _generate_large_string(size_bytes: int) -> str:
    return "x" * size_bytes


@pytest.fixture
def mistral_client() -> Mistral:
    server_url = os.getenv("SERVER_URL", "http://localhost:7444")
    api_key = os.getenv("MISTRAL_API_KEY")
    return get_mistral_client(server_url=server_url, api_key=api_key)


@min_api_version("2026-5")
@pytest.mark.integration
@pytest.mark.asyncio
async def test_execute_rejects_input_exceeding_limit(mistral_client: Mistral) -> None:
    large_input = LargeInput(data=_generate_large_string(MAX_INPUT_SIZE_BYTES + 1000))

    with pytest.raises(Exception):
        await mistral_client.workflows.execute_workflow_async(
            workflow_identifier=WORKFLOW_EXAMPLE_HELLO_WORLD,
            input=large_input,
            task_queue=TEST_TASK_QUEUE,
        )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_execute_accepts_input_at_limit(mistral_client: Mistral) -> None:
    result = await mistral_client.workflows.execute_workflow_async(
        workflow_identifier=WORKFLOW_EXAMPLE_HELLO_WORLD,
        input=HelloWorldInput(document_title="test"),
        task_queue=TEST_TASK_QUEUE,
    )

    assert result.execution_id is not None
