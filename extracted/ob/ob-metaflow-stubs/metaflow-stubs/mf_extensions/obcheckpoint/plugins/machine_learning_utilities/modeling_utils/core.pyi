######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.911522                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.modeling_utils.model_storage
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.modeling_utils.core
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures

from ..datastore.core import STORAGE_FORMATS as STORAGE_FORMATS
from ..exceptions import KeyNotFoundError as KeyNotFoundError
from ..exceptions import KeyNotCompatibleException as KeyNotCompatibleException
from ..exceptions import IncompatibleObjectTypeException as IncompatibleObjectTypeException
from .model_storage import ModelDatastore as ModelDatastore
from .exceptions import LoadingException as LoadingException
from ..datastore.utils import safe_serialize as safe_serialize
from ..utils.general import get_path_size as get_path_size
from ..utils.general import unit_convert as unit_convert
from ..utils.general import warning_message as warning_message
from ..utils.identity_utils import safe_hash as safe_hash
from ..utils.serialization_handler.tar import TarHandler as TarHandler
from ..datastructures import ModelArtifact as ModelArtifact
from ..datastructures import Factory as Factory
from ..datastructures import MetaflowDataArtifactReference as MetaflowDataArtifactReference

MAX_HASH_LEN: int

SERIALIZATION_HANDLERS: dict

OBJECT_MAX_SIZE_ALLOWED_FOR_ARTIFACT: int

def create_write_store(pathspec, attempt, storage_backend) -> metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.modeling_utils.model_storage.ModelDatastore:
    ...

def create_read_store(storage_backend, model_key = None, pathspec = None, attempt = None) -> metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.modeling_utils.model_storage.ModelDatastore:
    ...

class LoadedModels(object, metaclass=type):
    """
    A class that loads models from the datastore and stores them in a temporary directory.
    This class helps manage all the models loaded via `@model(load=...)` decorator and
    `current.model.load` method.
    
    It is exposed via the `current.model.loaded` property. It is a dictionary like object
    that stores the loaded models in a temporary directory. The keys of the dictionary are the
    artifact names and the values are the paths to the temporary directories where the models are stored.
    
    Usage:
    ------
    ```python
        @model(load=["model_key", "chckpt_key"])
        @step
        def mid_step(self):
            import os
            os.listdir(current.model.loaded["model_key"])
            os.listdir(current.model.loaded["chckpt_key"])
    ```
    """
    def __init__(self, storage_backend, flow, artifact_references: typing.Union[typing.List[str], typing.List[typing.Tuple[str, typing.Optional[str]]], str], best_effort = False, temp_dir_root = None, mode = 'eager', logger = None):
        ...
    @property
    def info(self):
        ...
    def __getitem__(self, key):
        ...
    def __contains__(self, key):
        ...
    def __iter__(self):
        ...
    def __len__(self):
        ...
    def cleanup(self, artifact_name):
        ...
    ...

class ModelSerializer(object, metaclass=type):
    def __init__(self, pathspec, attempt, storage_backend):
        ...
    @property
    def loaded(self) -> LoadedModels:
        ...
    def save(self, path, label = None, metadata = None, storage_format = 'tar'):
        ...
    def load(self, reference: typing.Union[str, metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.MetaflowDataArtifactReference, dict], path: typing.Optional[str] = None):
        """
        Load a model/checkpoint from the datastore to a temporary directory or a specified path.
        
        Returns:
        --------
        str : The path to the temporary directory where the model is loaded.
        """
        ...
    ...

