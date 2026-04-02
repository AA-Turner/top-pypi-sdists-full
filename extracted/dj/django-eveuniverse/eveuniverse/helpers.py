"""Helper functions and classes for Eve Universe."""

import hashlib
import json
from typing import Any, Dict, Optional

from django.db import models

# CCP uses a non-standard factor to calculate light years
# See also: https://gitlab.com/ErikKalkoken/django-eveuniverse/-/issues/16
METERS_PER_LY = 9_460_000_000_000_000


def meters_to_ly(value: float) -> Optional[float]:
    """Convert meters into lightyears."""
    return float(value) / METERS_PER_LY if value is not None else None


def meters_to_au(value: float) -> Optional[float]:
    """Convert meters into AU."""
    return float(value) / 149_597_870_691 if value is not None else None


def get_or_create_esi_or_none(
    prop_name: str, dct: dict, model_class: type
) -> Optional[models.Model]:
    """Create a new eveuniverse object from a dictionary entry and return it
    or return None if the prop name is not in the dict.

    :meta private:
    """
    if eve_id := dct.get(prop_name):
        return model_class.objects.get_or_create_esi(id=eve_id)[0]  # type: ignore
    return None


class EveEntityNameResolver:
    """Container with a mapping between entity Ids and entity names
    and a performant API
    """

    def __init__(self, names_map: Dict[int, str]) -> None:
        self._names_map = names_map

    def to_name(self, id: int) -> str:
        """Resolved an entity ID to a name

        Args:
            id: ID of the Eve entity to resolve

        Returns:
            name for corresponding entity ID if known else an empty string
        """
        try:
            name = self._names_map[id]
        except KeyError:
            name = ""

        return name


def dict_hash(dictionary: Dict[str, Any]) -> str:
    """SHA256 hash of a dictionary.

    :meta private:
    """
    my_hash = hashlib.sha256()
    encoded = json.dumps(dictionary, sort_keys=True).encode(encoding="utf8")
    my_hash.update(encoded)
    return my_hash.hexdigest()
