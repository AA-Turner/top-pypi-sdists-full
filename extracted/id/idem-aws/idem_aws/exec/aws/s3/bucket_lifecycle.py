"""Exec functions for s3 bucket's lifecycle configurations."""
from typing import Dict


async def get(hub, ctx, name: str, resource_id: str) -> Dict:
    """Returns the lifecycle configuration of a bucket.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str):
            AWS S3 bucket name.

    Examples:
        Calling from the CLI:

        .. code-block:: bash

            $ idem exec aws.s3.bucket_lifecycle.get name="bucket-name" resource_id="bucket-id"

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
    ret = await hub.exec.boto3.client.s3.get_bucket_lifecycle_configuration(
        ctx, Bucket=resource_id
    )
    if not ret["result"]:
        if "NoSuchLifecycleConfiguration" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.s3.bucket_lifecycle", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    if "Rules" not in ret["ret"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.s3.bucket_lifecycle", name=name
            )
        )
        result["comment"] += list(ret["comment"])
        return result

    result[
        "ret"
    ] = hub.tool.aws.s3.bucket_lifecycle.convert_raw_bucket_lifecycle_to_present(
        bucket=resource_id, raw_resource=ret["ret"], idem_resource_name=name
    )
    return result
