"""State module for managing Amazon Organizations Accounts."""
import copy
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]
SERVICE = "organizations"


TREQ = {
    "absent": {
        "require": [
            "aws.organizations.policy_attachment.absent",
            "aws.organizations.policy.absent",
        ],
    },
    "present": {
        "require": [
            "aws.organizations.organization_unit.present",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    email: str,
    role_name: str = None,
    iam_user_access_to_billing: str = "ALLOW",
    resource_id: str = None,
    parent_id: str = None,
    tags: List[Dict[str, Any]] or Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Creates an AWS account that is automatically a member of the organization whose credentials made the request.

    Args:
        name(str):
            The name of the member account.
        email(str):
            The email address of the owner to assign to the new member account.
            This email address must not already be associated with another Amazon Web Services account.
            You must use a valid email address to complete account creation.
        role_name(str, Optional):
            The name of an IAM role that Organizations automatically preconfigures in the new member account.
            This role trusts the management account, allowing users in the management account to assume the role,
            as permitted by the management account administrator. The role has administrator permissions in the new member account.
            If you don't specify this parameter, the role name defaults to ``OrganizationAccountAccessRole``.
        iam_user_access_to_billing(str, Optional):
            If set to ``ALLOW``, the new account enables IAM users to access account billing information if they have the required permissions.
            If set to ``DENY``, only the root user of the new account can access account billing information.
            If you don't specify this parameter, the value defaults to ``ALLOW``.
        resource_id(str, Optional):
            The ID of the member account in Amazon Web Services.
        parent_id(str, Optional):
            Parent Organizational Unit ID or Root ID for the account. Defaults to the Organization default Root ID.
        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]`` to associate with the member account.

            * Key (*str*):
                The key identifier, or name, of the tag.
            * Value (*str*):
                The string value that's associated with the key of the tag.

    Request Syntax:
      .. code-block:: sls

        [idem_test_aws_organizations_account]:
          aws.organizations.account.present:
            - name: 'string'
            - resource_id: 'string'
            - email: 'string'
            - role_name: 'string'
            - iam_user_access_to_billing: 'ALLOW|DENY'
            - parent_id: 'string'
            - tags:
              - Key: 'string'
                Value: 'string

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_organizations_account:
              aws.organizations.account.present:
                - name: 'idem_test_account'
                - email: 'xyz@email.com'
                - role_name: 'idem_test_role'
                - iam_user_access_to_billing: 'ALLOW'
                - parent_id: 'o-parent-id'
                - tags:
                  - Key: 'provider'
                    Value: 'idem'
    """
    result = dict(comment=[], name=name, result=True, old_state=None, new_state=None)
    before = None
    update_tag = False
    update_parent = False

    if resource_id:
        before = await hub.exec.aws.organizations.account.get(
            ctx, resource_id=resource_id, name=name
        )
        if not before["result"]:
            result["result"] = before["result"]
            result["comment"] = before["comment"]
            return result

    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    if before and before["ret"]:
        # Account exists , update
        try:
            result["old_state"] = before["ret"]
            plan_state = copy.deepcopy(result["old_state"])
            # we need to list parents to check if move is required in case the new_parent_id is not equal to current_
            # parent_id
            current_parent_id = before["ret"]["parent_id"]
            if current_parent_id and parent_id and current_parent_id != parent_id:
                if not ctx.get("test", False):
                    move_account_result = (
                        await hub.tool.aws.organizations.account.move_account(
                            ctx, resource_id, result, parent_id
                        )
                    )
                    if move_account_result and not move_account_result["result"]:
                        result["comment"] += [
                            f"Could not update parent for aws.organizations.account {name}"
                        ]
                        result["result"] = False
                        return result
                update_parent = True
            if update_parent:
                plan_state["parent_id"] = parent_id
                result["comment"] += [
                    f"Would update parent for aws.organizations.account {name}"
                ]

            # update tags
            if tags is not None and tags != result["old_state"].get("tags"):
                update_tags_ret = await hub.tool.aws.organizations.tag.update_tags(
                    ctx, resource_id, result["old_state"].get("tags"), tags
                )
                if not update_tags_ret["result"]:
                    result["comment"] += update_tags_ret["comment"]
                    result["result"] = update_tags_ret["result"]
                    return result

                result["comment"] += [
                    f"Updated tags on aws.organizations.account '{name}'."
                ]
                update_tag = True
                if ctx.get("test", False):
                    if update_tags_ret["ret"]:
                        plan_state["tags"] = update_tags_ret["ret"]
                    else:
                        plan_state["tags"] = result["old_state"]["tags"]

        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False

    else:
        # Account not present , create
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "email": email,
                    "name": name,
                    "parent_id": parent_id,
                    "role_name": role_name,
                    "iam_user_access_to_billing": iam_user_access_to_billing,
                    "tags": tags,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.organizations.account", name=name
            )
            return result

        try:
            create_account_ret = (
                await hub.exec.boto3.client.organizations.create_account(
                    ctx,
                    Email=email,
                    AccountName=name,
                    RoleName=role_name,
                    IamUserAccessToBilling=iam_user_access_to_billing,
                    Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                    if tags
                    else None,
                )
            )

            result["result"] = create_account_ret["result"]
            if not result["result"]:
                result["comment"] += create_account_ret["comment"]
                return result

            account_status_id = create_account_ret["ret"]["CreateAccountStatus"]["Id"]

            # Call a custom waiter to wait on account's creation.

            acceptors = [
                {
                    "matcher": "path",
                    "expected": "SUCCEEDED",
                    "state": "success",
                    "argument": "CreateAccountStatus.State",
                },
                {
                    "matcher": "path",
                    "expected": "IN_PROGRESS",
                    "state": "retry",
                    "argument": "CreateAccountStatus.State",
                },
                {
                    "matcher": "path",
                    "expected": "FAILED",
                    # Failure is also mapped with success to catch the error message
                    "state": "success",
                    "argument": "CreateAccountStatus.State",
                },
            ]
            account_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
                name="AccountCreated",
                operation="DescribeCreateAccountStatus",
                argument=["CreateAccountStatus.State"],
                acceptors=acceptors,
                client=await hub.tool.boto3.client.get_client(ctx, SERVICE),
                matcher="path",
                delay=10,
                max_tries=10,
            )
            await hub.tool.boto3.client.wait(
                ctx,
                SERVICE,
                "AccountCreated",
                account_waiter,
                CreateAccountRequestId=account_status_id,
            )

            account_status = await hub.exec.boto3.client.organizations.describe_create_account_status(
                ctx, CreateAccountRequestId=account_status_id
            )
            if account_status["result"]:
                create_account_status = account_status["ret"]["CreateAccountStatus"]
                account_state = create_account_status["State"]
                if account_state == "FAILED":
                    result["result"] = False
                    result["comment"] += [create_account_status["FailureReason"]]
                    return result
                elif account_state == "SUCCEEDED":
                    resource_id = create_account_status["AccountId"]
                    result["comment"] = hub.tool.aws.comment_utils.create_comment(
                        resource_type="aws.organizations.account", name=name
                    )
                    if resource_id is not None and parent_id is not None:
                        parents = (
                            await hub.exec.boto3.client.organizations.list_parents(
                                ctx, ChildId=resource_id
                            )
                        )
                        result["result"] = result["result"] and parents["result"]
                        if not result["result"]:
                            result["comment"] += parents["comment"]
                            return result
                        if parents:
                            current_parent_id = parents["ret"]["Parents"][0]["Id"]
                            if current_parent_id != parent_id:
                                move_account_result = await hub.tool.aws.organizations.account.move_account(
                                    ctx, resource_id, result, parent_id
                                )
                                if (
                                    move_account_result
                                    and not move_account_result["result"]
                                ):
                                    result["comment"] += [
                                        f"Could not update parent for aws.organizations.account {name}"
                                    ]
                                    result["result"] = False
                                    return result
            else:
                result["result"] = False
                result["comment"] += account_status["comment"]
                return result

        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif not before or update_parent or update_tag and resource_id:
        try:
            after = await hub.exec.aws.organizations.account.get(
                ctx, resource_id=resource_id, name=name
            )
            if after and after.get("ret"):
                result["new_state"] = after["ret"]
            else:
                result["result"] = result["result"] and after["result"]
                if not result["result"]:
                    result["comment"] += after["comment"]
                    return result

        except Exception as e:
            result["comment"] += [str(e)]
            result["result"] = False

    else:
        result["new_state"] = copy.deepcopy(result["old_state"])

    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Removes the specified account from the organization.

    The removed account becomes a standalone account that isn't a member of any organization.
    It's no longer subject to any policies and is responsible for its own bill payments.
    The organization's management account is no longer charged for any expenses accrued by
    the member account after it's removed from the organization.
    This operation can be called only from the organization's management account.

    Args:
        name(str):
            The name of the member account.
        resource_id(str, Optional):
            The ID of the member account in Amazon Web Services.

    Request syntax:
      .. code-block:: sls

        [idem_test_aws_organizations_account]:
          aws.organizations.account.absent:
            - name: 'string'
            - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_organizations_account:
              aws.organizations.account.absent:
                - name: 'idem_test_account'
                - resource_id: '123456789012'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.organizations.account",
            name=name,
        )
        return result

    before = await hub.exec.aws.organizations.account.get(
        ctx, resource_id=resource_id, name=name
    )

    if not before["result"]:
        result["result"] = before["result"]
        result["comment"] = before["comment"]
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.organizations.account",
            name=name,
        )
    elif ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.organizations.account",
            name=name,
        )
    else:
        try:
            ret = await hub.exec.boto3.client.organizations.remove_account_from_organization(
                ctx, AccountId=resource_id
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] += ret["comment"]
                return result
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.organizations.account", name=name
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False

    if before:
        result["old_state"] = before["ret"]
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes AWS Organizations Accounts in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.organizations.account
    """
    result = {}

    describe_ret = await hub.exec.aws.organizations.account.list(ctx)
    if not describe_ret["ret"]:
        hub.log.warning(f"Could not list accounts {describe_ret['comment']}")
        return {}

    accounts = describe_ret["ret"]

    for account in accounts:
        account_id = account["resource_id"]
        result[account_id] = {
            "aws.organizations.account.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in account.items()
            ]
        }
    return result
