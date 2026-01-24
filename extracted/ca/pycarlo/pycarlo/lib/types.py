"""
Custom GraphQL types for the Monte Carlo Python Schema Library.

This module provides custom implementations of/replacements for sgqlc types that are used
in the auto-generated schema.
"""

import logging
from typing import Any, Optional, Union

import sgqlc.types

logger = logging.getLogger(__name__)


class Enum(sgqlc.types.Enum):
    """
    A backward-compatible GraphQL enum type that gracefully handles unknown values.

    Problem:
    When new enum values are added to the Monte Carlo GraphQL API, older SDK versions
    that don't have these values in their generated schema will crash with a ValueError
    when trying to deserialize API responses containing the new values.

    Solution:
    This custom Enum class returns unknown enum values as plain strings instead of
    raising an error. Since sgqlc enums are already represented as strings internally,
    this maintains full compatibility with existing code while preventing crashes.

    Behavior:
    - Known enum values: Returned as strings (same as sgqlc.types.Enum)
    - Unknown enum values: Returned as strings with a warning logged
    - All comparisons, collections, and operations work identically

    Example:
        # Previous Values for EntitlementTypes = ['SSO', 'MULTI_WORKSPACE']
        # API is updated to return new value: ['SSO', 'NEW_FEATURE', 'MULTI_WORKSPACE']

        # With standard sgqlc.types.Enum:
        # ValueError: EntitlementTypes does not accept value NEW_FEATURE

        # With this Enum:
        # Will return the new value as str and log a warning, no exception raised

        # Code still works:
        if 'SSO' in entitlements:  # Works
            enable_sso()
        if 'NEW_FEATURE' in entitlements:  # Also works
            enable_new_feature()
    """

    def __new__(
        cls, json_data: Any, _: Optional[Any] = None
    ) -> Union[str, sgqlc.types.Variable, None]:
        try:
            return sgqlc.types.get_variable_or_none(json_data)
        except ValueError:
            pass

        if json_data not in cls:
            # Log warning but don't crash - return the unknown value as a string
            logger.warning(
                f"Unknown enum value '{json_data}' for {cls.__name__}. "
                f"This may indicate the SDK is out of date. Returning raw string value."
            )
            return str(json_data)

        return str(json_data)
