from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str = None,
    resource_id: str = None,
    all_availability_zones: bool = None,
    filters: List = None,
) -> Dict:
    """
    Returns the list of AWS Availability Zones, Local Zones, and Wavelength Zones that are available
    within the region. The return will be in the same format as what the boto3 api returns.

    Args:
        name(str, Optional):
            The name of the AWS Availability Zone, Local Zone, or Wavelength Zone.

        resource_id(str, Optional):
            The id of the of the AWS Availability Zone, Local Zone, or Wavelength Zone.

        all_availability_zones(bool, Optional):
            Indicate whether to include all Availability Zones, Local Zones, and Wavelength Zones regardless of the opt-in status.

        filters(list[dict[str, Any]], Optional):
            One or more filters. For example: {"Name": "state", "Values": ["available"]},
            A complete list of filters can be found at https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_availability_zones

    .. code-block:: bash

        $ idem exec aws.ec2.availability_zones.get name=us-west-2b
    """
    result = dict(comment=[], ret=None, result=True)

    ret = await hub.tool.aws.ec2.availability_zones.search_raw(
        ctx=ctx,
        zone_names=[name] if name else None,
        zone_ids=[resource_id] if resource_id else None,
        all_availability_zones=all_availability_zones,
        filters=filters,
    )
    if not ret["result"]:
        result["result"] = False
        result["comment"] += list(ret["comment"])
        return result
    if not ret["ret"]["AvailabilityZones"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.availability_zones",
                name=name,
            )
        )
        return result

    resource = ret["ret"]["AvailabilityZones"][0]
    if len(ret["ret"]["AvailabilityZones"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_type="aws.ec2.availability_zones",
                resource_id=resource.get("ZoneId"),
            )
        )
    result[
        "ret"
    ] = hub.tool.aws.ec2.conversion_utils.convert_raw_availability_zone_to_snake_case(
        ctx, raw_resource=resource
    )

    return result


async def list_(
    hub, ctx, all_availability_zones: bool = None, filters: List = None
) -> Dict:
    """
    Returns the list of AWS Availability Zones, Local Zones, and Wavelength Zones that are available within the region.
    The return will be in the same format as what the boto3 api returns.

    Args:
        all_availability_zones(bool, Optional):
            Indicate whether to include all Availability Zones, Local Zones, and Wavelength Zones regardless of the opt-in status.

        filters(list[dict[str, Any]], Optional):
            One or more filters. For example: {"Name": "state", "Values": ["available"]}. A complete list of filters can
            be found at https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_availability_zones

    .. code-block:: bash

        $ idem exec aws.ec2.availability_zones.list all_availability_zones=true
    """
    result = dict(comment=[], ret=[], result=True)

    ret = await hub.tool.aws.ec2.availability_zones.search_raw(
        ctx=ctx,
        all_availability_zones=all_availability_zones,
        filters=filters,
    )
    if not ret["result"]:
        result["result"] = False
        result["comment"] += list(ret["comment"])
        return result
    if not ret["ret"]["AvailabilityZones"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.availability_zones"
            )
        )
        return result

    for az in ret["ret"]["AvailabilityZones"]:
        result["ret"].append(
            hub.tool.aws.ec2.conversion_utils.convert_raw_availability_zone_to_snake_case(
                ctx, raw_resource=az
            )
        )

    return result
