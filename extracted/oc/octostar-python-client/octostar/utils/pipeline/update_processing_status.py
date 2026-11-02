"""Update processing status utility functions."""

import logging
from typing import Any, Dict, List, Optional, TypedDict, Union

_logger = logging.getLogger(__name__)

from ...api.pipeline import update_processing_status as api_update_processing_status
from ...client import Client
from ..exceptions import ApiConnectionError

APPEND_TOKEN = "$append"


class ChildProcessingStatusUpdate(TypedDict, total=False):
    """
    Type definition for a child entry inside ``fragment_errors``,
    ``fragment_warnings``, or ``warnings``.

    All fields are optional to support cases where the child entity cannot
    be fully identified (e.g. missing fragments known only by index).

    Fields:
    - ``entity_id``: The child entity UID.
    - ``entity_type``: The child entity type/concept.
    - ``entity_label``: Human-readable label for the child entity.
    - ``status_code``: e.g. "RUNNING", "COMPLETED", "FAILED", "STALE", "UNKNOWN".
    - ``reason``: Reason for the status.
    - ``timestamp``: ISO 8601 timestamp of when the entry was produced.
    """

    entity_id: Optional[str]
    entity_type: Optional[str]
    entity_label: Optional[str]
    status_code: Optional[str]
    reason: Optional[str]
    timestamp: Optional[str]


class _ProcessingStatusUpdateRequired(TypedDict):
    """Required fields for processing status updates."""

    entity_id: str
    entity_type: str
    do_not_update_before: str


class ProcessingStatusUpdate(_ProcessingStatusUpdateRequired, total=False):
    """
    Type definition for processing status updates.

    Mirrors the backend's ``ProcessingStatus`` Pydantic model. The endpoint
    performs partial updates: only the keys you set are written, all other
    persisted fields are preserved.

    Required fields on every write:

    - ``entity_id``: The entity UID.
    - ``entity_type``: The entity type/concept.
    - ``do_not_update_before``: ISO 8601 timestamp guard. If the incoming
      value is older than the stored one, the entire update for this
      entity is silently nooped.

    Recommended on every status write:

    - ``os_workspace``: UID of the workspace this entity belongs to. The
      per-workspace stats aggregation buckets by this field, so omitting
      it strands the entry from those rollups.

    Required on every fragment write (i.e. any non-root entity):

    - ``source_entity_uid``: UID of the global root the fragment belongs
      to. The recursive rollup scopes its tree fetch by this field, so
      omitting it strands the fragment outside its parent's rollup view.
    - ``os_parent_uid``: UID of the direct parent in the fragment tree.
      Pair with ``source_entity_uid``. Root entities leave both as
      ``None`` (the default).

    Other optional fields:

    - ``entity_label``: Human-readable label.
    - ``status_code``: "RUNNING", "COMPLETED", "FAILED", "STALE", or
      "UNKNOWN" (default for new entities; preserved on partial updates
      that omit it).
    - ``reason``: Reason for the status.
    - ``timestamp``: ISO 8601 timestamp annotation.
    - ``do_not_reindex_before``: ISO 8601 timestamp guard for the
      search-side reindex.
    - ``timeout``: Redis cache TTL in seconds (default: 5 minutes).
    - ``n_child_fragments``: Number of direct child fragments this entity
      declares; used by the recursive rollup to detect missing branches.

    Appendable list fields -- ``fragment_errors``, ``fragment_warnings``,
    ``warnings`` -- share identical semantics:

    - ``["$append", item1, item2]`` -> append items to the existing list
    - ``[item1, item2]``            -> replace the entire list
    - ``[]`` or ``None``            -> clear the list
    - omitted                       -> no change

    Each item is a ``ChildProcessingStatusUpdate`` (or plain dict with the
    same shape). Example:
    ``{"fragment_errors": ["$append", {"entity_id": "c1", "reason": "bad"}]}``.

    **Trust contract on read.** The persisted snapshot returned by
    ``get_processing_status`` is fully trustworthy only when
    ``status_code`` is **``COMPLETED``** or **``FAILED``** (non-stale
    terminal states). ``STALE`` is also terminal but signals an
    *unsettled* prior run -- the redeploy cleanup transitions
    stuck-partial roots to ``STALE`` so a fresh run can reprocess
    them, and whatever data is attached reflects whatever
    the previous run managed to write before being torn down. Callers
    that need a definitive answer (e.g. "is this entity finished?")
    should gate on ``status_code in {"COMPLETED", "FAILED"} + detailed_status``; treating
    ``STALE`` as authoritative will silently surface stale data.

    Internal fields (normally written by the backend rollup job, not by
    callers):

    - ``detailed_status``: Persisted recursive-rollup payload.
    - ``detailed_status_hash``: SHA-256 used by the scripted update to
      short-circuit no-op writes.
    """

    entity_label: Optional[str]
    status_code: Optional[str]
    reason: Optional[str]
    timestamp: Optional[str]
    do_not_reindex_before: Optional[str]
    timeout: Optional[int]
    n_child_fragments: Optional[int]
    source_entity_uid: Optional[str]
    os_parent_uid: Optional[str]
    os_workspace: Optional[str]
    fragment_errors: Optional[
        List[Union[str, ChildProcessingStatusUpdate, Dict[str, Any]]]
    ]
    fragment_warnings: Optional[
        List[Union[str, ChildProcessingStatusUpdate, Dict[str, Any]]]
    ]
    warnings: Optional[List[Union[str, ChildProcessingStatusUpdate, Dict[str, Any]]]]
    detailed_status: Optional[Dict[str, Any]]
    detailed_status_hash: Optional[str]


