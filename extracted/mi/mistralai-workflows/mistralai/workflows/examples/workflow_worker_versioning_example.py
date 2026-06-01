"""Example workflow demonstrating worker versioning with pinned behavior.

This example shows how worker versioning can be enabled in production to ensure
workflow executions stay pinned to the same build they started on, preventing
mid-flight code changes during long-running workflows.

To run without versioning (local dev - default behavior):
    uv run python -m examples.workflow_worker_versioning_example

To run with versioning enabled (production):
    DEPLOYMENT_NAME=example-deployment \
    BUILD_ID=v1.0.0 \
    python -m examples.workflow_worker_versioning_example

Note: When versioning is disabled (default), workflows behave exactly as they always have.
"""

import asyncio

import pydantic

import mistralai.workflows as workflows
from mistralai.workflows import workflow
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.logging import setup_logging

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.getLogger(__name__)


class VersioningExampleInput(pydantic.BaseModel):
    message: str = pydantic.Field(description="Input message to process")
    sleep_seconds: float = pydantic.Field(default=1.0, description="Duration to sleep (simulates processing time)")


class ProcessedMessage(pydantic.BaseModel):
    processed_text: str = pydantic.Field(description="Processed message text")


class VersioningExampleOutput(pydantic.BaseModel):
    result: str = pydantic.Field(description="Processed result")
    workflow_id: str = pydantic.Field(description="Workflow execution ID")


@workflows.activity()
async def process_message(params: VersioningExampleInput) -> ProcessedMessage:
    """Simple activity that processes a message."""
    await asyncio.sleep(params.sleep_seconds)  # Simulate work
    return ProcessedMessage(processed_text=f"Processed: {params.message}")


@workflows.workflow.define(
    name="WorkerVersioningExample",
    workflow_description="Example workflow demonstrating pinned worker versioning behavior",
)
class WorkerVersioningExampleWorkflow:
    """Example workflow that demonstrates worker versioning.

    When worker versioning is enabled with PINNED behavior:
    - This workflow will stay on the build it started with for its entire lifetime
    - New workflow executions will be routed to the current build
    - Long-running workflows won't be affected by new deployments

    When versioning is disabled (default):
    - Workflow behaves normally without any versioning constraints
    """

    @workflows.workflow.entrypoint
    async def run(self, params: VersioningExampleInput) -> VersioningExampleOutput:
        execution_id = workflows.get_execution_id()

        # Call activity to process the message
        processed = await process_message(params)

        return VersioningExampleOutput(
            result=processed.processed_text,
            workflow_id=execution_id or "unknown",
        )


if __name__ == "__main__":
    setup_logging(
        log_format=config.common.log_format,
        log_level=config.common.log_level,
        app_version=config.common.app_version,
    )

    # Log versioning configuration at startup
    if config.worker.versioning.enabled:
        logger.info(
            "Worker versioning ENABLED",
            deployment_name=config.worker.versioning.deployment_name,
            build_id=config.worker.versioning.build_id,
        )
    else:
        logger.info("Worker versioning DISABLED (default local dev mode)")

    asyncio.run(workflows.run_worker([WorkerVersioningExampleWorkflow]))
