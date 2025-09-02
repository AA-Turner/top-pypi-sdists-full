"""State module for AWS neptune DB instance."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

STATE_NAME = "aws.neptune.db_instance"


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    *,
    db_instance_class: str,
    engine: str,
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
    publicly_accessible: bool = None,
    tags: Dict[str, Any],
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
    enable_cloudwatch_logs_exports: List[str] = None,
    deletion_protection: bool = None,
    apply_immediately: bool = None,
    allow_major_version_upgrade: bool = None,
    ca_certificate_identifier: str = None,
    cloudwatch_logs_export_configuration: make_dataclass(
        """Cloudwatch log export configuration dataclass."""
        "CloudwatchLogsExportConfiguration",
        [
            ("EnableLogTypes", List[str], field(default=None)),
            ("DisableLogTypes", List[str], field(default=None)),
        ],
    ) = None,
    timeout: make_dataclass(
        """Timeout configuration dataclass.""" "Timeout",
        [
            (
                "create",
                make_dataclass(
                    "CreateTimeout",
                    [
                        ("delay", int, field(default=15)),
                        ("max_attempts", int, field(default=40)),
                    ],
                ),
                field(default=None),
            ),
            (
                "update",
                make_dataclass(
                    "UpdateTimeout",
                    [
                        ("delay", int, field(default=15)),
                        ("max_attempts", int, field(default=40)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
) -> Dict[str, Any]:
    """Creates a new DB instance.

    Args:
        name(str):
            An Idem name of the resource. This is also DB instance identifier during resource creation. This
            parameter is stored as a lowercase string.
            Constraints:   Must contain from 1 to 63 letters, numbers, or hyphens.   First character must be a letter.
            Cannot end with a hyphen or contain two consecutive hyphens.   Example: mydbinstance.
        resource_id(str, Optional):
            AWS Neptune DBInstanceIdentifier to identify the resource. Defaults to None.
        db_name(str, Optional):
            Not supported. Defaults to None.
        allocated_storage(int, Optional):
            Not supported by Neptune. Defaults to None.
        db_instance_class(str):
            The compute and memory capacity of the DB instance, for example, db.m4.large. Not all DB
            instance classes are available in all Amazon Regions.
        engine(str):
            The name of the database engine to be used for this instance. Valid Values: neptune.
        master_username(str, Optional):
            Not supported by Neptune. Defaults to None.
        master_user_password(str, Optional):
            Not supported by Neptune. Defaults to None.
        db_security_groups(list[str], Optional):
            A list of DB security groups to associate with this DB instance. Default: The default DB
            security group for the database engine. Defaults to None.
        vpc_security_group_ids(list[str], Optional):
            A list of EC2 VPC security groups to associate with this DB instance. Not applicable. The
            associated list of EC2 VPC security groups is managed by the DB cluster. For more information,
            see CreateDBCluster. Default: The default EC2 VPC security group for the DB subnet group's VPC. Defaults to None.
        availability_zone(str, Optional):
            The EC2 Availability Zone that the DB instance is created in Default: A random, system-chosen
            Availability Zone in the endpoint's Amazon Region.  Example: us-east-1d   Constraint: The
            AvailabilityZone parameter can't be specified if the MultiAZ parameter is set to true. The
            specified Availability Zone must be in the same Amazon Region as the current endpoint. Defaults to None.
        db_subnet_group_name(str, Optional):
            A DB subnet group to associate with this DB instance. If there is no DB subnet group, then it is
            a non-VPC DB instance. Defaults to None.
        preferred_maintenance_window(str, Optional):
            The time range each week during which system maintenance can occur, in Universal Coordinated
            Time (UTC).  Format: ``ddd:hh24:mi-ddd:hh24:mi``  The default is a 30-minute window selected at
            random from an 8-hour block of time for each Amazon Region, occurring on a random day of the
            week. Valid Days: Mon, Tue, Wed, Thu, Fri, Sat, Sun. Constraints: Minimum 30-minute window. Defaults to None.
        db_parameter_group_name(str, Optional):
            The name of the DB parameter group to associate with this DB instance. If this argument is
            omitted, the default DBParameterGroup for the specified engine is used. Constraints:   Must be 1
            to 255 letters, numbers, or hyphens.   First character must be a letter   Cannot end with a
            hyphen or contain two consecutive hyphens. Defaults to None.
        backup_retention_period(int, Optional):
            The number of days for which automated backups are retained. Not applicable. The retention
            period for automated backups is managed by the DB cluster. For more information, see
            CreateDBCluster. Default: 1 Constraints:   Must be a value from 0 to 35   Cannot be set to 0 if
            the DB instance is a source to Read Replicas. Defaults to None.
        preferred_backup_window(str, Optional):
            The daily time range during which automated backups are created. Not applicable. The daily time
            range for creating automated backups is managed by the DB cluster. For more information, see
            CreateDBCluster. Defaults to None.
        port(int, Optional):
            The port number on which the database accepts connections. Not applicable. The port is managed
            by the DB cluster. For more information, see CreateDBCluster.  Default: 8182  Type: Integer. Defaults to None.
        multi_az(bool, Optional):
            Specifies if the DB instance is a Multi-AZ deployment. You can't set the AvailabilityZone
            parameter if the MultiAZ parameter is set to true. Defaults to None.
        engine_version(str, Optional):
            The version number of the database engine to use. Currently, setting this parameter has no
            effect. Defaults to None.
        auto_minor_version_upgrade(bool, Optional):
            Indicates that minor engine upgrades are applied automatically to the DB instance during the
            maintenance window. Default: true. Defaults to None.
        license_model(str, Optional):
            License model information for this DB instance.  Valid values: license-included | bring-your-
            own-license | general-public-license. Defaults to None.
        iops(int, Optional):
            The amount of Provisioned IOPS (input/output operations per second) to be initially allocated
            for the DB instance. Defaults to None.
        option_group_name(str, Optional):
            (Not supported by Neptune). Defaults to None.
        character_set_name(str, Optional):
            (Not supported by Neptune). Defaults to None.
        publicly_accessible(bool, Optional):
            This flag should no longer be used. Defaults to None.
        tags(dict, Optional):
            Dict in the format of {tag-key: tag-value} to associate with the VPC.
            Each tag consists of a key name and an associated value. Defaults to None.

            * Key (str, Optional):
                The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode
                characters. May not begin with aws:.

            * Value(str, Optional):
                The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256
                Unicode characters.
        db_cluster_identifier(str, Optional):
            The identifier of the DB cluster that the instance will belong to. For information on creating a
            DB cluster, see CreateDBCluster. Type: String. Defaults to None.
        storage_type(str, Optional):
            Specifies the storage type to be associated with the DB instance. Not applicable. Storage is
            managed by the DB Cluster. Defaults to None.
        tde_credential_arn(str, Optional):
            The ARN from the key store with which to associate the instance for TDE encryption. Defaults to None.
        tde_credential_password(str, Optional):
            The password for the given ARN from the key store in order to access the device. Defaults to None.
        storage_encrypted(bool, Optional):
            Specifies whether the DB instance is encrypted. Not applicable. The encryption for DB instances
            is managed by the DB cluster. For more information, see CreateDBCluster. Default: false. Defaults to None.
        kms_key_id(str, Optional):
            The Amazon KMS key identifier for an encrypted DB instance. The KMS key identifier is the Amazon
            Resource Name (ARN) for the KMS encryption key. If you are creating a DB instance with the same
            Amazon account that owns the KMS encryption key used to encrypt the new DB instance, then you
            can use the KMS key alias instead of the ARN for the KM encryption key. Not applicable. The KMS
            key identifier is managed by the DB cluster. For more information, see CreateDBCluster. If the
            StorageEncrypted parameter is true, and you do not specify a value for the KmsKeyId parameter,
            then Amazon Neptune will use your default encryption key. Amazon KMS creates the default
            encryption key for your Amazon account. Your Amazon account has a different default encryption
            key for each Amazon Region. Defaults to None.
        domain(str, Optional):
            Specify the Active Directory Domain to create the instance in. Defaults to None.
        copy_tags_to_snapshot(bool, Optional):
            True to copy all tags from the DB instance to snapshots of the DB instance, and otherwise false.
            The default is false. Defaults to None.
        monitoring_interval(int, Optional):
            The interval, in seconds, between points when Enhanced Monitoring metrics are collected for the
            DB instance. To disable collecting Enhanced Monitoring metrics, specify 0. The default is 0. If
            MonitoringRoleArn is specified, then you must also set MonitoringInterval to a value other than
            0. Valid Values: 0, 1, 5, 10, 15, 30, 60. Defaults to None.
        monitoring_role_arn(str, Optional):
            The ARN for the IAM role that permits Neptune to send enhanced monitoring metrics to Amazon
            CloudWatch Logs. For example, arn:aws:iam:123456789012:role/emaccess. If MonitoringInterval is
            set to a value other than 0, then you must supply a MonitoringRoleArn value. Defaults to None.
        domain_iam_role_name(str, Optional):
            Specify the name of the IAM role to be used when making API calls to the Directory Service. Defaults to None.
        promotion_tier(int, Optional):
            A value that specifies the order in which an Read Replica is promoted to the primary instance
            after a failure of the existing primary instance.  Default: 1 Valid Values: 0 - 15. Defaults to None.
        timezone(str, Optional):
            The time zone of the DB instance. Defaults to None.
        enable_iam_database_authentication(bool, Optional):
            Not supported by Neptune (ignored). Defaults to None.
        enable_performance_insights(bool, Optional):
            (Not supported by Neptune). Defaults to None.
        performance_insights_kms_key_id(str, Optional):
            (Not supported by Neptune). Defaults to None.
        enable_cloudwatch_logs_exports(list[str], Optional):
            The list of log types that need to be enabled for exporting to CloudWatch Logs. Defaults to None.
        deletion_protection(bool, Optional):
            A value that indicates whether the DB instance has deletion protection enabled. The database
            can't be deleted when deletion protection is enabled. By default, deletion protection is
            disabled. See Deleting a DB Instance. DB instances in a DB cluster can be deleted even when
            deletion protection is enabled in their parent DB cluster. Defaults to None.
        apply_immediately(bool, Optional):
            Specifies whether the modifications in this request and any pending modifications are asynchronously applied as soon as possible, regardless of the PreferredMaintenanceWindow setting for the DB instance.
            If this parameter is set to false , changes to the DB instance are applied during the next maintenance window. Some parameter changes can cause an outage and are applied on the next call to RebootDBInstance , or the next failure reboot.
            Default: false
        allow_major_version_upgrade(bool, Optional):
            Indicates that major version upgrades are allowed. Changing this parameter doesn't result in an outage and the change is asynchronously applied as soon as possible.
        ca_certificate_identifier(str, Optional):
            Indicates the certificate that needs to be associated with the instance.
        cloudwatch_logs_export_configuration(dict[str, Any], Optional):
            The configuration setting for the log types to be enabled for export to CloudWatch Logs for a specific DB instance.

            * EnableLogTypes (list[str], Optional):
                The list of log types to enable.

            * DisableLogTypes(list[str], Optional):
                The list of log types to disable.
        timeout(dict, Optional):
            Timeout configuration for create/update of AWS DB Instance.

            * create (*dict, Optional*):
                Timeout configuration for creating DB Cluster.

                * delay(*int, Optional*):
                    The amount of time in seconds to wait between attempts.

                * max_attempts(*int, Optional*):
                    Customized timeout configuration containing delay and max attempts.

            * update(*dict, Optional*):
                Timeout configuration for updating DB instance.

                * delay(*int, Optional*):
                    The amount of time in seconds to wait between attempts.

                * max_attempts(*int, Optional*):
                    Customized timeout configuration containing delay and max attempts.

    Request Syntax:
        .. code-block:: sls

            [idem_test_aws_neptune_db_instance]:
                  aws.neptune.db_instance.present:
                      - name: 'string'
                      - resource_id: 'string'
                      - db_instance_identifier: 'string'
                      - db_instance_class: 'string'
                      - engine: 'string'
                      - allocated_storage: 'integer'
                      - master_username: 'string'
                      - db_security_groups:
                            - 'string'
                            - 'string'
                      - availability_zone: 'string'
                      - preferred_maintenance_window: 'string'
                      - backup_retention_period: 'integer'
                      - preferred_backup_window: 'string'
                      - multi_az: 'boolean'
                      - engine_version: 'string'
                      - auto_minor_version_upgrade: 'boolean'
                      - license_model: 'string'
                      - publicly_accessible: 'boolean'
                      - db_cluster_identifier: 'string'
                      - storage_type: 'string'
                      - storage_encrypted: 'boolean'
                      - kms_key_id: 'string'
                      - copy_tags_to_snapshot: 'boolean'
                      - monitoring_interval: 'integer'
                      - promotion_tier: 'integer'
                      - enable_iam_database_authentication: 'boolean'
                      - enable_performance_insights: 'boolean'
                      - enable_cloudwatch_logs_exports:
                        - 'string'
                      - db_instance_arn: 'string'
                      - deletion_protection: 'boolean'
                      - vpc_security_group_ids:
                        - 'string'
                      - db_parameter_group_name: 'string'
                      - option_group_name: 'string'
                      - db_subnet_group_name: 'string'

    Returns:
        Dict[str, Dict[str,Any]]

    Examples:
        .. code-block:: sls

            database-1-instance-1:
              aws.neptune.db_instance.present:
                  - name: database-1-instance-1
                  - resource_id: database-1-instance-1
                  - db_instance_identifier: database-1-instance-1
                  - db_instance_class: db.t3.medium
                  - engine: neptune
                  - allocated_storage: 1
                  - master_username: admin
                  - db_security_groups: []
                  - availability_zone: ca-central-1d
                  - preferred_maintenance_window: sun:03:07-sun:03:37
                  - backup_retention_period: 1
                  - preferred_backup_window: 06:18-06:48
                  - multi_az: false
                  - engine_version: 1.1.1.0
                  - auto_minor_version_upgrade: true
                  - license_model: amazon-license
                  - publicly_accessible: false
                  - db_cluster_identifier: database-1
                  - storage_type: aurora
                  - storage_encrypted: true
                  - kms_key_id: arn:aws:kms:ca-central-1:746014882121:key/2a4a587a-04fb-4c3b-b4d5-c3f25fb7f69f
                  - copy_tags_to_snapshot: false
                  - monitoring_interval: 0
                  - promotion_tier: 1
                  - enable_iam_database_authentication: false
                  - enable_performance_insights: false
                  - enable_cloudwatch_logs_exports:
                    - audit
                  - db_instance_arn: arn:aws:rds:ca-central-1:746014882121:db:database-1-instance-1
                  - deletion_protection: false
                  - vpc_security_group_ids:
                    - sg-ad5a2ac5
                  - db_parameter_group_name: default.neptune1
                  - option_group_name: default:neptune-1-1
                  - db_subnet_group_name: default
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    # when creating, below is the desired state of resource
    desired_state = {
        "name": name,
        "resource_id": name,
        "db_instance_class": db_instance_class,
        "engine": engine,
        "db_name": db_name,
        "allocated_storage": allocated_storage,
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
        "enable_cloudwatch_logs_exports": enable_cloudwatch_logs_exports,
        "deletion_protection": deletion_protection,
    }
    # set a flag to keep track if the resource is newly created
    is_created = False

    if not resource_id:
        # if there is no resource_id, it is expected that we create the resource
        # if this is test run, just generate the new state and set in result
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={}, desired_state=desired_state
            )
            resource_id = desired_state["resource_id"]
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type=STATE_NAME, name=name
            )
        else:
            # if this is not a test run, create the real instance
            create_db_instance_result = (
                await hub.exec.boto3.client.neptune.create_db_instance(
                    ctx,
                    DBName=db_name,
                    DBInstanceIdentifier=name,
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
                    PubliclyAccessible=publicly_accessible,
                    Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
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
                    EnableCloudwatchLogsExports=enable_cloudwatch_logs_exports,
                    DeletionProtection=deletion_protection,
                )
            )
            # if create failed, fail the request
            if not create_db_instance_result["result"]:
                result["comment"] = create_db_instance_result["comment"]
                result["result"] = False
                return result

            # using the resource_id, wait till db instance is created
            resource_id = create_db_instance_result["ret"]["DBInstance"][
                "DBInstanceIdentifier"
            ]
            waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                default_delay=15,
                default_max_attempts=40,
                timeout_config=timeout.get("create") if timeout else None,
            )
            try:
                await hub.tool.boto3.client.wait(
                    ctx,
                    "neptune",
                    "db_instance_available",
                    DBInstanceIdentifier=resource_id,
                    WaiterConfig=waiter_config,
                )
                result["comment"] = hub.tool.aws.comment_utils.create_comment(
                    resource_type=STATE_NAME, name=name
                )
            except Exception as e:
                result["comment"] += [str(e)]
                result["result"] = False
                return result
        is_created = True

    # neptune db_instance has some parameters that can only be modified, so if
    # the user specifies modification parameters during creation of new db instance, idem will
    # create the instance and also modify it so that desired state is obtained
    desired_state["apply_immediately"] = apply_immediately
    desired_state[
        "cloudwatch_logs_export_configuration"
    ] = cloudwatch_logs_export_configuration
    desired_state["ca_certificate_identifier"] = ca_certificate_identifier
    desired_state["allow_major_version_upgrade"] = allow_major_version_upgrade

    update_db_instance_result = await hub.tool.aws.neptune.db_instance.update(
        ctx=ctx,
        name=name,
        resource_id=resource_id,
        desired_state=desired_state,
        is_created=is_created,
        timeout=timeout,
    )
    if not (
        update_db_instance_result
        and update_db_instance_result["result"]
        and update_db_instance_result["new_state"]
    ):
        result["result"] = False
        result["comment"] = update_db_instance_result["comment"]
        return result

    result["old_state"] = update_db_instance_result["old_state"]
    result["new_state"] = update_db_instance_result["new_state"]
    # update the result comment if the resource is not being created
    if not is_created:
        result["comment"] = update_db_instance_result["comment"]

    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    skip_final_snapshot: bool = None,
    final_db_snapshot_identifier: str = None,
    timeout: make_dataclass(
        """Timeout configuration.""" "Timeout",
        [
            (
                "delete",
                make_dataclass(
                    "DeleteTimeout",
                    [
                        ("delay", int, field(default=15)),
                        ("max_attempts", int, field(default=40)),
                    ],
                ),
                field(default=None),
            )
        ],
    ) = None,
) -> Dict[str, Any]:
    """Deletes a previously provisioned DB instance.

    When you delete a DB instance, all automated backups for that instance are deleted and can't be recovered.
    Manual DB snapshots of the DB instance to be deleted by DeleteDBInstance are not deleted.  If you request a final
    DB snapshot the status of the Amazon Neptune DB instance is deleting until the DB snapshot is created.
    The API action DescribeDBInstance is used to monitor the status of this operation. The action can't be canceled or
    reverted once submitted. Note that when a DB instance is in a failure state and has a status of failed,
    incompatible-restore, or incompatible-network, you can only delete it when the SkipFinalSnapshot parameter is set
    to true. You can't delete a DB instance if it is the only instance in the DB cluster, or if it has deletion
    protection enabled.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            AWS Neptune DBInstanceIdentifier to identify the resource. This parameter isn't case-
            sensitive. Idem automatically considers the resource being absent if resource_id is not specified.
            Constraints: Must match the name of an existing DB instance.
        skip_final_snapshot(bool, Optional):
            Determines whether a final DB snapshot is created before the DB instance is deleted. If true is
            specified, no DBSnapshot is created. If false is specified, a DB snapshot is created before the
            DB instance is deleted. Note that when a DB instance is in a failure state and has a status of
            'failed', 'incompatible-restore', or 'incompatible-network', it can only be deleted when the
            SkipFinalSnapshot parameter is set to "true". Specify true when deleting a Read Replica.  The
            FinalDBSnapshotIdentifier parameter must be specified if SkipFinalSnapshot is false.  Default:
            false. Defaults to None.
        final_db_snapshot_identifier(str, Optional):
            The DBSnapshotIdentifier of the new DBSnapshot created when SkipFinalSnapshot is set to false.
            Specifying this parameter and also setting the SkipFinalShapshot parameter to true results in an
            error.  Constraints:   Must be 1 to 255 letters or numbers.   First character must be a letter
            Cannot end with a hyphen or contain two consecutive hyphens   Cannot be specified when deleting
            a Read Replica. Defaults to None.
        timeout(dict, Optional):
            Timeout configuration for create/update of AWS DB Instance.

            * delete (*dict, Optional*):
                Timeout configuration for deleting DB Instance.

                * delay(*int, Optional*):
                    The amount of time in seconds to wait between attempts.

                * max_attempts(*int, Optional*):
                    Customized timeout configuration containing delay and max attempts.

    Request Syntax:
        .. code-block:: sls

            [idem_test_aws_neptune_db_instance]:
                aws.neptune.db_instance.absent:
                    - name: 'string'
                    - resource_id: 'string'
                    - skip_final_snapshot: 'boolean'
                    - final_db_snapshot_identifier: 'string'
                    - timeout:
                        delete:
                            delay: int
                            max_attempts: int

    Returns:
        Dict[str, Dict[str,Any]]

    Examples:
        .. code-block:: sls

            database-1-instance-1:
                aws.neptune.db_instance.absent:
                    - name: database-1-instance-1
                    - resource_id: database-1-instance-1
                    - skip_final_snapshot: True
    """
    already_absent_msg = hub.tool.aws.comment_utils.already_absent_comment(
        resource_type=STATE_NAME, name=name
    )
    result = dict(
        comment=already_absent_msg,
        old_state=None,
        new_state=None,
        name=name,
        result=True,
    )
    if not resource_id:
        return result
    before = await hub.exec.aws.neptune.db_instance.get(
        ctx, name=name, resource_id=resource_id
    )
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result
    if not before["ret"]:
        return result
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type=STATE_NAME, name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client.neptune.delete_db_instance(
            ctx,
            DBInstanceIdentifier=resource_id,
            SkipFinalSnapshot=skip_final_snapshot,
            FinalDBSnapshotIdentifier=final_db_snapshot_identifier,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type=STATE_NAME, name=name
        )

        # Waiting for the DBInstance to Delete
        waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
            default_delay=15,
            default_max_attempts=40,
            timeout_config=timeout.get("delete") if timeout else None,
        )
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "neptune",
                "db_instance_deleted",
                DBInstanceIdentifier=resource_id,
                WaiterConfig=waiter_config,
            )
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type=STATE_NAME, name=name
            )
        except Exception as e:
            result["comment"] += [str(e)]
            result["result"] = False

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns information about provisioned instances, and supports pagination.  This operation can also return
    information for Amazon RDS instances and Amazon DocDB instances.

    .. note::
        Following sensitive parameters are part of present but are not available as part of describe:
        * master_user_password
        * tde_credential_password

        Following parameter is not part of present and is ignored from describe,
        idem ensures that the status is in ready state before declaring the resource present:
        * db_instance_status

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.neptune.db_instance
    """
    result = {}
    ret = await hub.exec.boto3.client.neptune.describe_db_instances(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe db_instance {ret['comment']}")
        return {}

    for db_instance in ret["ret"]["DBInstances"]:
        # Including fields to match the 'present' function parameters
        resource_id = db_instance.get("DBInstanceIdentifier")
        resource_arn = db_instance.get("DBInstanceArn")
        tags = await hub.tool.aws.neptune.tag.get_tags_for_resource(
            ctx, resource_arn=resource_arn
        )
        if not tags["result"]:
            hub.log.warning(
                f"Failed listing tags for aws.neptune.db_instance '{resource_id}'"
                f"Describe will skip this aws.neptune.db_instance and continue. "
            )
            continue
        tags = tags["ret"]
        resource_translated = (
            hub.tool.aws.neptune.conversion_utils.convert_raw_db_instance_to_present(
                db_instance, idem_resource_name=resource_id, tags=tags
            )
        )
        result[resource_id] = {
            "aws.neptune.db_instance.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result
