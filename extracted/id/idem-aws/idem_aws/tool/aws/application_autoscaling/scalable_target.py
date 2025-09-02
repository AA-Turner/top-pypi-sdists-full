from typing import Any
from typing import Dict


async def update_scalable_target(
    hub,
    ctx,
    name: str,
    before: Dict[str, Any],
    service_namespace: str,
    scaling_resource_id: str,
    scalable_dimension: str,
    min_capacity: int,
    max_capacity: int,
    role_arn: str,
    suspended_state: Dict[str, bool],
):
    result = dict(comment=[], result=True, ret=None)
    update_allowed_params = [
        "min_capacity",
        "max_capacity",
        "role_arn",
        "suspended_state",
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
            ].register_scalable_target(
                ctx,
                ServiceNamespace=service_namespace,
                ResourceId=scaling_resource_id,
                ScalableDimension=scalable_dimension,
                MinCapacity=min_capacity,
                MaxCapacity=max_capacity,
                RoleARN=role_arn,
                SuspendedState=suspended_state,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.application_autoscaling.scalable_target", name=name
            )
    return result
