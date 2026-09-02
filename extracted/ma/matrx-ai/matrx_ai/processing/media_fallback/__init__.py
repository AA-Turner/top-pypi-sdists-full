"""Convert unsupported media or terminate before provider dispatch."""

from .handler import (
    MediaFallbackResolutionError,
    MediaResolveContext,
    ResolverResult,
    assert_media_resolvers_registered,
    has_unsupported_media,
    preprocess_unsupported_media,
    register_media_resolver,
)
from .resolvers import register_builtin_media_resolvers

# Register the ready resolvers (PDF) on import; idempotent.
register_builtin_media_resolvers()

__all__ = [
    "MediaResolveContext",
    "MediaFallbackResolutionError",
    "ResolverResult",
    "assert_media_resolvers_registered",
    "register_media_resolver",
    "register_builtin_media_resolvers",
    "has_unsupported_media",
    "preprocess_unsupported_media",
]
