"""The relation-words seam — how an AGENT TOOL gets words where a uuid is stored.

A ``relation`` column in the older user-data tables STORES a record's identifier and
MEANS that record's name. Lane OLD-TABLES-3 routed every server reader through ONE
resolver, ``matrx_records.store.relation_words``, reached through the aidream seam
``aidream/services/references/relation_words.py``. Two readers could not join them: the
``usertable_get_data`` and ``usertable_search_data`` tools live in THIS package, and
**matrx-ai must never import matrx-records** — the sibling graph is acyclic and
``matrx-records[agent]`` depends on matrx-ai, so the import would be a cycle as well as a
boundary violation (``scripts/check_package_boundaries.py``).

So the resolver is INJECTED, exactly the way every other host capability reaches this
package: the host passes ``relation_words_resolver=`` to :func:`matrx_ai.configure`, it
lands in ``_ext``, and this module reads it AT CALL TIME. The signature is deliberately
identical to the host resolver's, so the wiring is one line and never an adapter::

    async def resolver(table_id: str, rows: Sequence[Mapping[str, Any]], *,
                       user_id: str | None) -> list[dict[str, Any]]

**THE UNCONFIGURED DEFAULT IS NOT A SILENT PASS-THROUGH.** A host that never wired the
resolver still gets its page back — a missing formatter must never break a tool — but the
absence ANNOUNCES itself once, by name, with the wiring point in the message. The same
holds when an injected resolver raises: the page is returned as it stood and the failure
is logged with its traceback. A page of raw uuids reaching a model quietly is precisely
the defect this seam exists to end, and it would look identical to a working seam.
"""

from __future__ import annotations

import logging
from typing import Any, Mapping, Sequence

logger = logging.getLogger(__name__)

__all__ = ["EXT_KEY", "resolve_relation_columns"]

#: The ``_ext`` key the host's resolver is registered under.
EXT_KEY = "relation_words_resolver"

_WIRING_REMEDY = (
    "Relation cells will be shown to the model as raw record identifiers instead of the "
    "names they mean. REMEDY: wire the resolver at the host's single configuration point "
    "— aidream/package_integration.py, matrx_ai.configure(relation_words_resolver=...), "
    "pointing at aidream/services/references/relation_words.py::resolve_relation_columns."
)

#: Announce ONCE per process, not once per page: an agent loop calls these tools in a
#: tight cycle and a per-call warning would bury the sentence it is trying to deliver.
_announced: set[str] = set()


def _announce(key: str, message: str, *, exc_info: bool = False) -> None:
    if key in _announced:
        return
    _announced.add(key)
    logger.warning(message, exc_info=exc_info)


async def resolve_relation_columns(
    table_id: str,
    rows: Sequence[Mapping[str, Any]],
    *,
    user_id: str | None,
) -> list[dict[str, Any]]:
    """A page of row dicts with every relation cell already in words.

    Non-relation cells come back untouched, so a caller never branches on column type.
    """
    page = [dict(row) for row in rows]
    if not page:
        return page

    from matrx_ai._ext import get_ext, has_ext

    if not has_ext(EXT_KEY):
        _announce(
            "unconfigured",
            f"matrx-ai has no '{EXT_KEY}' configured, so relation columns of "
            f"table {table_id} are NOT resolved into words. {_WIRING_REMEDY}",
        )
        return page

    resolver = get_ext(EXT_KEY)
    try:
        resolved = await resolver(table_id, page, user_id=user_id)
    except Exception:  # noqa: BLE001 — a formatter must never break the tool
        _announce(
            "resolver_failed",
            f"the configured '{EXT_KEY}' raised while resolving table {table_id}; the "
            f"page is returned as it was stored. {_WIRING_REMEDY}",
            exc_info=True,
        )
        return page
    if resolved is None:
        _announce(
            "resolver_empty",
            f"the configured '{EXT_KEY}' answered nothing for table {table_id}; the page "
            f"is returned as it was stored. {_WIRING_REMEDY}",
        )
        return page
    return [dict(row) for row in resolved]
