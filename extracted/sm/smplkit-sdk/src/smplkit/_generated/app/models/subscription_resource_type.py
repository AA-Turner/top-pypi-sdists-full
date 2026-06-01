from typing import Literal, cast

SubscriptionResourceType = Literal["subscription"]

SUBSCRIPTION_RESOURCE_TYPE_VALUES: set[SubscriptionResourceType] = {
    "subscription",
}


def check_subscription_resource_type(value: str) -> SubscriptionResourceType:
    if value in SUBSCRIPTION_RESOURCE_TYPE_VALUES:
        return cast(SubscriptionResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SUBSCRIPTION_RESOURCE_TYPE_VALUES!r}")
