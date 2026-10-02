# Copyright 2023 Agnostiq Inc.


from importlib import metadata

from . import cloud_executor
from .cloud_executor.cloud_executor import CloudExecutor
from .cloud_executor.oci_cloud_executor import OCICloudExecutor
from .dispatch_management import (
    cancel,
    dispatch,
    get_dispatches,
    get_first_failure,
    get_node_errors,
    get_node_results,
    get_node_stderr,
    get_node_stdout,
    get_result,
    redispatch,
)
from .function_serve.decorators import service
from .function_serve.deployment import (
    create_inference_api_key,
    delete_inference_api_key,
    deploy,
    get_deployment,
    list_function_deployments,
    list_inference_api_keys,
)
from .function_serve.models import (
    Deployment,
    FunctionDeploymentList,
    InferenceAPIKey,
    InferenceKeyMetadata,
)
from .service_account_interface.auth_config_manager import (
    get_api_key,
    get_dr_api_token,
    save_api_key,
    save_dr_api_token,
)
from .service_account_interface.client import get_client
from .shared.classes.exceptions import (
    AuthenticationError,
    CovalentCloudError,
    ResourceNotFoundError,
    ValidationError,
)
from .shared.classes.settings import settings
from .shared.schemas.dispatch import DispatchListResponse, DispatchMetadata, DispatchRecord
from .shared.schemas.node import NodeError, NodeFailure, NodeOutput, NodeResult, NodeStderr
from .swe_management.models.environment_logs import EnvironmentLogs, LogEvent
from .swe_management.models.hardware import HardwareListResponse, HardwareSpec
from .swe_management.secrets_manager import delete_secret, list_secrets, store_secret
from .swe_management.swe_manager import (
    create_env,
    delete_env,
    get_environment_build_logs,
    get_environment_yaml,
    get_envs,
    list_hardware,
)
from .volume.volume import volume

__version__ = metadata.version("covalent_cloud")

__all__ = [
    "cloud_executor",
    "CloudExecutor",
    "OCICloudExecutor",
    "cancel",
    "dispatch",
    "get_result",
    "redispatch",
    "get_dispatches",
    "get_node_results",
    "get_node_errors",
    "get_node_stdout",
    "get_node_stderr",
    "get_first_failure",
    "get_api_key",
    "save_api_key",
    "get_dr_api_token",
    "save_dr_api_token",
    "get_client",
    "settings",
    "CovalentCloudError",
    "ResourceNotFoundError",
    "AuthenticationError",
    "ValidationError",
    "DispatchListResponse",
    "DispatchRecord",
    "DispatchMetadata",
    "NodeResult",
    "NodeError",
    "NodeOutput",
    "NodeStderr",
    "NodeFailure",
    "delete_secret",
    "list_secrets",
    "store_secret",
    "create_env",
    "get_envs",
    "delete_env",
    "get_environment_yaml",
    "get_environment_build_logs",
    "list_hardware",
    "EnvironmentLogs",
    "LogEvent",
    "HardwareSpec",
    "HardwareListResponse",
    "volume",
    "deploy",
    "get_deployment",
    "list_function_deployments",
    "create_inference_api_key",
    "list_inference_api_keys",
    "delete_inference_api_key",
    "Deployment",
    "FunctionDeploymentList",
    "InferenceAPIKey",
    "InferenceKeyMetadata",
    "service",
]
