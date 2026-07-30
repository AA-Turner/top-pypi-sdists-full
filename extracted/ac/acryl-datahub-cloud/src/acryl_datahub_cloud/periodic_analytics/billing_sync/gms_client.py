import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Protocol
from urllib.parse import urlparse, urlunparse

import requests
from pydantic import BaseModel

from acryl_datahub_cloud.periodic_analytics.billing_sync.mtd_keys import parse_mtd_key
from acryl_datahub_cloud.periodic_analytics.billing_sync.publish_ledger import (
    PendingIntent,
)
from acryl_datahub_cloud.periodic_analytics.partitions import (
    DAY_KEY_FORMAT,
    HourPartition,
)

logger = logging.getLogger(__name__)

_INT64_MAX = 2**63 - 1
_BILLING_EVENT_TYPE_BY_METRIC = {
    "mcp_query": "mcp_usage",
}


def _billing_event_type(metric_name: str) -> str:
    return _BILLING_EVENT_TYPE_BY_METRIC.get(metric_name, metric_name)


def derive_billing_usage_url(gms_base_or_url: str) -> str:
    """Map a GMS base or any .../openapi/v1/... URL → billing/usage."""
    parsed = urlparse(gms_base_or_url)
    path = parsed.path or ""
    marker = "/openapi/v1/"
    idx = path.find(marker)
    if idx >= 0:
        new_path = path[: idx + len(marker)] + "billing/usage"
    else:
        new_path = "/openapi/v1/billing/usage"
    return urlunparse(parsed._replace(path=new_path, params="", query="", fragment=""))


def resolve_publish_url(
    configured: Optional[str], gms_server: Optional[str] = None
) -> Optional[str]:
    """Prefer explicit recipe URL; else derive from graph ``server``."""
    if configured:
        return configured
    if gms_server:
        return derive_billing_usage_url(gms_server)
    return None


class BillingUsageRequest(BaseModel):
    # Field names mirror BillingUsageRequest.java exactly.
    eventType: str
    transactionId: str
    quantity: int
    rollup: bool = False
    providerPassThrough: bool = True
    product: Optional[str] = None
    # ISO-8601 instant for Metronome event attribution (as_of_hour end).
    timestamp: Optional[str] = None
    properties: Dict[str, object]


def as_of_hour_end_timestamp(as_of_date: str) -> str:
    """Return ISO-8601 UTC last millisecond inside an as_of hour (or legacy day).

    HourPartition.end is exclusive (start of the next hour). Using that boundary
    verbatim would attribute a June T23 emit to July in Metronome. Emit the last
    millisecond still inside the collected hour instead.
    """
    if "T" in as_of_date:
        exclusive_end: datetime = HourPartition.from_key(as_of_date).end
    else:
        # Legacy day-precision ledger keys: attribute to end of that UTC day.
        datetime.strptime(as_of_date, DAY_KEY_FORMAT)
        exclusive_end = HourPartition(dt=as_of_date, hour=23).end
    inclusive_end = exclusive_end - timedelta(milliseconds=1)
    return inclusive_end.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def build_delta_request(
    metric_name: str,
    delta: int,
    revision: int,
    period: str,
    as_of_date: str,
    finalized: bool,
    product: Optional[str],
    *,
    quantity: Optional[int] = None,
) -> BillingUsageRequest:
    # quantity defaults to signed delta (SUM model). Pass absolute cumulative
    # for LATEST snapshot metrics via quantity=.
    # metric_name may be a dimensional MTD key (api_calls\x1frequest_api=graphql).
    # MCP uses a distinct Tier C envelope (mcp_usage) so valueOf() does not
    # collide with per-request MCP_QUERY; metric_name stays mcp_query for S3
    # and Metronome.
    emitted = delta if quantity is None else quantity
    if abs(emitted) > _INT64_MAX:
        # The endpoint's quantity is a 64-bit long as of the 2026-07-15 GMS
        # fix (BillingController). A value that overflows even that is
        # absurd for any real metric, so fail loudly rather than publish
        # garbage.
        raise ValueError(
            f"quantity for {metric_name} ({emitted}) exceeds int64 — refusing "
            "to publish"
        )
    base_metric_name, dim_props = parse_mtd_key(metric_name)
    properties: Dict[str, object] = {
        "metric_name": base_metric_name,
        "period": period,
        "as_of_date": as_of_date,
        "finalized": finalized,
        # GMS classifies revision as a string pass-through property
        # (PROVIDER_PASS_THROUGH_METADATA); a JSON int lands in GMS's
        # numeric map instead and fails validate() as an unknown numeric
        # property. customer_id/instance_id/metric_family/cumulative_mtd
        # are intentionally NOT sent: none are in GMS's allowlist for
        # this event type, and customer_id/instance_id are already
        # stamped onto the wire BillingEvent server-side from
        # BillingConfiguration — cumulative_mtd stays local to the
        # publish ledger and close snapshot, which already preserve it.
        "revision": str(revision),
    }
    properties.update(dim_props)
    return BillingUsageRequest(
        eventType=_billing_event_type(base_metric_name),
        # Include full mtd_key so dimensional publishes don't collide.
        transactionId=f"{period}/{as_of_date}/{metric_name}/r{revision}",
        quantity=emitted,
        rollup=False,
        product=product,
        timestamp=as_of_hour_end_timestamp(as_of_date),
        properties=properties,
    )


