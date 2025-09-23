######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.7.5+obcheckpoint(0.2.7);ob(v1)                                                    #
# Generated on 2025-09-23T01:34:30.722272                                                            #
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
    This object provides a thin, Metaflow-friendly layer over huggingface_hub's [snapshot_download](https://huggingface.co/docs/huggingface_hub/main/en/package_reference/file_download#huggingface_hub.snapshot_download):
    
    - Snapshot references (persist-and-reuse): Use `current.huggingface_hub.snapshot_download(repo_id=..., ...)` to ensure a repo is available in the Metaflow datastore. If absent, it is downloaded once and saved; the call returns a reference dict you can store and load later (for example via `@model`).
    
    - On-demand local access (context manager):  Use `current.huggingface_hub.load(repo_id=..., [path=...], ...)` as a context manager to obtain a local filesystem path for immediate use. If the repo exists in the datastore, it is loaded from there; otherwise it is fetched from the Hugging Face Hub and then cached in the datastore. When `path` is omitted, a temporary directory is created and cleaned up automatically when the context exits. When `path` is provided, files are placed there and are not cleaned up by the context manager.
    
    Repos are cached in the datastore using the huggingface_hub.snapshot_download's arguments. The cache
    key may include: `repo_id`, `repo_type`, `revision`, `ignore_patterns`,
    and `allow_patterns` (see `cache_scope` for how keys are scoped).
    
    Examples
    --------
    ```python
    # Snapshot reference:
    ref = current.huggingface_hub.snapshot_download(
        repo_id="google-bert/bert-base-uncased",
        allow_patterns=["*.json"]
    )
    # Explicit Model Loading with Context manager:
    
    with current.huggingface_hub.load(
        repo_id="google-bert/bert-base-uncased",
        allow_patterns=["*.json"]
    ) as local_path:
        my_model = torch.load(os.path.join(local_path, "model.bin"))
    ```
    """
    def __init__(self, logger):
        ...
    @property
    def loaded(self) -> HuggingfaceLoadedModels:
        """
        This property provides a dictionary-like interface to access the local paths of the huggingface repos specified in the `load` argument of the `@huggingface_hub` decorator.
        """
        ...
    def snapshot_download(self, **kwargs) -> dict:
        """
        Downloads a model from the Hugging Face Hub and caches it in the Metaflow datastore.
        It passes all parameters to the `huggingface_hub.snapshot_download` function.
        
        Returns
        -------
        dict
            A reference to the artifact saved to or retrieved from the Metaflow datastore.
        """
        ...
    def load(self, repo_id = None, path = None, repo_type = 'model', **kwargs):
        """
        Context manager to load a Hugging Face repo (model/dataset) to a local path.
        
        - If `path` is provided, the repo is loaded there and the same path is yielded.
        - If `path` is not provided, a temporary directory is created, the repo is
          loaded there, the path is yielded, and the directory is cleaned up when
          the context exits.
        
        Parameters
        ----------
        repo_id : str, optional
            The Hugging Face repo ID. If omitted, must be provided via kwargs["repo_id"].
        path : str, optional
            Target directory to place files. If None, a temp directory is created.
        repo_type : str, optional
            Repo type (e.g., "model", "dataset"). Defaults to "model".
        **kwargs : Any
            Additional args forwarded to snapshot_download (e.g. force_download, revision,
            allow_patterns, ignore_patterns, etc.).
        
        Yields
        ------
        str
            Local filesystem path where the repo is available.
        """
        ...
    ...

class HuggingfaceLoadedModels(object, metaclass=type):
    """
    Manages loaded HuggingFace models/datasets and provides access to their local paths.
    
    `current.huggingface_hub.loaded` provides a dictionary-like interface to access the local paths of the huggingface repos specified in the `load` argument of the `@huggingface_hub` decorator.
    
    Examples
    --------
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
        """
        Returns metadata information about all loaded models from Hugging Face Hub.
        This property provides access to the metadata of models that have been loaded
        via the `@huggingface_hub(load=...)` decorator. The metadata includes information
        such as model repository details, storage location, and any cached information
        from the datastore. Returns a dictionary where keys are model repository IDs and values are metadata
        dictionaries containing information about each loaded model.
        """
        ...
    def cleanup(self):
        ...
    ...

