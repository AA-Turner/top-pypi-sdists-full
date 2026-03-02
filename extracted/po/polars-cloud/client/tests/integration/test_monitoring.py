# mypy: disable-error-code="no-untyped-def"

import os
import time
from datetime import datetime, timedelta, timezone
from uuid import UUID

import polars as pl
import polars_cloud as pc
import pytest
import requests
from polars.testing import assert_frame_equal
from polars_cloud import ComputeContext

from tests.integration.conftest import encode_auth_headers

from .conftest import ComputeContextSpecsInput  # noqa: TID252

# This applies the monitoring mark at the module level
pytestmark = pytest.mark.monitoring


def prometheus_query_params(query: str):
    start = datetime.now(timezone.utc) - timedelta(seconds=60 * 30)
    end = datetime.now(timezone.utc)
    interval_seconds = 60
    return {
        "query": query,
        "start": round(start.timestamp()),
        "end": round(end.timestamp()),
        "step": interval_seconds,
    }


def prometheus_output_available(cluster_id: UUID) -> bool:
    resp = requests.post(
        url=f"{os.environ['CI_PROMETHEUS_ENDPOINT']}/api/prom/api/v1/query_range",
        headers=encode_auth_headers(
            os.environ["CI_PROMETHEUS_USER"],
            os.environ["CI_GRAFANA_TOKEN"],
        ),
        params=prometheus_query_params(
            f'system_memory_utilization_ratio{{cluster_id="{cluster_id!s}"}}'
        ),
    )

    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        msg = f"checking prometheus output failed: {resp.json()}"
        raise RuntimeError(msg) from e

    json = resp.json()
    return len(json["data"]["result"]) != 0


def loki_output_available(cluster_id: UUID) -> bool:
    resp = requests.post(
        url=f"{os.environ['CI_LOKI_ENDPOINT']}/loki/api/v1/query_range",
        headers=encode_auth_headers(
            os.environ["CI_LOKI_USER"],
            os.environ["CI_GRAFANA_TOKEN"],
        ),
        params={
            "query": f'{{service_name="compute-plane"}} | cluster_id="{cluster_id!s}"'
        },
    )

    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        msg = f"checking loki output failed: {resp.json()}"
        raise RuntimeError(msg) from e

    json = resp.json()
    return len(json["data"]["result"]) != 0


def wait_for(f, timeout: int):
    start = datetime.now(timezone.utc)
    while datetime.now(timezone.utc) < start + timedelta(seconds=timeout):
        if f():
            return
        time.sleep(5)
    msg = f"Timed out waiting for output after {timeout} secs"
    raise RuntimeError(msg)


@pytest.mark.parametrize("aws_s3_uri", ["proxy_query.parquet"], indirect=True)
@pytest.mark.parametrize(
    "proxy_compute", [ComputeContextSpecsInput(instance_type="t3.micro")], indirect=True
)
def test_grafana_monitoring(proxy_compute: ComputeContext, aws_s3_uri: str) -> None:
    lf = pl.LazyFrame({"a": [1, 2, 3, 4, 5], "b": [9, 9, 9, 0, 0]})
    lf = lf.with_columns(pl.col("a").max().over("b").alias("ab_max"))

    _query = pc.spawn_blocking(lf, dst=aws_s3_uri, context=proxy_compute)
    result = pl.read_parquet(aws_s3_uri)
    assert_frame_equal(lf.collect(), result)

    assert proxy_compute._compute_id is not None  # to silence mypy
    wait_for(lambda: loki_output_available(proxy_compute._compute_id), timeout=60)
    wait_for(lambda: prometheus_output_available(proxy_compute._compute_id), timeout=60)
