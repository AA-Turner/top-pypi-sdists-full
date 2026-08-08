# Python internals
from enum import StrEnum
from typing import Protocol


class FeatureFlag(StrEnum):
    """Registry of WorkOS feature flag slugs."""


class _FeatureFlagsCarrier(Protocol):
    feature_flags: list[str]


def has_feature_flag(carrier: _FeatureFlagsCarrier, flag: FeatureFlag) -> bool:
    return flag.value in carrier.feature_flags
