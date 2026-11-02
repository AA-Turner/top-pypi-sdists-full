"""Typed metadata access to versioned project files."""

from __future__ import annotations
from urllib.parse import urlencode
from labqoat.base_client import BaseClient
from labqoat._generated.knowledge_file_page import KnowledgeFilePage
from labqoat._generated.knowledge_receipt import KnowledgeReceipt
from labqoat._generated.new_knowledge_file import NewKnowledgeFile


class MemoryFilesClient(BaseClient):
    """Inspect shared file heads and immutable path histories through one transport."""

    def list(self, path: str = "", after: str | None = None, limit: int = 100) -> KnowledgeFilePage:
        """List current file versions under an optional relative path."""
        query = {"path": path, "limit": str(limit)}
        if after is not None:
            query["after"] = after
        target = f"/api/v1/memory/files?{urlencode(query)}"
        return self.decode(self.send("GET", target), target, KnowledgeFilePage.from_dict)

    def log(self, path: str, before: int = 2_147_483_647) -> KnowledgeFilePage:
        """Read attributable historical versions for one shared path."""
        target = f"/api/v1/memory/files/history?{urlencode({'path': path, 'before': before})}"
        return self.decode(self.send("GET", target), target, KnowledgeFilePage.from_dict)

    def push(self, request: NewKnowledgeFile) -> KnowledgeReceipt:
        """Publish an already uploaded asset as the next checked path version."""
        target = "/api/v1/memory/files"
        return self.decode(self.send_json("POST", target, request.to_dict()), target, KnowledgeReceipt.from_dict)
