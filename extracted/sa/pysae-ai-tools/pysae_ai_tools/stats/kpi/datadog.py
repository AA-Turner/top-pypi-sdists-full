"""Datadog collectors: uptime SLO, p99 latency, 4XX/5XX error ratios, error budget burn.

All windows are unix-timestamp pairs ``(from_ts, to_ts)``. Queries target the
prod API service, consistent with the « Availability SLO for api service ».
"""

import datetime as dt

import httpx

from ...env.resolve import try_auto_resolve

DD_SITE = "datadoghq.eu"
API_SLO_ID = "c77fb31576955f2f81cee8a79d7d28cf"  # Availability SLO for api service
SLO_TARGET_PCT = 99.9
BASE_SCOPE = "env:prod,service:api*"


def client() -> httpx.Client:
    api_key = try_auto_resolve("DD_API_KEY")
    app_key = try_auto_resolve("DD_APP_KEY")
    if not api_key or not app_key:
        raise RuntimeError("DD keys not resolved — run `pysae-ai-tools env resolve DD_API_KEY DD_APP_KEY`")
    return httpx.Client(
        base_url=f"https://api.{DD_SITE}/api/v1",
        headers={"DD-API-KEY": api_key, "DD-APPLICATION-KEY": app_key},
        timeout=30,
    )


def quarter_start(day: dt.date) -> dt.date:
    """First day of the civil quarter containing ``day``."""
    return dt.date(day.year, 3 * ((day.month - 1) // 3) + 1, 1)


def budget_burn_pct(sli_pct: float, target_pct: float = SLO_TARGET_PCT) -> float:
    """Share of the error budget consumed, given the SLI over the budget window."""
    return round((100.0 - sli_pct) / (100.0 - target_pct) * 100.0, 1)


def slo_sli_pct(dd: httpx.Client, from_ts: int, to_ts: int) -> float:
    """Overall SLI (%) of the availability SLO over the window."""
    resp = dd.get(f"/slo/{API_SLO_ID}/history", params={"from_ts": from_ts, "to_ts": to_ts})
    resp.raise_for_status()
    sli = resp.json()["data"]["overall"]["sli_value"]
    return round(float(sli), 3)


def _query_point_values(dd: httpx.Client, query: str, from_ts: int, to_ts: int) -> list[float]:
    resp = dd.get("/query", params={"query": query, "from": from_ts, "to": to_ts})
    resp.raise_for_status()
    series = resp.json().get("series") or []
    return [point[1] for serie in series for point in (serie.get("pointlist") or []) if point[1] is not None]


def latency_p95_ms(dd: httpx.Client, from_ts: int, to_ts: int) -> float:
    """True p95 latency over the window, in milliseconds.

    Mirrors the « API, P95 ms, semaine passée » widget of the Dev Ops
    dashboard: request-weighted percentile over the whole window (v2 scalar
    query, ``aggregator: percentile``), NOT an average of per-interval p95
    points — that average over-weights low-traffic intervals and inflates
    the result several-fold. Trace metrics are in seconds — hence the ×1000.
    """
    body = {
        "data": {
            "type": "scalar_request",
            "attributes": {
                "from": from_ts * 1000,
                "to": to_ts * 1000,
                "queries": [
                    {
                        "data_source": "metrics",
                        "query": "p95:trace.fastapi.request{env:prod,service:api}",
                        "name": "q1",
                        "aggregator": "percentile",
                    }
                ],
                "formulas": [{"formula": "q1"}],
            },
        }
    }
    resp = dd.post(f"https://api.{DD_SITE}/api/v2/query/scalar", json=body)
    resp.raise_for_status()
    columns = resp.json()["data"]["attributes"]["columns"]
    values = [v for col in columns if col.get("type") != "group" for v in col.get("values", []) if v is not None]
    if not values:
        raise RuntimeError("empty p95 scalar response")
    return round(float(values[0]) * 1000.0, 2)


def error_ratios_pct(dd: httpx.Client, from_ts: int, to_ts: int) -> tuple[float, float]:
    """(4XX, 5XX) request ratios over the window, in percent."""
    total = sum(_query_point_values(dd, f"sum:trace.fastapi.request.hits{{{BASE_SCOPE}}}.as_count()", from_ts, to_ts))
    if not total:
        raise RuntimeError("empty hits series")
    ratios: list[float] = []
    for status_class in ("4*", "5*"):
        query = f"sum:trace.fastapi.request.hits{{{BASE_SCOPE},http.status_code:{status_class}}}.as_count()"
        ratios.append(round(sum(_query_point_values(dd, query, from_ts, to_ts)) / total * 100.0, 3))
    return ratios[0], ratios[1]
