from __future__ import annotations

import typing
from dataclasses import dataclass

import rich.repr
from flytekit.core.artifact import Partition
from flytekit.extras import accelerators as acc

from union import Artifact, Resources
from union.app import App, Input

ARCHITECTURE_KEY = "architecture"
TASK_KEY = "task"
FORMAT_KEY = "format"
MODALITY_KEY = "modality"
ARTIFACT_TYPE_KEY = "_u_type"
MODEL_TYPE_KEY = "model_type"
COMMIT_KEY = "commit"

_FASTAPI_ARCHITECTURES = ["xgboost".casefold(), "custom".casefold(), "joblib".casefold(), "sklearn".casefold()]

VLLM_IMAGE = "ghcr.io/unionai-oss/serving-vllm:0.1.16"


@dataclass
@rich.repr.auto()
class AppTemplate:
    app: App
    engine: str
    preferred: bool = False


def _sanitize_model_name(name: str) -> str:
    return name.lower().replace("/", "-").replace(":", "-").replace(".", "-").replace("_", "-")[:25]


@dataclass
class AppTemplateParams:
    limits: Resources
    accelerator: acc.GPUAccelerator
    prefrerred: bool = False


_TEMPLATES: typing.Dict[str, AppTemplateParams] = {
    "qwen2": AppTemplateParams(
        limits=Resources(cpu="7", mem="27Gi", gpu="1", ephemeral_storage="10Gi"),
        accelerator=acc.L4,
        prefrerred=True,
    ),
    "llama3": AppTemplateParams(
        limits=Resources(cpu="7", mem="27Gi", gpu="1", ephemeral_storage="10Gi"),
        accelerator=acc.L4,
        prefrerred=True,
    ),
    "llama2": AppTemplateParams(
        limits=Resources(cpu="7", mem="27Gi", gpu="1", ephemeral_storage="10Gi"),
        accelerator=acc.L4,
        prefrerred=True,
    ),
    "llama": AppTemplateParams(
        limits=Resources(cpu="7", mem="27Gi", gpu="1", ephemeral_storage="10Gi"),
        accelerator=acc.L4,
        prefrerred=True,
    ),
    "mistral": AppTemplateParams(
        limits=Resources(cpu="7", mem="27Gi", gpu="1", ephemeral_storage="10Gi"),
        accelerator=acc.L4,
        prefrerred=True,
    ),
    "gemma": AppTemplateParams(
        limits=Resources(cpu="7", mem="27Gi", gpu="1", ephemeral_storage="10Gi"),
        accelerator=acc.L4,
        prefrerred=True,
    ),
    "mixtral": AppTemplateParams(
        limits=Resources(cpu="7", mem="27Gi", gpu="1", ephemeral_storage="10Gi"),
        accelerator=acc.L4,
        prefrerred=True,
    ),
    "falcon": AppTemplateParams(
        limits=Resources(cpu="7", mem="27Gi", gpu="1", ephemeral_storage="10Gi"),
        accelerator=acc.L4,
        prefrerred=True,
    ),
    "qwen": AppTemplateParams(
        limits=Resources(cpu="7", mem="27Gi", gpu="1", ephemeral_storage="10Gi"),
        accelerator=acc.L4,
        prefrerred=True,
    ),
    "stablelm": AppTemplateParams(
        limits=Resources(cpu="7", mem="27Gi", gpu="1", ephemeral_storage="10Gi"),
        accelerator=acc.L4,
        prefrerred=True,
    ),
}


class VLLMApp(App):
    def __init__(
        self,
        name: str,
        model_input: typing.Union[Artifact, str],
        accelerator: acc.GPUAccelerator,
        limits: Resources,
        requires_auth: bool = False,
        **kwargs,
    ):
        if isinstance(model_input, Artifact):
            raise NotImplementedError("Artifact input not supported yet")
        super().__init__(
            name=name,
            container_image=VLLM_IMAGE,
            args=f"union-model-loader-vllm serve /home/union --served-model-name {name}",
            port=8000,
            limits=limits,
            accelerator=accelerator,
            env={
                "UNION_MODEL_LOADER_STREAM_SAFETENSORS": "true",
                "UNION_MODEL_LOADER_LOCAL_MODEL_PATH": "/home/union",
                "UNION_MODEL_LOADER_REMOTE_MODEL_PATH": model_input,
            },
            requires_auth=requires_auth,
        )


