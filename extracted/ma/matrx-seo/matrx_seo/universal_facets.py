"""THE universal (no-site) classification read for a keyword.

The 13 universal facts a keyword carries with no site in context live in the
fact store ``seo.keyword_facet`` (``site_id IS NULL``), with their provenance.
``seo.keyword_universal_facet`` is the canonical VIEW over it: one row per
keyword, the 13 dimensions as columns, resolved with the same source
precedence every other resolver uses (pinned > human > import >
matcher/rule/pack > classifier).

WHY THIS MODULE EXISTS. Those facts used to be MIRRORED onto plain columns of
``seo.keyword`` by this package's own classifier — two stores for one fact.
KI-035 retires the mirror: the columns are frozen and on their way out, so
every reader goes through the view instead. Reading the view rather than
re-deriving the precedence here is the point: there is ONE resolver, and it is
in the database.

The read itself is the ORM's: :class:`matrx_seo.db.models_seo.KeywordUniversalFacet`
is the generated read-only model of that view, so the dimension list this module
projects is checked against the live view at model-generation time instead of
drifting inside a hand-written SELECT.

SoR: common-docs/systems/marketing/seo/seo-keywords/legacy-retirement-blast-radius.md
"""

from __future__ import annotations

from typing import Any

from .db.models_seo import KeywordUniversalFacet
from .facet_registry import UNIVERSAL_FACET_DIMENSIONS as _REGISTRY_DIMENSIONS

#: The 13 universal dimensions, exactly as the view names them. Re-exported
#: from the registry so callers reading facts and callers writing them agree by
#: construction; never re-typed.
UNIVERSAL_FACET_DIMENSIONS: tuple[str, ...] = _REGISTRY_DIMENSIONS

__all__ = [
    "UNIVERSAL_FACET_DIMENSIONS",
    "read_universal_facets",
    "read_universal_facets_many",
]


async def read_universal_facets(keyword_id: str) -> dict[str, Any]:
    """This keyword's 13 universal facts, every dimension present.

    A keyword with no stamps on a dimension reads ``None`` there — exactly
    what the mirror column read before it was frozen.
    """
    rows = await KeywordUniversalFacet.filter(keyword_id=str(keyword_id)).values(
        *UNIVERSAL_FACET_DIMENSIONS
    )
    row = rows[0] if rows else {}
    return {dimension: row.get(dimension) for dimension in UNIVERSAL_FACET_DIMENSIONS}


async def read_universal_facets_many(
    keyword_ids: list[str],
) -> dict[str, dict[str, Any]]:
    """The same read for a batch, keyed by keyword id. Ids with no stamps at
    all are absent from the map; the caller reads them as all-``None``."""
    ids = [str(keyword_id) for keyword_id in dict.fromkeys(keyword_ids) if keyword_id]
    if not ids:
        return {}
    rows = await KeywordUniversalFacet.filter(keyword_id__in=ids).values(
        "keyword_id", *UNIVERSAL_FACET_DIMENSIONS
    )
    return {
        str(row["keyword_id"]): {
            dimension: row.get(dimension) for dimension in UNIVERSAL_FACET_DIMENSIONS
        }
        for row in rows
    }
