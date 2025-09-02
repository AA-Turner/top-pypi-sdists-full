from typing import Any
from typing import Dict


async def update_scaling_policy(
    hub,
    ctx,
    name: str,
    before: Dict[str, Any],
    policy_name: str,
    service_namespace: str,
    scaling_resource_id: str,
    scalable_dimension: str,
    policy_type: str,
    step_scaling_policy_configuration: Dict[str, Any],
    target_tracking_scaling_policy_configuration: Dict[str, Any],
):
    result = dict(comment=[], result=True, ret=None)
    update_allowed_params = [
        "policy_type",
        "step_scaling_policy_configuration",
        "target_tracking_scaling_policy_configuration",
    ]

    modified_params = {}
    for parameter in update_allowed_params:
        if (
            locals()[parameter] is not None
            and before.get(parameter) != locals()[parameter]
        ):
            modified_params[parameter] = locals()[parameter]
    if modified_params:
        result["ret"] = modified_params
        if not ctx.get("test", False):
            ret = await hub.exec.boto3.client[
                "application-autoscaling"
            ].put_scaling_policy(
                ctx,
                PolicyName=policy_name,
                ServiceNamespace=service_namespace,
                ResourceId=scaling_resource_id,
                ScalableDimension=scalable_dimension,
                PolicyType=policy_type,
                StepScalingPolicyConfiguration=step_scaling_policy_configuration,
                TargetTrackingScalingPolicyConfiguration=target_tracking_scaling_policy_configuration,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.application_autoscaling.scaling_policy", name=name
            )
    return result
