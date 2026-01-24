"""
"""

from dataclasses import dataclass
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import Tuple
from typing import TypedDict
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
class ExceptionResult(Generic[Err]):
    traceback: str
    error_cls: str
    gradio_error: Err | None
@dataclass
class AbortedResult:
    pass
@dataclass
class EndResult:
    pass
@dataclass
class GradioQueueEvent:
    method_name: str
    args: tuple[Any, ...]
    kwargs: dict[str, Any]

RegularResQueueResult   = OkResult[Res] | ExceptionResult[Err] | GradioQueueEvent
GeneratorResQueueResult = OkResult[Res] | ExceptionResult[Err] | EndResult | GradioQueueEvent
YieldQueueResult        = OkResult[Res] | ExceptionResult[Err] | EndResult | AbortedResult

Duration        = int | timedelta
DynamicDuration = Duration | Callable[Param, Duration] | None
