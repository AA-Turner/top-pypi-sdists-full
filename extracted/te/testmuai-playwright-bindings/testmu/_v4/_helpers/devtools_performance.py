from __future__ import annotations

import dataclasses
import re

from .devtools_types import CoreWebVitals

_COLLECT_JS = "(() => window.__v16_perf)()"

# Non-CDP engines only: which vitals the engine's PerformanceObserver cannot
# measure (same feature detection as the runner's collector).
_UNSUPPORTED_JS = """() => {
  const t = (typeof PerformanceObserver !== "undefined" && PerformanceObserver.supportedEntryTypes) || [];
  const inp = typeof PerformanceEventTiming !== "undefined" && "interactionId" in PerformanceEventTiming.prototype;
  return [["LCP", t.includes("largest-contentful-paint")], ["CLS", t.includes("layout-shift")],
          ["INP", t.includes("event") && inp], ["FCP", t.includes("paint")],
          ["TTFB", t.includes("navigation")]].filter(p => !p[1]).map(p => p[0]);
}"""

# Metric -> the names query code reads it by (``perf.cls``, ``all()["lcp_ms"]``).
_VITAL_TOKENS: dict[str, tuple[str, ...]] = {
    "CLS": ("cls",),
    "LCP": ("lcp_ms", "lcp"),
    "FCP": ("fcp_ms", "fcp"),
    "INP": ("inp_ms", "inp"),
    "TTFB": ("ttfb_ms", "ttfb"),
}


def unsupported_metrics_message(code: str, cwv: CoreWebVitals, engine: str = "") -> str | None:
    """"CLS is not supported on firefox" when ``code`` reads a vital listed in
    ``cwv.unsupported``; None otherwise (always None on Chromium)."""
    unsupported = getattr(cwv, "unsupported", None) or []
    hit = [
        m for m in unsupported
        if isinstance(m, str)
        and any(re.search(rf"\b{t}\b", code or "") for t in _VITAL_TOKENS.get(m.upper(), (re.escape(m.lower()),)))
    ]
    if not hit:
        return None
    if not engine:
        from testmu._aria_perception import session_engine
        engine = session_engine()
    engine = engine if engine != "chromium" else "this browser"
    return f"{', '.join(hit)} {'is' if len(hit) == 1 else 'are'} not supported on {engine}"


def _build_cwv(raw: dict) -> CoreWebVitals:
    """Build CoreWebVitals from raw web-vitals metrics dict."""
    def _f(key: str) -> float | None:
        v = raw.get(key)
        return float(v) if v is not None else None
    return CoreWebVitals(
        lcp_ms=_f("lcp"),
        cls=_f("cls"),
        inp_ms=_f("inp"),
        fcp_ms=_f("fcp"),
        ttfb_ms=_f("ttfb"),
        unsupported=[m for m in (raw.get("unsupported") or []) if isinstance(m, str)],
    )


async def snapshotPerformanceTrace(page) -> CoreWebVitals:
    """Read window.__v16_perf and return CoreWebVitals.

    Called by:
    - Generated Playwright test code (codegen ABI)
    - the equivalent performance snapshot on the recording path
    """
    raw = await page.evaluate(_COLLECT_JS)
    cwv = _build_cwv(raw or {})
    if not cwv.unsupported:
        from testmu._v4._helpers._perception import perception_for
        unsupported = await perception_for(page).unsupported_vitals()
        if unsupported:
            cwv = dataclasses.replace(cwv, unsupported=unsupported)
    return cwv


async def _unsupported_vitals_portable(page) -> list[str]:
    """Firefox: the vitals this engine's PerformanceObserver can't measure."""
    try:
        unsupported = await page.evaluate(_UNSUPPORTED_JS)
    except Exception:  # noqa: BLE001 — best-effort; the vitals stand
        return []
    return [m for m in (unsupported or []) if isinstance(m, str)]


# ---------------------------------------------------------------------------
# Code-generation query path (matches cookies/network/console pattern)
# ---------------------------------------------------------------------------

import textwrap  # noqa: E402
import traceback  # noqa: E402
import concurrent.futures  # noqa: E402

import testmu._v4._helpers.devtools_network as _net  # noqa: E402
from testmu._v4._helpers.devtools_network import DevtoolsQueryResult  # noqa: E402


class _ReadOnlyPerfStore:
    """Query-only wrapper for CoreWebVitals in worker process."""

    def __init__(self, cwv: CoreWebVitals) -> None:
        self._cwv = cwv

    @property
    def lcp_ms(self) -> float | None:
        return self._cwv.lcp_ms

    @property
    def cls(self) -> float | None:
        return self._cwv.cls

    @property
    def inp_ms(self) -> float | None:
        return self._cwv.inp_ms

    @property
    def fcp_ms(self) -> float | None:
        return self._cwv.fcp_ms

    @property
    def ttfb_ms(self) -> float | None:
        return self._cwv.ttfb_ms

    @property
    def unsupported(self) -> list[str]:
        return list(getattr(self._cwv, "unsupported", None) or [])

    def all(self) -> dict:
        return {
            "lcp_ms": self._cwv.lcp_ms,
            "cls": self._cwv.cls,
            "inp_ms": self._cwv.inp_ms,
            "fcp_ms": self._cwv.fcp_ms,
            "ttfb_ms": self._cwv.ttfb_ms,
        }


def _run_perf_worker(code: str, cwv: CoreWebVitals) -> tuple[str, str]:
    import json, math, re
    store = _ReadOnlyPerfStore(cwv)
    wrapped = textwrap.dedent(f"""\
def __extract__():
{textwrap.indent(code, '    ')}

__result__ = __extract__()
""")
    try:
        ns: dict = {"json": json, "re": re, "math": math, "perf": store}
        exec(compile(wrapped, "<devtools-perf-extract>", "exec"), ns)
        raw = ns.get("__result__")
        return ("ok", str(raw) if raw is not None else "")
    except Exception:
        return ("err", traceback.format_exc())


def devtools_performance_query(
    code: str,
    cwv: CoreWebVitals,
    timeout_sec: float = 2.0,
    engine: str = "",
) -> DevtoolsQueryResult:
    """Execute LLM-generated code against CoreWebVitals. Shares pool with network/console."""
    unsupported_err = unsupported_metrics_message(code, cwv, engine)
    if unsupported_err:
        # Non-Chromium only: fail loud rather than read a silent None.
        return DevtoolsQueryResult(success=False, error=unsupported_err)
    try:
        future = _net._executor.submit(_run_perf_worker, code, cwv)
        tag, val = future.result(timeout=timeout_sec)
    except concurrent.futures.TimeoutError:
        _net._replace_executor()
        return DevtoolsQueryResult(success=False, error="Execution timeout: code exceeded time limit")
    except concurrent.futures.BrokenExecutor:
        _net._replace_executor()
        return DevtoolsQueryResult(success=False, error="Executor crashed — replaced")
    except Exception as exc:
        return DevtoolsQueryResult(success=False, error=str(exc))
    if tag == "ok":
        return DevtoolsQueryResult(success=True, value=val)
    return DevtoolsQueryResult(success=False, error=val)
