from typing import Any
from typing import Dict
from typing import List

from dict_tools import data
from dict_tools import differ


async def search_raw(
    hub,
    ctx,
    name,
    resource_id: str = None,
    load_balancer_arn: str = None,
) -> Dict:
    """
    Fetch an ELBv2 Target Group from AWS. The return will be in the same format as what the boto3 api returns.

    **** Note ****: Users can specify one of the following to filter the results: the ARN of the load balancer,
                    the names of one or more target groups, or the ARNs of one or more target groups.

    Order of precedence of input params while performing search: resource_id, load_balancer_arn and finally name.
        If resource_id is not None, regardless whether the 2 other values are None or not, search always is done by
        resource_id only.
    Args:
        name(str, Optional): The name of the Idem state.
        resource_id(str, Optional): AWS ELBv2 Target Group ARN to identify the resource.
        load_balancer_arn(str, Optional): The Amazon Resource Name (ARN) of the load balancer.

    Returns:
        {"result": True|False, "comment": A message List, "ret": Dict}
    """
    result = dict(comment=[], ret=None, result=True)
    if resource_id:
        ret = await hub.exec.boto3.client.elbv2.describe_target_groups(
            ctx,
            TargetGroupArns=[resource_id],
        )
    elif load_balancer_arn:
        ret = await hub.exec.boto3.client.elbv2.describe_target_groups(
            ctx,
            LoadBalancerArn=load_balancer_arn,
        )
    else:
        ret = await hub.exec.boto3.client.elbv2.describe_target_groups(
            ctx, Names=[name]
        )
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]
    return result


