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
    execution_type: str = ""  # "local" or "cloud" — auto-derived if empty
    capabilities: tuple[str, ...] = ()  # e.g. ("chat", "code", "vision", "function_calling")

    def __post_init__(self):
        # Auto-derive execution_type from backend if not explicitly set
        if not self.execution_type:
            local_backends = ("gguf", "ollama", "llama_cpp", "onnx", "transformers", "vllm")
            derived = "local" if self.backend in local_backends else "cloud"
            object.__setattr__(self, "execution_type", derived)
        # Auto-derive capabilities from tags and category if not set
        if not self.capabilities:
            caps = ["chat"]  # All models support chat
            if self.category == "coding" or "code" in self.family.lower():
                caps.append("code")
            if "vision" in self.tags or self.category == "vision":
                caps.append("vision")
            if "tools" in self.tags:
                caps.append("function_calling")
            if "thinking" in self.tags or self.category == "reasoning":
                caps.append("reasoning")
            object.__setattr__(self, "capabilities", tuple(caps))

GCS_BUCKET = "https://storage.googleapis.com/sage-ai-models"

def _gcs_url(path: str) -> str:
    return f"{GCS_BUCKET}/gguf/{path}"

def _hf_url(repo: str, file: str) -> str:
    return f"https://huggingface.co/{repo}/resolve/main/{file}"
