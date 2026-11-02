import httpx
from typing import Optional
from ...client import Client, get_default_client
from ..exceptions import ApiConnectionError
from ..commons import network_retry_strategy


def sync(body: str, timeout: Optional[float] = 30.0, client: Optional[Client] = None):
    """
    # Make a request for multiple searches to the search engine.

    ## Arguments
    - `body`: The body for the search request. It should be compatible with OpenSearch's _msearch body format.
        Typically, it is in newline-separated JSONs, and it will look something like:
        ```
        {"preference": "result"}
        {"query": <first_opensearch_query>}
        {"preference": "result"}
        {"query": <second_opensearch_query>}
        ...
        ```
    - `timeout`: The timeout for the connection to the search engine. Can be set to "None" for no enforced timeout.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    The raw dictionary response from OpenSearch, containing the results of all requested searches.

    ## Raises
    - `ApiConnectionError`: If the query was unsuccessful.
    """
    if not client:
        client = get_default_client()
    if not body.endswith("\n"):
        body += "\n"
    endpoint_url = (
        f"{client.get_base_url_v1()}/api/v1/search_api/{client.ontology}/_msearch"
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
                        endpoint_url, data=body, headers=headers, timeout=timeout
                    )
                    response.raise_for_status()
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
        raise ApiConnectionError("multi_search", response, client)
    return parsed


async def asyncio(
    body: str, timeout: Optional[float] = 30.0, client: Optional[Client] = None
):
    """
    # Make asynchronously a request for multiple searches to the search engine.

    ## Arguments
    - `body`: The body for the search request. It should be compatible with OpenSearch's _msearch body format.
        Typically, it is in newline-separated JSONs, and it will look something like:
        ```
        {"preference": "result"}
        {"query": <first_opensearch_query>}
        {"preference": "result"}
        {"query": <second_opensearch_query>}
        ...
        ```
    - `timeout`: The timeout for the connection to the search engine. Can be set to "None" for no enforced timeout.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    The raw dictionary response from OpenSearch, containing the results of all requested searches.

    ## Raises
    - `ApiConnectionError`: If the query was unsuccessful.
    """
    if not client:
        client = get_default_client()
    if not body.endswith("\n"):
        body += "\n"
    endpoint_url = (
        f"{client.get_base_url_v1()}/api/v1/search_api/{client.ontology}/_msearch"
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
                        endpoint_url, data=body, headers=headers, timeout=timeout
                    )
                    response.raise_for_status()
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
        raise ApiConnectionError("multi_search", response, client)
    return parsed
