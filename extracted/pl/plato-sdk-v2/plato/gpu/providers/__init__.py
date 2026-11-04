"""GPU providers behind one protocol; ``provider_for`` picks by name."""

from plato.gpu.providers.base import (
    GpuProvider,
    GpuProviderError,
    PodInfo,
    PodSpec,
    RegistryCredential,
    RenderJobInput,
)
from plato.gpu.providers.runpod import RunpodProvider
from plato.gpu.settings import GpuSettings


def provider_for(settings: GpuSettings) -> GpuProvider:
    """The provider ``settings`` names, built with its credentials."""

    if settings.provider == "runpod":
        return RunpodProvider(
            settings.runpod_api_key,
            rest_url=settings.runpod_rest_url,
            api_url=settings.runpod_api_url,
            render_endpoint_id=settings.runpod_render_endpoint_id,
            registry_auth_id=settings.runpod_registry_auth_id,
        )
    raise GpuProviderError(f"no GPU provider named {settings.provider!r}; runpod is the one there is")


__all__ = [
    "GpuProvider",
    "GpuProviderError",
    "PodInfo",
    "PodSpec",
    "RegistryCredential",
    "RenderJobInput",
    "RunpodProvider",
    "provider_for",
]
