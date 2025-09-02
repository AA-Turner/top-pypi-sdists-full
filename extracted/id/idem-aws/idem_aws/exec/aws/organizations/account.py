"""Exec module for managing organization accounts."""
__func_alias__ = {"list_": "list"}

from typing import Dict, Any


async def get(hub, ctx, resource_id: str, name: str = None) -> Dict[str, Any]:
    """Get info about AWS Organizations account based on resource_id.

    Args:
        resource_id(str):
            AWS Organizations account id

        name(str, Optional):
            Name of the Idem state

    Returns:
        Dict[str, Any]:
            Returns account in present format

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.organizations.account.get name="get account" resource_id="account_id"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resources:
              exec.run:
                - path: aws.organizations.account.get
                - kwargs:
                    name: "get account info"
                    resource_id: "257230699585"
    """
    result = dict(result=True, ret=None, comment=[])
    ret = await hub.exec.boto3.client.organizations.describe_account(
        ctx, AccountId=resource_id
    )

    if not ret["result"]:
        if "AccountNotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.organizations.account", name=name
                )
            )
            return result
        result["result"] = ret["result"]
        result["comment"] += list(ret["comment"])
        return result

    account = ret["ret"]["Account"]
    if not account:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.organizations.account", name=name
            )
        )
        return result
    # get tags
    tags_ret = await hub.exec.boto3.client.organizations.list_tags_for_resource(
        ctx, ResourceId=resource_id
    )
    if not tags_ret["result"]:
        result["result"] = False
        result["comment"] += list(tags_ret["comment"])
        return result

    tags = None
    if tags_ret["ret"]["Tags"]:
        tags = tags_ret["ret"]["Tags"]

    # get parent_id
    parents_ret = await hub.exec.boto3.client.organizations.list_parents(
        ctx, ChildId=resource_id
    )
    if not parents_ret["result"]:
        result["result"] = False
        result["comment"] += list(parents_ret["comment"])
        return result

    current_parent_id = None
    if parents_ret["ret"]["Parents"]:
        current_parent_id = parents_ret["ret"]["Parents"][0]["Id"]

    result[
        "ret"
    ] = hub.tool.aws.organizations.conversion_utils.convert_raw_account_to_present(
        parent_id=current_parent_id, tags=tags, account=account
    )

    return result


async def list_(hub, ctx, name: str = None) -> Dict[str, Any]:
    """List AWS accounts in an organization.

    Args:
        name(str, Optional):
            Name of the Idem state.

    Returns:
        Dict[str, Any]:
            Returns organization accounts in present format

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.organizations.account.list name="list accounts"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resources:
              exec.run:
                - path: aws.organizations.account.list
                - kwargs:
                    name: my_accounts
    """

    result = dict(result=True, comment=[], ret=[])
    ret = await hub.exec.boto3.client.organizations.list_accounts(ctx)
    if not ret["result"]:
        result["result"] = ret["result"]
        result["comment"] += list(ret["comment"])
        return result

    if not ret["ret"]["Accounts"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.organizations.account", name=name
            )
        )
        return result
    for account in ret["ret"]["Accounts"]:
        account_id = account.get("Id")
        account_ret = await get(hub, ctx, resource_id=account_id)
        if not account_ret["result"]:
            hub.log.debug(
                f"Unable to get info for account: {account_id} Error:  {account_ret['comment']}. Hence skipping it in list"
            )
            continue
        result["ret"].append(account_ret["ret"])
    return result
