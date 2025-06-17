######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:03.038176                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import datetime
    import typing
FlowSpecDerived = typing.TypeVar("FlowSpecDerived", bound="FlowSpec", contravariant=False, covariant=False)
StepFlag = typing.NewType("StepFlag", bool)

from . import info_file as info_file
from . import exception as exception
from . import metaflow_config as metaflow_config
from . import multicore_utils as multicore_utils
from .multicore_utils import parallel_imap_unordered as parallel_imap_unordered
from .multicore_utils import parallel_map as parallel_map
from . import metaflow_current as metaflow_current
from .metaflow_current import current as current
from . import parameters as parameters
from . import user_configs as user_configs
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
from .user_configs.config_decorators import CustomFlowDecorator as CustomFlowDecorator
from .user_configs.config_decorators import CustomStepDecorator as CustomStepDecorator
from . import tuple_util as tuple_util
from . import cards as cards
from . import metaflow_git as metaflow_git
from . import events as events
from . import runner as runner
from . import plugins as plugins
from .mf_extensions.outerbounds.toplevel.global_aliases_for_metaflow_package import S3 as S3
from . import includefile as includefile
from .includefile import IncludeFile as IncludeFile
from .plugins.pypi.parsers import conda_environment_yml_parser as conda_environment_yml_parser
from .plugins.pypi.parsers import pyproject_toml_parser as pyproject_toml_parser
from .plugins.pypi.parsers import requirements_txt_parser as requirements_txt_parser
from . import client as client
from .client.core import namespace as namespace
from .client.core import get_namespace as get_namespace
from .client.core import default_namespace as default_namespace
from .client.core import metadata as metadata
from .client.core import get_metadata as get_metadata
from .client.core import default_metadata as default_metadata
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
from .mf_extensions.obcheckpoint.plugins.machine_learning_utilities.checkpoints.final_api import Checkpoint as Checkpoint
from .mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures import load_model as load_model
from .mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastore.context import artifact_store_from as artifact_store_from
from .mf_extensions.outerbounds.toplevel.global_aliases_for_metaflow_package import get_aws_client as get_aws_client
from .mf_extensions.outerbounds.plugins.snowflake.snowflake import Snowflake as Snowflake
from .mf_extensions.outerbounds.plugins.checkpoint_datastores.nebius import nebius_checkpoints as nebius_checkpoints
from .mf_extensions.outerbounds.plugins.checkpoint_datastores.coreweave import coreweave_checkpoints as coreweave_checkpoints
from .mf_extensions.outerbounds.plugins.aws.assume_role_decorator import assume_role as assume_role
from . import cli_components as cli_components
from . import system as system
from . import pylint_wrapper as pylint_wrapper
from . import cli as cli
from . import profilers as profilers

EXT_PKG: str

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
    f : Union[Callable[[FlowSpecDerived], None], Callable[[FlowSpecDerived, Any], None]]
        Function to make into a Metaflow Step
    
    Returns
    -------
    Union[Callable[[FlowSpecDerived, StepFlag], None], Callable[[FlowSpecDerived, Any, StepFlag], None]]
        Function that is a Metaflow Step
    """
    ...

@typing.overload
def step(f: typing.Callable[[FlowSpecDerived, typing.Any], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def step(f: typing.Union[typing.Callable[[FlowSpecDerived], None], typing.Callable[[FlowSpecDerived, typing.Any], None]]):
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
    f : Union[Callable[[FlowSpecDerived], None], Callable[[FlowSpecDerived, Any], None]]
        Function to make into a Metaflow Step
    
    Returns
    -------
    Union[Callable[[FlowSpecDerived, StepFlag], None], Callable[[FlowSpecDerived, Any, StepFlag], None]]
        Function that is a Metaflow Step
    """
    ...

