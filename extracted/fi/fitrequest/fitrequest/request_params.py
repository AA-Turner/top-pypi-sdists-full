import inspect
from collections.abc import Callable
from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, PlainSerializer, create_model

from fitrequest.errors import InvalidParamsTypeError
from fitrequest.method_models import environment_models
from fitrequest.utils import (
    check_reserved_names,
    is_basemodel_subclass,
    reserved_fitrequest_names,
    reserved_httpx_names,
)


def validate_init_value(value: Any) -> type[BaseModel] | None:
    """
    Validate the provided parameters.
    If a string is given, attempts to retrieve the corresponding model from the global environment.
    If a list of fields' names is supplied, dynamically create a Pydantic model
    to standardize the data type processed by `fitrequest` during method generation.
    Raise an `InvalidParamsTypeError` if the provided value has an incorrect type.
    """
    if isinstance(value, str):
        value = environment_models.get(value, value)

    if value is None:
        return None

    if is_basemodel_subclass(value):
        check_reserved_names(set(value.model_fields))
        return value

    if isinstance(value, list):
        attributes = dict.fromkeys(value, (str, None))
        check_reserved_names(set(attributes))
        return create_model('DynamicParamsModel', **attributes, __config__=ConfigDict(extra='allow'))

    raise InvalidParamsTypeError(provided_params=value)


def extract_params(func: Callable, endpoint_varnames: set[str]) -> BaseModel | None:
    """
    Extract the request parameters from the given function
    and return the corresponding Pydantic model for the fitrequest configuration.
    Return None if no parameters is found.
    """
    ignore = {'self', *reserved_fitrequest_names, *reserved_httpx_names, *endpoint_varnames}
    empty = inspect.Parameter.empty

    def get_default(param: inspect.Parameter) -> Any:
        return param.default if param.default is not empty else ...

    def get_annotation(param: inspect.Parameter) -> Any:
        return param.annotation if param.annotation is not empty else str

    request_params = {
        param.name: (get_annotation(param), get_default(param))
        for name, param in inspect.signature(func).parameters.items()
        if name not in ignore
    }
    if not request_params:
        return None

    return create_model('FitDecoratorParamsModel', **request_params, __config__=ConfigDict(extra='allow'))


ValidParams = Annotated[
    type[BaseModel] | list[str] | str | None,
    Field(validate_default=True),
    BeforeValidator(validate_init_value),
    PlainSerializer(lambda model: getattr(model, '__qualname__', None), return_type=str),
]
