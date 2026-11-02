"""Explicit absence for optional schema properties, distinct from a JSON null value."""

from enum import Enum


class Missing(Enum):
    """Represent an omitted field without applying annotation-only schema defaults."""

    VALUE = "missing"
