######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.39                                                                                #
# Generated on 2026-09-02T21:19:46.823834                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import datetime
    import typing
FlowSpecDerived = typing.TypeVar("FlowSpecDerived", bound="FlowSpec", contravariant=False, covariant=False)
StepFlag = typing.NewType("StepFlag", bool)

from . import meta_files as meta_files
from . import packaging_sys as packaging_sys
from . import exception as exception
from . import metaflow_config as metaflow_config
from . import multicore_utils as multicore_utils
from .multicore_utils import parallel_imap_unordered as parallel_imap_unordered
from .multicore_utils import parallel_map as parallel_map
from . import metaflow_current as metaflow_current
from .metaflow_current import current as current
from . import parameters as parameters
from . import user_configs as user_configs
from . import user_decorators as user_decorators
from . import tagging_util as tagging_util
from . import metadata_provider as metadata_provider
from . import flowspec as flowspec
from .flowspec import FlowSpec as FlowSpec
from .parameters import Parameter as Parameter
from .parameters import JSONTypeClass as JSONTypeClass
from .parameters import JSONType as JSONType
from .user_configs.config_parameters import Config as Config
from .user_configs.config_parameters import ConfigValue as ConfigValue
from .user_configs.config_parameters import config_expr as config_expr
from .user_decorators.user_step_decorator import UserStepDecorator as UserStepDecorator
from .user_decorators.user_step_decorator import StepMutator as StepMutator
from .user_decorators.user_step_decorator import user_step_decorator as user_step_decorator
from .user_decorators.user_flow_decorator import FlowMutator as FlowMutator
from . import metaflow_git as metaflow_git
from . import system_context as system_context
from . import tuple_util as tuple_util
from . import events as events
from . import runner as runner
from . import plugins as plugins
from .plugins.datatools.s3.s3 import S3 as S3
from . import includefile as includefile
from .includefile import IncludeFile as IncludeFile
from .plugins.package_sources import package_sources as package_sources
from .plugins.pypi.parsers import pyproject_toml_parser as pyproject_toml_parser
from .plugins.pypi.parsers import conda_environment_yml_parser as conda_environment_yml_parser
from .plugins.parsers import yaml_parser as yaml_parser
from .plugins.pypi.parsers import requirements_txt_parser as requirements_txt_parser
from .plugins.namespaced_events import namespaced_event_name as namespaced_event_name
from . import cards as cards
from . import client as client
from .client.core import namespace as namespace
from .client.core import get_namespace as get_namespace
from .client.core import default_namespace as default_namespace
from .client.core import metadata as metadata
from .client.core import get_metadata as get_metadata
from .client.core import default_metadata as default_metadata
from .client.core import inspect_spin as inspect_spin
from .client.core import Metaflow as Metaflow
from .client.core import Flow as Flow
from .client.core import Run as Run
from .client.core import Step as Step
from .client.core import Task as Task
from .client.core import DataArtifact as DataArtifact
from .runner.metaflow_runner import Runner as Runner
from .runner.nbrun import NBRunner as NBRunner
from .runner.deployer import Deployer as Deployer
from .runner.deployer import DeployedFlow as DeployedFlow
from .runner.nbdeploy import NBDeployer as NBDeployer
from . import version as version
from . import cli_components as cli_components
from . import system as system
from . import pylint_wrapper as pylint_wrapper
from . import cli as cli

EXT_PKG: str

USER_SKIP_STEP: dict

