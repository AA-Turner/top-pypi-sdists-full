from typing import Dict


async def update(
    hub,
    ctx,
    resource_id,
    old_tags: Dict[str, str],
    new_tags: Dict[str, str],
):
    """
    Update tags of AWS Elasticsearch domain. No update is performed if new_tags is none

    Args:
        resource_id(str): AWS Elasticsearch domain resource id
        old_tags(Dict[str, str]): dict of old tags
        new_tags(Dict[str, str]): dict of new tags

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": dict of updated tags}

    """
    tags_to_add = {}
    tags_to_remove = {}
    if new_tags is not None:
        tags_to_remove, tags_to_add = hub.tool.aws.tag_utils.diff_tags_dict(
            old_tags=old_tags, new_tags=new_tags
        )

    result = dict(comment=[], result=True, ret={})
    if (not tags_to_remove) and (not tags_to_add):
        return result

    account_details = await hub.exec.boto3.client.sts.get_caller_identity(ctx)
    account_id = account_details["ret"]["Account"]
    resource_arn = hub.tool.aws.arn_utils.build(
        service="es",
        region=ctx["acct"]["region_name"],
        account_id=account_id,
        resource="domain/" + resource_id,
    )
    if tags_to_remove:
        if not ctx.get("test", False):
            delete_ret = await hub.exec.boto3.client.es.remove_tags(
                ctx,
                ARN=resource_arn,
                TagKeys=[key for key, value in tags_to_remove.items()],
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result
    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.es.add_tags(
                ctx,
                ARN=resource_arn,
                TagList=hub.tool.aws.tag_utils.convert_tag_dict_to_list(
                    tags=tags_to_add
                ),
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
