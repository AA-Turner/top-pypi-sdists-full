from typing import Any, Callable, Dict, Optional, Tuple, Type, Union

from pydantic import BaseModel
from typing_extensions import get_type_hints

_cached_hints: dict[Tuple[Union[Type, Callable], bool], dict[str, Any]] = {}


def cached_get_type_hints(
    obj: Union[Type, Callable],
    include_extras: bool = False,
    globalns: Optional[Dict[str, Any]] = None,
) -> dict[str, Any]:
    k = (obj, include_extras)
    if k in _cached_hints:
        return _cached_hints[k]
    v = get_type_hints(obj, include_extras=include_extras, globalns=globalns)
    if isinstance(obj, type) and issubclass(obj, BaseModel) and "__slots__" in v:
        del v["__slots__"]
    _cached_hints[k] = v
    return v
