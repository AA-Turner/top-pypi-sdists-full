"""ChromaDB-backed memory service for persistent cross-session recall.

Implements ADK's BaseMemoryService interface using a local ChromaDB collection.
All data stays on disk — no cloud, no API keys.

Storage location: ~/.ghost_pc/chromadb/
Embedding model: all-MiniLM-L6-v2 (ONNX, downloaded once, ~80MB)

Falls back to InMemoryMemoryService if chromadb is not installed.
Install: pip install ghost-pc[memory]
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

import chromadb
from google.adk.memory.base_memory_service import BaseMemoryService, SearchMemoryResponse
from google.adk.memory.memory_entry import MemoryEntry

if TYPE_CHECKING:
    from google.adk.sessions import Session

logger = logging.getLogger(__name__)

DEFAULT_PERSIST_DIR = Path.home() / ".ghost_pc" / "chromadb"
COLLECTION_NAME = "ghost_pc_sessions"
MAX_SEARCH_RESULTS = 5
MIN_DOC_LENGTH = 20
MAX_DOC_LENGTH = 2000


class ChromaDBMemoryService(BaseMemoryService):
    """Persistent memory using local ChromaDB vector database.

    Uses cosine similarity for semantic search. Documents are extracted
    from session events (user messages and agent responses) and stored
    with metadata for user-scoped retrieval.
    """

    def __init__(self, persist_dir: str | Path | None = None) -> None:
        self._persist_dir = Path(persist_dir or DEFAULT_PERSIST_DIR)
        self._persist_dir.mkdir(parents=True, exist_ok=True)

        self._client = chromadb.PersistentClient(path=str(self._persist_dir))
        self._collection = self._client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(
            "ChromaDB memory initialized at %s (%d documents)",
            self._persist_dir,
            self._collection.count(),
        )

    async def add_session_to_memory(self, session: Session) -> None:
        """Extract text from session events and store as documents."""
        if not session.events:
            return

        documents: list[str] = []
        ids: list[str] = []
        metadatas: list[dict[str, str]] = []

        for i, event in enumerate(session.events):
            if not event.content or not event.content.parts:
                continue
            text_parts = [p.text for p in event.content.parts if p.text]
            if not text_parts:
                continue

            text = " ".join(text_parts)
            if len(text) < MIN_DOC_LENGTH:
                continue

            doc_id = f"{session.id}_{i}"
            documents.append(text[:MAX_DOC_LENGTH])
            ids.append(doc_id)
            metadatas.append(
                {
                    "session_id": session.id,
                    "user_id": session.user_id,
                    "role": event.content.role or "unknown",
                    "author": getattr(event, "author", "unknown"),
                }
            )

        if documents:
            # Upsert to handle duplicates from re-rotations
            self._collection.upsert(
                documents=documents,
                ids=ids,
                metadatas=metadatas,
            )
            logger.info(
                "Stored %d documents from session %s (total: %d)",
                len(documents),
                session.id,
                self._collection.count(),
            )

    async def search_memory(
        self,
        *,
        app_name: str,
        user_id: str,
        query: str,
    ) -> SearchMemoryResponse:
        """Search past sessions for relevant context.

        Returns SearchMemoryResponse with MemoryEntry objects that ADK's
        PreloadMemoryTool can inject into the agent's context.
        """
        from google.genai import types

        if self._collection.count() == 0:
            return SearchMemoryResponse(memories=[])

        n_results = min(MAX_SEARCH_RESULTS, self._collection.count())

        # Scope search to the requesting user
        where_filter = {"user_id": user_id} if user_id else None

        results = self._collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter,
        )

        memories: list[MemoryEntry] = []
        if results and results["documents"]:
            for doc_idx, doc_list in enumerate(results["documents"]):
                for item_idx, doc in enumerate(doc_list):
                    meta = (
                        results["metadatas"][doc_idx][item_idx] if results.get("metadatas") else {}
                    )
                    memories.append(
                        MemoryEntry(
                            content=types.Content(
                                role="user",
                                parts=[types.Part(text=f"[Memory] {doc}")],
                            ),
                            author=meta.get("author"),
                            timestamp=None,
                        )
                    )

        return SearchMemoryResponse(memories=memories)
