import copy
from collections import OrderedDict
from typing import Any
from typing import Dict


async def update_metric(
    hub,
    ctx,
    alarm_name: str,
    raw_resource: Dict[str, Any],
    resource_parameters: Dict[str, None],
):
    """
    Update tags of AWS cloudwatch metric alarm
    Args:
        hub:
        ctx:
        alarm_name: alarm name
        raw_resource: old state of metric alarm
        resource_parameters: list of new params

    Returns:
        {"result": True|False, "comment": "A message", "ret": None}

    """

    parameters = OrderedDict(
        {
            "AlarmDescription": "alarm_description",
            "ActionsEnabled": "actions_enabled",
            "OKActions": "ok_actions",
            "AlarmActions": "alarm_actions",
            "InsufficientDataActions": "insufficient_data_actions",
            "MetricName": "metric_name",
            "Namespace": "namespace",
            "Statistic": "statistic",
            "ExtendedStatistic": "extended_statistic",
            "Dimensions": "dimensions",
            "Period": "period",
            "Unit": "unit",
            "EvaluationPeriods": "evaluation_periods",
            "DatapointsToAlarm": "datapoints_to_alarm",
            "Threshold": "threshold",
            "ComparisonOperator": "comparison_operator",
            "TreatMissingData": "treat_missing_data",
            "EvaluateLowSampleCountPercentile": "evaluate_low_sample_count_percentile",
            "Metrics": "metrics",
            "ThresholdMetricId": "threshold_metric_id",
        }
    )
    resource_update = {}
    result = dict(comment=[], result=True, ret=None)
    resource_parameters.pop("Tags", None)
    for key, value in resource_parameters.items():
        if value is None or value == raw_resource[key]:
            continue
        resource_update[key] = resource_parameters[key]

    if resource_update:
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.cloudwatch.put_metric_alarm(
                ctx, **resource_parameters
            )
            if not update_ret["result"]:
                result["comment"] = update_ret["comment"]
                result["result"] = False
                return result
            result["comment"] += [f"Updated '{alarm_name}'"]

        result["ret"] = {}
        for parameter_raw, parameter_present in parameters.items():
            if parameter_raw in resource_update:
                result["ret"][parameter_present] = resource_update[parameter_raw]

    return result


async def update_metric_tags(
    hub,
    ctx,
    alarm_arn,
    old_tags: Dict[str, Any],
    new_tags: Dict[str, Any],
):
    """
    Update tags of AWS CloudWatch resources
    Args:
        alarm_arn:
        hub:
        ctx:
        old_tags (Dict): Dict in the format of {tag-key: tag-value}
        new_tags (Dict): Dict in the format of {tag-key: tag-value}

    Returns:
        {"result": True|False, "comment": "A message", "ret": dict of updated tags}

    """
    tags_to_add = {}
    tags_to_remove = {}

    if new_tags is not None:
        tags_to_remove, tags_to_add = hub.tool.aws.tag_utils.diff_tags_dict(
            old_tags=old_tags, new_tags=new_tags
        )
    result = dict(comment=[], result=True, ret={})
    if (not tags_to_remove) and (not tags_to_add):
        result["ret"] = copy.deepcopy(old_tags if old_tags else {})
        return result
    if tags_to_remove:
        if not ctx.get("test", False):
            delete_ret = await hub.exec.boto3.client.cloudwatch.untag_resource(
                ctx, ResourceARN=alarm_arn, TagKeys=list(tags_to_remove)
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result
    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.cloudwatch.tag_resource(
                ctx,
                ResourceARN=alarm_arn,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags_to_add),
            )
            if not add_ret["result"]:
                result["comment"] = add_ret["comment"]
                result["result"] = False
                return result

    result["ret"] = new_tags
    result["comment"] += [
        f"Updated tags: Added [{tags_to_add}] Removed [{tags_to_remove}]"
    ]
    return result
