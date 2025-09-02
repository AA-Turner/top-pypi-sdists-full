"""State module for managing backup vault."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    encryption_key_arn: str = None,
    creator_request_id: str = None,
    tags: Dict[str, str] = None,
) -> Dict[str, Any]:
    """Create/Update the backup vault.

    Creates a logical container where backups are stored. A CreateBackupVault request includes a name, optionally one or
    more resource tags, an encryption key, and a request ID.

    Args:
        name(str):
            An Idem name of the resource.
            The name of a logical container where backups are stored. Backup vaults are identified by names that are
            unique to the account used to create them and the Amazon Web Services Region where they are created.
            They consist of letters, numbers, and hyphens.

        resource_id(str, Optional):
            An Idem resource id of the resource as well as name of the backup vault.

        encryption_key_arn(str, Optional):
            The server-side encryption key that is used to protect your backups;
            for example, arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab .

        creator_request_id(str, Optional):
            A unique string that identifies the request and allows failed requests to be retried without the risk of
            running the operation twice. This parameter is optional.
            If used, this parameter must contain 1 to 50 alphanumeric or '-_.' characters.

        tags(dict, Optional):
            Metadata that you can assign to help organize the resources that you create. Each tag is a key-value pair.

    Request Syntax:
        .. code-block:: sls

            vault_name:
              aws.backup.backup_vault.present:
              - name: "string"
              - resource_id: "string"
              - encryption_key_arn: "string"
              - creator_request_id: "string"
              - tags: "dict"


    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws.backup.backup_vault.present:
                - name: idem_backup_vault
                - resource_id: idem_backup_vault
                - encryption_key_arn: arn:aws:kms:us-east-1:011922870716:key/ff4fd718-612c-4d0f-8172-8150025bb4fa
                - tags:
                    name: backup_vault
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False

    if resource_id:
        before = await hub.exec.aws.backup.backup_vault.get(
            ctx, resource_id=resource_id, name=name
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.backup.backup_vault", name=name
        )
        result["old_state"] = copy.deepcopy(before["ret"])
        result["new_state"] = copy.deepcopy(result["old_state"])

        if tags is not None and tags != result["old_state"].get("tags"):
            update_ret = await hub.tool.aws.backup.tag.update_tags(
                ctx=ctx,
                backup_vault_arn=result["old_state"].get("backup_vault_arn"),
                old_tags=result["old_state"].get("tags"),
                new_tags=tags,
            )
            result["comment"] = update_ret["comment"]
            if not update_ret["result"]:
                result["result"] = False
                return result

            resource_updated = resource_updated or bool(update_ret["ret"])
            if update_ret["ret"] and ctx.get("test", False):
                result["new_state"].update(update_ret["ret"])
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.backup.backup_vault", name=name
                )
            if resource_updated and ctx.get("test", False):
                return result
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "encryption_key_arn": encryption_key_arn,
                    "creator_request_id": creator_request_id,
                    "tags": tags,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.backup.backup_vault", name=name
            )
            return result
        create_ret = await hub.exec.boto3.client.backup.create_backup_vault(
            ctx,
            BackupVaultName=name,
            EncryptionKeyArn=encryption_key_arn,
            CreatorRequestId=creator_request_id,
            BackupVaultTags=tags if tags else None,
        )

        if not create_ret["result"]:
            result["result"] = False
            result["comment"] = create_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.backup.backup_vault", name=name
        )
        resource_id = name

    if (not result["old_state"]) or resource_updated:
        after_ret = await hub.exec.aws.backup.backup_vault.get(
            ctx, name=name, resource_id=resource_id
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
    resource_id: str = None,
) -> Dict[str, Any]:
    """Deletes the backup vault.

    Deletes the backup vault identified by its name. A vault can be deleted only if it is empty.

    Args:
        name(str): Idem name of the backup vault.
        resource_id(str): Name of the backup vault to be deleted, Idem automatically considers this resource being
            absent if this field is not specified.

    Request Syntax:
        .. code-block:: sls

            vault_name:
              aws.backup.backup_vault.absent:
                - name: "string"
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            vault_name:
              aws.backup.backup_vault.absent:
                - name: idem_backup_vault
                - resource_id: idem_backup_vault
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.backup.backup_vault", name=name
        )
        return result

    before = await hub.exec.aws.backup.backup_vault.get(
        ctx, resource_id=resource_id, name=name
    )

    if not before["result"] and not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.backup.backup_vault", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.backup.backup_vault", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        delete_ret = await hub.exec.boto3.client.backup.delete_backup_vault(
            ctx, BackupVaultName=resource_id
        )
        if not delete_ret["result"]:
            result["result"] = False
            result["comment"] = delete_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.backup.backup_vault", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Gets information about the backup vault.

    Returns a list of recovery point storage containers along with information about them.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.backup.backup_Vault
    """

    result = {}
    ret = await hub.exec.aws.backup.backup_vault.list(ctx, "backup_vault")
    if not ret["result"]:
        hub.log.warning(f"Could not describe backup vault {ret['comment']}")
        return {}

    for backup_vault in ret["ret"]:
        vault_name = backup_vault.get("name")

        result[vault_name] = {
            "aws.backup.backup_vault.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in backup_vault.items()
            ]
        }
    return result
