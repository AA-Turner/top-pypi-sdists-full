import functools
from typing import Tuple, Dict, Any, Callable, List

from requests import Response

from spotlight.core.common.decorators.data.__util import __process_response
from spotlight.core.common.function import no_transform


def data_request(
    request: Callable = None,
    *,
    processor: Callable[[Response], Any] = lambda response: response.json(),
    transformers: List[Callable[[Any], Any]] = None
) -> Callable:
    """
    Decorator for processing the response of a REST request.

    Args:
        request (Callable): Function
        processor (Callable[[Response], Any]): Transform response
        transformers (Callable[[Any], Any]): List of transform functions to run the data through in order

    Returns:
        Callable: Wrapped function
    """

    @functools.wraps(request)
    def decorator(f):
        @functools.wraps(f)
        def wrap(*args: Tuple, **kwargs: Dict[str, Any]) -> Any:
            _processor = kwargs.pop("processor", None) or processor
            _transformers = (
                kwargs.pop("transformers", None)
                or transformers
                or [lambda data: no_transform(data)]
            )
            response: Response = f(*args, **kwargs)
            return __process_response(response, _processor, _transformers)

        return wrap

    if request is None:
        return decorator
    return decorator(request)
