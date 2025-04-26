from typing import Type, TypeVar
from warnings import warn

T = TypeVar("T")


def create_model_with_defaults(model_type: Type[T], **kwargs) -> T:
    warn(
        "This function is deprecated and will be removed in version 2.x",
        DeprecationWarning,
        stacklevel=2,
    )
    return model_type(**kwargs)
