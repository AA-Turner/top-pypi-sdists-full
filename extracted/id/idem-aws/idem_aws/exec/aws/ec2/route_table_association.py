"""Exec module for managing EC2 route table associations."""
from typing import Dict


async def get(
    hub,
    ctx,
    route_table_id: str,
    name: str = None,
    resource_id: str = None,
    gateway_id: str = None,
    subnet_id: str = None,
) -> Dict:
    """
    Get a route table association of a route table using Association ID, Gateway ID or Subnet ID.

    Args:
        route_table_id(str):
            ID of the AWS Route table.

        name(str, Optional):
            The name of the Idem state.

        resource_id(str, Optional):
            The route table association ID.

        gateway_id(str, Optional):
            The ID of the internet gateway or virtual private gateway.

        subnet_id(str, Optional):
            The ID of the subnet.


    Returns:
        Dict[str, Any]:
            Returns security group in present format

    Examples:
        Calling this exec module function from the cli with filters

        .. code-block:: bash

            idem exec aws.ec2.route_table_association.get name="my_resource" route_table_id=rtb-13ewdeae  resource_id=rtbassoc-0rera607rre12a2c5

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ec2.route_table_association.get
                - kwargs:
                    name: my_resource
                    route_table_id: rtb-13ewdeae
                    resource_id: rtbassoc-0rera607rre12a2c5
    """
    result = dict(comment=[], ret=None, result=True)

    route_table_ret = await hub.exec.boto3.client.ec2.describe_route_tables(
        ctx, RouteTableIds=[route_table_id]
    )

    if not route_table_ret["result"]:
        if "InvalidRouteTableID.NotFound" in str(route_table_ret.get("comment", "")):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.route_table_association", name=name
                )
            )
            result["result"] = False
            result["comment"] += list(route_table_ret["comment"])
            return result
        result["comment"] += list(route_table_ret.get("comment", ""))
        result["result"] = False
        return result

    if not route_table_ret.get("ret", {}).get("RouteTables"):
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.route_table_association", name=name
            )
        )
        return result

    resource = route_table_ret["ret"].get("RouteTables")[0]
    association = hub.tool.aws.ec2.route_table.get_route_table_association_by_id(
        resource["Associations"],
        resource_id=resource_id,
        gateway_id=gateway_id,
        subnet_id=subnet_id,
    )

    if not association["result"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.route_table_association", name=name
            )
        )
        return result

    result[
        "ret"
    ] = hub.tool.aws.ec2.conversion_utils.convert_raw_route_table_association_to_present(
        resource=association["ret"],
        idem_resource_name=name,
    )
    return result
