from typing import Any
from typing import Dict
from typing import List

import dict_tools


async def update(
    hub,
    ctx,
    name: str,
    resource_id: str,
    before: Dict[str, Any],
    auto_scaling_group_name: str,
    policy_type: str,
    adjustment_type: str,
    min_adjustment_step: int,
    min_adjustment_magnitude: int,
    scaling_adjustment: int,
    cooldown: int,
    metric_aggregation_type: str,
    step_adjustments: List[Dict[str, Any]],
    estimated_instance_warmup: int,
    target_tracking_configuration: Dict[str, Any],
    enabled: bool,
    predictive_scaling_configuration: Dict[str, Any],
):
    result = dict(comment=[], result=True, ret=None)
    update_allowed_params = [
        "policy_type",
        "adjustment_type",
        "min_adjustment_step",
        "min_adjustment_magnitude",
        "scaling_adjustment",
        "cooldown",
        "metric_aggregation_type",
        "estimated_instance_warmup",
        "enabled",
    ]

    modified_params = {}
    for parameter in update_allowed_params:
        input_parameter_value = locals()[parameter]
        if (
            input_parameter_value is not None
            and before.get(parameter) != input_parameter_value
        ):
            modified_params[parameter] = input_parameter_value
    if dict_tools.data.recursive_diff(
        step_adjustments,
        before.get("step_adjustments"),
        ignore_order=True,
    ):
        modified_params["step_adjustments"] = step_adjustments
    if dict_tools.data.recursive_diff(
        before.get("target_tracking_configuration"),
        target_tracking_configuration,
        ignore_order=True,
    ):
        modified_params["target_tracking_configuration"] = target_tracking_configuration
    if dict_tools.data.recursive_diff(
        before.get("predictive_scaling_configuration"),
        predictive_scaling_configuration,
        ignore_order=True,
    ):
        modified_params[
            "predictive_scaling_configuration"
        ] = predictive_scaling_configuration

    if modified_params:
        result["ret"] = modified_params
        if not ctx.get("test", False):
            ret = await hub.exec.boto3.client.autoscaling.put_scaling_policy(
                ctx,
                AutoScalingGroupName=auto_scaling_group_name,
                PolicyName=resource_id,
                PolicyType=policy_type,
                AdjustmentType=adjustment_type,
                MinAdjustmentStep=min_adjustment_step,
                MinAdjustmentMagnitude=min_adjustment_magnitude,
                ScalingAdjustment=scaling_adjustment,
                Cooldown=cooldown,
                MetricAggregationType=metric_aggregation_type,
                StepAdjustments=step_adjustments,
                EstimatedInstanceWarmup=estimated_instance_warmup,
                TargetTrackingConfiguration=target_tracking_configuration,
                Enabled=enabled,
                PredictiveScalingConfiguration=predictive_scaling_configuration,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.autoscaling.scaling_policy", name=name
            )
    return result
