from typing import Literal, cast

JobHttpConfigurationMethod = Literal["DELETE", "GET", "PATCH", "POST", "PUT"]

JOB_HTTP_CONFIGURATION_METHOD_VALUES: set[JobHttpConfigurationMethod] = {
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
}


def check_job_http_configuration_method(value: str) -> JobHttpConfigurationMethod:
    if value in JOB_HTTP_CONFIGURATION_METHOD_VALUES:
        return cast(JobHttpConfigurationMethod, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {JOB_HTTP_CONFIGURATION_METHOD_VALUES!r}")
