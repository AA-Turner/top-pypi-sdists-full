"""Immutable logical-to-physical shape independent of schema assertion semantics."""

from __future__ import annotations

from dataclasses import dataclass

import pyarrow as pa

from labqoat.json_document import JsonValue


@dataclass(frozen=True)
class LayoutNode:
    """Describe a fixed record, homogeneous array, or lossless scalar storage slot."""

    kind: str
    nullable: bool = False
    optional: bool = False
    children: tuple[tuple[str, LayoutNode], ...] = ()
    asset_reference: bool = False

    def document(self) -> dict[str, JsonValue]:
        """Expose the stable layout identity without Arrow's display formatting."""
        document: dict[str, JsonValue] = {
            "kind": self.kind,
            "nullable": self.nullable,
            "optional": self.optional,
            "children": {name: child.document() for name, child in self.children},
        }
        if self.asset_reference:
            document["asset_reference"] = True
        return document

    def wraps(self) -> bool:
        """Whether this slot or any below it stores an optional field behind a presence wrapper."""
        return self.optional or any(child.wraps() for _, child in self.children)

    def refers(self) -> bool:
        """Whether this slot or any below it holds a schema-marked asset reference."""
        return self.asset_reference or any(child.refers() for _, child in self.children)

    def arrow_type(self) -> pa.DataType:
        """Compile named children in deterministic order with explicit nullability."""
        if self.kind == "object":
            return pa.struct([child.arrow_field(name) for name, child in self.children])
        if self.kind == "array":
            return pa.list_(self.children[0][1].arrow_field("element"))
        scalars: dict[str, pa.DataType] = {
            "integer": pa.int64(),
            "number": pa.float64(),
            "boolean": pa.bool_(),
            "string": pa.string(),
        }
        return scalars[self.kind]

    def arrow_field(self, name: str) -> pa.Field[pa.DataType]:
        """Use a presence wrapper for optional fields, preserving present nulls."""
        value_type = self.arrow_type()
        if self.optional:
            wrapper = pa.struct(
                [
                    pa.field("present", pa.bool_(), nullable=False),
                    pa.field("value", value_type, nullable=True),
                ]
            )
            return pa.field(name, wrapper, nullable=False)
        return pa.field(name, value_type, nullable=self.nullable)