@typing.overload
def model(*, load: typing.Union[typing.List[str], str, typing.List[typing.Tuple[str, typing.Optional[str]]]] = None, temp_dir_root: str = None) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Enables loading / saving of models within a step.
    
    
    
    Parameters
    ----------
    load : Union[List[str],str,List[Tuple[str,Union[str,None]]]], default: None
        Artifact name/s referencing the models/checkpoints to load. Artifact names refer to the names of the instance variables set to `self`.
        These artifact names give to `load` be reference objects or reference `key` string's from objects created by:
        - `current.checkpoint`
        - `current.model`
        - `current.huggingface_hub`
    
        If a list of tuples is provided, the first element is the artifact name and the second element is the path the artifact needs be unpacked on
        the local filesystem. If the second element is None, the artifact will be unpacked in the current working directory.
        If a string is provided, then the artifact corresponding to that name will be loaded in the current working directory.
    
    temp_dir_root : str, default: None
        The root directory under which `current.model.loaded` will store loaded models
    """
    ...

@typing.overload
def model(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def model(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def model(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, load: typing.Union[typing.List[str], str, typing.List[typing.Tuple[str, typing.Optional[str]]]] = None, temp_dir_root: str = None):
    """
    Enables loading / saving of models within a step.
    
    
    
    Parameters
    ----------
    load : Union[List[str],str,List[Tuple[str,Union[str,None]]]], default: None
        Artifact name/s referencing the models/checkpoints to load. Artifact names refer to the names of the instance variables set to `self`.
        These artifact names give to `load` be reference objects or reference `key` string's from objects created by:
        - `current.checkpoint`
        - `current.model`
        - `current.huggingface_hub`
    
        If a list of tuples is provided, the first element is the artifact name and the second element is the path the artifact needs be unpacked on
        the local filesystem. If the second element is None, the artifact will be unpacked in the current working directory.
        If a string is provided, then the artifact corresponding to that name will be loaded in the current working directory.
    
    temp_dir_root : str, default: None
        The root directory under which `current.model.loaded` will store loaded models
    """
    ...

@typing.overload
def checkpoint(*, load_policy: str = 'fresh', temp_dir_root: str = None) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Enables checkpointing for a step.
    
    
    
    Parameters
    ----------
    load_policy : str, default: "fresh"
        The policy for loading the checkpoint. The following policies are supported:
            - "eager": Loads the the latest available checkpoint within the namespace.
            With this mode, the latest checkpoint written by any previous task (can be even a different run) of the step
            will be loaded at the start of the task.
            - "none": Do not load any checkpoint
            - "fresh": Loads the lastest checkpoint created within the running Task.
            This mode helps loading checkpoints across various retry attempts of the same task.
            With this mode, no checkpoint will be loaded at the start of a task but any checkpoints
            created within the task will be loaded when the task is retries execution on failure.
    
    temp_dir_root : str, default: None
        The root directory under which `current.checkpoint.directory` will be created.
    """
    ...

