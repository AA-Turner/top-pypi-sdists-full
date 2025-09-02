"""State module for managing AWS S3 bucket versioning configuration."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]

STATE_NAME = "aws.s3.bucket_versioning"


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    *,
    bucket: str,
    mfa_delete: str = "Disabled",
    status: str = "Enabled",
) -> Dict[str, Any]:
    """Creates a versioning configuration for an S3 bucket resource.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            The name of the S3 bucket in Amazon Web Services. It must be equal to the bucket parameter.

        bucket(str):
            The name of the S3 bucket in Amazon Web Services.

        mfa_delete(str, Optional):
            The versioning state of the bucket. Defaults to "Disabled".

        status(str, Optional):
            Specifies whether MFA delete is enabled in the bucket versioning configuration. Defaults to "Enabled".

    Request Syntax:
        .. code-block:: yaml

            [idem_test_aws_s3_bucket_versioning]:
              aws.s3.bucket_versioning.present:
                - name: 'string'
                - bucket: 'string'
                - mfa_delete: 'string'
                - status: 'string'

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            idem_test_aws_s3_bucket_versioning:
              aws.s3.bucket_versioning.present:
                - name: value
                - bucket: value
                - mfa_delete: 'Enabled'
                - status: 'Enabled'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    before_ret = None

    if resource_id:
        if resource_id != bucket:
            result["result"] = False
            result["comment"] += [
                f"Bucket '{bucket}' and resource_id '{resource_id}' parameters must be the same"
            ]
            return result

        before_ret = await hub.exec.boto3.client.s3.get_bucket_versioning(
            ctx, Bucket=resource_id
        )
        if not before_ret["result"]:
            result["result"] = False
            result["comment"] = before_ret["comment"]
            return result

    if before_ret:
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type=STATE_NAME, name=name
        )
        result[
            "old_state"
        ] = hub.tool.aws.s3.bucket_versioning.convert_raw_bucket_versioning_to_present(
            bucket=resource_id,
            raw_resource=before_ret.get("ret"),
            idem_resource_name=name,
        )
        result["new_state"] = copy.deepcopy(result["old_state"])

        if mfa_delete == result["old_state"].get("mfa_delete") and status == result[
            "old_state"
        ].get("status"):
            # no updates to apply
            return result

        if ctx.get("test", False):
            result["new_state"]["mfa_delete"] = mfa_delete
            result["new_state"]["status"] = status
            result["comment"] = result[
                "comment"
            ] + hub.tool.aws.comment_utils.would_update_comment(
                resource_type=STATE_NAME, name=name
            )
            return result
        else:
            result["comment"] = result[
                "comment"
            ] + hub.tool.aws.comment_utils.update_comment(
                resource_type=STATE_NAME, name=name
            )
    else:
        if ctx.get("test", False):
            result[
                "new_state"
            ] = raw_resource = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "bucket": bucket,
                    "mfa_delete": mfa_delete,
                    "status": status,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type=STATE_NAME, name=name
            )
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type=STATE_NAME, name=name
        )

    put_bucket_versioning_ret = await hub.exec.boto3.client.s3.put_bucket_versioning(
        ctx,
        Bucket=bucket,
        VersioningConfiguration={
            "MFADelete": mfa_delete,
            "Status": status,
        },
    )
    if not put_bucket_versioning_ret["result"]:
        result["result"] = False
        result["comment"] += put_bucket_versioning_ret["comment"]
        return result

    after_ret = await hub.exec.boto3.client.s3.get_bucket_versioning(ctx, Bucket=bucket)
    if not after_ret["result"]:
        result["result"] = False
        result["comment"] += after_ret["comment"]
        return result

    result[
        "new_state"
    ] = hub.tool.aws.s3.bucket_versioning.convert_raw_bucket_versioning_to_present(
        bucket=bucket, raw_resource=after_ret.get("ret"), idem_resource_name=name
    )

    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Suspends a versioning configuration for an S3 bucket resource.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            The name of the S3 bucket in Amazon Web Services. Idem automatically considers this resource being absent if this field is not specified.

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            idem_test_aws_s3_bucket_versioning:
              aws.s3.bucket_versioning.absent:
                - name: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type=STATE_NAME, name=name
        )
        return result

    before_ret = await hub.exec.boto3.client.s3.get_bucket_versioning(
        ctx, Bucket=resource_id
    )
    if not before_ret["result"]:
        if "NoSuchBucket" in str(before_ret["comment"]):
            result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
                resource_type=STATE_NAME, name=name
            )
            return result
        result["result"] = False
        result["comment"] = before_ret["comment"]
        return result

    if (
        before_ret["ret"].get("MFADelete", "Disabled") == "Disabled"
        and before_ret["ret"].get("Status", "Suspended") == "Suspended"
    ):
        result["comment"] += [f"{STATE_NAME} '{name}' already suspended"]
        return result

    result[
        "old_state"
    ] = hub.tool.aws.s3.bucket_versioning.convert_raw_bucket_versioning_to_present(
        bucket=resource_id, raw_resource=before_ret["ret"], idem_resource_name=name
    )

    mfa_delete = "Disabled"
    status = "Suspended"

    if ctx.get("test", False):
        result["new_state"] = copy.deepcopy(result["old_state"])
        result["new_state"]["mfa_delete"] = mfa_delete
        result["new_state"]["status"] = status
        result["comment"] += [f"Would suspend {STATE_NAME} '{name}'"]
        return result

    put_bucket_versioning_ret = await hub.exec.boto3.client.s3.put_bucket_versioning(
        ctx,
        Bucket=resource_id,
        VersioningConfiguration={
            "MFADelete": mfa_delete,
            "Status": status,
        },
    )
    if not put_bucket_versioning_ret["result"]:
        result["result"] = False
        result["comment"] = put_bucket_versioning_ret["comment"]
        return result

    after_ret = await hub.exec.boto3.client.s3.get_bucket_versioning(
        ctx, Bucket=resource_id
    )
    if not after_ret["result"]:
        result["result"] = False
        result["comment"] = after_ret["comment"]
        return result

    result[
        "new_state"
    ] = hub.tool.aws.s3.bucket_versioning.convert_raw_bucket_versioning_to_present(
        bucket=resource_id, raw_resource=after_ret["ret"], idem_resource_name=name
    )

    result["comment"] += [f"{STATE_NAME} '{name}' suspended"]
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Gets the versioning configuration for each S3 bucket under the given AWS account.

    Returns:
        dict[str, dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.s3.bucket_versioning
    """
    result = {}

    list_buckets_ret = await hub.exec.boto3.client.s3.list_buckets(ctx)
    if not list_buckets_ret["result"]:
        hub.log.warning(f"Could not list S3 buckets: {list_buckets_ret['comment']}")
        return result

    for bucket in list_buckets_ret["ret"]["Buckets"]:
        bucket_name = bucket.get("Name")

        get_bucket_versioning_ret = (
            await hub.exec.boto3.client.s3.get_bucket_versioning(
                ctx, Bucket=bucket_name
            )
        )
        if not get_bucket_versioning_ret["result"]:
            hub.log.debug(
                f"Could not get versioning configuration for S3 bucket '{bucket_name}': "
                f"{get_bucket_versioning_ret['comment']}. Describe will skip this S3 bucket and continue."
            )
            continue

        get_bucket_versioning_ret["ret"].pop("ResponseMetadata", None)

        if get_bucket_versioning_ret["ret"]:
            resource_translated = hub.tool.aws.s3.bucket_versioning.convert_raw_bucket_versioning_to_present(
                bucket=bucket_name,
                raw_resource=get_bucket_versioning_ret["ret"],
            )

            result[resource_translated["name"]] = {
                f"{STATE_NAME}.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource_translated.items()
                ]
            }
        else:
            hub.log.debug(
                f"Versioning configuration is not present for S3 bucket '{bucket_name}'. Describe will skip this S3 bucket and continue."
            )

    return result
