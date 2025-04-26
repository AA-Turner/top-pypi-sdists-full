from typing import Any, Dict, Optional, Union

from anyscale._private.sdk import sdk_command
from anyscale.cli_logger import BlockLogger
from anyscale.job._private.job_sdk import PrivateJobSDK
from anyscale.job.models import JobConfig, JobLogMode, JobState, JobStatus


logger = BlockLogger()


def _resolve_id_from_args(
    id: Optional[str], kwargs: Dict[str, Any]  # noqa: A002
) -> Optional[str]:
    """Return the correct id as passed through id and kwargs.

    As job_id is being soft deprecated, we will warn if that is passed
    through kwargs.

    If id is passed, id will always be returned (regardless of job_id
    being passed in kwargs). If id is None and job_id is passed in kwargs,
    we will return that as the id to be used.
    """
    if "job_id" in kwargs:
        logger.warning("`job_id` has been deprecated, use `id` instead.")

    if id is not None:
        return id
    else:
        return kwargs.get("job_id", None)


_JOB_SDK_SINGLETON_KEY = "job_sdk"

_SUBMIT_EXAMPLE = """
import anyscale
from anyscale.job.models import JobConfig

anyscale.job.submit(
    JobConfig(
        name="my-job",
        entrypoint="python main.py",
        working_dir=".",
    ),
)
"""

_SUBMIT_ARG_DOCSTRINGS = {"config": "The config options defining the job."}


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    PrivateJobSDK,
    doc_py_example=_SUBMIT_EXAMPLE,
    arg_docstrings=_SUBMIT_ARG_DOCSTRINGS,
)
def submit(config: JobConfig, *, _private_sdk: Optional[PrivateJobSDK] = None) -> str:
    """Submit a job.

    Returns the id of the submitted job.
    """
    return _private_sdk.submit(config)  # type: ignore


_STATUS_EXAMPLE = """
import anyscale
from anyscale.job.models import JobStatus

status: JobStatus = anyscale.job.status(name="my-job")
"""

_STATUS_ARG_DOCSTRINGS = {
    "name": "Name of the job.",
    "id": "Unique ID of the job",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
}


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    PrivateJobSDK,
    doc_py_example=_STATUS_EXAMPLE,
    arg_docstrings=_STATUS_ARG_DOCSTRINGS,
)
def status(
    *,
    name: Optional[str] = None,
    id: Optional[str] = None,  # noqa: A002
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    _private_sdk: Optional[PrivateJobSDK] = None,
    **_kwargs: Dict[str, Any],
) -> JobStatus:
    """Get the status of a job."""
    id = _resolve_id_from_args(id, _kwargs)  # noqa: A001
    return _private_sdk.status(name=name, job_id=id, cloud=cloud, project=project)  # type: ignore


_TERMINATE_EXAMPLE = """
import anyscale

anyscale.job.terminate(name="my-job")
"""

_TERMINATE_ARG_DOCSTRINGS = {
    "name": "Name of the job.",
    "id": "Unique ID of the job",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
}


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    PrivateJobSDK,
    doc_py_example=_TERMINATE_EXAMPLE,
    arg_docstrings=_TERMINATE_ARG_DOCSTRINGS,
)
def terminate(
    *,
    name: Optional[str] = None,
    id: Optional[str] = None,  # noqa: A002
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    _private_sdk: Optional[PrivateJobSDK] = None,
    **_kwargs: Dict[str, Any],
) -> str:
    """Terminate a job.

    This command is asynchronous, so it always returns immediately.

    Returns the id of the terminated job.
    """
    id = _resolve_id_from_args(id, _kwargs)  # noqa: A001
    return _private_sdk.terminate(name=name, job_id=id, cloud=cloud, project=project)  # type: ignore


_ARCHIVE_EXAMPLE = """
import anyscale

anyscale.job.archive(name="my-job")
"""

_ARCHIVE_ARG_DOCSTRINGS = {
    "name": "Name of the job.",
    "id": "Unique ID of the job",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the job . If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
}


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    PrivateJobSDK,
    doc_py_example=_ARCHIVE_EXAMPLE,
    arg_docstrings=_ARCHIVE_ARG_DOCSTRINGS,
)
def archive(
    *,
    name: Optional[str] = None,
    id: Optional[str] = None,  # noqa: A002
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    _private_sdk: Optional[PrivateJobSDK] = None,
    **_kwargs: Dict[str, Any],
) -> str:
    """Archive a job.

    This command is asynchronous, so it always returns immediately.

    Returns the id of the archived job.
    """
    id = _resolve_id_from_args(id, _kwargs)  # noqa: A001
    return _private_sdk.archive(name=name, job_id=id, cloud=cloud, project=project)  # type: ignore


_WAIT_EXAMPLE = """\
import anyscale

anyscale.job.wait(name="my-job", timeout_s=180)"""

_WAIT_ARG_DOCSTRINGS = {
    "name": "Name of the job.",
    "id": "Unique ID of the job",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
    "state": "Target state of the job",
    "timeout_s": "Number of seconds to wait before timing out, this timeout will not affect job execution",
}


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    PrivateJobSDK,
    doc_py_example=_WAIT_EXAMPLE,
    arg_docstrings=_WAIT_ARG_DOCSTRINGS,
)
def wait(
    *,
    name: Optional[str] = None,
    id: Optional[str] = None,  # noqa: A002
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    state: Union[JobState, str] = JobState.SUCCEEDED,
    timeout_s: float = 1800,
    _private_sdk: Optional[PrivateJobSDK] = None,
    **_kwargs: Dict[str, Any],
):
    """"Wait for a job to enter a specific state."""
    id = _resolve_id_from_args(id, _kwargs)  # noqa: A001
    _private_sdk.wait(  # type: ignore
        name=name,
        job_id=id,
        cloud=cloud,
        project=project,
        state=state,
        timeout_s=timeout_s,
    )


_GET_LOGS_EXAMPLE = """\
import anyscale

anyscale.job.get_logs(name="my-job", run="job-run-name")
"""

_GET_LOGS_ARG_DOCSTRINGS = {
    "name": "Name of the job",
    "id": "Unique ID of the job",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
    "run": "The name of the run to query. Names can be found in the JobStatus. If not provided, the last job run will be used.",
    "mode": "The mode of log fetching to be used. Supported modes can be found in JobLogMode. If not provided, JobLogMode.TAIL will be used.",
    "max_lines": "The number of log lines to be fetched. If not provided, the complete log will be fetched.",
}


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    PrivateJobSDK,
    doc_py_example=_GET_LOGS_EXAMPLE,
    arg_docstrings=_GET_LOGS_ARG_DOCSTRINGS,
)
def get_logs(
    *,
    id: Optional[str] = None,  # noqa: A002
    name: Optional[str] = None,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    run: Optional[str] = None,
    mode: Union[str, JobLogMode] = JobLogMode.TAIL,
    max_lines: Optional[int] = None,
    _private_sdk: Optional[PrivateJobSDK] = None,
    **_kwargs: Dict[str, Any],
) -> str:
    """Query the jobs for a job run."""
    id = _resolve_id_from_args(id, _kwargs)  # noqa: A001
    return _private_sdk.get_logs(  # type: ignore
        job_id=id,
        name=name,
        cloud=cloud,
        project=project,
        run=run,
        mode=mode,
        max_lines=max_lines,
    )
