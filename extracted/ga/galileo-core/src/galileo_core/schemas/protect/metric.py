from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_serializer, field_validator

from galileo_core.schemas.shared.metric import MetricValueType


class MetricComputationStatus(str, Enum):
    success = "success"
    timeout = "timeout"
    failed = "failed"
    error = "error"


class MetricComputation(BaseModel):
    value: MetricValueType = None
    execution_time: Optional[float] = None
    status: Optional[MetricComputationStatus] = None
    error_message: Optional[str] = None

    @field_serializer("status", when_used="json-unless-none")
    def upper_case_status(self, value: MetricComputationStatus) -> str:
        return value.value.upper()

    @field_validator("status", mode="before")
    def lower_case_status(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.lower()
