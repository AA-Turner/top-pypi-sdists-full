######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.935723                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.checkpoints.core
    import metaflow
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.checkpoints.checkpoint_storage

from ......metaflow_current import current as current
from ......exception import MetaflowException as MetaflowException
from .exceptions import CheckpointNotAvailableException as CheckpointNotAvailableException
from .exceptions import CheckpointException as CheckpointException
from ..utils import flowspec_utils as flowspec_utils
from .checkpoint_storage import CheckpointDatastore as CheckpointDatastore
from ..datastructures import CheckpointArtifact as CheckpointArtifact
from ..datastore.task_utils import init_datastorage_object as init_datastorage_object
from ..datastore.task_utils import resolve_storage_backend as resolve_task_storage_backend
from ..datastore.task_utils import storage_backend_from_flow as storage_backend_from_flow

TYPE_CHECKING: bool

CHECKPOINT_TAG_PREFIX: str

MAX_HASH_LEN: int

DEFAULT_NAME: str

CHECKPOINT_UID_ENV_VAR_NAME: str

DEFAULT_STORAGE_FORMAT: str

class Checkpointer(object, metaclass=type):
    @property
    def current_version(self):
        ...
    def set_root_prefix(self, root_prefix):
        ...
    def __init__(self, datastore: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.checkpoints.checkpoint_storage.CheckpointDatastore, attempt: int = 0):
        ...
    def load_metadata(self, version_id: int = None, name = 'mfchckpt') -> dict:
        ...
    def artifact_id(self, name: str, version_id: int = None):
        ...
    def save(self, path: str, metadata = {}, latest = True, name = 'mfchckpt', storage_format = 'files') -> metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact:
        ...
    ...

class CheckpointLoadPolicy(object, metaclass=type):
    @classmethod
    def fresh(cls, datastore: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.checkpoints.checkpoint_storage.CheckpointDatastore, flow: "metaflow.FlowSpec") -> typing.Optional[metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact]:
        """
        ```python
        @checkpoint(load_policy="fresh")
        ```
        While in `fresh` mode, we want to load the "latest" checkpoint from
        what ever task is executing at the current memoment.
        
        The behavior is will be such that 1st attempt of any task will not load
        any checkpoint and there after it will load the checkpoint from the previous
        attempt of the task (ala the lastest checkpoint within the task).
        """
        ...
    @classmethod
    def eager(cls, datastore: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.checkpoints.checkpoint_storage.CheckpointDatastore, flow: "metaflow.FlowSpec") -> typing.Optional[metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact]:
        """
        ```python
        @checkpoint(load_policy="eager")
        ```
        While in `eager` mode, we want to load the "latest" checkpoint ever
        written at the "scope" level based on the kind of task that is executing.
        
        Setting this mode helps "checkpoints leak across executions" for the same task
        there by allowing a way to reboot the state when new executions start.
        """
        ...
    ...

class ScopeResolver(object, metaclass=type):
    @classmethod
    def from_namespace(cls):
        ...
    @classmethod
    def from_tags(cls, tags):
        ...
    ...

def warning_message(message, logger = None, ts = False, prefix = '[@checkpoint][warning]'):
    ...

class ReadResolver(object, metaclass=type):
    """
    Responsible for instantiating the `CheckpointDatastore` during read operations
    based on different context's.
    """
    @classmethod
    def from_pathspec(cls, pathspec):
        ...
    @classmethod
    def from_key(cls, checkpoint_key):
        """
        """
        ...
    @classmethod
    def from_checkpoint(cls, checkpoint: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact):
        """
        """
        ...
    @classmethod
    def from_key_and_run(cls, run, checkpoint_key) -> metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.checkpoints.checkpoint_storage.CheckpointDatastore:
        """
        """
        ...
    ...

class WriteResolver(object, metaclass=type):
    """
    Responsible for instantiating the `CheckpointDatastore` and the subsequent
    `_checkpointer_uid` which can instantiate the `Checkpointer` object outside
    of the metaflow context.
    """
    @classmethod
    def can_resolve_from_envionment(cls):
        ...
    @classmethod
    def decompose_checkpoint_id(cls, checkpoint_id):
        ...
    @classmethod
    def resolver_info(cls, flow, run, step, taskid, taskidf, scope, attempt):
        ...
    @classmethod
    def construct_checkpoint_id(cls, resolver_info: ResolverInfo):
        ...
    @classmethod
    def from_environment(cls):
        ...
    @classmethod
    def from_run(cls, run: "metaflow.FlowSpec", scope: str, task_identifier: typing.Optional[str] = None, gang_scheduled_task = False):
        """
        The task-identifier gets computed in the Metaflow main process with the
        i.e. in the decorator. The pathspec we choose to write the metadata store
        depends on if the task is being gang scheduled or not.
        """
        ...
    ...

class CheckpointReferenceResolver(object, metaclass=type):
    """
    Resolve the Metaflow checkpoint object based on the flow artifact reference
    or key; Used for lineage derivation.
    """
    @classmethod
    def from_key(cls, flow, checkpoint_key):
        """
        Used by lineage derivation
        """
        ...
    ...

