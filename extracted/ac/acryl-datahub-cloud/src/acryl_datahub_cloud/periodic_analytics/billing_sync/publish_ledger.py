import posixpath
from typing import Dict, List, Optional

from pydantic import BaseModel

from acryl_datahub_cloud.periodic_analytics.constants import MANIFESTS_DIR
from acryl_datahub_cloud.periodic_analytics.storage import ObjectStore

_LEDGER_SUBDIR = "billing_publish"


class PendingIntent(BaseModel):
    """A recorded intent to send a request, before its success is confirmed."""

    revision: int
    delta: int
    cumulative_mtd: int
    transaction_id: str
    finalized: bool = False
    as_of_date: Optional[str] = None


class LedgerEntry(BaseModel):
    last_ingested_mtd: int = 0
    # Hour-precision as_of key (YYYY-MM-DDTHH); legacy day keys still read.
    last_as_of_date: Optional[str] = None
    revision: int = 0
    pending: Optional[PendingIntent] = None
    # Sub-month final: last as_of through which this metric is sealed.
    sealed_through_as_of: Optional[str] = None
    # Day-final: last UTC calendar day whose completion was finalized.
    last_finalized_day: Optional[str] = None
    # Month-final: period sealed for this metric after month finalization.
    period_sealed: bool = False


class PublishLedger:
    """R15 ledger: last successfully ingested MTD per metric for a period."""

    def __init__(self, store: ObjectStore, metric_family: str, period: str) -> None:
        self._store = store
        self._period = period
        self._path = posixpath.join(
            store.family_root(metric_family),
            MANIFESTS_DIR,
            _LEDGER_SUBDIR,
            f"{period}.json",
        )
        self._cache: Optional[Dict[str, LedgerEntry]] = None

    def _metrics(self) -> Dict[str, LedgerEntry]:
        if self._cache is None:
            manifest = self._store.read_json(self._path) or {}
            self._cache = {
                metric: LedgerEntry.model_validate(entry)
                for metric, entry in manifest.get("metrics", {}).items()
            }
        return self._cache

    def _persist(self, metrics: Dict[str, LedgerEntry]) -> None:
        self._store.write_json(
            self._path,
            {
                "period": self._period,
                "metrics": {
                    name: entry.model_dump() for name, entry in metrics.items()
                },
            },
        )

    def get(self, metric: str) -> Optional[LedgerEntry]:
        return self._metrics().get(metric)

    def metric_names(self) -> List[str]:
        return list(self._metrics().keys())

    def has_pending(self) -> bool:
        return any(e.pending is not None for e in self._metrics().values())

    def record_intent(
        self,
        metric: str,
        delta: int,
        cumulative_mtd: int,
        as_of_date: str,
        revision: int,
        transaction_id: str,
        finalized: bool = False,
    ) -> None:
        metrics = self._metrics()
        existing = metrics.get(metric)
        metrics[metric] = LedgerEntry(
            last_ingested_mtd=existing.last_ingested_mtd if existing else 0,
            last_as_of_date=existing.last_as_of_date if existing else None,
            revision=existing.revision if existing else 0,
            sealed_through_as_of=(existing.sealed_through_as_of if existing else None),
            last_finalized_day=(existing.last_finalized_day if existing else None),
            period_sealed=existing.period_sealed if existing else False,
            pending=PendingIntent(
                revision=revision,
                delta=delta,
                cumulative_mtd=cumulative_mtd,
                transaction_id=transaction_id,
                finalized=finalized,
                as_of_date=as_of_date,
            ),
        )
        self._persist(metrics)

    def record_success(self, metric: str, as_of_date: str) -> None:
        metrics = self._metrics()
        entry = metrics.get(metric)
        if entry is None or entry.pending is None:
            raise RuntimeError(
                f"record_success called for metric {metric!r} with no pending "
                "intent recorded — record_intent must be called before "
                "record_success (two-phase publish invariant)"
            )
        pending = entry.pending
        sealed_through = entry.sealed_through_as_of
        period_sealed = entry.period_sealed
        if pending.finalized:
            sealed_through = as_of_date
            # Month-final seals use as_of at/after period end; callers also
            # set period_sealed via record_seal when finalize_grain=month.
        metrics[metric] = LedgerEntry(
            last_ingested_mtd=pending.cumulative_mtd,
            last_as_of_date=as_of_date,
            revision=pending.revision,
            pending=None,
            sealed_through_as_of=sealed_through,
            last_finalized_day=entry.last_finalized_day,
            period_sealed=period_sealed,
        )
        self._persist(metrics)

    def record_promoted(
        self,
        metric: str,
        cumulative_mtd: int,
        as_of: str,
        revision: int,
        *,
        seal_hour: bool = False,
        seal_period: bool = False,
    ) -> None:
        """Advance ledger without a pending intent (dry-run emit or zero-delta seal)."""
        metrics = self._metrics()
        existing = metrics.get(metric)
        sealed_through = existing.sealed_through_as_of if existing else None
        period_sealed = existing.period_sealed if existing else False
        if seal_hour:
            sealed_through = as_of
        if seal_period:
            period_sealed = True
            sealed_through = as_of
        metrics[metric] = LedgerEntry(
            last_ingested_mtd=cumulative_mtd,
            last_as_of_date=as_of,
            revision=revision,
            pending=None,
            sealed_through_as_of=sealed_through,
            last_finalized_day=(existing.last_finalized_day if existing else None),
            period_sealed=period_sealed,
        )
        self._persist(metrics)

    def mark_period_sealed(self, metric: str) -> None:
        metrics = self._metrics()
        existing = metrics.get(metric) or LedgerEntry()
        metrics[metric] = existing.model_copy(update={"period_sealed": True})
        self._persist(metrics)

    def mark_day_finalized(self, metric: str, finalized_day: str) -> None:
        metrics = self._metrics()
        existing = metrics.get(metric) or LedgerEntry()
        metrics[metric] = existing.model_copy(
            update={"last_finalized_day": finalized_day}
        )
        self._persist(metrics)
