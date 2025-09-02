"""Exec module for updating status of cost allocation tags."""
from typing import Any
from typing import Dict


async def update_status(hub, ctx, tags: Dict[str, Any]):
    """Updates status of a cost allocation tags.

    If the tag status is already in same state, the request doesn't fail.
    Instead, it doesn't have any effect on the tag status (for example, activating the active tag).

    Args:
        tags(dict):
            Dictionary of Cost allocation tags in format {tag-key: tag-status}.

    Returns:
        Dict[str, str]
    """
    result = dict(comment=[], result=True, ret=None)

    # converting tag dict to list of tags, format required for api
    cost_allocation_tags = [
        {"TagKey": key, "Status": value} for key, value in tags.items()
    ]
    if not ctx.get("test", False):
        update_ret = await hub.exec.boto3.client.ce.update_cost_allocation_tags_status(
            ctx=ctx, CostAllocationTagsStatus=cost_allocation_tags
        )
        if not update_ret["result"]:
            result["comment"] += update_ret["comment"]
            result["result"] = False
            return result
    result["ret"] = {}
    result["ret"]["cost_allocation_tags"] = cost_allocation_tags
    if ctx.get("test", False):
        result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
            resource_type="aws.costexplorer.cost_allocation_tag",
            name=cost_allocation_tags,
        )
    else:
        result["comment"] += hub.tool.aws.comment_utils.update_comment(
            resource_type="aws.costexplorer.cost_allocation_tag",
            name=cost_allocation_tags,
        )

    return result
