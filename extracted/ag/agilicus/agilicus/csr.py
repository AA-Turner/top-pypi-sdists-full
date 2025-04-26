from . import context
from .input_helpers import get_org_from_input_or_ctx, strip_none
from .input_helpers import pop_item_if_none
import agilicus
from .output.table import (
    spec_column,
    format_table,
    metadata_column,
    status_column,
    subtable,
)

TARGET_ISSUER_VALUES = [
    "agilicus-private",
    "agilicus-public-acme",
]


ReasonEnum = agilicus.CSRReasonEnum.allowed_values[("value",)]


def add_agent_csr(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    kwargs = strip_none(kwargs)

    if kwargs["request"] is not None:
        csr_request = open(kwargs["request"], "r").read()
        kwargs["request"] = csr_request

    spec = agilicus.CertSigningReqSpec(org_id=org_id, **kwargs)
    req = agilicus.CertSigningReq(spec=spec)
    return apiclient.connectors_api.create_agent_csr(connector_id, req)


def list_agent_csr(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    kwargs = strip_none(kwargs)

    query_results = apiclient.connectors_api.list_agent_csr(
        org_id=org_id, **kwargs
    ).certificate_signing_requests
    return query_results


def get_agent_csr(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)

    return apiclient.connectors_api.get_agent_csr(
        org_id=org_id,
        **kwargs,
    )


def reissue_csr(ctx, csr_id, org_id, old_not_after, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)

    spec = agilicus.CertSigningReqReissueSpec(
        csr_id=csr_id, org_id=org_id, old_not_after=old_not_after
    )

    req = agilicus.CertSigningReqReissue(
        spec=spec,
    )

    return apiclient.certificates_api.reissue_cert_for_csr(
        cert_signing_req_reissue=req,
    )


def list_csr(ctx, reason=None, not_valid_after=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    if reason is not None:
        kwargs["reason"] = reason

    if org_id:
        kwargs["org_id"] = org_id

    if not_valid_after is not None:
        kwargs["not_valid_after"] = not_valid_after

    kwargs = strip_none(kwargs)
    query_results = apiclient.certificates_api.list_csr(
        **kwargs
    ).certificate_signing_requests
    return query_results


def get_csr(ctx, csr_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    pop_item_if_none(kwargs)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)

    return apiclient.certificates_api.get_csr(csr_id, org_id=org_id, **kwargs)


def delete_csr(ctx, csr_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)

    return apiclient.certificates_api.delete_csr(csr_id, org_id=org_id, **kwargs)


def update_csr(ctx, csr_id, uid=None, private_key_id=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)

    csr = apiclient.certificates_api.get_csr(csr_id, org_id=org_id, **kwargs)

    if uid is not None:
        csr.spec.uid = uid
    if private_key_id is not None:
        csr.spec.private_key_id = private_key_id

    return apiclient.certificates_api.replace_csr(
        csr_id, org_id=org_id, cert_signing_req=csr, **kwargs
    )


def format_csr_as_text(ctx, csrs, get_certificate_updates=False, **kwargs):
    certificate_columns = [
        spec_column("reason"),
        status_column("not_after"),
    ]
    columns = [
        metadata_column("id"),
        spec_column("org_id"),
        spec_column("uid"),
        spec_column("private_key_id", "key_id", max_size=8),
        spec_column("target_issuer"),
        status_column("connector_id"),
        status_column("auto_renew"),
        status_column("dns_names"),
        subtable(ctx, "certificates", certificate_columns, subobject_name="status"),
    ]

    if get_certificate_updates:
        certificate_updates_columns = [
            metadata_column("created"),
            spec_column("message"),
        ]
        columns.append(
            subtable(
                ctx,
                "certificate_updates",
                certificate_updates_columns,
                subobject_name="status",
            )
        )

    return format_table(ctx, csrs, columns)


def add_csr(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    kwargs = strip_none(kwargs)

    if kwargs["request"] is not None:
        csr_request = open(kwargs["request"], "r").read()
        kwargs["request"] = csr_request

    spec = agilicus.CertSigningReqSpec(org_id=org_id, **kwargs)
    req = agilicus.CertSigningReq(spec=spec)
    return apiclient.connectors_api.create_csr(req)
