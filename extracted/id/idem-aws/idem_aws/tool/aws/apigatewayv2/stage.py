"""Util functions for AWS API Gateway v2 Stage resources."""
from collections import OrderedDict
from typing import Any
from typing import Dict


def convert_raw_stage_to_present(
    hub, api_id: str, raw_resource: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert AWS API Gateway v2 Stage resource to a common idem present state.

    Args:
        hub: required for functions in hub.
        api_id(str): The API resource identifier in Amazon Web Services.
        raw_resource(Dict[str, Any]): The AWS response to convert.

    Returns:
        Dict[str, Any]: Common idem present state
    """

    resource_parameters = OrderedDict(
        {
            "AccessLogSettings": "access_log_settings",
            "ApiGatewayManaged": "api_gateway_managed",
            "AutoDeploy": "auto_deploy",
            "ClientCertificateId": "client_certificate_id",
            "DefaultRouteSettings": "default_route_settings",
            "DeploymentId": "deployment_id",
            "Description": "description",
            "LastDeploymentStatusMessage": "last_deployment_status_message",
            "RouteSettings": "route_settings",
            "StageVariables": "stage_variables",
            "Tags": "tags",
        }
    )
    resource_translated = {
        "resource_id": raw_resource.get("StageName"),
        "name": raw_resource.get("StageName"),
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
    """Updates a Stage.

    Args:
        api_id(str):
            The API identifier.

        resource_id(str):
            The stage name. Stage names can contain only alphanumeric characters, hyphens, and underscores,
            or be $default. Maximum length is 128 characters.

        raw_resource(dict[str, Any]):
            Existing resource parameters in AWS.

        resource_parameters(dict[str, Any]):
            Parameters from SLS file.

    Returns:
        Dict[str, Any]:
            Returns the updated stage.
    """
    result = dict(comment=[], result=True, ret=None)

    parameters = OrderedDict(
        {
            "AccessLogSettings": "access_log_settings",
            "AutoDeploy": "auto_deploy",
            "ClientCertificateId": "client_certificate_id",
            "DefaultRouteSettings": "default_route_settings",
            "DeploymentId": "deployment_id",
            "Description": "description",
            "RouteSettings": "route_settings",
            "StageVariables": "stage_variables",
        }
    )

    parameters_to_update = {}

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
            update_ret = await hub.exec.boto3.client.apigatewayv2.update_stage(
                ctx,
                ApiId=api_id,
                StageName=resource_id,
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
