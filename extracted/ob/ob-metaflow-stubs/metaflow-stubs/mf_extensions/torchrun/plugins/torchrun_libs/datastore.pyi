######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.21.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-04-03T19:36:22.611226                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.torchrun.plugins.torchrun_libs.datastore

from .exceptions import DatastoreKeyNotFoundError as DatastoreKeyNotFoundError
from .exceptions import BarrierTimeoutException as BarrierTimeoutException

TORCHRUN_SUFFIX: str

class TorchrunDatastoreBlob(tuple, metaclass=type):
    """
    TorchrunDatastoreBlob(blob, url, text)
    """
    @staticmethod
    def __new__(_cls, blob, url, text):
        """
        Create new instance of TorchrunDatastoreBlob(blob, url, text)
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

class TorchrunListPathResult(tuple, metaclass=type):
    """
    TorchrunListPathResult(url,)
    """
    @staticmethod
    def __new__(_cls, url):
        """
        Create new instance of TorchrunListPathResult(url,)
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

class TorchrunDatastore(object, metaclass=type):
    """
    This class is a wrapper around the basic Metaflow cloud datastore functionality.
    It is used to interact with each cloud datastore provider from within the TorchrunExecutor and TorchrunDecorator class.
    For now, local storage is not supported.
    Methods provided follow the naming convention of Metaflow's S3 client: put, get, and list_paths.
    """
    def __init__(self, flow_datastore, pathspec = None):
        ...
    @property
    def get_storage_root(self):
        """
        Return the path to the root of the torchrun datastore.
        This method is where the unique torchrun datastore root for each cloud provider is specified.
        
        Note: S3Storage class uses the S3 client (other clouds do not have this),
            which prepends the storage root inside the self._backend calls this class uses.
        """
        ...
    def get_datastore_key_location(self):
        ...
    def get_datastore_file_location(self, key):
        ...
    def put(self, key: str, obj: typing.Union[str, bytes], overwrite: bool = False):
        """
        Put a single object into the datastore's `key` index.
        """
        ...
    def put_files(self, key_paths: typing.List[typing.Tuple[str, str]], overwrite = False):
        ...
    def get(self, key):
        """
        Get a single object residing in the datastore's `key` index.
        """
        ...
    def get_many(self, keys):
        ...
    def list_paths(self, keys):
        """
        List all objects in the datastore's `keys` index.
        """
        ...
    ...

def wait_for_key_data(datastore: TorchrunDatastore, keys: typing.List[str], max_wait_time: float = 600, frequency = 0.1) -> typing.Dict[str, metaflow.mf_extensions.torchrun.plugins.torchrun_libs.datastore.TorchrunDatastoreBlob]:
    """
    Wait for the keys to be available in the datastore.
    If the keys are not available after `max_wait_time` seconds, raise an error.
    """
    ...

def task_sync_barrier(barrier_name, datastore: TorchrunDatastore, keys: typing.List[str], max_wait_time = 600, frequency = 0.1, description = None):
    """
    A context manager that waits for keys to be written to the datastore and acts like a distributed-barrier.
    When multiple tasks are running in parallel, this context manager can be used to ensure that all tasks
    can wait on a certain keys to be written to the datastore. If the keys are not written to the datastore
    after `max_wait_time` seconds, a `BarrierTimeoutException` error is raised. This way only once all the keys
    are written to the datastore, the tasks will proceed. This context manager is used to ensure that all tasks
    are in sync before proceeding to the next step.
    
    Args:
        barrier_name (str): The name of the barrier. Used for debugging purposes.
        datastore (TorchrunDatastore)
        keys (List[str]): The keys to wait for in the datastore.
        max_wait_time (float): The maximum time to wait for the keys to be written to the datastore.
        frequency (float): The frequency to check the datastore for the keys.
        description (str): A description of the barrier. Used for debugging purposes.
    """
    ...

