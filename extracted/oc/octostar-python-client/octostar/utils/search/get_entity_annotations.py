"""Thin wrapper around the server-side annotations endpoint.

All heavy lifting (fragment type resolution, DFS tree building, merge logic,
pagination) is handled by the ``POST /v1/search_api/{ontology}/annotations``
server-side endpoint.  This module simply POSTs and returns the result.
"""

import logging
import httpx
from typing import Any, Dict, List, Optional

try:
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore[assignment]

from ...client import Client, get_default_client
from ...api.search.get_annotations import _build_body
from ..commons import network_retry_strategy
from ..exceptions import ApiConnectionError

logger = logging.getLogger(__name__)

_FRAGMENT_BATCH_SIZE = 10000


class MergeKwargs(TypedDict, total=False):
    """Tunables for the server-side fragment merge step (``merge=True``).

    Declared ``total=False`` so callers can provide any subset of fields;
    missing keys fall back to server defaults. New merge options can be
    added here without changing the function signature.

    Fields:
    - ``inline_inserts``: When True (default on the server), insert-type
      fragments (e.g. embedded images) are wrapped with a contextual marker
      and included in the merged text. When False, insert-type fragments
      are excluded from the merge entirely. Only meaningful when
      ``merge=True``.
    """

    inline_inserts: bool


def _post_annotations(
    client: Client,
    body: Dict[str, Any],
    timeout: Optional[float],
) -> Dict[str, Any]:
    url = f"{client.get_base_url_v1()}/api/v1/search_api/{client.ontology}/annotations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {client.token}",
        "x-ontology": client.ontology,
    }
    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                with httpx.Client() as hc:
                    response = hc.post(
                        url,
                        json=body,
                        headers=headers,
                        timeout=timeout,
                    )
                    if response.status_code != 200:
                        raise ConnectionError(
                            f"annotations endpoint returned {response.status_code}: "
                            + f"{response.text[:500]}"
                        )
                    payload = response.json()
                    resp_errors = payload.get("errors")
                    if resp_errors:
                        logger.warning(
                            "annotations endpoint returned non-fatal warnings: %s",
                            "; ".join(resp_errors),
                        )
                    return payload["data"]
    except ConnectionError:
        raise ApiConnectionError("get_entity_annotations", response, client)
    except Exception:
        raise ApiConnectionError("get_entity_annotations", response, client)
    return {}


async def _post_annotations_async(
    client: Client,
    body: Dict[str, Any],
    timeout: Optional[float],
) -> Dict[str, Any]:
    url = f"{client.get_base_url_v1()}/api/v1/search_api/{client.ontology}/annotations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {client.token}",
        "x-ontology": client.ontology,
    }
    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                async with httpx.AsyncClient() as hc:
                    response = await hc.post(
                        url,
                        json=body,
                        headers=headers,
                        timeout=timeout,
                    )
                    if response.status_code != 200:
                        raise ConnectionError(
                            f"annotations endpoint returned {response.status_code}: "
                            + f"{response.text[:500]}"
                        )
                    payload = response.json()
                    resp_errors = payload.get("errors")
                    if resp_errors:
                        logger.warning(
                            "annotations endpoint returned non-fatal warnings: %s",
                            "; ".join(resp_errors),
                        )
                    return payload["data"]
    except ConnectionError:
        raise ApiConnectionError("get_entity_annotations", response, client)
    except Exception:
        raise ApiConnectionError("get_entity_annotations", response, client)
    return {}


def sync(
    os_entity_uids: List[str],
    fields: Optional[List[str]] = None,
    timeout: Optional[float] = 30.0,
    client: Optional[Client] = None,
    recurse: bool = True,
    merge: bool = True,
    max_fragments: Optional[int] = _FRAGMENT_BATCH_SIZE,
    fragment_filter: Optional[Dict[str, Any]] = None,
    include_record: bool = False,
    collapse: bool = True,
    merge_kwargs: Optional[MergeKwargs] = None,
):
    """# Get the annotations associated with one or more entities.

    ## Arguments
    - `os_entity_uids`: A list of entity IDs.
    - `fields`: A list of annotations fields to fetch, or "None" for all
      annotations.  Nested fields can be specified with ".".
    - `timeout`: The timeout for the connection to the search engine.  Can be
      set to "None" for no enforced timeout.
    - `client`: The Client with which to connect to Octostar.  If None, the
      default one is used.
    - `recurse`: If True, also fetches annotations from fragment documents whose
      `document_fields.source_entity_uid` matches the **root file** for each
      input.  For a fragment input that root comes from `source_entity_uid`;
      for a non-fragment from `os_entity_uid`.  Fragment subtrees are ordered via
      `document_fields.os_parent_uid` and `fragment_index`.
    - `merge`: Only meaningful when `recurse=True`.  If True, fragment
      annotations are merged into the parent's annotations using
      `_MERGE_STRATEGY` and the return shape is `{entity_id: annotations}`.
      If False, all annotations (parent and fragments) are returned as-is
      in DFS tree order and the return shape is
      `{entity_id: {doc_id: annotations}}` where the first key is the
      input entity followed by fragment IDs.
    - `max_fragments`: Maximum number of fragment documents to fetch.  Defaults
      to 10 000.  Set to ``None`` to fetch all fragments (paginated
      automatically in batches of 10 000).
    - `fragment_filter`: Optional raw OpenSearch query DSL clause applied to the
      fragment query.  Only fragments matching this filter (and their subtrees)
      are included in the result.
    - `include_record`: When True, each entry includes the document_fields
      (flattened) alongside a ``#annotations`` key.  When False (default), each
      entry is the annotations dict directly (backwards-compatible).
    - `collapse`: Only meaningful when ``merge=True``.  When True (default),
      all fragment annotations are collapsed into a single entry per entity.
      When False, each fragment's subtree is merged into that fragment but all
      fragments are returned (same shape as ``merge=False``).
    - `merge_kwargs`: Options that tune the merge step. Only applied when
      ``merge=True``.  Pass as a ``MergeKwargs`` dict, e.g.
      ``{"inline_inserts": False}``.  See :class:`MergeKwargs` for the
      supported fields.  Grouped so new knobs can be added without changing
      this function's signature.

    ## Returns
    When `include_record=False` (default):
      - `recurse=False` or (`merge=True` and `collapse=True`):
        ``{entity_id: annotations_dict}``
      - `recurse=True` and (`merge=False` or `collapse=False`):
        ``{entity_id: {doc_id: annotations_dict}}``

    When `include_record=True`:
      - `recurse=False` or (`merge=True` and `collapse=True`):
        ``{entity_id: {**document_fields, "#annotations": annotations_dict}}``
      - `recurse=True` and (`merge=False` or `collapse=False`):
        ``{entity_id: {doc_id: {**document_fields, "#annotations": annotations_dict}}}``

    ## Raises
    - `ApiConnectionError`: If the query for annotations was unsuccessful.
    """
    if not client:
        client = get_default_client()
    if not os_entity_uids:
        return {}

    body = _build_body(
        os_entity_uids,
        fields,
        recurse,
        merge,
        max_fragments,
        fragment_filter,
        include_record,
        collapse,
        merge_kwargs,
    )
    return _post_annotations(client, body, timeout)


