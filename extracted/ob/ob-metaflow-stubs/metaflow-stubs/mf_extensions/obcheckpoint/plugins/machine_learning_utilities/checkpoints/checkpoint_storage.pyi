######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.34.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-07-21T20:55:40.986249                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.checkpoints.checkpoint_storage
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastore.core
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures
    import metaflow.datastore.datastore_storage

from ..exceptions import KeyNotCompatibleWithObjectException as KeyNotCompatibleWithObjectException
from ..utils.identity_utils import pathspec_hash as pathspec_hash
from ..utils.general import replace_start_and_end_slash as replace_start_and_end_slash
from ..datastore.core import allow_safe as allow_safe
from ..datastore.core import DatastoreInterface as DatastoreInterface
from ..datastore.core import ObjectStorage as ObjectStorage
from ..datastore.core import STORAGE_FORMATS as STORAGE_FORMATS
from ..datastore.core import warning_message as warning_message
from ..datastore.exceptions import DatastoreReadInitException as DatastoreReadInitException
from ..datastore.exceptions import DatastoreWriteInitException as DatastoreWriteInitException
from ..datastore.exceptions import DatastoreNotReadyException as DatastoreNotReadyException
from ..datastructures import CheckpointArtifact as CheckpointArtifact
from ..datastore.utils import safe_serialize as safe_serialize

DEFAULT_NAME: str

CHECKPOINTS_STORAGE_PREFIX: str

DEFAULT_STORAGE_FORMAT: str

ARTIFACT_STORE_NAME: str

METADATA_STORE_NAME: str

ARTIFACT_METADATA_STORE_NAME: str

class CheckpointsPathComponents(tuple, metaclass=type):
    """
    CheckpointsPathComponents(flow_name, step_name, run_id, task_id, scope, task_identifier, pathspec_hash, attempt, name, version_id, is_metadata, key_name, root_prefix)
    """
    @staticmethod
    def __new__(_cls, flow_name, step_name, run_id, task_id, scope, task_identifier, pathspec_hash, attempt, name, version_id, is_metadata, key_name, root_prefix):
        """
        Create new instance of CheckpointsPathComponents(flow_name, step_name, run_id, task_id, scope, task_identifier, pathspec_hash, attempt, name, version_id, is_metadata, key_name, root_prefix)
        """
        ...
    def __repr__(self):
        """
        Return a nicely formatted representation string
        """
        ...
    def __getnewargs__(self):
        """
        Return self as a plain tuple.  Used by copy and pickle.
        """
        ...
    ...

def decompose_key_artifact_metadata_store(key) -> CheckpointsPathComponents:
    ...

def decompose_key_artifact_store(key) -> CheckpointsPathComponents:
    """
    Convert Key into Path Components.
    PATH COMPONENTS: mf.checkpoints/artifacts/<flow_name>/<step_name>/<scope>/<task_identifier>/<pathspec_hash>.<attempt>.<name>.<version_id>
    """
    ...

def decompose_key_metadata_store(key) -> CheckpointsPathComponents:
    """
    Convert Key into Path Components.
    PATH COMPONENTS: mf.checkpoints/metadata/<flow_name>/<runid>/<stepname>/<taskid>/<pathspec_hash>.<attempt>.<name>.<version_id>.metadata
    """
    ...

class CheckpointDatastore(metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastore.core.DatastoreInterface, metaclass=type):
    """
    Consisits of 3 main components:
    - `artifact_store`: This is where the checkpoint artifacts are stored.
        - This key to the checkpoint in this store becomes the "key for the checkpoint"
    - `metadata_store`: This is where the metadata of the checkpoint is stored it based on the currently executing task (path structure resembles that of a metaflow pathspec).
        - This store helps retrieve information about all the checkpoints stored for a task during the execution.
    - `artifact_metadatastore`: This is similar to the metadata store but holds a pathstructure similar to the artifact store.
        - this store helps reverse lookup the Checkpoint metadata object from the checkpoint key.
    """
    @property
    def metadata_ready(self):
        ...
    @property
    def artifact_ready(self):
        ...
    def set_root_prefix(self, root_prefix):
        ...
    @classmethod
    def init_read_store(cls, storage_backend: metaflow.datastore.datastore_storage.DataStoreStorage, pathspec = None, checkpoint_key = None):
        """
        This will initialize the datastore for reading.
        
        - If there is only the pathspec that's provided then it can mean the user is doing a list operations
        - if only the checkpoint_key is provided then it can mean the user is trying to load a specific checkpoint
        """
        ...
    def create_key_name(self, *args):
        ...
    @classmethod
    def init_global_registry_write_store(cls, storage_backend: metaflow.datastore.datastore_storage.DataStoreStorage, pathspec, artifact_store_path_components):
        """
        The normal mode of operation ie (init_write_store) is a metaflow coupled mode of operation where we store the checkpoints based on metaflow based logic.
        """
        ...
    @classmethod
    def init_write_store(cls, storage_backend: metaflow.datastore.datastore_storage.DataStoreStorage, pathspec, scope, task_identifier):
        ...
    def save(self, local_path: str, attempt, version_id, name = 'mfchckpt', metadata = {}, set_latest = True, storage_format = 'files') -> metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact:
        ...
    def latest(*args, **kwargs):
        ...
    def load(self, local_path, version_id, attempt, name, storage_format = 'files'):
        ...
    def load_metadata(self, attempt, version_id, name = 'mfchckpt') -> dict:
        ...
    def list(self, name: typing.Union[str, None] = None, attempt: typing.Union[int, None] = None, within_task: typing.Union[bool, None] = True):
        ...
    def delete(self, checkpoint_artifact: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact) -> bool:
        """
        Delete a checkpoint from all stores.
        
        Deletion order:
        1. Delete artifact data (files/tarball)
        2. Delete artifact metadata
        3. Delete task metadata
        
        NOTE: This does NOT modify the 'latest' pointer in any store.
        
        Parameters
        ----------
        checkpoint_artifact : CheckpointArtifact
            The checkpoint artifact to delete.
        
        Returns
        -------
        bool
            True if all deletions were successful.
        
        Raises
        ------
        DatastoreNotReadyException
            If the datastore is not properly initialized for delete operations.
        """
        ...
    @classmethod
    def init_delete_store(cls, storage_backend: metaflow.datastore.datastore_storage.DataStoreStorage, checkpoint_artifact: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact):
        """
        Initialize datastore for delete operations from a checkpoint artifact.
        
        This creates a datastore instance with access to all three stores
        needed for complete checkpoint deletion.
        """
        ...
    @classmethod
    def decompose_key(cls, key) -> CheckpointsPathComponents:
        ...
    def __str__(self):
        ...
    def __init__(self, artifact_store: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastore.core.ObjectStorage, metadata_store: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastore.core.ObjectStorage, artifact_metadatastore: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastore.core.ObjectStorage):
        ...
    ...

