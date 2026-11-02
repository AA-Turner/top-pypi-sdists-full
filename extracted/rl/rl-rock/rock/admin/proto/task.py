from enum import Enum

from pydantic import BaseModel


class TaskCreateRequest(BaseModel):
    command: str


class TaskCreateResponse(BaseModel):
    task_id: str | None = None


class TaskPhaseStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class TaskPhase(BaseModel):
    phase: str | None = None
    status: TaskPhaseStatus = TaskPhaseStatus.PENDING
    start_timestamp: int | None = None
    end_timestamp: int | None = None
    message: str | None = None


class TaskResponse(BaseModel):
    task_id: str | None = None
    task_phase_list: list[TaskPhase] | None = None
    status: TaskPhaseStatus = TaskPhaseStatus.PENDING
    start_timestamp: int | None = None
    end_timestamp: int | None = None
    message: str | None = None
