from typing import Dict
from typing import List


async def search_raw(
    hub,
    ctx,
    zone_names: List = None,
    zone_ids: List = None,
    all_availability_zones: bool = None,
    filters: List = None,
) -> Dict:
    """
    Fetch one or more availability zones from AWS. The return will be in the same format as what the boto3 api returns.

    Args:
        hub: The redistributed pop central hub.
        ctx: The context.
        zone_names(List, Optional): The names of the AWS Availability Zones, Local Zones, and Wavelength Zones to search.
        zone_ids(List, Optional): The ids of the AWS Availability Zones, Local Zones, and Wavelength Zones to search.
        all_availability_zones(bool, Optional): Indicate whether to include all AWS Availability Zones, Local Zones, and Wavelength Zones regardless of the opt-in status.
        filters(list, Optional): One or more filters. For example: {"Name": "state", "Values": ["available"]},
          A complete list of filters can be found at https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_availability_zones

    Returns:
        {"result": True|False, "comment": A message List, "ret": Dict}
    """
    result = dict(comment=[], ret=None, result=True)

    syntax_validation = hub.tool.aws.search_utils.search_filter_syntax_validation(
        filters=filters
    )
    if not syntax_validation["result"]:
        result["result"] = False
        result["comment"] = list(syntax_validation["comment"])
        return result
    boto3_filter = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
        filters=filters
    )

    ret = await hub.exec.boto3.client.ec2.describe_availability_zones(
        ctx,
        Filters=boto3_filter,
        ZoneNames=zone_names,
        ZoneIds=zone_ids,
        AllAvailabilityZones=all_availability_zones,
    )
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]

    return result
