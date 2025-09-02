"""Exec functions for S3 bucket's logging."""
from typing import Dict


async def get(hub, ctx, name: str, resource_id: str) -> Dict:
    """Returns the logging configuration for the S3 bucket.

    Args:
        name(str):
            The name of the Idem state.
        resource_id(str):
            AWS S3 bucket name.

    Examples:
        Calling from the CLI:

        .. code-block:: bash

            $ idem exec aws.s3.bucket_logging.get name="bucket-logging-name" resource_id="bucket-logging-id"

        Using in a state:

        .. code-block:: yaml

            get_a_bucket_logging:
              exec.run:
                - path: aws.s3.bucket_logging.get
                - kwargs:
                   name: bucket-logging-name
                   resource_id: bucket-logging-id
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.s3.get_bucket_logging(ctx, Bucket=resource_id)

    if not ret["result"]:
        if "NoSuchBucket" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.s3.bucket_logging", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    if "LoggingEnabled" not in ret["ret"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.s3.bucket_logging", name=name
            )
        )
        result["comment"] += list(ret["comment"])
        return result

    result[
        "ret"
    ] = hub.tool.aws.s3.conversion_utils.convert_raw_bucket_logging_to_present(
        ctx=ctx, raw_resource=ret["ret"], bucket_name=resource_id
    )
    return result
