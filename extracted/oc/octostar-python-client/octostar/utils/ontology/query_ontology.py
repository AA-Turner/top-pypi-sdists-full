"""
# General SQL queries on one ontology
Use this to query your ontology for entities or data. The syntax is based on timbr/SQL. For more information, see the "fusion centre" documentation.

Example of a query:
```sql
SELECT * FROM os_thing WHERE os_workspace = 'my_workspace';
```

"""

import os
import json
import logging
from typing import List, Dict, Optional, Any, Union

from ...api.ontology import query
from ...models.query_json_body import QueryJsonBody
from ...client import Client, get_default_client
from ..exceptions import ApiConnectionError

_logger = logging.getLogger(__name__)
_CONTEXT_NAME = "query_ontology"


def _process_query_response(
    response, sql_query: str, client: Client
) -> Optional[List[Dict[str, Any]]]:
    if response is None:
        _logger.error(f"{_CONTEXT_NAME}: Response is None for query {sql_query}")
        return None

    # Check if content exists
    if not hasattr(response, "content") or response.content is None:
        _logger.error(
            f"{_CONTEXT_NAME}: No content available in response for query {sql_query}"
        )
        raise ApiConnectionError(_CONTEXT_NAME, response, client)

    # Log the raw response content
    _logger.debug(
        f"{_CONTEXT_NAME}: Response content for query {sql_query}: {response.content}"
    )

    # Check response status code
    if (
        hasattr(response, "status_code")
        and response.status_code
        and response.status_code.value != 200
    ):
        _logger.error(
            f"{_CONTEXT_NAME}: Failed with status code {response.status_code.value} for query {sql_query}"
        )
        raise ApiConnectionError(_CONTEXT_NAME, response, client)

    response_content = response.content

    # Handle empty content
    if not response_content:
        _logger.error(
            f"{_CONTEXT_NAME}: Empty content in response for query {sql_query}"
        )
        raise ApiConnectionError(_CONTEXT_NAME, response, client)

    # Handle the case where response_content is already a dictionary
    if isinstance(response_content, dict):
        content = response_content
    else:
        try:
            # If it's a string, try to parse as JSON
            if isinstance(response_content, str):
                content = json.loads(response_content)
            elif isinstance(response_content, bytes):
                content = json.loads(response_content.decode("utf-8"))
            else:
                _logger.error(
                    f"{_CONTEXT_NAME}: Unexpected response content type: {type(response_content)}"
                )
                raise ValueError(
                    f"Unexpected response content type: {type(response_content)}"
                )
        except json.JSONDecodeError as e:
            _logger.error(
                f"{_CONTEXT_NAME}: Failed to parse JSON response: %s. Content: %s",
                str(e),
                str(response_content),
            )
            raise ValueError(
                f"Invalid JSON response from API: {str(e)}. Content (truncated): {str(response_content)[:200]}"
            )

    if not content:
        _logger.error(f"{_CONTEXT_NAME}: Empty parsed content for query {sql_query}")
        raise ApiConnectionError(_CONTEXT_NAME, response, client)

    # Get detailed error information if status is not success
    if content.get("status") != "success":
        error_message = content.get("message", "Unknown error")
        error_details = content.get("error", {})

        # Construct a detailed error message
        detailed_msg = f"Request failed with status: {content.get('status')}. Message: {error_message}"
        if error_details:
            detailed_msg += f". Details: {json.dumps(error_details)}"

        _logger.error(f"{_CONTEXT_NAME}: {detailed_msg} for query {sql_query}")
        raise ApiConnectionError(_CONTEXT_NAME, response, client)

    if (
        isinstance(content, dict)
        and "data" in content
        and isinstance(content["data"], list)
    ):
        return content["data"]

    else:
        _logger.debug(
            f"{_CONTEXT_NAME}: Non-SELECT query executed successfully: %s", str(content)
        )
        return None


def sync(
    sql_query: str, ontology_name: str = None, client: Client = None
) -> Optional[List[Dict[str, Any]]]:
    """
    # Query Ontology for Entities or Data

    Executes a query on an ontology to retrieve entities or data.

    ## Arguments
    - `sql_query`: A string which is a valid timbr/SQL query.
    - `ontology_name`: The name of the ontology.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    - For SELECT queries: A list of dictionaries, each containing a result row with named columns.
      The result can be passed e.g. to pd.DataFrame().
    - For non-SELECT queries: None

    ## Raises
    - `ApiConnectionError`: If the query was unsuccessful.
    - `ValueError`: If the response cannot be properly parsed.
    """
    if not ontology_name:
        if not client:
            client = get_default_client()
        ontology_name = client.ontology
    response = query.sync_detailed(
        client=client, json_body=QueryJsonBody(query=sql_query), ontology=ontology_name
    )

    return _process_query_response(response, sql_query, client)


async def asyncio(
    sql_query: str, ontology_name: str = None, client: Client = None
) -> Optional[List[Dict[str, Any]]]:
    """
    # Query Ontology for Entities or Data Asynchronously

    Asynchronously executes a query on an ontology to retrieve entities or data.

    ## Arguments
    - `sql_query`: A string which is a valid timbr/SQL query.
    - `ontology_name`: The name of the ontology.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    - For SELECT queries: A list of dictionaries, each containing a result row with named columns.
      The result can be passed e.g. to pd.DataFrame().
    - For non-SELECT queries: None

    ## Raises
    - `ApiConnectionError`: If the query was unsuccessful.
    - `ValueError`: If the response cannot be properly parsed.
    """
    if not ontology_name:
        if not client:
            client = get_default_client()
        ontology_name = client.ontology
    response = await query.asyncio_detailed(
        client=client, json_body=QueryJsonBody(query=sql_query), ontology=ontology_name
    )

    return _process_query_response(response, sql_query, client)
