from typing import Literal, cast

ForwarderHttpConfigurationMethod = Literal["DELETE", "GET", "PATCH", "POST", "PUT"]

FORWARDER_HTTP_CONFIGURATION_METHOD_VALUES: set[ForwarderHttpConfigurationMethod] = {
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
}


def check_forwarder_http_configuration_method(value: str) -> ForwarderHttpConfigurationMethod:
    if value in FORWARDER_HTTP_CONFIGURATION_METHOD_VALUES:
        return cast(ForwarderHttpConfigurationMethod, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FORWARDER_HTTP_CONFIGURATION_METHOD_VALUES!r}")
