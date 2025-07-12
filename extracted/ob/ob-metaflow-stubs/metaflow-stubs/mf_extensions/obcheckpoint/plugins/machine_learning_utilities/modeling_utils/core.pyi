######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.557431                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.modeling_utils.model_storage
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.modeling_utils.core

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
    This property helps manage all the models loaded via `@model(load=...)` decorator and `current.model.load` method.
    
    It is a dictionary like object that stores the loaded models in a temporary directory. The keys of the dictionary are the artifact names and the values are the paths to the temporary directories where the models are stored.
    
    Examples
    --------
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
        """
        Returns metadata information about all loaded models.
        
        This property provides access to the metadata of models that have been loaded
        via the `@model(load=...)` decorator or `current.model.load` method. The metadata
        includes information such as model type, creation time, size, storage format,
        and any custom metadata that was saved with the model. For example setting
        `@model(load=["my_model"])` will allow accessing it's metadata during flow runtime
        using `current.model.loaded.info["my_model"]`
        """
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
        """
        Save a model to the datastore.
        
        Parameters
        ----------
        path : str or os.PathLike
            The path to the model file or directory to save. If a directory path is provided,
            all contents within that directory will be saved. If a file path is provided,
            the file will be directly saved to the datastore.
        label : str, optional
            A label to identify the saved model. If not provided, a default label based on
            the flow and step name will be used.
        metadata : dict, optional
            Additional metadata to store with the model. Default is None.
        storage_format : str, optional
            The storage format for the model. Must be one of STORAGE_FORMATS.TAR or
            STORAGE_FORMATS.FILES. Default is STORAGE_FORMATS.TAR.
        
        Returns
        -------
        dict
            A dictionary representation of the saved model artifact containing metadata
            and reference information.
        
        Raises
        ------
        ValueError
            If an unsupported storage format is provided.
        """
        ...
    def load(self, reference: typing.Union[str, metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.MetaflowDataArtifactReference, dict], path: typing.Optional[str] = None):
        """
        Load a model/checkpoint from the datastore to a temporary directory or a specified path.
        
        Returns
        -------
        str : The path to the temporary directory where the model is loaded.
        """
        ...
    ...

