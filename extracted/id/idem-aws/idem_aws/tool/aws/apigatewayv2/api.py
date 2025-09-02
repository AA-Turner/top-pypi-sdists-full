from collections import OrderedDict
from typing import Any
from typing import Dict

"""
Util functions for AWS API Gateway v2 API resources.
"""


def convert_raw_api_to_present(hub, raw_resource: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert AWS API Gateway v2 API resource to a common idem present state.

    Args:
        hub: required for functions in hub.
        raw_resource(Dict[str, Any]): The AWS response to convert.

    Returns:
        Dict[str, Any]: Common idem present state
    """

    resource_parameters = OrderedDict(
        {
            "ApiEndpoint": "api_endpoint",
            "ApiGatewayManaged": "api_gateway_managed",
            "ApiId": "api_id",
            "ApiKeySelectionExpression": "api_key_selection_expression",
            "CorsConfiguration": "cors_configuration",
            "Description": "description",
            "DisableExecuteApiEndpoint": "disable_execute_api_endpoint",
            "DisableSchemaValidation": "disable_schema_validation",
            "Name": "name",
            "ProtocolType": "protocol_type",
            "RouteSelectionExpression": "route_selection_expression",
            "Tags": "tags",
            "Version": "version",
        }
    )
    resource_translated = {
        "resource_id": raw_resource.get("ApiId"),
    }

    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw) is not None:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated


async def update(
    hub,
    ctx,
    resource_id: str,
    raw_resource: Dict[str, Any],
    resource_parameters: Dict[str, None],
) -> Dict[str, Any]:
    """
    Updates an AWS API Gateway v2 API resource.

    Args:
        hub: required for functions in hub.
        ctx: context.
        resource_id(str): The API resource identifier in Amazon Web Services.
        raw_resource(Dict): Existing resource parameters in Amazon Web Services.
        resource_parameters(Dict): Parameters from SLS file.

    Returns:
        Dict[str, Any]
    """

    result = dict(comment=[], result=True, ret=None)

    parameters = OrderedDict(
        {
            "api_key_selection_expression": "ApiKeySelectionExpression",
            "cors_configuration": "CorsConfiguration",
            "credentials_arn": "CredentialsArn",
            "description": "Description",
            "disable_execute_api_endpoint": "DisableExecuteApiEndpoint",
            "disable_schema_validation": "DisableSchemaValidation",
            "route_key": "RouteKey",
            "route_selection_expression": "RouteSelectionExpression",
            "target": "Target",
            "version": "Version",
        }
    )

    parameters_to_update = {}

    cors_configuration = resource_parameters.get("cors_configuration")
    if cors_configuration is not None:
        update_cors_configuration = False
        old_cors_configuration = raw_resource.get("cors_configuration")

        if cors_configuration.get(
            "AllowCredentials"
        ) is not None and cors_configuration.get(
            "AllowCredentials"
        ) != old_cors_configuration.get(
            "MaxAge"
        ):
            update_cors_configuration = True
        elif (
            not hub.tool.aws.state_comparison_utils.are_lists_identical(
                cors_configuration.get("AllowHeaders"),
                old_cors_configuration.get("AllowHeaders"),
            )
            or not hub.tool.aws.state_comparison_utils.are_lists_identical(
                cors_configuration.get("AllowMethods"),
                old_cors_configuration.get("AllowMethods"),
            )
            or not hub.tool.aws.state_comparison_utils.are_lists_identical(
                cors_configuration.get("AllowOrigins"),
                old_cors_configuration.get("AllowOrigins"),
            )
            or not hub.tool.aws.state_comparison_utils.are_lists_identical(
                cors_configuration.get("ExposeHeaders"),
                old_cors_configuration.get("ExposeHeaders"),
            )
        ):
            update_cors_configuration = True
        elif cors_configuration.get("MaxAge") is not None and cors_configuration.get(
            "MaxAge"
        ) != old_cors_configuration.get("MaxAge"):
            update_cors_configuration = True

        if update_cors_configuration:
            parameters_to_update["CorsConfiguration"] = cors_configuration

        resource_parameters.pop("cors_configuration")

    for key, value in resource_parameters.items():
        if value is not None and value != raw_resource[key]:
            parameters_to_update[parameters[key]] = resource_parameters[key]

    if parameters_to_update:
        result["ret"] = {}
        for parameter_present, parameter_raw in parameters.items():
            if parameter_raw in parameters_to_update:
                result["ret"][parameter_present] = parameters_to_update[parameter_raw]

        if ctx.get("test", False):
            result["comment"] = (
                "Would update parameters: " + ",".join(result["ret"].keys()),
            )
        else:
            update_ret = await hub.exec.boto3.client.apigatewayv2.update_api(
                ctx,
                ApiId=resource_id,
                **parameters_to_update,
            )
            if not update_ret["result"]:
                result["result"] = False
                result["comment"] = update_ret["comment"]
                return result

            result["comment"] = (
                "Updated parameters: " + ",".join(result["ret"].keys()),
            )

    return result
