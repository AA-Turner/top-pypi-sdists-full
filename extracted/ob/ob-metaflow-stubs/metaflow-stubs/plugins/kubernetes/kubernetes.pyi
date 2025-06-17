######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.927650                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...metaflow_current import current as current
from ...exception import MetaflowException as MetaflowException
from ...mf_extensions.outerbounds.remote_config import init_config as init_config
from .kubernetes_client import KubernetesClient as KubernetesClient

ARGO_EVENTS_EVENT: None

ARGO_EVENTS_EVENT_BUS: str

ARGO_EVENTS_EVENT_SOURCE: None

ARGO_EVENTS_INTERNAL_WEBHOOK_URL: None

ARGO_EVENTS_SERVICE_ACCOUNT: None

ARGO_EVENTS_WEBHOOK_AUTH: str

ARGO_WORKFLOWS_KUBERNETES_SECRETS: str

ARGO_WORKFLOWS_ENV_VARS_TO_SKIP: str

AWS_SECRETS_MANAGER_DEFAULT_REGION: None

AZURE_KEY_VAULT_PREFIX: None

AZURE_STORAGE_BLOB_SERVICE_ENDPOINT: None

CARD_AZUREROOT: None

CARD_GSROOT: None

CARD_S3ROOT: None

DATASTORE_SYSROOT_AZURE: None

DATASTORE_SYSROOT_GS: None

DATASTORE_SYSROOT_S3: None

DATATOOLS_S3ROOT: None

DEFAULT_AWS_CLIENT_PROVIDER: str

DEFAULT_GCP_CLIENT_PROVIDER: str

DEFAULT_METADATA: str

DEFAULT_SECRETS_BACKEND_TYPE: None

GCP_SECRET_MANAGER_PREFIX: None

KUBERNETES_FETCH_EC2_METADATA: bool

KUBERNETES_SANDBOX_INIT_SCRIPT: None

OTEL_ENDPOINT: None

S3_ENDPOINT_URL: None

S3_SERVER_SIDE_ENCRYPTION: None

SERVICE_HEADERS: dict

KUBERNETES_SECRETS: str

SERVICE_INTERNAL_URL: None

UBF_CONTROL: str

UBF_TASK: str

BASH_SAVE_LOGS: str

LOGS_DIR: str

STDOUT_FILE: str

STDERR_FILE: str

STDOUT_PATH: str

STDERR_PATH: str

METAFLOW_PARALLEL_STEP_CLI_OPTIONS_TEMPLATE: str

class KubernetesException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class KubernetesKilledException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class Kubernetes(object, metaclass=type):
    def __init__(self, datastore, metadata, environment):
        ...
    def launch_job(self, **kwargs):
        ...
    def create_jobset(self, flow_name, run_id, step_name, task_id, attempt, user, code_package_sha, code_package_url, code_package_ds, docker_image, docker_image_pull_policy, image_pull_secrets = None, step_cli = None, service_account = None, secrets = None, node_selector = None, namespace = None, cpu = None, gpu = None, gpu_vendor = None, disk = None, memory = None, use_tmpfs = None, tmpfs_tempdir = None, tmpfs_size = None, tmpfs_path = None, run_time_limit = None, env = None, persistent_volume_claims = None, tolerations = None, labels = None, annotations = None, shared_memory = None, port = None, num_parallel = None, qos = None, security_context = None):
        ...
    def create_job_object(self, flow_name, run_id, step_name, task_id, attempt, user, code_package_sha, code_package_url, code_package_ds, step_cli, docker_image, docker_image_pull_policy, image_pull_secrets = None, service_account = None, secrets = None, node_selector = None, namespace = None, cpu = None, gpu = None, gpu_vendor = None, disk = None, memory = None, use_tmpfs = None, tmpfs_tempdir = None, tmpfs_size = None, tmpfs_path = None, run_time_limit = None, env = None, persistent_volume_claims = None, tolerations = None, labels = None, shared_memory = None, port = None, name_pattern = None, qos = None, annotations = None, security_context = None):
        ...
    def create_k8sjob(self, job):
        ...
    def wait(self, stdout_location, stderr_location, echo = None):
        ...
    ...

