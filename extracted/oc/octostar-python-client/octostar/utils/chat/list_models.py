import httpx
from typing import Optional
from ...client import Client, get_default_client
from ..exceptions import ApiConnectionError
from typing import Optional
from ..commons import network_retry_strategy


def _prepare_list_models_request(client):
    endpoint_url = f"{client.get_base_url_v1()}/api/v1/chat/models"
    headers = {
        "Authorization": f"Bearer {client.token}",
        "x-ontology": client.ontology,
    }
    return {
        "url": endpoint_url,
        "headers": headers,
        "timeout": 60,
    }


def sync(
    client: Optional[Client] = None,
) -> list[dict]:
    """
    # List the available AI chat models.

    ## Arguments
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A list of information for each available AI model.

    ## Raises
    - `ApiConnectionError`: If the query was unsuccessful.
    """
    if not client:
        client = get_default_client()
    response = None
    try:
        for attempt in network_retry_strategy(retries=3):
            with attempt:
                with httpx.Client() as httpx_client:
                    response = httpx_client.get(**_prepare_list_models_request(client))
                    response.raise_for_status()
                try:
                    response = response.json()
                except Exception as e:
                    raise ConnectionError(
                        f"Unparsable response format {response.content} with exception {e}"
                    )
    except Exception:
        raise ApiConnectionError("list_models", response, client)
    return response


async def asyncio(
    client: Optional[Client] = None,
) -> list[dict]:
    """
    # List asynchronously the available AI chat models.

    ## Arguments
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A list of information for each available AI model.

    ## Raises
    - `ApiConnectionError`: If the query was unsuccessful.
    """
    if not client:
        client = get_default_client()
    response = None
    try:
        for attempt in network_retry_strategy(retries=3):
            with attempt:
                async with httpx.AsyncClient() as httpx_client:
                    response = await httpx_client.get(
                        **_prepare_list_models_request(client)
                    )
                    response.raise_for_status()
                try:
                    response = response.json()
                except Exception as e:
                    raise ConnectionError(
                        f"Unparsable response format {response.content} with exception {e}"
                    )
    except Exception:
        raise ApiConnectionError("list_models", response, client)
    return response
