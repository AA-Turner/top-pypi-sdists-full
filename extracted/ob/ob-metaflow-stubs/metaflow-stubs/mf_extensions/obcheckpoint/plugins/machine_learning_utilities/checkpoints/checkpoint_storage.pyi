######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:03.002445                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.datastore.datastore_storage
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastore.core
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.checkpoints.checkpoint_storage
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures

from ..exceptions import KeyNotCompatibleWithObjectException as KeyNotCompatibleWithObjectException
from ..utils.identity_utils import pathspec_hash as pathspec_hash
from ..utils.general import replace_start_and_end_slash as replace_start_and_end_slash
from ..datastore.core import allow_safe as allow_safe
from ..datastore.core import DatastoreInterface as DatastoreInterface
from ..datastore.core import ObjectStorage as ObjectStorage
from ..datastore.core import STORAGE_FORMATS as STORAGE_FORMATS
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
    CheckpointsPathComponents(flow_name, step_name, scope, task_identifier, pathspec_hash, attempt, name, version_id, is_metadata, key_name, root_prefix)
    """
    @staticmethod
    def __new__(_cls, flow_name, step_name, scope, task_identifier, pathspec_hash, attempt, name, version_id, is_metadata, key_name, root_prefix):
        """
        Create new instance of CheckpointsPathComponents(flow_name, step_name, scope, task_identifier, pathspec_hash, attempt, name, version_id, is_metadata, key_name, root_prefix)
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
    PATH COMPONENTS: mf.checkpoints/artifacts/<flow_name>/<step_name>/<scope>/<task_identifier>/<pathspec_hash>.<attempt>.<name>.<version_id>
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
    def list(self, name: typing.Optional[str] = None, attempt: typing.Optional[int] = None, within_task: typing.Optional[bool] = True):
        ...
    @classmethod
    def decompose_key(cls, key) -> CheckpointsPathComponents:
        ...
    def __str__(self):
        ...
    def __init__(self, artifact_store: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastore.core.ObjectStorage, metadata_store: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastore.core.ObjectStorage, artifact_metadatastore: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastore.core.ObjectStorage):
        ...
    ...

