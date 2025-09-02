"""Utility functions for EC2 VPC Endpoint Service Permissions."""
from typing import Any
from typing import Dict


async def convert_raw_resource_to_present_async(
    hub, ctx, idem_resource_name: str, resource_id: str, raw_resource: dict
) -> Dict[str, Any]:
    r"""
    Convert raw resource of vpc_endpoint_service_permission type into present format.

    Args:
        idem_resource_name(str): An Idem name of the resource.

        resource_id(str): An identifier of the resource in the provider.

        raw_resource(dict): The raw representation of the resource in the provider.

    Returns:
        Dict[str, Any]
    """
    resource_translated = {}

    resource_parameters = {
        "PrincipalType": "principal_type",
        "Principal": "principal_arn",
        "ServicePermissionId": "service_permission_id",
    }

    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    resource_translated["name"] = idem_resource_name or raw_resource.get(
        "ServicePermissionId"
    )
    resource_translated["resource_id"] = (
        raw_resource.get("ServicePermissionId") or resource_id or idem_resource_name
    )

    if "Tags" in resource_translated:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )

    return resource_translated
