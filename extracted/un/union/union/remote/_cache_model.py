from __future__ import annotations

import json
import logging
import os
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional, Tuple, Union

from flytekit import ImageSpec, Resources, Secret, Workflow, current_context
from flytekit.core.context_manager import ExecutionParameters
from flytekit.extras import accelerators

import union
from union.artifacts import Artifact
from union.artifacts._card import ModelCard
from union.remote import UnionRemote
from union.remote._app_template_factory import (
    ARCHITECTURE_KEY,
    ARTIFACT_TYPE_KEY,
    COMMIT_KEY,
    FORMAT_KEY,
    HUGGINGFACE_SOURCE_KEY,
    MODALITY_KEY,
    MODEL_TYPE_KEY,
    SHARD_ENGINE_KEY,
    SHARD_PARALLELISM_KEY,
    TASK_KEY,
    HuggingFaceModelInfo,
    ShardConfig,
)

logger = logging.getLogger(__name__)


def _get_remote(ctx: ExecutionParameters) -> UnionRemote:
    """
    Get the remote object for the current execution. This is used to interact with the Union backend.
    Args:
        self: flytekit.core.context_manager.ExecutionParameters
    Returns: UnionRemote
    """
    project = ctx.execution_id.project if ctx.execution_id else None
    domain = ctx.execution_id.domain if ctx.execution_id else None
    raw_output = ctx.raw_output_prefix
    return UnionRemote(config=None, project=project, domain=domain, data_upload_location=raw_output)


def _emit_artifact(ctx: ExecutionParameters, o: Artifact) -> Artifact:
    """
    Emit an artifact to Union. This will create a new artifact with the given name and version and will
    associate with this execution.
    If o is None or not an Artifact, this function will do nothing.
    Args:
        self: flytekit.core.context_manager.ExecutionParameters
        o: Artifact

    Raises: Exception if artifact creation fails.
    """
    # TODO add node_id to the context.
    from union.internal.artifacts import artifacts_pb2

    # Emit artifact
    if "HOSTNAME" in os.environ:
        hostname = os.environ["HOSTNAME"]
        try:
            node_id = hostname.split("-")[1]
        except Exception:
            node_id = "n1"
    else:
        node_id = "n1"

    o.set_source(
        artifacts_pb2.ArtifactSource(
            workflow_execution=ctx.execution_id.to_flyte_idl(),
            task_id=ctx.task_id.to_flyte_idl(),
            retry_attempt=int(os.getenv("FLYTE_ATTEMPT_NUMBER", "0")),
            node_id=node_id,
        )
    )
    remote = _get_remote(ctx)
    try:
        return remote.create_artifact(o)
    except Exception as e:
        logger.error(f"Failed to create artifact {o}: {e}")
        return remote.get_artifact(query=o.query().to_flyte_idl())


def lookup_huggingface_model_info(model_repo: str, commit: str, token: str) -> Tuple[str, str]:
    """
    Lookup Hugging Face model info for a model repo.
    This looks up the model info in huggingface config.json file.

    The assumed path is of the kind:
        https://huggingface.co/{model_repo}/resolve/{commit}/config.json
    example:
        https://huggingface.co/deepseek-ai/DeepSeek-V3-Base/resolve/69cf1d97df36843c038062eed5672df1d8480b32/config.json
    The json file is downloaded and the following fields are extracted:
        - model_type
        - architecture
    :param model_repo: The model repo name in huggingface
    :param token: The huggingface token for private models
    :return: HuggingFaceModelInfo
    """

    from huggingface_hub import hf_hub_download

    config_file = hf_hub_download(repo_id=model_repo, filename="config.json", revision=commit, token=token)
    arch = None
    model_type = None
    with open(config_file, "r") as f:
        j = json.load(f)
        arch = j.get("architecture", None)
        if arch is None:
            arch = j.get("architectures", None)
            if arch:
                arch = ",".join(arch)
            model_type = j.get("model_type", None)
    return model_type, arch


def get_partition_keys_for_model(info: HuggingFaceModelInfo, commit: str) -> Dict[str, str]:
    """
    Get partition keys for a model, given the architecture, task, modality, serial format and model type.

    :param info: The model info
    :return: The partition keys for the model
    """
    return {
        ARCHITECTURE_KEY: info.architecture,
        TASK_KEY: info.task,
        FORMAT_KEY: info.serial_format,
        HUGGINGFACE_SOURCE_KEY: info.repo,
        COMMIT_KEY: commit,
        MODALITY_KEY: ",".join(info.modality),
        ARTIFACT_TYPE_KEY: "model",
        MODEL_TYPE_KEY: info.model_type,
        SHARD_ENGINE_KEY: str(info.shard_config.engine) if info.shard_config else "None",
        SHARD_PARALLELISM_KEY: str(info.shard_config.args.tensor_parallel_size) if info.shard_config else "None",
    }


