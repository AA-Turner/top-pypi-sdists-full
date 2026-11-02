"""Walk schema-owned asset positions in validated logical rows without guessing from value shapes."""

from collections.abc import Iterator

from labqoat.data_layout.layout_node import LayoutNode
from labqoat.json_document import JsonDocument, JsonValue


class AssetReferences:
    """Retain source pointers for explicit assets through nullable records, arrays and captured references."""

    def __init__(self, root: LayoutNode) -> None:
        """Keep only the captured, nonrecursive physical layout."""
        self.root = root
        self.present = root.refers()

    def read(self, row: JsonValue) -> Iterator[tuple[str, dict[str, JsonValue]]]:
        """Yield references only from fields marked by the captured schema; most layouts mark none."""
        if not self.present:
            return iter(())
        return self._walk(self.root, row, "")

    @classmethod
    def _walk(cls, node: LayoutNode, value: JsonValue, pointer: str) -> Iterator[tuple[str, dict[str, JsonValue]]]:
        """Optional missing values and explicit nulls contain no asset authority."""
        if value is None:
            return
        if node.asset_reference:
            yield pointer, JsonDocument.expect_dict(value)
        elif node.kind == "object":
            record = JsonDocument.expect_dict(value)
            for name, child in node.children:
                path = pointer + "/" + name.replace("~", "~0").replace("/", "~1")
                yield from cls._walk(child, record.get(name), path)
        elif node.kind == "array":
            for index, item in enumerate(JsonDocument.expect_list(value)):
                yield from cls._walk(node.children[0][1], item, f"{pointer}/{index}")
