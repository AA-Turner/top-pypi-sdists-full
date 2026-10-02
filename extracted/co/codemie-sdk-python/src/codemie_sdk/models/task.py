from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class BackgroundTaskStatus(str, Enum):
    """Enum for background task statuses."""

    STARTED = "STARTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TaskUser(BaseModel):
    """Model representing task user information."""

    model_config = ConfigDict(extra="ignore")

    user_id: str = Field(description="Unique identifier of the user")
    username: str = Field(default="", description="Username of the task owner")
    name: str = Field(default="", description="Display name of the task owner")


class BackgroundTaskEntity(BaseModel):
    """Model representing a background task."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(description="Unique identifier of the task")
    task: str = Field(description="Task description or name")
    user: TaskUser = Field(description="Information about the task owner")
    final_output: str | None = Field(
        default="", description="The final result or output of the task"
    )
    current_step: str | None = Field(
        default="", description="Current step or stage of the task"
    )
    status: BackgroundTaskStatus = Field(
        description="Task status (STARTED, COMPLETED, or FAILED)"
    )
    date: datetime = Field(description="Task creation timestamp")
    update_date: datetime = Field(description="Last update timestamp")
