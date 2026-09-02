"""
External Dependency Registry for matrx-scraper package.

Provides a configuration-based approach for injecting external dependencies
that come from the host application (e.g., search functions).

Usage (host application startup):

    from matrx_scraper._ext import configure_ext
    configure_ext(wrapped_brave_search=wrapped_brave_search)

Usage (within matrx-scraper package):

    from matrx_scraper._ext import get_ext
    wrapped_brave_search = get_ext("wrapped_brave_search")
"""

from __future__ import annotations

from typing import Any

_registry: dict[str, Any] = {}


class ExtNotConfiguredError(RuntimeError):
    pass


def configure_ext(**kwargs: Any) -> None:
    _registry.update(kwargs)


def get_ext(name: str) -> Any:
    if name not in _registry:
        raise ExtNotConfiguredError(
            f"matrx-scraper external dependency '{name}' not registered. "
            f"Call matrx_scraper.configure() before using this functionality."
        )
    return _registry[name]


def has_ext(name: str) -> bool:
    return name in _registry
