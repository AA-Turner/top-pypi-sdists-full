from enum import Enum
from typing import Optional, Type, TypeVar, Union

from benchling_api_client.v2.extensions import Enums


class CommonSortValues(str, Enum):
    """
    A list of commonly used sort parameters.

    These can be used as parameters to listing endpoints which can specify `sort=`.  If the chosen sort value is not
    supported by that endpoint, a bad request error (BenchlingError) will occur, with a message indicating so.
    """

    CREATEDAT = "createdAt"
    CREATEDATASC = "createdAt:asc"
    CREATEDATDESC = "createdAt:desc"
    MODIFIEDAT = "modifiedAt"
    MODIFIEDATASC = "modifiedAt:asc"
    MODIFIEDATDESC = "modifiedAt:desc"
    NAME = "name"
    NAMEASC = "name:asc"
    NAMEDESC = "name:desc"


_T = TypeVar("_T", bound=Enums.KnownString)


def _translate_to_string_enum(t: Type[_T], val: Union[None, _T, str]) -> Optional[_T]:
    if isinstance(val, t) or val is None:
        return val

    try:
        return t(val)
    except ValueError:
        strval = val.value if isinstance(val, Enum) else val
        return t.of_unknown(strval)  # type: ignore
