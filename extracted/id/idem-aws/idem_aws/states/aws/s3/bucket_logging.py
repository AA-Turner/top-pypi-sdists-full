"""State module for managing S3 bucket's logging parameters."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List


__contracts__ = ["resource"]

TREQ = {
    "present": {"require": ["aws.s3.bucket.present"]},
}


async def present(
    hub,
    ctx,
    name: str,
    bucket_logging_status: make_dataclass(
        "BucketLoggingStatus",
        [
            (
                "LoggingEnabled",
                make_dataclass(
                    "LoggingEnabled",
                    [
                        ("TargetBucket", str),
                        ("TargetPrefix", str),
                        (
                            "TargetGrants",
                            List[
                                make_dataclass(
                                    "TargetGrant",
                                    [
                                        (
                                            "Grantee",
                                            make_dataclass(
                                                "Grantee",
                                                [
                                                    ("Type", str),
                                                    (
                                                        "DisplayName",
                                                        str,
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "EmailAddress",
                                                        str,
                                                        field(default=None),
                                                    ),
                                                    ("ID", str, field(default=None)),
                                                    ("URI", str, field(default=None)),
                                                ],
                                            ),
                                            field(default=None),
                                        ),
                                        ("Permission", str, field(default=None)),
                                    ],
                                )
                            ],
                            field(default=None),
                        ),
                    ],
                ),
                field(default=None),
            )
        ],
    ),
    resource_id: str = None,
) -> Dict[str, Any]:
    """Create/Update the logging parameter for S3 bucket.

    Set the logging parameters for a bucket and to specify permissions for who can view and modify the logging
    parameters. All logs are saved to bucket in the same Amazon Web Services Region as the source bucket. To set
    the logging status of a bucket, you must be the bucket owner. The bucket owner is automatically granted
    FULL_CONTROL to all logs. You use the Grantee request element to grant access to other people. The Permissions
    request element specifies the kind of access the grantee has to the logs.

    Args:
        name(str):
            An Idem name of the resource.
            This is also used as the name of the bucket for which to set the logging parameters during resource creation.

        resource_id(str, Optional):
            Name of the S3 bucket.

        bucket_logging_status(dict):
            Container for logging status information.

            * LoggingEnabled (dict, Optional):
                Describes where logs are stored and the prefix that Amazon S3 assigns to all log object keys for a bucket.

                * TargetBucket (str):
                    Specifies the bucket where you want Amazon S3 to store server access logs.
                    You can have your logs delivered to any bucket that you own, including the same bucket that is being
                    logged. You can also configure multiple buckets to deliver their logs to the same target bucket.
                    In this case, you should choose a different TargetPrefix for each source bucket so that the delivered
                    log files can be distinguished by key.

                * TargetGrants (list, Optional):
                    Container for granting information.
                    Buckets that use the bucket owner enforced setting for Object Ownership don't support target grants.

                    * Grantee (dict, Optional):
                        Container for the person being granted permissions.

                        * DisplayName (str, Optional):
                            Screen name of the grantee.

                        * EmailAddress (str, Optional):
                            Email address of the grantee.

                        * ID (str, Optional):
                            The canonical user ID of the grantee.

                        * Type (str):
                            Type of grantee.

                        * URI (str, Optional):
                            URI of the grantee group.

                    * Permission (str, Optional):
                        Logging permissions assigned to the grantee for the bucket.

                * TargetPrefix (str):
                    A prefix for all log object keys. If you store log files from multiple Amazon S3 buckets in a
                    single bucket, you can use a prefix to distinguish which log files came from which bucket.

    Request Syntax:
        .. code-block:: yaml

            [bucket_name]-logging:
              aws.s3.bucket_logging.present:
              - name: "string"
              - resource_id: "string"
              - bucket_logging_status:
                  LoggingEnabled:
                    TargetBucket: "string"
                    TargetGrants:
                    - Grantee:
                        DisplayName: [string]
                        EmailAddress: [string]
                        ID: [string]
                        Type: [string]
                        URI: [string]
                      Permission: [string]
                    TargetPrefix: [string]

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            test-bucket-logging:
              aws.s3.bucket_logging.present:
                - name: test-bucket
                - bucket_logging_status:
                    LoggingEnabled:
                        TargetBucket: test-bucket
                        TargetGrants:
                        - Grantee:
                            URI: http://acs.amazonaws.com/groups/s3/LogDelivery
                            Type: Group
                          Permission: WRITE
                        - Grantee:
                            URI: http://acs.amazonaws.com/groups/s3/LogDelivery
                            Type: Group
                          Permission: READ_ACP
                        TargetPrefix: logs
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False

    if resource_id:
        before = await hub.exec.aws.s3.bucket_logging.get(
            ctx, resource_id=resource_id, name=name
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.s3.bucket_logging", name=name
        )
        result["old_state"] = copy.deepcopy(before["ret"])
        result["new_state"] = copy.deepcopy(result["old_state"])

        update_ret = await hub.tool.aws.s3.bucket_logging.update(
            ctx,
            resource_id=resource_id,
            before=before["ret"],
            bucket_logging_status=bucket_logging_status,
        )
        result["comment"] += update_ret["comment"]
        if not update_ret["result"]:
            result["result"] = False
            return result

        resource_updated = resource_updated or bool(update_ret["ret"])
        if update_ret["ret"] and ctx.get("test", False):
            result["new_state"].update(update_ret["ret"])
            result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.s3.bucket_logging", name=name
            )
        if resource_updated and ctx.get("test", False):
            return result
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_id": name,
                    "bucket_logging_status": bucket_logging_status,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.s3.bucket_logging", name=name
            )
            return result
        create_ret = await hub.exec.boto3.client.s3.put_bucket_logging(
            ctx, Bucket=name, BucketLoggingStatus=bucket_logging_status
        )
        if not create_ret["result"]:
            result["result"] = False
            result["comment"] = create_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.s3.bucket_logging", name=name
        )
        resource_id = name

    if (not result["old_state"]) or resource_updated:
        after_ret = await hub.exec.aws.s3.bucket_logging.get(
            ctx, name=name, resource_id=resource_id
        )
        if not after_ret["result"] or not after_ret["ret"]:
            result["result"] = False
            result["comment"] += after_ret["comment"]
            return result
        result["new_state"] = after_ret["ret"]

    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes the logging configuration for an S3 bucket.

    This action enables you to delete logging configurations from a bucket using a single HTTP request.
    If you know the object keys that you want to delete, then this action provides a suitable alternative to sending
    individual delete requests, reducing per-request overhead. For each configuration, Amazon S3 performs a delete
    action and returns the result of that delete, success, or failure, in the response.

    Args:
        name(str):
            Idem name of the bucket.

        resource_id(str):
            Name of the bucket on which logging needs to be deleted.

    Request Syntax:
        .. code-block:: yaml

            [bucket_name]-logging:
              aws.s3.bucket_logging.absent:
                - name: "string"
                - resource_id: "string"

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            test-bucket-logging:
              aws.s3.bucket_logging.absent:
                - name: test-bucket
                - resource_id: test-bucket
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.s3.bucket_logging", name=name
        )
        return result

    before = await hub.exec.aws.s3.bucket_logging.get(
        ctx, name=name, resource_id=resource_id
    )
    if not before["result"]:
        if "NoSuchBucket" in str(before["comment"]):
            result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
                resource_type="aws.s3.bucket_logging", name=name
            )
            return result
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.s3.bucket_logging", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.s3.bucket_logging", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        delete_ret = await hub.exec.boto3.client.s3.put_bucket_logging(
            ctx, Bucket=resource_id, BucketLoggingStatus={}
        )
        if not delete_ret["result"]:
            result["result"] = False
            result["comment"] = delete_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.s3.bucket_logging", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Gets information about the S3 bucket logging parameters.

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        dict[str, dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.s3.bucket_logging

    """
    result = {}
    # To describe the logging configurations of all the buckets, we first need to list all the buckets,
    # then get the logging configurations of each bucket
    ret = await hub.exec.boto3.client.s3.list_buckets(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe S3 buckets {ret['comment']}")
        return {}

    for bucket in ret["ret"]["Buckets"]:
        bucket_name = bucket.get("Name")
        # get logging configuration for each bucket
        bucket_logging_response = await hub.exec.boto3.client.s3.get_bucket_logging(
            ctx, Bucket=bucket_name
        )
        if bucket_logging_response["result"]:
            if (
                bucket_logging_response["ret"]
                and "LoggingEnabled" in bucket_logging_response["ret"]
            ):
                bucket_logging_response["ret"].pop("ResponseMetadata", None)
                translated_resource = hub.tool.aws.s3.conversion_utils.convert_raw_bucket_logging_to_present(
                    ctx=ctx,
                    raw_resource=bucket_logging_response["ret"],
                    bucket_name=bucket_name,
                )

                result[bucket_name + "-logging"] = {
                    "aws.s3.bucket_logging.present": [
                        {parameter_key: parameter_value}
                        for parameter_key, parameter_value in translated_resource.items()
                    ]
                }
    return result
