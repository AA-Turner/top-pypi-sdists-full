"""get_runs SDK for MAPI"""
from __future__ import annotations

from concurrent.futures import Future
from datetime import datetime
from http import HTTPStatus
from typing import List, Optional, Union, cast, overload

from typing_extensions import Literal

from mcli.api.engine.engine import convert_plural_future_to_singleton, get_return_response, run_paginated_mapi_request
from mcli.api.exceptions import MAPIException
from mcli.api.model.cluster_details import ClusterDetails
from mcli.api.model.run import Run, RunType
from mcli.api.users.api_get_users import get_current_user
from mcli.config import MCLIConfig
from mcli.models.common import ObjectList
from mcli.models.gpu_type import GPUType
from mcli.utils.utils_run_status import RunStatus

__all__ = ['get_runs', 'get_run']

DEFAULT_LIMIT = 100

QUERY_FUNCTION_PAGINATED = 'getRunsPaginated'
VARIABLE_DATA_NAME_PAGINATED = 'getRunsPaginatedData'
QUERY = f"""
query GetRunsPaginated(${VARIABLE_DATA_NAME_PAGINATED}: GetRunsPaginatedInput!) {{
  {QUERY_FUNCTION_PAGINATED}({VARIABLE_DATA_NAME_PAGINATED}: ${VARIABLE_DATA_NAME_PAGINATED}) {{
  cursor
  hasNextPage
  runs {{
    id
    name
    status
    createdAt
    updatedAt
    reason
    createdByEmail
    priority
    maxRetries
    preemptible
    retryOnSystemFailure
    maxDurationSeconds
    isDeleted
    runType
    resumptions {{
        clusterName
        cpus
        gpuType
        gpus
        nodes
        executionIndex
        startTime
        endTime
        status
        estimatedEndTime
        reason
    }}
  }}
  }}
}}"""

QUERY_WITH_DETAILS = f"""
query GetRunsPaginated(${VARIABLE_DATA_NAME_PAGINATED}: GetRunsPaginatedInput!) {{
  {QUERY_FUNCTION_PAGINATED}({VARIABLE_DATA_NAME_PAGINATED}: ${VARIABLE_DATA_NAME_PAGINATED}) {{
  cursor
  hasNextPage
  runs {{
    id
    name
    status
    createdAt
    updatedAt
    reason
    createdByEmail
    priority
    maxRetries
    preemptible
    retryOnSystemFailure
    maxDurationSeconds
    runType
    isDeleted
    resumptions {{
        clusterName
        cpus
        gpuType
        gpus
        nodes
        executionIndex
        startTime
        endTime
        status
        estimatedEndTime
        reason
    }}
    details {{
        image
        originalRunInput
        metadata
        lastExecutionId
        lifecycle {{
            executionIndex
            status
            startTime
            endTime
            reason
        }}
        nodes {{
            rank
            name
            status
            reason
        }}
        formattedRunEvents {{
            resumptionIndex
            eventType
            eventTime
            eventMessage
        }}
    }}
  }}
  }}
}}"""


@overload
def get_run(
    run: Union[str, Run],
    *,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
    include_details: bool = True,
) -> Run:
    ...


@overload
def get_run(
    run: Union[str, Run],
    *,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
    include_details: bool = True,
) -> Future[Run]:
    ...


def get_run(
    run: Union[str, Run],
    *,
    timeout: Optional[float] = 10,
    future: bool = False,
    include_details: bool = True,
):
    """Get a run that has been launched in the MosaicML platform

    The run will contain all details requested

    Arguments:
        run: Run on which to get information
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to `get_runs` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of runs, use ``return_value.result()``
            with an optional ``timeout`` argument.
        include_details: If true, will fetch detailed information like run input for each run.

    Raises:
        MAPIException: If connecting to MAPI, raised when a MAPI communication error occurs
    """

    runs = cast(Union[List[str], List[Run]], [run])
    error_message = f'Run {run.name if isinstance(run, Run) else run} not found'

    if future:
        res = get_runs(runs=runs, timeout=None, future=True, include_details=include_details, limit=1)
        return convert_plural_future_to_singleton(res, error_message)

    res = get_runs(runs=runs, timeout=timeout, future=False, include_details=include_details)
    if not res:
        raise MAPIException(HTTPStatus.NOT_FOUND, error_message)
    return res[0]


