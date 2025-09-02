"""Utility functions for Rds Db Proxy Target Groups."""
from typing import Any
from typing import Dict


async def convert_raw_resource_to_present_async(
    hub, ctx, idem_resource_name: str, resource_id: str, raw_resource: dict
) -> Dict[str, Any]:
    r"""
    Convert raw resource of db_proxy_target_group type into present format.

    """

    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}

    resource_parameters = {
        "ConnectionPoolConfig": "connection_pool_config",
        "DBProxyName": "db_proxy_name",
        "IsDefault": "is_default",
        "TargetGroupName": "target_group_name",
    }
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated
