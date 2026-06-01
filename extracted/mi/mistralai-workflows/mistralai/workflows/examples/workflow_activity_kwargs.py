import asyncio
from typing import Any

from pydantic import BaseModel, Field

import mistralai.workflows as workflows
from mistralai.workflows import Depends, workflow

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.get_logger(__name__)


class SearchParams(BaseModel):
    query: str = Field(..., description="Search query")


class SearchResult(BaseModel):
    query: str
    results: list[str]
    filters_applied: dict


@workflows.activity()
async def search_documents(query: str, limit: int = 10, **kwargs: Any) -> SearchResult:
    """Activity with explicit params + **kwargs."""
    logger.debug(
        "Searching documents",
        query=query,
        limit=limit,
        filters=kwargs,
    )

    # Simulate search with filters
    results = [f"Document matching '{query}' with filters {kwargs}"]

    return SearchResult(
        query=query,
        results=results,
        filters_applied={"limit": limit, **kwargs},
    )


class BaseModelKwargsResult(BaseModel):
    model_data: dict
    extra_kwargs: dict


@workflows.activity()
async def process_with_basemodel(params: SearchParams, **kwargs: Any) -> BaseModelKwargsResult:
    """Activity with single BaseModel param + **kwargs."""
    logger.debug(
        "Processing with basemodel",
        params=params,
        kwargs=kwargs,
    )

    return BaseModelKwargsResult(
        model_data=params.model_dump(),
        extra_kwargs=kwargs,
    )


class FlexibleSearchResult(BaseModel):
    params_received: dict
    result_count: int


@workflows.activity()
async def flexible_search(**kwargs: Any) -> FlexibleSearchResult:
    """Activity with only **kwargs - fully dynamic parameters."""
    logger.debug("Flexible search called", kwargs=kwargs)

    return FlexibleSearchResult(
        params_received=kwargs,
        result_count=len(kwargs),
    )


@workflows.workflow.define(name="example-activity-kwargs")
class SearchWorkflow:
    """Workflow demonstrating explicit params + **kwargs activity."""

    @workflows.workflow.entrypoint
    async def run(self, params: SearchParams) -> SearchResult:
        result = await search_documents(
            params.query,
            limit=5,
            category="engineering",
            author="team-ai",
            include_archived=False,
        )
        return result


@workflows.workflow.define(name="example-activity-only-kwargs")
class FlexibleSearchWorkflow:
    """Workflow demonstrating only **kwargs activity."""

    @workflows.workflow.entrypoint
    async def run(self, params: SearchParams) -> FlexibleSearchResult:
        result = await flexible_search(
            query=params.query,
            source="workflow",
            timestamp=12345,
            include_metadata=True,
        )
        return result


@workflows.workflow.define(name="example-basemodel-with-kwargs")
class BaseModelWithKwargsWorkflow:
    """Workflow demonstrating single BaseModel param + **kwargs activity."""

    @workflows.workflow.entrypoint
    async def run(self, params: SearchParams) -> BaseModelKwargsResult:
        result = await process_with_basemodel(
            params,
            extra_filter="important",
            priority=1,
            tags=["test", "demo"],
        )
        return result


class ComputeResult(BaseModel):
    total: int
    label: str
    multiplied: int


@workflows.activity()
async def compute_score(value: int, multiplier: int, label: str) -> ComputeResult:
    """Activity with only typed params (no **kwargs) — called with keyword arguments."""
    return ComputeResult(
        total=value + multiplier,
        label=label,
        multiplied=value * multiplier,
    )


@workflows.workflow.define(name="example-activity-typed-kwargs")
class TypedParamsKwargsWorkflow:
    """Workflow demonstrating typed-only params activity called with keyword arguments."""

    @workflows.workflow.entrypoint
    async def run(self, params: SearchParams) -> ComputeResult:
        result = await compute_score(
            value=10,
            multiplier=3,
            label=params.query,
        )
        return result


class GapResult(BaseModel):
    query: str
    limit: int
    sort: str


@workflows.activity()
async def search_with_defaults(query: str, limit: int = 10, sort: str = "relevance") -> GapResult:
    """Activity with optional params between positional and kwarg-provided params."""
    return GapResult(query=query, limit=limit, sort=sort)


@workflows.workflow.define(name="example-activity-kwargs-gap")
class TypedParamsKwargsGapWorkflow:
    """Workflow that skips an optional param and provides a later one as kwarg."""

    @workflows.workflow.entrypoint
    async def run(self, params: SearchParams) -> GapResult:
        result = await search_with_defaults(
            params.query,
            sort="date",
        )
        return result


class FakeService:
    def __init__(self) -> None:
        self.called = True

    def process(self, value: int) -> int:
        return value * 2


def get_fake_service() -> FakeService:
    return FakeService()


class DependsKwargsResult(BaseModel):
    total: int
    label: str
    service_called: bool


@workflows.activity()
async def compute_with_depends(
    value: int,
    label: str,
    svc: FakeService = Depends(get_fake_service),
) -> DependsKwargsResult:
    """Activity with typed params + Depends, called with keyword arguments."""
    return DependsKwargsResult(
        total=svc.process(value),
        label=label,
        service_called=svc.called,
    )


@workflows.workflow.define(name="example-activity-depends-kwargs")
class DependsKwargsWorkflow:
    """Workflow calling a Depends activity with keyword arguments."""

    @workflows.workflow.entrypoint
    async def run(self, params: SearchParams) -> DependsKwargsResult:
        result = await compute_with_depends(
            value=7,
            label=params.query,
        )
        return result


if __name__ == "__main__":
    asyncio.run(
        workflows.run_worker(
            [
                SearchWorkflow,
                FlexibleSearchWorkflow,
                BaseModelWithKwargsWorkflow,
                TypedParamsKwargsWorkflow,
                TypedParamsKwargsGapWorkflow,
                DependsKwargsWorkflow,
            ]
        )
    )
