from typing import Required, Literal, TypedDict, Union


class SharedResourcesUsage(TypedDict, total=False):
    """ shared_resources_usage. """

    timestamp: Required[int]
    """ Required property """

    shared_resource_id: Required[str]
    """ Required property """

    app_feature: Required[str]
    """ Required property """

    usage_unit: Required["_SharedResourcesUsageUsageUnit"]
    """ Required property """

    amount: Required[int]
    """ Required property """



_SharedResourcesUsageUsageUnit = Union[Literal['bytes'], Literal['milliseconds'], Literal['milliseconds_sec']]
_SHAREDRESOURCESUSAGEUSAGEUNIT_BYTES: Literal['bytes'] = "bytes"
"""The values for the '_SharedResourcesUsageUsageUnit' enum"""
_SHAREDRESOURCESUSAGEUSAGEUNIT_MILLISECONDS: Literal['milliseconds'] = "milliseconds"
"""The values for the '_SharedResourcesUsageUsageUnit' enum"""
_SHAREDRESOURCESUSAGEUSAGEUNIT_MILLISECONDS_SEC: Literal['milliseconds_sec'] = "milliseconds_sec"
"""The values for the '_SharedResourcesUsageUsageUnit' enum"""

