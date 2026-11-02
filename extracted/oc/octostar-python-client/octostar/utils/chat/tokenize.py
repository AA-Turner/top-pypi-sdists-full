import httpx
from typing import Optional
from ...client import Client, get_default_client
from ..exceptions import ApiConnectionError
from typing import Optional
from ..commons import network_retry_strategy


def _prepare_tokenize_request(client, text, model_name):
    endpoint_url = f"{client.get_base_url_v1()}/api/v2/ai/llm/tokenize"
    headers = {
        "Authorization": f"Bearer {client.token}",
        "x-ontology": client.ontology,
    }
    return {
        "url": endpoint_url,
        "headers": headers,
        "timeout": 60,
        "json": {
            "text": text,
            "model_name": model_name,
        },
    }


def sync(
    text: str,
    model_name: str,
    client: Optional[Client] = None,
) -> list[int]:
    """
    # Tokenize a string into a list of LLM tokens.

    ## Arguments
    - `text`: The input string to tokenize.
    - `model_name`: The model with which to tokenize the input text.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A list of tokens.

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
                    response = httpx_client.post(
                        **_prepare_tokenize_request(client, text, model_name)
                    )
                    response.raise_for_status()
                try:
                    response = response.json()["tokens"]
                except Exception as e:
                    raise ConnectionError(
                        f"Unparsable response format {response.content} with exception {e}"
                    )
    except Exception:
        raise ApiConnectionError("tokenize", response, client)
    return response  # pyright: ignore[reportReturnType]


async def asyncio(
    text: str,
    model_name: str,
    client: Optional[Client] = None,
) -> list[int]:
    """
    # Tokenize a string into a list of LLM tokens.

    ## Arguments
    - `text`: The input string to tokenize.
    - `model_name`: The model with which to tokenize the input text.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A list of tokens.

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
                    response = await httpx_client.post(
                        **_prepare_tokenize_request(client, text, model_name)
                    )
                    response.raise_for_status()
                try:
                    response = response.json()["tokens"]
                except Exception as e:
                    raise ConnectionError(
                        f"Unparsable response format {response.content} with exception {e}"
                    )
    except Exception:
        raise ApiConnectionError("tokenize", response, client)
    return response  # pyright: ignore[reportReturnType]
