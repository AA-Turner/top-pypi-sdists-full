from datetime import timedelta
from typing import Any, Callable

from pydantic import BaseModel
from pydantic import ConfigDict

from project.operation_execution.util import every_timedelta_is_time_func
from project.sqlalchemy_db_.sqlalchemy_model import OperationDBM


class ScheduledOperation(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)

    type: str
    input_data: dict[str, Any] = {}
    is_time_func: Callable
    timeout_after_creation: timedelta | None = None


healthcheck_every_0_01_seconds_so = ScheduledOperation(
    type=OperationDBM.Types.healthcheck_,
    input_data={"healthcheck": "healthcheck"},
    is_time_func=every_timedelta_is_time_func(td=timedelta(seconds=0.01))
)

healthcheck_every_3_seconds_so = ScheduledOperation(
    type=OperationDBM.Types.healthcheck_,
    input_data={"healthcheck": "healthcheck"},
    is_time_func=every_timedelta_is_time_func(td=timedelta(seconds=3))
)

healthcheck_every_24_hours_so = ScheduledOperation(
    type=OperationDBM.Types.healthcheck_,
    input_data={"healthcheck": "healthcheck"},
    is_time_func=every_timedelta_is_time_func(td=timedelta(hours=24))
)

raise_fake_error_every_3_seconds_so = ScheduledOperation(
    type=OperationDBM.Types.raise_fake_error_,
    input_data={"raise_fake_error": "raise_fake_error"},
    is_time_func=every_timedelta_is_time_func(td=timedelta(seconds=3))
)


def get_scheduled_operations() -> list[ScheduledOperation]:
    res = []
    res.append(healthcheck_every_3_seconds_so)
    res.append(healthcheck_every_24_hours_so)
    return res
