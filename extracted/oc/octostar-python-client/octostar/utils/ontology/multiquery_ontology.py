import os
import json
import sys
import logging
from typing import Optional, Union, List, Dict
from collections.abc import AsyncIterator

from ...api.ontology import multi_query
from ...models.multi_query_json_body import MultiQueryJsonBody
from ...models.multi_query_json_body_queries_item import MultiQueryJsonBodyQueriesItem
from ...client import Client
from ...types import Response
from ..exceptions import StopAsyncIterationWithResult
from ..commons import (
    sync_request,
    asyncio_request,
    streaming_request,
    FailCondition,
    ChunksEndCondition,
    ChunksFailCondition,
    streaming_get_full_content,
)

logger = logging.getLogger(__name__)


def sync(
    sql_queries: Union[List[str], Dict[str, str]],
    raise_on_missing: bool = False,
    ontology_name: str = os.getenv("OS_ONTOLOGY"),
    client: Client = None,
) -> Union[List[str], Dict[str, str]]:
    """
    Query an ontology with multiple queries (batching) for entities or data.

    Args:
        sql_queries: The queries to send, expressed either as:
            A list of strings which are valid timbr/SQL queries, OR
            A dictionary of arbitrary query IDs to valid timbr/SQL queries.
        raise_on_missing: Whether to raise a ValueError if some of the queries error out. If not set, invalid queries will correspond to None in the output.
        ontology_name: The name of the ontology.
        client: The Client with which to connect to Octostar. If None, the default one is used.
    Returns:
        A list of elements or a dictionary, as per the input.
        Each element is the result of a query expressed as a list of dictionaries,
        each containing a result row with named columns.
        The result of each query can be passed e.g. to pd.DataFrame().
        If some queries have failed, the corresponding elements are None.

    Raises:
        ApiConnectionError: If the overall query batch was unsuccessful.
        ValueError: If some queries in the batch have failed and raise_on_missing is set.
    """
    return_as_list = False
    if isinstance(sql_queries, list):
        return_as_list = True
        sql_queries = {str(i): sql_queries[i] for i in range(len(sql_queries))}
    body = MultiQueryJsonBody(
        queries=[
            MultiQueryJsonBodyQueriesItem(query_id=str(id), sql=query)
            for id, query in sql_queries.items()
        ]
    )
    fail_condition = FailCondition(callable=lambda resp: resp.status_code != 200)
    response = sync_request(
        client=client,
        module=multi_query,
        fail_condition=fail_condition,
        json_body=body,
        ontology=ontology_name,
    )
    result = [
        json.loads(r)
        for r in response.content.decode("utf-8", errors="ignore").split("\n")
        if r.strip()
    ]
    result = {r["query_id"]: r for r in result}
    error_result = {
        rk: rv
        for rk, rv in result.items()
        if "status" not in rv.keys()
        or rv["status"] != "success"
        or "data" not in rv
        or not isinstance(rv["data"], list)
    }
    if raise_on_missing and any(error_result):
        raise ValueError(
            "Some of the queries in multiquery_ontology failed! "
            + str(list(error_result.values()))
        )
    error_result = {rk: {} for rk in error_result.keys()}
    result = {**result, **error_result}
    result = {rk: rv.get("data") for rk, rv in result.items()}
    result = {**{rk: None for rk in sql_queries.keys()}, **result}
    if return_as_list:
        result = [x[1] for x in sorted(result.items(), key=lambda x: x[0])]
    return result


async def asyncio(
    sql_queries: Union[List[str], Dict[str, str]],
    raise_on_missing: bool = False,
    ontology_name: str = os.getenv("OS_ONTOLOGY"),
    client: Client = None,
) -> Union[List[str], Dict[str, str]]:
    """
    Query asynchronously an ontology with multiple queries (batching) for entities or data.

    Args:
        sql_queries: The queries to send, expressed either as:
            A list of strings which are valid timbr/SQL queries, OR
            A dictionary of arbitrary query IDs to valid timbr/SQL queries.
        raise_on_missing: Whether to raise a ValueError if some of the queries error out. If not set, invalid queries will correspond to None in the output.
        ontology_name: The name of the ontology.
        client: The Client with which to connect to Octostar. If None, the default one is used.
    Returns:
        A list of elements or a dictionary, as per the input.
        Each element is the result of a query expressed as a list of dictionaries,
        each containing a result row with named columns.
        The result of each query can be passed e.g. to pd.DataFrame().
        If some queries have failed, the corresponding elements are None.

    Raises:
        ApiConnectionError: If the overall query batch was unsuccessful.
        ValueError: If some queries in the batch have failed and raise_on_missing is set.
    """
    return_as_list = False
    if isinstance(sql_queries, list):
        return_as_list = True
        sql_queries = {str(i): sql_queries[i] for i in range(len(sql_queries))}
    body = MultiQueryJsonBody(
        queries=[
            MultiQueryJsonBodyQueriesItem(query_id=str(id), sql=query)
            for id, query in sql_queries.items()
        ]
    )
    fail_condition = FailCondition(callable=lambda resp: resp.status_code != 200)
    response = await asyncio_request(
        client=client,
        module=multi_query,
        fail_condition=fail_condition,
        json_body=body,
        ontology=ontology_name,
    )
    result = [
        json.loads(r)
        for r in response.content.decode("utf-8", errors="ignore").split("\n")
        if r.strip()
    ]
    result = {r["query_id"]: r for r in result}
    error_result = {
        rk: rv
        for rk, rv in result.items()
        if "status" not in rv.keys()
        or rv["status"] != "success"
        or "data" not in rv
        or not isinstance(rv["data"], list)
    }
    if raise_on_missing and any(error_result):
        raise ValueError(
            "Some of the queries in multiquery_ontology failed! "
            + str(list(error_result.values()))
        )
    error_result = {rk: {} for rk in error_result.keys()}
    result = {**result, **error_result}
    result = {rk: rv.get("data") for rk, rv in result.items()}
    result = {**{rk: None for rk in sql_queries.keys()}, **result}
    if return_as_list:
        result = [x[1] for x in sorted(result.items(), key=lambda x: x[0])]
    return result


