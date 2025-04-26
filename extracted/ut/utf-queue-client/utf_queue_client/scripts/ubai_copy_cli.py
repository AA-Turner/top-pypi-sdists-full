import os
from typing import Iterable, Tuple

import click
import requests
from opentelemetry import trace
from otel_extensions import instrumented
from retry import retry
from ubai_client.apis import ArtifactApi

from utf_queue_client import DISABLE_SSL_VERIFICATION_DEFAULT
from utf_queue_client.scripts import get_or_make_ca_file, setup_telemetry


@click.command()
@click.option(
    "--artifact_id",
    required=True,
    help="artifact id to copy from",
)
@click.option(
    "--name",
    required=True,
    help="name of artifact",
)
@click.option(
    "--extension",
    required=True,
    help="extension of artifact",
)
@click.option("--metadata", multiple=True, type=(str, str))
@click.option(
    "--retries", default=6, help="number of retries (in case of network-related issues)"
)
def cli_entrypoint(
    artifact_id: str,
    name: str,
    extension: str,
    metadata: Iterable[Tuple[str, str]],
    retries: int,
):
    cli(artifact_id, name, extension, metadata, retries)


def cli(
    artifact_id: str,
    name: str,
    extension: str,
    metadata: Iterable[Tuple[str, str]],
    retries: int = 6,
):
    with setup_telemetry():
        metadata_dict = {}
        for key, value in metadata:
            metadata_dict[key] = value

        @retry(Exception, delay=5, backoff=2, max_delay=30, tries=retries + 1)
        def retry_wrapper():
            copy_artifact(artifact_id, name, extension, metadata_dict)

        retry_wrapper()


@instrumented
def copy_artifact(artifact_id, name, extension, metadata_dict):
    verify_ssl = not (
        os.environ.get("DISABLE_SSL_VERIFICATION", DISABLE_SSL_VERIFICATION_DEFAULT)
        == "true"
    )
    span = trace.get_current_span()
    span.set_attribute("artifact.name", name)
    span.set_attribute("artifact.extension", extension)
    for key in metadata_dict:
        span.set_attribute(f"metadata.{key}", metadata_dict[key])
    span.set_attribute("copy_artifact", True)
    # use copy endpoint
    artifact_api = ArtifactApi()
    resp = requests.post(
        f"{artifact_api.api_client.configuration.host}/api/v1/artifacts/{artifact_id}/copy",
        json={"name": name, "extension": extension, "metadata": metadata_dict},
        verify=get_or_make_ca_file() if verify_ssl else False,
    )
    if resp.status_code != 200 and resp.status_code != 201:
        raise RuntimeError(resp.content)


if __name__ == "__main__":
    cli_entrypoint()
