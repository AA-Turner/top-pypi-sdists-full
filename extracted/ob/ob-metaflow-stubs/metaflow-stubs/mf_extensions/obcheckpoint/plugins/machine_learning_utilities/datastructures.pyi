######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.526029                                                            #
######################################################################################################

from __future__ import annotations

import typing
import metaflow
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures

from .exceptions import KeyNotCompatibleWithObjectException as KeyNotCompatibleWithObjectException
from .exceptions import KeyNotCompatibleException as KeyNotCompatibleException
from .exceptions import IncompatibleObjectTypeException as IncompatibleObjectTypeException
from .datastore.task_utils import init_datastorage_object as init_datastorage_object

class MetaflowDataArtifactReference(object, metaclass=type):
    @property
    def size(self):
        ...
    @property
    def url(self):
        ...
    @property
    def key(self):
        ...
    @property
    def pathspec(self):
        ...
    @property
    def attempt(self):
        ...
    @property
    def created_on(self):
        ...
    @property
    def metadata(self):
        ...
    def __init__(self, **kwargs):
        ...
    def validate(self, data):
        ...
    @classmethod
    def from_dict(cls, data) -> typing.Union["ModelArtifact", "CheckpointArtifact"]:
        ...
    @classmethod
    def hydrate(cls, data: typing.Union["ModelArtifact", "CheckpointArtifact", dict]):
        ...
    def to_dict(self):
        ...
    ...

class ModelArtifact(MetaflowDataArtifactReference, metaclass=type):
    def __init__(self, **kwargs):
        ...
    @property
    def blob(self):
        ...
    @property
    def uuid(self):
        ...
    @property
    def serializer(self):
        ...
    @property
    def source(self):
        ...
    @property
    def storage_format(self):
        ...
    @classmethod
    def create(cls, pathspec = None, attempt = None, key = None, url = None, model_uuid = None, metadata = None, storage_format = None, source = None, serializer = None, label = None):
        ...
    ...

class CheckpointArtifact(MetaflowDataArtifactReference, metaclass=type):
    @property
    def storage_format(self):
        ...
    @property
    def version_id(self):
        ...
    @property
    def name(self):
        ...
    def __init__(self, **kwargs):
        ...
    ...

class Factory(object, metaclass=type):
    @classmethod
    def hydrate(cls, data):
        ...
    @classmethod
    def from_dict(cls, data):
        ...
    @classmethod
    def load(cls, data, local_path, storage_backend):
        ...
    @classmethod
    def object_type_from_key(cls, reference_key):
        ...
    @classmethod
    def load_from_key(cls, key_object, local_path, storage_backend):
        ...
    @classmethod
    def load_metadata_from_key(cls, key_object, storage_backend) -> typing.Union[metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact, metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.ModelArtifact]:
        ...
    ...

def load_model(reference: typing.Union[str, metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.MetaflowDataArtifactReference, dict], path: str):
    """
    Load a model or checkpoint from Metaflow's datastore to a local path.
    
    This function provides a convenient way to load models and checkpoints that were previously saved using `@model`, `@checkpoint`, or `@huggingface_hub` decorators, either from within a Metaflow task or externally using the Run API.
    
    Parameters
    ----------
    reference : Union[str, MetaflowDataArtifactReference, dict]
        The reference to the model/checkpoint to load. This can be A string key (e.g., "model/my_model_abc123") OR A MetaflowDataArtifactReference object OR a dictionary artifact reference (e.g., self.my_model from a previous step)
    path : str
        The local filesystem path where the model/checkpoint should be loaded. The directory will be created if it doesn't exist.
    
    Raises
    ------
    ValueError
        If reference or path is None
    KeyNotCompatibleException
        If the reference key is not compatible with supported artifact types
    
    Examples
    --------
    **Loading within a Metaflow task:**
    
    ```python
    from metaflow import FlowSpec, step
    
    
    class MyFlow(FlowSpec):
        @model
        @step
        def train(self):
            # Save a model
            self.my_model = current.model.save(
                "/path/to/trained/model",
                label="trained_model"
            )
            self.next(self.evaluate)
    
        @step
        def evaluate(self):
            from metaflow import load_model
            # Load the model using the artifact reference
            load_model(self.my_model, "/tmp/loaded_model")
            # Model is now available at /tmp/loaded_model
            self.next(self.end)
    ```
    
    **Loading externally using Metaflow's Run API:**
    
    ```python
    from metaflow import Run
    from metaflow import load_model
    
    # Get a reference to a completed run
    run = Run("MyFlow/123")
    
    # Load using artifact reference from a step
    task_model_ref = run["train"].task.data.my_model
    load_model(task_model_ref, "/local/path/to/model")
    
    model_ref = run.data.my_model
    load_model(model_ref, "/local/path/to/model")
    ```
    
    **Loading HuggingFace models:**
    
    ```python
    # If you saved a HuggingFace model reference
    @huggingface_hub
    @step
    def download_hf_model(self):
        self.hf_model = current.huggingface_hub.snapshot_download(
            repo_id="mistralai/Mistral-7B-Instruct-v0.1"
        )
        self.next(self.use_model)
    
    @step
    def use_model(self):
        from metaflow import load_model
        # Load the HuggingFace model
        load_model(self.hf_model, "/tmp/mistral_model")
        # Model files are now available at /tmp/mistral_model
    ```
    """
    ...

