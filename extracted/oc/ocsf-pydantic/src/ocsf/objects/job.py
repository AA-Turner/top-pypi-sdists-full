from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from .file import File
from .user import User

class JobRunStateId(Enum):
    """
    The run state ID of the job.
    """
    Unknown: int = 0
    Ready: int = 1
    Queued: int = 2
    Running: int = 3
    Stopped: int = 4
    Other: int = 99

class Job(BaseModel):
    """
    The Job object provides information about a scheduled job or task, including its
    name, command line, and state. It encompasses attributes that describe the
    properties and status of the scheduled job.
    """

    file: File # The file that pertains to the job.
    name: str # The name of the job.

    # Recommended:
    cmd_line: str | None = None # The job command line.
    created_time: datetime | None = None # The time when the job was created.
    desc: str | None = None # The description of the job.
    last_run_time: datetime | None = None # The time when the job was last run.
    run_state_id: JobRunStateId | None = None # The run state ID of the job.

    # Optional:
    next_run_time: datetime | None = None # The time when the job will next be run.
    run_state: str | None = None # The run state of the job.
    user: User | None = None # The user that created the job.
