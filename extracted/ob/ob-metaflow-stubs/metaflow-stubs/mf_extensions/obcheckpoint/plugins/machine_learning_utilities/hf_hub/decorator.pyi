######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.910557                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.hf_hub.decorator
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.checkpoints.decorator

from ..checkpoints.decorator import CheckpointDecorator as CheckpointDecorator
from ..checkpoints.decorator import CurrentCheckpointer as CurrentCheckpointer
from ..checkpoints.decorator import warning_message as warning_message
from ......metadata_provider.metadata import MetaDatum as MetaDatum

HUGGINGFACE_HUB_ROOT_PREFIX: str

def get_tqdm_class():
    ...

def show_progress():
    ...

def download_model_from_huggingface(**kwargs):
    ...

class HuggingfaceRegistry(object, metaclass=type):
    """
    This object provides syntactic sugar
    over [huggingface_hub](https://github.com/huggingface/huggingface_hub)'s
    [snapshot_download](https://huggingface.co/docs/huggingface_hub/main/en/package_reference/file_download#huggingface_hub.snapshot_download) function.
    The `current.huggingface_hub.snapshot_download` function downloads objects from huggingface hub and saves them to the Metaflow's datastore under the
    `<repo_type>/<repo_id>` name. The `repo_type` is by default `model` and can be overriden by passing the `repo_type` parameter to the `snapshot_download` function.
    """
    def __init__(self, logger):
        ...
    @property
    def loaded(self):
        ...
    def snapshot_download(self, **kwargs) -> dict:
        """
        Downloads a model from huggingface hub and cache's it to the Metaflow's datastore.
        It passes down all the parameters to the `huggingface_hub.snapshot_download` function.
        
        Returns
        -------
        dict
            A reference to the artifact that was saved/retrieved from the Metaflow's datastore.
        """
        ...
    ...

class HuggingfaceLoadedModels(object, metaclass=type):
    """
    Manages loaded Hugging Face models and provides access to their local paths.
    
    This class is accessed through `current.huggingface_hub.loaded` and provides a dictionary-like
    interface to access the local paths of the huggingface repos specified in the `load` argument of the `@huggingface_hub` decorator.
    
    Usage:
    ------
    ```python
    # Basic loading and access
    @huggingface_hub(load=["mistralai/Mistral-7B-Instruct-v0.1"])
    @step
    def my_step(self):
        # Access the local path of a loaded model
        model_path = current.huggingface_hub.loaded["mistralai/Mistral-7B-Instruct-v0.1"]
    
        # Check if a model is loaded
        if "mistralai/Mistral-7B-Instruct-v0.1" in current.huggingface_hub.loaded:
            print("Model is loaded!")
    
    # Custom path and advanced loading
    @huggingface_hub(load=[
        ("mistralai/Mistral-7B-Instruct-v0.1", "/custom/path"),  # Specify custom path
        {
            "repo_id": "org/model-name",
            "force_download": True,  # Force fresh download
            "repo_type": "dataset"   # Load dataset instead of model
        }
    ])
    @step
    def another_step(self):
        # Models are available at specified paths
        pass
    ```
    """
    def __init__(self, checkpointer: HuggingfaceRegistry, logger, temp_dir_root = None):
        ...
    def __getitem__(self, key):
        ...
    def __contains__(self, key):
        ...
    @property
    def info(self):
        ...
    def cleanup(self):
        ...
    ...

