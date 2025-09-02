"""Exec module for managing s3 bucket."""
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(hub, ctx, name: str, resource_id: str) -> Dict:
    """Returns the S3 bucket.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str):
            AWS S3 bucket name.

    Examples:
        Calling from the CLI:

        .. code-block:: bash

            $ idem exec aws.s3.bucket.get name="bucket-name" resource_id="bucket-id"

        Using in a state:

        .. code-block:: yaml

            get_a_bucket:
              exec.run:
                - path: aws.s3.bucket.get
                - kwargs:
                   name: bucket-name
                   resource_id: bucket-id
    """
    result = dict(comment=[], ret=None, result=True)
    resource = await hub.tool.boto3.resource.create(ctx, "s3", "Bucket", resource_id)
    ret = await hub.tool.boto3.resource.describe(resource)
    if not ret:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.s3.bucket", name=name
            )
        )
        return result

    result[
        "ret"
    ] = await hub.tool.aws.s3.conversion_utils.convert_raw_s3_to_present_async(
        ctx, idem_resource_name=resource_id
    )
    return result


async def list_(
    hub,
    ctx,
    name: str = None,
) -> Dict:
    """Fetch a list of bucket from AWS that are owned by the calling user.

    The function returns empty list when no resource is found.

    Args:
        name(str, Optional):
            The name of the Idem state.

    Examples:
        Calling from the CLI:

        .. code-block:: bash

            $ idem exec aws.s3.bucket.list name="bucket-search-for-user-A"

        Using in a state:

        .. code-block:: yaml

            buckets_list:
              exec.run:
                - path: aws.s3.bucket.list
    """
    result = dict(comment=[], ret=[], result=True)
    ret = await hub.exec.boto3.client.s3.list_buckets(ctx)
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["Buckets"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.s3.bucket", name=name
            )
        )
        return result
    for bucket in ret["ret"]["Buckets"]:
        result["ret"].append(
            await hub.tool.aws.s3.conversion_utils.convert_raw_s3_to_present_async(
                ctx=ctx, idem_resource_name=bucket["Name"]
            )
        )
    return result
