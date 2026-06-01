from typing import Literal, cast

ForwarderType = Literal["datadog", "elastic", "honeycomb", "http", "new_relic", "splunk_hec", "sumo_logic"]

FORWARDER_TYPE_VALUES: set[ForwarderType] = {
    "datadog",
    "elastic",
    "honeycomb",
    "http",
    "new_relic",
    "splunk_hec",
    "sumo_logic",
}


def check_forwarder_type(value: str) -> ForwarderType:
    if value in FORWARDER_TYPE_VALUES:
        return cast(ForwarderType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FORWARDER_TYPE_VALUES!r}")
