from typing import Literal, cast

EnvironmentClassification = Literal["AD_HOC", "STANDARD"]

ENVIRONMENT_CLASSIFICATION_VALUES: set[EnvironmentClassification] = {
    "AD_HOC",
    "STANDARD",
}


def check_environment_classification(value: str) -> EnvironmentClassification:
    if value in ENVIRONMENT_CLASSIFICATION_VALUES:
        return cast(EnvironmentClassification, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ENVIRONMENT_CLASSIFICATION_VALUES!r}")
