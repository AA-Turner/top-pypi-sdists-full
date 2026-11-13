"""ResearchOSSource, split by read family (search, entities, catalog, lineage, runs ...). Front door of
the old `probe.mcp.source`: every name it had, read live; a patch lands on every piece binding it."""

from __future__ import annotations

from ...foundation.front_door.front_door import serve_pieces

# Every piece loads here, as the old module ran whole on import (statically, so the deploy
# gate's import walk in scripts/ci/test_gate.py sees each one; serve_pieces loads the nested ones).
from . import catalog, documents, entities, lineage, people, projects, runs, search, sessions, source  # noqa: F401

#: The old module's pieces, in the split's load order: a write through the door reaches these only.
_PIECES = (
    "probe.mcp.source.catalog",
    "probe.mcp.source.documents",
    "probe.mcp.source.entities",
    "probe.mcp.source.lineage",
    "probe.mcp.source.people",
    "probe.mcp.source.projects",
    "probe.mcp.source.runs",
    "probe.mcp.source.search",
    "probe.mcp.source.sessions",
    "probe.mcp.source.source",
)

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    # probe.mcp.source.projects
    "logging": "probe.mcp.source.projects",
    # probe.mcp.source.documents
    "base64": "probe.mcp.source.documents",
    "NoteCatalogKind": "probe.mcp.source.documents",
    "current_delivery": "probe.mcp.source.documents",
    "document_hint": "probe.mcp.source.documents",
    "pin_document": "probe.mcp.source.documents",
    "source_changed": "probe.mcp.source.documents",
    "_NOTE_KIND_RANK": "probe.mcp.source.documents",
    # probe.mcp.source.catalog
    "re": "probe.mcp.source.catalog",
    "uuid": "probe.mcp.source.catalog",
    "Any": "probe.mcp.source.catalog",
    "quote": "probe.mcp.source.catalog",
    "errors": "probe.mcp.source.catalog",
    "EnvelopeState": "probe.mcp.source.catalog",
    "EntityType": "probe.mcp.source.catalog",
    "_CATALOG_DETAIL_ROUTES": "probe.mcp.source.catalog",
    "CATALOG_NO_MATCH": "probe.mcp.source.catalog",
    "_CATALOG_CAPABILITY": "probe.mcp.source.catalog",
    "CATALOG_FEATURE": "probe.mcp.source.catalog",
    "_DATASET_NAME": "probe.mcp.source.catalog",
    "_DATASET_VERSION": "probe.mcp.source.catalog",
    "_DATASET_LATEST": "probe.mcp.source.catalog",
    "dataset_ref_problem": "probe.mcp.source.catalog",
    "catalog_path_ref": "probe.mcp.source.catalog",
    # probe.mcp.source.source
    "time": "probe.mcp.source.source",
    "Client": "probe.mcp.source.source",
    "Capability": "probe.mcp.source.source",
    "_IDENTITY_TTL_SECONDS": "probe.mcp.source.source",
    "_IDENTITY_FAILURE_BACKOFF_SECONDS": "probe.mcp.source.source",
    "ResearchOSSource": "probe.mcp.source.source",
    # probe.mcp.source.runs
    "nonfinite": "probe.mcp.source.runs",
    "SOURCE_READ_CONTRACT": "probe.mcp.source.runs",
    "RunListQuery": "probe.mcp.source.runs",
    # probe.mcp.source.people
    "PeopleFilters": "probe.mcp.source.people",
    # probe.mcp.source.entities
    "Anchor": "probe.mcp.source.entities",
    "_RETIRED_REF_KIND": "probe.mcp.source.entities",
    "_RETIRED_REF_DETAIL": "probe.mcp.source.entities",
    "_INDEX_SLUG": "probe.mcp.source.entities",
    # probe.mcp.source.sessions
    "_transcript_agents": "probe.mcp.source.sessions",
    "_TRANSCRIPT_AGENTS": "probe.mcp.source.sessions",
    "_SESSION_ID_RE": "probe.mcp.source.sessions",
}
#: `from <old path> import *` takes what the old module's did.
__all__ = [name for name in _HOMES if not name.startswith("_")]

serve_pieces(__name__, _HOMES, pieces=_PIECES)
