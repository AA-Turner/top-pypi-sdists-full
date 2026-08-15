######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.34.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-08-14T20:17:07.914513                                                            #
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
    @classmethod
    def delete(cls, data, storage_backend) -> bool:
        """
        Delete an artifact (checkpoint or model) from storage.
        
        Parameters
        ----------
        data : Union[dict, MetaflowDataArtifactReference]
            The artifact reference to delete.
        storage_backend : DataStoreStorage
            The storage backend to use.
        
        Returns
        -------
        bool
            True if deletion was successful.
        """
        ...
    @classmethod
    def delete_from_key(cls, key: str, storage_backend) -> bool:
        """
        Delete an artifact by its key string.
        
        The key pattern is used to determine whether this is a
        checkpoint or model, then the appropriate delete method is called.
        
        Parameters
        ----------
        key : str
            The artifact key string.
        storage_backend : DataStoreStorage
            The storage backend to use.
        
        Returns
        -------
        bool
            True if deletion was successful.
        
        Raises
        ------
        KeyNotCompatibleException
            If the key doesn't match any supported artifact type.
        """
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

def delete_model(reference: typing.Union[str, metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.MetaflowDataArtifactReference, dict]) -> bool:
    """
    Delete a model or checkpoint from Metaflow's datastore.
    
    This function deletes artifacts that were previously saved using
    `@model`, `@checkpoint`, or `@huggingface_hub` decorators.
    
    The deletion removes:
    1. The actual artifact data (files or tarball)
    2. The artifact metadata
    3. The task metadata (when accessible)
    
    NOTE: This does NOT modify any 'latest' pointers. If you delete the
    checkpoint that 'latest' points to, the pointer will become stale.
    
    Parameters
    ----------
    reference : Union[str, MetaflowDataArtifactReference, dict]
        The reference to the artifact to delete. This can be:
        - A string key (e.g., "mf.checkpoints/checkpoints/artifacts/...")
        - A MetaflowDataArtifactReference object (CheckpointArtifact or ModelArtifact)
        - A dictionary artifact reference (e.g., from self.my_checkpoint)
    
    Returns
    -------
    bool
        True if deletion was successful, False if any component failed to delete.
    
    Raises
    ------
    ValueError
        If reference is None.
    KeyNotCompatibleException
        If the reference key doesn't match any supported artifact type.
    
    Examples
    --------
    **Delete using a dictionary reference:**
    
    ```python
    from metaflow import FlowSpec, step, delete_model
    
    class MyFlow(FlowSpec):
        @step
        def cleanup(self):
            # Delete a checkpoint saved in a previous step
            delete_model(self.old_checkpoint)
            self.next(self.end)
    ```
    
    **Delete using a key string:**
    
    ```python
    from metaflow import delete_model
    
    # Delete by key
    delete_model("mf.checkpoints/checkpoints/artifacts/MyFlow/train/abc123/...")
    ```
    
    **Delete from a notebook/script:**
    
    ```python
    from metaflow import Run, delete_model
    
    run = Run("MyFlow/123")
    checkpoint_ref = run["train"].task.data.my_checkpoint
    delete_model(checkpoint_ref)
    ```
    """
    ...

