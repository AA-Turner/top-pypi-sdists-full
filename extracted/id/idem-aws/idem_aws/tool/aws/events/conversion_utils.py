from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List

"""
Util functions to convert raw CloudWatchEvents Rule resource state from AWS to present input format.
"""


async def convert_raw_cloud_watch_rule_to_present_async(
    hub,
    ctx,
    raw_resource: Dict[str, Any],
    idem_resource_name: str,
    tags: List = None,
) -> Dict[str, Any]:
    describe_parameters = OrderedDict(
        {
            "State": "rule_status",
            "ScheduleExpression": "schedule_expression",
            "EventBusName": "event_bus_name",
            "Description": "description",
            "EventPattern": "event_pattern",
            "RoleArn": "role_arn",
            "Arn": "arn",
        }
    )
    resource_translated = {
        "resource_id": idem_resource_name,
        "name": idem_resource_name,
    }
    result = dict(comment=[], result=True, ret=None)
    for parameter_old_key, parameter_new_key in describe_parameters.items():
        if raw_resource.get(parameter_old_key) is not None:
            resource_translated[parameter_new_key] = raw_resource.get(parameter_old_key)

    targets = await hub.exec.boto3.client.events.list_targets_by_rule(
        ctx, Rule=idem_resource_name
    )
    result["result"] = targets["result"]
    if not result["result"]:
        result["comment"] += targets["comment"]

    if result["result"] and targets["ret"]["Targets"]:
        resource_translated["targets"] = targets["ret"]["Targets"]

    if tags:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            tags
        )

    result["ret"] = resource_translated
    return result
