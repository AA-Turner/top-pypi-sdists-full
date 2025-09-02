"""State module for managing EC2 Snapshots"""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    volume_id: str,
    resource_id: str = None,
    description: str = None,
    outpost_arn: str = None,
    tags: Dict[str, str] = None,
) -> Dict[str, Any]:
    """Register an AWS Snapshot.

    Creates crash-consistent snapshots of multiple EBS volumes and stores the data in S3. Volumes are chosen by
    specifying an instance. Any attached volumes will produce one snapshot each that is crash-consistent across the
    instance. Boot volumes can be excluded by changing the parameters.  You can create multi-volume snapshots of
    instances in a Region and instances on an Outpost. If you create snapshots from an instance in a Region, the
    snapshots must be stored in the same Region as the instance. If you create snapshots from an instance on an
    Outpost, the snapshots can be stored on the same Outpost as the instance, or in the Region for that Outpost.

    Args:
        name (str):
            An Idem name for the snapshot resource.

        volume_id (str):
            AWS Volume volume_id of the volume the snapshot is to be created from.

        resource_id (str, Optional):
            AWS Snapshot snapshot_id.

        description (str, Optional):
            A description propagated to every snapshot specified by the instance. Defaults to None.

        outpost_arn (str, Optional):
            The Amazon Resource Name (ARN) of the Outpost on which to create the local snapshots.   To
            create snapshots from an instance in a Region, omit this parameter. The snapshots are created in
            the same Region as the instance.   To create snapshots from an instance on an Outpost and store
            the snapshots in the Region, omit this parameter. The snapshots are created in the Region for
            the Outpost.   To create snapshots from an instance on an Outpost and store the snapshots on an
            Outpost, specify the ARN of the destination Outpost. The snapshots must be created on the same
            Outpost as the instance.   For more information, see  Create multi-volume local snapshots from
            instances on an Outpost in the Amazon Elastic Compute Cloud User Guide. Defaults to None.

        tags (dict, Optional):
            Dict in the format of ``{tag-key: tag-value}`` to associate with the Snapshot.

            * Key (str):
                The key name that can be used to look up or retrieve the associated value.

            * Value (str):
                The value associated with this tag. For example tags with the key name of Name could have
                the AWS snapshot_id as the associated value.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws_auto.ec2.snapshot.present:
                - name: some-snapshot-ARN
                - resource_id: some-snapsshot-ARN
                - volume_id: some-volume-ARN
                - tags:
                    - Key: name
                      Value: ONE
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    if resource_id:
        before = await hub.exec.aws.ec2.snapshot.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["comment"] = before["comment"]
            result["result"] = before["result"]
            return result

    if before:
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])

        old_tags = result["old_state"].get("tags")
        if tags is not None and tags != old_tags:
            update_ret = await hub.tool.aws.ec2.tag.update_tags(
                ctx=ctx,
                resource_id=resource_id,
                old_tags=old_tags,
                new_tags=tags,
            )
            if not update_ret["result"]:
                result["comment"] = update_ret["comment"]
                result["result"] = False
                return result

            if update_ret["ret"]:
                result["comment"] = update_ret["comment"]
            resource_updated = resource_updated or bool(update_ret["ret"])
            if ctx.get("test", False) and update_ret["ret"] is not None:
                plan_state["tags"] = update_ret["ret"].get("tags")
                result["comment"] += [f"Would update tags for'{name}'"]
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "volume_id": volume_id,
                    "description": description,
                    "outpost_arn": outpost_arn,
                    "tags": tags,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.ec2.snapshot", name=name
            )
            return result

        ret = await hub.exec.boto3.client.ec2.create_snapshot(
            ctx,
            Description=description,
            OutpostArn=outpost_arn,
            VolumeId=volume_id,
            TagSpecifications=[
                {
                    "ResourceType": "snapshot",
                    "Tags": hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
                }
            ]
            if tags
            else None,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        resource_id = ret["ret"]["SnapshotId"]
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.ec2.snapshot", name=name
        )

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            response = await hub.exec.aws.ec2.snapshot.get(
                ctx, name=name, resource_id=resource_id
            )
            after = response["ret"]
            result["new_state"] = copy.deepcopy(after)
        else:
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                resource_type="aws.ec2.snapshot", name=name
            )
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deregisters the specified Snapshot

    Deletes the specified snapshot. When you make periodic snapshots of a volume, the snapshots are incremental, and
    only the blocks on the device that have changed since your last snapshot are saved in the new snapshot. When you
    delete a snapshot, only the data not needed for any other snapshot is removed. So regardless of which prior
    snapshots have been deleted, all active snapshots will have access to all the information needed to restore the
    volume. You cannot delete a snapshot of the root device of an EBS volume used by a registered AMI. You must
    first de-register the AMI before you can delete the snapshot. For more information, see Delete an Amazon EBS
    snapshot in the Amazon Elastic Compute Cloud User Guide.

    Args:
        name (str, Optional): An Idem name of the snapshot.
        resource_id(str): The snapshot ID.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws_auto.ec2.snapshot.absent:
                - name: value
                - resource_id: value
                - snapshot_id: value
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.snapshot", name=name
        )
        return result

    before = await hub.exec.aws.ec2.snapshot.get(
        ctx, name=name, resource_id=resource_id
    )

    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.snapshot", name=name
        )
    else:
        result["old_state"] = before["ret"]

        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.ec2.snapshot", name=name
            )
            return result

        ret = await hub.exec.boto3.client.ec2.delete_snapshot(
            ctx, SnapshotId=resource_id
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
        else:
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.ec2.snapshot", name=name
            )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Gets information about the AWS Snapshot(s)

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws_auto.ec2.snapshot
    """

    result = {}
    ret = await hub.exec.boto3.client.ec2.describe_snapshots(ctx, OwnerIds=["self"])

    if not ret["result"]:
        hub.log.warning(f"Could not describe snapshot {ret['comment']}")
        return {}

    for snapshot in ret["ret"]["Snapshots"]:
        resource_id = snapshot.get("SnapshotId")
        resource_translated = await hub.tool.aws.ec2.conversion_utils.convert_raw_snapshot_to_present_async(
            ctx=ctx, raw_resource=snapshot, idem_resource_name=resource_id
        )
        result[resource_id] = {
            "aws.ec2.snapshot.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result
