from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator, Field, PlainSerializer

from fitrequest.errors import InvalidResponseTypeError
from fitrequest.method_models import environment_models
from fitrequest.utils import is_basemodel_subclass


def validate_init_value(value: Any) -> type[BaseModel] | None:
    """
    Validate the response model.
    If a string is given, attempts to retrieve the corresponding model from the global environment.
    Raise an `InvalidResponseTypeError` if the provided value has an incorrect type.
    """
    if isinstance(value, str):
        value = environment_models.get(value, value)

    if is_basemodel_subclass(value):
        return value

    if value is None:
        return None

    raise InvalidResponseTypeError(provided_model=value)


ValidResponse = Annotated[
    type[BaseModel] | str | None,
    Field(validate_default=True),
    BeforeValidator(validate_init_value),
    PlainSerializer(lambda model: getattr(model, '__qualname__', None), return_type=str),
]
