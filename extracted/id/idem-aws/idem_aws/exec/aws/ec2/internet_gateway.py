from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}


async def list_(
    hub,
    ctx,
    name: str = None,
    filters: List = None,
) -> Dict:
    """
    Use an un-managed Internet Gateway as a data-source. Supply one of the inputs as the filter.

    Args:
        name(str): The name of the Idem state.
        filters(list, optional): One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
         https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_internet_gateways

    """
    result = dict(comment=[], ret=[], result=True)
    if filters:
        filters = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
            filters=filters
        )

    ret = await hub.exec.boto3.client.ec2.describe_internet_gateways(
        ctx,
        Filters=filters,
    )

    # If there was an error in the call then report failure
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    for internet_gateway in ret["ret"]["InternetGateways"]:
        resource_id = internet_gateway.get("InternetGatewayId")
        resource_converted = (
            hub.tool.aws.ec2.conversion_utils.convert_raw_internet_gateway_to_present(
                resource=internet_gateway, idem_resource_name=resource_id
            )
        )
        result["ret"].append(resource_converted)

    return result
