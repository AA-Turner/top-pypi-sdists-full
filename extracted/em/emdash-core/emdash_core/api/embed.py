"""Embedding endpoints."""

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/embed", tags=["embeddings"])


class EmbedIndexRequest(BaseModel):
    """Request to index embeddings."""
    repo_path: str = Field(..., description="Path to repository")
    include_prs: bool = Field(default=True, description="Index PR embeddings")
    include_functions: bool = Field(default=True, description="Index function embeddings")
    include_classes: bool = Field(default=True, description="Index class embeddings")
    reindex: bool = Field(default=False, description="Reindex all embeddings")


class EmbedStatus(BaseModel):
    """Embedding status."""
    total_entities: int
    embedded_entities: int
    coverage_percent: float
    pr_count: int
    function_count: int
    class_count: int


class EmbedModel(BaseModel):
    """Embedding model info."""
    name: str
    dimension: int
    description: str


@router.get("/status", response_model=EmbedStatus)
async def get_embed_status():
    """Get embedding coverage statistics."""
    try:
        from ..embeddings.service import EmbeddingService

        service = EmbeddingService()
        stats = service.get_coverage_stats()

        total = stats.get("total", 1)
        embedded = stats.get("embedded", 0)

        return EmbedStatus(
            total_entities=total,
            embedded_entities=embedded,
            coverage_percent=(embedded / total * 100) if total > 0 else 0,
            pr_count=stats.get("pr_count", 0),
            function_count=stats.get("function_count", 0),
            class_count=stats.get("class_count", 0),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/index")
async def index_embeddings(request: EmbedIndexRequest):
    """Generate embeddings for graph entities."""
    from pathlib import Path
    from ..graph.connection import configure_for_repo
    from ..embeddings.indexer import EmbeddingIndexer

    try:
        # Configure database for the repo
        repo_root = Path(request.repo_path).resolve()
        configure_for_repo(repo_root)

        indexer = EmbeddingIndexer()
        total_indexed = 0

        if request.include_prs:
            total_indexed += indexer.index_pull_requests()
        if request.include_functions:
            total_indexed += indexer.index_functions(reindex=request.reindex)
        if request.include_classes:
            total_indexed += indexer.index_classes(reindex=request.reindex)

        return {
            "success": True,
            "indexed": total_indexed,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
async def list_models():
    """List available embedding models."""
    return {
        "models": [
            EmbedModel(
                name="all-MiniLM-L6-v2",
                dimension=384,
                description="Fast, general purpose (default)",
            ),
            EmbedModel(
                name="all-mpnet-base-v2",
                dimension=768,
                description="Higher quality, slower",
            ),
            EmbedModel(
                name="paraphrase-multilingual-MiniLM-L12-v2",
                dimension=384,
                description="Multilingual support",
            ),
        ]
    }


@router.post("/test")
async def test_embedding(text: str, model: Optional[str] = None):
    """Test embedding generation with sample text."""
    try:
        from ..embeddings.service import EmbeddingService

        service = EmbeddingService(model_name=model)
        embedding = service.embed(text)

        return {
            "text": text[:100] + "..." if len(text) > 100 else text,
            "dimension": len(embedding),
            "model": model or "default",
            "preview": embedding[:5],  # First 5 dimensions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
