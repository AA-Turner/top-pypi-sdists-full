from .. import context
import json
from ..input_helpers import get_org_from_input_or_ctx, strip_none
import agilicus
from ..output.table import (
    spec_column,
    format_table,
    metadata_column,
    subtable,
    column,
)


def add_host(ctx, hostname, labels, port=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs = strip_none(kwargs)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    spec = agilicus.HostSpec(agilicus.Domain(hostname), **kwargs)
    if port:
        spec.port = agilicus.NetworkPort(port)

    if labels:
        spec.labels = [agilicus.HostLabelName(label) for label in labels]
    req = agilicus.Host(spec=spec)
    try:
        return apiclient.hosts_api.add_host(req)
    except Exception as exc:
        if exc.status == 409:
            body = exc.body
            if not body:
                raise
            result = json.loads(body)
            guid = agilicus.find_guid(result)
            req = apiclient.hosts_api.get_host(guid, org_id=org_id)
            if not req.spec.labels:
                req.spec.labels = []
            for label in labels:
                req.spec.labels.append(agilicus.TrustedCertificateLabelName(label))
            return apiclient.hosts_api.replace_host(
                req.metadata.id,
                req,
            )
        else:
            raise


def get_host(ctx, host_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    kwargs = strip_none(kwargs)
    return apiclient.hosts_api.get_host(
        host_id,
        **kwargs,
    )


def delete_host(ctx, host_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    kwargs = strip_none(kwargs)
    return apiclient.hosts_api.delete_host(
        host_id,
        **kwargs,
    )


def add_label(ctx, label, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    labelName = agilicus.HostLabelName(label)
    spec = agilicus.HostLabelSpec(labelName, **kwargs)
    req = agilicus.HostLabel(spec=spec)
    return apiclient.hosts_api.add_host_label(req)


def add_bundle(ctx, bundle, label=None, label_org_id=None, exclude=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    if label_org_id is None:
        label_org_id = org_id
    bundle_label = None
    if label is not None:
        label_name = agilicus.HostLabelName(label)
        label_spec = agilicus.HostLabelSpec(name=label_name, org_id=label_org_id)
        bundle_label = agilicus.HostBundleLabel(label=label_spec)
        if exclude is not None:
            bundle_label.exclude = exclude

    bundle_name = agilicus.HostBundleName(bundle)
    spec = agilicus.HostBundleSpec(bundle_name, **kwargs)
    if bundle_label:
        spec.labels = []
        spec.labels.append(bundle_label)
    req = agilicus.HostBundle(spec=spec)
    return apiclient.hosts_api.add_host_bundle(req)


def add_bundle_label(ctx, bundle_id, label, label_org_id=None, exclude=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    if label_org_id is None:
        label_org_id = org_id

    bundle = get_bundle(ctx, bundle_id, **kwargs)
    bundle_label = None
    label_name = agilicus.HostLabelName(label)
    label_spec = agilicus.HostLabelSpec(name=label_name, org_id=label_org_id)
    bundle_label = agilicus.HostBundleLabel(label=label_spec)
    if exclude is not None:
        bundle_label.exclude = exclude

    if not bundle.spec.labels:
        bundle.spec.labels = []

    bundle.spec.labels.append(bundle_label)
    return apiclient.hosts_api.replace_host_bundle(bundle_id, bundle)


def delete_bundle(ctx, bundle_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    return apiclient.hosts_api.delete_host_bundle(bundle_id, **kwargs)


def list_bundles(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    kwargs = strip_none(kwargs)
    return apiclient.hosts_api.list_host_bundles(
        **kwargs,
    ).host_bundles


def get_bundle(ctx, bundle_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    kwargs = strip_none(kwargs)
    return apiclient.hosts_api.get_host_bundle(
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
    return apiclient.hosts_api.list_host_labels(
        **kwargs,
    ).host_labels


def list_hosts(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)

    kwargs = strip_none(kwargs)
    return apiclient.hosts_api.list_hosts(org_id=org_id, **kwargs).hosts


def format_labels(ctx, labels):
    columns = [
        metadata_column("created"),
        spec_column("org_id"),
        spec_column("name"),
    ]
    return format_table(ctx, labels, columns)


def format_hosts_as_text(ctx, hosts):
    columns = [
        metadata_column("id"),
        metadata_column("created"),
        spec_column("org_id"),
        spec_column("hostname"),
        spec_column("path"),
        spec_column("port"),
        spec_column("labels"),
    ]
    return format_table(ctx, hosts, columns)


def list_orgs(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id

    kwargs = strip_none(kwargs)
    return apiclient.hosts_api.list_host_orgs(
        **kwargs,
    ).orgs


def format_orgs(ctx, orgs):
    columns = [
        column("id"),
        column("organisation"),
    ]
    return format_table(ctx, orgs, columns)
