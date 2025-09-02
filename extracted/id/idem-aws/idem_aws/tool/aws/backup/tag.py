import copy
from typing import Any
from typing import Dict


async def update_tags(
    hub,
    ctx,
    backup_vault_arn: str,
    old_tags: Dict[str, Any],
    new_tags: Dict[str, Any],
):
    """
    Update tags of AWS backup vault resources.

    Args:
        backup_vault_arn(str): AWS backup vault arn to add or update tags
        old_tags(Dict[str, str]): dict of old tags in the format of {"Name": name, "Description": a load balancer}
        new_tags(Dict[str, str]): dict of new tags in the format of {"Name": name, "Description": a load balancer}.
            If this value is None, the function will do no operation on tags.
    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": dict of updated tags}

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
            delete_ret = await hub.exec.boto3.client.backup.untag_resource(
                ctx,
                ResourceArn=backup_vault_arn,
                TagKeyList=[key for key, value in tags_to_remove.items()],
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result

    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.backup.tag_resource(
                ctx,
                ResourceArn=backup_vault_arn,
                Tags=tags_to_add,
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
