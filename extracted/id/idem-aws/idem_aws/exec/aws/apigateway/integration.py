async def get(
    hub,
    ctx,
    resource_id: str,
    name: str = None,
):
    """
    Get a single API Gateway Integration from AWS. The function returns None if no resource is found.

    Args:
        resource_id(str):
            Idem Resource ID that is generated once the resource is created,
            formatted as: rest_api_id-parent_resource_id-http_method.

        name(str, Optional):
            An Idem name of the API Gateway Integration.
    """
    result = dict(comment=[], ret=None, result=True)

    if resource_id and len(resource_id.split("-")) == 3:
        rest_api_id, parent_resource_id, http_method = resource_id.split("-")
        get_integration = await hub.exec.boto3.client.apigateway.get_integration(
            ctx,
            restApiId=rest_api_id,
            resourceId=parent_resource_id,
            httpMethod=http_method,
        )

        if not get_integration["result"]:
            if "NotFoundException" in str(get_integration["comment"]):
                result["comment"].append(
                    hub.tool.aws.comment_utils.get_empty_comment(
                        resource_type="aws.apigateway.integration", name=name
                    )
                )
                result["comment"] += list(get_integration["comment"])
                return result
            result["comment"] += list(get_integration["comment"])
            result["result"] = False
            return result

        if get_integration["ret"]:
            result[
                "ret"
            ] = hub.tool.aws.apigateway.integration.convert_raw_integration_to_present(
                idem_resource_name=name,
                raw_resource=get_integration["ret"],
                resource_id=resource_id,
            )

        return result

    else:
        result["comment"] = [f"Invalid Resource ID '{resource_id}'."]
        result["result"] = False
        return result
