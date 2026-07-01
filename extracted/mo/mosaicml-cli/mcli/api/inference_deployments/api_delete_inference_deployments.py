""" Delete a deployment. """
from __future__ import annotations

from concurrent.futures import Future
from typing import List, Optional, Union, cast, overload

from typing_extensions import Literal

from mcli.api.engine.engine import convert_plural_future_to_singleton, get_return_response, run_plural_mapi_request
from mcli.api.model.inference_deployment import InferenceDeployment
from mcli.config import MCLIConfig
from mcli.models.common import ObjectList

QUERY_FUNCTION = 'deleteInferenceDeployments'
VARIABLE_DATA_NAME = 'getInferenceDeploymentsData'
QUERY = f"""
mutation DeleteInferenceDeployments(${VARIABLE_DATA_NAME}: GetInferenceDeploymentsInput!) {{
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
    createdByEmail
  }}
}}"""

__all__ = ['delete_inference_deployments', 'delete_inference_deployment']


@overload
def delete_inference_deployment(
    deployment: Union[str, InferenceDeployment],
    *,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> InferenceDeployment:
    ...


@overload
def delete_inference_deployment(
    deployment: Union[str, InferenceDeployment],
    *,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[InferenceDeployment]:
    ...


def delete_inference_deployment(
    deployment: Union[str, InferenceDeployment],
    *,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Delete an inference deployment in the MosaicML Cloud

    If it is currently running the deployment will first be stopped.

    Args:
        deployment: An inference deployments or inference deployment name to delete
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to `delete_inference_deployments` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :type InferenceDeployment: output, use ``return_value.result()``
            with an optional ``timeout`` argument.

    Returns:
        A :type InferenceDeployment: that was deleted
    """
    deployments = cast(Union[List[str], List[InferenceDeployment]], [deployment])

    if future:
        res = delete_inference_deployments(deployments=deployments, timeout=None, future=True)
        return convert_plural_future_to_singleton(res)

    return delete_inference_deployments(deployments=deployments, timeout=timeout, future=False)[0]


@overload
def delete_inference_deployments(
    deployments: Union[List[str], List[InferenceDeployment], ObjectList[InferenceDeployment]],
    *,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> ObjectList[InferenceDeployment]:
    ...


@overload
def delete_inference_deployments(
    deployments: Union[List[str], List[InferenceDeployment], ObjectList[InferenceDeployment]],
    *,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[ObjectList[InferenceDeployment]]:
    ...


def delete_inference_deployments(
    deployments: Union[List[str], List[InferenceDeployment], ObjectList[InferenceDeployment]],
    *,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Delete a list of inference deployments in the MosaicML Cloud

    Any deployments that are currently running will first be stopped.

    Args:
        deployments: A list of inference deployments or inference deployment names to delete
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to `delete_inference_deployments` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :type InferenceDeployment: output, use ``return_value.result()``
            with an optional ``timeout`` argument.

    Returns:
        A list of :type InferenceDeployment: for the inference deployments that were deleted
    """
    # Extract run names
    deployment_names = [d.name if isinstance(d, InferenceDeployment) else d for d in deployments]

    filters = {}
    if deployment_names:
        filters['name'] = {'in': deployment_names}

    variables = {VARIABLE_DATA_NAME: {'filters': filters}}

    cfg = MCLIConfig.load_config()
    cfg.update_entity(variables[VARIABLE_DATA_NAME], set_user=False)

    response = run_plural_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=InferenceDeployment,
        variables=variables,
    )

    return get_return_response(response, future=future, timeout=timeout)
