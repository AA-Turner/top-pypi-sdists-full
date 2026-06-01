from typing import Any, Optional

import pytest
from pydantic import BaseModel, Field, ValidationError

import mistralai.workflows as workflows
from mistralai.workflows import workflow
from mistralai.workflows.core.definition.validation._validator import (
    get_function_signature_type_hints,
    raise_if_function_has_invalid_return_type,
    raise_if_function_has_invalid_signature,
    raise_if_function_has_invalid_usage,
)
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException
from mistralai.workflows.models import WORKFLOW_NAME_MAX_LENGTH, WorkflowSpec, WorkflowSpecWithTaskQueue
from mistralai.workflows.protocol.v1.workflow import EXECUTION_ID_MAX_LENGTH, WorkflowExecutionRequest


class ParamsModel(BaseModel):
    name: str = Field(description="Test name")
    count: int = Field(default=1)


class ResultModel(BaseModel):
    message: str
    success: bool = True


class TestGetFunctionSignatureTypeHints:
    def test_function_with_dependency_injection(self) -> None:
        from mistralai.workflows.core.dependencies.dependency_injector import Depends

        def get_service() -> str:
            return "service"

        async def test_func(params: ParamsModel, service: str = Depends(get_service)) -> ResultModel:
            return ResultModel(message="ok")

        params_dict, return_type, _ = get_function_signature_type_hints(test_func, is_method=False)

        # Should only count params, not dependency
        assert "params" in params_dict
        assert params_dict["params"] == ParamsModel
        assert "service" not in params_dict  # Depends params are filtered out
        assert return_type == ResultModel

    def test_function_without_type_annotation_raises_error(self) -> None:
        async def test_func(params) -> ResultModel:  # type: ignore[no-untyped-def]
            return ResultModel(message="ok")

        with pytest.raises(WorkflowsException, match="must have a type annotation") as exc:
            get_function_signature_type_hints(test_func, is_method=False)
        assert exc.value.code == ErrorCode.ACTIVITY_DEFINITION_ERROR

    def test_has_kwargs_detection(self) -> None:
        async def with_kwargs(name: str, **kwargs: Any) -> dict:
            return {}

        async def without_kwargs(name: str) -> dict:
            return {}

        _, _, has_kwargs_true = get_function_signature_type_hints(with_kwargs, is_method=False)
        _, _, has_kwargs_false = get_function_signature_type_hints(without_kwargs, is_method=False)

        assert has_kwargs_true is True
        assert has_kwargs_false is False

    def test_unwraps_activity_decorator(self):
        """WFL-1243: @workflows.activity loses type hints on Python 3.14+ (PEP 649)."""

        @workflows.activity(retry_policy_max_attempts=0, _skip_registering=True)
        async def uppercase(text: str) -> str:
            return text.upper()

        params, return_type, _has_kwargs = get_function_signature_type_hints(uppercase, is_method=False)
        assert "text" in params
        assert params["text"] is str
        assert return_type is str


class TestRaiseIfFunctionHasInvalidSignature:
    def test_sync_function_raises_error(self) -> None:
        def sync_func(params: ParamsModel) -> ResultModel:
            return ResultModel(message="sync")

        with pytest.raises(WorkflowsException, match="must be async function") as exc:
            raise_if_function_has_invalid_signature(sync_func, is_method=False)
        assert exc.value.code == ErrorCode.ACTIVITY_DEFINITION_ERROR

    def test_primitive_param_works(self) -> None:
        async def valid_func(name: str, count: int) -> dict:
            return {"name": name, "count": count}

        raise_if_function_has_invalid_signature(valid_func, is_method=False)

    def test_primitive_return_works(self) -> None:
        async def valid_func(params: ParamsModel) -> str:
            return "valid"

        raise_if_function_has_invalid_signature(valid_func, is_method=False)

    def test_invalid_pydantic_conversion_raises_error(self) -> None:
        class InvalidType:
            def __init__(self) -> None:
                self.value = "test"

        async def invalid_func(params: InvalidType) -> ResultModel:
            return ResultModel(message="ok")

        with pytest.raises(WorkflowsException, match="Cannot generate Pydantic model from parameters") as exc:
            raise_if_function_has_invalid_signature(invalid_func, is_method=False)
        assert exc.value.code == ErrorCode.ACTIVITY_DEFINITION_ERROR

    def test_invalid_return_type_pydantic_conversion_raises_error(self) -> None:
        class InvalidReturnType:
            def __init__(self) -> None:
                self.value = "test"

        async def invalid_func(params: ParamsModel) -> InvalidReturnType:
            return InvalidReturnType()

        with pytest.raises(WorkflowsException, match="Cannot generate Pydantic model from return type") as exc:
            raise_if_function_has_invalid_signature(invalid_func, is_method=False)
        assert exc.value.code == ErrorCode.ACTIVITY_DEFINITION_ERROR


