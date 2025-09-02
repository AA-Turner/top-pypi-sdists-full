import copy
from typing import Any
from typing import Dict
from typing import List


async def update_tags(
    hub,
    ctx,
    resource_id,
    old_tags: List[Dict[str, Any]] or Dict[str, Any],
    new_tags: List[Dict[str, Any]] or Dict[str, Any],
):
    """
    Update tags of AWS Certificate
    Args:
        hub:
        ctx:
        resource_id: the Amazon Resource Name (ARN) of certificate to identify the resource
        old_tags: list of old tags in the format of [{"Key": tag-key, "Value": tag-value}] or dict in the format of
         {tag-key: tag-value}
        new_tags: list of new tags in the format of [{"Key": tag-key, "Value": tag-value}] or dict in the format of
         {tag-key: tag-value}. If this value is None, the function will do no operation on tags.

    Returns:
        {"result": True|False, "comment": "A tuple", "ret": dict of updated tags}

    """
    tags_to_add = {}
    tags_to_remove = {}
    if isinstance(old_tags, List):
        old_tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(old_tags)
    if isinstance(new_tags, List):
        new_tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(new_tags)
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
            delete_ret = await hub.exec.boto3.client.acm.remove_tags_from_certificate(
                ctx,
                CertificateArn=resource_id,
                Tags=[{"Key": key} for key, value in tags_to_remove.items()],
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result
    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.acm.add_tags_to_certificate(
                ctx,
                CertificateArn=resource_id,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags_to_add),
            )
            if not add_ret["result"]:
                result["comment"] = add_ret["comment"]
                result["result"] = False
                return result
    result["ret"] = new_tags
    result["comment"] += [f"Update tags: Add [{tags_to_add}] Remove [{tags_to_remove}]"]
    return result
