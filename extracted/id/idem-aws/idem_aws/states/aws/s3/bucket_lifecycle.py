"""State module for managing AWS S3 bucket lifecycle configuration."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

STATE_NAME = "aws.s3.bucket_lifecycle"


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    *,
    bucket: str,
    lifecycle_configuration: make_dataclass(
        "LifecycleConfiguration",
        [
            (
                "Rules",
                List[
                    make_dataclass(
                        "Rules",
                        [
                            ("ID", str),
                            ("Status", str),
                            (
                                "Filter",
                                make_dataclass(
                                    "Filter",
                                    [
                                        ("Prefix", str, field(default=None)),
                                        (
                                            "Tag",
                                            make_dataclass(
                                                "Tag",
                                                [
                                                    ("Key", str),
                                                    ("Value", str),
                                                ],
                                            ),
                                            field(default=None),
                                        ),
                                        (
                                            "ObjectSizeGreaterThan",
                                            int,
                                            field(default=None),
                                        ),
                                        (
                                            "ObjectSizeLessThan",
                                            int,
                                            field(default=None),
                                        ),
                                        (
                                            "And",
                                            make_dataclass(
                                                "And",
                                                [
                                                    (
                                                        "Prefix",
                                                        str,
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "Tag",
                                                        make_dataclass(
                                                            "Tag",
                                                            [
                                                                ("Key", str),
                                                                ("Value", str),
                                                            ],
                                                        ),
                                                        field(default=None),
                                                    ),
                                                ],
                                            ),
                                            field(default=None),
                                        ),
                                    ],
                                ),
                            ),
                            (
                                "Expiration",
                                make_dataclass(
                                    "Expiration",
                                    [
                                        ("Date", str, field(default=None)),
                                        ("Days", int, field(default=None)),
                                        (
                                            "ExpiredObjectDeleteMarker",
                                            bool,
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "Transition",
                                make_dataclass(
                                    "Transition",
                                    [
                                        ("Date", str, field(default=None)),
                                        ("Days", int, field(default=None)),
                                        ("StorageClass", str, field(default=None)),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "NoncurrentVersionTransition",
                                make_dataclass(
                                    "NoncurrentVersionTransition",
                                    [
                                        ("NoncurrentDays", int, field(default=None)),
                                        ("StorageClass", str, field(default=None)),
                                        (
                                            "NewerNoncurrentVersions",
                                            int,
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "NoncurrentVersionExpiration",
                                make_dataclass(
                                    "NoncurrentVersionExpiration",
                                    [
                                        ("NoncurrentDays", int, field(default=None)),
                                        (
                                            "NewerNoncurrentVersions",
                                            int,
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "AbortIncompleteMultipartUpload",
                                make_dataclass(
                                    "AbortIncompleteMultipartUpload",
                                    [("DaysAfterInitiation", int, field(default=None))],
                                ),
                                field(default=None),
                            ),
                        ],
                    )
                ],
            )
        ],
    ) = None,
    timeout: make_dataclass(
        "Timeout",
        [
            (
                "update",
                make_dataclass(
                    "UpdateTimeout",
                    [
                        ("delay", int, field(default=4)),
                        ("max_attempts", int, field(default=30)),
                    ],
                ),
                field(default=None),
            )
        ],
    ) = None,
) -> Dict[str, Any]:
    """Creates a lifecycle configuration for an S3 bucket resource.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            The name of the S3 bucket in Amazon Web Services. It must be equal to the bucket parameter.

        bucket(str):
            The name of the S3 bucket in Amazon Web Services.

        lifecycle_configuration(dict[str, Any], Optional):
            The lifecycle configuration for the S3 bucket. Defaults to None.

            * Rules (list[dict[str, Any]]):
                Specifies lifecycle configuration rules for an Amazon S3 bucket.

                * ID (str):
                    Unique identifier for the rule. The value can't be longer than 255 characters.

                * Status (str):
                    If Enabled, the rule is currently being applied. If Disabled, the rule is not currently being
                    applied.

                * Filter (dict[str, Any]):
                    The Filter is used to identify objects that a Lifecycle Rule applies to. A Filter must have exactly
                    one of Prefix , Tag , or And specified.

                    * Prefix (str, Optional):
                        Prefix identifying one or more objects to which the rule applies.

                    * Tag (dict[str, Any], Optional):
                        This tag must exist in the object's tag set in order for the rule to apply.

                        * Key (str):
                            Name of the object key.
                        * Value (str):
                            Value of the tag.

                    * ObjectSizeGreaterThan (int, Optional):
                        Minimum object size to which the rule applies.

                    * ObjectSizeLessThan (int, Optional):
                        Maximum object size to which the rule applies.

                    * And (dict[str, Any], Optional):
                        This is used in a Lifecycle Rule Filter to apply a logical AND to two or more predicates. The
                        Lifecycle Rule will apply to any object matching all of the predicates configured inside the And
                         operator.

                        * Prefix (str, Optional):
                            Prefix identifying one or more objects to which the rule applies.

                        * Tag (dict[str, Any], Optional):
                            This tag must exist in the object's tag set in order for the rule to apply.

                            * Key (str):
                                Name of the object key.
                            * Value (str):
                                Value of the tag.

                        * ObjectSizeGreaterThan (int, Optional):
                            Minimum object size to which the rule applies.

                        * ObjectSizeLessThan (int, Optional):
                            Maximum object size to which the rule applies.

                * Expiration (dict[str, Any], Optional):
                    Specifies the expiration for the lifecycle of the object.

                    * Date (str, Optional):
                        Indicates at what date the object is to be moved or deleted. Should be in GMT ISO 8601 Format.

                    * Days (int, Optional):
                        Indicates the lifetime, in days, of the objects that are subject to the rule. The value must be
                        a non-zero positive integer.

                    * ExpiredObjectDeleteMarker (bool, Optional):
                        Indicates whether Amazon S3 will remove a delete marker with no noncurrent versions. If set to
                        true, the delete marker will be expired; if set to false the policy takes no action. This cannot
                        be specified with Days or Date in a Lifecycle Expiration Policy.

                * Transition (dict[str, Any], Optional):
                    Specifies when an object transitions to a specified storage class. For more information about
                    Amazon S3 lifecycle configuration rules, see Transitioning Objects Using Amazon S3 Lifecycle in
                    the Amazon S3 User Guide.

                    * Date (str, Optional):
                        Indicates when objects are transitioned to the specified storage class. The date value must be
                        in ISO 8601 format. The time is always midnight UTC.

                    * Days (int, Optional):
                        Indicates the number of days after creation when objects are transitioned to the specified
                        storage class. The value must be a positive integer.

                    * StorageClass (str, Optional):
                        The storage class to which you want the object to transition.

                * NoncurrentVersionTransition (dict[str, Any], Optional):
                    Container for the transition rule that describes when noncurrent objects transition to the
                    STANDARD_IA, ONEZONE_IA, INTELLIGENT_TIERING, GLACIER_IR, GLACIER, or DEEP_ARCHIVE storage
                    class. If your bucket is versioning-enabled (or versioning is suspended), you can set this
                    action to request that Amazon S3 transition noncurrent object versions to the STANDARD_IA,
                    ONEZONE_IA, INTELLIGENT_TIERING, GLACIER_IR, GLACIER, or DEEP_ARCHIVE storage class at a
                    specific period in the object's lifetime.

                    * NoncurrentDays (int, Optional):
                        Specifies the number of days an object is noncurrent before Amazon S3 can perform the associated
                        action. For information about the noncurrent days calculations, see How Amazon S3 Calculates How
                        Long an Object Has Been Noncurrent in the Amazon S3 User Guide.

                    * StorageClass (str, Optional):
                        The class of storage used to store the object.

                    * NewerNoncurrentVersions (int, Optional):
                        Specifies how many noncurrent versions Amazon S3 will retain. If there are this many more recent
                        noncurrent versions, Amazon S3 will take the associated action. For more information about
                        noncurrent versions, see Lifecycle configuration elements in the Amazon S3 User Guide.

                * NoncurrentVersionExpiration (dict[str, Any], Optional):
                    Specifies when noncurrent object versions expire. Upon expiration, Amazon S3 permanently deletes
                    the noncurrent object versions. You set this lifecycle configuration action on a bucket that has
                    versioning enabled (or suspended) to request that Amazon S3 delete noncurrent object versions at
                    a specific period in the object's lifetime.

                    * NoncurrentDays (int, Optional):
                        Specifies the number of days an object is noncurrent before Amazon S3 can perform the associated
                        action. The value must be a non-zero positive integer. For information about the noncurrent days
                        calculations, see How Amazon S3 Calculates When an Object Became Noncurrent in the Amazon S3
                        User Guide.

                    * NewerNoncurrentVersions (int, Optional):
                        Specifies how many noncurrent versions Amazon S3 will retain. If there are this many more recent
                        noncurrent versions, Amazon S3 will take the associated action. For more information about
                        noncurrent versions, see Lifecycle configuration elements in the Amazon S3 User Guide.

                * AbortIncompleteMultipartUpload (dict[str, Any], Optional):
                    Specifies the days since the initiation of an incomplete multipart upload that Amazon S3 will
                    wait before permanently removing all parts of the upload. For more information, see  Aborting
                    Incomplete Multipart Uploads Using a Bucket Lifecycle Policy in the Amazon S3 User Guide.

                    * DaysAfterInitiation (int, Optional):
                        Specifies the number of days after which Amazon S3 aborts an incomplete multipart upload.

        timeout(dict, Optional):
            Timeout configuration for S3 bucket lifecycle configuration.

            * update (str):
                Timeout configuration for updating the S3 bucket lifecycle configuration.

                * delay (int, Optional):
                    The amount of time in seconds to wait between attempts. Defaults to 4 seconds.
                * max_attempts (int, Optional):
                    Maximum attempts of waiting for the update. Defaults to 30 attempts.

    Request Syntax:
        .. code-block:: yaml

            [idem_test_aws_s3_bucket_lifecycle]:
              aws.s3.bucket_lifecycle.present:
                - name: 'str'
                - bucket: 'str'
                - lifecycle_configuration: {'str': []}

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            idem_test_aws_s3_bucket_lifecycle:
              aws.s3.bucket_lifecycle.present:
                - name: value
                - bucket: value
                - lifecycle_configuration:
                    Rules:
                    - ID: 'str'
                      Status: 'Enabled'
                      Filter:
                        Prefix: ''
                      Expiration:
                        Date: datetime(2015, 1, 1)
                        Days: 123
                        ExpiredObjectDeleteMarker: True
                      Transition:
                        Date: datetime(2015, 1, 1)
                        Days: 123
                        StorageClass: 'GLACIER'
                      NoncurrentVersionTransitions:
                        - NoncurrentDays: 123
                          StorageClass: 'GLACIER'
                          NewerNoncurrentVersions: 123
                      NoncurrentVersionExpiration:
                        NoncurrentDays: 123
                        NewerNoncurrentVersions: 123
                      AbortIncompleteMultipartUpload:
                        DaysAfterInitiation: 123
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

        before_ret = await hub.exec.aws.s3.bucket_lifecycle.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before_ret["result"]:
            result["result"] = False
            result["comment"] = before_ret["comment"]
            return result

    if before_ret:
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type=STATE_NAME, name=name
        )
        result["old_state"] = copy.deepcopy(before_ret["ret"])
        result["new_state"] = copy.deepcopy(result["old_state"])

        resource_parameters = {
            "lifecycle_configuration": lifecycle_configuration,
        }

        if hub.tool.aws.s3.bucket_lifecycle.is_bucket_lifecycle_configuration_identical(
            resource_parameters, result["old_state"]
        ):
            # no updates to apply
            return result

        if ctx.get("test", False):
            result["new_state"].update(resource_parameters)
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
                    "lifecycle_configuration": lifecycle_configuration,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type=STATE_NAME, name=name
            )
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type=STATE_NAME, name=name
        )

    put_ret = await hub.exec.boto3.client.s3.put_bucket_lifecycle_configuration(
        ctx,
        Bucket=bucket,
        LifecycleConfiguration=lifecycle_configuration,
    )
    if not put_ret["result"]:
        result["result"] = False
        result["comment"] += put_ret["comment"]
        return result

    wait_for_updates_ret = await hub.tool.aws.s3.bucket_lifecycle.wait_for_updates(
        ctx,
        bucket=bucket,
        lifecycle_configuration=lifecycle_configuration,
        timeout=timeout.get("update") if timeout else None,
    )
    if not wait_for_updates_ret["result"]:
        result["result"] = False
        result["comment"] += wait_for_updates_ret["comment"]
        return result

    after_ret = await hub.exec.aws.s3.bucket_lifecycle.get(
        ctx, name=name, resource_id=bucket
    )
    result["new_state"] = copy.deepcopy(after_ret["ret"])

    return result


