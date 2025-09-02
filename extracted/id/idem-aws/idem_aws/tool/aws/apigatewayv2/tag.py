"""Util functions for AWS API Gateway v2 tags."""
import copy
from typing import Any
from typing import Dict


async def update_tags(
    hub,
    ctx,
    resource_arn: str,
    old_tags: Dict[str, Any],
    new_tags: Dict[str, Any],
) -> Dict[str, Any]:
    """Updates tags for an AWS API Gateway v2 resource.

    Args:
        resource_arn(str):
            AWS API Gateway v2 resource arn.

        old_tags(dict[str, Any]):
            List of existing tags in the format of ``{"Key": tag-key, "Value": tag-value}``.

            * Key (*str*):
                The key of the tag.
            * Value (*str*):
                The value of the tag.

        new_tags(dict[str, Any]):
            List of new tags in the format of ``{"Key": tag-key, "Value": tag-value}``.

            * Key (*str*):
                The key of the tag.
            * Value (*str*):
                The value of the tag.

    Returns:
        Dict[str, Any]:
            Returns updated tags for the resource.
    """
    result = dict(comment=[], result=True, ret=None)

    tags_to_add = {}
    tags_to_remove = []
    tags_result = copy.deepcopy(old_tags)

    for key, value in new_tags.items():
        if (key in old_tags and old_tags.get(key) != new_tags.get(key)) or (
            key not in old_tags
        ):
            tags_to_add[key] = value

    for key in old_tags:
        if key not in new_tags:
            tags_to_remove.append(key)

    if tags_to_remove:
        if not ctx.get("test", False):
            untag_ret = await hub.exec.boto3.client.apigatewayv2.untag_resource(
                ctx, ResourceArn=resource_arn, TagKeys=tags_to_remove
            )
            if not untag_ret["result"]:
                result["result"] = False
                result["comment"] = untag_ret["comment"]
                return result
        [tags_result.pop(key, None) for key in tags_to_remove]

    if tags_to_add:
        if not ctx.get("test", False):
            tag_ret = await hub.exec.boto3.client.apigatewayv2.tag_resource(
                ctx, ResourceArn=resource_arn, Tags=tags_to_add
            )
            if not tag_ret["result"]:
                result["result"] = False
                result["comment"] = tag_ret["comment"]
                return result

    if ctx.get("test", False):
        result["comment"] += [
            f"Would update tags: Add {list(tags_to_add.keys())} Remove {tags_to_remove}"
        ]
    else:
        result["comment"] += [
            f"Updated tags: Add {list(tags_to_add.keys())} Remove {tags_to_remove}"
        ]
    result["ret"] = {"tags": {**tags_result, **tags_to_add}}
    return result
