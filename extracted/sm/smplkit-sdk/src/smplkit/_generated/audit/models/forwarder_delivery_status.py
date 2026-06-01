from typing import Literal, cast

ForwarderDeliveryStatus = Literal["FAILED", "FILTERED_OUT", "SKIPPED_DO_NOT_FORWARD", "SUCCEEDED"]

FORWARDER_DELIVERY_STATUS_VALUES: set[ForwarderDeliveryStatus] = {
    "FAILED",
    "FILTERED_OUT",
    "SKIPPED_DO_NOT_FORWARD",
    "SUCCEEDED",
}


def check_forwarder_delivery_status(value: str) -> ForwarderDeliveryStatus:
    if value in FORWARDER_DELIVERY_STATUS_VALUES:
        return cast(ForwarderDeliveryStatus, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FORWARDER_DELIVERY_STATUS_VALUES!r}")
