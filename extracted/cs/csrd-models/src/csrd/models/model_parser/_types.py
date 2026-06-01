from typing import Any, TypeVar

T = TypeVar("T")

ResponseModelType = type[T]
type ParsedResponse = Any  # T | list[T] | bytes | dict — not expressible as a static type alias
