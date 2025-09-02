"""State module for managing EC2 Volumes"""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource", "allow_sync_sls_name_and_name_tag"]


async def present(
    hub,
    ctx,
    name: str,
    availability_zone: str,
    resource_id: str = None,
    encrypted: bool = None,
    iops: int = None,
    kms_key_id: str = None,
    outpost_arn: str = None,
    size: int = None,
    snapshot_id: str = None,
    volume_type: str = None,
    multi_attach_enabled: bool = None,
    throughput: int = None,
    tags: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Register an AWS Volume

    Creates an EBS volume that can be attached to an instance in the same Availability Zone. You can create a new
    empty volume or restore a volume from an EBS snapshot. Any Amazon Web Services Marketplace product codes from
    the snapshot are propagated to the volume. You can create encrypted volumes. Encrypted volumes must be attached
    to instances that support Amazon EBS encryption. Volumes that are created from encrypted snapshots are also
    automatically encrypted. For more information, see Amazon EBS encryption in the Amazon Elastic Compute Cloud
    User Guide. You can tag your volumes during creation. For more information, see Tag your Amazon EC2 resources in
    the Amazon Elastic Compute Cloud User Guide. For more information, see Create an Amazon EBS volume in the Amazon
    Elastic Compute Cloud User Guide.

    Args:
        name (str):
            An Idem name of the volume resource.

        resource_id (str, Optional):
            The AWS volume_id of the Volume. Defaults to None.

        availability_zone (str):
            The Availability Zone in which to create the volume.

        encrypted (bool, Optional):
            Indicates whether the volume should be encrypted. The effect of setting the encryption state to
            true depends on the volume origin (new or from a snapshot), starting encryption state,
            ownership, and whether encryption by default is enabled. For more information, see Encryption by
            default in the Amazon Elastic Compute Cloud User Guide. Encrypted Amazon EBS volumes must be
            attached to instances that support Amazon EBS encryption. For more information, see Supported
            instance types. Defaults to None.

        iops (int, Optional):
            The number of I/O operations per second (IOPS). For gp3, io1, and io2 volumes, this represents
            the number of IOPS that are provisioned for the volume. For gp2 volumes, this represents the
            baseline performance of the volume and the rate at which the volume accumulates I/O credits for
            bursting. The following are the supported values for each volume type:    gp3: 3,000-16,000 IOPS
            io1: 100-64,000 IOPS    io2: 100-64,000 IOPS    io1 and io2 volumes support up to 64,000 IOPS
            only on Instances built on the Nitro System. Other instance families support performance up to
            32,000 IOPS. This parameter is required for io1 and io2 volumes. The default for gp3 volumes is
            3,000 IOPS. This parameter is not supported for gp2, st1, sc1, or standard volumes. Defaults to None.

        kms_key_id (str, Optional):
            The identifier of the Key Management Service (KMS) KMS key to use for Amazon EBS encryption. If
            this parameter is not specified, your KMS key for Amazon EBS is used. If KmsKeyId is specified,
            the encrypted state must be true. You can specify the KMS key using any of the following:   Key
            ID. For example, 1234abcd-12ab-34cd-56ef-1234567890ab.   Key alias. For example,
            alias/ExampleAlias.   Key ARN. For example, arn:aws:kms:us-
            east-1:012345678910:key/1234abcd-12ab-34cd-56ef-1234567890ab.   Alias ARN. For example,
            arn:aws:kms:us-east-1:012345678910:alias/ExampleAlias.   Amazon Web Services authenticates the
            KMS key asynchronously. Therefore, if you specify an ID, alias, or ARN that is not valid, the
            action can appear to complete, but eventually fails. Defaults to None.

        outpost_arn (str, Optional):
            The Amazon Resource Name (ARN) of the Outpost. Defaults to None.

        size (int, Optional):
            The size of the volume, in GiBs. You must specify either a snapshot ID or a volume size. If you
            specify a snapshot, the default is the snapshot size. You can specify a volume size that is
            equal to or larger than the snapshot size. The following are the supported volumes sizes for
            each volume type:    gp2 and gp3: 1-16,384    io1 and io2: 4-16,384    st1 and sc1: 125-16,384
            standard: 1-1,024. Defaults to None.

        snapshot_id (str, Optional):
            The snapshot from which to create the volume. You must specify either a snapshot ID or a volume
            size. Defaults to None.

        volume_type (str, Optional): ]
            The volume type. This parameter can be one of the following values:   General Purpose SSD: gp2 |
            gp3    Provisioned IOPS SSD: io1 | io2    Throughput Optimized HDD: st1    Cold HDD: sc1
            Magnetic: standard    For more information, see Amazon EBS volume types in the Amazon Elastic
            Compute Cloud User Guide. Default: gp2. Defaults to None.

        multi_attach_enabled (bool, Optional):
            Indicates whether to enable Amazon EBS Multi-Attach. If you enable Multi-Attach, you can attach
            the volume to up to 16 Instances built on the Nitro System in the same Availability Zone. This
            parameter is supported with io1 and io2 volumes only. For more information, see  Amazon EBS
            Multi-Attach in the Amazon Elastic Compute Cloud User Guide. Defaults to None.

        throughput (int, Optional):
            The throughput to provision for a volume, with a maximum of 1,000 MiB/s. This parameter is valid
            only for gp3 volumes. Valid Range: Minimum value of 125. Maximum value of 1000. Defaults to None.

        tags (dict, Optional):
            dict in the format of ``{tag-key: tag-value}``. Defaults to None.

            * Key (str):
                The key of the tag. Tag keys are case-sensitive and accept a maximum of 127 Unicode characters. May not begin with aws: .

            * Value (str):
                The value of the tag. Tag values are case-sensitive and accept a maximum of 255 Unicode characters.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws_auto.ec2.volume.present:
                - name: some-volume-ARN
                - snapshot_id: some-snapshot-ARN
                - volume_type: standard
                - availability_zone: us-east-1a
                - size: 1
                - encrypted: True
                - tags:
                  - Key: name
                    Value: some-volume-ARN
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False

    if resource_id:
        before = await hub.exec.aws.ec2.volume.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])
        if tags is not None and tags != result["old_state"].get("tags"):
            # Update tags
            update_ret = await hub.tool.aws.ec2.tag.update_tags(
                ctx=ctx,
                resource_id=before["ret"]["resource_id"],
                old_tags=result["old_state"].get("tags"),
                new_tags=tags,
            )
            result["comment"] += update_ret["comment"]
            result["result"] = result["result"] and update_ret["result"]
            resource_updated = resource_updated or update_ret["result"]
            if ctx.get("test", False) and update_ret["result"]:
                plan_state["tags"] = update_ret["ret"]
        if resource_updated:
            if ctx.get("test", False):
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.ec2.volume", name=name
                )
            else:
                result["comment"] += hub.tool.aws.comment_utils.update_comment(
                    resource_type="aws.ec2.volume", name=name
                )
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "availability_zone": availability_zone,
                    "encrypted": encrypted,
                    "iops": iops,
                    "kms_key_id": kms_key_id,
                    "outpost_arn": outpost_arn,
                    "size": size,
                    "snapshot_id": snapshot_id,
                    "volume_type": volume_type,
                    "tags": tags,
                    "multi_attach_enabled": multi_attach_enabled,
                    "throughput": throughput,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.ec2.volume", name=name
            )
            return result

        ret = await hub.exec.boto3.client.ec2.create_volume(
            ctx,
            AvailabilityZone=availability_zone,
            Encrypted=encrypted,
            Iops=iops,
            KmsKeyId=kms_key_id,
            OutpostArn=outpost_arn,
            Size=size,
            SnapshotId=snapshot_id,
            VolumeType=volume_type,
            Throughput=throughput,
            MultiAttachEnabled=multi_attach_enabled,
            TagSpecifications=[
                {
                    "ResourceType": "volume",
                    "Tags": hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
                }
            ]
            if tags
            else None,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["result"] = ret["result"]
            result["comment"] = ret["comment"]
            return result
        resource_id = ret["ret"]["VolumeId"]
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.ec2.volume", name=name
        )

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            after = await hub.exec.aws.ec2.volume.get(
                ctx=ctx, name=name, resource_id=resource_id
            )
            if not after["result"]:
                result["result"] = False
                result["comment"] = after["comment"]
                return result
            result["new_state"] = copy.deepcopy(after["ret"])
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deregisters the specified Volume

    Deletes the specified EBS volume. The volume must be in the available state (not attached to an instance). The
    volume can remain in the deleting state for several minutes. For more information, see Delete an Amazon EBS
    volume in the Amazon Elastic Compute Cloud User Guide.

    Args:
        name (str): An Idem name of the resource.
        resource_id (str, Optional): Volume ID.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws_auto.ec2.volume.absent:
                - name: idem-test-volume
                - resource_id: volume-123456789
                - volume_id: volume-123456789
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.volume", name=name
        )
        return result

    before = await hub.exec.aws.ec2.volume.get(
        ctx=ctx, name=name, resource_id=resource_id
    )

    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result
    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.volume", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.ec2.volume", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client.ec2.delete_volume(ctx, VolumeId=resource_id)
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.ec2.volume", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Describes the specified EBS volumes or all of your EBS volumes. If you are describing a long list of volumes, we
    recommend that you paginate the output to make the list more manageable. The MaxResults parameter sets the
    maximum number of results returned in a single page. If the list of results exceeds your MaxResults value, then
    that number of results is returned along with a NextToken value that can be passed to a subsequent
    DescribeVolumes request to retrieve the remaining results. For more information about EBS volumes, see Amazon
    EBS volumes in the Amazon Elastic Compute Cloud User Guide.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe aws_auto.ec2.volume

    """

    result = {}
    ret = await hub.exec.boto3.client.ec2.describe_volumes(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe volume {ret['comment']}")
        return {}

    for volume in ret["ret"]["Volumes"]:
        # Including fields to match the 'present' function parameters
        resource_id = volume.get("VolumeId")
        resource_translated = (
            hub.tool.aws.ec2.conversion_utils.convert_raw_volume_to_present(
                raw_resource=volume, idem_resource_name=resource_id
            )
        )
        result[resource_id] = {
            "aws.ec2.volume.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result