@overload
def get_runs(
    runs: Optional[Union[List[str], List[Run], ObjectList[Run]]] = None,
    *,
    cluster_names: Optional[Union[List[str], List[ClusterDetails], ObjectList[ClusterDetails]]] = None,
    before: Optional[Union[str, datetime]] = None,
    after: Optional[Union[str, datetime]] = None,
    gpu_types: Optional[Union[List[str], List[GPUType]]] = None,
    gpu_nums: Optional[List[int]] = None,
    statuses: Optional[Union[List[str], List[RunStatus]]] = None,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
    user_emails: Optional[List[str]] = None,
    run_types: Optional[Union[List[str], List[RunType]]] = None,
    include_details: bool = False,
    include_deleted: bool = False,
    ended_before: Optional[Union[str, datetime]] = None,
    ended_after: Optional[Union[str, datetime]] = None,
    limit: Optional[int] = DEFAULT_LIMIT,
    all_users: bool = False,
) -> ObjectList[Run]:
    ...


@overload
def get_runs(
    runs: Optional[Union[List[str], List[Run], ObjectList[Run]]] = None,
    *,
    cluster_names: Optional[Union[List[str], List[ClusterDetails], ObjectList[ClusterDetails]]] = None,
    before: Optional[Union[str, datetime]] = None,
    after: Optional[Union[str, datetime]] = None,
    gpu_types: Optional[Union[List[str], List[GPUType]]] = None,
    gpu_nums: Optional[List[int]] = None,
    statuses: Optional[Union[List[str], List[RunStatus]]] = None,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
    user_emails: Optional[List[str]] = None,
    run_types: Optional[Union[List[str], List[RunType]]] = None,
    include_details: bool = False,
    include_deleted: bool = False,
    ended_before: Optional[Union[str, datetime]] = None,
    ended_after: Optional[Union[str, datetime]] = None,
    limit: Optional[int] = DEFAULT_LIMIT,
    all_users: bool = False,
) -> Future[ObjectList[Run]]:
    ...


