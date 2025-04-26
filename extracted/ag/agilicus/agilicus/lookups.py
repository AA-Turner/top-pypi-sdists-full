from . import context
from .input_helpers import get_org_from_input_or_ctx
import agilicus


def lookup(ctx, guid, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    res = apiclient.lookups_api.lookup_org_guid(org_id, guid)
    return res


def bulk_lookup(ctx, guids, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    request = agilicus.LookupRequest(org_id=org_id, guids=guids)

    res = apiclient.lookups_api.bulk_query_org_guids(request)
    return res
