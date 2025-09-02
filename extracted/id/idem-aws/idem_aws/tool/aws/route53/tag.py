import copy
from typing import Any
from typing import Dict
from typing import List


async def update_tags(
    hub,
    ctx,
    resource_id: str,
    resource_type: str,
    old_tags: List[Dict[str, Any]] or Dict[str, Any] = None,
    new_tags: List[Dict[str, Any]] or Dict[str, Any] = None,
):
    """
    Update tags of AWS route53 hosted zone resources
    Args:
        resource_id (str):
            route53 hosted_zone resource id

        resource_type (str):
            type of resource

        old_tags (list or dict):
            list of old tags in the format of ``[{"Key": tag-key, "Value": tag-value}]`` or dict in the format of
            ``{tag-key: tag-value}``

        new_tags (list or dict):
            list of new tags in the format of ``[{"Key": tag-key, "Value": tag-value}]`` or dict in the format of
            ``{tag-key: tag-value}``

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
    elif not tags_to_remove:
        tags_to_remove = None
    elif not tags_to_add:
        tags_to_add = None
    if not ctx.get("test", False):
        change_tag_resp = await hub.exec.boto3.client.route53.change_tags_for_resource(
            ctx,
            ResourceType=resource_type,
            ResourceId=resource_id,
            AddTags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags_to_add),
            RemoveTagKeys=list(tags_to_remove) if tags_to_remove else None,
        )
        if not change_tag_resp["result"]:
            response_message = change_tag_resp["comment"]
            hub.log.debug(
                f"Could not modify tags for {resource_id} with error {response_message}"
            )
            result["comment"] += [
                f"Could not modify tags for {resource_id} with error {response_message}"
            ]
            result["result"] = False
            return result
        hub.log.debug(f"modified tags for {resource_id}")

    result["ret"] = new_tags
    result["comment"] += [f"Update tags: Add [{tags_to_add}] Remove [{tags_to_remove}]"]
    return result
