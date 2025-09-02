"""State module for managing EC2 placement groups."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    strategy: str = None,
    partition_count: int = None,
    tags: Dict[str, str] = None,
    spread_level: str = None,
) -> Dict[str, Any]:
    """Manage creation and updates for an EC2 placement group.

    Creates a placement group in which to launch instances. The strategy of the placement group determines how the
    instances are organized within the group.  A cluster placement group is a logical grouping of instances within a
    single Availability Zone that benefit from low network latency, high network throughput. A spread placement
    group places instances on distinct hardware. A partition placement group places groups of instances in different
    partitions, where instances in one partition do not share the same hardware with instances in another partition.
    For more information, see Placement groups in the Amazon EC2 User Guide.

    Args:
        name(str):
            An Idem name of the resource and the GroupName of the placement group.

        resource_id(str, Optional):
            The GroupName of the placement group.

        strategy(str, Optional):
            The placement strategy. Defaults to None.
            May be one of the following.
            cluster/spread/partition

        partition_count(int, Optional):
            The number of partitions. Valid only when Strategy is set to partition. Defaults to None.

        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
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

        spread_level(str, Optional):
            Determines how placement groups spread instances.
                * Host: You can use host only with Outpost placement groups.
                * Rack: No usage restrictions. Defaults to None.

    Request Syntax:
        .. code-block:: sls

            idem_placement_group_name:
              aws.ec2.placement_group.present:
                - name: value
                - strategy: cluster

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_placement_group_name:
              aws.ec2.placement_group.present:
                - name: my_placement_group_name
                - strategy: cluster
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False

    if resource_id:
        before = await hub.exec.aws.ec2.placement_group.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])
        old_tags = result["old_state"].get("tags")

        if tags is not None and tags != old_tags:
            group_id = before["ret"]["group_id"]
            update_ret = await hub.tool.aws.ec2.tag.update_tags(
                ctx,
                resource_id=group_id,
                old_tags=old_tags,
                new_tags=tags,
            )

            result["comment"] += list(update_ret["comment"])
            result["result"] = update_ret["result"]

            resource_updated = resource_updated or bool(update_ret["ret"])
            if ctx.get("test", False) and update_ret["ret"]:
                plan_state["tags"] = update_ret["ret"]

            if not update_ret["result"]:
                return result

        if ctx.get("test", False) and resource_updated:
            plan_state["tags"] = update_ret["ret"]

            result["new_state"] = plan_state
            result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                "aws.ec2.placement_group", name
            )
            return result
        if not resource_updated:
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                "aws.ec2.placement_group", name
            )
    else:
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.ec2.placement_group", name=name
            )
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_id": None,
                    "group_name": name,
                    "strategy": strategy,
                    "partition_count": partition_count,
                    "spread_level": spread_level,
                    "tags": tags,
                },
            )
            return result

        boto_tags = hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
        boto_tag_specification = [
            {"ResourceType": "placement-group", "Tags": boto_tags}
        ]
        ret = await hub.exec.boto3.client.ec2.create_placement_group(
            ctx,
            **{
                "GroupName": name,
                "Strategy": strategy,
                "PartitionCount": partition_count,
                "TagSpecifications": boto_tag_specification,
                "SpreadLevel": spread_level,
            },
        )

        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.ec2.placement_group", name=name
        )

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif (not before) or resource_updated:
        after = await hub.exec.aws.ec2.placement_group.get(
            ctx, name=name, resource_id=resource_id
        )
        if not after["result"]:
            result["comment"] = after["comment"]
            result["result"] = after["result"]
            return result
        result["new_state"] = copy.deepcopy(after["ret"])
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])

    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Delete an EC2 placement group if it exists.

    Deletes the specified placement group. You must terminate all instances in the placement group before you can
    delete the placement group. For more information, see Placement groups in the Amazon EC2 User Guide.

    Args:
        name(str): An Idem name of the resource and the GroupName of the placement group
        resource_id(str, Optional):
            The GroupName of the placement group.
            Idem automatically considers this resource to be absent if this field is not specified.

    Request Syntax:
        .. code-block:: sls

            idem_placement_group_name:
              aws.ec2.placement_group.absent:
                - name: value
                - resource_id: value

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_placement_group_name:
              aws.ec2.placement_group.absent:
                - name: my_placement_group_name
                - resource_id: my_placement_group_name
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.placement_group", name=name
        )
        return result

    before = await hub.exec.aws.ec2.placement_group.get(
        ctx, name=name, resource_id=resource_id
    )

    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.placement_group", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = copy.deepcopy(before["ret"])
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.ec2.placement_group", name=name
        )
        return result
    else:
        result["old_state"] = copy.deepcopy(before["ret"])
        ret = await hub.exec.boto3.client.ec2.delete_placement_group(
            ctx, **{"GroupName": resource_id}
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.ec2.placement_group", name=name
        )

    return result


async def describe(
    hub,
    ctx,
) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Gets information about the AWS EC2 placement group

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.ec2.placement_group
    """
    result = {}
    ret = await hub.exec.aws.ec2.placement_group.list(ctx, name=None, filters=None)

    if not ret["result"]:
        hub.log.warning(f"Could not describe aws.ec2.placement_group {ret['comment']}")
        return result

    for placement_group in ret["ret"]:
        resource_id = placement_group.get("group_name", None)
        if resource_id:
            result[resource_id] = {
                "aws.ec2.placement_group.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in placement_group.items()
                ]
            }

    return result
