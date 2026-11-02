from types import SimpleNamespace
from typing import Dict, TypedDict, Union, List, Any
import uuid
import httpx
import logging

_logger = logging.getLogger(__name__)

from ..commons import network_retry_strategy
from ...client import Client, get_default_client
from ..exceptions import ApiConnectionError, ApiValidationError

MAX_ERROR_DETAILS = 10


class _EntityBaseRequired(TypedDict):
    entity_type: str
    fields: Dict[str, Any]


class EntityBase(_EntityBaseRequired, total=False):
    os_entity_uid: str


def _raise_validation_error(
    message,
    client,
    *,
    entity_errors=None,
    missing_entity_ids=None,
    mismatched_keys=None,
):
    # status_code=200 mirrors the actual HTTP status — the server accepted
    # the request and returned a structured per-entity breakdown; the
    # failures were inside that response body, not at the transport layer.
    raise ApiValidationError(
        "upsert_entities",
        SimpleNamespace(status_code=200, content=message),
        client,
        entity_errors=entity_errors,
        missing_entity_ids=missing_entity_ids,
        mismatched_keys=mismatched_keys,
    )


def _validate_response(body, entities, data, response, client):
    expected_ids = {e["os_entity_uid"] for e in entities}
    returned_ids = {e["entity_id"] for e in data.get("entities", [])}
    errors_list = data.get("errors", [])
    error_ids = {e["entity_id"] for e in errors_list}
    accounted_ids = returned_ids | error_ids

    missing_ids = expected_ids - accounted_ids
    if missing_ids:
        missing_entities = [e for e in body if e["entity_id"] in missing_ids]
        _raise_validation_error(
            f"Entities missing from response (neither in entities nor errors): "
            f"{missing_ids}, payload: {missing_entities}",
            client,
            missing_entity_ids=missing_ids,
        )

    expected_keys = {(e["entity_id"], e["os_workspace"]) for e in body}
    returned_keys = {
        (e["entity_id"], e["os_workspace"]) for e in data.get("entities", [])
    }
    mismatched = returned_keys - expected_keys
    if mismatched:
        _raise_validation_error(
            f"Returned entities have unexpected (entity_id, os_workspace) keys "
            f"(possibly stale records): {mismatched}",
            client,
            mismatched_keys=list(mismatched),
        )

    if errors_list:
        lines = [
            f"  {e['entity_id']}: {e['error']}" for e in errors_list[:MAX_ERROR_DETAILS]
        ]
        if len(errors_list) > MAX_ERROR_DETAILS:
            lines.append(f"  ... and {len(errors_list) - MAX_ERROR_DETAILS} more")
        _raise_validation_error(
            f"{len(errors_list)} entities failed to upsert:\n" + "\n".join(lines),
            client,
            entity_errors=errors_list,
        )

    return list({e["entity_id"]: e for e in data.get("entities", [])}.values())


