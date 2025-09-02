from collections import OrderedDict
from typing import Any
from typing import Dict

"""
Util functions for AWS API Gateway v2 Integration resources.
"""


def convert_raw_integration_to_present(
    hub, api_id: str, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    """
    Convert AWS API Gateway v2 Integration resource to a common idem present state.

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
            "ConnectionId": "connection_id",
            "ConnectionType": "connection_type",
            "ContentHandlingStrategy": "content_handling_strategy",
            "CredentialsArn": "credentials_arn",
            "Description": "description",
            "IntegrationMethod": "integration_method",
            "IntegrationResponseSelectionExpression": "integration_response_selection_expression",
            "IntegrationSubtype": "integration_subtype",
            "IntegrationType": "integration_type",
            "IntegrationUri": "integration_uri",
            "PassthroughBehavior": "passthrough_behavior",
            "PayloadFormatVersion": "payload_format_version",
            "RequestParameters": "request_parameters",
            "RequestTemplates": "request_templates",
            "ResponseParameters": "response_parameters",
            "TemplateSelectionExpression": "template_selection_expression",
            "TimeoutInMillis": "timeout_in_millis",
            "TlsConfig": "tls_config",
        }
    )
    resource_translated = {
        "name": idem_resource_name
        if idem_resource_name
        else raw_resource.get("IntegrationId"),
        "resource_id": raw_resource.get("IntegrationId"),
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
    resource_parameters: Dict[str, None],
) -> Dict[str, Any]:
    """
    Updates an AWS API Gateway v2 Integration resource.

    Args:
        api_id(str): The API resource identifier in Amazon Web Services.
        resource_id(str): The Integration resource identifier in Amazon Web Services.
        raw_resource(Dict): Existing resource parameters in Amazon Web Services.
        resource_parameters(Dict): Parameters from SLS file.

    Returns:
        Dict[str, Any]
    """

    result = dict(comment=[], result=True, ret=None)

    parameters = OrderedDict(
        {
            "connection_id": "ConnectionId",
            "connection_type": "ConnectionTypes",
            "content_handling_strategy": "ContentHandlingStrategy",
            "credentials_arn": "CredentialsArn",
            "description": "Description",
            "integration_method": "IntegrationMethod",
            "integration_subtype": "IntegrationSubtype",
            "integration_type": "IntegrationType",
            "integration_uri": "IntegrationUri",
            "passthrough_behavior": "PassthroughBehavior",
            "payload_format_version": "PayloadFormatVersion",
            "request_parameters": "RequestParameters",
            "request_templates": "RequestTemplates",
            "response_parameters": "ResponseParameters",
            "template_selection_expression": "TemplateSelectionExpression",
            "timeout_in_millis": "TimeoutInMillis",
            "tls_config": "TlsConfig",
        }
    )

    parameters_to_update = {}

    for key, value in resource_parameters.items():
        if value is not None and value != raw_resource.get(key):
            parameters_to_update[parameters[key]] = resource_parameters[key]

    if parameters_to_update:
        result["ret"] = {}
        for parameter_present, parameter_raw in parameters.items():
            if parameter_raw in parameters_to_update:
                result["ret"][parameter_present] = parameters_to_update[parameter_raw]

        if ctx.get("test", False):
            result["comment"] = (
                f"Would update parameters: " + ",".join(result["ret"].keys()),
            )
        else:
            update_ret = await hub.exec.boto3.client.apigatewayv2.update_integration(
                ctx,
                ApiId=api_id,
                IntegrationId=resource_id,
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
