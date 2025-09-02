"""State module for managing Amazon DB Subnet Group."""
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
    db_subnet_group_description: str,
    subnet_ids: List,
    resource_id: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass("Tag", [("Key", str), ("Value", str, field(default=None))])
    ] = None,
) -> Dict[str, Any]:
    """Creates a new subnet group.

    Subnet groups must contain at least one subnet in at least two Availability Zones in
    the Amazon Web Services Region.

    Args:
        name(str):
            An Idem name of the resource.
        db_subnet_group_description(str):
            The description for the subnet group.
        subnet_ids(list):
            The Amazon EC2 subnet IDs for the subnet group.
        resource_id(str, Optional):
            AWS DocumentDB Subnet Group Name. Defaults to None.
        tags(dict or list, Optional):
            Dict in the format of {tag-key: tag-value} or List of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]``. The tags to be assigned to the subnet group. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
      .. code-block:: sls

        resource_is_present:
          aws.docdb.db_subnet_group.present:
            - name: value
            - resource_id: value
            - db_subnet_group_description: value
            - subnet_ids: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
    if resource_id:
        before = await hub.exec.aws.docdb.db_subnet_group.get(
            ctx=ctx, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["comment"] = before["comment"]
            result["result"] = False
            return result

    if before and before["ret"]:
        resource_arn = before["ret"]["db_subnet_group_arn"]
        old_tags = before["ret"]["tags"]

        if not old_tags:
            result["result"] = False
            result["comment"] += old_tags["comment"]
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        future_state = copy.deepcopy(result["old_state"])

        old_subnets = result["old_state"].get("subnet_ids", [])
        update_parameters = {
            "DBSubnetGroupName": resource_id,
            "SubnetIds": old_subnets,
        }

        # Check to see if SubNet Ids need to be updated
        if subnet_ids is not None and set(old_subnets) != set(subnet_ids):
            resource_updated = True
            update_parameters["SubnetIds"] = subnet_ids

        # Check to see if Subnet Description need to be updated
        old_description = result["old_state"].get("db_subnet_group_description")
        if (
            db_subnet_group_description is not None
            and old_description != db_subnet_group_description
        ):
            resource_updated = True
            update_parameters["DBSubnetGroupDescription"] = db_subnet_group_description

        if resource_updated:
            if ctx.get("test", False):
                future_state["subnet_ids"] = subnet_ids
                future_state[
                    "db_subnet_group_description"
                ] = db_subnet_group_description
            else:
                ret = await hub.exec.boto3.client.docdb.modify_db_subnet_group(
                    ctx, **update_parameters
                )
                result["result"] = ret["result"]
                result["comment"] += ret["comment"]
                if not result["result"]:
                    return result

        # Update Tags
        if tags is not None and not hub.tool.aws.state_comparison_utils.compare_dicts(
            tags, old_tags
        ):
            resource_updated = True
            update_ret = await hub.tool.aws.docdb.tag.update_tags(
                ctx=ctx,
                resource_arn=resource_arn,
                old_tags=old_tags,
                new_tags=tags,
            )
            if not update_ret["result"]:
                result["comment"] = update_ret["comment"]
                result["result"] = False
                hub.log.debug(
                    f"Failed updating tags for aws.docdb.db_subnet_group '{name}'"
                )
                return result
            result["comment"] += update_ret["comment"]
            if ctx.get("test", False) and update_ret["ret"] is not None:
                future_state["tags"] = update_ret["ret"]

        if ctx.get("test", False):
            if resource_updated:
                result["new_state"] = future_state
                result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.docdb.db_subnet_group", name=name
                )
            else:
                result["comment"] += [
                    f"aws.docdb.db_subnet_group '{name}' already exists"
                ]
                result["new_state"] = copy.deepcopy(result["old_state"])
            return result

        if not resource_updated:
            result["comment"] += [f"aws.docdb.db_subnet_group '{name}' already exists"]
        else:
            result["comment"] = result[
                "comment"
            ] + hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.docdb.db_subnet_group", name=name
            )
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "db_subnet_group_name": name,
                    "db_subnet_group_description": db_subnet_group_description,
                    "resource_id": resource_id,
                    "subnet_ids": subnet_ids,
                    "tags": tags,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.docdb.db_subnet_group", name=name
            )
            return result

        ret = await hub.exec.boto3.client.docdb.create_db_subnet_group(
            ctx,
            DBSubnetGroupName=name,
            DBSubnetGroupDescription=db_subnet_group_description,
            SubnetIds=subnet_ids,
            Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        resource_id = ret["ret"]["DBSubnetGroup"]["DBSubnetGroupName"]
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.docdb.db_subnet_group", name=name
        )

    if (not before) or resource_updated:
        after = await hub.exec.aws.docdb.db_subnet_group.get(
            ctx=ctx, resource_id=resource_id
        )

        if not (after["result"] and after["ret"]):
            result["result"] = False
            result["comment"] += after["comment"]
            return result
        result["new_state"] = copy.deepcopy(after["ret"])
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes a subnet group.

    The specified database subnet group must not be associated with any DB instances.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            AWS DocumentDB Subnet Group Name. Defaults to None.
            Idem automatically considers this resource being absent if this field is not specified

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.docdb.db_subnet_group.absent:
                - name: value
                - resource_id: value
    """
    already_absent_msg = hub.tool.aws.comment_utils.already_absent_comment(
        resource_type="aws.docdb.db_subnet_group", name=name
    )

    result = dict(
        comment=already_absent_msg,
        old_state=None,
        new_state=None,
        name=name,
        result=True,
    )

    if not resource_id:
        return result

    before = await hub.exec.aws.docdb.db_subnet_group.get(
        ctx=ctx,
        resource_id=resource_id,
    )

    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result
    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.docdb.db_subnet_group", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.docdb.db_subnet_group", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client.docdb.delete_db_subnet_group(
            ctx, **{"DBSubnetGroupName": name}
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.docdb.db_subnet_group", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Returns a list of DBSubnetGroup descriptions.

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function.
    If a DBSubnetGroupName is specified, the list will contain only the descriptions of the specified DBSubnetGroup.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.docdb.db_subnet_group
    """
    result = {}
    ret = await hub.exec.boto3.client.docdb.describe_db_subnet_groups(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe db_subnet_group {ret['comment']}")
        return {}

    for db_subnet_group in ret["ret"]["DBSubnetGroups"]:
        # Including fields to match the 'present' function parameters
        resource_id = db_subnet_group.get("DBSubnetGroupName")
        resource_arn = db_subnet_group.get("DBSubnetGroupArn")
        tags = await hub.tool.aws.docdb.tag.get_tags_for_resource(
            ctx, resource_arn=resource_arn
        )
        if not tags["result"]:
            # if error occurs when fetching tags
            hub.log.warning(
                f"Failed listing tags for aws.docdb.db_subnet_group '{resource_id}'"
                f"Describe will skip this aws.docdb.db_subnet_group and continue. "
            )
            continue
        tags = tags["ret"]
        resource_translated = (
            hub.tool.aws.docdb.db_subnet_group.convert_raw_db_subnet_group_to_present(
                db_subnet_group, idem_resource_name=resource_id, tags=tags
            )
        )

        result[resource_id] = {
            "aws.docdb.db_subnet_group.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result