class TestRaiseIfFunctionHasInvalidUsage:
    def test_kwargs_accepted_for_typed_params(self) -> None:
        """Calling with keyword arguments is valid Python even without **kwargs."""

        async def test_func(params: ParamsModel) -> ResultModel:
            return ResultModel(message="ok")

        # Should NOT raise - keyword arguments for typed params are valid
        raise_if_function_has_invalid_usage(test_func, (), {"params": ParamsModel(name="test")}, is_method=False)

    def test_unknown_kwargs_raises_error(self) -> None:
        """Unknown keyword arguments should raise when function doesn't have **kwargs."""

        async def test_func(name: str) -> dict:
            return {"name": name}

        with pytest.raises(WorkflowsException, match="unexpected keyword arguments") as exc:
            raise_if_function_has_invalid_usage(test_func, (), {"name": "test", "unknown": "value"}, is_method=False)
        assert exc.value.code == ErrorCode.INVALID_ARGUMENTS_ERROR

    def test_duplicate_positional_and_kwarg_raises_error(self) -> None:
        """Providing a param both positionally and as kwarg should raise."""

        async def test_func(name: str, count: int) -> dict:
            return {"name": name, "count": count}

        with pytest.raises(WorkflowsException, match="multiple values for parameter 'name'") as exc:
            raise_if_function_has_invalid_usage(test_func, ("test",), {"name": "other", "count": 5}, is_method=False)
        assert exc.value.code == ErrorCode.INVALID_ARGUMENTS_ERROR

    def test_wrong_param_type_raises_error(self) -> None:
        async def test_func(params: ParamsModel) -> ResultModel:
            return ResultModel(message="ok")

        with pytest.raises(WorkflowsException, match="should be of type") as exc:
            raise_if_function_has_invalid_usage(test_func, ("wrong_type",), {}, is_method=False)
        assert exc.value.code == ErrorCode.INVALID_ARGUMENTS_ERROR

    def test_wrong_param_type_via_kwarg_raises_error(self) -> None:
        async def test_func(params: ParamsModel) -> ResultModel:
            return ResultModel(message="ok")

        with pytest.raises(WorkflowsException, match="should be of type") as exc:
            raise_if_function_has_invalid_usage(test_func, (), {"params": "wrong_type"}, is_method=False)
        assert exc.value.code == ErrorCode.INVALID_ARGUMENTS_ERROR

    def test_wrong_param_count_raises_error(self) -> None:
        async def test_func(param1: ParamsModel, param2: str) -> ResultModel:
            return ResultModel(message="ok")

        with pytest.raises(WorkflowsException, match="missing required parameter: 'param2'") as exc:
            raise_if_function_has_invalid_usage(test_func, (ParamsModel(name="test"),), {}, is_method=False)
        assert exc.value.code == ErrorCode.INVALID_ARGUMENTS_ERROR

    def test_kwargs_for_typed_params_without_var_keyword(self) -> None:
        """The exact scenario from WFL-695: typed params called with kwargs should work."""

        async def test_func(name: str, age: int) -> dict:
            return {"message": f"Hello {name}!"}

        # All as kwargs - should work
        raise_if_function_has_invalid_usage(test_func, (), {"name": "test", "age": 8}, is_method=False)

        # Mixed positional and kwargs - should work
        raise_if_function_has_invalid_usage(test_func, ("test",), {"age": 8}, is_method=False)

    def test_kwargs_allowed_for_var_keyword_function(self) -> None:
        async def test_func(name: str, **kwargs: Any) -> dict:
            return {"name": name, **kwargs}

        raise_if_function_has_invalid_usage(test_func, ("test",), {"extra": "value"}, is_method=False)

    def test_kwargs_function_counts_positional_and_keyword_args(self) -> None:
        """Parameters can be provided via positional args OR kwargs."""

        async def test_func(name: str, count: int, **kwargs: Any) -> dict:
            return {"name": name, "count": count, **kwargs}

        # All positional
        raise_if_function_has_invalid_usage(test_func, ("test", 5), {}, is_method=False)

        # All as kwargs
        raise_if_function_has_invalid_usage(test_func, (), {"name": "test", "count": 5}, is_method=False)

        # Mixed positional and kwargs
        raise_if_function_has_invalid_usage(test_func, ("test",), {"count": 5, "extra": "value"}, is_method=False)

    def test_kwargs_function_missing_required_params_raises_error(self) -> None:
        """Missing required params should raise even with **kwargs."""

        async def test_func(name: str, count: int, **kwargs: Any) -> dict:
            return {"name": name, "count": count, **kwargs}

        # Missing 'count' - only 1 of 2 required params provided
        with pytest.raises(WorkflowsException, match="missing required parameter: 'count'") as exc:
            raise_if_function_has_invalid_usage(test_func, ("test",), {"extra": "value"}, is_method=False)
        assert exc.value.code == ErrorCode.INVALID_ARGUMENTS_ERROR

    def test_kwargs_function_optional_param_does_not_satisfy_required(self) -> None:
        """Providing optional param via kwargs should not satisfy a different required param."""

        async def test_func(query: str, limit: int = 10, **kwargs: Any) -> dict:
            return {"query": query, "limit": limit, **kwargs}

        # Providing 'limit' (optional) and 'extra' but missing 'query' (required)
        with pytest.raises(WorkflowsException, match="missing required parameter: 'query'") as exc:
            raise_if_function_has_invalid_usage(test_func, (), {"limit": 5, "extra": "value"}, is_method=False)
        assert exc.value.code == ErrorCode.INVALID_ARGUMENTS_ERROR

    def test_kwargs_function_too_many_positional_raises_error(self) -> None:
        """Too many positional args should raise error."""

        async def test_func(name: str, **kwargs: Any) -> dict:
            return {"name": name, **kwargs}

        # 2 positional args but only 1 explicit param
        with pytest.raises(WorkflowsException, match="expects at most 1 positional parameters") as exc:
            raise_if_function_has_invalid_usage(test_func, ("test", "extra"), {}, is_method=False)
        assert exc.value.code == ErrorCode.INVALID_ARGUMENTS_ERROR

    def test_only_kwargs_function_accepts_any_kwargs(self) -> None:
        """Function with only **kwargs should accept any kwargs."""

        async def test_func(**kwargs: Any) -> dict:
            return kwargs

        # No params required
        raise_if_function_has_invalid_usage(test_func, (), {}, is_method=False)

        # Any kwargs accepted
        raise_if_function_has_invalid_usage(test_func, (), {"a": 1, "b": 2, "c": 3}, is_method=False)


