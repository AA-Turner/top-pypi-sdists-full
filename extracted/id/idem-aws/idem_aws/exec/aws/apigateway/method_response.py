async def get(
    hub,
    ctx,
    resource_id: str,
    name: str = None,
):
    """
    Get an API Gateway Method Response from AWS.

    Args:
        hub:

        ctx:

        resource_id(str):
            Idem Resource ID that is generated once the resource is created,
                formatted as: rest_api_id-parent_resource_id-http_method-status_code.

        name(str, Optional):
            An Idem name of the API Gateway Method.

    """

    result = dict(comment=[], ret=None, result=True)
    if resource_id and len(resource_id.split("-")) == 4:
        rest_api_id, parent_resource_id, http_method, status_code = resource_id.split(
            "-"
        )

        get_method_response = (
            await hub.exec.boto3.client.apigateway.get_method_response(
                ctx,
                restApiId=rest_api_id,
                resourceId=parent_resource_id,
                httpMethod=http_method,
                statusCode=status_code,
            )
        )

        if not get_method_response["result"]:
            if "NotFoundException" or "'NoneType' object is not iterable" in str(
                get_method_response["comment"]
            ):
                result["comment"].append(
                    hub.tool.aws.comment_utils.get_empty_comment(
                        resource_type="aws.apigateway.method_response", name=name
                    )
                )
                result["comment"] += list(get_method_response["comment"])
                return result
            result["comment"] += list(get_method_response["comment"])
            result["result"] = False
            return result

        if get_method_response["ret"]:
            result[
                "ret"
            ] = hub.tool.aws.apigateway.method_response.convert_raw_method_response_to_present(
                idem_resource_name=name,
                raw_resource=get_method_response["ret"],
                resource_id=resource_id,
            )

        return result

    else:
        result["comment"] += [f"Invalid Resource ID '{resource_id}'."]
        result["result"] = False
        return result
