"""Tests for activity **kwargs support."""

from typing import Any

import pytest

from mistralai.workflows import get_workflow_definition
from mistralai.workflows.examples.workflow_activity_kwargs import (
    BaseModelWithKwargsWorkflow,
    DependsKwargsWorkflow,
    FlexibleSearchWorkflow,
    SearchWorkflow,
    TypedParamsKwargsGapWorkflow,
    TypedParamsKwargsWorkflow,
)

from .utils import create_test_worker, get_temporal_activities_by_names


class TestActivityKwargsWorkflows:
    @pytest.mark.asyncio
    async def test_activity_with_explicit_params_and_kwargs(self, temporal_env: Any) -> None:
        """Test workflow with activity that has explicit params + **kwargs."""
        activities = get_temporal_activities_by_names(["search_documents"])
        async with create_test_worker(
            temporal_env,
            workflows=[SearchWorkflow],
            activities=activities,
        ):
            workflow_def = get_workflow_definition(SearchWorkflow)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"query": "AI research papers"},
                id="test-activity-kwargs",
                task_queue="test-task-queue",
            )

            result = await handle.result()

            assert isinstance(result, dict)
            assert result["query"] == "AI research papers"
            assert "filters_applied" in result
            filters = result["filters_applied"]
            assert filters["limit"] == 5
            assert filters["category"] == "engineering"
            assert filters["author"] == "team-ai"
            assert filters["include_archived"] is False

    @pytest.mark.asyncio
    async def test_activity_with_only_kwargs(self, temporal_env: Any) -> None:
        """Test workflow with activity that only takes **kwargs."""
        activities = get_temporal_activities_by_names(["flexible_search"])
        async with create_test_worker(
            temporal_env,
            workflows=[FlexibleSearchWorkflow],
            activities=activities,
        ):
            workflow_def = get_workflow_definition(FlexibleSearchWorkflow)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"query": "test query"},
                id="test-activity-only-kwargs",
                task_queue="test-task-queue",
            )

            result = await handle.result()

            assert isinstance(result, dict)
            assert "params_received" in result
            params = result["params_received"]
            assert params["query"] == "test query"
            assert params["source"] == "workflow"
            assert params["timestamp"] == 12345
            assert params["include_metadata"] is True
            assert result["result_count"] == 4

    @pytest.mark.asyncio
    async def test_activity_with_typed_params_called_as_kwargs(self, temporal_env: Any) -> None:
        """Test that an activity with only typed params (no **kwargs) can be called with keyword arguments.

        This is the core WFL-695 regression: before the fix, calling an activity
        with keyword arguments raised an error even when all params were valid.
        """
        activities = get_temporal_activities_by_names(["compute_score"])
        async with create_test_worker(
            temporal_env,
            workflows=[TypedParamsKwargsWorkflow],
            activities=activities,
        ):
            workflow_def = get_workflow_definition(TypedParamsKwargsWorkflow)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"query": "my-label"},
                id="test-activity-typed-kwargs",
                task_queue="test-task-queue",
            )

            result = await handle.result()

            assert isinstance(result, dict)
            assert result["total"] == 13  # 10 + 3
            assert result["multiplied"] == 30  # 10 * 3
            assert result["label"] == "my-label"

    @pytest.mark.asyncio
    async def test_activity_with_basemodel_and_kwargs(self, temporal_env: Any) -> None:
        """Test workflow with activity that has single BaseModel param + **kwargs."""
        activities = get_temporal_activities_by_names(["process_with_basemodel"])
        async with create_test_worker(
            temporal_env,
            workflows=[BaseModelWithKwargsWorkflow],
            activities=activities,
        ):
            workflow_def = get_workflow_definition(BaseModelWithKwargsWorkflow)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"query": "basemodel test"},
                id="test-activity-basemodel-kwargs",
                task_queue="test-task-queue",
            )

            result = await handle.result()

            assert isinstance(result, dict)
            assert "model_data" in result
            assert result["model_data"]["query"] == "basemodel test"
            assert "extra_kwargs" in result
            extra = result["extra_kwargs"]
            assert extra["extra_filter"] == "important"
            assert extra["priority"] == 1
            assert extra["tags"] == ["test", "demo"]

    @pytest.mark.asyncio
    async def test_activity_kwargs_with_optional_param_gap(self, temporal_env: Any) -> None:
        """Test that kwargs with optional param gaps preserve correct argument positions.

        Regression test: calling search_with_defaults("test", sort="date") should keep
        limit=10 (default) and sort="date", not assign "date" to limit.
        """
        activities = get_temporal_activities_by_names(["search_with_defaults"])
        async with create_test_worker(
            temporal_env,
            workflows=[TypedParamsKwargsGapWorkflow],
            activities=activities,
        ):
            workflow_def = get_workflow_definition(TypedParamsKwargsGapWorkflow)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"query": "test"},
                id="test-activity-kwargs-gap",
                task_queue="test-task-queue",
            )

            result = await handle.result()

            assert isinstance(result, dict)
            assert result["query"] == "test"
            assert result["limit"] == 10  # default preserved, not overwritten by "date"
            assert result["sort"] == "date"  # correctly assigned to sort param

    @pytest.mark.asyncio
    async def test_activity_with_depends_called_as_kwargs(self, temporal_env: Any) -> None:
        """Test that Depends params don't leak into temporal_args when kwargs are used.

        Regression test: when an activity has Depends params and is called with keyword
        arguments, the Depends params should be filtered out of the positional args
        sent to Temporal. Without the fix, DependsCls defaults would be appended to
        temporal_args, causing argument-count errors at runtime.
        """
        activities = get_temporal_activities_by_names(["compute_with_depends"])
        async with create_test_worker(
            temporal_env,
            workflows=[DependsKwargsWorkflow],
            activities=activities,
        ):
            workflow_def = get_workflow_definition(DependsKwargsWorkflow)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"query": "dep-test"},
                id="test-activity-depends-kwargs",
                task_queue="test-task-queue",
            )

            result = await handle.result()

            assert isinstance(result, dict)
            assert result["total"] == 14  # 7 * 2
            assert result["label"] == "dep-test"
            assert result["service_called"] is True
