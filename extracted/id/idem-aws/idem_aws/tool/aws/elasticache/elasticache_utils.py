import copy
from collections import OrderedDict
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List


async def update_tags(
    hub,
    ctx,
    resource_arn: str,
    old_tags: Dict[str, Any],
    new_tags: Dict[str, Any],
    waiter=None,
    waiter_args: Dict[str, Any] = None,
):
    """

    Args:
        hub:
        ctx:
        resource_arn(str): aws elasticache arn
        old_tags(Dict[str, Any]): dict of old tags in the format of {tag-key: tag-value}
        new_tags(Dict[str, Any]): dict of new tags in the format of {tag-key: tag-value}. If this value is None, the function will do no operation on tags.
        waiter: waiter function to wait for the resource to be in available status after update.
        waiter_args(Dict[str, Any]): arguments provided for waiter function to execute.

    Returns:
        {"result": True|False, "comment": "A message tuple", "ret": dict of updated tags}

    """

    result = dict(comment=[], result=True, ret=None)

    tags_to_add = {}
    tags_to_delete = {}
    if new_tags is not None:
        tags_to_delete, tags_to_add = hub.tool.aws.tag_utils.diff_tags_dict(
            old_tags=old_tags, new_tags=new_tags
        )
    if (not tags_to_delete) and (not tags_to_add):
        result["ret"] = copy.deepcopy(old_tags if old_tags else {})
        return result

    if not ctx.get("test", False) and tags_to_delete:
        delete_tag_resp = (
            await hub.exec.boto3.client.elasticache.remove_tags_from_resource(
                ctx, ResourceName=resource_arn, TagKeys=list(tags_to_delete.keys())
            )
        )
        if not delete_tag_resp["result"]:
            hub.log.debug(
                f"Could not delete tags {tags_to_delete} for resource: '{resource_arn}' due to the error: {delete_tag_resp['comment']}"
            )
            result["comment"] = delete_tag_resp["comment"]
            result["result"] = False
            return result

        if waiter:
            # Optional waiter to wait for the resource to be in available status after updating the tags as the
            # resource might be in modifying status
            waiter_ret = await waiter(**waiter_args)
            if not waiter_ret["result"]:
                result["result"] = False
                result["comment"] += waiter_ret["comment"]

    if not ctx.get("test", False) and tags_to_add:
        create_tag_resp = await hub.exec.boto3.client.elasticache.add_tags_to_resource(
            ctx,
            ResourceName=resource_arn,
            Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags=tags_to_add),
        )
        if not create_tag_resp["result"]:
            hub.log.debug(
                f"Could not create tags {tags_to_add} for resource: '{resource_arn}' due to the error: {create_tag_resp['comment']}"
            )
            result["comment"] = create_tag_resp["comment"]
            result["result"] = False
            return result

        if waiter:
            # Optional waiter to wait for the resource to be in available status after updating the tags as the
            # resource might be in modifying status
            waiter_ret = await waiter(**waiter_args)
            if not waiter_ret["result"]:
                result["result"] = False
                result["comment"] += waiter_ret["comment"]
    result["ret"] = new_tags
    if ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_update_tags_comment(
            tags_to_remove=tags_to_delete, tags_to_add=tags_to_add
        )
    else:
        result["comment"] = hub.tool.aws.comment_utils.update_tags_comment(
            tags_to_remove=tags_to_delete, tags_to_add=tags_to_add
        )
    return result


def get_updated_cache_parameter_group(hub, old_paramaters, parameter_name_values):
    """
    Checks if the input ParameterNamesValues needs to be updated and returns a list of parameters that needs to be modified.

    Args:

        old_parameters: The detailed parameter list for a particular cache parameter group.
        parameter_name_values: Parameters Values as needed by the user.

    Returns:
        [
            {
                "ParameterName": "Text",
                "ParameterValue": "Text"
            },
        ]
    """
    final_parameters = []
    old_parameter_map = {
        params.get("ParameterName"): params for params in old_paramaters
    }
    if parameter_name_values:
        for new_parameters in parameter_name_values:
            if new_parameters.get("ParameterName") in old_parameter_map:
                if not new_parameters.get("ParameterValue") == old_parameter_map.get(
                    new_parameters.get("ParameterName")
                ).get("ParameterValue"):
                    final_parameters.append(new_parameters)
    return final_parameters


