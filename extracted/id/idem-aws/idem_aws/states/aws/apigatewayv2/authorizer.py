"""States module for API Gateway v2 authorized resources."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    api_id: str,
    authorizer_type: str,
    identity_source: List[str],
    resource_id: str = None,
    authorizer_credentials_arn: str = None,
    authorizer_payload_format_version: str = None,
    authorizer_result_ttl_in_seconds: int = None,
    authorizer_uri: str = None,
    enable_simple_responses: bool = None,
    jwt_configuration: make_dataclass(
        "JWTConfiguration",
        [
            ("Audience", List[str], field(default=None)),
            ("Issuer", str, field(default=None)),
        ],
    ) = None,
) -> Dict[str, Any]:
    """Creates an API Gateway v2 authorized resource.

    Args:
        name(str): An Idem name of the resource. This is also used as the name of the Authorizer during resource creation.
        api_id(str): The API resource identifier in Amazon Web Services.
        authorizer_type(str): The authorizer type. Specify REQUEST for a Lambda function using incoming request parameters.
            Specify JWT to use JSON Web Tokens (supported only for HTTP APIs).
        resource_id(str, Optional): The authorizer resource identifier in Amazon Web Services.
        authorizer_credentials_arn(str, Optional): Specifies the required credentials as an IAM role for API Gateway to invoke the authorizer. To
            specify an IAM role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To use
            resource-based permissions on the Lambda function, don't specify this parameter. Supported only
            for REQUEST authorizers.
        authorizer_payload_format_version(str, Optional): Specifies the format of the payload sent to an HTTP API Lambda authorizer. Required for HTTP API
            Lambda authorizers. Supported values are 1.0 and 2.0. To learn more, see Working with AWS Lambda
            authorizers for HTTP APIs.
        authorizer_result_ttl_in_seconds(int, Optional): The time to live (TTL) for cached authorizer results, in seconds. If it equals 0, authorization
            caching is disabled. If it is greater than 0, API Gateway caches authorizer responses. The
            maximum value is 3600, or 1 hour. Supported only for HTTP API Lambda authorizers.
        authorizer_type(str): The authorizer type. Specify REQUEST for a Lambda function using incoming request parameters.
            Specify JWT to use JSON Web Tokens (supported only for HTTP APIs).
        authorizer_uri(str, Optional): The authorizer's Uniform Resource Identifier (URI). For REQUEST authorizers, this must be a
            well-formed Lambda function URI, for example, arn:aws:apigateway:us-
            west-2:lambda:path/2015-03-31/functions/arn:aws:lambda:us-
            west-2:{account_id}:function:{lambda_function_name}/invocations. In general, the URI has this
            form: arn:aws:apigateway:{region}:lambda:path/{service_api}                , where {region} is
            the same as the region hosting the Lambda function, path indicates that the remaining substring
            in the URI should be treated as the path to the resource, including the initial /. For Lambda
            functions, this is usually of the form /2015-03-31/functions/[FunctionARN]/invocations.
            Supported only for REQUEST authorizers.
        enable_simple_responses(bool, Optional): Specifies whether a Lambda authorizer returns a response in a simple format. By default, a
            Lambda authorizer must return an IAM policy. If enabled, the Lambda authorizer can return a
            boolean value instead of an IAM policy. Supported only for HTTP APIs. To learn more, see Working
            with AWS Lambda authorizers for HTTP APIs.
        identity_source(List): The identity source for which authorization is requested. For a REQUEST authorizer, this is
            optional. The value is a set of one or more mapping expressions of the specified request
            parameters. The identity source can be headers, query string parameters, stage variables, and
            context parameters. For example, if an Auth header and a Name query string parameter are defined
            as identity sources, this value is route.request.header.Auth, route.request.querystring.Name for
            WebSocket APIs. For HTTP APIs, use selection expressions prefixed with $, for example,
            $request.header.Auth, $request.querystring.Name. These parameters are used to perform runtime
            validation for Lambda-based authorizers by verifying all of the identity-related request
            parameters are present in the request, not null, and non-empty. Only when this is true does the
            authorizer invoke the authorizer Lambda function. Otherwise, it returns a 401 Unauthorized
            response without calling the Lambda function. For HTTP APIs, identity sources are also used as
            the cache key when caching is enabled. To learn more, see Working with AWS Lambda authorizers
            for HTTP APIs. For JWT, a single entry that specifies where to extract the JSON Web Token (JWT)
            from inbound requests. Currently only header-based and query parameter-based selections are
            supported, for example $request.header.Authorization.
        jwt_configuration(dict[str, Any], Optional): Represents the configuration of a JWT authorizer. Required for the JWT authorizer type.
            Supported only for HTTP APIs. Defaults to None.

            * Audience (list[str], Optional): A list of the intended recipients of the JWT. A valid JWT must provide an aud that matches at
                least one entry in this list. See RFC 7519. Supported only for HTTP APIs.
            * Issuer (str, Optional): The base domain of the identity provider that issues JSON Web Tokens. For example, an Amazon
                Cognito user pool has the following format: https://cognito-idp.{region}.amazonaws.com/{userPoolId}.
                Required for the JWT authorizer type. Supported only for HTTP APIs.

    Request Syntax:
        .. code-block:: sls

            [idem_test_aws_apigatewayv2_authorizer]:
              aws.apigatewayv2.authorizer.present:
                - name: 'string'
                - api_id: 'string'
                - authorizer_type: 'REQUEST|JWT'
                - identity_source: ['string']
                - authorizer_credentials_arn: 'string'
                - authorizer_payload_format_version: 'string'
                - authorizer_result_ttl_in_seconds: 123
                - authorizer_uri: 'string'
                - enable_simple_responses: 'True|False'
                - jwt_configuration: {
                    'Audience': ['string'],
                    'Issuer': 'string'
                }

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_apigatewayv2_authorizer:
              aws.apigatewayv2.authorizer.present:
                - name: value
                - api_id: value
                - authorizer_type: value
                - identity_source: [value]
                - authorizer_credentials_arn: value
                - authorizer_payload_format_version: value
                - authorizer_result_ttl_in_seconds: value
                - authorizer_uri: value
                - enable_simple_responses: True|False
                - jwt_configuration: {
                    'Audience': [value],
                    'Issuer': value
                  }
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False

    if resource_id:
        before_ret = await hub.exec.aws.apigatewayv2.authorizer.get(
            ctx=ctx, name=name, resource_id=resource_id, api_id=api_id
        )
        if not before_ret["result"] or not before_ret["ret"]:
            result["result"] = False
            result["comment"] = before_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.apigatewayv2.authorizer", name=name
        )
        result["old_state"] = copy.deepcopy(before_ret["ret"])
        result["new_state"] = copy.deepcopy(result["old_state"])

        resource_parameters = {
            "authorizer_credentials_arn": authorizer_credentials_arn,
            "authorizer_payload_format_version": authorizer_payload_format_version,
            "authorizer_result_ttl_in_seconds": authorizer_result_ttl_in_seconds,
            "authorizer_type": authorizer_type,
            "authorizer_uri": authorizer_uri,
            "enable_simple_responses": enable_simple_responses,
            "identity_source": identity_source,
            "jwt_configuration": jwt_configuration,
        }

        update_authorizer_ret = await hub.tool.aws.apigatewayv2.authorizer.update(
            ctx,
            api_id=api_id,
            resource_id=resource_id,
            raw_resource=before_ret.get("ret"),
            resource_parameters=resource_parameters,
        )
        result["comment"] += update_authorizer_ret["comment"]
        if not update_authorizer_ret["result"]:
            result["result"] = False
            return result

        resource_updated = resource_updated or bool(update_authorizer_ret["ret"])
        if update_authorizer_ret["ret"] and ctx.get("test", False):
            result["new_state"].update(update_authorizer_ret["ret"])

        if resource_updated and ctx.get("test", False):
            return result
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "api_id": api_id,
                    "authorizer_credentials_arn": authorizer_credentials_arn,
                    "authorizer_payload_format_version": authorizer_payload_format_version,
                    "authorizer_result_ttl_in_seconds": authorizer_result_ttl_in_seconds,
                    "authorizer_type": authorizer_type,
                    "authorizer_uri": authorizer_uri,
                    "enable_simple_responses": enable_simple_responses,
                    "identity_source": identity_source,
                    "jwt_configuration": jwt_configuration,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.apigatewayv2.authorizer", name=name
            )
            return result

        create_ret = await hub.exec.boto3.client.apigatewayv2.create_authorizer(
            ctx,
            ApiId=api_id,
            AuthorizerCredentialsArn=authorizer_credentials_arn,
            AuthorizerPayloadFormatVersion=authorizer_payload_format_version,
            AuthorizerResultTtlInSeconds=authorizer_result_ttl_in_seconds,
            AuthorizerType=authorizer_type,
            AuthorizerUri=authorizer_uri,
            EnableSimpleResponses=enable_simple_responses,
            IdentitySource=identity_source,
            JwtConfiguration=jwt_configuration,
            Name=name,
        )
        if not create_ret["result"]:
            result["result"] = False
            result["comment"] = create_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.apigatewayv2.authorizer", name=name
        )
        resource_id = create_ret["ret"]["AuthorizerId"]

    if (not result["old_state"]) or resource_updated:
        after_ret = await hub.exec.aws.apigatewayv2.authorizer.get(
            ctx=ctx, name=name, api_id=api_id, resource_id=resource_id
        )
        if not after_ret["result"]:
            result["result"] = False
            result["comment"] += after_ret["comment"]
            return result

        result["new_state"] = after_ret["ret"]

    return result