_REQUIRED_KEYS = ("entity_id", "entity_type", "do_not_update_before")


def _validate(statuses: List[Union[ProcessingStatusUpdate, Dict[str, Any]]]) -> None:
    for status in statuses:
        for key in _REQUIRED_KEYS:
            if key not in status:
                raise ValueError(f"Each status must have a '{key}' field")
            value = status[key]  # type: ignore[literal-required]
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Each status's '{key}' must be a non-empty string")


def sync(
    statuses: List[Union[ProcessingStatusUpdate, Dict[str, Any]]],
    client: Client = None,
) -> Dict[str, Any]:
    """
    Update the processing status for a list of entities.

    Only provided fields are updated; existing fields are preserved unless
    explicitly set (e.g. an empty list ``[]`` clears an appendable list,
    ``None`` clears a scalar where the backend allows it).

    Args:
        statuses: List of status updates. See :class:`ProcessingStatusUpdate`
            for the full set of supported keys, including the ``$append``
            semantics for ``fragment_errors`` / ``fragment_warnings`` /
            ``warnings`` and the fragment-write contract
            (``source_entity_uid`` + ``os_parent_uid`` required for any
            non-root entity). At minimum each dict must contain:

            - ``entity_id`` (str): The entity UID.
            - ``entity_type`` (str): The entity type/concept.
            - ``do_not_update_before`` (str): ISO 8601 timestamp guard;
              older incoming values cause the whole entry to be nooped.

            See also :func:`get_processing_status` for the trust
            contract on what reads back as authoritative
            (``COMPLETED`` / ``FAILED`` only -- ``STALE`` is terminal
            but signals an unsettled prior run).
        client: The Client with which to connect to Octostar. If None, the default is used.

    Returns:
        Response dict with ``status``, ``message``, ``count``,
        ``skipped_entity_ids``, and ``errors``. The ``errors`` list
        contains per-entity dicts with ``entity_id``, ``type``, and
        ``detail`` for any entities that failed.

    Raises:
        ApiConnectionError: If the request was unsuccessful.
        ValueError: If any status is missing one of the required
            identity fields (``entity_id``, ``entity_type``,
            ``do_not_update_before``) or sets it to an empty string.
    """
    if not statuses:
        return {
            "status": "success",
            "message": "No statuses to update",
            "count": 0,
            "skipped_entity_ids": [],
            "errors": [],
        }
    _validate(statuses)
    json_body = [dict(s) for s in statuses]
    response = api_update_processing_status.sync_detailed(
        json_body=json_body, client=client
    )
    if response.status_code != 200:
        raise ApiConnectionError("update_processing_status", response, client)
    return response.parsed or {
        "status": "success",
        "count": len(statuses),
        "skipped_entity_ids": [],
        "errors": [],
    }


async def asyncio(
    statuses: List[Union[ProcessingStatusUpdate, Dict[str, Any]]],
    client: Client = None,
) -> Dict[str, Any]:
    """
    Update the processing status for a list of entities (async).

    Only provided fields are updated; existing fields are preserved unless
    explicitly set (e.g. an empty list ``[]`` clears an appendable list,
    ``None`` clears a scalar where the backend allows it).

    Args:
        statuses: List of status updates. See :class:`ProcessingStatusUpdate`
            for the full set of supported keys, including the ``$append``
            semantics for ``fragment_errors`` / ``fragment_warnings`` /
            ``warnings`` and the fragment-write contract
            (``source_entity_uid`` + ``os_parent_uid`` required for any
            non-root entity). At minimum each dict must contain:

            - ``entity_id`` (str): The entity UID.
            - ``entity_type`` (str): The entity type/concept.
            - ``do_not_update_before`` (str): ISO 8601 timestamp guard;
              older incoming values cause the whole entry to be nooped.

            See also :func:`get_processing_status` for the trust
            contract on what reads back as authoritative
            (``COMPLETED`` / ``FAILED`` only -- ``STALE`` is terminal
            but signals an unsettled prior run).
        client: The Client with which to connect to Octostar. If None, the default is used.

    Returns:
        Response dict with ``status``, ``message``, ``count``,
        ``skipped_entity_ids``, and ``errors``. The ``errors`` list
        contains per-entity dicts with ``entity_id``, ``type``, and
        ``detail`` for any entities that failed.

    Raises:
        ApiConnectionError: If the request was unsuccessful.
        ValueError: If any status is missing one of the required
            identity fields (``entity_id``, ``entity_type``,
            ``do_not_update_before``) or sets it to an empty string.
    """
    if not statuses:
        return {
            "status": "success",
            "message": "No statuses to update",
            "count": 0,
            "skipped_entity_ids": [],
            "errors": [],
        }
    _validate(statuses)
    json_body = [dict(s) for s in statuses]
    response = await api_update_processing_status.asyncio_detailed(
        json_body=json_body, client=client
    )
    if response.status_code != 200:
        raise ApiConnectionError("update_processing_status", response, client)
    return response.parsed or {
        "status": "success",
        "count": len(statuses),
        "skipped_entity_ids": [],
        "errors": [],
    }
