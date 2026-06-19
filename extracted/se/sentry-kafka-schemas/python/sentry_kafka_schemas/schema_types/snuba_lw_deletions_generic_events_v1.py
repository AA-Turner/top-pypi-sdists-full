from typing import List, TypedDict, Dict, Required, Union


class LwDeleteGenericEvents(TypedDict, total=False):
    """ lw_delete_generic_events. """

    storage_name: Required[str]
    """ Required property """

    rows_to_delete: Required[int]
    """ Required property """

    conditions: Required["_LwDeleteGenericEventsConditions"]
    """ Required property """

    tenant_ids: Required[Dict[str, "_LwDeleteGenericEventsTenantIdsAdditionalproperties"]]
    """ Required property """



class _LwDeleteGenericEventsConditions(TypedDict, total=False):
    project_id: List[int]
    group_id: List[int]


_LwDeleteGenericEventsTenantIdsAdditionalproperties = Union[str, "_LwDeleteGenericEventsTenantIdsAdditionalpropertiesAnyof1"]
""" Aggregation type: anyOf """



_LwDeleteGenericEventsTenantIdsAdditionalpropertiesAnyof1 = int
""" minimum: 1 """

