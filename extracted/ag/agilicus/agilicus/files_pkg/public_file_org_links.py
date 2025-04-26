from .. import context
from ..input_helpers import (
    get_org_from_input_or_ctx,
    strip_none,
)
import agilicus
from ..output.table import (
    spec_column,
    format_table,
    metadata_column,
)


def add_public_file_org_link(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs = strip_none(kwargs)

    spec = agilicus.PublicFileOrgLinkSpec(**kwargs)

    obj = agilicus.PublicFileOrgLink(spec=spec)
    return apiclient.files_api.create_public_file_org_link(obj).to_dict()


def list_public_file_org_links(ctx, link_org_id=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["link_org_id"] = get_org_from_input_or_ctx(ctx, org_id=link_org_id)
    kwargs = strip_none(kwargs)

    return apiclient.files_api.list_public_file_org_links(**kwargs).public_file_org_links


def get_public_file_org_link(ctx, link_org_id=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["link_org_id"] = get_org_from_input_or_ctx(ctx, org_id=link_org_id)
    kwargs = strip_none(kwargs)

    return apiclient.files_api.get_public_file_org_link(**kwargs)


def delete_public_file_org_link(ctx, link_org_id=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["link_org_id"] = get_org_from_input_or_ctx(ctx, org_id=link_org_id)
    kwargs = strip_none(kwargs)

    apiclient.files_api.delete_public_file_org_link(**kwargs)


def format_public_file_org_links(ctx, labels):
    columns = [
        metadata_column("id"),
        spec_column("link_org_id"),
        spec_column("target_org_id"),
        spec_column("file_tag"),
    ]

    return format_table(ctx, labels, columns)
