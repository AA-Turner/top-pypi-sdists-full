from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name,
    resource_id: str,
) -> Dict:
    """
    Use an un-managed vpc_endpoint as a data-source. Supply resource_id as a filter.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str):
            An AWS vpc_endpoint resource_id to identify the resource.

    Returns:
        Dict[bool, list, dict or None]:

    Examples:
        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.ec2.vpc_endpoint.get name="idem_name" resource_id="resource_id"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ec2.vpc_endpoint.get
                - kwargs:
                    name: my_resource
                    resource_id: resource_id
    """

    result = dict(comment=[], ret=None, result=True)

    resource_ret = await hub.exec.boto3.client.ec2.describe_vpc_endpoints(
        ctx, VpcEndpointIds=[resource_id]
    )

    if not resource_ret["result"]:
        if "InvalidVpcEndpointId.NotFound" in str(resource_ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.vpc_endpoint", name=name
                )
            )
            result["comment"] += list(resource_ret["comment"])
            return result
        result["comment"] += list(resource_ret["comment"])
        result["result"] = resource_ret["result"]
        return result

    if not resource_ret["ret"]["VpcEndpoints"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.vpc_endpoint", name=name
            )
        )
        return result

    result[
        "ret"
    ] = hub.tool.aws.ec2.conversion_utils.convert_raw_vpc_endpoint_to_present(
        raw_resource=resource_ret["ret"]["VpcEndpoints"][0], idem_resource_name=name
    )

    return result


async def list_(hub, ctx, name: str = None, filters=None) -> Dict:
    """
    Use an un-managed VPC Endpoints as a data-source.

    Args:
        name (str, Optional):
            The name of the Idem state.

        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpc_endpoints

    Returns:
        Dict[bool, list, dict or None]:

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.ec2.vpc_endpoint.list name="idem_name"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ec2.vpc_endpoint.list
                - kwargs:
                    name: my_resource

    """
    result = dict(comment=[], ret=[], result=True)
    if filters:
        filters = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
            filters=filters
        )
    ret = await hub.exec.boto3.client.ec2.describe_vpc_endpoints(ctx, Filters=filters)
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["VpcEndpoints"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.vpc_endpoint", name=name
            )
        )
        return result
    for vpc_endpoint in ret["ret"]["VpcEndpoints"]:
        resource_id = vpc_endpoint.get("VpcEndpointId")
        converted_resource = (
            hub.tool.aws.ec2.conversion_utils.convert_raw_vpc_endpoint_to_present(
                vpc_endpoint, idem_resource_name=resource_id
            )
        )
        result["ret"].append(converted_resource)
    return result
