"""Util functions for AWS API Gateway v2 Route resources."""
from collections import OrderedDict
from typing import Any
from typing import Dict


def convert_raw_route_to_present(
    hub, api_id: str, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    """
    Convert AWS API Gateway v2 Route resource to a common idem present state.

    Args:
        hub: required for functions in hub.
        api_id(str): The API resource identifier in Amazon Web Services.
        raw_resource(Dict[str, Any]): The AWS response to convert.
        idem_resource_name(str, Optional): An Idem name of the resource.

    Returns:
        Dict[str, Any]: Common idem present state
    """

    resource_parameters = OrderedDict(
        {
            "ApiGatewayManaged": "api_gateway_managed",
            "ApiKeyRequired": "api_key_required",
            "AuthorizationScopes": "authorization_scopes",
            "AuthorizationType": "authorization_type",
            "AuthorizerId": "authorizer_id",
            "ModelSelectionExpression": "model_selection_expression",
            "OperationName": "operation_name",
            "RequestModels": "request_models",
            "RequestParameters": "request_parameters",
            "RouteId": "route_id",
            "RouteKey": "route_key",
            "RouteResponseSelectionExpression": "route_response_selection_expression",
            "Target": "target",
        }
    )
    resource_translated = {
        "name": idem_resource_name
        if idem_resource_name
        else raw_resource.get("RouteId"),
        "resource_id": raw_resource.get("RouteId"),
        "api_id": api_id,
    }

    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw) is not None:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated


async def update(
    hub,
    ctx,
    api_id: str,
    resource_id: str,
    raw_resource: Dict[str, Any],
    resource_parameters: Dict[str, Any],
) -> Dict[str, Any]:
    """Updates a Route.

    Args:
        api_id(str):
            The API identifier.

        resource_id(str):
            The route ID.

        raw_resource(dict[str, Any]):
            Existing resource parameters in AWS.

        resource_parameters(dict[str, Any]):
            Parameters from SLS file.

    Returns:
        Dict[str, Any]:
            Returns the updated route.
    """
    result = dict(comment=[], result=True, ret=None)

    parameters = OrderedDict(
        {
            "ApiKeyRequired": "api_key_required",
            "AuthorizationScopes": "authorization_scopes",
            "AuthorizationType": "authorization_type",
            "AuthorizerId": "authorizer_id",
            "ModelSelectionExpression": "model_selection_expression",
            "OperationName": "operation_name",
            "RequestModels": "request_models",
            "RequestParameters": "request_parameters",
            "RouteKey": "route_key",
            "RouteResponseSelectionExpression": "route_response_selection_expression",
            "Target": "target",
        }
    )

    parameters_to_update = {}

    authorization_scopes = resource_parameters.get("AuthorizationScopes")
    if authorization_scopes is not None:
        if not hub.tool.aws.state_comparison_utils.are_lists_identical(
            authorization_scopes,
            raw_resource.get("AuthorizationScopes"),
        ):
            parameters_to_update["AuthorizationScopes"] = authorization_scopes

        resource_parameters.pop("AuthorizationScopes")

    for key, value in resource_parameters.items():
        if value is not None and value != raw_resource.get(key):
            parameters_to_update[key] = resource_parameters[key]

    if parameters_to_update:
        result["ret"] = {}
        for parameter_raw, parameter_present in parameters.items():
            if parameter_raw in parameters_to_update:
                result["ret"][parameter_present] = parameters_to_update[parameter_raw]

        if ctx.get("test", False):
            result["comment"] = (
                f"Would update parameters: " + ",".join(result["ret"].keys()),
            )
        else:
            update_ret = await hub.exec.boto3.client.apigatewayv2.update_route(
                ctx,
                ApiId=api_id,
                RouteId=resource_id,
                **parameters_to_update,
            )
            if not update_ret["result"]:
                result["result"] = False
                result["comment"] = update_ret["comment"]
                return result

            result["comment"] = (
                f"Updated parameters: " + ",".join(result["ret"].keys()),
            )

    return result
