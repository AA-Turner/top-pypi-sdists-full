from typing import Literal, cast

SubscriptionChangeProjectionEffect = Literal["IMMEDIATE", "NEXT_PERIOD"]

SUBSCRIPTION_CHANGE_PROJECTION_EFFECT_VALUES: set[SubscriptionChangeProjectionEffect] = {
    "IMMEDIATE",
    "NEXT_PERIOD",
}


def check_subscription_change_projection_effect(value: str) -> SubscriptionChangeProjectionEffect:
    if value in SUBSCRIPTION_CHANGE_PROJECTION_EFFECT_VALUES:
        return cast(SubscriptionChangeProjectionEffect, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SUBSCRIPTION_CHANGE_PROJECTION_EFFECT_VALUES!r}")