class TestRaiseIfFunctionHasInvalidReturnType:
    def test_wrong_return_type_raises_error(self) -> None:
        async def test_func(params: ParamsModel) -> ResultModel:
            return ResultModel(message="ok")

        with pytest.raises(WorkflowsException, match="return type validation failed") as exc:
            raise_if_function_has_invalid_return_type(test_func, "wrong_type", is_method=False)
        assert exc.value.code == ErrorCode.ACTIVITY_DEFINITION_ERROR

    def test_pydantic_model_validation_error(self) -> None:
        async def test_func(params: ParamsModel) -> ResultModel:
            return ResultModel(message="ok")

        with pytest.raises(WorkflowsException, match="return type validation failed"):
            raise_if_function_has_invalid_return_type(test_func, {"invalid": "structure"}, is_method=False)

    def test_generic_list_return_type_works(self) -> None:
        async def test_func_list_str(offset: int, limit: int) -> list[str]:
            return ["item1", "item2", "item3"]

        # This should not raise TypeError
        result = ["item1", "item2", "item3"]
        raise_if_function_has_invalid_return_type(test_func_list_str, result, is_method=False)

    def test_generic_dict_return_type_works(self) -> None:
        async def test_func_dict(key: str) -> dict[str, int]:
            return {"count": 42}

        result = {"count": 42}
        raise_if_function_has_invalid_return_type(test_func_dict, result, is_method=False)

    def test_generic_optional_list_return_type_works(self) -> None:
        async def test_func_optional_list(query: str) -> Optional[list[str]]:
            return ["result1", "result2"]

        result = ["result1", "result2"]
        raise_if_function_has_invalid_return_type(test_func_optional_list, result, is_method=False)

        raise_if_function_has_invalid_return_type(test_func_optional_list, None, is_method=False)

    def test_list_with_wrong_element_type_raises_error(self) -> None:
        async def test_func_list_str(offset: int, limit: int) -> list[str]:
            return ["item1", "item2", "item3"]

        with pytest.raises(WorkflowsException, match="return type validation failed") as exc:
            raise_if_function_has_invalid_return_type(test_func_list_str, [1, 2, 3], is_method=False)
        assert exc.value.code == ErrorCode.ACTIVITY_DEFINITION_ERROR

    def test_list_with_mixed_element_types_raises_error(self) -> None:
        async def test_func_list_str(offset: int, limit: int) -> list[str]:
            return ["item1", "item2", "item3"]

        with pytest.raises(WorkflowsException, match="return type validation failed") as exc:
            raise_if_function_has_invalid_return_type(test_func_list_str, ["str", 1, 2], is_method=False)
        assert exc.value.code == ErrorCode.ACTIVITY_DEFINITION_ERROR

    def test_dict_with_wrong_value_type_raises_error(self) -> None:
        async def test_func_dict(key: str) -> dict[str, int]:
            return {"count": 42}

        with pytest.raises(WorkflowsException, match="return type validation failed") as exc:
            raise_if_function_has_invalid_return_type(test_func_dict, {"count": "not_an_int"}, is_method=False)
        assert exc.value.code == ErrorCode.ACTIVITY_DEFINITION_ERROR

    def test_nested_list_dict_validation(self) -> None:
        async def test_func_nested(query: str) -> list[dict[str, int]]:
            return [{"count": 1}, {"count": 2}]

        raise_if_function_has_invalid_return_type(test_func_nested, [{"count": 1}, {"count": 2}], is_method=False)

        with pytest.raises(WorkflowsException, match="return type validation failed"):
            raise_if_function_has_invalid_return_type(test_func_nested, [{"count": "wrong"}], is_method=False)

    def test_tuple_fixed_length_validation(self) -> None:
        async def test_func_tuple(query: str) -> tuple[str, int, bool]:
            return ("test", 42, True)

        raise_if_function_has_invalid_return_type(test_func_tuple, ("test", 42, True), is_method=False)

        with pytest.raises(WorkflowsException, match="return type validation failed"):
            raise_if_function_has_invalid_return_type(test_func_tuple, ("test", "wrong", True), is_method=False)

        with pytest.raises(WorkflowsException, match="return type validation failed"):
            raise_if_function_has_invalid_return_type(test_func_tuple, ("test", 42), is_method=False)

    def test_tuple_variable_length_validation(self) -> None:
        async def test_func_tuple(query: str) -> tuple[str, ...]:
            return ("a", "b", "c")

        raise_if_function_has_invalid_return_type(test_func_tuple, ("a", "b", "c"), is_method=False)

        with pytest.raises(WorkflowsException, match="return type validation failed"):
            raise_if_function_has_invalid_return_type(test_func_tuple, ("a", 1, "c"), is_method=False)

    def test_set_validation(self) -> None:
        async def test_func_set(query: str) -> set[str]:
            return {"a", "b", "c"}

        raise_if_function_has_invalid_return_type(test_func_set, {"a", "b", "c"}, is_method=False)

        with pytest.raises(WorkflowsException, match="return type validation failed"):
            raise_if_function_has_invalid_return_type(test_func_set, {1, 2, 3}, is_method=False)

    def test_frozenset_validation(self) -> None:
        async def test_func_frozenset(query: str) -> frozenset[int]:
            return frozenset([1, 2, 3])

        raise_if_function_has_invalid_return_type(test_func_frozenset, frozenset([1, 2, 3]), is_method=False)

        with pytest.raises(WorkflowsException, match="return type validation failed"):
            raise_if_function_has_invalid_return_type(test_func_frozenset, frozenset(["a", "b"]), is_method=False)

    def test_union_validation(self) -> None:
        async def test_func_union(query: str) -> str | int:
            return "test"

        raise_if_function_has_invalid_return_type(test_func_union, "test", is_method=False)

        raise_if_function_has_invalid_return_type(test_func_union, 42, is_method=False)

        with pytest.raises(WorkflowsException, match="return type validation failed"):
            raise_if_function_has_invalid_return_type(test_func_union, [], is_method=False)

    def test_deeply_nested_validation(self) -> None:
        async def test_func_deep(query: str) -> dict[str, list[tuple[int, str]]]:
            return {"key": [(1, "a"), (2, "b")]}

        raise_if_function_has_invalid_return_type(test_func_deep, {"key": [(1, "a"), (2, "b")]}, is_method=False)

        with pytest.raises(WorkflowsException, match="return type validation failed"):
            raise_if_function_has_invalid_return_type(test_func_deep, {"key": [(1, 2), (2, "b")]}, is_method=False)


