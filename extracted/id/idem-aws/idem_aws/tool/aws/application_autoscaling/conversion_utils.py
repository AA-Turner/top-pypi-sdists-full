from collections import OrderedDict
from typing import Any
from typing import Dict

"""
Util function to convert raw resource state from AWS Application Autoscaling to present input format.
"""


def convert_raw_scaling_policy_to_present(
    hub, ctx, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    resource_id = f"{raw_resource.get('ServiceNamespace')}/{raw_resource.get('ResourceId')}/{raw_resource.get('ScalableDimension')}/{raw_resource.get('PolicyName')}"
    resource_parameters = OrderedDict(
        {
            "PolicyName": "policy_name",
            "PolicyARN": "arn",
            "ServiceNamespace": "service_namespace",
            "ResourceId": "scaling_resource_id",
            "ScalableDimension": "scalable_dimension",
            "PolicyType": "policy_type",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    if "StepScalingPolicyConfiguration" in raw_resource:
        resource_translated["step_scaling_policy_configuration"] = raw_resource.get(
            "StepScalingPolicyConfiguration"
        ).copy()
    if "TargetTrackingScalingPolicyConfiguration" in raw_resource:
        resource_translated[
            "target_tracking_scaling_policy_configuration"
        ] = raw_resource.get("TargetTrackingScalingPolicyConfiguration").copy()

    return resource_translated


def convert_raw_scaling_target_to_present(
    hub, ctx, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    resource_id = f"{raw_resource.get('ServiceNamespace')}/{raw_resource.get('ResourceId')}/{raw_resource.get('ScalableDimension')}"
    resource_parameters = OrderedDict(
        {
            "ServiceNamespace": "service_namespace",
            "ResourceId": "scaling_resource_id",
            "ScalableDimension": "scalable_dimension",
            "MinCapacity": "min_capacity",
            "MaxCapacity": "max_capacity",
            "RoleARN": "role_arn",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    if "SuspendedState" in raw_resource:
        resource_translated["suspended_state"] = raw_resource["SuspendedState"].copy()
    return resource_translated
