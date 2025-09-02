import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    rest_api_id: str,
    http_method: str,
    status_code: str,
    parent_resource_id: str,
    resource_id: str = None,
    response_models: Dict = None,
    response_parameters: Dict = None,
):
    """
    Creates a new API Gateway Method Response or modifies an existing one.

    Args:
        name(str):
            An idem name of the resource.

        rest_api_id(str):
            AWS rest_api id of the associated RestApi.

        parent_resource_id(str):
            The parent resource's id.

        http_method(str):
            String that specifies the method request's HTTP method type.

        status_code(str):
            The method response's status code.

        resource_id(str, Optional):
            Defaults to None. Idem Resource id, formatted as: rest_api_id-parent_resource_id-http_method-status_code.

        response_models(dict, Optional):
            Specifies the Model resources used for the response's content-type.
                Response models are represented as a key/value map, with a content-type as the key and a Model name
                as the value.

        response_parameters(dict, Optional):
            A key-value map specifying required or optional response parameters
                that API Gateway can send back to the caller. A key defines a method response header and the value
                specifies whether the associated method response header is required or not. The expression of the key
                must match the pattern method.response.header.{name} , where name is a valid and unique header name.
                API Gateway passes certain integration response data to the method response headers specified here
                according to the mapping you prescribe in the API's IntegrationResponse. The integration response data
                that can be mapped include an integration response header expressed in integration.response.header.{name},
                a static value enclosed within a pair of single quotes (e.g., 'application/json' ), or a JSON expression
                from the back-end response payload in the form of integration.response.body.{JSON-expression},
                where JSON-expression is a valid JSON expression without the $ prefix.)

    Request Syntax:
        [idem_test_aws_apigateway_method_response]:
          aws.apigateway.method_response.present:
            - name: 'string'
            - rest_api_id: 'string'
            - parent_resource_id: 'string'
            - http_method: 'string'
            - status_code: 'string'

    Returns:
        Dict[str, Any]

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False

    if resource_id:
        before = await hub.exec.aws.apigateway.method_response.get(
            ctx,
            name=name,
            resource_id=resource_id,
        )

        if not before["result"] or not before["ret"]:
            result["comment"] = before["comment"]
            result["result"] = False
            return result

        result["old_state"] = before["ret"]
        result["new_state"] = copy.deepcopy(result["old_state"])

        update_parameters = {
            "response_models": response_models,
            "response_parameters": response_parameters,
        }

        update_method_response_ret = (
            await hub.tool.aws.apigateway.method_response.update(
                ctx,
                old_state=result["old_state"],
                updatable_resource_parameters=update_parameters,
            )
        )
        result["comment"] += update_method_response_ret["comment"]

        if not update_method_response_ret["result"]:
            result["result"] = False
            return result
        resource_updated = bool(update_method_response_ret["ret"])

    else:
        resource_id = f"{rest_api_id}-{parent_resource_id}-{http_method}-{status_code}"

        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "rest_api_id": rest_api_id,
                    "parent_resource_id": parent_resource_id,
                    "http_method": http_method,
                    "status_code": status_code,
                    "response_parameters": response_parameters,
                    "response_models": response_models,
                },
            )

            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.apigateway.method_response", name=name
            )
            return result

        ret = await hub.exec.boto3.client.apigateway.put_method_response(
            ctx,
            restApiId=rest_api_id,
            resourceId=parent_resource_id,
            httpMethod=http_method,
            statusCode=status_code,
            responseModels=response_models,
            responseParameters=response_parameters,
        )

        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.apigateway.method_response", name=name
        )
    if (not before) or resource_updated:
        after = await hub.exec.aws.apigateway.method_response.get(
            ctx,
            name=name,
            resource_id=resource_id,
        )
        if not (after["result"] and after["ret"]):
            result["result"] = False
            result["comment"] += after["comment"]
            return result

        resource_translated = after["ret"]
        result["new_state"] = resource_translated
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """
    Deletes an API Gateway Method Response.

    Args:
        hub:

        ctx:

        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            Idem Resource id, formatted as: rest_api_id-parent_resource_id-http_method-status_code. Defaults to None.
                Idem automatically considers this resource being absent if this field is not specified.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

        idem_test_aws_apigateway_method_response:
          aws.apigateway.method_response.absent:
            - name: value
            - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        # if resource_id isn't specified, the resource is considered to be absent.
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.apigateway.method_response", name=name
        )
        return result

    before_ret = await hub.exec.aws.apigateway.method_response.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )

    if not before_ret["result"]:
        result["result"] = False
        result["comment"] = before_ret["comment"]

    if not before_ret["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.apigateway.method_response", name=name
        )
        return result

    elif ctx.get("test", False):
        result["old_state"] = before_ret["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.apigateway.method_response", name=name
        )
        return result

    else:
        rest_api_id, parent_resource_id, http_method, status_code = resource_id.split(
            "-"
        )
        result["old_state"] = before_ret["ret"]
        delete_ret = await hub.exec.boto3.client.apigateway.delete_method_response(
            ctx,
            restApiId=rest_api_id,
            resourceId=parent_resource_id,
            httpMethod=http_method,
            statusCode=status_code,
        )

        if not delete_ret["result"]:
            result["result"] = False
            result["comment"] = delete_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.apigateway.method_response", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """

    Describe the API Gateway Method Responses associated with a specific Method.

    Returns a list of apigateway.method_response descriptions

    Returns:
        Dict[str, Any]


    Examples:

        .. code-block:: bash

            $ idem describe aws.apigateway.method_response

    """

    result = {}

    get_rest_apis_ret = await hub.exec.boto3.client.apigateway.get_rest_apis(ctx)
    if not get_rest_apis_ret["result"]:
        hub.log.warning(f"Could not get Rest Apis {get_rest_apis_ret['comment']}")
        return result

    for rest_api in get_rest_apis_ret["ret"]["items"]:
        rest_api_id = rest_api.get("id")

        get_resources_ret = await hub.exec.boto3.client.apigateway.get_resources(
            ctx, restApiId=rest_api_id
        )
        if not get_resources_ret["result"]:
            hub.log.debug(
                f"Could not get Resources {get_resources_ret['comment']}. Will skip this Resource."
            )
            continue

        if get_resources_ret["ret"]["items"] is not None:
            for resource in get_resources_ret["ret"]["items"]:
                parent_resource_id = resource.get("id")
                if resource.get("resourceMethods") is not None:
                    for resource_method in resource.get("resourceMethods"):
                        method = await hub.exec.boto3.client.apigateway.get_method(
                            ctx,
                            restApiId=rest_api_id,
                            resourceId=parent_resource_id,
                            httpMethod=resource_method,
                        )
                        if not method["result"]:
                            hub.log.debug(
                                f"Could not get Resource Method {method['comment']}. Will skip this Method."
                            )
                            continue

                        http_method = method["ret"]["httpMethod"]
                        for method_response in method["ret"].get("methodResponses", {}):
                            resource_id = f"{rest_api_id}-{parent_resource_id}-{http_method}-{method_response}"

                            method_response = (
                                await hub.exec.aws.apigateway.method_response.get(
                                    ctx,
                                    resource_id=resource_id,
                                )
                            )
                            if (
                                not method_response["result"]
                                or not method_response["ret"]
                            ):
                                hub.log.debug(
                                    f"Could not get Resource Method Response {method_response['comment']}. Will skip this Method Response."
                                )
                                continue

                            resource_translated = method_response["ret"]
                            result[resource_translated["resource_id"]] = {
                                "aws.apigateway.method_response.present": [
                                    {parameter_key: parameter_value}
                                    for parameter_key, parameter_value in resource_translated.items()
                                ]
                            }

    return result
