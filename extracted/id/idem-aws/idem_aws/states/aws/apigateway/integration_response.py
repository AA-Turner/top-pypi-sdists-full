"""State module for managing Amazon API Gateway Integration Responses."""
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
    response_templates: Dict = None,
    response_parameters: Dict = None,
    content_handling: str = None,
    selection_pattern: str = None,
):
    """
    Creates a new API Gateway Integration Response or modifies an existing one.

    Args:
        name(str):
            An idem name of the resource.

        rest_api_id(str):
            AWS rest_api id of the associated RestApi.

        http_method(str):
            String that specifies the method request's HTTP method type.

        status_code(str):
            The method response's status code.

        parent_resource_id(str):
            The parent resource's id.

        resource_id(str, Optional):
            Defaults to None. Idem Resource id, formatted as: rest_api_id-parent_resource_id-http_method-status_code.

        response_parameters(dict, Optional):
            A key-value map specifying response parameters that are passed to the method response from the back end.
                The key is a method response header parameter name and the mapped value is an integration response header
                value, a static value enclosed within a pair of single quotes, or a JSON expression from the integration
                response body. The mapping key must match the pattern of method.response.header.{name} , where name is a
                valid and unique header name. The mapped non-static value must match the pattern of
                integration.response.header.{name} or integration.response.body.{JSON-expression} , where name must be a
                valid and unique response header name and JSON-expression a valid JSON expression without the $ prefix.
                Must be of format {'string': 'string'}.

        response_templates(dict, Optional):
            Specifies a put integration response's templates. Must be of format {'string': 'string'}.

        content_handling(str, Optional):
            Specifies how to handle response payload content type conversions. Supported values are CONVERT_TO_BINARY
                and CONVERT_TO_TEXT , with the following behaviors: If this property is not defined, the response payload
                will be passed through from the integration response to the method response without modification.

        selection_pattern(str, Optional):
            Specifies the selection pattern of a put integration response.

    Returns:
        dict[str, Any]

    Request Syntax:
        .. code-block:: sls

            [idem_test_aws_apigateway_integration_response]:
              aws.apigateway.integration_response.present:
                - name: 'string'
                - rest_api_id: 'string'
                - parent_resource_id: 'string'
                - http_method: 'string'
                - status_code: 'string'
                - response_parameters: dict
                - response_templates: dict
                - content_handling: 'string'
                - selection_pattern: 'string'

    Examples:
        .. code-block:: sls

            idem_test_apigateway_integration_response:
              aws.apigateway.integration_response.present:
                - name: 'idem_test_apigateway_integration_response'
                - rest_api_id: 'integration.get('rest_api_id')'
                - parent_resource_id: 'integration.get('parent_resource_id')'
                - http_method: 'GET'
                - status_code: '400'

    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False

    if resource_id:
        before = await hub.exec.aws.apigateway.integration_response.get(
            ctx,
            name=name,
            resource_id=resource_id,
        )

        if not before["result"] or not before["ret"]:
            result["comment"] = before["comment"]
            result["result"] = False
            return result

        result["old_state"] = before["ret"]

        update_parameters = {
            "response_templates": response_templates,
            "response_parameters": response_parameters,
            "content_handling": content_handling,
            "selection_pattern": selection_pattern,
        }

        update_integration_response_ret = (
            await hub.tool.aws.apigateway.integration_response.update(
                ctx,
                old_state=result["old_state"],
                updatable_parameters=update_parameters,
            )
        )
        result["comment"] = (
            result["comment"] + update_integration_response_ret["comment"]
        )

        if not update_integration_response_ret["result"]:
            result["result"] = False
            return result
        resource_updated = bool(update_integration_response_ret["ret"])

    else:
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
                    "response_templates": response_templates,
                    "content_handling": content_handling,
                    "selection_pattern": selection_pattern,
                },
            )

            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.apigateway.integration_response", name=name
            )
            return result

        resource_id = f"{rest_api_id}-{parent_resource_id}-{http_method}-{status_code}"

        ret = await hub.exec.boto3.client.apigateway.put_integration_response(
            ctx,
            restApiId=rest_api_id,
            resourceId=parent_resource_id,
            httpMethod=http_method,
            statusCode=status_code,
            responseTemplates=response_templates,
            responseParameters=response_parameters,
            contentHandling=content_handling,
        )

        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.apigateway.integration_response", name=name
        )

    if (not before) or resource_updated:
        after = await hub.exec.aws.apigateway.integration_response.get(
            ctx,
            name=name,
            resource_id=resource_id,
        )
        if not (after["result"] and after["ret"]):
            result["result"] = False
            result["comment"] += after["comment"]
            return result

        result["new_state"] = after["ret"]
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(hub, ctx, name: str, resource_id: str = None):
    """
    Deletes an API Gateway Integration Response.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            Idem Resource id, formatted as: rest_api_id-parent_resource_id-http_method-status_code. Defaults to None.
                Idem automatically considers this resource being absent if this field is not specified.

    Request Syntax:
        .. code-block:: sls

          [idem_test_aws_apigateway_integration_response]:
            aws.apigateway.integration_response.absent:
              - name: 'string'
              - resource_id: 'string'

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: sls

          idem_test_aws_apigateway_integration_response:
            aws.apigateway.integration_response.absent:
              - name: 'idem_test_apigateway_integration_response'
              - resource_id: 'rest_api_id-parent_resource_id-http_method-status_code'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        # if resource_id isn't specified, the resource is considered to be absent.
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.apigateway.integration_response", name=name
        )
        return result

    before_ret = await hub.exec.aws.apigateway.integration_response.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )

    if not before_ret["result"]:
        result["result"] = False
        result["comment"] = before_ret["comment"]

    if not before_ret["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.apigateway.integration_response", name=name
        )
        return result

    elif ctx.get("test", False):
        result["old_state"] = before_ret["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.apigateway.integration_response", name=name
        )
        return result

    else:
        rest_api_id, parent_resource_id, http_method, status_code = resource_id.split(
            "-"
        )
        result["old_state"] = before_ret["ret"]
        delete_ret = await hub.exec.boto3.client.apigateway.delete_integration_response(
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
            resource_type="aws.apigateway.integration_response", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """

    Describe the API Gateway Integration Responses associated with a specific Integration.

    Returns a list of apigateway.integration_response descriptions

    Returns:
        dict[str, dict[str, Any]]


    Examples:

        .. code-block:: bash

            $ idem describe aws.apigateway.integration_response

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
                        integration_resource_id = (
                            f"{rest_api_id}-{parent_resource_id}-{resource_method}"
                        )
                        integration_ret = await hub.exec.aws.apigateway.integration.get(
                            ctx, resource_id=integration_resource_id
                        )
                        if not integration_ret["result"]:
                            hub.log.debug(
                                f"Could not get Integration {integration_ret['comment']}. Will skip this Integration."
                            )
                            continue
                        integration_responses = integration_ret["ret"].get(
                            "integration_responses", []
                        )

                        for status_code in integration_responses:
                            int_resp_resource_id = f"{rest_api_id}-{parent_resource_id}-{resource_method}-{status_code}"

                            integration_response = (
                                await hub.exec.aws.apigateway.integration_response.get(
                                    ctx, resource_id=int_resp_resource_id
                                )
                            )
                            if not integration_response["result"]:
                                hub.log.debug(
                                    f"Could not get Integration Response {integration_response['comment']}. Will skip this Integration Response."
                                )
                                continue

                            resource_translated = integration_response["ret"]
                            result[resource_translated["resource_id"]] = {
                                "aws.apigateway.integration_response.present": [
                                    {parameter_key: parameter_value}
                                    for parameter_key, parameter_value in resource_translated.items()
                                ]
                            }
    return result
