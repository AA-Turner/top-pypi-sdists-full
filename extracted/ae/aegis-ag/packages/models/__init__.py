"""Provider-neutral model adapter interfaces and baseline adapters."""

from .inventory import MODEL_SURFACES
from .model_metadata import (
    ResolvedModelMetadata,
    get_cached_context_length,
    resolve_provider_model_metadata,
    save_context_length,
)
from .provider_runtime import (
    InMemoryProviderManifestRegistry,
    InMemoryProviderTransportRegistry,
    ProviderCatalogRecord,
    ProviderManifest,
    ProviderManifestRegistry,
    ProviderRuntimeResolution,
    ProviderRuntimeResolver,
    ProviderSetupGuide,
    ProviderTransportDefinition,
    ProviderTransportRegistry,
)
from .runtime import (
    CredentialSource,
    InMemoryModelAdapterRegistry,
    ModelAdapter,
    ModelAdapterDescriptor,
    ModelEmbeddingResult,
    ModelRequest,
    ModelTextResult,
    ModelUsage,
    PreviewModelProviderCapability,
    PromptEchoModelAdapter,
    StaticTextModelAdapter,
)

__all__ = [
    "CredentialSource",
    "InMemoryProviderManifestRegistry",
    "InMemoryProviderTransportRegistry",
    "InMemoryModelAdapterRegistry",
    "MODEL_SURFACES",
    "ModelAdapter",
    "ModelAdapterDescriptor",
    "ModelEmbeddingResult",
    "ModelRequest",
    "ModelTextResult",
    "ModelUsage",
    "ProviderCatalogRecord",
    "ProviderManifest",
    "ProviderManifestRegistry",
    "ProviderRuntimeResolution",
    "ProviderRuntimeResolver",
    "ProviderSetupGuide",
    "ProviderTransportDefinition",
    "ProviderTransportRegistry",
    "PreviewModelProviderCapability",
    "PromptEchoModelAdapter",
    "ResolvedModelMetadata",
    "StaticTextModelAdapter",
    "get_cached_context_length",
    "resolve_provider_model_metadata",
    "save_context_length",
]
