"""Probe service API v1 never loses a name an older piece uses (plan A4, D22).

A session left open for two weeks (D4) runs the tap, hooks and pi code it
started with, and a desktop app is updated on its own schedule: each of them
speaks API v1 as it was when it shipped. So v1 only grows. The snapshot
(`fixtures/service_api_v1_contract.json`) is what R2 shipped; a name missing
from the current protocol fails here. Add to the snapshot when the API grows.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from probe.service import protocol as p

SNAPSHOT = json.loads((Path(__file__).parent / "fixtures" / "service_api_v1_contract.json").read_text())


def _consts(cls) -> set:
    return {v for k, v in vars(cls).items() if k.isupper() and isinstance(v, (str, int))}


CURRENT = {
    "methods": set(p.METHODS), "topics": set(p.TOPICS), "clients": set(p.CLIENTS), "modes": set(p.MODES),
    "actions": set(p.ACTIONS), "check_triggers": set(p.CHECK_TRIGGERS), "report_triggers": set(p.REPORT_TRIGGERS),
    "error_codes": _consts(p.ErrorCode), "refused_reasons": _consts(p.RefusedReason),
    "defer_reasons": _consts(p.DeferReason), "check_outcomes": _consts(p.CheckOutcome), "states": _consts(p.State),
    "worker_states": _consts(p.WorkerState),
    "stop_reasons": _consts(p.StopReason), "end_reasons": _consts(p.EndReason), "context_env": set(p.CONTEXT_ENV),
    "mailbox_parts": set(p.MAILBOX_PARTS),
    "receipt_fields": set(p.RECEIPT_FIELDS), "receipt_scope_fields": set(p.RECEIPT_SCOPE_FIELDS),
    "harness_receipt_fields": set(p.HARNESS_RECEIPT_FIELDS), "desktop_ops": _consts(p.DesktopOp),
    "busy_holders": _consts(p.BusyHolder),
    "background_states": _consts(p.BackgroundState), "background_refusals": set(p.BACKGROUND_REFUSALS),
    "caps": set(p.CAPS),
    # The desktop app's update check, decided by the service (`update.check_now`'s
    # `app`, `app.check`, `update.app_result`): what the app reads and sends.
    "step_states": _consts(p.StepState), "app_check_reasons": _consts(p.AppCheckReason),
    "app_results": set(p.APP_RESULTS), "app_step_outcomes": _consts(p.AppStepOutcome),
    "app_report_ignored": _consts(p.AppReportIgnored),
}


def test_every_app_result_is_listed():
    """`APP_RESULTS` names every `AppResult`: `update.app_result` takes exactly these."""
    assert set(p.APP_RESULTS) == _consts(p.AppResult)


def test_every_background_refusal_is_listed():
    """`BACKGROUND_REFUSALS` names every `BackgroundRefusal`: an SDK reads them all."""
    assert set(p.BACKGROUND_REFUSALS) == _consts(p.BackgroundRefusal)


def test_the_api_version_is_still_1():
    assert p.API_VERSION == SNAPSHOT["api"] == 1


@pytest.mark.parametrize("name", sorted(CURRENT))
def test_nothing_an_older_piece_uses_is_gone(name):
    missing = set(SNAPSHOT[name]) - CURRENT[name]
    assert not missing, f"API v1 {name} lost {sorted(missing)}: an older tap, app or CLI still sends or reads it"
