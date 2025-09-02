"""Exec module for managing Amazon API Gateway Resources."""


async def get(hub, ctx, name: str, resource_id: str, rest_api_id: str):
    """Get an API Gateway Resource from AWS.

    Args:
        name (str): An Idem name of the API Gateway Resource.

        resource_id (str): AWS Resource id of the associated Rest API.

        rest_api_id (str): AWS rest_api id of the associated RestApi.
    """

    result = dict(comment=[], ret=None, result=True)
    before = await hub.exec.boto3.client.apigateway.get_resource(
        ctx, resourceId=resource_id, restApiId=rest_api_id
    )

    if not before["result"]:
        if "NotFoundException" in str(before["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.api.gateway", name=name
                )
            )
            result["comment"] += list(before["comment"])
            return result
        result["result"] = False
        result["comment"] = before["comment"]
        return result

    if before["ret"]:
        result["ret"] = before["ret"]

    return result
