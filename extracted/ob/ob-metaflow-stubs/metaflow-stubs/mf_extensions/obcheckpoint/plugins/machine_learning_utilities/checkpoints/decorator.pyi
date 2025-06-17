######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.909647                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures
    import metaflow
    import os
    import metaflow.decorators

from .exceptions import CheckpointException as CheckpointException
from ..utils import flowspec_utils as flowspec_utils
from ..card_utils.deco_injection_mixin import CardDecoratorInjector as CardDecoratorInjector
from ..card_utils.async_cards import AsyncPeriodicRefresher as AsyncPeriodicRefresher
from .cards.checkpoint_lister import CheckpointListRefresher as CheckpointListRefresher
from .cards.checkpoint_lister import CheckpointsCollector as CheckpointsCollector
from .cards.lineage_card import create_checkpoint_card as create_checkpoint_card
from .cards.lineage_card import null_card as null_card
from .lineage import checkpoint_load_related_metadata as checkpoint_load_related_metadata
from .lineage import trace_lineage as trace_lineage
from .constructors import load_checkpoint as load_checkpoint
from .core import ScopeResolver as ScopeResolver
from .core import CheckpointLoadPolicy as CheckpointLoadPolicy
from ..datastructures import CheckpointArtifact as CheckpointArtifact
from ..datastore.decorator import set_datastore_context as set_datastore_context
from .final_api import Checkpoint as Checkpoint

DEFAULT_NAME: str

CHECKPOINT_TAG_PREFIX: str

CHECKPOINT_TASK_IDENTIFIER_ENV_VAR_NAME: str

CHECKPOINT_UID_ENV_VAR_NAME: str

TASK_CHECKPOINTS_ARTIFACT_NAME: str

TASK_LATEST_CHECKPOINT_ARTIFACT_NAME: str

DEFAULT_STORAGE_FORMAT: str

INTERNAL_ARTIFACTS_SET: set

TYPE_CHECKING: bool

def warning_message(message, logger = None, ts = False, prefix = '[@checkpoint]'):
    ...

class CurrentCheckpointer(object, metaclass=type):
    @property
    def task_identifier(self):
        ...
    @property
    def directory(self):
        ...
    @property
    def is_loaded(self):
        ...
    @property
    def info(self):
        ...
    def __init__(self, flow, task_identifier, resolved_scope, logger, gang_scheduled_task = False, temp_dir_root = None):
        ...
    def save(self, path: typing.Union[str, os.PathLike, None] = None, name: typing.Optional[str] = 'mfchckpt', metadata: typing.Optional[typing.Dict] = {}, latest: bool = True, storage_format: str = 'files'):
        """
        Saves the checkpoint to the datastore.
        
        Parameters
        ----------
        path : Optional[Union[str, os.PathLike]], default: None
            The path to save the checkpoint. Accepts a file path or a directory path.
                - If a directory path is provided, all the contents within that directory will be saved.
                When a checkpoint is reloaded during task retries, `the current.checkpoint.directory` will
                contain the contents of this directory.
                - If a file path is provided, the file will be directly saved to the datastore (with the same filename).
                When the checkpoint is reloaded during task retries, the file with the same name will be available in the
                `current.checkpoint.directory`.
                - If no path is provided then the `current.checkpoint.directory` will be saved as the checkpoint.
        
        name : Optional[str], default: "mfchckpt"
            The name of the checkpoint.
        
        metadata : Optional[Dict], default: {}
            Any metadata that needs to be saved with the checkpoint.
        
        latest : bool, default: True
            If True, the checkpoint will be marked as the latest checkpoint.
            This helps determine if the checkpoint gets loaded when the task restarts.
        
        storage_format : str, default: files
            If `tar`, the contents of the directory will be tarred before saving to the datastore.
            If `files`, saves directory directly to the datastore.
        """
        ...
    def list(self, name: typing.Optional[str] = None, task: typing.Union["metaflow.Task", str, None] = None, attempt: typing.Optional[int] = None, full_namespace: bool = False) -> typing.List[typing.Dict]:
        """
        lists the checkpoints in the current task or the specified task.
        
        When users call `list` without any arguments, it will list all the checkpoints in the currently executing
        task (this includes all attempts). If the `list` method is called without any arguments outside a Metaflow Task execution context,
        it will raise an exception. Users can also call `list` with `attempt` argument to list all checkpoints within a
        the specific attempt of the currently executing task.
        
        When a `task` argument is provided, the `list` method will return all the checkpoints
        for a task's latest attempt unless a specific attempt number is set in the `attempt` argument.
        If the `Task` object contains a `DataArtifact` with all the previous checkpoints, then the `list` method will return
        all the checkpoints from the data artifact. If for some reason the DataArtifact is not written, then the `list` method will
        return all checkpoints directly from the checkpoint's datastore.
        
        Usage:
        ------
        
        ```python
        current.checkpoint.list(name="best") # lists checkpoints in the current task with the name "best"
        current.checkpoint.list( # Identical as the above one but lists checkpoints from the specified task with the name "best"
            task="anotherflow/somerunid/somestep/sometask",
            name="best"
        )
        current.checkpoint.list() # lists **all** the checkpoints in the current task (including the ones from all attempts)
        ```
        
        Parameters
        ----------
        
        name : Optional[str], default: None
            Filter checkpoints by name.
        
        task : Optional[Union["metaflow.Task", str]], default: None
            The task to list checkpoints from. Can be either a `Task` object or a task pathspec string.
            If None, lists checkpoints for the current task.
            Raises an exception if task is not provided when called outside a Metaflow Task execution context.
        
        attempt : Optional[Union[int, str]], default: None
            Filter checkpoints by attempt.
            If `task` is not None and `attempt` is None, then it will load the task's latest attempt
        
        full_namespace : bool, default: False
            If True, lists checkpoints from the full namespace.
            Only allowed during a Metaflow Task execution context.
            Raises an exception if `full_namespace` is set to True when called outside a Metaflow Task execution context.
        
        Returns
        -------
        List[Dict]
        """
        ...
    def cleanup(self):
        ...
    def refresh_directory(self):
        ...
    def load(self, reference: typing.Union[str, typing.Dict, metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact], path: typing.Optional[str] = None):
        """
        loads a checkpoint reference from the datastore. (resembles a read op)
        
        This can have two meanings:
            - If the path is provided, it will load the checkpoint in the provided path
            - If no path is provided, it will load the checkpoint in the default directory
        
        Parameters
        ----------
        
        `reference` :
            - can be a string, dict or a CheckpointArtifact object:
                - string: a string reference to the checkpoint
                - dict: a dictionary form of the CheckpointArtifact
                - CheckpointArtifact: a CheckpointArtifact object reference to the checkpoint
        """
        ...
    ...

