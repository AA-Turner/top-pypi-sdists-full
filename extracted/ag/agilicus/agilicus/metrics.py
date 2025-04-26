from agilicus.input_helpers import pop_item_if_none, strip_none
from . import context
from . import connectors
from . import orgs
from .output.table import (
    column,
    format_table,
)
import operator


def query_top(
    ctx,
    org_id=None,
    dt_from=None,
    dt_to=None,
    app_id=None,
    sub_org_id=None,
    interval=None,
    limit=None,
    **kwargs,
):
    token = context.get_token(ctx)

    if not org_id:
        org_id = context.get_org_id(ctx, token)

    apiclient = context.get_apiclient(ctx, token)

    pop_item_if_none(kwargs)
    params = strip_none(kwargs)
    params["dt_from"] = dt_from
    params["dt_to"] = dt_to

    if app_id:
        params["app_id"] = app_id
    if interval:
        params["interval"] = int(interval)
    if limit:
        params["limit"] = int(limit)

    resp = apiclient.metrics_api.list_top_users(org_id, **params)

    return resp.top_users


def query_active(
    ctx,
    org_id=None,
    dt_from=None,
    dt_to=None,
    app_id=None,
    sub_org_id=None,
    interval=None,
    **kwargs,
):
    token = context.get_token(ctx)

    if not org_id:
        org_id = context.get_org_id(ctx, token)

    apiclient = context.get_apiclient(ctx, token)

    params = strip_none(kwargs)
    pop_item_if_none(kwargs)
    params["dt_from"] = dt_from
    params["dt_to"] = dt_to

    if app_id:
        params["app_id"] = app_id
    if interval:
        params["interval"] = int(interval)

    resp = apiclient.metrics_api.list_active_users(org_id, **params)

    return resp.active_users


def show_top_connectors(ctx, n=10, org_id=None):
    by_org = {}
    for connector in connectors.query(ctx, org_id=org_id):
        conns = by_org.setdefault(connector.spec.org_id, [])
        conns.append(connector)

    org_by_id, _ = orgs.get_org_by_dictionary(ctx, org_id)
    rows = []
    for k, v in sorted(by_org.items(), key=lambda item: len(item[1]), reverse=True):
        if len(rows) >= n:
            break
        org_name = org_by_id.get(k, {}).get("organisation", "unknown org")
        rows.append({"org_id": k, "Organisation": org_name, "num_connectors": len(v)})
    columns = [
        column("org_id"),
        column("Organisation"),
        column("num_connectors"),
    ]
    print(format_table(ctx, rows, columns, getter=operator.itemgetter))
