"""
    Wrap platform calls related to model database
"""

import os
import httpx
from .sync_wrapper import sync_wrapper

ATLAS_API_BASE_URL = os.getenv("ATLAS_API_BASE_URL", "https://api.optilogic.app/v0/")

# the optilogic library has a setting for overriding the base
# url used for API calls. If this setting needs to be set, use
# this instead of the current ATLAS_API_BASE_URL
optilogic_api_url = os.getenv("OPTILOGIC_API_URL")
if optilogic_api_url:
    ATLAS_API_BASE_URL = f"{optilogic_api_url}/v0/"


async def query_storage_async(
    app_key: str, storage_name: str, api_key: str = None, bearer_token: str = None
):
    """
    Get db details
    """
    assert ATLAS_API_BASE_URL

    headers = {}

    if app_key is None and api_key is None and bearer_token is None:
        raise ValueError("No authentication was provided in query_storage_async")

    if app_key:
        headers["X-App-KEY"] = app_key

    if api_key:
        headers["X-Api-Key"] = api_key

    if bearer_token:
        headers["X-Api-Key"] = bearer_token.replace("Bearer ", "")

    url = ATLAS_API_BASE_URL.strip("/")
    url = f"{url}/storage/{storage_name}/connection-string"

    async with httpx.AsyncClient() as client:
        result = await client.get(url, headers=headers, timeout=10)

        if result.status_code != 200:
            return None

        return result.json()


query_storage = sync_wrapper(query_storage_async)


async def get_db_id_async(
    app_key: str, storage_name: str, api_key: str = None, bearer_token: str = None
):
    """
    For a given DB name, get DB ID
    """

    result = await query_storage_async(
        app_key, storage_name, api_key=api_key, bearer_token=bearer_token
    )

    if result is None:
        return None

    return result["raw"]["dbname"]


get_db_id = sync_wrapper(get_db_id_async)
