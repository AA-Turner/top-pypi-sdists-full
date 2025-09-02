"""Exec module for managing Guardduty org admins."""
__func_alias__ = {"list_": "list"}

from typing import Dict


async def list_(hub, ctx, name: str = None) -> Dict:
    """List AWS Guardduty organization admin accounts.

    Fetch a list of organization admin accounts for AWS Guardduty. The function returns empty list when no resource is found.
    Only the organization's management account can run this API operation.

    Args:
        name(str, Optional):
            The name of the Idem state.

    Returns:
        Dict[str, Any]:
            Returns organization admin accounts in present format

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.guardduty.organization_admin_account.list name="list org admins"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resources:
              exec.run:
                - path: aws.guardduty.organization_admin_account.list
                - kwargs:
                    name: my_resources
    """
    result = dict(comment=[], ret=[], result=True)
    ret = await hub.exec.boto3.client.guardduty.list_organization_admin_accounts(ctx)
    if not ret["result"]:
        result["result"] = ret["result"]
        result["comment"] += list(ret["comment"])
        return result
    if not ret["ret"]["AdminAccounts"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.guardduty.organization_admin_account", name=name
            )
        )
        return result
    for admin_account in ret["ret"]["AdminAccounts"]:
        result["ret"].append(
            hub.tool.aws.guardduty.conversion_utils.convert_raw_org_admin_account_to_present(
                raw_resource=admin_account, idem_resource_name=name
            )
        )
    return result
