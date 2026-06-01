"""Tests for execute_activities_in_parallel with primitive and Pydantic types."""

from typing import Any, List

import pytest
from pydantic import BaseModel
from temporalio.client import WorkflowFailureError
from temporalio.exceptions import ApplicationError

import mistralai.workflows as workflows
from mistralai.workflows import get_workflow_definition, workflow
from mistralai.workflows.core.execution.concurrency._concurrency_workflow import ParallelExecutionWorkflow
from mistralai.workflows.core.execution.concurrency._execute_activities_in_batch import execute_activity_in_batch
from mistralai.workflows.core.execution.concurrency._utils import build_type_adapters, coerce_multi_params
from mistralai.workflows.core.execution.concurrency.execute_activities_in_parallel import (
    _validate_items,
    execute_activities_in_parallel,
)

from .utils import create_test_worker, get_temporal_activities_by_names


class ItemModel(BaseModel):
    item_id: int
    value: str


class ResultModel(BaseModel):
    processed: str
    item_id: int


@workflows.activity()
async def process_single_str(name: str) -> str:
    return f"hello_{name}"


@workflows.activity()
async def process_multi_params(name: str, count: int) -> str:
    return f"{name}_{count}"


@workflows.activity()
async def process_pydantic_item(item: ItemModel) -> ResultModel:
    return ResultModel(processed=f"done_{item.value}", item_id=item.item_id)


@workflows.activity()
async def process_mixed_params(name: str, item: ItemModel) -> str:
    return f"{name}_{item.item_id}_{item.value}"


@workflows.activity()
async def process_kwargs_only(**kwargs: Any) -> str:
    return f"{kwargs['name']}_{kwargs['count']}"


@workflows.activity()
async def process_explicit_with_kwargs(name: str, **kwargs: Any) -> str:
    return f"{name}_{kwargs['count']}"


@workflows.activity()
async def get_next_str(prev: str | None) -> str | None:
    if prev is None:
        return "item_0"
    idx = int(prev.split("_")[1])
    if idx + 1 >= 3:
        return None
    return f"item_{idx + 1}"


@workflows.activity()
async def get_next_dict_with_typo(prev: dict | None) -> dict | None:
    """Chain provider that returns dicts with a misnamed key (typo)."""
    if prev is None:
        return {"name": "a", "countt": 1}  # typo: "countt" instead of "count"
    return None


@workflows.activity()
async def get_next_dict_missing_key(prev: dict | None) -> dict | None:
    """Chain provider that returns dicts missing a required key."""
    if prev is None:
        return {"name": "a"}  # missing "count"
    return None


@workflows.activity()
async def get_dict_missing_key_by_index(params: workflows.GetItemFromIndexParams) -> dict:
    """Offset pagination provider that returns dicts missing a required key."""
    return {"name": f"item_{params.idx}"}  # missing "count"


@workflows.activity()
async def get_str_by_index(params: workflows.GetItemFromIndexParams) -> str:
    return f"item_{params.idx}"


@workflows.activity()
async def get_dict_with_typo_by_index(params: workflows.GetItemFromIndexParams) -> dict:
    """Offset pagination provider that returns dicts with a misnamed key (typo)."""
    return {"name": f"item_{params.idx}", "countt": params.idx}  # typo: "countt" instead of "count"


@workflows.activity()
async def get_next_kwargs_dict(prev: dict | None) -> dict | None:
    if prev is None:
        return {"name": "item_0", "count": 0}
    idx = prev["count"] + 1
    if idx >= 3:
        return None
    return {"name": f"item_{idx}", "count": idx}


@workflows.activity()
async def get_kwargs_dict_by_index(params: workflows.GetItemFromIndexParams) -> dict:
    return {"name": f"item_{params.idx}", "count": params.idx}


# --- Unit tests for _validate_items (no Temporal env) ---


