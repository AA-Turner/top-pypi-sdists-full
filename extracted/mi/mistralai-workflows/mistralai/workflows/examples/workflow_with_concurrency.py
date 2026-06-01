"""
workflows concurrency examples showcasing three execution patterns:

Each pattern is demonstrated with both primitive types and Pydantic models:

1. **List Executor** - Process a known list of items
2. **Chain Executor** - Process items sequentially from a stream/queue (token-based pagination)
3. **Offset Pagination Executor** - Process items by fetching pages/chunks by index
"""

import asyncio
from typing import Any, List

import pydantic

import mistralai.workflows as workflows
from mistralai.workflows import workflow

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.getLogger(__name__)

NB_ITEMS = 10


# --- Pydantic model types ---


class ItemData(pydantic.BaseModel):
    item_id: int
    value: str
    extra_data: Any | None = None


class ActivityResult(pydantic.BaseModel):
    processed_value: str
    item_id: int
    extra_data: Any | None = None


# --- Activities (primitive types) ---


@workflows.activity()
async def process_primitive_activity(name: str, count: int) -> str:
    """Process primitive parameters (str + int)."""
    return f"processed_{name}_{count}"


@workflows.activity()
async def get_next_primitive_from_chain(prev_item: dict | None) -> dict | None:
    """Chain helper: returns next dict of primitive params, or None when done."""
    if prev_item is None:
        return {"name": "item_0", "count": 0}

    next_id = prev_item["count"] + 1
    if next_id >= NB_ITEMS:
        return None
    return {"name": f"item_{next_id}", "count": next_id}


@workflows.activity()
async def get_primitive_by_index(params: workflows.GetItemFromIndexParams) -> dict:
    """Offset pagination helper: returns dict of primitive params at given index."""
    return {"name": f"item_{params.idx}", "count": params.idx}


# --- Activities (Pydantic models) ---


@workflows.activity()
async def process_item_activity(item: ItemData) -> ActivityResult:
    """Process a single Pydantic model item."""
    return ActivityResult(processed_value=f"processed_{item.value}", item_id=item.item_id, extra_data=item.extra_data)


@workflows.activity()
async def get_next_item_from_chain(prev_item: ItemData | None) -> ItemData | None:
    """Chain helper: returns next item from previous, or None when done."""
    if prev_item is None:
        return ItemData(item_id=0, value="item_0")

    next_id = prev_item.item_id + 1
    if next_id >= NB_ITEMS:
        return None
    return ItemData(item_id=next_id, value=f"item_{next_id}")


@workflows.activity()
async def get_item_by_index(params: workflows.GetItemFromIndexParams) -> ItemData:
    """Offset pagination helper: returns item at given index."""
    return ItemData(item_id=params.idx, value=f"item_{params.idx}", extra_data=params.extra_params)


# --- List Executor Workflows ---


@workflows.workflow.define(name="list-executor-primitive-example")
class ListExecutorPrimitiveExample:
    """List executor with primitive types — each item is a dict of parameter names to values."""

    @workflows.workflow.entrypoint
    async def run(self) -> List[str]:
        return await workflows.execute_activities_in_parallel(
            activity=process_primitive_activity,
            items=[{"name": f"item_{i}", "count": i} for i in range(NB_ITEMS)],
        )


@workflows.workflow.define(name="list-executor-pydantic-example")
class ListExecutorPydanticExample:
    """List executor with Pydantic models."""

    @workflows.workflow.entrypoint
    async def run(self) -> List[ActivityResult]:
        return await workflows.execute_activities_in_parallel(
            activity=process_item_activity,
            items=[ItemData(item_id=i, value=f"item_{i}") for i in range(NB_ITEMS)],
        )


# --- Chain Executor Workflows ---


@workflows.workflow.define(name="chain-executor-primitive-example")
class ChainExecutorPrimitiveExample:
    """Chain executor with primitive types."""

    @workflows.workflow.entrypoint
    async def run(self) -> List[str]:
        return await workflows.execute_activities_in_parallel(
            activity=process_primitive_activity,
            get_item_from_prev_item_activity=get_next_primitive_from_chain,
        )


@workflows.workflow.define(name="chain-executor-pydantic-example")
class ChainExecutorPydanticExample:
    """Chain executor with Pydantic models."""

    @workflows.workflow.entrypoint
    async def run(self) -> List[ActivityResult]:
        return await workflows.execute_activities_in_parallel(
            activity=process_item_activity,
            get_item_from_prev_item_activity=get_next_item_from_chain,
        )


# --- Offset Pagination Executor Workflows ---


@workflows.workflow.define(name="offset-pagination-primitive-example")
class OffsetPaginationPrimitiveExample:
    """Offset pagination executor with primitive types."""

    @workflows.workflow.entrypoint
    async def run(self) -> List[str]:
        return await workflows.execute_activities_in_parallel(
            activity=process_primitive_activity,
            get_item_from_index_activity=get_primitive_by_index,
            n_items=NB_ITEMS,
        )


@workflows.workflow.define(name="offset-pagination-pydantic-example")
class OffsetPaginationPydanticExample:
    """Offset pagination executor with Pydantic models."""

    @workflows.workflow.entrypoint
    async def run(self, extra_params: Any | None = None) -> List[ActivityResult]:
        return await workflows.execute_activities_in_parallel(
            activity=process_item_activity,
            get_item_from_index_activity=get_item_by_index,
            n_items=NB_ITEMS,
            extra_params=extra_params,
        )


if __name__ == "__main__":
    asyncio.run(
        workflows.run_worker(
            [
                ListExecutorPrimitiveExample,
                ListExecutorPydanticExample,
                ChainExecutorPrimitiveExample,
                ChainExecutorPydanticExample,
                OffsetPaginationPrimitiveExample,
                OffsetPaginationPydanticExample,
            ]
        )
    )
