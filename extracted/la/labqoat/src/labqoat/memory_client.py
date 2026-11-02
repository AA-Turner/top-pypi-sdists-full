"""Typed client for Labqoat-owned versioned research memory."""

from __future__ import annotations

from urllib.parse import urlencode

from labqoat._generated.knowledge_history import KnowledgeHistory
from labqoat._generated.knowledge_node import KnowledgeNode
from labqoat._generated.knowledge_publication import KnowledgePublication
from labqoat._generated.knowledge_receipt import KnowledgeReceipt
from labqoat._generated.new_knowledge_revision import NewKnowledgeRevision
from labqoat._generated.knowledge_view import KnowledgeView
from labqoat.base_client import BaseClient
from labqoat._generated.knowledge_brief import KnowledgeBrief
from labqoat._generated.new_knowledge_brief import NewKnowledgeBrief
from labqoat._generated.new_knowledge_status import NewKnowledgeStatus
from labqoat._generated.new_knowledge_link import NewKnowledgeLink
from labqoat._generated.knowledge_file_page import KnowledgeFilePage
from labqoat.memory_files_client import MemoryFilesClient
from labqoat.memory_query import MemoryQuery


class MemoryClient(BaseClient):
    """Read and publish the selected project's research with exact versions and caller-owned retry keys."""

    def publish(self, request: KnowledgePublication) -> KnowledgeReceipt:
        """Atomically publish roots, branches and syntheses without overwriting shared content."""
        path = "/api/v1/memory/commits"
        return self.decode(self.send_json("POST", path, request.to_dict()), path, KnowledgeReceipt.from_dict)

    def node(self, node: str, revision: str | None = None) -> KnowledgeNode:
        """Read a node's current head or one exact historical revision."""
        query = {"node": node}
        if revision is not None:
            query["revision"] = revision
        path = f"/api/v1/memory/nodes/item?{urlencode(query)}"
        return self.decode(self.send("GET", path), path, KnowledgeNode.from_dict)

    def revision(self, revision: str) -> KnowledgeNode:
        """Resolve an exact citation without separately knowing its owning node."""
        path = f"/api/v1/memory/revisions/item?{urlencode({'revision': revision})}"
        return self.decode(self.send("GET", path), path, KnowledgeNode.from_dict)

    def history(self, node: str, before: int | None = None) -> KnowledgeHistory:
        """Read a bounded history page using its immutable revision-number continuation."""
        query = {"node": node}
        if before is not None:
            query["before"] = str(before)
        path = f"/api/v1/memory/nodes/history?{urlencode(query)}"
        return self.decode(self.send("GET", path), path, KnowledgeHistory.from_dict)

    def revise(self, node: str, request: NewKnowledgeRevision) -> KnowledgeReceipt:
        """Publish full content under a required head check; surface conflicts for caller reconciliation."""
        path = f"/api/v1/memory/nodes/revisions?{urlencode({'node': node})}"
        return self.decode(self.send_json("POST", path, request.to_dict()), path, KnowledgeReceipt.from_dict)

    def search(
        self,
        query: str = "",
        limit: int | None = None,
        after: str | None = None,
        kind: str | None = None,
        run_id: str | None = None,
        node: str | None = None,
        include_all: bool = False,
    ) -> KnowledgeView:
        """Rank findings and evidence, preserving the frontier across opaque continuation cursors."""
        params: dict[str, object] = {
            "query": query,
            "limit": limit,
            "all": str(include_all).lower(),
        }
        params.update(
            {
                name: value
                for name, value in {"after": after, "kind": kind, "run_id": run_id, "node": node}.items()
                if value is not None
            }
        )
        path = f"/api/v1/memory/search?{urlencode(params)}"
        return self.decode(self.send("GET", path), path, KnowledgeView.from_dict)

    def retrieve(self, query: MemoryQuery) -> KnowledgeView:
        """Retrieve bounded evidence with explicit hybrid, lexical or semantic search settings."""
        path = f"/api/v1/memory/search?{urlencode(query.to_params())}"
        return self.decode(self.send("GET", path), path, KnowledgeView.from_dict)

    def changes(self, after: int = 0, limit: int = 20) -> KnowledgeView:
        """Resume a durable commit sequence independently of notifications or chat lifetime."""
        path = f"/api/v1/memory/changes?{urlencode({'after': after, 'limit': limit})}"
        return self.decode(self.send("GET", path), path, KnowledgeView.from_dict)

    def brief(
        self, *, include_all: bool = False, limit: int | None = None, max_bytes: int | None = None
    ) -> KnowledgeBrief:
        """Read the shared brief, hypotheses by status, results, open work and disagreements.

        The server bounds it to 8 rows a section within 24 KiB unless ``limit`` or ``max_bytes`` asks for more.
        """
        chosen = {"limit": limit, "max_bytes": max_bytes}
        query = {"all": str(include_all).lower(), **{key: value for key, value in chosen.items() if value is not None}}
        path = f"/api/v1/memory/brief?{urlencode(query)}"
        return self.decode(self.send("GET", path), path, KnowledgeBrief.from_dict)

    def edit_brief(self, request: NewKnowledgeBrief) -> KnowledgeReceipt:
        """Revise the pinned document under an optimistic version check."""
        path = "/api/v1/memory/brief"
        return self.decode(self.send_json("POST", path, request.to_dict()), path, KnowledgeReceipt.from_dict)

    def brief_history(self, before: int = 2_147_483_647) -> KnowledgeFilePage:
        """Read the versioned brief history with attribution."""
        path = f"/api/v1/memory/brief/history?{urlencode({'before': before})}"
        return self.decode(self.send("GET", path), path, KnowledgeFilePage.from_dict)

    def set_status(self, node: str, request: NewKnowledgeStatus) -> KnowledgeReceipt:
        """Change research status without creating a content revision."""
        path = f"/api/v1/memory/nodes/status?{urlencode({'node': node})}"
        return self.decode(self.send_json("POST", path, request.to_dict()), path, KnowledgeReceipt.from_dict)

    def link(self, request: NewKnowledgeLink) -> KnowledgeReceipt:
        """Link nodes or cite shared files, assets and runs."""
        path = "/api/v1/memory/links"
        return self.decode(self.send_json("POST", path, request.to_dict()), path, KnowledgeReceipt.from_dict)

    @property
    def files(self) -> MemoryFilesClient:
        """Share credentials and agent attribution with the project's versioned files."""
        return MemoryFilesClient(self._transport)
