"""
Human-readable label resolution for parameter IDs.

Maps technical Homematic parameter identifiers to user-friendly labels
using upstream CCU translations from aiohomematic. Falls back to automatic
formatting when no translation is available.

Public API of this module is defined by __all__.
"""

import inspect
from typing import Final

from aiohomematic.ccu_translations import get_parameter_translation

from aiohomematic_config.const import DEFAULT_LOCALE


class LabelResolver:
    """
    Resolve parameter IDs to human-readable labels.

    Uses upstream CCU translations from aiohomematic.
    Falls back to automatic formatting (split by underscore, title case)
    when no translation is found.
    """

    __slots__ = ("_locale",)

    def __init__(self, *, locale: str = DEFAULT_LOCALE) -> None:
        """Initialize the label resolver."""
        self._locale: Final = locale

    @property
    def locale(self) -> str:
        """Return the current locale."""
        return self._locale

    def has_translation(self, *, parameter_id: str, channel_type: str = "") -> bool:
        """Return True if a CCU translation exists for the parameter."""
        return (
            get_parameter_translation(
                parameter=parameter_id,
                channel_type=channel_type or None,
                locale=self._locale,
            )
            is not None
        )

    def resolve(self, *, parameter_id: str, channel_type: str = "") -> str:
        """
        Resolve a parameter ID to a human-readable label.

        Returns the translated label if available, otherwise applies
        automatic formatting: split by underscores, title case each word.
        """
        if (
            label := get_parameter_translation(
                parameter=parameter_id,
                channel_type=channel_type or None,
                locale=self._locale,
            )
        ) is not None:
            return label
        return _humanize_parameter_id(parameter_id=parameter_id)


def _humanize_parameter_id(*, parameter_id: str) -> str:
    """
    Convert a technical parameter ID to a human-readable label.

    Example: ``TEMPERATURE_OFFSET`` -> ``Temperature Offset``
    """
    return parameter_id.replace("_", " ").title()


__all__ = tuple(
    sorted(
        name
        for name, obj in globals().items()
        if not name.startswith("_")
        and (name.isupper() or inspect.isfunction(obj) or inspect.isclass(obj))
        and getattr(obj, "__module__", __name__) == __name__
    )
)
