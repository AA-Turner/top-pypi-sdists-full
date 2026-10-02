from dataclasses import dataclass
from typing import Any

from django.conf import settings as django_settings


@dataclass(frozen=True)
class HushSetting:
    name: str
    hush_value: str


DEFAULT_SETTINGS: tuple[HushSetting, ...] = (
    HushSetting(name="log_statement", hush_value="none"),
    HushSetting(name="log_min_duration_statement", hush_value="-1"),
    HushSetting(name="log_duration", hush_value="off"),
    HushSetting(name="log_min_messages", hush_value="PANIC"),
    HushSetting(name="client_min_messages", hush_value="ERROR"),
)


def get_effective_registry() -> tuple[HushSetting, ...]:
    """Return the active settings registry.

    If HUSH_PG_SETTINGS_REGISTRY is set in Django settings to a non-None dict,
    it completely replaces DEFAULT_SETTINGS. An empty dict means "suppress no
    PG settings by default." If not set or None, returns DEFAULT_SETTINGS.
    """
    custom = getattr(django_settings, "HUSH_PG_SETTINGS_REGISTRY", None)
    if custom is None:
        return DEFAULT_SETTINGS
    return tuple(
        HushSetting(name=name, hush_value=value) for name, value in custom.items()
    )


def get_hush_default(name: str, fallback: Any) -> Any:
    """Read a HUSH_<name> setting from Django settings, with fallback."""
    return getattr(django_settings, f"HUSH_{name}", fallback)
