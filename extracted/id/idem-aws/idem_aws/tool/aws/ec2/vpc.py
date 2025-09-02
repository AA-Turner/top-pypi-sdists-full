import copy
from typing import Any
from typing import Dict
from typing import List


async def search_raw(
    hub, ctx, name, filters: List = None, resource_id: str = None, default: bool = None
) -> Dict:
    """
    Fetch one or more subnets from AWS. The return will be in the same format as what the boto3 api returns.

    Args:
        name(str): The name of the Idem state.
        resource_id(str, Optional): AWS VPC id to identify the resource.
        default(bool, Optional): Indicate whether the VPC is the default VPC.
        filters(list, Optional): One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
         https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpcs

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
    if default is not None:
        boto3_filter.append({"Name": "is-default", "Values": [str(default).lower()]})
    ret = await hub.exec.boto3.client.ec2.describe_vpcs(
        ctx,
        Filters=boto3_filter,
        VpcIds=[resource_id] if resource_id else None,
    )
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]
    return result


async def update_cidr_blocks(
    hub,
    ctx,
    vpc_id: str,
    old_ipv4_cidr_blocks: List[Dict[str, Any]],
    old_ipv6_cidr_blocks: List[Dict[str, Any]],
    new_ipv4_cidr_blocks: List[Dict[str, Any]],
    new_ipv6_cidr_blocks: List[Dict[str, Any]],
):
    """
    Update associated cidr blocks of a vpc. This function compares the existing(old) cidr blocks and the
    new cidr blocks. Cidr blocks that are in the new_cidr_blocks but not in the old_cidr_blocks will be associated to
    vpc. Cidr blocks that are in the old_cidr_blocks but not in the new_cidr_blocks will be disassociated from vpc.

    Args:
        vpc_id: The AWS resource id of the existing vpc
        old_ipv4_cidr_blocks: The ipv4 cidr blocks on the existing vpc
        old_ipv6_cidr_blocks: The ipv6 cidr blocks on the existing vpc
        new_ipv4_cidr_blocks: The expected ipv4 cidr blocks on the existing vpc
        new_ipv6_cidr_blocks: The expected ipv6 cidr blocks on the existing vpc

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": Dict}
        The ret contains the updated values. It contains empty dict if no parameter has been updated.

    """
    # If a block is None, we'll skip updating such cidr block.
    if new_ipv4_cidr_blocks is None:
        new_ipv4_cidr_blocks = old_ipv4_cidr_blocks
    if new_ipv6_cidr_blocks is None:
        new_ipv6_cidr_blocks = old_ipv6_cidr_blocks
    result = dict(comment=[], result=True, ret={})
    ipv4_cidr_block_map = {
        cidr_block.get("CidrBlock"): cidr_block for cidr_block in old_ipv4_cidr_blocks
    }
    ipv6_cidr_block_map = {
        cidr_block.get("Ipv6CidrBlock"): cidr_block
        for cidr_block in old_ipv6_cidr_blocks
    }
    cidr_blocks_to_add = []
    ipv4_cidr_block_results = copy.deepcopy(ipv4_cidr_block_map)
    ipv6_cidr_block_results = copy.deepcopy(ipv6_cidr_block_map)
    for cidr_block_set in new_ipv4_cidr_blocks:
        if cidr_block_set.get("CidrBlock") not in ipv4_cidr_block_map:
            cidr_blocks_to_add.append(
                hub.tool.aws.network_utils.generate_cidr_request_payload_for_vpc(
                    cidr_block_set, "ipv4"
                )
            )
            ipv4_cidr_block_results[cidr_block_set.get("CidrBlock")] = cidr_block_set
        else:
            ipv4_cidr_block_map.pop(cidr_block_set.get("CidrBlock"), None)
    for ipv6_cidr_block_set in new_ipv6_cidr_blocks:
        if ipv6_cidr_block_set.get("Ipv6CidrBlock") not in ipv6_cidr_block_map:
            cidr_blocks_to_add.append(
                hub.tool.aws.network_utils.generate_cidr_request_payload_for_vpc(
                    ipv6_cidr_block_set, "ipv6"
                )
            )
            ipv6_cidr_block_results[
                ipv6_cidr_block_set.get("Ipv6CidrBlock")
            ] = ipv6_cidr_block_set
        else:
            ipv6_cidr_block_map.pop(ipv6_cidr_block_set.get("Ipv6CidrBlock"), None)
            ipv6_cidr_block_results.pop(ipv6_cidr_block_set.get("Ipv6CidrBlock"), None)
    cidr_blocks_to_remove = list(ipv4_cidr_block_map.values()) + list(
        ipv6_cidr_block_map.values()
    )
    for cidr_to_remove in ipv4_cidr_block_map:
        ipv4_cidr_block_results.pop(cidr_to_remove)
    for cidr_to_remove in ipv6_cidr_block_map:
        ipv6_cidr_block_results.pop(cidr_to_remove)
    if (not cidr_blocks_to_remove) and (not cidr_blocks_to_add):
        return result
    if not ctx.get("test", False):
        for cidr_block in cidr_blocks_to_remove:
            ret = await hub.exec.boto3.client.ec2.disassociate_vpc_cidr_block(
                ctx, AssociationId=cidr_block.get("AssociationId")
            )
            if not ret.get("result"):
                result["comment"] = ret["comment"]
                result["result"] = False
                return result
        for request_payload in cidr_blocks_to_add:
            ret = await hub.exec.boto3.client.ec2.associate_vpc_cidr_block(
                ctx, VpcId=vpc_id, **request_payload
            )
            if not ret.get("result"):
                result["comment"] = ret["comment"]
                result["result"] = False
                return result
    result["comment"] += [f"Update cidr_blocks"]
    result["ret"] = {
        "cidr_block_association_set": list(ipv4_cidr_block_results.values()),
        "ipv6_cidr_block_association_set": list(ipv6_cidr_block_results.values()),
    }
    return result


async def update_vpc_attributes(
    hub,
    ctx,
    enable_dns_hostnames,
    enable_dns_support,
    old_dns_hostnames,
    old_dns_support,
    resource_id,
):
    """
    Update enable_dns_hostnames and enable_dns_support of a vpc.

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": Dict}
        The ret contains the updated values. It contains empty dict if no parameter has been updated.
    """
    result = dict(comment=[], result=True, ret={})
    if enable_dns_support is not None and enable_dns_support != old_dns_support:
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.ec2.modify_vpc_attribute(
                ctx,
                EnableDnsSupport={"Value": enable_dns_support},
                VpcId=resource_id,
            )
            if not update_ret["result"]:
                result["result"] = False
                result["comment"] = update_ret["comment"]
        if result["result"]:
            result["ret"].update({"enable_dns_support": enable_dns_support})
    if enable_dns_hostnames is not None and enable_dns_hostnames != old_dns_hostnames:
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.ec2.modify_vpc_attribute(
                ctx,
                EnableDnsHostnames={"Value": enable_dns_hostnames},
                VpcId=resource_id,
            )
            if not update_ret["result"]:
                result["result"] = False
                result["comment"] += update_ret["comment"]
        if result["result"]:
            result["ret"].update({"enable_dns_hostnames": enable_dns_hostnames})
    return result
