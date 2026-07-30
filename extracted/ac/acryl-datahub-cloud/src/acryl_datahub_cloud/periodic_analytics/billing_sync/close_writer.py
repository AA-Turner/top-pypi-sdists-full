import posixpath
from typing import Any, Dict, Optional

import polars as pl
from pydantic import BaseModel, model_validator

from acryl_datahub_cloud.periodic_analytics.constants import SCHEMA_VERSION, Layer
from acryl_datahub_cloud.periodic_analytics.storage import ObjectStore


class CloseSnapshot(BaseModel):
    period: str
    as_of_hour: str
    finalized: bool
    metrics: Dict[str, int]

    @model_validator(mode="before")
    @classmethod
    def _coerce_as_of(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        if "as_of_hour" not in data and "as_of_date" in data:
            as_of = str(data["as_of_date"])
            data = {
                **data,
                "as_of_hour": as_of if "T" in as_of else f"{as_of}T23",
            }
        return data

    @property
    def as_of_date(self) -> str:
        return self.as_of_hour[:10]


def write_close(
    store: ObjectStore, metric_family: str, snapshot: CloseSnapshot, job_run_id: str
) -> str:
    df = pl.DataFrame(
        [
            {
                "customer_id": store.config.customer_id,
                "instance_id": store.config.instance_id,
                "metric_family": metric_family,
                "metric_name": name,
                "value_sum": value,
                "period": snapshot.period,
                "as_of_hour": snapshot.as_of_hour,
                "as_of_date": snapshot.as_of_date,
                "finalized": snapshot.finalized,
                "job_run_id": job_run_id,
                "schema_version": SCHEMA_VERSION,
            }
            for name, value in sorted(snapshot.metrics.items())
        ]
    )
    return store.write_parquet(
        df,
        store.period_dir(metric_family, Layer.BILLING_CLOSE, snapshot.period),
        f"close-{snapshot.as_of_hour}.parquet",
    )


def read_latest_close(
    store: ObjectStore, metric_family: str, period: str
) -> Optional[CloseSnapshot]:
    period_dir = store.period_dir(metric_family, Layer.BILLING_CLOSE, period)
    files = store.list_parquet_files(period_dir)
    if not files:
        return None
    latest = max(files, key=lambda f: posixpath.basename(f))
    df = store.scan_parquet([latest]).collect(engine="streaming")
    as_of_hour = (
        str(df["as_of_hour"][0])
        if "as_of_hour" in df.columns
        else str(df["as_of_date"][0])
    )
    if "T" not in as_of_hour:
        as_of_hour = f"{as_of_hour}T23"
    return CloseSnapshot(
        period=period,
        as_of_hour=as_of_hour,
        finalized=bool(df["finalized"][0]),
        metrics={
            row["metric_name"]: int(row["value_sum"])
            for row in df.iter_rows(named=True)
        },
    )
