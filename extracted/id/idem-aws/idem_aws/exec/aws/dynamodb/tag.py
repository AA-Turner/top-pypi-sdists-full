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
    """Update tags of AWS Dynamo DB resources

    Args:
        resource_arn:
            Identifies the Amazon DynamoDB resource to which tags should be added.
            This value is an Amazon Resource Name (ARN).

        old_tags:
            Dict of existing tags.

        new_tags:
            Dict of new tags.

    Returns:
        {"result": True|False, "comment": ["A list"], "ret": dict of updated tags}

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
            delete_ret = await hub.exec.boto3.client.dynamodb.untag_resource(
                ctx,
                ResourceArn=resource_arn,
                TagKeys=list(tags_to_remove.keys()),
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result
    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.dynamodb.tag_resource(
                ctx,
                ResourceArn=resource_arn,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags_to_add),
            )
            if not add_ret["result"]:
                result["comment"] += add_ret["comment"]
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
