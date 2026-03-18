"""Verifier registration and discovery."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plato.verifiers.base import BaseVerifier

logger = logging.getLogger(__name__)

_VERIFIER_REGISTRY: dict[str, type[BaseVerifier]] = {}


def register_verifier(name: str):
    """Decorator to register a verifier class.

    Usage::

        @register_verifier("my-verifier")
        class MyVerifier(BaseVerifier[MyConfig]):
            ...
    """

    def decorator(cls: type[BaseVerifier]) -> type[BaseVerifier]:
        if name in _VERIFIER_REGISTRY:
            logger.warning("Overwriting verifier registration for '%s'", name)
        _VERIFIER_REGISTRY[name] = cls
        cls.name = name
        return cls

    return decorator


def get_verifier(name: str) -> type[BaseVerifier] | None:
    """Get a registered verifier class by name."""
    return _VERIFIER_REGISTRY.get(name)


def get_registered_verifiers() -> dict[str, type[BaseVerifier]]:
    """Get all registered verifier classes."""
    return dict(_VERIFIER_REGISTRY)


def discover_verifiers() -> None:
    """Discover and load installed verifier packages via entry points.

    Verifier packages declare entry points in pyproject.toml::

        [project.entry-points."plato.verifiers"]
        my-verifier = "my_verifier_pkg:MyVerifier"
    """
    from plato.utils.discovery import discover_plugins

    discover_plugins("plato.verifiers", logger)
