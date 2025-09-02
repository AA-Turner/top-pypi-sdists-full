import copy
from typing import Any
from typing import Dict


async def update_tags(
    hub, ctx, old_tags: Dict[str, Any], new_tags: Dict[str, Any], resource_id: str
):
    """
    Update tags of AWS auto scaling group
    Args:
        hub:
        ctx:
        old_tags: dict of old tags in the format of {tag-key: tag-value, propagate_at_launch-tag_key: value}
        new_tags: dict of new tags in the format of {tag-key: tag-value, propagate_at_launch-tag_key: value}
        resource_id: The name of the Auto Scaling group.

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": dict of updated tags}

    """
    tags_to_add = {}
    tags_to_remove = {}
    if new_tags is not None:
        (
            tags_to_remove,
            tags_to_add,
        ) = hub.tool.aws.tag_utils.diff_auto_scaling_dict_tags(
            old_tags=old_tags, new_tags=new_tags
        )
    result = dict(comment=[], result=True, ret=None)
    if (not tags_to_remove) and (not tags_to_add):
        result["ret"] = copy.deepcopy(old_tags if old_tags else {})
        return result
    if tags_to_remove:
        if not ctx.get("test", False):
            list_tags_to_remove = (
                hub.tool.aws.tag_utils.convert_auto_scaling_tag_dict_to_list(
                    tags_to_remove
                )
            )
            raw_tags_to_remove = hub.tool.aws.autoscaling.auto_scaling_group_utils.convert_present_tags_to_raw_tags(
                resource_id, list_tags_to_remove
            )
            delete_ret = await hub.exec.boto3.client.autoscaling.delete_tags(
                ctx, Tags=raw_tags_to_remove
            )
            if not delete_ret["result"]:
                result["comment"] += [delete_ret["comment"]]
                result["result"] = False
                return result

    if tags_to_add:
        if not ctx.get("test", False):
            list_tags_to_add = (
                hub.tool.aws.tag_utils.convert_auto_scaling_tag_dict_to_list(
                    tags_to_add
                )
            )
            raw_tags_to_add = hub.tool.aws.autoscaling.auto_scaling_group_utils.convert_present_tags_to_raw_tags(
                resource_id, list_tags_to_add
            )
            add_ret = await hub.exec.boto3.client.autoscaling.create_or_update_tags(
                ctx, Tags=raw_tags_to_add
            )
            if not add_ret["result"]:
                result["comment"] += [add_ret["comment"]]
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
