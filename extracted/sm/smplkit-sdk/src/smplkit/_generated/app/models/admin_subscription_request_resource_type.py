from typing import Literal, cast

AdminSubscriptionRequestResourceType = Literal["subscription"]

ADMIN_SUBSCRIPTION_REQUEST_RESOURCE_TYPE_VALUES: set[AdminSubscriptionRequestResourceType] = {
    "subscription",
}


def check_admin_subscription_request_resource_type(value: str) -> AdminSubscriptionRequestResourceType:
    if value in ADMIN_SUBSCRIPTION_REQUEST_RESOURCE_TYPE_VALUES:
        return cast(AdminSubscriptionRequestResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ADMIN_SUBSCRIPTION_REQUEST_RESOURCE_TYPE_VALUES!r}")
