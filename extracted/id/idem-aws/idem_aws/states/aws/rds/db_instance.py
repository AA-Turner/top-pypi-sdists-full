"""State operations for RDS db_instance"""
import copy
from collections import OrderedDict
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    db_instance_class: str,
    engine: str,
    resource_id: str = None,
    db_name: str = None,
    allocated_storage: int = None,
    master_username: str = None,
    master_user_password: str = None,
    db_security_groups: List[str] = None,
    vpc_security_group_ids: List[str] = None,
    availability_zone: str = None,
    db_subnet_group_name: str = None,
    preferred_maintenance_window: str = None,
    db_parameter_group_name: str = None,
    backup_retention_period: int = None,
    preferred_backup_window: str = None,
    port: int = None,
    multi_az: bool = None,
    engine_version: str = None,
    auto_minor_version_upgrade: bool = None,
    license_model: str = None,
    iops: int = None,
    option_group_name: str = None,
    character_set_name: str = None,
    nchar_character_set_name: str = None,
    publicly_accessible: bool = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass("Tag", [("Key", str), ("Value", str, field(default=None))])
    ] = None,
    db_cluster_identifier: str = None,
    storage_type: str = None,
    tde_credential_arn: str = None,
    tde_credential_password: str = None,
    storage_encrypted: bool = None,
    kms_key_id: str = None,
    domain: str = None,
    copy_tags_to_snapshot: bool = None,
    monitoring_interval: int = None,
    monitoring_role_arn: str = None,
    domain_iam_role_name: str = None,
    promotion_tier: int = None,
    timezone: str = None,
    enable_iam_database_authentication: bool = None,
    enable_performance_insights: bool = None,
    performance_insights_kms_key_id: str = None,
    performance_insights_retention_period: int = None,
    enable_cloudwatch_logs_exports: List[str] = None,
    processor_features: List[
        make_dataclass(
            "ProcessorFeatureList",
            [("Name", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
    deletion_protection: bool = None,
    max_allocated_storage: int = None,
    enable_customer_owned_ip: bool = None,
    custom_iam_instance_profile: str = None,
    backup_target: str = None,
    apply_immediately: bool = None,
    allow_major_version_upgrades: bool = None,
    ca_certificate_identifier: str = None,
    cloudwatch_logs_export_configuration: Dict = None,
    use_default_processor_features: bool = None,
    certificate_rotation_restart: bool = None,
    replica_mode: str = None,
    aws_backup_recovery_point_arn: str = None,
    automation_mode: str = None,
    resume_full_automation_mode_minutes: int = None,
    domain_auth_secret_arn: str = None,
    manage_master_user_password: bool = None,
    master_user_secret_kms_key_id: str = None,
    timeout: make_dataclass(
        "Timeout",
        [
            (
                "create",
                make_dataclass(
                    "CreateTimeout",
                    [
                        ("delay", int, field(default=None)),
                        ("max_attempts", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "update",
                make_dataclass(
                    "UpdateTimeout",
                    [
                        ("delay", int, field(default=None)),
                        ("max_attempts", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
) -> Dict[str, Any]:
    r'''
    Creates a new DB instance.

    Args:
        name(str):
            Idem name to identify the resource

        allocated_storage(int):
            The amount of storage in gibibytes (GiB) to allocate for the DB instance

        db_instance_class(str):
            The compute and memory capacity of the DB instance, for example db.m4.large

        engine(str):
            The name of the database engine to be used for this instance

        resource_id(str, Optional):
            AWS Id of the resource

        db_name(str, Optional):
            Name of the database

        master_username(str, Optional):
            The name for the master user.Not required for aurora

        master_user_password(str, Optional):
            The password for the master user. The password can include any printable ASCII character except "/", """,
            or "@". Not required for aurora

        db_security_groups(list, Optional):
            A list of DB security groups to associate with this DB instance

        vpc_security_group_ids(list, Optional):
            A list of DB security groups to associate with this DB instance

        availability_zone(str, Optional):
            The Availability Zone (AZ) where the database will be created

        db_subnet_group_name(str, Optional):
            A DB subnet group to associate with this DB instance

        preferred_maintenance_window(str, Optional):
            The time range each week during which system maintenance can occur, in Universal Coordinated Time (UTC)

        db_parameter_group_name(str, Optional):
            The name of the DB parameter group to associate with this DB instance. If you do not specify a value, then
            the default DB parameter group for the specified DB engine and version is used.

        backup_retention_period(int, Optional):
            The number of days for which automated backups are retained. Setting this parameter to a positive number
            enables backups. Setting this parameter to 0 disables automated backups.

        preferred_backup_window(str, Optional):
            The daily time range during which automated backups are created if automated backups are enabled,using the
            BackupRetentionPeriod parameter.

        port(int, Optional):
            The port number on which the database accepts connections.

        multi_az(bool, Optional):
            A value that indicates whether the DB instance is a Multi-AZ deployment. You can't set the AvailabilityZone
            parameter if the DB instance is a Multi-AZ deployment.

        engine_version(str, Optional):
            The version number of the database engine to use.

        auto_minor_version_upgrade(bool, Optional):
            A value that indicates whether minor engine upgrades are applied automatically to the DB instance during
            the maintenance window. By default, minor engine upgrades are applied automatically.

        license_model(str, Optional):
            License model information for this DB instance.

        iops(int, Optional):
            The amount of Provisioned IOPS (input/output operations per second) to be initially allocated for the DB
            instance.

        option_group_name(str, Optional):
            A value that indicates that the DB instance should be associated with the
            specified option group.

        character_set_name(str, Optional):
            For supported engines, this value indicates that the DB instance should be associated with the specified
            CharacterSet.

        nchar_character_set_name(str, Optional):
            The name of the NCHAR character set for the Oracle DB instance.

        publicly_accessible(bool, Optional):
            A value that indicates whether the DB instance is publicly accessible.

        tags(Dict or List, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of ``[{"Key": tag-key,
            "Value": tag-value}]`` to associate with the DB instance.  Each tag consists of a key name and an
            associated value. Defaults to None.

            * Key (str, Optional): The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of
              127 Unicode characters. May not begin with aws:.

            * Value(str, Optional): The value of the tag. Constraints: Tag values are case-sensitive and accept a
              maximum of 256 Unicode characters.

        db_cluster_identifier(str, Optional):
            The identifier of the DB cluster that the instance will belong to.

        storage_type(str, Optional):
            Specifies the storage type to be associated with the DB instance.

        tde_credential_arn(str, Optional):
            The ARN from the key store with which to associate the instance for TDE encryption.

        tde_credential_password(str, Optional):
            The password for the given ARN from the key store in order to access the device.

        storage_encrypted(bool, Optional):
            A value that indicates whether the DB instance is encrypted. By default, it isn't encrypted

        kms_key_id(str, Optional):
            The Amazon Web Services KMS key identifier for an encrypted DB instance.

        domain(str, Optional):
            The Active Directory, directory ID to create the DB instance in

        copy_tags_to_snapshot(str, Optional):
            A value that indicates whether to copy tags from the DB instance to snapshots of the DB instance. By
            default, tags are not copied.

        monitoring_interval(int, Optional):
            The interval, in seconds, between points when Enhanced Monitoring metrics are collected for the DB
            instance.To disable collection of Enhanced Monitoring metrics, specify 0. The default is 0.  If
            MonitoringRoleArn is specified, then you must set MonitoringInterval to a value other than 0.

        monitoring_role_arn(str, Optional):
            The ARN for the IAM role that permits RDS to send enhanced monitoring metrics to Amazon CloudWatch Logs.

        domain_iam_role_name(str, Optional):
            Specify the name of the IAM role to be used when making API calls to the Directory Service.

        promotion_tier(int, Optional):
            A value that specifies the order in which an Aurora Replica is promoted to the primary instance after a
            failure of the existing primary instance.

        timezone(str, Optional):
            The time zone of the DB instance.

        enable_iam_database_authentication(bool, Optional):
            A value that indicates whether to enable mapping of Amazon Web Services Identity and Access Management
            (IAM) accounts to database accounts. By default, mapping isn't enabled.

        enable_performance_insights(bool, Optional):
            A value that indicates whether to enable Performance Insights for the DB instance.

        performance_insights_kms_key_id(str, Optional):
            The Amazon Web Services KMS key identifier for encryption of Performance Insights data.

        performance_insights_retention_period(int, Optional):
            The amount of time, in days, to retain Performance Insights data.

        enable_cloudwatch_logs_exports(List, Optional):
            The list of log types that need to be enabled for exporting to CloudWatch Logs. The values in the list
            depend on the DB engine.

        processor_features(List[Dict[str, Any]], Optional):
            The number of CPU cores and the number of threads per core for the DB instance class of the DB instance.
            This setting doesn't apply to RDS Custom. Defaults to None.

            * Name (str, Optional): The name of the processor feature. Valid names are coreCount and threadsPerCore.

            * Value (str, Optional): The value of a processor feature name.

        deletion_protection(bool, Optional):
            A value that indicates whether the DB instance has deletion protection enabled. The database can't be
            deleted when deletion protection is enabled.  By default, deletion protection isn't enabled.

        max_allocated_storage(int, Optional):
            The upper limit in gigabytes (GiB) to which Amazon RDS can automatically scale the storage of the DB
            instance.

        enable_customer_owned_ip(bool, Optional):
            A value that indicates whether to enable a customer-owned IP address (CoIP) for an RDS on Outposts DB
            instance.

        custom_iam_instance_profile(str, Optional):
            The instance profile associated with the underlying Amazon EC2 instance of an RDS Custom DB instance.

        backup_target(str, Optional):
            Value to specify where automated backups and manual snapshots are stored.

        apply_immediately(bool, Optional):
            A value that indicates whether the modifications in this request and any pending modifications are
            asynchronously applied as soon as possible, regardless of the PreferredMaintenanceWindow setting for the DB
            instance.  By default, this parameter is disabled.

        allow_major_version_upgrades(bool, Optional):
            A value that indicates whether major version upgrades are allowed.  Changing this parameter doesn't result
            in an outage and the change is asynchronously applied as soon as possible.

        cloudwatch_logs_export_configuration(Dict, Optional):
            The configuration setting for the log types to be enabled for export to CloudWatch Logs for a specific DB
            instance.

        ca_certificate_identifier(str, Optional):
            The identifier of the CA certificate for the DB instance.

        use_default_processor_features(bool, Optional):
            A value that indicates whether the DB instance class of the DB instance uses its default processor
            features.

        certificate_rotation_restart(bool, Optional):
            A value that indicates whether the DB instance is restarted when you rotate your SSL/TLS certificate.

        replica_mode(str, Optional):
            A value that sets the open mode of a replica database to either mounted or read-only

        aws_backup_recovery_point_arn(str, Optional):
            The Amazon Resource Name (ARN) of the recovery point in Amazon Web Services Backup.

        automation_mode(str, Optional):
            The automation mode of the RDS Custom DB instance: full or all paused.

        resume_full_automation_mode_minutes(int, Optional):
            The number of minutes to pause the automation. When the time period ends, RDS Custom resumes full
            automation

        domain_auth_secret_arn(str, Optional): The ARN for the Secrets Manager secret that contains the credentials
            for the user performing the domain join.
            Example: arn:aws:secretsmanager:region:account-number:secret:myselfmanagedADtestsecret-123456.
            Defaults to None.

        manage_master_user_password(bool, Optional): Specifies whether to manage the master user password with Amazon Web Services Secrets Manager.
            For more information, see Password management with Amazon Web Services Secrets Manager in the
            Amazon RDS User Guide.  Constraints:   Can't manage the master user password with Amazon Web
            Services Secrets Manager if MasterUserPassword is specified. Defaults to None.

        master_user_secret_kms_key_id(str, Optional): The Amazon Web Services KMS key identifier to encrypt a secret that is automatically generated
            and managed in Amazon Web Services Secrets Manager. This setting is valid only if the master
            user password is managed by RDS in Amazon Web Services Secrets Manager for the DB instance. The
            Amazon Web Services KMS key identifier is the key ARN, key ID, alias ARN, or alias name for the
            KMS key. To use a KMS key in a different Amazon Web Services account, specify the key ARN or
            alias ARN. If you don't specify MasterUserSecretKmsKeyId, then the aws/secretsmanager KMS key is
            used to encrypt the secret. If the secret is in a different Amazon Web Services account, then
            you can't use the aws/secretsmanager KMS key to encrypt the secret, and you must use a customer
            managed KMS key. There is a default KMS key for your Amazon Web Services account. Your Amazon
            Web Services account has a different default KMS key for each Amazon Web Services Region. Defaults to None.

        timeout(Dict, Optional):
            Timeout configuration for create/update of AWS DB Cluster.

            * create (Dict) -- Timeout configuration for creating DB Instance
              * delay(int) -- The amount of time in seconds to wait between attempts.Defaults to 30
              * max_attempts(int) -- Customized timeout configuration containing delay and max attempts.Defaults to 60

            * update (Dict) -- Timeout configuration for updating DB Instance
              * delay(int) -- The amount of time in seconds to wait between attempts.Defaults to 30
              * max_attempts(int) -- Customized timeout configuration containing delay and max attempts.Defaults to 60


    Request Syntax:
        .. code-block:: sls

          [db-instance-name]:
            aws.rds.db_instance.present:
              - db_instance_class: 'string'
              - engine: 'string'
              - resource_id: 'string'
              - availability_zone: 'string'
              - preferred_maintenance_window: 'string'
              - multi_az: 'bool'
              - engine_version: 'string'
              - auto_minor_version_upgrade: 'bool'
              - license_model: 'string'
              - publicly_accessible: 'bool'
              - db_cluster_identifier: 'string'
              - storage_type: 'string'
              - storage_encrypted: 'bool'
              - copy_tags_to_snapshot: 'bool'
              - monitoring_interval: 'int'
              - monitoring_role_arn: 'string'
              - promotion_tier: 'int'
              - enable_performance_insights: 'bool'
              - performance_insights_kms_key_id: 'string'
              - performance_insights_retention_period: 'int'
              - backup_target: 'string'
              - vpc_security_group_id: 'List'
              - db_subnet_group_name: 'string'
              - db_parameter_group_name: 'string'
              - option_group_name: 'string'
              - tags: 'List'
              - timeout: 'Dict'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

              instance-1:
                aws.rds.db_instance.present:
                - db_instance_class: db.r5.large
                - engine: aurora-postgresql
                - availability_zone: us-east-2b
                - preferred_maintenance_window: sat:04:15-sat:04:45
                - multi_az: false
                - engine_version: '12.7'
                - auto_minor_version_upgrade: true
                - license_model: postgresql-license
                - publicly_accessible: false
                - db_cluster_identifier: db-cluster-1
                - storage_type: aurora
                - storage_encrypted: true
                - copy_tags_to_snapshot: false
                - monitoring_interval: 60
                - monitoring_role_arn: arn:aws:iam::537227425989:role/rds-monitoring-role
                - promotion_tier: 1
                - enable_performance_insights: true
                - performance_insights_kms_key_id: arn:aws:kms:us-east-2:537227425989:key/e9e79921-8dda-48d7-afd7-38a64dd8e9b1
                - performance_insights_retention_period: 7
                - backup_target: region
                - vpc_security_group_id:
                  - sg-f5eeba9c
                - db_subnet_group_name: default
                - db_parameter_group_name: default.aurora-postgresql12
                - option_group_name: default:aurora-postgresql-12
                - tags:
                  - Key: name
                    Value: value
                - timeout:
                    create:
                      delay: 10
                      max_attempts: 30

    '''
    result = {
        "comment": [],
        "old_state": None,
        "new_state": None,
        "name": name,
        "result": True,
    }
    params_to_modify = {}
    plan_state = None
    before = None
    resource_updated = False

    if resource_id:
        before = await hub.exec.aws.rds.db_instance.get(
            ctx,
            resource_id=resource_id,
        )
    tags = (
        hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
        if isinstance(tags, List)
        else tags
    )
    if before and before.get("ret"):
        db_instance_arn = before["ret"].get("db_instance_arn")
        before["ret"]["name"] = before["ret"].get("tags", {}).get("Name", name)
        ret_tags = await hub.exec.boto3.client.rds.list_tags_for_resource(
            ctx, ResourceName=db_instance_arn
        )
        if not ret_tags["result"]:
            result["comment"] = ret_tags["comment"]
            result["result"] = False
            return result
        result["old_state"] = before["ret"]
        plan_state = copy.deepcopy(result["old_state"])
        old_tags = plan_state.get("tags")

        if tags is not None:
            update_tags_ret = await hub.exec.aws.rds.tag.update_rds_tags(
                ctx,
                resource_arn=db_instance_arn,
                old_tags=old_tags,
                new_tags=tags,
            )
            result["comment"] = update_tags_ret["comment"]
            if not update_tags_ret["result"]:
                result["result"] = False
                return result
            resource_updated = update_tags_ret["result"]
            if ctx.get("test", False) and update_tags_ret["result"]:
                plan_state["tags"] = update_tags_ret["ret"]

        modify_params = OrderedDict(
            {
                "AllocatedStorage": "allocated_storage",
                "DBInstanceClass": "db_instance_class",
                "MasterUserPassword": "master_user_password",
                "DBSecurityGroups": "db_security_groups",
                "VpcSecurityGroupIds": "vpc_security_group_ids",
                "DBSubnetGroupName": "db_subnet_group_name",
                "PreferredMaintenanceWindow": "preferred_maintenance_window",
                "DBParameterGroupName": "db_parameter_group_name",
                "BackupRetentionPeriod": "backup_retention_period",
                "PreferredBackupWindow": "preferred_backup_window",
                "MultiAZ": "multi_az",
                "EngineVersion": "engine_version",
                "AllowMajorVersionUpgrade": "allow_major_version_upgrades",
                "AutoMinorVersionUpgrade": "auto_minor_version_upgrade",
                "LicenseModel": "license_model",
                "Iops": "iops",
                "OptionGroupName": "option_group_name",
                "StorageType": "storage_type",
                "TdeCredentialArn": "tde_credential_arn",
                "TdeCredentialPassword": "tde_credential_password",
                "CACertificateIdentifier": "ca_certificate_identifier",
                "Domain": "domain",
                "CopyTagsToSnapshot": "copy_tags_to_snapshot",
                "MonitoringInterval": "monitoring_interval",
                "DBPortNumber": "port",
                "PubliclyAccessible": "publicly_accessible",
                "MonitoringRoleArn": "monitoring_role_arn",
                "DomainIAMRoleName": "domain_iam_role_name",
                "PromotionTier": "promotion_tier",
                "EnableIAMDatabaseAuthentication": "enable_iam_database_authentication",
                "EnablePerformanceInsights": "enable_performance_insights",
                "PerformanceInsightsKMSKeyId": "performance_insights_kms_key_id",
                "PerformanceInsightsRetentionPeriod": "performance_insights_retention_period",
                "CloudwatchLogsExportConfiguration": "cloudwatch_logs_export_configuration",
                "ProcessorFeatures": "processor_features",
                "UseDefaultProcessorFeatures": "use_default_processor_features",
                "DeletionProtection": "deletion_protection",
                "MaxAllocatedStorage": "max_allocated_storage",
                "CertificateRotationRestart": "certificate_rotation_restart",
                "ReplicaMode": "replica_mode",
                "EnableCustomerOwnedIp": "enable_customer_owned_ip",
                "AwsBackupRecoveryPointArn": "aws_backup_recovery_point_arn",
                "AutomationMode": "automation_mode",
                "ResumeFullAutomationModeMinutes": "resume_full_automation_mode_minutes",
                "DomainAuthSecretArn": "domain_auth_secret_arn",
                "ManageMasterUserPassword": "manage_master_user_password",
                "MasterUserSecretKmsKeyId": "master_user_secret_kms_key_id",
            }
        )
        for parameter_raw, parameter_present in modify_params.items():
            # Add to modify list only if parameter is changed
            if (
                locals()[parameter_present] is not None
                and result["old_state"].get(parameter_present)
                != locals()[parameter_present]
            ):
                params_to_modify[parameter_raw] = locals()[parameter_present]

        if params_to_modify:
            if ctx.get("test", False):
                result["comment"] += [f"Would update aws.rds.db_instance '{name}'"]
                for key, value in params_to_modify.items():
                    plan_state[modify_params.get(key)] = value
            else:
                # apply_immediately is only used in update to decide whether to apply the update immediate or not
                # this property is not returned in describe, so this should not be compared with old_state as this
                # property will not be present in old_state.
                if apply_immediately is not None:
                    params_to_modify["ApplyImmediately"] = apply_immediately
                modify_ret = await hub.exec.boto3.client.rds.modify_db_instance(
                    ctx, DBInstanceIdentifier=resource_id, **params_to_modify
                )
                if not modify_ret["result"]:
                    result["comment"] += modify_ret["comment"]
                    result["result"] = False
                    return result
                # Waiting for the DBInstances status to be available after updates
                waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                    default_delay=30,
                    default_max_attempts=60,
                    timeout_config=timeout.get("update") if timeout else None,
                )
                try:
                    await hub.tool.boto3.client.wait(
                        ctx,
                        "rds",
                        "db_instance_available",
                        None,
                        30,
                        DBInstanceIdentifier=resource_id,
                        WaiterConfig=waiter_config,
                    )
                except Exception as e:
                    result["comment"] += [str(e)]
                    result["result"] = False

                resource_updated = resource_updated or modify_ret["result"]
                result["comment"] += [
                    f"Updated aws.rds.db_instance '{name}'.updated parameters '{params_to_modify}'"
                ]

    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "db_name": db_name,
                    "allocated_storage": allocated_storage,
                    "db_instance_class": db_instance_class,
                    "engine": engine,
                    "master_username": master_username,
                    "master_user_password": master_user_password,
                    "db_security_groups": db_security_groups,
                    "vpc_security_group_ids": vpc_security_group_ids,
                    "availability_zone": availability_zone,
                    "db_subnet_group_name": db_subnet_group_name,
                    "preferred_maintenance_window": preferred_maintenance_window,
                    "db_parameter_group_name": db_parameter_group_name,
                    "backup_retention_period": backup_retention_period,
                    "preferred_backup_window": preferred_backup_window,
                    "port": port,
                    "multi_az": multi_az,
                    "engine_version": engine_version,
                    "auto_minor_version_upgrade": auto_minor_version_upgrade,
                    "license_model": license_model,
                    "iops": iops,
                    "option_group_name": option_group_name,
                    "character_set_name": character_set_name,
                    "nchar_character_set_name": nchar_character_set_name,
                    "publicly_accessible": publicly_accessible,
                    "tags": tags,
                    "db_cluster_identifier": db_cluster_identifier,
                    "storage_type": storage_type,
                    "tde_credential_arn": tde_credential_arn,
                    "tde_credential_password": tde_credential_password,
                    "storage_encrypted": storage_encrypted,
                    "kms_key_id": kms_key_id,
                    "domain": domain,
                    "copy_tags_to_snapshot": copy_tags_to_snapshot,
                    "monitoring_interval": monitoring_interval,
                    "monitoring_role_arn": monitoring_role_arn,
                    "domain_iam_role_name": domain_iam_role_name,
                    "promotion_tier": promotion_tier,
                    "timezone": timezone,
                    "enable_iam_database_authentication": enable_iam_database_authentication,
                    "enable_performance_insights": enable_performance_insights,
                    "performance_insights_kms_key_id": performance_insights_kms_key_id,
                    "performance_insights_retention_period": performance_insights_retention_period,
                    "enable_cloudwatch_logs_exports": enable_cloudwatch_logs_exports,
                    "processor_features": processor_features,
                    "deletion_protection": deletion_protection,
                    "max_allocated_storage": max_allocated_storage,
                    "enable_customer_owned_ip": enable_customer_owned_ip,
                    "custom_iam_instance_profile": custom_iam_instance_profile,
                    "backup_target": backup_target,
                    "domain_auth_secret_arn": domain_auth_secret_arn,
                    "manage_master_user_password": manage_master_user_password,
                    "master_user_secret_kms_key_id": master_user_secret_kms_key_id,
                },
            )
            result["comment"] += [f"Would create aws.rds.db_instance '{name}'"]
            return result
        ret = await hub.exec.boto3.client.rds.create_db_instance(
            ctx,
            DBInstanceIdentifier=name,
            DBName=db_name,
            AllocatedStorage=allocated_storage,
            DBInstanceClass=db_instance_class,
            Engine=engine,
            MasterUsername=master_username,
            MasterUserPassword=master_user_password,
            DBSecurityGroups=db_security_groups,
            VpcSecurityGroupIds=vpc_security_group_ids,
            AvailabilityZone=availability_zone,
            DBSubnetGroupName=db_subnet_group_name,
            PreferredMaintenanceWindow=preferred_maintenance_window,
            DBParameterGroupName=db_parameter_group_name,
            BackupRetentionPeriod=backup_retention_period,
            PreferredBackupWindow=preferred_backup_window,
            Port=port,
            MultiAZ=multi_az,
            EngineVersion=engine_version,
            AutoMinorVersionUpgrade=auto_minor_version_upgrade,
            LicenseModel=license_model,
            Iops=iops,
            OptionGroupName=option_group_name,
            CharacterSetName=character_set_name,
            NcharCharacterSetName=nchar_character_set_name,
            PubliclyAccessible=publicly_accessible,
            Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
            if tags
            else None,
            DBClusterIdentifier=db_cluster_identifier,
            StorageType=storage_type,
            TdeCredentialArn=tde_credential_arn,
            TdeCredentialPassword=tde_credential_password,
            StorageEncrypted=storage_encrypted,
            KmsKeyId=kms_key_id,
            Domain=domain,
            CopyTagsToSnapshot=copy_tags_to_snapshot,
            MonitoringInterval=monitoring_interval,
            MonitoringRoleArn=monitoring_role_arn,
            DomainIAMRoleName=domain_iam_role_name,
            PromotionTier=promotion_tier,
            Timezone=timezone,
            EnableIAMDatabaseAuthentication=enable_iam_database_authentication,
            EnablePerformanceInsights=enable_performance_insights,
            PerformanceInsightsKMSKeyId=performance_insights_kms_key_id,
            PerformanceInsightsRetentionPeriod=performance_insights_retention_period,
            EnableCloudwatchLogsExports=enable_cloudwatch_logs_exports,
            ProcessorFeatures=processor_features,
            DeletionProtection=deletion_protection,
            MaxAllocatedStorage=max_allocated_storage,
            EnableCustomerOwnedIp=enable_customer_owned_ip,
            CustomIamInstanceProfile=custom_iam_instance_profile,
            BackupTarget=backup_target,
            DomainAuthSecretArn=domain_auth_secret_arn,
            ManageMasterUserPassword=manage_master_user_password,
            MasterUserSecretKmsKeyId=master_user_secret_kms_key_id,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        resource_id = ret["ret"]["DBInstance"]["DBInstanceIdentifier"]
        # Waiting until the DBInstance creation
        waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
            default_delay=30,
            default_max_attempts=60,
            timeout_config=timeout.get("create") if timeout else None,
        )
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "rds",
                "db_instance_available",
                DBInstanceIdentifier=resource_id,
                WaiterConfig=waiter_config,
            )
        except Exception as e:
            result["comment"] += [str(e)]
            result["result"] = False
        result["comment"] += [f"Created aws.rds.db_instance '{name}'"]

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif (not before) or resource_updated:
        after = await hub.exec.aws.rds.db_instance.get(
            ctx,
            resource_id=resource_id,
        )
        after["ret"]["name"] = name
        db_instance_arn = after["ret"].get("db_instance_arn")
        ret_tags = await hub.exec.boto3.client.rds.list_tags_for_resource(
            ctx, ResourceName=db_instance_arn
        )
        if not ret_tags["result"]:
            result["comment"] += ret_tags["comment"]
            result["result"] = False
        result["new_state"] = after["ret"]
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])

    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    skip_final_snapshot: bool = False,
    final_db_snapshot_identifier: str = None,
    timeout: Dict = None,
) -> Dict[str, Any]:
    """
    The DeleteDBInstance action deletes a previously provisioned DB instance. When you delete a DB instance, all
    automated backups for that instance are deleted and can't be recovered. Manual DB snapshots of the DB instance
    to be deleted by DeleteDBInstance are not deleted.  If you request a final DB snapshot the status of the Amazon
    RDS DB instance is deleting until the DB snapshot is created. The API action DescribeDBInstance is used to
    monitor the status of this operation. The action can't be canceled or reverted once submitted.  When a DB
    instance is in a failure state and has a status of failed, incompatible-restore, or incompatible-network, you
    can only delete it when you skip creation of the final snapshot with the SkipFinalSnapshot parameter. If the
    specified DB instance is part of an Amazon Aurora DB cluster, you can't delete the DB instance if both of the
    following conditions are true:   The DB cluster is a read replica of another Amazon Aurora DB cluster.   The DB
    instance is the only instance in the DB cluster.   To delete a DB instance in this case, first call the
    PromoteReadReplicaDBCluster API action to promote the DB cluster so it's no longer a read replica. After the
    promotion completes, then call the DeleteDBInstance API action to delete the final instance in the DB cluster.

    Args:
        name(str):
            Idem name to identify the resource.

        resource_id(str, Optional):
            AWS ID to identify the resource.

        skip_final_snapshot(bool, Optional):
            Mention this true if you want to skip creating snapshot default is false.

        final_db_snapshot_identifier(str, Optional):
            Identifier for the created final db_snapshot.

        timeout(Dict, Optional): Timeout configuration for deletion of AWS DB Instance.

            * delete (Dict) -- Timeout configuration for deletion of a DB Instance
              * delay(int) -- The amount of time in seconds to wait between attempts.Defaults to 30
              * max_attempts(int) -- Customized timeout configuration containing delay and max attempts.Defaults to 60

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            test-db-instance:
              aws.rds.db_instance.absent:
                - resource_id: test-db-instance,
                - skip_final_snapshot: true
    """
    result = {
        "comment": [],
        "old_state": None,
        "new_state": None,
        "name": name,
        "result": True,
    }

    before = await hub.exec.aws.rds.db_instance.get(
        ctx,
        resource_id=resource_id,
    )

    if not before["ret"]:
        result["comment"] += [f"aws.rds.db_instance '{name}' already absent"]
    else:
        db_instance_arn = before["ret"].get("db_instance_arn")
        ret_tags = await hub.exec.boto3.client.rds.list_tags_for_resource(
            ctx, ResourceName=db_instance_arn
        )
        if not ret_tags["result"]:
            result["comment"] = ret_tags["comment"]
            result["result"] = False
            return result
        result["old_state"] = before["ret"]
        if ctx.get("test", False):
            result["comment"] += [f"Would delete aws.rds.db_instance '{name}'"]
            return result
        ret = await hub.exec.boto3.client.rds.delete_db_instance(
            ctx,
            DBInstanceIdentifier=resource_id,
            SkipFinalSnapshot=skip_final_snapshot,
            FinalDBSnapshotIdentifier=final_db_snapshot_identifier,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result
        # Waiting for the DBInstance to Delete
        waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
            default_delay=30,
            default_max_attempts=60,
            timeout_config=timeout.get("delete") if timeout else None,
        )
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "rds",
                "db_instance_deleted",
                DBInstanceIdentifier=resource_id,
                WaiterConfig=waiter_config,
            )
        except Exception as e:
            result["comment"] += [str(e)]
            result["result"] = False
        result["comment"] += [f"Deleted aws.rds.db_instance '{name}'"]

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function


    Returns information about provisioned RDS instances. This API supports pagination.  This operation can also
    return information for Amazon Neptune DB instances and Amazon DocumentDB instances.


    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.rds.db_instance
    """

    result = {}
    ret = await hub.exec.aws.rds.db_instance.list(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe db_instance {ret['comment']}")
        return result
    for db_instance in ret["ret"]:
        # Including fields to match the 'present' function parameters
        resource_id = db_instance.get("resource_id")
        db_instance["name"] = db_instance.get("tags", {}).get("Name", resource_id)
        db_instance_arn = db_instance.get("db_instance_arn")
        ret_tags = await hub.exec.boto3.client.rds.list_tags_for_resource(
            ctx, ResourceName=db_instance_arn
        )
        resource_translated = db_instance
        result[resource_id] = {
            "aws.rds.db_instance.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result
