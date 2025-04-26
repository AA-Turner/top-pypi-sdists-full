from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional, Tuple, Union

from flytekit import ImageSpec, Resources, Secret, Workflow, current_context
from flytekit.core.context_manager import ExecutionParameters

import union
from union.artifacts import Artifact
from union.artifacts._card import ModelCard
from union.remote import UnionRemote
from union.remote._app_template_factory import (
    ARCHITECTURE_KEY,
    ARTIFACT_TYPE_KEY,
    COMMIT_KEY,
    FORMAT_KEY,
    MODALITY_KEY,
    MODEL_TYPE_KEY,
    TASK_KEY,
    HuggingFaceModelInfo,
)

# Created by running maint_tools/build_llm_models.py
CHUNK_SIZE = 8 * 1024 * 1024  # 8MB


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


def get_partition_keys_for_model(info: HuggingFaceModelInfo) -> Dict[str, str]:
    """
    Get partition keys for a model, given the architecture, task, modality, serial format and model type.

    :param info: The model info
    :return: The partition keys for the model
    """
    return {
        ARCHITECTURE_KEY: info.architecture,
        TASK_KEY: info.task,
        FORMAT_KEY: info.serial_format,
        MODALITY_KEY: ",".join(info.modality),
        ARTIFACT_TYPE_KEY: "model",
        MODEL_TYPE_KEY: info.model_type,
    }


def stream_all_files_to_flytedir(
    repo_id: str,
    commit: str,
    token: str | None = None,
    chunk_size: int = CHUNK_SIZE,
) -> Tuple[union.FlyteDirectory, str | None]:
    """
    TODO we should use hf-transfer for this, but the only option on hf-transfer is to download the files to local disk.
    Stream all files in a Hugging Face Hub repository to a FlyteDirectory.

    Args:
        :param repo_id: str The repository ID (e.g., 'julien-c/EsperBERTo-small').
        :param commit: str The commit ID.
        :param token: str[optional] The Hugging Face Hub token for authentication.
        :param chunk_size: int[optional] The chunk size to use when streaming the model files.
    """
    from huggingface_hub import HfFileSystem

    directory = union.FlyteDirectory.new_remote()
    card = None

    hfs = HfFileSystem(token=token)
    for file_details in hfs.ls(repo_id, revision=commit, detail=True):
        f = file_details["name"]
        if f.endswith(".md"):
            print(f"Reading card from {f}")
            with hfs.open(f, "r") as res:
                card = res.read()
            continue

        with hfs.open(f, "rb", block_size=0) as res:
            filename = os.path.basename(f)
            size = file_details["size"]
            ff = directory.new_file(filename)
            copied = 0
            print(f"Copying {f} to {ff.path}, size: {size}. Total chunks: {size // chunk_size}")
            with ff.open("wb") as sink:
                while True:
                    chunk = res.read(chunk_size)
                    sink.write(chunk)
                    copied = copied + len(chunk)
                    if copied >= size:
                        break
                    percent_complete = copied / size * 100
                    if int(percent_complete) > 0 and int(percent_complete) % 10 == 0:
                        print(f"Completed copying {percent_complete} %...")
        print(f"Copied {f} to {directory.path}")
    return directory, card


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
    blob: str
    model_uri: str


# Container, secrets, and resources are set in the create_hf_model_cache_workflow
@union.task(cache=True, cache_version="1.1")
def cache_model_from_hf(
    info: HuggingFaceModelInfo, commit: str, chunk_size: int, retry: int, hf_token_key: str
) -> ArtifactInfo:
    """
    This task caches a model from the Hugging Face Hub, given the model info.
    Args:
        info: HugoingFaceModelInfo: The model info.
        commit: str: The commit id of the model.

    Returns:
        FlyteDirectory: The model artifact.
    """
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

    partitions = get_partition_keys_for_model(info)
    partitions["huggingface-source"] = info.repo
    partitions[COMMIT_KEY] = commit
    print(f"Partitions: {partitions}")

    print("Streaming files to blob storage...", flush=True)
    directory, card = stream_all_files_to_flytedir(info.repo, commit, token, chunk_size=chunk_size)
    print(f"Data streamed to {directory.path}")
    artifact_name = info.repo.split("/")[-1]
    artifact_name = artifact_name.replace(".", "_")
    if retry > 0:
        artifact_name = f"{artifact_name}-{retry}"

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
    return ArtifactInfo(blob=directory.path, model_uri=a.metadata().uri if a else "NA")


def create_hf_model_cache_workflow(
    image: Union[str, ImageSpec],
    hf_token_key: str,
    union_api_key: str,
    resources: Optional[Resources] = None,
):
    """
    Create workflow runs the cache_model_from_hf task.

    The arguments are:
    image: image to run tasks in.
    retry: this can be used to force a new artifact to be created with the same name and an incremented version,
            this will create a new copy in blob store too
    info: HuggingFaceInfo: The model info.
    chunk_size: Optional[int]: The chunk size to use when streaming the model files.

    The outputs are:
    ArtifactInfo: The model artifact
    """
    imperative_wf = Workflow(name=f"{__name__}.hf_model_cacher")
    imperative_wf.add_workflow_input("info", HuggingFaceModelInfo)
    imperative_wf.add_workflow_input("chunk_size", int)
    imperative_wf.add_workflow_input("retry", int)
    imperative_wf.add_workflow_input("hf_token_key", str)

    if resources is None:
        resources = union.Resources(mem="2Gi", cpu="2")

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
    )(cache_model_from_hf.task_function)

    cache_model_from_hf_node = imperative_wf.add_entity(
        cache_mode_task,
        info=imperative_wf.inputs["info"],
        commit=validate_repo_node.outputs["o0"],
        chunk_size=imperative_wf.inputs["chunk_size"],
        retry=imperative_wf.inputs["retry"],
        hf_token_key=imperative_wf.inputs["hf_token_key"],
    )
    imperative_wf.add_workflow_output("artifact", cache_model_from_hf_node.outputs["o0"])

    return imperative_wf, os.path.dirname(union.__path__[0]), additional_context
