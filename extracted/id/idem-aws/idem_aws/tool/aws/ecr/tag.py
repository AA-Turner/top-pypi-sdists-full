import copy
from typing import Any
from typing import Dict


async def update_tags(
    hub,
    ctx,
    resource_arn: str,
    old_tags: Dict[str, Any],
    new_tags: Dict[str, Any],
):
    """

    Args:
        hub:
        ctx:
        resource_arn: AWS resource arn
        old_tags: old tags in the format of {tag-key: tag-value}
        new_tags: new tags in the format of {tag-key: tag-value}. If this value is None, the function will do no operation on tags.

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": dict of updated tags}

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
        delete_tag_resp = await hub.exec.boto3.client.ecr.untag_resource(
            ctx, resourceArn=resource_arn, tagKeys=list(tags_to_delete.keys())
        )
        if not delete_tag_resp["result"]:
            hub.log.debug(
                f"Could not delete tags {tags_to_delete} for resource: '{resource_arn}' due to the error: {delete_tag_resp['comment']}"
            )
            result["comment"] = delete_tag_resp["comment"]
            result["result"] = False
            return result

    if not ctx.get("test", False) and tags_to_add:
        create_tag_resp = await hub.exec.boto3.client.ecr.tag_resource(
            ctx,
            resourceArn=resource_arn,
            tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags=tags_to_add),
        )
        if not create_tag_resp["result"]:
            hub.log.debug(
                f"Could not create tags {tags_to_add} for resource: '{resource_arn}' due to the error: {create_tag_resp['comment']}"
            )
            result["comment"] = create_tag_resp["comment"]
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


async def get_resource_tags(hub, ctx, resource_arn):
    """
    Get resource tags for an ecr resource
    Args:
        resource_arn(str):
            The ARN for the ecr resource
    """
    tag_results = dict(comment=[], ret=None, result=True)

    tags_ret = await hub.exec.boto3.client.ecr.list_tags_for_resource(
        ctx, resourceArn=resource_arn
    )

    if not tags_ret["result"]:
        hub.log.warning(
            f"Could not get tags for resource: {resource_arn}. Details: {tags_ret.get('comment')}"
        )
        return tag_results

    tag_results["ret"] = tags_ret["ret"].get("tags")
    return tag_results
