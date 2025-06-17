######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.906683                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception
    import metaflow.datastore.content_addressed_store

from ..exception import MetaflowException as MetaflowException

CLIENT_CACHE_PATH: str

CLIENT_CACHE_MAX_SIZE: int

CLIENT_CACHE_MAX_FLOWDATASTORE_COUNT: int

CLIENT_CACHE_MAX_TASKDATASTORE_COUNT: int

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
    ...

class FileBlobCache(metaflow.datastore.content_addressed_store.BlobCache, metaclass=type):
    def __init__(self, filecache, cache_id):
        ...
    def load_key(self, key):
        ...
    def store_key(self, key, blob):
        ...
    ...

