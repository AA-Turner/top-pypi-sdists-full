######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.21                                                                                #
# Generated on 2026-03-12T01:00:36.721097                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import abc
import typing
if typing.TYPE_CHECKING:
    import abc
    import metaflow.datastore.flow_datastore
    import metaflow.datastore.content_addressed_store
    import metaflow.exception

from ..exception import MetaflowException as MetaflowException

CLIENT_CACHE_PATH: str

CLIENT_CACHE_MAX_SIZE: int

CLIENT_CACHE_MAX_FLOWDATASTORE_COUNT: int

DATASTORES: list

NEW_FILE_QUARANTINE: int

def od_move_to_end(od, key):
    ...

class FileCacheException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class FileCache(object, metaclass=type):
    def __init__(self, cache_dir = None, max_size = None):
        ...
    @property
    def cache_dir(self):
        ...
    def get_logs_stream(self, ds_type, ds_root, stream, attempt, flow_name, run_id, step_name, task_id):
        ...
    def get_log_legacy(self, ds_type, location, logtype, attempt, flow_name, run_id, step_name, task_id):
        ...
    def get_legacy_log_size(self, ds_type, location, logtype, attempt, flow_name, run_id, step_name, task_id):
        ...
    def get_log_size(self, ds_type, ds_root, logtype, attempt, flow_name, run_id, step_name, task_id):
        ...
    def get_data(self, ds_type, flow_name, location, key):
        ...
    def get_artifact_size_by_location(self, ds_type, location, attempt, flow_name, run_id, step_name, task_id, name):
        """
        Gets the size of the artifact content (in bytes) for the name at the location
        """
        ...
    def get_artifact_size(self, ds_type, ds_root, attempt, flow_name, run_id, step_name, task_id, name):
        """
        Gets the size of the artifact content (in bytes) for the name
        """
        ...
    def get_artifact_by_location(self, ds_type, location, data_metadata, flow_name, run_id, step_name, task_id, name):
        ...
    def get_artifact(self, ds_type, ds_root, data_metadata, flow_name, run_id, step_name, task_id, name):
        ...
    def get_all_artifacts(self, ds_type, ds_root, data_metadata, flow_name, run_id, step_name, task_id):
        ...
    def get_artifacts(self, ds_type, ds_root, data_metadata, flow_name, run_id, step_name, task_id, names):
        ...
    def create_file(self, path, value):
        ...
    def read_file(self, path):
        ...
    @staticmethod
    def flow_ds_id(ds_type, ds_root, flow_name):
        ...
    @staticmethod
    def task_ds_id(ds_type, ds_root, flow_name, run_id, step_name, task_id, attempt):
        ...
    ...

class TaskMetadataCache(metaflow.datastore.flow_datastore.MetadataCache, metaclass=abc.ABCMeta):
    def __init__(self, filecache, ds_type, ds_root, flow_name):
        ...
    def load_metadata(self, run_id, step_name, task_id, attempt):
        ...
    def store_metadata(self, run_id, step_name, task_id, attempt, metadata_dict):
        ...
    ...

class FileBlobCache(metaflow.datastore.content_addressed_store.BlobCache, metaclass=type):
    def __init__(self, filecache, cache_id):
        ...
    def load_key(self, key):
        ...
    def store_key(self, key, blob):
        ...
    ...

