import copy
from collections import OrderedDict
from typing import Any
from typing import Dict

"""
Util functions for AWS DynamoDB Table resources.
"""


def convert_raw_table_to_present(
    hub,
    ctx,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    """
    Util functions to convert raw Dynamo DB resource state from AWS to present input format.

    Args:
        hub: required for functions in hub.
        ctx: context.
        raw_resource(Dict[str, Any]): The AWS response to convert.
        idem_resource_name(str): The name of the Idem state.

    Returns:
        Dict[str, Any]: Common idem present state
    """
    describe_parameters = OrderedDict(
        {
            "AttributeDefinitions": "attribute_definitions",
            "KeySchema": "key_schema",
            "TableArn": "table_arn",
            "TableStatus": "table_status",
        }
    )
    new_table_resource = {"resource_id": idem_resource_name, "name": idem_resource_name}
    for parameter_old_key, parameter_new_key in describe_parameters.items():
        if raw_resource.get(parameter_old_key) is not None:
            new_table_resource[parameter_new_key] = raw_resource.get(parameter_old_key)

    if raw_resource.get("BillingModeSummary"):
        new_table_resource["billing_mode"] = raw_resource.get("BillingModeSummary").get(
            "BillingMode"
        )
    else:
        new_table_resource["billing_mode"] = "PROVISIONED"

    if raw_resource.get("GlobalSecondaryIndexes"):
        global_secondary_indexes = []
        for global_index in raw_resource.get("GlobalSecondaryIndexes"):
            new_global_index = {
                "IndexName": global_index["IndexName"],
                "KeySchema": global_index["KeySchema"],
                "Projection": global_index["Projection"],
            }
            if global_index.get("ProvisionedThroughput"):
                provisioned_throughput = global_index.get("ProvisionedThroughput")
                new_provisioned = {
                    "ReadCapacityUnits": provisioned_throughput["ReadCapacityUnits"],
                    "WriteCapacityUnits": provisioned_throughput["WriteCapacityUnits"],
                }
                new_global_index["ProvisionedThroughput"] = new_provisioned
            global_secondary_indexes.append(new_global_index)
        new_table_resource["global_secondary_indexes"] = global_secondary_indexes

    if raw_resource.get("LocalSecondaryIndexes"):
        local_secondary_indexes = []
        for local_index in raw_resource.get("LocalSecondaryIndexes"):
            new_local_index = {
                "IndexName": local_index["IndexName"],
                "KeySchema": local_index["KeySchema"],
                "Projection": local_index["Projection"],
            }
            local_secondary_indexes.append(new_local_index)
        new_table_resource["local_secondary_indexes"] = local_secondary_indexes

    continuous_backups_description = raw_resource.get("ContinuousBackupsDescription")
    if continuous_backups_description:
        point_in_time_recovery_description = continuous_backups_description.get(
            "PointInTimeRecoveryDescription"
        )
        if point_in_time_recovery_description:
            if (
                point_in_time_recovery_description.get(
                    "PointInTimeRecoveryStatus", "DISABLED"
                )
                == "ENABLED"
            ):
                point_in_time_recovery = {"Enabled": True}
            else:
                point_in_time_recovery = {"Enabled": False}
            new_table_resource["point_in_time_recovery"] = point_in_time_recovery

    if raw_resource.get("ProvisionedThroughput"):
        provisioned_throughput = raw_resource.get("ProvisionedThroughput")
        new_provisioned = {
            "ReadCapacityUnits": provisioned_throughput["ReadCapacityUnits"],
            "WriteCapacityUnits": provisioned_throughput["WriteCapacityUnits"],
        }
        new_table_resource["provisioned_throughput"] = new_provisioned

    if raw_resource.get("Replicas"):
        new_table_resource["replica_updates"] = raw_resource.get("Replicas")

    if raw_resource.get("SSEDescription"):
        sse_specification = raw_resource.get("SSEDescription")
        new_sse_specification = {}
        kms_master_key_arn = sse_specification.get("KMSMasterKeyArn")
        if kms_master_key_arn:
            new_sse_specification["KMSMasterKeyId"] = kms_master_key_arn
        sse_type = sse_specification.get("SSEType")
        if sse_type:
            new_sse_specification["SSEType"] = sse_type
        if (
            sse_specification.get("Status") == "ENABLED"
            or sse_specification.get("Status") == "ENABLING"
        ):
            new_sse_specification["Enabled"] = True
        else:
            new_sse_specification["Enabled"] = False
        new_table_resource["sse_specification"] = new_sse_specification
    else:
        new_table_resource["sse_specification"] = {
            "Enabled": False,
        }

    if raw_resource.get("StreamSpecification"):
        new_table_resource["stream_specification"] = raw_resource.get(
            "StreamSpecification"
        )

    if raw_resource.get("TableClassSummary"):
        new_table_resource["table_class"] = raw_resource.get("TableClassSummary").get(
            "TableClass"
        )

    tags = raw_resource.get("Tags")
    if tags:
        new_table_resource["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            tags
        )

    time_to_live_description = raw_resource.get("TimeToLiveDescription")
    if time_to_live_description:
        if time_to_live_description.get("TimeToLiveStatus", "DISABLED") == "ENABLED":
            time_to_live = {
                "Enabled": True,
                "AttributeName": time_to_live_description.get("AttributeName"),
            }
        else:
            time_to_live = {"Enabled": False}
        new_table_resource["time_to_live"] = time_to_live

    return new_table_resource


async def update(
    hub,
    ctx,
    name: str,
    resource_id: str,
    old_state: Dict[str, Any],
    desired_state: Dict[str, Any],
    timeout: Dict = None,
) -> Dict[str, Any]:
    """
    Updates a DynamoDB Table resource.

    Args:
        hub: required for functions in hub.
        ctx: context.
        name(str): The name of the Idem state.
        resource_id(str): The name of the Dynamodb table.
        old_state(dict): The old state for the specified table.
        desired_state(dict): The desired state for the specified table.
        timeout(Dict, Optional): Timeout configuration for updates.

    Returns:
        Dict[str, Any]
    """
    result = dict(comment=[], result=True, ret=None)
    updated_attributes = {}

    table_parameters = OrderedDict(
        {
            "billing_mode": "BillingMode",
            "global_secondary_indexes": "GlobalSecondaryIndexUpdates",
            "provisioned_throughput": "ProvisionedThroughput",
            "replica_updates": "ReplicaUpdates",
            "stream_specification": "StreamSpecification",
            "table_class": "TableClass",
        }
    )
    table_parameters_to_update = {}

    attribute_definitions = desired_state.get("attribute_definitions")
    if attribute_definitions is not None:
        if not hub.tool.aws.state_comparison_utils.are_lists_identical(
            old_state.get("attribute_definitions"),
            attribute_definitions,
        ):
            table_parameters_to_update["AttributeDefinitions"] = attribute_definitions

    global_secondary_indexes = desired_state.get("global_secondary_indexes")
    if global_secondary_indexes is not None:
        if not hub.tool.aws.state_comparison_utils.are_lists_identical(
            old_state.get("global_secondary_indexes"),
            global_secondary_indexes,
        ):
            table_parameters_to_update[
                "GlobalSecondaryIndexUpdates"
            ] = global_secondary_indexes

    new_sse_specification = desired_state.get("sse_specification")
    old_sse_specification = old_state.get("sse_specification")
    if new_sse_specification != old_sse_specification:
        if new_sse_specification.get("Enabled") != old_sse_specification.get(
            "Enabled"
        ) or (
            new_sse_specification.get("KMSMasterKeyId")
            and new_sse_specification.get("KMSMasterKeyId")
            != old_sse_specification.get("KMSMasterKeyId")
        ):
            table_parameters_to_update["SSESpecification"] = new_sse_specification
            updated_attributes["sse_specification"] = new_sse_specification

    replica_updates = desired_state.get("replica_updates")
    if replica_updates is not None:
        if not hub.tool.aws.state_comparison_utils.are_lists_identical(
            old_state.get("replica_updates"),
            replica_updates,
        ):
            table_parameters_to_update["ReplicaUpdates"] = replica_updates

    for key, value in desired_state.items():
        if key in table_parameters.keys():
            if value is not None and value != old_state.get(key):
                table_parameters_to_update[table_parameters[key]] = value

    if table_parameters_to_update:
        for parameter_present, parameter_raw in table_parameters.items():
            if parameter_raw in table_parameters_to_update:
                updated_attributes[parameter_present] = table_parameters_to_update[
                    parameter_raw
                ]

        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.dynamodb.update_table(
                ctx=ctx,
                TableName=resource_id,
                **table_parameters_to_update,
            )
            if not update_ret["result"]:
                result["result"] = False
                result["comment"] = update_ret["comment"]
                return result

            hub.log.debug(f"Waiting on updating aws.dynamodb.table '{name}'")
            waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                default_delay=15,
                default_max_attempts=40,
                timeout_config=timeout.get("update") if timeout else None,
            )
            try:
                await hub.tool.boto3.client.wait(
                    ctx,
                    "dynamodb",
                    "table_exists",
                    TableName=resource_id,
                    WaiterConfig=waiter_config,
                )
            except Exception as e:
                result["result"] = False
                result["comment"] += [str(e)]

    if desired_state.get("point_in_time_recovery"):
        update_ret = await hub.tool.aws.dynamodb.table.update_point_in_time_recovery(
            ctx,
            name=name,
            resource_id=resource_id,
            old_point_in_time_recovery=old_state.get("point_in_time_recovery"),
            new_point_in_time_recovery=desired_state.get("point_in_time_recovery"),
        )
        if not update_ret["result"]:
            result["result"] = False
            result["comment"] += update_ret["comment"]
            return result

        if update_ret["ret"]:
            updated_attributes["point_in_time_recovery"] = copy.deepcopy(
                update_ret["ret"]
            )

    if desired_state.get("time_to_live"):
        update_ret = await hub.tool.aws.dynamodb.table.update_time_to_live(
            ctx,
            name=name,
            resource_id=resource_id,
            old_time_to_live=old_state.get("time_to_live"),
            new_time_to_live=desired_state.get("time_to_live"),
        )
        if not update_ret["result"]:
            result["result"] = False
            result["comment"] += update_ret["comment"]
            return result

        if update_ret["ret"]:
            updated_attributes["time_to_live"] = copy.deepcopy(update_ret["ret"])

    if updated_attributes:
        result["ret"] = copy.deepcopy(updated_attributes)
        if ctx.get("test", False):
            result["comment"] = result[
                "comment"
            ] + hub.tool.aws.comment_utils.would_update_comment(
                "aws.dynamodb.table", name
            )
        else:
            result["comment"] = result[
                "comment"
            ] + hub.tool.aws.comment_utils.update_comment("aws.dynamodb.table", name)

    return result


