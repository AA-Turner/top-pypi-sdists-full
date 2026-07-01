""" Update a deployment. """
from __future__ import annotations

from concurrent.futures import Future
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast, overload

from typing_extensions import Literal

from mcli.api.engine.engine import convert_plural_future_to_singleton, get_return_response, run_plural_mapi_request
from mcli.api.exceptions import MAPIException
from mcli.api.model.inference_deployment import InferenceDeployment
from mcli.config import MCLIConfig
from mcli.models.common import ObjectList

QUERY_FUNCTION = 'updateInferenceDeployments'
VARIABLE_DATA_GET_DEPLOYMENTS = 'getInferenceDeploymentsData'
VARIABLE_DATA_UPDATE_DEPLOYMENTS = 'updateInferenceDeploymentsData'
QUERY = f"""
mutation UpdateInferenceDeployments(${VARIABLE_DATA_GET_DEPLOYMENTS}: GetInferenceDeploymentsInput!, ${VARIABLE_DATA_UPDATE_DEPLOYMENTS}: UpdateInferenceDeploymentsInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_GET_DEPLOYMENTS}: ${VARIABLE_DATA_GET_DEPLOYMENTS}, {VARIABLE_DATA_UPDATE_DEPLOYMENTS}: ${VARIABLE_DATA_UPDATE_DEPLOYMENTS}) {{
    id
    name
    inferenceDeploymentInput
    originalInferenceDeploymentInput
    status
    createdById
    organizationId
    createdAt
    updatedAt
    clusterId
    isDeleted
    publicDNS
    deletedAt
    createdByEmail
  }}
}}"""

__all__ = ['update_inference_deployments', 'update_inference_deployment']


@overload
def update_inference_deployment(
    deployment: Union[str, InferenceDeployment],
    updates: Dict[str, Any],
    *,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> InferenceDeployment:
    ...


@overload
def update_inference_deployment(
    deployment: Union[str, InferenceDeployment],
    updates: Dict[str, Any],
    *,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[InferenceDeployment]:
    ...


def update_inference_deployment(
    deployment: Union[str, InferenceDeployment],
    updates: Dict[str, Any],
    *,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Updates a single inference deployment that has been launched in the MosaicML platform

    Any deployments that are currently running will not be interrupted.

    Args:
        deployment: An inference deployment or inference deployment name to update
        updates: A dictionary of inference deployment fields to update
            (eg. {"image": "new_image", "replicas": 2})
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to `update_inference_deployments` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :type InferenceDeployment: output, use ``return_value.result()``
            with an optional ``timeout`` argument.

    Raises:
        MAPIException: Raised if updating the deployment failed

    Returns:
        A :type InferenceDeployment: for the deployment that was updated
    """
    deployments = cast(Union[List[str], List[InferenceDeployment]], [deployment])
    name = deployment.name if isinstance(deployment, InferenceDeployment) else deployment
    error_message = f"Deployment {name} not found"

    if future:
        res = update_inference_deployments(deployments=deployments, updates=updates, timeout=None, future=True)
        return convert_plural_future_to_singleton(res, error_message)

    res = update_inference_deployments(deployments=deployments, updates=updates, timeout=timeout, future=False)
    if not res:
        raise MAPIException(HTTPStatus.NOT_FOUND, error_message)
    return res[0]


@overload
def update_inference_deployments(
    deployments: Union[List[str], List[InferenceDeployment], ObjectList[InferenceDeployment]],
    updates: Dict[str, Any],
    *,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> ObjectList[InferenceDeployment]:
    ...


@overload
def update_inference_deployments(
    deployments: Union[List[str], List[InferenceDeployment], ObjectList[InferenceDeployment]],
    updates: Dict[str, Any],
    *,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[ObjectList[InferenceDeployment]]:
    ...


def update_inference_deployments(
    deployments: Union[List[str], List[InferenceDeployment], ObjectList[InferenceDeployment]],
    updates: Dict[str, Any],
    *,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Updates a list of inference deployments that have been launched in the MosaicML platform

    Any deployments that are currently running will not be interrupted.

    Args:
        deployments: A list of inference deployments or inference deployment names to update
        updates: A dictionary of inference deployment fields to update
            (eg. {"image": "new_image", "replicas": 2})
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to `update_inference_deployments` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :type InferenceDeployment: output, use ``return_value.result()``
            with an optional ``timeout`` argument.

    Raises:
        MAPIException: Raised if updating the deployments failed

    Returns:
        A list of :type InferenceDeployment: for the deployments that were updated
    """
    # Extract deployment names
    variables = {
        VARIABLE_DATA_GET_DEPLOYMENTS: {
            'filters': {
                'name': {
                    'in': [d.name if isinstance(d, InferenceDeployment) else d for d in deployments]
                },
            }
        },
        VARIABLE_DATA_UPDATE_DEPLOYMENTS: updates,
    }

    cfg = MCLIConfig.load_config()
    cfg.update_entity(variables[VARIABLE_DATA_GET_DEPLOYMENTS], set_user=False)

    response = run_plural_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=InferenceDeployment,
        variables=variables,
    )

    return get_return_response(response, future=future, timeout=timeout)
