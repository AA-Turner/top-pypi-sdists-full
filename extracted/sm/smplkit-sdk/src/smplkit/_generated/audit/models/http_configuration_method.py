from typing import Literal, cast

HttpConfigurationMethod = Literal["DELETE", "GET", "PATCH", "POST", "PUT"]

HTTP_CONFIGURATION_METHOD_VALUES: set[HttpConfigurationMethod] = {
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
}


def check_http_configuration_method(value: str) -> HttpConfigurationMethod:
    if value in HTTP_CONFIGURATION_METHOD_VALUES:
        return cast(HttpConfigurationMethod, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {HTTP_CONFIGURATION_METHOD_VALUES!r}")
