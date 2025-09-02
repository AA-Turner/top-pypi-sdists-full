from typing import Any
from typing import Dict
from typing import List


async def search_raw(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict:
    """
    Fetch a load balancer from AWS. The return will be in the same format as what the boto3 api returns.

    Can't specify names and LoadBalancerArns in the same call. AWS API is failing with following exception.
        ['ClientError: An error occurred (ValidationError) when calling the 'DescribeLoadBalancers operation:
        Load balancer names and load balancer ARNs cannot be specified at the same time']
    Here, resource_id get higher priority in search than name i.e. if both name and resource_id are not None,
        search is done with resource_id than name.

    Args:
        name(str): The name of the Idem state.
        resource_id(str, Optional): AWS ELBv2 Load Balancer ARN to identify the resource.

    Returns:
        {"result": True|False, "comment": A message List, "ret": Dict}

    """
    ret = result = dict(comment=[], ret=None, result=True)
    if resource_id:
        ret = await hub.exec.boto3.client.elbv2.describe_load_balancers(
            ctx,
            LoadBalancerArns=[resource_id],
        )
    elif name:
        ret = await hub.exec.boto3.client.elbv2.describe_load_balancers(
            ctx,
            Names=[name],
        )
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]
    return result


async def update(
    hub,
    ctx,
    current_state: Dict[str, Any],
    input_map: Dict[str, Any],
    resource_id: str,
    plan_state: Dict[str, Any],
):
    """
    1. Associates the specified security groups with the specified Application Load Balancer. The specified security
       groups override the previously associated security groups. You can't specify a security group for a Network
       Load Balancer or Gateway Load Balancer.
    2. Enables the Availability Zones for the specified public subnets for the specified Application Load Balancer or
       Network Load Balancer. The specified subnets replace the previously enabled subnets.

       When you specify subnets for a Network Load Balancer, you must include all subnets that were enabled previously,
       with their existing configurations, plus any additional subnets.
    3. Modifies the specified attributes of the specified Application Load Balancer, Network Load Balancer, or
       Gateway Load Balancer.If any of the specified attributes can't be modified as requested, the call fails. Any
       existing attributes that you do not modify retain their current values.

    Args:
        current_state: response returned by describe on an AWS ELB load balancer
        input_map: a dictionary with newly passed values of params.
        resource_id: AWS ELB load balancer name.
        plan_state: idem --test state for update on AWS ElasticLoadBalancing Load Balancer.

    Returns:
        {"result": True|False, "comment": ("A tuple",), "ret": None}

    """
    result = dict(comment=[], result=True, ret=[])
    hub.log.debug(
        f"Current state of ELBv2 Load Balancer '{current_state.get('name')}' with resource id '{resource_id}' before update: "
        f"{current_state}"
    )
    if input_map.get("Attributes"):
        ret = compare_attributes(
            hub,
            old_attributes=current_state.get("attributes"),
            new_attributes=input_map.get("Attributes"),
        )
        if not ctx.get("test", False):
            if ret["ret"].get("modify"):
                attributes_update = (
                    await hub.exec.boto3.client.elbv2.modify_load_balancer_attributes(
                        ctx,
                        LoadBalancerArn=resource_id,
                        Attributes=ret["ret"].get("modify"),
                    )
                )
                if not attributes_update["result"]:
                    result["comment"] = list(attributes_update["comment"])
                    result["result"] = False
                    return result
                result["comment"].append("Modified Attributes ")
                result["ret"].append(
                    {
                        "Key": "attributes",
                        "Value": attributes_update["ret"]["Attributes"],
                    }
                )
        else:
            if ret["ret"].get("modify"):
                result["ret"].append(
                    {"Key": "attributes", "Value": ret["ret"].get("attributes")}
                )

    if input_map.get("SecurityGroups"):
        if not current_state.get("security_groups") or set(
            current_state.get("security_groups")
        ) != set(input_map.get("SecurityGroups")):
            if not ctx.get("test", False):
                update_security_groups = (
                    await hub.exec.boto3.client.elbv2.set_security_groups(
                        ctx,
                        LoadBalancerArn=resource_id,
                        SecurityGroups=input_map.get("SecurityGroups"),
                    )
                )
                if not update_security_groups["result"]:
                    result["comment"] += list(update_security_groups["comment"])
                    result["result"] = False
                    return result
                result["comment"].append("Updated SecurityGroups.")
                result["ret"].append(
                    {
                        "Key": "security_groups",
                        "Value": update_security_groups["ret"]["SecurityGroupIds"],
                    }
                )
            else:
                result["ret"].append(
                    {"Key": "security_groups", "Value": input_map.get("SecurityGroups")}
                )

    if input_map.get("Subnets"):
        if not current_state.get("subnets") or set(current_state.get("subnets")) != set(
            input_map.get("Subnets")
        ):
            if not ctx.get("test", False):
                update_subnets = await hub.exec.boto3.client.elbv2.set_subnets(
                    ctx,
                    LoadBalancerArn=resource_id,
                    Subnets=input_map.get("Subnets"),
                    IpAddressType=input_map.get("IpAddressType")
                    if input_map.get("Type") != "application"
                    else None,
                )
                if not update_subnets["result"]:
                    result["comment"] += list(update_subnets["comment"])
                    result["result"] = False
                    return result
                result["comment"].append("Updated Subnets.")
                result["ret"].append(
                    {
                        "Key": "subnets",
                        "Value": update_subnets["ret"]["AvailabilityZones"],
                    }
                )
            else:
                result["ret"].append(
                    {"Key": "subnets", "Value": input_map.get("Subnets")}
                )

    if input_map.get("IpAddressType"):
        if not current_state.get("ip_address_type") or (
            current_state.get("ip_address_type") != input_map.get("IpAddressType")
        ):
            if not ctx.get("test", False):
                update_ip_address_type = (
                    await hub.exec.boto3.client.elbv2.set_ip_address_type(
                        ctx,
                        LoadBalancerArn=resource_id,
                        IpAddressType=input_map.get("IpAddressType"),
                    )
                )
                if not update_ip_address_type["result"]:
                    result["comment"] += list(update_ip_address_type["comment"])
                    result["result"] = False
                    return result
                result["comment"].append("Updated IpAddressType.")
                result["ret"].append(
                    {
                        "Key": "ip_address_type",
                        "Value": update_ip_address_type["ret"]["IpAddressType"],
                    }
                )
            else:
                result["ret"].append(
                    {"Key": "ip_address_type", "Value": input_map.get("IpAddressType")}
                )
    return result


