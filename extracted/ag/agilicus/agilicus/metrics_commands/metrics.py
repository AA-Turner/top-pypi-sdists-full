from datetime import datetime

from agilicus.input_helpers import strip_none
from .. import context
from ..output.table import column, format_table
from ..pagination import normalize_page_args
from ..pagination.auto_iterator import get_limit_max


def _format_time_val(val, ctx=None):
    if val is None:
        return ""
    if isinstance(val, datetime):
        return val.isoformat()
    return str(val)


def _normalize_list_param(val):
    if not val:
        return None
    if isinstance(val, str):
        return [x.strip() for x in val.split(",") if x.strip()]
    if isinstance(val, (list, tuple)):
        flattened = []
        for item in val:
            if isinstance(item, str):
                flattened.extend([x.strip() for x in item.split(",") if x.strip()])
            else:
                flattened.append(str(item))
        return flattened
    return [str(val)]


def _normalize_sort_order(val):
    if not val:
        return None
    val = str(val).lower().strip()
    if val in ("asc", "ascending"):
        return "ascending"
    if val in ("desc", "descending"):
        return "descending"
    return val


def _apply_preset(
    preset, breakdown_by, sort_by, sort_order, bucket_size, dt_from, dt_to, all_orgs
):
    if preset == "user-usage":
        return (
            breakdown_by or ["user_id"],
            sort_by or "access_count",
            sort_order or "descending",
            bucket_size,
            dt_from,
            dt_to,
            all_orgs,
        )
    if preset == "resource-usage":
        return (
            breakdown_by or ["resource_id", "resource_type"],
            sort_by or "access_count",
            sort_order or "ascending",
            bucket_size,
            dt_from,
            dt_to,
            all_orgs,
        )
    if preset == "adoption":
        return (
            breakdown_by,
            sort_by,
            sort_order,
            bucket_size or "P1D",
            dt_from or "now-30d",
            dt_to,
            all_orgs,
        )
    if preset == "velocity":
        return (
            breakdown_by,
            sort_by,
            sort_order,
            bucket_size or "P1M",
            dt_from or "6 months ago",
            dt_to or "1 month ago",
            all_orgs,
        )
    if preset == "resource-types":
        return (
            breakdown_by or ["resource_type"],
            sort_by,
            sort_order,
            bucket_size or "P1W",
            dt_from,
            dt_to,
            all_orgs,
        )
    if preset == "unique-users":
        return (
            breakdown_by,
            sort_by,
            sort_order,
            bucket_size or "P1M",
            dt_from,
            dt_to,
            all_orgs,
        )
    if preset == "fleet-comparison":
        return (
            breakdown_by or ["org_id"],
            sort_by,
            sort_order,
            bucket_size or "P1M",
            dt_from,
            dt_to,
            True,
        )
    return (
        breakdown_by,
        sort_by,
        sort_order,
        bucket_size,
        dt_from,
        dt_to,
        all_orgs,
    )


def _build_usage_params(
    org_id,
    org_ids,
    dt_from,
    dt_to,
    bucket_size,
    breakdown_by,
    resource_type,
    resource_id,
    user_id,
    sort_by,
    sort_order,
    page_on,
    page_at_key,
    page_sort,
):
    params = {}
    if org_id:
        params["org_id"] = str(org_id)
    if org_ids:
        params["org_ids"] = org_ids
    if dt_from:
        params["dt_from"] = str(dt_from)
    if dt_to:
        params["dt_to"] = str(dt_to)
    if bucket_size:
        params["bucket_size"] = str(bucket_size)
    if breakdown_by:
        params["breakdown_by"] = breakdown_by
    if resource_type:
        params["resource_type"] = str(resource_type)
    if resource_id:
        params["resource_id"] = str(resource_id)
    if user_id:
        params["user_id"] = str(user_id)
    if sort_by:
        params["sort_by"] = str(sort_by)
    if sort_order:
        params["sort_order"] = _normalize_sort_order(sort_order)
    if page_on:
        params["page_on"] = page_on
    if page_at_key:
        params["page_at_key"] = page_at_key
    if page_sort:
        params["page_sort"] = page_sort
    return normalize_page_args(params)


