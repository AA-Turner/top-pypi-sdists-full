from collections import OrderedDict
from typing import Any
from typing import Dict

"""
Util function to convert raw resource state from AWS Launch Configuration to present input format.
"""


def convert_raw_launch_configuration_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    resource_id = raw_resource.get("LaunchConfigurationName")
    resource_parameters = OrderedDict(
        {
            "LaunchConfigurationName": "name",
            "ImageId": "image_id",
            "KeyName": "key_name",
            "SecurityGroups": "security_groups",
            "ClassicLinkVPCId": "classic_link_vpc_id",
            "ClassicLinkVPCSecurityGroups": "classic_link_vpc_security_groups",
            "UserData": "user_data",
            "InstanceId": "instance_id",
            "InstanceType": "instance_type",
            "KernelId": "kernel_id",
            "RamdiskId": "ramdisk_id",
            "BlockDeviceMappings": "block_device_mappings",
            "InstanceMonitoring": "instance_monitoring",
            "SpotPrice": "spot_price",
            "IamInstanceProfile": "iam_instance_profile",
            "EbsOptimized": "ebs_optimized",
            "AssociatePublicIpAddress": "associate_public_ip_address",
            "PlacementTenancy": "placement_tenancy",
            "MetadataOptions": "metadata_options",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    resource_translated = (
        hub.tool.aws.autoscaling.conversion_utils.handle_security_groups(
            resource=resource_translated
        )
    )
    return resource_translated


def handle_security_groups(hub, resource):
    # security_groups and classic_link_vpc_security_groups are of type List(str)
    # Just the change in the order of their elements should not be considered as a difference in new state and old state
    # So sorting the values for security_groups and classic_link_vpc_security_groups.
    if resource.get("security_groups"):
        resource["security_groups"] = sorted(resource["security_groups"])
    if resource.get("classic_link_vpc_security_groups"):
        resource["classic_link_vpc_security_groups"] = sorted(
            resource["classic_link_vpc_security_groups"]
        )
    return resource


def convert_raw_scaling_policy_to_present(
    hub, ctx, raw_resource: Dict[str, Any]
) -> Dict[str, Any]:
    resource_id = raw_resource.get("PolicyName")

    resource_parameters = OrderedDict(
        {
            "AutoScalingGroupName": "auto_scaling_group_name",
            "PolicyType": "policy_type",
            "AdjustmentType": "adjustment_type",
            "MinAdjustmentStep": "min_adjustment_step",
            "MinAdjustmentMagnitude": "min_adjustment_magnitude",
            "ScalingAdjustment": "scaling_adjustment",
            "Cooldown": "cooldown",
            "MetricAggregationType": "metric_aggregation_type",
            "EstimatedInstanceWarmup": "estimated_instance_warmup",
            "Enabled": "enabled",
        }
    )
    resource_translated = {
        "name": raw_resource.get("PolicyName"),
        "resource_id": resource_id,
    }
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    if "StepAdjustments" in raw_resource:
        resource_translated["step_adjustments"] = raw_resource.get(
            "StepAdjustments"
        ).copy()

    if "TargetTrackingConfiguration" in raw_resource:
        resource_translated["target_tracking_configuration"] = raw_resource.get(
            "TargetTrackingConfiguration"
        ).copy()

    if "PredictiveScalingConfiguration" in raw_resource:
        resource_translated["predictive_scaling_configuration"] = raw_resource.get(
            "PredictiveScalingConfiguration"
        ).copy()

    return resource_translated
