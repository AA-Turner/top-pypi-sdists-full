from typing import Any

import pytest
import structlog
import temporalio
from pydantic import BaseModel

from mistralai.workflows.core.definition.validation._validator import (
    validate_query_handler_signature,
    validate_signal_handler_signature,
    validate_update_handler_signature,
)
from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition
from mistralai.workflows.core.workflow import (
    QueryDefinition,
    SignalDefinition,
    UpdateDefinition,
    workflow,
)
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException

logger = structlog.get_logger(__name__)


class SimpleInput(BaseModel):
    message: str


class SimpleOutput(BaseModel):
    reply: str


class AnotherInput(BaseModel):
    value: int


class SimplerWorkflowForSignalAndUpdate:
    @workflow.signal(name="TestSignal", description="A simple signal")
    async def handle_signal(self, data: SimpleInput) -> None:
        logger.info(f"Signal handled: {data.message}")

    @workflow.update(name="TestUpdate", description="A simple update")
    async def handle_update(self, data: SimpleInput) -> SimpleOutput:
        return SimpleOutput(reply=f"Updated with {data.message}")


def test_validate_signal_handler_valid_sync_no_param():
    def handler(self) -> None:
        pass

    validate_signal_handler_signature(handler)


def test_validate_signal_handler_valid_async_pydantic_param():
    async def handler(self, data: SimpleInput) -> None:
        pass

    validate_signal_handler_signature(handler)


def test_validate_signal_handler_valid_primitive_param():
    def handler(self, data: int) -> None:
        pass

    validate_signal_handler_signature(handler)


def test_validate_query_handler_invalid_async():
    async def handler(self) -> SimpleOutput:
        return SimpleOutput(reply="foo")

    with pytest.raises(WorkflowsException, match="must be a synchronous function") as exc:
        validate_query_handler_signature(handler)
    assert exc.value.code == ErrorCode.REJECTED_QUERY_ERROR


def test_validate_query_handler_invalid_no_return_type():
    def handler(self):
        return SimpleOutput(reply="foo")

    with pytest.raises(WorkflowsException, match="must have a return type annotation") as exc:
        validate_query_handler_signature(handler)
    assert exc.value.code == ErrorCode.ACTIVITY_DEFINITION_ERROR


def test_validate_query_handler_invalid_return_none():
    def handler(self) -> None:
        pass

    with pytest.raises(WorkflowsException, match="must have a return type annotation other than None") as exc:
        validate_query_handler_signature(handler)
    assert exc.value.code == ErrorCode.REJECTED_QUERY_ERROR


def test_signal_handler_attaches_metadata_and_temporal_decorator():
    # Test the module-level class method
    method_to_test = SimplerWorkflowForSignalAndUpdate.handle_signal

    logger.info(f"Testing method: {method_to_test}")
    logger.info(f"dir(method_to_test): {dir(method_to_test)}")
    try:
        # Try to access it directly to see the actual error if not found
        _ = method_to_test.__temporal_signal_definition
        logger.info("__temporal_signal_definition found via direct access.")
    except AttributeError:
        logger.error("__temporal_signal_definition NOT found via direct access.")

    assert hasattr(method_to_test, "__temporal_signal_definition"), (
        "__temporal_signal_definition should be set by Temporal's decorator"
    )

    # Check Abraxas metadata (this part should be fine if __temporal_... passes)
    abraxas_def = getattr(method_to_test, "__wf_signal_def", None)
    assert abraxas_def is not None, "__wf_signal_def should be set"
    assert isinstance(abraxas_def, SignalDefinition)
    assert abraxas_def.name == "TestSignal"
    assert abraxas_def.input_schema == SimpleInput.model_json_schema()

    # If the above hasattr passes, this should also pass
    if hasattr(method_to_test, "__temporal_signal_definition"):
        assert method_to_test.__temporal_signal_definition.name == "TestSignal"


def test_signal_handler_defaults_name_and_no_input_schema():
    class MyWorkflowSignalTestMinimal:
        @workflow.signal()
        async def another_signal(self) -> None:  # No input param
            pass

    abraxas_def = getattr(MyWorkflowSignalTestMinimal.another_signal, "__wf_signal_def", None)
    assert abraxas_def is not None
    assert abraxas_def.name == "another_signal"  # Defaults to method name
    assert abraxas_def.input_schema == {
        "additionalProperties": False,
        "properties": {},
        "title": "another_signal_Input",
        "type": "object",
    }

    assert hasattr(MyWorkflowSignalTestMinimal.another_signal, "__temporal_signal_definition")
    assert MyWorkflowSignalTestMinimal.another_signal.__temporal_signal_definition.name == "another_signal"


