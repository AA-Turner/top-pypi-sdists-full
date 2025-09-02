from typing import Any
from typing import Dict


def convert_raw_backup_vault_to_present(
    hub, ctx, raw_resource: Dict[str, Any], vault_name: str
) -> Dict[str, Any]:
    """
    Convert the backup vault response to a common format

    Args:
        raw_resource: Dictionary of backup vault
        vault_name: Name of the backup vault.

    Returns:
        A dictionary of the backup vault
    """
    translated_resource = {}
    raw_resource.pop("ResponseMetadata", None)

    if raw_resource:
        translated_resource["name"] = vault_name
        translated_resource["resource_id"] = vault_name
        translated_resource["backup_vault_arn"] = raw_resource["BackupVaultArn"]
        translated_resource["encryption_key_arn"] = raw_resource["EncryptionKeyArn"]
        translated_resource["number_of_recovery_points"] = raw_resource[
            "NumberOfRecoveryPoints"
        ]
        if raw_resource.get("Tags") is not None:
            translated_resource["tags"] = raw_resource.get("Tags")

    return translated_resource
