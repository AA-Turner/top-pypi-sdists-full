from typing import Dict, List, Optional

from anyscale._private.models.model_base import ResultIterator
from anyscale._private.sdk import sdk_command
from anyscale.job_queue._private.job_queue_sdk import PrivateJobQueueSDK
from anyscale.job_queue.models import JobQueueStatus


_JOB_QUEUE_SDK_SINGLETON_KEY = "job_queue_sdk"


_LIST_EXAMPLE = """
import anyscale

# Example: List the first 50 job queues
for jq in anyscale.job_queue.list(max_items=50):
    print(jq.id, jq.name, jq.state)
"""

_LIST_ARG_DOCSTRINGS = {
    "job_queue_id": "If provided, fetches only the job queue with this ID.",
    "name": "Filter by job queue name.",
    "creator_id": "Filter by the user ID of the creator.",
    "cloud": "Filter by cloud name.",
    "project": "Filter by project name.",
    "cluster_status": "Filter by the state of the associated cluster.",
    "tags_filter": "Filter by tags. Accepts dict[key] -> List[values] or list['key:value'] entries.",
    "page_size": "Number of items per API request page.",
    "max_items": "Maximum total number of items to return.",
    "sorting_directives": "List of directives to sort the results.",
}

_STATUS_EXAMPLE = """
import anyscale

status = anyscale.job_queue.status(job_queue_id=\"jobq_abc123\")
print(status)
"""

_STATUS_ARG_DOCSTRINGS = {
    "job_queue_id": "The unique ID of the job queue.",
}

_UPDATE_EXAMPLE = """
import anyscale

updated_jq = anyscale.job_queue.update(job_queue_id=\"jobq_abc123\", max_concurrency=5)
print(updated_jq)
"""

_UPDATE_ARG_DOCSTRINGS = {
    "job_queue_id": "ID of the job queue to update.",
    "job_queue_name": "Name of the job queue to update (alternative to ID).",
    "max_concurrency": "New maximum concurrency value.",
    "idle_timeout_s": "New idle timeout in seconds.",
}

_TAGS_ADD_EXAMPLE = """
import anyscale

anyscale.job_queue.add_tags(job_queue_id="jobq_abc123", tags={"team": "mlops"})
"""

_TAGS_ADD_ARG_DOCSTRINGS = {
    "job_queue_id": "ID of the job queue to tag (alternative to name).",
    "name": "Name of the job queue to tag (alternative to ID).",
    "tags": "Key/value tags to upsert as a map {key: value}.",
}

_TAGS_REMOVE_EXAMPLE = """
import anyscale

anyscale.job_queue.remove_tags(job_queue_id="jobq_abc123", keys=["team"])
"""

_TAGS_REMOVE_ARG_DOCSTRINGS = {
    "job_queue_id": "ID of the job queue to modify (alternative to name).",
    "name": "Name of the job queue to modify (alternative to ID).",
    "keys": "List of tag keys to remove.",
}


@sdk_command(
    _JOB_QUEUE_SDK_SINGLETON_KEY,
    PrivateJobQueueSDK,
    doc_py_example=_LIST_EXAMPLE,
    arg_docstrings=_LIST_ARG_DOCSTRINGS,
)
def list(  # noqa: A001
    *,
    job_queue_id: Optional[str] = None,
    name: Optional[str] = None,
    creator_id: Optional[str] = None,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    cluster_status: Optional[str] = None,
    tags_filter: Optional[Dict[str, List[str]]] = None,
    page_size: Optional[int] = None,
    max_items: Optional[int] = None,
    sorting_directives: Optional[List[str]] = None,
    _private_sdk: Optional[PrivateJobQueueSDK] = None,
) -> ResultIterator[JobQueueStatus]:
    """List job queues or fetch a single job queue by ID."""
    return _private_sdk.list(  # type: ignore
        job_queue_id=job_queue_id,
        name=name,
        creator_id=creator_id,
        cloud=cloud,
        project=project,
        cluster_status=cluster_status,
        tags_filter=tags_filter,
        page_size=page_size,
        max_items=max_items,
        sorting_directives=sorting_directives,
    )


