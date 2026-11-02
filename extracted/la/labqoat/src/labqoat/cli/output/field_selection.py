"""Keep only the fields a reader named with --select, so large documents need no script to read."""

from labqoat.json_document import JsonValue


class FieldSelection:
    """Dotted paths such as ``status,manifest.args.steps``; on a page they select inside each item."""

    KEY = "labqoat.select"
    PAGING: tuple[str, ...] = ("next_cursor", "links")

    def __init__(self, spec: str) -> None:
        """Parse comma-separated dotted paths, ignoring blanks."""
        self.paths = [tuple(part for part in path.strip().split(".") if part) for path in spec.split(",")]
        self.paths = [path for path in self.paths if path]

    def apply(self, document: JsonValue) -> JsonValue:
        """The named fields of an object, or of each item of a page; anything else is returned as it is."""
        if not isinstance(document, dict) or not self.paths:
            return document
        items = document.get("items")
        if isinstance(items, list) and not any(path[0] in document for path in self.paths if path[0] != "items"):
            page: dict[str, JsonValue] = {"items": [self.pick(item) for item in items]}
            page.update({key: document[key] for key in self.PAGING if key in document})
            return page
        return self.pick(document)

    def pick(self, document: JsonValue) -> JsonValue:
        """Copy each named path that exists, keeping its nesting."""
        if not isinstance(document, dict):
            return document
        selected: dict[str, JsonValue] = {}
        for path in self.paths:
            FieldSelection.copy(document, selected, path)
        return selected

    @staticmethod
    def copy(source: dict[str, JsonValue], target: dict[str, JsonValue], path: tuple[str, ...]) -> None:
        """Copy one path from source into target; a missing step copies nothing."""
        head, rest = path[0], path[1:]
        if head not in source:
            return
        value = source[head]
        existing = target.get(head)
        if not rest or existing is value:
            target[head] = value
            return
        if isinstance(value, dict):
            branch = existing if isinstance(existing, dict) else {}
            target[head] = branch
            FieldSelection.copy(value, branch, rest)
