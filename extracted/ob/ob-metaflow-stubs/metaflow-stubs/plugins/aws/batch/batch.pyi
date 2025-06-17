######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.952806                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...datatools.s3.s3tail import S3Tail as S3Tail
from ..aws_utils import sanitize_batch_tag as sanitize_batch_tag
from ....exception import MetaflowException as MetaflowException
from .batch_client import BatchClient as BatchClient

OTEL_ENDPOINT: None

SERVICE_INTERNAL_URL: None

DATATOOLS_S3ROOT: None

DATASTORE_SYSROOT_S3: None

DEFAULT_METADATA: str

SERVICE_HEADERS: dict

BATCH_EMIT_TAGS: bool

CARD_S3ROOT: None

S3_ENDPOINT_URL: None

DEFAULT_SECRETS_BACKEND_TYPE: None

AWS_SECRETS_MANAGER_DEFAULT_REGION: None

S3_SERVER_SIDE_ENCRYPTION: None

BASH_SAVE_LOGS: str

LOGS_DIR: str

STDOUT_FILE: str

STDERR_FILE: str

STDOUT_PATH: str

STDERR_PATH: str

class BatchException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class BatchKilledException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class Batch(object, metaclass=type):
    def __init__(self, metadata, environment):
        ...
    def list_jobs(self, flow_name, run_id, user, echo):
        ...
    def kill_jobs(self, flow_name, run_id, user, echo):
        ...
    def create_job(self, step_name, step_cli, task_spec, code_package_sha, code_package_url, code_package_ds, image, queue, iam_role = None, execution_role = None, cpu = None, gpu = None, memory = None, run_time_limit = None, shared_memory = None, max_swap = None, swappiness = None, inferentia = None, efa = None, env = {}, attrs = {}, host_volumes = None, efs_volumes = None, use_tmpfs = None, tmpfs_tempdir = None, tmpfs_size = None, tmpfs_path = None, num_parallel = 0, ephemeral_storage = None, log_driver = None, log_options = None):
        ...
    def launch_job(self, step_name, step_cli, task_spec, code_package_sha, code_package_url, code_package_ds, image, queue, iam_role = None, execution_role = None, cpu = None, gpu = None, memory = None, run_time_limit = None, shared_memory = None, max_swap = None, swappiness = None, inferentia = None, efa = None, host_volumes = None, efs_volumes = None, use_tmpfs = None, tmpfs_tempdir = None, tmpfs_size = None, tmpfs_path = None, num_parallel = 0, env = {}, attrs = {}, ephemeral_storage = None, log_driver = None, log_options = None):
        ...
    def wait(self, stdout_location, stderr_location, echo = None):
        ...
    ...

