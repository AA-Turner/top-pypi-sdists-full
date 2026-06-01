from typing import Any


class PathValue(dict[str, Any]):
    """Dictionary wrapper that also supports dot-notation for key access."""

    def __getattr__(self, item: str) -> Any:
        """Return dict values via dot-notation, raising AttributeError for missing keys."""
        if item.startswith("__"):
            raise AttributeError(item)
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' has no key '{item}'") from None

    def __setattr__(self, key: str, value: Any) -> None:
        """Map attribute assignment to dictionary item assignment."""
        if key.startswith("__"):
            super().__setattr__(key, value)
            return
        self[key] = value

    def __delattr__(self, item: str) -> None:
        """Map attribute deletion to dictionary item deletion."""
        if item.startswith("__"):
            super().__delattr__(item)
            return
        try:
            del self[item]
        except KeyError as exc:
            raise AttributeError(item) from exc


__all__ = ("PathValue",)