def get_vllm_app_template(model: Artifact) -> AppTemplate:
    if model.literal is None or model.literal.scalar is None or model.literal.scalar.blob is None:
        raise ValueError(f"Model artifact must have a Directory or a File location, found {model.literal}")
    model_uri = model.literal.scalar.blob.uri
    model_type = find_model_type_for_model(model)
    if model_type is None:
        raise ValueError("Model type not found")
    v = model_type.value.static_value
    if v not in _TEMPLATES:
        raise ValueError(f"Model type {model_type.value} not supported")
    template = _TEMPLATES[v]
    return AppTemplate(
        app=VLLMApp(
            name=f"{_sanitize_model_name(model.name)}-vllm",
            model_input=model_uri,
            accelerator=template.accelerator,
            limits=template.limits,
        ),
        engine="vllm",
        preferred=template.prefrerred,
    )


def _get_fastapi_app_template(model: Artifact) -> AppTemplate:
    return AppTemplate(
        app=App(
            name=f"{_sanitize_model_name(model.name)}-fapi",
            container_image="",
            inputs=[
                Input(
                    name="model",
                    value=model.query(),
                    env_var="MODEL_FILE_PATH",
                ),
            ],
            limits=Resources(cpu="2", mem="4Gi"),
            port=8080,
            include=["./app.py"],
            command=["uvicorn", "--port", "8080", "app:app"],
        ),
        engine="fastapi",
        preferred=True,
    )


def get_partition_keys_for_model(
    architecture: str,
    task: str,
    modality: typing.List[str] | None = None,
    serial_format: str = "safetensors",
    model_type: str | None = None,
) -> typing.Dict[str, str]:
    """
    Get partition keys for a model, given the architecture, task, modality, serial format and model type.
    :param architecture: The architecture of the model
    :param task: The task of the model
    :param modality: The modality of the model
    :param serial_format: The serial format of the model
    :param model_type: The model type of the model
    :return: The partition keys for the model
    """
    if not modality:
        modality = ["text"]

    if architecture is None:
        architecture = "custom"

    if task is None:
        task = "auto"

    if model_type is None:
        model_type = "custom"

    return {
        ARCHITECTURE_KEY: architecture,
        TASK_KEY: task,
        FORMAT_KEY: serial_format,
        MODALITY_KEY: ",".join(modality),
        ARTIFACT_TYPE_KEY: "model",
        MODEL_TYPE_KEY: model_type,
    }


def find_architecture_for_model(model: Artifact) -> Partition | None:
    if model.partitions and model.partitions.partitions:
        return model.partitions.partitions.get(ARCHITECTURE_KEY, None)
    return None


def find_model_type_for_model(model: Artifact) -> Partition | None:
    if model.partitions and model.partitions.partitions:
        return model.partitions.partitions.get(MODEL_TYPE_KEY, None)
    return None


def get_app_templates_for_model(model: Artifact) -> typing.List[AppTemplate]:
    """Get app templates for a model."""
    mt = find_model_type_for_model(model)
    if mt and mt.value:
        # TODO: Update when xgboost is actually supported
        if mt.value.static_value.casefold() == "xgboost":
            return [_get_fastapi_app_template(model)]
    return [get_vllm_app_template(model)]


@dataclass
@rich.repr.auto()
class HuggingFaceModelInfo:
    """
    Captures information about a Hugging Face model. Only repo is required, all other fields are optional, and are
    automatically determined from the model's config.json file. If not found, the fields are initialized to defaults.

    :param repo: The model repo name in huggingface.
    :param model_type: The model type.
    :param architecture: The model architecture.
    :param task: The model task.
    :param modality: The model modality.
    :param serial_format: The model serialization format.
    :param short_description: A short description of the model.
    """

    repo: str
    model_type: str | None = None
    architecture: str | None = None
    task: str = "auto"
    modality: typing.List[str] | None = None
    serial_format: str = "safetensors"
    short_description: str | None = None

    def __post_init__(self):
        if self.modality is None:
            self.modality = ["text"]
