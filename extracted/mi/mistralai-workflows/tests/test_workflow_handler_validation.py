import warnings
from datetime import timedelta
from typing import Any

import pytest

from mistralai.workflows import workflow
from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition
from mistralai.workflows.exceptions import WorkflowsException
from mistralai.workflows.models import ScheduleDefinition, ScheduleInterval


class TestSignalHandlerValidation:
    def test_signal_with_invalid_param_schema_raises_error(self) -> None:
        class InvalidType:
            value: str

        with pytest.raises(WorkflowsException, match="has invalid parameters for schema generation"):

            @workflow.define(name="test_workflow")
            class TestWorkflow:
                @workflow.entrypoint
                async def run(self) -> None:
                    pass

                @workflow.signal()
                async def invalid_signal(self, data: InvalidType) -> None:
                    pass

    def test_signal_with_kwargs_is_accepted(self) -> None:
        """Signal handlers should accept **kwargs."""

        @workflow.define(name="test-signal-kwargs-ok")
        class TestWorkflow:
            @workflow.entrypoint
            async def run(self) -> None:
                pass

            @workflow.signal()
            async def my_signal(self, name: str, **kwargs: Any) -> None:
                pass

        # Verify the signal was registered
        signal_def = getattr(TestWorkflow.my_signal, "__wf_signal_def", None)
        assert signal_def is not None
        assert signal_def.name == "my_signal"


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

    def test_query_with_none_return_raises_error(self) -> None:
        with pytest.raises(WorkflowsException, match="must have a return type annotation other than None"):

            @workflow.define(name="test_workflow")
            class TestWorkflow:
                @workflow.entrypoint
                async def run(self) -> None:
                    pass

                @workflow.query()
                def none_query(self) -> None:
                    pass

    def test_query_with_kwargs_is_accepted(self) -> None:
        """Query handlers should accept **kwargs."""

        @workflow.define(name="test-query-kwargs-ok")
        class TestWorkflow:
            @workflow.entrypoint
            async def run(self) -> None:
                pass

            @workflow.query()
            def my_query(self, name: str, **kwargs: Any) -> str:
                return name

        # Verify the query was registered
        query_def = getattr(TestWorkflow.my_query, "__wf_query_def", None)
        assert query_def is not None
        assert query_def.name == "my_query"


class TestUpdateHandlerValidation:
    def test_update_with_invalid_param_schema_raises_error(self) -> None:
        class InvalidType:
            value: str

        with pytest.raises(WorkflowsException, match="has invalid parameters for schema generation"):

            @workflow.define(name="test_workflow")
            class TestWorkflow:
                @workflow.entrypoint
                async def run(self) -> None:
                    pass

                @workflow.update()
                async def invalid_update(self, data: InvalidType) -> str:
                    return "test"

    def test_update_with_none_return_raises_error(self) -> None:
        with pytest.raises(WorkflowsException, match="must have a return type annotation other than None"):

            @workflow.define(name="test_workflow")
            class TestWorkflow:
                @workflow.entrypoint
                async def run(self) -> None:
                    pass

                @workflow.update()
                async def none_update(self) -> None:
                    pass

    def test_update_with_kwargs_is_accepted(self) -> None:
        """Update handlers should accept **kwargs."""

        @workflow.define(name="test-update-kwargs-ok")
        class TestWorkflow:
            @workflow.entrypoint
            async def run(self) -> None:
                pass

            @workflow.update()
            async def my_update(self, name: str, **kwargs: Any) -> str:
                return name

        # Verify the update was registered
        update_def = getattr(TestWorkflow.my_update, "__wf_update_def", None)
        assert update_def is not None
        assert update_def.name == "my_update"


class TestWorkflowEntrypointValidation:
    def test_missing_entrypoint_raises_error(self) -> None:
        with pytest.raises(WorkflowsException, match="must have an entrypoint method"):

            @workflow.define(name="test_workflow")
            class TestWorkflow:
                async def some_other_method(self) -> None:
                    pass

    def test_sync_entrypoint_raises_error(self) -> None:
        with pytest.raises(WorkflowsException, match="must be async"):

            @workflow.define(name="test_workflow")
            class TestWorkflow:
                @workflow.entrypoint  # pyright: ignore[reportArgumentType]
                def run(self) -> None:
                    pass

    def test_entrypoint_with_invalid_param_schema_raises_error(self) -> None:
        class InvalidType:
            value: str

        with pytest.raises(WorkflowsException, match="Cannot generate Pydantic model from parameters"):

            @workflow.define(name="test_workflow")
            class TestWorkflow:
                @workflow.entrypoint
                async def run(self, data: InvalidType) -> None:
                    pass

    def test_workflow_define_on_non_class_raises_error(self) -> None:
        with pytest.raises(WorkflowsException, match="only supports classes"):

            @workflow.define(name="test")  # pyright: ignore[reportGeneralTypeIssues]
            async def some_function() -> None:
                pass

    def test_entrypoint_method_name_is_preserved(self) -> None:
        @workflow.define(name="test_workflow")
        class TestWorkflow:
            @workflow.entrypoint
            async def execute(self) -> None:
                pass

        assert hasattr(TestWorkflow, "execute")
        assert callable(TestWorkflow.execute)


class TestOnBehalfOfValidation:
    def test_on_behalf_of_with_schedules_raises_error(self) -> None:
        with pytest.raises(WorkflowsException, match="on_behalf_of=True cannot be combined with schedules"):

            @workflow.define(
                name="test-obo-with-schedule",
                on_behalf_of=True,
                schedules=[ScheduleDefinition(input={}, intervals=[ScheduleInterval(every=timedelta(hours=1))])],
            )
            class TestWorkflow:
                @workflow.entrypoint
                async def run(self) -> None:
                    pass

    def test_on_behalf_of_without_schedules_succeeds(self) -> None:
        @workflow.define(name="test-obo-no-schedule", on_behalf_of=True)
        class TestWorkflow:
            @workflow.entrypoint
            async def run(self) -> None:
                pass

        spec = get_workflow_definition(TestWorkflow)
        assert spec.on_behalf_of is True

    def test_on_behalf_of_defaults_to_false(self) -> None:
        @workflow.define(name="test-obo-default")
        class TestWorkflow:
            @workflow.entrypoint
            async def run(self) -> None:
                pass

        spec = get_workflow_definition(TestWorkflow)
        assert spec.on_behalf_of is False


class TestSchedulesDeprecation:
    """Tests for schedules parameter deprecation."""

    def test_schedules_parameter_emits_deprecation_warning(self) -> None:
        """Using schedules parameter should emit a DeprecationWarning."""
        with pytest.warns(
            DeprecationWarning,
            match="schedules.*parameter.*deprecated.*will be removed in the next major release",
        ):

            @workflow.define(
                name="test-schedules-deprecated",
                schedules=[ScheduleDefinition(input={}, intervals=[ScheduleInterval(every=timedelta(hours=1))])],
            )
            class TestWorkflow:
                @workflow.entrypoint
                async def run(self) -> None:
                    pass

        spec = get_workflow_definition(TestWorkflow)
        assert len(spec.schedules) == 1

    def test_no_warning_without_schedules(self) -> None:
        """Not using schedules parameter should not emit a warning."""
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter("always")

            @workflow.define(name="test-no-schedules")
            class TestWorkflow:
                @workflow.entrypoint
                async def run(self) -> None:
                    pass

            spec = get_workflow_definition(TestWorkflow)
            assert len(spec.schedules) == 0

        # Verify no DeprecationWarning was raised
        assert not any(issubclass(w.category, DeprecationWarning) for w in warning_list)