async def update(
    hub,
    ctx,
    name: str,
    current_state: Dict[str, Any],
    input_map: Dict[str, Any],
    plan_state: Dict[str, Any],
    resource_id: str,
):
    """
    1. Modifies the health checks used when evaluating the health state of the targets in the specified target group.
       If the protocol of the target group is TCP, TLS, UDP, or TCP_UDP, you can't modify the health check protocol,
       interval, timeout, or success codes.
    2. Modifies the specified attributes of the specified target group.
    3. De-registers the specified targets from the specified target group. After the targets are de-registered, they no
       longer receive traffic from the load balancer.
    4. Registers the specified targets with the specified target group. If the target is an EC2 instance, it must be in
       the running state when you register it.
       a. By default, load balancer routes requests to registered targets using the protocol and port for the target group.
          Alternatively, you can override port for a target when you register it.
       b. You can register each EC2 instance or IP address with the same target group multiple times using different ports.
          With a Network Load Balancer, you cannot register instances by instance ID if they have the following instance
          types: C1, CC1, CC2, CG1, CG2, CR1, CS1, G1, G2, HI1, HS1, M1, M2, M3, and T1. You can register instances of
          these types by IP address.

    Args:
        name(str):The name of the AWS ElasticLoadBalancingv2 target group.
        current_state(Dict[str, Any]): response returned by describe on an AWS ELBv2 Target Group.
        input_map(Dict[st, Any]): a dictionary with newly passed values of params.
        resource_id(str): AWS ElasticLoadBalancingv2 target group ARN.
        plan_state(Dict[str, Any]): idem --test state for update on AWS ElasticLoadBalancingv2 target group.

    Returns:
        {"result": True|False, "comment": A message List, "ret": None}

    """
    result = dict(comment=[], result=True, ret=[])
    if input_map:
        update = {}
        modify_params = {
            "HealthCheckProtocol": "health_check_protocol",
            "HealthCheckPort": "health_check_port",
            "HealthCheckPath": "health_check_path",
            "HealthCheckEnabled": "health_check_enabled",
            "HealthCheckIntervalSeconds": "health_check_interval_seconds",
            "HealthCheckTimeoutSeconds": "health_check_timeout_seconds",
            "HealthyThresholdCount": "healthy_threshold_count",
            "UnhealthyThresholdCount": "unhealthy_threshold_count",
            "Matcher": "matcher",
        }
        hub.log.debug(
            f"Current state of ELBv2 Target Group '{name}' with resource id '{resource_id}' before update: "
            f"{current_state}"
        )
        for param_raw, param_present in modify_params.items():
            if input_map.get(param_present) is not None and current_state.get(
                param_present
            ) != input_map.get(param_present):
                update[param_raw] = input_map[param_present]

        if update:
            if not ctx.get("test", False):
                modify_target_group = (
                    await hub.exec.boto3.client.elbv2.modify_target_group(
                        ctx,
                        TargetGroupArn=resource_id,
                        **update,
                    )
                )
                if not modify_target_group["result"]:
                    result["comment"] = list(modify_target_group["comment"])
                    result["result"] = False
                    return result
                result["comment"] = list(
                    hub.tool.aws.comment_utils.update_comment(
                        resource_type="aws.elbv2.target_group", name=name
                    )
                )
            for key, value in update.items():
                result["ret"].append({"Key": modify_params.get(key), "Value": value})

    if input_map.get("attributes"):
        ret = hub.tool.aws.elbv2.load_balancer.compare_attributes(
            old_attributes=current_state.get("attributes"),
            new_attributes=input_map.get("attributes"),
        )
        if not ctx.get("test", False):
            if ret["ret"].get("modify"):
                modify_attributes = (
                    await hub.exec.boto3.client.elbv2.modify_target_group_attributes(
                        ctx,
                        TargetGroupArn=resource_id,
                        Attributes=ret["ret"].get("modify"),
                    )
                )
                if not modify_attributes["result"]:
                    result["comment"] += list(modify_attributes["comment"])
                    result["result"] = False
                    return result
                result["comment"].append("Modified Attributes.")
                result["ret"].append(
                    {
                        "Key": "attributes",
                        "Value": modify_attributes["ret"]["Attributes"],
                    }
                )
        else:
            if ret["ret"].get("modify"):
                result["ret"].append(
                    {"Key": "attributes", "Value": ret["ret"].get("attributes")}
                )

    if input_map.get("targets"):
        ret = compare_targets(
            old_targets=current_state.get("targets"),
            new_targets=input_map.get("targets"),
        )
        if not ctx.get("test", False):
            if ret["ret"]:
                if ret["ret"]["to_deregister"]:
                    deregister_targets = (
                        await hub.exec.boto3.client.elbv2.deregister_targets(
                            ctx,
                            TargetGroupArn=resource_id,
                            Targets=ret["ret"]["to_deregister"],
                        )
                    )
                    if not deregister_targets["result"]:
                        result["comment"] += list(deregister_targets["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append("Deregistered Targets.")
                    hub.log.debug(
                        f"De-registered targets for ELBv2 Target Group '{name}' with resource id '{resource_id}': "
                        f"{ret['ret']['to_deregister']}"
                    )

                if ret["ret"]["to_register"]:
                    register_targets = (
                        await hub.exec.boto3.client.elbv2.register_targets(
                            ctx,
                            TargetGroupArn=resource_id,
                            Targets=ret["ret"]["to_register"],
                        )
                    )
                    if not register_targets["result"]:
                        result["comment"] += list(register_targets["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append("Registered Targets.")
                    hub.log.debug(
                        f"Registered targets for ELBv2 Target Group '{name}' with resource id '{resource_id}': "
                        f"{ret['ret']['to_register']}"
                    )
                    result["ret"].append(
                        {"Key": "targets", "Value": ret["ret"]["to_register"]}
                    )
        else:
            if ret["ret"]["to_register"]:
                result["ret"].append(
                    {"Key": "targets", "Value": ret["ret"]["to_register"]}
                )
    return result


def compare_targets(
    old_targets: List[Dict[str, Any]], new_targets: List[Dict[str, Any]]
):
    """
    1. Compares old_targets and new_targets and return the new list of targets that need to be created/ updated.
    2. After targets are de-registered, they no longer receive traffic from the load balancer.
    3. If you specified a port-override when you registered a target, you must specify both the target ID and the port
        when you de-register it.

    Args:
        new_targets(List[Dict[str, Any]]): Newer list of targets to be registered with ELB v2 Target Group.
        old_targets(List[Dict[str, Any]]): Existing list of listeners de-registered with ELB v2 Target Group.

    Returns:
        {"comment": ("A tuple",), "ret": Dict}

    """
    result = dict(ret=None)
    to_register = []
    old_targets_map = {target.get("Id"): target for target in old_targets or []}
    if new_targets is not None:
        for target in new_targets:
            if target.get("Id") in old_targets_map:
                if target == old_targets_map[target.get("Id")]:
                    del old_targets_map[target.get("Id")]
                else:
                    to_register.append(target)
            else:
                to_register.append(target)

        to_deregister = list(old_targets_map.values())
        result["ret"] = {"to_register": to_register, "to_deregister": to_deregister}
    return result
