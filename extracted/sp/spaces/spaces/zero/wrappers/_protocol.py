"""
What transits between the main process and a worker:

- Tasks to run
- Generator forwarding protocol: each request is answered by one response,
  starting with an implicit `next` request and ending with the first non-`Yield` response
"""

from dataclasses import dataclass
from traceback import format_exception
from typing import Any
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import Generic
from typing import Tuple
from typing import TypeVar

from ..errors import ZeroGPUExceptionPicklingError
from ..errors import ZeroGPUReturnValuePicklingError
from ..errors import ZeroGPUSendValuePicklingError
from ..errors import ZeroGPUThrowValuePicklingError
from ..errors import ZeroGPUYieldValuePicklingError

Yielded = TypeVar('Yielded')
Sent = TypeVar('Sent')
Returned = TypeVar('Returned')

Params = Tuple[Tuple[object, ...], Dict[str, Any]]
Task = Tuple[Params, Callable[[], None]]


# Requests (main process -> worker)

@dataclass
class Send(Generic[Sent]):
    value: Sent
    pickling_error: ClassVar = ZeroGPUSendValuePicklingError

@dataclass
class Throw:
    exception: Exception | GeneratorExit
    pickling_error: ClassVar = ZeroGPUThrowValuePicklingError

Request = Send[Sent] | Throw


# Responses (worker -> main process)

@dataclass
class Yield(Generic[Yielded]):
    value: Yielded
    pickling_error: ClassVar = ZeroGPUYieldValuePicklingError

@dataclass
class Return(Generic[Returned]):
    value: Returned
    pickling_error: ClassVar = ZeroGPUReturnValuePicklingError

@dataclass
class Raise:
    exception: Exception | GeneratorExit
    traceback: str
    pickling_error: ClassVar = ZeroGPUExceptionPicklingError
    @classmethod
    def of(cls, exception: Exception | GeneratorExit):
        formatted = format_exception(type(exception), exception, exception.__traceback__)
        return cls(exception=exception, traceback=''.join(formatted))

Response = Yield[Yielded] | Return[Returned] | Raise