def merge_dicts_with_precedence(*args: dict) -> dict:
    """
    Merges multiple dictionaries, respecting the order of precedence.
    
    This function takes any number of dictionary arguments and merges them into a single dictionary.
    If the same key exists in multiple dictionaries, the value from the dictionary that appears
    last in the argument list takes precedence, except where the value is None, in which case
    the search continues in the earlier dictionaries for a non-None value.
    
    The operation is not recursive and will only consider top-level keys.
    
    Parameters:
    - args: A variable number of dictionary arguments. Each argument must be a dictionary.
    
    Returns:
    - dict: A single dictionary that results from merging the input dictionaries according to their order of precedence.
    
    Examples:
    - merge_dicts_with_precedence(defaults, attrs)
      Here, `defaults` is a dictionary of default values, and `attrs` contains override values.
      Any None values in `attrs` will result in values from `defaults` being used.
    
    - merge_dicts_with_precedence(defaults, global_config, attrs)
      In this scenario, `global_config` can override `defaults`, and `attrs` can override both
      `defaults` and `global_config`. The order of arguments defines the precedence.
    
    Note:
    The function behaves differently if the order of the arguments changes, reflecting the
    precedence of the values set based on their position in the argument list.
    """
    ...

class CheckpointDecorator(metaflow.decorators.StepDecorator, metaclass=type):
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
    
    
    MF Add To Current
    -----------------
    checkpoint -> metaflow_extensions.obcheckpoint.plugins.machine_learning_utilities.checkpoints.decorator.CurrentCheckpointer
        The `@checkpoint` decorator makes saving/loading checkpoints available through the `current.checkpoint`.
        The object exposes `save`/`load`/`list` methods for saving/loading checkpoints.
    
        You can check if a checkpoint is loaded by `current.checkpoint.is_loaded` and get the checkpoint information
        by using `current.checkpoint.info`. The `current.checkpoint.directory` returns the path to the checkpoint directory
        where the checkpoint maybe loaded or saved.
    
        Usage (Saving Checkpoints):
        -------
        ```
        @checkpoint
        @step
        def train(self):
            model = create_model(self.parameters, checkpoint_path = None)
            for i in range(self.epochs):
                # some training logic
                loss = model.train(self.dataset)
                if i % 10 == 0:
                    model.save(
                        current.checkpoint.directory,
                    )
                    # saves the contents of the `current.checkpoint.directory` as a checkpoint
                    # and returns a reference dictionary to the checkpoint saved in the datastore
                    self.latest_checkpoint = current.checkpoint.save(
                        name="epoch_checkpoint",
                        metadata={
                            "epoch": i,
                            "loss": loss,
                        }
                    )
        ```
        Usage (Using Loaded Checkpoints):
        -------
        ```
        @retry(times=3)
        @checkpoint
        @step
        def train(self):
            # Assume that the task has restarted and the previous attempt of the task
            # saved a checkpoint
            checkpoint_path = None
            if current.checkpoint.is_loaded: # Check if a checkpoint is loaded
                print("Loaded checkpoint from the previous attempt")
                checkpoint_path = current.checkpoint.directory
    
            model = create_model(self.parameters, checkpoint_path = checkpoint_path)
            for i in range(self.epochs):
                ...
        ```
    
        @@ Returns
        -------
        CurrentCheckpointer
            The object for handling checkpointing within a step.
    """
    def step_init(self, flow, graph, step_name, decorators, environment, flow_datastore, logger):
        ...
    def task_exception(self, exception, step_name, flow, graph, retry_count, max_user_code_retries):
        ...
    def task_pre_step(self, step_name, task_datastore, metadata, run_id, task_id, flow, graph, retry_count, max_user_code_retries, ubf_context, inputs):
        ...
    def task_decorate(self, step_func, flow, graph, retry_count, max_user_code_retries, ubf_context):
        ...
    def task_post_step(self, step_name, flow, graph, retry_count, max_user_code_retries):
        ...
    ...