def compare_attributes(
    hub,
    old_attributes: List[Dict[str, Any]],
    new_attributes: List[Dict[str, Any]],
):
    """
    1. Compares old_attributes and new_attributes and return the new list of attributes that need to be created/ updated.
    2. If any of the specified attributes can't be modified as requested, the call fails.
    3. Any existing attributes that you do not modify retain their current values.

    Args:
        new_attributes(List[Dict[str, Any]]): Newer list of attributes to be modified with ELB v2 Load Balancer.
        old_attributes(List[Dict[str, Any]]): Existing list of attributes currently with ELB v2 Load Balancer.

    Returns:
        {"comment": ("A tuple",), "ret": Dict}

    """
    result = dict(ret=None)
    modify = []
    attributes = []
    new_attributes_map = {
        attribute.get("Key"): attribute for attribute in new_attributes or []
    }
    if new_attributes is not None:
        for attribute in old_attributes:
            if attribute.get("Key") in new_attributes_map:
                if attribute.get("Value") != (
                    new_attributes_map[attribute.get("Key")]
                ).get("Value"):
                    modify.append(
                        {
                            "Key": attribute.get("Key"),
                            "Value": (new_attributes_map[attribute.get("Key")]).get(
                                "Value"
                            ),
                        }
                    )
                else:
                    attributes.append(attribute)
            else:
                attributes.append(attribute)

        # append unchanged attributes to modified attributes to have final list of attributes.
        attributes.extend(modify)
        result["ret"] = {"modify": modify, "attributes": attributes}
    return result
