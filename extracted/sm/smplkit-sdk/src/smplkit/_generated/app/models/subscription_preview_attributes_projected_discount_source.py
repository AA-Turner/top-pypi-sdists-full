from typing import Literal, cast

SubscriptionPreviewAttributesProjectedDiscountSource = Literal["OVERRIDE", "VOLUME"]

SUBSCRIPTION_PREVIEW_ATTRIBUTES_PROJECTED_DISCOUNT_SOURCE_VALUES: set[
    SubscriptionPreviewAttributesProjectedDiscountSource
] = {
    "OVERRIDE",
    "VOLUME",
}


def check_subscription_preview_attributes_projected_discount_source(
    value: str,
) -> SubscriptionPreviewAttributesProjectedDiscountSource:
    if value in SUBSCRIPTION_PREVIEW_ATTRIBUTES_PROJECTED_DISCOUNT_SOURCE_VALUES:
        return cast(SubscriptionPreviewAttributesProjectedDiscountSource, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {SUBSCRIPTION_PREVIEW_ATTRIBUTES_PROJECTED_DISCOUNT_SOURCE_VALUES!r}"
    )