@sdk_command(
    _JOB_QUEUE_SDK_SINGLETON_KEY,
    PrivateJobQueueSDK,
    doc_py_example=_STATUS_EXAMPLE,
    arg_docstrings=_STATUS_ARG_DOCSTRINGS,
)
def status(
    job_queue_id: str, _private_sdk: Optional[PrivateJobQueueSDK] = None
) -> JobQueueStatus:
    """Get the status and details for a specific job queue."""
    return _private_sdk.status(  # type: ignore
        job_queue_id=job_queue_id
    )


@sdk_command(
    _JOB_QUEUE_SDK_SINGLETON_KEY,
    PrivateJobQueueSDK,
    doc_py_example=_UPDATE_EXAMPLE,
    arg_docstrings=_UPDATE_ARG_DOCSTRINGS,
)
def update(
    *,
    job_queue_id: Optional[str] = None,
    job_queue_name: Optional[str] = None,
    max_concurrency: Optional[int] = None,
    idle_timeout_s: Optional[int] = None,
    _private_sdk: Optional[PrivateJobQueueSDK] = None,
) -> JobQueueStatus:
    """Update a job queue."""
    return _private_sdk.update(  # type: ignore
        job_queue_id=job_queue_id,
        job_queue_name=job_queue_name,
        max_concurrency=max_concurrency,
        idle_timeout_s=idle_timeout_s,
    )


@sdk_command(
    _JOB_QUEUE_SDK_SINGLETON_KEY,
    PrivateJobQueueSDK,
    doc_py_example=_TAGS_ADD_EXAMPLE,
    arg_docstrings=_TAGS_ADD_ARG_DOCSTRINGS,
)
def add_tags(
    *,
    job_queue_id: Optional[str] = None,
    name: Optional[str] = None,
    tags: Dict[str, str],
    _private_sdk: Optional[PrivateJobQueueSDK] = None,
):
    """Upsert tags for a job queue."""
    return _private_sdk.add_tags(job_queue_id=job_queue_id, name=name, tags=tags)  # type: ignore


@sdk_command(
    _JOB_QUEUE_SDK_SINGLETON_KEY,
    PrivateJobQueueSDK,
    doc_py_example=_TAGS_REMOVE_EXAMPLE,
    arg_docstrings=_TAGS_REMOVE_ARG_DOCSTRINGS,
)
def remove_tags(
    *,
    job_queue_id: Optional[str] = None,
    name: Optional[str] = None,
    keys: List[str],
    _private_sdk: Optional[PrivateJobQueueSDK] = None,
):
    """Remove tags by key from a job queue."""
    return _private_sdk.remove_tags(job_queue_id=job_queue_id, name=name, keys=keys)  # type: ignore


_TAGS_LIST_EXAMPLE = """
import anyscale

tags: dict[str, str] = anyscale.job_queue.list_tags(name="my-queue")
"""

_TAGS_LIST_ARG_DOCSTRINGS = {
    "job_queue_id": "ID of the job queue to read tags (alternative to name).",
    "name": "Name of the job queue to read tags (alternative to ID).",
}


@sdk_command(
    _JOB_QUEUE_SDK_SINGLETON_KEY,
    PrivateJobQueueSDK,
    doc_py_example=_TAGS_LIST_EXAMPLE,
    arg_docstrings=_TAGS_LIST_ARG_DOCSTRINGS,
)
def list_tags(
    *,
    job_queue_id: Optional[str] = None,
    name: Optional[str] = None,
    _private_sdk: Optional[PrivateJobQueueSDK] = None,
) -> Dict[str, str]:
    """List tags for a job queue as a key/value mapping."""
    return _private_sdk.list_tags(job_queue_id=job_queue_id, name=name)  # type: ignore