def test_query_handler_attaches_metadata_and_temporal_decorator():
    class MyWorkflowQueryTest:
        @workflow.query(name="GetStateQuery", description="Fetches current state")
        def get_current_state(self, params: SimpleInput) -> SimpleOutput:
            return SimpleOutput(reply=f"State for {params.message}")

    abraxas_def = getattr(MyWorkflowQueryTest.get_current_state, "__wf_query_def", None)
    assert abraxas_def is not None
    assert isinstance(abraxas_def, QueryDefinition)
    assert abraxas_def.name == "GetStateQuery"
    assert abraxas_def.description == "Fetches current state"
    assert abraxas_def.input_schema == SimpleInput.model_json_schema()
    assert abraxas_def.output_schema == SimpleOutput.model_json_schema()

    assert hasattr(MyWorkflowQueryTest.get_current_state, "__temporal_query_definition")
    assert MyWorkflowQueryTest.get_current_state.__temporal_query_definition.name == "GetStateQuery"


def test_validate_update_handler_valid_sync_no_param():
    def handler(self) -> SimpleOutput:
        return SimpleOutput(reply="foo")

    validate_update_handler_signature(handler)


def test_validate_update_handler_valid_async_pydantic_param():
    async def handler(self, data: SimpleInput) -> SimpleOutput:
        return SimpleOutput(reply=data.message)

    validate_update_handler_signature(handler)


def test_validate_update_handler_return_None():
    async def handler(self, data: SimpleInput):
        return SimpleOutput(reply="foo")

    with pytest.raises(WorkflowsException, match="must have a return type annotation") as exc:
        validate_update_handler_signature(handler)
    assert exc.value.code == ErrorCode.ACTIVITY_DEFINITION_ERROR


def test_validate_update_hander_return_None_on_workflow():
    with pytest.raises(WorkflowsException, match="must have a return type annotation") as exc:

        class TestWorkflowForUpdateError:
            @workflow.update(name="TestUpdate", description="A simple update")
            async def handle_update(self, data: SimpleInput):
                return SimpleOutput(reply=f"Updated with {data.message}")

    assert exc.value.code == ErrorCode.ACTIVITY_DEFINITION_ERROR


def test_update_handler_attaches_metadata_and_temporal_decorator():
    method_to_test = SimplerWorkflowForSignalAndUpdate.handle_update

    logger.info(f"Method to test: {method_to_test}")
    logger.info(f"dir(method_to_test): {dir(method_to_test)}")
    try:
        _ = method_to_test._defn
        logger.info("_defn found via direct access.")
    except AttributeError:
        logger.error("_defn NOT found via direct access.")

    assert hasattr(method_to_test, "_defn"), "_defn should be set by Temporal's decorator"

    abraxas_def = getattr(method_to_test, "__wf_update_def", None)
    assert abraxas_def is not None, "__wf_update_def should be set"
    assert isinstance(abraxas_def, UpdateDefinition)
    assert abraxas_def.name == "TestUpdate"
    assert abraxas_def.input_schema == SimpleInput.model_json_schema()
    assert abraxas_def.output_schema == SimpleOutput.model_json_schema()

    # If the above hasattr passes, this should also pass
    if hasattr(method_to_test, "__temporal_update_definition"):
        assert method_to_test.__temporal_update_definition.name == "TestUpdate"


@workflow.define(name="ComprehensiveWorkflow", workflow_description="Tests all handlers")
class MyComprehensiveWorkflow:
    # Entrypoint
    @workflow.entrypoint
    async def run(self, data: SimpleInput) -> SimpleOutput:
        # Pretend to do something
        await temporalio.workflow.sleep(0.1)
        return SimpleOutput(reply=f"Workflow run with {data.message}")

    # Signal
    @workflow.signal(name="UpdateValueSignal", description="Updates an internal value")
    async def update_value(self, new_val: AnotherInput) -> None:
        # Pretend to update
        logger.info(f"Signal received: {new_val.value}")

    # Query
    @workflow.query(name="FetchValueQuery", description="Fetches an internal value")
    def fetch_value(self) -> SimpleOutput:
        return SimpleOutput(reply="some_value")

    @workflow.update(name="Update", description="sends a update and except a reply")
    async def update(self, data: SimpleInput) -> SimpleOutput:
        # pretend to do something
        return SimpleOutput(reply=data.message)


def test_workflow_define_collects_all_definitions():
    wf_def = get_workflow_definition(MyComprehensiveWorkflow)
    assert wf_def is not None
    assert wf_def.name == "ComprehensiveWorkflow"
    assert wf_def.input_schema == SimpleInput.model_json_schema()
    assert wf_def.output_schema == SimpleOutput.model_json_schema()

    assert len(wf_def.signals) == 1
    signal_meta = wf_def.signals[0]
    assert signal_meta.name == "UpdateValueSignal"
    assert signal_meta.description == "Updates an internal value"
    assert signal_meta.input_schema == AnotherInput.model_json_schema()

    assert len(wf_def.queries) == 1
    query_meta = wf_def.queries[0]
    assert query_meta.name == "FetchValueQuery"
    assert query_meta.description == "Fetches an internal value"
    assert query_meta.input_schema == {
        "additionalProperties": False,
        "properties": {},
        "title": "fetch_value_Input",
        "type": "object",
    }
    assert query_meta.output_schema == SimpleOutput.model_json_schema()

    assert len(wf_def.updates) == 1
    update_meta = wf_def.updates[0]
    assert update_meta.name == "Update"
    assert update_meta.description == "sends a update and except a reply"
    assert update_meta.input_schema == SimpleInput.model_json_schema()
    assert update_meta.output_schema == SimpleOutput.model_json_schema()

    # Check if the class itself is recognized by Temporal
    assert hasattr(MyComprehensiveWorkflow, "__temporal_workflow_definition")


