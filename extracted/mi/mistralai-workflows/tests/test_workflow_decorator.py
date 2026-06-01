import pytest

from mistralai.workflows import get_workflow_definition, workflow
from mistralai.workflows.core.config.config import config
from mistralai.workflows.exceptions import WorkflowsException

from .fixtures import ParamsModel, ResultModel


class TestWorkflowDefineDecorator:
    def test_workflow_define_on_function_raises_error(self) -> None:
        with pytest.raises(WorkflowsException, match="only supports classes"):

            @workflow.define(name="test-workflow-func")  # pyright: ignore[reportGeneralTypeIssues]
            async def test_workflow_func(params: ParamsModel) -> ResultModel:
                return ResultModel(message="test")

    def test_workflow_entrypoint_sync_function_raises_error(self) -> None:
        with pytest.raises(WorkflowsException, match="must be async"):

            @workflow.entrypoint  # pyright: ignore[reportArgumentType]
            def sync_run(self: object, params: ParamsModel) -> ResultModel:
                return ResultModel(message="test")

    def test_workflow_name_prefix_applied(self) -> None:
        original_prefix = config.worker.workflow_name_prefix
        config.worker.workflow_name_prefix = "myprefix_"

        try:

            @workflow.define(name="test_workflow")
            class PrefixedWorkflow:
                @workflow.entrypoint
                async def run(self) -> str:
                    return "done"

            workflow_def = get_workflow_definition(PrefixedWorkflow)
            assert workflow_def is not None
            assert workflow_def.name == "myprefix_test_workflow"
        finally:
            config.worker.workflow_name_prefix = original_prefix
