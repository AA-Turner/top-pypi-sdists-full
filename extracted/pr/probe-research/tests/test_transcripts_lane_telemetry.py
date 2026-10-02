"""The past-sessions lane's verdict: the other half of the import offer.

The folder lane has had a funnel since the wizard shipped. The lane beside it
in the same offer had none — it returns early from seven places, each rendering
as a short message the wizard prints and moves on from, so "session capture was
never paired", "there is nothing on this machine" and "the person read the
review and said no" were the same silence.

The outcome is named at each of those returns rather than inferred from the
prose, so a copy edit cannot quietly re-bucket an outcome.
"""

from __future__ import annotations

import pytest

from probe.cli import backfill_transcripts as bt
from probe.cli import capabilities, tui
from probe.cli import telemetry as tm


@pytest.fixture(autouse=True)
def hosted(monkeypatch):
    monkeypatch.setenv("PROBE_BASE_URL", "https://api.research.prbe.ai")
    monkeypatch.setenv("PROBE_TELEMETRY", "on")


@pytest.fixture(autouse=True)
def captured(monkeypatch):
    records: list[dict] = []
    monkeypatch.setattr(tm, "_sender", None)
    monkeypatch.setattr(tm, "_flush_registered", True)
    monkeypatch.setattr(tm._Sender, "start", lambda self: None)
    monkeypatch.setattr(tm._Sender, "put", lambda self, rec: records.append(rec))
    context = tm.TelemetryContext(
        session_id="wizardsession", via=tm.Via.WIZARD, invoked_by=tm.InvokedBy.HUMAN,
    )
    monkeypatch.setattr(tm, "_current", context)
    return records


def _summary(records):
    return next(
        record["properties"] for record in records
        if record["event"] == tm.EVENT_TRANSCRIPTS_SUMMARY
    )


def test_a_lane_with_no_sources_selected_says_so(captured):
    bt.run_lane(client=object(), interactive=False, sources=[])
    assert _summary(captured)["outcome"] == tm.TranscriptsOutcome.NO_SOURCES


def test_a_machine_that_never_paired_capture_is_not_a_machine_with_no_sessions(
    captured, monkeypatch,
):
    """Two different problems with two different fixes, and they used to be the
    same event: none."""
    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda s=None: None)
    monkeypatch.setattr(capabilities, "tap_plugin_dir", lambda s=None: None)
    bt.run_lane(client=object(), interactive=False, sources=[bt.CLAUDE])
    summary = _summary(captured)
    assert summary["outcome"] == tm.TranscriptsOutcome.NOT_PAIRED
    assert summary["unpaired"] == 1


def test_a_census_that_verified_nothing_reports_why(captured, monkeypatch):
    monkeypatch.setattr(
        capabilities, "resolved_capture_credential", lambda s=None: ("tok", "http://x"),
    )
    monkeypatch.setattr(capabilities, "capture_device_id", lambda s=None: "dev")
    monkeypatch.setattr(capabilities, "tap_plugin_dir", lambda s=None: None)
    monkeypatch.setattr(
        bt, "discover",
        lambda **kw: bt.Census(candidates=[], identity_unverified=3, identity_conflicts=1),
    )
    bt.run_lane(client=object(), interactive=False, sources=[bt.CLAUDE])
    summary = _summary(captured)
    assert summary["outcome"] == tm.TranscriptsOutcome.NO_CANDIDATES
    assert summary["identity_unverified"] == 3
    assert summary["identity_conflicts"] == 1


def test_a_lane_that_ran_to_completion_carries_what_it_looked_at(
    captured, monkeypatch, tmp_path,
):
    """A lane that RAN is not a lane that finished uploading -- but it is the
    one outcome where the counts mean something, so they ride it."""
    transcript = bt.Transcript(
        path=tmp_path / "s-1.jsonl", session_id="s-1", agent=bt.CLAUDE,
        cwd=None, size=10, mtime=0.0,
    )
    (tmp_path / "s-1.jsonl").write_text("{}\n")
    monkeypatch.setattr(
        capabilities, "resolved_capture_credential", lambda s=None: ("tok", "http://x"),
    )
    monkeypatch.setattr(capabilities, "capture_device_id", lambda s=None: "dev")
    monkeypatch.setattr(capabilities, "tap_plugin_dir", lambda s=None: None)
    monkeypatch.setattr(bt, "discover", lambda **kw: bt.Census(candidates=[transcript]))
    monkeypatch.setattr(
        bt.TranscriptLedger, "for_device",
        classmethod(lambda cls: bt.TranscriptLedger(tmp_path / "ledger.jsonl")),
    )
    monkeypatch.setattr(bt, "_execute_census", lambda census, **kw: ["Imported."])
    bt.run_lane(client=object(), interactive=False, sources=[bt.CLAUDE])
    summary = _summary(captured)
    assert summary["outcome"] == tm.TranscriptsOutcome.COMPLETED
    assert summary["candidates"] == 1
    assert summary["agents"] == 1
    assert summary["unpaired"] == 0


def test_a_crash_is_reported_and_still_a_crash(captured, monkeypatch):
    def explode(**kwargs):
        raise RuntimeError("census exploded")

    monkeypatch.setattr(bt, "_run_lane", explode)
    with pytest.raises(RuntimeError):
        bt.run_lane(client=object(), interactive=False)
    assert _summary(captured)["outcome"] == tm.TranscriptsOutcome.ERROR


def test_an_abort_is_separable_from_a_crash(captured, monkeypatch):
    def interrupt(**kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(bt, "_run_lane", interrupt)
    with pytest.raises(KeyboardInterrupt):
        bt.run_lane(client=object(), interactive=False)
    assert _summary(captured)["outcome"] == tm.TranscriptsOutcome.ABORTED


def test_the_lane_reports_under_the_wizard_session_that_opened_it(captured, monkeypatch):
    monkeypatch.setattr(bt, "_run_lane", lambda **kwargs: ["done"])
    bt.run_lane(client=object(), interactive=False)
    summary = _summary(captured)
    assert summary["session_id"] == "wizardsession" and summary["via"] == "wizard"


def test_exactly_one_summary_per_call(captured, monkeypatch):
    monkeypatch.setattr(bt, "_run_lane", lambda **kwargs: ["done"])
    bt.run_lane(client=object(), interactive=False)
    assert [record["event"] for record in captured].count(tm.EVENT_TRANSCRIPTS_SUMMARY) == 1


def test_a_back_out_is_not_an_outcome_the_funnel_counts_as_declining(captured, monkeypatch):
    def back(**kwargs):
        kwargs["summary"]["outcome"] = "back"
        return tui.BACK

    monkeypatch.setattr(bt, "_run_lane", back)
    assert bt.run_lane(client=object(), interactive=True) is tui.BACK
    assert _summary(captured)["outcome"] == tm.TranscriptsOutcome.BACK


def test_every_outcome_the_lane_names_is_a_declared_one():
    """The lane sets bare strings at each return; nothing else pins them to the
    enum the dashboards are built on."""
    import re
    from pathlib import Path

    source = Path(bt.__file__).read_text()
    named = set(re.findall(r'summary\["outcome"\] = "([a-z_]+)"', source))
    assert named, "the regex stopped matching the assignments"
    assert named <= {value.value for value in tm.TranscriptsOutcome}