class HuggingfaceHubDecorator(metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.checkpoints.decorator.CheckpointDecorator, metaclass=type):
    """
    Decorator that helps cache, version, and store models/datasets from the Hugging Face Hub.
    
    Examples
    --------
    
    ```python
    # **Usage: creating references to models from the Hugging Face Hub that may be loaded in downstream steps**
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
    
    # **Usage: explicitly loading models at runtime from the Hugging Face Hub or from cache (from Metaflow's datastore)**
    @huggingface_hub
    @step
    def run_training(self):
        # Temporary directory (auto-cleaned on exit)
        with current.huggingface_hub.load(
            repo_id="google-bert/bert-base-uncased",
            allow_patterns=["*.bin"],
        ) as local_path:
            # Use files under local_path
            train_model(local_path)
            ...
    
    # **Usage: loading models directly from the Hugging Face Hub or from cache (from Metaflow's datastore)**
    
    @huggingface_hub(load=["mistralai/Mistral-7B-Instruct-v0.1"])
    @step
    def pull_model_from_huggingface(self):
        path_to_model = current.huggingface_hub.loaded["mistralai/Mistral-7B-Instruct-v0.1"]
    
    @huggingface_hub(load=[("mistralai/Mistral-7B-Instruct-v0.1", "/my-directory"), ("myorg/mistral-lora", "/my-lora-directory")])
    @step
    def finetune_model(self):
        path_to_model = current.huggingface_hub.loaded["mistralai/Mistral-7B-Instruct-v0.1"]
        # path_to_model will be /my-directory
    
    
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
    
    Parameters
    ----------
    temp_dir_root : str, optional
        The root directory that will hold the temporary directory where objects will be downloaded.
    
    cache_scope : str, optional
        The scope of the cache. Can be `checkpoint` / `flow` / `global`.
            - `checkpoint` (default): All repos are stored like objects saved by `@checkpoint`.
                i.e., the cached path is derived from the namespace, flow, step, and Metaflow foreach iteration.
                Any repo downloaded under this scope will only be retrieved from the cache when the step runs under the same namespace in the same flow (at the same foreach index).
    
            - `flow`: All repos are cached under the flow, regardless of namespace.
                i.e., the cached path is derived solely from the flow name.
                When to use this mode: (1) Multiple users are executing the same flow and want shared access to the repos cached by the decorator. (2) Multiple versions of a flow are deployed, all needing access to the same repos cached by the decorator.
    
            - `global`: All repos are cached under a globally static path.
                i.e., the base path of the cache is static and all repos are stored under it.
                When to use this mode:
                    - All repos from the Hugging Face Hub need to be shared by users across all flow executions.
            - Each caching scope comes with its own trade-offs:
                - `checkpoint`:
                    - Has explicit control over when caches are populated (controlled by the same flow that has the `@huggingface_hub` decorator) but ends up hitting the Hugging Face Hub more often if there are many users/namespaces/steps.
                    - Since objects are written on a `namespace/flow/step` basis, the blast radius of a bad checkpoint is limited to a particular flow in a namespace.
                - `flow`:
                    - Has less control over when caches are populated (can be written by any execution instance of a flow from any namespace) but results in more cache hits.
                    - The blast radius of a bad checkpoint is limited to all runs of a particular flow.
                    - It doesn't promote cache reuse across flows.
                - `global`:
                    - Has no control over when caches are populated (can be written by any flow execution) but has the highest cache hit rate.
                    - It promotes cache reuse across flows.
                    - The blast radius of a bad checkpoint spans every flow that could be using a particular repo.
    
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
    
        This object provides a thin, Metaflow-friendly layer over
        [huggingface_hub]'s `snapshot_download`:
    
        - Snapshot references (persist-and-reuse):
            Use `current.huggingface_hub.snapshot_download(repo_id=..., ...)` to
            ensure a repo is available in the Metaflow datastore. If absent, it is
            downloaded once and saved; the call returns a reference dict you can
            store and load later (for example via `@model`).
    
        - On-demand local access (context manager):
            Use `current.huggingface_hub.load(repo_id=..., [path=...], ...)` as a
            context manager to obtain a local filesystem path for immediate use.
            If the repo exists in the datastore, it is loaded from there;
            otherwise it is fetched from the Hugging Face Hub and then cached in
            the datastore. When `path` is omitted, a temporary directory is
            created and cleaned up automatically when the context exits. When
            `path` is provided, files are placed there and are not cleaned up by
            the context manager.
    
        Repos are cached in the datastore using the huggingface_hub.snapshot_download's arguments. The cache
        key may include: `repo_id`, `repo_type`, `revision`, `ignore_patterns`,
        and `allow_patterns` (see `cache_scope` for how keys are scoped).
    
        > Usage Styles
        ```python
        # Snapshot reference:
        ref = current.huggingface_hub.snapshot_download(
            repo_id="google-bert/bert-base-uncased",
            allow_patterns=["*.json"]
        )
    
        # Explicit Model Loading with Context manager:
        with current.huggingface_hub.load(
            repo_id="google-bert/bert-base-uncased",
            allow_patterns=["*.json"]
        ) as local_path:
            my_model = torch.load(os.path.join(local_path, "model.bin"))
        ```
    
        @@ Returns
        ----------
        HuggingfaceRegistry
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