async def absent(
    hub, ctx, name: str, resource_id: str = None, timeout: Dict = None
) -> Dict[str, Any]:
    """Deletes a lifecycle configuration from an S3 bucket resource.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            The name of the S3 bucket in Amazon Web Services.
            Idem automatically considers this resource being absent if this field is not specified.

        timeout(dict, Optional):
            Timeout configuration for S3 bucket lifecycle configuration.

            * delete (str):
                Timeout configuration for deleting the S3 bucket lifecycle configuration.

                * delay (int, Optional):
                    The amount of time in seconds to wait between attempts. Defaults to 4 seconds.

                * max_attempts (int, Optional):
                    Maximum attempts of waiting for the deletion. Defaults to 30 attempts.

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            idem_test_aws_s3_bucket_lifecycle:
              aws.s3.bucket_lifecycle.absent:
                - name: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type=STATE_NAME, name=name
        )
        return result

    before_ret = await hub.exec.aws.s3.bucket_lifecycle.get(
        ctx, name=name, resource_id=resource_id
    )
    if not before_ret["result"]:
        if "NoSuchLifecycleConfiguration" in str(
            before_ret["comment"][0]
        ) or "NoSuchBucket" in str(before_ret["comment"]):
            result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
                resource_type=STATE_NAME, name=name
            )
        else:
            result["result"] = False
            result["comment"] = before_ret["comment"]
        return result
    elif not before_ret["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type=STATE_NAME, name=name
        )
        return result
    result["old_state"] = before_ret["ret"]

    if ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type=STATE_NAME, name=name
        )
        return result

    delete_ret = await hub.exec.boto3.client.s3.delete_bucket_lifecycle(
        ctx, Bucket=resource_id
    )
    if not delete_ret["result"]:
        result["result"] = False
        result["comment"] = delete_ret["comment"]
        return result

    wait_for_delete_ret = await hub.tool.aws.s3.bucket_lifecycle.wait_for_delete(
        ctx,
        bucket=resource_id,
        timeout=timeout.get("delete") if timeout else None,
    )
    if not wait_for_delete_ret["result"]:
        result["result"] = False
        result["comment"] = wait_for_delete_ret["comment"]
        return result

    result["comment"] = hub.tool.aws.comment_utils.delete_comment(
        resource_type=STATE_NAME, name=name
    )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Gets the lifecycle configuration for each S3 bucket under the given AWS account.

    Returns:
        dict[str, dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.s3.bucket_lifecycle
    """
    result = {}

    list_buckets_ret = await hub.exec.boto3.client.s3.list_buckets(ctx)
    if not list_buckets_ret["result"]:
        hub.log.warning(f"Could not list S3 buckets: {list_buckets_ret['comment']}")
        return result

    for bucket in list_buckets_ret["ret"]["Buckets"]:
        bucket_name = bucket.get("Name")

        get_bucket_lifecycle_ret = (
            await hub.exec.boto3.client.s3.get_bucket_lifecycle_configuration(
                ctx, Bucket=bucket_name
            )
        )
        if not get_bucket_lifecycle_ret["result"]:
            if "NoSuchLifecycleConfiguration" not in str(
                get_bucket_lifecycle_ret["comment"][0]
            ):
                hub.log.debug(
                    f"Could not get lifecycle configuration for S3 bucket '{bucket_name}': "
                    f"{get_bucket_lifecycle_ret['comment']}. Describe will skip this S3 bucket and continue."
                )
            continue

        resource_translated = (
            hub.tool.aws.s3.bucket_lifecycle.convert_raw_bucket_lifecycle_to_present(
                bucket=bucket_name,
                raw_resource=get_bucket_lifecycle_ret["ret"],
            )
        )

        result[resource_translated["name"]] = {
            f"{STATE_NAME}.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result
