from typing import Any, Dict, List, Optional, Union

from anyscale._private.models.model_base import ResultIterator
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
        return kwargs.get("job_id")


_JOB_SDK_SINGLETON_KEY = "job_sdk"

_SUBMIT_EXAMPLE = """
import anyscale
from anyscale.job.models import JobConfig, ConnectionConfig, ConnectionType

# Basic job submission. submit() returns the ID of the submitted job as a string.
job_id: str = anyscale.job.submit(
    JobConfig(
        name="my-job",
        entrypoint="python main.py",
        working_dir=".",
    ),
)
print(job_id)
# e.g. "prodjob_6ntzknwk1i9b1uw1zk1gp9dbhe"

# The returned ID can be passed to other commands, e.g. status / get_logs / terminate.
status = anyscale.job.status(id=job_id)

# Job with Databricks connection for credential injection.
job_id = anyscale.job.submit(
    JobConfig(
        name="my-job-with-databricks",
        entrypoint="python main.py",
        working_dir=".",
        connections=[
            ConnectionConfig(
                type=ConnectionType.DATABRICKS,
                name="my-databricks-connection",
            )
        ],
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

# status() returns a JobStatus describing the job.
status: JobStatus = anyscale.job.status(name="my-job")
print(status.id, status.name, status.state)
# Key fields: id, name, state, runs, config (see the JobStatus model).
"""

_STATUS_ARG_DOCSTRINGS = {
    "name": "Name of the job.",
    "id": "Unique ID of the job",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
    "include_archived": "Include archived jobs when searching by name. Ignored when using id.",
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
    include_archived: bool = False,
    _private_sdk: Optional[PrivateJobSDK] = None,
    **_kwargs: Dict[str, Any],
) -> JobStatus:
    """Get the status of a job."""
    id = _resolve_id_from_args(id, _kwargs)  # noqa: A001
    return _private_sdk.status(name=name, job_id=id, cloud=cloud, project=project, include_archived=include_archived)  # type: ignore


_TERMINATE_EXAMPLE = """
import anyscale

# terminate() returns the ID of the terminated job as a string.
job_id: str = anyscale.job.terminate(name="my-job")
# e.g. "prodjob_6ntzknwk1i9b1uw1zk1gp9dbhe"
"""

_TERMINATE_ARG_DOCSTRINGS = {
    "name": "Name of the job.",
    "id": "Unique ID of the job",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
    "include_archived": "Include archived jobs when searching by name. Ignored when using id.",
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
    include_archived: bool = False,
    _private_sdk: Optional[PrivateJobSDK] = None,
    **_kwargs: Dict[str, Any],
) -> str:
    """Terminate a job.

    This command is asynchronous, so it always returns immediately.

    Returns the id of the terminated job.
    """
    id = _resolve_id_from_args(id, _kwargs)  # noqa: A001
    return _private_sdk.terminate(name=name, job_id=id, cloud=cloud, project=project, include_archived=include_archived)  # type: ignore


_ARCHIVE_EXAMPLE = """
import anyscale

# archive() returns the ID of the archived job as a string.
job_id: str = anyscale.job.archive(name="my-job")
# e.g. "prodjob_6ntzknwk1i9b1uw1zk1gp9dbhe"
"""

_ARCHIVE_ARG_DOCSTRINGS = {
    "name": "Name of the job.",
    "id": "Unique ID of the job",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
    "include_archived": "Include archived jobs when searching by name. Ignored when using id.",
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
    include_archived: bool = False,
    _private_sdk: Optional[PrivateJobSDK] = None,
    **_kwargs: Dict[str, Any],
) -> str:
    """Archive a job.

    This command is asynchronous, so it always returns immediately.

    Returns the id of the archived job.
    """
    id = _resolve_id_from_args(id, _kwargs)  # noqa: A001
    return _private_sdk.archive(name=name, job_id=id, cloud=cloud, project=project, include_archived=include_archived)  # type: ignore


_DELETE_EXAMPLE = """
import anyscale

# delete() returns the ID of the deleted job as a string.
job_id: str = anyscale.job.delete(name="my-job")
# e.g. "prodjob_6ntzknwk1i9b1uw1zk1gp9dbhe"
"""

_DELETE_ARG_DOCSTRINGS = {
    "name": "Name of the job.",
    "id": "Unique ID of the job",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
    "include_archived": "Include archived jobs when searching by name. Ignored when using id.",
}


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    PrivateJobSDK,
    doc_py_example=_DELETE_EXAMPLE,
    arg_docstrings=_DELETE_ARG_DOCSTRINGS,
)
def delete(
    *,
    name: Optional[str] = None,
    id: Optional[str] = None,  # noqa: A002
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    include_archived: bool = False,
    _private_sdk: Optional[PrivateJobSDK] = None,
    **_kwargs: Dict[str, Any],
) -> str:
    """Delete a job and all associated job runs.

    The job must be in a terminal state (SUCCEEDED, FAILED).
    This action permanently removes the job and cannot be undone.

    Returns the id of the deleted job.
    """
    id = _resolve_id_from_args(id, _kwargs)  # noqa: A001
    return _private_sdk.delete(name=name, job_id=id, cloud=cloud, project=project, include_archived=include_archived)  # type: ignore


