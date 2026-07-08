from __future__ import annotations

from dataclasses import dataclass, field

@dataclass(frozen=True)
class CatalogModel:
    """A downloadable model entry."""

    name: str  # Short CLI name (e.g. "gemma3-4b")
    display_name: str  # Human-readable name
    filename: str  # GGUF filename (empty for Ollama models)
    url: str  # Direct download URL (empty for Ollama models)
    size_gb: float  # Approximate file size in GB (0 for cloud-only)
    params: str  # Parameter count (e.g. "4B")
    family: str  # Model family (e.g. "Gemma")
    description: str  # Short description
    backend: str = "gguf"  # "gguf" or "ollama"
    tags: tuple[str, ...] = ()  # Capability tags (tools, thinking, vision, etc.)
    category: str = "general"  # coding, reasoning, general, vision, small, embedding
    default: bool = False  # Whether this is a default-install model

GCS_BUCKET = "https://storage.googleapis.com/sage-ai-models"

def _gcs_url(path: str) -> str:
    return f"{GCS_BUCKET}/gguf/{path}"

def _hf_url(repo: str, file: str) -> str:
    return f"https://huggingface.co/{repo}/resolve/main/{file}"
