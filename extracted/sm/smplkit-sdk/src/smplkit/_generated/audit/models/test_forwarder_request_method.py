from typing import Literal, cast

TestForwarderRequestMethod = Literal["DELETE", "GET", "PATCH", "POST", "PUT"]

TEST_FORWARDER_REQUEST_METHOD_VALUES: set[TestForwarderRequestMethod] = {
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
}


def check_test_forwarder_request_method(value: str) -> TestForwarderRequestMethod:
    if value in TEST_FORWARDER_REQUEST_METHOD_VALUES:
        return cast(TestForwarderRequestMethod, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TEST_FORWARDER_REQUEST_METHOD_VALUES!r}")
