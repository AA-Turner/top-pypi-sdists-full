"""Define compute resource settings."""

from .base import Base, LowercaseStrEnum


class ComputeType(LowercaseStrEnum):
    """Hardware compute type."""

    CPU = "cpu"
    GPU = "gpu"
    AUTO = "auto"


class ComputeSettings(Base):
    """Hardware compute settings.

    Attributes:
        requested_compute_type: requested hardware type
        compute_type_used: actual hardware type used (set after execution)
    """

    requested_compute_type: ComputeType = ComputeType.CPU
    compute_type_used: ComputeType | None = None
