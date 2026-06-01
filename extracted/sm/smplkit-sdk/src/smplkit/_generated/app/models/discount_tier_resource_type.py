from typing import Literal, cast

DiscountTierResourceType = Literal["discount_tier"]

DISCOUNT_TIER_RESOURCE_TYPE_VALUES: set[DiscountTierResourceType] = {
    "discount_tier",
}


def check_discount_tier_resource_type(value: str) -> DiscountTierResourceType:
    if value in DISCOUNT_TIER_RESOURCE_TYPE_VALUES:
        return cast(DiscountTierResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DISCOUNT_TIER_RESOURCE_TYPE_VALUES!r}")
