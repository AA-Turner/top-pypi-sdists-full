from typing import Dict


async def get(hub, ctx, name: str, resource_id: str = None) -> Dict:
    """Pass required params to get a Kinesis stream resource. Retrieves the specified Kinesis Stream.

    Args:
        name(str):
          AWS Kinesis Stream name to uniquely identify the resource.

        resource_id(str, Optional):
            AWS Kinesis Stream name.

    Returns:
        Dict[bool, list, dict or None]:

        result(bool):
            Whether the result of the function has been successful (``True``) or not (``False``).
        comment(list):
            A list of messages.
        ret(dict or None):
           The Kinesis Stream in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.kinesis.stream.get name="idem_name" resource_id="resource_id"

        Calling this exec module function from within a state module in pure python:

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await hub.exec.aws.kinesis.stream.get(
                    ctx, name=name, resource_id=resource_id
                )
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.tool.aws.kinesis.stream.search_raw(
        ctx=ctx,
        name=resource_id if resource_id else name,
    )
    if not ret["result"]:
        if "ResourceNotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.kinesis.stream", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if "StreamDescriptionSummary" not in ret["ret"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.kinesis.stream", name=name
            )
        )
        return result

    resource_id = ret["ret"]["StreamDescriptionSummary"].get("StreamName")
    tags = {}
    tags_ret = await hub.exec.boto3.client.kinesis.list_tags_for_stream(
        ctx, StreamName=resource_id if resource_id else name
    )
    if not tags_ret["result"]:
        result["comment"] = list(tags_ret["comment"])
        result["result"] = False
        return result
    else:
        if tags_ret["ret"] and tags_ret.get("ret")["Tags"]:
            tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
                tags_ret.get("ret")["Tags"]
            )

    result["ret"] = hub.tool.aws.kinesis.conversion_utils.convert_raw_stream_to_present(
        raw_resource=ret["ret"]["StreamDescriptionSummary"],
        idem_resource_name=resource_id,
        tags=tags,
    )
    return result
