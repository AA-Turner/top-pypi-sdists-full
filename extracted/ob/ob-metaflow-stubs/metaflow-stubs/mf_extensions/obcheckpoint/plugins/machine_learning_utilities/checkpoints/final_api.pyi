######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.877279                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures
    import metaflow

from ..datastructures import CheckpointArtifact as CheckpointArtifact
from .constructors import load_checkpoint as load_checkpoint
from .exceptions import CheckpointNotAvailableException as CheckpointNotAvailableException
from .exceptions import CheckpointException as CheckpointException

TYPE_CHECKING: bool

CHECKPOINT_UID_ENV_VAR_NAME: str

DEFAULT_NAME: str

TASK_CHECKPOINTS_ARTIFACT_NAME: str

DEFAULT_STORAGE_FORMAT: str

class Checkpoint(object, metaclass=type):
    def __init__(self, temp_dir_root = None, init_dir = False):
        ...
    @property
    def directory(self):
        ...
    def save(self, path = None, metadata = None, latest = True, name = 'mfchckpt', storage_format = 'files') -> typing.Dict:
        """
        Saves the checkpoint to the datastore
        
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
                - If no path is provided then the `Checkpoint.directory` will be saved as the checkpoint.
        
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
    def generate_key(self, name: str, version_id: int = None):
        ...
    def __enter__(self):
        ...
    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
    def list(self, name: typing.Optional[str] = None, task: typing.Union["metaflow.Task", str, None] = None, attempt: typing.Union[int, str, None] = None, full_namespace: bool = False, as_dict: bool = True) -> typing.List[typing.Union[typing.Dict, metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact]]:
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
        
        Checkpoint().list(name="best") # lists checkpoints in the current task with the name "best"
        Checkpoint().list(task="anotherflow/somerunid/somestep/sometask", name="best") # Identical as the above one but
        Checkpoint().list() # lists **all** the checkpoints in the current task (including the ones from all attempts)
        
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
    def load(self, reference: typing.Union[str, typing.Dict, metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact], path: typing.Optional[str] = None):
        """
        loads a checkpoint reference from the datastore. (resembles a read op)
        
        Parameters
        ----------
        
        `reference` :
            - can be a string, dict or a CheckpointArtifact object:
                - string: a string reference to the checkpoint (checkpoint key)
                - dict: a dictionary reference to the checkpoint
                - CheckpointArtifact: a CheckpointArtifact object reference to the checkpoint
        """
        ...
    ...

