######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.953837                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators

from ....metaflow_current import current as current
from ....metadata_provider.metadata import MetaDatum as MetaDatum
from ....metadata_provider.util import sync_local_metadata_to_datastore as sync_local_metadata_to_datastore
from ...timeout_decorator import get_run_time_limit_for_task as get_run_time_limit_for_task
from ..aws_utils import compute_resource_attributes as compute_resource_attributes
from ..aws_utils import get_docker_registry as get_docker_registry
from ..aws_utils import get_ec2_instance_metadata as get_ec2_instance_metadata
from .batch import BatchException as BatchException

BATCH_CONTAINER_IMAGE: None

BATCH_CONTAINER_REGISTRY: None

BATCH_JOB_QUEUE: None

DATASTORE_LOCAL_DIR: str

ECS_FARGATE_EXECUTION_ROLE: None

ECS_S3_ACCESS_IAM_ROLE: None

UBF_CONTROL: str

class BatchDecorator(metaflow.decorators.StepDecorator, metaclass=type):
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
    """
    def init(self):
        ...
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
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

