"""Exec functions for backup vault."""
from typing import Dict


__func_alias__ = {"list_": "list"}


async def get(hub, ctx, name: str, resource_id: str = None):
    """Returns the backup vault.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str):
            AWS Backup vault name.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.backup.backup_vault.get name="idem_name"

        Calling this exec module function from within a state module in pure python:

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await hub.exec.aws.backup.backup_vault.get(
                    ctx, name=name, resource_id=resource_id
                )
    """
    result = dict(comment=[], ret=None, result=True)

    if not resource_id:
        resource_id = name
    ret = await hub.exec.boto3.client.backup.describe_backup_vault(
        ctx, BackupVaultName=resource_id
    )
    if not ret["result"]:
        if "ResourceNotFoundException" or "ClientError:" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.backup.backup_vault", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["result"] = False
        result["comment"] += list(ret["comment"])
        return result

    if not ret["ret"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.backup.backup_vault", name=name
            )
        )
        result["comment"] += list(ret["comment"])
        return result

    arn = ret["ret"]["BackupVaultArn"]
    tags_ret = await hub.exec.boto3.client.backup.list_tags(ctx, ResourceArn=arn)
    if not tags_ret["result"]:
        result["result"] = False
        result["comment"] = tags_ret["comment"]
        return result

    if tags_ret["ret"].get("Tags"):
        ret["ret"]["Tags"] = tags_ret["ret"]["Tags"]

    result[
        "ret"
    ] = hub.tool.aws.backup.conversion_utils.convert_raw_backup_vault_to_present(
        ctx=ctx,
        raw_resource=ret["ret"],
        vault_name=resource_id,
    )

    return result


async def list_(hub, ctx, name: str = None) -> Dict:
    """Fetch a list of backup vaults from AWS.

    The function returns empty list when no resource is found.

    Args:
        name (str, Optional):
            The name of the Idem state for logging.

    Returns:
        Dict[bool, list, dict or None]:

        result(bool):
            Whether the result of the function has been successful (``True``) or not (``False``).
        comment(list):
            A list of messages.
        ret(dict or None):
           The AWS backup vault list in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.backup.backup_vault.list name="idem_name"

        Calling this exec module function from within a state module in pure python:

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await hub.exec.aws.backup.backup_vault.list(ctx, name)

    """
    result = dict(comment=[], ret=[], result=True)

    ret = await hub.exec.boto3.client.backup.list_backup_vaults(ctx)

    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["BackupVaultList"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.backup.backup_vault", name=name
            )
        )
        return result

    for backup_vault in ret["ret"]["BackupVaultList"]:
        tags_ret = await hub.exec.boto3.client.backup.list_tags(
            ctx, ResourceArn=backup_vault.get("BackupVaultArn")
        )

        if not tags_ret["result"]:
            result["result"] = False
            result["comment"] = tags_ret["comment"]
            return result

        if tags_ret["ret"].get("Tags"):
            backup_vault["Tags"] = tags_ret["ret"]["Tags"]

        result["ret"].append(
            hub.tool.aws.backup.conversion_utils.convert_raw_backup_vault_to_present(
                ctx=ctx,
                raw_resource=backup_vault,
                vault_name=backup_vault["BackupVaultName"],
            )
        )
    return result