class TestQueryHandlerValidation:
    def test_async_query_handler_raises_error(self) -> None:
        with pytest.raises(WorkflowsException, match="Query.*must be a synchronous function"):

            @workflow.define(name="test_workflow")
            class TestWorkflow:
                @workflow.entrypoint
                async def run(self) -> None:
                    pass

                @workflow.query()
                async def async_query(self) -> str:
                    return "test"

    def test_query_with_invalid_return_type_schema(self) -> None:
        class InvalidType:
            value: str

        with pytest.raises(WorkflowsException, match="has invalid return type for schema generation"):

            @workflow.define(name="test_workflow")
            class TestWorkflow:
                @workflow.entrypoint
                async def run(self) -> None:
                    pass

                @workflow.query()
                def invalid_query(self) -> InvalidType:
                    return InvalidType()


class TestReservedHandlerNames:
    def test_reserved_query_name_raises_error(self) -> None:
        with pytest.raises(ValueError, match="Query name '__get_pending_inputs' is reserved by the framework"):

            @workflow.define(name="test_workflow_reserved_query")
            class TestWorkflow:
                @workflow.entrypoint
                async def run(self) -> None:
                    pass

                @workflow.query(name="__get_pending_inputs")
                def bad_query(self) -> dict:
                    return {}

    def test_reserved_update_name_raises_error(self) -> None:
        with pytest.raises(ValueError, match="Update name '__submit_input' is reserved by the framework"):

            @workflow.define(name="test_workflow_reserved_update")
            class TestWorkflow:
                @workflow.entrypoint
                async def run(self) -> None:
                    pass

                @workflow.update(name="__submit_input")
                async def bad_update(self, data: dict) -> dict:
                    return {}


