"""
"""

from datetime import timedelta
from typing import TypedDict
from typing_extensions import Annotated
from typing_extensions import Callable
from typing_extensions import ParamSpec
from typing_extensions import TypeVar


Param = ParamSpec('Param')


class EmptyKwargs(TypedDict):
    pass


Duration        = int | timedelta
DynamicDuration = Duration | Callable[Param, Duration] | None


class _PicklableMarker:
    pass

T = TypeVar('T')

Picklable = Annotated[T, _PicklableMarker()]
