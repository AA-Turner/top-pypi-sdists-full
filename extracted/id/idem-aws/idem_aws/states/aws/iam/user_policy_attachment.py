"""State module for managing IAM User Policy Attachments."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub, ctx, name: str, user_name: str, policy_arn: str, resource_id: str = None
) -> Dict[str, Any]:
    """Attaches the specified managed policy to the specified user.

    Use this operation to attach a managed policy to a user.

    Args:
        name(str):
            An Idem name of the state.

        user_name(str):
            The name (friendly name, not ARN) of the IAM user to detach the policy from. This parameter allows(through
            its regex pattern) a string of characters consisting of upper and lowercase alphanumeric characters with no
            spaces. You can also include any of the following characters: _+=,.@-

        policy_arn(str):
            The Amazon Resource Name (ARN) of the IAM policy you want to attach.

        resource_id(str, Optional):
            An identifier refers to an existing resource. The format is <user_name>/<policy_arn>

    Request Syntax:
        .. code-block:: sls

            [iam-attach-user-policy]:
              aws.iam.user_policy_attachment.present:
                - name: "string"
                - user_name: 'string'
                - policy_arn: 'string'
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem-test-attach-policy:
              aws.iam.user_policy_attachment.present:
                - name: test-policy-attachment
                - user_name: serverless
                - policy_arn: arn:aws:iam::aws:policy/AdministratorAccess

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    generated_resource_id = f"{user_name}/{policy_arn}"
    if resource_id and generated_resource_id != resource_id:
        result["comment"].append(
            f"resource_id mismatches. Use newly generated resource_id {generated_resource_id}"
        )
        # newly generated resource_id is used to populate resource state in get()

    before_ret = await hub.exec.aws.iam.user_policy_attachment.get(
        ctx, name=name, user_name=user_name, policy_arn=policy_arn
    )
    if not before_ret["result"]:
        # If user name does not exists yet and this is a 'test' mode, do not fail
        if "NoSuchEntityException" in before_ret["comment"][0] and ctx.get(
            "test", False
        ):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "user_name": user_name,
                    "policy_arn": policy_arn,
                    "resource_id": generated_resource_id,
                },
            )
            result["comment"] += list(
                hub.tool.aws.comment_utils.would_create_comment(
                    resource_type="aws.iam.user_policy_attachment", name=name
                )
            )
            return result
        result["result"] = False
        result["comment"] = before_ret["comment"]
        return result
    if before_ret["ret"]:
        result["comment"] += list(
            hub.tool.aws.comment_utils.already_exists_comment(
                resource_type="aws.iam.user_policy_attachment", name=name
            )
        )
        result["old_state"] = before_ret["ret"]
        result["new_state"] = copy.deepcopy(result["old_state"])
        return result
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "user_name": user_name,
                    "policy_arn": policy_arn,
                    "resource_id": generated_resource_id,
                },
            )
            result["comment"] += list(
                hub.tool.aws.comment_utils.would_create_comment(
                    resource_type="aws.iam.user_policy_attachment", name=name
                )
            )
        else:
            ret = await hub.exec.boto3.client.iam.attach_user_policy(
                ctx,
                UserName=user_name,
                PolicyArn=policy_arn,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] += list(
                hub.tool.aws.comment_utils.create_comment(
                    resource_type="aws.iam.user_policy_attachment", name=name
                )
            )

            ret = await hub.exec.boto3.client.iam.attach_user_policy(
                ctx,
                UserName=user_name,
                PolicyArn=policy_arn,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] += list(
                hub.tool.aws.comment_utils.create_comment(
                    resource_type="aws.iam.user_policy_attachment", name=name
                )
            )

        result["new_state"] = {
            "name": name,
            "user_name": user_name,
            "policy_arn": policy_arn,
            "resource_id": generated_resource_id,
        }

    return result