class TestValidateItems:
    def test_valid_single_param(self) -> None:
        _validate_items(items=["a", "b"], user_params_dict={"name": str}, is_single_param=True, activity_name="act")

    def test_valid_multi_param(self) -> None:
        _validate_items(
            items=[{"name": "a", "count": 1}],
            user_params_dict={"name": str, "count": int},
            is_single_param=False,
            activity_name="act",
        )

    def test_valid_multi_param_with_pydantic(self) -> None:
        _validate_items(
            items=[{"name": "a", "item": {"item_id": 1, "value": "v"}}],
            user_params_dict={"name": str, "item": ItemModel},
            is_single_param=False,
            activity_name="act",
        )

    def test_valid_pydantic_as_dict(self) -> None:
        _validate_items(
            items=[{"item_id": 1, "value": "test"}],
            user_params_dict={"item": ItemModel},
            is_single_param=True,
            activity_name="act",
        )

    def test_empty_items(self) -> None:
        _validate_items(items=[], user_params_dict={"name": str}, is_single_param=True, activity_name="act")

    def test_kwargs_only_not_dict_raises_error(self) -> None:
        with pytest.raises(ApplicationError, match="kwargs activity"):
            _validate_items(
                items=["not_a_dict"],
                user_params_dict={},
                is_single_param=False,
                activity_name="act",
                has_kwargs=True,
            )

    def test_multi_param_with_kwargs_accepts_extra_keys(self) -> None:
        _validate_items(
            items=[{"name": "ok", "count": 1, "extra": "allowed"}],
            user_params_dict={"name": str},
            is_single_param=False,
            activity_name="act",
            activity_func=process_explicit_with_kwargs.__original_func__,  # type: ignore[attr-defined]
            has_kwargs=True,
        )

    def test_single_param_wrong_type(self) -> None:
        with pytest.raises(ApplicationError, match="Item at index 1 is not compatible"):
            _validate_items(items=["ok", 123], user_params_dict={"name": str}, is_single_param=True, activity_name="a")

    def test_multi_param_not_a_dict(self) -> None:
        with pytest.raises(ApplicationError, match="must be a dict"):
            _validate_items(
                items=["not_a_dict"],
                user_params_dict={"name": str, "count": int},
                is_single_param=False,
                activity_name="act",
            )

    def test_multi_param_wrong_key(self) -> None:
        with pytest.raises(ApplicationError, match="Item at index 0 is not compatible"):
            _validate_items(
                items=[{"wrong_key": "v", "count": 1}],
                user_params_dict={"name": str, "count": int},
                is_single_param=False,
                activity_name="act",
            )

    def test_multi_param_wrong_value_type(self) -> None:
        with pytest.raises(ApplicationError, match="Item at index 0 is not compatible"):
            _validate_items(
                items=[{"name": "ok", "count": "not_int"}],
                user_params_dict={"name": str, "count": int},
                is_single_param=False,
                activity_name="act",
            )

    def test_pydantic_invalid_dict(self) -> None:
        with pytest.raises(ApplicationError, match="Item at index 0 is not compatible"):
            _validate_items(
                items=[{"wrong_field": 1}],
                user_params_dict={"item": ItemModel},
                is_single_param=True,
                activity_name="act",
            )


# --- Unit tests for coerce_multi_params ---


