######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.942887                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.datastore.datastore_storage
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastore.core

from ......exception import MetaflowException as MetaflowException
from ..utils.tar_utils import create_tarball_on_disk as create_tarball_on_disk
from ..utils.tar_utils import extract_tarball as extract_tarball
from ..utils.general import safe_serialize as safe_serialize
from ..exceptions import KeyNotFoundError as KeyNotFoundError

STORAGE_INJECTIONS_SINGLE_FILE_SAVE: dict

STORAGE_INJECTIONS_MULTIPLE_FILE_SAVE: dict

STORAGE_INJECTIONS_LOAD_FILES: dict

class DatastoreBlob(tuple, metaclass=type):
    """
    DatastoreBlob(blob, url, path)
    """
    @staticmethod
    def __new__(_cls, blob, url, path):
        """
        Create new instance of DatastoreBlob(blob, url, path)
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

class ListPathResult(tuple, metaclass=type):
    """
    ListPathResult(full_url, key)
    """
    @staticmethod
    def __new__(_cls, full_url, key):
        """
        Create new instance of ListPathResult(full_url, key)
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

COMPRESSION_METHOD: None

COMPATIBLE_BACKENDS: list

class STORAGE_FORMATS(object, metaclass=type):
    ...

def warning_message(message, logger = None, ts = False, prefix = '[@checkpoint][artifact-store]'):
    ...

def allow_safe(func):
    ...

class ObjectStorage(object, metaclass=type):
    """
    `ObjectStorage` wraps around the DataStoreStorage object and provides the lower level
    storage APIs needed by the subsequent classes. This datastore's main function that
    distingushes it from the DataStoreStorage object is that it manages a generalizable
    path structure over different storage backends (s3, azure, gs, local etc.).
    
    This object will be used to create multiple "Logical" datastores for constructs like
    `Checkpoints`, `Models` etc.
    
    Usage
    -----
    ```
    storage = ObjectStorage(
        storage_backend,
        root_prefix = "mf.checkpoints",
        path_components = ["artifacts", "MyFlow", "step_a", "cd2312rd12d", "x5avasdhtsdfqw"]
    )
    ```
    """
    def __init__(self, storage_backend: metaflow.datastore.datastore_storage.DataStoreStorage, root_prefix: str, path_components: typing.List):
        ...
    @property
    def path_components(self):
        ...
    def set_full_prefix(self, root_prefix):
        ...
    def full_base_url(self, prefix = None):
        ...
    def create_key_name(self, *args):
        ...
    @property
    def datastore_root(self):
        ...
    def resolve_key_relative_path(self, key):
        ...
    def resolve_key_full_url(self, key):
        ...
    def resolve_key_path(self, key):
        ...
    def put(self, key: str, obj: typing.Union[str, bytes], overwrite: bool = False) -> str:
        """
        TODO : [THIS IS TERRIBLY INEFFICIENT]
        """
        ...
    def put_file(self, key: str, path: str, overwrite = False):
        ...
    def put_files(self, key_paths: typing.List[typing.Tuple[str, str]], overwrite = False):
        ...
    def get(self, key) -> DatastoreBlob:
        """
        TODO : [THIS IS TERRIBLY INEFFICIENT]
        """
        ...
    def get_file(self, key):
        ...
    def list_paths(self, keys, recursive = False) -> typing.Iterator[metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastore.core.ListPathResult]:
        """
        List all objects in the datastore's `keys` index.
        """
        ...
    def __str__(self) -> str:
        ...
    ...

class DatastoreInterface(object, metaclass=type):
    """
    This is the root abstraction used by any underlying datastores like Checkpoint/Model etc.
    to create the saving/loading mechanics using multiple ObjectStores.
    
    The inherited classes require the following implemented:
        - `ROOT_PREFIX` : The root prefix for the datastore such as `mf.checkpoints` or `mf.models`.
        - `init_read_store` : The method to initialize the read store; The inheriting class can compose together any number of `BaseDatastore` objects
        - `init_write_store` : The method to initialize the write store; The inheriting class can compose together any number of `BaseDatastore` objects
        - `save` : The method to save the artifact data.
        - `load` : The method to load the artifact data.
        - `save_metadata` : The method to save the metadata about the artifact.
        - `load_metadata` : The method to load the metadata about the artifact.
        - `list` : The method to list all the artifacts.
    """
    def set_root_prefix(self, root_prefix):
        """
        This function helps ensuring that the root prefix of the datastore
        and it's underlying ObjectStores can change trivially.
        """
        ...
    def save(self, *args, **kwargs):
        ...
    def load(self, *args, **kwargs):
        ...
    def save_metadata(self, *args, **kwargs):
        ...
    def load_metadata(self, *args, **kwargs):
        ...
    def list(self, *args, **kwargs):
        ...
    @classmethod
    def init_read_store(cls, storage_backend: metaflow.datastore.datastore_storage.DataStoreStorage, *args, **kwargs):
        ...
    @classmethod
    def init_write_store(cls, storage_backend: metaflow.datastore.datastore_storage.DataStoreStorage, *args, **kwargs):
        ...
    ...

