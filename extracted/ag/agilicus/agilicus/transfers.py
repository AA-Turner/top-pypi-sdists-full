from . import context
from .input_helpers import get_org_from_input_or_ctx
from agilicus import input_helpers
import agilicus

from .output.table import (
    spec_column,
    status_column,
    format_table,
    metadata_column,
)


def query_connector(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    params = {}
    params["org_id"] = org_id
    input_helpers.update_if_not_none(params, kwargs)
    query_results = apiclient.connectors_api.list_transfers(connector_id, **params)
    return query_results.connector_transfers


def format(ctx, transfers, **kwargs):
    columns = [
        metadata_column("id"),
        spec_column("org_id"),
        spec_column("src_instance_id"),
        spec_column("src_public_key"),
        spec_column("dst_instance_id"),
        spec_column("dst_public_key"),
        spec_column("transfer_type"),
        status_column("status"),
        status_column("encrypted_data_length"),
        status_column("expiry_time"),
    ]

    return format_table(ctx, transfers, columns)


def new_transfer(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    spec = agilicus.ConnectorSecureTransferSpec(org_id=org_id)
    transfer = agilicus.ConnectorSecureTransfer(spec)
    return apiclient.connectors_api.create_transfer(connector_id, transfer)
