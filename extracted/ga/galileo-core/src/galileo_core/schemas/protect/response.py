from time import time_ns
from uuid import uuid4

from pydantic import (
    UUID4,
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    field_validator,
)

from galileo_core.schemas.protect.execution_status import ExecutionStatus, ExecutionStatusMixIn


class BaseTraceMetadata(BaseModel):
    id: UUID4 = Field(default_factory=uuid4, description="Unique identifier for the request.")
    received_at: int = Field(
        default_factory=time_ns,
        description="Time the request was received by the server in nanoseconds.",
    )


class TraceMetadata(BaseTraceMetadata):
    response_at: int = Field(
        default_factory=time_ns,
        description="Time the response was sent by the server in nanoseconds.",
    )
    # Set a default value for execution_time to -1 to indicate that it is not set.
    execution_time: float = Field(
        default=-1,
        description="Execution time for the request (in seconds).",
        validate_default=True,
    )

    @field_validator("execution_time", mode="before")
    def set_execution_time(cls, value: int, info: ValidationInfo) -> int:
        # Our timestamps are in nanoseconds, so we convert to seconds to get the
        # execution time.
        if value <= 0:
            value = (info.data.get("response_at", 0) - info.data.get("received_at", 0)) * 1e-9
        return value


class Response(ExecutionStatusMixIn):
    text: str = Field(description="Text from the request after processing the rules.")
    trace_metadata: TraceMetadata
    status: ExecutionStatus = Field(
        default=ExecutionStatus.not_triggered, description="Status of the request after processing the rules."
    )

    model_config = ConfigDict(extra="allow")
