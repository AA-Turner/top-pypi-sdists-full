import json
import os
from typing import Iterable, Tuple

import click
import requests
from opentelemetry import trace
from otel_extensions import instrumented
from retry import retry
from ubai_client.apis import ArtifactApi

from utf_queue_client import DISABLE_SSL_VERIFICATION_DEFAULT
from utf_queue_client.clients.ubai_artifact_upload_request_producer import (
    UbaiArtifactUploadRequestProducer,
)
from utf_queue_client.scripts import get_or_make_ca_file, setup_telemetry
from utf_queue_client.utils import prepare_queue_central_url

MULTIPART_SIZE_THRESHOLD = 1000000


@click.command()
@click.option(
    "--file-path",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help="Path to file to upload",
)
@click.option("--metadata", multiple=True, type=(str, str))
@click.option(
    "--username",
    envvar="UTF_QUEUE_USERNAME",
    help="UTF queue username",
)
@click.option(
    "--password",
    envvar="UTF_QUEUE_PASSWORD",
    help="UTF queue password",
)
@click.option(
    "--client-id", type=str, default="Unknown Client", help="Optional client identifier"
)
@click.option(
    "--retries", default=6, help="number of retries (in case of network-related issues)"
)
@click.option("--queue/--no-queue", default=False)
def cli_entrypoint(
    file_path: str,
    metadata: Iterable[Tuple[str, str]],
    username: str,
    password: str,
    client_id: str,
    retries: int,
    queue: bool,
):
    cli(file_path, metadata, username, password, client_id, retries, queue)


def cli(
    file_path: str,
    metadata: Iterable[Tuple[str, str]],
    username: str,
    password: str,
    client_id: str,
    retries: int = 6,
    queue: bool = False,
):
    with setup_telemetry():
        url = ""
        if queue:
            url = prepare_queue_central_url(username, password)

        metadata_dict = {}
        for key, value in metadata:
            metadata_dict[key] = value

        @retry(Exception, delay=5, backoff=2, max_delay=30, tries=retries + 1)
        def retry_wrapper():
            if queue:
                upload_artifact_through_queue(url, client_id, file_path, metadata_dict)
            else:
                upload_artifact_direct(file_path, metadata_dict)

        retry_wrapper()


@instrumented
def upload_artifact_through_queue(url, client_id, file_path, metadata_dict):
    client = UbaiArtifactUploadRequestProducer(url, client_id)
    client.upload_artifact(file_path, metadata=metadata_dict)


@instrumented
def upload_artifact_direct(file_path, metadata_dict):
    (
        name,
        extension,
        contents,
        base64_content,
    ) = UbaiArtifactUploadRequestProducer.extract_payload(file_path)
    verify_ssl = not (
        os.environ.get("DISABLE_SSL_VERIFICATION", DISABLE_SSL_VERIFICATION_DEFAULT)
        == "true"
    )
    span = trace.get_current_span()
    span.set_attribute("artifact.name", name)
    span.set_attribute("artifact.extension", extension)
    span.set_attribute("artifact.length", len(contents))
    for key in metadata_dict:
        span.set_attribute(f"metadata.{key}", metadata_dict[key])
    if len(contents) > MULTIPART_SIZE_THRESHOLD:
        span.set_attribute("multipart_upload", True)
        # use multipart transfer endpoint
        artifact_api = ArtifactApi()
        with open(file_path, "rb") as f:
            files = {"file": (name + extension, f)}
            resp = requests.post(
                f"{artifact_api.api_client.configuration.host}/api/v1/artifact-upload-file",
                files=files,
                data={"metadata": json.dumps(metadata_dict)},
                verify=get_or_make_ca_file() if verify_ssl else False,
            )
            if resp.status_code != 200 and resp.status_code != 201:
                raise RuntimeError(resp.content)
    else:
        span.set_attribute("multipart_upload", False)
        UbaiArtifactUploadRequestProducer.upload_artifact_direct(
            name, extension, base64_content, metadata_dict, verify_ssl=verify_ssl
        )


if __name__ == "__main__":
    cli_entrypoint()
