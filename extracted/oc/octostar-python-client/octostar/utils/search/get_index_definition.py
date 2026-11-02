import httpx
from typing import Optional
from ...client import Client, get_default_client
from ..commons import network_retry_strategy
from ..exceptions import ApiConnectionError


def sync(timeout: Optional[float] = 30.0, client: Optional[Client] = None) -> dict:
    """
    # Get the search index definition (mapping + settings).

    ## Arguments
    - `timeout`: The timeout for the connection to the search engine. Can be set to "None" for no enforced timeout.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    The raw dictionary response from OpenSearch, containing the entire mapping definition.

    ## Raises
    - `ApiConnectionError`: If the query was unsuccessful.
    """
    if not client:
        client = get_default_client()
    endpoint_url = f"{client.get_base_url_v1()}/api/v1/search_api/{client.ontology}/_index_definition"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {client.token}",
        "x-ontology": client.ontology,
    }
    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                with httpx.Client() as httpx_client:
                    response = httpx_client.get(
                        endpoint_url, headers=headers, timeout=timeout
                    )
                    if response.status_code != 200:
                        raise ConnectionError(
                            f"Could not fetch data from search engine (status code {response.status_code}), responded with\n"
                            + str(response.content)
                        )
                    try:
                        parsed = response.json()
                    except ValueError:
                        raise ConnectionError(
                            "Could not fetch data from search engine (failed to parse response), responded with\n"
                            + str(response.content)
                        )
                    if parsed.get("errors"):
                        raise ConnectionError(
                            "Could not fetch data from search engine, (errors), responded with\n"
                            + str(response.content)
                        )
    except Exception:
        raise ApiConnectionError("get_index_definition", response, client)
    return parsed


async def asyncio(
    timeout: Optional[float] = 30.0, client: Optional[Client] = None
) -> dict:
    """
    # Get asynchronously the search index definition (mapping + settings).

    ## Arguments
    - `timeout`: The timeout for the connection to the search engine. Can be set to "None" for no enforced timeout.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    The raw dictionary response from OpenSearch, containing the entire mapping definition.

    ## Raises
    - `ApiConnectionError`: If the query was unsuccessful.
    """
    if not client:
        client = get_default_client()
    endpoint_url = f"{client.get_base_url_v1()}/api/v1/search_api/{client.ontology}/_index_definition"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {client.token}",
        "x-ontology": client.ontology,
    }
    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                async with httpx.AsyncClient() as httpx_client:
                    response = await httpx_client.get(
                        endpoint_url, headers=headers, timeout=timeout
                    )
                    if response.status_code != 200:
                        raise ConnectionError(
                            f"Could not fetch data from search engine (status code {response.status_code}), responded with\n"
                            + str(response.content)
                        )
                    try:
                        parsed = response.json()
                    except ValueError:
                        raise ConnectionError(
                            "Could not fetch data from search engine (failed to parse response), responded with\n"
                            + str(response.content)
                        )
                    if parsed.get("errors"):
                        raise ConnectionError(
                            "Could not fetch data from search engine, (errors), responded with\n"
                            + str(response.content)
                        )
    except Exception:
        raise ApiConnectionError("get_index_definition", response, client)
    return parsed
