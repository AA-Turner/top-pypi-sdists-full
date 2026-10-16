import re
from typing import Any, Iterator, Optional

from tmo.types.base_entity import BaseEntityMixin

_SNAKE_PATTERN = re.compile(r"(?<!^)(?=[A-Z])")


def to_snake_case(key: str) -> str:
    """Convert a camelCase API key to snake_case (`sourceId` -> `source_id`)."""
    return _SNAKE_PATTERN.sub("_", key).lower()


def to_camel_case(key: str) -> str:
    """Convert a snake_case attribute name to camelCase (`source_id` -> `sourceId`)."""
    first, *rest = key.split("_")
    return first + "".join(part.capitalize() for part in rest)


def api_field(name: str) -> property:
    """Create a read/write property backed by the private `_<name>` attribute."""
    private = f"_{name}"

    def getter(self) -> Any:
        return getattr(self, private)

    def setter(self, value: Any) -> None:
        setattr(self, private, value)
        self._present.add(name)

    return property(getter, setter, doc=f"API field '{to_camel_case(name)}'")


class ApiResourceMixin(BaseEntityMixin):
    """
    Typed view over an API response that stays dict-compatible.

    Subclasses declare `_FIELDS` (snake_case core fields, exposed through `api_field`
    properties). Any other key of the response is kept as an extra and remains
    reachable. Both camelCase (API) and snake_case (Python) keys work with `[]`,
    `get`, `in` and attribute access.
    """

    _FIELDS: tuple[str, ...] = ()

    def __init__(self, **values: Any) -> None:
        for name in self._FIELDS:
            setattr(self, f"_{name}", None)
        # Core fields supplied by the API or assigned later, so explicit nulls are kept
        self._present: set[str] = set()
        self._extra: dict[str, Any] = {}
        for key, value in values.items():
            snake = to_snake_case(key)
            if snake in self._FIELDS:
                setattr(self, f"_{snake}", value)
                self._present.add(snake)
            else:
                self._extra[key] = value

    @classmethod
    def from_dict(cls, values: dict) -> "ApiResourceMixin":
        """Build the resource from an API response dictionary."""
        return cls(**values)

    def _resolve(self, key: str) -> tuple[bool, Any]:
        snake = to_snake_case(key)
        if snake in self._FIELDS:
            return True, getattr(self, f"_{snake}")
        for extra_key, value in self._extra.items():
            if extra_key == key or to_snake_case(extra_key) == snake:
                return True, value
        return False, None

    def __getitem__(self, key: str) -> Any:
        found, value = self._resolve(key)
        if not found:
            raise KeyError(key)
        return value

    def __getattr__(self, name: str) -> Any:
        # Only called when normal lookup fails; never resolve private/dunder names
        if name.startswith("_"):
            raise AttributeError(name)
        found, value = self._resolve(name)
        if not found:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )
        return value

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        found, value = self._resolve(key)
        return value if found else default

    def __contains__(self, key: object) -> bool:
        return isinstance(key, str) and self._resolve(key)[0]

    def keys(self) -> list[str]:
        return list(self.to_dict().keys())

    def values(self) -> list[Any]:
        return list(self.to_dict().values())

    def items(self) -> list[tuple[str, Any]]:
        return list(self.to_dict().items())

    def __iter__(self) -> Iterator[str]:
        return iter(self.keys())

    def _raw_dict(self) -> dict:
        result = {}
        for name in self._FIELDS:
            if name in self._present:
                result[to_camel_case(name)] = getattr(self, f"_{name}")
        result.update(self._extra)
        return result

    def to_dict(self) -> dict:
        """Return the resource using the original API (camelCase) keys."""
        return {k: self._to_json_value(v) for k, v in self._raw_dict().items()}

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ApiResourceMixin):
            return self._raw_dict() == other._raw_dict()
        if isinstance(other, dict):
            return self._raw_dict() == other
        return NotImplemented

    __hash__ = None

    def _should_skip_attribute(self, attr_name: str) -> bool:
        if attr_name in ("_present", "_FIELDS"):
            return True
        return super()._should_skip_attribute(attr_name)
