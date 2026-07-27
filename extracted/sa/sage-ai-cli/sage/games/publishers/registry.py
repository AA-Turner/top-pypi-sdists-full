"""Publisher registry — map publisher name → adapter factory."""

from __future__ import annotations

from typing import Callable

from .adapters import (
    AppStoreAdapter,
    GitHubPagesAdapter,
    GooglePlayAdapter,
    ItchAdapter,
    SteamAdapter,
)
from .base import PublisherAdapter


REGISTRY: dict[str, Callable[[], PublisherAdapter]] = {
    "itch.io":       ItchAdapter,
    "itch":          ItchAdapter,
    "steam":         SteamAdapter,
    "github-pages":  GitHubPagesAdapter,
    "gh-pages":      GitHubPagesAdapter,
    "google-play":   GooglePlayAdapter,
    "play":          GooglePlayAdapter,
    "app-store":     AppStoreAdapter,
    "testflight":    AppStoreAdapter,
}


def get_publisher(name: str) -> PublisherAdapter:
    """Look up a publisher adapter by name. Raises ValueError on unknown.

    Unlike engines (which silently default to Godot), an unknown publisher
    is a user error worth surfacing — we don't want to "default" someone's
    Steam upload to itch.io."""
    key = (name or "").lower().strip()
    factory = REGISTRY.get(key)
    if factory is None:
        raise ValueError(
            f"unknown publisher: {name!r}. "
            f"Available: {', '.join(sorted(set(REGISTRY)))}"
        )
    return factory()
