""" Create a InferenceDeployment """
from __future__ import annotations

from concurrent.futures import Future
from typing import Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import get_return_response, run_singular_mapi_request
from mcli.api.model.inference_deployment import InferenceDeployment
from mcli.models.inference_deployment_config import FinalInferenceDeploymentConfig, InferenceDeploymentConfig

QUERY_FUNCTION = 'createInferenceDeployment'
VARIABLE_DATA_NAME = 'createInferenceDeploymentData'
QUERY = f"""
mutation CreateInferenceDeployment(${VARIABLE_DATA_NAME}: CreateInferenceDeploymentInput!) {{
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


@overload
def create_inference_deployment(
    deployment: Union[InferenceDeploymentConfig, FinalInferenceDeploymentConfig],
    *,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> InferenceDeployment:
    ...


@overload
def create_inference_deployment(
    deployment: Union[InferenceDeploymentConfig, FinalInferenceDeploymentConfig],
    *,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[InferenceDeployment]:
    ...


def create_inference_deployment(
    deployment: Union[InferenceDeploymentConfig, FinalInferenceDeploymentConfig],
    *,
    timeout: Optional[float] = 10,
    future: bool = False,
) -> Union[InferenceDeployment, Future[InferenceDeployment]]:
    """Launch a inference deployment in the MosaicML platform

    The provided :class:`deploy <mcli.models.inference_deployment_config.InferenceDeploymentConfig>` must contain
    enough information to fully detail the inference deployment

    Args:
        deployment: A fully-configured inference deployment to launch. The deployment will be queued and persisted
            in the deployment database.
        timeout: Time, in seconds, in which the call should complete. If the deployment creation
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to `create_deployment` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :type InferenceDeployment: output, use ``return_value.result()``
            with an optional ``timeout`` argument.
    Returns:
        A InferenceDeployment that includes the launched deployment details and the deployment status
    """

    if isinstance(deployment, InferenceDeploymentConfig):
        deployment = FinalInferenceDeploymentConfig.finalize_config(deployment)

    variables = {
        VARIABLE_DATA_NAME: deployment.to_create_deployment_api_input(),
    }

    response = run_singular_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=InferenceDeployment,
        variables=variables,
    )

    return get_return_response(response, future=future, timeout=timeout)
