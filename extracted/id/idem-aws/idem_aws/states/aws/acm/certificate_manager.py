"""States module for managing ACM certificates."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List


__contracts__ = ["resource"]
__reconcile_wait__ = {"static": {"wait_in_seconds": 60}}

acceptors = [
    {
        "matcher": "error",
        "expected": "ResourceNotFoundException",
        "state": "retry",
        "argument": "Error.Code",
    },
    {
        "matcher": "path",
        "expected": "ISSUED",
        "state": "success",
        "argument": "Certificate.Status",
    },
    {
        "matcher": "path",
        "expected": "PENDING_VALIDATION",
        "state": "success",
        "argument": "Certificate.Status",
    },
    {
        "matcher": "path",
        "expected": "FAILED",
        "state": "success",
        "argument": "Certificate.Status",
    },
    {
        "matcher": "path",
        "expected": "VALIDATION_TIMED_OUT",
        "state": "success",
        "argument": "Certificate.Status",
    },
    {
        "matcher": "path",
        "expected": "INACTIVE",
        "state": "success",
        "argument": "Certificate.Status",
    },
    {
        "matcher": "path",
        "expected": "EXPIRED",
        "state": "success",
        "argument": "Certificate.Status",
    },
    {
        "matcher": "path",
        "expected": "REVOKED",
        "state": "success",
        "argument": "Certificate.Status",
    },
]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    certificate: str = None,
    private_key: str = None,
    certificate_chain: str = None,
    domain_name: str = None,
    validation_method: str = None,
    subject_alternative_names: List[str] = None,
    idempotency_token: str = None,
    domain_validation_options: List[
        make_dataclass(
            "DomainValidationOption",
            [
                ("domain_name", str),
                ("validation_domain", str),
                ("validation_method", str, field(default=None)),
                (
                    "resource_record",
                    make_dataclass(
                        "ResourceRecord",
                        [
                            ("Name", str, field(default=None)),
                            ("Type", str, field(default=None)),
                            ("Value", str, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                ("validation_status", str, field(default=None)),
            ],
        )
    ] = None,
    options: make_dataclass(
        "CertificateOptions",
        [("CertificateTransparencyLoggingPreference", str, field(default=None))],
    ) = None,
    certificate_authority_arn: str = None,
    timeout: make_dataclass(
        "Timeout",
        [
            (
                "create",
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
    tags: Dict[str, Any]
    or List[
        make_dataclass(
            "Tag",
            [("Key", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
) -> Dict[str, Any]:
    """Manage SSL/TLS certificates for your AWS-based websites and applications.

    Imports a certificate into AWS Certificate Manager (ACM) to use with services that are integrated with ACM.

    Note that integrated services allow only certificate types and keys they support to be associated with their
    resources. Further, their support differs depending on whether the certificate is imported into IAM or into ACM.
    Requests an ACM certificate for use with other AWS services. To request an ACM certificate, you must specify a
    fully qualified domain name (FQDN) in the DomainName parameter. You can also specify additional FQDNs in the
    SubjectAlternativeNames parameter.

    If you are requesting a private certificate, domain validation is not required. If you are requesting a public
    certificate, each domain name that you specify must be validated to verify that you own or control the domain.
    You can use DNS validation or email validation.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            The Amazon Resource Name (ARN) of certificate to identify the resource.

        certificate(bytes, Optional):
            The certificate to import.

        private_key(bytes, Optional):
            The private key that matches the public key in the certificate.

        certificate_chain(bytes, Optional):
            The PEM encoded certificate chain.

        domain_name(str, Optional):
            Fully qualified domain name (FQDN), such as www.example.com, that you want to secure with an ACM certificate.

        validation_method(str, Optional):
            The method you want to use if you are requesting a public certificate to validate that you own or control domain.

        subject_alternative_names(list[str], Optional):
            Additional FQDNs to be included in the Subject Alternative Name extension of the ACM certificate.

        idempotency_token(str, Optional):
            Customer chosen string that can be used to distinguish between calls to RequestCertificate.

        domain_validation_options(list[dict[str, Any]], Optional):
            The domain name that you want ACM to use to send you emails so that you can validate domain ownership.

            Defaults to None.

            * domain_name (str):
                A fully qualified domain name (FQDN) in the certificate request.

            * validation_domain (str):
                The domain name that you want ACM to use to send you validation emails. This domain name is the
                suffix of the email addresses that you want ACM to use. This must be the same as the DomainName
                value or a superdomain of the DomainName value.

                For example, if you request a certificate for testing.example.com, you can specify example.com for this value.
                In that case, ACM sends domain validation emails to the following five addresses:
                admin@example.com, administrator@example.com, hostmaster@example.com, postmaster@example.com, webmaster@example.com

            * validation_method (str):
                Specifies the domain validation method.

            * resource_record (dict[str, Any]):
                Contains the CNAME record that you add to your DNS database for domain validation.

                * Name (str):
                    The name of the DNS record to create in your domain. This is supplied by ACM.

                * Type (str):
                    The type of DNS record. Currently this can be CNAME.

                * Value (str):
                    The value of the CNAME record to add to your DNS database. This is supplied by ACM.

            * validation_status (str):
                The validation status of the domain name.
                This can be one of the following values:

                    * PENDING_VALIDATION
                    * SUCCESS
                    * FAILED

        options(dict[str, Any], Optional):
            Currently, you can use this parameter to specify whether to add the certificate to a certificate
            transparency log. Certificate transparency makes it possible to detect SSL/TLS certificates that
            have been mistakenly or maliciously issued. Certificates that have not been logged typically
            produce an error message in a browser. For more information, see Opting Out of Certificate
            Transparency Logging. Defaults to None.

            * CertificateTransparencyLoggingPreference (str, Optional):
                You can opt out of certificate transparency logging by specifying the DISABLED option. Opt in by specifying ENABLED.

        certificate_authority_arn(str, Optional):
            The Amazon Resource Name (ARN) of the private certificate authority (CA) that will be used to issue the certificate.

        tags(dict[str, str], Optional):
            The collection of tags associated with the certificate. Defaults to None.

            * Key (str):
                The key of the tag.

            * Value (str):
                The value of the tag.

        timeout(dict[str, Any], Optional):
            Timeout configuration for request/import AWS Certificate.

            * create(dict[str, int]:
                Timeout configuration for request/importing AWS Certificate.

                * delay (int, Optional):
                    The amount of time in seconds to wait between attempts.

                * max_attempts (int, Optional):
                    Customized timeout configuration containing delay and max attempts.

    Request Syntax:
        .. code-block:: sls

            [certificate-resource-id]:
              aws.acm.certificate_manager.present:
                - domain_name: 'string'
                - validation_method: 'string'
                - subject_alternative_names:
                  - 'string'
                - idempotency_token: 'string'
                - domain_validation_options:
                  - domain_name: 'string'
                    validation_domain: 'string'
                    validation_method: 'string'
                    resource_record:
                      Name: 'string'
                      Value: 'string'
                      Type: 'string'
                    validation_status: PENDING_VALIDATION|SUCCESS|FAILED
                - options:
                  CertificateTransparencyLoggingPreference: ENABLED|DISABLED
                - certificate_authority_arn: 'string'
                - tags:
                  - 'string': 'string'
                - timeout:
                  create:
                    delay: 'int'
                    max_attempts: 'int'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

          # Request a certificate
          [certificate-resource-id]:
            aws.acm.certificate_manager.present:
              - domain_name: www.example.com
              - validation_method: DNS
              - subject_alternative_names:
                  - www.example.net
              - idempotency_token: ExampleIdempotancyToken
              - domain_validation_options:
                - domain_name: testing.example.com
                  validation_domain: example.com
              - options:
                  CertificateTransparencyLoggingPreference: DISABLED
              - certificate_authority_arn: arn:aws:acm-pca:region:account:certificate-authority/12345678-1234-1234-1234-123456789012
              - tags:
                - class: test

          # Import a certificate
          [certificate-resource-id]:
            aws.acm.certificate_manager.present:
              - resource_id: arn:aws:acm-pca:region:account:certificate-authority/12345678-1234-1234-1234-123456789012
              - certificate_arn: arn:aws:acm-pca:region:account:certificate-authority/12345678-1234-1234-1234-123456789012
              - certificate: example_certificate
              - private_key: -----BEGIN RSA PRIVATE KEY-----
                  MIIEpQIBAAKCAQEA3Tz2mr7SZiAMfQyuvBjM9Oi..Z1BjP5CE/Wm/Rr500P
                  RK+Lh9x5eJPo5CAZ3/ANBE0sTK0ZsDGMak2m1g7..3VHqIxFTz0Ta1d+NAj
                  -----END RSA PRIVATE KEY-----
              - certificate_chain: example_certificate_chain
              - tags:
                - class: test
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None

    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    if resource_id:
        before = await hub.exec.aws.acm.certificate_manager.get(
            ctx,
            name=name,
            resource_id=resource_id,
        )

        if not before["result"] or not before["ret"]:
            result["comment"] = before["comment"]
            result["result"] = False
            return result

        result["old_state"] = copy.deepcopy(before["ret"])
        result["new_state"] = copy.deepcopy(result["old_state"])

        are_tags_updated = False
        is_reimported = False

        try:
            plan_state = copy.deepcopy(result["old_state"])

            # Reimport certificate if certificate arn,private key and certificate body is given as input
            # In Idem we cannot check if these properties are changed because they are not retrievable from other APIs
            # We cannot provide tags when reimporting a certificate.
            if private_key and certificate:
                re_imported = await hub.exec.boto3.client.acm.import_certificate(
                    ctx=ctx,
                    CertificateArn=resource_id,
                    Certificate=certificate,
                    PrivateKey=private_key,
                    CertificateChain=certificate_chain,
                )
                result["result"] = re_imported["result"]
                if not result["result"]:
                    result["comment"] = re_imported["comment"]
                    return result
                is_reimported = re_imported["result"]
                result["comment"] += [
                    f"Re-Imported aws.acm.certificate_manager '{name}'"
                ]
                if ctx.get("test", False) and is_reimported:
                    plan_state["private_key"] = private_key
                    plan_state["certificate"] = certificate
                    if certificate_chain:
                        plan_state["certificate_chain"] = certificate_chain
                    result["comment"] += [
                        f"Would reimport certificate for aws.acm.certificate_manager {name}"
                    ]
            if tags is not None and tags != result["old_state"].get("tags"):
                # Update tags
                update_tags_ret = await hub.tool.aws.acm.tag.update_tags(
                    ctx=ctx,
                    resource_id=resource_id,
                    old_tags=result["old_state"].get("tags"),
                    new_tags=tags,
                )
                if not update_tags_ret["result"]:
                    result["comment"] += update_tags_ret["comment"]
                    result["result"] = False
                    return result
                are_tags_updated = bool(update_tags_ret["ret"])
                if ctx.get("test", False) and are_tags_updated:
                    plan_state["tags"] = update_tags_ret["ret"]
                    result["comment"] += [
                        f"Would update tags for aws.acm.certificate_manager {name}"
                    ]
                elif are_tags_updated:
                    result["comment"] += [
                        f"Updated tags for aws.acm.certificate_manager '{name}'"
                    ]
            if not are_tags_updated and not is_reimported:
                result["comment"] += [
                    f"aws.acm.certificate_manager '{name}' has no property that needs to be updated"
                ]
        except Exception as e:
            result["comment"] += [str(e)]
            result["result"] = False
    else:
        # If private key is provided as an input then certificate needs to be imported
        # To import new certificate, CertificateArn should not be provided
        if private_key:
            try:
                if ctx.get("test", False):
                    result[
                        "new_state"
                    ] = hub.tool.aws.test_state_utils.generate_test_state(
                        enforced_state={},
                        desired_state={
                            "name": name,
                            "certificate": certificate,
                            "private_key": private_key,
                            "certificate_chain": certificate_chain,
                            "tags": tags,
                        },
                    )
                    result["comment"] += [
                        f"Would import aws.acm.certificate_manager {name}"
                    ]
                    return result
                imported = await hub.exec.boto3.client.acm.import_certificate(
                    ctx=ctx,
                    Certificate=certificate,
                    PrivateKey=private_key,
                    CertificateChain=certificate_chain,
                    Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                    if tags
                    else None,
                )
                result["result"] = imported["result"]
                if not result["result"]:
                    result["comment"] += imported["comment"]
                    return result

                resource_id = imported["ret"]["CertificateArn"]

                # Custom waiter for import
                # When the certificate is just created, there is a delay of several seconds before we can retrieve information about it.
                waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                    default_delay=10,
                    default_max_attempts=6,
                    timeout_config=timeout.get("create") if timeout else None,
                )
                certificate_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
                    name="CertificateCreated",
                    operation="DescribeCertificate",
                    argument=["Error.Code", "Certificate.Status"],
                    acceptors=acceptors,
                    client=await hub.tool.boto3.client.get_client(ctx, "acm"),
                )
                await hub.tool.boto3.client.wait(
                    ctx,
                    "acm",
                    "CertificateCreated",
                    certificate_waiter,
                    CertificateArn=resource_id,
                    WaiterConfig=waiter_config,
                )

                result["comment"] += [f"Imported aws.acm.certificate_manager '{name}'"]

            except Exception as e:
                result["comment"] += [str(e)]
                result["result"] = False
        # If domain name is provided as an input then certificate needs to be requested/created
        elif domain_name:
            try:
                if ctx.get("test", False):
                    result[
                        "new_state"
                    ] = hub.tool.aws.test_state_utils.generate_test_state(
                        enforced_state={},
                        desired_state={
                            "name": name,
                            "domain_name": domain_name,
                            "validation_method": validation_method,
                            "subject_alternative_names": subject_alternative_names,
                            "idempotency_token": idempotency_token,
                            "domain_validation_options": domain_validation_options,
                            "options": options,
                            "certificate_authority_arn": certificate_authority_arn,
                            "tags": tags,
                        },
                    )
                    result["comment"] = result[
                        "comment"
                    ] + hub.tool.aws.comment_utils.would_create_comment(
                        resource_type="aws.acm.certificate_manager", name=name
                    )
                    return result

                requested = await hub.exec.boto3.client.acm.request_certificate(
                    ctx=ctx,
                    DomainName=domain_name,
                    ValidationMethod=validation_method,
                    SubjectAlternativeNames=subject_alternative_names,
                    IdempotencyToken=idempotency_token,
                    DomainValidationOptions=domain_validation_options,
                    Options=options,
                    CertificateAuthorityArn=certificate_authority_arn,
                    Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                    if tags
                    else None,
                )
                result["result"] = requested["result"]
                if not result["result"]:
                    result["comment"] += requested["comment"]
                    return result
                resource_id = requested["ret"]["CertificateArn"]

                # Custom waiter for request
                # When the certificate is just created, there is a delay of several seconds before we can retrieve information about it.
                waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                    default_delay=10,
                    default_max_attempts=6,
                    timeout_config=timeout.get("create") if timeout else None,
                )
                certificate_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
                    name="CertificateCreated",
                    operation="DescribeCertificate",
                    argument=["Error.Code", "Certificate.Status"],
                    acceptors=acceptors,
                    client=await hub.tool.boto3.client.get_client(ctx, "acm"),
                )
                await hub.tool.boto3.client.wait(
                    ctx,
                    "acm",
                    "CertificateCreated",
                    certificate_waiter,
                    CertificateArn=resource_id,
                    WaiterConfig=waiter_config,
                    delay=30,
                )

                result["comment"] = result[
                    "comment"
                ] + hub.tool.aws.comment_utils.create_comment(
                    resource_type="aws.acm.certificate_manager", name=name
                )

            except Exception as e:
                result["comment"] += [str(e)]
                result["result"] = False
                return result
        # If neither of private key and domain name is provided
        else:
            hub.log.debug(
                "AWS Certificate must be imported (private_key) or created (domain_name)"
            )
            result["comment"] += [
                "AWS Certificate must be imported (private_key) or created (domain_name)"
            ]
            result["result"] = False
            return result
    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif not (before and before["result"]) or are_tags_updated or is_reimported:
            after = await hub.exec.aws.acm.certificate_manager.get(
                ctx,
                name=name,
                resource_id=resource_id,
            )
            if not after["result"]:
                result["result"] = False
                result["comment"] = after["comment"]
                return result
            result["new_state"] = copy.deepcopy(after["ret"])
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])

    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes a certificate and its associated private key.

    If this action succeeds, the certificate no longer appears in the list that can be displayed by calling the
    ListCertificates action or be retrieved by calling the GetCertificate action.
    The certificate will not be available for use by Amazon Web Services services integrated with ACM.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            The Amazon Resource Name (ARN) of certificate to identify the resource.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.acm.certificate.absent:
                - name: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.acm.certificate_manager", name=name
        )
        return result
    before = await hub.exec.aws.acm.certificate_manager.get(
        ctx=ctx, name=name, resource_id=resource_id
    )
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result
    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.acm.certificate_manager", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.acm.certificate_manager", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client.acm.delete_certificate(
            ctx, CertificateArn=resource_id
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.acm.certificate_manager", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns detailed metadata about ACM certificates.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.acm.certificate
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
            await hub.tool.aws.acm.conversion_utils.convert_raw_acm_to_present_async(
                ctx,
                raw_resource=resource,
                idem_resource_name=resource_id,
            )
        )
        if not convert_ret["result"]:
            hub.log.warning(
                f"Could not describe AWS Certificate '{resource_id}' {convert_ret['comment']}"
            )
            continue
        resource_translated = convert_ret.get("ret")
        result[resource_id] = {
            "aws.acm.certificate_manager.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result