class HuggingfaceHubDecorator(metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.checkpoints.decorator.CheckpointDecorator, metaclass=type):
    """
    Decorator that helps cache, version and store models/datasets from huggingface hub.
    
    Parameters
    ----------
    temp_dir_root : str, optional
        The root directory that will hold the temporary directory where objects will be downloaded.
    
    load: Union[List[str], List[Tuple[Dict, str]], List[Tuple[str, str]], List[Dict], None]
        The list of repos (models/datasets) to load.
    
        Loaded repos can be accessed via `current.huggingface_hub.loaded`. If load is set, then the following happens:
    
        - If repo (model/dataset) is not found in the datastore:
            - Downloads the repo from Hugging Face Hub to a temporary directory (or uses specified path) for local access
            - Stores it in Metaflow's datastore (s3/gcs/azure etc.) with a unique name based on repo_type/repo_id
                - All HF models loaded for a `@step` will be cached separately under flow/step/namespace.
    
        - If repo is found in the datastore:
            - Loads it directly from datastore to local path (can be temporary directory or specified path)
    
    
    MF Add To Current
    -----------------
    huggingface_hub -> metaflow_extensions.obcheckpoint.plugins.machine_learning_utilities.hf_hub.decorator.HuggingfaceRegistry
        The `@huggingface_hub` injects a `huggingface_hub` object into the `current` object. This object provides syntactic sugar
        over [huggingface_hub](https://github.com/huggingface/huggingface_hub)'s
        [snapshot_download](https://huggingface.co/docs/huggingface_hub/main/en/package_reference/file_download#huggingface_hub.snapshot_download) function.
        The `current.huggingface_hub.snapshot_download` function downloads objects from huggingface hub and saves them to the Metaflow's datastore under the
        `<repo_type>/<repo_id>` name. The `repo_type` is by default `model` and can be overriden by passing the `repo_type` parameter to the `snapshot_download` function.
    
    
        Usage:
        ------
    
        **Usage: creating references of models from huggingface that may be loaded in downstream steps**
        ```python
            @huggingface_hub
            @step
            def pull_model_from_huggingface(self):
                # `current.huggingface_hub.snapshot_download` downloads the model from the Hugging Face Hub
                # and saves it in the backend storage based on the model's `repo_id`. If there exists a model
                # with the same `repo_id` in the backend storage, it will not download the model again. The return
                # value of the function is a reference to the model in the backend storage.
                # This reference can be used to load the model in the subsequent steps via `@model(load=["llama_model"])`
    
                self.model_id = "mistralai/Mistral-7B-Instruct-v0.1"
                self.llama_model = current.huggingface_hub.snapshot_download(
                    repo_id=self.model_id,
                    allow_patterns=["*.safetensors", "*.json", "tokenizer.*"],
                )
                self.next(self.train)
        ```
    
        **Usage: loading models directly from huggingface hub or from cache (from metaflow's datastore)**
        ```python
            @huggingface_hub(load=["mistralai/Mistral-7B-Instruct-v0.1"])
            @step
            def pull_model_from_huggingface(self):
                path_to_model = current.huggingface_hub.loaded["mistralai/Mistral-7B-Instruct-v0.1"]
        ```
    
        ```python
            @huggingface_hub(load=[("mistralai/Mistral-7B-Instruct-v0.1", "/my-directory"), ("myorg/mistral-lora, "/my-lora-directory")])
            @step
            def finetune_model(self):
                path_to_model = current.huggingface_hub.loaded["mistralai/Mistral-7B-Instruct-v0.1"]
                # path_to_model will be /my-directory
        ```
    
        ```python
            # Takes all the arguments passed to `snapshot_download`
            # except for `local_dir`
            @huggingface_hub(load=[
                {
                    "repo_id": "mistralai/Mistral-7B-Instruct-v0.1",
                },
                {
                    "repo_id": "myorg/mistral-lora",
                    "repo_type": "model",
                },
            ])
            @step
            def finetune_model(self):
                path_to_model = current.huggingface_hub.loaded["mistralai/Mistral-7B-Instruct-v0.1"]
                # path_to_model will be /my-directory
        ```
    """
    def step_init(self, flow, graph, step_name, decorators, environment, flow_datastore, logger):
        ...
    def task_pre_step(self, step_name, task_datastore, metadata, run_id, task_id, flow, graph, retry_count, max_user_code_retries, ubf_context, inputs):
        ...
    def task_decorate(self, step_func, flow, graph, retry_count, max_user_code_retries, ubf_context):
        ...
    def task_post_step(self, step_name, flow, graph, retry_count, max_user_code_retries):
        ...
    def task_exception(self, exception, step_name, flow, graph, retry_count, max_user_code_retries):
        ...
    ...