def download_all_files_to_flytedir(
    repo_id: str,
    commit: str,
    token: str | None = None,
) -> Tuple[union.FlyteDirectory, str | None]:
    """
    TODO we should use hf-transfer for this, but the only option on hf-transfer is to download the files to local disk.
    Stream all files in a Hugging Face Hub repository to a FlyteDirectory.

    Args:
        :param repo_id: str The repository ID (e.g., 'julien-c/EsperBERTo-small').
        :param commit: str The commit ID.
        :param token: str[optional] The Hugging Face Hub token for authentication.
    """
    from huggingface_hub import HfFileSystem, snapshot_download

    directory = union.FlyteDirectory.new("model_snapshot")
    card = None

    hfs = HfFileSystem(token=token)

    try:
        readme_file_details = hfs.info(f"{repo_id}/README.md", revision=commit)
        readme_name = readme_file_details["name"]
        with tempfile.NamedTemporaryFile() as temp_file:
            hfs.download(readme_name, temp_file.name, revision=commit)
            with open(temp_file.name, "r") as f:
                card = f.read()

    except FileNotFoundError:
        print("No readme file", flush=True)

    print(f"Downloading model from {repo_id} to {directory.path}", flush=True)
    snapshot_download(
        repo_id=repo_id,
        revision=commit,
        local_dir=directory.path,
        token=token,
    )
    return directory, card


def shard_model(
    shard_config: ShardConfig,
    model_path: str,
) -> union.FlyteDirectory:
    """Shard a model using the given shard config."""

    from vllm import LLM

    assert shard_config.engine == "vllm", "'vllm' is the only supported sharding engine for now"
    sharded_model_dir = union.FlyteDirectory.new("sharded_model_snapshot")

    # Create LLM instance from arguments
    llm = LLM(**shard_config.args.get_vllm_args(model_path))
    print(f"LLM initialized: {llm}")

    # Check which engine version is being used
    is_v1_engine = hasattr(llm.llm_engine, "engine_core")

    if is_v1_engine:
        # For V1 engine, we need to use engine_core.save_sharded_state
        print("Using V1 engine save path")
        llm.llm_engine.engine_core.save_sharded_state(
            path=sharded_model_dir.path,
            pattern=shard_config.args.file_pattern,
            max_size=shard_config.args.max_file_size,
        )
    else:
        # For V0 engine
        print("Using V0 engine save path")
        model_executor = llm.llm_engine.model_executor
        model_executor.save_sharded_state(
            path=sharded_model_dir.path,
            pattern=shard_config.args.file_pattern,
            max_size=shard_config.args.max_file_size,
        )

    # Copy metadata files to output directory
    print(f"Copying metadata files to {sharded_model_dir.path}")
    for file in os.listdir(model_path):
        if os.path.splitext(file)[1] not in (".bin", ".pt", ".safetensors"):
            if os.path.isdir(os.path.join(model_path, file)):
                shutil.copytree(os.path.join(model_path, file), os.path.join(sharded_model_dir.path, file))
            else:
                shutil.copy(os.path.join(model_path, file), sharded_model_dir.path)

    return sharded_model_dir


# Container and secrets are set in the create_hf_model_cache_workflow
@union.task
def validate_repo(info: HuggingFaceModelInfo, hf_token_key: str) -> Tuple[str, datetime]:
    """
    Validate if the repo exists in Hugging Face Hub.
    Args:
        info: HuggingFaceModelInfo: The model info.

    Returns:
        Returns the latest version of the model in the huggingface repo.
    """
    from huggingface_hub import list_repo_commits, repo_exists

    token = current_context().secrets.get(key=hf_token_key)
    if not repo_exists(info.repo, token=token):
        raise ValueError(f"Repository {info.repo} does not exist in huggingface.")

    commit = list_repo_commits(info.repo, token=token)[0]
    return commit.commit_id, commit.created_at


@dataclass
class ArtifactInfo:
    artifact_name: str
    blob: str
    model_uri: str