class TestCoerceMultiParams:
    def test_valid_keys(self) -> None:
        adapters = build_type_adapters({"name": str, "count": int})
        result = coerce_multi_params({"name": "hello", "count": 42}, adapters)
        assert result == {"name": "hello", "count": 42}

    def test_extra_keys_raises_error(self) -> None:
        adapters = build_type_adapters({"name": str, "count": int})
        with pytest.raises(ApplicationError, match="Unexpected keys"):
            coerce_multi_params({"name": "hello", "count": 1, "typo_key": "val"}, adapters)

    def test_extra_keys_allowed_when_activity_accepts_kwargs(self) -> None:
        adapters = build_type_adapters({"name": str})
        result = coerce_multi_params({"name": "hello", "count": 1, "extra": "ok"}, adapters, allow_extra=True)
        assert result == {"name": "hello", "count": 1, "extra": "ok"}

    def test_subset_of_keys_is_allowed_without_required(self) -> None:
        adapters = build_type_adapters({"name": str, "count": int})
        result = coerce_multi_params({"name": "hello"}, adapters)
        assert result == {"name": "hello"}

    def test_missing_required_keys_raises_error(self) -> None:
        adapters = build_type_adapters({"name": str, "count": int})
        required = {"name", "count"}
        with pytest.raises(ApplicationError, match="Missing required keys"):
            coerce_multi_params({"name": "hello"}, adapters, required)

    def test_missing_optional_keys_is_allowed(self) -> None:
        adapters = build_type_adapters({"name": str, "count": int})
        required = {"name"}  # count is optional
        result = coerce_multi_params({"name": "hello"}, adapters, required)
        assert result == {"name": "hello"}

    def test_coerces_pydantic_from_dict(self) -> None:
        adapters = build_type_adapters({"item": ItemModel})
        result = coerce_multi_params({"item": {"item_id": 1, "value": "v"}}, adapters)
        assert isinstance(result["item"], ItemModel)
        assert result["item"].item_id == 1


# --- Input validation via execute_activities_in_parallel (no Temporal env) ---


