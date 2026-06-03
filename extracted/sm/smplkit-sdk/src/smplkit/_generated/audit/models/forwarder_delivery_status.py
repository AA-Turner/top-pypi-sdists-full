from typing import Literal, cast

ForwarderDeliveryStatus = Literal["FAILED", "SUCCEEDED"]

FORWARDER_DELIVERY_STATUS_VALUES: set[ForwarderDeliveryStatus] = {
    "FAILED",
    "SUCCEEDED",
}


def check_forwarder_delivery_status(value: str) -> ForwarderDeliveryStatus:
    if value in FORWARDER_DELIVERY_STATUS_VALUES:
        return cast(ForwarderDeliveryStatus, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FORWARDER_DELIVERY_STATUS_VALUES!r}")
