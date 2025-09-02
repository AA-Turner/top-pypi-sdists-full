import json
from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List


def convert_raw_db_instance_to_present(
    hub,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
    tags: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    Convert AWS returned data structure to idem neptune db_instance present state.
    Following parameters are part of present but are not available as part of describe:
    - master_user_password
    - tde_credential_password
    Following parameter is not part of present and is ignored from describe:
    - db_instance_status

    Args:
        hub: required for functions in hub
        raw_resource: The aws response to convert
        idem_resource_name (str, Optional): The idem name of the resource
        tags (Dict, Optional): The tags of the resource. Defaults to None.

    Returns: Valid idem state for neptune db_instance of type Dict['string', Any]
    """
    resource_id = raw_resource.get("DBInstanceIdentifier")
    raw_resource["Tags"] = dict(tags) if tags else None
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    resource_parameters = OrderedDict(
        {
            "DBInstanceIdentifier": "db_instance_identifier",
            "DBInstanceClass": "db_instance_class",
            "Engine": "engine",
            "DBName": "db_name",
            "AllocatedStorage": "allocated_storage",
            "MasterUsername": "master_username",
            "DBSecurityGroups": "db_security_groups",
            "AvailabilityZone": "availability_zone",
            "PreferredMaintenanceWindow": "preferred_maintenance_window",
            "BackupRetentionPeriod": "backup_retention_period",
            "PreferredBackupWindow": "preferred_backup_window",
            "DBInstancePort": "port",
            "MultiAZ": "multi_az",
            "EngineVersion": "engine_version",
            "AutoMinorVersionUpgrade": "auto_minor_version_upgrade",
            "LicenseModel": "license_model",
            "Iops": "iops",
            "CharacterSetName": "character_set_name",
            "PubliclyAccessible": "publicly_accessible",
            "Tags": "tags",
            "DBClusterIdentifier": "db_cluster_identifier",
            "StorageType": "storage_type",
            "TdeCredentialArn": "tde_credential_arn",
            "StorageEncrypted": "storage_encrypted",
            "KmsKeyId": "kms_key_id",
            "CopyTagsToSnapshot": "copy_tags_to_snapshot",
            "MonitoringInterval": "monitoring_interval",
            "MonitoringRoleArn": "monitoring_role_arn",
            "PromotionTier": "promotion_tier",
            "Timezone": "timezone",
            "IAMDatabaseAuthenticationEnabled": "enable_iam_database_authentication",
            "PerformanceInsightsEnabled": "enable_performance_insights",
            "PerformanceInsightsKMSKeyId": "performance_insights_kms_key_id",
            "EnabledCloudwatchLogsExports": "enable_cloudwatch_logs_exports",
            "DBInstanceArn": "db_instance_arn",
            "DeletionProtection": "deletion_protection",
        }
    )
    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw) is not None:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    # lambda to extract values from dict containing a list of dict
    list_processor = lambda r, a, b: [e.get(b) for e in r.get(a)]
    get_first = lambda l: next((e for e in l if e is not None), None)

    # process the VpcSecurityGroups which is a list of object to map it as list of vpc security group id strings
    if raw_resource.get("VpcSecurityGroups") is not None:
        resource_translated["vpc_security_group_ids"] = list_processor(
            r=raw_resource, a="VpcSecurityGroups", b="VpcSecurityGroupId"
        )

    # process db parameter group name
    if raw_resource.get("DBParameterGroups") is not None:
        # even though this is returned as list, we are only allowed to associate one DB parameter group per instance, so below should execute once
        db_param_grp_name = get_first(
            list_processor(
                r=raw_resource, a="DBParameterGroups", b="DBParameterGroupName"
            )
        )
        if db_param_grp_name:
            resource_translated["db_parameter_group_name"] = db_param_grp_name

    # process for option_group_name
    if raw_resource.get("OptionGroupMemberships") is not None:
        option_group_name = get_first(
            list_processor(
                r=raw_resource, a="OptionGroupMemberships", b="OptionGroupName"
            )
        )
        if option_group_name:
            resource_translated["option_group_name"] = option_group_name

    # process domain and domain_iam_role_name
    if raw_resource.get("DomainMemberships") is not None:
        domain = get_first(
            list_processor(r=raw_resource, a="DomainMemberships", b="Domain")
        )
        if domain:
            resource_translated["domain"] = domain

        domain_iam_role_name = get_first(
            list_processor(r=raw_resource, a="DomainMemberships", b="DomainIAMRoleName")
        )
        if domain_iam_role_name:
            resource_translated["domain_iam_role_name"] = domain_iam_role_name

    # process db_subnet_group_name
    if raw_resource.get("DBSubnetGroup") is not None:
        db_subnet_group_name = raw_resource["DBSubnetGroup"].get("DBSubnetGroupName")
        if db_subnet_group_name:
            resource_translated["db_subnet_group_name"] = db_subnet_group_name
    return resource_translated


def convert_raw_db_cluster_parameter_group_to_present(
    hub,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
    parameters: List[Dict[str, Any]] = None,
    tags: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    Convert AWS returned data structure to correct idem db_cluster_parameter_group present state

     Args:
        hub: required for functions in hub
        raw_resource: The aws response to convert
        idem_resource_name (str, Optional): The idem of the idem resource
        parameters (List, Optional): The DBClusterParameterGroup Parameters.
        tags (List, Optional): The tags of the resource. Defaults to None.

    Returns: Valid idem state for db_cluster_parameter_group of type Dict['string', Any]
    """
    resource_id = raw_resource.get("DBClusterParameterGroupName")
    raw_resource["Tags"] = tags
    raw_resource["Parameters"] = parameters
    resource_parameters = OrderedDict(
        {
            "DBParameterGroupFamily": "db_parameter_group_family",
            "Description": "description",
            "Tags": "tags",
            "Parameters": "parameters",
            "DBClusterParameterGroupArn": "db_cluster_parameter_group_arn",
        }
    )
    resource_translated = {
        "name": idem_resource_name if idem_resource_name else resource_id,
        "resource_id": resource_id,
    }
    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw) is not None:
            resource_translated[parameter_present] = json.loads(
                json.dumps(raw_resource.get(parameter_raw))
            )
    return resource_translated


def convert_raw_db_parameter_group_to_present(
    hub,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
    parameters: List[Dict[str, Any]] = None,
    tags: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    Convert AWS returned data structure to correct idem db_parameter_group present state

     Args:
        hub: required for functions in hub
        raw_resource: The aws response to convert
        idem_resource_name (str, Optional): The idem of the idem resource
        parameters (List[Dict[str, str]], Optional): The Parameter list of the resource. Defaults to None.
        tags (Dict, Optional): The tags of the resource. Defaults to None.

    Returns: Valid idem state for db_parameter_group of type Dict['string', Any]
    """
    resource_id = raw_resource.get("DBParameterGroupName")
    raw_resource["Tags"] = tags
    raw_resource["Parameters"] = parameters
    resource_parameters = OrderedDict(
        {
            "DBParameterGroupFamily": "db_parameter_group_family",
            "Description": "description",
            "Tags": "tags",
            "Parameters": "parameters",
            "DBParameterGroupArn": "db_parameter_group_arn",
        }
    )
    resource_translated = {
        "name": idem_resource_name if idem_resource_name else resource_id,
        "resource_id": resource_id,
    }
    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw) is not None:
            resource_translated[parameter_present] = json.loads(
                json.dumps(raw_resource.get(parameter_raw))
            )
    return resource_translated
