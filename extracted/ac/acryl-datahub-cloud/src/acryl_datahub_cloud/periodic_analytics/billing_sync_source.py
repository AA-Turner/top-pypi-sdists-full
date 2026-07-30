import logging
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from typing import Callable, Dict, Iterable, List, Optional, Tuple, Type, Union

from acryl_datahub_cloud.periodic_analytics.billing_sync.close_writer import (
    CloseSnapshot,
    read_latest_close,
    write_close,
)
from acryl_datahub_cloud.periodic_analytics.billing_sync.derivation import (
    compute_derived_metrics,
)
from acryl_datahub_cloud.periodic_analytics.billing_sync.gms_client import (
    BillingPublishClient,
    BillingUsageRequest,
    DryRunBillingPublishClient,
    HttpBillingPublishClient,
    build_delta_request,
    build_replay_request,
    resolve_publish_url,
)
from acryl_datahub_cloud.periodic_analytics.billing_sync.mtd import (
    compute_mtd,
    resolve_contiguous_as_of_hour,
)
from acryl_datahub_cloud.periodic_analytics.billing_sync.mtd_keys import (
    base_metric_name,
    is_flat_mtd_key,
    mtd_has_dimensional_keys,
    parse_mtd_key,
)
from acryl_datahub_cloud.periodic_analytics.billing_sync.publish_ledger import (
    LedgerEntry,
    PublishLedger,
)
from acryl_datahub_cloud.periodic_analytics.billing_sync.usage_operations import (
    load_usage_operations,
)
from acryl_datahub_cloud.periodic_analytics.billing_sync.validation import (
    BillingValidationError,
    validate_mtd,
)
from acryl_datahub_cloud.periodic_analytics.config import BillingSyncSourceConfig
from acryl_datahub_cloud.periodic_analytics.constants import (
    BILLING_SYNC_SOURCE_KIND,
    SYSTEM_USAGE_METRIC_FAMILY,
    Layer,
)
from acryl_datahub_cloud.periodic_analytics.partitions import (
    HourPartition,
    MonthPartition,
    last_hour_of_period,
)
from acryl_datahub_cloud.periodic_analytics.registry import MetricRegistry, MetricSpec
from acryl_datahub_cloud.periodic_analytics.run_lock import (
    LockClient,
    RunLock,
    RunLockOwnershipLostError,
    build_run_lock,
)
from acryl_datahub_cloud.periodic_analytics.storage import ObjectStore
from acryl_datahub_cloud.periodic_analytics.system_usage_sync.gauge import (
    METRIC_DATA_ASSETS_STORED,
    METRIC_DATA_ASSETS_STORED_SOFT_DELETED,
    resolve_data_assets_stored_snapshot,
)
from acryl_datahub_cloud.periodic_analytics.system_usage_sync.openapi_counts import (
    fetch_entity_counts,
    resolve_counts_url,
)
from acryl_datahub_cloud.periodic_analytics.watermark import WatermarkStore
from datahub.configuration.common import ConfigurationError
from datahub.ingestion.api.common import PipelineContext
from datahub.ingestion.api.decorators import (
    SupportStatus,
    config_class,
    platform_name,
    support_status,
)
from datahub.ingestion.api.source import Source, SourceReport
from datahub.ingestion.api.workunit import MetadataWorkUnit
from datahub.ingestion.api.workunit_processor import WorkunitProcessor
from datahub.ingestion.workunit_processors.auto_workunits_reporter import (
    AutoWorkunitsReporterProcessor,
)

logger = logging.getLogger(__name__)


@dataclass
class PeriodicAnalyticsBillingSyncReport(SourceReport):
    deferred: bool = False
    metrics_computed: int = 0
    validation_failures: int = 0
    close_written: bool = False
    published: bool = False
    publish_dry_run: bool = False
    periods_written: List[str] = field(default_factory=list)
    periods_deferred: List[str] = field(default_factory=list)
    deltas_sent: int = 0
    deltas_skipped_zero: int = 0
    deltas_skipped_cadence: int = 0
    seals_without_emit: int = 0
    system_usage_quantity: Optional[int] = None
    system_usage_soft_deleted_quantity: Optional[int] = None
    system_usage_deferred: bool = False


@dataclass
class _PendingPublish:
    metric_name: str
    delta: int
    revision: int
    cumulative_mtd: int
    request: BillingUsageRequest
    is_replay: bool = False
    ledger_as_of: Optional[str] = None
    seal_hour: bool = False
    finalized_day: Optional[str] = None
    seal_period: bool = False


