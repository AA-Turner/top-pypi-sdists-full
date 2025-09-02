"""Exec module for managing EC2 subnets."""
from typing import Any
from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name,
    resource_id: str = None,
    availability_zone: str = None,
    availability_zone_id: str = None,
    cidr_block: str = None,
    default_for_az: str = None,
    filters: List = None,
    ipv6_cidr_block: str = None,
    status: str = None,
    vpc_id: str = None,
    tags: List[Dict[str, Any]] or Dict[str, str] = None,
) -> Dict:
    """Get EC2 subnet from AWS account.

    Get a single subnet from AWS. If more than one resource is found, the first resource returned from AWS will be used.
    The function returns None when no resource is found.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str, Optional):
            AWS subnet id to identify the resource.

        availability_zone(str, Optional):
            The Availability Zone for the subnet.

        availability_zone_id(str, Optional):
            The ID of the Availability Zone for the subnet.

        cidr_block(str, Optional):
            The IPv4 CIDR block of the subnet. The CIDR block you specify must exactly match
            the subnet's CIDR block for information to be returned for the subnet.

        default_for_az(str, Optional):
            Indicate whether the subnet is the default subnet in the Availability Zone.

        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_subnets

        ipv6_cidr_block(str, Optional): An IPv6 CIDR block associated with the subnet.

        status(str, Optional): The state of the subnet (pending | available ).

        vpc_id(str, Optional):
            The ID of the VPC for the subnet.

        tags(list or dict, Optional):
            The list or dict of tags to filter by. For example, to find all resources that have a tag with the key
            "Owner" and the value "TeamA" , specify "tag:Owner" for the Dict key and "TeamA" for the Dict value.

            * Key (str):
                The key name for the tag to be used to filter by.

            * Value(str):
                The value associated with this tag to filter by.

    Returns:
        Dict[str, Any]:
            Returns ami in present format

    Examples:
        Calling this exec module function from the cli with filters

        .. code-block:: bash

            idem exec aws.ec2.subnet.get name="my_resource" filters=[{'name': 'name', 'values': ['subnet-name']}]

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ec2.subnet.get
                - kwargs:
                    name: my_resource
                    filters:
                        - name: 'name'
                          values: ["subnet-name"]
    """
    result = dict(comment=[], ret=None, result=True)
    if isinstance(tags, Dict):
        tags = hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
    ret = await hub.tool.aws.ec2.subnet.search_raw(
        ctx=ctx,
        name=name,
        resource_id=resource_id,
        availability_zone=availability_zone,
        availability_zone_id=availability_zone_id,
        cidr_block=cidr_block,
        default_for_az=default_for_az,
        filters=filters,
        ipv6_cidr_block=ipv6_cidr_block,
        status=status,
        vpc_id=vpc_id,
        tags=tags,
    )
    if not ret["result"]:
        if "InvalidSubnetID.NotFound" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.subnet", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["Subnets"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.subnet", name=name
            )
        )
        return result

    resource = ret["ret"]["Subnets"][0]
    if len(ret["ret"]["Subnets"]) > 1:
        result["comment"].append(
            f"More than one aws.ec2.subnet resource was found. Use resource {resource.get('SubnetId')}"
        )
    result["ret"] = hub.tool.aws.ec2.conversion_utils.convert_raw_subnet_to_present(
        raw_resource=resource, idem_resource_name=name
    )

    return result


async def list_(
    hub,
    ctx,
    name: str = None,
    availability_zone: str = None,
    availability_zone_id: str = None,
    cidr_block: str = None,
    default_for_az: str = None,
    filters: List = None,
    ipv6_cidr_block: str = None,
    status: str = None,
    vpc_id: str = None,
    tags: List[Dict[str, Any]] or Dict[str, str] = None,
) -> Dict:
    """List EC2 ami from AWS account.

    Fetch a list of subnets AWS. The function returns empty list when no resource is found.

    Args:
        name(str, Optional):
            The name of the Idem state.

        availability_zone(str, Optional):
            The Availability Zone for the subnet.

        availability_zone_id(str, Optional):
            The ID of the Availability Zone for the subnet.

        cidr_block(str, Optional):
            The IPv4 CIDR block of the subnet. The CIDR block you specify must exactly match
            the subnet's CIDR block for information to be returned for the subnet.

        default_for_az(str, Optional):
            Indicate whether the subnet is the default subnet in the Availability Zone.

        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_subnets

        ipv6_cidr_block(str, Optional):
            An IPv6 CIDR block associated with the subnet.

        status(str, Optional):
            The state of the subnet (pending | available ).

        vpc_id(str, Optional):
            The ID of the VPC for the subnet.

        tags(list or dict, Optional):
            The list or dict of tags to filter by. For example, to find all resources that have a tag with the key
            "Owner" and the value "TeamA" , specify "tag:Owner" for the Dict key and "TeamA" for the Dict value.

            * Key (str):
                The key name for the tag to be used to filter by.

            * Value(str):
                The value associated with this tag to filter by.

    Returns:
        Dict[str, Any]:
            Returns ami in present format

    Examples:
        Calling this exec module function from the cli with vpc_id

        .. code-block:: bash

            idem exec aws.ec2.subnet.list name="my_resources" vpc_id="vpc-a123"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resources:
              exec.run:
                - path: aws.ec2.subnet.list
                - kwargs:
                    name: my_resources
                    vcp_id: vpc-a123
    """
    result = dict(comment=[], ret=[], result=True)
    if isinstance(tags, Dict):
        tags = hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
    ret = await hub.tool.aws.ec2.subnet.search_raw(
        ctx=ctx,
        name=name,
        availability_zone=availability_zone,
        availability_zone_id=availability_zone_id,
        cidr_block=cidr_block,
        default_for_az=default_for_az,
        filters=filters,
        ipv6_cidr_block=ipv6_cidr_block,
        status=status,
        vpc_id=vpc_id,
        tags=tags,
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["Subnets"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.subnet", name=name
            )
        )
        return result
    for subnet in ret["ret"]["Subnets"]:
        subnet_id = subnet.get("SubnetId")
        result["ret"].append(
            hub.tool.aws.ec2.conversion_utils.convert_raw_subnet_to_present(
                raw_resource=subnet, idem_resource_name=subnet_id
            )
        )

    return result
