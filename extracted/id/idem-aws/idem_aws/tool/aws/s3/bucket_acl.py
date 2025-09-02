"""Tool module for managing Amazon S3 bucket policy."""
from typing import Any
from typing import Dict

from dict_tools import data


async def update(
    hub,
    ctx,
    resource_id: str,
    raw_resource: Dict[str, Any],
    access_control_policy: Dict[str, None],
) -> Dict[str, Any]:
    """Updates an AWS Bucket ACL resource.

    Args:
        resource_id(str):
            ACL Policy name identifier in Amazon Web Services.

        raw_resource(Dict):
            Existing resource parameters in Amazon Web Services.

        access_control_policy(Dict):
            Parameters from SLS file.

    Returns:
        Dict[str, Any]
    """
    result = dict(comment=[], result=True, ret=None)

    acl_policy_diff = data.recursive_diff(
        access_control_policy, raw_resource, ignore_order=True
    )

    if acl_policy_diff:
        result["ret"] = {}

        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.s3.put_bucket_acl(
                ctx,
                Bucket=resource_id,
                AccessControlPolicy=access_control_policy,
            )
            if not update_ret["result"]:
                result["comment"] = update_ret["comment"]
                result["result"] = False
                return result
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.s3.bucket_acl", name=resource_id
            )
        result["ret"]["access_control_policy"] = access_control_policy

    return result
