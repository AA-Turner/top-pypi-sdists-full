from .. import context
from datetime import date
import json
from ..input_helpers import get_org_from_input_or_ctx, strip_none
import agilicus
import pem
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from cryptography.hazmat.primitives import serialization
import httpx
from ..output.table import (
    spec_column,
    format_table,
    metadata_column,
    status_column,
    subtable,
    column,
)


def add_certificate(ctx, certificate=None, certificate_url=None, **kwargs):
    results = []
    if certificate:
        for certificate in pem.parse_file(certificate):
            results.append(_add_certificate_pem(ctx, str(certificate), **kwargs))
    if certificate_url:
        response = httpx.get(certificate_url)
        if response.status_code != 200:
            return results
        crt_data = response.content
        cert = x509.load_der_x509_certificate(crt_data, default_backend())
        pem_data = cert.public_bytes(serialization.Encoding.PEM).decode()
        results.append(_add_certificate_pem(ctx, str(pem_data), **kwargs))
    return results


def _add_certificate_pem(ctx, certificate, labels, **kwargs):
    token = context.get_token(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    apiclient = context.get_apiclient(ctx, token)
    spec = agilicus.TrustedCertificateSpec(str(certificate), **kwargs)
    if labels:
        spec.labels = [agilicus.TrustedCertificateLabelName(label) for label in labels]
    req = agilicus.TrustedCertificate(spec=spec)

    try:
        return apiclient.trusted_certs_api.create_trusted_cert(req)
    except Exception as exc:
        if exc.status == 409:
            body = exc.body
            if not body:
                raise
            result = json.loads(body)
            guid = agilicus.find_guid(result)
            req = apiclient.trusted_certs_api.get_trusted_cert(guid, org_id=org_id)
            req.spec.certificate = str(certificate)
            if not req.spec.labels:
                req.spec.labels = []
            for label in labels:
                req.spec.labels.append(agilicus.TrustedCertificateLabelName(label))
            updated_cert = apiclient.trusted_certs_api.replace_trusted_cert(
                req.metadata.id,
                req,
            )
            return updated_cert
        raise


def globalsize_get_cert_url(common_name):
    url = ""
    mappings = {"GlobalSign": "gs"}
    if "GlobalSign" not in common_name:
        return None

    for part in common_name.split(" "):
        url += mappings.get(part, part.lower())
    return f"https://secure.globalsign.com/cacert/{url}.crt"


def get_globalsign_urls(**kwargs):
    base = "https://secure.globalsign.com/cacert/gsatlasr3dvtlsca"
    year = date.today().year
    urls = []
    for year in [year, year + 1]:
        url = base + str(year)

        for q in range(1, 5):
            urls.append(url + f"q{str(q)}.crt")
    return urls


def update_globalsign_certs(ctx, **kwargs):
    results = []
    for url in get_globalsign_urls():
        results.extend(add_certificate(ctx, certificate_url=url, labels=["all"]))
    return results


def update_trusted_certificates(ctx, common_name=None, globalsign=None, **kwargs):
    results = []
    if globalsign:
        results.extend(update_globalsign_certs(ctx, **kwargs))
    if common_name:
        url = globalsize_get_cert_url(common_name)
        if not url:
            return "cannot find cert url from CN"
        return add_certificate(ctx, certificate_url=url, labels=["all"], **kwargs)
    return results


def get_certificate(ctx, certificate_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    kwargs = strip_none(kwargs)
    return apiclient.trusted_certs_api.get_trusted_cert(
        certificate_id,
        **kwargs,
    )


def delete_certificate(ctx, certificate_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    kwargs = strip_none(kwargs)
    return apiclient.trusted_certs_api.delete_trusted_cert(
        certificate_id,
        **kwargs,
    )


def add_label(ctx, label, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    labelName = agilicus.TrustedCertificateLabelName(label)
    spec = agilicus.TrustedCertificateLabelSpec(labelName, **kwargs)
    req = agilicus.TrustedCertificateLabel(spec=spec)
    return apiclient.trusted_certs_api.create_label(req)


def add_bundle(ctx, bundle, label=None, label_org_id=None, exclude=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    if label_org_id is None:
        label_org_id = org_id
    bundle_label = None
    if label is not None:
        label_name = agilicus.TrustedCertificateLabelName(label)
        label_spec = agilicus.TrustedCertificateLabelSpec(
            name=label_name, org_id=label_org_id
        )
        bundle_label = agilicus.TrustedCertificateBundleLabel(label=label_spec)
        if exclude is not None:
            bundle_label.exclude = exclude

    bundle_name = agilicus.TrustedCertificateBundleName(bundle)
    spec = agilicus.TrustedCertificateBundleSpec(bundle_name, **kwargs)
    if bundle_label:
        spec.labels = []
        spec.labels.append(bundle_label)
    req = agilicus.TrustedCertificateBundle(spec=spec)
    return apiclient.trusted_certs_api.create_bundle(req)


def add_bundle_label(ctx, bundle_id, label, label_org_id=None, exclude=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    if label_org_id is None:
        label_org_id = org_id

    bundle = get_bundle(ctx, bundle_id, **kwargs)
    bundle_label = None
    label_name = agilicus.TrustedCertificateLabelName(label)
    label_spec = agilicus.TrustedCertificateLabelSpec(
        name=label_name, org_id=label_org_id
    )
    bundle_label = agilicus.TrustedCertificateBundleLabel(label=label_spec)
    if exclude is not None:
        bundle_label.exclude = exclude

    if not bundle.spec.labels:
        bundle.spec.labels = []

    bundle.spec.labels.append(bundle_label)
    return apiclient.trusted_certs_api.replace_bundle(bundle_id, bundle)


def delete_bundle(ctx, bundle_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    return apiclient.trusted_certs_api.delete_bundle(bundle_id, **kwargs)


def list_bundles(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    kwargs = strip_none(kwargs)
    return apiclient.trusted_certs_api.list_bundles(
        **kwargs,
    ).trusted_cert_bundles


def get_bundle(ctx, bundle_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    kwargs = strip_none(kwargs)
    return apiclient.trusted_certs_api.get_bundle(
        bundle_id,
        **kwargs,
    )


def format_bundles(ctx, bundles):
    label_columns = [
        column("label"),
    ]
    columns = [
        metadata_column("id"),
        metadata_column("created"),
        spec_column("org_id"),
        spec_column("name"),
        subtable(ctx, "spec.labels", label_columns),
    ]
    return format_table(ctx, bundles, columns)


def list_labels(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    kwargs = strip_none(kwargs)
    return apiclient.trusted_certs_api.list_labels(
        **kwargs,
    ).trusted_cert_labels


def list_certificates(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)

    kwargs = strip_none(kwargs)
    query_results = apiclient.trusted_certs_api.list_trusted_certs(
        org_id=org_id, **kwargs
    ).trusted_certs
    return query_results


def format_labels(ctx, labels):
    columns = [
        metadata_column("created"),
        spec_column("org_id"),
        spec_column("name"),
    ]
    return format_table(ctx, labels, columns)


def format_certificates_as_text(ctx, certificates):
    columns = [
        metadata_column("id"),
        metadata_column("created"),
        spec_column("org_id"),
        spec_column("root"),
        spec_column("labels"),
        status_column("key_usage_extension"),
        status_column("subject"),
    ]
    return format_table(ctx, certificates, columns)


def list_orgs(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    kwargs = strip_none(kwargs)
    return apiclient.trusted_certs_api.list_cert_orgs(
        **kwargs,
    ).orgs


def format_orgs(ctx, orgs):
    columns = [
        column("id"),
        column("organisation"),
    ]
    return format_table(ctx, orgs, columns)
