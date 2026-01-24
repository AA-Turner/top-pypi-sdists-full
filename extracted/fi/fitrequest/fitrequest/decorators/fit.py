import functools
import inspect
from collections.abc import Callable
from dataclasses import asdict, dataclass
from typing import Any, Literal

import makefun

from fitrequest.errors import FitDecoratorInvalidUsageError


@dataclass
class Fit:
    """
    Decorator class for marking methods as FitRequest methods.
    The decorator's attributes are a subset of the ``MethodConfig`` attributes.
    Additional attributes are inferred from the function's signature (e.g., name, async_method, docstring, ...)
    """

    endpoint: str
    base_url: str | None = None
    save_method: bool = False
    raise_for_status: bool = True
    request_verb: Literal['DELETE', 'GET', 'PATCH', 'POST', 'PUT'] = 'GET'
    json_path: str | None = None

    def __call__(self, func: Callable) -> Callable:
        """
        This decorator has two main roles:
            1. Marking the function as a FitRequest method (set the `fit_decorator` attribute).
            2. Executing the generated FitRequest method stored in `shared['generated_method']`.

        The 'fit_decorator' attribute is assigned to the function being decorated.
        It holds an instance of the @fit decorator, allowing ClassFactory.handle_fit_decorator
        to access its properties and configuration details.

        The 'shared' attribute is initialized as a dictionary on the function.
        This serves as a storage area where ClassFactory.handle_fit_decorator will store the
        dynamically generated FitRequest method implementation under the key 'generated_method'.
        """
        func.fit_method = True
        func.fit_decorator = self
        func.shared = {}

        @makefun.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if method := func.shared.get('generated_method'):
                return method(*args, **kwargs)
            raise FitDecoratorInvalidUsageError

        @makefun.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            if method := func.shared.get('generated_method'):
                return await method(*args, **kwargs)
            raise FitDecoratorInvalidUsageError

        return async_wrapper if inspect.iscoroutinefunction(func) else wrapper

    def dump(self) -> dict:
        return asdict(self)


fit = Fit  # Expose a lowercase alias
get = functools.partial(fit, request_verb='GET')
put = functools.partial(fit, request_verb='PUT')
post = functools.partial(fit, request_verb='POST')
patch = functools.partial(fit, request_verb='PATCH')
delete = functools.partial(fit, request_verb='DELETE')

for deco, verb in [(get, 'GET'), (put, 'PUT'), (post, 'POST'), (patch, 'PATCH'), (delete, 'DELETE')]:
    docstring = f'Partial object from the `@fit` decorator where the `request_verb` argument is set to *{verb}*.'
    deco.__doc__ = docstring
