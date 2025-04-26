""" API calls for deployment management """
# pylint: disable=cyclic-import
from mcli.api.inference_deployments.api_create_default_deployment import create_default_deployment
from mcli.api.inference_deployments.api_create_inference_deployment import create_inference_deployment
from mcli.api.inference_deployments.api_delete_inference_deployments import (delete_inference_deployment,
                                                                             delete_inference_deployments)
from mcli.api.inference_deployments.api_get_inference_deployment_logs import get_inference_deployment_logs
from mcli.api.inference_deployments.api_get_inference_deployments import (get_inference_deployment,
                                                                          get_inference_deployments)
from mcli.api.inference_deployments.api_ping import ping
from mcli.api.inference_deployments.api_predict_inference_deployment import predict
from mcli.api.inference_deployments.api_stop_inference_deployments import (stop_inference_deployment,
                                                                           stop_inference_deployments)
from mcli.api.inference_deployments.api_update_inference_deployments import (update_inference_deployment,
                                                                             update_inference_deployments)
from mcli.api.model.inference_deployment import InferenceDeployment
from mcli.models import InferenceDeploymentConfig

__all__ = [
    "create_default_deployment",
    "create_inference_deployment",
    "delete_inference_deployment",
    "delete_inference_deployments",
    "get_inference_deployment_logs",
    "get_inference_deployment",
    "get_inference_deployments",
    "InferenceDeployment",
    "InferenceDeploymentConfig",
    "ping",
    "predict",
    "stop_inference_deployment",
    "stop_inference_deployments",
    "update_inference_deployment",
    "update_inference_deployments",
]
