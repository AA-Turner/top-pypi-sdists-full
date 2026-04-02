from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Optional

import typer
from croniter import croniter


class ExecutionMode(StrEnum):
    SINGLE = "single"
    CLUSTER = "cluster"
    STREAM = "stream"


class JobScheduleMode(StrEnum):
    ONCE = "once"
    CRON = "cron"


@dataclass
class ApiConfig:
    base_url: str
    auth_token: str

    def __post_init__(self):
        for field_name, field_value in self.__dict__.items():
            if field_value is None:
                raise ValueError(f"The field '{field_name}' cannot be None.")


@dataclass
class JobExecutionSchedule:
    schedule_mode: JobScheduleMode
    start_time: datetime | None
    until: datetime | None
    cron_expression: str | None
    interval: int | None
    run_overlap: bool = True
    initial_run: bool = True
    timezone: str = "UTC"

    def __post_init__(self):
        import re
        from datetime import datetime

        fmt = "%Y-%m-%dT%H:%M"
        regex = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$"
        for field in ["start_time", "until"]:
            value = getattr(self, field)
            if value:
                if isinstance(value, str):
                    if not re.match(regex, value):
                        raise ValueError(
                            f"{field} must be in format YYYY-MM-DDTHH:MM, e.g., 2025-08-12T18:35"
                        )
                    try:
                        datetime.strptime(value, fmt)
                    except ValueError:
                        raise ValueError(f"{field} is not a valid date/time: {value}")
                elif isinstance(value, datetime):
                    pass
                else:
                    raise TypeError(
                        f"{field} must be a string in format YYYY-MM-DDTHH:MM or a datetime object"
                    )

        cron_value = self.cron_expression
        if cron_value:
            if not croniter.is_valid(cron_value):
                raise ValueError(
                    "cron_expression must be a valid 5-field cron string, e.g., '0 0 * * *'"
                )


@dataclass
class JobMetadata:
    """Metadata container for job execution in a pipeline system.

    This class encapsulates necessary metadata for executing a job within
    a pipeline, including security credentials, execution configuration, and
    resource requirements.

    Attributes:
        pipeline_hash (str): Unique identifier hash for the pipeline instance.
        confidential_level (str): Security classification level of the job
            (e.g., 'public', 'internal', 'confidential', 'secret').
        execution_mode (ExecutionMode): Enum specifying how the job should be
            executed (e.g., local, distributed, containerized).
        execution_plan (Optional[JobExecutionSchedule]): Schedule configuration
            for job execution. None if job runs immediately or on-demand.
        main_file_path (str): Path to the main executable file or script.
        env_file_path (str): Path to the environment configuration file.
        secret_key (str): Encryption key for securing sensitive job data.
        iv (str): Initialization vector for encryption operations.
        requirement_file (str): Path to the file containing job dependencies.
        requirements_type (str): Type of requirements specification
            (e.g., 'pip', 'conda', 'poetry').
        complexity_factor (float): Numerical measure of job computational
            complexity, used for resource allocation.
        data_size (float): Expected size of data in KB to be processed in the job.
    """

    pipeline_hash: str
    confidential_level: str
    execution_mode: ExecutionMode
    execution_plan: Optional[JobExecutionSchedule]
    main_file_path: str
    env_file_path: str
    requirement_file: Optional[str]
    requirements_type: Optional[str]
    complexity_factor: float
    data_size: float
    code_size: float
    secret_key: Optional[str]
    iv: Optional[str]
    env_vars: dict = None


class BaseTyperCommand:
    def __init__(self, report: bool = False):
        self.report = report

    def echo(self, msg, *args, **kwargs):
        if not self.report:
            return
        typer.echo(msg, *args, **kwargs)
