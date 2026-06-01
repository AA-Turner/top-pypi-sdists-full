from typing import Literal, cast

ContextTypeResourceType = Literal["context_type"]

CONTEXT_TYPE_RESOURCE_TYPE_VALUES: set[ContextTypeResourceType] = {
    "context_type",
}


def check_context_type_resource_type(value: str) -> ContextTypeResourceType:
    if value in CONTEXT_TYPE_RESOURCE_TYPE_VALUES:
        return cast(ContextTypeResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CONTEXT_TYPE_RESOURCE_TYPE_VALUES!r}")
