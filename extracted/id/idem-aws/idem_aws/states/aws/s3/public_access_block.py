"""State module for managing AWS S3 bucket public access block."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict

__contracts__ = ["resource"]

TREQ = {
    "present": {
        "require": [
            "aws.s3.bucket.present",
        ],
    },
    "absent": {
        "require": [
            "aws.s3.bucket.absent",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    bucket: str,
    public_access_block_configuration: make_dataclass(
        "PublicAccessBlockConfiguration",
        [
            ("BlockPublicAcls", bool, field(default=None)),
            ("IgnorePublicAcls", bool, field(default=None)),
            ("BlockPublicPolicy", bool, field(default=None)),
            ("RestrictPublicBuckets", bool, field(default=None)),
        ],
    ),
    expected_bucket_owner: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Creates or modifies the PublicAccessBlock configuration for an Amazon S3 bucket.

    To use this operation, the calling entity must have the s3:PutBucketPublicAccessBlock permission.

    Args:
      name(str):
        The name of the bucket public access block configuration.

      bucket(str):
        Bucket name to identify the resource

      public_access_block_configuration(dict[str, Any]):
        The PublicAccessBlock configuration that you want to apply to this Amazon S3 bucket. You can
        enable the configuration options in any combination. For more information about when Amazon S3
        considers a bucket or object public, see The Meaning of "Public" in the Amazon S3 User Guide.

        * BlockPublicAcls (bool, Optional):
            Specifies whether Amazon S3 should block public access control lists (ACLs) for this bucket and
            objects in this bucket. Setting this element to TRUE causes the following behavior:   PUT Bucket
            ACL and PUT Object ACL calls fail if the specified ACL is public.   PUT Object calls fail if the
            request includes a public ACL.   PUT Bucket calls fail if the request includes a public ACL.
            Enabling this setting doesn't affect existing policies or ACLs.

        * IgnorePublicAcls (bool, Optional):
            Specifies whether Amazon S3 should ignore public ACLs for this bucket and objects in this
            bucket. Setting this element to TRUE causes Amazon S3 to ignore all public ACLs on this bucket
            and objects in this bucket. Enabling this setting doesn't affect the persistence of any existing
            ACLs and doesn't prevent new public ACLs from being set.

        * BlockPublicPolicy (bool, Optional):
            Specifies whether Amazon S3 should block public bucket policies for this bucket. Setting this
            element to TRUE causes Amazon S3 to reject calls to PUT Bucket policy if the specified bucket
            policy allows public access.  Enabling this setting doesn't affect existing bucket policies.

        * RestrictPublicBuckets (bool, Optional):
            Specifies whether Amazon S3 should restrict public bucket policies for this bucket. Setting this
            element to TRUE restricts access to this bucket to only Amazon Web Service principals and
            authorized users within this account if the bucket has a public policy. Enabling this setting
            doesn't affect previously stored bucket policies, except that public and cross-account access
            within any public bucket policy, including non-public delegation to specific accounts, is
            blocked.

      expected_bucket_owner (str, Optional):
        The account ID of the expected bucket owner. If the bucket is owned by a different account, the request will
        fail with an HTTP 403 (Access Denied) error.

      resource_id (str, Optional):
        Bucket name to identify the resource

    Request Syntax:
        .. code-block:: yaml

          resource_name:
            aws.s3.public_access_block.present:
              - name: string
              - bucket: string
              - public_access_block_configuration: dict
              - expected_bucket_owner: string
              - resource_id: string

    Returns:
      dict[str, Any]

    Examples:
      .. code-block:: yaml

      test-bucket-1232323-public-access-block:
        aws.s3.public_access_block.present:
          - name: test-bucket-1232323-public-access-block
          - bucket: test-bucket-1232323
          - public_access_block_configuration: {"BlockPublicAcls": true, "IgnorePublicAcls": true,
                                                "BlockPublicPolicy": true, "RestrictPublicBuckets": true }
          - expected_bucket_owner: 1234567890
          - resource_id: test-bucket-1232323


    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_id = resource_id if resource_id else bucket
    # fetching old public access block configuration
    old_configuration_ret = await hub.exec.boto3.client.s3.get_public_access_block(
        ctx, Bucket=resource_id
    )
    if old_configuration_ret["result"]:
        old_public_access_block_configuration = old_configuration_ret["ret"][
            "PublicAccessBlockConfiguration"
        ]
        result[
            "old_state"
        ] = hub.tool.aws.s3.conversion_utils.convert_raw_public_access_block_to_present(
            bucket, old_public_access_block_configuration
        )
    elif "NoSuchPublicAccessBlockConfiguration" in str(
        old_configuration_ret["comment"]
    ):
        old_public_access_block_configuration = None
    elif "NoSuchBucket" in str(old_configuration_ret["comment"]):
        old_public_access_block_configuration = None
    else:
        result["comment"] = old_configuration_ret["comment"]
        result["result"] = False
        return result

    # If new public access block configuration is same as old
    if old_public_access_block_configuration == public_access_block_configuration:
        result["new_state"] = copy.deepcopy(result["old_state"])
        result["comment"] += [f"aws.s3.public_access_block '{name}' already exists"]
        return result

    if ctx.get("test", False):
        result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
            enforced_state={},
            desired_state={
                "name": name,
                "bucket": bucket,
                "public_access_block_configuration": public_access_block_configuration,
                "expected_bucket_owner": expected_bucket_owner,
            },
        )
        operation = "create" if not old_public_access_block_configuration else "update"
        result[
            "comment"
        ] = f"Would {operation} aws.s3.public_access_block '{name}' configuration for bucket {bucket}"
        return result

    # create or update the bucket public access block configuration
    ret = await hub.exec.boto3.client.s3.put_public_access_block(
        ctx,
        Bucket=resource_id,
        PublicAccessBlockConfiguration=public_access_block_configuration,
        ExpectedBucketOwner=expected_bucket_owner,
    )

    if not ret["result"]:
        result["comment"] += ret["comment"]
        result["result"] = False
        return result

    # fetching new public access block configuration
    new_configuration_ret = await hub.exec.boto3.client.s3.get_public_access_block(
        ctx, Bucket=resource_id
    )
    result[
        "new_state"
    ] = hub.tool.aws.s3.conversion_utils.convert_raw_public_access_block_to_present(
        bucket, new_configuration_ret["ret"]["PublicAccessBlockConfiguration"]
    )
    operation = "Created" if not old_public_access_block_configuration else "Updated"
    result["comment"] += [f"{operation} aws.s3.public_access_block '{name}'"]
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    expected_bucket_owner: str = None,
) -> Dict[str, Any]:
    """Removes the PublicAccessBlock configuration for an Amazon S3 bucket.

    To use this operation, you must have the s3:PutBucketPublicAccessBlock permission.

    Args:
        name(str):
            The name of public block configuration
        resource_id (str, Optional):
            Bucket name to identify the resource
        expected_bucket_owner (str, Optional):
            The account ID of the expected bucket owner. If the bucket is owned by a different account, the request
            will fail with an HTTP 403 (Access Denied) error.

    Returns:
        dict[str, Any]

    Request Syntax:
        .. code-block:: yaml

            resource_name:
              aws.s3.public_access_block.absent:
                - name: string
                - resource_id: string
                - expected_bucket_owner: string

    Examples:
        .. code-block:: yaml

            test-bucket-1232323-public-access-block:
              aws.s3.public_access_block.absent:
              - name: test-bucket-1232323-public-access-block
              - resource_id: test-bucket-1232323
              - expected_bucket_owner: 1234567890
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.s3.public_access_block", name=name
        )
        return result
    # fetching old public access block configuration
    old_configuration_ret = await hub.exec.boto3.client.s3.get_public_access_block(
        ctx, Bucket=resource_id
    )

    if old_configuration_ret["result"]:
        old_public_access_block_configuration = old_configuration_ret["ret"][
            "PublicAccessBlockConfiguration"
        ]
        result[
            "old_state"
        ] = hub.tool.aws.s3.conversion_utils.convert_raw_public_access_block_to_present(
            resource_id, old_public_access_block_configuration
        )
    elif "NoSuchPublicAccessBlockConfiguration" in str(
        old_configuration_ret["comment"]
    ) or "NoSuchBucket" in str(old_configuration_ret["comment"]):
        result["comment"] += [f"aws.s3.public_access_block '{name}' already absent"]
        return result
    else:
        result["comment"] = old_configuration_ret["comment"]
        result["result"] = False
        return result

    if ctx.get("test", False):
        result[
            "comment"
        ] = f"Would delete aws.s3.public_access_block '{name}' configuration for bucket {resource_id}"
        return result

    ret = await hub.exec.boto3.client.s3.delete_public_access_block(
        ctx, Bucket=resource_id, ExpectedBucketOwner=expected_bucket_owner
    )
    result["result"] = ret["result"]
    if not result["result"]:
        result["comment"] = ret["comment"]
        result["result"] = False
        return result
    result[
        "comment"
    ] = f"Deleted aws.s3.public_access_block '{name}' for bucket '{resource_id}'"

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Obtain S3 public access block configuration for each bucket under the given context for any user.

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.s3.public_access_block
    """
    result = {}
    # To describe the public access block configuration of all the buckets, we first need to list all the buckets, then get the
    # configuration of each bucket
    ret_buckets = await hub.exec.boto3.client.s3.list_buckets(ctx)

    if not ret_buckets["result"]:
        hub.log.warning(f"Could not describe buckets {ret_buckets['comment']}")
        return result

    for bucket in ret_buckets["ret"]["Buckets"]:
        bucket_name = bucket.get("Name")
        resource_name = f"{bucket_name}-public-access-block"
        # get configuration for each bucket
        config_ret = await hub.exec.boto3.client.s3.get_public_access_block(
            ctx, Bucket=bucket_name
        )
        if not config_ret["result"]:
            hub.log.warning(
                f"Could not get public access block configuration for bucket {bucket_name} with error"
                f" {config_ret['comment']} . Describe will skip this bucket and continue."
            )
        else:
            resource_translated = hub.tool.aws.s3.conversion_utils.convert_raw_public_access_block_to_present(
                bucket_name, config_ret["ret"].get("PublicAccessBlockConfiguration")
            )
            result[resource_name] = {
                "aws.s3.public_access_block.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource_translated.items()
                ]
            }
    return result
