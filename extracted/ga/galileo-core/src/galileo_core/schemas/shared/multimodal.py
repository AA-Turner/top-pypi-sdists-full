from enum import Enum


class ContentModality(str, Enum):
    """Classification of content modality"""

    text = "text"  # plain text
    document = "document"
    image = "image"
    audio = "audio"
    video = "video"
    webpage = "webpage"
    unknown = "unknown"


class FileSource(str, Enum):
    """Source of the file data."""

    direct_upload = "direct_upload"  # Base64 embedded in trace
    external_files_api = "external_files_api"  # Provider file API (OpenAI, Gemini, Anthropic, etc.)
    external_url = "external_url"  # Public URL reference
    assembled_stream = "assembled_stream"  # Streaming audio/video assembled


class ExternalProvider(str, Enum):
    """External provider of file"""

    openai_files_api = "openai_files_api"


class FileStatus(str, Enum):
    """Processing status of the file."""

    complete = "complete"  # Successfully stored
    failed = "failed"  # Storage failed
    pending = "pending"  # Data is still being uploaded
    not_uploaded = "not_uploaded"  # external_url / provider file IDs not uploaded


class MultimodalCapability(str, Enum):
    vision = "vision"
    audio = "audio"


MultimodalCapabilityMapping: dict[MultimodalCapability, set[ContentModality]] = {
    MultimodalCapability.vision: {ContentModality.image, ContentModality.document},
    MultimodalCapability.audio: {ContentModality.audio},
}
