"""Property source registry for aggregating environment information."""

import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .providers import (
    DockerConfigProvider,
    PropertySourceProvider,
    SystemEnvironmentProvider,
    SystemPropertiesProvider,
)

logger = logging.getLogger(__name__)

# Spring Boot's default keys-to-sanitize patterns.
DEFAULT_KEYS_TO_SANITIZE: tuple[str, ...] = (
    "password",
    "secret",
    "key",
    "token",
    ".*credentials.*",
    "vcap_services",
)

REDACTED_VALUE = "******"


class ShowValues(Enum):
    """Controls when property values are visible vs redacted.

    Mirrors Spring Boot 3's ``management.endpoint.env.show-values`` setting.

    Members:
        NEVER: Redact ALL values — nothing is shown in the clear.
        ALWAYS: Show benign values in the clear; sensitive keys are still redacted.
        WHEN_AUTHORIZED: Reserved for future use with authentication checks.
            Currently behaves like NEVER (safe default until auth is wired).
    """

    NEVER = "NEVER"
    ALWAYS = "ALWAYS"
    WHEN_AUTHORIZED = "WHEN_AUTHORIZED"


@dataclass(frozen=True)
class SanitizationConfig:
    """Configuration for property value redaction.

    Args:
        keys_to_sanitize: Regex patterns for keys that are **always** redacted,
            regardless of ``show_values``.  Defaults to Spring Boot's default set.
        additional_keys_to_sanitize: Extra patterns appended to the defaults.
        show_values: Controls visibility of *non-sensitive* values.
            ``NEVER`` redacts everything; ``ALWAYS`` shows benign values.
    """

    keys_to_sanitize: tuple[str, ...] = DEFAULT_KEYS_TO_SANITIZE
    additional_keys_to_sanitize: tuple[str, ...] = ()
    show_values: ShowValues = ShowValues.NEVER

    def __post_init__(self) -> None:
        all_patterns = self.keys_to_sanitize + self.additional_keys_to_sanitize
        pattern = re.compile("|".join(all_patterns), re.IGNORECASE) if all_patterns else None
        # frozen=True requires object.__setattr__ for post-init assignment
        object.__setattr__(self, "_sensitive_pattern", pattern)

    _sensitive_pattern: re.Pattern[str] | None = field(init=False, default=None)

    @property
    def sensitive_pattern(self) -> re.Pattern[str] | None:
        """Return the compiled sensitive-key regex (computed once at init)."""
        return self._sensitive_pattern


class PropertySourceRegistry:
    """Manages all property source providers with built-in defaults.

    The registry maintains a set of named property source providers and can
    aggregate their outputs. It comes with sensible defaults but allows
    registration and override of providers.

    Sanitization is controlled via ``SanitizationConfig``:

    - ``keys_to_sanitize`` — base patterns (default: password, secret, key, …)
    - ``additional_keys_to_sanitize`` — extra patterns on top of defaults
    - ``show_values`` — ``NEVER`` (default), ``ALWAYS``, or ``WHEN_AUTHORIZED``
    """

    def __init__(
        self,
        with_defaults: bool = True,
        sanitization: SanitizationConfig | None = None,
    ) -> None:
        """Initialize the registry.

        Args:
            with_defaults: If True, register built-in providers (systemEnvironment,
                          systemProperties, dockerConfig). If False, start empty.
            sanitization: Redaction configuration. If None, uses default config
                         (redact keys matching password, secret, key, token, etc.).
        """
        self._providers: dict[str, PropertySourceProvider] = {}
        self._sanitization = sanitization or SanitizationConfig()
        if with_defaults:
            self._init_defaults()

    def _init_defaults(self) -> None:
        """Register built-in providers that are always included."""
        self.register("systemEnvironment", SystemEnvironmentProvider())
        self.register("systemProperties", SystemPropertiesProvider())
        self.register("dockerConfig", DockerConfigProvider())

    def register(self, name: str, provider: PropertySourceProvider) -> None:
        """Register or override a property source provider.

        If a provider with the given name already exists, it is replaced.

        Args:
            name: Unique identifier for the provider.
            provider: Object implementing the PropertySourceProvider protocol.
        """
        self._providers[name] = provider

    def unregister(self, name: str) -> None:
        """Remove a provider by name.

        Args:
            name: Name of the provider to remove.
        """
        self._providers.pop(name, None)

    def get_all_sources(self, to_match: str | None = None) -> list[dict[str, Any]]:
        """Aggregate property sources from all registered providers.

        Redaction is two-tier:
        - Sensitive keys (matching ``keys_to_sanitize``) are **always** redacted.
        - When ``show_values`` is ``NEVER``, *all* values are redacted.
        - When ``show_values`` is ``ALWAYS``, only
          sensitive keys are redacted and benign values are shown.

        Args:
            to_match: Optional case-insensitive substring filter applied to
                     each provider's output.

        Returns:
            List of property source dicts aggregated from all providers.
        """
        sources = []
        for name, provider in self._providers.items():
            try:
                sources.extend(provider.get_sources(to_match))
            except Exception:
                logger.exception("Provider '%s' failed in get_sources()", name)

        redact_all = self._sanitization.show_values != ShowValues.ALWAYS
        sensitive = self._sanitization.sensitive_pattern
        return [
            _sanitize_source(source, sensitive=sensitive, redact_all=redact_all)
            for source in sources
        ]


def _sanitize_source(
    source: dict[str, Any],
    *,
    sensitive: re.Pattern[str] | None,
    redact_all: bool,
) -> dict[str, Any]:
    """Replace values of sensitive (or all) keys with the redacted placeholder."""
    properties = source.get("properties")
    if not isinstance(properties, dict):
        return source

    if not redact_all and sensitive is None:
        return source

    sanitized: dict[str, Any] = {}
    for prop_key, prop_value in properties.items():
        is_sensitive = sensitive is not None and sensitive.search(prop_key)
        if redact_all or is_sensitive:
            # Preserve the Spring-style {"value": ...} wrapper if present
            if isinstance(prop_value, dict) and "value" in prop_value:
                sanitized[prop_key] = {"value": REDACTED_VALUE}
            else:
                sanitized[prop_key] = REDACTED_VALUE
        else:
            sanitized[prop_key] = prop_value

    return {**source, "properties": sanitized}


def create_property_source_registry(
    with_defaults: bool = True,
    sanitization: SanitizationConfig | None = None,
) -> PropertySourceRegistry:
    """Create a new property source registry.

    Args:
        with_defaults: If True, include built-in providers. If False, start empty.
        sanitization: Redaction configuration. If None, uses default config.

    Returns:
        A new PropertySourceRegistry instance.
    """
    return PropertySourceRegistry(
        with_defaults=with_defaults,
        sanitization=sanitization,
    )
