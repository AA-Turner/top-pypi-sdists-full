"""Exec module for managing Amazon Cloudfront Distribution."""
from typing import Dict


async def get(
    hub,
    ctx,
    name,
    resource_id: str,
) -> Dict:
    """Use an un-managed Cloudfront distribution as a data-source. Supply resource_id as a filter.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str):
            AWS cloudfront distribution id to identify the resource.

    Returns:
        .. code-block:: python

            {"result": True|False, "comment": A message List, "ret": None|Dict}

    Examples:
        Calling this exec module function from the cli with name and resource_id

        .. code-block:: bash

            idem exec aws.cloudfront.distribution.get name="name" resource_id="resource_id"

        Calling this exec module function from within a state module in pure python.

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id):
                before = await hub.exec.aws.cloudfront.distribution.get(
                ctx, name=name, resource_id=resource_id
            )
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.cloudfront.get_distribution(ctx, Id=resource_id)
    if not ret["result"]:
        if "NoSuchDistribution" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.cloudfront.distribution", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["Distribution"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.cloudfront.distribution", name=name
            )
        )
        return result
    arn = ret["ret"]["Distribution"]["ARN"]
    before_tag = await hub.exec.boto3.client.cloudfront.list_tags_for_resource(
        ctx, Resource=arn
    )
    if not before_tag["result"]:
        result["result"] = False
        result["comment"] = before_tag["comment"]
        return result

    if before_tag["ret"].get("Tags"):
        ret["ret"]["Distribution"]["Tags"] = (
            before_tag["ret"].get("Tags").get("Items", [])
        )
    ret["ret"]["Distribution"]["ETag"] = ret["ret"]["ETag"]
    result[
        "ret"
    ] = hub.tool.aws.cloudfront.conversion_utils.convert_raw_distribution_to_present(
        ctx, raw_resource=ret["ret"]["Distribution"], idem_resource_name=name
    )
    return result
