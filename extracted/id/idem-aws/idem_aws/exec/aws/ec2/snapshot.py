"""Exec module for managing EC2 Snapshots"""
from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str = None,
    resource_id: str = None,
    filters: List = None,
    tags: Dict[str, str] = None,
) -> Dict:
    """
    Get a single snapshot from AWS. If more than one resource is found, the first resource returned from AWS
    will be used. The function returns None when no resource is found.

    Args:
        name (str):
            The name of the Idem state.

        resource_id (str, Optional):
            Snapshot ID of the snapshot.

        filters (list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_snapshots

        tags (dict, Optional):
            The dict of tags to filter by in the format ``{tag-key: tag-value}`` . For example, to find all resources
            that have a tag with the key "Owner" and the value "TeamA" , specify ``{Owner: TeamA}``

            * Key (str):
                The key name for the tag to be used to filter by.

            * Value(str):
                The value associated with this tag to filter by.
    """
    result = dict(comment=[], ret=None, result=True)

    tags = hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)

    ret = await hub.tool.aws.ec2.snapshot.search_raw(
        ctx=ctx, resource_id=resource_id, filters=filters, tags=tags
    )
    if not ret["result"]:
        if "InvalidSnapshot.NotFound" in str(
            ret["comment"]
        ) or "InvalidSnapshotID.Malformed" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.snapshot", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["Snapshots"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.snapshot", name=name
            )
        )
        return result

    resource = ret["ret"]["Snapshots"][0]
    if len(ret["ret"]["Snapshots"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_type="aws.ec2.snapshot", resource_id=resource_id
            )
        )
    result[
        "ret"
    ] = await hub.tool.aws.ec2.conversion_utils.convert_raw_snapshot_to_present_async(
        ctx=ctx, raw_resource=resource, idem_resource_name=name
    )

    return result


async def list_(
    hub,
    ctx,
    name: str = None,
    filters: List = None,
    tags: Dict[str, str] = None,
) -> Dict:
    """
    Fetch a list of snapshots from AWS. The function returns empty list when no resource is found.

    Args:
        name (str, Optional):
            The name of the Idem state.

        filters (list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_snapshots

        tags (dict, Optional):
            The dict of tags to filter by in the format ``{tag-key: tag-value}`` . For example, to find all resources
            that have a tag with the key "Owner" and the value "TeamA" , specify ``{Owner: TeamA}``

            * Key (str):
                The key name for the tag to be used to filter by.

            * Value(str):
                The value associated with this tag to filter by.
    """
    result = dict(comment=[], ret=[], result=True)

    tags = hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)

    ret = await hub.tool.aws.ec2.snapshot.search_raw(
        ctx=ctx,
        filters=filters,
        tags=tags,
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["Snapshots"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.snapshot", name=name
            )
        )
        return result
    for snapshot in ret["ret"]["Snapshots"]:
        snapshot_id = snapshot.get("SnapshotId")
        result["ret"].append(
            await hub.tool.aws.ec2.conversion_utils.convert_raw_snapshot_to_present_async(
                ctx, raw_resource=snapshot, idem_resource_name=snapshot_id
            )
        )
    return result
