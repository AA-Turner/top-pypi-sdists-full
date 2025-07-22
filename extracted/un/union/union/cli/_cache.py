import re
from pathlib import Path
from typing import List

import rich_click as click
import yaml
from rich.console import Console

from union import Resources
from union.cli._common import CommandBase
from union.remote import HuggingFaceModelInfo, ShardConfig, UnionRemote, VLLMShardArgs

DEFAULT_UNION_API_KEY = "EAGER_API_KEY"
HF_TOKEN_KEY = "HF_TOKEN"


@click.group()
def cache():
    """Cache certain artifacts from remote registries."""


@cache.command(cls=CommandBase)
@click.argument("repo", type=str)
@click.option(
    "--artifact-name",
    type=str,
    required=False,
    default=None,
    help=(
        "Artifact name to use for the cached model. Must only contain alphanumeric characters, underscores, and "
        "hyphens. If not provided, the repo name will be used (replacing '.' with '-')."
    ),
)
@click.option(
    "--architecture",
    type=str,
    help="Model architecture, as given in HuggingFace config.json, For non transformer models use XGBoost, Custom etc.",
)
@click.option(
    "--task",
    default="auto",
    type=str,
    help="Model task, E.g, `generate`, `classify`, `embed`, `score` etc refer to VLLM docs, "
    "`auto` will try to discover this automatically",
)
@click.option(
    "--modality",
    type=str,
    multiple=True,
    help="Modalities supported by Model, E.g, `text`, `image`, `audio`, `video` etc refer to VLLM Docs",
)
@click.option("--format", type=str, help="Model serialization format, e.g safetensors, onnx, torchscript, joblib, etc")
@click.option(
    "--model-type",
    type=str,
    help="Model type, e.g, `transformer`, `xgboost`, `custom` etc. Model Type is important for non-transformer models."
    "For huggingface models, this is auto determined from config.json['model_type']",
)
@click.option("--short-description", type=str, help="Short description of the model")
@click.option("--force", type=int, help="Force caching of the model, pass --force=1/2/3... to force cache")
@click.option("--wait", is_flag=True, help="Wait for the model to be cached.")
@click.option("--hf-token-key", type=str, help="Union secret key with hugging face token", default=HF_TOKEN_KEY)
@click.option(
    "--union-api-key", type=str, help="Union secret key with admin permissions", default=DEFAULT_UNION_API_KEY
)
@click.option(
    "--cpu",
    type=str,
    help="Amount of CPU to use for downloading, (optionally) sharding, and caching hugging face model",
)
@click.option(
    "--gpu",
    type=str,
    help="Amount of GPU to use for downloading (optionally) sharding, and caching hugging face model",
)
@click.option(
    "--mem",
    type=str,
    help="Amount of Memory to use for downloading, (optionally) sharding, and caching hugging face model",
)
@click.option(
    "--ephemeral-storage",
    type=str,
    help="Amount of Ephemeral Storage to use for downloading, (optionally) sharding, and caching hugging face model",
)
@click.option(
    "--accelerator",
    default=None,
    type=click.Choice(
        [
            "nvidia-l4",
            "nvidia-l4-vws",
            "nvidia-l40s",
            "nvidia-a100",
            "nvidia-a100-80gb",
            "nvidia-a10g",
            "nvidia-tesla-k80",
            "nvidia-tesla-m60",
            "nvidia-tesla-p4",
            "nvidia-tesla-p100",
            "nvidia-tesla-t4",
            "nvidia-tesla-v100",
        ]
    ),
    help="The accelerator to use for downloading, (optionally) sharding, and caching hugging face model",
)
@click.option(
    "--shard-config",
    type=Path,
    help="The engine to shard the model with. Supported values are {{vllm}}",
)
def model_from_hf(
    repo: str,
    artifact_name: str,
    project: str,
    domain: str,
    architecture: str,
    task: str,
    modality: List[str],
    format: str,
    short_description: str,
    model_type: str,
    wait: bool,
    force: int,
    hf_token_key: str,
    union_api_key: str,
    cpu: str,
    gpu: str,
    mem: str,
    ephemeral_storage: str,
    accelerator: str,
    shard_config: Path,
):
    """Create a model with NAME."""
    remote = UnionRemote(default_domain=domain, default_project=project)

    if artifact_name is not None:
        assert re.match(r"^[a-zA-Z0-9_-]+$", artifact_name), (
            "Artifact name must only contain alphanumeric characters, underscores, and hyphens"
        )

    if shard_config is not None:
        with shard_config.open() as f:
            shard_config_dict = yaml.safe_load(f)
            shard_config = ShardConfig(
                engine=shard_config_dict["engine"],
                args=VLLMShardArgs(**shard_config_dict["args"]),
            )

    info = HuggingFaceModelInfo(
        repo=repo,
        artifact_name=artifact_name,
        architecture=architecture,
        task=task,
        modality=modality,
        serial_format=format,
        model_type=model_type,
        short_description=short_description,
        shard_config=shard_config,
    )
    cache_exec = remote._create_model_from_hf(
        info=info,
        hf_token_key=hf_token_key,
        union_api_key=union_api_key,
        retry=force,
        resources=Resources(cpu=cpu, mem=mem, gpu=gpu, ephemeral_storage=ephemeral_storage),
        accelerator=accelerator,
    )
    c = Console()
    url = cache_exec.execution_url
    c.print(
        f"🔄 Started background process to cache model from Hugging Face repo {repo}.\n"
        f" Check the console for status at [link={url}]{url}[/link]"
    )
    if wait:
        with c.status("Waiting for model to be cached...", spinner="dots"):
            cache_exec = cache_exec.wait(poll_interval=2)

        model_uri = cache_exec.outputs["artifact"].model_uri
        c.print(f"Cached model at: [cyan]{cache_exec.outputs['artifact'].blob}[/cyan]")
        c.print(f"Model Artifact ID: [green]{model_uri}[/green]")
        c.print()
        c.print("To deploy this model run:")
        c.print(f"union deploy model --project {project} --domain {domain} {model_uri}")