async def update_replication_group(
    hub,
    ctx,
    name,
    resource_id: str,
    old_state: Dict[str, Any] = None,
    plan_state: Dict[str, Any] = None,
    replication_group_description: str = None,
    primary_cluster_id: str = None,
    snapshotting_cluster_id: str = None,
    automatic_failover_enabled: bool = None,
    multi_az_enabled: bool = None,
    node_group_id: str = None,
    cache_security_group_names: List[str] = None,
    security_group_ids: List[str] = None,
    preferred_maintenance_window: str = None,
    notification_topic_arn: str = None,
    cache_parameter_group_name: str = None,
    notification_topic_status: str = None,
    apply_immediately: bool = None,
    engine_version: str = None,
    auto_minor_version_upgrade: bool = None,
    snapshot_retention_limit: int = None,
    snapshot_window: str = None,
    cache_node_type: str = None,
    auto_token_update_strategy: str = None,
    user_group_ids_to_add: List[str] = None,
    user_group_ids_to_remove: List[str] = None,
    remove_user_groups: bool = None,
    log_delivery_configurations: List[
        make_dataclass(
            "LogDeliveryConfigurationRequest",
            [
                ("LogType", str, field(default=None)),
                ("DestinationType", str, field(default=None)),
                (
                    "DestinationDetails",
                    make_dataclass(
                        "DestinationDetails",
                        [
                            (
                                "CloudWatchLogsDetails",
                                make_dataclass(
                                    "CloudWatchLogsDestinationDetails",
                                    [("LogGroup", str, field(default=None))],
                                ),
                                field(default=None),
                            ),
                            (
                                "KinesisFirehoseDetails",
                                make_dataclass(
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
):
    """
    Modifies the settings for a replication group.
    - Scaling for Amazon ElastiCache for Redis (cluster mode enabled) in the ElastiCache User Guide
    - ModifyReplicationGroupShardConfiguration in the ElastiCache API Reference
    Note: This operation is valid for Redis only.

    Args:
        name(str): An Idem name of the resource. It is used as ReplicationGroupID during resource creation
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        replication_group_description(str): A user-created description for the replication group.
        primary_cluster_id(str, Optional): The identifier of the cluster that serves as the primary for this replication group. This
            cluster must already exist and have a status of available. This parameter is not required if
            NumCacheClusters, NumNodeGroups, or ReplicasPerNodeGroup is specified. Defaults to None.
        snapshotting_cluster_id (str, Optional): The cluster ID that is used as the daily snapshot source for the replication group. This parameter
                    cannot be set for Redis (cluster mode enabled) replication groups.
        automatic_failover_enabled(bool, Optional): Specifies whether a read-only replica is automatically promoted to read/write primary if the
            existing primary fails.  AutomaticFailoverEnabled must be enabled for Redis (cluster mode
            enabled) replication groups. Default: false. Defaults to None.
        multi_az_enabled(bool, Optional): A flag indicating if you have Multi-AZ enabled to enhance fault tolerance. For more information,
            see Minimizing Downtime: Multi-AZ. Defaults to None.
        node_group_id(str, Optional): Deprecated. This parameter is not used.
        notification_topic_status(bool, Optional): The Amazon Resource Name (ARN) of the Amazon SNS topic to which notifications are sent.
        apply_immediately(bool, Optional): If true , this parameter causes the modifications in this request and any pending modifications to be applied,
            asynchronously and as soon as possible, regardless of the PreferredMaintenanceWindow setting for the replication group.
            If false , changes to the nodes in the replication group are applied on the next maintenance reboot, or the next failure reboot,
            whichever occurs first.
            Valid values: true | false
            Default: false
        cache_security_group_names(List[str], Optional): A list of cache security group names to associate with this replication group. Defaults to None.
        security_group_ids(List[str], Optional): One or more Amazon VPC security groups associated with this replication group. Use this
            parameter only when you are creating a replication group in an Amazon Virtual Private Cloud
            (Amazon VPC). Defaults to None.
        preferred_maintenance_window(str, Optional): Specifies the weekly time range during which maintenance on the cluster is performed. It is
            specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum
            maintenance window is a 60 minute period. Valid values for ddd are: Specifies the weekly time
            range during which maintenance on the cluster is performed. It is specified as a range in the
            format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute
            period. Valid values for ddd are:    sun     mon     tue     wed     thu     fri     sat
            Example: sun:23:00-mon:01:30. Defaults to None.
        engine_version(str, Optional): The version number of the cache engine to be used for the clusters in this replication group. To
            view the supported cache engine versions, use the DescribeCacheEngineVersions operation.
            Important: You can upgrade to a newer engine version (see Selecting a Cache Engine and Version)
            in the ElastiCache User Guide, but you cannot downgrade to an earlier engine version. If you
            want to use an earlier engine version, you must delete the existing cluster or replication group
            and create it anew with the earlier engine version. Defaults to None.
        auto_minor_version_upgrade(bool, Optional):  If you are running Redis engine version 6.0 or later, set this parameter to yes if you want to
            opt-in to the next auto minor version upgrade campaign. This parameter is disabled for previous
            versions. . Defaults to None.
        snapshot_retention_limit(int, Optional): The number of days for which ElastiCache retains automatic snapshots before deleting them. For
            example, if you set SnapshotRetentionLimit to 5, a snapshot that was taken today is retained for
            5 days before being deleted. Default: 0 (i.e., automatic backups are disabled for this cluster). Defaults to None.
        snapshot_window(str, Optional): The daily time range (in UTC) during which ElastiCache begins taking a daily snapshot of your
            node group (shard). Example: 05:00-09:00  If you do not specify this parameter, ElastiCache
            automatically chooses an appropriate time range. Defaults to None.
        cache_node_type(str, Optional): The compute and memory capacity of the nodes in the node group (shard). The following node types
            are supported by ElastiCache. Generally speaking, the current generation types provide more
            memory and computational power at lower cost when compared to their equivalent previous
            generation counterparts.
        auto_token_update_strategy(str, Optional): Specifies the strategy to use to update the AUTH token. This parameter must be specified with
                the auth-token parameter. Possible values:
                Rotate
                Set
                For more information, see Authenticating Users with Redis AUTH
        user_group_ids_to_add(List[str], Optional): The ID of the user group you are associating with the replication group.
        user_group_ids_to_remove(List[str], Optional): The ID of the user group to disassociate from the replication group, meaning the users in
                the group no longer can access the replication group.
        remove_user_groups(bool, Optional): Removes the user group associated with this replication group.
        log_delivery_configurations(List[Dict], Optional): Specifies the destination, format and type of the logs. Defaults to None.
            * LogType (str, Optional): Refers to slow-log.
            * DestinationType (str, Optional): Specify either cloudwatch-logs or kinesis-firehose as the destination type.
            * DestinationDetails (str, Optional): Configuration details of either a CloudWatch Logs destination or Kinesis Data Firehose
            destination.
                * CloudWatchLogsDetails (Dict, Optional): The configuration details of the CloudWatch Logs destination.
                    * LogGroup (str, Optional): The name of the CloudWatch Logs log group.
                * KinesisFirehoseDetails (Dict, Optional): The configuration details of the Kinesis Data Firehose destination.
                    * DeliveryStream (str, Optional): The name of the Kinesis Data Firehose delivery stream.
            * LogFormat (str, Optional): Specifies either JSON or TEXT
            * Enabled (bool, Optional): Specify if log delivery is enabled. Default true.

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": Dict}

    """
    result = dict(comment=[], result=True, ret=None)
    params_to_modify = {}
    modify_params = OrderedDict(
        {
            "ReplicationGroupDescription": "replication_group_description",
            "PrimaryClusterId": "primary_cluster_id",
            "SnapshottingClusterId": "snapshotting_cluster_id",
            "AutomaticFailoverEnabled": "automatic_failover_enabled",
            "MultiAZEnabled": "multi_az_enabled",
            "NodeGroupId": "node_group_id",
            "CacheSecurityGroupNames": "cache_security_group_names",
            "SecurityGroupIds": "security_group_ids",
            "PreferredMaintenanceWindow": "preferred_maintenance_window",
            "NotificationTopicArn": "notification_topic_arn",
            "CacheParameterGroupName": "cache_parameter_group_name",
            "NotificationTopicStatus": "notification_topic_status",
            "EngineVersion": "engine_version",
            "AutoMinorVersionUpgrade": "auto_minor_version_upgrade",
            "SnapshotRetentionLimit": "snapshot_retention_limit",
            "SnapshotWindow": "snapshot_window",
            "CacheNodeType": "cache_node_type",
            "AuthTokenUpdateStrategy": "auto_token_update_strategy",
            "UserGroupIdsToAdd": "user_group_ids_to_add",
            "UserGroupIdsToRemove": "user_group_ids_to_remove",
            "RemoveUserGroups": "remove_user_groups",
            "LogDeliveryConfigurations": "log_delivery_configurations",
        }
    )
    for parameter_raw, parameter_present in modify_params.items():
        # Add to modify list only if parameter is changed
        input_parameter_value = locals()[parameter_present]
        if (
            input_parameter_value is not None
            and old_state.get(parameter_present) != input_parameter_value
        ):
            params_to_modify[parameter_raw] = input_parameter_value
    if params_to_modify:
        if ctx.get("test", False):
            result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.elasticache.replication_group", name=name
            )
            for key, value in params_to_modify.items():
                plan_state[modify_params.get(key)] = value
        else:
            # apply_immediately is only used in update to decide whether to apply the update immediate or not
            # this property is not returned in describe, so this should not be compared with old_state as this
            # property will not be present in old_state.
            if apply_immediately is not None:
                params_to_modify["ApplyImmediately"] = apply_immediately
            modify_ret = (
                await hub.exec.boto3.client.elasticache.modify_replication_group(
                    ctx, ReplicationGroupId=resource_id, **params_to_modify
                )
            )
            result["result"] = result["result"] and modify_ret["result"]
            result["comment"] += hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.elasticache.replication_group", name=name
            )
            if not modify_ret["result"]:
                result["comment"] += modify_ret["comment"]
                result["result"] = False
                return result
    return result


async def replication_group_waiter(
    hub, ctx, name: str, resource_id: str, timeout: Dict, operation_type: str
):
    """

    Waiter to wait for the replication group to become active.

        Args:
           name(str): An Idem name of the resource. It is used as ReplicationGroupID during resource creation
           resource_id(str): Replication group id to Identify the resource
           timeout(Dict, Optional): Timeout configuration for creating or updating replication group.
            * create (Dict) -- Timeout configuration for creating replication group
                * delay(int, default=60) -- The amount of time in seconds to wait between attempts.
                * max_attempts(int, default=40) -- Customized timeout configuration containing delay and max attempts.
            * update (str) -- Timeout configuration for updating replication group
                * delay(int, default=60) -- The amount of time in seconds to wait between attempts.
                * max_attempts(int, default=40) -- Customized timeout configuration containing delay and max attempts.
           operation_type(str): create or update operation

        Returns:
            Dict[str, Any]
    """

    result = dict(comment=[], result=True, ret={})
    waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
        default_delay=15,
        default_max_attempts=40,
        timeout_config=timeout.get(operation_type) if timeout else None,
    )
    hub.log.debug(
        f"Waiting on {operation_type} aws.elasticache.replication_group '{name}'"
    )
    try:
        await hub.tool.boto3.client.wait(
            ctx,
            "elasticache",
            "replication_group_available",
            ReplicationGroupId=resource_id,
            WaiterConfig=waiter_config,
        )
    except Exception as e:
        result["comment"] += list(str(e))
        result["result"] = False
    return result
