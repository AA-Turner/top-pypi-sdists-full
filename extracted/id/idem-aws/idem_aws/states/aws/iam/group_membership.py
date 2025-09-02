"""State module for managing IAM Group Membership."""
import copy
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub, ctx, name: str, group: str, users: List, resource_id: str = None
) -> Dict[str, Any]:
    """Adds the specified user to the specified group.

    Args:
        name(str): A name to represent the operation. This name is only for logging purpose. It is not used to
            attach a user to a group.

        group(str): Group Name

        users(List): List of users to attach to the group.

        resource_id(str, Optional): The identifier for this object. Group Name

    Request Syntax:
        .. code-block:: sls

            [iam-group-membership]:
              aws.iam.group_membership.present:
                - name: 'string'
                - resource_id: 'string'
                - group: 'string'
                - users: list

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            iam-group-membership-temp-name:
              aws.iam.group_membership.present:
                - name: test_group
                - resource_id: test_group
                - group: test_group
                - users:
                  - test_user

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False

    if resource_id:
        before = await hub.exec.aws.iam.group_membership.get(
            ctx, name=group, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = copy.deepcopy(before["ret"])
        result["new_state"] = copy.deepcopy(result["old_state"])
        result["comment"] += hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.iam.group_membership", name=name
        )

        update_ret = await hub.tool.aws.iam.group_membership.update(
            ctx,
            resource_id=resource_id,
            before=before["ret"],
            users=users,
        )
        result["comment"] += update_ret["comment"]
        if not update_ret["result"]:
            result["result"] = False
            return result

        resource_updated = bool(update_ret["ret"])

        if update_ret["ret"] and ctx.get("test", False):
            result["new_state"].update(update_ret["ret"])

        if resource_updated and ctx.get("test", False):
            return result

    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_id": group,
                    "group": group,
                    "users": users,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.iam.group_membership", name=group
            )
            return result

        for user in users:
            create_ret = await hub.exec.boto3.client.iam.add_user_to_group(
                ctx, GroupName=group, UserName=user
            )
            if not create_ret["result"]:
                result["result"] = False
                result["comment"] = create_ret["comment"]
                return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.iam.group_membership", name=group
        )
        resource_id = group

    if (not result["old_state"]) or resource_updated:
        after_ret = await hub.exec.aws.iam.group_membership.get(
            ctx, name=resource_id, resource_id=resource_id
        )
        if not after_ret["result"] or not after_ret["ret"]:
            result["result"] = False
            result["comment"] += after_ret["comment"]
            return result
        result["new_state"] = after_ret["ret"]

    return result


async def absent(
    hub,
    ctx,
    name: str,
    users: List = [],
    resource_id: str = None,
) -> Dict[str, Any]:
    """Removes users from the specified Group.

    Args:
        name(str): The name of the AWS IAM Group.
        users(List, Optional): List of users to remove.
        resource_id(str): Name of IAM group.

    Request Syntax:
        .. code-block:: sls

            [group_name]:
              aws.iam.group.absent:
                - name: "string"
                - resource_id: "string"
                - users:
                  - "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            iam-group-membership-test-group:
              aws.iam.group_membership.absent:
                - name: test_group
                - resource_id: test_group
                - users:
                  - test_user
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.iam.group_membership", name=name
        )
        return result

    before = await hub.exec.aws.iam.group_membership.get(
        ctx, name=name, resource_id=resource_id
    )
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.iam.group_membership", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.iam.group_membership", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]

        for user in users:
            if not ctx.get("test", False):
                remove_usr_ret = await hub.exec.boto3.client.iam.remove_user_from_group(
                    ctx=ctx, GroupName=resource_id, UserName=user
                )
                if not remove_usr_ret["result"]:
                    result["comment"] = remove_usr_ret["comment"]
                    result["result"] = False
                    return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.iam.group_membership", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Gets information about the IAM Group membership.

    Lists the names of the users in IAM group.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.iam.group_membership

    """
    result = {}
    ret_groups = await hub.exec.boto3.client.iam.list_groups(ctx)
    if not ret_groups["result"]:
        result["comment"] = ret_groups["comment"]
        result["result"] = False
        return result

    group_name_list = [group.get("GroupName") for group in ret_groups["ret"]["Groups"]]

    for group_name in group_name_list:
        ret_group_users = await hub.exec.boto3.client.iam.get_group(
            ctx=ctx, GroupName=group_name
        )
        if not ret_group_users["result"]:
            result["comment"] = ret_group_users["comment"]
            result["result"] = False
            return result
        else:
            users = ret_group_users["ret"].get("Users")

            translated_resource = hub.tool.aws.iam.conversion_utils.convert_raw_group_membership_to_present(
                group=group_name, users=[user.get("UserName") for user in users]
            )

            resource_id = f"iam-group-membership-{group_name}"
            result[resource_id] = {
                "aws.iam.group_membership.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in translated_resource.items()
                ]
            }
    return result