def sync(
    os_workspace: Union[str, List[str]],
    entities: List[EntityBase],
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Create or update a set of local entities in a workspace

    ## Arguments
    - `os_workspace`: The workspace ID, or a list of workspace IDs (one per entity)
    - `entities`: The entities to update or create, as a list of dictionaries
        Each dictionary must contain:
        - `entity_type`: The concept name for the entity
        - `fields`: A dictionary of fields for the entity, according to the concept definition in the ontology
        Each dictionary can optionally contain:
        - `os_entity_uid`: The ID for the entity. Only necessary in case of an update
    - `ontology_name`: The name of the ontology
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    The list of created/updated entity records

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ApiValidationError`: The server accepted the request but rejected
        one or more entities. The per-entity breakdown is on the
        exception as structured attributes (see the class docstring for
        the shape of each):
        - `entity_errors`: full per-entity error rows from the server
          (``list[{"entity_id": str, "error": str}]``)
        - `missing_entity_ids`: ``set[str]`` of IDs the server returned
          no record for
        - `mismatched_keys`: ``list[(entity_id, os_workspace)]`` of
          entries returned under an unexpected workspace
        - `invalid_fields`: ``dict[entity_id, list[field_name]]`` for
          per-field rejections — drop these fields and re-upsert to
          recover
        - `reserved_keyword_entity_types`: ``set[str]`` of entity-type
          tokens flagged as reserved keywords by the query parser
        Subclass of `ApiConnectionError` for backward compatibility.
    - `ApiConnectionError`: If the transport layer failed (network error,
        non-2xx response from the upsert endpoint).
    """
    assert len(entities) > 0
    for entity in entities:
        entity["os_entity_uid"] = entity.get("os_entity_uid", None) or str(uuid.uuid4())
        if "fields" not in entity:
            entity["fields"] = dict()
    if isinstance(os_workspace, str):
        os_workspace = [os_workspace] * len(entities)
    assert len(os_workspace) == len(entities)
    if not ontology_name:
        if not client:
            client = get_default_client()
        ontology_name = client.ontology
    if ontology_name != client.ontology:
        raise NotImplementedError(
            "This operation is currently only supported on the current ontology!"
        )
    body = [
        {
            **entities[i]["fields"],
            "entity_id": entities[i]["os_entity_uid"],
            "entity_type": entities[i]["entity_type"],
            "os_workspace": os_workspace[i],
        }
        for i in range(len(entities))
    ]
    endpoint_url = f"{client.get_base_url_v1()}/api/v1/entities/upsert"
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
                        endpoint_url, json=body, headers=headers, timeout=120
                    )
                    response.raise_for_status()
    except Exception:
        raise ApiConnectionError("upsert_entities", response, client)

    return _validate_response(body, entities, response.json(), response, client)


async def asyncio(
    os_workspace: Union[str, List[str]],
    entities: List[EntityBase],
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Create or update asynchronously a set of local entities in a workspace

    ## Arguments
    - `os_workspace`: The workspace ID, or a list of workspace IDs (one per entity)
    - `entities`: The entities to update or create, as a list of dictionaries
        Each dictionary must contain:
        - `entity_type`: The concept name for the entity
        - `fields`: A dictionary of fields for the entity, according to the concept definition in the ontology
        Each dictionary can optionally contain:
        - `os_entity_uid`: The ID for the entity. Only necessary in case of an update
    - `ontology_name`: The name of the ontology
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    The list of created/updated entity records

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ApiValidationError`: The server accepted the request but rejected
        one or more entities. The per-entity breakdown is on the
        exception as structured attributes (see the class docstring for
        the shape of each):
        - `entity_errors`: full per-entity error rows from the server
          (``list[{"entity_id": str, "error": str}]``)
        - `missing_entity_ids`: ``set[str]`` of IDs the server returned
          no record for
        - `mismatched_keys`: ``list[(entity_id, os_workspace)]`` of
          entries returned under an unexpected workspace
        - `invalid_fields`: ``dict[entity_id, list[field_name]]`` for
          per-field rejections — drop these fields and re-upsert to
          recover
        - `reserved_keyword_entity_types`: ``set[str]`` of entity-type
          tokens flagged as reserved keywords by the query parser
        Subclass of `ApiConnectionError` for backward compatibility.
    - `ApiConnectionError`: If the transport layer failed (network error,
        non-2xx response from the upsert endpoint).
    """
    assert len(entities) > 0
    for entity in entities:
        entity["os_entity_uid"] = entity.get("os_entity_uid", None) or str(uuid.uuid4())
        if "fields" not in entity:
            entity["fields"] = dict()
    if isinstance(os_workspace, str):
        os_workspace = [os_workspace] * len(entities)
    assert len(os_workspace) == len(entities)
    if not ontology_name:
        if not client:
            client = get_default_client()
        ontology_name = client.ontology
    if ontology_name != client.ontology:
        raise NotImplementedError(
            "This operation is currently only supported on the current ontology!"
        )
    body = [
        {
            **entities[i]["fields"],
            "entity_id": entities[i]["os_entity_uid"],
            "entity_type": entities[i]["entity_type"],
            "os_workspace": os_workspace[i],
        }
        for i in range(len(entities))
    ]
    endpoint_url = f"{client.get_base_url_v1()}/api/v1/entities/upsert"
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
                        endpoint_url, json=body, headers=headers, timeout=120
                    )
                    response.raise_for_status()
    except Exception:
        raise ApiConnectionError("upsert_entities", response, client)

    return _validate_response(body, entities, response.json(), response, client)
