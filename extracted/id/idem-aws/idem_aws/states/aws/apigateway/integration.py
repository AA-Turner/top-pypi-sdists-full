import copy

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    rest_api_id: str,
    parent_resource_id: str,
    http_method: str,
    input_type: str,
    resource_id: str = None,
    cache_namespace: str = None,
    cache_key_parameters: list = None,
    integration_responses: dict = None,
    timeout_in_millis: int = None,
    passthrough_behavior: str = None,
    connection_id: str = None,
    integration_http_method: str = None,
    uri: str = None,
):
    """
    Creates a new API Gateway Integration or modifies an existing one.

    Args:
        name(str):
            An idem name of the resource.

        rest_api_id(str):
            AWS rest_api id of the associated RestApi.

        parent_resource_id(str):
            The parent resource's id.

        http_method(str):
            String that specifies the method request's HTTP method type.

        input_type(str):
            Specifies a put integration input's type.

        resource_id(str, Optional):
            Idem resource id, formatted as: rest_api_id-parent_resource_id-http_method. Defaults to None.

        cache_namespace(str, Optional):
            Specifies a group of related cached parameters. By default, API Gateway uses
            the resource ID as the cacheNamespace . You can specify the same cacheNamespace across resources to return
            the same cached data for requests to different resources.

        cache_key_parameters(list, Optional):
            A list of request parameters whose values API Gateway caches. To be valid
            values for cacheKeyParameters , these parameters must also be specified for Method requestParameters.

        timeout_in_millis(int, Optional):
            Custom timeout between 50 and 29,000 milliseconds. The default value is 29,000 milliseconds or 29 seconds.

        passthrough_behavior:
            Custom timeout between 50 and 29,000 milliseconds. The default value is
            29,000 milliseconds or 29 seconds.

        connection_id(str, Optional):
            The ID of the VpcLink used for the integration. Specify this value only if you specify VPC_LINK as the
            connection type.

        integration_responses(dict, Optional):
            Specifies the integration's responses. The status code must map to an existing MethodResponse,
            and parameters and templates can be used to transform the back-end response.

        integration_http_method(string, Optional):
            The HTTP method for the integration.

        uri(string, Optional):
            Specifies Uniform Resource Identifier (URI) of the integration endpoint. For HTTP or HTTP_PROXY integrations, the URI must be a fully formed,
            encoded HTTP(S) URL according to the RFC-3986 specification, for either standard integration, where connectionType is not VPC_LINK ,
            or private integration, where connectionType is VPC_LINK . For a private HTTP integration, the URI is not used for routing.
            For AWS or AWS_PROXY integrations, the URI is of the form arn:aws:apigateway:{region}:{subdomain.service|service}:path|action/{service_api }.
            Here, {Region} is the API Gateway region (e.g., us-east-1); {service} is the name of the integrated Amazon Web Services service (e.g., s3);
            and {subdomain} is a designated subdomain supported by certain Amazon Web Services service for fast host-name lookup. action can be used for
            an Amazon Web Services service action-based API, using an Action={name}&{p1}={v1}&p2={v2}... query string.
            The ensuing {service_api} refers to a supported action {name} plus any required input parameters. Alternatively, path can be used for an
            Amazon Web Services service path-based API. The ensuing service_api refers to the path to an Amazon Web Services service resource,
            including the region of the integrated Amazon Web Services service, if applicable. For example, for integration with the S3 API of GetObject ,
            the uri can be either arn:aws:apigateway:us-west-2:s3:action/GetObject&Bucket={bucket}&Key={key} or arn:aws:apigateway:us-west-2:s3:path/{bucket}/{key} .

    Request Syntax:
        [idem_test_aws_apigateway_integration]:
          aws.apigateway.integration.present:
            - name: 'string'
            - rest_api_id: 'string'
            - parent_resource_id: 'string'
            - http_method: 'string'
            - input_type: 'string'

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_apigateway_integration:
              aws.apigateway.integration.present:
                - name: test_integration
                - rest_api_id: ${aws.apigateway.rest_api:idem_test_aws_apigateway_rest_api:resource_id}
                - parent_resource_id: ${aws.apigateway.rest_api:test_rest_api:root_resource_id}
                - http_method: ${aws.apigateway.method:test_method:http_method}
                - input_type: MOCK

            idem_test_aws_apigateway_method:
              aws.apigateway.method.present:
                - name: test_method
                - rest_api_id: ${aws.apigateway.rest_api:idem_test_aws_apigateway_rest_api:resource_id}
                - parent_resource_id: ${aws.apigateway.rest_api:idem_test_aws_apigateway_rest_api:root_resource_id}
                - http_method: GET
                - authorization_type: AWS_IAM

            idem_test_aws_apigateway_rest_api:
              aws.apigateway.rest_api.present:
                - name: test_rest_api

        Above, note that the integration's http_method is ``${aws.apigateway.method:test_method:http_method}``.
        This evaluates to ``GET``, plus an implicit ``require`` of the resource. You could also set it to ``GET``
        explicitly, and use an explicit ``require``:

        .. code-block:: sls

            idem_test_aws_apigateway_integration:
              aws.apigateway.integration.present:
                - require:
                    - aws.apigateway.method: test_method
                - http_method: GET
                ...

        .. code-block:: sls

            [idem_test_aws_apigateway_integration]:
              aws.apigateway.integration.present:
                - name: 'string'
                - rest_api_id: 'string'
                - parent_resource_id: 'string'
                - http_method: 'string'
                - input_type: 'string'

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False

    if resource_id:
        before = await hub.exec.aws.apigateway.integration.get(
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
            "cache_namespace": cache_namespace,
            "cache_key_parameters": cache_key_parameters,
            "integration_responses": integration_responses,
            "input_type": input_type,
            "timeout_in_millis": timeout_in_millis,
            "passthrough_behavior": passthrough_behavior,
            "connection_id": connection_id,
            "uri": uri,
        }

        update_ret = await hub.tool.aws.apigateway.integration.update(
            ctx,
            old_state=result["old_state"],
            updatable_parameters=update_parameters,
        )

        if not update_ret["result"]:
            result["result"] = False
            result["comment"] = update_ret["comment"]
            return result
        result["comment"] += update_ret["comment"]
        resource_updated = bool(update_ret["ret"])

        if resource_updated and ctx.get("test", False):
            result["new_state"].update(update_ret["ret"])

        if resource_updated:
            if ctx.get("test", False):
                result["comment"] = result[
                    "comment"
                ] + hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.apigateway.integration", name=name
                )
                return result

    else:
        resource_id = f"{rest_api_id}-{parent_resource_id}-{http_method}"

        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "rest_api_id": rest_api_id,
                    "resource_id": resource_id,
                    "parent_resource_id": parent_resource_id,
                    "http_method": http_method,
                    "passthrough_behavior": passthrough_behavior,
                    "timeout_in_millis": timeout_in_millis,
                    "cache_namespace": cache_namespace,
                    "cache_key_parameters": cache_key_parameters,
                    "integration_responses": integration_responses,
                    "connection_id": connection_id,
                    "input_type": input_type,
                    "integration_http_method": integration_http_method,
                    "uri": uri,
                },
            )

            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.apigateway.integration", name=name
            )
            return result

        ret = await hub.exec.boto3.client.apigateway.put_integration(
            ctx,
            restApiId=rest_api_id,
            resourceId=parent_resource_id,
            httpMethod=http_method,
            type=input_type,
            cacheNamespace=cache_namespace,
            cacheKeyParameters=cache_key_parameters,
            timeoutInMillis=timeout_in_millis,
            passthroughBehavior=passthrough_behavior,
            connectionId=connection_id,
            integrationHttpMethod=integration_http_method,
            uri=uri,
        )

        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.apigateway.integration", name=name
        )
    if (not before) or resource_updated:
        after = await hub.exec.aws.apigateway.integration.get(
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
):
    """
    Deletes an API Gateway Integration.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            Idem resource id, formatted as: rest_api_id-parent_resource_id-http_method. Defaults to None.
            Idem automatically considers this resource being absent if this field is not specified.

    Examples:

        .. code-block:: sls

            idem_test_aws_apigateway_integration:
              aws.apigateway.integration.absent:
                - name: value
                - resource_id: value

    Returns:
        dict[str, Any]
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.apigateway.integration", name=name
        )
        return result

    before_ret = await hub.exec.aws.apigateway.integration.get(
        ctx, name=name, resource_id=resource_id
    )

    if not before_ret["result"]:
        result["result"] = False
        result["comment"] = before_ret["comment"]

    if not before_ret["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.apigateway.integration", name=name
        )
        return result

    elif ctx.get("test", False):
        result["old_state"] = before_ret["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.apigateway.integration", name=name
        )
        return result

    else:
        rest_api_id, parent_resource_id, http_method = resource_id.split("-")
        result["old_state"] = before_ret["ret"]
        delete_ret = await hub.exec.boto3.client.apigateway.delete_integration(
            ctx,
            restApiId=rest_api_id,
            resourceId=parent_resource_id,
            httpMethod=http_method,
        )

        if not delete_ret["result"]:
            result["result"] = False
            result["comment"] = delete_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.apigateway.integration", name=name
        )
        return result


async def describe(hub, ctx):
    """
    Describe the API Gateway Integrations.

    Returns a list of apigateway.integration descriptions

    Returns:
        dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe aws.apigateway.integration
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
            f"Could not get Resources {get_resources_ret['comment']}. Will skip this Resource."
            continue

        if get_resources_ret["ret"]["items"] is not None:
            for resource in get_resources_ret["ret"]["items"]:
                parent_resource_id = resource.get("id")
                if resource.get("resourceMethods") is not None:
                    for resource_method in resource.get("resourceMethods"):
                        method_resource_id = (
                            f"{rest_api_id}-{parent_resource_id}-{resource_method}"
                        )

                        integration = await hub.exec.aws.apigateway.integration.get(
                            ctx,
                            resource_id=method_resource_id,
                        )

                        if not integration["ret"]:
                            hub.log.debug(
                                f"Could not get Integration {integration['comment']}. Will skip this Integration."
                            )
                            continue

                        resource_translated = integration["ret"]
                        result[resource_translated["resource_id"]] = {
                            "aws.apigateway.integration.present": [
                                {parameter_key: parameter_value}
                                for parameter_key, parameter_value in resource_translated.items()
                            ]
                        }

    return result
