from typing import Union

from dealcloud_sdk.constants.auth import AVAILABLE_SCOPES

AvailableScopeTypes = Union[tuple[str], tuple[str, str], tuple[str, str, str]]


def validate_scope(scope: AvailableScopeTypes):
    """Check the assigned scope for DealCloudBase and validate all options are acceptable"""
    for s in scope:
        if s not in AVAILABLE_SCOPES:
            raise TypeError(f"s: {s} must be one of {AVAILABLE_SCOPES}")
