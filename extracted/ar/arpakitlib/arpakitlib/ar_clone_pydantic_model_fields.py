# arpakit
from typing import Any, Type, Iterable

from pydantic import BaseModel, create_model
from pydantic_core import PydanticUndefined

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def clone_pydantic_model_fields(
        *,
        model_cls: Type[BaseModel],
        fields_to_remove: Iterable[str] | None = None,
        new_class_name: str | None = None,
) -> Type[BaseModel]:
    if fields_to_remove is None:
        fields_to_remove = set()
    if new_class_name is None:
        new_class_name = f"{model_cls.__name__}Cloned"

    field_defs: dict[str, tuple[type[Any], Any]] = {}

    for field_name, field_ in model_cls.model_fields.items():
        if field_name in fields_to_remove:
            continue

        if field_.default_factory is not None and field_.default is PydanticUndefined:
            default = field_
        elif field_.default is not PydanticUndefined:
            default = field_.default
        else:
            default = field_

        field_defs[field_name] = ((field_.annotation or Any), default)

    return create_model(
        new_class_name,
        __base__=BaseModel,
        **field_defs,
    )


def __example():
    pass


if __name__ == '__main__':
    __example()
