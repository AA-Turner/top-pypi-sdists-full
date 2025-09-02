"""Utility functions for Secretsmanager Tags. Tags related functions for AWS service 'secretsmanager'."""
import copy
from typing import Any
from typing import Dict


async def update_tags(
    hub, ctx, resource_id: str, old_tags: dict, new_tags: dict
) -> Dict[str, Any]:
    r"""
    Updates tags for a given resource.
    """

    result = dict(comment=[], result=True, ret=None)
    tags_to_add = {}
    tags_to_remove = {}
    if new_tags is not None:
        tags_to_remove, tags_to_add = hub.tool.aws.tag_utils.diff_tags_dict(
            old_tags=old_tags, new_tags=new_tags
        )

    if (not tags_to_remove) and (not tags_to_add):
        # If there is nothing to add or remove, return from here with old tags, if present
        result["ret"] = copy.deepcopy(old_tags if old_tags else {})
        return result

    if tags_to_remove:
        if not ctx.get("test", False):
            delete_ret = await hub.exec.boto3.client.secretsmanager.untag_resource(
                ctx, SecretId=resource_id, TagKeys=list(tags_to_remove.keys())
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result

    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.secretsmanager.tag_resource(
                ctx,
                SecretId=resource_id,
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
