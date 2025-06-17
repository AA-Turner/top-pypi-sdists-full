######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.928785                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators

from ...metaflow_current import current as current
from ...exception import MetaflowException as MetaflowException
from ...metadata_provider.metadata import MetaDatum as MetaDatum
from ...metadata_provider.util import sync_local_metadata_to_datastore as sync_local_metadata_to_datastore
from ..resources_decorator import ResourcesDecorator as ResourcesDecorator
from ..timeout_decorator import get_run_time_limit_for_task as get_run_time_limit_for_task
from ..aws.aws_utils import get_docker_registry as get_docker_registry
from ..aws.aws_utils import get_ec2_instance_metadata as get_ec2_instance_metadata
from .kubernetes import KubernetesException as KubernetesException
from .kube_utils import validate_kube_labels as validate_kube_labels
from .kube_utils import parse_kube_keyvalue_list as parse_kube_keyvalue_list

DATASTORE_LOCAL_DIR: str

KUBERNETES_CONTAINER_IMAGE: None

KUBERNETES_CONTAINER_REGISTRY: None

KUBERNETES_CPU: None

KUBERNETES_DISK: None

KUBERNETES_FETCH_EC2_METADATA: bool

KUBERNETES_GPU_VENDOR: str

KUBERNETES_IMAGE_PULL_POLICY: None

KUBERNETES_IMAGE_PULL_SECRETS: str

KUBERNETES_MEMORY: None

KUBERNETES_LABELS: str

KUBERNETES_ANNOTATIONS: str

KUBERNETES_NAMESPACE: str

KUBERNETES_NODE_SELECTOR: str

KUBERNETES_PERSISTENT_VOLUME_CLAIMS: str

KUBERNETES_PORT: None

KUBERNETES_SERVICE_ACCOUNT: None

KUBERNETES_SHARED_MEMORY: None

KUBERNETES_TOLERATIONS: str

KUBERNETES_QOS: str

KUBERNETES_CONDA_ARCH: None

UBF_CONTROL: str

MAX_MEMORY_PER_TASK: None

MAX_CPU_PER_TASK: None

SUPPORTED_KUBERNETES_QOS_CLASSES: list

class KubernetesDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    """
    Specifies that this step should execute on Kubernetes.
    
    Parameters
    ----------
    cpu : int, default 1
        Number of CPUs required for this step. If `@resources` is
        also present, the maximum value from all decorators is used.
    memory : int, default 4096
        Memory size (in MB) required for this step. If
        `@resources` is also present, the maximum value from all decorators is
        used.
    disk : int, default 10240
        Disk size (in MB) required for this step. If
        `@resources` is also present, the maximum value from all decorators is
        used.
    image : str, optional, default None
        Docker image to use when launching on Kubernetes. If not specified, and
        METAFLOW_KUBERNETES_CONTAINER_IMAGE is specified, that image is used. If
        not, a default Docker image mapping to the current version of Python is used.
    image_pull_policy: str, default KUBERNETES_IMAGE_PULL_POLICY
        If given, the imagePullPolicy to be applied to the Docker image of the step.
    image_pull_secrets: List[str], default []
        The default is extracted from METAFLOW_KUBERNETES_IMAGE_PULL_SECRETS.
        Kubernetes image pull secrets to use when pulling container images
        in Kubernetes.
    service_account : str, default METAFLOW_KUBERNETES_SERVICE_ACCOUNT
        Kubernetes service account to use when launching pod in Kubernetes.
    secrets : List[str], optional, default None
        Kubernetes secrets to use when launching pod in Kubernetes. These
        secrets are in addition to the ones defined in `METAFLOW_KUBERNETES_SECRETS`
        in Metaflow configuration.
    node_selector: Union[Dict[str,str], str], optional, default None
        Kubernetes node selector(s) to apply to the pod running the task.
        Can be passed in as a comma separated string of values e.g.
        'kubernetes.io/os=linux,kubernetes.io/arch=amd64' or as a dictionary
        {'kubernetes.io/os': 'linux', 'kubernetes.io/arch': 'amd64'}
    namespace : str, default METAFLOW_KUBERNETES_NAMESPACE
        Kubernetes namespace to use when launching pod in Kubernetes.
    gpu : int, optional, default None
        Number of GPUs required for this step. A value of zero implies that
        the scheduled node should not have GPUs.
    gpu_vendor : str, default KUBERNETES_GPU_VENDOR
        The vendor of the GPUs to be used for this step.
    tolerations : List[str], default []
        The default is extracted from METAFLOW_KUBERNETES_TOLERATIONS.
        Kubernetes tolerations to use when launching pod in Kubernetes.
    labels: Dict[str, str], default: METAFLOW_KUBERNETES_LABELS
        Kubernetes labels to use when launching pod in Kubernetes.
    annotations: Dict[str, str], default: METAFLOW_KUBERNETES_ANNOTATIONS
        Kubernetes annotations to use when launching pod in Kubernetes.
    use_tmpfs : bool, default False
        This enables an explicit tmpfs mount for this step.
    tmpfs_tempdir : bool, default True
        sets METAFLOW_TEMPDIR to tmpfs_path if set for this step.
    tmpfs_size : int, optional, default: None
        The value for the size (in MiB) of the tmpfs mount for this step.
        This parameter maps to the `--tmpfs` option in Docker. Defaults to 50% of the
        memory allocated for this step.
    tmpfs_path : str, optional, default /metaflow_temp
        Path to tmpfs mount for this step.
    persistent_volume_claims : Dict[str, str], optional, default None
        A map (dictionary) of persistent volumes to be mounted to the pod for this step. The map is from persistent
        volumes to the path to which the volume is to be mounted, e.g., `{'pvc-name': '/path/to/mount/on'}`.
    shared_memory: int, optional
        Shared memory size (in MiB) required for this step
    port: int, optional
        Port number to specify in the Kubernetes job object
    compute_pool : str, optional, default None
        Compute pool to be used for for this step.
        If not specified, any accessible compute pool within the perimeter is used.
    hostname_resolution_timeout: int, default 10 * 60
        Timeout in seconds for the workers tasks in the gang scheduled cluster to resolve the hostname of control task.
        Only applicable when @parallel is used.
    qos: str, default: Burstable
        Quality of Service class to assign to the pod. Supported values are: Guaranteed, Burstable, BestEffort
    
    security_context: Dict[str, Any], optional, default None
        Container security context. Applies to the task container. Allows the following keys:
        - privileged: bool, optional, default None
        - allow_privilege_escalation: bool, optional, default None
        - run_as_user: int, optional, default None
        - run_as_group: int, optional, default None
        - run_as_non_root: bool, optional, default None
    """
    def init(self):
        ...
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        ...
    def package_init(self, flow, step_name, environment):
        ...
    def runtime_init(self, flow, graph, package, run_id):
        ...
    def runtime_task_created(self, task_datastore, task_id, split_index, input_paths, is_cloned, ubf_context):
        ...
    def runtime_step_cli(self, cli_args, retry_count, max_user_code_retries, ubf_context):
        ...
    def task_pre_step(self, step_name, task_datastore, metadata, run_id, task_id, flow, graph, retry_count, max_retries, ubf_context, inputs):
        ...
    def task_finished(self, step_name, flow, graph, is_task_ok, retry_count, max_retries):
        ...
    ...

