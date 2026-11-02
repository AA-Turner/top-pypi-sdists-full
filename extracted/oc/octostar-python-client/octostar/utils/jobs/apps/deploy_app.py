import os
import logging
from typing import Any, Optional

_logger = logging.getLogger(__name__)

from ....api.apps import deploy_app
from ....models.deploy_app_json_body import DeployAppJsonBody
from ....models.deploy_app_json_body_secrets import DeployAppJsonBodySecrets
from ....client import Client
from ...exceptions import ApiConnectionError


def sync(
    workspace_id: str,
    os_entity_uid: str,
    secrets: Optional[dict[str, Any]] = None,
    client: Client = None,
):
    """
    # Deploys the App defined by a given workspace and entity (the app root folder).

    ## Arguments
    - `workspace_id`: The ID of the workspace containing the app folder.
    - `os_entity_uid`: The entity ID of the app folder.
    - `secrets`: An optional key-value pair of secrets to deploy the app with.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    The app entity.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    if not secrets:
        secrets = {}
    secrets_body = DeployAppJsonBody(DeployAppJsonBodySecrets(**secrets))
    response = deploy_app.sync_detailed(
        workspace=workspace_id,
        os_entity_uid=os_entity_uid,
        json_body=secrets_body,
        client=client,
    )
    if response.status_code not in (200, 202):
        raise ApiConnectionError("deploy_app", response, client)
    return response.parsed


async def asyncio(
    workspace_id: str,
    os_entity_uid: str,
    secrets: Optional[dict[str, Any]] = None,
    client: Client = None,
):
    """
    # Deploys asynchronously the App defined by a given workspace and entity (the app root folder).

    ## Arguments
    - `workspace_id`: The ID of the workspace containing the app folder.
    - `os_entity_uid`: The entity ID of the app folder.
    - `secrets`: An optional key-value pair of secrets to deploy the app with.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    The app entity.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    if not secrets:
        secrets = {}
    secrets_body = DeployAppJsonBody(DeployAppJsonBodySecrets(**secrets))
    response = await deploy_app.asyncio_detailed(
        workspace=workspace_id,
        os_entity_uid=os_entity_uid,
        json_body=secrets_body,
        client=client,
    )
    if response.status_code not in (200, 202):
        raise ApiConnectionError("deploy_app", response, client)
    return response.parsed
