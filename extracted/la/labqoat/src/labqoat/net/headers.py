"""Case-insensitive header fields that keep their order and repeated names."""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping


class Headers(Mapping[str, str]):
    """Read header values by any capitalization; a repeated name reads as its values joined by commas."""

    def __init__(self, fields: Mapping[str, str] | Iterable[tuple[str, str]] | None = None) -> None:
        """Keep each field as sent, in order."""
        pairs = fields.items() if isinstance(fields, Mapping) else (fields or ())
        self._fields = [(str(name), str(value)) for name, value in pairs]

    def __getitem__(self, name: str) -> str:
        """Join every value of the name, as a single field would have carried them."""
        values = self.get_list(name)
        if not values:
            raise KeyError(name)
        return ", ".join(values)

    def __iter__(self) -> Iterator[str]:
        """Yield each distinct name once, lowercased, in first-seen order."""
        return iter(dict.fromkeys(name.lower() for name, _value in self._fields))

    def __len__(self) -> int:
        """Count distinct names."""
        return len({name.lower() for name, _value in self._fields})

    def __repr__(self) -> str:
        """Show names only: values may carry credentials."""
        return f"Headers({list(self)!r})"

    def get_list(self, name: str) -> list[str]:
        """Every value sent under the name, in order."""
        wanted = name.lower()
        return [value for field, value in self._fields if field.lower() == wanted]

    def multi_items(self) -> list[tuple[str, str]]:
        """Every field as sent, repeated names included."""
        return list(self._fields)

    def merged(self, extra: Mapping[str, str] | Iterable[tuple[str, str]] | None) -> Headers:
        """These fields with ``extra`` replacing any of the same name."""
        added = Headers(extra)
        names = set(added)
        kept = [(name, value) for name, value in self._fields if name.lower() not in names]
        return Headers(kept + added.multi_items())
