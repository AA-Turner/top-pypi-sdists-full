from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}
__contracts__ = ["soft_fail"]


async def get(
    hub,
    ctx,
    name: str = None,
    resource_id: str = None,
    filters: List[Dict[str, str]] = None,
) -> Dict:
    """
    Get a Network Interface resource from AWS. Supply one of the inputs as the filter.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str, Optional):
            AWS Network Interface id to identify the resource.

        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
             https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_network_interfaces
    """
    result = dict(comment=[], ret=None, result=True)
    if filters:
        filters = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
            filters=filters
        )

    if resource_id:
        ret = await hub.exec.boto3.client.ec2.describe_network_interfaces(
            ctx,
            NetworkInterfaceIds=[resource_id],
            Filters=filters,
        )
    else:
        ret = await hub.exec.boto3.client.ec2.describe_network_interfaces(
            ctx,
            Filters=filters,
        )

    if not ret["result"]:
        if "InvalidNetworkInterfaceID.NotFound" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.network_interface", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    present_states = hub.tool.aws.ec2.network_interface.convert_to_present(ret.ret)

    # If the resource can't be found but there were no results then "result" is True and "ret" is None
    if not present_states:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.network_interface", name=name
            )
        )
        return result

    # return the first result as a plain dictionary
    result["ret"] = next(iter((present_states).values()))

    return result


async def list_(hub, ctx, name: str = None, filters: List = None) -> Dict:
    """
    Use an un-managed Network Interface as a data-source. Supply one of the inputs as the filter.

    Args:
        name(str, Optional):
            The name of the Idem state.

        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_network_interfaces
    """

    result = dict(comment=[], ret=[], result=True)
    if filters:
        filters = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
            filters=filters
        )
    ret = await hub.exec.boto3.client.ec2.describe_network_interfaces(
        ctx,
        Filters=filters,
    )

    # If there was an error in the call then report failure
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    present_states = hub.tool.aws.ec2.network_interface.convert_to_present(ret.ret)
    if not present_states:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.network_interface", name=name
            )
        )
        return result

    # Return a list of dictionaries with details about all the instances
    result["ret"] = list(present_states.values())

    return result


async def create(
    hub,
    ctx,
    *,
    name: str = None,
    client_token: str = None,
    subnet_id: str,
    description: str = None,
    groups: List[str] = None,
    interface_type: str = None,
    primary_ip_address: str = None,
    private_ip_addresses: List[str] = None,
    ipv4_address_count: int = None,
    ipv4_prefix_count: int = None,
    ipv4_prefixes: List[str] = None,
    ipv6_addresses: List[str] = None,
    ipv6_address_count: int = None,
    ipv6_prefix_count: int = None,
    ipv6_prefixes: List[str] = None,
    tags: Dict[str, str] = None,
    **kwargs,
):
    """
    Create a Network Interface
    """
    result = dict(comment=[], ret=[], result=True)

    # "describe" will define multiple of these parameters, some of which are mutually exclusive.
    validated_ipv6_addresses = None
    validated_ipv6_prefixes = None
    validated_ipv6_address_count = None
    validated_ipv4_addresses = None
    validated_ipv4_prefixes = None
    validated_ipv4_address_count = None

    # Default to specific addresses, fallback to prefixes, then count
    if ipv6_addresses:
        validated_ipv6_addresses = [{"IPv6Address": i} for i in ipv6_addresses]
    elif ipv6_prefixes:
        validated_ipv6_prefixes = [{"IPv6Prefix": i} for i in ipv6_prefixes]
    elif ipv6_address_count:
        validated_ipv6_address_count = ipv6_address_count

    # Add primary IP in the list of IPs, if it's not already there
    if primary_ip_address:
        if not private_ip_addresses:
            private_ip_addresses = [primary_ip_address]
        elif primary_ip_address not in private_ip_addresses:
            private_ip_addresses.append(primary_ip_address)

    # Default to specific addresses, fallback to prefixes, then count
    if private_ip_addresses:
        if not primary_ip_address:
            result["comment"].append(
                "When private_ip_addresses is used, the primary address should also be specified in primary_ip_address"
            )
            result["result"] = False
            return result

        validated_ipv4_addresses = [
            {"PrivateIpAddress": i, "Primary": primary_ip_address == i}
            for i in private_ip_addresses
        ]
    elif ipv4_prefixes:
        validated_ipv4_prefixes = [{"Ipv4Prefix": i} for i in ipv4_prefixes]
    elif ipv4_address_count:
        validated_ipv4_address_count = ipv4_address_count

    tag_specification = None
    if tags:
        tag_specification = [
            {
                "ResourceType": "network-interface",
                "Tags": [{"Key": k, "Value": v} for k, v in tags.items()],
            }
        ]

    ret = await hub.exec.boto3.client.ec2.create_network_interface(
        ctx,
        **{
            "Description": description,
            "Groups": groups,
            "Ipv6Addresses": validated_ipv6_addresses,
            # If concrete IPs are specified in the request, all IPs are included in this list, even the primary IP
            "PrivateIpAddresses": validated_ipv4_addresses,
            "Ipv4Prefixes": validated_ipv4_prefixes,
            "Ipv6Prefixes": validated_ipv6_prefixes,
            "SecondaryPrivateIpAddressCount": validated_ipv4_address_count,
            "Ipv6AddressCount": validated_ipv6_address_count,
            "Ipv4PrefixCount": ipv4_prefix_count,
            "Ipv6PrefixCount": ipv6_prefix_count,
            "InterfaceType": interface_type,
            "SubnetId": subnet_id,
            "TagSpecifications": tag_specification,
            "ClientToken": client_token,
        },
    )
    result["result"] = ret["result"]
    if not result["result"]:
        result["comment"] = ret["comment"]
        return result

    result["comment"] += [f"Created '{name}'"]
    resource_id = ret.ret["NetworkInterface"]["NetworkInterfaceId"]
    result["new_state"] = dict(name=name, resource_id=resource_id)

    present_ret = hub.tool.aws.ec2.network_interface.convert_to_present(
        describe_network_interfaces={"NetworkInterfaces": [ret.ret["NetworkInterface"]]}
    )
    result["ret"] = present_ret[resource_id]
    return result


async def update(
    hub,
    ctx,
    **kwargs,
):
    """
    Update a Network Interface
    """
    result = dict(comment=[], ret=[], result=True)
    return result


async def delete(hub, ctx, *, name: str = None, resource_id: str, **kwargs):
    """
    Delete a Network Interface
    """
    result = dict(comment=[], ret=[], result=True)
    ret = await hub.exec.boto3.client.ec2.delete_network_interface(
        ctx, **{"NetworkInterfaceId": resource_id}
    )
    result["result"] = ret["result"]
    if not result["result"]:
        result["comment"] = ret["comment"]
        result["result"] = False
        return result
    result["comment"] += [f"Deleted '{name}'"]

    return result