def build_replay_request(
    metric_name: str,
    pending: PendingIntent,
    period: str,
    as_of_date: str,
    finalized: bool,
    product: Optional[str],
) -> BillingUsageRequest:
    # C1: a byte-identical resend of a previously-recorded intent. quantity
    # and transactionId come straight from the pending record — never
    # recomputed — so the vendor's dedup-by-transactionId either drops a true
    # duplicate (it landed) or accepts the original quantity (it never did).
    # `properties` is rebuilt fresh from this run's period/as_of_date/
    # finalized/revision — same allowlist-constrained shape as
    # build_delta_request — since a `PendingIntent` only ever stores
    # primitives (revision, delta, cumulative_mtd, transaction_id), never a
    # full request. That also means a pending record from before this fix
    # replays safely: it was never delivered (GMS dropped the old shape
    # silently), so resending under the same transactionId with the new
    # shape cannot double-count — the vendor has no prior delivery to
    # collide with.
    # Prefer the pending as_of for timestamp so LATEST resolves to the
    # original event time, not the wake that is replaying.
    replay_as_of = pending.as_of_date or as_of_date
    base_metric_name, dim_props = parse_mtd_key(metric_name)
    properties: Dict[str, object] = {
        "metric_name": base_metric_name,
        "period": period,
        "as_of_date": as_of_date,
        "finalized": finalized,
        "revision": str(pending.revision),
    }
    properties.update(dim_props)
    return BillingUsageRequest(
        eventType=_billing_event_type(base_metric_name),
        transactionId=pending.transaction_id,
        quantity=pending.delta,
        rollup=False,
        product=product,
        timestamp=as_of_hour_end_timestamp(replay_as_of),
        properties=properties,
    )


class BillingPublishClient(Protocol):
    def publish_one(self, request: BillingUsageRequest) -> None: ...


class DryRunBillingPublishClient:
    def publish_one(self, request: BillingUsageRequest) -> None:
        logger.info(
            "dry-run: NOT sending to GMS (publish_enabled=false): %s",
            request.model_dump_json(exclude_none=True),
        )


class HttpBillingPublishClient:
    def __init__(self, gms_publish_url: str, authorization: str):
        self._url = gms_publish_url
        # Full Authorization header value (Bearer … or system Basic …).
        self._authorization = authorization

    def publish_one(self, request: BillingUsageRequest) -> None:
        # Metronome is append-only: each transactionId is unique per
        # (as_of_date, revision), so a duplicate re-send of the same request
        # is dropped by the vendor as idempotent replay rather than
        # double-counted — unlike the old cumulative-MTD scheme, there is no
        # "last write wins" state to corrupt.
        response = requests.post(
            self._url,
            json=request.model_dump(exclude_none=True),
            headers={"Authorization": self._authorization},
            timeout=30,
        )
        response.raise_for_status()
