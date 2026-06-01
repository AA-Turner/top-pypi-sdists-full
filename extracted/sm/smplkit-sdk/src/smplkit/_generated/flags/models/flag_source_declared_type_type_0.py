from typing import Literal, cast

FlagSourceDeclaredTypeType0 = Literal["BOOLEAN", "JSON", "NUMERIC", "STRING"]

FLAG_SOURCE_DECLARED_TYPE_TYPE_0_VALUES: set[FlagSourceDeclaredTypeType0] = {
    "BOOLEAN",
    "JSON",
    "NUMERIC",
    "STRING",
}


def check_flag_source_declared_type_type_0(value: str) -> FlagSourceDeclaredTypeType0:
    if value in FLAG_SOURCE_DECLARED_TYPE_TYPE_0_VALUES:
        return cast(FlagSourceDeclaredTypeType0, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FLAG_SOURCE_DECLARED_TYPE_TYPE_0_VALUES!r}")
