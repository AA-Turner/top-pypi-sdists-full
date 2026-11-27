from unittest.mock import AsyncMock, patch

import pytest
from pydantic import BaseModel, Field
from temporalio.exceptions import ApplicationError

from mistralai.workflows import activity
from mistralai.workflows.core.activity import get_all_temporal_activities
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.rate_limiting.rate_limit import (
    RateLimit,
    clear_rate_limit,
    get_rate_limit,
    set_rate_limit,
)
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException


class ParamsModel(BaseModel):
    name: str = Field(description="Test name")
    count: int = Field(default=1)


class ResultModel(BaseModel):
    message: str
    success: bool = True


_attempts: list[str] = []


@activity(retry_policy_max_attempts=3)
async def fails_for_good(params: str) -> str:
    _attempts.append(params)
    raise ApplicationError("will not work", non_retryable=True)


@activity(retry_policy_max_attempts=3)
async def fails_for_now(params: str) -> str:
    _attempts.append(params)
    raise ApplicationError("may work later")


class TestActivityOutsideWorkflow:
    @pytest.fixture(autouse=True)
    def no_backoff(self, monkeypatch: pytest.MonkeyPatch) -> None:
        _attempts.clear()
        monkeypatch.setattr(config.worker, "local_retry_backoff_coefficient", 0)

    async def test_non_retryable_application_error_is_not_retried(self) -> None:
        with pytest.raises(ApplicationError, match="will not work"):
            await fails_for_good("call")

        assert _attempts == ["call"]

    async def test_retryable_error_is_retried_up_to_the_attempt_limit(self) -> None:
        with pytest.raises(ApplicationError, match="may work later"):
            await fails_for_now("call")

        assert _attempts == ["call", "call", "call"]


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

    @pytest.mark.asyncio
    async def test_rate_limit_can_be_configured_after_decoration(self) -> None:
        @activity()
        async def dynamically_rate_limited_activity() -> str:
            return "done"

        temporal_activity = next(
            candidate
            for candidate in reversed(get_all_temporal_activities())
            if candidate.__name__ == dynamically_rate_limited_activity.__name__
        )
        rate_limit = RateLimit(time_window_in_sec=10, max_execution=2)

        with patch("mistralai.workflows.core.activity.local_wait_rate_limit", new_callable=AsyncMock) as wait:
            set_rate_limit(dynamically_rate_limited_activity, rate_limit)
            assert get_rate_limit(temporal_activity) is not None
            assert await dynamically_rate_limited_activity() == "done"
            wait.assert_awaited_once()

            clear_rate_limit(dynamically_rate_limited_activity)
            assert get_rate_limit(temporal_activity) is None
            assert await dynamically_rate_limited_activity() == "done"
            wait.assert_awaited_once()
