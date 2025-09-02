"""State module for managing AWS neptune DB cluster."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]
create_waiter_acceptors = [
    {
        "matcher": "pathAll",
        "expected": "available",
        "state": "success",
        "argument": "DBClusters[].Status",
    },
    {
        "matcher": "pathAll",
        "expected": "creating",
        "state": "retry",
        "argument": "DBClusters[].Status",
    },
]
update_waiter_acceptors = [
    {
        "matcher": "pathAll",
        "expected": "available",
        "state": "success",
        "argument": "DBClusters[].Status",
    },
    {
        "matcher": "pathAll",
        "expected": "modifying",
        "state": "retry",
        "argument": "DBClusters[].Status",
    },
    {
        "matcher": "pathAll",
        "expected": "resetting-master-credentials",
        "state": "retry",
        "argument": "DBClusters[].Status",
    },
    {
        "matcher": "pathAll",
        "expected": "renaming",
        "state": "retry",
        "argument": "DBClusters[].Status",
    },
    {
        "matcher": "pathAll",
        "expected": "upgrading",
        "state": "retry",
        "argument": "DBClusters[].Status",
    },
]
delete_waiter_acceptors = [
    {
        "matcher": "error",
        "expected": "DBClusterNotFoundFault",
        "state": "success",
        "argument": "Error.Code",
    },
    {
        "matcher": "pathAll",
        "expected": "available",
        "state": "retry",
        "argument": "DBClusters[].Status",
    },
    {
        "matcher": "pathAll",
        "expected": "deleting",
        "state": "retry",
        "argument": "DBClusters[].Status",
    },
]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    *,
    engine: str,
    availability_zones: List = None,
    backup_retention_period: int = None,
    copy_tags_to_snapshot: bool = None,
    database_name: str = None,
    db_cluster_parameter_group_name: str = None,
    vpc_security_group_ids: List = None,
    db_subnet_group_name: str = None,
    engine_version: str = None,
    port: int = None,
    master_username: str = None,
    master_user_password: str = None,
    option_group_name: str = None,
    preferred_backup_window: str = None,
    preferred_maintenance_window: str = None,
    replication_source_identifier: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass("Tag", [("Key", str), ("Value", str, field(default=None))])
    ] = None,
    storage_encrypted: bool = None,
    kms_key_id: str = None,
    enable_iam_database_authentication: bool = None,
    enable_cloudwatch_logs_exports: List = None,
    deletion_protection: bool = True,
    source_region: str = None,
    apply_immediately: bool = None,
    cloudwatch_logs_export_configuration: make_dataclass(
        """Cloudwatch log export configuration.""" "CloudwatchLogsExportConfiguration",
        [
            ("EnableLogTypes", List[str], field(default=None)),
            ("DisableLogTypes", List[str], field(default=None)),
        ],
    ) = None,
    db_instance_parameter_group_name: str = None,
    allow_major_version_upgrades: bool = None,
    timeout: make_dataclass(
        """Timeout configuration.""" "Timeout",
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
    """Creates a new Amazon Neptune DB cluster.

    You can use the ReplicationSourceIdentifier parameter to create the DB
    cluster as a Read Replica of another DB cluster or Amazon Neptune DB instance. Note that when you create a new
    cluster using CreateDBCluster directly, deletion protection is disabled by default (when you create a new
    production cluster in the console, deletion protection is enabled by default). You can only delete a DB cluster
    if its DeletionProtection field is set to false.

    Args:
        name(str):
            An Idem name of the resource. This also maps to db_cluster_identifier while creating the cluster.
        resource_id(str, Optional):
            An identifier of the resource in the provider, this also maps to DBClusterIdentifier during update. Defaults to None.
            The DB cluster identifier - This parameter is stored as a lowercase string. Constraints:   Must
            contain from 1 to 63 letters, numbers, or hyphens.   First character must be a letter.   Cannot
            end with a hyphen or contain two consecutive hyphens.   Example: my-cluster1.
        availability_zones(list, Optional):
            A list of EC2 Availability Zones that instances in the DB cluster can be created in. Defaults to None.
        backup_retention_period(int, Optional):
            The number of days for which automated backups are retained. You must specify a minimum value of
            1. Default: 1 Constraints:   Must be a value from 1 to 35. Defaults to None.
        copy_tags_to_snapshot(bool, Optional):
            If set to True, tags are copied to any snapshot of the DB cluster that is created. Defaults to None.
        database_name(str, Optional):
            The name for your database of up to 64 alpha-numeric characters. If you do not provide a name,
            Amazon Neptune will not create a database in the DB cluster you are creating. Defaults to None.
        db_cluster_parameter_group_name(str, Optional):
            The name of the DB cluster parameter group to associate with this DB cluster. If this argument
            is omitted, the default is used. Constraints:   If supplied, must match the name of an existing
            DBClusterParameterGroup. Defaults to None.
        vpc_security_group_ids(list, Optional):
            A list of EC2 VPC security groups to associate with this DB cluster. Defaults to None.
        db_subnet_group_name(str, Optional):
            A DB subnet group to associate with this DB cluster. Constraints: Must match the name of an
            existing DBSubnetGroup. Must not be default. Example: mySubnetgroup. Defaults to None.
        engine(str):
            The name of the database engine to be used for this DB cluster. Valid Values: neptune.
        engine_version(str, Optional):
            The version number of the database engine to use for the new DB cluster. Example: 1.0.2.1. Defaults to None.
        port(int, Optional):
            The port number on which the instances in the DB cluster accept connections.  Default: 8182. Defaults to None.
        preferred_backup_window(str, Optional):
            The daily time range during which automated backups are created if automated backups are enabled
            using the BackupRetentionPeriod parameter. The default is a 30-minute window selected at random
            from an 8-hour block of time for each Amazon Region. To see the time blocks available, see
            Adjusting the Preferred Maintenance Window in the Amazon Neptune User Guide.  Constraints:
            Must be in the format hh24:mi-hh24:mi.   Must be in Universal Coordinated Time (UTC).   Must not
            conflict with the preferred maintenance window.   Must be at least 30 minutes. Defaults to None.
        preferred_maintenance_window(str, Optional):
            The weekly time range during which system maintenance can occur, in Universal Coordinated Time
            (UTC). Format: ddd:hh24:mi-ddd:hh24:mi  The default is a 30-minute window selected at random
            from an 8-hour block of time for each Amazon Region, occurring on a random day of the week. To
            see the time blocks available, see  Adjusting the Preferred Maintenance Window in the Amazon
            Neptune User Guide.  Valid Days: Mon, Tue, Wed, Thu, Fri, Sat, Sun. Constraints: Minimum
            30-minute window. Defaults to None.
        replication_source_identifier(str, Optional):
            The Amazon Resource Name (ARN) of the source DB instance or DB cluster if this DB cluster is
            created as a Read Replica. Defaults to None.
        tags(dict or list, Optional):
            Dict in the format of {tag-key: tag-value} or List of tags in the format of
            [{"Key": tag-key, "Value": tag-value}] to associate with the DB cluster.Each tag consists of a key name and
            an associated value. Defaults to None.

            * Key(str, Optional):
                The key of the tag.
                Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode
                characters. May not begin with aws:.

            * Value(str, Optional):
                The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256
                Unicode characters.
        storage_encrypted(bool, Optional):
            Specifies whether the DB cluster is encrypted. Defaults to None.
        kms_key_id(str, Optional):
            The Amazon KMS key identifier for an encrypted DB cluster. The KMS key identifier is the Amazon
            Resource Name (ARN) for the KMS encryption key. If you are creating a DB cluster with the same
            Amazon account that owns the KMS encryption key used to encrypt the new DB cluster, then you can
            use the KMS key alias instead of the ARN for the KMS encryption key. If an encryption key is not
            specified in KmsKeyId:   If ReplicationSourceIdentifier identifies an encrypted source, then
            Amazon Neptune will use the encryption key used to encrypt the source. Otherwise, Amazon Neptune
            will use your default encryption key.   If the StorageEncrypted parameter is true and
            ReplicationSourceIdentifier is not specified, then Amazon Neptune will use your default
            encryption key.   Amazon KMS creates the default encryption key for your Amazon account. Your
            Amazon account has a different default encryption key for each Amazon Region. If you create a
            Read Replica of an encrypted DB cluster in another Amazon Region, you must set KmsKeyId to a KMS
            key ID that is valid in the destination Amazon Region. This key is used to encrypt the Read
            Replica in that Amazon Region. Defaults to None.
        enable_iam_database_authentication(bool, Optional):
            If set to true, enables Amazon Identity and Access Management (IAM) authentication for the
            entire DB cluster (this cannot be set at an instance level). Default: false. Defaults to None.
        enable_cloudwatch_logs_exports(list, Optional):
            The list of log types that need to be enabled for exporting to CloudWatch Logs. Defaults to None.
        deletion_protection(bool, Optional):
            A value that indicates whether the DB cluster has deletion protection enabled. The database
            can't be deleted when deletion protection is enabled. By default, deletion protection is
            enabled. Defaults to None.
        source_region(str, Optional):
            The ID of the region that contains the source for the db cluster. Defaults to None.
        apply_immediately(bool, Optional):
            A value that indicates whether the modifications in this request and any
            pending modifications are asynchronously applied as soon as possible,
            regardless of the PreferredMaintenanceWindow setting for the DB cluster.
            If this parameter is disabled, changes to the DB cluster are applied during
            the next maintenance window.
            The ApplyImmediately parameter only affects the
            EnableIAMDatabaseAuthentication,MasterUserPassword and NewDBClusterIdentifier
            values.If the ApplyImmediately parameter is disabled, then changes to the
            EnableIAMDatabaseAuthentication,MasterUserPassword and NewDBClusterIdentifier
            values are applied during the next maintenance window. All other changes are
            applied immediately,regardless of the value of the ApplyImmediately parameter
        cloudwatch_logs_export_configuration(dict[str, Any], Optional):
            The configuration setting for the log types to be enabled for export to CloudWatch Logs for a specific DB cluster.

            * EnableLogTypes (list[str], Optional):
                The list of log types to enable.

            * DisableLogTypes(list[str], Optional):
                The list of log types to disable.
        db_instance_parameter_group_name(str, Optional):
            The name of the DB parameter group to apply to all instances of
            the DB cluster.
        allow_major_version_upgrades(bool, Optional):
            A value that indicates whether major version upgrades are allowed.
        timeout(dict, Optional):
            Timeout configuration for create/update of AWS DB Cluster.

            * create (*dict, Optional*):
                Timeout configuration for creating DB Cluster.

                * delay(*int, Optional*):
                    The amount of time in seconds to wait between attempts.

                * max_attempts(*int, Optional*):
                    Customized timeout configuration containing delay and max attempts.

            * update(*dict, Optional*):
                Timeout configuration for updating DB Cluster

                * delay(*int, Optional*):
                    The amount of time in seconds to wait between attempts.

                * max_attempts(*int, Optional*):
                    Customized timeout configuration containing delay and max attempts.

    Request Syntax:
        .. code-block:: sls

            [idem_test_aws_neptune_db_cluster]:
                aws.neptune.db_cluster.present:
                    - name: 'string'
                    - resource_id: 'string'
                    - engine: 'string'
                    - availability_zones:
                        - 'string'
                        - 'string'
                    - backup_retention_period: 'integer'
                    - copy_tags_to_snapshot: 'boolean'
                    - database_name: 'string'
                    - db_cluster_parameter_group_name: 'string'
                    - vpc_security_group_ids:
                        - 'string'
                        - 'string'
                    - db_subnet_group_name: 'string'
                    - engine_version: 'string'
                    - port: 'integer'
                    - master_username: 'string'
                    - master_user_password: 'string'
                    - option_group_name: 'string'
                    - preferred_backup_window: 'string'
                    - preferred_maintenance_window: 'string'
                    - replication_source_identifier: 'string'
                    - tags:
                        - Key: 'string'
                          Value: 'string'
                        - Key: 'string'
                          Value: 'string'
                    - storage_encrypted: 'boolean'
                    - kms_key_id: 'string'
                    - enable_iam_database_authentication: 'boolean'
                    - enable_cloudwatch_logs_exports:
                        - string
                        - string
                    - deletion_protection: 'boolean'
                    - source_region: 'string'
                    - apply_immediately: 'boolean'
                    - cloudwatch_logs_export_configuration:
                        - EnableLogTypes:
                            - 'string'
                            - 'string'
                        - DisableLogTypes:
                            - 'string'
                            - 'string'
                    - db_instance_parameter_group_name: 'string'
                    - allow_major_version_upgrades: 'boolean'
                    - timeout:
                        create:
                            delay: 'integer'
                            max_attempts: 'integer'
                        update:
                            delay: 'integer'
                            max_attempts: 'integer'

    Returns:
        Dict[str, Dict[str,Any]]

    Examples:
        .. code-block:: sls

            database-1:
              aws.neptune.db_cluster.present:
              - name: database-1
              - resource_id: database-1
              - db_cluster_identifier: database-1
              - engine: neptune
              - availability_zones:
                - ca-central-1a
                - ca-central-1b
                - ca-central-1d
              - backup_retention_period: 1
              - copy_tags_to_snapshot: true
              - db_cluster_parameter_group_name: default.neptune1
              - db_subnet_group_name: default
              - engine_version: 1.1.1.0
              - port: 8182
              - preferred_backup_window: 06:18-06:48
              - preferred_maintenance_window: wed:04:33-wed:05:03
              - tags:
                  test: test
              - storage_encrypted: true
              - kms_key_id: arn:aws:kms:ca-central-1:746014882121:key/2a4a587a-04fb-4c3b-b4d5-c3f25fb7f69f
              - deletion_protection: false
              - vpc_security_group_ids:
                - sg-ad5a2ac5
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
    desired_state = {
        "name": name,
        "availability_zones": availability_zones,
        "backup_retention_period": backup_retention_period,
        "copy_tags_to_snapshot": copy_tags_to_snapshot,
        "database_name": database_name,
        "db_cluster_parameter_group_name": db_cluster_parameter_group_name,
        "vpc_security_group_ids": vpc_security_group_ids,
        "db_subnet_group_name": db_subnet_group_name,
        "engine": engine,
        "engine_version": engine_version,
        "port": port,
        "master_username": master_username,
        "master_user_password": master_user_password,
        "option_group_name": option_group_name,
        "preferred_backup_window": preferred_backup_window,
        "preferred_maintenance_window": preferred_maintenance_window,
        "replication_source_identifier": replication_source_identifier,
        "tags": tags,
        "storage_encrypted": storage_encrypted,
        "kms_key_id": kms_key_id,
        "enable_iam_database_authentication": enable_iam_database_authentication,
        "enable_cloudwatch_logs_exports": enable_cloudwatch_logs_exports,
        "deletion_protection": deletion_protection,
        "source_region": source_region,
    }
    hub.log.debug(f"desired state is {desired_state}")
    is_created = False

    if not resource_id:
        # if there is no resource_id, create db cluster
        # if test run, generate the new state and set in result
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={}, desired_state=desired_state
            )
            resource_id = desired_state["name"]
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.neptune.db_cluster", name=name
            )
        else:
            # if this is not a test run, create the real cluster
            create_db_cluster_result = (
                await hub.exec.boto3.client.neptune.create_db_cluster(
                    ctx,
                    DBClusterIdentifier=name,
                    AvailabilityZones=availability_zones,
                    BackupRetentionPeriod=backup_retention_period,
                    CopyTagsToSnapshot=copy_tags_to_snapshot,
                    DatabaseName=database_name,
                    DBClusterParameterGroupName=db_cluster_parameter_group_name,
                    VpcSecurityGroupIds=vpc_security_group_ids,
                    DBSubnetGroupName=db_subnet_group_name,
                    Engine=engine,
                    EngineVersion=engine_version,
                    Port=port,
                    MasterUsername=master_username,
                    MasterUserPassword=master_user_password,
                    OptionGroupName=option_group_name,
                    PreferredBackupWindow=preferred_backup_window,
                    PreferredMaintenanceWindow=preferred_maintenance_window,
                    ReplicationSourceIdentifier=replication_source_identifier,
                    Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                    if tags
                    else None,
                    StorageEncrypted=storage_encrypted,
                    KmsKeyId=kms_key_id,
                    EnableIAMDatabaseAuthentication=enable_iam_database_authentication,
                    EnableCloudwatchLogsExports=enable_cloudwatch_logs_exports,
                    DeletionProtection=deletion_protection,
                    SourceRegion=source_region,
                )
            )
            # if create failed, fail the request
            if not create_db_cluster_result["result"]:
                result["comment"] += create_db_cluster_result["comment"]
                result["result"] = False
                return result

            # using the resource_id, wait till db cluster is created
            resource_id = create_db_cluster_result["ret"]["DBCluster"][
                "DBClusterIdentifier"
            ]
            waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                default_delay=15,
                default_max_attempts=40,
                timeout_config=timeout.get("create") if timeout else None,
            )
            cluster_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
                name="ClusterCreated",
                operation="DescribeDBClusters",
                argument=["DBClusters[].Status"],
                acceptors=create_waiter_acceptors,
                client=await hub.tool.boto3.client.get_client(ctx, "neptune"),
            )
            try:
                await hub.tool.boto3.client.wait(
                    ctx,
                    "neptune",
                    "ClusterCreated",
                    cluster_waiter,
                    DBClusterIdentifier=resource_id,
                    WaiterConfig=waiter_config,
                )
                result["comment"] = hub.tool.aws.comment_utils.create_comment(
                    resource_type="aws.neptune.db_cluster", name=name
                )
            except Exception as e:
                result["comment"] += [str(e)]
                result["result"] = False
                return result
        is_created = True

    # neptune db_cluster has some parameters that can only be applied while modification,
    # so if user specifies those parameters as during creation of a new db cluster, we have to modify
    # the new db cluster to achieve desired state
    desired_state["apply_immediately"] = apply_immediately
    desired_state[
        "cloudwatch_logs_export_configuration"
    ] = cloudwatch_logs_export_configuration
    desired_state["db_instance_parameter_group_name"] = db_instance_parameter_group_name
    desired_state["allow_major_version_upgrades"] = allow_major_version_upgrades

    update_db_cluster_result = await hub.tool.aws.neptune.db_cluster.update_db_cluster(
        ctx=ctx,
        name=name,
        resource_id=resource_id,
        desired_state=desired_state,
        is_created=is_created,
        update_waiter_acceptors=update_waiter_acceptors,
        timeout=timeout,
    )
    if not (
        update_db_cluster_result
        and update_db_cluster_result["result"]
        and update_db_cluster_result["new_state"]
    ):
        result["result"] = False
        result["comment"] += update_db_cluster_result["comment"]
        return result

    result["old_state"] = update_db_cluster_result["old_state"]
    result["new_state"] = update_db_cluster_result["new_state"]
    # update the result comment if the resource is not being created
    if not is_created:
        result["comment"] += update_db_cluster_result["comment"]

    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    skip_final_snapshot: bool = None,
    final_db_snapshot_identifier: str = None,
    timeout: Dict = None,
) -> Dict[str, Any]:
    """The DeleteDBCluster action deletes a previously provisioned DB cluster.

    When you delete a DB cluster, all automated backups for that DB cluster are deleted and can't be recovered.
    Manual DB cluster snapshots of the specified DB cluster are not deleted.
    Note that the DB Cluster cannot be deleted if deletion protection is
    enabled. To delete it, you must first set its DeletionProtection field to False.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            An identifier of the resource in the provider. The DB cluster identifier for the DB cluster to be deleted. This parameter isn't case-sensitive.
            Idem automatically considers this resource being absent if this field is not specified.
            Constraints:   Must match an existing DBClusterIdentifier.
        skip_final_snapshot(bool, Optional):
            Determines whether a final DB cluster snapshot is created before the DB cluster is deleted. If
            true is specified, no DB cluster snapshot is created. If false is specified, a DB cluster
            snapshot is created before the DB cluster is deleted.  You must specify a
            FinalDBSnapshotIdentifier parameter if SkipFinalSnapshot is false.  Default: false. Defaults to None.
        final_db_snapshot_identifier(str, Optional):
            The DB cluster snapshot identifier of the new DB cluster snapshot created when
            SkipFinalSnapshot is set to false.   Specifying this parameter and also setting the
            SkipFinalShapshot parameter to true results in an error.  Constraints:   Must be 1 to 255
            letters, numbers, or hyphens.   First character must be a letter   Cannot end with a hyphen or
            contain two consecutive hyphens. Defaults to None.
        timeout(dict, Optional):
            Timeout configuration for create/update of AWS DB Cluster.

            * delete (*dict, Optional*):
                Timeout configuration for deleting DB Cluster.

                * delay(*int, Optional*):
                    The amount of time in seconds to wait between attempts.

                * max_attempts(*int, Optional*):
                    Customized timeout configuration containing delay and max attempts.

    Request Syntax:
        .. code-block:: sls

            [idem_test_aws_neptune_db_cluster]:
                aws.neptune.db_cluster.absent:
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

            resource_is_absent:
              aws_auto.neptune.db_cluster.absent:
                - name: database-1
                - resource_id: database-1
                - skip_final_snapshot: True
    """
    already_absent_msg = hub.tool.aws.comment_utils.already_absent_comment(
        resource_type="aws.neptune.db_cluster", name=name
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

    before = await hub.exec.boto3.client.neptune.describe_db_clusters(
        ctx, DBClusterIdentifier=resource_id
    )
    db_clusters = before["ret"].get("DBClusters") if before.get("ret") else None

    if not (before["result"] and db_clusters):
        if not ("DBClusterNotFoundFault" in str(before["comment"])):
            result["comment"] = before["comment"]
            result["result"] = False
        return result

    resource_arn = db_clusters[0].get("DBClusterArn")
    tags = await hub.tool.aws.neptune.tag.get_tags_for_resource(
        ctx, resource_arn=resource_arn
    )
    if not tags["result"]:
        result["result"] = False
        result["comment"] = tags["comment"]
        return result
    tags = tags["ret"]
    result[
        "old_state"
    ] = hub.tool.aws.neptune.db_cluster.convert_raw_db_cluster_to_present(
        db_clusters[0], idem_resource_name=resource_id, tags=tags
    )

    if ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.neptune.db_cluster", name=name
        )
        return result

    ret = await hub.exec.boto3.client.neptune.delete_db_cluster(
        ctx,
        DBClusterIdentifier=resource_id,
        SkipFinalSnapshot=skip_final_snapshot,
        FinalDBSnapshotIdentifier=final_db_snapshot_identifier,
    )
    result["result"] = ret["result"]
    if not result["result"]:
        result["comment"] = ret["comment"]
        return result
    # Custom waiter for delete
    waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
        default_delay=15,
        default_max_attempts=40,
        timeout_config=timeout.get("delete") if timeout else None,
    )
    cluster_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
        name="ClusterDelete",
        operation="DescribeDBClusters",
        argument=["Error.Code", "DBClusters[].Status"],
        acceptors=delete_waiter_acceptors,
        client=await hub.tool.boto3.client.get_client(ctx, "neptune"),
    )
    try:
        await hub.tool.boto3.client.wait(
            ctx,
            "neptune",
            "ClusterDelete",
            cluster_waiter,
            DBClusterIdentifier=resource_id,
            WaiterConfig=waiter_config,
        )
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.neptune.db_cluster", name=name
        )
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns information about provisioned Neptune DB clusters.  This operation can also return
    information for Amazon RDS clusters and Amazon DocDB clusters.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.neptune.db_cluster
    """
    result = {}
    ret = await hub.exec.boto3.client.neptune.describe_db_clusters(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe aws.neptune.db_cluster {ret['comment']}")
        return {}

    for db_cluster in ret["ret"]["DBClusters"]:
        resource_id = db_cluster.get("DBClusterIdentifier")
        resource_arn = db_cluster.get("DBClusterArn")
        tags = await hub.tool.aws.neptune.tag.get_tags_for_resource(
            ctx, resource_arn=resource_arn
        )
        if not tags["result"]:
            # if something goes wrong fetching the tags (not if the tags are None that is a normal path)
            hub.log.warning(
                f"Failed listing tags for aws.neptune.db_cluster '{resource_id}'"
                f"Describe will skip this aws.neptune.db_cluster and continue. "
            )
            continue
        tags = tags["ret"]
        # Including fields to match the 'present' function parameters
        resource_translated = (
            hub.tool.aws.neptune.db_cluster.convert_raw_db_cluster_to_present(
                db_cluster, idem_resource_name=resource_id, tags=tags
            )
        )
        result[resource_id] = {
            "aws.neptune.db_cluster.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result
