"""Version-one portable policy for captured, self-contained JSON Schema."""

from typing import ClassVar
from urllib.parse import unquote

from labqoat.json_document import JsonValue
from labqoat.schemas.schema_nodes import SchemaNodes


class SchemaPolicy:
    """Reject unsupported protocol features before invoking a standards validator."""

    dialect: ClassVar[str] = "https://json-schema.org/draft/2020-12/schema"
    vocabularies: ClassVar[frozenset[str]] = frozenset(
        {
            "core",
            "applicator",
            "unevaluated",
            "validation",
            "meta-data",
            "format-annotation",
            "content",
        }
    )
    nonportable_patterns: ClassVar[tuple[str, ...]] = (
        "\\",
        "$",
        "(?",
        "(*",
        "&&",
        "[[:",
        "[[",
        "*+",
        "++",
        "?+",
        "}+",
    )

    @classmethod
    def check(cls, schema: dict[str, JsonValue] | bool) -> None:
        """Check dialect, vocabulary, references, extensions, and regex portability."""
        nodes = dict(SchemaNodes.walk(schema))
        targets = frozenset(nodes) | frozenset(anchor for node in nodes.values() for anchor in cls._anchors(node))
        for pointer, node in nodes.items():
            if isinstance(node, dict):
                cls._node(node, pointer, targets)

    @staticmethod
    def _anchors(node: JsonValue) -> list[str]:
        """Only schema-position anchors can extend the captured reference closure."""
        if not isinstance(node, dict):
            return []
        return [value for key in ("$anchor", "$dynamicAnchor") if isinstance(value := node.get(key), str)]

    @classmethod
    def _node(cls, node: dict[str, JsonValue], pointer: str, paths: frozenset[str]) -> None:
        """Keep protocol restrictions distinct from full schema semantics."""
        if node.get("$schema", cls.dialect) != cls.dialect:
            raise ValueError(f"{pointer}/$schema: only Draft 2020-12 is supported")
        cls._vocabulary(node.get("$vocabulary", {}), pointer)
        for keyword, value in node.items():
            cls._keyword(keyword, value, pointer + "/" + keyword, paths)

    @classmethod
    def _keyword(cls, keyword: str, value: JsonValue, pointer: str, paths: frozenset[str]) -> None:
        """Reject executable extensions and check schema-owned references and patterns."""
        if keyword.startswith("x-jsv-"):
            raise ValueError(f"{pointer}: executable schema extensions are forbidden")
        if keyword in {"$ref", "$dynamicRef"} and isinstance(value, str):
            cls._reference(value, pointer, paths)
        if keyword == "pattern" and isinstance(value, str):
            cls._pattern(value, pointer)
        if keyword == "patternProperties" and isinstance(value, dict):
            for pattern in value:
                cls._pattern(pattern, pointer)

    @staticmethod
    def _reference(value: str, pointer: str, paths: frozenset[str]) -> None:
        """Allow fragment references only to captured schema positions and anchors."""
        if not value.startswith("#") and value != "":
            raise ValueError(f"{pointer}: references must be self-contained fragments")
        fragment = unquote(value.removeprefix("#"))
        if fragment not in paths:
            raise ValueError(f"{pointer}: reference does not target a captured schema position")

    @classmethod
    def _vocabulary(cls, value: JsonValue, pointer: str) -> None:
        """Require known assertion vocabularies; unknown optional vocabularies annotate."""
        if isinstance(value, dict):
            for uri, required in value.items():
                supported = {"https://json-schema.org/draft/2020-12/vocab/" + name for name in cls.vocabularies}
                if required is True and uri not in supported:
                    raise ValueError(f"{pointer}/$vocabulary: unsupported required vocabulary {uri}")

    @classmethod
    def _pattern(cls, value: str, pointer: str) -> None:
        """Limit patterns to the shared search grammar; never reinterpret a constraint."""
        if any(fragment in value for fragment in cls.nonportable_patterns):
            raise ValueError(f"{pointer}: pattern is outside portable_regex_v1; use explicit character classes")
