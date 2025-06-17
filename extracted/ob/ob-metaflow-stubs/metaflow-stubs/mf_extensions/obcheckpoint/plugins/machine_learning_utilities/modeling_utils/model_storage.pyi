######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.944086                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastore.core
    import metaflow.datastore.datastore_storage

from ..datastore.core import ObjectStorage as ObjectStorage
from ..datastore.core import DatastoreInterface as DatastoreInterface
from ..datastore.core import STORAGE_FORMATS as STORAGE_FORMATS
from .exceptions import ModelException as ModelException
from ..exceptions import KeyNotFoundError as KeyNotFoundError
from ..datastructures import ModelArtifact as ModelArtifact
from ..exceptions import KeyNotCompatibleWithObjectException as KeyNotCompatibleWithObjectException

MODELS_PEFFIX: str

ARTIFACT_STORE_NAME: str

METADATA_STORE_NAME: str

ARTIFACT_METADATA_STORE_NAME: str

class ModelPathComponents(tuple, metaclass=type):
    """
    ModelPathComponents(model_uuid, root_prefix)
    """
    @staticmethod
    def __new__(_cls, model_uuid, root_prefix):
        """
        Create new instance of ModelPathComponents(model_uuid, root_prefix)
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

def decompose_model_artifact_key(key):
    ...

class ModelDatastore(metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastore.core.DatastoreInterface, metaclass=type):
    def save(self, artifact: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.ModelArtifact, file_path, storage_format = 'tar'):
        ...
    def load_metadata(self, model_id):
        ...
    def save_metadata(self, attempt, model_id, metadata):
        ...
    def load(self, model_id, path):
        ...
    def list(self, *args, **kwargs):
        ...
    @classmethod
    def init_read_store(cls, storage_backend: metaflow.datastore.datastore_storage.DataStoreStorage, pathspec: typing.Optional[str] = None, attempt: typing.Optional[str] = None, model_key = None, *args, **kwargs):
        ...
    @classmethod
    def decompose_key(cls, key):
        ...
    @classmethod
    def init_write_store(cls, storage_backend: metaflow.datastore.datastore_storage.DataStoreStorage, pathspec: str, attempt, *args, **kwargs):
        ...
    def __init__(self, artifact_store: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastore.core.ObjectStorage, metadata_store: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastore.core.ObjectStorage, artifact_metadatastore: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastore.core.ObjectStorage):
        ...
    ...

