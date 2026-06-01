import asyncio
from typing import List

import pydantic

import mistralai.workflows as workflows
from mistralai.workflows import workflow

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.getLogger(__name__)


class PageParams(pydantic.BaseModel):
    offset: int = 0
    limit: int = 100
    total_processed: int = 0


class ProcessingResult(pydantic.BaseModel):
    total_processed: int
    status: str = "completed"


@workflows.activity()
async def fetch_items_activity(offset: int, limit: int) -> List[str]:
    """Fetch a page of items from a data source."""
    await asyncio.sleep(0.01)  # Simulating work

    if offset >= 500:
        return []

    items = [f"item_{i}" for i in range(offset, min(offset + limit, 500))]
    logger.info("Fetched items", offset=offset, count=len(items))
    return items


@workflows.activity()
async def process_items_activity(items: List[str]) -> int:
    """Process a batch of items."""
    await asyncio.sleep(0.02)  # Simulating work
    logger.info("Processed items", count=len(items))
    return len(items)


@workflows.workflow.define(name="example-continue-as-new")
class ContinueAsNewWorkflow:
    """
    Workflow demonstrating continue-as-new for paginated processing.

    This workflow processes a large dataset in pages. When the workflow history
    approaches size limits, it uses continue-as-new to reset the history while
    maintaining state through the input parameters.
    """

    @workflows.workflow.entrypoint
    async def run(self, params: PageParams) -> ProcessingResult:
        items = await fetch_items_activity(params.offset, params.limit)

        if not items:
            return ProcessingResult(total_processed=params.total_processed)

        processed_count = await process_items_activity(items)

        next_params = PageParams(
            offset=params.offset + params.limit,
            limit=params.limit,
            total_processed=params.total_processed + processed_count,
        )

        if workflows.workflow.should_continue_as_new():
            workflows.workflow.continue_as_new(next_params)

        return await self.run(next_params)


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([ContinueAsNewWorkflow]))
