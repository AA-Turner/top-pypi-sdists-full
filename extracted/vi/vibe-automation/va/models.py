from enum import Enum
from typing import Any

from pydantic import BaseModel


class ExecutionModel(BaseModel):
    id: str
    input: Any


class ReviewStatus(str, Enum):
    PENDING = "pending"
    READY = "ready"


class ReviewModal(BaseModel):
    id: str
    type: str
    instruction: str
    artifacts: list[Any] | None
    status: ReviewStatus
    data: Any
