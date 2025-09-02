"""State module for managing IAM Groups."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]

TREQ = {
    "absent": {"require": ["aws.iam.user.absent"]},
}


async def present(
    hub, ctx, name: str, group_name: str, resource_id: str = None, path: str = None
) -> Dict[str, Any]:
    """Create/Update the IAM Group.

    Creates a new group.  For information about the number of groups you can create, see IAM and STS quotas in the
    IAM User Guide.

    Args:
        name(str): An Idem name of the resource. This is also used as the name of the IAM group.

        resource_id(str, Optional): An identifier of the resource in the provider. Name of Group.

        path(str, Optional): The path to the group. This parameter is optional. If it is not included,
            it defaults to a slash (/). This parameter allows (through its regex pattern) a string of
            characters consisting of either a forward slash (/) by itself or a string that must begin and
            end with forward slashes. For more information about paths, see IAM identifiers in the IAM User Guide.

        group_name(str): The name of the group to create. Do not include the path in this value.
            IAM user, group, role, and policy names must be unique within the account. Names are not distinguished by
            case. For example, you cannot create resources named both "MyResource" and "myresource".

    Request Syntax:
        .. code-block:: sls

            [group_name]:
              aws.iam.group.present:
                - name: "string"
                - group_name: "string"
                - resource_id: "string"
                - path: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            test-group:
              aws.iam.group.present:
                - name: test-group
                - resource_id: test-group
                - group_name: test-group
                - path: /

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False

    if resource_id:
        before = await hub.exec.aws.iam.group.get(
            ctx, resource_id=resource_id, name=name
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["comment"] += hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.iam.group", name=name
        )
        result["old_state"] = copy.deepcopy(before["ret"])
        result["new_state"] = copy.deepcopy(result["old_state"])

        update_ret = await hub.tool.aws.iam.group.update(
            ctx,
            resource_id=resource_id,
            before=before["ret"],
            group_name=group_name,
            path=path,
        )
        result["comment"] += update_ret["comment"]
        if not update_ret["result"]:
            result["result"] = False
            return result

        if update_ret["ret"] and "group_name" in update_ret["ret"]:
            resource_id = group_name
        resource_updated = bool(update_ret["ret"])

        if update_ret["ret"] and ctx.get("test", False):
            result["new_state"].update(update_ret["ret"])
            result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.iam.group", name=name
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
                    "group_name": group_name,
                    "path": path,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.iam.group", name=name
            )
            return result
        create_ret = await hub.exec.boto3.client.iam.create_group(
            ctx, GroupName=group_name, Path=path
        )
        if not create_ret["result"]:
            result["result"] = False
            result["comment"] = create_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.iam.group", name=name
        )
        resource_id = group_name

    if (not result["old_state"]) or resource_updated:
        after_ret = await hub.exec.aws.iam.group.get(
            ctx, name=group_name, resource_id=resource_id
        )
        if not after_ret["result"] or not after_ret["ret"]:
            result["result"] = False
            result["comment"] += after_ret["comment"]
            return result
        result["new_state"] = after_ret["ret"]

    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes the specified IAM group.

    The group must not contain any users or have any attached policies.

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): Name of IAM group.

    Request Syntax:
        .. code-block:: sls

            [group_name]:
              aws.iam.group.absent:
                - name: "string"
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            test-group:
              aws.iam.group.absent:
                - name: test-group
                - resource_id: test-group
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.iam.group", name=name
        )
        return result

    before = await hub.exec.aws.iam.group.get(ctx, name=name, resource_id=resource_id)
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.iam.group", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.iam.group", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        delete_ret = await hub.exec.boto3.client.iam.delete_group(
            ctx, GroupName=resource_id
        )
        if not delete_ret["result"]:
            result["result"] = False
            result["comment"] = delete_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.iam.group", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Gets information about the IAM Group.

    Describe the resource in a way that can be recreated/managed with the corresponding
    present function.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.iam.group

    """
    result = {}
    ret = await hub.exec.boto3.client.iam.list_groups(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe iam group {ret['comment']}")
        return {}

    for group in ret["ret"]["Groups"]:
        group_name = group.get("GroupName")

        translated_resource = (
            hub.tool.aws.iam.conversion_utils.convert_raw_group_to_present(
                raw_resource=group,
                idem_resource_name=group_name,
            )
        )
        resource_key = f"iam-group-{group_name}"
        result[resource_key] = {
            "aws.iam.group.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in translated_resource.items()
            ]
        }

    return result
