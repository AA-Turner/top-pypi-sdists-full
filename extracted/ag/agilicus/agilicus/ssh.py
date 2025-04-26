from . import context
from agilicus.agilicus_api import (
    SSHResource,
    SSHResourceSpec,
    NetworkPort,
    NetworkPortRange,
    NetworkServiceConfig,
)

from .input_helpers import build_updated_model
from .input_helpers import update_org_from_input_or_ctx
from .input_helpers import strip_none
from .output.table import (
    spec_column,
    format_table,
    metadata_column,
)
from .resource_helpers import map_resource_published


def list_ssh_resources(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    params = strip_none(kwargs)
    query_results = apiclient.app_services_api.list_ssh_resources(**params)
    return query_results.ssh_resources


def add_ssh_resource(ctx, port, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    spec = SSHResourceSpec(**strip_none(kwargs))
    if port is not None:
        ports = NetworkPortRange(port=NetworkPort(str(port)))
        spec["config"] = NetworkServiceConfig(ports=[ports])
    model = SSHResource(spec=spec)

    return apiclient.app_services_api.create_ssh_resource(model).to_dict()


def _get_ssh_resource(ctx, apiclient, resource_id, **kwargs):
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return apiclient.app_services_api.get_ssh_resource(resource_id, **kwargs)


def show_ssh_resource(ctx, resource_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return _get_ssh_resource(ctx, apiclient, resource_id, **kwargs).to_dict()


def delete_ssh_resource(ctx, resource_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return apiclient.app_services_api.delete_ssh_resource(resource_id, **kwargs)


def update_ssh_resource(ctx, resource_id, port, published, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    get_args = {}
    update_org_from_input_or_ctx(get_args, ctx, **kwargs)
    mapping = _get_ssh_resource(ctx, apiclient, resource_id, **get_args)

    # check_type=False works around nested types not deserializing correctly
    mapping.spec = build_updated_model(
        SSHResourceSpec, mapping.spec, kwargs, check_type=False
    )
    if port is not None:
        ports = NetworkPortRange(port=NetworkPort(str(port)))
        mapping.spec["config"] = NetworkServiceConfig(ports=[ports])

    mapping = map_resource_published(mapping, published)

    return apiclient.app_services_api.replace_ssh_resource(
        resource_id, ssh_resource=mapping
    ).to_dict()


def format_ssh_as_text(ctx, resources):
    columns = [
        metadata_column("id"),
        spec_column("org_id"),
        spec_column("name"),
        spec_column("address"),
        spec_column("connector_id"),
        spec_column("config"),
    ]

    return format_table(ctx, resources, columns)