class TestInputValidation:
    @pytest.mark.asyncio
    async def test_wrong_type_raises_error(self) -> None:
        with pytest.raises(ApplicationError, match="Item at index 0 is not compatible"):
            await execute_activities_in_parallel(activity=process_single_str, items=[123])

    @pytest.mark.asyncio
    async def test_multi_param_wrong_keys_raises_error(self) -> None:
        with pytest.raises(ApplicationError, match="Item at index 0 is not compatible"):
            await execute_activities_in_parallel(activity=process_multi_params, items=[{"wrong": "val", "count": 1}])

    @pytest.mark.asyncio
    async def test_multi_param_not_dict_raises_error(self) -> None:
        with pytest.raises(ApplicationError, match="must be a dict"):
            await execute_activities_in_parallel(activity=process_multi_params, items=["not_a_dict"])

    @pytest.mark.asyncio
    async def test_non_activity_raises_error(self) -> None:
        async def not_an_activity(x: str) -> str:
            return x

        with pytest.raises(ApplicationError, match="must be an activity"):
            await execute_activities_in_parallel(activity=not_an_activity, items=["a"])

    @pytest.mark.asyncio
    async def test_offset_fetcher_wrong_param_type_raises_error(self) -> None:
        @workflows.activity()
        async def bad_fetcher(idx: int) -> str:
            return f"item_{idx}"

        with pytest.raises(ApplicationError, match="must take a single parameter of type GetItemFromIndexParams"):
            await execute_activities_in_parallel(
                activity=process_single_str,
                get_item_from_index_activity=bad_fetcher,
                n_items=5,
            )

    @pytest.mark.asyncio
    async def test_chain_provider_wrong_return_type_raises_error(self) -> None:
        @workflows.activity()
        async def bad_chain_provider(prev: str | None) -> str | None:
            return None

        with pytest.raises(ApplicationError, match="returns str.*expects ItemModel"):
            await execute_activities_in_parallel(
                activity=process_pydantic_item,
                get_item_from_prev_item_activity=bad_chain_provider,
            )

    @pytest.mark.asyncio
    async def test_chain_provider_input_incompatible_with_return_raises_error(self) -> None:
        @workflows.activity()
        async def bad_chain_provider(prev: str | None) -> ItemModel | None:
            return None

        with pytest.raises(ApplicationError, match="returns ItemModel.*its own input expects str"):
            await execute_activities_in_parallel(
                activity=process_pydantic_item,
                get_item_from_prev_item_activity=bad_chain_provider,
            )

    @pytest.mark.asyncio
    async def test_chain_provider_non_dict_for_multi_param_raises_error(self) -> None:
        @workflows.activity()
        async def bad_chain_provider(prev: str | None) -> str | None:
            return None

        with pytest.raises(ApplicationError, match="returns str.*expects a dict"):
            await execute_activities_in_parallel(
                activity=process_multi_params,
                get_item_from_prev_item_activity=bad_chain_provider,
            )

    @pytest.mark.asyncio
    async def test_offset_fetcher_wrong_return_type_raises_error(self) -> None:
        @workflows.activity()
        async def bad_fetcher(params: workflows.GetItemFromIndexParams) -> str:
            return f"item_{params.idx}"

        with pytest.raises(ApplicationError, match="returns str.*expects ItemModel"):
            await execute_activities_in_parallel(
                activity=process_pydantic_item,
                get_item_from_index_activity=bad_fetcher,
                n_items=5,
            )

    @pytest.mark.asyncio
    async def test_offset_fetcher_non_dict_for_multi_param_raises_error(self) -> None:
        @workflows.activity()
        async def bad_fetcher(params: workflows.GetItemFromIndexParams) -> str:
            return f"item_{params.idx}"

        with pytest.raises(ApplicationError, match="returns str.*expects a dict"):
            await execute_activities_in_parallel(
                activity=process_multi_params,
                get_item_from_index_activity=bad_fetcher,
                n_items=5,
            )

    @pytest.mark.asyncio
    async def test_chain_provider_non_dict_for_kwargs_only_raises_error(self) -> None:
        @workflows.activity()
        async def bad_chain_provider(prev: str | None) -> str | None:
            return None

        with pytest.raises(ApplicationError, match="returns str.*expects a dict"):
            await execute_activities_in_parallel(
                activity=process_kwargs_only,
                get_item_from_prev_item_activity=bad_chain_provider,
            )

    @pytest.mark.asyncio
    async def test_offset_fetcher_non_dict_for_kwargs_only_raises_error(self) -> None:
        @workflows.activity()
        async def bad_fetcher(params: workflows.GetItemFromIndexParams) -> str:
            return f"item_{params.idx}"

        with pytest.raises(ApplicationError, match="returns str.*expects a dict"):
            await execute_activities_in_parallel(
                activity=process_kwargs_only,
                get_item_from_index_activity=bad_fetcher,
                n_items=5,
            )

    @pytest.mark.asyncio
    async def test_zero_param_activity_raises_error(self) -> None:
        @workflows.activity()
        async def no_input_activity() -> str:
            return "done"

        with pytest.raises(ApplicationError, match="silently ignored"):
            await execute_activities_in_parallel(
                activity=no_input_activity,
                items=["a", "b"],
            )

    @pytest.mark.asyncio
    async def test_no_execution_pattern_raises_error(self) -> None:
        with pytest.raises(ApplicationError, match="Must specify one execution pattern"):
            await execute_activities_in_parallel(activity=process_single_str)

    @pytest.mark.asyncio
    async def test_chain_provider_generic_type_mismatch_raises_error(self) -> None:
        """Chain provider returning str is caught when activity expects list[str]."""

        @workflows.activity()
        async def process_list(items: list[str]) -> str:
            return ",".join(items)

        @workflows.activity()
        async def bad_chain(prev: str | None) -> str | None:
            return None

        with pytest.raises(ApplicationError, match="returns str.*expects list"):
            await execute_activities_in_parallel(
                activity=process_list,
                get_item_from_prev_item_activity=bad_chain,
            )

    @pytest.mark.asyncio
    async def test_offset_fetcher_generic_type_mismatch_raises_error(self) -> None:
        """Offset fetcher returning str is caught when activity expects list[str]."""

        @workflows.activity()
        async def process_list(items: list[str]) -> str:
            return ",".join(items)

        @workflows.activity()
        async def bad_fetcher(params: workflows.GetItemFromIndexParams) -> str:
            return "item"

        with pytest.raises(ApplicationError, match="returns str.*expects list"):
            await execute_activities_in_parallel(
                activity=process_list,
                get_item_from_index_activity=bad_fetcher,
                n_items=3,
            )

    @pytest.mark.asyncio
    async def test_chain_provider_generic_type_compatible_passes(self) -> None:
        """Chain provider returning list[str] passes when activity expects list[str]."""

        @workflows.activity()
        async def process_list(items: list[str]) -> str:
            return ",".join(items)

        @workflows.activity()
        async def good_chain(prev: list[str] | None) -> list[str] | None:
            return None

        # Should not raise — origin classes match (list == list)
        # Will raise "Must specify one execution pattern" only if we don't pass enough args,
        # but here it should pass validation and attempt to run the workflow
        # (which will fail because no Temporal env, but that's after validation)
        try:
            await execute_activities_in_parallel(
                activity=process_list,
                get_item_from_prev_item_activity=good_chain,
            )
        except ApplicationError as e:
            # Should NOT be a type mismatch error
            assert "returns" not in str(e) and "expects" not in str(e)


