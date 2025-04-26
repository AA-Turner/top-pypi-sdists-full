from .. import context
from agilicus.agilicus_api import (
    NetworkPort,
    NetworkPortRange,
    NetworkServiceConfig,
)

from agilicus import agilicus_api

from ..input_helpers import build_updated_model
from ..input_helpers import update_org_from_input_or_ctx
from ..input_helpers import strip_none
from ..output.table import (
    spec_column,
    format_table,
    metadata_column,
)
from ..resource_helpers import map_resource_published

PROTOCOLS = ["postgresql"]


def list_database_resources(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    params = strip_none(kwargs)
    query_results = apiclient.app_services_api.list_database_resources(**params)
    return query_results.database_resources


def add_database_resource(ctx, port, name, data_source_name, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    if data_source_name is None:
        data_source_name = name

    spec = agilicus_api.DatabaseResourceSpec(
        name=name, data_source_name=data_source_name, **strip_none(kwargs)
    )
    if port is not None:
        ports = NetworkPortRange(port=NetworkPort(str(port)))
        spec["config"] = NetworkServiceConfig(ports=[ports])
    model = agilicus_api.DatabaseResource(spec=spec)

    return apiclient.app_services_api.create_database_resource(model).to_dict()


def _get_database_resource(ctx, apiclient, resource_id, **kwargs):
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return apiclient.app_services_api.get_database_resource(resource_id, **kwargs)


def show_database_resource(ctx, resource_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return _get_database_resource(ctx, apiclient, resource_id, **kwargs).to_dict()


def delete_database_resource(ctx, resource_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return apiclient.app_services_api.delete_database_resource(resource_id, **kwargs)


def update_database_resource(
    ctx,
    resource_id,
    port,
    published,
    runtime_parameters,
    replace_runtime_parameters,
    **kwargs,
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    get_args = {}
    update_org_from_input_or_ctx(get_args, ctx, **kwargs)
    mapping = _get_database_resource(ctx, apiclient, resource_id, **get_args)

    # check_type=False works around nested types not deserializing correctly
    mapping.spec = build_updated_model(
        agilicus_api.DatabaseResourceSpec, mapping.spec, kwargs, check_type=False
    )

    runtime_parameters = list(runtime_parameters or [])

    if not replace_runtime_parameters:
        runtime_parameters = (mapping.spec.runtime_parameters or []) + runtime_parameters

    mapping.spec.runtime_parameters = runtime_parameters

    if port is not None:
        ports = NetworkPortRange(port=NetworkPort(str(port)))
        mapping.spec["config"] = NetworkServiceConfig(ports=[ports])

    mapping = map_resource_published(mapping, published)

    return apiclient.app_services_api.replace_database_resource(
        resource_id, database_resource=mapping
    ).to_dict()


def format_database_as_text(ctx, resources):
    columns = [
        metadata_column("id"),
        spec_column("org_id"),
        spec_column("name"),
        spec_column("address"),
        spec_column("database_protocol"),
        spec_column("data_source_name"),
        spec_column("connector_id"),
        spec_column("config"),
    ]

    return format_table(ctx, resources, columns)
