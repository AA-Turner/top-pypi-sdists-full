import os
from typing import Iterable, Optional, Tuple

import click
from opentelemetry import trace
from otel_extensions import instrumented
from retry import retry
from ubai_client.apis import SearchApi
from ubai_client.models import ArtifactStorage

from utf_queue_client import DISABLE_SSL_VERIFICATION_DEFAULT
from utf_queue_client.scripts import setup_telemetry


@click.command()
@click.option("--name", default=None, help="artifact name")
@click.option("--extension", default=None, help="artifact extension, e.g. '.bin'")
@click.option("--metadata", multiple=True, type=(str, str))
@click.option(
    "--retries", default=6, help="number of retries (in case of network-related issues)"
)
def cli_entrypoint(
    name: Optional[str],
    extension: Optional[str],
    metadata: Iterable[Tuple[str, str]],
    retries: int,
):
    search_results = cli(name, extension, metadata, retries)
    for result in search_results:
        print(result)


def cli(
    name: Optional[str],
    extension: Optional[str],
    metadata: Iterable[Tuple[str, str]],
    retries: int = 6,
):
    with setup_telemetry():
        metadata_dict = {}
        for key, value in metadata:
            metadata_dict[key] = value
        if len(metadata_dict) == 0 and name is None and extension is None:
            raise RuntimeError("Must specify at least one search criterion")
        search_opts = ArtifactStorage(metadata=metadata_dict)
        if name is not None:
            search_opts.name = name
        if extension is not None:
            search_opts.extension = extension

        @retry(Exception, delay=5, backoff=2, max_delay=30, tries=retries + 1)
        def retry_wrapper():
            return find_all_artifacts(search_opts)

        return retry_wrapper()


@instrumented
def find_all_artifacts(search_opts: ArtifactStorage):
    search_api = SearchApi()
    if (
        os.environ.get("DISABLE_SSL_VERIFICATION", DISABLE_SSL_VERIFICATION_DEFAULT)
        == "true"
    ):
        search_api.api_client.configuration.verify_ssl = False
        search_api.api_client.configuration.assert_hostname = False
    search_api.api_client.configuration.discard_unknown_keys = True
    span = trace.get_current_span()
    span.set_attribute("artifact.name", search_opts.get("name") or "")
    span.set_attribute("artifact.extension", search_opts.get("extension") or "")
    for key in search_opts.metadata:
        span.set_attribute(f"metadata.{key}", search_opts.metadata[key])
    search_results = search_api.find_all_artifacts(search_opts)
    result_ids = [result.id for result in search_results]
    span.set_attribute("search_results", result_ids)
    return result_ids


if __name__ == "__main__":
    cli_entrypoint()
