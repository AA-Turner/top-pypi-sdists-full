"""Asset IDs or digests given where a structured parameter declares an Artifact, swapped for catalog descriptors."""

import typing
from collections.abc import Callable
from dataclasses import is_dataclass
from types import UnionType
from typing import get_args, get_origin, get_type_hints

from labqoat.json_document import JsonValue
from labqoat.references import AssetRef

Lookup = Callable[[str], JsonValue]


class AssetSelectors:
    """Walk a JSON document alongside its declared type; a string where an Artifact belongs is a selector."""

    @classmethod
    def replace(cls, annotation: object, document: JsonValue, lookup: Lookup) -> JsonValue:
        """The document with every selector at an Artifact position replaced by ``lookup(selector)``."""
        annotation = cls.unwrap(annotation)
        if annotation is AssetRef:
            return lookup(document) if isinstance(document, str) else document
        if isinstance(document, list):
            return [cls.replace(cls.element(annotation), item, lookup) for item in document]
        if isinstance(document, dict):
            return {key: cls.replace(cls.member(annotation, key), value, lookup) for key, value in document.items()}
        return document

    @classmethod
    def selectors(cls, annotation: object, document: JsonValue) -> list[str]:
        """The selectors the document gives at Artifact positions, in document order."""
        found: list[str] = []

        def note(selector: str) -> JsonValue:
            found.append(selector)
            return selector

        cls.replace(annotation, document, note)
        return found

    @staticmethod
    def element(annotation: object) -> object:
        """The item type of a list or a homogeneous tuple."""
        arguments = get_args(AssetSelectors.unwrap(annotation))
        homogeneous = len(arguments) == 1 or (len(arguments) == 2 and arguments[1] is Ellipsis)
        return arguments[0] if homogeneous else None

    @staticmethod
    def member(annotation: object, key: str) -> object:
        """A dataclass field's type, or a mapping's value type."""
        annotation = AssetSelectors.unwrap(annotation)
        if is_dataclass(annotation):
            return get_type_hints(annotation).get(key)
        arguments = get_args(annotation)
        return arguments[1] if get_origin(annotation) is dict and len(arguments) == 2 else None

    @staticmethod
    def unwrap(annotation: object) -> object:
        """``T | None`` is read as ``T``."""
        if get_origin(annotation) in (UnionType, typing.Union):
            members = [value for value in get_args(annotation) if value is not type(None)]
            return members[0] if len(members) == 1 else None
        return annotation
