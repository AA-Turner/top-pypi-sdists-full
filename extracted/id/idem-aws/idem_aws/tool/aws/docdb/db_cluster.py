import copy
from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List


def convert_raw_db_cluster_to_present(
    hub,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
    tags: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    Convert AWS returned data structure to correct idem docdb db_cluster present state

    Args:
        hub: required for functions in hub
        raw_resource: The aws response to convert
        idem_resource_name (Text, Optional): The idem name of the resource
        tags (List, Optional): The tags of the resource. Defaults to None.

    Returns: Valid idem state for docdb db_cluster of type Dict['string', Any]
    """
    resource_id = raw_resource.get("DBClusterIdentifier")
    raw_resource["Tags"] = dict(tags)
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    # below contains everything except VpcSecurityGroups as that needs to be handled as a list
    resource_parameters = OrderedDict(
        {
            "DBClusterIdentifier": "db_cluster_identifier",
            "Engine": "engine",
            "AvailabilityZones": "availability_zones",
            "BackupRetentionPeriod": "backup_retention_period",
            "CopyTagsToSnapshot": "copy_tags_to_snapshot",
            "DatabaseName": "database_name",
            "DBClusterParameterGroup": "db_cluster_parameter_group_name",  # DBClusterParameterGroupName is provided during input and mapped to DBClusterParameterGroup in output
            "DBSubnetGroup": "db_subnet_group_name",  # DBSubnetGroupName during input is mapped to DBSubnetGroup in output
            "EngineVersion": "engine_version",
            "Port": "port",
            "PreferredBackupWindow": "preferred_backup_window",
            "PreferredMaintenanceWindow": "preferred_maintenance_window",
            "ReplicationSourceIdentifier": "replication_source_identifier",
            "Tags": "tags",
            "StorageEncrypted": "storage_encrypted",
            "KmsKeyId": "kms_key_id",
            "EnableIAMDatabaseAuthentication": "enable_iam_database_authentication",
            "EnableCloudwatchLogsExports": "enable_cloudwatch_logs_exports",
            "DeletionProtection": "deletion_protection",
            "SourceRegion": "source_region",
            "DBClusterArn": "db_cluster_arn",
        }
    )
    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw) is not None:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    # also process the VpcSecurityGroups which is a list of object to map it as list of vpc security group id strings
    if raw_resource.get("VpcSecurityGroups") is not None:
        resource_translated["vpc_security_group_ids"] = [
            vpcsecgroup["VpcSecurityGroupId"]
            for vpcsecgroup in raw_resource.get("VpcSecurityGroups")
        ]
    return resource_translated


async def get_present_db_cluster(
    hub, ctx, name: str, resource_id: str, is_created: bool, desired_state: Dict = None
) -> Dict[str, Any]:
    """
    Get the idem present state representation of db cluster using the resource_id.

    Args:
        hub: required for functions in hub
        ctx: pop context
        name: idem name of resource,
        resource_id: db_cluster_identifier of the resource

    Returns: Valid idem state representing a docdb db cluster for the given resource id along with tags
    """
    result = dict(comment=[], result=True, present_db_cluster=None, resource_arn=None)

    # we should only return desired state like this during a --test: TRUE create scenario. Otherwise, always call boto3
    if ctx.get("test", False) and is_created:
        result["present_db_cluster"] = desired_state
        return result
    raw_db_cluster_result = await hub.exec.boto3.client.docdb.describe_db_clusters(
        ctx, DBClusterIdentifier=resource_id
    )
    # if we don't find db_cluster with provided resource id, fail the request
    if not (
        raw_db_cluster_result["result"]
        and raw_db_cluster_result["ret"]
        and raw_db_cluster_result["ret"].get("DBClusters")
    ):
        result["result"] = False
        result["comment"] = raw_db_cluster_result["comment"]
        return result
    resource_arn = raw_db_cluster_result["ret"].get("DBClusters")[0].get("DBClusterArn")
    result["resource_arn"] = resource_arn
    tags = await hub.tool.aws.docdb.tag.get_tags_for_resource(
        ctx, resource_arn=resource_arn
    )
    # if failure while fetching tags, fail the request
    if not tags["result"]:
        result["result"] = False
        result["comment"] = tags["comment"]
        return result
    tags = tags["ret"]
    result[
        "present_db_cluster"
    ] = hub.tool.aws.docdb.db_cluster.convert_raw_db_cluster_to_present(
        raw_resource=raw_db_cluster_result["ret"]["DBClusters"][0],
        idem_resource_name=name,
        tags=tags,
    )
    return result


async def update_db_cluster(
    hub,
    ctx,
    name: str,
    resource_id: str,
    desired_state: Dict,
    is_created: bool,
    update_waiter_acceptors: List,
    timeout: Dict,
) -> Dict[str, Any]:
    """
    Updates the docdb db cluster represented by the provided resource_id to the desired state.
    If is_created flag is set to True, the comment in result is not updated as it is assumed that
    the resource is being updated right after it was created to apply remaining parameters.
    """
    # below is the mapping of boto3 parameters applicable for modification of docdb db_cluster in idem (tags are handled separately)
    modify_params = OrderedDict(
        {
            "ApplyImmediately": "apply_immediately",
            "BackupRetentionPeriod": "backup_retention_period",
            "DBClusterParameterGroupName": "db_cluster_parameter_group_name",
            "VpcSecurityGroupIds": "vpc_security_group_ids",
            "Port": "port",
            "PreferredBackupWindow": "preferred_backup_window",
            "PreferredMaintenanceWindow": "preferred_maintenance_window",
            "CloudwatchLogsExportConfiguration": "cloudwatch_logs_export_configuration",
            "EngineVersion": "engine_version",
            "DeletionProtection": "deletion_protection",
            "CopyTagsToSnapshot": "copy_tags_to_snapshot",
        }
    )
    result = dict(comment=[], old_state=None, new_state=None, result=True)
    if ctx.get("test", False) and is_created:
        current_state = desired_state
    else:
        current_db_cluster_result = await hub.exec.aws.docdb.db_cluster.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not (
            current_db_cluster_result
            and current_db_cluster_result["result"]
            and current_db_cluster_result["ret"]
        ):
            result["result"] = False
            result["comment"].append(current_db_cluster_result["comment"])
            return result
        current_state = current_db_cluster_result["ret"]

    if not is_created:
        result["old_state"] = current_state
    params_to_modify = {}
    plan_state = copy.deepcopy(current_state)
    resource_arn = current_state.get("db_cluster_arn")

    # create a dict 'params_to_modify' of (non tag) raw parameter key mapped to desired value,
    # where the desired value is not none and current value does not match desired value
    hub.log.debug(f"current state before update {current_state}")
    for param_raw, param_present in modify_params.items():
        if desired_state.get(param_present) is not None and current_state.get(
            param_present
        ) != desired_state.get(param_present):
            params_to_modify[param_raw] = desired_state[param_present]

    # This is the only key that is excluded since there is no way to get a "before" version of this key
    # boto3 does not return the master_user_password so this is done seperately depending on if the value is
    # given by the user
    if desired_state["master_user_password"] is not None:
        params_to_modify["MasterUserPassword"] = desired_state["master_user_password"]

    # if we have some parameters to modify, apply it
    hub.log.debug(f"params to modify {params_to_modify}")
    if params_to_modify:
        if ctx.get("test", False):
            for key, value in params_to_modify.items():
                plan_state[modify_params.get(key)] = value
            if not is_created:
                result["comment"].append(
                    hub.tool.aws.comment_utils.would_update_comment(
                        resource_type="aws.docdb.db_cluster", name=name
                    )[0]
                )
        else:
            modify_db_cluster_result = (
                await hub.exec.boto3.client.docdb.modify_db_cluster(
                    ctx, DBClusterIdentifier=resource_id, **params_to_modify
                )
            )
            if not modify_db_cluster_result["result"]:
                result["comment"].append(modify_db_cluster_result["comment"])
                result["result"] = False
                return result
            # wait for update of cluster
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
                client=await hub.tool.boto3.client.get_client(ctx, "docdb"),
            )
            try:
                await hub.tool.boto3.client.wait(
                    ctx,
                    "docdb",
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
            if not is_created:
                result["comment"].append(
                    hub.tool.aws.comment_utils.update_comment(
                        resource_type="aws.docdb.db_cluster", name=name
                    )
                )

    # modify tags if it has changed
    old_tags = current_state["tags"]
    new_tags = desired_state["tags"]
    if new_tags is not None and new_tags != old_tags:
        # below code updates tags on AWS only if it is not a test run
        update_tags_ret = await hub.tool.aws.docdb.tag.update_tags(
            ctx=ctx,
            resource_arn=resource_arn,
            old_tags=old_tags,
            new_tags=new_tags,
        )
        if not update_tags_ret["result"]:
            result["comment"].append(update_tags_ret["comment"][0])
            result["result"] = False
            hub.log.debug(f"Failed updating tags for aws.docdb.db_cluster '{name}'")
            return result
        # update comment if tags were updated
        result["comment"].append(update_tags_ret["comment"][0])
        if ctx.get("test", False) and update_tags_ret["ret"] is not None:
            plan_state["tags"] = update_tags_ret["ret"]
            if not is_created:
                result["comment"].append(
                    hub.tool.aws.comment_utils.would_update_comment(
                        resource_type="aws.docdb.db_cluster", name=resource_id
                    )
                )

    # set new_state
    if ctx.get("test", False):
        result["new_state"] = plan_state
    else:
        current_db_cluster_result = (
            await hub.tool.aws.docdb.db_cluster.get_present_db_cluster(
                ctx=ctx, name=name, resource_id=resource_id, is_created=is_created
            )
        )
        if not (
            current_db_cluster_result
            and current_db_cluster_result["result"]
            and current_db_cluster_result["present_db_cluster"]
            and current_db_cluster_result["resource_arn"]
        ):
            result["result"] = False
            result["comment"].append(current_db_cluster_result["comment"])
            return result
        result["new_state"] = current_db_cluster_result["present_db_cluster"]

    return result
