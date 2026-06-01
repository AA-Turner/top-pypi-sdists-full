from typing import Literal, cast

ContextResourceType = Literal["context"]

CONTEXT_RESOURCE_TYPE_VALUES: set[ContextResourceType] = {
    "context",
}


def check_context_resource_type(value: str) -> ContextResourceType:
    if value in CONTEXT_RESOURCE_TYPE_VALUES:
        return cast(ContextResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CONTEXT_RESOURCE_TYPE_VALUES!r}")
