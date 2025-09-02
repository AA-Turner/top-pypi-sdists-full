import copy
from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List


async def update_tags(
    hub,
    ctx,
    resource_id,
    old_tags: List[Dict[str, Any]],
    new_tags: List[Dict[str, Any]],
):
    """
    Update tags of AWS Cost Category
    Args:
        hub:
        ctx:
        resource_id: aws resource id
        old_tags: list of old tags
        new_tags: list of new tags

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": None}

    """
    tags_to_add = []
    tags_to_remove = []
    old_tags_map = {tag.get("Key"): tag for tag in old_tags or []}
    tags_result = copy.deepcopy(old_tags_map)
    if new_tags is not None:
        for tag in new_tags:
            if tag.get("Key") in old_tags_map:
                if tag.get("Value") != old_tags_map.get(tag.get("Key")).get("Value"):
                    tags_to_add.append(tag)
                del old_tags_map[tag.get("Key")]
            else:
                tags_to_add.append(tag)
        tags_to_remove = [tag.get("Key") for tag in old_tags_map.values()]
    result = dict(comment=[], result=True, ret=None)
    if (not tags_to_remove) and (not tags_to_add):
        return result
    if tags_to_remove:
        if not ctx.get("test", False):
            delete_ret = await hub.exec.boto3.client.ce.untag_resource(
                ctx, ResourceArn=resource_id, ResourceTagKeys=tags_to_remove
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result
        [tags_result.pop(key, None) for key in tags_to_remove]
    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.ce.tag_resource(
                ctx, ResourceArn=resource_id, ResourceTags=tags_to_add
            )
            if not add_ret["result"]:
                result["comment"] = add_ret["comment"]
                result["result"] = False
                return result
    result["ret"] = {"tags": list(tags_result.values()) + tags_to_add}
    result["comment"] += [f"Update tags: Add [{tags_to_add}] Remove [{tags_to_remove}]"]
    return result


async def update_cost_category_definition(
    hub,
    ctx,
    before: Dict[str, Any],
    rules: List[Dict[str, Any]],
    default_value: str,
    split_charge_rules: List[Dict[str, Any]],
):
    """
    Updates the Cost Category Definition
    Args:
        before: existing resource
        rules(List[Dict[str, Any]]): The Cost Category rules used to categorize costs.
        split_charge_rules(List[Dict[str, Any]]): The split charge rules used to allocate your charges between your Cost Category values.
        default_value(str): The default value for the cost category.

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": None}

    """
    result = dict(comment=[], result=True, ret=None)
    update_payload = {}

    if not hub.tool.aws.state_comparison_utils.are_lists_identical(
        rules,
        before.get("Rules"),
    ):
        update_payload["Rules"] = rules

    if not hub.tool.aws.state_comparison_utils.are_lists_identical(
        split_charge_rules,
        before.get("SplitChargeRules"),
    ):
        update_payload["SplitChargeRules"] = split_charge_rules

    if default_value and default_value != before.get("DefaultValue"):
        update_payload["DefaultValue"] = default_value

    if update_payload:
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.ce.update_cost_category_definition(
                ctx,
                CostCategoryArn=before.get("CostCategoryArn"),
                RuleVersion=before.get("RuleVersion"),
                Rules=rules,
                SplitChargeRules=split_charge_rules,
                DefaultValue=default_value,
            )
            if not update_ret["result"]:
                result["comment"] += update_ret["comment"]
                result["result"] = False
                return result
        result["ret"] = {}
        result = update_result(result, update_payload)

    return result


def update_result(
    result: Dict[str, Any], update_payload: Dict[str, Any]
) -> Dict[str, Any]:
    parameters = OrderedDict(
        {
            "DefaultValue": "default_value",
            "SplitChargeRules": "split_charge_rules",
            "Rules": "rules",
        }
    )

    for raw_parameter, present_parameter in parameters.items():
        if raw_parameter in update_payload:
            result["ret"][present_parameter] = update_payload[raw_parameter]
            result["comment"] += [
                f"Update {present_parameter}: {update_payload[raw_parameter]}"
            ]
    return result
