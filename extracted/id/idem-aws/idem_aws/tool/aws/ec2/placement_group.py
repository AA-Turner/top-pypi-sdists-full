from typing import Dict
from typing import List


async def search_raw(
    hub,
    ctx,
    filters: List = None,
    resource_id: str = None,
) -> Dict:
    """
    Fetch one or more placement groups from AWS. The return will be in the same format as what the boto3 api returns.

    Args:
        filters (list, Optional):
            One or more filters. For example: {"Name": "strategy", "Values": ["cluster"]},
            A complete list of filters can be found at https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_placement_groups

        resource_id (str, Optional):
            The GroupName of the placement group.

    Returns:
        {"result": True|False, "comment": A message List, "ret": Dict}

    """
    result = dict(comment=[], ret=None, result=True)
    syntax_validation = hub.tool.aws.search_utils.search_filter_syntax_validation(
        filters=filters
    )
    if not syntax_validation["result"]:
        result["result"] = False
        result["comment"] = list(syntax_validation["comment"])
        return result
    boto3_filter = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
        filters=filters
    )

    ret = await hub.exec.boto3.client.ec2.describe_placement_groups(
        ctx,
        Filters=boto3_filter,
        GroupNames=[resource_id] if resource_id else None,
    )

    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]
    return result
