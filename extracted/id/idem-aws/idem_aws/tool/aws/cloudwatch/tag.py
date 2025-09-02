import copy
from typing import Any
from typing import Dict


async def update_tags(
    hub,
    ctx,
    resource_name: str,
    old_tags: Dict[str, Any],
    new_tags: Dict[str, Any],
):
    """

    Args:
        hub:
        ctx:
        resource_name: aws cloudwatch resource name
        old_tags: Dict of existing tags
        new_tags: Dict of new tags

    Returns:
        {"result": True|False, "comment": "A message", "ret": dict of updated tags}

    """
    result = dict(comment=[], result=True, ret={})
    tags_to_add = {}
    tags_to_delete = {}
    if new_tags is not None:
        tags_to_delete, tags_to_add = hub.tool.aws.tag_utils.diff_tags_dict(
            old_tags=old_tags, new_tags=new_tags
        )
    if (not tags_to_delete) and (not tags_to_add):
        result["ret"] = copy.deepcopy(old_tags if old_tags else {})
        return result
    if not ctx.get("test", False) and tags_to_delete:
        delete_tag_resp = await hub.exec.boto3.client.logs.untag_log_group(
            ctx, logGroupName=resource_name, tags=list(tags_to_delete.keys())
        )
        if not delete_tag_resp["result"]:
            result["comment"] = delete_tag_resp["comment"]
            result["result"] = False
            return result
    if not ctx.get("test", False) and tags_to_add:
        create_tag_resp = await hub.exec.boto3.client.logs.tag_log_group(
            ctx, logGroupName=resource_name, tags=tags_to_add
        )
        if not create_tag_resp["result"]:
            result["comment"] += create_tag_resp["comment"]
            result["result"] = False
            return result
    result["ret"] = new_tags
    if ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_update_tags_comment(
            tags_to_remove=tags_to_delete, tags_to_add=tags_to_add
        )
    else:
        result["comment"] = hub.tool.aws.comment_utils.update_tags_comment(
            tags_to_remove=tags_to_delete, tags_to_add=tags_to_add
        )
    return result
