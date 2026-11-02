"""The event catalog (`probe.analytics.events`): every name is a wire value PostHog
destinations and insights key on, so the catalog may grow but never rename."""

from __future__ import annotations

import pytest

from probe import analytics
from probe.analytics import events

#: Every product event name the client sends, frozen when the catalog moved into
#: `probe.analytics` (restructure step 4). Add new events; never edit a value.
FROZEN = {
    "WIZARD_INVOKED": "wizard.invoked",
    "WIZARD_STARTED": "wizard.started",
    "WIZARD_ACTION_CHOSEN": "wizard.action_chosen",
    "WIZARD_CONFIGURE_STARTED": "wizard.configure_started",
    "WIZARD_SIGNED_IN": "wizard.signed_in",
    "WIZARD_CONFIGURE_COMPLETED": "wizard.configure_completed",
    "INTEGRATION_REINSTALL_STARTED": "wizard.integration_reinstall_started",
    "INTEGRATION_REINSTALL_COMPLETED": "wizard.integration_reinstall_completed",
    "BACKFILL_INVOKED": "backfill.invoked",
    "BACKFILL_STARTED": "backfill.started",
    "BACKFILL_SCANNED": "backfill.scanned",
    "BACKFILL_PLAN_READY": "backfill.plan_ready",
    "BACKFILL_APPROVED": "backfill.approved",
    "BACKFILL_SUMMARY": "backfill.summary",
    "WIZARD_INSTALL_SETTLED": "wizard.install_settled",
    "WIZARD_IMPORTS_CHOSEN": "wizard.imports_chosen",
    "WIZARD_ONBOARDING_COMPLETED": "wizard.onboarding_completed",
    "WIZARD_UNINSTALL_STARTED": "wizard.uninstall_started",
    "WIZARD_UNINSTALL_COMPLETED": "wizard.uninstall_completed",
    "WIZARD_SIGNED_OUT": "wizard.signed_out",
    "WIZARD_RECORDER_CHANGED": "wizard.recorder_changed",
    "TRANSCRIPTS_SUMMARY": "transcripts.summary",
    "IMPORT_JOB_ENQUEUED": "import_job.enqueued",
    "IMPORT_JOB_STALLED": "import_job.stalled",
    "IMPORT_JOB_FINISHED": "import_job.finished",
    "IMPORT_JOB_CLEARED": "import_job.cleared",
    "OUTBOX_DRAINED": "outbox.drained",
    "OUTBOX_STUCK": "outbox.stuck",
    "OUTBOX_RESCUED": "outbox.rescued",
    "OUTBOX_DISCARDED": "outbox.discarded",
    "OUTBOX_RESTORED": "outbox.restored",
    "OUTBOX_PAUSE_LIFTED": "outbox.pause_lifted",
    "CAPTURE_REPAIR_APPLIED": "capture.repair_applied",
    "SETTINGS_REMOTE_APPLIED": "settings.remote_applied",
    "DELIVERY_SUMMARY": "sdk.delivery.summary",
    "REPORT_UNDELIVERABLE": "service.report_undeliverable",
    "DAEMON_ERROR": "daemon.error",
    "SERVICE_STARTED": "service.started",
    "SERVICE_STATE": "service.state",
    "SERVICE_STOPPED": "service.stopped",
    "LIFEBOAT_ACTED": "lifeboat.acted",
    "MCP_TOOL_SERVED": "mcp.tool_served",
    "EXCEPTION": "$exception",
}


def test_no_event_was_renamed_or_dropped():
    catalog = {member.name: member.value for member in analytics.Event}
    assert {name: catalog.get(name) for name in FROZEN} == FROZEN


def test_each_event_constant_is_its_member():
    for member in analytics.Event:
        assert getattr(events, f"EVENT_{member.name}") == member
        assert str(member) == member.value  # what goes on the wire, on 3.10 too


def test_the_service_and_the_mcp_send_the_catalogs_names():
    from probe.mcp.delivery import accounting

    assert accounting.EVENT_TOOL_SERVED == analytics.Event.MCP_TOOL_SERVED
    assert {analytics.Event.SERVICE_STARTED, analytics.Event.SERVICE_STATE, analytics.Event.SERVICE_STOPPED,
            analytics.Event.LIFEBOAT_ACTED} == analytics.SERVICE_EVENTS


@pytest.fixture
def queued(monkeypatch):
    records: list[dict] = []
    monkeypatch.setenv("PROBE_TELEMETRY", "on")
    monkeypatch.setattr(analytics.sender, "_sender", None)
    monkeypatch.setattr(analytics.sender, "_flush_registered", True)  # keep atexit out of tests
    monkeypatch.setattr(analytics.sender._Sender, "start", lambda self: None)
    monkeypatch.setattr(analytics.sender._Sender, "put", lambda self, record: records.append(record))
    return records


def test_track_sends_under_the_ambient_context(monkeypatch, queued):
    monkeypatch.setattr(analytics.analytics, "_current", None)  # start() sets it; undone after
    context = analytics.TelemetryContext.start(
        via=analytics.Via.COMMAND, interactive=False, base_url="https://api.research.prbe.ai"
    )
    analytics.track(analytics.Event.OUTBOX_STUCK, pending=3)
    (record,) = queued
    assert record["event"] == "outbox.stuck" and type(record["event"]) is str
    assert record["properties"]["pending"] == 3
    assert record["properties"]["session_id"] == context.session_id


def test_track_without_a_context_sends_nothing(monkeypatch, queued):
    monkeypatch.setattr(analytics.analytics, "_current", None)
    analytics.track(analytics.Event.OUTBOX_STUCK, pending=3)
    assert queued == []
