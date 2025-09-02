from collections import OrderedDict
from typing import Any
from typing import Dict

"""
Util functions for AWS API Gateway v2 Authorizer resources.
"""


def convert_raw_authorizer_to_present(
    hub, api_id: str, raw_resource: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert AWS API Gateway v2 Authorizer resource to a common idem present state.

    Args:
        hub: required for functions in hub.
        api_id(str): The API resource identifier in Amazon Web Services.
        raw_resource(Dict[str, Any]): The AWS response to convert.

    Returns:
        Dict[str, Any]: Common idem present state
    """

    resource_parameters = OrderedDict(
        {
            "AuthorizerCredentialsArn": "authorizer_credentials_arn",
            "AuthorizerPayloadFormatVersion": "authorizer_payload_format_version",
            "AuthorizerResultTtlInSeconds": "authorizer_result_ttl_in_seconds",
            "AuthorizerType": "authorizer_type",
            "AuthorizerUri": "authorizer_uri",
            "EnableSimpleResponses": "enable_simple_responses",
            "IdentitySource": "identity_source",
            "JwtConfiguration": "jwt_configuration",
        }
    )
    resource_translated = {
        "name": raw_resource.get("Name"),
        "resource_id": raw_resource.get("AuthorizerId"),
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
    Updates an AWS API Gateway v2 Authorizer resource.

    Args:
        hub: required for functions in hub.
        ctx: context.
        api_id(str): The API resource identifier in Amazon Web Services.
        resource_id(str): The Authorizer resource identifier in Amazon Web Services.
        raw_resource(Dict): Existing resource parameters in Amazon Web Services.
        resource_parameters(Dict): Parameters from SLS file.

    Returns:
        Dict[str, Any]
    """

    result = dict(comment=[], result=True, ret=None)

    parameters = OrderedDict(
        {
            "authorizer_credentials_arn": "AuthorizerCredentialsArn",
            "authorizer_payload_format_version": "AuthorizerPayloadFormatVersion",
            "authorizer_result_ttl_in_seconds": "AuthorizerResultTtlInSeconds",
            "authorizer_type": "AuthorizerType",
            "authorizer_uri": "AuthorizerUri",
            "enable_simple_responses": "EnableSimpleResponses",
            "identity_source": "IdentitySource",
            "jwt_configuration": "JwtConfiguration",
        }
    )

    parameters_to_update = {}

    identity_source = resource_parameters.get("identity_source")
    if identity_source is not None:
        if set(identity_source) != set(raw_resource.get("identity_source", [])):
            parameters_to_update["IdentitySource"] = identity_source
        resource_parameters.pop("identity_source")

    jwt_configuration = resource_parameters.get("jwt_configuration")
    if jwt_configuration is not None:
        update_jwt_configuration = False
        old_jwt_configuration = raw_resource.get("jwt_configuration")

        if set(jwt_configuration.get("Audience", [])) != set(
            old_jwt_configuration.get("Audience", [])
        ):
            update_jwt_configuration = True
        elif jwt_configuration.get("Issuer") is not None and jwt_configuration.get(
            "Issuer"
        ) != old_jwt_configuration.get("Issuer"):
            update_jwt_configuration = True

        if update_jwt_configuration:
            parameters_to_update["JwtConfiguration"] = jwt_configuration

        resource_parameters.pop("jwt_configuration")

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
            update_ret = await hub.exec.boto3.client.apigatewayv2.update_authorizer(
                ctx,
                ApiId=api_id,
                AuthorizerId=resource_id,
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
