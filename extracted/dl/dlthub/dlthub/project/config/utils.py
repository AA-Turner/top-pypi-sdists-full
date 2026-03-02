from typing import Mapping, Any, Callable, cast

from dlt.common.typing import TypeVar
from dlt.common.utils import (
    update_dict_nested as _update_dict_nested,
    clone_dict_nested as _clone_dict_nested,
)

TMapping = TypeVar("TMapping", bound=Mapping[str, Any])

# TODO: maybe move to OSS, cast so TypedDict could be cloned
clone_dict_nested = cast(Callable[[TMapping], TMapping], _clone_dict_nested)
update_dict_nested = cast(Callable[[TMapping, Mapping[str, Any]], TMapping], _update_dict_nested)
