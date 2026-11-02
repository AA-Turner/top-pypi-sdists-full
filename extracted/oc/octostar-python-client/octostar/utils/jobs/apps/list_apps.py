import logging
from typing import Optional
import httpx
from httpx import QueryParams

_logger = logging.getLogger(__name__)

from ....client import Client
from ...exceptions import ApiConnectionError
from ...commons import network_retry_strategy


def sync(
    workspaces: Optional[list[str]] = None,
    include_all: bool = False,
    main_namespace_only: bool = False,
    client: Client = None,
):
    """
    # List Apps

    List all of the apps running in Octostar.

    ## Arguments
    - `workspaces`: The list of workspace IDs by which to filter apps. If None, all workspaces are searched.
    - `include_all`: If False, only running apps are returned. If True, undeployed apps are also returned.
    - `main_namespace_only`: If True, running apps will only be searched in the main kubernetes namespace.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A list of apps, each containing their full info.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    endpoint_url = f"{client.get_base_url_v1()}/api/v1/apps/"
    headers = {
        "Authorization": f"Bearer {client.token}",
        "x-ontology": client.ontology,
    }
    if not workspaces:
        workspaces = []
    query_params = QueryParams(
        [
            *[("workspaces", ws) for ws in workspaces],
            ("include_all", include_all),
            ("main_namespace_only", main_namespace_only),
        ]
    )
    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                with httpx.Client() as httpx_client:
                    response = httpx_client.get(
                        endpoint_url, headers=headers, params=query_params, timeout=30
                    )
                    response.raise_for_status()
                    try:
                        parsed = response.json()
                    except ValueError:
                        raise ConnectionError(
                            "Could not fetch data from API (failed to parse response), responded with\n"
                            + str(response.content)
                        )
    except Exception:
        raise ApiConnectionError("list_apps", response, client)
    return parsed["apps"]


async def asyncio(
    workspaces: Optional[list[str]] = None,
    include_all: bool = False,
    main_namespace_only: bool = False,
    client: Client = None,
):
    """
    # List Apps

    List asynchronously all of the apps running in Octostar.

    ## Arguments
    - `workspaces`: The list of workspace IDs by which to filter apps. If None, all workspaces are searched.
    - `include_all`: If False, only running apps are returned. If True, undeployed apps are also returned.
    - `main_namespace_only`: If True, running apps will only be searched in the main kubernetes namespace.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A list of apps, each containing their full info.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    endpoint_url = f"{client.get_base_url_v1()}/api/v1/apps/"
    headers = {
        "Authorization": f"Bearer {client.token}",
        "x-ontology": client.ontology,
    }
    if not workspaces:
        workspaces = []
    query_params = QueryParams(
        [
            *[("workspaces", ws) for ws in workspaces],
            ("include_all", include_all),
            ("main_namespace_only", main_namespace_only),
        ]
    )
    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                async with httpx.AsyncClient() as httpx_client:
                    response = await httpx_client.get(
                        endpoint_url, headers=headers, params=query_params, timeout=30
                    )
                    response.raise_for_status()
                    try:
                        parsed = response.json()
                    except ValueError:
                        raise ConnectionError(
                            "Could not fetch data from API (failed to parse response), responded with\n"
                            + str(response.content)
                        )
    except Exception:
        raise ApiConnectionError("list_apps", response, client)
    return parsed["apps"]
