import copy
from typing import Any
from typing import Dict
from typing import List


async def update_tags(
    hub,
    ctx,
    resource_id,
    old_tags: List[Dict[str, Any]] or Dict[str, str],
    new_tags: List[Dict[str, Any]] or Dict[str, str],
):
    """
    Update tags of AWS EC2 resources.

    Args:
        resource_id:
            aws resource id.

        old_tags:
            list of old tags in the format of ``[{"Key": tag-key, "Value": tag-value}]`` or dict in the format of
            ``{tag-key: tag-value}``.

        new_tags:
            list of new tags in the format of ``[{"Key": tag-key, "Value": tag-value}]`` or dict in the format of
            ``{tag-key: tag-value}``. If this value is None, the function will do no operation on tags.

    Returns:
        Dict[str, Any]

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
            delete_ret = await hub.exec.boto3.client.ec2.delete_tags(
                ctx,
                Resources=[resource_id],
                Tags=[{"Key": key} for key, value in tags_to_remove.items()],
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result
    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.ec2.create_tags(
                ctx,
                Resources=[resource_id],
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


async def get_tags_for_resource(hub, ctx, resource_id: str) -> Dict[str, Any]:
    r"""
    Get tags for a given resource in EC2.
    """
    result = dict(comment=[], result=True, ret=None)

    if not resource_id:
        result["result"] = False
        result["comment"] = ["resource_id parameter is None"]
        return result

    tags_ret = await hub.exec.boto3.client.ec2.describe_tags(
        ctx,
        Filters=[
            {
                "Name": "resource-id",
                "Values": [
                    resource_id,
                ],
            },
        ],
    )

    if not tags_ret["result"]:
        result["result"] = False
        result["comment"] = tags_ret["comment"]
        return result

    if tags_ret.get("ret"):
        tags = tags_ret.get("ret").get("Tags")

    result["ret"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    return result
