import copy
from typing import Any
from typing import Dict


async def update_tags(
    hub,
    ctx,
    key_id: str,
    old_tags: Dict[str, Any],
    new_tags: Dict[str, Any],
):
    """

    Args:
        hub:
        ctx:
        key_id: aws kms key id
        old_tags: dict of old tags
        new_tags: dict of new tags

    Returns:
        {"result": True|False, "comment": Tuple, "ret": "dict of tags after update"}

    """
    result = dict(comment=[], result=True, ret=None)

    tags_to_add = {}
    tags_to_remove = {}
    if new_tags is not None:
        tags_to_remove, tags_to_add = hub.tool.aws.tag_utils.diff_tags_dict(
            old_tags=old_tags, new_tags=new_tags
        )
    if (not tags_to_remove) and (not tags_to_add):
        result["ret"] = copy.deepcopy(old_tags if old_tags else {})
        return result
    if tags_to_remove and not ctx.get("test", False):
        tag_keys = list(tags_to_remove.keys())
        delete_ret = await hub.exec.boto3.client.kms.untag_resource(
            ctx, KeyId=key_id, TagKeys=tag_keys
        )
        if not delete_ret["result"]:
            result["comment"] = delete_ret["comment"]
            result["result"] = False
            return result
    if tags_to_add and not ctx.get("test", False):
        add_ret = await hub.exec.boto3.client.kms.tag_resource(
            ctx,
            KeyId=key_id,
            Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list_tagkey(
                tags=tags_to_add
            ),
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
