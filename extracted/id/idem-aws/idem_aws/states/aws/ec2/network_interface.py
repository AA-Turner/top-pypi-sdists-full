"""
Manage Ec2 Network Interfaces
"""
from typing import Any
from typing import Dict
from typing import List

from dict_tools.typing import Computed

__contracts__ = ["resource", "allow_sync_sls_name_and_name_tag"]  # , "soft_fail"]


TREQ = {
    "present": {
        "require": [
            "aws.ec2.subnet.present",
        ],
    },
}


async def present(
    hub,
    ctx,
    *,
    name: str,
    subnet_id: str,
    resource_id: str = None,
    client_token: str = None,
    description: str = None,
    groups: List[str] = None,
    interface_type: str = None,
    default_ipv6_address: str = None,
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
    # Parameters cannot be used on creation
    # Computed Parameters (cannot be modified) # TODO some of these CAN be modified
    availability_zone: Computed[str] = None,
    mac_address: Computed[str] = None,
    outpost_arn: Computed[str] = None,
    owner_id: Computed[str] = None,
    private_dns_name: Computed[str] = None,
    requester_id: Computed[str] = None,
    requester_managed: Computed[str] = None,
    source_dest_check: Computed[str] = None,
    status: Computed[str] = None,
    vpc_id: Computed[str] = None,
    deny_all_igw_traffic: Computed[bool] = None,
    ipv6_native: Computed[bool] = None,
    # Association
    allocation_id: Computed[str] = None,
    ip_owner_id: Computed[str] = None,
    public_dns_name: Computed[str] = None,
    public_ip: Computed[str] = None,
    customer_owned_ip: Computed[str] = None,
    carrier_ip: Computed[str] = None,
    # Attachment
    attachment_id: Computed[str] = None,
    delete_on_termination: Computed[bool] = None,
    device_index: Computed[int] = None,
    network_card_index: Computed[int] = None,
    ena_srd_enabled: Computed[bool] = None,
    ena_srd_udp_enabled: Computed[bool] = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Creates a network interface in the specified subnet. The number of IP addresses you can assign to a network
    interface varies by instance type. For more information, see IP Addresses Per ENI Per Instance Type in the
    Amazon Virtual Private Cloud User Guide. For more information about network interfaces, see Elastic network
    interfaces in the Amazon Elastic Compute Cloud User Guide.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str):
            An identifier of the resource in the provider. Defaults to None.

        client_token(str, Optional):
            The idempotency token for the network interface.

        description(str, Optional):
            A description for the network interface. Defaults to None.

        groups(List[str], Optional): The IDs of one or more security groups. Defaults to None.

        ipv6_addresses(List[str]], Optional):
            The IPv6 addresses from the IPv6 CIDR block range of your subnet.  Defaults to None.

        default_ipv6_address(str, Optional):
            The default IPv6 address.

        primary_ip_address(str, Optional):
            The primary private IPv4 address of the network interface. If you don't specify an IPv4 address,
            Amazon EC2 selects one for you from the subnet's IPv4 CIDR range. Defaults to None.

        private_ip_addresses(List[str]], Optional):
            The private IPv4 addresses. If you specify the private IPv4 addresses, you should also specify the
            primary private IPv4 address using the primary_ip_address property. If you only need a primary private
            IPv4 address, you can specify it using the primary_ip_address property and not use this property.

        interface_type(str, Optional):
            The type of network interface. The default is interface. The only supported values are efa and
            trunk. Defaults to None.

        subnet_id(str):
            The ID of the subnet to associate with the network interface.

        tags(Dict[str, str], Optional):
            The tags to apply to the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            default_vpc:
              exec.run:
                - path: aws.ec2.vpc.get
                - kwargs:
                    filters:
                      - name: is-default
                        values:
                          - "true"

            default_subnet:
              exec.run:
                - path: aws.ec2.subnet.get
                - kwargs:
                    filters:
                      - name: vpc-id
                        values:
                          - ${exec:default_vpc:resource_id}

            my_network_interface:
              aws.ec2.network_interface.present:
                - subnet_id: ${exec:default_subnet:resource_id}
    """
    # Convert a list of dictionaries to a plain dictionary before calculating desired_state
    if isinstance(tags, list):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    # Get all the parameters passed to this function as a single dictionary
    desired_state = {
        k: v for k, v in locals().items() if k not in ("hub", "ctx", "kwargs")
    }

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    current_state = None
    if resource_id:
        get = await hub.exec.aws.ec2.network_interface.get(
            ctx, name=name, resource_id=resource_id
        )

        if get.result is True:
            if get.ret is None:
                result["comment"] += [
                    f"Could not find Network Interface for '{name}' with existing id '{resource_id}'"
                ]
                result["result"] = False
                return result
            else:
                result["comment"] += [f"Network Interface '{name}' already exists"]
                current_state = result["old_state"] = get.ret
    elif client_token:
        get = await hub.exec.aws.ec2.instance.get(
            ctx, name=name, filters=[{"Name": "client-token", "Values": [client_token]}]
        )

        if get.result is True:
            if get.ret is None:
                result["comment"] += [
                    f"Could not find Network Interface for '{name}' with existing idempotence token '{client_token}'"
                ]
            else:
                current_state = result["old_state"] = get.ret
                resource_id = current_state.resource_id
                result["comment"] += [f"Network Interface '{name}' already exists"]

    # No resource_id from cache or parameters, we need to create the resource
    if not resource_id:
        if ctx.test:
            result["new_state"] = desired_state
            result["comment"] += hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.ec2.network_interface", name=name
            )
            return result
        else:
            create_ret = await hub.exec.aws.ec2.network_interface.create(
                ctx, **desired_state
            )
            # If we fail to create the network interface, just return the proper error message
            if not create_ret["result"]:
                result["result"] = False
                result["comment"] += [create_ret.comment]
                return result

            result["comment"] += hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.ec2.network_interface", name=name
            )
            result["result"] &= create_ret.result
            result["new_state"] = current_state = create_ret.ret
            # This makes sure the created Network Interface is saved to esm regardless if the subsequent update call fails or not.
            result["force_save"] = True

    if not current_state:
        result["comment"] += [f"Unable to get the current_state: '{name}'"]
        result["result"] = False
        return result

    # Modify all the attributes that need modification
    if ctx.test:
        result["new_state"] = desired_state
    else:
        ctx.old_state = current_state
        await hub.exec.aws.ec2.network_interface.update(ctx, **desired_state)
        # The API could return empty response on certain situations (ref: API documentation)
        # Adding one of the recommended filters which is required for network interface to scope its lookup
        get = await hub.exec.aws.ec2.network_interface.get(
            ctx,
            name=name,
            resource_id=current_state["resource_id"],
            filters=[
                {
                    "Name": "subnet-id",
                    "Values": [
                        subnet_id,
                    ],
                },
            ],
        )
        if get.result:
            result["new_state"] = get.ret

    return result


async def absent(
    hub, ctx, *, name: str, resource_id: str = None, client_token: str = None, **kwargs
) -> Dict[str, Any]:
    r"""
    Deletes the specified network interface. You must detach the network interface before you can delete it.

    Args:
        name(str):
        An Idem name of the resource.

        resource_id(str, Optional):
            The ID of the network interface.

        client_token(str, Optional):
            The idempotency token for the network interface.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_absent:
              aws_auto.ec2.network_interface.absent:
                - name: value
                - resource_id: value
    """
    result = dict(
        comment=[], old_state=ctx.old_state, new_state=None, name=name, result=True
    )

    # Get the resource_id from ESM
    if not resource_id:
        resource_id = (ctx.old_state or {}).get("resource_id")

    if not resource_id and client_token:
        get = await hub.exec.aws.ec2.instance.get(
            ctx, name=name, filters=[{"Name": "client-token", "Values": [client_token]}]
        )
        resource_id = get.ret.resource_id

    # If there still is no resource_id, the instance is gone
    if not resource_id:
        result["comment"] += hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.network_interface", name=name
        )
        return result

    if ctx.test:
        result["comment"] += hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.ec2.network_interface", name=name
        )
        return result

    ret = await hub.exec.aws.ec2.network_interface.delete(ctx, resource_id=resource_id)
    result["comment"].extend(ret.comment)

    if not ret.result and any("does not exist" in c for c in ret.comment):
        result["comment"] += hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.network_interface", name=name
        )
        # The command failed because the instance no longer exists
        return result

    elif not ret.result:
        # The failure is some other reason we need to examine
        result["result"] &= ret.result
        result["comment"] += [ret.comment]
    else:
        result["comment"] += hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.ec2.network_interface", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Describes one or more of your network interfaces.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe aws_auto.ec2.network_interface
    """
    result = {}
    ret = await hub.exec.boto3.client.ec2.describe_network_interfaces(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe network_interface {ret['comment']}")
        return result

    network_interfaces = hub.tool.aws.ec2.network_interface.convert_to_present(
        ret["ret"]
    )

    for resource_id, resource_present_state in network_interfaces.items():
        result[resource_id] = {
            "aws.ec2.network_interface.present": [
                {k: v} for k, v in resource_present_state.items() if v is not None
            ]
        }

    return result