@typing.overload
def step(f: typing.Callable[[FlowSpecDerived], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    """
    Marks a method in a FlowSpec as a Metaflow Step. Note that this
    decorator needs to be placed as close to the method as possible (ie:
    before other decorators).
    
    In other words, this is valid:
    ```
    @batch
    @step
    def foo(self):
        pass
    ```
    
    whereas this is not:
    ```
    @step
    @batch
    def foo(self):
        pass
    ```
    
    Parameters
    ----------
    f : callable, optional
        Function to make into a Metaflow Step. When using keyword arguments
        (e.g. ``@step(start=True)``), this is ``None`` and a decorator
        function is returned instead.
    start : bool, default False
        Mark this step as the start (entry) step of the flow.
    end : bool, default False
        Mark this step as the end (terminal) step of the flow.
    node_info : dict, optional
        Extra metadata to attach to this step's DAGNode. Extensions can use
        this to store arbitrary information accessible via ``flow._graph``
        (live references) and ``_graph_info`` (serialized via ``to_pod``).
    
    Returns
    -------
    callable
        The decorated function, or a decorator if keyword arguments were used.
    """
    ...

@typing.overload
def step(f: typing.Callable[[FlowSpecDerived, typing.Any], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def step(f = None, *, start = False, end = False, node_info = None):
    """
    Marks a method in a FlowSpec as a Metaflow Step. Note that this
    decorator needs to be placed as close to the method as possible (ie:
    before other decorators).
    
    In other words, this is valid:
    ```
    @batch
    @step
    def foo(self):
        pass
    ```
    
    whereas this is not:
    ```
    @step
    @batch
    def foo(self):
        pass
    ```
    
    Parameters
    ----------
    f : callable, optional
        Function to make into a Metaflow Step. When using keyword arguments
        (e.g. ``@step(start=True)``), this is ``None`` and a decorator
        function is returned instead.
    start : bool, default False
        Mark this step as the start (entry) step of the flow.
    end : bool, default False
        Mark this step as the end (terminal) step of the flow.
    node_info : dict, optional
        Extra metadata to attach to this step's DAGNode. Extensions can use
        this to store arbitrary information accessible via ``flow._graph``
        (live references) and ``_graph_info`` (serialized via ``to_pod``).
    
    Returns
    -------
    callable
        The decorated function, or a decorator if keyword arguments were used.
    """
    ...

@typing.overload
def conda(*, packages: typing.Dict[str, str] = {}, libraries: typing.Dict[str, str] = {}, python: typing.Union[str, None] = None, disabled: bool = False) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies the Conda environment for the step.
    
    Information in this decorator will augment any
    attributes set in the `@conda_base` flow-level decorator. Hence,
    you can use `@conda_base` to set packages required by all
    steps and use `@conda` to specify step-specific overrides.
    
    
    Parameters
    ----------
    packages : Dict[str, str], default {}
        Packages to use for this step. The key is the name of the package
        and the value is the version to use.
    libraries : Dict[str, str], default {}
        Supported for backward compatibility. When used with packages, packages will take precedence.
    python : str, optional, default None
        Version of Python to use, e.g. '3.7.4'. A default value of None implies
        that the version used will correspond to the version of the Python interpreter used to start the run.
    disabled : bool, default False
        If set to True, disables @conda.
    """
    ...

@typing.overload
def conda(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def conda(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def conda(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, packages: typing.Dict[str, str] = {}, libraries: typing.Dict[str, str] = {}, python: typing.Union[str, None] = None, disabled: bool = False):
    """
    Specifies the Conda environment for the step.
    
    Information in this decorator will augment any
    attributes set in the `@conda_base` flow-level decorator. Hence,
    you can use `@conda_base` to set packages required by all
    steps and use `@conda` to specify step-specific overrides.
    
    
    Parameters
    ----------
    packages : Dict[str, str], default {}
        Packages to use for this step. The key is the name of the package
        and the value is the version to use.
    libraries : Dict[str, str], default {}
        Supported for backward compatibility. When used with packages, packages will take precedence.
    python : str, optional, default None
        Version of Python to use, e.g. '3.7.4'. A default value of None implies
        that the version used will correspond to the version of the Python interpreter used to start the run.
    disabled : bool, default False
        If set to True, disables @conda.
    """
    ...

@typing.overload
def parallel(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    """
    Decorator prototype for all step decorators. This function gets specialized
    and imported for all decorators types by _import_plugin_decorators().
    """
    ...

@typing.overload
def parallel(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def parallel(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None):
    """
    Decorator prototype for all step decorators. This function gets specialized
    and imported for all decorators types by _import_plugin_decorators().
    """
    ...

@typing.overload
def retry(*, times: int = 3, minutes_between_retries: int = 2) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies the number of times the task corresponding
    to a step needs to be retried.
    
    This decorator is useful for handling transient errors, such as networking issues.
    If your task contains operations that can't be retried safely, e.g. database updates,
    it is advisable to annotate it with `@retry(times=0)`.
    
    This can be used in conjunction with the `@catch` decorator. The `@catch`
    decorator will execute a no-op task after all retries have been exhausted,
    ensuring that the flow execution can continue.
    
    
    Parameters
    ----------
    times : int, default 3
        Number of times to retry this task.
    minutes_between_retries : int, default 2
        Number of minutes between retries.
    """
    ...

@typing.overload
def retry(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def retry(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def retry(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, times: int = 3, minutes_between_retries: int = 2):
    """
    Specifies the number of times the task corresponding
    to a step needs to be retried.
    
    This decorator is useful for handling transient errors, such as networking issues.
    If your task contains operations that can't be retried safely, e.g. database updates,
    it is advisable to annotate it with `@retry(times=0)`.
    
    This can be used in conjunction with the `@catch` decorator. The `@catch`
    decorator will execute a no-op task after all retries have been exhausted,
    ensuring that the flow execution can continue.
    
    
    Parameters
    ----------
    times : int, default 3
        Number of times to retry this task.
    minutes_between_retries : int, default 2
        Number of minutes between retries.
    """
    ...

def kubernetes(*, cpu: int = 1, memory: int = 4096, disk: int = 10240, image: typing.Union[str, None] = None, image_pull_policy: str = 'KUBERNETES_IMAGE_PULL_POLICY', image_pull_secrets: typing.List[str] = [], service_account: str = 'METAFLOW_KUBERNETES_SERVICE_ACCOUNT', secrets: typing.Union[typing.List[str], None] = None, node_selector: typing.Union[typing.Dict[str, str], str, None] = None, namespace: str = 'METAFLOW_KUBERNETES_NAMESPACE', gpu: typing.Union[int, None] = None, gpu_vendor: str = 'KUBERNETES_GPU_VENDOR', tolerations: typing.List[typing.Dict[str, str]] = [], labels: typing.Dict[str, str] = 'METAFLOW_KUBERNETES_LABELS', annotations: typing.Dict[str, str] = 'METAFLOW_KUBERNETES_ANNOTATIONS', use_tmpfs: bool = False, tmpfs_tempdir: bool = True, tmpfs_size: typing.Union[int, None] = None, tmpfs_path: typing.Union[str, None] = '/metaflow_temp', persistent_volume_claims: typing.Union[typing.Dict[str, str], None] = None, shared_memory: typing.Union[int, None] = None, port: typing.Union[int, None] = None, compute_pool: typing.Union[str, None] = None, hostname_resolution_timeout: int = 600, qos: str = 'Burstable', extended_resources: typing.Union[typing.Dict[str, str], None] = {}, security_context: typing.Union[typing.Dict[str, typing.Any], None] = None) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
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
    tolerations : List[Dict[str,str]], default []
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
    extended_resources: Dict[str, str], optional, default {}
        Extended resources to be requested for the pod.
        https://kubernetes.io/docs/tasks/administer-cluster/extended-resource-node/
    
    security_context: Dict[str, Any], optional, default None
        Container security context. Applies to the task container. Allows the following keys:
        - privileged: bool, optional, default None
        - allow_privilege_escalation: bool, optional, default None
        - run_as_user: int, optional, default None
        - run_as_group: int, optional, default None
        - run_as_non_root: bool, optional, default None
    """
    ...

@typing.overload
def batch(*, cpu: int = 1, gpu: int = 0, memory: int = 4096, image: typing.Union[str, None] = None, queue: str = 'METAFLOW_BATCH_JOB_QUEUE', iam_role: str = 'METAFLOW_ECS_S3_ACCESS_IAM_ROLE', execution_role: str = 'METAFLOW_ECS_FARGATE_EXECUTION_ROLE', shared_memory: typing.Union[int, None] = None, max_swap: typing.Union[int, None] = None, swappiness: typing.Union[int, None] = None, aws_batch_tags: typing.Union[typing.Dict[str, str], None] = None, use_tmpfs: bool = False, tmpfs_tempdir: bool = True, tmpfs_size: typing.Union[int, None] = None, tmpfs_path: typing.Union[str, None] = None, inferentia: int = 0, trainium: int = None, efa: int = 0, ephemeral_storage: int = None, log_driver: typing.Union[str, None] = None, log_options: typing.Union[typing.List[str], None] = None, privileged: bool = False) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies that this step should execute on [AWS Batch](https://aws.amazon.com/batch/).
    
    
    Parameters
    ----------
    cpu : int, default 1
        Number of CPUs required for this step. If `@resources` is
        also present, the maximum value from all decorators is used.
    gpu : int, default 0
        Number of GPUs required for this step. If `@resources` is
        also present, the maximum value from all decorators is used.
    memory : int, default 4096
        Memory size (in MB) required for this step. If
        `@resources` is also present, the maximum value from all decorators is
        used.
    image : str, optional, default None
        Docker image to use when launching on AWS Batch. If not specified, and
        METAFLOW_BATCH_CONTAINER_IMAGE is specified, that image is used. If
        not, a default Docker image mapping to the current version of Python is used.
    queue : str, default METAFLOW_BATCH_JOB_QUEUE
        AWS Batch Job Queue to submit the job to.
    iam_role : str, default METAFLOW_ECS_S3_ACCESS_IAM_ROLE
        AWS IAM role that AWS Batch container uses to access AWS cloud resources.
    execution_role : str, default METAFLOW_ECS_FARGATE_EXECUTION_ROLE
        AWS IAM role that AWS Batch can use [to trigger AWS Fargate tasks]
        (https://docs.aws.amazon.com/batch/latest/userguide/execution-IAM-role.html).
    shared_memory : int, optional, default None
        The value for the size (in MiB) of the /dev/shm volume for this step.
        This parameter maps to the `--shm-size` option in Docker.
    max_swap : int, optional, default None
        The total amount of swap memory (in MiB) a container can use for this
        step. This parameter is translated to the `--memory-swap` option in
        Docker where the value is the sum of the container memory plus the
        `max_swap` value.
    swappiness : int, optional, default None
        This allows you to tune memory swappiness behavior for this step.
        A swappiness value of 0 causes swapping not to happen unless absolutely
        necessary. A swappiness value of 100 causes pages to be swapped very
        aggressively. Accepted values are whole numbers between 0 and 100.
    aws_batch_tags: Dict[str, str], optional, default None
        Sets arbitrary AWS tags on the AWS Batch compute environment.
        Set as string key-value pairs.
    use_tmpfs : bool, default False
        This enables an explicit tmpfs mount for this step. Note that tmpfs is
        not available on Fargate compute environments
    tmpfs_tempdir : bool, default True
        sets METAFLOW_TEMPDIR to tmpfs_path if set for this step.
    tmpfs_size : int, optional, default None
        The value for the size (in MiB) of the tmpfs mount for this step.
        This parameter maps to the `--tmpfs` option in Docker. Defaults to 50% of the
        memory allocated for this step.
    tmpfs_path : str, optional, default None
        Path to tmpfs mount for this step. Defaults to /metaflow_temp.
    inferentia : int, default 0
        Number of Inferentia chips required for this step.
    trainium : int, default None
        Alias for inferentia. Use only one of the two.
    efa : int, default 0
        Number of elastic fabric adapter network devices to attach to container
    ephemeral_storage : int, default None
        The total amount, in GiB, of ephemeral storage to set for the task, 21-200GiB.
        This is only relevant for Fargate compute environments
    log_driver: str, optional, default None
        The log driver to use for the Amazon ECS container.
    log_options: List[str], optional, default None
        List of strings containing options for the chosen log driver. The configurable values
        depend on the `log driver` chosen. Validation of these options is not supported yet.
        Example: [`awslogs-group:aws/batch/job`]
    privileged: bool, default False
        Control whether the task can run as a privileged process on AWS Batch
    """
    ...

@typing.overload
def batch(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def batch(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def batch(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, cpu: int = 1, gpu: int = 0, memory: int = 4096, image: typing.Union[str, None] = None, queue: str = 'METAFLOW_BATCH_JOB_QUEUE', iam_role: str = 'METAFLOW_ECS_S3_ACCESS_IAM_ROLE', execution_role: str = 'METAFLOW_ECS_FARGATE_EXECUTION_ROLE', shared_memory: typing.Union[int, None] = None, max_swap: typing.Union[int, None] = None, swappiness: typing.Union[int, None] = None, aws_batch_tags: typing.Union[typing.Dict[str, str], None] = None, use_tmpfs: bool = False, tmpfs_tempdir: bool = True, tmpfs_size: typing.Union[int, None] = None, tmpfs_path: typing.Union[str, None] = None, inferentia: int = 0, trainium: int = None, efa: int = 0, ephemeral_storage: int = None, log_driver: typing.Union[str, None] = None, log_options: typing.Union[typing.List[str], None] = None, privileged: bool = False):
    """
    Specifies that this step should execute on [AWS Batch](https://aws.amazon.com/batch/).
    
    
    Parameters
    ----------
    cpu : int, default 1
        Number of CPUs required for this step. If `@resources` is
        also present, the maximum value from all decorators is used.
    gpu : int, default 0
        Number of GPUs required for this step. If `@resources` is
        also present, the maximum value from all decorators is used.
    memory : int, default 4096
        Memory size (in MB) required for this step. If
        `@resources` is also present, the maximum value from all decorators is
        used.
    image : str, optional, default None
        Docker image to use when launching on AWS Batch. If not specified, and
        METAFLOW_BATCH_CONTAINER_IMAGE is specified, that image is used. If
        not, a default Docker image mapping to the current version of Python is used.
    queue : str, default METAFLOW_BATCH_JOB_QUEUE
        AWS Batch Job Queue to submit the job to.
    iam_role : str, default METAFLOW_ECS_S3_ACCESS_IAM_ROLE
        AWS IAM role that AWS Batch container uses to access AWS cloud resources.
    execution_role : str, default METAFLOW_ECS_FARGATE_EXECUTION_ROLE
        AWS IAM role that AWS Batch can use [to trigger AWS Fargate tasks]
        (https://docs.aws.amazon.com/batch/latest/userguide/execution-IAM-role.html).
    shared_memory : int, optional, default None
        The value for the size (in MiB) of the /dev/shm volume for this step.
        This parameter maps to the `--shm-size` option in Docker.
    max_swap : int, optional, default None
        The total amount of swap memory (in MiB) a container can use for this
        step. This parameter is translated to the `--memory-swap` option in
        Docker where the value is the sum of the container memory plus the
        `max_swap` value.
    swappiness : int, optional, default None
        This allows you to tune memory swappiness behavior for this step.
        A swappiness value of 0 causes swapping not to happen unless absolutely
        necessary. A swappiness value of 100 causes pages to be swapped very
        aggressively. Accepted values are whole numbers between 0 and 100.
    aws_batch_tags: Dict[str, str], optional, default None
        Sets arbitrary AWS tags on the AWS Batch compute environment.
        Set as string key-value pairs.
    use_tmpfs : bool, default False
        This enables an explicit tmpfs mount for this step. Note that tmpfs is
        not available on Fargate compute environments
    tmpfs_tempdir : bool, default True
        sets METAFLOW_TEMPDIR to tmpfs_path if set for this step.
    tmpfs_size : int, optional, default None
        The value for the size (in MiB) of the tmpfs mount for this step.
        This parameter maps to the `--tmpfs` option in Docker. Defaults to 50% of the
        memory allocated for this step.
    tmpfs_path : str, optional, default None
        Path to tmpfs mount for this step. Defaults to /metaflow_temp.
    inferentia : int, default 0
        Number of Inferentia chips required for this step.
    trainium : int, default None
        Alias for inferentia. Use only one of the two.
    efa : int, default 0
        Number of elastic fabric adapter network devices to attach to container
    ephemeral_storage : int, default None
        The total amount, in GiB, of ephemeral storage to set for the task, 21-200GiB.
        This is only relevant for Fargate compute environments
    log_driver: str, optional, default None
        The log driver to use for the Amazon ECS container.
    log_options: List[str], optional, default None
        List of strings containing options for the chosen log driver. The configurable values
        depend on the `log driver` chosen. Validation of these options is not supported yet.
        Example: [`awslogs-group:aws/batch/job`]
    privileged: bool, default False
        Control whether the task can run as a privileged process on AWS Batch
    """
    ...

@typing.overload
def secrets(*, sources: typing.List[typing.Union[str, typing.Dict[str, typing.Any]]] = [], role: typing.Union[str, None] = None, allow_override: typing.Union[bool, None] = False) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies secrets to be retrieved and injected as environment variables prior to
    the execution of a step.
    
    
    Parameters
    ----------
    sources : List[Union[str, Dict[str, Any]]], default: []
        List of secret specs, defining how the secrets are to be retrieved
    role : str, optional, default: None
        Role to use for fetching secrets
    allow_override : bool, optional, default: False
        Toggle whether secrets can replace existing environment variables.
    """
    ...

@typing.overload
def secrets(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def secrets(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def secrets(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, sources: typing.List[typing.Union[str, typing.Dict[str, typing.Any]]] = [], role: typing.Union[str, None] = None, allow_override: typing.Union[bool, None] = False):
    """
    Specifies secrets to be retrieved and injected as environment variables prior to
    the execution of a step.
    
    
    Parameters
    ----------
    sources : List[Union[str, Dict[str, Any]]], default: []
        List of secret specs, defining how the secrets are to be retrieved
    role : str, optional, default: None
        Role to use for fetching secrets
    allow_override : bool, optional, default: False
        Toggle whether secrets can replace existing environment variables.
    """
    ...

@typing.overload
def catch(*, var: typing.Union[str, None] = None, print_exception: bool = True) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies that the step will success under all circumstances.
    
    The decorator will create an optional artifact, specified by `var`, which
    contains the exception raised. You can use it to detect the presence
    of errors, indicating that all happy-path artifacts produced by the step
    are missing.
    
    
    Parameters
    ----------
    var : str, optional, default None
        Name of the artifact in which to store the caught exception.
        If not specified, the exception is not stored.
    print_exception : bool, default True
        Determines whether or not the exception is printed to
        stdout when caught.
    """
    ...

@typing.overload
def catch(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def catch(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def catch(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, var: typing.Union[str, None] = None, print_exception: bool = True):
    """
    Specifies that the step will success under all circumstances.
    
    The decorator will create an optional artifact, specified by `var`, which
    contains the exception raised. You can use it to detect the presence
    of errors, indicating that all happy-path artifacts produced by the step
    are missing.
    
    
    Parameters
    ----------
    var : str, optional, default None
        Name of the artifact in which to store the caught exception.
        If not specified, the exception is not stored.
    print_exception : bool, default True
        Determines whether or not the exception is printed to
        stdout when caught.
    """
    ...

@typing.overload
def timeout(*, seconds: int = 0, minutes: int = 0, hours: int = 0) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies a timeout for your step.
    
    This decorator is useful if this step may hang indefinitely.
    
    This can be used in conjunction with the `@retry` decorator as well as the `@catch` decorator.
    A timeout is considered to be an exception thrown by the step. It will cause the step to be
    retried if needed and the exception will be caught by the `@catch` decorator, if present.
    
    Note that all the values specified in parameters are added together so if you specify
    60 seconds and 1 hour, the decorator will have an effective timeout of 1 hour and 1 minute.
    
    
    Parameters
    ----------
    seconds : int, default 0
        Number of seconds to wait prior to timing out.
    minutes : int, default 0
        Number of minutes to wait prior to timing out.
    hours : int, default 0
        Number of hours to wait prior to timing out.
    """
    ...

@typing.overload
def timeout(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def timeout(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def timeout(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, seconds: int = 0, minutes: int = 0, hours: int = 0):
    """
    Specifies a timeout for your step.
    
    This decorator is useful if this step may hang indefinitely.
    
    This can be used in conjunction with the `@retry` decorator as well as the `@catch` decorator.
    A timeout is considered to be an exception thrown by the step. It will cause the step to be
    retried if needed and the exception will be caught by the `@catch` decorator, if present.
    
    Note that all the values specified in parameters are added together so if you specify
    60 seconds and 1 hour, the decorator will have an effective timeout of 1 hour and 1 minute.
    
    
    Parameters
    ----------
    seconds : int, default 0
        Number of seconds to wait prior to timing out.
    minutes : int, default 0
        Number of minutes to wait prior to timing out.
    hours : int, default 0
        Number of hours to wait prior to timing out.
    """
    ...

@typing.overload
def resources(*, cpu: int = 1, gpu: typing.Union[int, None] = None, disk: typing.Union[int, None] = None, memory: int = 4096, shared_memory: typing.Union[int, None] = None) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies the resources needed when executing this step.
    
    Use `@resources` to specify the resource requirements
    independently of the specific compute layer (`@batch`, `@kubernetes`).
    
    You can choose the compute layer on the command line by executing e.g.
    ```
    python myflow.py run --with batch
    ```
    or
    ```
    python myflow.py run --with kubernetes
    ```
    which executes the flow on the desired system using the
    requirements specified in `@resources`.
    
    
    Parameters
    ----------
    cpu : int, default 1
        Number of CPUs required for this step.
    gpu : int, optional, default None
        Number of GPUs required for this step.
    disk : int, optional, default None
        Disk size (in MB) required for this step. Only applies on Kubernetes.
    memory : int, default 4096
        Memory size (in MB) required for this step.
    shared_memory : int, optional, default None
        The value for the size (in MiB) of the /dev/shm volume for this step.
        This parameter maps to the `--shm-size` option in Docker.
    """
    ...

@typing.overload
def resources(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def resources(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def resources(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, cpu: int = 1, gpu: typing.Union[int, None] = None, disk: typing.Union[int, None] = None, memory: int = 4096, shared_memory: typing.Union[int, None] = None):
    """
    Specifies the resources needed when executing this step.
    
    Use `@resources` to specify the resource requirements
    independently of the specific compute layer (`@batch`, `@kubernetes`).
    
    You can choose the compute layer on the command line by executing e.g.
    ```
    python myflow.py run --with batch
    ```
    or
    ```
    python myflow.py run --with kubernetes
    ```
    which executes the flow on the desired system using the
    requirements specified in `@resources`.
    
    
    Parameters
    ----------
    cpu : int, default 1
        Number of CPUs required for this step.
    gpu : int, optional, default None
        Number of GPUs required for this step.
    disk : int, optional, default None
        Disk size (in MB) required for this step. Only applies on Kubernetes.
    memory : int, default 4096
        Memory size (in MB) required for this step.
    shared_memory : int, optional, default None
        The value for the size (in MiB) of the /dev/shm volume for this step.
        This parameter maps to the `--shm-size` option in Docker.
    """
    ...

@typing.overload
def environment(*, vars: typing.Dict[str, str] = {}) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies environment variables to be set prior to the execution of a step.
    
    
    Parameters
    ----------
    vars : Dict[str, str], default {}
        Dictionary of environment variables to set.
    """
    ...

@typing.overload
def environment(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def environment(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def environment(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, vars: typing.Dict[str, str] = {}):
    """
    Specifies environment variables to be set prior to the execution of a step.
    
    
    Parameters
    ----------
    vars : Dict[str, str], default {}
        Dictionary of environment variables to set.
    """
    ...

@typing.overload
def card(*, type: str = 'default', id: typing.Union[str, None] = None, options: typing.Dict[str, typing.Any] = {}, timeout: int = 45) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Creates a human-readable report, a Metaflow Card, after this step completes.
    
    Note that you may add multiple `@card` decorators in a step with different parameters.
    
    
    Parameters
    ----------
    type : str, default 'default'
        Card type.
    id : str, optional, default None
        If multiple cards are present, use this id to identify this card.
    options : Dict[str, Any], default {}
        Options passed to the card. The contents depend on the card type.
    timeout : int, default 45
        Interrupt reporting if it takes more than this many seconds.
    """
    ...

@typing.overload
def card(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def card(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def card(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, type: str = 'default', id: typing.Union[str, None] = None, options: typing.Dict[str, typing.Any] = {}, timeout: int = 45):
    """
    Creates a human-readable report, a Metaflow Card, after this step completes.
    
    Note that you may add multiple `@card` decorators in a step with different parameters.
    
    
    Parameters
    ----------
    type : str, default 'default'
        Card type.
    id : str, optional, default None
        If multiple cards are present, use this id to identify this card.
    options : Dict[str, Any], default {}
        Options passed to the card. The contents depend on the card type.
    timeout : int, default 45
        Interrupt reporting if it takes more than this many seconds.
    """
    ...

@typing.overload
def pypi(*, packages: typing.Dict[str, str] = {}, python: typing.Union[str, None] = None) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies the PyPI packages for the step.
    
    Information in this decorator will augment any
    attributes set in the `@pyi_base` flow-level decorator. Hence,
    you can use `@pypi_base` to set packages required by all
    steps and use `@pypi` to specify step-specific overrides.
    
    
    Parameters
    ----------
    packages : Dict[str, str], default: {}
        Packages to use for this step. The key is the name of the package
        and the value is the version to use.
    python : str, optional, default: None
        Version of Python to use, e.g. '3.7.4'. A default value of None implies
        that the version used will correspond to the version of the Python interpreter used to start the run.
    """
    ...

@typing.overload
def pypi(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def pypi(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def pypi(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, packages: typing.Dict[str, str] = {}, python: typing.Union[str, None] = None):
    """
    Specifies the PyPI packages for the step.
    
    Information in this decorator will augment any
    attributes set in the `@pyi_base` flow-level decorator. Hence,
    you can use `@pypi_base` to set packages required by all
    steps and use `@pypi` to specify step-specific overrides.
    
    
    Parameters
    ----------
    packages : Dict[str, str], default: {}
        Packages to use for this step. The key is the name of the package
        and the value is the version to use.
    python : str, optional, default: None
        Version of Python to use, e.g. '3.7.4'. A default value of None implies
        that the version used will correspond to the version of the Python interpreter used to start the run.
    """
    ...

def project(*, name: str, branch: typing.Union[str, None] = None, production: bool = False) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
    """
    Specifies what flows belong to the same project.
    
    A project-specific namespace is created for all flows that
    use the same `@project(name)`.
    
    
    Parameters
    ----------
    name : str
        Project name. Make sure that the name is unique amongst all
        projects that use the same production scheduler. The name may
        contain only lowercase alphanumeric characters and underscores.
    
    branch : Optional[str], default None
        The branch to use. If not specified, the branch is set to
        `user.<username>` unless `production` is set to `True`. This can
        also be set on the command line using `--branch` as a top-level option.
        It is an error to specify `branch` in the decorator and on the command line.
    
    production : bool, default False
        Whether or not the branch is the production branch. This can also be set on the
        command line using `--production` as a top-level option. It is an error to specify
        `production` in the decorator and on the command line.
        The project branch name will be:
          - if `branch` is specified:
            - if `production` is True: `prod.<branch>`
            - if `production` is False: `test.<branch>`
          - if `branch` is not specified:
            - if `production` is True: `prod`
            - if `production` is False: `user.<username>`
    """
    ...

@typing.overload
def conda_base(*, packages: typing.Dict[str, str] = {}, libraries: typing.Dict[str, str] = {}, python: typing.Union[str, None] = None, disabled: bool = False) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
    """
    Specifies the Conda environment for all steps of the flow.
    
    Use `@conda_base` to set common libraries required by all
    steps and use `@conda` to specify step-specific additions.
    
    
    Parameters
    ----------
    packages : Dict[str, str], default {}
        Packages to use for this flow. The key is the name of the package
        and the value is the version to use.
    libraries : Dict[str, str], default {}
        Supported for backward compatibility. When used with packages, packages will take precedence.
    python : str, optional, default None
        Version of Python to use, e.g. '3.7.4'. A default value of None implies
        that the version used will correspond to the version of the Python interpreter used to start the run.
    disabled : bool, default False
        If set to True, disables Conda.
    """
    ...

@typing.overload
def conda_base(f: typing.Type[FlowSpecDerived]) -> typing.Type[FlowSpecDerived]:
    ...

def conda_base(f: typing.Union[typing.Type[FlowSpecDerived], None] = None, *, packages: typing.Dict[str, str] = {}, libraries: typing.Dict[str, str] = {}, python: typing.Union[str, None] = None, disabled: bool = False):
    """
    Specifies the Conda environment for all steps of the flow.
    
    Use `@conda_base` to set common libraries required by all
    steps and use `@conda` to specify step-specific additions.
    
    
    Parameters
    ----------
    packages : Dict[str, str], default {}
        Packages to use for this flow. The key is the name of the package
        and the value is the version to use.
    libraries : Dict[str, str], default {}
        Supported for backward compatibility. When used with packages, packages will take precedence.
    python : str, optional, default None
        Version of Python to use, e.g. '3.7.4'. A default value of None implies
        that the version used will correspond to the version of the Python interpreter used to start the run.
    disabled : bool, default False
        If set to True, disables Conda.
    """
    ...

@typing.overload
def trigger(*, event: typing.Union["Union[str, Dict[str, Any], Callable[[ParameterContext], Union[str, Dict[str, Any]]]]", None] = None, events: "List[Union[str, Dict[str, Any],Callable[[ParameterContext], Union[str, Dict[str, Any]]]]]" = [], options: typing.Dict[str, typing.Any] = {}) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
    """
    Specifies the event(s) that this flow depends on.
    
    ```
    @trigger(event='foo')
    ```
    or
    ```
    @trigger(events=['foo', 'bar'])
    ```
    
    Additionally, you can specify the parameter mappings
    to map event payload to Metaflow parameters for the flow.
    ```
    @trigger(event={'name':'foo', 'parameters':{'flow_param': 'event_field'}})
    ```
    or
    ```
    @trigger(events=[{'name':'foo', 'parameters':{'flow_param_1': 'event_field_1'},
                     {'name':'bar', 'parameters':{'flow_param_2': 'event_field_2'}])
    ```
    
    'parameters' can also be a list of strings and tuples like so:
    ```
    @trigger(event={'name':'foo', 'parameters':['common_name', ('flow_param', 'event_field')]})
    ```
    This is equivalent to:
    ```
    @trigger(event={'name':'foo', 'parameters':{'common_name': 'common_name', 'flow_param': 'event_field'}})
    ```
    
    For namespaced events, you can use `namespaced_event_name` which resolves the
    full event name at deploy time based on @project settings:
    ```
    from metaflow import namespaced_event_name
    
    @trigger(event=namespaced_event_name('foo'))
    
    @trigger(event={'name': namespaced_event_name('foo'), 'parameters': {'x': 'y'}})
    ```
    
    
    Parameters
    ----------
    event : Union[str, Dict[str, Any], Callable[[ParameterContext], Union[str, Dict[str, Any]]]], optional, default None
        Event dependency for this flow. Can be a string, dict, or a callable that
        returns a string or dict at deploy time.
    events : List[Union[str, Dict[str, Any],Callable[[ParameterContext], Union[str, Dict[str, Any]]]]], default []
        Events dependency for this flow. Each element can be a string, dict, or callable.
    options : Dict[str, Any], default {}
        Backend-specific configuration for tuning eventing behavior.
    """
    ...

@typing.overload
def trigger(f: typing.Type[FlowSpecDerived]) -> typing.Type[FlowSpecDerived]:
    ...

def trigger(f: typing.Union[typing.Type[FlowSpecDerived], None] = None, *, event: typing.Union["Union[str, Dict[str, Any], Callable[[ParameterContext], Union[str, Dict[str, Any]]]]", None] = None, events: "List[Union[str, Dict[str, Any],Callable[[ParameterContext], Union[str, Dict[str, Any]]]]]" = [], options: typing.Dict[str, typing.Any] = {}):
    """
    Specifies the event(s) that this flow depends on.
    
    ```
    @trigger(event='foo')
    ```
    or
    ```
    @trigger(events=['foo', 'bar'])
    ```
    
    Additionally, you can specify the parameter mappings
    to map event payload to Metaflow parameters for the flow.
    ```
    @trigger(event={'name':'foo', 'parameters':{'flow_param': 'event_field'}})
    ```
    or
    ```
    @trigger(events=[{'name':'foo', 'parameters':{'flow_param_1': 'event_field_1'},
                     {'name':'bar', 'parameters':{'flow_param_2': 'event_field_2'}])
    ```
    
    'parameters' can also be a list of strings and tuples like so:
    ```
    @trigger(event={'name':'foo', 'parameters':['common_name', ('flow_param', 'event_field')]})
    ```
    This is equivalent to:
    ```
    @trigger(event={'name':'foo', 'parameters':{'common_name': 'common_name', 'flow_param': 'event_field'}})
    ```
    
    For namespaced events, you can use `namespaced_event_name` which resolves the
    full event name at deploy time based on @project settings:
    ```
    from metaflow import namespaced_event_name
    
    @trigger(event=namespaced_event_name('foo'))
    
    @trigger(event={'name': namespaced_event_name('foo'), 'parameters': {'x': 'y'}})
    ```
    
    
    Parameters
    ----------
    event : Union[str, Dict[str, Any], Callable[[ParameterContext], Union[str, Dict[str, Any]]]], optional, default None
        Event dependency for this flow. Can be a string, dict, or a callable that
        returns a string or dict at deploy time.
    events : List[Union[str, Dict[str, Any],Callable[[ParameterContext], Union[str, Dict[str, Any]]]]], default []
        Events dependency for this flow. Each element can be a string, dict, or callable.
    options : Dict[str, Any], default {}
        Backend-specific configuration for tuning eventing behavior.
    """
    ...

def airflow_s3_key_sensor(*, timeout: int, poke_interval: int, mode: str, exponential_backoff: bool, pool: str, soft_fail: bool, name: str, description: str, bucket_key: typing.Union[str, typing.List[str]], bucket_name: str, wildcard_match: bool, aws_conn_id: str, verify: bool) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
    """
    The `@airflow_s3_key_sensor` decorator attaches a Airflow [S3KeySensor](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/sensors/s3/index.html#airflow.providers.amazon.aws.sensors.s3.S3KeySensor)
    before the start step of the flow. This decorator only works when a flow is scheduled on Airflow
    and is compiled using `airflow create`. More than one `@airflow_s3_key_sensor` can be
    added as a flow decorators. Adding more than one decorator will ensure that `start` step
    starts only after all sensors finish.
    
    
    Parameters
    ----------
    timeout : int
        Time, in seconds before the task times out and fails. (Default: 3600)
    poke_interval : int
        Time in seconds that the job should wait in between each try. (Default: 60)
    mode : str
        How the sensor operates. Options are: { poke | reschedule }. (Default: "poke")
    exponential_backoff : bool
        allow progressive longer waits between pokes by using exponential backoff algorithm. (Default: True)
    pool : str
        the slot pool this task should run in,
        slot pools are a way to limit concurrency for certain tasks. (Default:None)
    soft_fail : bool
        Set to true to mark the task as SKIPPED on failure. (Default: False)
    name : str
        Name of the sensor on Airflow
    description : str
        Description of sensor in the Airflow UI
    bucket_key : Union[str, List[str]]
        The key(s) being waited on. Supports full s3:// style url or relative path from root level.
        When it's specified as a full s3:// url, please leave `bucket_name` as None
    bucket_name : str
        Name of the S3 bucket. Only needed when bucket_key is not provided as a full s3:// url.
        When specified, all the keys passed to bucket_key refers to this bucket. (Default:None)
    wildcard_match : bool
        whether the bucket_key should be interpreted as a Unix wildcard pattern. (Default: False)
    aws_conn_id : str
        a reference to the s3 connection on Airflow. (Default: None)
    verify : bool
        Whether or not to verify SSL certificates for S3 connection. (Default: None)
    """
    ...

@typing.overload
def schedule(*, hourly: bool = False, daily: bool = True, weekly: bool = False, cron: typing.Union[str, None] = None, timezone: typing.Union[str, None] = None) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
    """
    Specifies the times when the flow should be run when running on a
    production scheduler.
    
    
    Parameters
    ----------
    hourly : bool, default False
        Run the workflow hourly.
    daily : bool, default True
        Run the workflow daily.
    weekly : bool, default False
        Run the workflow weekly.
    cron : str, optional, default None
        Run the workflow at [a custom Cron schedule](https://docs.aws.amazon.com/eventbridge/latest/userguide/scheduled-events.html#cron-expressions)
        specified by this expression.
    timezone : str, optional, default None
        Timezone on which the schedule runs (default: None). Currently supported only for Argo workflows,
        which accepts timezones in [IANA format](https://nodatime.org/TimeZones).
    """
    ...

@typing.overload
def schedule(f: typing.Type[FlowSpecDerived]) -> typing.Type[FlowSpecDerived]:
    ...

def schedule(f: typing.Union[typing.Type[FlowSpecDerived], None] = None, *, hourly: bool = False, daily: bool = True, weekly: bool = False, cron: typing.Union[str, None] = None, timezone: typing.Union[str, None] = None):
    """
    Specifies the times when the flow should be run when running on a
    production scheduler.
    
    
    Parameters
    ----------
    hourly : bool, default False
        Run the workflow hourly.
    daily : bool, default True
        Run the workflow daily.
    weekly : bool, default False
        Run the workflow weekly.
    cron : str, optional, default None
        Run the workflow at [a custom Cron schedule](https://docs.aws.amazon.com/eventbridge/latest/userguide/scheduled-events.html#cron-expressions)
        specified by this expression.
    timezone : str, optional, default None
        Timezone on which the schedule runs (default: None). Currently supported only for Argo workflows,
        which accepts timezones in [IANA format](https://nodatime.org/TimeZones).
    """
    ...

def airflow_external_task_sensor(*, timeout: int, poke_interval: int, mode: str, exponential_backoff: bool, pool: str, soft_fail: bool, name: str, description: str, external_dag_id: str, external_task_ids: typing.List[str], allowed_states: typing.List[str], failed_states: typing.List[str], execution_delta: "datetime.timedelta", check_existence: bool) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
    """
    The `@airflow_external_task_sensor` decorator attaches a Airflow [ExternalTaskSensor](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/sensors/external_task/index.html#airflow.sensors.external_task.ExternalTaskSensor) before the start step of the flow.
    This decorator only works when a flow is scheduled on Airflow and is compiled using `airflow create`. More than one `@airflow_external_task_sensor` can be added as a flow decorators. Adding more than one decorator will ensure that `start` step starts only after all sensors finish.
    
    
    Parameters
    ----------
    timeout : int
        Time, in seconds before the task times out and fails. (Default: 3600)
    poke_interval : int
        Time in seconds that the job should wait in between each try. (Default: 60)
    mode : str
        How the sensor operates. Options are: { poke | reschedule }. (Default: "poke")
    exponential_backoff : bool
        allow progressive longer waits between pokes by using exponential backoff algorithm. (Default: True)
    pool : str
        the slot pool this task should run in,
        slot pools are a way to limit concurrency for certain tasks. (Default:None)
    soft_fail : bool
        Set to true to mark the task as SKIPPED on failure. (Default: False)
    name : str
        Name of the sensor on Airflow
    description : str
        Description of sensor in the Airflow UI
    external_dag_id : str
        The dag_id that contains the task you want to wait for.
    external_task_ids : List[str]
        The list of task_ids that you want to wait for.
        If None (default value) the sensor waits for the DAG. (Default: None)
    allowed_states : List[str]
        Iterable of allowed states, (Default: ['success'])
    failed_states : List[str]
        Iterable of failed or dis-allowed states. (Default: None)
    execution_delta : datetime.timedelta
        time difference with the previous execution to look at,
        the default is the same logical date as the current task or DAG. (Default: None)
    check_existence: bool
        Set to True to check if the external task exists or check if
        the DAG to wait for exists. (Default: True)
    """
    ...

@typing.overload
def trigger_on_finish(*, flow: typing.Union[typing.Dict[str, str], str, None] = None, flows: typing.List[typing.Union[str, typing.Dict[str, str]]] = [], options: typing.Dict[str, typing.Any] = {}) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
    """
    Specifies the flow(s) that this flow depends on.
    
    ```
    @trigger_on_finish(flow='FooFlow')
    ```
    or
    ```
    @trigger_on_finish(flows=['FooFlow', 'BarFlow'])
    ```
    This decorator respects the @project decorator and triggers the flow
    when upstream runs within the same namespace complete successfully
    
    Additionally, you can specify project aware upstream flow dependencies
    by specifying the fully qualified project_flow_name.
    ```
    @trigger_on_finish(flow='my_project.branch.my_branch.FooFlow')
    ```
    or
    ```
    @trigger_on_finish(flows=['my_project.branch.my_branch.FooFlow', 'BarFlow'])
    ```
    
    You can also specify just the project or project branch (other values will be
    inferred from the current project or project branch):
    ```
    @trigger_on_finish(flow={"name": "FooFlow", "project": "my_project", "project_branch": "branch"})
    ```
    
    Note that `branch` is typically one of:
      - `prod`
      - `user.bob`
      - `test.my_experiment`
      - `prod.staging`
    
    
    Parameters
    ----------
    flow : Union[str, Dict[str, str]], optional, default None
        Upstream flow dependency for this flow.
    flows : List[Union[str, Dict[str, str]]], default []
        Upstream flow dependencies for this flow.
    options : Dict[str, Any], default {}
        Backend-specific configuration for tuning eventing behavior.
    """
    ...

@typing.overload
def trigger_on_finish(f: typing.Type[FlowSpecDerived]) -> typing.Type[FlowSpecDerived]:
    ...

def trigger_on_finish(f: typing.Union[typing.Type[FlowSpecDerived], None] = None, *, flow: typing.Union[typing.Dict[str, str], str, None] = None, flows: typing.List[typing.Union[str, typing.Dict[str, str]]] = [], options: typing.Dict[str, typing.Any] = {}):
    """
    Specifies the flow(s) that this flow depends on.
    
    ```
    @trigger_on_finish(flow='FooFlow')
    ```
    or
    ```
    @trigger_on_finish(flows=['FooFlow', 'BarFlow'])
    ```
    This decorator respects the @project decorator and triggers the flow
    when upstream runs within the same namespace complete successfully
    
    Additionally, you can specify project aware upstream flow dependencies
    by specifying the fully qualified project_flow_name.
    ```
    @trigger_on_finish(flow='my_project.branch.my_branch.FooFlow')
    ```
    or
    ```
    @trigger_on_finish(flows=['my_project.branch.my_branch.FooFlow', 'BarFlow'])
    ```
    
    You can also specify just the project or project branch (other values will be
    inferred from the current project or project branch):
    ```
    @trigger_on_finish(flow={"name": "FooFlow", "project": "my_project", "project_branch": "branch"})
    ```
    
    Note that `branch` is typically one of:
      - `prod`
      - `user.bob`
      - `test.my_experiment`
      - `prod.staging`
    
    
    Parameters
    ----------
    flow : Union[str, Dict[str, str]], optional, default None
        Upstream flow dependency for this flow.
    flows : List[Union[str, Dict[str, str]]], default []
        Upstream flow dependencies for this flow.
    options : Dict[str, Any], default {}
        Backend-specific configuration for tuning eventing behavior.
    """
    ...

@typing.overload
def pypi_base(*, packages: typing.Dict[str, str] = {}, python: typing.Union[str, None] = None) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
    """
    Specifies the PyPI packages for all steps of the flow.
    
    Use `@pypi_base` to set common packages required by all
    steps and use `@pypi` to specify step-specific overrides.
    
    Parameters
    ----------
    packages : Dict[str, str], default: {}
        Packages to use for this flow. The key is the name of the package
        and the value is the version to use.
    python : str, optional, default: None
        Version of Python to use, e.g. '3.7.4'. A default value of None implies
        that the version used will correspond to the version of the Python interpreter used to start the run.
    """
    ...

@typing.overload
def pypi_base(f: typing.Type[FlowSpecDerived]) -> typing.Type[FlowSpecDerived]:
    ...

def pypi_base(f: typing.Union[typing.Type[FlowSpecDerived], None] = None, *, packages: typing.Dict[str, str] = {}, python: typing.Union[str, None] = None):
    """
    Specifies the PyPI packages for all steps of the flow.
    
    Use `@pypi_base` to set common packages required by all
    steps and use `@pypi` to specify step-specific overrides.
    
    Parameters
    ----------
    packages : Dict[str, str], default: {}
        Packages to use for this flow. The key is the name of the package
        and the value is the version to use.
    python : str, optional, default: None
        Version of Python to use, e.g. '3.7.4'. A default value of None implies
        that the version used will correspond to the version of the Python interpreter used to start the run.
    """
    ...

