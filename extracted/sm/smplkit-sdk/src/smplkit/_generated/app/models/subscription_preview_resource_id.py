from typing import Literal, cast

SubscriptionPreviewResourceId = Literal["preview"]

SUBSCRIPTION_PREVIEW_RESOURCE_ID_VALUES: set[SubscriptionPreviewResourceId] = {
    "preview",
}


def check_subscription_preview_resource_id(value: str) -> SubscriptionPreviewResourceId:
    if value in SUBSCRIPTION_PREVIEW_RESOURCE_ID_VALUES:
        return cast(SubscriptionPreviewResourceId, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SUBSCRIPTION_PREVIEW_RESOURCE_ID_VALUES!r}")
