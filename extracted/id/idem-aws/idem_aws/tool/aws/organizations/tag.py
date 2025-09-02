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

    Args:
        resource_id: aws organizations resource id
        old_tags: dict in the format of {tag-key: tag-value}
        new_tags: dict in the format of {tag-key: tag-value}. If this value is None, the function will do no operation on tags.


    Returns:
        {"result": True|False, "comment": "A message Tuple", "ret": dict of updated tags}

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
            delete_tag_resp = await hub.exec.boto3.client.organizations.untag_resource(
                ctx, ResourceId=resource_id, TagKeys=list(tags_to_remove.keys())
            )
            if not delete_tag_resp["result"]:
                hub.log.debug(
                    f"Could not delete tags {tags_to_remove} on resource {resource_id} with error {delete_tag_resp['comment']}"
                )
                result["comment"] += delete_tag_resp["comment"]
                result["result"] = delete_tag_resp["result"]
                return result
    if tags_to_add:
        if not ctx.get("test", False):
            create_tag_resp = await hub.exec.boto3.client.organizations.tag_resource(
                ctx,
                ResourceId=resource_id,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags_to_add),
            )
            if not create_tag_resp["result"]:
                hub.log.debug(
                    f"Could not create tags {tags_to_add} on resource {resource_id} with error {create_tag_resp['comment']}"
                )
                result["comment"] += create_tag_resp["comment"]
                result["result"] = create_tag_resp["result"]
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
