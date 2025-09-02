"""Exec functions for s3 bucket's website configurations."""
from typing import Dict


async def get(
    hub, ctx, resource_id: str, name: str = None, expected_bucket_owner: str = None
) -> Dict:
    """Returns the website configuration of a bucket.

    Args:

        resource_id(str):
            AWS S3 bucket name.

        name(str, Optional):
            The name of the Idem state.

        expected_bucket_owner(str, Optional):
            The account ID of the expected bucket owner. If the bucket is owned by a different account, the
            request fails with the HTTP status code 403 Forbidden (access denied). Defaults to None.

    Examples:
        Calling from the CLI:

        .. code-block:: bash

            $ idem exec aws.s3.bucket_website.get name="bucket-name" resource_id="bucket-id"

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
    ret = await hub.exec.boto3.client.s3.get_bucket_website(
        ctx, Bucket=resource_id, ExpectedBucketOwner=expected_bucket_owner
    )
    if not ret["result"]:
        if "NoSuchWebsiteConfiguration" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.s3.bucket_website", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    result[
        "ret"
    ] = hub.tool.aws.s3.bucket_website.convert_raw_bucket_website_to_present(
        bucket=resource_id, raw_resource=ret["ret"], idem_resource_name=name
    )
    return result
