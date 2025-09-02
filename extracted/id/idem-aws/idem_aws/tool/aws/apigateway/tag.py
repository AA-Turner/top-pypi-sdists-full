"""Tool functions for AWS API Gateway tags."""
import copy
from typing import Any
from typing import Dict


async def update(
    hub,
    ctx,
    resource_arn: str,
    old_tags: Dict[str, Any],
    new_tags: Dict[str, Any],
):
    """
    Updates tags for an AWS API Gateway resource.

    Args:
        resource_arn: AWS API Gateway resource arn.

        old_tags(dict[str, Any]): Dict of existing tags.

        new_tags(dict[str, Any]): Dict of new tags.

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": dict of updated tags}
    """
    result = dict(comment=[], result=True, ret=None)

    if new_tags is not None:
        tags_to_remove, tags_to_add = hub.tool.aws.tag_utils.diff_tags_dict(
            old_tags=old_tags, new_tags=new_tags
        )
    if (not tags_to_remove) and (not tags_to_add):
        result["ret"] = copy.deepcopy(old_tags if old_tags else {})
        return result

    if tags_to_remove:
        if not ctx.get("test", False):
            untag_ret = await hub.exec.boto3.client.apigateway.untag_resource(
                ctx,
                resourceArn=resource_arn,
                tagKeys=list(tags_to_remove.keys()),
            )
            if not untag_ret["result"]:
                result["result"] = False
                result["comment"] += untag_ret["comment"]
                return result

    if tags_to_add:
        if not ctx.get("test", False):
            tag_ret = await hub.exec.boto3.client.apigateway.tag_resource(
                ctx,
                resourceArn=resource_arn,
                tags=tags_to_add,
            )
            if not tag_ret["result"]:
                result["result"] = False
                result["comment"] += tag_ret["comment"]
                return result

    # If new_tags is coming empty, that would mean it is trying removing all tags.
    result["ret"] = new_tags if new_tags is not None else tags_to_remove

    if ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_update_tags_comment(
            tags_to_remove=tags_to_remove, tags_to_add=tags_to_add
        )
    else:
        result["comment"] = hub.tool.aws.comment_utils.update_tags_comment(
            tags_to_remove=tags_to_remove, tags_to_add=tags_to_add
        )
    return result
