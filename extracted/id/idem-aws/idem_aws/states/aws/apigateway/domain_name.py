"""State module for managing AWS Api Gateway Domain Name."""
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
    certificate_name: str = None,
    certificate_arn: str = None,
    regional_certificate_name: str = None,
    regional_certificate_arn: str = None,
    resource_id: str = None,
    endpoint_configuration: make_dataclass(
        "endpointConfigurationInput",
        [
            ("types", List[str], field(default=None)),
            ("vpcEndpointIds", List[str], field(default=None)),
        ],
    ) = None,
    mutual_tls_authentication: make_dataclass(
        "MutualTlsAuthenticationInput",
        [
            ("TruststoreUri", str, field(default=None)),
            ("TruststoreVersion", str, field(default=None)),
        ],
    ) = None,
    security_policy: str = None,
    tags: Dict[str, str] = None,
    timeout: make_dataclass(
        "Timeout",
        [
            (
                "update",
                make_dataclass(
                    "UpdateTimeout",
                    [
                        ("delay", int, field(default=30)),
                        ("max_attempts", int, field(default=60)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
) -> Dict[str, Any]:
    """Creates or updates the apigateway domain name resource.

    Args:
        name(str):
            The name of the DomainName resource
        certificate_name(str, Optional):
            The user-friendly name of the certificate that will be used
            by edge-optimized endpoint for this domain name.
        certificate_arn(str, Optional):
            The reference to an AWS-managed certificate that will be used by
            edge-optimized endpoint for this domain name. AWS Certificate Manager is
            the only supported source.
        regional_certificate_name(str, Optional):
            The user-friendly name of the certificate that will be used by regional
            endpoint for this domain name.
        regional_certificate_arn(str, Optional):
            The reference to an AWS-managed certificate that will be used by regional
            endpoint for this domain name. AWS Certificate Manager is the only supported source.
        resource_id(str, Optional):
            idem required name for the AWS API Gateway domain
        endpoint_configuration(dict, Optional):
            The endpoint configuration of this DomainName showing the endpoint types of
            the domain name.
            - types(list, Optional):
                A list of endpoint types of an API (RestApi) or its custom domain name
                (DomainName). For an edge-optimized API and its custom domain name, the
                endpoint type is "EDGE" . For a regional API and its custom domain name,
                the endpoint type is REGIONAL . For a private API, the endpoint type
                is PRIVATE .
                string) -- The endpoint type. The valid values are EDGE for edge-optimized
                API setup, most suitable for mobile applications; REGIONAL for regional API
                endpoint setup, most suitable for calling from AWS Region; and PRIVATE
                for private APIs.
            - vpcEndpointIds (list, Optional):
                A list of VpcEndpointIds of an API (RestApi) against which to create Route53
                ALIASes. It is only supported for PRIVATE endpoint type.
        mutual_tls_authentication(dict, Optional):
            The mutual TLS authentication configuration for a custom domain name. If specified,
            API Gateway performs two-way authentication between the client and the server.
            Clients must present a trusted certificate to access your API.
            - TruststoreUri(str, Optional)--
                An Amazon S3 URL that specifies the truststore for mutual TLS authentication,
                for example s3://bucket-name/key-name . The truststore can contain certificates
                from public or private certificate authorities. To update the truststore,
                upload a new version to S3, and then update your custom domain name to use the
                new version. To update the truststore, you must have permissions to access the S3 object.
            - TruststoreVersion(str, Optional):
                The version of the S3 object that contains your truststore. To specify a version,
                you must have versioning enabled for the S3 bucket
        security_policy(str, Optional):
            The Transport Layer Security (TLS) version + cipher suite for this DomainName.
            The valid values are TLS_1_0 and TLS_1_2
        tags(dict, Optional):
            The key-value map of strings. The valid character set is [a-zA-Z+-=._:/]. The tag key can
            be up to 128 characters and must not start with aws: . The tag value can be up to 256 characters.
        Timeout configuration for create/update of AWS ApiGateway Domain Name
                * update(dict, Optional):
                    Timeout configuration for updating AWS ApiGateway Domain Name
                        * delay(int, Optional): The amount of time in seconds to wait between attempts. Default value is ``15``.
                        * max_attempts(int, Optional): Customized timeout configuration containing delay and max attempts. Default value is ``40``.
    Request Syntax:
        .. code-block:: sls

             idem-test.idem-jedi-test.com:
              aws.apigateway.domain_name.present:
              - domain_name: string
              - regional_certificate_name: string
              - regional_certificate_arn: string
              - security_policy: string
              - endpoint_configuration: dict

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls

            idem-test.idem-jedi-test.com:
              aws.apigateway.domain_name.present:
              - domain_name: idem-test.idem-jedi-test.com
              - regional_certificate_arn: arn:aws:acm:us-west-2:746014882121:certificate/bb79ca7e-0fd0-485b-a977-cf96ba19f62c
              - security_policy: TLS_1_2
              - endpoint_configuration:
                  types:
                  - REGIONAL
              - tags:
                  -Key: 'idem-resource-name'
                   Value: 'idem-fixture-acm07f548a9-ad28-4b73-bc17-28559c357784.example.com'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False
    before_ret = None
    if resource_id:
        before_ret = await hub.exec.aws.apigateway.domain_name.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not before_ret["result"] or not before_ret["ret"]:
            result["result"] = False
            result["comment"] = before_ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.apigateway.domain_name", name=name
        )
        result["old_state"] = before_ret["ret"]
        result["new_state"] = copy.deepcopy(result["old_state"])
        resource_arn = hub.tool.aws.arn_utils.build(
            service="apigateway",
            region=ctx["acct"]["region_name"],
            resource="/domainnames/" + resource_id,
        )
        update_parameters = {
            "certificate_name": certificate_name,
            "certificate_arn": certificate_arn,
            "endpoint_configuration": endpoint_configuration,
            "mutual_tls_authentication_input": mutual_tls_authentication,
            "regional_certificate_name": regional_certificate_name,
            "regional_certificate_arn": regional_certificate_arn,
            "security_policy": security_policy,
        }
        update_domain_name = await hub.tool.aws.apigateway.domain_name.update(
            ctx,
            name=name,
            old_state=result["old_state"],
            updatable_parameters=update_parameters,
        )
        if not update_domain_name["result"]:
            result["result"] = False
            result["comment"] = update_domain_name["comment"]
            return result
        result["comment"] += update_domain_name["comment"]
        resource_updated = bool(update_domain_name["ret"])
        if resource_updated and ctx.get("test", False):
            result["new_state"].update(update_domain_name["ret"])
        if tags is not None and tags != result["old_state"].get("tags", {}):
            update_tags_ret = await hub.tool.aws.apigateway.tag.update(
                ctx,
                resource_arn=resource_arn,
                old_tags=result["old_state"].get("tags", {}),
                new_tags=tags,
            )
            if not update_tags_ret["result"]:
                result["result"] = False
                result["comment"] = update_tags_ret["comment"]
                return result
            result["comment"] += update_tags_ret["comment"]
            resource_updated = resource_updated or bool(update_tags_ret["ret"])
            if update_tags_ret["ret"] and ctx.get("test", False):
                result["new_state"]["tags"] = update_tags_ret["ret"]
        if resource_updated:
            if ctx.get("test", False):
                result["comment"] = result[
                    "comment"
                ] + hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.apigateway.domain_name", name=name
                )
                result["new_state"] = update_parameters
                result["new_state"]["domain_name"] = name
                result["new_state"]["resource_id"] = name
                result["new_state"]["tags"] = tags
                return result
            else:
                result["comment"] = result[
                    "comment"
                ] + hub.tool.aws.comment_utils.update_comment(
                    resource_type="aws.apigateway.domain_name", name=name
                )
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "regional_certificate_name": regional_certificate_name,
                    "regional_certificate_arn": regional_certificate_arn,
                    "endpoint_configuration": endpoint_configuration,
                    "certificate_name": certificate_name,
                    "certificate_arn": certificate_arn,
                    "security_policy": security_policy,
                    "tags": tags,
                    "mutual_tls_authentication": mutual_tls_authentication,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.apigateway.domain_name", name=name
            )
            return result
        else:
            response = await hub.exec.boto3.client.apigateway.create_domain_name(
                ctx,
                domainName=name,
                regionalCertificateName=regional_certificate_name,
                regionalCertificateArn=regional_certificate_arn,
                certificateName=certificate_name,
                certificateArn=certificate_arn,
                endpointConfiguration=endpoint_configuration,
                securityPolicy=security_policy,
                tags=tags,
                mutualTlsAuthentication=mutual_tls_authentication,
            )
            result["result"] = response["result"]
            if not response["result"]:
                result["comment"] = response["comment"]
                return result

            result["comment"] = hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.apigateway.domain_name", name=name
            )
            resource_id = name
    if (not before_ret) or resource_updated:
        after = await hub.exec.aws.apigateway.domain_name.get(
            ctx, name=name, resource_id=resource_id
        )
        if not (after["result"] and after["ret"]):
            result["result"] = False
            result["comment"] = after["comment"]
            return result
        result["new_state"] = after["ret"]
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    timeout: make_dataclass(
        """Specifies timeout for deletion of domain.""" "Timeout",
        [
            (
                "delete",
                make_dataclass(
                    "DeleteTimeout",
                    [
                        ("delay", int, field(default=40)),
                        ("max_attempts", int, field(default=60)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
) -> Dict[str, Any]:
    """Deletes an API Gateway domain name resource.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            AWS API Gateway domain name. Idem automatically considers this
            resource being absent if this field is not specified.
        timeout(dict, Optional):
            Timeout configuration for AWS Elasticsearch domain
                * delete(dict, Optional):
                    Timeout configuration when deleting an AWS Elasticsearch domain
                        * delay(int, Optional) -- The amount of time in seconds to wait between attempts. Default value is ``40``.
                        * max_attempts(int, Optional) -- Max attempts of waiting for change. Default value is ``60``.

    Returns:
        Dict[str, Any]

    Request syntax:

        .. code-block:: sls

            idem_test_aws_apigateway_domain_name::
              aws.apigateway.domain_name.absent:
                - name: 'str'
                - resource_id: 'str'

    Examples:

        .. code-block:: sls

            idem-test.idem-jedi-test.com:
              aws.apigateway.domain_name.present:
              - name: idem-test.idem-jedi-test.com
              - resource_id: idem-test.idem-jedi-test.com
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.apigateway.domain_name", name=name
        )
        return result

    before_ret = await hub.exec.aws.apigateway.domain_name.get(
        ctx=ctx, name=name, resource_id=resource_id
    )
    if not before_ret["result"]:
        result["result"] = False
        result["comment"] = before_ret["comment"]
        return result
    if not before_ret["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.apigateway.domain_name", name=name
        )

    elif ctx.get("test", False):
        result["old_state"] = before_ret["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.apigateway.domain_name", name=name
        )
        return result
    else:
        result["old_state"] = before_ret["ret"]
        delete_ret = await hub.exec.boto3.client.apigateway.delete_domain_name(
            ctx, domainName=resource_id
        )
        if not delete_ret["result"]:
            result["result"] = False
            result["comment"] = delete_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.apigateway.domain_name", name=name
        )
        delete_waiter_acceptors = [
            {
                "matcher": "path",
                "expected": "AVAILABLE",
                "state": "retry",
                "argument": "domainNameStatus",
            },
            {
                "matcher": "path",
                "expected": "UPDATING",
                "state": "retry",
                "argument": "domainNameStatus",
            },
            {
                "matcher": "path",
                "expected": "PENDING",
                "state": "retry",
                "argument": "domainNameStatus",
            },
            {
                "matcher": "path",
                "expected": "PENDING_CERTIFICATE_REIMPORT",
                "state": "retry",
                "argument": "domainNameStatus",
            },
            {
                "matcher": "path",
                "expected": "PENDING_OWNERSHIP_VERIFICATION",
                "state": "retry",
                "argument": "domainNameStatus",
            },
            {
                "matcher": "error",
                "expected": "NotFoundException",
                "state": "success",
                "argument": "Error.Code",
            },
            {
                "matcher": "error",
                "expected": "BadRequestException",
                "state": "retry",
                "argument": "Error.Code",
            },
            {
                "matcher": "error",
                "expected": "UnauthorizedException",
                "state": "retry",
                "argument": "Error.Code",
            },
            {
                "matcher": "error",
                "expected": "TooManyRequestsException",
                "state": "retry",
                "argument": "Error.Code",
            },
        ]

        delete_waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
            default_delay=40,
            default_max_attempts=60,
            timeout_config=timeout.get("delete") if timeout else None,
        )
        delete_domain_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
            name="ApiGatewayDomainNameDelete",
            operation="GetDomainName",
            argument=["domainNameStatus"],
            acceptors=delete_waiter_acceptors,
            client=await hub.tool.boto3.client.get_client(ctx, "apigateway"),
        )
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "apigateway",
                "ApiGatewayDomainNameDelete",
                delete_domain_waiter,
                domainName=resource_id,
                WaiterConfig=delete_waiter_config,
            )
        except Exception as e:
            result["comment"] += [str(e)]
            result["result"] = False

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe all the API Gateway domain_name.

    Returns:
        Dict[str, Dict[str, Any]]

    Request Syntax:

        .. code-block:: sls

            $ idem describe aws.apigateway.domain_name
    """

    result = {}
    get_domain_names_ret = await hub.exec.aws.apigateway.domain_name.list(ctx)
    for domain_name in get_domain_names_ret["ret"]:
        domain_name["resource_id"]
        result[domain_name["resource_id"]] = {
            "aws.apigateway.domain_name.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in domain_name.items()
            ]
        }
    return result
