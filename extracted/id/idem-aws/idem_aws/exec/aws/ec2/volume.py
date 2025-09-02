"""Exec module for managing EC2 Volumes"""
from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    filters: List = None,
    tags: Dict[str, str] = None,
) -> Dict:
    """
    Get a single Volume from AWS. If more than one resource is found, the first resource returned from AWS
    will be used. The function returns None when no resource is found.

    Args:
        resource_id (str, Optional):
            Volume ID of the volume.

        filters (list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_volumes

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

    ret = await hub.tool.aws.ec2.volume.search_raw(
        ctx=ctx, resource_id=resource_id, filters=filters, tags=tags
    )
    if not ret["result"]:
        if "InvalidVolume.NotFound" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.volume", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["Volumes"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.volume", name=name
            )
        )
        return result

    resource = ret["ret"]["Volumes"][0]
    if len(ret["ret"]["Volumes"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_type="aws.ec2.volume", resource_id=resource_id
            )
        )
    result["ret"] = hub.tool.aws.ec2.conversion_utils.convert_raw_volume_to_present(
        raw_resource=resource, idem_resource_name=name
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
    Fetch a list of volumes from AWS. The function returns empty list when no resource is found.

    Args:
        name (str):
            The name of the Idem state.

        filters (list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_volumes

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

    ret = await hub.tool.aws.ec2.volume.search_raw(ctx=ctx, filters=filters, tags=tags)
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["Volumes"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.volume", name=name
            )
        )
        return result

    for volume in ret["ret"]["Volumes"]:
        result["ret"].append(
            hub.tool.aws.ec2.conversion_utils.convert_raw_volume_to_present(
                raw_resource=volume, idem_resource_name=name
            )
        )

    return result
