"""Exec module for managing EC2 VPC Endpoint Service Permissions."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["soft_fail"]

__func_alias__ = {"list_": "list"}


async def get(
    hub, ctx, service_id: str, principal_arn: str, name: str = None
) -> Dict[str, Any]:
    """
    Describes the principal (service consumer) that are permitted to discover your VPC endpoint service.

    Args:
        service_id(str): The ID of the service.

        principal_arn(str): The ARN of the principal.

        name(str, Optional): Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            unmanaged_resource:
              exec.run:
                - path: aws.ec2.vpc_endpoint_service_permission.get
                - kwargs:
                    - service_id: value
                    - principal_arn: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.ec2.vpc_endpoint_service_permission.get service_id=value principal_arn=value
    """

    result = dict(comment=[], ret=None, result=True)

    get = await hub.exec.boto3.client.ec2.describe_vpc_endpoint_service_permissions(
        ctx,
        **{
            "ServiceId": service_id,
            # Create filter for principal_arn
            "Filters": [
                {"Name": "principal", "Values": [principal_arn]},
            ],
        },
    )

    # Case: Error
    if not get["result"]:
        if "NotFound" in str(get["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.vpc_endpoint_service_permission",
                    name=service_id,
                )
            )
            result["comment"].append(get["comment"])
            return result

        result["comment"].append(get["comment"])
        result["result"] = False
        return result

    # Case: Empty results
    if not get["ret"] or not get["ret"]["AllowedPrincipals"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.vpc_endpoint_service_permission",
                name=service_id,
            )
        )
        return result

    if len(get["ret"]["AllowedPrincipals"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_id=service_id,
                resource_type="aws.ec2.vpc_endpoint_service_permission",
            )
        )

    # Taking first one
    raw_resource = get["ret"]["AllowedPrincipals"][0]

    result[
        "ret"
    ] = await hub.tool.aws.ec2.vpc_endpoint_service_permission.convert_raw_resource_to_present_async(
        ctx=ctx,
        resource_id=None,
        raw_resource=raw_resource,
        idem_resource_name=name,
    )

    return result


async def list_(
    hub,
    ctx,
    service_id: str,
    filters: List[
        make_dataclass(
            "Filter",
            [
                ("Name", str, field(default=None)),
                ("Values", List[str], field(default=None)),
            ],
        )
    ] = None,
) -> Dict[str, Any]:
    """
    Describes the principals (service consumers) that are permitted to discover your VPC endpoint service.

    Args:
        service_id(str): The ID of the service.

        filters(List[dict[str, Any]], Optional): The filters.

            * principal - The ARN of the principal.

            * principal-type - The principal type (All | Service | OrganizationUnit | Account | User | Role). Defaults to None.

            (structure)
             A filter name and value pair that is used to return a more specific list of results from a describe operation. Filters can be used to match a set of resources by specific criteria, such as tags, attributes, or IDs.

             If you specify multiple filters, the filters are joined with an AND , and the request returns only results that match all of the specified filters.

                 * Name(str): The name of the filter. Filter names are case-sensitive.

                 * Values(List[str]): The filter values. Filter values are case-sensitive. If you specify multiple values for a filter, the values are joined with an OR , and the request returns all results that match any of the specified values.

    Returns:
        Dict[str, Any]

    Examples:

        Resource State:

        .. code-block:: sls

            unmanaged_resources:
              exec.run:
                - path: aws.ec2.vpc_endpoint_service_permission.list
                - kwargs:
                    - service_id: value


        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.ec2.vpc_endpoint_service_permission.list service_id=value
    """

    result = dict(comment=[], ret=[], result=True)

    ret = await hub.exec.boto3.client.ec2.describe_vpc_endpoint_service_permissions(
        ctx, **{"ServiceId": service_id, "Filters": filters}
    )

    if not ret["result"]:
        result["comment"].append(ret["comment"])
        result["result"] = False
        return result

    if not ret["ret"].get("AllowedPrincipals"):
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.vpc_endpoint_service_permission", name=None
            )
        )
        return result

    for resource in ret["ret"]["AllowedPrincipals"]:
        result["ret"].append(
            await hub.tool.aws.ec2.vpc_endpoint_service_permission.convert_raw_resource_to_present_async(
                ctx=ctx,
                resource_id=None,
                raw_resource=resource,
                idem_resource_name=None,
            )
        )

    return result


async def create(
    hub, ctx, service_id: str, add_allowed_principals: List[str], name: str = None
) -> Dict[str, Any]:
    """
    Adds the permissions for your VPC endpoint service. You can add permissions for service consumers
    (Amazon Web Services accounts, users, and IAM roles) to connect to your endpoint service.

    If you grant permissions to all principals, the service is public. Any users who know the name of a public service can send a request to attach an endpoint. If the service does not require manual approval, attachments are automatically approved.

    Args:
        service_id(str): The ID of the service.

        add_allowed_principals(List[str]): The Amazon Resource Names (ARN) of the principals. Permissions are granted to the principals in this list. To grant permissions to all principals, specify an asterisk (*).

        name(str, Optional): Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            unmanaged_resources:
              exec.run:
                - path: aws.ec2.vpc_endpoint_service_permission.create:
                - kwargs:
                    - service_id: value
                    - add_allowed_principals:
                      - value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.ec2.vpc_endpoint_service_permission.create service_id=value add_allowed_principals=[values]
    """

    result = dict(comment=[], ret={}, result=True)

    ret = await hub.exec.boto3.client.ec2.modify_vpc_endpoint_service_permissions(
        ctx,
        **{
            "ServiceId": service_id,
            "AddAllowedPrincipals": add_allowed_principals,
        },
    )

    result["result"] = ret["result"]

    if not result["result"]:
        result["comment"].append(ret["comment"])
        return result

    result["comment"].append(
        f"Created aws.ec2.vpc_endpoint_service_permission '{name}'",
    )

    result["ret"]["resource_id"] = ret.get("ret", {}).get("ServicePermissionId")
    result["ret"]["name"] = name

    return result


async def update(
    hub,
    ctx,
    service_id: str,
    add_allowed_principals: List[str] = None,
    remove_allowed_principals: List[str] = None,
    name: str = None,
) -> Dict[str, Any]:
    """
    Modifies the permissions for your VPC endpoint service. You can add or remove permissions for service consumers
    (Amazon Web Services accounts, users, and IAM roles) to connect to your endpoint service.

    If you grant permissions to all principals, the service is public. Any users who know the name of a public service can send a
    request to attach an endpoint. If the service does not require manual approval, attachments are automatically
    approved.

    Args:
        service_id(str): The ID of the service.

        add_allowed_principals(List[str], Optional): The Amazon Resource Names (ARN) of the principals. Permissions are granted to the principals in this list. To grant permissions to all principals, specify an asterisk (*). Defaults to None.

        remove_allowed_principals(List[str], Optional): The Amazon Resource Names (ARN) of the principals.

        name(str, Optional): Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            unmanaged_resources:
              exec.run:
                - path: aws.ec2.vpc_endpoint_service_permission.update:
                - kwargs:
                    - service_id: value
                    - add_allowed_principals:
                        - value
                    - remove_allowed_principals:
                        - value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.ec2.vpc_endpoint_service_permission.update service_id=value add_allowed_principals=[values] remove_allowed_principals=[values]
    """

    result = dict(comment=[], ret={}, result=True)

    # If at least one of them is given
    if add_allowed_principals or remove_allowed_principals:
        ret = await hub.exec.boto3.client.ec2.modify_vpc_endpoint_service_permissions(
            ctx,
            **{
                "ServiceId": service_id,
                "AddAllowedPrincipals": add_allowed_principals,
                "RemoveAllowedPrincipals": remove_allowed_principals,
            },
        )

        if not ret["result"]:
            result["result"] = False
            result["comment"].append(
                f"Could not update aws.ec2.vpc_endpoint_service_permission '{name}'",
            )
            result["comment"].append(ret["comment"])
            return result

        result["comment"].append(
            f"Updated aws.ec2.vpc_endpoint_service_permission '{name}'",
        )

    if "AddedPrincipals" in ret["ret"]:
        result["ret"]["resource_id"] = ret.get("ret", {}).get("ServicePermissionId")

    result["ret"]["name"] = name

    return result


async def delete(
    hub,
    ctx,
    service_id: str,
    remove_allowed_principals: List[str] = None,
    name: str = None,
) -> Dict[str, Any]:
    """
    Removes the permissions for your VPC endpoint service. You can remove permissions for service consumers
    (Amazon Web Services accounts, users, and IAM roles) to connect to your endpoint service.

    Args:
        service_id(str): The ID of the service.

        remove_allowed_principals(List[str], Optional): The Amazon Resource Names (ARN) of the principals.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.ec2.vpc_endpoint_service_permission.absent:
                - service_id: value
                - remove_allowed_principals:
                    - value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.ec2.vpc_endpoint_service_permission.delete service_id=value remove_allowed_principals=[values]
    """

    result = dict(comment=[], ret=None, result=True)

    delete_ret = (
        await hub.exec.boto3.client.ec2.modify_vpc_endpoint_service_permissions(
            ctx,
            **{
                "ServiceId": service_id,
                "RemoveAllowedPrincipals": remove_allowed_principals,
            },
        )
    )

    result["result"] = delete_ret["result"]

    if not result["result"]:
        result["comment"] = delete_ret["comment"]
        result["result"] = False
        return result

    result["comment"] = hub.tool.aws.comment_utils.delete_comment(
        resource_type="aws.ec2.vpc_endpoint_service_permission", name=name
    )

    return result
