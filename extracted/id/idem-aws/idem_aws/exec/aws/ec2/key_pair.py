from typing import Dict
from typing import List


async def get(
    hub,
    ctx,
    name,
    resource_id: str = None,
    filters: List[Dict[str, str]] = None,
) -> Dict:
    """Get a key_pair resource from AWS.

    Supply one of the inputs as the filter to find a key pair. If more than one resource is found, the first resource
    returned from AWS will be used. The function returns None when no resource is found.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str, Optional):
            AWS key pair id to identify the resource.

        filters(list[dict[str, str]], Optional):
            One or more filters. For example: {"Name": "key-pair-id", "Values": [resource_id]}, A complete list of filters
            can be found at https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_key_pairs
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.tool.aws.ec2.key_pair.search_raw(
        ctx=ctx,
        name=name,
        resource_id=resource_id,
        filters=filters,
    )
    if not ret["result"]:
        if "InvalidKeyPair.NotFound" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.key_pair", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["KeyPairs"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.key_pair", name=name
            )
        )
        return result

    if len(ret["ret"]["KeyPairs"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_type="aws.ec2.key_pair", name=name
            )
        )
    resource = ret["ret"]["KeyPairs"][0]
    result["ret"] = hub.tool.aws.ec2.conversion_utils.convert_raw_key_pair_to_present(
        raw_resource=resource
    )
    return result
