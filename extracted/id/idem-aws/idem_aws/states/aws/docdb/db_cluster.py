"""State module for managing AWS Doc DB cluster."""
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
    db_cluster_parameter_group_name: str = None,
    vpc_security_group_ids: List = None,
    db_subnet_group_name: str = None,
    engine_version: str = None,
    port: int = None,
    master_username: str = None,
    master_user_password: str = None,
    preferred_backup_window: str = None,
    preferred_maintenance_window: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass("Tag", [("Key", str), ("Value", str, field(default=None))])
    ] = None,
    storage_encrypted: bool = None,
    kms_key_id: str = None,
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
    """Creates a new Amazon DocumentDB cluster.

    Args:
        name(str):
            An Idem name of the resource. This also maps to db_cluster_identifier while creating the cluster.
        resource_id(str, Optional):
            An identifier of the resource in the provider, this also maps to DBClusterIdentifier during update. Defaults to None.
            The DB cluster identifier - This parameter is stored as a lowercase string. Constraints: Must
            contain from 1 to 63 letters, numbers, or hyphens. First character must be a letter. Cannot
            end with a hyphen or contain two consecutive hyphens. Example: my-cluster1.
        availability_zones(list, Optional):
            A list of EC2 Availability Zones that instances in the DB cluster can be created in. Defaults to None.
        backup_retention_period(int, Optional):
            The number of days for which automated backups are retained. You must specify a minimum value of
            1. Default: 1 Constraints: Must be a value from 1 to 35. Defaults to None.
        db_cluster_parameter_group_name(str, Optional):
            The name of the DB cluster parameter group to associate with this DB cluster. If this argument
            is omitted, the default is used. Constraints: If supplied, must match the name of an existing
            DBClusterParameterGroup. Defaults to None.
        vpc_security_group_ids(list, Optional):
            A list of EC2 VPC security groups to associate with this DB cluster. Defaults to None.
        db_subnet_group_name(str, Optional):
            A DB subnet group to associate with this DB cluster. Constraints: Must match the name of an
            existing DBSubnetGroup. Must not be default. Example: mySubnetgroup. Defaults to None.
        engine(str):
            The name of the database engine to be used for this DB cluster. Valid Values: docdb.
        engine_version(str, Optional):
            The version number of the database engine to use for the new DB cluster. Example: 1.0.2.1. Defaults to
            default to the latest major engine version.
        port(int, Optional):
            The port number on which the instances in the DB cluster accept connections.
        master_username(str, Optional):
            The name of the master user for the cluster. Constraints: Must be from 1 to 63 letters or numbers.
            The first character must be a letter. Cannot be a reserved word for the chosen database engine.
        master_user_password(str, Optional):
            The password for the master database user. This password can contain any printable ASCII character except
            forward slash (/), double quote ("), or the "at" symbol (@). Constraints: Must contain from 8 to 100 characters.
        preferred_backup_window(str, Optional):
            The daily time range during which automated backups are created if automated backups are enabled
            using the BackupRetentionPeriod parameter. The default is a 30-minute window selected at random
            from an 8-hour block of time for each Amazon Region. To see the time blocks available, see
            Adjusting the Preferred Maintenance Window in the Amazon Doc User Guide.  Constraints:
            Must be in the format hh24:mi-hh24:mi. Must be in Universal Coordinated Time (UTC).   Must not
            conflict with the preferred maintenance window. Must be at least 30 minutes. Defaults to None.
        preferred_maintenance_window(str, Optional):
            The weekly time range during which system maintenance can occur, in Universal Coordinated Time
            (UTC). Format: ddd:hh24:mi-ddd:hh24:mi  The default is a 30-minute window selected at random
            from an 8-hour block of time for each Amazon Region, occurring on a random day of the week. To
            see the time blocks available, see  Adjusting the Preferred Maintenance Window in the Amazon
            Doc User Guide.  Valid Days: Mon, Tue, Wed, Thu, Fri, Sat, Sun. Constraints: Minimum
            30-minute window. Defaults to None.
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
            The KMS key identifier for an encrypted cluster.

            The KMS key identifier is the Amazon Resource Name (ARN) for the KMS encryption key. If you are
            creating a cluster using the same Amazon Web Services account that owns the KMS encryption
            key that is used to encrypt the new cluster, you can use the KMS key alias instead
            of the ARN for the KMS encryption key. If an encryption key is not
            specified in KmsKeyId: If ReplicationSourceIdentifier identifies an encrypted source, then
            Amazon Doc will use the encryption key used to encrypt the source. Otherwise, Amazon Doc
            will use your default encryption key. If the StorageEncrypted parameter is true, then Amazon Doc will use
            your default encryption key. KMS creates the default encryption key for your Amazon Web Services account.
            Your Amazon Web Services account has a different default encryption key for each Amazon Web Services Regions.
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

            [idem_test_aws_doc_db_cluster]:
                aws.docdb.db_cluster.present:
                    - name: 'string'
                    - resource_id: 'string'
                    - engine: 'string'
                    - availability_zones:
                        - 'string'
                        - 'string'
                    - backup_retention_period: 'integer'
                    - db_cluster_parameter_group_name: 'string'
                    - vpc_security_group_ids:
                        - 'string'
                        - 'string'
                    - db_subnet_group_name: 'string'
                    - engine_version: 'string'
                    - port: 'integer'
                    - master_username: 'string'
                    - master_user_password: 'string'
                    - preferred_backup_window: 'string'
                    - preferred_maintenance_window: 'string'
                    - tags:
                        - Key: 'string'
                          Value: 'string'
                        - Key: 'string'
                          Value: 'string'
                    - storage_encrypted: 'boolean'
                    - kms_key_id: 'string'
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
              aws.docdb.db_cluster.present:
              - name: database-1
              - resource_id: database-1
              - db_cluster_identifier: database-1
              - engine: docdb
              - availability_zones:
                - ca-central-1a
                - ca-central-1b
                - ca-central-1d
              - backup_retention_period: 1
              - db_cluster_parameter_group_name: default.docdb1
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
        "db_cluster_parameter_group_name": db_cluster_parameter_group_name,
        "vpc_security_group_ids": vpc_security_group_ids,
        "db_subnet_group_name": db_subnet_group_name,
        "engine": engine,
        "engine_version": engine_version,
        "port": port,
        "master_username": master_username,
        "master_user_password": master_user_password,
        "preferred_backup_window": preferred_backup_window,
        "preferred_maintenance_window": preferred_maintenance_window,
        "tags": tags,
        "storage_encrypted": storage_encrypted,
        "kms_key_id": kms_key_id,
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
                resource_type="aws.docdb.db_cluster", name=name
            )
        else:
            # if this is not a test run, create the real cluster
            create_db_cluster_result = (
                await hub.exec.boto3.client.docdb.create_db_cluster(
                    ctx,
                    DBClusterIdentifier=name,
                    AvailabilityZones=availability_zones,
                    BackupRetentionPeriod=backup_retention_period,
                    DBClusterParameterGroupName=db_cluster_parameter_group_name,
                    VpcSecurityGroupIds=vpc_security_group_ids,
                    DBSubnetGroupName=db_subnet_group_name,
                    Engine=engine,
                    EngineVersion=engine_version,
                    Port=port,
                    MasterUsername=master_username,
                    MasterUserPassword=master_user_password,
                    PreferredBackupWindow=preferred_backup_window,
                    PreferredMaintenanceWindow=preferred_maintenance_window,
                    Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                    if tags
                    else None,
                    StorageEncrypted=storage_encrypted,
                    KmsKeyId=kms_key_id,
                    EnableCloudwatchLogsExports=enable_cloudwatch_logs_exports,
                    DeletionProtection=deletion_protection,
                    SourceRegion=source_region,
                )
            )
            # if create failed, fail the request
            if not create_db_cluster_result["result"]:
                result["comment"].append(create_db_cluster_result["comment"])
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
                client=await hub.tool.boto3.client.get_client(ctx, "docdb"),
            )
            try:
                await hub.tool.boto3.client.wait(
                    ctx,
                    "docdb",
                    "ClusterCreated",
                    cluster_waiter,
                    DBClusterIdentifier=resource_id,
                    WaiterConfig=waiter_config,
                )
                result["comment"] = hub.tool.aws.comment_utils.create_comment(
                    resource_type="aws.docdb.db_cluster", name=name
                )
                result["new_state"] = create_db_cluster_result
            except Exception as e:
                result["comment"] += [str(e)]
                result["result"] = False
                return result
        is_created = True

    # docdb db_cluster has some parameters that can only be applied while modification,
    # so if user specifies those parameters as during creation of a new db cluster, we have to modify
    # the new db cluster to achieve desired state
    desired_state["apply_immediately"] = apply_immediately
    desired_state[
        "cloudwatch_logs_export_configuration"
    ] = cloudwatch_logs_export_configuration

    update_db_cluster_result = await hub.tool.aws.docdb.db_cluster.update_db_cluster(
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
        result["comment"].append(update_db_cluster_result["comment"])
        return result

    result["old_state"] = update_db_cluster_result["old_state"]
    result["new_state"] = update_db_cluster_result["new_state"]
    # update the result comment if the resource is not being created
    if not is_created:
        result["comment"] = update_db_cluster_result["comment"]

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

            [idem_test_aws_doc_db_cluster]:
                aws.docdb.db_cluster.absent:
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
              aws_auto.docdb.db_cluster.absent:
                - name: database-1
                - resource_id: database-1
                - skip_final_snapshot: True
    """
    already_absent_msg = hub.tool.aws.comment_utils.already_absent_comment(
        resource_type="aws.docdb.db_cluster", name=name
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

    before = await hub.exec.aws.docdb.db_cluster.get(ctx=ctx, name=resource_id)

    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result
    if not before["ret"]:
        return result

    result["old_state"] = before["ret"]

    if ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.docdb.db_cluster", name=name
        )
        return result

    ret = await hub.exec.boto3.client.docdb.delete_db_cluster(
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
        client=await hub.tool.boto3.client.get_client(ctx, "docdb"),
    )
    try:
        await hub.tool.boto3.client.wait(
            ctx,
            "docdb",
            "ClusterDelete",
            cluster_waiter,
            DBClusterIdentifier=resource_id,
            WaiterConfig=waiter_config,
        )
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.docdb.db_cluster", name=name
        )
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns information about provisioned Doc DB clusters.  This operation can also return
    information for Amazon RDS clusters and Amazon DocDB clusters.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.docdb.db_cluster
    """
    result = {}
    ret = await hub.exec.aws.docdb.db_cluster.list(ctx=ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe aws.docdb.db_cluster {ret['comment']}")
        return {}

    for db_cluster in ret["ret"]:
        resource_id = db_cluster.get("db_cluster_identifier")
        result[resource_id] = {"aws.docdb.db_cluster.present": [db_cluster]}

    return result
