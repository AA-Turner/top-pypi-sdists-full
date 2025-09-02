"""State modules for managing RDS db_cluster."""
import copy
import uuid
from collections import OrderedDict
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

TREQ = {
    "present": {
        "require": ["aws.rds.db_subnet_group.present"],
    },
    "absent": {
        "require": ["aws.rds.db_instance.absent"],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    engine: str,
    resource_id: str = None,
    availability_zones: List[str] = None,
    backup_retention_period: int = None,
    character_set_name: str = None,
    database_name: str = None,
    db_cluster_parameter_group_name: str = None,
    vpc_security_group_ids: List[str] = None,
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
    pre_signed_url: str = None,
    enable_iam_database_authentication: bool = None,
    backtrack_window: int = None,
    enable_cloudwatch_logs_exports: List[str] = None,
    engine_mode: str = None,
    scaling_configuration: make_dataclass(
        "ScalingConfiguration",
        [
            ("MinCapacity", int, field(default=None)),
            ("MaxCapacity", int, field(default=None)),
            ("AutoPause", bool, field(default=None)),
            ("SecondsUntilAutoPause", int, field(default=None)),
            ("TimeoutAction", str, field(default=None)),
            ("SecondsBeforeTimeout", int, field(default=None)),
        ],
    ) = None,
    deletion_protection: bool = None,
    global_cluster_identifier: str = None,
    enable_http_endpoint: bool = None,
    copy_tags_to_snapshot: bool = None,
    domain: str = None,
    domain_iam_role_name: str = None,
    enable_global_write_forwarding: bool = None,
    db_cluster_instance_class: str = None,
    allocated_storage: int = None,
    storage_type: str = None,
    iops: int = None,
    publicly_accessible: bool = None,
    auto_minor_version_upgrade: bool = None,
    monitoring_interval: int = None,
    monitoring_role_arn: str = None,
    enable_performance_insights: bool = None,
    performance_insights_kms_key_id: str = None,
    performance_insights_retention_period: int = None,
    source_region: str = None,
    apply_immediately: bool = None,
    allow_major_version_upgrades: bool = None,
    cloudwatch_logs_export_configuration: Dict = None,
    db_instance_parameter_group_name: str = None,
    serverless_v2_scaling_configuration: make_dataclass(
        "ServerlessV2ScalingConfiguration",
        [
            ("MinCapacity", float, field(default=None)),
            ("MaxCapacity", float, field(default=None)),
        ],
    ) = None,
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
    r'''Creates a new Amazon Aurora DB cluster or Multi-AZ DB cluster.

    You can use the ReplicationSourceIdentifier parameter to create an Amazon Aurora DB cluster as a read replica of
    another DB cluster or Amazon RDS MySQL or PostgreSQL DB instance. For cross-Region replication where the DB cluster
    identified by ReplicationSourceIdentifier is encrypted, also specify the PreSignedUrl parameter.

    For more information on Amazon Aurora, see What is Amazon Aurora? in the Amazon Aurora User Guide.For more
    information on Multi-AZ DB clusters, see Multi-AZ deployments with two readable standby DB instances in the Amazon
    RDS User Guide. TheMulti-AZ DB clusters feature is in preview and is subject to change by the aws provider.

    Args:
        name(str):
            A name, ID to identify the resource.

        engine(str):
            Name of the database engine to be used for this DB cluster.

        resource_id(str, Optional):
            AWS Id of the resource.

        availability_zones(list, Optional):
            A list of Availability Zones (AZs) where DB instances in the DB cluster can be created. For information on
            Amazon Web Services Regions and Availability Zones, see Choosing the Regions and Availability Zones in the
            Amazon Aurora User Guide. Defaults to None.

            * Valid for: Aurora DB clusters only.

        backup_retention_period(int, Optional):
            The number of days for which automated backups are retained.

            * Default: 1
            * Constraints: Must be a value from 1 to 35
            * Valid for: Aurora DB clusters and Multi-AZ DB clusters.

        character_set_name(str, Optional):
            A value that indicates that the DB cluster should be associated with the specified CharacterSet. Defaults
            to None.

            * Valid for: Aurora DB clusters only.

        database_name(str, Optional):
            The name for your database of up to 64 alphanumeric characters. If you do not provide a name, Amazon RDS
            doesn't create a database in the DB cluster you are creating.

            * Valid for: Aurora DB clusters and Multi-AZ DB clusters. Defaults to None.

        db_cluster_parameter_group_name(str, Optional):
            The name of the DB cluster parameter group to associate with this DB cluster. If you do not specify a
            value, then the default DB cluster parameter group for the specified DB engine and version is used.

            * Constraints: If supplied, must match the name of an existing DB cluster parameter group.
            * Valid for: Aurora DB clusters and Multi-AZ DB clusters. Defaults to None.

        vpc_security_group_ids(list[str], Optional):
            A list of EC2 VPC security groups to associate with this DB cluster.

            * Valid for: Aurora DB clusters and Multi-AZ DB clusters. Defaults to None.

        db_subnet_group_name(str, Optional):
            A DB subnet group to associate with this DB cluster. This setting is required to create a Multi-AZ DB
            cluster.

            * Constraints: Must match the name of an existing DBSubnetGroup. Must not be default.
            * Example: mydbsubnetgroup
            * Valid for: Aurora DB clusters and Multi-AZ DB clusters. Defaults to None.

        engine(str):
            The name of the database engine to be used for this DB cluster.

            * Valid Values:
                * aurora (for MySQL 5.6-compatible Aurora)
                * aurora-mysql (for MySQL 5.7-compatible and MySQL 8.0-compatibleAurora)
                * aurora-postgresql
                * mysql
                * postgres.
            * Valid for: Aurora DB clusters and Multi-AZ DB clusters.

        engine_version(str, Optional):
            The version number of the database engine to use.

            To list all of the available engine versions for MySQL 5.6-compatible Aurora, use the following command:

            .. code-block:: bash

                aws rds describe-db-engine-versions --engine aurora --query "DBEngineVersions[].EngineVersion"

            To list all of the available engine versions for MySQL 5.7-compatible and MySQL 8.0-compatible Aurora, use
            the following command:

            .. code-block:: bash

                aws rds describe-db-engine-versions --engine aurora-mysql --query "DBEngineVersions[].EngineVersion"

            To list all of the available engine versions for Aurora PostgreSQL, use the following command:

            .. code-block:: bash

                aws rds describe-db-engine-versions --engine aurora- postgresql --query "DBEngineVersions[].EngineVersion"

            To list all of the available engine versions for RDS for MySQL, use the following command:

            .. code-block:: bash

                aws rds describe-db-engine-versions --engine mysql --query "DBEngineVersions[].EngineVersion"

            To list all of the available engine versions for RDS for PostgreSQL, use the following command:

            .. code-block:: bash

                aws rds describe-db-engine-versions --engine postgres --query "DBEngineVersions[].EngineVersion"

            Aurora MySQL:
                For information, see MySQL on Amazon RDS Versions in the Amazon Aurora User Guide.

            Aurora PostgreSQL:
                For information, see Amazon Aurora PostgreSQL releases and engine versions in the Amazon Aurora User
                Guide.

            MySQL:
                For information, see MySQL on Amazon RDS Versions in the Amazon RDS User Guide.

            PostgreSQL:
                For information, see Amazon RDS for PostgreSQL versions and extensions in the Amazon RDS User Guide.

            * Valid for: Aurora DB clusters and Multi-AZ DB clusters. Defaults to None.

        port(int, Optional):
            The port number on which the instances in the DB cluster accept connections.

            * RDS for MySQL and Aurora MySQL  Default: 3306  Valid values: 1150-65535
            * RDS for PostgreSQL and Aurora PostgreSQL Default: 5432  Valid values: 1150-65535
            * Valid for: Aurora DB clusters and Multi-AZ DB clusters.

        master_username(str, Optional):
            The name of the master user for the DB cluster.

            * Constraints: Must be 1 to 16 letters or numbers. First character must be a letter.Can't be a reserved
              word for the chosen database engine.
            * Valid for: Aurora DB clusters and Multi-AZ DB clusters. Defaults to None.

        master_user_password(str, Optional):
            The password for the master database user. This password can contain any printable ASCII
            character except "/", """, or "@".

            * Constraints: Must contain from 8 to 41 characters.
            * Valid for: Aurora DB clusters and Multi-AZ DB clusters. Defaults to None.

        option_group_name(str, Optional):
            A value that indicates that the DB cluster should be associated with the specified option group.  DB
            clusters are associated with a default option group that can't be modified. Defaults to None.

        preferred_backup_window(str, Optional):
            The daily time range during which automated backups are created if automated backups are enabled using the
            BackupRetentionPeriod parameter. The default is a 30-minute window selected at random from an 8-hour block
            of time for each Amazon Web Services Region. To view the time blocks available, see  Backup window in the
            Amazon Aurora User Guide.

            * Constraints: Must be in the format hh24:mi-hh24:mi.Must be in Universal Coordinated Time (UTC).Must not
              conflict with the preferred maintenance window.Must be at least 30 minutes.
            * Valid for: Aurora DB clusters and Multi-AZ DB clusters. Defaults to None.

        preferred_maintenance_window(str, Optional):
            The weekly time range during which system maintenance can occur, in Universal Coordinated Time (UTC).

            * Format: ddd:hh24:mi-ddd:hh24:mi

                The default is a 30-minute window selected at random from an 8-hour block of time for each Amazon Web
                Services Region, occurring on a random day of the week. To see the time blocks available, see
                Adjusting the Preferred DB Cluster Maintenance Window in the Amazon Aurora User Guide.

            * Valid Days: Mon, Tue, Wed, Thu, Fri, Sat, Sun.
            * Constraints: Minimum 30-minute window.
            * Valid for: Aurora DB clusters and Multi-AZ DB clusters. Defaults to None.

        replication_source_identifier(str, Optional):
            The Amazon Resource Name (ARN) of the source DB instance or DB cluster if this DB cluster is created as a
            read replica.

            * Valid for: Aurora DB clusters only. Defaults to None.

        tags(dict or list, Optional):
            dict in the format of {tag-key: tag-value} or list of tags in the format of ``[{"Key": tag-key, "Value":
            tag-value}]`` to associate with the DB cluster.  Each tag consists of a key name and an associated value.
            Defaults to None.

            * Key (str, Optional):
                The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode
                characters. May not begin with aws:.

            * Value(str, Optional):
                The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256
                Unicode characters.

        storage_encrypted(bool, Optional):
            A value that indicates whether the DB cluster is encrypted.

            * Valid for: Aurora DB clusters and Multi-AZ DB clusters. Defaults to None.

        kms_key_id(str, Optional):
            The Amazon Web Services KMS key identifier for an encrypted DB cluster. The Amazon Web Services KMS key
            identifier is the key ARN, key ID, alias ARN, or alias name for the KMS key.

            To use a KMS key in a different Amazon Web Services account, specify the key ARN or alias ARN.

            When a KMS key isn't specified in KmsKeyId:   If ReplicationSourceIdentifier identifies an encrypted
            source, then Amazon RDS will use the KMS key used to encrypt the source. Otherwise, Amazon RDS will use
            your default KMS key.

            If the StorageEncrypted parameter is enabled and ReplicationSourceIdentifier isn't specified, then Amazon
            RDS will use your default KMS key.  There is a default KMS key for your Amazon Web Services account. Your
            Amazon Web Services account has a different default KMS key for each Amazon Web Services Region. If you
            create a read replica of an encrypted DB cluster in another Amazon Web Services Region, you must set
            KmsKeyId to a KMS key identifier that is valid in the destination Amazon Web Services Region.  This KMS key
            is used to encrypt the read replica in that Amazon Web Services Region.

            * Valid for: Aurora DB clusters and Multi-AZ DB clusters. Defaults to None.

        pre_signed_url(str, Optional):
            A URL that contains a Signature Version 4 signed request for the CreateDBCluster action to be called in the
            source Amazon Web Services Region where the DB cluster is replicated from.

            Specify PreSignedUrl only when you are performing cross-Region replication from an encrypted DB cluster.
            The pre-signed URL must be a valid request for the CreateDBCluster API action that can be executed in the
            source Amazon Web Services Region that contains the encrypted DB cluster to be copied.

            The pre-signed URL request must contain the following parameter values:

            * KmsKeyId - The Amazon Web Services KMS key identifier for the KMS key to use to encrypt the copy of the
            DB cluster in the destination Amazon Web Services Region. This should refer to the same KMS key for both
            the CreateDBCluster action that is called in the destination Amazon Web Services Region, and the action
            contained in the pre-signed URL.

            * DestinationRegion - The name of the Amazon Web Services Region that Aurora read replica will be created
            in.

            * ReplicationSourceIdentifier - The DB cluster identifier for the encrypted DB cluster to be copied.  This
            identifier must be in the Amazon Resource Name (ARN) format for the source Amazon Web Services Region.  For
            example, if you are copying an encrypted DB cluster from the us-west-2 Amazon Web Services Region, then
            your ReplicationSourceIdentifier would look like:

            Example:

                ``arn:aws:rds:us-west-2:123456789012:cluster:aurora-cluster1``

            To learn how to generate a Signature Version 4 signed request, see  Authenticating Requests: Using Query
            Parameters (Amazon Web Services Signature Version 4) and  Signature Version 4 Signing Process.

            If you are using an Amazon Web Services SDK tool or the CLI, you can specify SourceRegion (or
            ``--source-region`` for the CLI) instead of specifying PreSignedUrl manually. Specifying SourceRegion
            autogenerates a pre-signed URL that is a valid request for the operation that can be executed in the source
            Amazon Web Services Region.

            * Valid for: Aurora DB clusters only. Defaults to None.

        enable_iam_database_authentication(bool, Optional):
            A value that indicates whether to enable mapping of Amazon Web Services Identity and Access Management
            (IAM) accounts to database accounts. By default, mapping isn't enabled. For more information, see  IAM
            Database Authentication in the Amazon Aurora User Guide.

            * Valid for:Aurora DB clusters only. Defaults to None.

        backtrack_window(int, Optional):
            The target backtrack window, in seconds. To disable backtracking, set this value to 0.

            * Default: 0
            * Constraints: If specified, this value must be set to a number from 0 to 259,200 (72 hours).
            * Valid for: Aurora MySQL DB clusters only.

        enable_cloudwatch_logs_exports(list[str], Optional):
            The list of log types that need to be enabled for exporting to CloudWatch Logs. The values in the list
            depend on the DB engine being used.

            RDS for MySQL: Possible values are error, general, and slowquery.

            RDS for PostgreSQL  Possible values are postgresql and upgrade.

            Aurora MySQL: Possible values are audit, error, general, and slowquery.

            Aurora PostgreSQL  Possible value is postgresql.

            For more information about exporting CloudWatch Logs for Amazon RDS, see Publishing Database Logs to Amazon
            CloudWatch Logs in the Amazon RDS User Guide. For more information about exporting CloudWatch Logs for
            Amazon Aurora, see Publishing Database Logs to Amazon CloudWatch Logs in the Amazon Aurora User Guide.

            * Valid for: Aurora DB clusters and Multi-AZ DB clusters. Defaults to None.

        engine_mode(str, Optional):
            The DB engine mode of the DB cluster, either provisioned, serverless, parallelquery, global, or
            multimaster.

            The parallelquery engine mode isn't required for Aurora MySQL version 1.23 and higher 1.x versions, and
            version 2.09 and higher 2.x versions.

            The global engine mode isn't required for Aurora MySQL version 1.22 and higher 1.x versions, and global
            engine mode isn't required for any 2.x versions.

            The multimaster engine mode only applies for DB clusters created with Aurora MySQL version 5.6.10a.

            For Aurora PostgreSQL, the global engine mode isn't required, and both the parallelquery and the
            multimaster engine modes currently aren't supported.

            Limitations and requirements apply to some DB engine modes. For more information, see the following
            sections in the Amazon Aurora User Guide:

                * Limitations of Aurora Serverless v1
                * Limitations of Parallel Query
                * Limitations of Aurora Global Databases
                * Limitations of Multi-Master Clusters

            * Valid for: Aurora DB clusters only. Defaults to None.

        scaling_configuration(dict[str, Any], Optional):
            For DB clusters in serverless DB engine mode, the scaling properties of the DB cluster. Valid
            for: Aurora DB clusters only. Defaults to None.

            * MinCapacity (int, Optional):
                The minimum capacity for an Aurora DB cluster in serverless DB engine mode. For Aurora MySQL, valid
                capacity values are 1, 2, 4, 8, 16, 32, 64, 128, and 256. For Aurora PostgreSQL, valid capacity values
                are 2, 4, 8, 16, 32, 64, 192, and 384. The minimum capacity must be less than or equal to the maximum
                capacity.

            * MaxCapacity (int, Optional):
                The maximum capacity for an Aurora DB cluster in serverless DB engine mode. For Aurora MySQL, valid
                capacity values are 1, 2, 4, 8, 16, 32, 64, 128, and 256. For Aurora PostgreSQL, valid capacity values
                are 2, 4, 8, 16, 32, 64, 192, and 384. The maximum capacity must be greater than or equal to the
                minimum capacity.

            * AutoPause (bool, Optional):
                A value that indicates whether to allow or disallow automatic pause for an Aurora DB cluster in
                serverless DB engine mode. A DB cluster can be paused only when it's idle (it has no connections).  If
                a DB cluster is paused for more than seven days, the DB cluster might be backed up with a snapshot. In
                this case, the DB cluster is restored when there is a request to connect to it.

            * SecondsUntilAutoPause (int, Optional):
                The time, in seconds, before an Aurora DB cluster in serverless mode is paused. Specify a value between
                300 and 86,400 seconds.

            * TimeoutAction (str, Optional):
                The action to take when the timeout is reached, either ForceApplyCapacityChange or
                RollbackCapacityChange.

                ForceApplyCapacityChange sets the capacity to the specified value as soon as possible.

                RollbackCapacityChange, the default, ignores the capacity change if a scaling point isn't found in the
                timeout period.

                If you specify ForceApplyCapacityChange, connections that prevent Aurora Serverless v1 from finding a
                scaling point might be dropped.  For more information, see  Autoscaling for Aurora Serverless v1 in the
                Amazon Aurora User Guide.

            * SecondsBeforeTimeout (int, Optional):
                The amount of time, in seconds, that Aurora Serverless v1 tries to find a scaling point to perform
                seamless scaling before enforcing the timeout action. The default is 300. Specify a value between 60
                and 600 seconds.

        deletion_protection(bool, Optional):
            A value that indicates whether the DB cluster has deletion protection enabled. The database can't be
            deleted when deletion protection is enabled. By default, deletion protection isn't enabled. Valid for:
            Aurora DB clusters and Multi-AZ DB clusters. Defaults to None.

        global_cluster_identifier(str, Optional):
            The global cluster ID of an Aurora cluster that becomes the primary cluster in the new global database
            cluster. Valid for: Aurora DB clusters only. Defaults to None.

        enable_http_endpoint(bool, Optional):
            A value that indicates whether to enable the HTTP endpoint for an Aurora Serverless v1 DB cluster. By
            default, the HTTP endpoint is disabled. When enabled, the HTTP endpoint provides a connectionless web
            service API for running SQL queries on the Aurora Serverless v1 DB cluster.  You can also query your
            database from inside the RDS console with the query editor. For more information, see Using the Data API
            for Aurora Serverless v1 in the Amazon Aurora User Guide.

            * Valid for: Aurora DB clusters only. Defaults to None.

        copy_tags_to_snapshot(bool, Optional):
            A value that indicates whether to copy all tags from the DB cluster to snapshots of the DB cluster. The
            default is not to copy them.

            * Valid for: Aurora DB clusters and Multi-AZ DB clusters. Defaults to None.

        domain(str, Optional):
            The Active Directory directory ID to create the DB cluster in. For Amazon Aurora DB clusters, Amazon RDS
            can use Kerberos authentication to authenticate users that connect to the DB cluster.  For more
            information, see Kerberos authentication in the Amazon Aurora User Guide.

            * Valid for: Aurora DB clusters only. Defaults to None.

        domain_iam_role_name(str, Optional):
            Specify the name of the IAM role to be used when making API calls to the Directory Service.

            * Valid for: Aurora DB clusters only. Defaults to None.

        enable_global_write_forwarding(bool, Optional):
            A value that indicates whether to enable this DB cluster to forward write operations to the primary cluster
            of an Aurora global database (GlobalCluster). By default, write operations are not allowed on Aurora DB
            clusters that are secondary clusters in an Aurora global database. You can set this value only on Aurora DB
            clusters that are members of an Aurora global database.  With this parameter enabled, a secondary cluster
            can forward writes to the current primary cluster and the resulting changes are replicated back to this
            cluster. For the primary DB cluster of an Aurora global database, this value is used immediately if the
            primary is demoted by the FailoverGlobalCluster API operation, but it does nothing until then.

            * Valid for: Aurora DB clusters only. Defaults to None.

        db_cluster_instance_class(str, Optional):
            The compute and memory capacity of each DB instance in the Multi-AZ DB cluster, for example
            ``db.m6g.xlarge``. Not all DB instance classes are available in all Amazon Web Services Regions, or for all
            database engines. For the full list of DB instance classes and availability for your engine, see DB
            instance class in the Amazon RDS User Guide. This setting is required to create a Multi-AZ DB cluster.

            * Valid for: Multi-AZ DB clusters only. Defaults to None.

        allocated_storage(int, Optional):
            The amount of storage in gibibytes (GiB) to allocate to each DB instance in the Multi-AZ DB cluster. This
            setting is required to create a Multi-AZ DB cluster.

            * Valid for: Multi-AZ DB clusters only. Defaults to None.

        storage_type(str, Optional):
            Specifies the storage type to be associated with the DB cluster. This setting is required to create a
            Multi-AZ DB cluster.

            * Valid values: io1  When specified, a value for the Iops parameter is required.
            * Default: io1
            * Valid for: Multi-AZ DB clusters only.

        iops(int, Optional):
            The amount of Provisioned IOPS (input/output operations per second) to be initially allocated for each DB
            instance in the Multi-AZ DB cluster. For information about valid Iops values, see Amazon RDS Provisioned
            IOPS storage to improve performance in the Amazon RDS User Guide. This setting is required to create a
            Multi-AZ DB cluster.

            * Constraints: Must be a multiple between .5 and 50 of the storage amount for the DB cluster.
            * Valid for: Multi-AZ DB clusters only. Defaults to None.

        publicly_accessible(bool, Optional):
            A value that indicates whether the DB cluster is publicly accessible. When the DB cluster is publicly
            accessible, its Domain Name System (DNS) endpoint resolves to the private IP address from within the DB
            cluster's virtual private cloud (VPC). It resolves to the public IP address from outside of the DB
            cluster's VPC. Access to the DB cluster is ultimately controlled by the security group it uses. That public
            access isn't permitted if the security group assigned to the DB cluster doesn't permit it. When the DB
            cluster isn't publicly accessible, it is an internal DB cluster with a DNS name that resolves to a private
            IP address.

            Default:
                The default behavior varies depending on whether DBSubnetGroupName is specified. If DBSubnetGroupName
                isn't specified, and PubliclyAccessible isn't specified, the following applies: If the default VPC in
                the target Region doesn’t have an internet gateway attached to it, the DB cluster is private. If the
                default VPC in the target Region has an internet gateway attached to it, the DB cluster is public. If
                DBSubnetGroupName is specified, and PubliclyAccessible isn't specified, the following applies: If the
                subnets are part of a VPC that doesn’t have an internet gateway attached to it, the DB cluster is
                private. If the subnets are part of a VPC that has an internet gateway attached to it, the DB cluster
                is public.

            * Valid for: Multi-AZ DB clusters only. Defaults to None.

        auto_minor_version_upgrade(bool, Optional):
            A value that indicates whether minor engine upgrades are applied automatically to the DB cluster during the
            maintenance window. By default, minor engine upgrades are applied automatically.

            * Valid for: Multi-AZ DB clusters only.

        monitoring_interval(int, Optional):
            The interval, in seconds, between points when Enhanced Monitoring metrics are collected for the DB cluster.
            To turn off collecting Enhanced Monitoring metrics, specify 0.

            * The default is 0. If MonitoringRoleArn is specified, also set MonitoringInterval to a value other than 0.
              Valid Values: 0, 1, 5, 10, 15, 30, 60

            * Valid for: Multi-AZ DB clusters only.

        monitoring_role_arn(str, Optional):
            The Amazon Resource Name (ARN) for the IAM role that permits RDS to send Enhanced Monitoring metrics to
            Amazon CloudWatch Logs. An example is arn:aws:iam:123456789012:role/emaccess. For information on creating a
            monitoring role, see Setting up and enabling Enhanced Monitoring in the Amazon RDS User Guide.

            * If MonitoringInterval is set to a value other than 0, supply a MonitoringRoleArn value.
            * Valid for: Multi-AZ DB clusters only. Defaults to None.

        enable_performance_insights(bool, Optional):
            A value that indicates whether to turn on Performance Insights for the DB cluster. For more information,
            see  Using Amazon Performance Insights in the Amazon RDS User Guide.

            * Valid for: Multi-AZ DB clusters only. Defaults to None.

        performance_insights_kms_key_id(str, Optional):
            The Amazon Web Services KMS key identifier for encryption of Performance Insights data. The Amazon Web
            Services KMS key identifier is the key ARN, key ID, alias ARN, or alias name for the KMS key. If you don't
            specify a value for PerformanceInsightsKMSKeyId, then Amazon RDS uses your default KMS key. There is a
            default KMS key for your Amazon Web Services account. Your Amazon Web Services account has a different
            default KMS key for each Amazon Web Services Region.

            * Valid for: Multi-AZ DB clusters only. Defaults to None.

        performance_insights_retention_period(int, Optional):
            The amount of time, in days, to retain Performance Insights data.

            * Valid values are 7 or 731 (2years).
            * Valid for: Multi-AZ DB clusters only. Defaults to None.

        serverless_v2_scaling_configuration(dict[str, Any], Optional):
            Contains the scaling configuration of an Aurora Serverless v2 DB cluster. For more information, see Using
            Amazon Aurora Serverless v2 in the Amazon Aurora User Guide. Defaults to None.

            * MinCapacity (float, Optional):
                The minimum number of Aurora capacity units (ACUs) for a DB instance in an Aurora Serverless v2
                cluster. You can specify ACU values in half-step increments, such as 8, 8.5, 9, and so on. The smallest
                value that you can use is 0.5.

            * MaxCapacity (float, Optional):
                The maximum number of Aurora capacity units (ACUs) for a DB instance in an Aurora Serverless v2
                cluster. You can specify ACU values in half-step increments, such as 40, 40.5, 41, and so on.  The
                largest value that you can use is 128.

        apply_immediately(bool, Optional):
            A value that indicates whether the modifications in this request and any pending modifications are
            asynchronously applied as soon as possible, regardless of the PreferredMaintenanceWindow setting for the DB
            cluster.  If this parameter is disabled, changes to the DB cluster are applied during the next maintenance
            window.  The ApplyImmediately parameter only affects the EnableIAMDatabaseAuthentication,MasterUserPassword
            and NewDBClusterIdentifier values. If the ApplyImmediately parameter is disabled, then changes to the
            EnableIAMDatabaseAuthentication, MasterUserPassword and NewDBClusterIdentifier values are applied during
            the next maintenance window. All other changes are applied immediately,regardless of the value of the
            ApplyImmediately parameter.

        allow_major_version_upgrades(bool, Optional):
            A value that indicates whether major version upgrades are allowed.

        cloudwatch_logs_export_configuration(dict, Optional):
            The configuration setting for the log types to be enabled for export to CloudWatch Logs for a specific DB
            cluster.

        db_instance_parameter_group_name(str, Optional):
            The name of the DB parameter group to apply to all instances of the DB cluster.

        source_region(str, Optional):
            The ID of the region that contains the source for the db cluster. Defaults to None.

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

        timeout(dict, Optional):
            Timeout configuration for create/update of AWS DB Cluster.

            * create(dict):
                Timeout configuration for creating DB Cluster

                * delay(int):
                    The amount of time in seconds to wait between attempts.
                * max_attempts(int):
                    Customized timeout configuration containing delay and max attempts.

            * update(dict):
                Timeout configuration for updating DB Cluster

                * delay(int):
                    The amount of time in seconds to wait between attempts.
                * max_attempts(int):
                    Customized timeout configuration containing delay and max attempts.

    Request Syntax:
        [db-cluster-name]:
          aws.rds.db_cluster.present:
            - availability_zone:'list'
            - backup_retention_period: 'int'
            - database_name: 'string'
            - engine: 'string'
            - engine_version: 'string'
            - port: 'int'
            - master_username: 'string'
            - master_user_password: 'string'
            - preferred_backup_window: 'string'
            - preferred_maintenance_window: 'string'
            - storage_encrypted: 'bool'
            - kms_key_id: 'string'
            - engine_mode: 'string'
            - deletion_protection: 'bool'
            - copy_tags_to_snapshot: 'bool'
            - vpc_security_group_ids: 'list'
            - db_cluster_parameter_group_name: 'string'
            - tags: 'list'


    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            db-cluster-1:
              aws.rds.db_cluster.present:
                - availability_zone:
                    - us-east-2b
                    - us-east-2c
                    - us-east-2a
                - backup_retention_period: 7
                - database_name: dbname123
                - engine: aurora-postgresql
                - engine_version: '12.7'
                - port: 5432
                - master_username: postgres
                - master_user_password: abcd1234
                - preferred_backup_window: 07:41-08:11
                - preferred_maintenance_window: sat:09:29-sat:09:59
                - storage_encrypted: true
                - kms_key_id: arn:aws:kms:us-east-2:537227425989:key/e9e79921-8dda-48d7-afd7-38a64dd8e9b1
                - engine_mode: provisioned
                - deletion_protection: false
                - copy_tags_to_snapshot: true
                - vpc_security_group_ids:
                    - sg-f5eeba9c
                - db_cluster_parameter_group_name: default.aurora-postgresql12
                - tags:
                    - Key: name
                      Value: value
    '''
    result = {
        "comment": [],
        "old_state": None,
        "new_state": None,
        "name": name,
        "result": True,
    }
    params_to_modify = {}
    before = None
    plan_state = None
    resource_updated = False
    if resource_id:
        before = await hub.exec.aws.rds.db_cluster.get(
            ctx,
            resource_id=resource_id,
        )
    tags = (
        hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
        if isinstance(tags, List)
        else tags
    )
    if before:
        result["old_state"] = before["ret"]
        plan_state = copy.deepcopy(result["old_state"])
        resource_arn = before["ret"].get("db_cluster_arn")
        old_tags = result["old_state"].get("tags")
        if tags is not None and old_tags != tags:
            update_tags_ret = await hub.exec.aws.rds.tag.update_rds_tags(
                ctx,
                resource_arn=resource_arn,
                old_tags=old_tags,
                new_tags=tags,
            )
            if not update_tags_ret["result"]:
                result["comment"] = update_tags_ret["comment"]
                result["result"] = False
                return result
            resource_updated = update_tags_ret["result"]
            result["comment"] = update_tags_ret["comment"]
            if ctx.get("test", False) and update_tags_ret["result"]:
                plan_state["tags"] = update_tags_ret["ret"]
        modify_params = OrderedDict(
            {
                "BackupRetentionPeriod": "backup_retention_period",
                "DBClusterParameterGroupName": "db_cluster_parameter_group_name",
                "VpcSecurityGroupIds": "vpc_security_group_ids",
                "Port": "port",
                "OptionGroupName": "option_group_name",
                "PreferredBackupWindow": "preferred_backup_window",
                "PreferredMaintenanceWindow": "preferred_maintenance_window",
                "EnableIAMDatabaseAuthentication": "enable_iam_database_authentication",
                "BacktrackWindow": "backtrack_window",
                "CloudwatchLogsExportConfiguration": "cloudwatch_logs_export_configuration",
                "EngineVersion": "engine_version",
                "AllowMajorVersionUpgrade": "allow_major_version_upgrades",
                "DBInstanceParameterGroupName": "db_instance_parameter_group_name",
                "Domain": "domain",
                "DomainIAMRoleName": "domain_iam_role_name",
                "ScalingConfiguration": "scaling_configuration",
                "DeletionProtection": "deletion_protection",
                "EnableHttpEndpoint": "enable_http_endpoint",
                "CopyTagsToSnapshot": "copy_tags_to_snapshot",
                "EnableGlobalWriteForwarding": "enable_global_write_forwarding",
                "DBClusterInstanceClass": "db_cluster_instance_class",
                "AllocatedStorage": "allocated_storage",
                "StorageType": "storage_type",
                "Iops": "iops",
                "AutoMinorVersionUpgrade": "auto_minor_version_upgrade",
                "MonitoringInterval": "monitoring_interval",
                "MonitoringRoleArn": "monitoring_role_arn",
                "EnablePerformanceInsights": "enable_performance_insights",
                "PerformanceInsightsKMSKeyId": "performance_insights_kms_key_id",
                "PerformanceInsightsRetentionPeriod": "performance_insights_retention_period",
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
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.rds.db_cluster", name=name
                )
                for key, value in params_to_modify.items():
                    plan_state[modify_params.get(key)] = value
            else:
                # apply_immediately is only used in update to decide whether to apply the update immediate or not
                # this property is not returned in describe, so this should not be compared with old_state as this
                # property will not be present in old_state.
                if apply_immediately is not None:
                    params_to_modify["ApplyImmediately"] = apply_immediately
                modify_ret = await hub.exec.boto3.client.rds.modify_db_cluster(
                    ctx, DBClusterIdentifier=resource_id, **params_to_modify
                )
                if not modify_ret["result"]:
                    result["comment"] += modify_ret["comment"]
                    result["result"] = False
                    return result
                resource_updated = resource_updated or modify_ret["result"]

                # Custom Waiter for update
                waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                    default_delay=15,
                    default_max_attempts=40,
                    timeout_config=timeout.get("update") if timeout else None,
                )
                cluster_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
                    name="ClusterModified",
                    operation="DescribeDBClusters",
                    argument=["DBClusters[].Status"],
                    acceptors=update_waiter_acceptors,
                    client=await hub.tool.boto3.client.get_client(ctx, "rds"),
                )
                try:
                    await hub.tool.boto3.client.wait(
                        ctx,
                        "rds",
                        "ClusterModified",
                        cluster_waiter,
                        30,
                        DBClusterIdentifier=resource_id,
                        WaiterConfig=waiter_config,
                    )
                    result["comment"] += hub.tool.aws.comment_utils.update_comment(
                        resource_type="aws.rds.db_cluster", name=name
                    )
                except Exception as e:
                    result["comment"] += [str(e)]
                    result["result"] = False
                    return result

    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "availability_zones": availability_zones,
                    "backup_retention_period": backup_retention_period,
                    "character_set_name": character_set_name,
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
                    "pre_signed_url": pre_signed_url,
                    "enable_iam_database_authentication": enable_iam_database_authentication,
                    "backtrack_window": backtrack_window,
                    "enable_cloudwatch_logs_exports": enable_cloudwatch_logs_exports,
                    "engine_mode": engine_mode,
                    "scaling_configuration": scaling_configuration,
                    "deletion_protection": deletion_protection,
                    "global_cluster_identifier": global_cluster_identifier,
                    "enable_http_endpoint": enable_http_endpoint,
                    "copy_tags_to_snapshot": copy_tags_to_snapshot,
                    "domain": domain,
                    "domain_iam_role_name": domain_iam_role_name,
                    "enable_global_write_forwarding": enable_global_write_forwarding,
                    "db_cluster_instance_class": db_cluster_instance_class,
                    "allocated_storage": allocated_storage,
                    "storage_type": storage_type,
                    "iops": iops,
                    "publicly_accessible": publicly_accessible,
                    "auto_minor_version_upgrade": auto_minor_version_upgrade,
                    "monitoring_interval": monitoring_interval,
                    "monitoring_role_arn": monitoring_role_arn,
                    "enable_performance_insights": enable_performance_insights,
                    "performance_insights_kms_key_id": performance_insights_kms_key_id,
                    "performance_insights_retention_period": performance_insights_retention_period,
                    "source_region": source_region,
                    "apply_immediately": apply_immediately,
                    "allow_major_version_upgrades": allow_major_version_upgrades,
                    "cloudwatch_logs_export_configuration": cloudwatch_logs_export_configuration,
                    "db_instance_parameter_group_name": db_instance_parameter_group_name,
                    "domain_auth_secret_arn": domain_auth_secret_arn,
                    "manage_master_user_password": manage_master_user_password,
                    "master_user_secret_kms_key_id": master_user_secret_kms_key_id,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.rds.db_cluster", name=name
            )
            return result

        ret = await hub.exec.boto3.client.rds.create_db_cluster(
            ctx,
            DBClusterIdentifier=name,
            AvailabilityZones=availability_zones,
            BackupRetentionPeriod=backup_retention_period,
            CharacterSetName=character_set_name,
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
            PreSignedUrl=pre_signed_url,
            EnableIAMDatabaseAuthentication=enable_iam_database_authentication,
            BacktrackWindow=backtrack_window,
            EnableCloudwatchLogsExports=enable_cloudwatch_logs_exports,
            EngineMode=engine_mode,
            ScalingConfiguration=scaling_configuration,
            DeletionProtection=deletion_protection,
            GlobalClusterIdentifier=global_cluster_identifier,
            EnableHttpEndpoint=enable_http_endpoint,
            CopyTagsToSnapshot=copy_tags_to_snapshot,
            Domain=domain,
            DomainIAMRoleName=domain_iam_role_name,
            EnableGlobalWriteForwarding=enable_global_write_forwarding,
            DBClusterInstanceClass=db_cluster_instance_class,
            AllocatedStorage=allocated_storage,
            StorageType=storage_type,
            Iops=iops,
            PubliclyAccessible=publicly_accessible,
            AutoMinorVersionUpgrade=auto_minor_version_upgrade,
            MonitoringInterval=monitoring_interval,
            MonitoringRoleArn=monitoring_role_arn,
            EnablePerformanceInsights=enable_performance_insights,
            PerformanceInsightsKMSKeyId=performance_insights_kms_key_id,
            PerformanceInsightsRetentionPeriod=performance_insights_retention_period,
            SourceRegion=source_region,
            DomainAuthSecretArn=domain_auth_secret_arn,
            ManageMasterUserPassword=manage_master_user_password,
            MasterUserSecretKmsKeyId=master_user_secret_kms_key_id,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        resource_id = ret["ret"]["DBCluster"]["DBClusterIdentifier"]

        # Custom waiter for create
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
            client=await hub.tool.boto3.client.get_client(ctx, "rds"),
        )
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "rds",
                "ClusterCreated",
                cluster_waiter,
                DBClusterIdentifier=resource_id,
                WaiterConfig=waiter_config,
            )
        except Exception as e:
            result["comment"] += [str(e)]
            result["result"] = False
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.rds.db_cluster", name=name
        )

        # In db_cluster some parameters can only be applied while modifying the resource, if user specify these
        # parameters while creating the resource we apply them after creating the resource.
        if (
            apply_immediately
            or allow_major_version_upgrades
            or cloudwatch_logs_export_configuration
            or db_instance_parameter_group_name
        ):
            modify_ret = await hub.exec.boto3.client.rds.modify_db_cluster(
                ctx,
                DBClusterIdentifier=resource_id,
                ApplyImmediately=apply_immediately,
                AllowMajorVersionUpgrade=allow_major_version_upgrades,
                CloudwatchLogsExportConfiguration=cloudwatch_logs_export_configuration,
                DBInstanceParameterGroupName=db_instance_parameter_group_name,
            )
            if not modify_ret["result"]:
                result["comment"] += modify_ret["comment"]
                result["result"] = False
                return result
            # Custom Waiter for update
            waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                default_delay=15,
                default_max_attempts=40,
                timeout_config=timeout.get("update") if timeout else None,
            )
            cluster_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
                name="ClusterModified",
                operation="DescribeDBClusters",
                argument=["DBClusters[].Status"],
                acceptors=update_waiter_acceptors,
                client=await hub.tool.boto3.client.get_client(ctx, "rds"),
            )
            try:
                await hub.tool.boto3.client.wait(
                    ctx,
                    "rds",
                    "ClusterModified",
                    cluster_waiter,
                    30,
                    DBClusterIdentifier=resource_id,
                    WaiterConfig=waiter_config,
                )
            except Exception as e:
                result["comment"] += [str(e)]
                result["result"] = False
                return result

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif (not before) or resource_updated:
        after = await hub.exec.aws.rds.db_cluster.get(
            ctx,
            resource_id=resource_id,
        )
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
    """The DeleteDBCluster action deletes a previously provisioned DB cluster.

    When you delete a DB cluster, all automated backups for that DB cluster are deleted and can't be recovered. Manual
    DB cluster snapshots of the specified DB cluster are not deleted. For more information on Amazon Aurora, see What
    is Amazon Aurora? in the Amazon Aurora User Guide.  For more information on Multi-AZ DB clusters, see  Multi-AZ
    deployments with two readable standby DB instances in the Amazon RDS User Guide. The Multi-AZ DB clusters feature
    is in preview and is subject to change.

    Args:
        name(str):
            Idem name to identify the resource.

        resource_id(str, Optional):
            AWS ID to identify the resource.

        skip_final_snapshot(bool, Optional):
            Mention this true if you want to skip creating snapshot default is false.

        final_db_snapshot_identifier(str, Optional):
            Identifier for the created final db_snapshot. If skip_final_snapshot is not specified or False(which is the default),
            final_db_snapshot_identifier will be auto generated.

        timeout(dict, Optional):
            Timeout configuration for deletion of AWS DB Cluster.

            * delete(dict):
                Timeout configuration for deletion of a DB Cluster

                * delay(int): The amount of time in seconds to wait between attempts.
                * max_attempts(int): Customized timeout configuration containing delay and max attempts.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            test-db-cluster:
              aws.rds.db_cluster.absent:
                - resource_id: test-db-cluster
                - skip_final_snapshot: true
    """
    result = {
        "comment": [],
        "old_state": "",
        "new_state": "",
        "name": name,
        "result": True,
    }

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.rds.db_cluster", name=name
        )
        return result

    before = await hub.exec.aws.rds.db_cluster.get(
        ctx,
        resource_id=resource_id,
    )

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.rds.db_cluster", name=name
        )

    else:
        result["old_state"] = before["ret"]
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.rds.db_cluster", name=name
            )
            return result
        # we need at least one of these parameters. If the user provide neither of them,
        # we assume db_snapshot name to be name appended with unique id., so that we can back up the db instance before
        # deletion.
        if skip_final_snapshot is False and final_db_snapshot_identifier is None:
            final_db_snapshot_identifier = name + "-" + str(uuid.uuid4())
        ret = await hub.exec.boto3.client.rds.delete_db_cluster(
            ctx,
            DBClusterIdentifier=resource_id,
            SkipFinalSnapshot=skip_final_snapshot,
            FinalDBSnapshotIdentifier=final_db_snapshot_identifier,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            result["result"] = False
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
            client=await hub.tool.boto3.client.get_client(ctx, "rds"),
        )
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "rds",
                "ClusterDelete",
                cluster_waiter,
                DBClusterIdentifier=resource_id,
                WaiterConfig=waiter_config,
            )
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.rds.db_cluster", name=name
            )
        except Exception as e:
            result["comment"] += [str(e)]
            result["result"] = False
            return result

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns information about Amazon Aurora DB clusters and Multi-AZ DB clusters. This API supports pagination. For
    more information on Amazon Aurora DB clusters, see  What is Amazon Aurora? in the Amazon Aurora User Guide.  For
    more information on Multi-AZ DB clusters, see  Multi-AZ deployments with two readable standby DB instances in
    the Amazon RDS User Guide.   The Multi-AZ DB clusters feature is in preview and is subject to change.  This
    operation can also return information for Amazon Neptune DB instances and Amazon DocumentDB instances.


    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.rds.db_cluster
    """
    result = {}
    ret = await hub.exec.boto3.client.rds.describe_db_clusters(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe db_cluster {ret['comment']}")
        return {}

    for db_cluster in ret["ret"]["DBClusters"]:
        # Including fields to match the 'present' function parameters
        resource_id = db_cluster.get("DBClusterIdentifier")
        resource_translated = (
            hub.tool.aws.rds.conversion_utils.convert_raw_db_cluster_to_present(
                raw_resource=db_cluster, idem_resource_name=resource_id
            )
        )
        result[resource_id] = {
            "aws.rds.db_cluster.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result
