from typing import Literal, cast

RunTrigger = Literal["MANUAL", "RERUN", "SCHEDULE"]

RUN_TRIGGER_VALUES: set[RunTrigger] = {
    "MANUAL",
    "RERUN",
    "SCHEDULE",
}


def check_run_trigger(value: str) -> RunTrigger:
    if value in RUN_TRIGGER_VALUES:
        return cast(RunTrigger, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {RUN_TRIGGER_VALUES!r}")
