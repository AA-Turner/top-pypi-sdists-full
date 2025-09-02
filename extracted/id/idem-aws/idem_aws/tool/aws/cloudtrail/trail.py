import copy
from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List


async def update_tags(
    hub,
    ctx,
    resource_id,
    old_tags: Dict[str, Any],
    new_tags: Dict[str, Any],
):
    """Update tags of AWS CloudTrail resources.

    Args:
        resource_id: aws resource id
        old_tags: dict of old tags in the format of {tag-key: tag-value}
        new_tags: dict of new tags in the format of {tag-key: tag-value}. If this value is None, the function will do no operation on tags.

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": dict of updated tags}

    """
    tags_to_add = {}
    tags_to_remove = {}
    if new_tags is not None:
        tags_to_remove, tags_to_add = hub.tool.aws.tag_utils.diff_tags_dict(
            old_tags=old_tags, new_tags=new_tags
        )
    result = dict(comment=[], result=True, ret=None)
    if (not tags_to_remove) and (not tags_to_add):
        result["ret"] = copy.deepcopy(old_tags if old_tags else {})
        return result
    if tags_to_remove:
        if not ctx.get("test", False):
            delete_ret = await hub.exec.boto3.client.cloudtrail.remove_tags(
                ctx,
                ResourceId=resource_id,
                TagsList=hub.tool.aws.tag_utils.convert_tag_dict_to_list(
                    tags=tags_to_remove
                ),
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result

    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.cloudtrail.add_tags(
                ctx,
                ResourceId=resource_id,
                TagsList=hub.tool.aws.tag_utils.convert_tag_dict_to_list(
                    tags=tags_to_add
                ),
            )
            if not add_ret["result"]:
                result["comment"] = add_ret["comment"]
                result["result"] = False
                return result
    result["ret"] = new_tags
    if ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_update_tags_comment(
            tags_to_remove=tags_to_remove, tags_to_add=tags_to_add
        )
    else:
        result["comment"] = hub.tool.aws.comment_utils.update_tags_comment(
            tags_to_remove=tags_to_remove, tags_to_add=tags_to_add
        )
    return result


async def update_trail(
    hub,
    ctx,
    before: Dict[str, Any],
    s3_bucket_name: str,
    s3_key_prefix: str,
    sns_topic_name: str,
    include_global_service_events: bool,
    is_multi_region_trail: bool,
    enable_logfile_validation: bool,
    cloud_watch_logs_loggroup_arn: str,
    cloud_watch_logs_role_arn: str,
    kms_key_id: str,
    is_organization_trail: bool,
):
    result = dict(comment=[], result=True, ret=None)
    update_payload = {}

    resource_parameters = OrderedDict(
        {
            "S3BucketName": s3_bucket_name,
            "S3KeyPrefix": s3_key_prefix,
            "SnsTopicName": sns_topic_name,
            "IncludeGlobalServiceEvents": include_global_service_events,
            "IsMultiRegionTrail": is_multi_region_trail,
            "CloudWatchLogsLogGroupArn": cloud_watch_logs_loggroup_arn,
            "CloudWatchLogsRoleArn": cloud_watch_logs_role_arn,
            "KmsKeyId": kms_key_id,
            "IsOrganizationTrail": is_organization_trail,
        }
    )

    if "LogFileValidationEnabled" in before.keys():
        if (
            enable_logfile_validation is not None
        ) and enable_logfile_validation != before["LogFileValidationEnabled"]:
            update_payload["EnableLogFileValidation"] = enable_logfile_validation

    for key, value in resource_parameters.items():
        if key in before.keys():
            if (value is not None) and value != before[key]:
                update_payload[key] = resource_parameters[key]
    if update_payload:
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.cloudtrail.update_trail(
                ctx, Name=before.get("Name"), **update_payload
            )
            if not update_ret["result"]:
                result["comment"] += update_ret["comment"]
                result["result"] = False
                return result
        result["ret"] = {}
        result = update_result(result, update_payload, ctx)

    return result


def update_result(
    result: Dict[str, Any], update_payload: Dict[str, Any], ctx
) -> Dict[str, Any]:
    parameters = OrderedDict(
        {
            "S3BucketName": "s3_bucket_name",
            "S3KeyPrefix": "s3_key_prefix",
            "SnsTopicName": "sns_topic_name",
            "IncludeGlobalServiceEvents": "include_global_service_events",
            "IsMultiRegionTrail": "is_multi_region_trail",
            "EnableLogFileValidation": "enable_logfile_validation",
            "CloudWatchLogsLogGroupArn": "cloud_watch_logs_loggroup_arn",
            "CloudWatchLogsRoleArn": "cloud_watch_logs_role_arn",
            "KmsKeyId": "kms_key_id",
            "IsOrganizationTrail": "is_organization_trail",
        }
    )

    for raw_parameter, present_parameter in parameters.items():
        if raw_parameter in update_payload:
            if not ctx.get("test", False):
                result["comment"] += [
                    f"Update {present_parameter}: {update_payload[raw_parameter]}"
                ]
            else:
                result["comment"] += [
                    f"Would Update {present_parameter}: {update_payload[raw_parameter]}"
                ]
            result["ret"][present_parameter] = update_payload[raw_parameter]

    return result


async def update_trail_attributes(
    hub,
    ctx,
    before: Dict[str, Any],
    resource_id: str,
    is_logging: bool,
    update_insight_selectors: List,
    update_event_selectors: List,
    update_advanced_event_selectors: List,
) -> Dict[str, Any]:
    result = dict(comment=[], result=True, ret=None)
    exising_attributes = await existing_attributes(hub, ctx, before, resource_id)
    result["ret"] = {}
    if not exising_attributes["result"]:
        result["comment"] = exising_attributes["comment"]
        result["result"] = False
    if (
        is_logging is not None
        and exising_attributes["result"]
        and is_logging != exising_attributes["ret"].get("existingTrailStatus")
    ):
        if not ctx.get("test", False):
            if is_logging:
                update_ret = await hub.exec.boto3.client.cloudtrail.start_logging(
                    ctx, Name=before["TrailARN"]
                )
            else:
                update_ret = await hub.exec.boto3.client.cloudtrail.stop_logging(
                    ctx, Name=before["TrailARN"]
                )
            if not update_ret["result"]:
                result["comment"] += update_ret["comment"]
                result["result"] = False
                return result
            result["comment"] += [f"Update is_logging: {is_logging}"]
        else:
            result["comment"] += [f"Would Update is_logging: {is_logging}"]
        result["ret"]["is_logging"] = is_logging

    if exising_attributes["result"] and (
        not hub.tool.aws.state_comparison_utils.are_lists_identical(
            update_insight_selectors,
            exising_attributes["ret"].get("existingInsightSelectors"),
        )
    ):
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.cloudtrail.put_insight_selectors(
                ctx,
                TrailName=before["TrailARN"],
                InsightSelectors=update_insight_selectors,
            )
            if not update_ret["result"]:
                result["comment"] += update_ret["comment"]
                result["result"] = False
                return result
            result["comment"] += [
                f"Update insight_selectors: {update_insight_selectors}"
            ]
        else:
            result["comment"] += [
                f"Would Update insight_selectors: {update_insight_selectors}"
            ]
        result["ret"]["insight_selectors"] = update_insight_selectors

    ## Update event selectors
    if (
        exising_attributes["result"]
        and update_event_selectors is not None
        and (
            not hub.tool.aws.state_comparison_utils.are_lists_identical(
                update_event_selectors, exising_attributes["ret"].get("event_selectors")
            )
        )
    ):
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.cloudtrail.put_event_selectors(
                ctx,
                TrailName=before["TrailARN"],
                EventSelectors=update_event_selectors,
                AdvancedEventSelectors=update_advanced_event_selectors,
            )
            if not update_ret["result"]:
                result["comment"] += update_ret["comment"]
                result["result"] = False
                return result
            result["comment"] += [f"Update event_selectors: {update_event_selectors}"]
        else:
            result["comment"] += [
                f"Would Update event_selectors: {update_event_selectors}"
            ]
        result["ret"]["event_selectors"] = update_event_selectors

    if (
        exising_attributes["result"]
        and update_advanced_event_selectors is not None
        and (
            not hub.tool.aws.state_comparison_utils.are_lists_identical(
                update_advanced_event_selectors,
                exising_attributes["ret"].get("advanced_event_selectors"),
            )
        )
    ):
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.cloudtrail.put_event_selectors(
                ctx,
                TrailName=before["TrailARN"],
                EventSelectors=update_event_selectors,
                AdvancedEventSelectors=update_advanced_event_selectors,
            )
            if not update_ret["result"]:
                result["comment"] += update_ret["comment"]
                result["result"] = False
                return result
            result["comment"] += [
                f"Update advanced_event_selectors: {update_advanced_event_selectors}"
            ]
        else:
            result["comment"] += [
                f"Would Update advanced_event_selectors: {update_advanced_event_selectors}"
            ]
        result["ret"]["advanced_event_selectors"] = update_advanced_event_selectors

    return result


async def existing_attributes(
    hub, ctx, before: Dict[str, Any], resource_id: str
) -> Dict[str, Any]:
    result = dict(comment=[], result=True, ret=None)
    existing_logging = None
    existing_insight_selectors = None
    existing_event_selectors = None
    existing_advanced_event_selectors = None

    existingTrailStatus = await hub.exec.boto3.client.cloudtrail.get_trail_status(
        ctx, Name=resource_id
    )
    if existingTrailStatus["result"]:
        existing_logging = existingTrailStatus["ret"]["IsLogging"]
    else:
        result["comment"] += existingTrailStatus["comment"]
        result["result"] = False

    existingInsightSelectors = (
        await hub.exec.boto3.client.cloudtrail.get_insight_selectors(
            ctx,
            TrailName=resource_id,
        )
    )
    if before["HasInsightSelectors"]:
        if existingInsightSelectors["result"]:
            existing_insight_selectors = existingInsightSelectors["ret"][
                "InsightSelectors"
            ]
        else:
            result["comment"] += existingInsightSelectors["comment"]
            result["result"] = False

    existingEventSelectors = await hub.exec.boto3.client.cloudtrail.get_event_selectors(
        ctx,
        TrailName=resource_id,
    )
    if existingEventSelectors["result"]:
        if "EventSelectors" in existingEventSelectors["ret"]:
            existing_event_selectors = existingEventSelectors["ret"]["EventSelectors"]
        else:
            existing_advanced_event_selectors = existingEventSelectors["ret"][
                "AdvancedEventSelectors"
            ]
    else:
        result["comment"] += existingEventSelectors["comment"]
        result["result"] = False

    result["ret"] = {
        "existingTrailStatus": existing_logging,
        "existingInsightSelectors": existing_insight_selectors,
        "event_selectors": existing_event_selectors,
        "advanced_event_selectors": existing_advanced_event_selectors,
    }
    return result