@typing.overload
def checkpoint(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def checkpoint(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def checkpoint(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, load_policy: str = 'fresh', temp_dir_root: str = None):
    """
    Enables checkpointing for a step.
    
    
    
    Parameters
    ----------
    load_policy : str, default: "fresh"
        The policy for loading the checkpoint. The following policies are supported:
            - "eager": Loads the the latest available checkpoint within the namespace.
            With this mode, the latest checkpoint written by any previous task (can be even a different run) of the step
            will be loaded at the start of the task.
            - "none": Do not load any checkpoint
            - "fresh": Loads the lastest checkpoint created within the running Task.
            This mode helps loading checkpoints across various retry attempts of the same task.
            With this mode, no checkpoint will be loaded at the start of a task but any checkpoints
            created within the task will be loaded when the task is retries execution on failure.
    
    temp_dir_root : str, default: None
        The root directory under which `current.checkpoint.directory` will be created.
    """
    ...

def huggingface_hub(*, temp_dir_root: typing.Optional[str] = None, load: typing.Union[typing.List[str], typing.List[typing.Tuple[typing.Dict, str]], typing.List[typing.Tuple[str, str]], typing.List[typing.Dict], None]) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Decorator that helps cache, version and store models/datasets from huggingface hub.
    
    
    Parameters
    ----------
    temp_dir_root : str, optional
        The root directory that will hold the temporary directory where objects will be downloaded.
    
    load: Union[List[str], List[Tuple[Dict, str]], List[Tuple[str, str]], List[Dict], None]
        The list of repos (models/datasets) to load.
    
        Loaded repos can be accessed via `current.huggingface_hub.loaded`. If load is set, then the following happens:
    
        - If repo (model/dataset) is not found in the datastore:
            - Downloads the repo from Hugging Face Hub to a temporary directory (or uses specified path) for local access
            - Stores it in Metaflow's datastore (s3/gcs/azure etc.) with a unique name based on repo_type/repo_id
                - All HF models loaded for a `@step` will be cached separately under flow/step/namespace.
    
        - If repo is found in the datastore:
            - Loads it directly from datastore to local path (can be temporary directory or specified path)
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

def ollama(*, models: list, backend: str, force_pull: bool, cache_update_policy: str, force_cache_update: bool, debug: bool, circuit_breaker_config: dict, timeout_config: dict) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    This decorator is used to run Ollama APIs as Metaflow task sidecars.
    
    User code call
    --------------
    @ollama(
        models=[...],
        ...
    )
    
    Valid backend options
    ---------------------
    - 'local': Run as a separate process on the local task machine.
    - (TODO) 'managed': Outerbounds hosts and selects compute provider.
    - (TODO) 'remote': Spin up separate instance to serve Ollama models.
    
    Valid model options
    -------------------
    Any model here https://ollama.com/search, e.g. 'llama3.2', 'llama3.3'
    
    
    Parameters
    ----------
    models: list[str]
        List of Ollama containers running models in sidecars.
    backend: str
        Determines where and how to run the Ollama process.
    force_pull: bool
        Whether to run `ollama pull` no matter what, or first check the remote cache in Metaflow datastore for this model key.
    cache_update_policy: str
        Cache update policy: "auto", "force", or "never".
    force_cache_update: bool
        Simple override for "force" cache update policy.
    debug: bool
        Whether to turn on verbose debugging logs.
    circuit_breaker_config: dict
        Configuration for circuit breaker protection. Keys: failure_threshold, recovery_timeout, reset_timeout.
    timeout_config: dict
        Configuration for various operation timeouts. Keys: pull, stop, health_check, install, server_startup.
    """
    ...

@typing.overload
def resources(*, cpu: int = 1, gpu: typing.Optional[int] = None, disk: typing.Optional[int] = None, memory: int = 4096, shared_memory: typing.Optional[int] = None) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
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

def resources(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, cpu: int = 1, gpu: typing.Optional[int] = None, disk: typing.Optional[int] = None, memory: int = 4096, shared_memory: typing.Optional[int] = None):
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

def nvct(*, gpu: int, gpu_type: str) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies that this step should execute on DGX cloud.
    
    
    Parameters
    ----------
    gpu : int
        Number of GPUs to use.
    gpu_type : str
        Type of Nvidia GPU to use.
    """
    ...

@typing.overload
def fast_bakery_internal(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    """
    Internal decorator to support Fast bakery
    """
    ...

@typing.overload
def fast_bakery_internal(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def fast_bakery_internal(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None):
    """
    Internal decorator to support Fast bakery
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

def app_deploy(*, app_port: int, app_name: str) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies that this step is used to deploy an instance of the app.
    Requires that self.app_name, self.app_port, self.entrypoint and self.deployDir is set.
    
    
    Parameters
    ----------
    app_port : int
        Number of GPUs to use.
    app_name : str
        Name of the app to deploy.
    """
    ...

def nvidia(*, gpu: int, gpu_type: str, queue_timeout: int) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies that this step should execute on DGX cloud.
    
    
    Parameters
    ----------
    gpu : int
        Number of GPUs to use.
    gpu_type : str
        Type of Nvidia GPU to use.
    queue_timeout : int
        Time to keep the job in NVCF's queue.
    """
    ...

@typing.overload
def catch(*, var: typing.Optional[str] = None, print_exception: bool = True) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
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

def catch(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, var: typing.Optional[str] = None, print_exception: bool = True):
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
def card(*, type: str = 'default', id: typing.Optional[str] = None, options: typing.Dict[str, typing.Any] = {}, timeout: int = 45) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
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

def card(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, type: str = 'default', id: typing.Optional[str] = None, options: typing.Dict[str, typing.Any] = {}, timeout: int = 45):
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
def conda(*, packages: typing.Dict[str, str] = {}, libraries: typing.Dict[str, str] = {}, python: typing.Optional[str] = None, disabled: bool = False) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
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

def conda(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, packages: typing.Dict[str, str] = {}, libraries: typing.Dict[str, str] = {}, python: typing.Optional[str] = None, disabled: bool = False):
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

def kubernetes(*, cpu: int = 1, memory: int = 4096, disk: int = 10240, image: typing.Optional[str] = None, image_pull_policy: str = 'KUBERNETES_IMAGE_PULL_POLICY', image_pull_secrets: typing.List[str] = [], service_account: str = 'METAFLOW_KUBERNETES_SERVICE_ACCOUNT', secrets: typing.Optional[typing.List[str]] = None, node_selector: typing.Union[typing.Dict[str, str], str, None] = None, namespace: str = 'METAFLOW_KUBERNETES_NAMESPACE', gpu: typing.Optional[int] = None, gpu_vendor: str = 'KUBERNETES_GPU_VENDOR', tolerations: typing.List[str] = [], labels: typing.Dict[str, str] = 'METAFLOW_KUBERNETES_LABELS', annotations: typing.Dict[str, str] = 'METAFLOW_KUBERNETES_ANNOTATIONS', use_tmpfs: bool = False, tmpfs_tempdir: bool = True, tmpfs_size: typing.Optional[int] = None, tmpfs_path: typing.Optional[str] = '/metaflow_temp', persistent_volume_claims: typing.Optional[typing.Dict[str, str]] = None, shared_memory: typing.Optional[int] = None, port: typing.Optional[int] = None, compute_pool: typing.Optional[str] = None, hostname_resolution_timeout: int = 600, qos: str = 'Burstable', security_context: typing.Optional[typing.Dict[str, typing.Any]] = None) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
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
    ...

def vllm(*, model: str, backend: str, debug: bool, kwargs: typing.Any) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    This decorator is used to run vllm APIs as Metaflow task sidecars.
    
    User code call
    --------------
    @vllm(
        model="...",
        ...
    )
    
    Valid backend options
    ---------------------
    - 'local': Run as a separate process on the local task machine.
    
    Valid model options
    -------------------
    Any HuggingFace model identifier, e.g. 'meta-llama/Llama-3.2-1B'
    
    NOTE: vLLM's OpenAI-compatible server serves ONE model per server instance.
    If you need multiple models, you must create multiple @vllm decorators.
    
    
    Parameters
    ----------
    model: str
        HuggingFace model identifier to be served by vLLM.
    backend: str
        Determines where and how to run the vLLM process.
    debug: bool
        Whether to turn on verbose debugging logs.
    kwargs : Any
        Any other keyword arguments are passed directly to the vLLM engine.
        This allows for flexible configuration of vLLM server settings.
        For example, `tensor_parallel_size=2`.
    """
    ...

@typing.overload
def pypi(*, packages: typing.Dict[str, str] = {}, python: typing.Optional[str] = None) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
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

def pypi(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, packages: typing.Dict[str, str] = {}, python: typing.Optional[str] = None):
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
def secrets(*, sources: typing.List[typing.Union[str, typing.Dict[str, typing.Any]]] = []) -> typing.Callable[[typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]], typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]]]:
    """
    Specifies secrets to be retrieved and injected as environment variables prior to
    the execution of a step.
    
    
    Parameters
    ----------
    sources : List[Union[str, Dict[str, Any]]], default: []
        List of secret specs, defining how the secrets are to be retrieved
    """
    ...

@typing.overload
def secrets(f: typing.Callable[[FlowSpecDerived, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, StepFlag], None]:
    ...

@typing.overload
def secrets(f: typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]) -> typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None]:
    ...

