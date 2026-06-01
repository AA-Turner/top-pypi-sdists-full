from typing import Literal, cast

ContextValueResourceType = Literal["context_value"]

CONTEXT_VALUE_RESOURCE_TYPE_VALUES: set[ContextValueResourceType] = {
    "context_value",
}


def check_context_value_resource_type(value: str) -> ContextValueResourceType:
    if value in CONTEXT_VALUE_RESOURCE_TYPE_VALUES:
        return cast(ContextValueResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CONTEXT_VALUE_RESOURCE_TYPE_VALUES!r}")
