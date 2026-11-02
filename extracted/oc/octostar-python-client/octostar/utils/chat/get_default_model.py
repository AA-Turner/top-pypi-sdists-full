from typing import Optional
from ...client import Client
from . import list_models


def _get_default_model_from_list(models):
    default_model = list(filter(lambda x: x.get("is_default") == True, models))
    if len(default_model) != 1:
        raise ValueError(f"Found {len(default_model)} default models instead of 1")
    return default_model[0]


def sync(
    client: Optional[Client] = None,
) -> dict:
    """
    # Get the current default AI chat model.

    ## Arguments
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    The information about the default AI model.

    ## Raises
    - `ApiConnectionError`: If the query was unsuccessful.
    - `ValueError`: If no default model is available.
    """
    models = list_models.sync(client=client)
    return _get_default_model_from_list(models)


async def asyncio(
    client: Optional[Client] = None,
) -> dict:
    """
    # Get asynchronously the current default AI chat model.

    ## Arguments
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    The information about the default AI model.

    ## Raises
    - `ApiConnectionError`: If the query was unsuccessful.
    - `ValueError`: If no default model is available.
    """
    models = await list_models.asyncio(client=client)
    return _get_default_model_from_list(models)
