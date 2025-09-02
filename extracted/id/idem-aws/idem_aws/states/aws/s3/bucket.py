"""State module for managing AWS S3 buckets."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    acl: str = None,
    create_bucket_configuration: make_dataclass(
        "CreateBucketConfiguration", [("LocationConstraint", str, field(default=None))]
    ) = None,
    grant_full_control: str = None,
    grant_read: str = None,
    grant_read_acp: str = None,
    grant_write: str = None,
    grant_write_acp: str = None,
    object_lock_enabled_for_bucket: bool = None,
    object_ownership: str = None,
    object_lock_configuration: make_dataclass(
        "ObjectLockConfiguration",
        [
            ("ObjectLockEnabled", str, field(default=None)),
            (
                "Rule",
                make_dataclass(
                    "ObjectLockRule",
                    [
                        (
                            "DefaultRetention",
                            make_dataclass(
                                "DefaultRetention",
                                [
                                    ("Mode", str, field(default=None)),
                                    ("Days", int, field(default=None)),
                                    ("Years", int, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        )
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass("Tag", [("Key", str), ("Value", str, field(default=None))])
    ] = None,
) -> Dict[str, Any]:
    """Create an AWS S3 Bucket.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional): AWS S3 Bucket id

        acl(str, Optional):
            The associated acl for this bucket ('private', 'public-read', 'public-read-write', 'authenticated-read').

        create_bucket_configuration(dict[str, Any], Optional):
            The configuration information for the bucket. Defaults to None.
            LocationConstraint (str, Optional): Specifies the Region where the bucket will be created.
            If you don't specify a Region, the bucket is created in the US East (N. Virginia) Region (us-east-1).

        grant_full_control (str, Optional):
            Allows grantee the read, write, read ACP, and write ACP permissions on the bucket.

        grant_read (str, Optional):
            Allows grantee to list the objects in the bucket.

        grant_read_acp (str, Optional):
            Allows grantee to read the bucket ACL.

        grant_write (str, Optional):
            Allows grantee to create new objects in the bucket.
            For the bucket and object owners of existing objects, also allows deletions and overwrites of those objects.

        grant_write_acp (str, Optional):
            Allows grantee to write the ACL for the applicable bucket.

        object_lock_enabled_for_bucket (bool, Optional):
            Specifies whether you want S3 Object Lock to be enabled for the new bucket.

        object_ownership (str, Optional):
            The container element for object ownership for a bucket's ownership controls.

            * BucketOwnerPreferred
                Objects uploaded to the bucket change ownership to the bucket owner if
                the objects are uploaded with the bucket-owner-full-control canned ACL.
            * ObjectWriter
                The uploading account will own the object if the object is uploaded
                with the bucket-owner-full-control canned ACL.
            * BucketOwnerEnforced
                Access control lists (ACLs) are disabled and no longer affect permissions.
                The bucket owner automatically owns and has full control over every object
                in the bucket. The bucket only accepts PUT requests that don't specify an
                ACL or bucket owner full control ACLs, such as the bucket-owner-full-control
                canned ACL or an equivalent form of this ACL expressed in the XML format.

        object_lock_configuration (dict, Optional):
            The Object Lock configuration that you want to apply to the specified bucket.

            * ObjectLockEnabled (str):
                Indicates whether this bucket has an Object Lock configuration enabled. Enable ObjectLockEnabled
                when you apply ObjectLockConfiguration to a bucket.
            * Rule (dict):
                Specifies the Object Lock rule for the specified object. Enable this rule when you apply
                ObjectLockConfiguration to a bucket. Bucket settings require both a mode and a period. The period can
                be either Days or Years but you must select one. You cannot specify Days and Years at the same time.

                * DefaultRetention (dict):
                    The default Object Lock retention mode and period that you want to apply to new objects placed
                    in the specified bucket. Bucket settings require both a mode and a period. The period can be either
                    Days or Years but you must select one. You cannot specify Days and Years at the same time.

                    * Mode (str):
                        The default Object Lock retention mode you want to apply to new objects placed in the specified
                        bucket. Must be used with either Days or Years.
                    * Days (int):
                        The number of days that you want to specify for the default retention period. Must be used with
                        Mode.
                    * Years (int):
                        The number of years that you want to specify for the default retention period. Must be used with
                        Mode.

        tags(dict or list, Optional):
            dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]`` to associate with the AMI.

            * Key (str):
                The key name that can be used to look up or retrieve the associated value. For example,
                Department or Cost Center are common choices.

            * Value (str):
                The value associated with this tag. For example, tags with a key name of Department could have
                values such as Human Resources, Accounting, and Support. Tags with a key name of Cost Center
                might have values that consist of the number associated with the different cost centers in your
                company. Typically, many resources have tags with the same key name but with different values.
                Amazon Web Services always interprets the tag Value as a single string. If you need to store an
                array, you can store comma-separated values in the string. However, you must interpret the value
                in your code.

    Request Syntax:
       .. code-block:: yaml

            [s3-resource-id]:
              aws.s3.bucket.present:
                - name: "string"
                - acl: "private|public-read|public-read-write|authenticated-read"
                - create_bucket_configuration:
                    LocationConstraint: "string"
                - grant_full_control: "string"
                - grant_read: "string"
                - grant_read_acp: "string"
                - grant_write: "string"
                - grant_write_acp: "string"
                - object_lock_enabled_for_bucket: True|False
                - object_ownership: "BucketOwnerPreferred|ObjectWriter|BucketOwnerEnforced"
                - object_lock_configuration:
                    ObjectLockEnabled: "string"
                    Rule:
                      DefaultRetention:
                        Mode: "string"
                        Days: integer
                - tags:
                    - Key: "string"
                      Value: "string"

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            test_bucket-bb7bb32e9533:
              aws.s3.bucket.present:
                - name: "test_bucket-bb7bb32e9533"
                - acl: "private"
                - create_bucket_configuration:
                    LocationConstraint: "sa-east-1"
                - object_lock_enabled_for_bucket: True
                - object_lock_configuration:
                    ObjectLockEnabled: "Enabled"
                    Rule:
                      DefaultRetention:
                        Mode: "GOVERNANCE"
                        Days: 1
                - object_ownership: "BucketOwnerEnforced"
                - tags:
                    - Key: "Name1"
                      Value: "s3-test1"
                    - Key: "Name2"
                      Value: "s3-test2"
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    tags_list = None
    tags_dict = None
    if tags is not None:
        if isinstance(tags, Dict):
            tags_list = hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
            tags_dict = tags
        else:
            tags_list = tags
            tags_dict = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    if resource_id:
        before = await hub.exec.aws.s3.bucket.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["comment"] = before["comment"]
            result["result"] = False
            return result

        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            "aws.s3.bucket", name
        )
        # S3 Object Lock can only be enabled on bucket creation and cannot be enabled on existing buckets.
        # Changed the condition to fix the object_lock_enabled_for_bucket issue. The issue was when we provide
        # object_lock_enabled_for_bucket as false in sls it was creating changes constantly leading to
        # put_object_lock_configuration retry max out exception. The fix is updating the lock configuration only if
        # there is change in rules and does not try to update based on object_lock_enabled_for_bucket flag.
        if (
            object_lock_configuration is not None
            and object_lock_configuration
            != result["old_state"].get("object_lock_configuration", {})
        ):
            if not ctx.get("test", False):
                update_ret = (
                    await hub.exec.boto3.client.s3.put_object_lock_configuration(
                        ctx,
                        Bucket=resource_id,
                        ObjectLockConfiguration=object_lock_configuration,
                    )
                )
                if not update_ret["result"]:
                    result["comment"] = update_ret["comment"]
                    result["result"] = False
                    return result
                result["comment"] += update_ret["comment"]
                result["result"] = update_ret["result"]
                resource_updated = resource_updated or bool(update_ret["ret"])
            else:
                plan_state[
                    "object_lock_enabled_for_bucket"
                ] = object_lock_enabled_for_bucket
                plan_state["object_lock_configuration"] = object_lock_configuration
                result["comment"] = result[
                    "comment"
                ] + hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.s3.bucket", name=name
                )
        if (
            tags_dict is not None
            and not hub.tool.aws.state_comparison_utils.compare_dicts(
                result["old_state"].get("tags"), tags_dict
            )
        ):
            if not ctx.get("test", False):
                update_ret = await hub.exec.boto3.client.s3.put_bucket_tagging(
                    ctx,
                    Bucket=resource_id,
                    Tagging={"TagSet": tags_list},
                )
                result["comment"] += update_ret["comment"]
                result["result"] = update_ret["result"]
                resource_updated = resource_updated or bool(update_ret["ret"])
            else:
                plan_state["tags"] = tags_dict
    else:
        # If there is no 'resource_id' and 'get_resource_only_with_resource_id' is True,
        # the request is to create a new bucket.
        # Since bucket name is unique, we should fail if a bucket with the given name  already exists.
        # However hub.exec.boto3.client.s3.create_bucket() does not fail if one exists with
        # the same name. This check will ensure we fail.
        if hub.OPT.idem.get("get_resource_only_with_resource_id", False):
            already_exists = await hub.exec.aws.s3.bucket.get(
                ctx, name=name, resource_id=name
            )
            if already_exists["result"] and already_exists["ret"]:
                result["comment"] += hub.tool.aws.comment_utils.already_exists_comment(
                    "aws.s3.bucket", name
                ) + [f"Cannot create a new aws.s3.bucket with the same name '{name}'."]

                result["result"] = False
                return result

        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "acl": acl,
                    "name": name,
                    "resource_id": resource_id,
                    "create_bucket_configuration": create_bucket_configuration,
                    "grant_full_control": grant_full_control,
                    "grant_read": grant_read,
                    "grant_read_acp": grant_read_acp,
                    "grant_write": grant_write,
                    "grant_write_acp": grant_write_acp,
                    "object_lock_enabled_for_bucket": object_lock_enabled_for_bucket,
                    "object_ownership": object_ownership,
                    "tags": tags_dict,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.s3.bucket", name=name
            )
            return result

        payload = hub.tool.aws.s3.s3_utils.get_create_bucket_payload(
            acl,
            name,
            create_bucket_configuration,
            grant_full_control,
            grant_read,
            grant_read_acp,
            grant_write,
            grant_write_acp,
            object_lock_enabled_for_bucket,
            object_ownership,
        )
        ret = await hub.exec.boto3.client.s3.create_bucket(ctx, **payload)
        if not ret["result"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.s3.bucket", name=name
        )
        resource_id = name
        if tags_list is not None:
            ret = await hub.exec.boto3.client.s3.put_bucket_tagging(
                ctx,
                Bucket=name,
                Tagging={"TagSet": tags_list},
            )
            if not ret["result"]:
                result["comment"] += ret["comment"]
                result["result"] = False
                return result

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif (not before) or resource_updated:
        get_ret = await hub.exec.aws.s3.bucket.get(
            ctx, name=name, resource_id=resource_id
        )
        result["result"] = get_ret["result"]
        if not get_ret["result"]:
            result["comment"] += get_ret["comment"]
        result["new_state"] = copy.deepcopy(get_ret["ret"])
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Delete the specified s3 bucket.

    Args:
        name(str):
            The Idem name of the s3 bucket.

        resource_id(str, Optional):
            AWS S3 Bucket name.

    Request Syntax:
        .. code-block:: yaml

            idem-name:
              aws.s3.bucket.absent:
                - name: value
                - resource_id: value

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            bucket-5435423646-456464:
              aws.s3.bucket.absent:
                - name: bucket1
                - resource_id: bucket1
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.s3.bucket", name=name
        )
        return result

    before = await hub.exec.aws.s3.bucket.get(
        ctx=ctx, name=name, resource_id=resource_id
    )

    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.s3.bucket", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.s3.bucket", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client.s3.delete_bucket(ctx, Bucket=resource_id)
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.s3.bucket", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the AWS bucket in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        dict[str, dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.s3
    """
    result = {}
    ret = await hub.exec.boto3.client.s3.list_buckets(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe S3 buckets {ret['comment']}")
        return {}

    for bucket in ret["ret"]["Buckets"]:
        resource_id = bucket.get("Name")

        try:
            translated_resource = (
                await hub.tool.aws.s3.conversion_utils.convert_raw_s3_to_present_async(
                    ctx, idem_resource_name=resource_id
                )
            )
        except Exception as e:
            hub.log.warning(
                f"Could not describe s3 bucket '{resource_id}' with error {e}"
            )
            continue

        result[resource_id] = {
            "aws.s3.bucket.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in translated_resource.items()
            ]
        }

    return result
