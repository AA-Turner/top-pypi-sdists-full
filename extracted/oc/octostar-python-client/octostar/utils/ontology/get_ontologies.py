import logging

_logger = logging.getLogger(__name__)

from ...api.ontology import get_ontologies
from ...client import Client
from ..exceptions import ApiConnectionError


def sync(client: Client = None):
    """
    # Query Ontology List

    Retrieves the list of ontologies.

    ## Arguments
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A list of strings, the names of the ontologies.

    ## Raises
    - `ApiConnectionError`: If the query was unsuccessful.
    """
    response = get_ontologies.sync_detailed(client=client)
    if response.status_code != 200:
        raise ApiConnectionError("get_ontologies", response, client)
    content = response.parsed
    if "status" in content and content["status"] != "success":
        raise ApiConnectionError("get_ontologies", response, client)
    return response.parsed["data"]


async def asyncio(client: Client = None):
    """
    # Query Ontology List Asynchronously

    Asynchronously retrieves the list of ontologies.

    ## Arguments
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A list of strings, the names of the ontologies.

    ## Raises
    - `ApiConnectionError`: If the query was unsuccessful.
    """
    response = await get_ontologies.asyncio_detailed(client=client)
    if response.status_code != 200:
        raise ApiConnectionError("get_ontologies", response, client)
    content = response.parsed
    if "status" in content and content["status"] != "success":
        raise ApiConnectionError("get_ontologies", response, client)
    return response.parsed["data"]
