import os
from typing import Dict, Optional, Any, Union
from uuid import UUID, uuid4
from datetime import datetime
from asyncdb.models import Model, Field


class Job(Model):
    job_id: str = Field(required=True, primary_key=True)
    job_uuid: UUID = Field(
        required=False,
        primary_key=True,
        db_default="auto",
        default=uuid4,
        repr=False
    )
    job: Optional[dict] = Field(required=True, default_factory=dict)
    attributes: Optional[dict] = Field(default_factory=dict)
    schedule_type: str = Field(required=False, default="interval")
    schedule: Optional[dict] = Field(default_factory=dict)
    jitter: Optional[int] = Field(required=False, default=0)
    is_coroutine: bool = Field(required=False, default=True)
    jobstore: str = Field(required=False, default="default")
    executor: str = Field(required=False, default="default")
    run_date: Optional[datetime]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    last_exec_time: Optional[datetime]
    next_run_time: Optional[datetime]
    job_status: int = Field(required=False, default=0)
    job_state: Optional[bytes] = Field(required=False, repr=False)
    traceback: Optional[str] = Field(required=False, repr=False)
    params: Optional[dict] = Field(default_factory=dict)
    enabled: bool = Field(required=False, default=True)
    reschedule: bool = Field(required=False, default=False)
    reschedule_jitter: Optional[int] = Field(required=False, default=0)
    rescheduled_max: Optional[int] = Field(required=False, default=0)
    notification: bool = Field(required=False, default=False)
    priority: Optional[str] = Field(required=False)
    created_at: datetime = Field(
        required=False,
        default=datetime.now(),
        repr=False
    )
    updated_at: datetime = Field(
        required=False,
        default=datetime.now(),
        repr=False
    )
    ## ALTER TABLE troc.jobs add column if not exists created_by integer;
    created_by: int = Field(required=False)

    class Meta:
        driver = "pg"
        name = "jobs"
        schema = os.environ.get("DB_SCHEMA", "troc")
        app_label = os.environ.get("DB_SCHEMA", "troc")
        strict = True
        frozen = False
