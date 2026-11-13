"""
"""

from dataclasses import dataclass
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import Tuple
from typing import TypedDict
from typing_extensions import Annotated
from typing_extensions import Callable
from typing_extensions import Generic
from typing_extensions import ParamSpec
from typing_extensions import TypeVar


Params = Tuple[Tuple[object, ...], Dict[str, Any]]
Res = TypeVar('Res')
Err = TypeVar('Err')
Param = ParamSpec('Param')


class EmptyKwargs(TypedDict):
    pass

@dataclass
class OkResult(Generic[Res]):
    value: Res

@dataclass
class ExceptionResult:
    traceback: str
    error_cls: str
    exception: Exception

@dataclass
class AbortedResult:
    pass

@dataclass
class EndResult:
    pass

RegularResQueueResult   = OkResult[Res] | ExceptionResult
GeneratorResQueueResult = OkResult[Res] | ExceptionResult | EndResult
YieldQueueResult        = OkResult[Res] | ExceptionResult | EndResult | AbortedResult

Duration        = int | timedelta
DynamicDuration = Duration | Callable[Param, Duration] | None


class _PicklableMarker:
    pass

T = TypeVar('T')

Picklable = Annotated[T, _PicklableMarker()]
