"""
Type stubs for django_enum.choices.

The runtime module uses DjangoEnumPropertiesMeta (a composite of
EnumPropertiesMeta and ChoicesType) as the metaclass for its choice classes.
Mypy struggles to resolve metaclass @property attributes when the metaclass
is a subtype of Django's @type_check_only _TextChoicesType / _IntegerChoicesType.

By declaring the choice classes to inherit directly from the appropriate
Django base class (without the custom metaclass), mypy can use Django-stubs'
built-in _TextChoicesType / _IntegerChoicesType metaclass resolution and
properly expose .choices, .names, .labels, and .values as class attributes.
"""

from __future__ import annotations

from enum import IntFlag
from typing import Any

from django.db.models import Choices
from django.db.models import IntegerChoices as DjangoIntegerChoices
from django.db.models import TextChoices as DjangoTextChoices
from django.db.models.enums import ChoicesType

# DjangoEnumPropertiesMeta and DjangoSymmetricMixin are exported from this
# module at runtime; declare them so they can be imported.

class DjangoEnumPropertiesMeta(ChoicesType): ...
class DjangoSymmetricMixin: ...

class TextChoices(DjangoTextChoices):  # type: ignore[misc]
    """
    A character enumeration type that extends Django's TextChoices and
    accepts enum-properties property lists.
    """

    def __init__(self, *args: Any) -> None: ...  # type: ignore[override]

class IntegerChoices(DjangoIntegerChoices):  # type: ignore[misc]
    """
    An integer enumeration type that extends Django's IntegerChoices and
    accepts enum-properties property lists.
    """

    def __init__(self, *args: Any) -> None: ...  # type: ignore[override]

class FloatChoices(float, Choices):  # type: ignore[misc]
    """
    A floating point enumeration type that accepts enum-properties
    property lists.
    """

    ...

class FlagChoices(IntFlag, Choices):  # type: ignore[misc]
    """
    An integer flag enumeration type that accepts enum-properties property
    lists.
    """

    ...