# --- E2E tests (with Temporal env) ---


class ListStrInput(BaseModel):
    items: List[str]


class ListMultiParamInput(BaseModel):
    items: List[dict]


class ListMixedParamInput(BaseModel):
    items: List[dict]


class ListPydanticInput(BaseModel):
    items: List[ItemModel]


class ListKwargsInput(BaseModel):
    items: List[dict]


@workflow.define(name="test-parallel-list-str-e2e")
class ListStrE2EWorkflow:
    @workflow.entrypoint
    async def run(self, input: ListStrInput) -> List[str]:
        return await execute_activities_in_parallel(activity=process_single_str, items=input.items)


@workflow.define(name="test-parallel-list-multi-e2e")
class ListMultiParamE2EWorkflow:
    @workflow.entrypoint
    async def run(self, input: ListMultiParamInput) -> List[str]:
        return await execute_activities_in_parallel(
            activity=process_multi_params,
            items=input.items,
        )


@workflow.define(name="test-parallel-list-mixed-e2e")
class ListMixedParamE2EWorkflow:
    @workflow.entrypoint
    async def run(self, input: ListMixedParamInput) -> List[str]:
        return await execute_activities_in_parallel(
            activity=process_mixed_params,
            items=input.items,
        )


@workflow.define(name="test-parallel-list-pydantic-e2e")
class ListPydanticE2EWorkflow:
    @workflow.entrypoint
    async def run(self, input: ListPydanticInput) -> List[ResultModel]:
        return await execute_activities_in_parallel(
            activity=process_pydantic_item,
            items=input.items,
        )


@workflow.define(name="test-parallel-list-kwargs-e2e")
class ListKwargsE2EWorkflow:
    @workflow.entrypoint
    async def run(self, input: ListKwargsInput) -> List[str]:
        return await execute_activities_in_parallel(
            activity=process_kwargs_only,
            items=input.items,
        )


@workflow.define(name="test-parallel-chain-str-e2e")
class ChainStrE2EWorkflow:
    @workflow.entrypoint
    async def run(self) -> List[str]:
        return await execute_activities_in_parallel(
            activity=process_single_str,
            get_item_from_prev_item_activity=get_next_str,
        )


@workflow.define(name="test-parallel-chain-kwargs-e2e")
class ChainKwargsE2EWorkflow:
    @workflow.entrypoint
    async def run(self) -> List[str]:
        return await execute_activities_in_parallel(
            activity=process_kwargs_only,
            get_item_from_prev_item_activity=get_next_kwargs_dict,
        )


@workflow.define(name="test-parallel-offset-str-e2e")
class OffsetStrE2EWorkflow:
    @workflow.entrypoint
    async def run(self) -> List[str]:
        return await execute_activities_in_parallel(
            activity=process_single_str,
            get_item_from_index_activity=get_str_by_index,
            n_items=3,
        )


