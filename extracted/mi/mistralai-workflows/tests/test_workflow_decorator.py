from datetime import timedelta

import pytest

from mistralai.workflows import get_workflow_definition, workflow
from mistralai.workflows.core.config.config import config
from mistralai.workflows.exceptions import WorkflowsException
from mistralai.workflows.models.workflow import WORKFLOW_TAG_MAX_LENGTH
from mistralai.workflows.protocol.v1.workflow import WorkflowUpdateRequest

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

    def test_unprepared_definition_ignores_loaded_legacy_config(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(config.worker, "workflow_name_prefix", "myprefix_")

        @workflow.define(name="test_workflow")
        class PrefixedWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        assert get_workflow_definition(PrefixedWorkflow).name == "test_workflow"

    @pytest.mark.parametrize(
        "extra_positional",
        [("Some description",), (None, []), (True,)],
        ids=["v3-description", "v3-description-and-schedules", "is-technical"],
    )
    def test_workflow_define_rejects_positional_args_after_name(self, extra_positional: tuple[object, ...]) -> None:
        # v3 accepted (name, workflow_description, schedules, ...); a v3 call must not shift into is_technical.
        with pytest.raises(TypeError, match="positional argument"):
            workflow.define("test-workflow-positional", *extra_positional)  # pyright: ignore[reportCallIssue]

    def test_workflow_define_accepts_keyword_args(self) -> None:
        @workflow.define(
            "test-workflow-keywords",
            is_technical=True,
            enforce_determinism=False,
            execution_timeout=timedelta(minutes=5),
        )
        class KeywordWorkflow:
            @workflow.entrypoint
            async def run(self) -> str:
                return "done"

        definition = get_workflow_definition(KeywordWorkflow)
        assert definition.name == "test-workflow-keywords"
        assert definition.is_technical is True
        assert definition.enforce_determinism is False
        assert definition.execution_timeout == timedelta(minutes=5)


class TestWorkflowUpdateRequestTagValidation:
    def test_tags_none_is_allowed(self) -> None:
        req = WorkflowUpdateRequest(tags=None)
        assert req.tags is None

    def test_tags_empty_list_is_allowed(self) -> None:
        req = WorkflowUpdateRequest(tags=[])
        assert req.tags == []

    def test_tags_strip_whitespace(self) -> None:
        req = WorkflowUpdateRequest(tags=["  idp  ", "ocr"])
        assert req.tags == ["idp", "ocr"]

    def test_tag_too_long_raises(self) -> None:
        with pytest.raises(ValueError, match=f"at most {WORKFLOW_TAG_MAX_LENGTH} characters"):
            WorkflowUpdateRequest(tags=["a" * (WORKFLOW_TAG_MAX_LENGTH + 1)])

    def test_empty_tag_raises(self) -> None:
        with pytest.raises(ValueError, match="empty or whitespace"):
            WorkflowUpdateRequest(tags=[""])

    def test_whitespace_only_tag_raises(self) -> None:
        with pytest.raises(ValueError, match="empty or whitespace"):
            WorkflowUpdateRequest(tags=["   "])
