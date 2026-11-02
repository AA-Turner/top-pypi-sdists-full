"""matrx_rag.api — FastAPI HTTP surface for matrx-rag.

Phase 2d ships a minimal viable router covering the three endpoints
matrx-local needs to run a complete RAG roundtrip:

* ``POST /rag/search`` — hybrid retrieval (vector + lexical, RRF,
                          MMR, optional multi-query + HyDE, optional
                          Cohere rerank).
* ``POST /rag/ingest`` — synchronous one-shot ingestion of a single
                          source (note / code_file / cld_file).
* ``GET  /rag/health`` — schema sanity probe + chunk / embedding
                          counts per scope.

The remaining aidream surface (verify, library,
data-stores, admin) is intentionally **not** ported in this commit.
Each of those is large and stateful enough to deserve its own focused
follow-on. Phase 2d's load-bearing constraint is "matrx-local can mount
matrx-rag and run a complete ingest + search cycle"; everything else
follows incrementally.

Mount example::

    from fastapi import FastAPI
    import matrx_rag.api as rag_api

    app = FastAPI()
    rag_api.include_routers(app, prefix="/rag")

Default prefix is ``/rag``. Aidream is NOT required to mount these —
aidream has its own ``aidream/api/routers/rag.py`` covering the full
surface (currently 3,139 LOC). The package routes exist primarily for
matrx-local, which has no aidream routes of its own.

Auth model: every endpoint uses ``Depends(context_dep)`` from
matrx-connect to receive an ``AppContext`` with the caller's
``user_id`` and ``organization_id``. Endpoints reject requests without
a user_id. RLS scoping is enforced by the underlying matrx_rag.search
and matrx_rag.ingestion call sites; the router is a thin wrapper.
"""

from __future__ import annotations

from typing import Any

from matrx_rag.api.router_rag import router as rag_router


def include_routers(app: Any, *, prefix: str = "/rag") -> None:
    """Mount all matrx-rag routers on the given FastAPI app.

    Args:
        app: FastAPI instance (or anything exposing ``include_router``).
        prefix: URL prefix for the RAG routes. Default ``/rag``.
    """
    app.include_router(rag_router, prefix=prefix, tags=["rag"])


def include_knowledge_routers(app: Any, *, prefix: str = "/knowledge") -> None:
    """Mount the canonical Knowledge HTTP alias without removing old routes."""
    app.include_router(rag_router, prefix=prefix, tags=["knowledge"])


__all__ = [
    "rag_router",
    "include_routers",
    "include_knowledge_routers",
]