# Container, secrets, and resources are set in the create_hf_model_cache_workflow
@union.task(cache=True, cache_version="1.1")
def cache_model_from_hf(info: HuggingFaceModelInfo, commit: str, retry: int, hf_token_key: str) -> ArtifactInfo:
    """
    This task caches a model from the Hugging Face Hub, given the model info.
    Args:
        info: HuggingFaceModelInfo: The model info.
        commit: str: The commit id of the model.

    Returns:
        FlyteDirectory: The model artifact.
    """
    print("Model info: ", info)
    print(f"Caching model from huggingface repo: {info.repo}, commit: {commit}", flush=True)
    ctx = union.current_context()
    token = ctx.secrets.get(key=hf_token_key)
    if not info.model_type or not info.architecture:
        print("Looking up huggingface model info...")
        model_type = "custom"
        architecture = "custom"
        try:
            model_type, architecture = lookup_huggingface_model_info(info.repo, commit, token)
        except Exception as e:
            print(f"Error looking up huggingface model info: {e}")
        info.model_type = info.model_type or model_type
        info.architecture = info.architecture or architecture

    print(f"Model type: {info.model_type}, architecture: {info.architecture}")

    partitions = get_partition_keys_for_model(info, commit)
    print(f"Partitions: {partitions}")

    print("Downloading files...", flush=True)
    directory, card = download_all_files_to_flytedir(info.repo, commit, token)
    print(f"Data downloaded to {directory.path}")

    if info.shard_config is not None:
        print(f"Sharding model with {info.shard_config.engine} engine")
        directory = shard_model(info.shard_config, directory.path)

    if info.artifact_name is None:
        artifact_name = info.repo.split("/")[-1]
        artifact_name = artifact_name.replace(".", "-")
    else:
        artifact_name = info.artifact_name

    o = union.Artifact(
        name=artifact_name,
        python_type=union.FlyteDirectory,
        python_val=directory,
        short_description=f"Model cached from huggingface repo: {info.repo}, commit: {commit} "
        f"by execution: {ctx.execution_id}.",
        partitions=partitions,
        project=ctx.execution_id.project if ctx.execution_id else None,
        domain=ctx.execution_id.domain if ctx.execution_id else None,
        card=ModelCard.from_obj(card) if card else None,
    )
    print(f"Emitting artifact, {o}")
    a: union.Artifact = _emit_artifact(ctx, o)
    print(f"Artifact emitted, {a.metadata().uri}")
    return ArtifactInfo(artifact_name=artifact_name, blob=directory.path, model_uri=a.metadata().uri if a else "NA")


def create_hf_model_cache_workflow(
    image: Union[str, ImageSpec],
    hf_token_key: str,
    union_api_key: str,
    resources: Optional[Resources] = None,
    accelerator: Optional[str] = None,
):
    """
    Create workflow runs the cache_model_from_hf task.

    The arguments are:
    image: image to run tasks in.
    retry: this can be used to force a new artifact to be created with the same name and an incremented version,
            this will create a new copy in blob store too
    info: HuggingFaceInfo: The model info.

    The outputs are:
    ArtifactInfo: The model artifact
    """
    imperative_wf = Workflow(name=f"{__name__}.hf_model_cacher")
    imperative_wf.add_workflow_input("info", HuggingFaceModelInfo)
    imperative_wf.add_workflow_input("retry", int)
    imperative_wf.add_workflow_input("hf_token_key", str)

    if resources is None:
        resources = union.Resources(mem="2Gi", cpu="2", ephemeral_storage="16Gi")

    task_kwargs = {}
    if accelerator is not None:
        if accelerator == "nvidia-a100":
            accelerator = accelerators.A100
        elif accelerator == "nvidia-a100-80gb":
            accelerator = accelerators.A100_80GB
        else:
            accelerator = accelerators.GPUAccelerator(accelerator)
        task_kwargs["accelerator"] = accelerator
        task_kwargs["shared_memory"] = True

    hf_secret = Secret(key=hf_token_key)
    union_api_secret = Secret(key=union_api_key, env_var="UNION_API_KEY")
    additional_context = [
        str(resources.to_json()),
        str(hf_secret.serialize_to_string()),
        str(union_api_secret.serialize_to_string()),
    ]

    validate_repo_task = union.task(
        container_image=image,
        requests=resources,
        limits=resources,
        secret_requests=[hf_secret],
        **task_kwargs,
    )(validate_repo.task_function)

    validate_repo_node = imperative_wf.add_entity(
        validate_repo_task,
        info=imperative_wf.inputs["info"],
        hf_token_key=imperative_wf.inputs["hf_token_key"],
    )

    cache_mode_task = union.task(
        container_image=image,
        requests=resources,
        limits=resources,
        secret_requests=[hf_secret, union_api_secret],
        **task_kwargs,
    )(cache_model_from_hf.task_function)

    cache_model_from_hf_node = imperative_wf.add_entity(
        cache_mode_task,
        info=imperative_wf.inputs["info"],
        commit=validate_repo_node.outputs["o0"],
        retry=imperative_wf.inputs["retry"],
        hf_token_key=imperative_wf.inputs["hf_token_key"],
    )
    imperative_wf.add_workflow_output("artifact", cache_model_from_hf_node.outputs["o0"])

    return imperative_wf, os.path.dirname(union.__path__[0]), additional_context
