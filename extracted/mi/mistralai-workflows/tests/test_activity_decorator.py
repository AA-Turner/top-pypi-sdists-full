import pytest
from pydantic import BaseModel, Field

from mistralai.workflows import activity
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException


class ParamsModel(BaseModel):
    name: str = Field(description="Test name")
    count: int = Field(default=1)


class ResultModel(BaseModel):
    message: str
    success: bool = True


class TestActivityDecorator:
    def test_activity_not_async_raises_error(self) -> None:
        with pytest.raises(WorkflowsException, match="must be async function") as exc:

            @activity()
            def sync_activity(params: ParamsModel) -> ResultModel:
                return ResultModel(message="test")

        assert exc.value.code == ErrorCode.ACTIVITY_DEFINITION_ERROR

    def test_activity_with_primitive_param_works(self) -> None:
        @activity()
        async def valid_activity_primitive_param(params: str) -> ResultModel:
            return ResultModel(message=params)

        assert valid_activity_primitive_param is not None

    def test_activity_with_primitive_return_works(self) -> None:
        @activity()
        async def valid_activity_primitive_return(params: ParamsModel) -> str:
            return "test"

        assert valid_activity_primitive_return is not None

    def test_activity_on_class_raises_error(self) -> None:
        with pytest.raises(WorkflowsException, match="only supports module-level functions") as exc:

            @activity()
            class NotAFunction:
                pass

        assert exc.value.code == ErrorCode.ACTIVITY_NOT_MODULE_LEVEL

    def test_activity_with_reserved_prefix_raises_error(self) -> None:
        with pytest.raises(WorkflowsException, match="uses reserved prefix '__internal__'") as exc:

            @activity(name="__internal__my_activity")
            async def reserved_activity(params: ParamsModel) -> ResultModel:
                return ResultModel(message="test")

        assert exc.value.code == ErrorCode.ACTIVITY_RESERVED_NAME

    def test_activity_with_reserved_prefix_in_function_name_raises_error(self) -> None:
        with pytest.raises(WorkflowsException, match="uses reserved prefix '__internal__'") as exc:

            @activity()
            async def __internal__another_activity(params: ParamsModel) -> ResultModel:
                return ResultModel(message="test")

        assert exc.value.code == ErrorCode.ACTIVITY_RESERVED_NAME
