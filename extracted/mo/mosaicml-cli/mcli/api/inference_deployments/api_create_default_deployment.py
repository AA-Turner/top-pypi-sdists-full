""" Create a InferenceDeployment """
from __future__ import annotations

from concurrent.futures import Future
from typing import Dict, Optional, Union, cast, overload

from typing_extensions import Literal

from mcli.api.engine.engine import get_return_response, run_singular_mapi_request
from mcli.api.inference_deployments.api_create_inference_deployment import QUERY, QUERY_FUNCTION, VARIABLE_DATA_NAME
from mcli.api.model.inference_deployment import InferenceDeployment
from mcli.models.inference_deployment_config import (DefaultModelConfig, FinalInferenceDeploymentConfig,
                                                     InferenceDeploymentConfig)
from mcli.utils.utils_config import ComputeConfig


@overload
def create_default_deployment(
    name: str,
    compute: Union[Dict[str, str], ComputeConfig],
    replicas: int,
    model_type: str,
    checkpoint_path: Dict[str, str],
    *,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> InferenceDeployment:
    ...


@overload
def create_default_deployment(
    name: str,
    compute: Union[Dict[str, str], ComputeConfig],
    replicas: int,
    model_type: str,
    checkpoint_path: Dict[str, str],
    *,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[InferenceDeployment]:
    ...


def create_default_deployment(
    name: str,
    compute: Union[Dict[str, str], ComputeConfig],
    replicas: int,
    model_type: str,
    checkpoint_path: Dict[str, str],
    *,
    timeout: Optional[float] = 10,
    future: bool = False,
) -> Union[InferenceDeployment, Future[InferenceDeployment]]:
    """Launch a default inference deployment in the MosaicML platform

    Deploys an optimized inference deployment for the given model type using the specified checkpoint.

    Args:
        name: Name for the created inference deployment
        compute: A :class:`compute <mcli.utils.utils_config.ComputeConfig>` specifying the resources to deploy
        this deployment with.
        replicas: The number of replicas that should be created for this deployment
        model_type: The model type to deploy
        checkpoint_path: A dictionary specifing where to fetch the model checkpoint from. Keys should be sources
        (e.g hf_path, s3_path, gpc_path) and values the respective paths.
        timeout: Time, in seconds, in which the call should complete. If the deployment creation
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :type concurrent.futures.Future:. If True, the
            call to `create_deployment` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :type InferenceDeployment: output, use ``return_value.result()``
            with an optional ``timeout`` argument.
    Returns:
        A InferenceDeployment that includes the launched deployment details and the deployment status
    """

    compute = cast(ComputeConfig, compute)
    config = InferenceDeploymentConfig(name=name,
                                       compute=compute,
                                       replicas=replicas,
                                       default_model=DefaultModelConfig(model_type=model_type,
                                                                        checkpoint_path=checkpoint_path))
    deployment = FinalInferenceDeploymentConfig.finalize_config(config)

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
