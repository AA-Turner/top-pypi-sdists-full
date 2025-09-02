"""Exec module for managing Scaling policies."""
from typing import Dict


async def get(
    hub,
    ctx,
    name,
    auto_scaling_group_name: str,
    resource_id: str = None,
    policy_type: str = None,
) -> Dict:
    """Retrieves the specified scaling policy.

    Use an un-managed scaling policy as a data-source. Supply one of the inputs as the filter.
    If resource_id is set, autoscaling group is searched based on the resource_id and policy_type is ignored.

    Args:
        name(str):
            The name of the Idem state.

        auto_scaling_group_name(str):
            The name of the Auto Scaling group.

        resource_id(str, Optional):
            Name of the Auto Scaling group's policy.

        policy_type(str, Optional):
            Type of Auto Scaling group's policy. This is used to fetch a policy if resource_id is not specified.

    Returns:
        .. code-block:: python

            {"result": True|False, "comment": list, "ret": None|dict}

    Examples:
        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.autoscaling.scaling_policy.get auto_scaling_group_name="asg_1" resource_id="resource_id"

        Calling this exec module function from within a state module in pure python

        .. code-block:: python

            async def state_function(hub, ctx, name, auto_scaling_group_name, resource_id):
                ret = await hub.exec.aws.autoscaling.scaling_policy.get(
                    ctx=ctx,
                    name=name,
                    resource_id=resource_id,
                    auto_scaling_group_name=auto_scaling_group_name
                )

    """
    result = dict(comment=[], ret=None, result=True)
    if resource_id:
        ret = await hub.exec.boto3.client.autoscaling.describe_policies(
            ctx=ctx,
            AutoScalingGroupName=auto_scaling_group_name,
            PolicyNames=[resource_id],
        )
    else:
        ret = await hub.exec.boto3.client.autoscaling.describe_policies(
            ctx=ctx,
            AutoScalingGroupName=auto_scaling_group_name,
            PolicyTypes=[policy_type] if policy_type else None,
        )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["ScalingPolicies"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.autoscaling.scaling_policy", name=name
            )
        )
        return result

    resource = ret["ret"]["ScalingPolicies"][0]
    if len(ret["ret"]["ScalingPolicies"]) > 1:
        result["comment"].append(
            f"More than one aws.autoscaling.scaling_policy resource was found. Use resource {resource.get('PolicyName')}"
        )
    result[
        "ret"
    ] = hub.tool.aws.autoscaling.conversion_utils.convert_raw_scaling_policy_to_present(
        ctx, raw_resource=resource
    )
    return result
