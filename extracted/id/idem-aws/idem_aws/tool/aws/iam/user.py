import copy
from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}


async def update_user_tags(
    hub,
    ctx,
    user_name: str,
    old_tags: Dict[str, Any],
    new_tags: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Update tags of AWS IAM user

    Args:
        hub: The redistributed pop central hub.
        ctx: A dict with the keys/values for the execution of the Idem run located in
        `hub.idem.RUNS[ctx['run_name']]`.
        user_name: AWS IAM username
        old_tags: dict of old tags
        new_tags: dict of new tags

    Returns:
        {"result": True|False, "comment": Tuple, "ret": Dict}
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
            tag_keys = list(tags_to_remove.keys())
            delete_ret = await hub.exec.boto3.client.iam.untag_user(
                ctx, UserName=user_name, TagKeys=tag_keys
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result
    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.iam.tag_user(
                ctx,
                UserName=user_name,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags=tags_to_add),
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


async def update_user(
    hub,
    ctx,
    before: Dict[str, Any],
    user_name: str = None,
    path: str = None,
):
    result = dict(comment=[], result=True, ret=None)
    update_payload = {}
    if user_name and before.get("user_name") != user_name:
        update_payload["NewUserName"] = user_name
    if path and before.get("path") != path:
        update_payload["NewPath"] = path
    if update_payload:
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.iam.update_user(
                ctx=ctx, UserName=before.get("resource_id"), **update_payload
            )
            if not update_ret["result"]:
                result["comment"] = update_ret["comment"]
                result["result"] = False
                return result
        result["ret"] = {}
        if "NewUserName" in update_payload:
            result["ret"]["user_name"] = update_payload["NewUserName"]
            result["comment"] += [
                f"Update user_name: {update_payload['NewUserName']} on user {before.get('user_name')}"
            ]
        if "NewPath" in update_payload:
            result["ret"]["path"] = update_payload["NewPath"]
            result["comment"] += [
                f"Update path: {update_payload['NewPath']} on user {before.get('user_name')}"
            ]
    return result