async def absent(
    hub, ctx, name: str, api_id: str, resource_id: str = None
) -> Dict[str, Any]:
    """Deletes an API Gateway v2 authorizer resource.

    Args:
        name(str): An Idem name of the resource.
        api_id(str): The API resource identifier in Amazon Web Services.
        resource_id(str, Optional): The Authorizer resource identifier in Amazon Web Services.
            Idem automatically considers this resource being absent if this field is not specified.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_apigatewayv2_authorizer:
              aws.apigatewayv2.authorizer.absent:
                - name: value
                - api_id: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.apigatewayv2.authorizer", name=name
        )
        return result

    before_ret = await hub.exec.aws.apigatewayv2.authorizer.get(
        ctx=ctx, name=name, api_id=api_id, resource_id=resource_id
    )
    if not before_ret["result"]:
        result["result"] = False
        result["comment"] = before_ret["comment"]
        return result
    if not before_ret["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.apigatewayv2.authorizer", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before_ret["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.apigatewayv2.authorizer", name=name
        )
    else:
        result["old_state"] = before_ret["ret"]
        delete_ret = await hub.exec.boto3.client.apigatewayv2.delete_authorizer(
            ctx, ApiId=api_id, AuthorizerId=resource_id
        )
        if not delete_ret["result"]:
            result["result"] = False
            result["comment"] = delete_ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.apigatewayv2.authorizer", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Gets the API Gateway v2 authorized resources for an AWS account.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.apigatewayv2.authorizer
    """
    result = {}

    get_apis_ret = await hub.exec.boto3.client.apigatewayv2.get_apis(ctx)
    if not get_apis_ret["result"]:
        hub.log.warning(f"Could not get apis {get_apis_ret['comment']}")
        return result

    for api in get_apis_ret["ret"]["Items"]:
        api_id = api.get("ApiId")

        get_authorizers_ret = await hub.exec.boto3.client.apigatewayv2.get_authorizers(
            ctx, ApiId=api_id
        )
        if not get_authorizers_ret["result"]:
            hub.log.debug(
                f"Could not get authorizers for ApiId '{api_id}': "
                f"{get_authorizers_ret['comment']}. Describe will skip this api and continue."
            )
            continue

        for authorizer in get_authorizers_ret["ret"]["Items"]:
            resource_translated = (
                hub.tool.aws.apigatewayv2.authorizer.convert_raw_authorizer_to_present(
                    api_id=api_id,
                    raw_resource=authorizer,
                )
            )

            result[resource_translated["resource_id"]] = {
                "aws.apigatewayv2.authorizer.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource_translated.items()
                ]
            }

    return result