async def asyncio(
    os_entity_uids: List[str],
    fields: Optional[List[str]] = None,
    timeout: Optional[float] = 30.0,
    client: Optional[Client] = None,
    recurse: bool = True,
    merge: bool = True,
    max_fragments: Optional[int] = _FRAGMENT_BATCH_SIZE,
    fragment_filter: Optional[Dict[str, Any]] = None,
    include_record: bool = False,
    collapse: bool = True,
    merge_kwargs: Optional[MergeKwargs] = None,
):
    """# Get asynchronously the annotations associated with one or more entities.

    ## Arguments
    - `os_entity_uids`: A list of entity IDs.
    - `fields`: A list of annotations fields to fetch, or "None" for all
      annotations.  Nested fields can be specified with ".".
    - `timeout`: The timeout for the connection to the search engine.  Can be
      set to "None" for no enforced timeout.
    - `client`: The Client with which to connect to Octostar.  If None, the
      default one is used.
    - `recurse`: If True, also fetches annotations from fragment documents whose
      `document_fields.source_entity_uid` matches the **root file** for each
      input.  For a fragment input that root comes from `source_entity_uid`;
      for a non-fragment from `os_entity_uid`.  Fragment subtrees are ordered via
      `document_fields.os_parent_uid` and `fragment_index`.
    - `merge`: Only meaningful when `recurse=True`.  If True, fragment
      annotations are merged into the parent's annotations using
      `_MERGE_STRATEGY` and the return shape is `{entity_id: annotations}`.
      If False, all annotations (parent and fragments) are returned as-is
      in DFS tree order and the return shape is
      `{entity_id: {doc_id: annotations}}` where the first key is the
      input entity followed by fragment IDs.
    - `max_fragments`: Maximum number of fragment documents to fetch.  Defaults
      to 10 000.  Set to ``None`` to fetch all fragments (paginated
      automatically in batches of 10 000).
    - `fragment_filter`: Optional raw OpenSearch query DSL clause applied to the
      fragment query.  Only fragments matching this filter (and their subtrees)
      are included in the result.
    - `include_record`: When True, each entry includes the document_fields
      (flattened) alongside a ``#annotations`` key.  When False (default), each
      entry is the annotations dict directly (backwards-compatible).
    - `collapse`: Only meaningful when ``merge=True``.  When True (default),
      all fragment annotations are collapsed into a single entry per entity.
      When False, each fragment's subtree is merged into that fragment but all
      fragments are returned (same shape as ``merge=False``).
    - `merge_kwargs`: Options that tune the merge step. Only applied when
      ``merge=True``.  Pass as a ``MergeKwargs`` dict, e.g.
      ``{"inline_inserts": False}``.  See :class:`MergeKwargs` for the
      supported fields.  Grouped so new knobs can be added without changing
      this function's signature.

    ## Returns
    When `include_record=False` (default):
      - `recurse=False` or (`merge=True` and `collapse=True`):
        ``{entity_id: annotations_dict}``
      - `recurse=True` and (`merge=False` or `collapse=False`):
        ``{entity_id: {doc_id: annotations_dict}}``

    When `include_record=True`:
      - `recurse=False` or (`merge=True` and `collapse=True`):
        ``{entity_id: {**document_fields, "#annotations": annotations_dict}}``
      - `recurse=True` and (`merge=False` or `collapse=False`):
        ``{entity_id: {doc_id: {**document_fields, "#annotations": annotations_dict}}}``

    ## Raises
    - `ApiConnectionError`: If the query for annotations was unsuccessful.
    """
    if not client:
        client = get_default_client()
    if not os_entity_uids:
        return {}

    body = _build_body(
        os_entity_uids,
        fields,
        recurse,
        merge,
        max_fragments,
        fragment_filter,
        include_record,
        collapse,
        merge_kwargs,
    )
    return await _post_annotations_async(client, body, timeout)
