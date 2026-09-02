"""Exception classes for the issue template system."""

from __future__ import annotations


class TemplateNotFoundError(Exception):
    """Raised when a required template cannot be found or is not registered."""


class TemplateValidationError(Exception):
    """Raised when required properties are missing from the issue."""


class PresetLoadError(Exception):
    """Raised when ``preset.yml`` is missing or cannot be parsed as valid YAML.

    Distinct from :class:`TemplateNotFoundError`, which assumes preset loading
    succeeded but no matching template (type-specific or default) was found.
    """
