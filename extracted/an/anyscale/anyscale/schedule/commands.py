from typing import Optional

from anyscale._private.sdk import sdk_command
from anyscale.cli_logger import BlockLogger
from anyscale.schedule._private.schedule_sdk import PrivateScheduleSDK
from anyscale.schedule.models import ScheduleConfig, ScheduleState, ScheduleStatus


logger = BlockLogger()

_SCHEDULE_SDK_SINGLETON_KEY = "schedule_sdk"

_APPLY_EXAMPLE = """
import anyscale
from anyscale.job.models import JobConfig
from anyscale.schedule.models import ScheduleConfig

anyscale.schedule.apply(
    ScheduleConfig(
        cron_expression="0 0 * * * *",
        job_config=JobConfig(
            name="my-job",
            entrypoint="python main.py",
            working_dir=".",
        )
    )
)
"""

_APPLY_ARG_DOCSTRINGS = {"config": "The config options defining the schedule."}


@sdk_command(
    _SCHEDULE_SDK_SINGLETON_KEY,
    PrivateScheduleSDK,
    doc_py_example=_APPLY_EXAMPLE,
    arg_docstrings=_APPLY_ARG_DOCSTRINGS,
)
def apply(
    config: ScheduleConfig, *, _private_sdk: Optional[PrivateScheduleSDK] = None
) -> str:
    """Apply or update a schedule.

    Returns the id of the schedule.
    """
    return _private_sdk.apply(config)  # type: ignore


_SET_STATE_EXAMPLE = """
import anyscale
from anyscale.schedule.models import ScheduleState

anyscale.schedule.set_state(
    id="my=schedule-id",
    state=ScheduleState.DISABLED,
)
"""

_SET_STATE_ARG_DOCSTRINGS = {
    "id": "The id of the schedule.",
    "name": "The name of the schedule.",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
    "state": "The state to set the schedule to.",
}


@sdk_command(
    _SCHEDULE_SDK_SINGLETON_KEY,
    PrivateScheduleSDK,
    doc_py_example=_SET_STATE_EXAMPLE,
    arg_docstrings=_SET_STATE_ARG_DOCSTRINGS,
)
def set_state(
    *,
    id: Optional[str] = None,  # noqa: A002
    name: Optional[str] = None,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    state: ScheduleState,
    _private_sdk: Optional[PrivateScheduleSDK] = None
) -> str:
    """Set the state of a schedule.

    Returns the id of the schedule.
    """
    return _private_sdk.set_state(  # type: ignore
        id=id, name=name, cloud=cloud, project=project, state=state,
    )


_STATUS_EXAMPLE = """
import anyscale
anyscale.schedule.status(id="cronjob_yt389jvskwht9k2ygx7rj6iz62")
"""

_STATUS_ARG_DOCSTRINGS = {
    "id": "The id of the schedule.",
    "name": "The name of the schedule.",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
}


@sdk_command(
    _SCHEDULE_SDK_SINGLETON_KEY,
    PrivateScheduleSDK,
    doc_py_example=_STATUS_EXAMPLE,
    arg_docstrings=_STATUS_ARG_DOCSTRINGS,
)
def status(
    *,
    id: Optional[str] = None,  # noqa: A002
    name: Optional[str] = None,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    _private_sdk: Optional[PrivateScheduleSDK] = None
) -> ScheduleStatus:
    """Return the status of the schedule.
    """
    return _private_sdk.status(id=id, name=name, cloud=cloud, project=project)  # type: ignore


_TRIGGER_EXAMPLE = """
import anyscale
anyscale.schedule.trigger(id="cronjob_yt389jvskwht9k2ygx7rj6iz62")
"""

_TRIGGER_ARG_DOCSTRINGS = {
    "id": "The id of the schedule.",
    "name": "The name of the schedule.",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
}


@sdk_command(
    _SCHEDULE_SDK_SINGLETON_KEY,
    PrivateScheduleSDK,
    doc_py_example=_TRIGGER_EXAMPLE,
    arg_docstrings=_TRIGGER_ARG_DOCSTRINGS,
)
def trigger(
    *,
    id: Optional[str] = None,  # noqa: A002
    name: Optional[str] = None,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    _private_sdk: Optional[PrivateScheduleSDK] = None
) -> str:
    """Trigger the execution of the schedule.
    """
    return _private_sdk.trigger(id=id, name=name, cloud=cloud, project=project)  # type: ignore
