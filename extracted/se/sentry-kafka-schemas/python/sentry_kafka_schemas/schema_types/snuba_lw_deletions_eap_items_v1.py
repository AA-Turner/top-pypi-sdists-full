from typing import List, TypedDict, Dict, Required, Union


class LwDeleteEapItems(TypedDict, total=False):
    """ lw_delete_eap_items. """

    storage_name: Required[str]
    """ Required property """

    rows_to_delete: Required[int]
    """ Required property """

    conditions: Required["_LwDeleteEapItemsConditions"]
    """ Required property """

    tenant_ids: Required[Dict[str, "_LwDeleteEapItemsTenantIdsAdditionalproperties"]]
    """ Required property """



class _LwDeleteEapItemsConditions(TypedDict, total=False):
    organization_id: List[int]
    project_id: List[int]
    trace_id: List[str]


_LwDeleteEapItemsTenantIdsAdditionalproperties = Union[str, "_LwDeleteEapItemsTenantIdsAdditionalpropertiesAnyof1"]
""" Aggregation type: anyOf """



_LwDeleteEapItemsTenantIdsAdditionalpropertiesAnyof1 = int
""" minimum: 1 """

