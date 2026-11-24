"""A matrx-ai test that fires the size gate never reaches the HOST's durable sink.

Live 2026-10-11..17: ``tool_result_overflow:seo_site`` (a high / fix class on the ops-triage
board) held 13 events whose call ids were ``call-big`` / ``call-gate`` — the ids
``test_oversized_json_result_stays_valid_and_continuable.py`` uses. aidream's bootstrap
registers its ops-triage writer into ``matrx_ai.tools.result_gate._SINKS`` outside
``configure()``, so the host-seam isolation never restored it, and a package test run beside
aidream wrote test firings into the production ledger as a tool defect.

The pair below is order-dependent on purpose (the same shape as test_host_seam_isolation.py):
the first installs a host-style sink and leaves it, the second asserts the autouse restore
removed it. Remove ``_SINKS`` from ``_SEAMS`` and the second goes red.
"""

from __future__ import annotations

from matrx_ai.testing import host_isolation
from matrx_ai.tools import result_gate

_HOST_SINK_CALLS: list[object] = []


def _host_durable_sink(event: object) -> None:
    _HOST_SINK_CALLS.append(event)


def test_a_host_registers_its_durable_gate_sink() -> None:
    result_gate.register_tool_result_gate_sink(_host_durable_sink)
    assert _host_durable_sink in result_gate._SINKS


def test_the_next_package_test_does_not_see_it() -> None:
    assert _host_durable_sink not in result_gate._SINKS


def test_restore_is_by_content_and_the_baseline_is_a_copy() -> None:
    baseline = host_isolation.capture_baseline()
    held = result_gate._SINKS  # the object a host imported to check membership
    result_gate.register_tool_result_gate_sink(_host_durable_sink)
    assert _host_durable_sink not in baseline.values[("matrx_ai.tools.result_gate", "_SINKS")]
    host_isolation.restore_baseline(baseline)
    assert _host_durable_sink not in held
    assert result_gate._SINKS is held
