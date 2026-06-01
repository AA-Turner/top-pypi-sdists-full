from typing import Literal, cast

PlanResourceType = Literal["plan"]

PLAN_RESOURCE_TYPE_VALUES: set[PlanResourceType] = {
    "plan",
}


def check_plan_resource_type(value: str) -> PlanResourceType:
    if value in PLAN_RESOURCE_TYPE_VALUES:
        return cast(PlanResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PLAN_RESOURCE_TYPE_VALUES!r}")
