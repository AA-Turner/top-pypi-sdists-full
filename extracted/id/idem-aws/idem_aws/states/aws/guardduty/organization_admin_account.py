"""State module for enabling organization admin account for Guardduty."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(hub, ctx, name: str, resource_id: str) -> Dict[str, Any]:
    r"""Enables an Amazon Web Services account within the organization as the GuardDuty delegated administrator.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str):
            An identifier of the resource in the provider. Here it is the Amazon Web Services Account ID for the organization account to be enabled as a GuardDuty
            delegated administrator.


    Request Syntax:
      .. code-block:: sls
            resource_is_present:
              aws.guardduty.organization_admin_account.present:
                - name: 'string'
                - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws.guardduty.organization_admin_account.present:
                - name: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_created = False
    before = await hub.exec.aws.guardduty.organization_admin_account.list(
        ctx, name=name
    )
    if not before["result"]:
        result["result"] = before["result"]
        result["comment"] = before["comment"]
        return result
    if before and before["ret"]:
        admin_accounts = before["ret"]
        # list call might return more than one account, so check whether it contains resource_id
        filtered_admin_accounts = filter(
            lambda admin: admin.get("resource_id") == resource_id
            and admin.get("admin_status") == "ENABLED",
            admin_accounts,
        )
        accounts = list(filtered_admin_accounts)
        if len(accounts) != 0:
            # resource_id is already an admin
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                resource_type="aws.guardduty.organization_admin_account", name=name
            )
            result["old_state"] = accounts[0]
        else:
            # some other account is an admin, so end the operation
            enabled_account_id = admin_accounts[0]["resource_id"]
            result["comment"] = (
                f"{enabled_account_id} is already enabled as organization_admin_account. "
                f"{resource_id} can only be enabled if {enabled_account_id} is removed as organization_admin_account"
            )
            result["result"] = False
            return result
    else:
        resource_created = True
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_id": resource_id,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.guardduty.organization_admin_account", name=name
            )
            return result
        ret = await hub.exec.boto3.client.guardduty.enable_organization_admin_account(
            ctx, AdminAccountId=resource_id
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.guardduty.organization_admin_account", name=name
        )
    if resource_created:
        # fetch resource
        after = await hub.exec.aws.guardduty.organization_admin_account.list(
            ctx, name=name
        )
        if not after["result"]:
            result["result"] = after["result"]
            result["comment"] = after["comment"]
            return result
        admin_accounts = after["ret"]
        filtered_admin_accounts = filter(
            lambda admin: admin.get("resource_id") == resource_id
            and admin.get("admin_status") == "ENABLED",
            admin_accounts,
        )
        account = list(filtered_admin_accounts)[0]
        result["new_state"] = account
    else:
        # already exists
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    r"""Disables an Amazon Web Services account within the Organization as the GuardDuty delegated administrator.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            The Amazon Web Services Account ID for the organizations account to be disabled as a GuardDuty
            delegated administrator.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.guardduty.organization_admin_account.absent:
                - name: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = await hub.exec.aws.guardduty.organization_admin_account.list(
        ctx, name=name
    )
    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.guardduty.organization_admin_account", name=name
        )
    else:
        admin_accounts = before["ret"]
        # list call might return more than one account, so check whether it contains resource_id
        filtered_admin_accounts = filter(
            lambda admin: admin.get("resource_id") == resource_id
            and admin.get("admin_status") == "ENABLED",
            admin_accounts,
        )
        eligible_accounts = list(filtered_admin_accounts)
        if len(eligible_accounts) != 0:
            # resource_id is the admin, disable it
            eligible_account = eligible_accounts[0]
            if ctx.get("test", False):
                result["old_state"] = eligible_account
                result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                    resource_type="aws.guardduty.organization_admin_account", name=name
                )
                return result
            else:
                result["old_state"] = eligible_account
                try:
                    ret = await hub.exec.boto3.client.guardduty.disable_organization_admin_account(
                        ctx, AdminAccountId=resource_id
                    )
                    result["result"] = ret["result"]
                    if not result["result"]:
                        result["comment"] = ret["comment"]
                        return result
                    result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                        resource_type="aws.guardduty.organization_admin_account",
                        name=name,
                    )
                except hub.tool.boto3.exception.ClientError as e:
                    result["comment"] += [f"{e.__class__.__name__}: {e}"]
        else:
            # already absent
            result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
                resource_type="aws.guardduty.organization_admin_account", name=name
            )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Lists the accounts configured as GuardDuty delegated administrators.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.guardduty.organization_admin_account
    """
    result = {}
    ret = await hub.exec.aws.guardduty.organization_admin_account.list(
        ctx, name="list organization admins"
    )
    if not ret["result"]:
        hub.log.warning(f"Could not list organization_admin_account {ret['comment']}")
        return {}
    for organization_admin_account in ret["ret"]:
        resource_id = organization_admin_account["resource_id"]
        # to avoid any other state overriding describe if just resource_id is the state_id
        resource_key = f"aws-guardduty-org_admin_account-{resource_id}"
        result[resource_key] = {
            "aws.guardduty.organization_admin_account.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in organization_admin_account.items()
            ]
        }
    return result