async def streaming(
    sql_queries: Union[List[str], Dict[str, str]],
    raise_on_missing: bool = False,
    ontology_name: str = os.getenv("OS_ONTOLOGY"),
    client: Client = None,
    timeout: float = None,
    fail_condition: Optional[ChunksFailCondition] = None,
    end_condition: Optional[ChunksEndCondition] = None,
) -> AsyncIterator[Union[Response, Union[List[str], Dict[str, str]]]]:
    """
    Query with results streaming an ontology with multiple queries (batching) for entities or data.

    Args:
        sql_queries: The queries to send, expressed either as:
            A list of strings which are valid timbr/SQL queries, OR
            A dictionary of arbitrary query IDs to valid timbr/SQL queries.
        raise_on_missing: Whether to raise a ValueError if some of the queries error out. If not set, invalid queries will correspond to None in the output.
        ontology_name: The name of the ontology.
        client: The Client with which to connect to Octostar. If None, the default one is used.
        timeout: The amount of time after which to stop streaming results.
        fail_condition: Custom condition to determine when the stream should be considered
            failed. Receives the list of Response chunks collected so far and returns True
            to trigger an ApiConnectionError. If None, defaults to checking for non-200
            status codes (and error results when raise_on_missing is set).
        end_condition: Custom condition to determine when the stream should stop early.
            Receives the list of Response chunks collected so far and returns True to end
            the stream. If None, defaults to streaming until completion (or timeout).
    Returns:
        Return raw responses corresponding to the server's response to each query, as they come.
        Each chunk will not necessarily map to a specific query (they may be incomplete).

        Catch StopAsyncIterationWithResult() to get the final parsed result from the stream:
        a list of elements or a dictionary, as per the input.
        Each element is the result of a query expressed as a list of dictionaries,
        each containing a result row with named columns.
        The result of each query can be passed e.g. to pd.DataFrame().
        If some queries have failed or timed-out, the corresponding elements are None.

    Raises:
        ApiConnectionError: If the overall query batch was unsuccessful.
        ValueError: If some queries in the batch have failed and raise_on_missing is set.
    """

    def _process_response_chunks(chunk_resps):
        content = streaming_get_full_content(chunk_resps)
        parsed = content.decode("utf-8", errors="ignore")
        elements = [e.strip() for e in parsed.split("\n") if e.strip()]
        result = []
        for i in range(len(elements)):
            try:
                result.append(json.loads(elements[i]))
            except json.JSONDecodeError:
                break  # we reached incomplete chunks, ignore them
        result = {r["query_id"]: r for r in result}
        return result

    return_as_list = False
    if isinstance(sql_queries, list):
        return_as_list = True
        sql_queries = {str(i): sql_queries[i] for i in range(len(sql_queries))}
    body = MultiQueryJsonBody(
        queries=[
            MultiQueryJsonBodyQueriesItem(query_id=str(id), sql=query)
            for id, query in sql_queries.items()
        ]
    )
    is_error_result = (
        lambda rk, rv: "status" not in rv.keys()
        or rv["status"] != "success"
        or "data" not in rv
        or not isinstance(rv["data"], list)
    )
    if fail_condition is None:
        fail_condition = ChunksFailCondition(
            callable=lambda resps: not resps
            or resps[0].status_code != 200
            or (
                raise_on_missing
                and any(
                    is_error_result(rk, rv)
                    for rk, rv in _process_response_chunks(resps).items()
                )
            )
        )
    if end_condition is None:
        end_condition = ChunksEndCondition(callable=lambda _: False, timeout=timeout)
    elif timeout is not None:
        end_condition.timeout = timeout
    try:
        async for chunk in streaming_request(
            client=client,
            module=multi_query,
            fail_condition=fail_condition,
            end_condition=end_condition,
            json_body=body,
            ontology=ontology_name,
        ):
            yield chunk
    except StopAsyncIterationWithResult as r:
        result = r.value
        result = _process_response_chunks(result)
        error_result = {
            rk: {}
            for rk, rv in result.items()
            if "status" not in rv.keys()
            or rv["status"] != "success"
            or "data" not in rv
            or not isinstance(rv["data"], list)
        }
        result = {**result, **error_result}
        result = {rk: rv.get("data") for rk, rv in result.items()}
        result = {**{rk: None for rk in sql_queries.keys()}, **result}
        if return_as_list:
            result = [x[1] for x in sorted(result.items(), key=lambda x: x[0])]
        raise StopAsyncIterationWithResult(value=result)
