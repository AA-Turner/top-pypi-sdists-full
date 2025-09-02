"""Utility functions for Rds Db Proxy Endpoints."""
from typing import Any
from typing import Dict


async def convert_raw_resource_to_present_async(
    hub, ctx, idem_resource_name: str, resource_id: str, raw_resource: dict
) -> Dict[str, Any]:
    r"""
    Convert raw resource of db_proxy_endpoint type into present format.

    """

    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}

    resource_parameters = {
        "DBProxyName": "db_proxy_name",
        "DBProxyEndpointName": "db_proxy_endpoint_name",
        "VpcSecurityGroupIds": "vpc_security_group_ids",
        "VpcSubnetIds": "vpc_subnet_ids",
        "TargetRole": "target_role",
    }

    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    # Get it from raw_resource or explicitly retrieved tags
    resource_tags_list = raw_resource.get("Tags") or raw_resource.get("TagList")

    if resource_tags_list:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            resource_tags_list
        )
    else:
        tags_ret = await hub.tool.aws.rds.tag.get_tags_for_resource(
            ctx, resource_arn=raw_resource.get("DBProxyEndpointArn")
        )
        if tags_ret["result"]:
            resource_translated["tags"] = tags_ret.get("ret", {})

    return resource_translated
