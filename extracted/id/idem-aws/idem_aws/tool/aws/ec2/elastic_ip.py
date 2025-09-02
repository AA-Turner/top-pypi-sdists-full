from typing import Dict
from typing import List


async def search_raw(
    hub, ctx, resource_id: str = None, filters: List = None, tags: List = None
) -> Dict:
    """
    Fetch one or more Elastic IP addresses from AWS. The return will be in the same format as what the boto3 api returns.

    Args:
        resource_id(str, Optional): Public IP of the Elastic IP address.
        filters(List, Optional): One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
         https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_addresses
        tags(List, Optional): The list of tags to filter by. For example, to find all resources that have a tag with the key
            "Owner" and the value "TeamA" , specify "tag:Owner" for the Dict key and "TeamA" for the Dict value.

    Returns:
        {"result": True|False, "comment": A message List, "ret": Dict}

    """
    result = dict(comment=[], ret=None, result=True)
    syntax_validation = hub.tool.aws.search_utils.search_filter_syntax_validation(
        filters=filters
    )
    if not syntax_validation["result"]:
        result["comment"] = list(syntax_validation["comment"])
        return result
    boto3_filter = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
        filters=filters
    )
    if tags is not None:
        for tag in tags:
            boto3_filter.append({"Name": tag["Key"], "Values": [tag["Value"]]})

    ret = await hub.exec.boto3.client.ec2.describe_addresses(
        ctx, Filters=boto3_filter, PublicIps=[resource_id] if resource_id else None
    )
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]
    return result
