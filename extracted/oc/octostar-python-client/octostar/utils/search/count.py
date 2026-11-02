import httpx
from typing import Optional
from ...client import Client, get_default_client
from ..commons import network_retry_strategy
from ..exceptions import ApiConnectionError


def sync(body: dict, timeout: Optional[float] = 30.0, client: Optional[Client] = None):
    """
    # Make a request for a count query to the search engine.

    ## Arguments
    - `body`: The body for the search request. It should be compatible with OpenSearch's _count body format.
    - `timeout`: The timeout for the connection to the search engine. Can be set to "None" for no enforced timeout.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    The raw dictionary response from OpenSearch, containing the requested count.

    ## Raises
    - `ApiConnectionError`: If the query was unsuccessful.
    """
    if not client:
        client = get_default_client()
    endpoint_url = (
        f"{client.get_base_url_v1()}/api/v1/search_api/{client.ontology}/_count"
    )
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
                    response = httpx_client.post(
                        endpoint_url, json=body, headers=headers, timeout=timeout
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
        raise ApiConnectionError("count", response, client)
    return parsed


async def asyncio(
    body: dict, timeout: Optional[float] = 30.0, client: Optional[Client] = None
):
    """
    # Make asynchronously a request for a count query to the search engine.

    ## Arguments
    - `body`: The body for the search request. It should be compatible with OpenSearch's _count body format.
    - `timeout`: The timeout for the connection to the search engine. Can be set to "None" for no enforced timeout.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    The raw dictionary response from OpenSearch, containing the requested count.

    ## Raises
    - `ApiConnectionError`: If the query was unsuccessful.
    """
    if not client:
        client = get_default_client()
    endpoint_url = (
        f"{client.get_base_url_v1()}/api/v1/search_api/{client.ontology}/_count"
    )
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
                    response = await httpx_client.post(
                        endpoint_url, json=body, headers=headers, timeout=timeout
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
        raise ApiConnectionError("count", response, client)
    return parsed
