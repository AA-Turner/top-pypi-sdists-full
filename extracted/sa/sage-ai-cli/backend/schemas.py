import re
from pydantic import BaseModel, Field, field_validator


class SchemaBase(BaseModel):
    model_config = {"protected_namespaces": ()}


# P0-8: Safe ID patterns to prevent path traversal
SAFE_MODEL_ID_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9_:\.\-]{0,127}$"
SAFE_CONVERSATION_ID_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9_\-]{0,63}$"


def validate_safe_id(value: str, id_type: str = "generic") -> str:
    """
    P0-8: Validate that an ID is safe and doesn't contain path traversal.

    Raises ValueError if validation fails.
    """
    if not value:
        raise ValueError(f"{id_type} cannot be empty")

    # Check for path traversal
    if ".." in value:
        raise ValueError(f"{id_type} contains path traversal")

    if value.startswith("/") or value.startswith("\\"):
        raise ValueError(f"{id_type} cannot start with path separator")

    # Check for null bytes
    if "\x00" in value:
        raise ValueError(f"{id_type} contains null byte")

    return value


# ── Model records ──────────────────────────────────────────────


class ModelVersion(SchemaBase):
    version: int
    version_tag: str | None = None  # git tag from source repo
    file_path: str
    source_url: str | None = None
    local_import: bool = False
    sha256: str | None = None
    size_gb: float | None = None
    created_at: str | None = None


class ModelRecord(SchemaBase):
    model_id: str
    runtime: str
    license: str | None = None
    format: str | None = None  # gguf, safetensors, onnx
    source_repo: str | None = None  # "owner/repo" on GitHub
    active_version: int = 1
    versions: list[ModelVersion] = Field(default_factory=list)

    def active(self) -> ModelVersion:
        for v in self.versions:
            if v.version == self.active_version:
                return v
        raise KeyError(f"Active version {self.active_version} not found")

    def latest_version_number(self) -> int:
        if not self.versions:
            return 0
        return max(v.version for v in self.versions)

    def all_hashes(self) -> set[str]:
        """Return all known SHA256 hashes for deduplication."""
        return {v.sha256.lower() for v in self.versions if v.sha256}

    def all_tags(self) -> set[str]:
        """Return all known version tags for deduplication."""
        return {v.version_tag for v in self.versions if v.version_tag}


# ── Request schemas ────────────────────────────────────────────

RUNTIME_PATTERN = "^(llama_cpp|transformers|vllm|onnx|ollama|cloud)$"


class DownloadModelReq(SchemaBase):
    model_id: str = Field(min_length=2, pattern=SAFE_MODEL_ID_PATTERN)
    source_url: str = Field(min_length=8)
    runtime: str = Field(pattern=RUNTIME_PATTERN)
    filename: str | None = None
    sha256: str | None = None
    license: str | None = None
    size_gb: float | None = None
    format: str | None = None
    version_tag: str | None = None

    @field_validator("model_id")
    @classmethod
    def validate_model_id(cls, v: str) -> str:
        return validate_safe_id(v, "model_id")


class ImportModelReq(SchemaBase):
    model_id: str = Field(min_length=2)
    local_path: str
    runtime: str = Field(pattern=RUNTIME_PATTERN)
    license: str | None = None
    format: str | None = None


class LoadModelReq(SchemaBase):
    model_id: str
    version: int | None = None
    threads: int | None = Field(default=None, ge=1, le=256)


class SetActiveVersionReq(SchemaBase):
    model_id: str
    version: int = Field(ge=1)


# ── File handling schemas ─────────────────────────────────────

# Large text threshold: content above this is treated as a file (100KB)
LARGE_TEXT_THRESHOLD = 100 * 1024

SAFE_FILENAME_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9_\.\-]{0,255}$"


def validate_safe_filename(filename: str) -> str:
    """Validate filename doesn't contain path traversal."""
    if not filename:
        raise ValueError("Filename cannot be empty")
    if ".." in filename:
        raise ValueError("Filename contains path traversal")
    if "/" in filename or "\\" in filename:
        # Extract just the filename part
        filename = filename.replace("\\", "/").split("/")[-1]
    if "\x00" in filename:
        raise ValueError("Filename contains null byte")
    return filename


class FileAttachment(SchemaBase):
    """File attachment metadata for chat messages."""
    file_id: str = Field(min_length=1)
    filename: str = Field(min_length=1)
    mime_type: str = Field(default="application/octet-stream")
    size_bytes: int = Field(default=0, ge=0)
    url: str | None = None
    content_preview: str | None = None

    @field_validator("file_id")
    @classmethod
    def validate_file_id(cls, v: str) -> str:
        return validate_safe_id(v, "file_id")

    @field_validator("filename")
    @classmethod
    def validate_filename(cls, v: str) -> str:
        return validate_safe_filename(v)


class LargeTextContent(SchemaBase):
    """Large text/paste content that should be treated as a file."""
    content: str = Field(min_length=1)
    filename: str | None = None
    language: str | None = None
    size_bytes: int | None = None

    def __init__(self, **data):
        # Auto-generate filename if not provided
        if "filename" not in data or data["filename"] is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            data["filename"] = f"paste_{timestamp}.txt"
        # Compute size_bytes from content
        if "size_bytes" not in data or data["size_bytes"] is None:
            data["size_bytes"] = len(data.get("content", "").encode("utf-8"))
        super().__init__(**data)


class ChatMessage(SchemaBase):
    role: str = Field(pattern="^(system|user|assistant)$")
    content: str
    attachments: list[FileAttachment] | None = Field(default=None)


class ChatReq(SchemaBase):
    model_id: str = Field(pattern=SAFE_MODEL_ID_PATTERN)
    messages: list[ChatMessage]
    temperature: float = Field(default=0.3, ge=0, le=2)
    max_tokens: int = Field(default=512, ge=32, le=4096)
    top_p: float = Field(default=0.95, ge=0, le=1)
    stream: bool = True
    conversation_id: str | None = Field(default=None, pattern=SAFE_CONVERSATION_ID_PATTERN)

    @field_validator("model_id")
    @classmethod
    def validate_model_id(cls, v: str) -> str:
        return validate_safe_id(v, "model_id")

    @field_validator("conversation_id")
    @classmethod
    def validate_conversation_id(cls, v: str | None) -> str | None:
        if v is not None:
            return validate_safe_id(v, "conversation_id")
        return v


class CreateConversationReq(SchemaBase):
    title: str = Field(min_length=1, max_length=120)


# ── Source tracking schemas ────────────────────────────────────


class AddSourceReq(SchemaBase):
    repo_url: str = Field(min_length=5)
    model_id: str = Field(min_length=2)
    runtime: str = Field(pattern=RUNTIME_PATTERN, default="llama_cpp")
    asset_pattern: str = Field(default="*.gguf")
    license: str | None = None