async def absent(
    hub,
    ctx,
    name: str,
    *,
    resource_id: str = None,
    user_name: str = None,
    policy_arn: str = None,
) -> Dict[str, Any]:
    """Removes the specified managed policy from the specified user.

    A user can also have inline policies embedded with it. To delete an inline policy, use DeleteUserPolicy

    Args:
        name(str):
            An Idem name of the state.

        resource_id(str, Optional):
            An identifier refers to an existing resource. The format is <user_name>/<policy_arn> Either resource_id
            or both user_name and policy_arn should be specified for absent.

        user_name(str, Optional):
            The name (friendly name, not ARN) of the IAM user to detach the policy from. This parameter allows
            (through its regex pattern ) a string of characters consisting of upper and lowercase alphanumeric
            characters with no spaces. You can also include any of the following characters: _+=,.@-

        policy_arn(str, Optional):
            The Amazon Resource Name (ARN) of the IAM policy you want to attach.

    Request Syntax:
        .. code-block:: sls

            [iam-user-policy-name]:
              aws.iam.user_policy_attachment.absent:
                - name: 'string'
                - user_name: 'string'
                - policy_arn: 'string'
                - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem-test-attach-policy:
              aws.iam.user_policy_attachment.absent:
                - name: test-policy-attachment
                - user_name: serverless
                - policy_arn: arn:aws:iam::aws:policy/AdministratorAccess
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not user_name and not policy_arn:
        result["comment"] += list(
            hub.tool.aws.comment_utils.already_absent_comment(
                resource_type="aws.iam.user_policy_attachment", name=name
            )
        )

    generated_resource_id = f"{user_name}/{policy_arn}"
    if resource_id and generated_resource_id != resource_id:
        result["comment"].append(
            f"resource_id mismatches. Use newly generated resource_id"
        )
    before_ret = await hub.exec.aws.iam.user_policy_attachment.get(
        ctx, name=name, user_name=user_name, policy_arn=policy_arn
    )
    if not before_ret["result"]:
        result["comment"] = before_ret["comment"]
        result["result"] = False
        return result
    if not before_ret["ret"]:
        result["comment"] += list(
            hub.tool.aws.comment_utils.already_absent_comment(
                resource_type="aws.iam.user_policy_attachment", name=name
            )
        )
    elif ctx.get("test", False):
        result["old_state"] = before_ret["ret"]
        result["comment"] += list(
            hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.iam.user_policy_attachment", name=name
            )
        )
    else:
        result["old_state"] = before_ret["ret"]
        ret = await hub.exec.boto3.client.iam.detach_user_policy(
            ctx, UserName=user_name, PolicyArn=policy_arn
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] += list(ret["comment"])
            result["result"] = False
            return result
        result["comment"] += list(
            hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.iam.user_policy_attachment", name=name
            )
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Lists all managed policies that are attached to the specified IAM user. Lists all managed policies that are attached
    to the specified IAM user.


    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws_auto.iam.user_policy_attachment
    """

    result = {}
    # Fetch all users and then policies for each of them
    users = await hub.exec.boto3.client.iam.list_users(ctx)
    if not users["result"]:
        hub.log.warning(f"Could not describe user {users['comment']}")
        return {}
    user_names = [user.get("UserName") for user in users["ret"]["Users"]]
    for user_name in user_names:
        ret_attached_policies = (
            await hub.exec.boto3.client.iam.list_attached_user_policies(
                ctx=ctx, UserName=user_name
            )
        )
        if not ret_attached_policies["result"]:
            hub.log.warning(
                f"Could not get attached policy list with user {user_name} with error"
                f" {ret_attached_policies['comment']} . Describe will skip this user and continue."
            )
        else:
            resources = ret_attached_policies["ret"].get("AttachedPolicies")
            for resource in resources:
                resource_name = f"{user_name}-{resource.get('PolicyArn')}"
                resource_translated = [
                    {"name": user_name},
                    {"user_name": user_name},
                    {"policy_arn": resource.get("PolicyArn")},
                ]
                result[resource_name] = {
                    "aws.iam.user_policy_attachment.present": resource_translated
                }
    return result
