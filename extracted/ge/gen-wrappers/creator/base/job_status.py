from enum import Enum


class JobStatus(Enum):
    """JobStatus enum."""
    READY = "READY"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