class TestWorkflowNameValidation:
    def test_valid_workflow_names(self) -> None:
        valid_names = [
            "my_workflow",
            "my-workflow",
            "MyWorkflow",
            "workflow123",
            "123workflow",
            "a",
            "A",
            "1",
            "my_workflow-name_123",
            "UPPERCASE_WORKFLOW",
            "-my_workflow",
            "_my_workflow",
            "__shared-workflow",
        ]
        for name in valid_names:
            spec = WorkflowSpec(name=name, input_schema={})
            assert spec.name == name

    def test_invalid_workflow_name_with_spaces(self) -> None:
        with pytest.raises(ValidationError, match="Workflow name.*is invalid"):
            WorkflowSpec(name="my workflow")

    def test_invalid_workflow_name_with_special_chars(self) -> None:
        invalid_names = [
            "my@workflow",
            "my#workflow",
            "my$workflow",
            "my%workflow",
            "my&workflow",
            "my*workflow",
            "my.workflow",
            "my/workflow",
            "my:workflow",
            "my;workflow",
            "my=workflow",
            "my?workflow",
            "my!workflow",
            "my+workflow",
            # UTF-8 special characters
            "my\u200bworkflow",  # Zero-width space
            "my🚀workflow",  # Emoji
            "myработаflow",  # Cyrillic
            "my工作流workflow",  # Chinese
        ]
        for name in invalid_names:
            with pytest.raises(ValidationError, match="Workflow name.*is invalid"):
                WorkflowSpec(name=name)

    def test_empty_workflow_name(self) -> None:
        with pytest.raises(ValidationError, match="Workflow name cannot be empty"):
            WorkflowSpec(name="")

    def test_workflow_name_max_length(self) -> None:
        name = "a" * WORKFLOW_NAME_MAX_LENGTH
        spec = WorkflowSpec(name=name, input_schema={})
        assert spec.name == name
        assert len(spec.name) == WORKFLOW_NAME_MAX_LENGTH

    def test_workflow_name_exceeds_max_length(self) -> None:
        name = "a" * (WORKFLOW_NAME_MAX_LENGTH + 1)
        with pytest.raises(ValidationError, match="String should have at most 128 characters"):
            WorkflowSpec(name=name)

    def test_workflow_spec_with_task_queue_inherits_validation(self) -> None:
        # Valid name should work
        spec = WorkflowSpecWithTaskQueue(name="valid_workflow", task_queue="my-queue", input_schema={})
        assert spec.name == "valid_workflow"

        # Invalid name should be rejected
        with pytest.raises(ValidationError, match="Workflow name.*is invalid"):
            WorkflowSpecWithTaskQueue(name="invalid@name", task_queue="my-queue")


