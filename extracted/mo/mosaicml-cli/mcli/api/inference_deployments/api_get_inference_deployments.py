"""get__inference_deployments SDK for MAPI"""
from __future__ import annotations

from concurrent.futures import Future
from datetime import datetime
from http import HTTPStatus
from typing import List, Optional, Union, cast, overload

from typing_extensions import Literal

from mcli.api.engine.engine import convert_plural_future_to_singleton, get_return_response, run_plural_mapi_request
from mcli.api.exceptions import MAPIException
from mcli.api.model.cluster_details import ClusterDetails
from mcli.api.model.inference_deployment import InferenceDeployment
from mcli.config import MCLIConfig
from mcli.models.common import ObjectList
from mcli.models.gpu_type import GPUType

__all__ = ['get_inference_deployments', 'get_inference_deployment']

QUERY_FUNCTION = 'getInferenceDeployments'
VARIABLE_DATA_NAME = 'getInferenceDeploymentsData'
QUERY = f"""
query GetInferenceDeployments(${VARIABLE_DATA_NAME}: GetInferenceDeploymentsInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
    id
    name
    inferenceDeploymentInput
    originalInferenceDeploymentInput
    status
    createdAt
    updatedAt
    deletedAt
    publicDNS
    currentVersion
    createdByEmail
    replicas{{
        name
        status
        latestRestartCount
        latestRestartTime
    }}
  }}
}}"""


@overload
def get_inference_deployment(
    deployment: Union[str, InferenceDeployment],
    *,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> InferenceDeployment:
    ...


@overload
def get_inference_deployment(
    deployment: Union[str, InferenceDeployment],
    *,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[InferenceDeployment]:
    ...


def get_inference_deployment(
    deployment: Union[str, InferenceDeployment],
    *,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Gets a single inference deployment that has been launched in the MosaicML platform

    The returned object will contain all of the details stored about the requested deployment.

    Arguments:
        deployment: Inference deployment object or name string
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to `get_inference_deployment` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of deployments, use ``return_value.result()``
            with an optional ``timeout`` argument.
    Raises:
        MAPIException: Raised when a MAPI communication error occurs
    """
    deployments = cast(Union[List[str], List[InferenceDeployment]], [deployment])
    name = deployment.name if isinstance(deployment, InferenceDeployment) else deployment
    error_message = f"Deployment {name} not found"

    if future:
        res = get_inference_deployments(deployments=deployments, timeout=None, future=True)
        return convert_plural_future_to_singleton(res, error_message)

    res = get_inference_deployments(deployments=deployments, timeout=timeout, future=False)
    if not res:
        raise MAPIException(HTTPStatus.NOT_FOUND, error_message)
    return res[0]


@overload
def get_inference_deployments(
    deployments: Optional[Union[List[str], List[InferenceDeployment], ObjectList[InferenceDeployment]]] = None,
    *,
    clusters: Optional[Union[List[str], List[ClusterDetails], ObjectList[ClusterDetails]]] = None,
    before: Optional[Union[str, datetime]] = None,
    after: Optional[Union[str, datetime]] = None,
    gpu_types: Optional[Union[List[str], List[GPUType]]] = None,
    gpu_nums: Optional[List[int]] = None,
    statuses: Optional[List[str]] = None,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> ObjectList[InferenceDeployment]:
    ...


@overload
def get_inference_deployments(
    deployments: Optional[Union[List[str], List[InferenceDeployment], ObjectList[InferenceDeployment]]] = None,
    *,
    clusters: Optional[Union[List[str], List[ClusterDetails], ObjectList[ClusterDetails]]] = None,
    before: Optional[Union[str, datetime]] = None,
    after: Optional[Union[str, datetime]] = None,
    gpu_types: Optional[Union[List[str], List[GPUType]]] = None,
    gpu_nums: Optional[List[int]] = None,
    statuses: Optional[List[str]] = None,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[ObjectList[InferenceDeployment]]:
    ...


def get_inference_deployments(
    deployments: Optional[Union[List[str], List[InferenceDeployment], ObjectList[InferenceDeployment]]] = None,
    *,
    clusters: Optional[Union[List[str], List[ClusterDetails], ObjectList[ClusterDetails]]] = None,
    before: Optional[Union[str, datetime]] = None,
    after: Optional[Union[str, datetime]] = None,
    gpu_types: Optional[Union[List[str], List[GPUType]]] = None,
    gpu_nums: Optional[List[int]] = None,
    statuses: Optional[List[str]] = None,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """List inference deployments that have been launched in the MosaicML platform

    The returned list will contain all of the details stored about the requested deployments.

    Arguments:
        deployments: List of inference deployments on which to get information
        clusters: List of clusters to filter inference deployments. This can be a list of str or
            :type Cluster: objects. Only deployments submitted to these clusters will be
            returned.
        before: Only inference deployments created strictly before this time will be returned. This
            can be a str in ISO 8601 format(e.g 2023-03-31T12:23:04.34+05:30)
            or a datetime object.
        after: Only inference deployments created at or after this time will be returned. This can
            be a str in ISO 8601 format(e.g 2023-03-31T12:23:04.34+05:30)
            or a datetime object.
        gpu_types: List of gpu types to filter inference deployments. This can be a list of str or
            :type GPUType: enums. Only deployments scheduled on these GPUs will be returned.
        gpu_nums: List of gpu counts to filter inference deployments. Only deployments scheduled on this number
            of GPUs will be returned.
        statuses: List of inference deployment statuses to filter deployments. This can be a list of str.
            Only deployments currently in these phases will be returned.
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to `get_inference_deployments` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of deployments, use ``return_value.result()``
            with an optional ``timeout`` argument.
    Raises:
        MAPIException: If connecting to MAPI, raised when a MAPI communication error occurs
    """

    filters = {}
    if deployments:
        filters['name'] = {'in': [r.name if isinstance(r, InferenceDeployment) else r for r in deployments]}
    if before or after:
        date_filters = {}
        if before:
            date_filters['lt'] = before.astimezone().isoformat() if isinstance(before, datetime) else before
        if after:
            date_filters['gte'] = after.astimezone().isoformat() if isinstance(after, datetime) else after
        filters['createdAt'] = date_filters
    if statuses:
        filters['status'] = {'in': statuses}
    if clusters:
        filters['cluster'] = {'in': [c if isinstance(c, str) else c.name for c in clusters]}
    if gpu_types:
        filters['gpuType'] = {'in': [gt.value if isinstance(gt, GPUType) else gt for gt in gpu_types]}
    if gpu_nums:
        filters['gpuNum'] = {'in': gpu_nums}

    variables = {
        VARIABLE_DATA_NAME: {
            'filters': filters,
            'includeDeleted': False,
        },
    }

    cfg = MCLIConfig.load_config()
    cfg.update_entity(variables[VARIABLE_DATA_NAME], set_user=False)

    response = run_plural_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=InferenceDeployment,
        variables=variables,
    )

    return get_return_response(response, future=future, timeout=timeout)
