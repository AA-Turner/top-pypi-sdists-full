"""Deterministic safe Python identifiers for schema property names."""

import keyword
import re


class FieldName:
    """Preserve all JSON names through explicit mappings while avoiding Python/runtime collisions."""

    _RESERVED = frozenset({"schema_digest", "field_names", "from_dict", "to_dict"})
    _RECORD_RESERVED = frozenset(
        {
            "SchemaRecord",
            "Missing",
            "Identity",
            "JsonDocument",
            "SchemaDocument",
            "ValueShape",
            "ValueDecoder",
            "ValueUnion",
            "AssetRef",
            "Mapping",
            "ClassVar",
            "Self",
            "Literal",
        }
    )

    @classmethod
    def allocate(cls, name: str, used: set[str]) -> str:
        """Allocate stable ASCII identifiers, including keywords, punctuation and collisions."""
        base = re.sub(r"[^a-zA-Z0-9_]", "_", name)
        if not base or not base[0].isalpha():
            base = "field_" + base
        if keyword.iskeyword(base) or keyword.issoftkeyword(base) or base in cls._RESERVED:
            base += "_field"
        candidate, suffix = base, 2
        while candidate in used:
            candidate = f"{base}_{suffix}"
            suffix += 1
        used.add(candidate)
        return candidate

    @staticmethod
    def module(name: str) -> str:
        """Require an explicit public class name and derive its class-per-file module path."""
        if re.fullmatch(r"[A-Z][a-zA-Z0-9]*", name) is None:
            raise ValueError("Generated record names must use an ASCII PascalCase identifier")
        if name in FieldName._RECORD_RESERVED:
            raise ValueError("Generated record name collides with a schema runtime declaration")
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