class TestExecutionIdValidation:
    def test_valid_execution_ids(self) -> None:
        valid_ids = [
            "my-execution-id",
            "my_execution_id",
            "MyExecutionId123",
            "123",
            "a",
            "A",
            "execution-id-2024",
            "test_run_001",
            "wf-customer-123",
            "-leading-dash",
            "_leading-underscore",
            "a" * EXECUTION_ID_MAX_LENGTH,
        ]
        for exec_id in valid_ids:
            request = WorkflowExecutionRequest(execution_id=exec_id)
            assert request.execution_id == exec_id

    def test_none_execution_id_allowed(self) -> None:
        request = WorkflowExecutionRequest(execution_id=None)
        assert request.execution_id is None

    def test_default_execution_id_is_none(self) -> None:
        request = WorkflowExecutionRequest()
        assert request.execution_id is None

    def test_invalid_execution_id_with_spaces(self) -> None:
        with pytest.raises(ValidationError, match="Execution ID.*is invalid"):
            WorkflowExecutionRequest(execution_id="my execution")

    def test_invalid_execution_id_with_special_chars(self) -> None:
        invalid_ids = [
            "my@execution",
            "my#execution",
            "my$execution",
            "my.execution",
            "my/execution",
            "my:execution",
            "my!execution",
            "my+execution",
            "my\u200bexecution",  # Zero-width space
        ]
        for exec_id in invalid_ids:
            with pytest.raises(ValidationError, match="Execution ID is invalid"):
                WorkflowExecutionRequest(execution_id=exec_id)

    def test_empty_execution_id_raises_error(self) -> None:
        with pytest.raises(ValidationError, match="Execution ID is invalid"):
            WorkflowExecutionRequest(execution_id="")

    def test_execution_id_exceeds_max_length(self) -> None:
        exec_id = "a" * (EXECUTION_ID_MAX_LENGTH + 1)
        with pytest.raises(ValidationError, match="String should have at most 256 characters"):
            WorkflowExecutionRequest(execution_id=exec_id)


class TestActivityDecoratorValidation:
    """Tests that the @activity() decorator correctly validates function signatures."""

    def test_valid_activities_pass(self) -> None:
        from mistralai.workflows.core.dependencies.dependency_injector import Depends

        async def get_mock_dependency() -> str:
            return "mock_value"

        @workflows.activity()
        async def valid_activity_with_deps(
            params: ParamsModel, dep: str = Depends(dependency=get_mock_dependency)
        ) -> None:
            pass

        @workflows.activity()
        async def valid_activity_no_params() -> None:
            pass

        @workflows.activity()
        async def valid_activity_one_param(params: ParamsModel) -> None:
            pass

        assert valid_activity_with_deps is not None
        assert valid_activity_no_params is not None
        assert valid_activity_one_param is not None

    def test_invalid_activity_with_default_param(self) -> None:

        with pytest.raises(WorkflowsException, match="must have a type annotation") as exc:

            @workflows.activity()
            async def bad_activity_default(params: ParamsModel, bad_default="test") -> None:
                pass

        assert exc.value.code == ErrorCode.ACTIVITY_DEFINITION_ERROR

    def test_invalid_activity_with_dependencies_none(self) -> None:

        with pytest.raises(WorkflowsException, match="must have a type annotation") as exc:

            @workflows.activity()
            async def bad_activity_deps_none(params: ParamsModel, dependencies=None) -> None:
                pass

        assert exc.value.code == ErrorCode.ACTIVITY_DEFINITION_ERROR

    def test_invalid_activity_with_multiple_defaults(self) -> None:

        with pytest.raises(WorkflowsException, match="must have a type annotation") as exc:

            @workflows.activity()
            async def bad_activity_multiple(params: ParamsModel, flag=True, timeout=30) -> None:
                pass

        assert exc.value.code == ErrorCode.ACTIVITY_DEFINITION_ERROR

    def test_workflow_with_bad_activity(self) -> None:

        with pytest.raises(WorkflowsException, match="must have a type annotation") as exc:

            @workflows.activity()
            async def bad_example_manual_dependencies_none(params: ParamsModel, dependencies=None) -> None:
                pass

        assert exc.value.code == ErrorCode.ACTIVITY_DEFINITION_ERROR
