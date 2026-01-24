from enum import Enum
from typing import Union

from pydantic import (
    BaseModel,
    Field,
    field_serializer,
    field_validator,
)


class ExecutionStatus(str, Enum):
    """Status of the execution."""

    triggered = "triggered"
    failed = "failed"
    error = "error"
    timeout = "timeout"
    paused = "paused"
    not_triggered = "not_triggered"
    skipped = "skipped"


class ExecutionStatusMixIn(BaseModel):
    status: ExecutionStatus = Field(default=ExecutionStatus.skipped, description="Status of the execution.")

    @field_validator("status", mode="before")
    def case_agnostic_status(cls, status: Union[str, ExecutionStatus]) -> ExecutionStatus:
        # Ensure that the status is case agnostic.
        return ExecutionStatus(status.lower())

    @field_serializer("status", when_used="always")
    def upper_case_status(self, execution_status: ExecutionStatus) -> str:
        return execution_status.value.upper()