@workflow.define(name="test-parallel-offset-kwargs-e2e")
class OffsetKwargsE2EWorkflow:
    @workflow.entrypoint
    async def run(self) -> List[str]:
        return await execute_activities_in_parallel(
            activity=process_kwargs_only,
            get_item_from_index_activity=get_kwargs_dict_by_index,
            n_items=3,
        )


@workflow.define(name="test-parallel-list-extra-keys-e2e")
class ListExtraKeysE2EWorkflow:
    @workflow.entrypoint
    async def run(self, input: ListMultiParamInput) -> List[str]:
        return await execute_activities_in_parallel(
            activity=process_multi_params,
            items=input.items,
        )


@workflow.define(name="test-parallel-chain-extra-keys-e2e")
class ChainExtraKeysE2EWorkflow:
    @workflow.entrypoint
    async def run(self) -> List[str]:
        return await execute_activities_in_parallel(
            activity=process_multi_params,
            get_item_from_prev_item_activity=get_next_dict_with_typo,
        )


@workflow.define(name="test-parallel-offset-extra-keys-e2e")
class OffsetExtraKeysE2EWorkflow:
    @workflow.entrypoint
    async def run(self) -> List[str]:
        return await execute_activities_in_parallel(
            activity=process_multi_params,
            get_item_from_index_activity=get_dict_with_typo_by_index,
            n_items=2,
        )


@workflow.define(name="test-parallel-list-missing-key-e2e")
class ListMissingKeyE2EWorkflow:
    @workflow.entrypoint
    async def run(self) -> List[str]:
        return await execute_activities_in_parallel(
            activity=process_multi_params,
            items=[{"name": "a"}],  # missing "count"
        )


@workflow.define(name="test-parallel-chain-missing-key-e2e")
class ChainMissingKeyE2EWorkflow:
    @workflow.entrypoint
    async def run(self) -> List[str]:
        return await execute_activities_in_parallel(
            activity=process_multi_params,
            get_item_from_prev_item_activity=get_next_dict_missing_key,
        )


@workflow.define(name="test-parallel-offset-missing-key-e2e")
class OffsetMissingKeyE2EWorkflow:
    @workflow.entrypoint
    async def run(self) -> List[str]:
        return await execute_activities_in_parallel(
            activity=process_multi_params,
            get_item_from_index_activity=get_dict_missing_key_by_index,
            n_items=2,
        )


