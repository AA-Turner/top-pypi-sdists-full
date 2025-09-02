"""RDS Tag operations"""
import copy
from typing import Any
from typing import Dict


async def update_rds_tags(
    hub,
    ctx,
    resource_arn,
    old_tags: Dict[str, Any],
    new_tags: Dict[str, Any],
):
    """
    Update tags of AWS RDS resources

    Args:
        resource_arn (str):
            AWS resource arn

        old_tags (dict):
            Dict in the format of {tag-key: tag-value}

        new_tags (dict):
            Dict in the format of {tag-key: tag-value}

    Returns:
        {"result": True|False, "comment": "A message", "ret": dict of updated tags}

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.rds.tag.update_rds_tags resource_arn="some_arn" old_tags='{"old_tag": "old_val"}' new_tags='{"new_tag": "new_val"}'

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.rds.tag.update_rds_tags
                - kwargs:
                    resource_arn: some_arn
                    old_tags:
                      old_tag: old_val
                    new_tags:
                      new_tag: new_val
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
            delete_ret = await hub.exec.boto3.client.rds.remove_tags_from_resource(
                ctx,
                ResourceName=resource_arn,
                TagKeys=list(tags_to_remove),
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result
    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.rds.add_tags_to_resource(
                ctx,
                ResourceName=resource_arn,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags_to_add),
            )
            if not add_ret["result"]:
                result["comment"] = add_ret["comment"]
                result["result"] = False
                return result
    result["ret"] = new_tags
    result["comment"] += [f"Update tags: Add [{tags_to_add}] Remove [{tags_to_remove}]"]
    return result