def secrets(f: typing.Union[typing.Callable[[FlowSpecDerived, StepFlag], None], typing.Callable[[FlowSpecDerived, typing.Any, StepFlag], None], None] = None, *, sources: typing.List[typing.Union[str, typing.Dict[str, typing.Any]]] = []):
    """
    Specifies secrets to be retrieved and injected as environment variables prior to
    the execution of a step.
    
    
    Parameters
    ----------
    sources : List[Union[str, Dict[str, Any]]], default: []
        List of secret specs, defining how the secrets are to be retrieved
    """
    ...

@typing.overload
def trigger(*, event: typing.Union[str, typing.Dict[str, typing.Any], None] = None, events: typing.List[typing.Union[str, typing.Dict[str, typing.Any]]] = [], options: typing.Dict[str, typing.Any] = {}) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
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
    
    
    Parameters
    ----------
    event : Union[str, Dict[str, Any]], optional, default None
        Event dependency for this flow.
    events : List[Union[str, Dict[str, Any]]], default []
        Events dependency for this flow.
    options : Dict[str, Any], default {}
        Backend-specific configuration for tuning eventing behavior.
    """
    ...

@typing.overload
def trigger(f: typing.Type[FlowSpecDerived]) -> typing.Type[FlowSpecDerived]:
    ...

def trigger(f: typing.Optional[typing.Type[FlowSpecDerived]] = None, *, event: typing.Union[str, typing.Dict[str, typing.Any], None] = None, events: typing.List[typing.Union[str, typing.Dict[str, typing.Any]]] = [], options: typing.Dict[str, typing.Any] = {}):
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
    
    
    Parameters
    ----------
    event : Union[str, Dict[str, Any]], optional, default None
        Event dependency for this flow.
    events : List[Union[str, Dict[str, Any]]], default []
        Events dependency for this flow.
    options : Dict[str, Any], default {}
        Backend-specific configuration for tuning eventing behavior.
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

def trigger_on_finish(f: typing.Optional[typing.Type[FlowSpecDerived]] = None, *, flow: typing.Union[typing.Dict[str, str], str, None] = None, flows: typing.List[typing.Union[str, typing.Dict[str, str]]] = [], options: typing.Dict[str, typing.Any] = {}):
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

def with_artifact_store(f: typing.Optional[typing.Type[FlowSpecDerived]] = None):
    """
    Allows setting external datastores to save data for the
    `@checkpoint`/`@model`/`@huggingface_hub` decorators.
    
    This decorator is useful when users wish to save data to a different datastore
    than what is configured in Metaflow. This can be for variety of reasons:
    
    1. Data security: The objects needs to be stored in a bucket (object storage) that is not accessible by other flows.
    2. Data Locality: The location where the task is executing is not located in the same region as the datastore.
        - Example: Metaflow datastore lives in US East, but the task is executing in Finland datacenters.
    3. Data Lifecycle Policies: The objects need to be archived / managed separately from the Metaflow managed objects.
        - Example: Flow is training very large models that need to be stored separately and will be deleted more aggressively than the Metaflow managed objects.
    
    Usage:
    ----------
    
    - Using a custom IAM role to access the datastore.
    
        ```python
        @with_artifact_store(
            type="s3",
            config=lambda: {
                "root": "s3://my-bucket-foo/path/to/root",
                "role_arn": ROLE,
            },
        )
        class MyFlow(FlowSpec):
    
            @checkpoint
            @step
            def start(self):
                with open("my_file.txt", "w") as f:
                    f.write("Hello, World!")
                self.external_bucket_checkpoint = current.checkpoint.save("my_file.txt")
                self.next(self.end)
    
        ```
    
    - Using credentials to access the s3-compatible datastore.
    
        ```python
        @with_artifact_store(
            type="s3",
            config=lambda: {
                "root": "s3://my-bucket-foo/path/to/root",
                "client_params": {
                    "aws_access_key_id": os.environ.get("MY_CUSTOM_ACCESS_KEY"),
                    "aws_secret_access_key": os.environ.get("MY_CUSTOM_SECRET_KEY"),
                },
            },
        )
        class MyFlow(FlowSpec):
    
            @checkpoint
            @step
            def start(self):
                with open("my_file.txt", "w") as f:
                    f.write("Hello, World!")
                self.external_bucket_checkpoint = current.checkpoint.save("my_file.txt")
                self.next(self.end)
    
        ```
    
    - Accessing objects stored in external datastores after task execution.
    
        ```python
        run = Run("CheckpointsTestsFlow/8992")
        with artifact_store_from(run=run, config={
            "client_params": {
                "aws_access_key_id": os.environ.get("MY_CUSTOM_ACCESS_KEY"),
                "aws_secret_access_key": os.environ.get("MY_CUSTOM_SECRET_KEY"),
            },
        }):
            with Checkpoint() as cp:
                latest = cp.list(
                    task=run["start"].task
                )[0]
                print(latest)
                cp.load(
                    latest,
                    "test-checkpoints"
                )
    
        task = Task("TorchTuneFlow/8484/train/53673")
        with artifact_store_from(run=run, config={
            "client_params": {
                "aws_access_key_id": os.environ.get("MY_CUSTOM_ACCESS_KEY"),
                "aws_secret_access_key": os.environ.get("MY_CUSTOM_SECRET_KEY"),
            },
        }):
            load_model(
                task.data.model_ref,
                "test-models"
            )
        ```
    Parameters:
    ----------
    
    type: str
        The type of the datastore. Can be one of 's3', 'gcs', 'azure' or any other supported metaflow Datastore.
    
    config: dict or Callable
        Dictionary of configuration options for the datastore. The following keys are required:
        - root: The root path in the datastore where the data will be saved. (needs to be in the format expected by the datastore)
            - example: 's3://bucket-name/path/to/root'
            - example: 'gs://bucket-name/path/to/root'
            - example: 'https://myblockacc.blob.core.windows.net/metaflow/'
        - role_arn (optional): AWS IAM role to access s3 bucket (only when `type` is 's3')
        - session_vars (optional): AWS session variables to access s3 bucket (only when `type` is 's3')
        - client_params (optional): AWS client parameters to access s3 bucket (only when `type` is 's3')
    """
    ...

@typing.overload
def schedule(*, hourly: bool = False, daily: bool = True, weekly: bool = False, cron: typing.Optional[str] = None, timezone: typing.Optional[str] = None) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
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

def schedule(f: typing.Optional[typing.Type[FlowSpecDerived]] = None, *, hourly: bool = False, daily: bool = True, weekly: bool = False, cron: typing.Optional[str] = None, timezone: typing.Optional[str] = None):
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
def pypi_base(*, packages: typing.Dict[str, str] = {}, python: typing.Optional[str] = None) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
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

def pypi_base(f: typing.Optional[typing.Type[FlowSpecDerived]] = None, *, packages: typing.Dict[str, str] = {}, python: typing.Optional[str] = None):
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

def project(*, name: str, branch: typing.Optional[str] = None, production: bool = False) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
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
def conda_base(*, packages: typing.Dict[str, str] = {}, libraries: typing.Dict[str, str] = {}, python: typing.Optional[str] = None, disabled: bool = False) -> typing.Callable[[typing.Type[FlowSpecDerived]], typing.Type[FlowSpecDerived]]:
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

def conda_base(f: typing.Optional[typing.Type[FlowSpecDerived]] = None, *, packages: typing.Dict[str, str] = {}, libraries: typing.Dict[str, str] = {}, python: typing.Optional[str] = None, disabled: bool = False):
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

pkg_name: str

