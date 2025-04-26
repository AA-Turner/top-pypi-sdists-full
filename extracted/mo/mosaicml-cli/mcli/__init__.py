""" MCLI Package """

from mcli.api.cluster import ClusterDetails, get_cluster, get_clusters
from mcli.api.engine.engine import PaginatedObjectList
from mcli.api.exceptions import MAPIException
from mcli.api.inference_deployments import (InferenceDeployment, InferenceDeploymentConfig, create_default_deployment,
                                            create_inference_deployment, delete_inference_deployment,
                                            delete_inference_deployments, get_inference_deployment,
                                            get_inference_deployment_logs, get_inference_deployments, ping, predict,
                                            update_inference_deployment, update_inference_deployments)
from mcli.api.model import EventType
from mcli.api.runs import (ComputeConfig, FinalRunConfig, Run, RunConfig, RunStatus, SchedulingConfig,
                           create_interactive_run, create_run, delete_run, delete_runs, follow_run_logs, get_run,
                           get_run_logs, get_runs, start_run, start_runs, stop_run, stop_runs, update_run,
                           update_run_metadata, wait_for_run_status, watch_run_status)
from mcli.api.secrets import create_secret, delete_secrets, get_secrets
from mcli.cli.m_init.m_init import initialize
from mcli.cli.m_set_unset.api_key import set_api_key
from mcli.config import FeatureFlag, MCLIConfig
from mcli.models import ObjectList

from .version import __version__

# Set to none to avoid import errors
LambdaInput = None  # pylint: disable=invalid-name
LambdaResponse = None  # pylint: disable=invalid-name
get_code_eval_output = None

__all__ = [
    'ClusterDetails',
    'ComputeConfig',
    'create_default_deployment',
    'create_inference_deployment',
    'create_interactive_run',
    'create_run',
    'create_secret',
    'delete_inference_deployment',
    'delete_inference_deployments',
    'delete_run',
    'delete_runs',
    'delete_secrets',
    'FeatureFlag',
    'FinalRunConfig',
    'follow_run_logs',
    'get_cluster',
    'get_clusters',
    'get_inference_deployment_logs',
    'get_inference_deployment',
    'get_inference_deployments',
    'get_run_logs',
    'get_run',
    'get_runs',
    'get_secrets',
    'InferenceDeployment',
    'InferenceDeploymentConfig',
    'initialize',
    'ObjectList',
    'EventType',
    'MAPIException',
    'MCLIConfig',
    'PaginatedObjectList',
    'ping',
    'predict',
    'Run',
    'RunConfig',
    'RunStatus',
    'SchedulingConfig',
    'set_api_key',
    'start_run',
    'start_runs',
    'stop_run',
    'stop_runs',
    'update_inference_deployment',
    'update_inference_deployments',
    'update_run_metadata',
    'update_run',
    'wait_for_run_status',
    'watch_run_status',
]
