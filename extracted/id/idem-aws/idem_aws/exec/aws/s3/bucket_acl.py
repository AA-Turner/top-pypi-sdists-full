"""Exec functions for S3 bucket's acl."""
from typing import Dict


async def get(hub, ctx, resource_id, name) -> Dict:
    """Returns the ACL policy for the S3 bucket.

    Args:
        resource_id(str):
            AWS S3 bucket name.

        name(str):
            The name of the Idem state.

    Examples:
        Calling from the CLI:

        .. code-block:: bash

            $ idem exec aws.s3.bucket_acl.get name="bucket-acl-name" resource_id="bucket-acl-id"

        Using in a state:

        .. code-block:: yaml

            get_a_bucket_acl:
              exec.run:
                - path: aws.s3.bucket_acl.get
                - kwargs:
                   name: bucket-acl-name
                   resource_id: bucket-acl-id
    """
    result = dict(comment=[], ret=None, result=True)

    ret = await hub.exec.boto3.client.s3.get_bucket_acl(ctx, Bucket=resource_id)
    if not ret["result"]:
        if "NotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.s3.bucket_acl", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    result["ret"] = hub.tool.aws.s3.conversion_utils.convert_raw_acl_policy_to_present(
        raw_resource=ret["ret"], bucket_name=resource_id
    )
    return result
