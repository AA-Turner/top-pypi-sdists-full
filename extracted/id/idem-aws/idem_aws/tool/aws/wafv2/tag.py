"""Tag utility module to add/remove/update tags for AWS WAFV2 resources."""
import copy
from typing import Any
from typing import Dict


async def get_tags_for_resource(hub, ctx, resource_arn: str = None):
    """Gets the tags for a wafv2 resources.

    Args:
        hub:
            The redistributed pop central hub.
        ctx:
            A dict with the keys/values for the execution of the Idem run located in
            `hub.idem.RUNS[ctx['run_name']]`.
        resource_arn (str):
            The Amazon Resource Name (ARN) of the entity.

    Returns:
           Dict[str, Any]

    Example:
        .. code-block:: python

            async def state_function(hub, ctx, resource_arn, old_tags, new_tags):
                tag= await hub.tool.aws.wafv2.tag.get_tags_for_resource(ctx, resource_arn=resource_arn)
    """
    result = dict(comment=[], result=False, ret=None)
    if not resource_arn:
        return result
    tags = await hub.exec.boto3.client.wafv2.list_tags_for_resource(
        ctx, ResourceARN=resource_arn
    )
    result["ret"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
        tags["ret"]["TagInfoForResource"]["TagList"] if tags.get("result") else None
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
    resource_arn: str,
    old_tags: Dict[str, Any],
    new_tags: Dict[str, Any],
):
    """Update the tags for a wafv2 resources in AWS.

    Args:
        hub:
            The redistributed pop central hub.
        ctx:
            A dict with the keys/values for the execution of the Idem run located in
                `hub.idem.RUNS[ctx['run_name']]`.
        resource_arn (str):
            The Amazon Resource Name (ARN) of the entity
        old_tags(dict of str):
            dict in the format of {tag-key: tag-value}
        new_tags(dict of str):
            dict in the format of {tag-key: tag-value}
    """
    tags_to_add = {}
    tags_to_remove = {}
    if new_tags is not None and not new_tags == []:
        tags_to_remove, tags_to_add = hub.tool.aws.tag_utils.diff_tags_dict(
            old_tags=old_tags, new_tags=new_tags
        )
    result = dict(comment=[], result=True, ret={})
    if (not tags_to_remove) and (not tags_to_add):
        result["ret"] = copy.deepcopy(old_tags if old_tags else {})
        return result
    if tags_to_remove:
        if not ctx.get("test", False):
            delete_ret = await hub.exec.boto3.client.wafv2.untag_resource(
                ctx,
                ResourceARN=resource_arn,
                TagKeys=[key for key, value in tags_to_remove.items()],
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result
    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.wafv2.tag_resource(
                ctx,
                ResourceARN=resource_arn,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags=tags_to_add),
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
