from typing import Dict
from typing import List


async def search_raw(
    hub,
    ctx,
    resource_id: str = None,
    filters: List = None,
    tags: List = None,
    executable_users: List = None,
    owners: List = None,
    include_deprecated: bool = False,
) -> Dict:
    """Search EC2 ami from AWS account.

    Fetch one or more ami's from AWS. The return will be in the same format as what the boto3 api returns.

    Args:
        resource_id(str, Optional):
            Resource ID of the ami.

        executable_users (list[str], Optional):
            Scopes the images by users with explicit launch permissions.
            Specify an Amazon Web Services account ID, self (the sender of the request), or all (public AMIs).

        owners (list[str], Optional):
            Scopes the results to images with the specified owners.
            You can specify a combination of Amazon Web Services account IDs, self , amazon , and aws-marketplace.
            If you omit this parameter, the results include all images for which you have launch permissions, regardless of ownership.

        include_deprecated (bool, Optional):
            If true , all deprecated AMIs are included in the response.
            If false , no deprecated AMIs are included in the response. If no value is specified, the default value is false .

        filters(List, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images

        tags(List, Optional):
            The list of tags to filter by. For example, to find all resources that have a tag with the key
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

    ami_args = {}
    if filters:
        ami_args["Filters"] = boto3_filter
    if resource_id:
        ami_args["ImageIds"] = [resource_id]
    if executable_users:
        ami_args["ExecutableUsers"] = executable_users
    if owners:
        ami_args["Owners"] = owners
    if include_deprecated:
        ami_args["IncludeDeprecated"] = include_deprecated

    ret = await hub.exec.boto3.client.ec2.describe_images(ctx, **ami_args)

    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]
    return result