class TestParallelActivitiesE2E:
    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_list_executor_with_str_items(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[ListStrE2EWorkflow, ParallelExecutionWorkflow],
            activities=[process_single_str],
        ):
            wf_def = get_workflow_definition(ListStrE2EWorkflow)
            handle = await temporal_env.client.start_workflow(
                wf_def.name, {"items": ["a", "b", "c"]}, id="test-parallel-list-str-e2e", task_queue="test-task-queue"
            )
            result = await handle.result()
            actual = result["result"] if isinstance(result, dict) else result
            assert sorted(actual) == ["hello_a", "hello_b", "hello_c"]

    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_list_executor_with_multi_params(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[ListMultiParamE2EWorkflow, ParallelExecutionWorkflow],
            activities=[process_multi_params],
        ):
            wf_def = get_workflow_definition(ListMultiParamE2EWorkflow)
            handle = await temporal_env.client.start_workflow(
                wf_def.name,
                {"items": [{"name": "x", "count": 1}, {"name": "y", "count": 2}]},
                id="test-parallel-list-multi-e2e",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            actual = result["result"] if isinstance(result, dict) else result
            assert sorted(actual) == ["x_1", "y_2"]

    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_list_executor_with_mixed_params(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[ListMixedParamE2EWorkflow, ParallelExecutionWorkflow],
            activities=[process_mixed_params],
        ):
            wf_def = get_workflow_definition(ListMixedParamE2EWorkflow)
            handle = await temporal_env.client.start_workflow(
                wf_def.name,
                {
                    "items": [
                        {"name": "x", "item": {"item_id": 1, "value": "a"}},
                        {"name": "y", "item": {"item_id": 2, "value": "b"}},
                    ]
                },
                id="test-parallel-list-mixed-e2e",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            actual = result["result"] if isinstance(result, dict) else result
            assert sorted(actual) == ["x_1_a", "y_2_b"]

    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_list_executor_with_pydantic_items(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[ListPydanticE2EWorkflow, ParallelExecutionWorkflow],
            activities=[process_pydantic_item],
        ):
            wf_def = get_workflow_definition(ListPydanticE2EWorkflow)
            handle = await temporal_env.client.start_workflow(
                wf_def.name,
                {"items": [{"item_id": 1, "value": "a"}, {"item_id": 2, "value": "b"}]},
                id="test-parallel-list-pydantic-e2e",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            actual = result["result"] if isinstance(result, dict) else result
            results_sorted = sorted(actual, key=lambda r: r["item_id"])
            assert results_sorted[0]["processed"] == "done_a"
            assert results_sorted[1]["processed"] == "done_b"

    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_list_executor_with_kwargs_only_activity(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[ListKwargsE2EWorkflow, ParallelExecutionWorkflow],
            activities=get_temporal_activities_by_names(["process_kwargs_only"]),
        ):
            wf_def = get_workflow_definition(ListKwargsE2EWorkflow)
            handle = await temporal_env.client.start_workflow(
                wf_def.name,
                {"items": [{"name": "x", "count": 1}, {"name": "y", "count": 2}]},
                id="test-parallel-list-kwargs-e2e",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            actual = result["result"] if isinstance(result, dict) else result
            assert sorted(actual) == ["x_1", "y_2"]

    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_chain_executor_with_str_items(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[ChainStrE2EWorkflow, ParallelExecutionWorkflow],
            activities=[process_single_str, get_next_str],
        ):
            wf_def = get_workflow_definition(ChainStrE2EWorkflow)
            handle = await temporal_env.client.start_workflow(
                wf_def.name, {}, id="test-parallel-chain-str-e2e", task_queue="test-task-queue"
            )
            result = await handle.result()
            actual = result["result"] if isinstance(result, dict) else result
            assert sorted(actual) == ["hello_item_0", "hello_item_1", "hello_item_2"]

    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_chain_executor_with_kwargs_only_activity(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[ChainKwargsE2EWorkflow, ParallelExecutionWorkflow],
            activities=get_temporal_activities_by_names(["process_kwargs_only", "get_next_kwargs_dict"]),
        ):
            wf_def = get_workflow_definition(ChainKwargsE2EWorkflow)
            handle = await temporal_env.client.start_workflow(
                wf_def.name, {}, id="test-parallel-chain-kwargs-e2e", task_queue="test-task-queue"
            )
            result = await handle.result()
            actual = result["result"] if isinstance(result, dict) else result
            assert sorted(actual) == ["item_0_0", "item_1_1", "item_2_2"]

    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_offset_executor_with_str_items(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[OffsetStrE2EWorkflow, ParallelExecutionWorkflow],
            activities=[process_single_str, get_str_by_index, execute_activity_in_batch],
        ):
            wf_def = get_workflow_definition(OffsetStrE2EWorkflow)
            handle = await temporal_env.client.start_workflow(
                wf_def.name, {}, id="test-parallel-offset-str-e2e", task_queue="test-task-queue"
            )
            result = await handle.result()
            actual = result["result"] if isinstance(result, dict) else result
            assert sorted(actual) == ["hello_item_0", "hello_item_1", "hello_item_2"]

    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_offset_executor_with_kwargs_only_activity(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[OffsetKwargsE2EWorkflow, ParallelExecutionWorkflow],
            activities=get_temporal_activities_by_names(["process_kwargs_only", "get_kwargs_dict_by_index"])
            + [execute_activity_in_batch],
        ):
            wf_def = get_workflow_definition(OffsetKwargsE2EWorkflow)
            handle = await temporal_env.client.start_workflow(
                wf_def.name, {}, id="test-parallel-offset-kwargs-e2e", task_queue="test-task-queue"
            )
            result = await handle.result()
            actual = result["result"] if isinstance(result, dict) else result
            assert sorted(actual) == ["item_0_0", "item_1_1", "item_2_2"]

    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_list_executor_extra_keys_raises_error(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[ListExtraKeysE2EWorkflow, ParallelExecutionWorkflow],
            activities=[process_multi_params],
        ):
            wf_def = get_workflow_definition(ListExtraKeysE2EWorkflow)
            handle = await temporal_env.client.start_workflow(
                wf_def.name,
                {"items": [{"name": "a", "countt": 1}]},  # typo: "countt"
                id="test-parallel-list-extra-keys-e2e",
                task_queue="test-task-queue",
            )
            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()
            # List executor catches extra keys in _validate_items (pre-validation)
            assert "not compatible" in str(exc_info.value.cause)

    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_chain_executor_extra_keys_raises_error(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[ChainExtraKeysE2EWorkflow, ParallelExecutionWorkflow],
            activities=[process_multi_params, get_next_dict_with_typo],
        ):
            wf_def = get_workflow_definition(ChainExtraKeysE2EWorkflow)
            handle = await temporal_env.client.start_workflow(
                wf_def.name, {}, id="test-parallel-chain-extra-keys-e2e", task_queue="test-task-queue"
            )
            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()
            # Chain executor: coerce_multi_params raises, unwrapped from ExceptionGroup
            assert "Unexpected keys" in exc_info.value.cause.cause.message

    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_offset_executor_extra_keys_raises_error(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[OffsetExtraKeysE2EWorkflow, ParallelExecutionWorkflow],
            activities=[process_multi_params, get_dict_with_typo_by_index, execute_activity_in_batch],
        ):
            wf_def = get_workflow_definition(OffsetExtraKeysE2EWorkflow)
            handle = await temporal_env.client.start_workflow(
                wf_def.name, {}, id="test-parallel-offset-extra-keys-e2e", task_queue="test-task-queue"
            )
            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()
            # Offset executor: ApplicationError extracted from nested ExceptionGroups
            assert "Unexpected keys" in exc_info.value.cause.cause.message

    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_list_executor_missing_key_raises_error(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[ListMissingKeyE2EWorkflow, ParallelExecutionWorkflow],
            activities=[process_multi_params],
        ):
            wf_def = get_workflow_definition(ListMissingKeyE2EWorkflow)
            handle = await temporal_env.client.start_workflow(
                wf_def.name, {}, id="test-parallel-list-missing-key-e2e", task_queue="test-task-queue"
            )
            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()
            # List executor validates items upfront via _validate_items / pydantic model_validate
            assert "count" in exc_info.value.cause.cause.message

    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_chain_executor_missing_key_raises_error(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[ChainMissingKeyE2EWorkflow, ParallelExecutionWorkflow],
            activities=[process_multi_params, get_next_dict_missing_key],
        ):
            wf_def = get_workflow_definition(ChainMissingKeyE2EWorkflow)
            handle = await temporal_env.client.start_workflow(
                wf_def.name, {}, id="test-parallel-chain-missing-key-e2e", task_queue="test-task-queue"
            )
            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()
            assert "Missing required keys" in exc_info.value.cause.cause.message

    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_offset_executor_missing_key_raises_error(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[OffsetMissingKeyE2EWorkflow, ParallelExecutionWorkflow],
            activities=[process_multi_params, get_dict_missing_key_by_index, execute_activity_in_batch],
        ):
            wf_def = get_workflow_definition(OffsetMissingKeyE2EWorkflow)
            handle = await temporal_env.client.start_workflow(
                wf_def.name, {}, id="test-parallel-offset-missing-key-e2e", task_queue="test-task-queue"
            )
            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()
            assert "Missing required keys" in exc_info.value.cause.cause.message