_WAIT_EXAMPLE = """\
import anyscale

# wait() blocks until the job reaches the target state (SUCCEEDED by default),
# or raises a TimeoutError if timeout_s elapses first. It returns no value.
anyscale.job.wait(name="my-job", timeout_s=180)"""

_WAIT_ARG_DOCSTRINGS = {
    "name": "Name of the job.",
    "id": "Unique ID of the job",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
    "state": "Target state of the job",
    "timeout_s": "Number of seconds to wait before timing out, this timeout will not affect job execution",
    "follow": "Whether to follow the logs of the job. If True, the logs will be streamed to the console.",
    "include_archived": "Include archived jobs when searching by name. Ignored when using id.",
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
    follow: bool = False,
    include_archived: bool = False,
    _private_sdk: Optional[PrivateJobSDK] = None,
    **_kwargs: Dict[str, Any],
):
    """Wait for a job to enter a specific state."""
    id = _resolve_id_from_args(id, _kwargs)  # noqa: A001
    _private_sdk.wait(  # type: ignore
        name=name,
        job_id=id,
        cloud=cloud,
        project=project,
        state=state,
        timeout_s=timeout_s,
        follow=follow,
        include_archived=include_archived,
    )


_GET_LOGS_EXAMPLE = """\
import anyscale

# get_logs() returns the job logs as a string.
logs: str = anyscale.job.get_logs(name="my-job", run="job-run-name")
print(logs)
"""

_GET_LOGS_ARG_DOCSTRINGS = {
    "name": "Name of the job",
    "id": "Unique ID of the job",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
    "run": "The name of the run to query. Names can be found in the JobStatus. If not provided, the last job run will be used.",
    "mode": "The mode of log fetching to be used. Supported modes can be found in JobLogMode. If not provided, JobLogMode.TAIL will be used.",
    "max_lines": "The number of log lines to be fetched. If not provided, the complete log will be fetched.",
    "include_archived": "Include archived jobs when searching by name. Ignored when using id.",
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
    include_archived: bool = False,
    _private_sdk: Optional[PrivateJobSDK] = None,
    **_kwargs: Dict[str, Any],
) -> str:
    """Get the logs for a job."""
    id = _resolve_id_from_args(id, _kwargs)  # noqa: A001
    return _private_sdk.get_logs(  # type: ignore
        job_id=id,
        name=name,
        cloud=cloud,
        project=project,
        run=run,
        mode=mode,
        max_lines=max_lines,
        include_archived=include_archived,
    )


_ADD_TAGS_EXAMPLE = """
import anyscale

# add_tags() returns nothing; it raises an exception on failure.
anyscale.job.add_tags(job_id="job_123", tags={"team": "mlops", "env": "prod"})
"""

_ADD_TAGS_ARG_DOCSTRINGS = {
    "job_id": "ID of the job. Provide either job_id or name.",
    "name": "Name of the job. Provide either job_id or name.",
    "cloud": "Cloud name (used when resolving by name).",
    "project": "Project name (used when resolving by name).",
    "tags": "Key/value tags to upsert as a map {key: value}.",
    "include_archived": "Include archived jobs when searching by name. Ignored when using job_id.",
}

_REMOVE_TAGS_EXAMPLE = """
import anyscale

# remove_tags() returns nothing; it raises an exception on failure.
anyscale.job.remove_tags(job_id="job_123", keys=["team", "env"])
"""

_REMOVE_TAGS_ARG_DOCSTRINGS = {
    "job_id": "ID of the job. Provide either job_id or name.",
    "name": "Name of the job. Provide either job_id or name.",
    "cloud": "Cloud name (used when resolving by name).",
    "project": "Project name (used when resolving by name).",
    "keys": "List of tag keys to remove.",
    "include_archived": "Include archived jobs when searching by name. Ignored when using job_id.",
}


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    PrivateJobSDK,
    doc_py_example=_ADD_TAGS_EXAMPLE,
    arg_docstrings=_ADD_TAGS_ARG_DOCSTRINGS,
)
def add_tags(
    *,
    job_id: Optional[str] = None,
    name: Optional[str] = None,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    tags: Dict[str, str],
    include_archived: bool = False,
    _private_sdk: Optional[PrivateJobSDK] = None,
):
    """Upsert (add/update) tag key/value pairs for a job."""
    return _private_sdk.add_tags(  # type: ignore
        job_id=job_id,
        name=name,
        cloud=cloud,
        project=project,
        tags=tags,
        include_archived=include_archived,
    )


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    PrivateJobSDK,
    doc_py_example=_REMOVE_TAGS_EXAMPLE,
    arg_docstrings=_REMOVE_TAGS_ARG_DOCSTRINGS,
)
def remove_tags(
    *,
    job_id: Optional[str] = None,
    name: Optional[str] = None,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    keys: List[str],
    include_archived: bool = False,
    _private_sdk: Optional[PrivateJobSDK] = None,
):
    """Remove tags by key from a job."""
    return _private_sdk.remove_tags(  # type: ignore
        job_id=job_id,
        name=name,
        cloud=cloud,
        project=project,
        keys=keys,
        include_archived=include_archived,
    )


