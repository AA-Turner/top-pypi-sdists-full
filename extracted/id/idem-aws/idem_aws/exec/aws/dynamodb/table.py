import copy
from typing import Any
from typing import Dict


"""
Exec functions for AWS DynamoDB Table resources.
"""


async def get(hub, ctx, name, resource_id) -> Dict[str, Any]:
    """Get a DynamoDB Table resource from AWS.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str):
            The name of the Dynamodb table.

    Returns:
        Dict[str, Any]
    """
    result = dict(comment=[], ret=None, result=True)

    describe_ret = await hub.exec.boto3.client.dynamodb.describe_table(
        ctx, TableName=resource_id
    )
    if not describe_ret["result"]:
        if "ResourceNotFoundException" in str(describe_ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.dynamodb.table", name=name
                )
            )
            result["comment"] += list(describe_ret["comment"])
            return result
        result["result"] = False
        result["comment"] = describe_ret["comment"]
        return result

    table_resource = describe_ret.get("ret").get("Table")

    tags_ret = await hub.exec.boto3.client.dynamodb.list_tags_of_resource(
        ctx, ResourceArn=table_resource.get("TableArn")
    )
    if not tags_ret["result"]:
        result["result"] = False
        result["comment"] = tags_ret["comment"]
        return result
    table_resource.update(copy.deepcopy(tags_ret["ret"]))

    continuous_backups_ret = (
        await hub.exec.boto3.client.dynamodb.describe_continuous_backups(
            ctx, TableName=table_resource.get("TableName")
        )
    )
    if not continuous_backups_ret.get("result"):
        result["result"] = False
        result["comment"] = continuous_backups_ret["comment"]
        return result
    table_resource.update(copy.deepcopy(continuous_backups_ret.get("ret")))

    time_to_live_ret = await hub.exec.boto3.client.dynamodb.describe_time_to_live(
        ctx, TableName=table_resource.get("TableName")
    )
    if not time_to_live_ret.get("result"):
        result["result"] = False
        result["comment"] = time_to_live_ret["comment"]
        return result
    table_resource.update(copy.deepcopy(time_to_live_ret.get("ret")))

    result["ret"] = hub.tool.aws.dynamodb.table.convert_raw_table_to_present(
        ctx, raw_resource=table_resource, idem_resource_name=name
    )

    return result
