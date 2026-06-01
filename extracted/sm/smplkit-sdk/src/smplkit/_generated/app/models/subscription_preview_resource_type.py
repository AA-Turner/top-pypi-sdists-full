from typing import Literal, cast

SubscriptionPreviewResourceType = Literal["subscription_preview"]

SUBSCRIPTION_PREVIEW_RESOURCE_TYPE_VALUES: set[SubscriptionPreviewResourceType] = {
    "subscription_preview",
}


def check_subscription_preview_resource_type(value: str) -> SubscriptionPreviewResourceType:
    if value in SUBSCRIPTION_PREVIEW_RESOURCE_TYPE_VALUES:
        return cast(SubscriptionPreviewResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SUBSCRIPTION_PREVIEW_RESOURCE_TYPE_VALUES!r}")
