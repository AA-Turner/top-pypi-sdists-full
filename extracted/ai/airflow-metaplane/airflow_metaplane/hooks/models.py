from datetime import datetime, timedelta
from attr import define
from typing import List, Optional


@define
class MPTask:
    task_id: str
    owner: str
    retries: Optional[int]
    retry_delay: timedelta
    max_retry_delay: Optional[timedelta]
    sla: Optional[timedelta]
    execution_timeout: Optional[timedelta]
    operator_class: str
    upstream_task_ids: List[str]
    downstream_task_ids: List[str]


@define
class MPDag:
    dag_id: str
    description: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    tags: List[str]
    tasks: List[MPTask]


@define
class MPTaskInstance:
    task_id: str
    dag_id: str
    run_id: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    execution_date: Optional[datetime]
    duration: Optional[float]
    state: Optional[str]
    try_number: int
    max_tries: int
    job_id: Optional[int]
    operator: str
    queued_dttm: Optional[datetime]
    queued_by_job_id: Optional[int]
    test_mode: bool


@define
class MPDagRun:
    id: int
    dag_id: str
    queued_at: datetime
    execution_date: datetime
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    state: str
    run_id: str
    external_trigger: bool
    run_type: str
    task_instances: List[MPTaskInstance]


@define
class MPDagContext:
    connection_id: str
    dag: MPDag
    dag_run: MPDagRun
    task_instance: Optional[MPTaskInstance]
    reason: Optional[str]
    exception: Optional[str]
    run_id: str
    test_mode: bool
