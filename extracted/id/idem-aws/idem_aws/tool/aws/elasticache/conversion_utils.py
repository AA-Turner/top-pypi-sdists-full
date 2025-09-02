from collections import OrderedDict
from typing import Any
from typing import Dict

"""
Util functions to convert raw resource state from AWS Elasticache to present input format.
"""


async def convert_raw_elasticache_subnet_to_present_async(
    hub,
    ctx,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    """
    Return converted raw resource state from AWS Elasticache subnet group to required input format for present.

     Args:
        raw_resource(Dict[str, str]): resource obtained from describe API
        idem_resource_name(str): name of idem resource

    Return: Dict[str, Any]
    """
    result = dict(comment=[], result=True, ret=None)
    resource_id = raw_resource.get("CacheSubnetGroupName")
    resource_parameters = OrderedDict(
        {
            "CacheSubnetGroupDescription": "cache_subnet_group_description",
            "ARN": "arn",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    if raw_resource.get("Subnets"):
        subnet_ids_list = []
        for subnet in raw_resource.get("Subnets"):
            if "SubnetIdentifier" in subnet:
                subnet_ids_list.append(subnet.get("SubnetIdentifier"))
        resource_translated["subnet_ids"] = subnet_ids_list

    if raw_resource.get("ARN"):
        tags = await hub.exec.boto3.client.elasticache.list_tags_for_resource(
            ctx, ResourceName=raw_resource.get("ARN")
        )
        result["result"] = tags["result"]
        if tags["result"] and tags.get("ret"):
            resource_translated[
                "tags"
            ] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags["ret"]["TagList"])
        if not result["result"]:
            result["comment"] += tags["comment"]
    result["ret"] = resource_translated
    return result


async def convert_raw_elasticache_parameter_group_to_present_async(
    hub,
    ctx,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    """
    Return converted raw resource state from AWS Elasticache parameter group to required input format for present.

     Args:
        raw_resource(Dict[str, str]): resource obtained from describe API
        idem_resource_name(str): name of idem resource

    Return: Dict[str, Any]
    """
    result = dict(comment=[], result=True, ret=None)
    resource_id = raw_resource.get("CacheParameterGroupName")
    resource_parameters = OrderedDict(
        {
            "CacheParameterGroupFamily": "cache_parameter_group_family",
            "Description": "description",
            "ARN": "arn",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    if raw_resource.get("ARN"):
        tags = await hub.exec.boto3.client.elasticache.list_tags_for_resource(
            ctx, ResourceName=raw_resource.get("ARN")
        )
        result["result"] = tags["result"]
        if tags["result"] and tags.get("ret"):
            resource_translated[
                "tags"
            ] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags["ret"]["TagList"])
        if not tags["result"]:
            result["comment"] += tags["comment"]

    ret_parameters = await hub.exec.boto3.client.elasticache.describe_cache_parameters(
        ctx, CacheParameterGroupName=resource_id
    )
    result["result"] = result["result"] and ret_parameters["result"]
    if not ret_parameters["result"]:
        result["comment"] += ret_parameters["comment"]
    elif ret_parameters["result"] and ret_parameters.get("ret"):
        updated_parameter_list = []
        for parameter in ret_parameters["ret"].get("Parameters"):
            parameter_list = {}
            if "ParameterName" in parameter:
                parameter_list["ParameterName"] = parameter.get("ParameterName")
            if "ParameterValue" in parameter:
                parameter_list["ParameterValue"] = parameter.get("ParameterValue")
            updated_parameter_list.append(parameter_list)
        resource_translated["parameter_name_values"] = updated_parameter_list

    result["ret"] = resource_translated
    return result


async def convert_raw_elasticache_replication_group_to_present_async(
    hub,
    ctx,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    """
    Return converted raw resource state from AWS Elasticache replication_group to required input format for present.

     Args:
        raw_resource(Dict[str, Any]): resource obtained from describe API
        idem_resource_name(str): name of idem resource

    Return: Dict[str, Any]
    """
    resource_id = raw_resource.get("ReplicationGroupId")
    resource_parameters = OrderedDict(
        {
            "ReplicationGroupId": "replication_group_id",
            "Description": "replication_group_description",
            "Status": "status",
            "PendingModifiedValues": "pending_modified_values",
            "MemberClusters": "member_clusters",
            "SnapshottingClusterId": "snapshotting_cluster_id",
            "ConfigurationEndpoint": "configuration_endpoint",
            "SnapshotRetentionLimit": "snapshot_retention_limit",
            "SnapshotWindow": "snapshot_window",
            "ClusterEnabled": "cluster_enabled",
            "CacheNodeType": "cache_node_type",
            "AuthTokenEnabled": "auth_token_enabled",
            "TransitEncryptionEnabled": "transit_encryption_enabled",
            "AtRestEncryptionEnabled": "at_rest_encryption_enabled",
            "MemberClustersOutpostArns": "member_clusters_outpost_arns",
            "KmsKeyId": "kms_key_id",
            "ARN": "arn",
            "UserGroupIds": "user_group_ids",
            "LogDeliveryConfigurations": "log_delivery_configurations",
            "DataTiering": "data_tiering",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    if raw_resource.get("NodeGroups"):
        for node in raw_resource.get("NodeGroups"):
            if not resource_translated.get("node_group_id") and "NodeGroupId" in node:
                resource_translated["node_group_id"] = node.get("NodeGroupId")
            if not resource_translated.get("port") and "PrimaryEndpoint" in node:
                resource_translated["port"] = (node.get("PrimaryEndpoint")).get("Port")

    resource_translated["automatic_failover_enabled"] = bool(
        raw_resource.get("AutomaticFailover") == "enabled"
    )
    resource_translated["multi_az_enabled"] = bool(
        raw_resource.get("MultiAZ") == "enabled"
    )
    resource_translated["data_tiering"] = bool(
        raw_resource.get("DataTiering") == "enabled"
    )
    if raw_resource.get("Tags") is not None:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )

    if raw_resource.get("MemberClusters"):
        cache_cluster_id = raw_resource.get("MemberClusters")[0]

        ret = await hub.exec.boto3.client.elasticache.describe_cache_clusters(
            ctx, CacheClusterId=cache_cluster_id
        )
        if not ret["result"]:
            hub.log.debug("Cannot describe cache clusters")

        if ret["ret"].get("CacheClusters"):
            cache_clusters_resource = ret["ret"].get("CacheClusters")[0]
            security_groups = cache_clusters_resource.get("SecurityGroups")
            security_group_ids = []
            if security_groups:
                for security_group in security_groups:
                    security_group_ids.append(security_group.get("SecurityGroupId"))
                resource_translated["security_group_ids"] = security_group_ids

            cluster_parameters = OrderedDict(
                {
                    "EngineVersion": "engine_version",
                    "PreferredMaintenanceWindow": "preferred_maintenance_window",
                    "CacheSubnetGroupName": "cache_subnet_group_name",
                }
            )
            for parameter_raw, parameter_present in cluster_parameters.items():
                if parameter_raw in cache_clusters_resource:
                    resource_translated[
                        parameter_present
                    ] = cache_clusters_resource.get(parameter_raw)
            if "CacheParameterGroup" in cache_clusters_resource:
                resource_translated[
                    "cache_parameter_group_name"
                ] = cache_clusters_resource["CacheParameterGroup"].get(
                    "CacheParameterGroupName"
                )

    return resource_translated
