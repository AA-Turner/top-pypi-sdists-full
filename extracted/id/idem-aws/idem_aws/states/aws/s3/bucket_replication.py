"""State module for managing S3 bucket's replication configurations."""
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
    role: str,
    rules: List[
        make_dataclass(
            "ReplicationRule",
            [
                ("Status", str),
                (
                    "Destination",
                    make_dataclass(
                        "Destination",
                        [
                            ("Bucket", str),
                            ("Account", str, field(default=None)),
                            ("StorageClass", str, field(default=None)),
                            (
                                "AccessControlTranslation",
                                make_dataclass(
                                    "AccessControlTranslation",
                                    [("Owner", str)],
                                ),
                                field(default=None),
                            ),
                            (
                                "EncryptionConfiguration",
                                make_dataclass(
                                    "EncryptionConfiguration",
                                    [
                                        (
                                            "ReplicaKmsKeyID",
                                            str,
                                            field(default=None),
                                        )
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "ReplicationTime",
                                make_dataclass(
                                    "ReplicationTime",
                                    [
                                        ("Status", str),
                                        (
                                            "Time",
                                            make_dataclass(
                                                "ReplicationTimeValue",
                                                [
                                                    (
                                                        "Minutes",
                                                        int,
                                                        field(default=None),
                                                    )
                                                ],
                                            ),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "Metrics",
                                make_dataclass(
                                    "Metrics",
                                    [
                                        ("Status", str),
                                        (
                                            "EventThreshold",
                                            "ReplicationTimeValue",
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                        ],
                    ),
                ),
                ("ID", str, field(default=None)),
                ("Priority", int, field(default=None)),
                ("Prefix", str, field(default=None)),
                (
                    "Filter",
                    make_dataclass(
                        "ReplicationRuleFilter",
                        [
                            ("Prefix", str, field(default=None)),
                            (
                                "Tag",
                                make_dataclass("Tag", [("Key", str), ("Value", str)]),
                                field(default=None),
                            ),
                            (
                                "And",
                                make_dataclass(
                                    "ReplicationRuleAndOperator",
                                    [
                                        (
                                            "Prefix",
                                            str,
                                            field(default=None),
                                        ),
                                        (
                                            "Tags",
                                            List["Tag"],
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "SourceSelectionCriteria",
                    make_dataclass(
                        "SourceSelectionCriteria",
                        [
                            (
                                "SseKmsEncryptedObjects",
                                make_dataclass(
                                    "SseKmsEncryptedObjects",
                                    [("Status", str)],
                                ),
                                field(default=None),
                            ),
                            (
                                "ReplicaModifications",
                                make_dataclass(
                                    "ReplicaModifications",
                                    [("Status", str)],
                                ),
                                field(default=None),
                            ),
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "ExistingObjectReplication",
                    make_dataclass("ExistingObjectReplication", [("Status", str)]),
                    field(default=None),
                ),
                (
                    "DeleteMarkerReplication",
                    make_dataclass(
                        "DeleteMarkerReplication",
                        [("Status", str, field(default=None))],
                    ),
                    field(default=None),
                ),
            ],
        )
    ],
    resource_id: str = None,
) -> Dict[str, Any]:
    """Create/Update the replication configuration for S3 bucket.

    Creates a replication configuration or replaces an existing one. Specify the replication configuration in the
    request body. In the replication configuration, you provide the name of the destination bucket or buckets where you
    want Amazon S3 to replicate objects, the IAM role that Amazon S3 can assume to replicate objects on your behalf,
    and other relevant information. A replication configuration must include at least one rule, and can contain a
    maximum of 1,000. Each rule identifies a subset of objects to replicate by filtering the objects in the source bucket.
    To choose additional subsets of objects to replicate, add a rule for each subset. To specify a subset of the objects in
    the source bucket to apply a replication rule to, add the Filter element as a child of the Rule element. You can
    filter objects based on an object key prefix, one or more object tags, or both.

    Args:
        name(str):
            An Idem name of the resource.
            This is also used as the name of the bucket on which replication needs to be configured.

        resource_id(str, Optional):
            Name of the S3 bucket.

        role (str):
            The Amazon Resource Name (ARN) of the Identity and Access Management (IAM) role that Amazon S3
            assumes when replicating objects.

        rules (list):
            A container for one or more replication rules. A replication configuration must have at least
            one rule and can contain a maximum of 1,000 rules.

            * ID (str, Optional):
                A unique identifier for the rule. The maximum value is 255 characters.

            * Priority (int, Optional):
                The priority indicates which rule has precedence whenever two or more replication rules
                conflict. Amazon S3 will attempt to replicate objects according to all replication rules.
                However, if there are two or more rules with the same destination bucket, then objects will be
                replicated according to the rule with the highest priority. The higher the number, the higher
                the priority.

            * Prefix (str, Optional):
                An object key name prefix that identifies the object or objects to which the rule applies. The
                maximum prefix length is 1,024 characters. To include all objects in a bucket, specify an empty
                string. Replacement must be made for object keys containing special characters (such as
                carriage returns) when using XML requests.

            * Filter (dict, Optional):
                A filter that identifies the subset of objects to which the replication rule applies. A Filter
                must specify exactly one Prefix, Tag, or an And child element.

                * Prefix (str, Optional):
                    An object key name prefix that identifies the subset of objects to which the rule applies.
                    Replacement must be made for object keys containing special characters (such as carriage
                    returns) when using XML requests.

                * Tag (dict, Optional):
                    A container for specifying a tag key and value.  The rule applies only to objects that have the
                    tag in their tag set.

                    * Key (str):
                        Name of the object key.

                    * Value (str):
                        Value of the tag.

                * And (dict, Optional):
                    A container for specifying rule filters. The filters determine the subset of objects to which
                    the rule applies. This element is required only if you specify more than one filter. For
                    example: If you specify both a Prefix and a Tag filter, wrap these filters in an And tag.
                    If you specify a filter based on multiple tags, wrap the Tag elements in an And tag.

                    * Prefix (str, Optional):
                        An object key name prefix that identifies the subset of objects to which the rule applies.

                    * Tags (list, Optional):
                        An array of tags containing key and value pairs.
            * Status (str):
                Specifies whether the rule is enabled.

            * SourceSelectionCriteria (dict, Optional):
                A container that describes additional filters for identifying the source objects that you want
                to replicate. You can choose to enable or disable the replication of these objects. Currently,
                Amazon S3 supports only the filter that you can specify for objects created with server-side
                encryption using a customer managed key stored in Amazon Web Services Key Management Service
                (SSE-KMS).

                * SseKmsEncryptedObjects (dict, Optional):
                    A container for filter information for the selection of Amazon S3 objects encrypted with Amazon
                    Web Services KMS. If you include SourceSelectionCriteria in the replication configuration, this
                    element is required.

                    * Status (str):
                        Specifies whether Amazon S3 replicates objects created with server-side encryption using an
                        Amazon Web Services KMS key stored in Amazon Web Services Key Management Service.

                * ReplicaModifications (dict, Optional):
                    A filter that you can specify for selections for modifications on replicas. Amazon S3 doesn't
                    replicate replica modifications by default. In the latest version of replication configuration
                    (when Filter is specified), you can specify this element and set the status to Enabled to
                    replicate modifications on replicas. If you don't specify the Filter element, Amazon S3
                    assumes that the replication configuration is the earlier version, V1. In the earlier version,
                    this element is not allowed

                    * Status (str):
                        Specifies whether Amazon S3 replicates modifications on replicas.

            * ExistingObjectReplication (dict, Optional):

                * Status (str):

            * Destination (dict[str, Any]):
                A container for information about the replication destination and its configurations including
                enabling the S3 Replication Time Control (S3 RTC).

                * Bucket (str):  The Amazon Resource Name (ARN) of the bucket where you want Amazon S3 to store the results.

                * Account (str, Optional):
                    Destination bucket owner account ID. In a cross-account scenario, if you direct Amazon S3 to
                    change replica ownership to the Amazon Web Services account that owns the destination bucket by
                    specifying the AccessControlTranslation property, this is the account ID of the destination
                    bucket owner.

                * StorageClass (str, Optional):
                    The storage class to use when replicating objects, such as S3 Standard or reduced redundancy.
                    By default, Amazon S3 uses the storage class of the source object to create the object replica.

                * AccessControlTranslation (dict, Optional):
                    Specify this only in a cross-account scenario (where source and destination bucket owners are
                    not the same), and you want to change replica ownership to the Amazon Web Services account that
                    owns the destination bucket. If this is not specified in the replication configuration, the
                    replicas are owned by same Amazon Web Services account that owns the source object.

                    * Owner (str):
                        Specifies the replica ownership.

                * EncryptionConfiguration (dict, Optional):
                    A container that provides information about encryption. If SourceSelectionCriteria is specified,
                    you must specify this element.

                    * ReplicaKmsKeyID (str, Optional):
                        Specifies the ID (Key ARN or Alias ARN) of the customer managed Amazon Web Services KMS key
                        stored in Amazon Web Services Key Management Service (KMS) for the destination bucket. Amazon S3
                        uses this key to encrypt replica objects. Amazon S3 only supports symmetric, customer managed
                        KMS keys.

                * ReplicationTime (dict, Optional):
                    A container specifying S3 Replication Time Control (S3 RTC), including whether S3 RTC is
                    enabled and the time when all objects and operations on objects must be replicated. Must be
                    specified together with a Metrics block.

                    * Status (str):
                        Specifies whether the replication time is enabled.

                    * Time (dict):
                        A container specifying the time by which replication should be complete for all objects and
                        operations on objects.

                        * Minutes (int, Optional):
                            Contains an integer specifying time in minutes.   Valid value: 15

                * Metrics (dict, Optional):
                    A container specifying replication metrics-related settings enabling replication metrics and
                    events.

                    * Status (str):
                        Specifies whether the replication metrics are enabled.

                    * EventThreshold ('ReplicationTimeValue', Optional):
                        A container specifying the time threshold for emitting the s3:Replication:OperationMissedThreshold event.

            * DeleteMarkerReplication (dict, Optional):
                Specifies whether Amazon S3 replicates delete markers. If you specify a Filter in your
                replication configuration, you must also include a DeleteMarkerReplication element. If your
                Filter includes a Tag element, the DeleteMarkerReplication Status must be set to Disabled,
                because Amazon S3 does not support replicating delete markers for tag-based rules. For an
                example configuration, see Basic Rule Configuration.  For more information about delete marker
                replication, see Basic Rule Configuration.   If you are using an earlier version of the
                replication configuration, Amazon S3 handles replication of delete markers differently.

                * Status (str, Optional):
                    Indicates whether to replicate delete markers.  Indicates whether to replicate delete markers.

    Request Syntax:
        .. code-block:: yaml

            [bucket_name]-replication:
              aws.s3.bucket_replication.present:
              - name: "string"
              - resource_id: "string"
              - replication_configuration:
                Role: "string"
                Rules:
                - DeleteMarkerReplication:
                    Status: "string"
                  Destination:
                    Bucket: "string"
                    EncryptionConfiguration:
                      ReplicaKmsKeyID: "string"
                    StorageClass: "string"
                  Filter:
                    And:
                      Prefix: "string"
                      Tags:
                      - Key: "string"
                        Value: "string"
                  ID: "string"
                  Priority: "int"
                  SourceSelectionCriteria:
                    SseKmsEncryptedObjects:
                      Status: "string"
                  Status: "string"

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            resource_is_present:
              aws.s3.bucket_replication.present:
                - name: replication-test-bucket
                - replication_configuration:
                    Role: arn:aws:iam::460671877902:role/admin
                    Rules:
                    - DeleteMarkerReplication:
                        Status: Disabled
                      Destination:
                        Bucket: arn:aws:s3:::replication-bucket-demo-1
                        EncryptionConfiguration:
                          ReplicaKmsKeyID: arn:aws:kms:us-east-1:460671877902:alias/aws/s3
                        StorageClass: STANDARD
                      Filter:
                        And:
                          Prefix: logx
                          Tags:
                          - Key: name
                            Value: replication
                      ID: rule-1
                      Priority: 0
                      SourceSelectionCriteria:
                        SseKmsEncryptedObjects:
                          Status: Enabled
                      Status: Enabled
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False

    if resource_id:
        before = await hub.exec.aws.s3.bucket_replication.get(
            ctx, resource_id=resource_id, name=name
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.s3.bucket_replication", name=name
        )
        result["old_state"] = copy.deepcopy(before["ret"])
        result["new_state"] = copy.deepcopy(result["old_state"])

        update_ret = await hub.tool.aws.s3.bucket_replication.update(
            ctx,
            resource_id=resource_id,
            before=before["ret"],
            role=role,
            rules=rules,
        )
        result["comment"] += update_ret["comment"]
        if not update_ret["result"]:
            result["result"] = False
            return result

        resource_updated = resource_updated or bool(update_ret["ret"])
        if update_ret["ret"] and ctx.get("test", False):
            result["new_state"].update(update_ret["ret"])
            result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.s3.bucket_replication", name=name
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
                    "role": role,
                    "rules": rules,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.s3.bucket_replication", name=name
            )
            return result
        payload = {"Role": role, "Rules": rules}
        create_ret = await hub.exec.boto3.client.s3.put_bucket_replication(
            ctx, Bucket=name, ReplicationConfiguration=payload
        )
        if not create_ret["result"]:
            result["result"] = False
            result["comment"] = create_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.s3.bucket_replication", name=name
        )
        resource_id = name

    if (not result["old_state"]) or resource_updated:
        after_ret = await hub.exec.aws.s3.bucket_replication.get(
            ctx, name=name, resource_id=resource_id
        )
        if not after_ret["result"] or not after_ret["ret"]:
            result["result"] = False
            result["comment"] += tuple(after_ret["comment"])
            return result
        result["new_state"] = after_ret["ret"]

    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Deletes the replication configuration for an S3 bucket.

    Deletes the replication configuration from the bucket. To use this operation, you must have permissions to
    perform the s3:PutReplicationConfiguration action. The bucket owner has these permissions by default and can
    grant it to others. It can take a while for the deletion of a replication configuration to fully propagate.

    Args:
        name(str): Idem name of the bucket.
        resource_id(str, Optional): Name of the bucket on which replication needs to be deleted.

    Request Syntax:
        .. code-block:: yaml

            [bucket_name]-replication:
              aws.s3.bucket_replication.absent:
                - name: "string"
                - resource_id: "string"

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: yaml

            test-bucket-replication:
              aws.s3.bucket_replication.absent:
                - name: bucket
                - resource_id: bucket
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.s3.bucket_replication", name=name
        )
        return result

    before = await hub.exec.aws.s3.bucket_replication.get(
        ctx, name=name, resource_id=resource_id
    )
    if not before["result"]:
        if "NoSuchBucket" in str(before["comment"]):
            result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
                resource_type="aws.s3.bucket_replication", name=name
            )
            return result
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.s3.bucket_replication", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.s3.bucket_replication", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        delete_ret = await hub.exec.boto3.client.s3.delete_bucket_replication(
            ctx, Bucket=resource_id
        )
        if not delete_ret["result"]:
            result["result"] = False
            result["comment"] = delete_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.s3.bucket_replication", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Gets information about the S3 bucket replication configurations.

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Returns:
        dict[str, dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.s3.bucket_replication
    """
    result = {}
    # To describe the replication configurations of all the buckets, we first need to list all the buckets,
    # then get the replication configurations of each bucket
    ret = await hub.exec.boto3.client.s3.list_buckets(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe S3 buckets {ret['comment']}")
        return {}

    for bucket in ret["ret"]["Buckets"]:
        bucket_name = bucket.get("Name")
        # get replication configuration for each bucket
        bucket_replication_response = (
            await hub.exec.boto3.client.s3.get_bucket_replication(
                ctx, Bucket=bucket_name
            )
        )
        if bucket_replication_response["result"]:
            bucket_replication_response["ret"].pop("ResponseMetadata", None)
            if bucket_replication_response["ret"]:
                translated_resource = hub.tool.aws.s3.conversion_utils.convert_raw_bucket_replication_to_present(
                    ctx=ctx,
                    raw_resource=bucket_replication_response["ret"],
                    bucket_name=bucket_name,
                )

                result[bucket_name + "-replication"] = {
                    "aws.s3.bucket_replication.present": [
                        {parameter_key: parameter_value}
                        for parameter_key, parameter_value in translated_resource.items()
                    ]
                }
    return result
