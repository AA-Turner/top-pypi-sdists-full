"""Typed research memory of the project the current invocation runs in."""

from dataclasses import dataclass
from urllib.parse import urlencode

from labqoat._generated.knowledge_node import KnowledgeNode
from labqoat._generated.knowledge_publication import KnowledgePublication
from labqoat._generated.knowledge_receipt import KnowledgeReceipt
from labqoat._generated.knowledge_view import KnowledgeView
from labqoat.worker.worker_api import WorkerApi
from labqoat._generated.knowledge_brief import KnowledgeBrief
from labqoat.memory_query import MemoryQuery


@dataclass(frozen=True)
class RunMemory:
    """Read shared research and append findings using worker credentials and server-owned execution identity."""

    api: WorkerApi

    def publish(self, request: KnowledgePublication) -> KnowledgeReceipt:
        """Atomically append findings and evidence; the service attaches this run and attempt."""
        return KnowledgeReceipt.from_dict(self.api.json("POST", "/api/v1/worker/memory/commits", request.to_dict()))

    def brief(self) -> KnowledgeBrief:
        """Read the shared research brief of this run's project."""
        return KnowledgeBrief.from_dict(self.api.json("GET", "/api/v1/worker/memory/brief"))

    def search(
        self,
        query: str = "",
        *,
        node: str | None = None,
        run_id: str | None = None,
        kind: str | None = None,
        after: str | None = None,
        limit: int | None = None,
    ) -> KnowledgeView:
        """Rank research and evidence while retaining a stable frontier across continuations."""
        params = {
            name: value
            for name, value in {"query": query, "node": node, "run_id": run_id, "kind": kind, "after": after}.items()
            if value is not None
        }
        params["limit"] = str(limit)
        return KnowledgeView.from_dict(self.api.json("GET", f"/api/v1/worker/memory/search?{urlencode(params)}"))

    def retrieve(self, query: MemoryQuery) -> KnowledgeView:
        """Retrieve bounded evidence within this run's project using explicit search settings."""
        path = f"/api/v1/worker/memory/search?{urlencode(query.to_params())}"
        return KnowledgeView.from_dict(self.api.json("GET", path))

    def revision(self, revision: str) -> KnowledgeNode:
        """Resolve an exact evidence revision and its execution provenance."""
        return KnowledgeNode.from_dict(
            self.api.json("GET", f"/api/v1/worker/memory/revisions/item?{urlencode({'revision': revision})}")
        )

    def changes(self, after: int = 0, limit: int = 20) -> KnowledgeView:
        """Recover project changes after a durable event sequence."""
        return KnowledgeView.from_dict(
            self.api.json("GET", f"/api/v1/worker/memory/changes?{urlencode({'after': after, 'limit': limit})}")
        )
