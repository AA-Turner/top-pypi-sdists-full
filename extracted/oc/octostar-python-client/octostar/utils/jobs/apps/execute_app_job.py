import os
import logging
import yaml
from typing import Optional, Union

_logger = logging.getLogger(__name__)

from ....api.apps import execute_app_job
from ....models.execute_app_job_json_body import ExecuteAppJobJsonBody
from ....models.execute_app_job_json_body_annotation import (
    ExecuteAppJobJsonBodyAnnotation,
)
from ....client import Client
from ...exceptions import ApiConnectionError


def sync(
    commands: str,
    zip_archive_link: Optional[str] = os.getenv("OS_SELF_ARCHIVE"),
    manifest: Optional[Union[dict, str]] = None,
    annotations: Optional[dict[str, str]] = None,
    client: Client = None,
):
    """
    # Start a new job

    ## Arguments

    - `commands`: The bash commands to execute in the new job.
    - `zip_archive_link`: A URL to a zip archive containing a valid app. Note that the app will not execute through `main.sh` but via the provided commands.
    - `manifest`: A manifest file, either as a dictionary parsable as YAML or as a raw YAML string.
            Note that `app_name`, `alias` and `app_title` are always inherited from the parent and cannot be overridden by this manifest.
    - `annotations`: A list of key-value strings to be appended to the kubernetes pod.
            Keys must start with 'app.octostar.com/'. Example: {'app.octostar.com/author': 'John Doe'}
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns

    An acknowledgment.

    ## Raises

    - `ApiConnectionError`: If the operation was unsuccessful on the server.
    """
    if not annotations:
        annotations = {}
    if not manifest:
        manifest = None
    if manifest and isinstance(manifest, dict):
        manifest = yaml.dump(manifest)
    response = execute_app_job.sync_detailed(
        json_body=ExecuteAppJobJsonBody(
            ontology=client.ontology,
            archive=zip_archive_link,
            commands=commands,
            manifest=manifest,
            annotation=ExecuteAppJobJsonBodyAnnotation(**annotations),
            ancestor=os.getenv("OS_ANCESTOR") or os.getenv("OS_APP_ID"),
        ),
        client=client,
    )
    if response.status_code != 200:
        raise ApiConnectionError("execute_app_job", response, client)
    return response.parsed


async def asyncio(
    commands: str,
    zip_archive_link: Optional[str] = os.getenv("OS_SELF_ARCHIVE"),
    manifest: Optional[Union[dict, str]] = None,
    annotations: Optional[dict[str, str]] = None,
    client: Client = None,
):
    """
    # Start a new job asynchronously

    ## Arguments

    - `commands`: The bash commands to execute in the new job.
    - `zip_archive_link`: A URL to a zip archive containing a valid app. Note that the app will not execute through `main.sh` but via the provided commands.
    - `manifest`: A manifest file, either as a dictionary parsable as YAML or as a raw YAML string.
            Note that `app_name`, `alias` and `app_title` are always inherited from the parent and cannot be overridden by this manifest.
    - `annotations`: A list of key-value strings to be appended to the kubernetes pod.
            Keys must start with 'app.octostar.com/'. Example: {'app.octostar.com/author': 'John Doe'}
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns

    An acknowledgment.

    ## Raises

    - `ApiConnectionError`: If the operation was unsuccessful on the server.
    """
    if not annotations:
        annotations = {}
    if not manifest:
        manifest = None
    if manifest and isinstance(manifest, dict):
        manifest = yaml.dump(manifest)
    response = await execute_app_job.asyncio_detailed(
        json_body=ExecuteAppJobJsonBody(
            ontology=client.ontology,
            archive=zip_archive_link,
            commands=commands,
            manifest=manifest,
            annotation=ExecuteAppJobJsonBodyAnnotation(**annotations),
            ancestor=os.getenv("OS_ANCESTOR") or os.getenv("OS_APP_ID"),
        ),
        client=client,
    )
    if response.status_code != 200:
        raise ApiConnectionError("execute_app_job", response, client)
    return response.parsed
