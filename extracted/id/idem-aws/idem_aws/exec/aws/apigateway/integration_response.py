"""Exec module for managing Amazon API Gateway Integration Responses."""


async def get(
    hub,
    ctx,
    resource_id: str,
    name: str = None,
):
    """
    Get an API Gateway Integration Response from AWS.

    Args:
        resource_id(str):
            Idem Resource ID that is generated once the resource is created,
                formatted as: <rest_api_id>-<parent_resource_id>-<http_method>-<status_code>

        name(str, Optional):
            An Idem name of the API Gateway Integration.

    Returns:
        .. code-block:: python

            {"result": True|False, "comment": A message List, "ret": Dict[str, Any]}

    Examples:

        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.apigateway.integration_response.get resource_id="resource_id" name=name


        Calling this exec module function from within a state module in pure python

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, name):
                ret = await hub.exec.aws.apigateway.integration_response.get(ctx, resource_id=resource_id, name=name)

    """

    result = dict(comment=[], ret=None, result=True)
    if resource_id and len(resource_id.split("-")) == 4:
        rest_api_id, parent_resource_id, http_method, status_code = resource_id.split(
            "-"
        )

        get_integration_response = (
            await hub.exec.boto3.client.apigateway.get_integration_response(
                ctx,
                restApiId=rest_api_id,
                resourceId=parent_resource_id,
                httpMethod=http_method,
                statusCode=status_code,
            )
        )

        if not get_integration_response["result"]:
            if "NotFoundException" in str(get_integration_response["comment"]):
                result["comment"].append(
                    hub.tool.aws.comment_utils.get_empty_comment(
                        resource_type="aws.apigateway.integration_response", name=name
                    )
                )
                result["comment"] += list(get_integration_response["comment"])
                return result
            result["comment"] += list(get_integration_response["comment"])
            result["result"] = False
            return result

        if get_integration_response["ret"]:
            result[
                "ret"
            ] = hub.tool.aws.apigateway.integration_response.convert_raw_integration_response_to_present(
                idem_resource_name=name,
                raw_resource=get_integration_response["ret"],
                resource_id=resource_id,
            )

        return result

    else:
        result["comment"] += [
            f"Invalid Resource ID '{resource_id}'. Resource ID should be of format <rest_api_id>-<parent_resource_id>-<http_method>-<status_code>."
        ]
        result["result"] = False
        return result
