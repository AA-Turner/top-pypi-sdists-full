"""Exec module for managing Amazon API Gateway Methods."""


async def get(
    hub,
    ctx,
    resource_id: str,
    name: str = None,
):
    # TODO: will revisit this part later to improve building the get() call when multiple params are used to fetch a resource from AWS
    """Get an API Gateway Method from AWS.

    Args:
        resource_id(str): Idem Resource ID that is generated once the resource is created.

        name(str, Optional): An Idem name of the API Gateway Method.
    """

    result = dict(comment=[], ret=None, result=True)
    get_method = await hub.exec.boto3.client.apigateway.get_method(
        ctx,
        restApiId=resource_id.split("-")[0],
        resourceId=resource_id.split("-")[1],
        httpMethod=resource_id.split("-")[2],
    )

    if not get_method["result"]:
        if "NotFoundException" in str(get_method["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.apigateway.method", name=name
                )
            )
            result["comment"] += list(get_method["comment"])
            return result
        result["comment"] += list(get_method["comment"])
        result["result"] = False
        return result
    if not get_method["ret"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.apigateway.method", name=name
            )
        )
        return result

    if get_method["ret"]:
        result["ret"] = hub.tool.aws.apigateway.method.convert_raw_method_to_present(
            raw_resource=get_method["ret"],
            idem_resource_name=name,
            resource_id=resource_id,
        )

    return result
