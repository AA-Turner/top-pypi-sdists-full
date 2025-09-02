import copy
from typing import Any
from typing import Dict


async def get_tags_for_resource(hub, ctx, resource_arn: str):
    """
    Gets the tags for a docdb resource

    Args:
        hub:
        ctx:
        resource_arn(str): aws resource arn

    Returns:
        {"result": True|False, "comment": "A message tuple", "ret": Dict['str', Any]|None}
    """
    result = dict(comment=[], result=False, ret=None)
    if not resource_arn:
        return result
    tags = await hub.exec.boto3.client.docdb.list_tags_for_resource(
        ctx, ResourceName=resource_arn
    )
    result["ret"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
        tags.get("ret").get("TagList") if tags.get("result") else None
    )
    result["result"] = tags.get("result")
    if not result["result"]:
        result[
            "comment"
        ] = f"Getting tags for resource with resource_arn: `{resource_arn}` failed"
    return result


async def update_tags(
    hub,
    ctx,
    resource_arn,
    old_tags: Dict[str, Any],
    new_tags: Dict[str, Any],
):
    """Update tags of AWS Doc DB resources.

    Args:
        hub:
        ctx:
        resource_arn: aws resource arn
        old_tags: dict in the format of {tag-key: tag-value}
        new_tags: dict in the format of {tag-key: tag-value}

    Returns:
        Dict[str, Any]

    Example:
        {"result": True|False, "comment": "A message tuple", "ret": dict of updated tags}
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
            delete_ret = await hub.exec.boto3.client.docdb.remove_tags_from_resource(
                ctx,
                ResourceName=resource_arn,
                TagKeys=[key for key, value in tags_to_remove.items()],
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result
    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.docdb.add_tags_to_resource(
                ctx,
                ResourceName=resource_arn,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags_to_add),
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
