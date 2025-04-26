from typing import List

import rich_click as click
from rich.console import Console

from union import Resources
from union.cli._common import CommandBase
from union.remote import HuggingFaceModelInfo, UnionRemote

DEFAULT_UNION_API_KEY = "UNION_API_KEY"
HF_TOKEN_KEY = "HF_TOKEN"


@click.group()
def cache():
    """Cache certain artifacts from remote registries."""


@cache.command(cls=CommandBase)
@click.argument("repo", type=str)
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
@click.option("--chunk-size", type=int, help="Chunk size in bytes if you want to override the default")
@click.option("--wait", is_flag=True, help="Wait for the model to be cached.")
@click.option("--hf-token-key", type=str, help="Union secret key with hugging face token", default=HF_TOKEN_KEY)
@click.option(
    "--union-api-key", type=str, help="Union secret key with admin permissions", default=DEFAULT_UNION_API_KEY
)
@click.option("--cpu", type=str, help="Amount of CPU to use for downloading and caching hugging face model")
@click.option("--mem", type=str, help="Amount of Memory to use for downloading and caching hugging face model")
def model_from_hf(
    repo: str,
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
    chunk_size: int,
    hf_token_key: str,
    union_api_key: str,
    cpu: str,
    mem: str,
):
    """Create a model with NAME."""
    remote = UnionRemote(default_domain=domain, default_project=project)
    info = HuggingFaceModelInfo(
        repo=repo,
        architecture=architecture,
        task=task,
        modality=modality,
        serial_format=format,
        model_type=model_type,
        short_description=short_description,
    )
    cache_exec = remote._create_model_from_hf(
        info=info,
        hf_token_key=hf_token_key,
        union_api_key=union_api_key,
        retry=force,
        chunk_size=chunk_size,
        resources=Resources(cpu=cpu, mem=mem),
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
