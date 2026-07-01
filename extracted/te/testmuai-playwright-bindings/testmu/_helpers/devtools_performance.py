from __future__ import annotations

from .devtools_types import CoreWebVitals

_COLLECT_JS = "(() => window.__v16_perf)()"


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
    )


async def snapshotPerformanceTrace(page) -> CoreWebVitals:
    """Read window.__v16_perf and return CoreWebVitals.

    Called by:
    - Generated Playwright test code (codegen ABI)
    - the equivalent performance snapshot on the recording path
    """
    raw = await page.evaluate(_COLLECT_JS)
    return _build_cwv(raw or {})


# ---------------------------------------------------------------------------
# Code-generation query path (matches cookies/network/console pattern)
# ---------------------------------------------------------------------------

import textwrap  # noqa: E402
import traceback  # noqa: E402
import concurrent.futures  # noqa: E402

import testmu._helpers.devtools_network as _net  # noqa: E402
from testmu._helpers.devtools_network import DevtoolsQueryResult  # noqa: E402


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
) -> DevtoolsQueryResult:
    """Execute LLM-generated code against CoreWebVitals. Shares pool with network/console."""
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
