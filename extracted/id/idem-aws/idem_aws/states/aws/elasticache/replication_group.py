"""State module for managing Amazon Elasticache Replication Groups."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

TREQ = {
    "present": {
        "require": [
            "aws.elasticache.cache_subnet_group.present",
            "aws.elasticache.cache_parameter_group.present",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    replication_group_description: str,
    resource_id: str = None,
    global_replication_group_id: str = None,
    primary_cluster_id: str = None,
    automatic_failover_enabled: bool = None,
    multi_az_enabled: bool = None,
    num_cache_clusters: int = None,
    preferred_cache_cluster_a_zs: List[str] = None,
    num_node_groups: int = None,
    replicas_per_node_group: int = None,
    node_group_configuration: List[
        make_dataclass(
            """A list of node group (shard) configuration options."""
            "NodeGroupConfiguration",
            [
                ("NodeGroupId", str, field(default=None)),
                ("Slots", str, field(default=None)),
                ("ReplicaCount", int, field(default=None)),
                ("PrimaryAvailabilityZone", str, field(default=None)),
                ("ReplicaAvailabilityZones", List[str], field(default=None)),
                ("PrimaryOutpostArn", str, field(default=None)),
                ("ReplicaOutpostArns", List[str], field(default=None)),
            ],
        )
    ] = None,
    cache_node_type: str = None,
    engine: str = None,
    engine_version: str = None,
    cache_parameter_group_name: str = None,
    cache_subnet_group_name: str = None,
    cache_security_group_names: List[str] = None,
    security_group_ids: List[str] = None,
    tags: Dict[str, str] = None,
    snapshot_arns: List[str] = None,
    snapshot_name: str = None,
    preferred_maintenance_window: str = None,
    port: int = None,
    notification_topic_arn: str = None,
    auto_minor_version_upgrade: bool = None,
    snapshot_retention_limit: int = None,
    snapshot_window: str = None,
    auth_token: str = None,
    transit_encryption_enabled: bool = None,
    at_rest_encryption_enabled: bool = None,
    kms_key_id: str = None,
    user_group_ids: List[str] = None,
    log_delivery_configurations: List[
        make_dataclass(
            """Specifies the destination, format and type of the logs."""
            "LogDeliveryConfigurationRequest",
            [
                ("LogType", str, field(default=None)),
                ("DestinationType", str, field(default=None)),
                (
                    "DestinationDetails",
                    make_dataclass(
                        """Configuration details of either a CloudWatch Logs destination or Kinesis Data Firehose destination."""
                        "DestinationDetails",
                        [
                            (
                                "CloudWatchLogsDetails",
                                make_dataclass(
                                    """The configuration details of the CloudWatch Logs destination."""
                                    "CloudWatchLogsDestinationDetails",
                                    [("LogGroup", str, field(default=None))],
                                ),
                                field(default=None),
                            ),
                            (
                                "KinesisFirehoseDetails",
                                make_dataclass(
                                    """The configuration details of the Kinesis Data Firehose destination."""
                                    "KinesisFirehoseDestinationDetails",
                                    [("DeliveryStream", str, field(default=None))],
                                ),
                                field(default=None),
                            ),
                        ],
                    ),
                    field(default=None),
                ),
                ("LogFormat", str, field(default=None)),
                ("Enabled", bool, field(default=None)),
            ],
        )
    ] = None,
    data_tiering_enabled: bool = None,
    snapshotting_cluster_id: str = None,
    node_group_id: str = None,
    notification_topic_status: str = None,
    apply_immediately: bool = None,
    auto_token_update_strategy: str = None,
    user_group_ids_to_add: List[str] = None,
    user_group_ids_to_remove: List[str] = None,
    remove_user_groups: bool = None,
    timeout: make_dataclass(
        "Timeout",
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
    """Creates a Redis (cluster mode disabled) or a Redis (cluster mode enabled) replication group.

    This resource can be used to create a standalone regional replication group or a secondary replication group associated
    with a Global datastore.

    A Redis (cluster mode disabled) replication group is a collection of clusters, where one of the
    clusters is a read/write primary and the others are read-only replicas. Writes to the primary are asynchronously
    propagated to the replicas.

    A Redis cluster-mode enabled cluster is comprised of from 1 to 90 shards. Each shard has a primary node and up to
    5 read-only replica nodes. The configuration can range from 90 shards and 0 replicas to 15 shards and 5 replicas,
    which is the maximum number or replicas allowed

    The node or shard limit can be increased to a maximum of 500 per cluster if the Redis engine version is 5.0.6 or
    higher. For example, you can choose to configure a 500 node cluster that ranges between 83 shards (one primary
    and 5 replicas per shard) and 500 shards (single primary and no replicas). Make sure there are enough available
    IP addresses to accommodate the increase. Common pitfalls include the subnets in the subnet group have too small
    a CIDR range or the subnets are shared and heavily used by other clusters. For more information, see Creating a
    Subnet Group. For versions below 5.0.6, the limit is 250 per cluster.

    To request a limit increase, see Amazon Service Limits and choose the limit type Nodes per cluster per instance type.

    When a Redis (cluster mode disabled) replication group has been successfully created, you can add one or more read replicas to it, up to a
    total of 5 read replicas. If you need to increase or decrease the number of node groups (console: shards), you
    can avail yourself of ElastiCache for Redis' scaling. For more information, see Scaling ElastiCache for Redis
    Clusters in the ElastiCache User Guide.  This operation is valid for Redis only.

    Args:
        name(str):
            An Idem name of the resource. It is used as the Replication Group ID during resource creation.
        resource_id(str, Optional):
            The ID of the replication group in Amazon Web Services.
        replication_group_description(str):
            A user-created description for the replication group.
        global_replication_group_id(str, Optional):
            The name of the Global datastore.
        primary_cluster_id(str, Optional):
            The identifier of the cluster that serves as the primary for this replication group. This
            cluster must already exist and have a status of ``available``.

            This parameter is not required if ``num_cache_clusters``, ``num_node_groups``, or ``replicas_per_node_group`` is specified.
        automatic_failover_enabled(bool, Optional):
            Specifies whether a read-only replica is automatically promoted to read/write primary if the existing primary fails.

            .. warning::
                ``automatic_failover_enabled`` must be enabled for Redis (cluster mode enabled) replication groups.

        multi_az_enabled(bool, Optional):
            A flag indicating if you have Multi-AZ enabled to enhance fault tolerance.
        num_cache_clusters(int, Optional):
            The number of clusters this replication group initially has.

            This parameter is not used if there is more than one node group (shard). You should use ``replicas_per_node_group`` instead.

            If ``automatic_failover_enabled`` is ``True``, the value of this parameter must be at least ``2``.
            If ``automatic_failover_enabled`` is ``True``, you can omit this parameter (it will default to ``1``), or you can
            explicitly set it to a value between ``2`` and ``6``.

            The maximum permitted value for ``num_cache_clusters`` is ``6`` (``1`` primary plus ``5`` replicas).
        preferred_cache_cluster_a_zs(list, Optional):
            A list of EC2 Availability Zones in which the replication group's clusters are created. The
            order of the Availability Zones in the list is the order in which clusters are allocated. The
            primary cluster is created in the first AZ in the list.

            This parameter is not used if there is more than one node group (shard). You should use ``node_group_configuration`` instead.

            .. note::
                If you are creating your replication group in an Amazon VPC (recommended), you can only locate clusters in
                Availability Zones associated with the subnets in the selected subnet group. The number of
                Availability Zones listed must equal the value of ``num_cache_clusters``.
        num_node_groups(int, Optional):
            An optional parameter that specifies the number of node groups (shards) for this Redis (cluster
            mode enabled) replication group. For Redis (cluster mode disabled) either omit this parameter or
            set it to ``1``.
        replicas_per_node_group(int, Optional):
            An optional parameter that specifies the number of replica nodes in each node group (shard).
            Valid values are ``0`` to ``5``.
        node_group_configuration(list, Optional):
            A list of node group (shard) configuration options.

            Each node group (shard) configuration has the following members: ``PrimaryAvailabilityZone``,
            ``ReplicaAvailabilityZones``, ``ReplicaCount``, and ``Slots``.

            If you're creating a Redis (cluster mode disabled) or a Redis (cluster mode enabled) replication group,
            you can use this parameter to individually configure each node group (shard), or you can omit this parameter.
            However, it is required when seeding a Redis (cluster mode enabled) cluster from a S3 rdb file. You must
            configure each node group (shard) using this parameter because you must specify the slots for each node group.

            * NodeGroupId (*str, Optional*):
                Either the ElastiCache for Redis supplied 4-digit id or a user supplied id for the node group these configuration values apply to.
            * Slots (*str, Optional*):
                A string that specifies the keyspace for a particular node group. Keyspaces range from ``0`` to ``16,383``.
                The string is in the format ``startkey-endkey``.
            * ReplicaCount (*int, Optional*):
                The number of read replica nodes in this node group (shard).
            * PrimaryAvailabilityZone (*str, Optional*):
                The Availability Zone where the primary node of this node group (shard) is launched.
            * ReplicaAvailabilityZones (*list, Optional*):
                A list of Availability Zones to be used for the read replicas. The number of Availability Zones in this list
                must match the value of ``ReplicaCount`` or ``ReplicasPerNodeGroup`` if not specified.
            * PrimaryOutpostArn (*str, Optional*):
                The outpost ARN of the primary node.
            * ReplicaOutpostArns (*list, optional*):
                The outpost ARN of the node replicas.

        cache_node_type(str, Optional):
            The compute and memory capacity of the nodes in the node group (shard).

            The following node types are supported by ElastiCache. Generally speaking, the current generation types provide more
            memory and computational power at lower cost when compared to their equivalent previous generation counterparts.

            * General purpose:
                - Current generation:
                    * **M6g node types** (available only for Redis engine version 5.0.6 onward and for Memcached engine version 1.5.16 onward): ``cache.m6g.large``,
                        ``cache.m6g.xlarge``, ``cache.m6g.2xlarge``, ``cache.m6g.4xlarge``, ``cache.m6g.8xlarge``, ``cache.m6g.12xlarge``, ``cache.m6g.16xlarge``.
                    * **M5 node types**: ``cache.m5.large``, ``cache.m5.xlarge``, ``cache.m5.2xlarge``, ``cache.m5.4xlarge``, ``cache.m5.12xlarge``, ``cache.m5.24xlarge``.
                    * **M4 node types**: ``cache.m4.large``, ``cache.m4.xlarge``, ``cache.m4.2xlarge``, ``cache.m4.4xlarge``, ``cache.m4.10xlarge``.
                    * **T4g node types** (available only for Redis engine version 5.0.6 onward and Memcached engine version 1.5.16 onward): ``cache.t4g.micro``,
                        ``cache.t4g.small``, ``cache.t4g.medium``.
                    * **T3 node types**: ``cache.t3.micro``, ``cache.t3.small``, ``cache.t3.medium``.
                    * **T2 node types**: ``cache.t2.micro``, ``cache.t2.small``, ``cache.t2.medium``.
                - Previous generation: (not recommended. Existing clusters are still supported but creation of new clusters is not supported for these types.):
                    * **T1 node types**: ``cache.t1.micro``.
                    * **M1 node types**: ``cache.m1.small``, ``cache.m1.medium``, ``cache.m1.large``, ``cache.m1.xlarge``.
                    * **M3 node types**: ``cache.m3.medium``, ``cache.m3.large``, ``cache.m3.xlarge``, ``cache.m3.2xlarge``.
            * Compute optimized:
                - Previous generation: (not recommended. Existing clusters are still supported but creation of new clusters is not supported for these types.)
                    * **C1 node types**: ``cache.c1.xlarge``
            * Memory optimized with data tiering:
                - Current generation:
                    * **R6gd node types** (available only for Redis engine version 6.2 onward:) ``cache.r6gd.xlarge``, ``cache.r6gd.2xlarge``,
                        ``cache.r6gd.4xlarge``, ``cache.r6gd.8xlarge``, ``cache.r6gd.12xlarge``, ``cache.r6gd.16xlarge``.
            * Memory optimized:
                - Current generation:
                    * **R6g node types** (available only for Redis engine version 5.0.6 onward and for Memcached engine version 1.5.16 onward): ``cache.r6g.large``,
                        ``cache.r6g.xlarge``, ``cache.r6g.2xlarge``, ``cache.r6g.4xlarge``, ``cache.r6g.8xlarge``, ``cache.r6g.12xlarge``, ``cache.r6g.16xlarge``.
                    * **R5 node types**: ``cache.r5.large``, ``cache.r5.xlarge``, ``cache.r5.2xlarge``, ``cache.r5.4xlarge``, ``cache.r5.12xlarge``, ``cache.r5.24xlarge``.
                    * **R4 node types**: ``cache.r4.large``, ``cache.r4.xlarge``, ``cache.r4.2xlarge``, ``cache.r4.4xlarge``, ``cache.r4.8xlarge``, ``cache.r4.16xlarge``.
                - Previous generation (not recommended. Existing clusters are still supported but creation of new clusters is not supported for these types.):
                    * **M2 node types**: ``cache.m2.xlarge``, ``cache.m2.2xlarge``, ``cache.m2.4xlarge``.
                    * **R3 node types**: ``cache.r3.large``, ``cache.r3.xlarge``, ``cache.r3.2xlarge``, ``cache.r3.4xlarge``, ``cache.r3.8xlarge``.

            .. note::
                Additional node type info

                * All current generation instance types are created in Amazon VPC by default.
                * Redis append-only files (AOF) are not supported for T1 or T2 instances.
                * Redis Multi-AZ with automatic failover is not supported on T1 instances.
                * Redis configuration variables ``appendonly`` and ``appendfsync`` are not supported on Redis version 2.8.22 and later.

        engine(str, Optional):
            The name of the cache engine to be used for the clusters in this replication group. Must be ``Redis``.
        engine_version(str, Optional):
            The version number of the cache engine to be used for the clusters in this replication group.

            .. warning::
                You can upgrade to a newer engine version (see Selecting a Cache Engine and Version
                in the ElastiCache User Guide), but you cannot downgrade to an earlier engine version. If you
                want to use an earlier engine version, you must delete the existing cluster or replication group
                and create it anew with the earlier engine version.
        cache_parameter_group_name(str, Optional):
            The name of the parameter group to associate with this replication group. If this argument is
            omitted, the default cache parameter group for the specified engine is used. If you are running
            Redis version 3.2.4 or later, only one node group (shard), and want to use a default parameter
            group, we recommend that you specify the parameter group by name.

            * To create a Redis (cluster mode disabled) replication group, use ``cache_parameter_group_name=default.redis3.2``.
            * To create a Redis (cluster mode enabled) replication group, use ``cache_parameter_group_name=default.redis3.2.cluster.on``.

        cache_subnet_group_name(str, Optional):
            The name of the cache subnet group to be used for the replication group.

            .. warning::
                If you're going to launch your cluster in an Amazon VPC, you need to create a subnet group before you start
                creating a cluster. For more information, see Subnets and Subnet Groups.

        cache_security_group_names(list, Optional):
            A list of cache security group names to associate with this replication group.
        security_group_ids(list, Optional):
            One or more Amazon VPC security groups associated with this replication group. Use this
            parameter only when you are creating a replication group in an Amazon Virtual Private Cloud
            (Amazon VPC).
        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]`` to associate with the replication group.

            * Key (*str*):
                The key of the tag.
            * Value (*str*):
                The value of the tag.

        snapshot_arns(list, Optional):
            A list of Amazon Resource Names (ARN) that uniquely identify the Redis RDB snapshot files stored
            in Amazon S3. The snapshot files are used to populate the new replication group. The Amazon S3
            object name in the ARN cannot contain any commas. The new replication group will have the number
            of node groups specified by the parameter ``num_node_groups`` or the number of node
            groups configured by ``node_group_configuration`` regardless of the number of ARNs specified here.

            Example of an Amazon S3 ARN: ``arn:aws:s3:::my_bucket/snapshot1.rdb``.
        snapshot_name(str, Optional):
            The name of a snapshot from which to restore data into the new replication group. The snapshot
            status changes to restoring while the new replication group is being created.
        preferred_maintenance_window(str, Optional):
            Specifies the weekly time range during which maintenance on the cluster is performed. It is
            specified as a range in the format ``ddd:hh24:mi-ddd:hh24:mi`` (24H Clock UTC). The minimum
            maintenance window is a 60 minute period. Valid values for ``ddd`` are: ``sun``, ``mon``, ``tue``, ``wed``, ``thu``, ``fri``, ``sat``.

            Example: ``sun:23:00-mon:01:30``.
        port(int, Optional):
            The port number on which each member of the replication group accepts connections.
        notification_topic_arn(str, Optional):
            The Amazon Resource Name (ARN) of the Amazon Simple Notification Service (SNS) topic to which
            notifications are sent.

            .. note::
                The Amazon SNS topic owner must be the same as the cluster owner.

        auto_minor_version_upgrade(bool, Optional):
            If you are running Redis engine version 6.0 or later, set this parameter to yes if you want to
            opt-in to the next auto minor version upgrade campaign. This parameter is disabled for previous
            versions.
        snapshot_retention_limit(int, Optional):
            The number of days for which ElastiCache retains automatic snapshots before deleting them. For
            example, if you set ``snapshot_retention_limit`` to ``5``, a snapshot that was taken today is retained for
            5 days before being deleted.

            Default: ``0`` (i.e., automatic backups are disabled for this cluster).
        snapshot_window(str, Optional):
            The daily time range (in UTC) during which ElastiCache begins taking a daily snapshot of your
            node group (shard).
            Example: ``05:00-09:00``.
            If you do not specify this parameter, ElastiCache automatically chooses an appropriate time range.
        auth_token(str, Optional):
            .. note::
                Reserved parameter. The password used to access a password protected server. ``auth_token`` can be
                specified only on replication groups where ``transit_encryption_enabled`` is ``True``.

            Password constraints:
                * Must be only printable ASCII characters.
                * Must be at least 16 characters and no more than 128 characters in length.
                * The only permitted printable special characters are ``!``, ``&``, ``#``, ``$``, ``^``, ``<``, ``>``, and ``-``. Other printable special characters cannot be  used in the AUTH token.

            For more information, see AUTH password at http://redis.io/commands/AUTH.
        transit_encryption_enabled(bool, Optional):
            A flag that enables in-transit encryption when set to true.

            You cannot modify the value of ``transit_encryption_enabled`` after the cluster is created. To enable in-transit encryption on a
            cluster you must set ``transit_encryption_enabled`` to ``True`` when you create a cluster.

            This parameter is valid only if the ``engine`` parameter is ``redis``, the ``engine_version`` parameter is ``3.2.6``, ``4.x`` or
            later, and the cluster is being created in an Amazon VPC. If you enable in-transit encryption,
            you must also specify a value for ``cache_subnet_group_name``.

            .. note::
                Required: Only available when creating a replication group in an Amazon VPC using redis version ``3.2.6``, ``4.x`` or later.

            .. warning::
                For HIPAA compliance, you must specify ``transit_encryption_enabled`` as ``True``, an ``auth_token``, and a ``cache_subnet_group_name``.

        at_rest_encryption_enabled(bool, Optional):
            A flag that enables encryption at rest when set to ``True``.

            You cannot modify the value of ``at_rest_encryption_enabled`` after the replication group is created.
            To enable encryption at rest on a replication group you must set ``at_rest_encryption_enabled`` to ``True`` when you
            create the replication group.

            .. note::
                Required: Only available when creating a replication group in an Amazon VPC using redis version ``3.2.6``, ``4.x`` or later.
        kms_key_id(str, Optional):
            The ID of the KMS key used to encrypt the disk in the cluster.
        user_group_ids(list, Optional):
            The user group to associate with the replication group.
        log_delivery_configurations(list, Optional):
            Specifies the destination, format and type of the logs.

            * LogType (*str, Optional*):
                Refers to slow-log.
            * DestinationType (*str, Optional*):
                Specify either cloudwatch-logs or kinesis-firehose as the destination type.
            * DestinationDetails (*dict, Optional*):
                Configuration details of either a CloudWatch Logs destination or Kinesis Data Firehose destination.

                * CloudWatchLogsDetails (*dict, Optional*):
                    The configuration details of the CloudWatch Logs destination.

                    * LogGroup (*str, Optional*):
                        The name of the CloudWatch Logs log group.
                * KinesisFirehoseDetails (*dict, Optional*):
                    The configuration details of the Kinesis Data Firehose destination.

                    * DeliveryStream (*str, Optional*):
                        The name of the Kinesis Data Firehose delivery stream.

            * LogFormat (*str, Optional*):
                Specifies either ``JSON`` or ``TEXT``.
            * Enabled (*bool, Optional*):
                Specify if log delivery is enabled.

        data_tiering_enabled(bool, Optional):
            Enables data tiering. Data tiering is only supported for replication groups using the ``r6gd`` node
            type. This parameter must be set to ``True`` when using ``r6gd`` nodes. For more information, see Data
            tiering.
        snapshotting_cluster_id(str, Optional):
            The cluster ID that is used as the daily snapshot source for the replication group. This parameter
            cannot be set for Redis (cluster mode enabled) replication groups.
        node_group_id(str, Optional):
            Deprecated. This parameter is not used.
        notification_topic_status(bool, Optional):
            The Amazon Resource Name (ARN) of the Amazon SNS topic to which notifications are sent.
        apply_immediately(bool, Optional):
            If ``True``, this parameter causes the modifications in this request and any pending modifications to be applied,
            asynchronously and as soon as possible, regardless of the ``preferred_maintenance_window`` setting for the replication group.
            If ``False``, changes to the nodes in the replication group are applied on the next maintenance reboot, or the next failure reboot,
            whichever occurs first.
        auto_token_update_strategy(str, Optional):
            Specifies the strategy to use to update the AUTH token. This parameter must be specified with
            the ``auth_token`` parameter. Possible values: ``Rotate``, and ``Set``. For more information, see Authenticating Users with Redis AUTH
        user_group_ids_to_add(list, Optional):
            The ID of the user group you are associating with the replication group.
        user_group_ids_to_remove(list, Optional):
            The ID of the user group to disassociate from the replication group, meaning the users in the group no longer can
            access the replication group.
        remove_user_groups(bool, Optional):
            Removes the user group associated with this replication group.
        timeout(dict, Optional):
            Timeout configuration for AWS Elasticache Replication Group operations.

            * create (*dict, Optional*):
                Timeout configuration when creating an AWS Elasticache Replication Group.

                * delay (*int, Optional*):
                    The amount of time in seconds to wait between attempts. Default value is ``15``.
                * max_attempts (*int, Optional*):
                    Max attempts of waiting for change. Default value is ``40``.

            * update (*dict, Optional*):
                Timeout configuration when updating an AWS Elasticache Replication Group.

                * delay (*int, Optional*):
                    The amount of time in seconds to wait between attempts. Default value is ``15``.
                * max_attempts (*int, Optional*):
                    Max attempts of waiting for change. Default value is ``40``.

    Request Syntax:
      .. code-block:: sls

        [idem_test_aws_elasticache_replication_group]:
          aws.elasticache.replication_group.present:
            - name: 'string'
            - resource_id: 'string'
            - replication_group_description: 'string'
            - global_replication_group_id: 'string'
            - primary_cluster_id: 'string'
            - automatic_failover_enabled: True|False
            - multi_az_enabled: True|False
            - num_cache_clusters: int
            - preferred_cache_cluster_a_zs:
                - 'string'
            - num_node_groups: int
            - replicas_per_node_group: int
            - node_group_configuration:
                - NodeGroupId: 'string'
                  Slots: 'string'
                  ReplicaCount: 'int'
                  PrimaryAvailabilityZone: 'string'
                  ReplicaAvailabilityZones:
                    - 'string'
                  PrimaryOutpostArn: 'string'
                  ReplicaOutpostArns:
                    - 'string'
            - cache_node_type: 'string'
            - engine: 'string'
            - engine_version: 'string'
            - cache_parameter_group_name: 'string'
            - cache_subnet_group_name: 'string'
            - cache_security_group_names:
                - 'string'
            - security_group_ids:
                - 'string'
            - tags:
                - Key: 'string'
                  Value: 'string'
            - snapshot_arns:
                - 'string'
            - snapshot_name: 'string'
            - preferred_maintenance_window: 'string'
            - port: int
            - notification_topic_arn: 'string'
            - auto_minor_version_upgrade: True|False
            - snapshot_retention_limit: int
            - snapshot_window: 'string'
            - auth_token: 'string'
            - transit_encryption_enabled: True|False
            - at_rest_encryption_enabled: True|False
            - kms_key_id: 'string'
            - user_group_ids:
                - 'string'
            - log_delivery_configurations:
                - LogType: 'string'
                  DestinationType: 'string'
                  DestinationDetails:
                    CloudWatchLogsDetails:
                      LogGroup: 'string'
                    KinesisFirehoseDetails:
                      DeliveryStream: 'string'
                  LogFormat: 'string'
                  Enabled: True|False
            - data_tiering_enabled: True|False
            - snapshotting_cluster_id: 'string'
            - node_group_id: 'string'
            - notification_topic_status: 'string'
            - apply_immediately: True|False
            - auto_token_update_strategy: 'string'
            - user_group_ids_to_add:
                - 'string'
            - user_group_ids_to_remove:
                - 'string'
            - remove_user_groups: True|False
            - timeout:
                create:
                  delay: int
                  max_attemps: int
                update:
                  delay: int
                  max_attemps: int

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_elasticache_replication_group:
              aws.elasticache.replication_group.present:
                - name: 'idem_test_replication_group'
                - replication_group_description: 'My Elasticache Replication Group'
                - num_node_groups: 1
                - num_cache_clusters: 123
                - automatic_failover_enabled: True
                - multi_az_enabled: True
                - engine: 'Redis'
                - cache_node_type: 'cache.t2.micro'
                - cache_subnet_group_name: 'idem_test_cache_subnet_group'
                - cache_parameter_group_name: 'idem_test_cache_parameter_group'
                - cache_security_group_names: 'idem_test_cache_security_group'
                - tags:
                    - Key: 'provider'
                      Value: 'idem'
    """
    result = dict(comment=[], name=name, old_state=None, new_state=None, result=True)
    before = None
    resource_updated = False
    if resource_id:
        before = await hub.exec.aws.elasticache.replication_group.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])
        update_ret = (
            await hub.tool.aws.elasticache.elasticache_utils.update_replication_group(
                ctx,
                name=name,
                resource_id=resource_id,
                plan_state=plan_state,
                old_state=result["old_state"],
                replication_group_description=replication_group_description,
                primary_cluster_id=primary_cluster_id,
                snapshotting_cluster_id=snapshotting_cluster_id,
                automatic_failover_enabled=automatic_failover_enabled,
                multi_az_enabled=multi_az_enabled,
                node_group_id=node_group_id,
                cache_security_group_names=cache_security_group_names,
                security_group_ids=security_group_ids,
                preferred_maintenance_window=preferred_maintenance_window,
                notification_topic_arn=notification_topic_arn,
                cache_parameter_group_name=cache_parameter_group_name,
                notification_topic_status=notification_topic_status,
                apply_immediately=apply_immediately,
                engine_version=engine_version,
                auto_minor_version_upgrade=auto_minor_version_upgrade,
                snapshot_retention_limit=snapshot_retention_limit,
                snapshot_window=snapshot_window,
                cache_node_type=cache_node_type,
                auto_token_update_strategy=auto_token_update_strategy,
                user_group_ids_to_add=user_group_ids_to_add,
                user_group_ids_to_remove=user_group_ids_to_remove,
                remove_user_groups=remove_user_groups,
                log_delivery_configurations=log_delivery_configurations,
            )
        )
        resource_updated = resource_updated or update_ret["result"]
        if not update_ret["result"]:
            result["comment"] += list(update_ret["comment"])
            result["result"] = False
            return result
        # Waiting for the ReplicationGroup status to be available after updates
        waiter_ret = (
            await hub.tool.aws.elasticache.elasticache_utils.replication_group_waiter(
                ctx, name, resource_id, timeout, "update"
            )
        )
        if not waiter_ret["result"]:
            result["result"] = False
            result["comment"] += list(waiter_ret["comment"])
        if tags is not None and tags != result["old_state"].get("tags"):
            # Update tags
            update_ret = await hub.tool.aws.elasticache.elasticache_utils.update_tags(
                ctx=ctx,
                resource_arn=result["old_state"].get("arn"),
                old_tags=result["old_state"].get("tags"),
                new_tags=tags,
                waiter=hub.tool.aws.elasticache.elasticache_utils.replication_group_waiter,
                waiter_args={
                    "ctx": ctx,
                    "name": name,
                    "resource_id": resource_id,
                    "timeout": timeout,
                    "operation_type": "update",
                },
            )
            result["comment"] += list(update_ret["comment"])
            result["result"] = update_ret["result"]
            resource_updated = bool(update_ret["result"])
            if ctx.get("test", False) and resource_updated:
                plan_state["tags"] = update_ret["ret"]
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "replication_group_id": name,
                    "replication_group_description": replication_group_description,
                    "engine": engine,
                    "cache_node_type": cache_node_type,
                    "cache_subnet_group_name": cache_subnet_group_name,
                    "security_group_ids": security_group_ids,
                    "global_replication_group_id": global_replication_group_id,
                    "primary_cluster_id": primary_cluster_id,
                    "automatic_failover_enabled": automatic_failover_enabled,
                    "num_cache_clusters": num_cache_clusters,
                    "preferred_cache_cluster_a_zs": preferred_cache_cluster_a_zs,
                    "num_node_groups": num_node_groups,
                    "replicas_per_node_group": replicas_per_node_group,
                    "node_group_configuration": node_group_configuration,
                    "engine_version": engine_version,
                    "cache_parameter_group_name": cache_parameter_group_name,
                    "cache_security_group_names": cache_security_group_names,
                    "tags": tags,
                    "snapshot_arns": snapshot_arns,
                    "snapshot_name": snapshot_name,
                    "preferred_maintenance_window": preferred_maintenance_window,
                    "port": port,
                    "notification_topic_arn": notification_topic_arn,
                    "auto_minor_version_upgrade": auto_minor_version_upgrade,
                    "snapshot_retention_limit": snapshot_retention_limit,
                    "snapshot_window": snapshot_window,
                    "auth_token": auth_token,
                    "transit_encryption_enabled": transit_encryption_enabled,
                    "at_rest_encryption_enabled": at_rest_encryption_enabled,
                    "kms_key_id": kms_key_id,
                    "user_group_ids": user_group_ids,
                    "log_delivery_configurations": log_delivery_configurations,
                    "data_tiering_enabled": data_tiering_enabled,
                },
            )
            result["comment"] = list(
                hub.tool.aws.comment_utils.would_create_comment(
                    resource_type="aws.elasticache.replication_group", name=name
                )
            )
            return result
        ret = await hub.exec.boto3.client.elasticache.create_replication_group(
            ctx,
            ReplicationGroupId=name,
            ReplicationGroupDescription=replication_group_description,
            Engine=engine,
            CacheNodeType=cache_node_type,
            CacheSubnetGroupName=cache_subnet_group_name,
            SecurityGroupIds=security_group_ids,
            GlobalReplicationGroupId=global_replication_group_id,
            PrimaryClusterId=primary_cluster_id,
            AutomaticFailoverEnabled=automatic_failover_enabled,
            MultiAZEnabled=multi_az_enabled,
            NumCacheClusters=num_cache_clusters,
            PreferredCacheClusterAZs=preferred_cache_cluster_a_zs,
            NumNodeGroups=num_node_groups,
            ReplicasPerNodeGroup=replicas_per_node_group,
            NodeGroupConfiguration=node_group_configuration,
            EngineVersion=engine_version,
            CacheParameterGroupName=cache_parameter_group_name,
            CacheSecurityGroupNames=cache_security_group_names,
            Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
            SnapshotArns=snapshot_arns,
            SnapshotName=snapshot_name,
            PreferredMaintenanceWindow=preferred_maintenance_window,
            Port=port,
            NotificationTopicArn=notification_topic_arn,
            AutoMinorVersionUpgrade=auto_minor_version_upgrade,
            SnapshotRetentionLimit=snapshot_retention_limit,
            SnapshotWindow=snapshot_window,
            AuthToken=auth_token,
            TransitEncryptionEnabled=transit_encryption_enabled,
            AtRestEncryptionEnabled=at_rest_encryption_enabled,
            KmsKeyId=kms_key_id,
            UserGroupIds=user_group_ids,
            LogDeliveryConfigurations=log_delivery_configurations,
            DataTieringEnabled=data_tiering_enabled,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = list(ret["comment"])
            return result
        resource_id = name
        # This makes sure the created replication group is saved to esm regardless if the subsequent update call
        # fails or not.
        result["new_state"] = {"name": name, "resource_id": resource_id}
        # Waiting until the ReplicationGroup creation
        waiter_ret = (
            await hub.tool.aws.elasticache.elasticache_utils.replication_group_waiter(
                ctx, name, resource_id, timeout, "create"
            )
        )
        if not waiter_ret["result"]:
            result["result"] = False
            result["comment"] = list(waiter_ret["comment"])
        result["comment"] = list(
            hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.elasticache.replication_group", name=name
            )
        )
    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif (not before) or resource_updated:
        after = await hub.exec.aws.elasticache.replication_group.get(
            ctx, name=name, resource_id=resource_id
        )
        if not after["result"]:
            result["result"] = False
            result["comment"] += list(after["comment"])
            return result
        result["new_state"] = copy.deepcopy(after["ret"])
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    retain_primary_cluster: bool = None,
    final_snapshot_identifier: str = None,
    timeout: make_dataclass(
        """Timeout configuration for AWS Elasticache Replication Group operations."""
        "Timeout",
        [
            (
                "delete",
                make_dataclass(
                    """Timeout configuration when deleting an AWS Elasticache Replication Group."""
                    "DeleteTimeout",
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
    """Deletes the specified AWS Elasticache Replication Group.

    By default, this operation deletes the entire replication group, including the primary/primaries and all of the read replicas.
    If the replication group has only one primary, you can optionally delete only the read replicas, while retaining the primary
    by setting ``retain_primary_cluster: True``.
    When you receive a successful response from this operation, Amazon ElastiCache immediately begins deleting the selected resources;
    you cannot cancel or revert this operation. This operation is valid for Redis only.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            The ID of the replication group in Amazon Web Services.

            .. warning::
              Idem automatically considers this resource being absent if this field is not specified.

        retain_primary_cluster(bool, Optional):
            If set to ``True``, all of the read replicas are deleted, but the primary node is retained.
        final_snapshot_identifier(str, Optional):
            The name of a final node group (shard) snapshot. ElastiCache creates the snapshot from the
            primary node in the cluster, rather than one of the replicas; this is to ensure that it captures
            the freshest data. After the final snapshot is taken, the replication group is immediately
            deleted.
        timeout(dict, Optional):
            Timeout configuration for AWS Elasticache Replication Group operations.

            * delete (*dict, Optional*):
                Timeout configuration when deleting an AWS Elasticache Replication Group.

                * delay (*int, Optional*) -- The amount of time in seconds to wait between attempts. Default value is ``15``.
                * max_attempts (*int, Optional*) -- Max attempts of waiting for change. Default value is ``40``.

    Request Syntax:
      .. code-block:: sls

        [idem_test_aws_elasticache_replication_group]:
          aws.elasticache.replication_group.absent:
            - name: 'string'
            - resource_id: 'string'
            - retain_primary_cluster: True|False
            - final_snapshot_identifier: 'string'
            - timeout:
                delete:
                  delay: int
                  max_attemps: int

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_elasticache_replication_group:
              aws.elasticache.replication_group.absent:
                - name: 'idem_test_replication_group'
                - resource_id: 'idem_test_replication_group'
    """
    result = dict(comment=[], name=name, old_state=None, new_state=None, result=True)

    if not resource_id:
        result["comment"] = list(
            hub.tool.aws.comment_utils.already_absent_comment(
                resource_type="aws.elasticache.replication_group", name=name
            )
        )
        return result
    before = await hub.exec.aws.elasticache.replication_group.get(
        ctx, name=name, resource_id=resource_id
    )
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = list(
            hub.tool.aws.comment_utils.already_absent_comment(
                resource_type="aws.elasticache.replication_group", name=name
            )
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = list(
            hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.elasticache.replication_group", name=name
            )
        )
        return result
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client.elasticache.delete_replication_group(
            ctx,
            ReplicationGroupId=resource_id,
            RetainPrimaryCluster=retain_primary_cluster,
            FinalSnapshotIdentifier=final_snapshot_identifier,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] += list(ret["comment"])
            result["result"] = False
            return result

        # Waiting for the ReplicationGroup to Delete
        waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
            default_delay=15,
            default_max_attempts=40,
            timeout_config=timeout.get("delete") if timeout else None,
        )
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "elasticache",
                "replication_group_deleted",
                ReplicationGroupId=resource_id,
                WaiterConfig=waiter_config,
            )
        except Exception as e:
            result["comment"] += list(str(e))
            result["result"] = False
        result["comment"] = list(
            hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.elasticache.replication_group", name=name
            )
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes Elasticache Replication Groups in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.elasticache.replication_group
    """
    result = {}
    ret = await hub.exec.boto3.client.elasticache.describe_replication_groups(ctx)

    if not ret["result"]:
        hub.log.warning(
            f"Could not describe aws.elasticache.replication_group {ret['comment']}"
        )
        return {}

    for resource in ret["ret"]["ReplicationGroups"]:
        resource_id = resource.get("ReplicationGroupId")
        tag_ret = await hub.exec.boto3.client.elasticache.list_tags_for_resource(
            ctx, ResourceName=resource.get("ARN")
        )
        if not tag_ret["result"]:
            # Error fetching tags. If fetching tags itself fails, just skip this and continue. Since tags are
            # optional, they need not be associated with all replication groups. But API needs to succeed.
            hub.log.warning(
                f"Failed listing tags for aws.elasticache.replication_group '{resource.get('ARN')}' with error {tag_ret['comment']}"
                f"Describe will skip this aws.elasticache.replication_group and continue. "
            )
            continue
        resource["Tags"] = tag_ret["ret"].get("TagList", [])
        resource_translated = await hub.tool.aws.elasticache.conversion_utils.convert_raw_elasticache_replication_group_to_present_async(
            ctx=ctx,
            raw_resource=resource,
            idem_resource_name=resource_id,
        )
        result[resource_id] = {
            "aws.elasticache.replication_group.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }
    return result
