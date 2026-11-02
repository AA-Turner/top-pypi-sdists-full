"""Get processing status utility functions."""

from typing import List, Dict, Any, Union
import logging

_logger = logging.getLogger(__name__)

from ...api.pipeline import get_processing_status as api_get_processing_status
from ...client import Client
from ..exceptions import ApiConnectionError


def sync(
    entity_ids: List[str],
    client: Client = None,
) -> Dict[str, Union[Dict[str, Any], None]]:
    """
    Retrieve the processing status for a list of entities.

    .. note::

        **Trust contract.** The persisted snapshot is fully trustworthy
        only when ``status_code`` is **``COMPLETED``** or **``FAILED``**
        (non-stale terminal states). Other codes carry caveats:

        - ``RUNNING`` / ``UNKNOWN``: the pipeline is still in flight; the
          data may be catching up.
        - ``STALE``: terminal but signals an *unsettled* prior run -- the
          redeploy cleanup transitions stuck-partial roots to ``STALE``
          so a fresh run can reprocess them; whatever data
          is attached reflects whatever the previous run managed to
          write before being torn down, not a settled processing status.
        - ``PARTIALLY_COMPLETED``: Sparse override
          at ``detailed_status.status_code`` whenever child fragment
          (``tree_live`` or ``remaining_floor > 0``); when the override is
          absent, callers should treat the parent's ``status_code`` as the
          effective value:
          ``detailed_status.status_code or status_code``.

        Callers that need a definitive answer (e.g. "is this entity
        finished?") should gate on
        ``status_code in {"COMPLETED", "FAILED"} plus detailed_status lookup``.

    Args:
        entity_ids: List of entity UIDs to get processing status for.
        client: The Client with which to connect to Octostar. If None, the default is used.

    Returns:
        A dictionary mapping entity IDs to their processing status information.
        Each status mirrors the backend's stored ``processing_status``
        document and may contain:

        - ``entity_id``: The entity UID.
        - ``entity_type``: The entity type/concept.
        - ``entity_label``: Human-readable label.
        - ``status_code``: "RUNNING", "COMPLETED", "FAILED", "STALE", or
          "UNKNOWN".
        - ``reason``: Reason for the status.
        - ``timestamp``: When the status was last updated.
        - ``do_not_reindex_before``: ISO 8601 timestamp guard for reindex.
        - ``do_not_update_before``: ISO 8601 timestamp; older incoming
          writes are silently nooped.
        - ``timeout``: Redis cache TTL in seconds.
        - ``n_child_fragments``: Number of direct child fragments declared.
        - ``source_entity_uid``: UID of the global root (``None`` for
          global roots).
        - ``os_parent_uid``: UID of the direct parent (``None`` for global
          roots).
        - ``os_workspace``: UID of the workspace.
        - ``fragment_errors``: List of child error dicts.
        - ``fragment_warnings``: List of child warning dicts.
        - ``warnings``: List of entity-level warning dicts.
        - ``detailed_status``: Persisted recursive-rollup payload. Always
          returned in-line for entities the debounced rollup job has
          visited. Fields:

          - ``total_indexed`` (int): docs visited by the aggregation.
          - ``total_terminal`` (int): visited docs in a terminal status.
          - ``total_running`` (int): visited docs not yet terminal.
          - ``total_missing`` (int): sum over visited parents of
            ``max(0, n_child_fragments - actual_children_indexed)``;
            counts children declared by a parent but never indexed.
          - ``total_failed`` (int): visited docs in a terminal status that
            isn't COMPLETED (i.e. FAILED or STALE).
          - ``known_floor`` (int): lower bound on eventual tree size.
          - ``remaining_floor`` (int): ``max(0, known_floor - total_terminal)``.
          - ``fully_complete`` (bool): fixpoint completion on the visited snapshot.
          - ``tree_live`` (bool): at least one non-terminal node present.
          - ``has_missing_branches`` (bool): orphan children or declared shortfall.
          - ``partial`` (bool): visit cap hit or query error; annotates trust and
            does NOT veto ``fully_complete``.
          - ``status_code`` (str, optional): sparse rollup-effective status
            override. Set only when it differs from the parent's
            ``status_code`` -- in practice, only ``"PARTIALLY_COMPLETED"``
            ever appears here (when the rollup is unsettled for a
            ``COMPLETED`` parent). Consumers should compute the effective
            status as
            ``detailed_status.status_code or status_code`` so a missing
            override falls through to the parent value.

        - ``detailed_status_hash``: SHA-256 of ``detailed_status``.

        If an entity has no processing status, its value will be None.

    Raises:
        ApiConnectionError: If the request was unsuccessful on the server.
    """
    response = api_get_processing_status.sync_detailed(
        entity_ids=entity_ids, client=client
    )

    if response.status_code != 200:
        raise ApiConnectionError("get_processing_status", response, client)

    parsed = response.parsed
    if parsed is None:
        return {eid: None for eid in entity_ids}

    return parsed.get("data", {})