async def update_point_in_time_recovery(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    old_point_in_time_recovery: Dict = None,
    new_point_in_time_recovery: Dict = None,
) -> Dict[str, Any]:
    """
    Updates the point in time recovery settings for a DynamoDB Table resource.

    Args:
        hub: required for functions in hub.
        ctx: context.
        name(str): The name of the Idem state.
        resource_id(str, Optional): The name of the Dynamodb table.
        old_point_in_time_recovery(dict, Optional): The old point in time recovery settings for the specified table.
        new_point_in_time_recovery(dict, Optional): The new point in time recovery settings for the specified table.

    Returns:
        Dict[str, Any]
    """
    result = dict(comment=[], result=True, ret=None)

    if (
        new_point_in_time_recovery
        and new_point_in_time_recovery != old_point_in_time_recovery
    ):
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.dynamodb.update_continuous_backups(
                ctx,
                TableName=resource_id,
                PointInTimeRecoverySpecification={
                    "PointInTimeRecoveryEnabled": new_point_in_time_recovery.get(
                        "Enabled", False
                    ),
                },
            )
            if not update_ret["result"]:
                result["result"] = False
                result["comment"] = update_ret["comment"]
                return result
        result["ret"] = new_point_in_time_recovery

    return result


async def update_time_to_live(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    old_time_to_live: Dict = None,
    new_time_to_live: Dict = None,
) -> Dict[str, Any]:
    """
    Updates the time to live (TTL) settings for a DynamoDB Table resource.

    Args:
        hub: required for functions in hub.
        ctx: context.
        name(str): The name of the Idem state.
        resource_id(str, Optional): The name of the Dynamodb table.
        old_time_to_live(dict, Optional): The old time to live (TTL) settings for the specified table.
        new_time_to_live(dict, Optional): The new time to live (TTL) settings for the specified table.

    Returns:
        Dict[str, Any]
    """
    result = dict(comment=[], result=True, ret=None)

    if new_time_to_live and (
        (not old_time_to_live and new_time_to_live.get("Enabled", False))
        or (old_time_to_live and new_time_to_live != old_time_to_live)
    ):
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.dynamodb.update_time_to_live(
                ctx,
                TableName=resource_id,
                TimeToLiveSpecification=new_time_to_live,
            )
            if not update_ret["result"]:
                result["result"] = False
                result["comment"] = update_ret["comment"]
                return result
        result["ret"] = new_time_to_live

    return result
