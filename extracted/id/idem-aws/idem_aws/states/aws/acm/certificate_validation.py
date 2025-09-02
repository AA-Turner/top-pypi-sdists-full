"""States module for managing ACM certificate validations."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]
AMAZON = "Amazon"
DNS = "DNS"
EMAIL = "EMAIL"
ISSUED = "ISSUED"


async def present(
    hub,
    ctx,
    name: str,
    certificate_arn: str = None,
    resource_id: str = None,
    validation_record_fqdns: List[str] = None,
    timeout: make_dataclass(
        "Timeout",
        [
            (
                "describe",
                make_dataclass(
                    "CreateTimeout",
                    [
                        ("delay", int, field(default=None)),
                        ("max_attempts", int, field(default=None)),
                    ],
                ),
                field(default=None),
            )
        ],
    ) = None,
) -> Dict[str, Any]:
    """Validate ACM Certificate.

    Before the Amazon certificate authority (CA) can issue a certificate for your site, AWS Certificate Manager (ACM)
    must prove that you own or control all of the domain names that you specify in your request. You can choose to prove
    your ownership with either Domain Name System (DNS) validation or with email validation at the time you request a
    certificate. In case of email validation, manual email approval of ACM certificate is required. Validation applies
    only to publicly trusted certificates issued by ACM. ACM does not validate domain ownership for imported certificates
    or for certificates signed by a private CA.

    Args:
        name(str):
            An Idem name of the resource.

        certificate_arn(str, Optional):
            The Amazon Resource Name (ARN) of certificate. Either certificate_arn or resource_id is required.

        resource_id(str, Optional):
            The Amazon Resource Name (ARN) of certificate to identify the resource. Either certificate_arn or resource_id is required.

        validation_record_fqdns(list[str], Optional):
            List of FQDNs that implement the validation. Only valid for DNS validation method ACM certificates.
            If this is set, the resource can implement additional sanity checks and has an explicit dependency
            on the resource that is implementing the validation.

        timeout(dict[str, Any], Optional):
            Timeout configuration for waiting for Aws Certificate to get issued.

            * describe (dict[str, Any])
                Timeout configuration for describing certificate

                * delay (int, Optional):
                    The amount of time in seconds to wait between attempts.

                * max_attempts (int, Optional):
                    Customized timeout configuration containing delay and max attempts.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

          [certificate-validation-resource-id]:
            aws.acm.certificate_validation.present:
            - certificate_arn: arn:aws:acm:eu-west-2:sample_arn
            - resource_id: arn:aws:acm:eu-west-2:sample_arn
            - validation_record_fqdns:
              - abc.dp.example.net.
              - abc2.testing.example.net.
            - timeout:
              describe:
                delay: 10
                max_attempts: 20
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = await hub.exec.boto3.client.acm.describe_certificate(
        ctx, CertificateArn=resource_id if resource_id else certificate_arn
    )
    if not (before and before["result"]):
        hub.log.debug(before["comment"])
        result["comment"] = before["comment"]
        result["result"] = False
        return result
    elif not before["ret"]:
        hub.log.debug(
            f"Error describing AWS Certificate {certificate_arn}: empty output"
        )
        result["comment"] += [
            f"Error describing AWS Certificate {certificate_arn}: empty output"
        ]
        return result
    else:
        old_certificate = before["ret"].get("Certificate")
        result["old_state"] = {
            "certificate_arn": old_certificate.get("CertificateArn"),
            "status": old_certificate.get("Status"),
        }
        if old_certificate.get("Status") == ISSUED and old_certificate.get("IssuedAt"):
            result["old_state"]["issued_at"] = old_certificate.get("IssuedAt").strftime(
                "%m/%d/%Y %H:%M:%S"
            )
            result["new_state"] = copy.deepcopy(result["old_state"])
            result["comment"] += [
                f"Certificate '{certificate_arn}' issued at {old_certificate.get('IssuedAt')}"
            ]
            return result

        # Check Issuer
        if old_certificate.get("Issuer") != AMAZON:
            hub.log.debug(
                f"Certificate '{certificate_arn}' is not Amazon issued, no validation necessary"
            )
            result["comment"] = (
                f"Certificate '{certificate_arn}' is not Amazon issued, no validation necessary",
            )
            result["result"] = False
            return result

        # Check Validation method
        validation_method = (
            hub.tool.aws.acm.certificate_validation_utils.extract_validation_method(
                old_certificate
            )
        )
        if validation_method != DNS:
            hub.log.debug(
                "aws.acm.certificate_validation is only valid for DNS validation"
            )
            result["comment"] += [
                "aws.acm.certificate_validation is only valid for DNS validation"
            ]
            result["result"] = False
            return result

        if validation_record_fqdns:
            validity_of_domain = (
                hub.tool.aws.acm.certificate_validation_utils.validation_rec(
                    validation_rec_fqdns=validation_record_fqdns,
                    certificate=old_certificate,
                )
            )
            if not validity_of_domain["result"]:
                result["comment"] += validity_of_domain["comment"]
                result["result"] = False
                return result

        waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
            default_delay=60,
            default_max_attempts=40,
            timeout_config=timeout.get("describe") if timeout else None,
        )
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "acm",
                "certificate_validated",
                CertificateArn=certificate_arn,
                WaiterConfig=waiter_config,
            )
        except Exception as e:
            result["comment"] += [str(e)]
            result["result"] = False

        after = await hub.exec.boto3.client.acm.describe_certificate(
            ctx, CertificateArn=certificate_arn
        )
        after_certificate = after["ret"].get("Certificate")
        result["new_state"] = {
            "certificate_arn": after_certificate.get("CertificateArn"),
            "status": after_certificate.get("Status"),
        }
        if after_certificate.get("Status") != ISSUED:
            hub.log.debug(
                f"Certificate '{certificate_arn}' not issued. It is in {after_certificate.get('Status')} state"
            )
            result["comment"] += [
                f"Certificate '{certificate_arn}' not issued It is in {after_certificate.get('Status')} state"
            ]
            result["result"] = True
            return result

        result["new_state"]["issued_at"] = after_certificate.get("IssuedAt").strftime(
            "%m/%d/%Y %H:%M:%S"
        )
        result["comment"] += [
            f"Certificate '{certificate_arn}' issued at {after_certificate.get('IssuedAt')}"
        ]
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """A No-Op function for certificate_validation.

    This is a configuration resource of the certificate_manager resource.
    It's not possible to delete certificate_validations,
    You can delete a certificate_manager resource by calling certificate_manager.absent,
    while providing the certificate_manager id.

    Args:
        name:
            The name of the resource.

        resource_id(str, Optional):
            The Amazon Resource Name (ARN) of certificate to identify the resource. Either certificate_arn or resource_id is required.

    Request Syntax:
        .. code-block:: sls

            [certificate-validation-resource-id]:
              aws.acm.certificate_validation.absent:
                - name: "string"

    Returns:
        Dict[str, Any]
    """
    result = dict(
        comment=(
            "No-Op: The certificate validation can not be deleted as it is not an AWS resource",
        ),
        old_state=None,
        new_state=None,
        name=name,
        result=True,
    )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns detailed metadata about ACM certificates required for certificates validations.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.acm.certificate_validation
    """
    result = {}
    certificate_list_ret = await hub.exec.boto3.client.acm.list_certificates(
        ctx,
        Includes={
            "keyTypes": [
                "RSA_1024",
                "RSA_2048",
                "RSA_3072",
                "RSA_4096",
                "EC_prime256v1",
                "EC_secp384r1",
                "EC_secp521r1",
            ]
        },
    )
    if not certificate_list_ret["result"]:
        hub.log.debug(
            f"Could not list AWS Certificates {certificate_list_ret['comment']}"
        )
        return {}
    certificate_list = certificate_list_ret["ret"].get("CertificateSummaryList")

    for certificate in certificate_list:
        resource_id = certificate.get("CertificateArn")
        ret = await hub.exec.boto3.client.acm.describe_certificate(
            ctx, CertificateArn=resource_id
        )
        if not ret["result"]:
            hub.log.warning(
                f"Could not describe AWS Certificate '{resource_id}' {ret['comment']}"
            )
            continue

        resource = ret["ret"].get("Certificate")

        convert_ret = (
            hub.tool.aws.acm.conversion_utils.convert_raw_acm_validation_to_present(
                raw_resource=resource,
                idem_resource_name=resource_id,
            )
        )
        resource_translated = convert_ret.get("ret")
        result[resource_id] = {
            "aws.acm.certificate_validation.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result