_LIST_TAGS_EXAMPLE = """
import anyscale

# list_tags() returns the job's tags as a key/value dict.
tags: dict[str, str] = anyscale.job.list_tags(name="my-job")
print(tags)
"""

_LIST_TAGS_ARG_DOCSTRINGS = {
    "job_id": "ID of the job. Provide either job_id or name.",
    "name": "Name of the job. Provide either job_id or name.",
    "cloud": "Cloud name (used when resolving by name).",
    "project": "Project name (used when resolving by name).",
    "include_archived": "Include archived jobs when searching by name. Ignored when using job_id.",
}


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    PrivateJobSDK,
    doc_py_example=_LIST_TAGS_EXAMPLE,
    arg_docstrings=_LIST_TAGS_ARG_DOCSTRINGS,
)
def list_tags(
    *,
    job_id: Optional[str] = None,
    name: Optional[str] = None,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    include_archived: bool = False,
    _private_sdk: Optional[PrivateJobSDK] = None,
) -> Dict[str, str]:
    """List tags for a job as a key/value mapping."""
    return _private_sdk.list_tags(  # type: ignore
        job_id=job_id,
        name=name,
        cloud=cloud,
        project=project,
        include_archived=include_archived,
    )


_LIST_EXAMPLE = """
import anyscale
from anyscale.job.models import JobStatus

# list() returns a ResultIterator; each item is a JobStatus.
for job in anyscale.job.list(max_items=10):
    print(f"{job.name}: {job.state}")

# Materialize into a list of JobStatus objects.
jobs = list(anyscale.job.list(project="my-project"))
"""

_LIST_ARG_DOCSTRINGS = {
    "name": "Filter by job name.",
    "job_id": "Fetch a specific job by ID.",
    "project": "Filter by project name.",
    "cloud": "Filter by cloud name.",
    "include_all_users": "Include jobs from all users.",
    "include_archived": "Include archived jobs.",
    "state_filter": "Filter by job states (list of JobState or str).",
    "tags_filter": "Filter by tags (dict of key to list of values).",
    "page_size": "Number of items per page.",
    "max_items": "Maximum total items to return.",
    "sort_field": "Field to sort by (CREATED_AT, NAME, STATUS, etc.).",
    "sort_order": "Sort order (ASC or DESC).",
    "created_at_from": "Filter for jobs created at or after this time (e.g. 2026-01-01T00:00:00Z).",
    "created_at_to": "Filter for jobs created at or before this time (e.g. 2026-12-31T23:59:59Z).",
    "updated_at_from": "Filter for jobs updated at or after this time (e.g. 2026-01-01T00:00:00Z).",
    "updated_at_to": "Filter for jobs updated at or before this time (e.g. 2026-12-31T23:59:59Z).",
    "status_updated_at_from": "Filter for jobs whose status was last updated at or after this time (e.g. 2026-01-01T00:00:00Z).",
    "status_updated_at_to": "Filter for jobs whose status was last updated at or before this time (e.g. 2026-12-31T23:59:59Z).",
}


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    PrivateJobSDK,
    doc_py_example=_LIST_EXAMPLE,
    arg_docstrings=_LIST_ARG_DOCSTRINGS,
)
def list(  # noqa: A001, PLR0913
    *,
    name: Optional[str] = None,
    job_id: Optional[str] = None,
    project: Optional[str] = None,
    cloud: Optional[str] = None,
    include_all_users: bool = False,
    include_archived: bool = False,
    state_filter: Optional[List[Union[JobState, str]]] = None,
    tags_filter: Optional[Dict[str, List[str]]] = None,
    page_size: Optional[int] = None,
    max_items: Optional[int] = None,
    sort_field: Optional[str] = None,
    sort_order: Optional[str] = None,
    created_at_from: Optional[str] = None,
    created_at_to: Optional[str] = None,
    updated_at_from: Optional[str] = None,
    updated_at_to: Optional[str] = None,
    status_updated_at_from: Optional[str] = None,
    status_updated_at_to: Optional[str] = None,
    _private_sdk: Optional[PrivateJobSDK] = None,
) -> ResultIterator[JobStatus]:
    """List jobs with filtering and pagination.

    Returns a ResultIterator that lazily fetches pages of jobs.
    """
    return _private_sdk.list(  # type: ignore
        name=name,
        job_id=job_id,
        project=project,
        cloud=cloud,
        include_all_users=include_all_users,
        include_archived=include_archived,
        state_filter=state_filter,
        tags_filter=tags_filter,
        page_size=page_size,
        max_items=max_items,
        sort_field=sort_field,
        sort_order=sort_order,
        created_at_from=created_at_from,
        created_at_to=created_at_to,
        updated_at_from=updated_at_from,
        updated_at_to=updated_at_to,
        status_updated_at_from=status_updated_at_from,
        status_updated_at_to=status_updated_at_to,
    )
