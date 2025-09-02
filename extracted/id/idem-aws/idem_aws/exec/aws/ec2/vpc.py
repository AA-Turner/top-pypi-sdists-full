"""Exec module for managing EC2 Virtual Private Gateways."""
from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name,
    resource_id: str = None,
    default: bool = None,
    filters: List = None,
) -> Dict:
    """
    Get a VPC resource from AWS

    Args:
        name (str):
            The name of the Idem state

        resource_id (str, Optional):
            ID of the VPC

        default (bool, Optional):
            Indicate whether the VPC is the default VPC

        filters (list[str], Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpcs

    Returns:
        Dict[str, Any]:
            Returns VPC in present format

    Examples:
        Calling this exec module function from the cli with filters

        .. code-block:: bash

            idem exec aws.ec2.vpc.get name="my_resource"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ec2.vpc.get
                - kwargs:
                    name: my_resource
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.tool.aws.ec2.vpc.search_raw(
        ctx=ctx,
        name=name,
        resource_id=resource_id,
        default=default,
        filters=filters,
    )
    if not ret["result"]:
        if "InvalidVpcID.NotFound" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.vpc", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["Vpcs"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.vpc", name=name
            )
        )
        return result

    resource = ret["ret"]["Vpcs"][0]
    if len(ret["ret"]["Vpcs"]) > 1:
        result["comment"].append(
            f"More than one aws.ec2.vpc resource was found. Use resource {resource.get('VpcId')}"
        )
    result[
        "ret"
    ] = await hub.tool.aws.ec2.conversion_utils.convert_raw_vpc_to_present_async(
        ctx, raw_resource=resource, idem_resource_name=name
    )
    return result


async def list_(
    hub, ctx, name: str = None, filters: List = None, default: bool = None
) -> Dict:
    """
    Get a list of VPC resources from AWS

    Args:
        name (str, Optional):
            The name of the Idem state

        default(bool, Optional):
            Indicate whether the VPC is the default VPC

        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpcs

    Returns:
        Dict[str, Any]:
            Returns VPC in present format

    Examples:
        Calling this exec module function from the cli with filters

        .. code-block:: bash

            idem exec aws.ec2.vpc.get name="my_resource"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ec2.vpc.get
                - kwargs:
                    name: my_resource
    """
    result = dict(comment=[], ret=[], result=True)
    ret = await hub.tool.aws.ec2.vpc.search_raw(
        ctx=ctx,
        name=name,
        default=default,
        filters=filters,
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["Vpcs"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.vpc", name=name
            )
        )
        return result
    for vpc in ret["ret"]["Vpcs"]:
        vpc_id = vpc.get("VpcId")
        result["ret"].append(
            await hub.tool.aws.ec2.conversion_utils.convert_raw_vpc_to_present_async(
                ctx, raw_resource=vpc, idem_resource_name=vpc_id
            )
        )
    return result
