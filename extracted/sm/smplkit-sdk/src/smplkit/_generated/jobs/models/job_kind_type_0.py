from typing import Literal, cast

JobKindType0 = Literal["manual", "one_off", "recurring"]

JOB_KIND_TYPE_0_VALUES: set[JobKindType0] = {
    "manual",
    "one_off",
    "recurring",
}


def check_job_kind_type_0(value: str) -> JobKindType0:
    if value in JOB_KIND_TYPE_0_VALUES:
        return cast(JobKindType0, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {JOB_KIND_TYPE_0_VALUES!r}")