async def asyncio(
    entity_ids: List[str],
    client: Client = None,
) -> Dict[str, Union[Dict[str, Any], None]]:
    """
    Retrieve the processing status for a list of entities (async).

    .. note::

        **Trust contract.** The persisted snapshot is fully trustworthy
        only when ``status_code`` is **``COMPLETED``** or **``FAILED``**
        (non-stale terminal states). Other codes carry caveats:

        - ``RUNNING`` / ``UNKNOWN``: the pipeline is still in flight; the
          data may be catching up.
        - ``STALE``: terminal but signals an *unsettled* prior run -- the
          redeploy cleanup transitions stuck-partial roots to ``STALE``
          so a fresh run can reprocess them; whatever data
          is attached reflects whatever the previous run managed to
          write before being torn down, not a settled processing status.
        - ``PARTIALLY_COMPLETED``: synthetic value. It never appears as the
          parent ``status_code`` (the doc is stored as ``COMPLETED`` with an
          unsettled ``detailed_status``). It does appear as a sparse override
          at ``detailed_status.status_code`` whenever the rollup is unsettled
          (``tree_live`` or ``remaining_floor > 0``); when the override is
          absent, callers should treat the parent's ``status_code`` as the
          effective value:
          ``detailed_status.status_code or status_code``.

        Callers that need a definitive answer (e.g. "is this entity
        finished?") should gate on
        ``status_code in {"COMPLETED", "FAILED"} plus detailed_status lookup``.

    Args:
        entity_ids: List of entity UIDs to get processing status for.
        client: The Client with which to connect to Octostar. If None, the default is used.

    Returns:
        A dictionary mapping entity IDs to their processing status information.
        Each status mirrors the backend's stored ``processing_status``
        document and may contain:

        - ``entity_id``: The entity UID.
        - ``entity_type``: The entity type/concept.
        - ``entity_label``: Human-readable label.
        - ``status_code``: "RUNNING", "COMPLETED", "FAILED", "STALE", or
          "UNKNOWN".
        - ``reason``: Reason for the status.
        - ``timestamp``: When the status was last updated.
        - ``do_not_reindex_before``: ISO 8601 timestamp guard for reindex.
        - ``do_not_update_before``: ISO 8601 timestamp; older incoming
          writes are silently nooped.
        - ``timeout``: Redis cache TTL in seconds.
        - ``n_child_fragments``: Number of direct child fragments declared.
        - ``source_entity_uid``: UID of the global root (``None`` for
          global roots).
        - ``os_parent_uid``: UID of the direct parent (``None`` for global
          roots).
        - ``os_workspace``: UID of the workspace.
        - ``fragment_errors``: List of child error dicts.
        - ``fragment_warnings``: List of child warning dicts.
        - ``warnings``: List of entity-level warning dicts.
        - ``detailed_status``: Persisted recursive-rollup payload. Always
          returned in-line for entities the debounced rollup job has
          visited. Fields:

          - ``total_indexed`` (int): docs visited by the aggregation.
          - ``total_terminal`` (int): visited docs in a terminal status.
          - ``total_running`` (int): visited docs not yet terminal.
          - ``total_missing`` (int): sum over visited parents of
            ``max(0, n_child_fragments - actual_children_indexed)``;
            counts children declared by a parent but never indexed.
          - ``total_failed`` (int): visited docs in a terminal status that
            isn't COMPLETED (i.e. FAILED or STALE).
          - ``known_floor`` (int): lower bound on eventual tree size.
          - ``remaining_floor`` (int): ``max(0, known_floor - total_terminal)``.
          - ``fully_complete`` (bool): fixpoint completion on the visited snapshot.
          - ``tree_live`` (bool): at least one non-terminal node present.
          - ``has_missing_branches`` (bool): orphan children or declared shortfall.
          - ``partial`` (bool): visit cap hit or query error; annotates trust and
            does NOT veto ``fully_complete``.
          - ``status_code`` (str, optional): sparse rollup-effective status
            override. Set only when it differs from the parent's
            ``status_code`` -- in practice, only ``"PARTIALLY_COMPLETED"``
            ever appears here (when the rollup is unsettled for a
            ``COMPLETED`` parent). Consumers should compute the effective
            status as
            ``detailed_status.status_code or status_code`` so a missing
            override falls through to the parent value.

        - ``detailed_status_hash``: SHA-256 of ``detailed_status``.

        If an entity has no processing status, its value will be None.

    Raises:
        ApiConnectionError: If the request was unsuccessful on the server.
    """
    response = await api_get_processing_status.asyncio_detailed(
        entity_ids=entity_ids, client=client
    )

    if response.status_code != 200:
        raise ApiConnectionError("get_processing_status", response, client)

    parsed = response.parsed
    if parsed is None:
        return {eid: None for eid in entity_ids}

    return parsed.get("data", {})
