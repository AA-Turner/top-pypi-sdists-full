"""State module for managing IAM Group policy attachment."""
import copy
from typing import Any
from typing import Dict


__contracts__ = ["resource"]


async def present(
    hub, ctx, name: str, group: str, policy_arn: str, resource_id: str = None
) -> Dict[str, Any]:
    """Attaches the specified managed policy to the specified IAM group.

    Use this operation to attach a managed policy to a user.

    Args:
        name(str): An Idem name of the state.

        group(str): The name (friendly name, not ARN) of the group to attach the policy to. This parameter allows
            (through its regex pattern) a string of characters consisting of upper and lowercase alphanumeric
            characters with no spaces. You can also include any of the following characters: _+=,.@-

        policy_arn(str): The Amazon Resource Name (ARN) of the IAM policy you want to attach.

        resource_id(str, Optional): Policy ARN

    Request Syntax:
        .. code-block:: sls

            [iam-attach-group-policy]:
              aws.iam.group_policy_attachment.present:
                - name: "string"
                - group: "string"
                - policy_arn: "string"
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem-test-attach-policy:
              aws.iam.group_policy_attachment.present:
                - name: test-policy-attachment
                - group: test-policy-attachment
                - policy_arn: arn:aws:iam::aws:policy/AdministratorAccess

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if resource_id:
        before_ret = await hub.exec.aws.iam.group_policy_attachment.get(
            ctx, name=name, group=group, resource_id=resource_id
        )
        if not before_ret["result"] or not before_ret["ret"]:
            result["result"] = False
            result["comment"] = before_ret["comment"]
            return result

        result["old_state"] = copy.deepcopy(before_ret["ret"])
        result["new_state"] = copy.deepcopy(result["old_state"])
        result["comment"] += hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.iam.group_policy_attachment", name=name
        )
        return result
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_id": policy_arn,
                    "group": group,
                    "policy_arn": policy_arn,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.iam.group_policy_attachment", name=group
            )
            return result

        attach_ret = await hub.exec.boto3.client.iam.attach_group_policy(
            ctx,
            GroupName=group,
            PolicyArn=policy_arn,
        )
        if not attach_ret["result"]:
            result["result"] = False
            result["comment"] = attach_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.iam.group_policy_attachment", name=group
        )
        resource_id = policy_arn

    if not result["old_state"]:
        after_ret = await hub.exec.aws.iam.group_policy_attachment.get(
            ctx, name=name, group=group, policy_arn=policy_arn, resource_id=resource_id
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
    group: str = None,
    policy_arn: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Removes the specified managed policy from the specified group.

    Args:
        name(str): An Idem name of the state.

        group(str, Optional):
            The name (friendly name, not ARN) of the IAM user to detach the policy from.

        policy_arn(str, Optional):
            The Amazon Resource Name (ARN) of the IAM policy you want to detach.

        resource_id(str, Optional): Policy ARN

    Request Syntax:
        .. code-block:: sls

            [iam-group-policy-name]:
              aws.iam.group_policy_attachment.absent:
                - name: "string"
                - group: "string"
                - policy_arn: '"string"
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem-test-attach-policy:
              aws.iam.group_policy_attachment.absent:
                - name: test-policy-attachment
                - group: test-group
                - policy_arn: arn:aws:iam::aws:policy/AdministratorAccess
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.iam.group_policy_attachment", name=name
        )
        return result

    if not group or not policy_arn:
        result["comment"] = hub.tool.aws.comment_utils.missing_args_for_absent_comment(
            resource_type="aws.iam.group_policy_attachment",
            name=name,
            args=["group", "policy_arn"],
        )
        result["result"] = False
        return result

    before = await hub.exec.aws.iam.group_policy_attachment.get(
        ctx, name=name, group=group, resource_id=resource_id
    )
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.iam.group_policy_attachment", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.iam.group_policy_attachment", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]

        if not ctx.get("test", False):
            detach_ret = await hub.exec.boto3.client.iam.detach_group_policy(
                ctx=ctx, GroupName=group, PolicyArn=policy_arn
            )
            if not detach_ret["result"]:
                result["comment"] = detach_ret["comment"]
                result["result"] = False
                return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.iam.group_policy_attachment", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Gets information about the IAM Group policy attachment.

    Lists all managed policies that are attached to the specified IAM group.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.iam.group_policy_attachment
    """
    result = {}
    # Fetch all groups and then policies for each of them
    groups = await hub.exec.boto3.client.iam.list_groups(ctx)
    if not groups["result"]:
        result["comment"] = groups["comment"]
        result["result"] = False
        return result
    groups = [group.get("GroupName") for group in groups["ret"]["Groups"]]
    for group in groups:
        ret_attached_policies = (
            await hub.exec.boto3.client.iam.list_attached_group_policies(
                ctx=ctx, GroupName=group
            )
        )
        if not ret_attached_policies["result"]:
            result["comment"] = ret_attached_policies["comment"]
            result["result"] = False
            return result
        else:
            resources = ret_attached_policies["ret"].get("AttachedPolicies")
            for resource in resources:
                resource_name = f"{group}/{resource.get('PolicyArn')}"

                translated_resource = hub.tool.aws.iam.conversion_utils.convert_raw_group_policy_attachment_to_present(
                    group=group,
                    policy_arn=resource.get("PolicyArn"),
                )

                result[resource_name] = {
                    "aws.iam.group_policy_attachment.present": [
                        {parameter_key: parameter_value}
                        for parameter_key, parameter_value in translated_resource.items()
                    ]
                }
    return result
