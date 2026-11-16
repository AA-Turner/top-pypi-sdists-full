"""GPU observations made by the serving worker while an identified request is active."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, FiniteFloat, field_validator

from ....compat import StrEnum


class GpuAttribution(StrEnum):
    SHARED_DEVICE = "shared_device"


class GpuUnsupported(StrEnum):
    """Why a sample can hold no GPU readings at all, known up front (stored as the part's `extras.gpu_unsupported`)."""

    ENGINE = "engine"  # its model calls ran on engines the run did not launch (external or provider-managed)


class GpuReading(BaseModel):
    wall_clock: datetime
    host: str = Field(min_length=1, max_length=256)
    device: str = Field(min_length=1, max_length=256)
    request_id: str = Field(min_length=1, max_length=256)
    active_requests: int = Field(ge=1)
    attribution: GpuAttribution = GpuAttribution.SHARED_DEVICE
    metrics: dict[str, FiniteFloat] = Field(max_length=16)

    @field_validator("wall_clock")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("GPU observations require a timezone")
        return value


class SampleHardwarePoint(BaseModel):
    key: str
    value: FiniteFloat
    wall_clock: datetime
    dimensions: dict = Field(default_factory=dict)
    request_id: str


class SampleHardware(BaseModel):
    run_id: UUID
    sample_id: UUID
    points: list[SampleHardwarePoint] = Field(default_factory=list)
    truncated: bool = False
    #: Set when this sample can hold no readings at all; the Compute tab then says so instead of "none recorded".
    unsupported: GpuUnsupported | None = None
