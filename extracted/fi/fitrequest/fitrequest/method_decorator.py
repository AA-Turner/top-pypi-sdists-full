import inspect
import re
from collections.abc import Callable
from typing import Annotated, Any

import makefun
from pydantic import BeforeValidator, PlainSerializer

from fitrequest.decorators.paginated import paginated
from fitrequest.decorators.retry import retry
from fitrequest.errors import InvalidMethodDecoratorError

#: Global dictionnary used to map ``json/yaml`` declared decorators to actual python decorators.
environment_decorators = {
    'retry': retry,
    'paginated': paginated,
}


def eval_decorator_signature(signature: str, environment: dict) -> Callable | None:
    """
    Evaluate the decorator signature and return the associated method from the environment.
    Return None if the decorator is not found.
    """
    # Decorator without args
    if not re.match(r'^\w+\(.*\)$', signature):
        return environment.get(signature)

    # Decorator with args
    deco_data = makefun.create_function(func_signature=signature, func_impl=lambda _: _)

    deco_name = deco_data.__name__
    deco_params = {field: value.default for field, value in inspect.signature(deco_data).parameters.items()}

    if (decorator := environment.get(deco_name)) is None:
        return None

    return decorator(**deco_params)


def validate_init_value(value: Any) -> Callable:
    """
    Validates the provided decorator value.
    If a string is given, attempts to retrieve the corresponding decorator from the global environment.
    Raises an InvalidMethodDecoratorError if the value is invalid.
    """
    if callable(value):
        return value

    if not isinstance(value, str):
        raise InvalidMethodDecoratorError(provided_decorator=str(value))

    if (decorator := eval_decorator_signature(value, environment=environment_decorators)) is None:
        raise InvalidMethodDecoratorError(provided_decorator=value)

    return decorator


ValidMethodDecorator = Annotated[
    Callable | str,
    BeforeValidator(validate_init_value),
    PlainSerializer(lambda func: func.__qualname__, return_type=str),
]