@platform_name(id="datahub", platform_name="datahub")
@config_class(BillingSyncSourceConfig)
@support_status(SupportStatus.INCUBATING)
class DataHubPeriodicAnalyticsBillingSyncSource(Source):
    def __init__(
        self,
        ctx: PipelineContext,
        config: BillingSyncSourceConfig,
        now_fn: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
        lock_client: Optional[LockClient] = None,
    ):
        super().__init__(ctx)
        self.config = config
        self.report = PeriodicAnalyticsBillingSyncReport()
        self.report.event_not_produced_warn = False
        self.job_run_id = ctx.run_id
        self.now_fn = now_fn
        self._ctx = ctx
        # Test-only override — bypasses provider dispatch in build_run_lock
        # so source-level lock tests don't need real S3/boto3.
        self._lock_client_override = lock_client
        # Set in get_workunits_internal once the lock is built, so
        # _verify_lock_ownership_or_abort can re-check the SAME lease object
        # right before each close-snapshot/ledger commit.
        self._run_lock: Optional[RunLock] = None

        if config.object_storage is None:
            return

        self.store = ObjectStore(config.object_storage)
        self.registry = MetricRegistry.load(config.metric_registry_override)
        self.usage_operations = load_usage_operations(config.usage_operations_path)
        self.hourly_wm = WatermarkStore(self.store, config.metric_family, Layer.HOURLY)
        self.daily_wm = WatermarkStore(
            self.store, config.metric_family, Layer.DAILY_ADDITIVE
        )
        self.publish_client: BillingPublishClient = self._build_publish_client(ctx)

    def close(self) -> None:
        store = getattr(self, "store", None)
        if store is not None:
            store.close()
        super().close()

    def _build_publish_client(self, ctx: PipelineContext) -> BillingPublishClient:
        if not self.config.publish_enabled:
            return DryRunBillingPublishClient()
        authorization = self._resolve_authorization_header(ctx)
        if not authorization:
            raise ConfigurationError(
                "publish_enabled=true requires a DataHub graph connection with an "
                "auth token (ctx.graph.config.token) or an Authorization header "
                "on the graph session to publish billing usage to GMS"
            )
        gms_server = ctx.graph.config.server if ctx.graph is not None else None
        publish_url = resolve_publish_url(self.config.gms_publish_url, gms_server)
        if not publish_url:
            raise ConfigurationError(
                "publish_enabled=true requires gms_publish_url or a DataHub graph "
                "connection (default datahub-rest sink) with config.server"
            )
        return HttpBillingPublishClient(
            gms_publish_url=publish_url, authorization=authorization
        )

    def _resolve_authorization_header(self, ctx: PipelineContext) -> Optional[str]:
        """Full Authorization header for GMS OpenAPI (Bearer or system Basic)."""
        if ctx.graph is None:
            return None
        if ctx.graph.config.token:
            return f"Bearer {ctx.graph.config.token}"
        raw_auth_header = ctx.graph._session.headers.get("Authorization")
        if raw_auth_header is None:
            return None
        return str(raw_auth_header)

    def get_report(self) -> SourceReport:
        return self.report

    def get_allowed_workunit_processors(
        self,
    ) -> Optional[List[Union[str, Type[WorkunitProcessor]]]]:
        return [AutoWorkunitsReporterProcessor]

    def get_workunits_internal(self) -> Iterable[MetadataWorkUnit]:
        if self.config.object_storage is None:
            self.report.warning(
                title="Periodic analytics billing-sync not configured",
                message="object_storage uri/bucket/customer_id/instance_id are unset "
                "— skipping this run (no-op) until "
                "DATAHUB_PERIODIC_ANALYTICS_BILLING_SYNC_BOOTSTRAP_VALUES is set "
                "(or DATAHUB_OBJECT_STORAGE_URI + BILLING_* env fallback)",
            )
            return

        self._run_lock = self._build_run_lock()
        with self._run_lock as acquired:
            if not acquired:
                # Mirrors the object_storage-unconfigured no-op above: the run
                # succeeds with zero workunits rather than failing, since a
                # concurrent run already owns this tenant+layer's work.
                self.report.warning(
                    title="Billing-sync skipped — run lock held",
                    message="another run of this source is already in progress "
                    "for this tenant; skipping this run (no-op)",
                    context=self.store.lock_key(
                        BILLING_SYNC_SOURCE_KIND, self.config.metric_family
                    ),
                )
                return
            self._run(self.now_fn())
        yield from []

    def _build_run_lock(self) -> RunLock:
        # Only called after get_workunits_internal's object_storage check, so
        # self.store (set in __init__ in that same branch) is always present.
        if self._lock_client_override is not None:
            return RunLock(
                client=self._lock_client_override,
                key=self.store.lock_key(
                    BILLING_SYNC_SOURCE_KIND, self.config.metric_family
                ),
                run_id=self.job_run_id,
                lease_minutes=self.config.lock_lease_minutes,
                report=self.report,
                now_fn=self.now_fn,
                steal_skew_minutes=self.config.lock_steal_skew_minutes,
            )
        return build_run_lock(
            self.store,
            BILLING_SYNC_SOURCE_KIND,
            self.config.metric_family,
            self.job_run_id,
            self.config.lock_lease_minutes,
            self.report,
            now_fn=self.now_fn,
            steal_skew_minutes=self.config.lock_steal_skew_minutes,
        )

    def _verify_lock_ownership_or_abort(self, context: str) -> None:
        # Called immediately before each close-snapshot/ledger commit below.
        # An overrunning run (lock_lease_minutes too short for this tenant's
        # real run time) can have its lease stolen mid-run; without this
        # check the old run would keep writing billing state after the steal
        # winner already owns the tenant, double-writing the same
        # close-snapshot/ledger entries the new owner is also writing.
        # self._run_lock is only None when _sync_period/_write_close/_publish
        # are exercised directly in a test, bypassing get_workunits_internal
        # (which always sets it before _run) -- nothing to verify there,
        # same as the client=None "no lock backend" case.
        if self._run_lock is None or self._run_lock.verify_ownership():
            return
        message = (
            "the run lock lease was stolen while this run was still "
            "executing (lock_lease_minutes too short for this run) -- "
            "another run now owns this tenant. Aborting before this "
            "commit rather than writing state the new owner also owns."
        )
        self.report.failure(
            title="Run lock ownership lost mid-run", message=message, context=context
        )
        raise RunLockOwnershipLostError(message)

    def _run(self, now: datetime) -> None:
        today = now.date()
        # Current calendar month is always a candidate (including the 1st) so
        # hourly metrics can emit as soon as the first hour of the period is
        # ready. Prior month stays eligible through stabilization / finalize.
        current_period = today.isoformat()[:7]

        periods_to_sync = self._periods_to_sync(today, current_period)
        logger.info(
            "billing-sync periods=%s publish_enabled=%s",
            [p for p, _ in periods_to_sync],
            self.config.publish_enabled,
        )
        for period, _hint_day in periods_to_sync:
            try:
                self._sync_period(period, now)
            except RunLockOwnershipLostError:
                # The tenant no longer belongs to this run -- continuing to
                # the next period would keep writing state the steal winner
                # also owns, exactly what I3's per-period isolation is NOT
                # meant to paper over. Report.failure already happened at
                # the commit site; stop the whole run here.
                raise
            except Exception as e:
                self.report.failure(
                    f"billing-sync: period {period} failed — continuing to "
                    "the next period",
                    exc=e,
                )
                continue

        try:
            self._sync_system_usage(now)
        except RunLockOwnershipLostError:
            raise
        except Exception as e:
            self.report.failure(
                "billing-sync: system_usage (data_assets_stored) failed",
                exc=e,
            )

    def _sync_system_usage(self, now: datetime) -> None:
        """Publish stored + soft_deleted gauges from sealed hourly latest buckets."""
        if not self.registry.metronome_names(SYSTEM_USAGE_METRIC_FAMILY):
            return

        as_of_hour = self._system_usage_eligible_as_of_hour(now)
        if as_of_hour is None:
            self.report.system_usage_deferred = True
            logger.info(
                "billing-sync system_usage: deferred — no sealed hourly "
                "watermark past input lag"
            )
            return

        billable_types = self._system_usage_billable_entity_types()
        snapshot = resolve_data_assets_stored_snapshot(
            self.store,
            SYSTEM_USAGE_METRIC_FAMILY,
            as_of_hour,
            billable_types,
            openapi_counts_fn=lambda: self._system_usage_openapi_counts(billable_types),
        )
        if snapshot is None:
            self.report.system_usage_deferred = True
            logger.info(
                "billing-sync system_usage: deferred — sealed hour %s has no "
                "LATEST samples and OpenAPI fallback unavailable",
                as_of_hour.key,
            )
            return

        self.report.system_usage_quantity = snapshot.stored
        self.report.system_usage_soft_deleted_quantity = snapshot.soft_deleted
        period = as_of_hour.day.month.key
        as_of = as_of_hour.key
        # Independent ledgers/pending intents per metric — process both every wake.
        self._publish_system_usage_absolute(
            METRIC_DATA_ASSETS_STORED, period, as_of, snapshot.stored
        )
        self._publish_system_usage_absolute(
            METRIC_DATA_ASSETS_STORED_SOFT_DELETED,
            period,
            as_of,
            snapshot.soft_deleted,
        )

    def _system_usage_eligible_as_of_hour(
        self, now: datetime
    ) -> Optional[HourPartition]:
        """Latest sealed system_usage hourly watermark whose input lag has elapsed.

        Unlike api_usage MTD, gauges do not require contiguity from month start —
        a mid-month rollup deploy should still publish from the newest sealed hour.
        """
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
        now_utc = now.astimezone(timezone.utc)
        lag = timedelta(minutes=self.config.input_lag.hourly_minutes)
        wm = WatermarkStore(self.store, SYSTEM_USAGE_METRIC_FAMILY, Layer.HOURLY)
        eligible: List[HourPartition] = []
        for key in wm.completed_keys():
            hour = HourPartition.from_key(key)
            if now_utc >= hour.end + lag:
                eligible.append(hour)
        if not eligible:
            return None
        return max(eligible, key=lambda h: h.key)

    def _system_usage_billable_entity_types(self) -> List[str]:
        if self.config.billable_entity_types:
            return list(self.config.billable_entity_types)
        spec = self.registry.metrics(SYSTEM_USAGE_METRIC_FAMILY).get(
            METRIC_DATA_ASSETS_STORED
        )
        if spec is None:
            raise ConfigurationError(
                f"{SYSTEM_USAGE_METRIC_FAMILY}.{METRIC_DATA_ASSETS_STORED} is not "
                "registered"
            )
        entity_types = spec.billable_entity_types
        if not entity_types:
            raise ConfigurationError(
                f"{SYSTEM_USAGE_METRIC_FAMILY}.{METRIC_DATA_ASSETS_STORED} requires "
                "rule_config.entity_types (set in registry) or recipe "
                "billable_entity_types override"
            )
        return entity_types

    def _system_usage_openapi_counts(
        self, billable_types: List[str]
    ) -> Optional[List[Dict]]:
        # Match other cloud SYSTEM sources: default to ctx.graph (executor
        # DATAHUB_GMS_* + system client auth) when recipe omits explicit URLs.
        graph = self._ctx.graph
        gms_server = graph.config.server if graph is not None else None
        # Same GMS resolution as publish: recipe gms_publish_url, else graph.server.
        publish_url = resolve_publish_url(self.config.gms_publish_url, gms_server)
        counts_url = resolve_counts_url(
            self.config.gms_entity_counts_url,
            publish_url,
            gms_server=gms_server,
        )
        authorization = self._resolve_authorization_header(self._ctx)
        if not counts_url or not authorization:
            return None
        return fetch_entity_counts(counts_url, authorization, billable_types)

    def _publish_system_usage_absolute(
        self, metric_name: str, period: str, as_of: str, quantity: int
    ) -> None:
        spec = self.registry.metrics(SYSTEM_USAGE_METRIC_FAMILY).get(metric_name)
        if spec is None or not spec.metronome_batch:
            raise ConfigurationError(
                f"{SYSTEM_USAGE_METRIC_FAMILY}.{metric_name} must be "
                "registered with metronome_batch=true"
            )
        if not spec.uses_max_snapshot:
            raise ConfigurationError(
                f"{metric_name} must use metronome_aggregation=max"
            )

        ledger = PublishLedger(self.store, SYSTEM_USAGE_METRIC_FAMILY, period)
        entry: Optional[LedgerEntry] = ledger.get(metric_name)

        # C1: pending intent must be replayed before any new emit — quantity and
        # transactionId come from the pending record (byte-identical resend).
        if entry is not None and entry.pending is not None:
            pending = entry.pending
            ledger_as_of = pending.as_of_date or as_of
            request = build_replay_request(
                metric_name=metric_name,
                pending=pending,
                period=period,
                as_of_date=as_of,
                finalized=pending.finalized,
                product=self.config.publish_product,
            )
            if isinstance(self.publish_client, DryRunBillingPublishClient):
                self.report.publish_dry_run = True
            self.publish_client.publish_one(request)
            self._verify_lock_ownership_or_abort(metric_name)
            ledger.record_success(metric_name, ledger_as_of)
            self.report.published = True
            self.report.deltas_sent += 1
            return

        last = entry.last_ingested_mtd if entry is not None else 0
        delta = quantity - last
        revision = (
            entry.revision + 1
            if entry is not None and entry.last_as_of_date == as_of
            else 1
        )

        # MAX: skip Metronome when absolute does not increase (peak retained).
        if delta <= 0:
            self.report.deltas_skipped_zero += 1
            seal_mtd = last if delta < 0 else quantity
            self._verify_lock_ownership_or_abort(metric_name)
            ledger.record_promoted(
                metric_name,
                seal_mtd,
                as_of,
                entry.revision if entry else 0,
                seal_hour=True,
            )
            logger.info(
                "billing-sync system_usage: skip Metronome metric=%s "
                "(quantity=%s last=%s delta=%s)",
                metric_name,
                quantity,
                last,
                delta,
            )
            return

        request = build_delta_request(
            metric_name=metric_name,
            delta=delta,
            revision=revision,
            period=period,
            as_of_date=as_of,
            finalized=True,
            product=self.config.publish_product,
            quantity=quantity,
        )
        request.transactionId = f"{period}_{metric_name}_{as_of}_r{revision}"

        if isinstance(self.publish_client, DryRunBillingPublishClient):
            self.report.publish_dry_run = True
            logger.info(
                "billing-sync system_usage dry-run publish: %s", request.model_dump()
            )
            self._verify_lock_ownership_or_abort(metric_name)
            ledger.record_promoted(
                metric_name,
                quantity,
                as_of,
                revision,
                seal_hour=True,
            )
        else:
            # Store emitted absolute quantity (not signed delta) so C1 replay
            # resends a byte-identical Metronome payload via pending.delta.
            self._verify_lock_ownership_or_abort(metric_name)
            ledger.record_intent(
                metric_name,
                request.quantity,
                quantity,
                as_of,
                revision,
                request.transactionId,
                finalized=True,
            )
            self.publish_client.publish_one(request)
            self._verify_lock_ownership_or_abort(metric_name)
            ledger.record_success(metric_name, as_of)
        self.report.published = True
        self.report.deltas_sent += 1

    def _periods_to_sync(
        self, today: date, current_period: str
    ) -> List[Tuple[str, str]]:
        current_period_first_day = date.fromisoformat(f"{current_period}-01")
        prior_last_day = current_period_first_day - timedelta(days=1)
        prior_period = prior_last_day.isoformat()[:7]

        candidates: List[Tuple[str, str]] = [
            (prior_period, prior_last_day.isoformat()),
            (current_period, today.isoformat()),
        ]
        periods: List[Tuple[str, str]] = []
        for period, as_of_date in candidates:
            close = read_latest_close(self.store, self.config.metric_family, period)
            if close is None or not close.finalized:
                periods.append((period, as_of_date))
                continue
            # Finalized periods with pending intents stay eligible for replay.
            ledger = PublishLedger(self.store, self.config.metric_family, period)
            if ledger.has_pending():
                periods.append((period, as_of_date))
        return periods

    def _sync_period(self, period: str, now: datetime) -> None:
        hourly_completed = set(self.hourly_wm.completed_keys())
        as_of_hour = resolve_contiguous_as_of_hour(
            period,
            hourly_completed,
            now,
            self.config.input_lag.hourly_minutes,
        )
        if as_of_hour is None:
            self.report.deferred = True
            self.report.periods_deferred.append(period)
            logger.info(
                "period %s not ready — no contiguous hourly watermark through "
                "input lag; deferring",
                period,
            )
            return

        daily_completed = set(self.daily_wm.completed_keys())
        month_final_due = self._is_month_final_due(period, now, as_of_hour)

        logger.info(
            "billing-sync period=%s as_of_hour=%s month_final_due=%s",
            period,
            as_of_hour.key,
            month_final_due,
        )

        mtd = compute_mtd(
            self.store,
            self.registry,
            self.config.metric_family,
            period,
            as_of_hour,
            self.config.billing_excluded_identities,
            self.daily_wm,
            self.hourly_wm,
            daily_completed=daily_completed,
        )
        self.report.metrics_computed = len(mtd)

        derived = compute_derived_metrics(
            self.store,
            self.registry,
            self.usage_operations,
            self.config.metric_family,
            period,
            as_of_hour,
            self.config.billing_excluded_identities,
            self.report,
            self.daily_wm,
            self.hourly_wm,
            daily_completed=daily_completed,
        )
        close_metrics = self._merge_derived(mtd, derived)
        self._log_metronome_batch_mtd(period, close_metrics)

        ledger = PublishLedger(self.store, self.config.metric_family, period)
        self._warn_post_seal_divergence(ledger, mtd, as_of_hour)
        self._validate(mtd, period, ledger)

        pending = self._build_pending_publishes(
            ledger, mtd, period, as_of_hour, month_final_due
        )
        self._publish(as_of_hour.key, pending, ledger)

        period_locked = self._should_lock_period(
            period, month_final_due, ledger, as_of_hour
        )
        self._write_close(period, as_of_hour.key, close_metrics, period_locked)
        logger.info(
            "billing-sync period=%s close written finalized=%s",
            period,
            period_locked,
        )

    def _log_metronome_batch_mtd(self, period: str, metrics: Dict[str, int]) -> None:
        # Always summarize metronome_batch metrics (including zero-delta /
        # dry-run skips) so operators can see MTD without relying on publish
        # payload logs. Include dimensional MTD keys (api_calls\x1f...).
        names = self.registry.metronome_names(self.config.metric_family)
        if not names:
            return
        parts: List[str] = []
        for name in sorted(names):
            dim_keys = sorted(
                k for k in metrics if k == name or k.startswith(name + "\x1f")
            )
            if dim_keys:
                for key in dim_keys:
                    parts.append(f"{self._format_mtd_log_key(key)}={metrics[key]}")
            else:
                parts.append(f"{name}={metrics.get(name, 0)}")
        logger.info(
            "billing-sync period=%s metronome_batch %s", period, " ".join(parts)
        )

    @staticmethod
    def _format_mtd_log_key(mtd_key: str) -> str:
        base, dims = parse_mtd_key(mtd_key)
        if not dims:
            return base
        dim_s = ",".join(f"{k}={v}" for k, v in sorted(dims.items()))
        return f"{base}[{dim_s}]"

    def _is_month_final_due(
        self, period: str, now: datetime, as_of_hour: HourPartition
    ) -> bool:
        if now <= self._stabilization_end(period):
            return False
        return as_of_hour.key >= last_hour_of_period(period).key

    def _should_lock_period(
        self,
        period: str,
        month_final_due: bool,
        ledger: PublishLedger,
        as_of_hour: HourPartition,
    ) -> bool:
        if not month_final_due or ledger.has_pending():
            return False
        if not self._month_final_metrics_sealed(ledger):
            return False
        last = last_hour_of_period(period)
        if not self._sub_month_metrics_sealed_through(ledger, last.key):
            return False
        return as_of_hour.key >= last.key

    def _month_final_metrics_sealed(self, ledger: PublishLedger) -> bool:
        for name in self.registry.metronome_names(self.config.metric_family):
            spec = self.registry.spec(self.config.metric_family, name)
            if not spec.is_month_final:
                continue
            entries = self._ledger_entries_for(ledger, name)
            if not entries or any(not entry.period_sealed for entry in entries):
                return False
        return True

    def _sub_month_metrics_sealed_through(
        self, ledger: PublishLedger, last_hour_key: str
    ) -> bool:
        for name in self.registry.metronome_names(self.config.metric_family):
            spec = self.registry.spec(self.config.metric_family, name)
            if spec.is_month_final:
                continue
            entries = self._ledger_entries_for(ledger, name)
            if not entries:
                # Idle dimensional metrics never wrote a ledger row — don't
                # block period lock.
                if spec.metronome_dimensions:
                    continue
                return False
            for entry in entries:
                sealed = entry.sealed_through_as_of
                if sealed is None or sealed < last_hour_key:
                    return False
        return True

    @staticmethod
    def _ledger_entries_for(
        ledger: PublishLedger, metric_name: str
    ) -> List[LedgerEntry]:
        entries: List[LedgerEntry] = []
        for key in ledger.metric_names():
            if base_metric_name(key) != metric_name:
                continue
            entry = ledger.get(key)
            if entry is not None:
                entries.append(entry)
        return entries

    def _merge_derived(
        self, mtd: Dict[str, int], derived: Dict[str, int]
    ) -> Dict[str, int]:
        close_metrics = dict(mtd)
        for name, value in derived.items():
            spec = self.registry.spec(self.config.metric_family, name)
            if spec.metronome_batch:
                mtd[name] = value
            close_metrics[name] = value
        return close_metrics

    def _validate(
        self, mtd: Dict[str, int], period: str, ledger: PublishLedger
    ) -> None:
        try:
            prior = read_latest_close(self.store, self.config.metric_family, period)
            # Replay-only path for pending intents may still enter.
            if prior and prior.finalized and not ledger.has_pending():
                raise BillingValidationError(
                    ["period already finalized — restate/re-publish forbidden"]
                )
            ledger_baseline: Dict[str, int] = {}
            for name in ledger.metric_names():
                entry = ledger.get(name)
                if entry is not None:
                    ledger_baseline[name] = entry.last_ingested_mtd
            family_metrics = self.registry.metrics(self.config.metric_family)
            metric_aggregations = {
                name: spec.metronome_aggregation
                for name, spec in family_metrics.items()
            }
            # Dimensional metronome metrics (e.g. api_calls × request_api) are
            # omitted when idle — do not require a flat zero key.
            required_metrics = [
                name
                for name in self.registry.metronome_names(self.config.metric_family)
                if not family_metrics[name].metronome_dimensions
            ]
            warnings = validate_mtd(
                mtd,
                prior.metrics if prior else None,
                required_metrics=required_metrics,
                ledger_baseline=ledger_baseline,
                allow_mtd_correction=self.config.allow_mtd_correction,
                metric_aggregations=metric_aggregations,
            )
            for message in warnings:
                self.report.warning(
                    title="MTD regression (non-fatal)",
                    message=message,
                    context=period,
                )
        except BillingValidationError:
            self.report.validation_failures += 1
            raise

    def _warn_post_seal_divergence(
        self,
        ledger: PublishLedger,
        mtd: Dict[str, int],
        as_of_hour: HourPartition,
    ) -> None:
        for name, current in mtd.items():
            entry = ledger.get(name)
            if entry is None:
                continue
            if name not in self.registry.metrics(self.config.metric_family):
                continue
            spec = self.registry.spec(self.config.metric_family, name)
            sealed = self._is_sealed(spec, entry, as_of_hour)
            if sealed and current > entry.last_ingested_mtd:
                self.report.warning(
                    title="Late data after seal (not emitted)",
                    message=(
                        f"metric {name}: computed MTD {current} exceeds last "
                        f"emitted {entry.last_ingested_mtd} after seal — "
                        "close snapshot updated; Metronome not re-emitted"
                    ),
                    context=as_of_hour.key,
                )

    def _is_sealed(
        self, spec: MetricSpec, entry: LedgerEntry, as_of_hour: HourPartition
    ) -> bool:
        if spec.is_month_final:
            return entry.period_sealed
        if entry.sealed_through_as_of is None:
            return False
        return as_of_hour.key <= entry.sealed_through_as_of

    def _is_hour_grain_due(
        self,
        spec: MetricSpec,
        entry: Optional[LedgerEntry],
        as_of_hour: HourPartition,
    ) -> bool:
        sealed = entry.sealed_through_as_of if entry else None
        if sealed is not None and as_of_hour.key <= sealed:
            return False
        if spec.publish_cadence != "daily":
            return True
        if as_of_hour.hour != 23:
            return False
        return sealed is None or as_of_hour.key > sealed

    def _is_month_progress_due(
        self,
        spec: MetricSpec,
        entry: Optional[LedgerEntry],
        as_of_hour: HourPartition,
    ) -> bool:
        last = entry.last_as_of_date if entry else None
        if last is None:
            return spec.publish_cadence != "daily" or (
                as_of_hour.hour == 23 or as_of_hour.dt[-2:] != "01"
            )
        if spec.publish_cadence == "daily":
            if as_of_hour.hour == 23 and as_of_hour.key > last:
                return True
            last_date = date.fromisoformat(last[:10])
            as_of_date = date.fromisoformat(as_of_hour.dt)
            if as_of_date <= last_date:
                return False
            last_hour = int(last[-2:]) if "T" in last else 23
            return last_hour < 23 or (as_of_date - last_date).days > 1
        return as_of_hour.key > last

    def _completed_day(self, as_of_hour: HourPartition) -> date:
        as_of_date = date.fromisoformat(as_of_hour.dt)
        if as_of_hour.hour == 23:
            return as_of_date
        return as_of_date - timedelta(days=1)

    def _day_boundary_as_of(self, finalized_day: str) -> str:
        return f"{finalized_day}T23"

    def _day_to_finalize(
        self,
        entry: Optional[LedgerEntry],
        period: str,
        as_of_hour: HourPartition,
    ) -> Optional[str]:
        completed_day = self._completed_day(as_of_hour)
        if completed_day.isoformat()[:7] != period:
            return None
        if (
            entry is not None
            and entry.last_finalized_day is not None
            and completed_day.isoformat() <= entry.last_finalized_day
        ):
            return None
        return completed_day.isoformat()

    def _metrics_through_hour(
        self, period: str, as_of_hour: HourPartition
    ) -> Dict[str, int]:
        """Publishable MTD (incl. metronome derived) through ``as_of_hour``."""
        daily_completed = set(self.daily_wm.completed_keys())
        mtd = compute_mtd(
            self.store,
            self.registry,
            self.config.metric_family,
            period,
            as_of_hour,
            self.config.billing_excluded_identities,
            self.daily_wm,
            self.hourly_wm,
            daily_completed=daily_completed,
        )
        derived = compute_derived_metrics(
            self.store,
            self.registry,
            self.usage_operations,
            self.config.metric_family,
            period,
            as_of_hour,
            self.config.billing_excluded_identities,
            self.report,
            self.daily_wm,
            self.hourly_wm,
            daily_completed=daily_completed,
        )
        self._merge_derived(mtd, derived)
        return mtd

    def _is_due(
        self,
        spec: MetricSpec,
        entry: Optional[LedgerEntry],
        as_of_hour: HourPartition,
        month_final_due: bool,
    ) -> bool:
        if entry is not None and self._is_sealed(spec, entry, as_of_hour):
            return False
        if spec.is_month_final and month_final_due:
            return True
        if spec.publish_cadence == "monthly":
            return False
        if spec.is_hour_final:
            return self._is_hour_grain_due(spec, entry, as_of_hour)
        return self._is_month_progress_due(spec, entry, as_of_hour)

    def _stabilization_end(self, period: str) -> datetime:
        last_day_of_period = date.fromisoformat(
            MonthPartition.from_key(period).days[-1].key
        )
        period_close = datetime(
            last_day_of_period.year,
            last_day_of_period.month,
            last_day_of_period.day,
            tzinfo=timezone.utc,
        ) + timedelta(days=1)
        return period_close + timedelta(
            seconds=self.config.stabilization_seconds_after_close
        )

    def _write_close(
        self, period: str, as_of_hour: str, mtd: Dict[str, int], finalized: bool
    ) -> None:
        self._verify_lock_ownership_or_abort(period)
        snapshot = CloseSnapshot(
            period=period,
            as_of_hour=as_of_hour,
            finalized=finalized,
            metrics=mtd,
        )
        write_close(self.store, self.config.metric_family, snapshot, self.job_run_id)
        self.report.close_written = True
        self.report.periods_written.append(period)

    def _flat_superseded_by_dimensions(
        self,
        metric: str,
        spec: Optional[MetricSpec],
        emit_mtd: Dict[str, int],
    ) -> bool:
        """True when a flat ledger leftover should auto-zero after dim breakout."""
        return (
            spec is not None
            and bool(spec.metronome_dimensions)
            and is_flat_mtd_key(metric)
            and mtd_has_dimensional_keys(emit_mtd, metric)
        )

    def _guard_negative_sum_delta(
        self,
        metric: str,
        spec: Optional[MetricSpec],
        emit_mtd: Dict[str, int],
        *,
        last: int,
        current: int,
        delta: int,
        use_absolute: bool,
        period: str,
    ) -> None:
        # LATEST snapshots may decrease (correction); SUM deltas need the
        # allow_mtd_correction gate for negative adjustments. MAX decreases
        # are handled as no_billable_change before this runs.
        #
        # Flat→dimensional: once MTD emits any metronome_dimensions key,
        # a prior flat ledger entry for the same base metric is superseded.
        # Auto-allow the signed zeroing delta (same Metronome eventType as
        # the dim breakouts, so the vendor net stays correct) without
        # requiring allow_mtd_correction. Flat leftovers with no dim keys
        # yet still hard-fail like any other disappearing metric.
        if use_absolute or delta >= 0:
            return
        if self._flat_superseded_by_dimensions(metric, spec, emit_mtd):
            self.report.warning(
                title="Flat ledger key superseded by dimensions",
                message=(
                    f"{metric}: retiring flat ledger entry "
                    f"(last={last}) after metronome_dimensions "
                    f"breakout; publishing signed delta {delta}"
                ),
                context=period,
            )
            return
        if not self.config.allow_mtd_correction:
            raise ValueError(
                f"MTD for metric {metric} decreased from {last} to "
                f"{current} (delta {delta}) vs the publish ledger — "
                "refusing to publish a negative delta. Set "
                "allow_mtd_correction=true to allow signed adjustment "
                "deltas for corrections."
            )

    def _build_pending_publishes(
        self,
        ledger: PublishLedger,
        mtd: Dict[str, int],
        period: str,
        as_of_hour: HourPartition,
        month_final_due: bool,
    ) -> List[_PendingPublish]:
        # get_workunits_internal returns before _sync_period (and thus this
        # method) is ever reached when object_storage is unconfigured.
        assert self.config.object_storage is not None
        as_of = as_of_hour.key

        pending: List[_PendingPublish] = []
        metric_names = sorted(set(mtd) | set(ledger.metric_names()))
        family_metrics = self.registry.metrics(self.config.metric_family)
        for metric in metric_names:
            spec: Optional[MetricSpec] = family_metrics.get(base_metric_name(metric))
            entry = ledger.get(metric)
            # Still process ledger leftovers (activation transition / flag
            # flipped off) so corrections and zeroing can run.
            if (
                spec is not None
                and not spec.metronome_batch
                and (
                    entry is None
                    or (entry.last_ingested_mtd == 0 and entry.pending is None)
                )
            ):
                continue

            if entry is not None and entry.pending is not None:
                request_finalized = entry.pending.finalized
                pending_as_of = entry.pending.as_of_date or as_of
                finalized_day = (
                    self._completed_day(
                        HourPartition.from_key(pending_as_of)
                    ).isoformat()
                    if spec is not None and spec.is_day_final and request_finalized
                    else None
                )
                # Prefer the day boundary when replaying a day-final intent that
                # was recorded against a mid-next-day wake (pre-fix ledgers).
                if finalized_day is not None:
                    pending_as_of = self._day_boundary_as_of(finalized_day)
                request = build_replay_request(
                    metric_name=metric,
                    pending=entry.pending,
                    period=period,
                    as_of_date=as_of,
                    finalized=request_finalized,
                    product=self.config.publish_product,
                )
                pending.append(
                    _PendingPublish(
                        metric_name=metric,
                        delta=entry.pending.delta,
                        revision=entry.pending.revision,
                        cumulative_mtd=entry.pending.cumulative_mtd,
                        request=request,
                        is_replay=True,
                        ledger_as_of=pending_as_of,
                        seal_hour=(
                            (spec is None or spec.is_hour_or_day_final)
                            and request_finalized
                        ),
                        finalized_day=finalized_day,
                        seal_period=(
                            spec is not None
                            and spec.is_month_final
                            and request_finalized
                        ),
                    )
                )
                continue

            if spec is not None and not self._is_due(
                spec, entry, as_of_hour, month_final_due
            ):
                self.report.deltas_skipped_cadence += 1
                continue

            finalized_day = (
                self._day_to_finalize(entry, period, as_of_hour)
                if spec is not None and spec.is_day_final
                else None
            )
            # Day-final catch-up must land on the completed day's last hour,
            # not the wake's mid-next-day as_of (which would include later hours
            # in a finalized day-boundary emit).
            emit_as_of = (
                self._day_boundary_as_of(finalized_day)
                if finalized_day is not None
                else as_of
            )
            emit_mtd = mtd
            if emit_as_of != as_of:
                emit_mtd = self._metrics_through_hour(
                    period, HourPartition.from_key(emit_as_of)
                )
            request_finalized = (
                spec is None
                or spec.is_hour_final
                or finalized_day is not None
                or (spec.is_month_final and month_final_due)
            )
            current = emit_mtd.get(metric, 0)
            last = entry.last_ingested_mtd if entry is not None else 0
            delta = current - last
            use_absolute = spec is not None and spec.uses_absolute_snapshot
            use_max = spec is not None and spec.uses_max_snapshot
            # SUM: quantity = signed delta. LATEST/MAX: absolute MTD.
            # MAX only emits when current > last (high-water); LATEST emits
            # on any change (including decreases).
            emitted_quantity = current if use_absolute else delta
            seal_through = request_finalized and (
                spec is None or spec.is_hour_or_day_final
            )

            # No billable change: unchanged absolute, or MAX with a decrease
            # (Metronome MAX cannot unwind a prior high-water mark).
            no_billable_change = delta == 0 or (use_max and delta < 0)
            if no_billable_change:
                self.report.deltas_skipped_zero += 1
                if request_finalized:
                    # Local seal — no Metronome call. Keep ledger at the
                    # last emitted high-water for MAX decreases.
                    seal_mtd = last if (use_max and delta < 0) else current
                    pending.append(
                        _PendingPublish(
                            metric_name=metric,
                            delta=0,
                            revision=entry.revision if entry else 0,
                            cumulative_mtd=seal_mtd,
                            request=build_delta_request(
                                metric_name=metric,
                                delta=0,
                                revision=1,
                                period=period,
                                as_of_date=emit_as_of,
                                finalized=True,
                                product=self.config.publish_product,
                                quantity=0,
                            ),
                            is_replay=False,
                            ledger_as_of=emit_as_of,
                            seal_hour=seal_through,
                            finalized_day=finalized_day,
                            seal_period=(spec is not None and spec.is_month_final),
                        )
                    )
                continue

            # LATEST / SUM negative-delta gate (MAX decreases handled above).
            self._guard_negative_sum_delta(
                metric,
                spec,
                emit_mtd,
                last=last,
                current=current,
                delta=delta,
                use_absolute=use_absolute,
                period=period,
            )
            revision = (
                entry.revision + 1
                if entry is not None and entry.last_as_of_date == emit_as_of
                else 1
            )
            request = build_delta_request(
                metric_name=metric,
                delta=delta,
                revision=revision,
                period=period,
                as_of_date=emit_as_of,
                finalized=request_finalized,
                product=self.config.publish_product,
                quantity=emitted_quantity,
            )
            pending.append(
                _PendingPublish(
                    metric_name=metric,
                    # Ledger pending.delta stores the emitted quantity so
                    # C1 replay resends the identical Metronome payload.
                    delta=emitted_quantity,
                    revision=revision,
                    cumulative_mtd=current,
                    request=request,
                    is_replay=False,
                    ledger_as_of=emit_as_of,
                    seal_hour=seal_through,
                    finalized_day=finalized_day,
                    seal_period=(
                        spec is not None and spec.is_month_final and request_finalized
                    ),
                )
            )
        return pending

    def _record_day_finalization(
        self, ledger: PublishLedger, item: _PendingPublish
    ) -> None:
        if item.finalized_day is not None:
            ledger.mark_day_finalized(item.metric_name, item.finalized_day)

    def _publish(
        self,
        as_of: str,
        pending: List[_PendingPublish],
        ledger: PublishLedger,
    ) -> None:
        for item in pending:
            item_as_of = item.ledger_as_of or as_of
            if item.delta == 0 and not item.is_replay:
                self._seal_without_emit(ledger, item, item_as_of)
                continue
            if not self._publish_one(ledger, item, item_as_of):
                return

        if self.config.publish_enabled:
            self.report.published = True

    def _seal_without_emit(
        self, ledger: PublishLedger, item: _PendingPublish, item_as_of: str
    ) -> None:
        # Zero-delta seal: bookkeeping only.
        ledger.record_promoted(
            item.metric_name,
            item.cumulative_mtd,
            item_as_of,
            item.revision,
            seal_hour=item.seal_hour,
            seal_period=item.seal_period,
        )
        self._record_day_finalization(ledger, item)
        self.report.seals_without_emit += 1

    def _publish_one(
        self, ledger: PublishLedger, item: _PendingPublish, item_as_of: str
    ) -> bool:
        # Returns False to stop _publish's loop early (a send/ledger-write
        # failure for this item); True to continue to the next item. Lets
        # RunLockOwnershipLostError propagate to abort the whole run.
        try:
            if not item.is_replay:
                # Store the emitted quantity (SUM delta or LATEST absolute)
                # so C1 replay resends a byte-identical Metronome payload.
                # Verify ownership immediately before this ledger write --
                # a crash between this line and the send (or between the
                # send and record_success below) leaves a pending record
                # that the next run's `_build_pending_publishes` replays
                # verbatim instead of recomputing against a possibly-
                # changed MTD, so a stolen-lease run must not get here.
                self._verify_lock_ownership_or_abort(item.metric_name)
                ledger.record_intent(
                    item.metric_name,
                    item.request.quantity,
                    item.cumulative_mtd,
                    item_as_of,
                    item.revision,
                    item.request.transactionId,
                    finalized=bool(item.request.properties.get("finalized")),
                )
            self.publish_client.publish_one(item.request)
        except RunLockOwnershipLostError:
            # The tenant no longer belongs to this run -- stopping at
            # "un-ingested in the ledger, heals next run" (the comment
            # below) is not enough here, since the steal winner may
            # already be writing the same ledger/close state. Propagate
            # rather than treating this like an ordinary publish failure.
            raise
        except Exception as e:
            self.report.failure(
                f"billing-sync: failed to publish metric {item.metric_name}",
                exc=e,
            )
            return False

        try:
            # M5: a ledger-write failure here is symmetric with a send
            # failure above — stop the loop rather than let it propagate
            # uncaught, since the send already happened and the C1 replay
            # record makes it safe to pick this metric back up next run.
            self._verify_lock_ownership_or_abort(item.metric_name)
            ledger.record_success(item.metric_name, item_as_of)
            self._record_day_finalization(ledger, item)
            if item.seal_period:
                ledger.mark_period_sealed(item.metric_name)
        except RunLockOwnershipLostError:
            raise
        except Exception as e:
            self.report.failure(
                "billing-sync: failed to record publish ledger success "
                f"for metric {item.metric_name}",
                exc=e,
            )
            return False

        if not self.config.publish_enabled:
            self.report.publish_dry_run = True
        else:
            self.report.deltas_sent += 1
        return True
