from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List


async def search_raw(
    hub,
    ctx,
    resource_id,
) -> Dict:
    """
    Fetches a load balancer from AWS. The return will be in the same format as what the boto3 api returns.

    Args:
        resource_id(str): The name of the ElasticLoadBalancing Load Balancer. This name must be unique
            within your set of load balancers for the region, must have a maximum of 32 characters,

    Returns:
        {"result": True|False, "comment": A message List, "ret": Dict}

    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.elb.describe_load_balancers(
        ctx,
        LoadBalancerNames=[resource_id],
    )
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]
    return result


async def create(
    hub,
    ctx,
    input_map: Dict[str, Any],
):
    """
    Creates a Classic Load Balancer.

    Args:
        input_map(Dict[str, Any]):a dictionary with all passed input values of params.

    Returns:
        {"result": True|False, "comment": A message List, "ret": None}
    """
    result = dict(comment=[], result=True, ret=[])
    ret = await hub.exec.boto3.client.elb.create_load_balancer(
        ctx,
        LoadBalancerName=input_map.get("LoadBalancerName"),
        Listeners=input_map.get("Listeners"),
        AvailabilityZones=input_map.get("AvailabilityZones"),
        Subnets=input_map.get("Subnets"),
        SecurityGroups=input_map.get("SecurityGroups"),
        Scheme=input_map.get("Scheme"),
        Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(input_map.get("Tags")),
    )
    if not ret["result"] and not ret["ret"]:
        result["comment"] = list(ret["comment"])
        result["result"] = False
        return result
    result["ret"].append({"load_balancer_response": ret["ret"]})

    if input_map.get("LoadBalancerAttributes"):
        add_attributes = (
            await hub.exec.boto3.client.elb.modify_load_balancer_attributes(
                ctx,
                LoadBalancerName=input_map.get("LoadBalancerName"),
                LoadBalancerAttributes=input_map.get("LoadBalancerAttributes"),
            )
        )
        if not add_attributes["result"]:
            result["comment"] += list(add_attributes["comment"])
            result["result"] = False
            return result
        result["comment"].append("Added Attributes.")
        result["ret"].append(
            {"add_attributes": add_attributes["ret"]["LoadBalancerAttributes"]}
        )
    if input_map.get("Instances"):
        register_instances = (
            await hub.exec.boto3.client.elb.register_instances_with_load_balancer(
                ctx,
                LoadBalancerName=input_map.get("LoadBalancerName"),
                Instances=input_map.get("Instances"),
            )
        )
        if not register_instances["result"]:
            result["comment"] += list(register_instances["comment"])
            result["result"] = False
            return result
        result["comment"].append("Registered Instances.")
        result["ret"].append(
            {"register_instances": register_instances["ret"]["Instances"]}
        )
    return result


async def update(
    hub,
    ctx,
    name: str,
    current_state: Dict[str, Any],
    input_map: Dict[str, Any],
    resource_id: str,
    plan_state: Dict[str, Any],
):
    """
    1. Associates one or more security groups with your load balancer in a virtual private cloud (VPC). The specified
       security groups override the previously associated security groups.
    2. Adds/Removes one or more subnets to the set of configured subnets for the specified load balancer. The load
       balancer evenly distributes requests across all registered subnets.
    3. Adds/ Removes the specified Availability Zones to the set of Availability Zones for the specified load balancer
       in EC2-Classic or a default VPC. For load balancers in a non-default VPC, use DetachLoadBalancerFromSubnets .

       There must be at least one Availability Zone registered with a load balancer at all times. After an Availability
       Zone is removed, all instances registered with the load balancer that are in the removed Availability Zone go
       into the OutOfService state. Then, the load balancer attempts to equally balance the traffic among its remaining
       Availability Zones.
    4. Modifies the attributes of the specified load balancer. You can modify the load balancer attributes, such as
       AccessLogs , ConnectionDraining , and CrossZoneLoadBalancing by either enabling or disabling them. Or, you can
       modify the load balancer attribute ConnectionSettings by specifying an idle connection timeout value for your
       load balancer.
    5. Adds/De-registers the specified instances to the specified load balancer. After the instance is de-registered,
       it no longer receives traffic from the load balancer.

       The instance must be a running instance in the same network as the load balancer (EC2-Classic or the same VPC).
       If you have EC2-Classic instances and a load balancer in a VPC with ClassicLink enabled, you can link the
       EC2-Classic instances to that VPC and then register the linked EC2-Classic instances with the load balancer
       in the VPC.

    Args:
        name(str):The name of the AWS ElasticLoadBalancing load balancer.
        current_state(Dict[str, Any]): response returned by describe on an AWS ElasticLoadBalancing load balancer
        input_map(Dict[str, Any]): a dictionary with newly passed values of params.
        resource_id(str): AWS ElasticLoadBalancing load balancer name.
        plan_state(Dict[str, Any]): idem --test state for update on AWS ElasticLoadBalancing Load Balancer.

    Returns:
        {"result": True|False, "comment": A message List, "ret": None}

    """
    result = dict(comment=[], result=True, ret=[])
    if not ctx.get("test", False):
        if input_map.get("LoadBalancerAttributes"):
            modify_attributes = (
                await hub.exec.boto3.client.elb.modify_load_balancer_attributes(
                    ctx,
                    LoadBalancerName=resource_id,
                    LoadBalancerAttributes=input_map.get("LoadBalancerAttributes"),
                )
            )
            if not modify_attributes["result"]:
                result["comment"] = list(modify_attributes["comment"])
                result["result"] = False
                return result
            result["comment"].append("Modified Attributes.")
            result["ret"].append(
                {
                    "modify_attributes": modify_attributes["ret"][
                        "LoadBalancerAttributes"
                    ]
                }
            )
        if input_map.get("SecurityGroups"):
            if not current_state.get("security_groups") or set(
                current_state.get("security_groups")
            ) != set(input_map.get("SecurityGroups")):
                apply_security_groups = await hub.exec.boto3.client.elb.apply_security_groups_to_load_balancer(
                    ctx,
                    LoadBalancerName=resource_id,
                    SecurityGroups=input_map.get("SecurityGroups"),
                )
                if not apply_security_groups["result"]:
                    result["comment"] += list(apply_security_groups["comment"])
                    result["result"] = False
                    return result
                result["comment"].append("Applied Security Groups.")
                result["ret"].append(
                    {
                        "apply_security_groups": apply_security_groups["ret"][
                            "SecurityGroups"
                        ]
                    }
                )

        if input_map.get("Subnets"):
            if not current_state.get("subnets") or set(
                current_state.get("subnets")
            ) != set(input_map.get("Subnets")):
                to_detach = list(
                    set(current_state.get("subnets", []))
                    - set(input_map.get("Subnets"))
                )
                to_attach = list(
                    set(input_map.get("Subnets"))
                    - set(current_state.get("subnets", []))
                )

                if to_detach:
                    detach_subnets = await hub.exec.boto3.client.elb.detach_load_balancer_from_subnets(
                        ctx,
                        LoadBalancerName=resource_id,
                        Subnets=to_detach,
                    )
                    if not detach_subnets["result"]:
                        result["comment"] += list(detach_subnets["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append("Detached Subnets.")
                    result["ret"].append(
                        {"detach_subnets": detach_subnets["ret"]["Subnets"]}
                    )

                if to_attach:
                    attach_subnets = (
                        await hub.exec.boto3.client.elb.attach_load_balancer_to_subnets(
                            ctx,
                            LoadBalancerName=resource_id,
                            Subnets=to_attach,
                        )
                    )
                    if not attach_subnets["result"]:
                        result["comment"] += list(attach_subnets["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append("Attached Subnets.")
                    result["ret"].append(
                        {"attach_subnets": attach_subnets["ret"]["Subnets"]}
                    )

        if input_map.get("AvailabilityZones"):
            if not current_state.get("availability_zones") or set(
                current_state.get("availability_zones")
            ) != set(input_map.get("AvailabilityZones")):
                to_disable = list(
                    set(current_state.get("availability_zones", []))
                    - set(input_map.get("AvailabilityZones"))
                )
                to_enable = list(
                    set(input_map.get("AvailabilityZones"))
                    - set(current_state.get("availability_zones", []))
                )

                if to_disable:
                    disable_zones = await hub.exec.boto3.client.elb.disable_availability_zones_for_load_balancer(
                        ctx,
                        LoadBalancerName=resource_id,
                        AvailabilityZones=to_disable,
                    )
                    if not disable_zones["result"]:
                        result["comment"] += list(disable_zones["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append("Disabled Availability Zones.")
                    result["ret"].append(
                        {"disable_zones": disable_zones["ret"]["AvailabilityZones"]}
                    )

                if to_enable:
                    enable_zones = await hub.exec.boto3.client.elb.enable_availability_zones_for_load_balancer(
                        ctx,
                        LoadBalancerName=resource_id,
                        AvailabilityZones=to_enable,
                    )
                    if not enable_zones["result"]:
                        result["comment"] += list(enable_zones["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append("Enabled Availability Zones.")
                    result["ret"].append(
                        {"enable_zones": enable_zones["ret"]["AvailabilityZones"]}
                    )

        if input_map.get("Instances"):
            ret = compare_instances(
                old_instances=current_state.get("instances"),
                new_instances=input_map.get("Instances"),
            )
            if ret["ret"]:
                if ret["ret"]["to_deregister"]:
                    deregister_instances = await hub.exec.boto3.client.elb.deregister_instances_from_load_balancer(
                        ctx,
                        LoadBalancerName=resource_id,
                        Instances=ret["ret"]["to_delete"],
                    )
                    if not deregister_instances["result"]:
                        result["comment"] += list(deregister_instances["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append("Instances Deregistered.")
                    result["ret"].append(
                        {
                            "deregister_instances": deregister_instances["ret"][
                                "Instances"
                            ]
                        }
                    )

                if ret["ret"]["to_register"]:
                    register_instances = await hub.exec.boto3.client.elb.register_instances_with_load_balancer(
                        ctx,
                        LoadBalancerName=resource_id,
                        Instances=ret["ret"]["to_register"],
                    )
                    if not register_instances["result"]:
                        result["comment"] += list(register_instances["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append(
                        "Instances Registered.",
                    )
                    result["ret"].append(
                        {"register_instances": register_instances["ret"]["Instances"]}
                    )

        if input_map.get("Listeners"):
            ret = compare_listeners(
                old_listeners=current_state.get("listeners"),
                new_listeners=input_map.get("Listeners"),
            )
            if ret["ret"]:
                if ret["ret"]["to_delete"]:
                    delete_listeners = (
                        await hub.exec.boto3.client.elb.delete_load_balancer_listeners(
                            ctx,
                            LoadBalancerName=resource_id,
                            LoadBalancerPorts=ret["ret"]["to_delete"],
                        )
                    )
                    if not delete_listeners["result"]:
                        result["comment"] += list(delete_listeners["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append("Listeners Deleted.")
                    result["ret"].append({"delete_listeners": delete_listeners["ret"]})

                if ret["ret"]["to_create"]:
                    create_listeners = (
                        await hub.exec.boto3.client.elb.create_load_balancer_listeners(
                            ctx,
                            LoadBalancerName=resource_id,
                            Listeners=ret["ret"]["to_create"],
                        )
                    )
                    if not create_listeners["result"]:
                        result["comment"] += list(create_listeners["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append("Listeners Created.")
                    result["ret"].append({"create_listeners": create_listeners["ret"]})
    else:
        update_params = OrderedDict(
            {
                "name": input_map.get("LoadBalancerName"),
                "listeners": input_map.get("Listeners"),
                "availability_zones": input_map.get("AvailabilityZones"),
                "subnets": input_map.get("Subnets"),
                "security_groups": input_map.get("SecurityGroups"),
                "scheme": input_map.get("Scheme"),
                "instances": input_map.get("Instances"),
                "load_balancer_attributes": input_map.get("LoadBalancerAttributes"),
                "tags": input_map.get("Tags"),
                "resource_id": input_map.get("FunctionName"),
            }
        )
        for key, value in update_params.items():
            if value is not None:
                plan_state[key] = value
        result["ret"] = plan_state
    return result


def compare_instances(
    old_instances: List[Dict[str, Any]], new_instances: List[Dict[str, Any]]
):
    """
    Compares old_instances and new_instances and return the new list of instances that need to be updated.

    Args:
        new_instances(List[Dict[str, Any]]): Newer list of instances to be associated with ELB v1 Load Balancer.
        old_instances(List[Dict[str, Any]]): Existing list of instances associated with ELB v1 Load Balancer.

    Returns:
        {"ret": Dict}

    """
    result = {"ret": None}
    if not old_instances:
        result["ret"] = {"to_register": new_instances}

    to_deregister = []
    to_register = []
    old_instances_map = {
        instance.get("InstanceId"): instance for instance in old_instances
    }
    if new_instances is not None:
        for instance in new_instances:
            if instance.get("InstanceId") in old_instances_map:
                del old_instances_map[instance.get("InstanceId")]
            else:
                to_register.append(instance)
        to_deregister = list(old_instances_map.values())
        result["ret"] = {"to_register": to_register, "to_deregister": to_deregister}
    return result


def compare_listeners(
    old_listeners: List[Dict[str, Any]], new_listeners: List[Dict[str, Any]]
):
    """
    Compares old_listeners and new_listeners and return the new list of listeners that need to be created/ updated.
    If a listener with the specified port does not already exist, it is created; otherwise, the properties of the
    new listener must match the properties of the existing listener.

    Args:
        new_listeners(List[Dict[str, Any]]): Newer list of listeners to be associated with ELB v1 Load Balancer.
        old_listeners(List[Dict[str, Any]]): Existing list of listeners associated with ELB v1 Load Balancer.

    Returns:
        {"ret": Dict}

    """
    result = {"ret": None}
    if not old_listeners:
        result["ret"] = {"to_create": new_listeners}

    to_delete = []
    to_create = []
    old_listeners_map = {
        listener.get("LoadBalancerPort"): listener for listener in old_listeners
    }
    if new_listeners is not None:
        for listener in new_listeners:
            if listener.get("LoadBalancerPort") in old_listeners_map:
                del old_listeners_map[listener.get("LoadBalancerPort")]
            else:
                to_create.append(listener)

        for listener in old_listeners_map.values():
            to_delete.append(listener.get("LoadBalancerPort"))
        result["ret"] = {"to_create": to_create, "to_delete": to_delete}
    return result