class TestSignalWithKwargs:
    def test_signal_with_explicit_params_and_kwargs(self) -> None:
        class MyWorkflow:
            @workflow.signal(name="flexible_signal")
            async def handle_signal(self, name: str, **kwargs: Any) -> None:
                pass

        signal_def = getattr(MyWorkflow.handle_signal, "__wf_signal_def", None)
        assert signal_def is not None
        assert signal_def.name == "flexible_signal"
        schema = signal_def.input_schema
        assert "name" in schema["properties"]

    def test_signal_with_only_kwargs(self) -> None:
        class MyWorkflow:
            @workflow.signal(name="dynamic_signal")
            async def handle_signal(self, **kwargs: Any) -> None:
                pass

        signal_def = getattr(MyWorkflow.handle_signal, "__wf_signal_def", None)
        assert signal_def is not None
        assert signal_def.name == "dynamic_signal"

    def test_sync_signal_with_kwargs(self) -> None:
        class MyWorkflow:
            @workflow.signal(name="sync_kwargs_signal")
            def handle_signal(self, name: str, **kwargs: Any) -> None:
                pass

        signal_def = getattr(MyWorkflow.handle_signal, "__wf_signal_def", None)
        assert signal_def is not None
        assert signal_def.name == "sync_kwargs_signal"


class TestQueryWithKwargs:
    def test_query_with_explicit_params_and_kwargs(self) -> None:
        class MyWorkflow:
            @workflow.query(name="flexible_query")
            def get_data(self, key: str, **kwargs: Any) -> dict:
                return {"key": key, **kwargs}

        query_def = getattr(MyWorkflow.get_data, "__wf_query_def", None)
        assert query_def is not None
        assert query_def.name == "flexible_query"
        schema = query_def.input_schema
        assert "key" in schema["properties"]

    def test_query_with_only_kwargs(self) -> None:
        class MyWorkflow:
            @workflow.query(name="dynamic_query")
            def get_data(self, **kwargs: Any) -> dict:
                return kwargs

        query_def = getattr(MyWorkflow.get_data, "__wf_query_def", None)
        assert query_def is not None
        assert query_def.name == "dynamic_query"


class TestUpdateWithKwargs:
    def test_update_with_explicit_params_and_kwargs(self) -> None:
        class MyWorkflow:
            @workflow.update(name="flexible_update")
            async def handle_update(self, name: str, **kwargs: Any) -> dict:
                return {"name": name, **kwargs}

        update_def = getattr(MyWorkflow.handle_update, "__wf_update_def", None)
        assert update_def is not None
        assert update_def.name == "flexible_update"
        schema = update_def.input_schema
        assert "name" in schema["properties"]

    def test_update_with_only_kwargs(self) -> None:
        class MyWorkflow:
            @workflow.update(name="dynamic_update")
            async def handle_update(self, **kwargs: Any) -> dict:
                return kwargs

        update_def = getattr(MyWorkflow.handle_update, "__wf_update_def", None)
        assert update_def is not None
        assert update_def.name == "dynamic_update"

    def test_sync_update_with_kwargs(self) -> None:
        class MyWorkflow:
            @workflow.update(name="sync_kwargs_update")
            def handle_update(self, value: int, **kwargs: Any) -> dict:
                return {"value": value, **kwargs}

        update_def = getattr(MyWorkflow.handle_update, "__wf_update_def", None)
        assert update_def is not None
        assert update_def.name == "sync_kwargs_update"


class TestKwargsHandlerInWorkflowDefine:
    def test_workflow_with_all_kwargs_handlers(self) -> None:
        from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition

        @workflow.define(name="test-kwargs-handlers-workflow")
        class KwargsWorkflow:
            @workflow.entrypoint
            async def run(self) -> None:
                pass

            @workflow.signal(name="kwargs_signal")
            async def my_signal(self, name: str, **kwargs: Any) -> None:
                pass

            @workflow.query(name="kwargs_query")
            def my_query(self, key: str, **kwargs: Any) -> dict:
                return {"key": key, **kwargs}

            @workflow.update(name="kwargs_update")
            async def my_update(self, value: int, **kwargs: Any) -> dict:
                return {"value": value, **kwargs}

        wf_def = get_workflow_definition(KwargsWorkflow)
        assert wf_def is not None
        assert len(wf_def.signals) == 1
        assert wf_def.signals[0].name == "kwargs_signal"
        assert len(wf_def.queries) == 1
        assert wf_def.queries[0].name == "kwargs_query"
        assert len(wf_def.updates) == 1
        assert wf_def.updates[0].name == "kwargs_update"
