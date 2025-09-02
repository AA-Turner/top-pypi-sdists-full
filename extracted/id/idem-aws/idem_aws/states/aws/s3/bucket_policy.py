"""State module for managing AWS S3 bucket policy."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]

TREQ = {
    "present": {
        "require": [
            "aws.s3.bucket.present",
        ],
    },
}

BUCKET_NOT_EXISTS_ERROR_MESSAGE = "ClientError: An error occurred (404) when calling the HeadBucket operation: Not Found"


async def present(
    hub,
    ctx,
    name: str,
    bucket: str,
    policy: str,
    confirm_remove_self_bucket_access: bool = None,
    expected_bucket_owner: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Applies an Amazon S3 bucket policy to an Amazon S3 bucket.

    If you are using an identity other than the root user of the Amazon Web Services account that owns the bucket, the
    calling identity must have the PutBucketPolicy permissions on the specified bucket and belong to the bucket owner's
    account in order to use this operation. If you don't have PutBucketPolicy permissions, Amazon S3 returns a
    403 Access Denied error. If you have the correct permissions, but you're not using an identity that belongs to the
    bucket owner's account, Amazon S3 returns a 405 Method Not Allowed error.

    Args:
        name(str):
            The name of the bucket policy.

        bucket(str):
            The name of the S3 bucket

        policy(str):
            The bucket policy as a JSON document.

        confirm_remove_self_bucket_access(bool, Optional):
            Set this parameter to true to confirm that you want to remove
            your permissions to change this bucket policy in the future.

        expected_bucket_owner(str, Optional):
            The account ID of the expected bucket owner. If the bucket is owned
            by a different account, the request will fail with an HTTP 403 (Access Denied) error.

        resource_id(str, Optional):
            S3 Bucket policy ID

    Request Syntax:
        .. code-block:: yaml

            [bucket_name]-policy:
              aws.s3.bucket_policy.present:
                - bucket: "string"
                - policy: "string"
                - confirm_remove_self_bucket_access: "bool"
                - expected_bucket_owner: "string"

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            my-s3-bucket-bb7bb32e9533-policy:
              aws.s3.bucket_policy.present:
                - bucket: my-s3-bucket-bb7bb32e9533
                - policy: '{"Version":"2012-10-17","Statement":[{"Sid":"PublicReadGetObject","Effect":"Allow","Principal":{"AWS":"arn:aws:iam::418235808912:root"},"Action":"s3:GetObject","Resource":"arn:aws:s3:::thebugbucket3/*"}]}'
                - confirm_remove_self_bucket_access: False
                - expected_bucket_owner: 1239234249


    """
    result = dict(comment=[], name=name, old_state=None, new_state=None, result=True)

    # Check if Policy state name has correct format i.e. [bucket_name]-policy
    if name.split("-policy")[0] != bucket:
        result["comment"] += [
            f"Incorrect aws.s3.bucket_policy name: {name}. Expected name {bucket}-policy"
        ]
        result["result"] = False
        return result

    before = None
    resource_updated = False
    plan_state = None

    # Standardise on the json format
    policy = hub.tool.aws.state_comparison_utils.standardise_json(policy)
    # Get current bucket policy for the bucket
    if resource_id:
        before = await hub.exec.boto3.client.s3.get_bucket_policy(
            ctx, Bucket=bucket, ExpectedBucketOwner=expected_bucket_owner
        )
        if not before["result"] or not before["ret"]:
            result["comment"] += [
                f"Failed to get existing Bucket policy '{name}'"
            ] + before["comment"]
            result["result"] = before["result"]
            return result

        result[
            "old_state"
        ] = hub.tool.aws.s3.conversion_utils.convert_raw_bucket_policy_to_present(
            raw_resource=before["ret"], bucket=bucket, name=name
        )
        plan_state = copy.deepcopy(result["old_state"])
        result["comment"] += [f"Bucket policy '{name}' already present."]
        if not hub.tool.aws.state_comparison_utils.are_policies_equal(
            result["old_state"]["policy"], policy
        ):
            resource_updated = True
            plan_state["policy"] = policy

    # Handling test scenario seperately
    if ctx.get("test", False):
        if not before:
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "policy": policy,
                    "bucket": bucket,
                    "resource_id": bucket + "-policy",
                },
            )
            result["comment"] += [f"Would create aws.s3.bucket_policy '{name}'"]
        else:
            result["new_state"] = plan_state
            if resource_updated:
                result["comment"] += [f"Would update aws.s3.bucket_policy '{name}'"]
            else:
                result["comment"] += [f"No change in policy."]
        return result

    # Check if bucket exists
    if not ctx.get("test", False):
        ret = await hub.exec.boto3.client.s3.head_bucket(ctx, Bucket=bucket)
        if not ret["result"]:
            if BUCKET_NOT_EXISTS_ERROR_MESSAGE in ret["comment"]:
                result["comment"] += [
                    f"aws.s3.bucket with name: {bucket} does not exist"
                ]
            else:
                result["comment"] = ret["comment"]
            result["result"] = False
            return result

    # If policy is not present or if it is updated
    if (not before) or resource_updated:
        ret = await hub.exec.boto3.client.s3.put_bucket_policy(
            ctx,
            Bucket=bucket,
            Policy=policy,
            ConfirmRemoveSelfBucketAccess=confirm_remove_self_bucket_access,
            ExpectedBucketOwner=expected_bucket_owner,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        if resource_updated:
            result["comment"] += [f"Policy updated successfully"]
        else:
            result["comment"] += [f"Bucket policy '{name}' created."]
        after = await hub.exec.boto3.client.s3.get_bucket_policy(
            ctx, Bucket=bucket, ExpectedBucketOwner=expected_bucket_owner
        )
        result[
            "new_state"
        ] = hub.tool.aws.s3.conversion_utils.convert_raw_bucket_policy_to_present(
            raw_resource=after["ret"], bucket=bucket, name=name
        )
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
        result["comment"] += [f"No change in policy."]
    return result


async def absent(
    hub,
    ctx,
    name: str,
    bucket: str = None,
    resource_id: str = None,
    expected_bucket_owner: str = None,
) -> Dict[str, Any]:
    """Deletes the policy of specified s3 bucket.

    Args:
        name(str):
            The name of the bucket policy.

        bucket(str, Optional):
            The name of the S3 bucket

        resource_id(str, Optional):
            S3 Bucket policy ID. Idem automatically considers this resource being absent if this field is not specified.

        expected_bucket_owner(str, Optional):
            The account ID of the expected bucket owner. If the bucket is owned by a different account, the request
            will fail with an HTTP 403 (Access Denied) error.

    Request Syntax:
        .. code-block:: sls

            [bucket_name]-policy:
              aws.s3.bucket_policy.absent:
                - bucket: string
                - expected_bucket_owner: string
    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            my-s3-bucket-bb7bb32e9533-policy:
              aws.s3.bucket_policy.absent:
                - bucket: my-s3-bucket-bb7bb32e9533
                - expected_bucket_owner: 1239234249
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.s3.bucket_policy", name=name
        )
        return result

    if not bucket:
        result["comment"] = hub.tool.aws.comment_utils.missing_args_for_absent_comment(
            resource_type="aws.s3.bucket_policy", name=name, args=["bucket"]
        )
        result["result"] = False
        return result

    if resource_id.split("-policy")[0] != bucket:
        result["comment"] += [f"Incorrect aws.s3.bucket name: '{bucket}'"]
        result["result"] = False
        return result

    # Check if bucket exists.
    ret = await hub.exec.boto3.client.s3.head_bucket(ctx, Bucket=bucket)
    if not ret["result"]:
        if BUCKET_NOT_EXISTS_ERROR_MESSAGE in ret["comment"]:
            result["comment"] += [f"aws.s3.bucket with name: '{bucket}' does not exist"]
        else:
            result["comment"] = ret["comment"]
        result["result"] = False
        return result

    before = await hub.exec.boto3.client.s3.get_bucket_policy(
        ctx, Bucket=bucket, ExpectedBucketOwner=expected_bucket_owner
    )

    if before and before["result"]:
        result[
            "old_state"
        ] = hub.tool.aws.s3.conversion_utils.convert_raw_bucket_policy_to_present(
            raw_resource=before["ret"], bucket=bucket, name=name
        )

        if ctx.get("test", False):
            result["comment"] += [f"Would delete aws.s3.bucket_policy '{name}'"]
            return result

        ret = await hub.exec.boto3.client.s3.delete_bucket_policy(
            ctx, Bucket=bucket, ExpectedBucketOwner=expected_bucket_owner
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] += [f"Deleted policy '{name}' for bucket '{bucket}'"]
        return result
    else:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.s3.bucket_policy", name=name
        )
        return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Obtain S3 bucket policy for each bucket under the given context for any user.

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.s3.bucket_policy
    """
    result = {}
    # To describe the policy of all the buckets, we first need to list all the buckets, then get the
    # policy of each bucket
    ret = await hub.exec.boto3.client.s3.list_buckets(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe S3 buckets {ret['comment']}")
        return {}

    for bucket in ret["ret"]["Buckets"]:
        bucket_name = bucket.get("Name")
        # get policy for each bucket
        bucket_policy = await hub.exec.boto3.client.s3.get_bucket_policy(
            ctx, Bucket=bucket_name
        )
        if bucket_policy["result"]:
            bucket_policy_name = f"{bucket_name}-policy"
            # translate policy to a common format
            policy_translated = (
                hub.tool.aws.s3.conversion_utils.convert_raw_bucket_policy_to_present(
                    raw_resource=bucket_policy["ret"],
                    bucket=bucket_name,
                    name=bucket_policy_name,
                )
            )
            result[bucket_policy_name] = {
                "aws.s3.bucket_policy.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in policy_translated.items()
                ]
            }
    return result
