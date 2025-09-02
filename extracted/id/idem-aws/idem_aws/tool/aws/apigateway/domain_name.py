import copy
from collections import OrderedDict
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List


def convert_raw_domain_name_to_present(
    hub,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    resource_parameters = OrderedDict(
        {
            "domainName": "domain_name",
            "regionalDomainName": "regional_domain_name",
            "certificateName": "certificate_name",
            "certificateUploadDate": "certificate_upload_date",
            "certificateArn": "certificate_arn",
            "regionalHostedZoneId": "regional_hosted_zone_id",
            "securityPolicy": "security_policy",
            "domainNameStatus": "domain_name_status",
            "endpointConfiguration": "endpoint_configuration",
            "distributionHostedZoneId": "distribution_hosted_zone_id",
            "distributionDomainName": "distribution_domain_name",
            "regionalCertificateArn": "regional_certificate_arn",
            "domainNameStatus": "domain_name_status",
            "domainNameStatusMessage": "domain_name_status_message",
            "securityPolicy": "security_policy",
            "tags": "tags",
            "mutualTlsAuthentication": "mutual_tls_authentication",
            "ownershipVerificationCertificateArn": "ownership_verification_certificate_arn",
        }
    )
    resource_id = raw_resource.get("domainName")
    resource_translated = {
        "resource_id": resource_id,
    }
    if idem_resource_name:
        resource_translated["name"] = idem_resource_name
    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)
    return resource_translated


async def update(
    hub,
    ctx,
    name,
    old_state: Dict[str, Any],
    updatable_parameters: Dict[str, Any],
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
):
    """
    Updates an API Gateway domain_name.

    Args:
        name(str):
            Apigateway domain name
        old_state(dict):
            Previous state of the resource.
        updatable_parameters(dict):
            Parameters from SLS File.
        timeout(dict, Optional): Timeout configuration for updating AWS ApiGateway Domain Name.

    Returns:
        Dict[str, Any]
    """
    result = dict(comment=[], result=True, ret=None)
    patch_operations = []

    new_state = copy.deepcopy(old_state)
    to_be_updated = False
    resource_id = name

    for key, value in updatable_parameters.items():
        if key == "certificate_name":
            key_final = "certificateName"
        elif key == "certificate_arn":
            key_final = "certificateArn"
        elif key == "endpoint_configuration":
            key_final = "endpointConfiguration/types"
        elif key == "mutual_tls_authentication_input":
            key_final = "mutualTlsAuthentication"
        elif key == "regional_certificate_name":
            key_final = "regionalCertificateName"
        elif key == "regional_certificate_arn":
            key_final = "regionalCertificateArn"
        elif key == "security_policy":
            key_final = "securityPolicy"

        if (
            old_state.get(key) is not None
            and value is not None
            and value != old_state.get(key)
        ):
            patch_operations.append(
                {
                    "op": "replace",
                    "path": f"/{key_final}",
                    "value": str(value)
                    if not isinstance(value, List)
                    else ",".join(value),
                }
            )
            to_be_updated = True
        elif old_state.get(key) is None and value is not None:
            patch_operations.append(
                {
                    "op": "add",
                    "path": f"/{key_final}",
                    "value": str(value)
                    if not isinstance(value, List)
                    else ",".join(value),
                }
            )
            new_state[key] = value
            to_be_updated = True
    if ctx.get("test", False):
        if to_be_updated:
            result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.apigateway.domain_name", name=old_state["name"]
            )
            result["ret"] = new_state
        else:
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                resource_type="aws.apigateway.domain_name", name=old_state["name"]
            )
            return result

    if to_be_updated:
        update_ret = await hub.exec.boto3.client.apigateway.update_domain_name(
            ctx, domainName=name, patchOperations=patch_operations
        )
        result["comment"] = hub.tool.aws.comment_utils.update_comment(
            resource_type="aws.apigateway.domain_name", name=old_state["name"]
        )
        if not update_ret["result"]:
            result["result"] = False
            result["comment"] = update_ret["comment"]
        waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
            default_delay=15,
            default_max_attempts=40,
            timeout_config=timeout.get("update") if timeout else None,
        )
        update_waiter_acceptors = [
            {
                "matcher": "path",
                "expected": "AVAILABLE",
                "state": "success",
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
                "matcher": "path",
                "expected": "NotFoundException",
                "state": "retry",
                "argument": "Error.Code",
            },
            {
                "matcher": "path",
                "expected": "BadRequestException",
                "state": "retry",
                "argument": "Error.Code",
            },
            {
                "matcher": "path",
                "expected": "ConflictException",
                "state": "retry",
                "argument": "Error.Code",
            },
            {
                "matcher": "path",
                "expected": "LimitExceededException",
                "state": "retry",
                "argument": "Error.Code",
            },
            {
                "matcher": "error",
                "expected": "UnauthorizedException",
                "state": "failure",
                "argument": "Error.Code",
            },
            {
                "matcher": "error",
                "expected": "TooManyRequestsException",
                "state": "retry",
                "argument": "Error.Code",
            },
        ]
        update_domain_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
            name="ApiGatewayDomainNameUpdate",
            operation="GetDomainName",
            argument=["Error.Code", "domainNameStatus"],
            acceptors=update_waiter_acceptors,
            client=await hub.tool.boto3.client.get_client(ctx, "apigateway"),
        )
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "apigateway",
                "ApiGatewayDomainNameUpdate",
                update_domain_waiter,
                domainName=resource_id,
                WaiterConfig=waiter_config,
            )
        except Exception as e:
            result["comment"] += [str(e)]
            result["result"] = False

    return result
