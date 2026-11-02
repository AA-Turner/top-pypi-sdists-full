"""Provider-family names used by session workflow routing."""

from typing import Final, Literal, cast

ProviderName = Literal["github", "linear", "notion", "slack"]

PROVIDER_NAMES: Final[frozenset[str]] = frozenset({"github", "linear", "notion", "slack"})

CONNECTOR_NAME_TO_PROVIDER_NAME: Final[dict[str, ProviderName]] = {
    "github_app": "github",
    "linear": "linear",
    "notion": "notion",
    "slack": "slack",
}


def _normalize_name(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("name must be a string")

    normalized = value.strip().lower()
    if not normalized:
        raise ValueError("name must not be empty")
    return normalized


def normalize_provider_name(provider: object) -> str:
    return _normalize_name(provider)


def require_provider_name(provider: object) -> ProviderName:
    normalized_provider = _normalize_name(provider)
    if normalized_provider not in PROVIDER_NAMES:
        valid = ", ".join(sorted(PROVIDER_NAMES))
        raise ValueError(f"Unknown provider {provider!r}; valid providers: {valid}")
    return cast("ProviderName", normalized_provider)


def provider_name_for_connector_name(connector_name: object) -> ProviderName:
    normalized_connector_name = _normalize_name(connector_name)
    provider_name = CONNECTOR_NAME_TO_PROVIDER_NAME.get(normalized_connector_name)
    if provider_name is None:
        known_connectors = ", ".join(sorted(CONNECTOR_NAME_TO_PROVIDER_NAME))
        raise ValueError(f"Unknown connector {connector_name!r}; known connectors: {known_connectors}")
    return provider_name


__all__ = [
    "CONNECTOR_NAME_TO_PROVIDER_NAME",
    "PROVIDER_NAMES",
    "ProviderName",
    "normalize_provider_name",
    "provider_name_for_connector_name",
    "require_provider_name",
]