def query_usage(
    ctx,
    org_id=None,
    org_ids=None,
    dt_from=None,
    dt_to=None,
    bucket_size=None,
    breakdown_by=None,
    resource_type=None,
    resource_id=None,
    user_id=None,
    sort_by=None,
    sort_order=None,
    limit=None,
    all_orgs=False,
    preset=None,
    get_all=False,
    page_on=None,
    page_at_key=None,
    page_sort=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    (
        breakdown_by,
        sort_by,
        sort_order,
        bucket_size,
        dt_from,
        dt_to,
        all_orgs,
    ) = _apply_preset(
        preset,
        breakdown_by,
        sort_by,
        sort_order,
        bucket_size,
        dt_from,
        dt_to,
        all_orgs,
    )

    org_ids = _normalize_list_param(org_ids)
    breakdown_by = _normalize_list_param(breakdown_by)
    page_on = _normalize_list_param(page_on)
    page_at_key = _normalize_list_param(page_at_key)
    page_sort = _normalize_list_param(page_sort)

    if not all_orgs and not org_id and not org_ids:
        ctx_org = context.get_org_id(ctx, token)
        if ctx_org:
            org_id = ctx_org

    params = _build_usage_params(
        org_id=org_id,
        org_ids=org_ids,
        dt_from=dt_from,
        dt_to=dt_to,
        bucket_size=bucket_size,
        breakdown_by=breakdown_by,
        resource_type=resource_type,
        resource_id=resource_id,
        user_id=user_id,
        sort_by=sort_by,
        sort_order=sort_order,
        page_on=page_on,
        page_at_key=page_at_key,
        page_sort=page_sort,
    )

    endpoint = apiclient.metrics_api.list_usage_metrics
    # The server caps a single request (e.g. 500 rows).  ``--limit`` is a
    # *total*, so anything above one page is fetched over several pages.  The
    # cap comes from the endpoint's own validation rather than a constant.
    page_size = get_limit_max(endpoint, default=500) or 500

    default_page_on = ["time"] + [d for d in (breakdown_by or []) if d != "time"]
    paging_params = dict(params)
    paging_params["page_on"] = paging_params.get("page_on") or default_page_on
    paging_params.setdefault("page_sort", ["asc"] * len(paging_params["page_on"]))

    if get_all:
        return endpoint.auto_paging_iter(
            limit=int(limit) if limit is not None else None,
            page_size=page_size,
            **paging_params,
        ).all()

    if limit is None:
        limit = page_size
    limit = int(limit)
    if limit > page_size:
        return endpoint.auto_paging_iter(
            limit=limit,
            page_size=page_size,
            **paging_params,
        ).all()

    return endpoint(limit=limit, **params)


def query_user_usage(ctx, **kwargs):
    kwargs = strip_none(kwargs)
    kwargs.setdefault("breakdown_by", ["user_id"])
    kwargs.setdefault("sort_by", "access_count")
    kwargs.setdefault("sort_order", "descending")
    return query_usage(ctx, **kwargs)


def query_resource_usage(ctx, **kwargs):
    kwargs = strip_none(kwargs)
    kwargs.setdefault("breakdown_by", ["resource_id", "resource_type"])
    kwargs.setdefault("sort_by", "access_count")
    kwargs.setdefault("sort_order", "ascending")
    return query_usage(ctx, **kwargs)


def query_adoption(ctx, **kwargs):
    kwargs = strip_none(kwargs)
    kwargs.setdefault("bucket_size", "P1D")
    kwargs.setdefault("dt_from", "now-30d")
    return query_usage(ctx, **kwargs)


def query_fleet_usage(ctx, **kwargs):
    kwargs = strip_none(kwargs)
    kwargs.setdefault("breakdown_by", ["org_id"])
    kwargs.setdefault("bucket_size", "P1M")
    kwargs.setdefault("all_orgs", True)
    return query_usage(ctx, **kwargs)


def _detect_active_dimensions(breakdown_dims, data):
    def has_dim(dim, attr1, attr2=None):
        if dim in breakdown_dims:
            return True
        for b in data:
            if hasattr(b, attr1) and getattr(b, attr1):
                return True
            if attr2 and hasattr(b, attr2) and getattr(b, attr2):
                return True
            if isinstance(b, dict):
                if b.get(attr1) or (attr2 and b.get(attr2)):
                    return True
        return False

    return {
        "org": has_dim("org_id", "org_id", "org_name"),
        "user": has_dim("user_id", "user_id", "email"),
        "resource": has_dim("resource_id", "resource_id", "resource_name"),
        "resource_type": has_dim("resource_type", "resource_type"),
    }


def _metric_getter(item):
    def func(obj):
        val = obj
        for name in item.split("."):
            if val is None:
                return None
            if isinstance(val, dict):
                val = val.get(name)
            else:
                val = getattr(val, name, None)
        if val is None and item in (
            "access_count",
            "unique_users",
            "unique_resources",
        ):
            return 0
        return val

    return func


def format_usage_metrics(ctx, resp):
    if isinstance(resp, list):
        data = resp
        breakdown_dims = set()
    else:
        data = getattr(resp, "data", None)
        if data is None and isinstance(resp, dict):
            data = resp.get("data", [])
        data = data or []
        breakdown_dims = getattr(resp, "breakdown_by", None) or []
        if isinstance(resp, dict):
            breakdown_dims = resp.get("breakdown_by") or breakdown_dims
        breakdown_dims = set(breakdown_dims)

    dims = _detect_active_dimensions(breakdown_dims, data)

    columns = [column("time", optional=True, format_fn=_format_time_val)]
    if dims["org"]:
        columns.extend(
            [
                column("org_id", optional=True),
                column("org_name", optional=True),
            ]
        )
    if dims["user"]:
        columns.extend(
            [
                column("user_id", optional=True),
                column("email", optional=True),
            ]
        )
    if dims["resource"]:
        columns.extend(
            [
                column("resource_id", optional=True),
                column("resource_name", optional=True),
            ]
        )
    if dims["resource_type"]:
        columns.append(column("resource_type", optional=True))
    columns.extend(
        [
            column("access_count", optional=True),
            column("unique_users", optional=True),
            column("unique_resources", optional=True),
        ]
    )

    records = resp if context.output_json(ctx) else data
    return format_table(ctx, records, columns, getter=_metric_getter)
