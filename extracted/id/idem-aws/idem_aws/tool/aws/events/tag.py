import copy
from typing import Any
from typing import Dict


async def update_tags(
    hub,
    ctx,
    resource_id: str,
    old_tags: Dict[str, Any],
    new_tags: Dict[str, Any],
):
    """
    Update tags of AWS CloudWatchEvents resources

    Args:
        hub:
        ctx:
        resource_id: aws events rule arn
        old_tags: Dict of existing tags
        new_tags: Dict of new tags

    Returns:
        {"result": True|False, "comment": ("A message",), "ret": Dict of updated tags}

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
            delete_tag_resp = await hub.exec.boto3.client.events.untag_resource(
                ctx, ResourceARN=resource_id, TagKeys=list(tags_to_remove.keys())
            )
            if not delete_tag_resp:
                failure_message = (
                    f"Could not delete tags {tags_to_remove} for aws.events.rule with ARN {resource_id}. "
                    f"Failed with error: {delete_tag_resp['comment']}",
                )
                hub.log.debug(failure_message)
                result["comment"] = failure_message
                result["result"] = False
                return result

    if tags_to_add:
        if not ctx.get("test", False):
            create_tag_resp = await hub.exec.boto3.client.events.tag_resource(
                ctx,
                ResourceARN=resource_id,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags=tags_to_add),
            )
            if not create_tag_resp:
                failure_message = (
                    f"Could not create tags {tags_to_add} for aws.events.rule with ARN {resource_id}."
                    f" Failed with error: {create_tag_resp['comment']}",
                )
                hub.log.debug(failure_message)
                result["comment"] += failure_message
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