def get_runs(
    runs: Optional[Union[List[str], List[Run], ObjectList[Run]]] = None,
    *,
    cluster_names: Optional[Union[List[str], List[ClusterDetails], ObjectList[ClusterDetails]]] = None,
    before: Optional[Union[str, datetime]] = None,
    after: Optional[Union[str, datetime]] = None,
    gpu_types: Optional[Union[List[str], List[GPUType]]] = None,
    gpu_nums: Optional[List[int]] = None,
    statuses: Optional[Union[List[str], List[RunStatus]]] = None,
    timeout: Optional[float] = 10,
    future: bool = False,
    user_emails: Optional[List[str]] = None,
    run_types: Optional[Union[List[str], List[RunType]]] = None,
    include_details: bool = False,
    include_deleted: bool = False,
    ended_before: Optional[Union[str, datetime]] = None,
    ended_after: Optional[Union[str, datetime]] = None,
    limit: Optional[int] = DEFAULT_LIMIT,
    all_users: bool = False,
):
    """List runs that have been launched in the MosaicML platform

    The returned list will contain all of the details stored about the requested runs.

    Arguments:
        runs: List of runs on which to get information
        cluster_names: List of cluster names to filter runs. This can be a list of str or
            :type Cluster: objects. Only runs submitted to these clusters will be
            returned.
        before: Only runs created strictly before this time will be returned. This
            can be a str in ISO 8601 format(e.g 2023-03-31T12:23:04.34+05:30)
            or a datetime object.
        after: Only runs created at or after this time will be returned. This can
            be a str in ISO 8601 format(e.g 2023-03-31T12:23:04.34+05:30)
            or a datetime object.
        gpu_types: List of gpu types to filter runs. This can be a list of str or
            :type GPUType: enums. Only runs scheduled on these GPUs will be returned.
        gpu_nums: List of gpu counts to filter runs. Only runs scheduled on this number
            of GPUs will be returned.
        statuses: List of run statuses to filter runs. This can be a list of str or
            :type RunStatus: enums. Only runs currently in these phases will be returned.
        user_emails: List of user emails to filter runs. Only runs submitted by these
            users will be returned. By default, will return runs submitted by the
            current user. Requires shared runs or admin permission
        run_types: List of run types to filter runs
            - 'INTERACTIVE': Runs created with the `mcli interactive` command
            - 'HERO_RUN': Runs created with `is_hero_run` in the metadata
            - 'TRAINING': All other runs
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to `get_runs` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of runs, use ``return_value.result()``
            with an optional ``timeout`` argument.
        include_details: If true, will fetch detailed information like run input for each run.
        include_deleted: If true, will include deleted runs in the response.
        ended_before: Only runs ended strictly before this time will be returned.
        ended_after: Only runs ended at or after this time will be returned.
        limit: Maximum number of runs to return. If None, the latest 100 runs will be returned.
        all_users: If true, will return runs from all users in the organization (if permitted).

    Raises:
        MAPIException: If connecting to MAPI, raised when a MAPI communication error occurs
    """

    filters = {}
    if runs:
        filters['name'] = {'in': [r.name if isinstance(r, Run) else r for r in runs]}
    if before or after:
        date_filters = {}
        if before:
            date_filters['lt'] = before.astimezone().isoformat() if isinstance(before, datetime) else before
        if after:
            date_filters['gte'] = after.astimezone().isoformat() if isinstance(after, datetime) else after
        filters['createdAt'] = date_filters
    if ended_before or ended_after:
        date_filters = {}
        if ended_before:
            date_filters['lt'] = ended_before.astimezone().isoformat() if isinstance(ended_before,
                                                                                     datetime) else ended_before
        if ended_after:
            date_filters['gte'] = ended_after.astimezone().isoformat() if isinstance(ended_after,
                                                                                     datetime) else ended_after
        filters['endedAt'] = date_filters

    if statuses:
        filters['status'] = {'in': [s.value.upper() if isinstance(s, RunStatus) else s.upper() for s in statuses]}

    if cluster_names:
        filters['clusterName'] = {'in': [c if isinstance(c, str) else c.name for c in cluster_names]}
    if gpu_types:
        filters['gpuType'] = {'in': [gt.value if isinstance(gt, GPUType) else gt for gt in gpu_types]}
    if gpu_nums:
        filters['gpuNum'] = {'in': gpu_nums}

    if run_types:
        filters['runType'] = {'in': [r.value.upper() if isinstance(r, RunType) else r.upper() for r in run_types]}

    variables = {
        VARIABLE_DATA_NAME_PAGINATED: {
            'filters': filters,
            'includeDeleted': include_deleted,
            'limit': limit,
        },
    }

    cfg = MCLIConfig.load_config()
    cfg.update_entity(variables[VARIABLE_DATA_NAME_PAGINATED])

    def get_first_org_id():
        return [get_current_user().organizations[0].id]

    if all_users:
        entity = variables[VARIABLE_DATA_NAME_PAGINATED].get('entity')
        if entity is not None:
            entity.pop('userIds', None)
            if 'organizationIds' not in entity:
                entity['organizationIds'] = get_first_org_id()
        else:
            variables[VARIABLE_DATA_NAME_PAGINATED]['entity'] = {'organizationIds': get_first_org_id()}

    if user_emails:
        if variables[VARIABLE_DATA_NAME_PAGINATED].get('entity'):
            variables[VARIABLE_DATA_NAME_PAGINATED]['entity']['emails'] = user_emails
        else:
            variables[VARIABLE_DATA_NAME_PAGINATED]['entity'] = {'emails': user_emails}

    response = run_paginated_mapi_request(
        query=QUERY if not include_details else QUERY_WITH_DETAILS,
        query_function=QUERY_FUNCTION_PAGINATED,
        return_model_type=Run,
        variables=variables,
    )

    return get_return_response(response, future=future, timeout=timeout)
